"""Planning recovery uses bounded values, real catalogs, and complete draft context."""

import copy
import json
import re
import socket
import unittest
from unittest import mock

from test_cathedrals import ROOT, RUNNER, architecture_core_payload, architecture_genesis_records, packet_plan_annotation
import test_reference_resolution as reference_fixtures

api_response = reference_fixtures.api_response


class PlanningRecoveryTests(unittest.TestCase):
    def setUp(self):
        reference_fixtures.ReferenceResolutionTests.setUp(self)
        self.records = architecture_genesis_records()
        for patch in (
            mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: self.records.get(kind)),
            mock.patch.object(RUNNER, "committed_records", return_value=[]),
            mock.patch.object(RUNNER, "_source_index", return_value={"commit_foundation": {}}),
            mock.patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")),
        ):
            patch.start()
            self.addCleanup(patch.stop)

    def state(self, payload):
        return {"payload": copy.deepcopy(payload), "values": {}, "hints": [], "unassigned": []}

    def core(self):
        value = architecture_core_payload()
        value["arcs"] = [copy.deepcopy(value["arcs"][0]) | {"arc_id": f"arc_{i:03d}"} for i in range(1, 5)]
        return value

    def test_saved_failure_recognizes_every_allocated_slot_without_asking_model(self):
        fixture = RUNNER.read_json(ROOT / "engine/tests/fixtures/plan-slot-reference-failure.json")
        core = RUNNER.build_architecture_core(self.run, self.core())
        core["scope_commitment"] |= fixture["scope_commitment"]
        core["attractors"] = [copy.deepcopy(core["attractors"][0]) | {"attractor_id": f"attractor_{i:03d}"} for i in range(1, 6)]
        core["arcs"] = [copy.deepcopy(core["arcs"][0]) | {"arc_id": f"arc_{i:03d}"} for i in range(1, 8)]
        self.records["architecture_core"] = core
        self.records["genesis"]["claimants"] = [{"claimant_id": f"claimant_{i:02d}", "technical_slot_id": f"claimant_slot_{i:02d}"} for i in range(1, 7)]
        self.records["genesis_cast"] = {"characters": [{"character_id": f"character_{i:03d}", "technical_slot_id": f"character_slot_{i:03d}"} for i in range(1, 5)]}
        payload = {"packet_plans": [packet_plan_annotation(item["packet_slot_id"], relevance=item["relevance"]) for item in fixture["annotations"]]}
        read_state_map = RUNNER._read_state_map
        with mock.patch.object(RUNNER, "_read_state_map", side_effect=lambda run, name: {identifier: {} for identifier in fixture["motif_aliases"].values()} if name == "motifs.json" else read_state_map(run, name)):
            issues = RUNNER.named_reference_issues(self.run, payload, "architecturePlanBatchPayload", specs=RUNNER.planned_packet_specs(core))
            self.assertFalse(any(item["kind"] == "technical slot" for item in issues))
            self.assertEqual(len(issues), 8)
            self.assertEqual({item["kind"] for item in issues}, {"state variable"})
            state = self.state(payload)
            transport = mock.Mock(return_value=api_response("__NARRATIVE_HINT__", text=True))
            RUNNER.repair_planning_references(self.run, "architecture_plan_batch_0001", state,
                RUNNER.architecture_plan_batch_schema(self.run, RUNNER.planned_packet_specs(core)), transport,
                specs=RUNNER.planned_packet_specs(core))
            self.assertEqual(transport.call_count, 8)
            self.assertEqual(len(state["hints"]), 8)
            self.assertEqual(RUNNER.named_reference_issues(self.run, state["payload"], "architecturePlanBatchPayload", specs=RUNNER.planned_packet_specs(core)), [])
        self.assertIn("scene_slot_0001", state["payload"]["packet_plans"][0]["relevance"]["technical_slot_ids"])

    def test_motif_event_identity_uses_recorded_alias_without_model_guess(self):
        fixture = RUNNER.read_json(ROOT / "engine/tests/fixtures/plan-slot-reference-failure.json")
        events = [{"motif_event_id": key, "motif_id": value} for key, value in fixture["motif_aliases"].items()]
        payload = {"packet_plans": [{"relevance": {"motif_ids": fixture["original_motif_references"]}}]}
        audit = []
        with mock.patch.object(RUNNER, "all_committed_records", return_value=[{"constraint_delta": {"motif_events": events}}]):
            normalized = RUNNER.canonical_planning_aliases(self.run, payload, audit)
        self.assertEqual(normalized["packet_plans"][0]["relevance"]["motif_ids"], ["lipstick_mark_on_glass", "lamp_cross_legged_at_317"])
        self.assertEqual(len(audit), 2)
        self.assertEqual(payload["packet_plans"][0]["relevance"]["motif_ids"], fixture["original_motif_references"])

    def test_failed_large_json_switches_to_values_and_retains_complete_members(self):
        self.records["architecture_core"] = RUNNER.build_architecture_core(self.run, self.core())
        schema = {"type": "object", "required": ["accepted", "missing"], "properties": {
            "accepted": {"type": "string"}, "missing": {"type": "integer"}}, "additionalProperties": False}
        transport = mock.Mock(side_effect=[api_response('{"accepted":"keep me", "missing":', text=True), api_response(0)])
        state = RUNNER.staged_planning_request(self.run, "architecture_plan_batch_test", "initial prompt", "context", schema, transport)
        self.assertEqual(state["payload"], {"accepted": "keep me"})
        RUNNER.fill_planning_shape(self.run, "architecture_plan_batch_test", state, schema, transport)
        self.assertEqual(state["payload"], {"accepted": "keep me", "missing": 0})
        prompt = transport.call_args.args[2]["messages"][1]["content"]
        self.assertIn('"accepted": "keep me"', prompt)
        self.assertIn("$.missing", prompt)
        self.assertNotIn("complete corrected payload", prompt)
        self.assertEqual(transport.call_count, 2)
        self.assertTrue(state["bulk_failed"])

    def test_false_zero_and_empty_list_are_values_not_missing_fields(self):
        for value, schema in ((False, {"type": "boolean"}), (0, {"type": "integer"}), ([], {"type": "array"})):
            with self.subTest(value=value):
                state = self.state({"anchor": "whole draft"})
                transport = mock.Mock(return_value=api_response(value))
                result = RUNNER.planning_value(self.run, "architecture_core", state, ["field"], schema, "synthetic", transport)
                self.assertEqual(result, value)
                self.assertEqual(RUNNER.planning_value(self.run, "architecture_core", state, ["field"], schema, "synthetic", mock.Mock(side_effect=AssertionError("repeated"))), value)
                self.assertEqual(transport.call_count, 1)

    def test_interrupted_initial_draft_pauses_then_resumes_only_missing_values(self):
        schema = {"type": "object", "required": ["accepted", "missing"], "properties": {
            "accepted": {"type": "string"}, "missing": {"type": "integer"}}, "additionalProperties": False}
        response = api_response('{"accepted":"keep me", "missing":', text=True)
        transport = mock.Mock(side_effect=RUNNER.IncompleteResponseError("synthetic interruption", response))
        with self.assertRaises(RUNNER.PausedError):
            RUNNER.staged_planning_request(self.run, "architecture_core", "prompt", "context", schema, transport)
        transport.assert_called_once()
        raw = self.run / "raw/architecture_core-attempt1.api.json"
        original = raw.read_bytes()
        self.assertFalse(RUNNER.read_json(raw)["_cathedrals_stream_complete"])
        forbidden = mock.Mock(side_effect=AssertionError("repeated broad request"))
        state = RUNNER.staged_planning_request(self.run, "architecture_core", "prompt", "context", schema, forbidden)
        self.assertEqual(state["payload"], {"accepted": "keep me"})
        self.records["architecture_core"] = RUNNER.build_architecture_core(self.run, self.core())
        RUNNER.fill_planning_shape(self.run, "generic_planning_test", state, schema,
                                  lambda *a, **kw: api_response(0))
        self.assertEqual(state["payload"], {"accepted": "keep me", "missing": 0})
        self.assertEqual(raw.read_bytes(), original)
        self.assertEqual(RUNNER.ledger_entries(self.run)[-1]["failure_class"], "provider_incomplete_response")

    def test_truncated_core_is_assembled_from_values_in_backward_order(self):
        desired = self.core()
        desired["topology"]["nodes"].pop()
        replacements = {}
        for group, identity in (("attractors", "attractor_id"), ("obligation_graph", "obligation_id"), ("arcs", "arc_id")):
            for index, item in enumerate(desired[group], 1):
                replacements[item[identity]] = f"draft_{identity[:-3]}_{index:03d}"
        for group, identity in (("nodes", "node_id"), ("edges", "edge_id")):
            for index, item in enumerate(desired["topology"][group], 1):
                replacements[item[identity]] = f"draft_{identity[:-3]}_{index:03d}"
        def remap(value):
            if isinstance(value, dict):
                return {key: remap(item) for key, item in value.items()}
            if isinstance(value, list):
                return [remap(item) for item in value]
            return replacements.get(value, value)
        desired = remap(desired)
        paths = []
        def transport(_method, _url, request, **kwargs):
            prompt = request["messages"][1]["content"]
            if "FIELD PATH\n" not in prompt:
                response = api_response('{"saturation_rationale":"keep me", "attractors":[', text=True)
                response["choices"][0]["finish_reason"] = "length"
                return response
            path = prompt.split("FIELD PATH\n", 1)[1].split("\n", 1)[0]
            paths.append(path)
            value = desired
            for component, index, quoted in re.findall(r'\.([A-Za-z_][A-Za-z0-9_]*)|\[(\d+)\]|\[("[^\"]*")\]', path):
                component = json.loads(quoted) if quoted else component
                value = len(value) if component == "$count" else value[int(index)] if index else value[component]
            return api_response(value, text=isinstance(value, str))
        with mock.patch.object(RUNNER, "architecture_core_prompt", return_value=("prompt", "context")):
            core = RUNNER.prepare_core_draft(self.run, transport)
        self.assertEqual(core["scope_commitment"]["saturation_rationale"], "keep me")
        self.assertEqual(len(core["arcs"]), 4)
        self.assertLess(paths.index("$.attractors[0].terminal_transformation"), paths.index("$.obligation_graph[0].description"))
        state = RUNNER.read_json(self.run / ".staging/architecture_core.planning.json")
        self.assertTrue(state["ready"])
        self.assertTrue(state["bulk_failed"])

    def test_backward_setup_pause_commits_nothing_and_resume_keeps_accepted_placement(self):
        core_payload = self.core()
        core_payload["topology"]["nodes"].pop()
        commits, calls = [], []
        stopped = False
        def transport(_method, _url, request, **kwargs):
            nonlocal stopped
            prompt = request["messages"][1]["content"]
            name = request.get("response_format", {}).get("json_schema", {}).get("name")
            if name == "architectureCorePayload":
                calls.append(name)
                return api_response(core_payload)
            if name == "architecturePlanBatchPayload":
                calls.append(name)
                core = RUNNER.planning_core(self.run)
                return api_response({"packet_plans": [packet_plan_annotation(spec["packet_slot_id"],
                    attractor_ids=[core["attractors"][0]["attractor_id"]] if spec["packet_kind"] == "ending" else [])
                    for spec in RUNNER.planned_packet_specs(core)]})
            self.assertFalse(commits, "Planning committed before all setups were accepted")
            path = prompt.split("FIELD PATH\n", 1)[1].split("\n", 1)[0]
            calls.append(path)
            schema = json.loads(prompt.split("VALUE SCHEMA\n", 1)[1].split("\nFULL ASSEMBLED", 1)[0])
            if path.endswith("setup_slot_id"):
                return api_response(schema["enum"][0], text=True)
            if not stopped:
                stopped = True
                raise RUNNER.IncompleteResponseError("synthetic setup interruption", api_response("partial", text=True))
            return api_response("Synthetic coherent earlier setup.", text=True)
        def commit(_run, record, _raw, response, **kwargs):
            draft = RUNNER.read_json(self.run / ".staging/architecture_core.planning.json")
            self.assertTrue(draft["setups_complete"])
            commits.append(record)
        with mock.patch.object(RUNNER, "architecture_core_prompt", return_value=("prompt", "context")), mock.patch.object(
            RUNNER, "commit_record", side_effect=commit
        ):
            with self.assertRaises(RUNNER.PausedError):
                RUNNER.execute_planning_phases(self.run, transport)
            self.assertFalse(commits)
            state = RUNNER.read_json(self.run / ".staging/architecture_core.planning.json")
            self.assertEqual(state["setups"][0]["setup_slot_id"], "scene_slot_0001")
            self.assertNotIn("instruction", state["setups"][0])
            RUNNER.execute_planning_phases(self.run, transport)
        self.assertEqual(calls.count("architectureCorePayload"), 1)
        self.assertEqual(calls.count("architecturePlanBatchPayload"), 1)
        self.assertEqual(calls.count(RUNNER.reference_path(["$setups", 0, "setup_slot_id"])), 1)
        self.assertEqual(len(commits), 2)
        plans = commits[1]["packet_plans"]
        self.assertTrue(any("Setup in scene_slot_0001" in text for text in plans[0]["soft_guidance"]))
        for plan in plans:
            if plan["packet_kind"] == "ending":
                self.assertIn(plans[0]["packet_slot_id"], plan["depends_on_packet_slot_ids"])

    def test_plan_dependencies_use_only_earlier_staged_batches(self):
        core = RUNNER.build_architecture_core(self.run, self.core())
        self.records["architecture_core"] = core
        specs = RUNNER.planned_packet_specs(core)
        prior = RUNNER.build_architecture_plan_batch(self.run, {"packet_plans": [packet_plan_annotation(item["packet_slot_id"]) for item in specs[:2]]}, specs[:2], 1, 3)
        future = RUNNER.build_architecture_plan_batch(self.run, {"packet_plans": [packet_plan_annotation(item["packet_slot_id"]) for item in specs[3:]]}, specs[3:], 3, 3)
        RUNNER.save_planning_draft(self.run, "architecture_plan_batch_0001", {"record": prior})
        RUNNER.save_planning_draft(self.run, "architecture_plan_batch_0003", {"record": future})
        annotation = packet_plan_annotation(specs[2]["packet_slot_id"],
            depends_on_packet_slot_ids=[specs[0]["packet_slot_id"], specs[-1]["packet_slot_id"]])
        issues = RUNNER.named_reference_issues(self.run, {"packet_plans": [annotation]}, "architecturePlanBatchPayload", specs=[specs[2]])
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["invalid"], specs[-1]["packet_slot_id"])
        self.assertIn(specs[0]["packet_slot_id"], issues[0]["candidates"])
        self.assertNotIn(specs[-1]["packet_slot_id"], issues[0]["candidates"])

    def test_core_completes_missing_ending_and_three_opening_paths_without_whole_rewrite(self):
        payload = self.core()
        payload["attractors"][0]["kind"] = "thematic"
        payload["topology"]["nodes"] = payload["topology"]["nodes"][:1]
        payload["topology"]["edges"] = [{"edge_id": "self_edge", "from_node_id": "node_intro",
            "to_node_id": "node_intro", "relation": "progression", "hard_obligation_ids": []}]
        payload["extra_setup"] = "Preserve this authored setup intent."
        calls = []
        def transport(_method, _url, request, **kwargs):
            prompt = request["messages"][1]["content"]
            if "FIELD PATH\n" not in prompt:
                calls.append("bulk")
                return api_response(payload)
            path = prompt.split("FIELD PATH\n", 1)[1].split("\n", 1)[0]
            calls.append(path)
            schema = json.loads(prompt.split("VALUE SCHEMA\n", 1)[1].split("\nFULL ASSEMBLED", 1)[0])
            if "$ending_attractor" in path:
                value = schema["enum"][0]
            elif "$opening_targets" in path:
                value = schema["items"]["enum"][:3]
            elif path.endswith(".node_type"):
                value = "branch_family"
            elif path.endswith(".purpose"):
                value = "Synthetic distinct branch purpose."
            else:
                self.assertTrue(path.endswith(".hard_obligation_ids"), path)
                value = []
            return api_response(value, text=isinstance(value, str))
        with mock.patch.object(RUNNER, "architecture_core_prompt", return_value=("prompt", "context")):
            core = RUNNER.prepare_core_draft(self.run, transport)
        self.assertEqual(calls.count("bulk"), 1)
        self.assertEqual(core["attractors"][0]["kind"], "ending")
        self.assertEqual(sum(item["relation"] == "branch" for item in core["topology"]["edges"]), 3)
        state = RUNNER.read_json(self.run / ".staging/architecture_core.planning.json")
        self.assertIn("Preserve this authored setup intent.", state["hints"][0]["text"])

    def test_independent_dependency_cycles_can_be_repaired_one_value_at_a_time(self):
        payload = self.core()
        payload["topology"]["nodes"].pop()
        original = payload["obligation_graph"][0]
        payload["obligation_graph"] = [original | {"obligation_id": f"debt_{index}",
            "requires": [f"debt_{index + 1 if index % 2 else index - 1}"]} for index in range(1, 5)]
        payload["attractors"][0]["prerequisite_obligation_ids"] = ["debt_1"]
        for arc in payload["arcs"]:
            arc["hard_obligation_ids"] = ["debt_1"]
        repairs = []
        def transport(_method, _url, request, **kwargs):
            prompt = request["messages"][1]["content"]
            if "FIELD PATH\n" not in prompt:
                return api_response(payload)
            path = prompt.split("FIELD PATH\n", 1)[1].split("\n", 1)[0]
            self.assertTrue(path.endswith(".requires"), path)
            repairs.append(path)
            return api_response([])
        with mock.patch.object(RUNNER, "architecture_core_prompt", return_value=("prompt", "context")):
            core = RUNNER.prepare_core_draft(self.run, transport)
        self.assertEqual(len(repairs), 2)
        self.assertEqual(RUNNER.architecture_obligation_cycle(core), [])

    def test_field_exhaustion_retains_draft_and_resume_retries_only_that_value(self):
        state = self.state({"accepted": "preserve"})
        transport = mock.Mock(return_value=api_response("not an integer", text=True))
        with self.assertRaises(RUNNER.PausedError):
            RUNNER.planning_value(self.run, "architecture_core", state, ["missing"], {"type": "integer"}, "synthetic", transport)
        self.assertEqual(transport.call_count, 3)
        self.assertEqual(state["payload"], {"accepted": "preserve"})
        value = RUNNER.planning_value(self.run, "architecture_core", state, ["missing"], {"type": "integer"}, "synthetic", lambda *args, **kwargs: api_response(4))
        self.assertEqual(value, 4)
        self.assertEqual(len(list((self.run / "raw").glob("*_value_*-attempt*.api.json"))), 4)

    def test_complete_draft_never_silently_disappears_under_context_pressure(self):
        state = self.state({"must_keep": "x" * 220000})
        transport = mock.Mock(side_effect=AssertionError("oversized prompt was sent"))
        with self.assertRaises(RUNNER.CathedralsError) as raised:
            RUNNER.planning_value(self.run, "architecture_core", state, ["value"], {"type": "integer"}, "synthetic", transport)
        self.assertEqual(raised.exception.failure_class, "budget_exhaustion")
        transport.assert_not_called()
        self.assertEqual(len(state["payload"]["must_keep"]), 220000)

    def test_unresolved_lookup_is_not_reused_as_success_and_every_attempt_is_accounted(self):
        issue = {"path": ["target"], "kind": "source", "invalid": "missing", "context": "Synthetic use.", "candidates": {"source_one": "Synthetic source."}}
        transport = mock.Mock(side_effect=[api_response("UNRESOLVED", text=True), api_response("source_one", text=True)])
        self.assertEqual(RUNNER.resolve_named_reference(self.run, "test_lookup", issue, transport), "UNRESOLVED")
        self.assertEqual(RUNNER.resolve_named_reference(self.run, "test_lookup", issue, transport), "source_one")
        self.assertEqual(transport.call_count, 2)
        entries = [item for item in RUNNER.ledger_entries(self.run) if item["planned_step_id"].startswith("test_lookup")]
        self.assertEqual(len(entries), 2)
        self.assertEqual([item["commit_status"] for item in entries], ["FAILED_BEFORE_COMMIT", "COMMITTED"])
        self.assertEqual(sum(item["token_accounting"]["output_tokens"] for item in entries), 14)

    def test_timeout_default_is_ninety_minutes_for_planning_values(self):
        state = self.state({})
        transport = mock.Mock(return_value=api_response(1))
        with mock.patch.dict(RUNNER.os.environ, {}, clear=True):
            RUNNER.planning_value(self.run, "architecture_core", state, ["value"], {"type": "integer"}, "synthetic", transport)
        self.assertEqual(transport.call_args.kwargs["timeout"], 5400)


if __name__ == "__main__":
    unittest.main()
