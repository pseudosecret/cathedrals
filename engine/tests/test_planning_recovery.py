"""Planning recovery uses bounded values, real catalogs, and complete draft context."""

import copy
import json
import socket
import unittest
from unittest import mock

from test_cathedrals import ROOT, RUNNER, architecture_core_payload, architecture_genesis_records, packet_plan_annotation
import test_reference_resolution as reference_fixtures

api_response = reference_fixtures.api_response
planning_response = reference_fixtures.planning_response
planning_path = reference_fixtures.planning_path


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
            transport = mock.Mock(side_effect=lambda method, url, request, **kwargs:
                planning_response(request, lambda path, node: "__NARRATIVE_HINT__"))
            RUNNER.repair_planning_references(self.run, "architecture_plan_batch_0001", state,
                RUNNER.architecture_plan_batch_schema(self.run, RUNNER.planned_packet_specs(core)), transport,
                specs=RUNNER.planned_packet_specs(core))
            self.assertEqual(transport.call_count, 1)
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
        self.assertIn('"accepted":"keep me"', prompt)
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
        state = self.state({})
        schemas = {"flag": {"type": "boolean"}, "count": {"type": "integer"}, "empty": {"type": "array"}}
        values = {"flag": False, "count": 0, "empty": []}
        tasks = [{"path": [key], "schema": schema, "reason": "Synthetic batch value."} for key, schema in schemas.items()]
        transport = mock.Mock(side_effect=lambda method, url, request, **kwargs: planning_response(request, lambda path, node: values[path[-1]]))
        RUNNER.planning_batch(self.run, "architecture_core", state, tasks, transport)
        RUNNER.planning_batch(self.run, "architecture_core", state, tasks, mock.Mock(side_effect=AssertionError("repeated")))
        self.assertEqual(state["payload"], values)
        self.assertEqual(transport.call_count, 1)

    def test_response_replays_after_success_was_ledgered_before_checkpoint_restore(self):
        state = self.state({"accepted": "keep"})
        transport = mock.Mock(return_value=api_response(7))
        value = RUNNER.planning_value(self.run, "architecture_core", state, ["pending"], {"type": "integer"}, "Synthetic recovery.", transport)
        self.assertEqual(value, 7)
        restored = self.state({"accepted": "keep"})
        forbidden = mock.Mock(side_effect=AssertionError("successful response repeated"))
        value = RUNNER.planning_value(self.run, "architecture_core", restored, ["pending"], {"type": "integer"}, "Synthetic recovery.", forbidden)
        self.assertEqual(value, 7)
        forbidden.assert_not_called()
        self.assertEqual(len([item for item in RUNNER.ledger_entries(self.run) if item["step_type"] == "analysis"]), 1)

    def test_reasoning_only_exact_enum_response_replays_with_same_validation(self):
        state = self.state({"accepted": "keep"})
        response = api_response("", text=True)
        response["choices"][0]["message"]["reasoning_content"] = "source_one"
        schema = {"type": "string", "enum": ["source_one"]}
        value = RUNNER.planning_value(self.run, "architecture_core", state, ["pending"], schema, "Synthetic identity.", lambda *args, **kwargs: response)
        self.assertEqual(value, "source_one")
        value = RUNNER.planning_value(self.run, "architecture_core", self.state({"accepted": "keep"}), ["pending"], schema, "Synthetic identity.", mock.Mock(side_effect=AssertionError("repeated")))
        self.assertEqual(value, "source_one")

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
        self.assertEqual([entry["failure_class"] for entry in RUNNER.ledger_entries(self.run)
                          if entry["commit_status"] == "FAILED_BEFORE_COMMIT"], ["provider_incomplete_response"])

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
            if "FIELD PATH\n" not in prompt and "BATCH TARGETS\n" not in prompt:
                response = api_response('{"saturation_rationale":"keep me", "attractors":[', text=True)
                response["choices"][0]["finish_reason"] = "length"
                return response
            def resolve(path, node):
                paths.append(RUNNER.reference_path(path))
                if path[0] == "$layout":
                    value = desired
                    for part in planning_path(path[1]):
                        value = value[part]
                    return len(value)
                value = desired
                for part in path:
                    value = value[part]
                return value
            return planning_response(request, resolve)
        with mock.patch.object(RUNNER, "architecture_core_prompt", return_value=("prompt", "context")):
            core = RUNNER.prepare_core_draft(self.run, transport)
        self.assertEqual(core["scope_commitment"]["saturation_rationale"], "keep me")
        self.assertEqual(len(core["arcs"]), 4)
        self.assertLess(paths.index("$.attractors[0]"), paths.index("$.obligation_graph[0]"))
        self.assertFalse(any(path.endswith(".status") for path in paths))
        self.assertLess(len(paths), 25)
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
            if not stopped:
                stopped = True
                raise RUNNER.IncompleteResponseError("synthetic setup interruption", api_response(
                    {"value_001": {"setup_slot_id": "scene_slot_0001"}}))
            def resolve(path, node):
                calls.append(path)
                if path[0] == "$setups":
                    if path[-1] == "instruction":
                        return "Synthetic coherent earlier setup."
                    return {"setup_slot_id": "scene_slot_0001", "instruction": "Synthetic coherent earlier setup."}
                self.fail(path)
            return planning_response(request, resolve)
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
        self.assertNotIn(["$setups", 0, "setup_slot_id"], calls)
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
            if "FIELD PATH\n" not in prompt and "BATCH TARGETS\n" not in prompt:
                calls.append("bulk")
                return api_response(payload)
            def resolve(path, node):
                calls.append(path)
                if "$ending_attractor" in path:
                    return node["enum"][0]
                if "$opening_targets" in path:
                    return node["items"]["enum"][:3]
                return {"node_type": "branch_family", "purpose": "Synthetic distinct branch purpose.", "hard_obligation_ids": []}
            return planning_response(request, resolve)
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
        with self.assertRaises(RUNNER.PausedError) as raised:
            RUNNER.planning_value(self.run, "architecture_core", state, ["value"], {"type": "integer"}, "synthetic", transport)
        self.assertEqual(raised.exception.failure_class, "budget_exhaustion")
        transport.assert_not_called()
        self.assertEqual(len(state["payload"]["must_keep"]), 220000)
        self.assertIn("estimated prompt", raised.exception.reason)
        self.assertFalse(any(item["failure_class"] == "budget_exhaustion" for item in RUNNER.ledger_entries(self.run)))

    def test_saved_prompt_sizes_fit_after_lossless_compaction_and_unused_schema_removal(self):
        fixture = RUNNER.read_json(ROOT / "engine/tests/fixtures/planning-context-budget-failure.json")
        def padded(size):
            value = {"records": [{"text": "synthetic context"} for _ in range(512)], "padding": ""}
            value["padding"] = "x" * (size - len(json.dumps(value, indent=2).encode()))
            self.assertEqual(len(json.dumps(value, indent=2).encode()), size)
            return value
        payload = padded(fixture["draft_pretty_bytes"])
        self.records["genesis"] = padded(fixture["genesis_pretty_bytes"])
        schema = {"type": "string", "$defs": {"unused": {"description": "x" * fixture["unused_schema_bytes"]}}}
        state = self.state(payload)
        transport = mock.Mock(return_value=api_response("active", text=True))
        RUNNER.planning_value(self.run, "architecture_core", state, ["status"], schema, "Synthetic regression.", transport)
        request = transport.call_args.args[2]
        prompt = request["messages"][1]["content"]
        context = json.loads(prompt.split("FULL ASSEMBLED PLANNING CONTEXT\n", 1)[1].split("\n\nReturn", 1)[0])
        self.assertEqual(context["assembled_draft"], payload)
        self.assertEqual(context["genesis"], self.records["genesis"])
        self.assertNotIn('"unused"', prompt)
        self.assertLess((len(prompt.encode()) + 2) // 3, fixture["max_prepared_context_tokens"])
        self.assertGreater(fixture["original_prompt_estimate_tokens"], fixture["max_prepared_context_tokens"])

    def test_truncated_array_keeps_eight_records_and_does_not_accept_broken_tokens(self):
        records = [{"obligation_id": f"debt_{index}", "description": f"Synthetic debt {index}."} for index in range(8)]
        content = '{"obligation_graph":[' + ','.join(json.dumps(item) for item in records) + ',{"description":"unfinished'
        value, incomplete = RUNNER.parsed_planning_fragment(content)
        self.assertEqual(value["obligation_graph"], records)
        self.assertIn(["obligation_graph"], incomplete)
        for suffix in ('1e', '"bad\\u12', 'tru'):
            with self.subTest(suffix=suffix):
                value, _ = RUNNER.parsed_planning_fragment('{"accepted":false,"unfinished":' + suffix)
                self.assertEqual(value, {"accepted": False})

    def test_record_batches_reduce_calls_and_preserve_owned_status_and_accepted_siblings(self):
        desired = self.core()
        original = desired["obligation_graph"][0]
        desired["obligation_graph"] = [copy.deepcopy(original) | {"obligation_id": f"debt_{index}", "description": f"Synthetic debt {index}."} for index in range(12)]
        payload = copy.deepcopy(desired)
        payload["obligation_graph"] = [{"obligation_id": item["obligation_id"], "description": item["description"]} for item in desired["obligation_graph"]]
        schema = RUNNER.definition_schema("architectureCorePayload")
        schema["$defs"]["obligation"].pop("allOf", None)
        state, calls = self.state(payload), []
        def transport(_method, _url, request, **kwargs):
            def resolve(path, node):
                calls.append(path)
                value = desired
                if path[0] == "$layout":
                    for part in planning_path(path[1]):
                        value = value[part]
                    return len(value)
                for part in path:
                    value = value[part]
                return value
            return planning_response(request, resolve)
        RUNNER.fill_planning_shape(self.run, "architecture_core", state, schema, transport)
        self.assertEqual(state["payload"], desired)
        self.assertTrue(all(item["status"] == "active" for item in state["payload"]["obligation_graph"]))
        self.assertFalse(any(path[-1] == "status" for path in calls))
        self.assertEqual(len(state["batch_calls"]), 4)  # One layout and three four-record batches.
        self.assertLess(len(state["batch_calls"]), 225 // 10)

    def test_mixed_batch_retains_valid_entries_and_retries_only_invalid_value(self):
        state = self.state({})
        tasks = [{"path": [name], "schema": {"type": "integer"}, "reason": "Synthetic value."} for name in ("good", "bad")]
        transport = mock.Mock(side_effect=[api_response({"value_001": 0, "value_002": "bad"}), api_response(4)])
        RUNNER.planning_batch(self.run, "architecture_core", state, tasks, transport)
        self.assertEqual(state["payload"], {"good": 0, "bad": 4})
        self.assertEqual(transport.call_count, 2)
        self.assertIn("$.bad", transport.call_args.args[2]["messages"][1]["content"])
        self.assertNotIn("FIELD PATH\n$.good", transport.call_args.args[2]["messages"][1]["content"])
        entries = [item for item in RUNNER.ledger_entries(self.run) if item["step_type"] == "analysis"]
        self.assertEqual(sum(item["token_accounting"]["output_tokens"] for item in entries), 14)
        self.assertEqual(len(entries), 2)

    def test_batch_exhaustion_and_resume_do_not_repeat_accepted_field(self):
        state = self.state({})
        tasks = [{"path": [name], "schema": {"type": "integer"}, "reason": "Synthetic value."} for name in ("good", "bad")]
        transport = mock.Mock(side_effect=[api_response({"value_001": 0}), *[api_response("bad", text=True) for _ in range(3)]])
        with self.assertRaises(RUNNER.PausedError):
            RUNNER.planning_batch(self.run, "architecture_core", state, tasks, transport)
        state = RUNNER.read_json(self.run / ".staging/architecture_core.planning.json")
        self.assertEqual(state["payload"], {"good": 0})
        resume = mock.Mock(return_value=api_response(5))
        RUNNER.planning_batch(self.run, "architecture_core", state, tasks, resume)
        self.assertEqual(state["payload"], {"good": 0, "bad": 5})
        self.assertEqual(resume.call_count, 1)

    def test_missing_nullable_batch_value_is_not_accepted_as_explicit_null(self):
        state = self.state({})
        tasks = [{"path": [name], "schema": {"type": "null"}, "reason": "Synthetic nullable value."} for name in ("one", "two")]
        transport = mock.Mock(side_effect=[api_response({"value_001": None}), api_response(None)])
        RUNNER.planning_batch(self.run, "architecture_core", state, tasks, transport)
        self.assertEqual(transport.call_count, 2)
        self.assertEqual(state["payload"], {"one": None, "two": None})

    def test_truncated_batch_array_retains_closed_records_and_partial_record_members(self):
        state = self.state({"records": [{}, {}]})
        item = {"type": "object", "required": ["a", "b"], "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}}
        tasks = [{"path": ["records"], "schema": {"type": "array", "minItems": 2, "maxItems": 2, "items": item}, "reason": "Synthetic records."}]
        transport = mock.Mock(side_effect=[api_response('{"value_001":[{"a":1,"b":2},{"a":3,"b":', text=True), api_response(4)])
        RUNNER.planning_batch(self.run, "architecture_core", state, tasks, transport)
        self.assertEqual(state["payload"], {"records": [{"a": 1, "b": 2}, {"a": 3, "b": 4}]})
        self.assertEqual(transport.call_count, 2)
        self.assertIn("FIELD PATH\n$.records[1].b", transport.call_args.args[2]["messages"][1]["content"])

    def test_record_batch_cannot_rewrite_accepted_siblings_or_nested_array_entries(self):
        state = self.state({"record": {"kept": "original", "sources": [{"key": "stay"}, {}]}})
        sources = {"type": "array", "minItems": 2, "maxItems": 2, "items": {
            "type": "object", "required": ["key"], "properties": {"key": {"type": "string"}}}}
        node = {"type": "object", "required": ["kept", "sources"], "properties": {"kept": {"type": "string"}, "sources": sources}}
        schema = {"type": "object", "additionalProperties": False, "required": ["sources"], "properties": {"sources": sources}}
        task = {"path": ["record"], "schema": schema, "preserve_schema": node, "root_schema": node, "reason": "Synthetic record."}
        transport = mock.Mock(return_value=api_response({"value_001": {"kept": "rewrite", "sources": [{"key": "rewrite"}, {"key": "new"}]}}))
        RUNNER.planning_batch(self.run, "architecture_core", state, [task], transport)
        self.assertEqual(state["payload"], {"record": {"kept": "original", "sources": [{"key": "stay"}, {"key": "new"}]}})
        self.assertEqual(transport.call_count, 1)

    def test_failed_group_splits_into_smaller_groups_without_repeating_success(self):
        state = self.state({})
        tasks = [{"path": [f"field_{index}"], "schema": {"type": "integer"}, "reason": "Synthetic independent value."} for index in range(4)]
        calls = []
        def transport(_method, _url, request, **kwargs):
            calls.append(request)
            if len(calls) == 1:
                return api_response({})
            return planning_response(request, lambda path, node: int(path[-1].split("_")[-1]))
        RUNNER.planning_batch(self.run, "architecture_core", state, tasks, transport)
        self.assertEqual(len(calls), 3)
        self.assertEqual(state["payload"], {f"field_{index}": index for index in range(4)})
        self.assertTrue(all("BATCH TARGETS\n" in request["messages"][1]["content"] for request in calls))

    def test_planning_output_allowance_shrinks_to_loaded_model_headroom(self):
        budgets = RUNNER.read_json(self.run / "run-manifest.json")["budgets"]
        read_json = RUNNER.read_json
        budgets = budgets | {"model_context_window_tokens": 6000, "context_safety_reserve_tokens": 4096}
        with mock.patch.object(RUNNER, "read_json", side_effect=lambda path: {"budgets": budgets} if path.name == "run-manifest.json" else read_json(path)):
            limit = RUNNER.planning_output_limit(self.run, "x" * 300, {"type": "string"}, 8192, "Synthetic capacity")
        self.assertEqual(limit, 1804)

    def test_batch_reduces_schema_size_before_pausing_for_context(self):
        state = self.state({"keep": "x" * 125000})
        choices = [f"choice_{index}_" + "x" * 64 for index in range(100)]
        tasks = [{"path": [f"field_{index}"], "schema": {"type": "string", "enum": choices}, "reason": "Synthetic independent choice."} for index in range(4)]
        transport = mock.Mock(side_effect=lambda method, url, request, **kwargs: planning_response(request, lambda path, node: choices[0]))
        RUNNER.planning_batch(self.run, "architecture_core", state, tasks, transport)
        self.assertEqual(transport.call_count, 2)
        self.assertEqual(state["payload"]["keep"], "x" * 125000)
        self.assertTrue(all(state["payload"][f"field_{index}"] == choices[0] for index in range(4)))
        for call in transport.call_args_list:
            prompt = call.args[2]["messages"][1]["content"]
            context = json.loads(prompt.split("FULL ASSEMBLED PLANNING CONTEXT\n", 1)[1].split("\n\nReturn", 1)[0])
            self.assertEqual(context["assembled_draft"]["keep"], state["payload"]["keep"])

    def test_true_context_overflow_pauses_main_without_terminal_finalization(self):
        state = self.state({"accepted": "x" * 220000})
        RUNNER.save_planning_draft(self.run, "architecture_core", state)
        draft = self.run / ".staging/architecture_core.planning.json"
        original = draft.read_bytes()
        forbidden = mock.Mock(side_effect=AssertionError("network forbidden"))
        def execute(*args, **kwargs):
            RUNNER.planning_value(self.run, "architecture_core", state, ["missing"], {"type": "integer"}, "Synthetic limit.", forbidden)
        with mock.patch.object(RUNNER, "ensure_runtime_layout"), mock.patch.object(RUNNER, "choose_resume", return_value=self.run), mock.patch.object(
            RUNNER, "snapshot_root", return_value=self.root / "absent"
        ), mock.patch.object(RUNNER, "ensure_resume_ready"), mock.patch.object(RUNNER, "execute_run", side_effect=execute):
            result = RUNNER.main([], output_fn=lambda value: None, transport=forbidden)
        self.assertEqual(result, 2)
        self.assertEqual(RUNNER.load_state(self.run)["status"], "PAUSED_GENERATION")
        self.assertFalse((self.run / "finalization.json").exists())
        self.assertEqual(draft.read_bytes(), original)
        forbidden.assert_not_called()

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
