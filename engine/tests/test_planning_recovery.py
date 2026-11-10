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

    def test_string_value_requests_a_strict_value_envelope_and_retains_raw_response(self):
        state = self.state({"accepted": "unchanged"})
        path = ["topology", "$connect", "node_target"]
        schema = {"type": "string", "enum": ["node_origin", "node_other"]}
        response = api_response({"value": "node_origin"})
        transport = mock.Mock(return_value=response)
        value = RUNNER.planning_value(self.run, "architecture_core", state, path, schema, "Choose a reachable predecessor.", transport)
        self.assertEqual(value, "node_origin")
        self.assertEqual(state["payload"], {"accepted": "unchanged"})
        request = transport.call_args.args[2]
        wire = request["response_format"]["json_schema"]["schema"]
        self.assertEqual(wire["required"], ["value"])
        self.assertFalse(wire["additionalProperties"])
        self.assertEqual(wire["properties"]["value"], schema)
        RUNNER.validate_json_schema({"value": value}, wire)
        self.assertIn('Return exactly {"value":', request["messages"][1]["content"])
        self.assertIn("not JSON properties", request["messages"][1]["content"])
        audit = RUNNER.read_json(self.run / ".staging/architecture_core.repair.json")["history"]
        self.assertEqual(audit[-1]["result"], "node_origin")
        self.assertEqual(audit[-1]["api_response"]["choices"][0]["message"]["content"], response["choices"][0]["message"]["content"])
        raw = self.run / "raw" / f"{audit[-1]['step_id']}-attempt1.api.json"
        self.assertEqual(RUNNER.read_json(raw)["choices"], response["choices"])
        self.assertEqual(transport.call_count, 1)

    def test_string_value_accepts_only_exact_literal_or_single_target_wrappers(self):
        path = ["topology", "$connect", "node_target"]
        schema = {"type": "string", "enum": ["node_origin"]}
        for index, content in enumerate((
            "  node_origin\n", '"node_origin"', '```json\n"node_origin"\n```',
            '{"value":"node_origin"}', '```json\n{"value":"node_origin"}\n```',
            '{"topology":{"$connect":{"node_target":"node_origin"}}}',
            '```json\n{"topology":{"$connect":{"node_target":"node_origin"}}}\n```',
        )):
            with self.subTest(content=content):
                state = self.state({"accepted": "unchanged"})
                transport = mock.Mock(return_value=api_response(content, text=True))
                value = RUNNER.planning_value(self.run, "architecture_core", state, path, schema, f"Synthetic wrapper case {index}.", transport)
                self.assertEqual(value, "node_origin")
                self.assertEqual(transport.call_count, 1)
                self.assertEqual(state["payload"], {"accepted": "unchanged"})

    def test_string_value_rejects_graph_patches_extra_fields_duplicates_and_invalid_targets(self):
        path = ["topology", "$connect", "node_target"]
        schema = {"type": "string", "enum": ["node_origin"]}
        for content in (
            '{"topology":{"edges":[{"from_node_id":"node_origin","to_node_id":"node_target"}]}}',
            '{"value":"node_origin","extra":"node_origin"}',
            '{"topology":{"$connect":{"node_target":"node_origin","node_other":"node_origin"}}}',
            '{"value":"node_origin","value":"node_origin"}',
            '{"topology":{"$connect":{"node_target":"node_origin","node_target":"node_origin"}}}',
            '["node_origin"]', '{"value":["node_origin"]}', '{"value":"node_unknown"}',
            '{"topology":{"$connect":{"wrong_target":"node_origin"}}}',
            'The predecessor is node_origin.',
        ):
            with self.subTest(content=content), self.assertRaises(RUNNER.SchemaError):
                value = RUNNER.planning_string_value(content, schema, path)
                RUNNER.validate_json_schema(value, schema)

    def test_wrapped_value_still_runs_schema_and_domain_validation_before_acceptance(self):
        state = self.state({"accepted": "unchanged"})
        schema = {"type": "string", "enum": ["node_origin", "node_other"]}
        transport = mock.Mock(side_effect=[api_response({"value": "node_unknown"}),
            api_response({"value": "node_origin"}), api_response({"value": "node_other"})])

        def domain(value):
            if value == "node_origin":
                raise RUNNER.SchemaError("Synthetic route restriction.")

        value = RUNNER.planning_value(self.run, "architecture_core", state, ["topology", "$connect", "node_target"],
            schema, "Synthetic validation.", transport, validator=domain)
        self.assertEqual(value, "node_other")
        self.assertEqual(transport.call_count, 3)
        self.assertEqual(state["payload"], {"accepted": "unchanged"})
        entries = [item for item in RUNNER.ledger_entries(self.run) if item["step_type"] == "analysis"]
        self.assertEqual([item["commit_status"] for item in entries], ["FAILED_BEFORE_COMMIT", "FAILED_BEFORE_COMMIT", "COMMITTED"])
        self.assertEqual(sum(item["token_accounting"]["output_tokens"] for item in entries), 21)

    def test_wrapped_string_response_replays_after_checkpoint_interruption_without_another_call(self):
        payload = {"accepted": "unchanged"}
        path = ["topology", "$connect", "node_target"]
        schema = {"type": "string", "enum": ["node_origin"]}
        transport = mock.Mock(return_value=api_response({"topology": {"$connect": {"node_target": "node_origin"}}}))
        with mock.patch.object(RUNNER, "save_planning_draft", side_effect=RUNNER.PausedError("test", "checkpoint interrupted")):
            with self.assertRaises(RUNNER.PausedError):
                RUNNER.planning_value(self.run, "architecture_core", self.state(payload), path, schema, "Synthetic replay.", transport)
        raw = next((self.run / "raw").glob("architecture_core_value_*-attempt1.api.json"))
        original = raw.read_bytes()
        restored = self.state(payload)
        forbidden = mock.Mock(side_effect=AssertionError("saved model choice must not be regenerated"))
        self.assertEqual(RUNNER.planning_value(self.run, "architecture_core", restored, path, schema, "Synthetic replay.", forbidden), "node_origin")
        forbidden.assert_not_called()
        self.assertEqual(raw.read_bytes(), original)
        self.assertEqual(restored["payload"], payload)
        entries = [item for item in RUNNER.ledger_entries(self.run) if item["step_type"] == "analysis"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["token_accounting"]["output_tokens"], 7)

    def test_freeform_string_value_preserves_whitespace_and_literal_json_text(self):
        for index, value in enumerate(('  Preserved wording.\n\n  ', '{"value":"literal text, not another wrapper"}')):
            with self.subTest(value=value):
                transport = mock.Mock(return_value=api_response({"value": value}))
                actual = RUNNER.planning_value(self.run, "architecture_core", self.state({}), ["description"],
                    {"type": "string"}, f"Synthetic wording {index}.", transport)
                self.assertEqual(actual, value)

    def test_string_value_envelope_keeps_schema_definition_references_at_the_root(self):
        schema = {"type": "string", "$ref": "#/$defs/choice", "$defs": {"choice": {"enum": ["node_origin"]}}}
        transport = mock.Mock(return_value=api_response({"value": "node_origin"}))
        self.assertEqual(RUNNER.planning_value(self.run, "architecture_core", self.state({}), ["pending"], schema,
            "Synthetic reference schema.", transport), "node_origin")
        wire = transport.call_args.args[2]["response_format"]["json_schema"]["schema"]
        RUNNER.validate_json_schema({"value": "node_origin"}, wire)
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_json_schema({"value": "node_unknown"}, wire)




    def test_macro_without_ending_repairs_only_the_attractor_kind(self):
        payload = self.core()
        payload["topology"] = RUNNER.scaffold_macro_topology()
        payload["attractors"][0]["kind"] = "thematic"
        RUNNER.save_planning_draft(self.run, "architecture_core", self.state(payload) | {"checkpoint_version": 3})
        transport = mock.Mock(side_effect=lambda method, url, request, **kwargs:
            planning_response(request, lambda path, node: node["enum"][0]))
        core = RUNNER.prepare_core_draft(self.run, transport)
        self.assertEqual(core["attractors"][0]["kind"], "ending")
        transport.assert_called_once()
        self.assertEqual(RUNNER.read_json(self.run / ".staging/architecture_core.planning.json")["payload"],
            payload | {"attractors": [payload["attractors"][0] | {"kind": "ending"}]})

    def test_independent_dependency_cycles_can_be_repaired_one_value_at_a_time(self):
        payload = self.core()
        payload["topology"] = RUNNER.scaffold_macro_topology()
        original = payload["obligation_graph"][0]
        payload["obligation_graph"] = [original | {"obligation_id": f"debt_{index}",
            "requires": [f"debt_{index + 1 if index % 2 else index - 1}"]} for index in range(1, 5)]
        payload["attractors"][0]["prerequisite_obligation_ids"] = ["debt_1"]
        for arc in payload["arcs"]: arc["hard_obligation_ids"] = ["debt_1"]
        RUNNER.save_planning_draft(self.run, "architecture_core", self.state(payload) | {"checkpoint_version": 3})
        transport = mock.Mock(return_value=api_response([]))
        core = RUNNER.prepare_core_draft(self.run, transport)
        self.assertEqual(transport.call_count, 2)
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
            RUNNER.planning_value(self.run, "architecture_core", state, ["must_keep"], {"type": "integer"}, "synthetic", transport)
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
        self.records["genesis"] |= padded(fixture["genesis_pretty_bytes"])
        schema = {"type": "string", "$defs": {"unused": {"description": "x" * fixture["unused_schema_bytes"]}}}
        state = self.state(payload)
        transport = mock.Mock(return_value=api_response("active", text=True))
        RUNNER.planning_value(self.run, "architecture_core", state, ["records"], schema, "Synthetic regression.", transport)
        request = transport.call_args.args[2]
        prompt = request["messages"][1]["content"]
        context = json.loads(prompt.split("FULL ASSEMBLED PLANNING CONTEXT\n", 1)[1].split("\n\nReturn", 1)[0])
        self.assertEqual(context["targets"][0]["retained_value"], payload["records"])
        self.assertNotIn("assembled_draft", context)
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
        self.assertGreaterEqual(limit, RUNNER.MIN_PLANNING_OUTPUT_TOKENS)
        self.assertLessEqual(limit + 100 + 4096, 6000)

    def test_batch_reduces_schema_size_before_pausing_for_context(self):
        state = self.state({"keep": "x" * 125000})
        choices = [f"choice_{index}_" + "x" * 64 for index in range(200)]
        tasks = [{"path": [f"field_{index}"], "schema": {"type": "string", "enum": choices}, "reason": "Synthetic independent choice."} for index in range(4)]
        transport = mock.Mock(side_effect=lambda method, url, request, **kwargs: planning_response(request, lambda path, node: choices[0]))
        RUNNER.planning_batch(self.run, "architecture_core", state, tasks, transport)
        self.assertEqual(transport.call_count, 2)
        self.assertEqual(state["payload"]["keep"], "x" * 125000)
        self.assertTrue(all(state["payload"][f"field_{index}"] == choices[0] for index in range(4)))
        for call in transport.call_args_list:
            prompt = call.args[2]["messages"][1]["content"]
            context = json.loads(prompt.split("FULL ASSEMBLED PLANNING CONTEXT\n", 1)[1].split("\n\nReturn", 1)[0])
            self.assertNotIn(state["payload"]["keep"], json.dumps(context))

    def test_true_context_overflow_pauses_main_without_terminal_finalization(self):
        state = self.state({"accepted": "x" * 220000})
        RUNNER.save_planning_draft(self.run, "architecture_core", state)
        draft = self.run / ".staging/architecture_core.planning.json"
        original = draft.read_bytes()
        forbidden = mock.Mock(side_effect=AssertionError("network forbidden"))
        def execute(*args, **kwargs):
            RUNNER.planning_value(self.run, "architecture_core", state, ["accepted"], {"type": "integer"}, "Synthetic limit.", forbidden)
        with mock.patch.object(RUNNER, "ensure_runtime_layout"), mock.patch.object(RUNNER, "choose_resume", return_value=self.run), mock.patch.object(
            RUNNER, "snapshot_root", return_value=ROOT
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
            RUNNER.planning_value(self.run, "architecture_core", state, ["must_keep"], {"type": "integer"}, "synthetic", transport)
        self.assertEqual(transport.call_args.kwargs["timeout"], 5400)


if __name__ == "__main__":
    unittest.main()
