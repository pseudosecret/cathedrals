"""Target-first planning, contract integrity and bounded local recovery."""
import json
import unittest
from collections import Counter
from unittest import mock

from test_cathedrals import RUNNER
from test_backward_scaffold import node
import test_scaffold_compiler as compiler
import test_reference_resolution as fixtures


SUPPORTED = []


class ScaffoldTargetTests(unittest.TestCase):
    setUp = compiler.ScaffoldCompilerTests.setUp
    provider = compiler.ScaffoldCompilerTests.provider
    expand = compiler.ScaffoldCompilerTests.expand

    def test_target_schema_binds_destination_cases_and_allows_one_to_five_exits(self):
        targets = [node(f"target_{index}", "ending") for index in range(6)]
        schema = RUNNER.scaffold_target_schema(targets)
        value = {"selection": {"targets": {}, "causal_job": "Synthetic backward assignment."}}
        for count in range(1, 6):
            value["selection"]["targets"] = {target["node_id"]: target["entry_cases"][0]["case_id"] for target in targets[:count]}
            RUNNER.validate_json_schema(value, schema)
        invalid = [None, {}, {"future_or_self": "unknown_case"},
            {targets[0]["node_id"]: targets[1]["entry_cases"][0]["case_id"]},
            {target["node_id"]: target["entry_cases"][0]["case_id"] for target in targets}]
        for choice in invalid:
            bad = {"selection": None if choice is None else {"targets": choice, "causal_job": "Synthetic assignment."}}
            with self.subTest(choice=choice), self.assertRaises(RUNNER.SchemaError):
                RUNNER.validate_json_schema(bad, schema)
        RUNNER.validate_json_schema({"selection": None}, RUNNER.scaffold_target_schema(targets, allow_finish=True))

    def test_model_can_finish_a_short_batch_without_filling_allocated_capacity(self):
        calls, base = self.provider()
        def request(run, step, prompt, schema, transport, **kwargs):
            if "_targets_" in step and self.allocated[1] in step:
                RUNNER.validate_json_schema({"selection": None}, schema)
                return {"selection": None}, {}
            return base(run, step, prompt, schema, transport, **kwargs)
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=request), mock.patch.object(
                RUNNER, "review_scaffold_connections", return_value=SUPPORTED):
            patch = self.expand(None)
            self.assertEqual(len(patch["nodes"]), 1)
            self.assertEqual(self.expand(None), patch)
        self.assertEqual(Counter(calls)["declare"], 1)

    def test_contract_text_rejects_reported_placeholders_and_serialized_metadata(self):
        bad = []
        for text in (",", " — … ", r'requirement_id\":\"scaffold_scene_00001_req_001',
                r'The reader arrives.\",\"requirement_id\":\"invented_id\"'):
            for field in ("guarantees", "preserves", "requirements"):
                value = compiler.declaration()
                if field == "requirements": value["entry_cases"][0][field] = [text]
                else: value[field] = [text]
                bad.append(value)
        duplicate = compiler.declaration(); duplicate["entry_cases"] = [{"requirements": []}, {"requirements": []}]; bad.append(duplicate)
        for value in bad:
            with self.subTest(value=value), self.assertRaises(RUNNER.SchemaError):
                RUNNER.compile_scaffold_declarations([value], self.allocated)
        seed = compiler.declaration() | {"terminal_role": "final", "attractor_id": "attractor_001",
            "prerequisite_obligation_ids": [], "guarantees": [","]}
        with self.assertRaisesRegex(RUNNER.SchemaError, "Malformed scaffold clause"):
            RUNNER.compile_scaffold_declarations([seed], self.allocated, seed=True)
        valid = compiler.declaration(); valid["guarantees"] = []; valid["entry_cases"] = [{"requirements": []}]
        RUNNER.compile_scaffold_declarations([valid], self.allocated)

    def test_capacity_rejects_fifth_case_before_binding_unconditional_destination(self):
        RUNNER.write_json(self.run / "run-manifest.json", RUNNER.derive_scope(8) | {"execution_policy": compiler.POLICY})
        calls, base = self.provider()
        def request(run, step, prompt, schema, transport, **kwargs):
            if "_declare_" in step:
                context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
                owner = context["source_node_id"]
                if owner in self.allocated[2:]:
                    value = compiler.declaration(owner)
                    value["entry_cases"] = [{"requirements": []}]
                    if owner == self.allocated[3]:
                        fields = schema["properties"]["nodes"]["items"]["properties"]
                        self.assertEqual(fields["entry_cases"]["maxItems"], 4)
                        five_cases = [{"requirements": [f"Condition {index}."]} for index in range(5)]
                        with self.assertRaises(RUNNER.SchemaError):
                            RUNNER.validate_json_schema({"nodes": [value | {"entry_cases": five_cases}]}, schema)
                        value["entry_cases"] = five_cases[:4]
                    kwargs["validator"]({"nodes": [value]})
                    return {"nodes": [value]}, {}
            return base(run, step, prompt, schema, transport, **kwargs)
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=request), mock.patch.object(
                RUNNER, "review_scaffold_connections", return_value=[]):
            patch = self.expand(None)
        self.assertEqual(len(patch["nodes"][-1]["entry_cases"]), 4)
        self.assertEqual(patch["nodes"][-1]["successors"][0]["supports"], [])
        self.assertNotIn(self.allocated[-1], calls)

    def test_binding_defect_replaces_owner_and_preserves_other_proofs(self):
        condition = "The witness displays the receipt."
        other = "The witness enters the gallery."
        for ending, text in zip(self.outcomes, (condition, other)):
            ending["entry_cases"][0]["requirements"] = [{"requirement_id": ending["node_id"] + "_req", "description": text}]
        calls, base = self.provider()
        requested = []
        def request(run, step, prompt, schema, transport, **kwargs):
            if "_connect_" in step:
                context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
                if context["predecessor"]["node_id"] == self.allocated[0]:
                    requested.append(context["requirements"])
                    answer = {"bindings": {identifier: ({"needs_guarantee": "The premise does not show the receipt."}
                        if description == condition else {"evidence_ids": ["commit_genesis"], "reason": "Preserved support."})
                        for identifier, description in context["requirements"].items()}}
                    RUNNER.validate_json_schema(answer, schema)
                    with self.assertRaises(RUNNER.SchemaError):
                        RUNNER.validate_json_schema({"contract_issue": {"fields": ["preserves"], "reason": "Missing guarantee"}}, schema)
                    return answer, {}
            return base(run, step, prompt, schema, transport, **kwargs)
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=request), mock.patch.object(
                RUNNER, "review_scaffold_connections", return_value=[]):
            patch = self.expand(None)
        self.assertEqual(len(requested), 1)
        source = patch["nodes"][0]
        self.assertIn(condition, [item["description"] for item in source["guarantees"]])
        first, second = source["successors"]
        self.assertTrue(first["supports"][0]["guarantee_ids"])
        self.assertEqual(second["supports"][0]["reason"], "Preserved support.")
        self.assertEqual(Counter(calls)["declare"], 5)

    def test_rejected_evidence_with_new_explanation_requires_new_guarantee(self):
        target = self.outcomes[0]
        condition = "The witness displays the receipt."
        requirement = {"requirement_id": "receipt_requirement", "description": condition}
        target["entry_cases"][0]["requirements"] = [requirement]
        calls, base = self.provider()
        def request(run, step, prompt, schema, transport, **kwargs):
            result, response = base(run, step, prompt, schema, transport, **kwargs)
            if "_connect_" in step:
                context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
                if context["rejected_evidence"]:
                    self.assertEqual(set(result["bindings"]), {requirement["requirement_id"]})
                    result["bindings"][requirement["requirement_id"]]["reason"] = "A different explanation of the same citation."
            return result, response
        issue = {"owner": self.allocated[0], "kind": "support", "requirement": requirement,
            "reason": "The Genesis premise does not show the receipt."}
        with mock.patch.object(RUNNER, "request_architecture_analysis", request), mock.patch.object(
                RUNNER, "review_scaffold_connections", side_effect=[[issue], []]):
            patch = self.expand(None)
        self.assertEqual(Counter(calls)[self.allocated[0]], 2)
        self.assertEqual(Counter(calls)["declare"], 5)
        self.assertEqual(patch["nodes"][0]["successors"][0]["supports"][0]["genesis_source_ids"], [])
        self.assertIn(condition, [item["description"] for item in patch["nodes"][0]["guarantees"]])

    def test_repair_limits_persist_after_alternate_assignment_fails(self):
        _calls, base = self.provider()
        def request(run, step, prompt, schema, transport, **kwargs):
            context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
            if "_targets_" in step and context["previous_targets"]:
                target = context["frontier_contracts"][0]
                result = {"selection": {"targets": {target["node_id"]: target["entry_cases"][0]["case_id"]},
                    "causal_job": "Different predecessor assignment."}}
            elif "_declare_" in step and context["previous_contract"]:
                if len(context["assignment"]["targets"]) == 2:
                    result = {"nodes": [context["previous_contract"]]}
                else:
                    result = {"nodes": [compiler.declaration("replacement " + str(context["assignment"]["targets"]),
                        requirement="Synthetic entry premise.")]}
            else:
                return base(run, step, prompt, schema, transport, **kwargs)
            RUNNER.validate_json_schema(result, schema)
            kwargs["validator"](result)
            return result, {}
        issue = {"owner": self.allocated[0], "kind": "contract", "reason": "The source cannot establish its promised event."}
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=request), mock.patch.object(
                RUNNER, "review_scaffold_connections", return_value=[issue]):
            with self.assertRaisesRegex(RUNNER.CathedralsError, "within the repair limits"):
                self.expand(None)
        checkpoint = RUNNER.read_json(self.run / ".staging/scaffold_expand_00001.contracts.json")
        self.assertEqual(checkpoint["repairs"][self.allocated[0]], ["replace", "retarget"])
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=AssertionError("Repeated terminal request")):
            with self.assertRaisesRegex(RUNNER.CathedralsError, "within the repair limits"):
                self.expand(None)

class ScaffoldCheckpointTests(unittest.TestCase):
    def setUp(self):
        fixtures.ReferenceResolutionTests.setUp(self)
        self.core = compiler.core_fixture()
        self.allocated = [f"scaffold_scene_{index:05d}" for index in range(1, 5)]
        self.state = {"nodes": [node(f"outcome_{index}", "ending") for index in (1, 2)], "round": 0}
        for patch in (mock.patch.object(RUNNER, "planning_core", return_value=self.core),
                mock.patch.object(RUNNER, "genesis_reference_catalog", return_value=compiler.GENESIS),
                mock.patch.object(RUNNER, "committed_record", return_value={})):
            patch.start(); self.addCleanup(patch.stop)

    def checkpoint_replay(self, phase):
        calls, interrupted = [], [False]
        def transport(_method, _url, request, **kwargs):
            fields = request["response_format"]["json_schema"]["schema"]["properties"]
            context = json.loads(request["messages"][1]["content"].split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
            if "selection" in fields:
                calls.append("targets")
                targets = context["frontier_contracts"]
                scenes = [item for item in targets if item["kind"] == "scene"]
                chosen = scenes[-1:] if scenes else targets
                value = {"selection": {"targets": {item["node_id"]: item["entry_cases"][0]["case_id"] for item in chosen},
                    "causal_job": "Synthetic backward assignment."}}
            elif "nodes" in fields:
                calls.append("declare")
                value = {"nodes": [compiler.declaration(requirement="Synthetic entry premise.")]}
            else:
                calls.append("connect")
                value = {"bindings": {key: {"evidence_ids": ["commit_genesis"], "reason": "Synthetic evidence."}
                    for key in context["requirements"]}}
            return fixtures.api_response(value)
        write = RUNNER.write_json
        def interrupt_write(path, value, **kwargs):
            if path.name == "scaffold_expand_00001.contracts.json" and not interrupted[0] and calls and calls[-1] == phase:
                interrupted[0] = True
                raise KeyboardInterrupt()
            return write(path, value, **kwargs)
        def expand():
            return RUNNER.prepare_scaffold_expansion(self.run, self.state, self.core,
                [item["node_id"] for item in self.state["nodes"]], self.allocated, transport)
        with mock.patch.object(RUNNER, "review_scaffold_connections", return_value=[]), mock.patch.object(
                RUNNER, "write_json", side_effect=interrupt_write):
            with self.assertRaises(KeyboardInterrupt):
                expand()
            originals = {path: path.read_bytes() for path in (self.run / "raw").glob("*.api.json")}
            prefix = (self.run / "ledger.jsonl").read_bytes()
            result = expand()
        self.assertEqual(Counter(calls), Counter({"targets": 4, "declare": 4, "connect": 3}))
        self.assertEqual([item["node_id"] for item in result["nodes"]], self.allocated)
        self.assertTrue((self.run / "ledger.jsonl").read_bytes().startswith(prefix))
        for path, original in originals.items():
            self.assertEqual(path.read_bytes(), original)
        state = RUNNER.load_state(self.run)
        self.assertEqual((state["input_tokens"], state["output_tokens"], state["analysis_step_count"]),
            (11 * len(calls), 7 * len(calls), len(calls)))

    def test_accepted_target_replays_without_another_call(self):
        self.checkpoint_replay("targets")

    def test_accepted_declaration_replays_without_another_call(self):
        self.checkpoint_replay("declare")

    def test_accepted_binding_replays_without_another_call(self):
        self.checkpoint_replay("connect")


if __name__ == "__main__":
    unittest.main()
