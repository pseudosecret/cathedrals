"""Complete planning context fits model capacity without dropping distinct content."""

import copy
import json
import math
import re
import socket
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_cathedrals import ROOT, RUNNER, architecture_core_payload, architecture_genesis_records, packet_plan_annotation
from test_reference_resolution import api_response, planning_response


def section(context, label):
    body = context.split(f"===== {label} =====\n", 1)[1]
    return re.split(r"(?m)^===== [^\n]+ =====\n", body, maxsplit=1)[0]


class PlanningContextTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RUNNER.read_json(ROOT / "engine/tests/fixtures/initial-planning-context-overflow.json")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        with mock.patch.object(RUNNER, "RUNTIME_ROOT", self.root / ".cathedrals"), mock.patch.object(
            RUNNER, "RUNS_ROOT", self.root / ".cathedrals/runs"
        ):
            self.run = RUNNER.create_run(RUNNER.FrozenInputs(possible_scene_count=self.fixture["possible_scene_count"]),
                "http://offline.invalid", "offline", output_fn=lambda value: None,
                model_context_window_tokens=self.fixture["model_context_window_tokens"])
        self.records = architecture_genesis_records()
        for patch in (
            mock.patch.object(RUNNER, "committed_record", side_effect=lambda run, kind: self.records.get(kind)),
            mock.patch.object(RUNNER, "committed_records", return_value=[]),
            mock.patch.object(RUNNER, "_source_index", return_value={"commit_foundation": {}}),
            mock.patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")),
        ):
            patch.start()
            self.addCleanup(patch.stop)
        payload = architecture_core_payload()
        payload["arcs"] = [copy.deepcopy(payload["arcs"][0]) | {"arc_id": f"arc_{index}"} for index in range(self.fixture["arc_count"])]
        payload["obligation_graph"] += [copy.deepcopy(payload["obligation_graph"][0]) | {"obligation_id": f"debt_{index}"}
                                        for index in range(1, self.fixture["obligation_count"])]
        payload["attractors"] += [copy.deepcopy(payload["attractors"][0]) | {"attractor_id": f"attractor_{index}"}
                                  for index in range(1, self.fixture["attractor_count"])]
        self.core = RUNNER.build_architecture_core(self.run, payload)
        self.payload = payload
        self.pad(self.records["genesis"], self.fixture["genesis_compact_bytes"], 256)
        self.pad(self.core, self.fixture["core_compact_bytes"], 32)
        self.records["architecture_core"] = self.core
        self.batches = RUNNER.plan_batches(self.core)
        self.assignments = RUNNER.ensure_frozen_geomancy(self.run)["assignments"]

    def pad(self, value, size, count):
        value["synthetic_context"] = [{"note": "Synthetic metadata."} for _ in range(count)]
        value["padding"] = ""
        remaining = size - len(RUNNER.canonical_json(value))
        self.assertGreaterEqual(remaining, 0)
        value["padding"] = "x" * remaining
        self.assertEqual(len(RUNNER.canonical_json(value)), size)

    def setup_draft(self):
        fixture = RUNNER.read_json(ROOT / "engine/tests/fixtures/backward-setup-context-overflow.json")
        core = {key: value for key, value in self.core.items() if key not in {"padding", "synthetic_context"}}
        self.records["architecture_core"] = core
        self.pad(self.records["genesis"], fixture["genesis_compact_bytes"], 256)
        payload = copy.deepcopy(self.payload)
        self.pad(payload, fixture["draft_compact_bytes"], 32)
        specs = RUNNER.planned_packet_specs(core)
        annotations = [packet_plan_annotation(spec["packet_slot_id"]) for spec in specs]
        tasks = []
        for index in range(fixture["setup_count"]):
            task = {"kind": "authored_hint", "text": f"Synthetic hint {index}.",
                    "origin_step": "architecture_plan_batch_0001", "source_path": ["packet_plans", 2, "relevance", "keywords", index],
                    "payoff_packet": specs[-1]["packet_slot_id"]}
            if index < fixture["attached_count"]:
                task |= {"attached": True, "setup_slot_id": specs[0]["scene_slot_ids"][0],
                         "instruction": f"Fixture {index}: λ — Keep  two spaces.\n" + "x" * 580 + "  Last line.  "}
                annotations[0]["soft_guidance"].append(f"Setup in {task['setup_slot_id']} for authored hint: {task['instruction']}")
            tasks.append(task)
        batch = RUNNER.build_architecture_plan_batch(self.run, {"packet_plans": annotations}, specs, 1, 1)
        self.pad(batch, fixture["plan_batch_compact_bytes"], 32)
        RUNNER.save_planning_draft(self.run, "architecture_plan_batch_0001", {
            "record": batch, "payload": {"packet_plans": annotations}, "hints": []})
        state = {"payload": payload, "record": core, "values": {}, "hints": [], "unassigned": [],
                 "setups": tasks, "setups_collected": True}
        context = RUNNER.planning_context(self.run, "architecture_core", state) | {"backward_setups": tasks}
        padding = len(payload["padding"]) + fixture["compact_context_bytes"] - len(RUNNER.canonical_json(context))
        self.assertGreaterEqual(padding, 0)
        payload["padding"] = "x" * padding
        RUNNER.save_planning_draft(self.run, "architecture_core", state)
        return state, batch

    def test_model_derived_budget_is_optional_and_other_phase_limits_stay_frozen(self):
        manifest = RUNNER.read_json(self.run / "run-manifest.json")
        budgets = manifest["budgets"]
        self.assertEqual(budgets["max_prepared_context_tokens"], 49152)
        self.assertEqual(budgets["max_planning_context_tokens"], 80384 - 4096 - 256)
        self.assertEqual(budgets["max_cumulative_input_tokens"],
            (2 * budgets["max_creative_step_count"] + budgets["max_analysis_step_count"]) * budgets["max_planning_context_tokens"])
        schema = RUNNER.definition_schema("runManifest")
        RUNNER.validate_json_schema(manifest, schema)
        del budgets["max_planning_context_tokens"]
        RUNNER.validate_json_schema(manifest, schema)
        self.assertEqual(RUNNER.prepared_context_limit(budgets, planning=True), 49152)
        budgets["max_planning_context_tokens"] = 0
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_json_schema(manifest, schema)

    def test_initial_request_above_legacy_cap_retains_output_and_safety_headroom(self):
        prompt = "x" * (49255 * 3)
        transport = mock.Mock(return_value=api_response({"kept": True}))
        schema = {"type": "object", "required": ["kept"], "properties": {"kept": {"type": "boolean"}}}
        state = RUNNER.staged_planning_request(self.run, "architecture_core", prompt, "full context", schema, transport)
        self.assertEqual(state["payload"], {"kept": True})
        request = transport.call_args.args[2]
        self.assertEqual(request["messages"][1]["content"], prompt)
        self.assertEqual(request["max_tokens"], RUNNER.EXPANDED_OUTPUT_TOKENS)
        self.assertLessEqual(49255 + request["max_tokens"] + 4096, 80384)

    def test_legacy_and_nonplanning_requests_keep_the_original_cap(self):
        prompt = "x" * (49255 * 3)
        manifest = RUNNER.read_json(self.run / "run-manifest.json")
        transport = mock.Mock(side_effect=AssertionError("request exceeds its frozen phase budget"))
        for planning, purpose in ((False, "planning"), (True, "semantic normalization"), (True, "planning")):
            with self.subTest(planning=planning, purpose=purpose):
                if planning and purpose == "planning":
                    del manifest["budgets"]["max_planning_context_tokens"]
                    RUNNER.write_json(self.run / "run-manifest.json", manifest)
                with self.assertRaises(RUNNER.CathedralsError):
                    RUNNER.request_architecture_analysis(self.run, "over_phase_limit", prompt, {"type": "string"}, transport,
                        planning_mode=planning, context_purpose=purpose)
        transport.assert_not_called()

    def test_large_value_request_keeps_full_context_and_accepted_value_on_replay(self):
        state = {"payload": {"accepted": "x" * 95000}, "values": {}}
        transport = mock.Mock(return_value=api_response("scene_slot_0001", text=True))
        schema = {"type": "string", "enum": ["scene_slot_0001"]}
        with mock.patch.object(RUNNER, "planning_core", return_value=None):
            value = RUNNER.planning_value(self.run, "architecture_core", state, ["missing"], schema, "Fixture placement.", transport)
            replay = RUNNER.planning_value(self.run, "architecture_core", state, ["missing"], schema, "Fixture placement.", transport)
        self.assertEqual(value, replay)
        transport.assert_called_once()
        request = transport.call_args.args[2]
        prompt = request["messages"][1]["content"]
        self.assertGreater(math.ceil(len(prompt.encode()) / 3), 49152)
        self.assertIn(state["payload"]["accepted"], prompt)
        self.assertEqual(request["max_tokens"], 15000)

    def test_loaded_window_and_frozen_planning_ceiling_both_limit_requests(self):
        state = RUNNER.load_state(self.run)
        schema = {"type": "string"}
        transport = mock.Mock(return_value=api_response("accepted", text=True))
        state["model_context_window_tokens"] = 60000
        RUNNER.save_state(self.run, state)
        value, _ = RUNNER.request_architecture_analysis(self.run, "loaded_headroom", "x" * (50000 * 3), schema,
            transport, value_mode=True, planning_mode=True)
        self.assertEqual(value, "accepted")
        request = transport.call_args.args[2]
        self.assertEqual(request["max_tokens"], 60000 - 50000 - 4096)
        state["model_context_window_tokens"] = 49255 + 4096 + 255
        RUNNER.save_state(self.run, state)
        with self.assertRaises(RUNNER.PausedError):
            RUNNER.request_architecture_analysis(self.run, "too_small_loaded_window", "x" * (49255 * 3), schema,
                transport, value_mode=True, planning_mode=True)
        state["model_context_window_tokens"] = 100000
        RUNNER.save_state(self.run, state)
        with self.assertRaises(RUNNER.PausedError) as raised:
            RUNNER.request_architecture_analysis(self.run, "frozen_ceiling", "x" * ((80384 - 4096 - 256 + 1) * 3), schema,
                transport, value_mode=True, planning_mode=True)
        self.assertIn("76,032", raised.exception.reason)
        self.assertEqual(transport.call_count, 1)

    def test_completed_setups_reference_exact_guidance_without_changing_saved_content(self):
        state, _ = self.setup_draft()
        checkpoint = self.run / ".staging/architecture_core.planning.json"
        saved = checkpoint.read_bytes()
        original = copy.deepcopy(state)
        context = RUNNER.planning_context(self.run, "architecture_core", state)
        for original_task, rendered in zip(state["setups"][:12], context["backward_setups"][:12]):
            guidance = context
            for part in rendered["instruction_ref"].removeprefix("/").split("/"):
                guidance = guidance[int(part) if isinstance(guidance, list) else part]
            self.assertEqual(guidance, f"Setup in {original_task['setup_slot_id']} for authored hint: {original_task['instruction']}")
            self.assertEqual({key: value for key, value in rendered.items() if key != "instruction_ref"},
                             {key: value for key, value in original_task.items() if key != "instruction"})
        self.assertEqual(context["backward_setups"][12:], state["setups"][12:])
        self.assertEqual(state, original)
        self.assertEqual(checkpoint.read_bytes(), saved)
        full = context | {"backward_setups": state["setups"]}
        self.assertEqual(len(RUNNER.canonical_json(full)), 146674)
        self.assertGreater(len(RUNNER.canonical_json(full)) - len(RUNNER.canonical_json(context)), 6000)

    def test_unmatched_ambiguous_and_pending_instructions_remain_complete(self):
        state, batch = self.setup_draft()
        for mode in ("missing", "ambiguous", "pending", "changed"):
            with self.subTest(mode=mode):
                candidate = copy.deepcopy(state)
                record = copy.deepcopy(batch)
                guidance = record["packet_plans"][0]["soft_guidance"]
                if mode == "missing":
                    del guidance[1]
                elif mode == "ambiguous":
                    guidance.append(guidance[1])
                elif mode == "pending":
                    candidate["setups"][0]["attached"] = False
                else:
                    guidance[1] += "changed"
                with mock.patch.object(RUNNER, "planning_batches_view", return_value=[record]):
                    context = RUNNER.planning_context(self.run, "architecture_core", candidate)
                self.assertEqual(context["backward_setups"][0], candidate["setups"][0])

    def test_saved_setup_sizes_continue_in_batches_and_resume_without_repeating_work(self):
        state, batch = self.setup_draft()
        original = copy.deepcopy(state)
        calls = []
        def transport(_method, _url, request, **kwargs):
            calls.append(request)
            def resolve(path, node):
                self.assertEqual(path[0], "$setups")
                self.assertGreaterEqual(path[1], 12)
                return {"setup_slot_id": "scene_slot_0001", "instruction": f"Setup {path[1]}: " + "x" * 600}
            return planning_response(request, resolve)
        RUNNER.place_planning_setups(self.run, state["record"], [batch], transport)
        complete = RUNNER.read_json(self.run / ".staging/architecture_core.planning.json")
        self.assertTrue(complete["setups_complete"])
        self.assertTrue(all(task["attached"] for task in complete["setups"]))
        self.assertEqual(complete["setups"][:12], original["setups"][:12])
        self.assertEqual(complete["payload"], original["payload"])
        self.assertEqual(len(calls), 2)
        for request in calls:
            self.assertIn("BATCH TARGETS\n", request["messages"][1]["content"])
            self.assertEqual(request["max_tokens"], 8192)
            self.assertLessEqual(math.ceil(len(request["messages"][1]["content"].encode()) / 3) + request["max_tokens"] + 4096, 80384)
        RUNNER.place_planning_setups(self.run, complete["record"], RUNNER.planning_batches_view(self.run),
            mock.Mock(side_effect=AssertionError("repeated setup generation")))
        self.assertFalse(RUNNER.committed_records(self.run, "architecture_core"))

    def test_complete_renderer_retains_json_types_unicode_and_authored_whitespace(self):
        values = {"JSON": {"text": "λ — Keep  two spaces.\nKeep this line.", "tail": [1, 2, "last"]},
                  "EMPTY": [], "FALSE": False, "ZERO": 0, "NULL": None}
        plain = "  Frozen law keeps its spaces.\n\nAnd its last line.  "
        context = RUNNER.complete_context([("PLAIN", plain), *values.items()])
        self.assertEqual(section(context, "PLAIN"), plain + "\n\n")
        for label, value in values.items():
            self.assertEqual(json.loads(section(context, label)), value)
        self.assertIn("λ", context)

    def test_large_initial_batch_retains_all_inputs_and_passes_existing_guard(self):
        prompt, context = RUNNER.architecture_plan_prompt(self.run, self.batches[0], 1, len(self.batches))
        self.assertEqual(json.loads(section(context, "IMMUTABLE GENESIS")), self.records["genesis"])
        self.assertEqual(json.loads(section(context, "VALIDATED STAGED ARCHITECTURE CORE")), self.core)
        self.assertEqual(json.loads(section(context, "PRIOR STAGED PACKET IDS")), [])
        assignments = json.loads(section(context, "THIS BATCH THRESHOLD GEOMANCY"))
        self.assertEqual(assignments, self.assignments)
        self.assertEqual(len(assignments), self.fixture["required_geomancy_assignments"])
        self.assertGreater(len(assignments), self.fixture["previously_rendered_geomancy_assignments"])
        allocation = json.loads(prompt.split("THIS BATCH'S EXACT ALLOCATIONS BEGIN\n\n", 1)[1].split("\n\nTHIS BATCH'S EXACT ALLOCATIONS END", 1)[0])
        self.assertEqual(allocation["packet_allocations"], self.batches[0])
        tokens = math.ceil(len(prompt.encode()) / 3)
        self.assertLess(tokens, self.fixture["max_prepared_context_tokens"])
        schema = RUNNER.architecture_plan_batch_schema(self.run, self.batches[0])
        payload = {"packet_plans": [packet_plan_annotation(spec["packet_slot_id"]) for spec in self.batches[0]]}
        transport = mock.Mock(return_value=api_response(payload))
        state = RUNNER.staged_planning_request(self.run, "architecture_plan_batch_0001", prompt, context, schema, transport)
        self.assertFalse(state["bulk_failed"])
        transport.assert_called_once()
        request = transport.call_args.args[2]
        self.assertEqual(request["messages"][1]["content"], prompt)
        self.assertEqual(request["max_tokens"], self.fixture["requested_output_tokens"])
        self.assertLessEqual(tokens + request["max_tokens"] + self.fixture["context_safety_reserve_tokens"], self.fixture["model_context_window_tokens"])
        self.assertEqual(RUNNER.read_json(self.run / "run-manifest.json")["budgets"]["max_prepared_context_tokens"], 49152)

    def test_initial_core_retains_law_manifest_and_complete_reference_catalogs(self):
        law = "Frozen law.\n\n  Keep  deliberate whitespace and λ.\nFinal required rule."
        with mock.patch.object(RUNNER, "engine_context", return_value=law):
            prompt, context = RUNNER.architecture_core_prompt(self.run)
        self.assertIn(law, context)
        self.assertEqual(json.loads(section(context, "FROZEN RUN MANIFEST")), RUNNER.read_json(self.run / "run-manifest.json"))
        self.assertEqual(json.loads(section(context, "IMMUTABLE GENESIS")), self.records["genesis"])
        catalog = RUNNER.genesis_reference_catalog(self.run)
        self.assertEqual(json.loads(section(context, "ALLOWED GENESIS CLAIMANTS")), [catalog["claimant_01"]])
        self.assertEqual(json.loads(section(context, "ALLOWED COMMITTED SOURCES")), [catalog["commit_foundation"]])
        self.assertIn("Final required rule.", prompt)

    def test_prior_packet_ids_are_preserved_in_order(self):
        prior = ["packet_first", "packet_last"]
        with mock.patch.object(RUNNER, "planning_batches_view", return_value=[
            {"batch_sequence": 1, "packet_plans": [{"packet_slot_id": key} for key in prior]},
            {"batch_sequence": 3, "packet_plans": [{"packet_slot_id": "future_packet"}]},
        ]):
            _, context = RUNNER.architecture_plan_prompt(self.run, self.batches[0], 2, 3)
        self.assertEqual(json.loads(section(context, "PRIOR STAGED PACKET IDS")), prior)

    def test_oversized_core_keeps_last_required_catalog_entry_and_pauses_before_post(self):
        catalog = RUNNER.genesis_reference_catalog(self.run)
        catalog["last_source"] = "λ" * 100000 + " LAST REQUIRED SOURCE"
        with mock.patch.object(RUNNER, "genesis_reference_catalog", return_value=catalog), mock.patch.object(
            RUNNER, "_source_index", return_value={"commit_foundation": {}, "last_source": {}}
        ):
            prompt, context = RUNNER.architecture_core_prompt(self.run)
        self.assertEqual(json.loads(section(context, "ALLOWED COMMITTED SOURCES"))[-1], catalog["last_source"])
        transport = mock.Mock(side_effect=AssertionError("oversized request posted"))
        with self.assertRaises(RUNNER.PausedError):
            RUNNER.staged_planning_request(self.run, "architecture_core", prompt, context,
                RUNNER.definition_schema("architectureCorePayload"), transport)
        transport.assert_not_called()
        self.assertFalse((self.run / "finalization.json").exists())

    def test_oversized_batch_does_not_omit_core_or_change_accepted_checkpoint(self):
        self.core["padding"] += "λ" * 100000
        checkpoint = self.run / ".staging/architecture_core.planning.json"
        RUNNER.write_json(checkpoint, {"record": self.core, "ready": True})
        original = checkpoint.read_bytes()
        prompt, context = RUNNER.architecture_plan_prompt(self.run, self.batches[0], 1, len(self.batches))
        self.assertEqual(json.loads(section(context, "VALIDATED STAGED ARCHITECTURE CORE")), self.core)
        self.assertEqual(json.loads(section(context, "THIS BATCH THRESHOLD GEOMANCY")), self.assignments)
        transport = mock.Mock(side_effect=AssertionError("oversized request posted"))
        with self.assertRaises(RUNNER.PausedError) as raised:
            RUNNER.staged_planning_request(self.run, "architecture_plan_batch_0001", prompt, context,
                RUNNER.architecture_plan_batch_schema(self.run, self.batches[0]), transport)
        self.assertEqual(raised.exception.failure_class, "budget_exhaustion")
        self.assertIn(str(math.ceil(len(prompt.encode()) / 3)), raised.exception.reason.replace(",", ""))
        transport.assert_not_called()
        self.assertEqual(checkpoint.read_bytes(), original)
        self.assertFalse((self.run / "finalization.json").exists())


if __name__ == "__main__":
    unittest.main()
