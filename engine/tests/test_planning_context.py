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


    def test_model_derived_budget_is_optional_and_other_phase_limits_stay_frozen(self):
        manifest = RUNNER.read_json(self.run / "run-manifest.json")
        budgets = manifest["budgets"]
        self.assertEqual(budgets["max_prepared_context_tokens"], 80384 - 4096)
        self.assertEqual(budgets["max_planning_context_tokens"], 80384 - 4096 - 256)
        self.assertEqual(budgets["max_cumulative_input_tokens"],
            (2 * budgets["max_creative_step_count"] + budgets["max_analysis_step_count"]) * max(budgets["max_planning_context_tokens"], budgets["max_prepared_context_tokens"]))
        schema = RUNNER.definition_schema("runManifest")
        RUNNER.validate_json_schema(manifest, schema)
        del budgets["max_planning_context_tokens"]
        RUNNER.validate_json_schema(manifest, schema)
        self.assertEqual(RUNNER.prepared_context_limit(budgets, planning=True), budgets["max_prepared_context_tokens"])
        budgets["max_planning_context_tokens"] = 0
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_json_schema(manifest, schema)


    def test_legacy_and_nonplanning_requests_keep_the_original_cap(self):
        prompt = "x" * (49255 * 3)
        manifest = RUNNER.read_json(self.run / "run-manifest.json")
        manifest["budgets"]["max_prepared_context_tokens"] = 49152
        RUNNER.write_json(self.run / "run-manifest.json", manifest)
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
        original = "x" * 160000
        state = {"payload": {"accepted": original}, "values": {}}
        transport = mock.Mock(return_value=api_response("scene_slot_0001", text=True))
        schema = {"type": "string", "enum": ["scene_slot_0001"]}
        with mock.patch.object(RUNNER, "planning_core", return_value=None):
            value = RUNNER.planning_value(self.run, "architecture_core", state, ["accepted"], schema, "Fixture placement.", transport)
            replay = RUNNER.planning_value(self.run, "architecture_core", state, ["accepted"], schema, "Fixture placement.", transport)
        self.assertEqual(value, replay)
        transport.assert_called_once()
        request = transport.call_args.args[2]
        prompt = request["messages"][1]["content"]
        self.assertGreater(math.ceil(len(prompt.encode()) / 3), 49152)
        self.assertIn(original, prompt)
        self.assertGreaterEqual(request["max_tokens"], RUNNER.MIN_PLANNING_OUTPUT_TOKENS)
        self.assertLess(request["max_tokens"], 15000)

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
        self.assertGreaterEqual(request["max_tokens"], RUNNER.MIN_PLANNING_OUTPUT_TOKENS)
        self.assertLessEqual(request["max_tokens"] + RUNNER.estimated_prompt_tokens(request["messages"][1]["content"]) + 4096, 60000)
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


    def test_complete_renderer_retains_json_types_unicode_and_authored_whitespace(self):
        values = {"JSON": {"text": "λ — Keep  two spaces.\nKeep this line.", "tail": [1, 2, "last"]},
                  "EMPTY": [], "FALSE": False, "ZERO": 0, "NULL": None}
        plain = "  Frozen law keeps its spaces.\n\nAnd its last line.  "
        context = RUNNER.complete_context([("PLAIN", plain), *values.items()])
        self.assertEqual(section(context, "PLAIN"), plain + "\n\n")
        for label, value in values.items():
            self.assertEqual(json.loads(section(context, label)), value)
        self.assertIn("λ", context)


    def test_scoped_core_keeps_law_canon_and_complete_reference_catalogs(self):
        law = "Frozen law.\n\n  Keep  deliberate whitespace and λ.\nFinal required rule."
        with mock.patch.object(RUNNER, "instruction_profile", return_value=(law, {})):
            context = RUNNER.scoped_planning_context(self.run, "architecture_core", {"payload": self.payload}, [["arcs", 0]])
        self.assertEqual(context["frozen_law"], law)
        self.assertEqual(context["global_canon"]["work_canon"], self.records["genesis"]["work_canon"])
        self.assertEqual(context["committed_source_catalog"], RUNNER.genesis_reference_catalog(self.run))
        self.assertEqual(context["targets"][0]["retained_value"], self.payload["arcs"][0])
        self.assertIn(self.payload["arcs"][0], context["relevant_records"])


if __name__ == "__main__":
    unittest.main()
