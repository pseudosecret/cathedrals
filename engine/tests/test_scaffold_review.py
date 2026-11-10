"""Scoped scaffold repair selectors preserve raw responses and substantive checks."""
import copy
import json
import unittest
from unittest import mock

from test_cathedrals import RUNNER
from test_backward_scaffold import node
import test_reference_resolution as fixtures
from test_reference_resolution import api_response
from test_scaffold_compiler import GENESIS, declaration, selection


class ScaffoldReviewTests(unittest.TestCase):
    def setUp(self):
        fixtures.ReferenceResolutionTests.setUp(self)
        self.identifiers = [f"scaffold_scene_{index:05d}" for index in range(8, 12)]
        target = node("scaffold_scene_00007", cases=[{"case_id": "prior_entry", "requirements": [
            {"requirement_id": "prior_requirement", "description": "Synthetic continuity."}]}])
        target["successors"] = [{"to_node_id": "scaffold_outcome_0002", "target_case_id": "older_entry", "supports": [
            {"requirement_id": "older_requirement", "guarantee_ids": [], "genesis_source_ids": ["older_genesis_citation"],
                "reason": "Synthetic earlier connection outside this review."}]}]
        self.frontier = [target]
        declarations = [declaration(str(index)) for index in range(4)]
        self.fields = list(declarations[0])
        nodes = RUNNER.compile_scaffold_declarations(declarations, self.identifiers)
        self.patch = {"nodes": [RUNNER.compile_scaffold_connections(source, self.frontier,
            selection(source, self.frontier), GENESIS) for source in nodes],
            "complete": False, "opening_node_id": None, "opening_support": []}

    def review(self, transport, *, mechanical_problem=None):
        return RUNNER.review_scaffold_connections(self.run, "scaffold_expand_00004", self.patch,
            self.frontier, self.fields, mechanical_problem, transport)

    def test_reported_duplicate_selectors_are_accepted_once_and_replayed_without_usage(self):
        payload = {"supported": False, "reason": "Synthetic contract and connection repairs.",
            "contract_repairs": {identifier: ["entry_cases", "arc_id", "arc_id"] for identifier in self.identifiers},
            "connection_repairs": {identifier: [self.frontier[0]["node_id"]] * 7 for identifier in self.identifiers}}
        before = RUNNER.canonical_json([self.patch, self.frontier, payload])
        transport = mock.Mock(return_value=api_response(payload))
        result = self.review(transport)
        transport.assert_called_once()
        self.assertFalse(result["supported"])
        self.assertEqual(result["contract_repairs"], {identifier: ["entry_cases", "arc_id"] for identifier in self.identifiers})
        self.assertEqual(result["connection_repairs"], {identifier: [self.frontier[0]["node_id"]] for identifier in self.identifiers})
        response_schema = transport.call_args.args[2]["response_format"]["json_schema"]["schema"]
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_json_schema(payload, response_schema)
        raw = next((self.run / "raw").glob("scaffold_expand_00004_review_*-attempt1.api.json"))
        original_raw = raw.read_bytes()
        self.assertEqual(json.loads(RUNNER.read_json(raw)["choices"][0]["message"]["content"]), payload)
        prefix = (self.run / "ledger.jsonl").read_bytes()
        forbidden = mock.Mock(side_effect=AssertionError("Accepted review was requested again"))
        self.assertEqual(self.review(forbidden), result)
        forbidden.assert_not_called()
        self.assertEqual(raw.read_bytes(), original_raw)
        self.assertEqual((self.run / "ledger.jsonl").read_bytes(), prefix)
        state = RUNNER.load_state(self.run)
        self.assertEqual((state["input_tokens"], state["output_tokens"], state["analysis_step_count"]), (11, 7, 1))
        history = RUNNER.read_json(self.run / ".staging/architecture_core.repair.json")["history"]
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["result"], result)
        self.assertEqual(json.loads(history[0]["api_response"]["choices"][0]["message"]["content"]), payload)
        entry = RUNNER.step_entries(self.run, history[0]["step_id"])[0]
        self.assertEqual(entry["output_hash"], RUNNER.sha256_bytes(RUNNER.canonical_json(result)))
        self.assertEqual(RUNNER.canonical_json([self.patch, self.frontier, payload]), before)

    def test_invalid_selectors_and_contradictory_verdicts_still_exhaust_repairs(self):
        source = self.identifiers[0]
        base = {"supported": False, "reason": "Synthetic invalid review.", "contract_repairs": {}, "connection_repairs": {}}
        cases = [
            (base | {"contract_repairs": {source: ["not_a_contract_field", "not_a_contract_field"]}}, None, "one of"),
            (base | {"contract_repairs": {"unknown_scene": ["arc_id", "arc_id"]}}, None, "field not allowed"),
            (base | {"connection_repairs": {source: ["unknown_target", "unknown_target"]}}, None, "one of"),
            (base | {"contract_repairs": {source: ["arc_id", {"arc_id": "different value"}, "arc_id"]}}, None, "one of"),
            (base | {"contract_repairs": {source: "arc_id"}}, None, "array"),
            (base, None, "Identify the specific"),
            (base | {"supported": True, "contract_repairs": {source: ["arc_id", "arc_id"]}}, None, "supported=true conflicts"),
            (base | {"supported": True}, "Synthetic structural problem", "supported=true conflicts"),
            ('{"supported":false,"reason":"Duplicate keys","contract_repairs":{},"contract_repairs":{},"connection_repairs":{}}',
                None, "duplicate JSON property"),
        ]
        for payload, problem, message in cases:
            with self.subTest(payload=payload):
                response = api_response(payload, text=isinstance(payload, str))
                transport = mock.Mock(return_value=response)
                with self.assertRaisesRegex(RUNNER.PausedError, message):
                    self.review(transport, mechanical_problem=problem)
                self.assertEqual(transport.call_count, 3)
        self.assertFalse((self.run / ".staging/architecture_core.repair.json").exists())

    def test_contract_issue_fields_normalize_before_strict_connection_validation(self):
        payload = {"contract_issue": {"fields": ["guarantees", "guarantees"], "reason": "Synthetic missing guarantee."}}
        schema = RUNNER.scaffold_connection_schema(self.patch["nodes"][0], self.frontier, GENESIS, allow_amendment=True)
        transport = mock.Mock(return_value=api_response(payload))
        result, response = RUNNER.request_architecture_analysis(self.run, "synthetic_contract_issue", "Select a contract repair.",
            schema, transport, planning_mode=True, result_normalizer=RUNNER.normalize_scaffold_repair_selectors)
        self.assertEqual(result["contract_issue"]["fields"], ["guarantees"])
        self.assertEqual(json.loads(response["choices"][0]["message"]["content"]), payload)
        transport.assert_called_once()

    def test_requests_without_scaffold_normalization_keep_unique_item_checks(self):
        payload = {"contract_issue": {"fields": ["guarantees", "guarantees"], "reason": "Synthetic missing guarantee."}}
        schema = RUNNER.scaffold_connection_schema(self.patch["nodes"][0], self.frontier, GENESIS, allow_amendment=True)
        transport = mock.Mock(return_value=api_response(payload))
        with self.assertRaisesRegex(RUNNER.PausedError, "unique items"):
            RUNNER.request_architecture_analysis(self.run, "synthetic_strict_request", "Select a contract repair.", schema,
                transport, planning_mode=True)
        self.assertEqual(transport.call_count, 3)

    def test_normalization_does_not_change_evidence_prose_or_malformed_values(self):
        payload = {"contract_issue": {"fields": ["guarantees", "entry_cases", "guarantees"]},
            "contract_repairs": {"scene": ["arc_id", "Arc_Id", "arc_id"], "malformed": ["arc_id", {"value": 1}, "arc_id"]},
            "connection_repairs": {"scene": ["target", "target"]},
            "connections": {"evidence_ids": ["source", "source"]}, "prose": ["Same words.", "Same words."]}
        before = copy.deepcopy(payload)
        result = RUNNER.normalize_scaffold_repair_selectors(payload)
        self.assertEqual(payload, before)
        self.assertEqual(result["contract_issue"]["fields"], ["guarantees", "entry_cases"])
        self.assertEqual(result["contract_repairs"]["scene"], ["arc_id", "Arc_Id"])
        self.assertEqual(result["connection_repairs"]["scene"], ["target"])
        for field in ("connections", "prose"):
            self.assertEqual(result[field], before[field])
        self.assertEqual(result["contract_repairs"]["malformed"], before["contract_repairs"]["malformed"])
        self.assertEqual(RUNNER.normalize_scaffold_repair_selectors(result), result)
        self.assertEqual(RUNNER.normalize_scaffold_repair_selectors(["arc_id", "arc_id"]), ["arc_id", "arc_id"])

    def test_review_omits_older_routes_and_keeps_complete_patch_evidence(self):
        support = self.patch["nodes"][0]["successors"][0]["supports"][0]
        support["genesis_source_ids"] = ["genesis_patch"]
        source = {"source_id": "genesis_patch", "source_commit_id": "commit_genesis", "source_hash": "a" * 64,
            "record_pointer": "/constraint_delta/canonical_facts/0", "authority": "COMMITTED SOURCE EVIDENCE",
            "immutable_source": {"status": "contested", "value": " Synthetic complete evidence.\r\nKeep spacing and λ.  "}}
        before = RUNNER.canonical_json([self.patch, self.frontier, source])
        transport = mock.Mock(return_value=api_response({"supported": True, "reason": "Synthetic supported patch.",
            "contract_repairs": {}, "connection_repairs": {}}))
        with mock.patch.object(RUNNER, "retrieve_original_sources", return_value=[source]) as retrieve:
            self.assertTrue(self.review(transport)["supported"])
        retrieve.assert_called_once_with(self.run, [{"sources": [{"artifact_id": "genesis_patch"}]}],
            limit=None, strict=True, follow_sources=False)
        context = json.loads(transport.call_args.args[2]["messages"][1]["content"].split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
        self.assertEqual(context["patch"], self.patch)
        self.assertEqual(context["committed_genesis_sources"], [source])
        self.assertEqual(context["existing_successors"], [{key: value for key, value in self.frontier[0].items() if key != "successors"}])
        self.assertNotIn("older_genesis_citation", json.dumps(context))
        self.assertEqual(RUNNER.canonical_json([self.patch, self.frontier, source]), before)


if __name__ == "__main__":
    unittest.main()
