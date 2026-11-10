"""Target-first planning, contract integrity and bounded local recovery."""
import copy
import json
import unittest
from collections import Counter
from unittest import mock

from test_cathedrals import RUNNER
from test_backward_scaffold import node
import test_scaffold_compiler as compiler
import test_reference_resolution as fixtures


SUPPORTED = {"supported": True, "reason": "Synthetic supported expansion.", "contract_repairs": {}, "connection_repairs": {}}


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

    def test_each_contract_follows_its_assignment_and_bindings_cannot_switch_cases(self):
        calls, base = self.provider()
        order = []
        def request(run, step, prompt, schema, transport, **kwargs):
            context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
            if "_targets_" in step:
                order.append("targets")
                source = context["source_node_id"]
                self.assertTrue(all(target["node_id"] < source for target in context["frontier_contracts"] if target["kind"] == "scene"))
            elif "_declare_" in step:
                order.append("declare")
                self.assertEqual(set(context["assignment"]["targets"]), {target["node_id"] for target in context["successor_interfaces"]})
            else:
                order.append("connect")
                fields = schema["anyOf"][0]["properties"]["connections"]
                self.assertEqual(set(fields["required"]), set(context["assignment"]["targets"]))
                for target in context["successor_interfaces"]:
                    self.assertEqual(len(target["entry_cases"]), 1)
                    bound = fields["properties"][target["node_id"]]["anyOf"][0]["properties"]["entry_case_id"]["const"]
                    self.assertEqual(bound, context["assignment"]["targets"][target["node_id"]])
            return base(run, step, prompt, schema, transport, **kwargs)
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=request), mock.patch.object(
                RUNNER, "review_scaffold_connections", return_value=SUPPORTED), mock.patch("builtins.input", side_effect=AssertionError("Human choice requested")):
            patch = self.expand(None)
        self.assertEqual(order, ["targets", "declare", "connect"] * 4)
        self.assertEqual(len(patch["nodes"][0]["successors"]), 2)
        self.assertTrue(all(len(item["successors"]) == 1 for item in patch["nodes"][1:]))

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

    def test_amendments_require_progress_and_cannot_leave_missing_guarantees_empty(self):
        prior = compiler.declaration(); prior["guarantees"] = []
        original = copy.deepcopy(prior)
        for amendment in ({"guarantees": []}, {"purpose": "  " + prior["purpose"] + "\n"},
                {"guarantees": [], "preserves": ["A different preserved condition."]},
                {"guarantees": [","], "preserves": ["A changed condition."]}):
            with self.subTest(amendment=amendment), self.assertRaises(RUNNER.SchemaError):
                RUNNER.validate_scaffold_amendment(prior, amendment)
        fixed = RUNNER.validate_scaffold_amendment(prior, {"guarantees": ["The scene establishes the required evidence."]})
        self.assertEqual(fixed["purpose"], prior["purpose"])
        self.assertEqual(prior, original)

    def local_replan_provider(self, *, still_unsupported=False):
        calls, base = self.provider()
        first = [True]
        def request(run, step, prompt, schema, transport, **kwargs):
            if "_amend_" in step:
                calls.append("ineffective_amendment")
                raise RUNNER.PausedError("Scaffold contract amendment", "No-op scaffold amendment exhausted focused attempts")
            if "_connect_" in step:
                context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
                if context["predecessor"]["node_id"] == self.allocated[0] and (still_unsupported or not context["predecessor"]["guarantees"]):
                    result = {"contract_issue": {"fields": ["guarantees"], "reason": "This predecessor must establish its successor condition."}}
                    RUNNER.validate_json_schema(result, schema)
                    return result, {}
            result, response = base(run, step, prompt, schema, transport, **kwargs)
            if "_declare_" in step and self.allocated[0] in step and first[0]:
                first[0] = False
                result["nodes"][0]["guarantees"] = []
                kwargs["validator"](result)
            return result, response
        return calls, request

    def test_ineffective_amendment_redeclares_only_the_failed_predecessor(self):
        calls, request = self.local_replan_provider()
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=request), mock.patch.object(
                RUNNER, "review_scaffold_connections", return_value=SUPPORTED):
            patch = self.expand(None)
        checkpoint = RUNNER.read_json(self.run / ".staging/scaffold_expand_00001.contracts.json")
        self.assertEqual(Counter(calls)["declare"], 5)
        self.assertEqual(Counter(calls)["targets"], 5)
        self.assertEqual(checkpoint["revisions"], {self.allocated[0]: 1})
        self.assertEqual([item["node_id"] for item in patch["nodes"]], self.allocated)
        self.assertEqual(len([item for item in checkpoint["history"] if item.get("kind") == "redeclaration"]), 1)

    def test_a_failed_local_redeclaration_pauses_instead_of_repeating_indefinitely(self):
        calls, request = self.local_replan_provider(still_unsupported=True)
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=request), self.assertRaisesRegex(
                RUNNER.PausedError, "bounded local re-declaration"):
            self.expand(None)
        checkpoint = RUNNER.read_json(self.run / ".staging/scaffold_expand_00001.contracts.json")
        self.assertEqual(Counter(calls)["declare"], 2)
        self.assertEqual(checkpoint["revisions"], {self.allocated[0]: 1})

    def test_changed_entry_conditions_redeclare_the_consumer_and_preserve_other_branches(self):
        calls, base = self.provider()
        original_branch = []
        def request(run, step, prompt, schema, transport, **kwargs):
            if "_targets_" in step:
                calls.append("targets")
                context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
                source = context["source_node_id"]; index = self.allocated.index(source)
                target_id = self.outcomes[index // 2]["node_id"] if index % 2 == 0 else self.allocated[index - 1]
                target = next(item for item in context["frontier_contracts"] if item["node_id"] == target_id)
                result = {"selection": {"targets": {target_id: target["entry_cases"][0]["case_id"]}, "causal_job": "Synthetic separate branch."}}
            elif "_amend_" in step:
                calls.append("amend")
                result = {self.allocated[0]: {"entry_cases": [{"requirements": ["Synthetic revised entry condition."]}]}}
            elif "_declare_" in step and self.allocated[1] in step and "reselect and redeclare" in prompt:
                calls.append("declare")
                result = {"nodes": [compiler.declaration("revised_consumer", requirement="Synthetic earlier condition.")]}
            else:
                return base(run, step, prompt, schema, transport, **kwargs)
            RUNNER.validate_json_schema(result, schema)
            if kwargs.get("validator"): kwargs["validator"](result)
            return result, {}
        def review(_run, _step, patch, *_args):
            if not original_branch:
                original_branch.extend(copy.deepcopy(patch["nodes"][2:]))
                return {"supported": False, "reason": "A new entry condition is needed.",
                    "contract_repairs": {self.allocated[0]: ["entry_cases"]}, "connection_repairs": {}}
            return SUPPORTED
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=request), mock.patch.object(
                RUNNER, "review_scaffold_connections", side_effect=review):
            patch = self.expand(None)
        self.assertEqual(patch["nodes"][2:], original_branch)
        self.assertEqual(Counter(calls)["declare"], 5)
        self.assertEqual([Counter(calls)[identifier] for identifier in self.allocated], [2, 2, 1, 1])
        checkpoint = RUNNER.read_json(self.run / ".staging/scaffold_expand_00001.contracts.json")
        self.assertEqual(checkpoint["revisions"], {self.allocated[0]: 1, self.allocated[1]: 1})
        self.assertFalse(checkpoint["pending"])

    def test_incompatible_target_rejection_can_retarget_one_uncommitted_predecessor(self):
        calls, base = self.provider()
        reviews = []
        def request(run, step, prompt, schema, transport, **kwargs):
            if "_amend_" in step:
                raise RUNNER.PausedError("Scaffold contract amendment", "Focused fields cannot resolve the incompatible branch assignment")
            if "_targets_" in step and self.allocated[0] in step:
                context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
                if context["previous_contract"] is not None:
                    calls.append("targets")
                    target = context["frontier_contracts"][0]
                    return {"selection": {"targets": {target["node_id"]: target["entry_cases"][0]["case_id"]},
                        "causal_job": "Earn one compatible outcome instead of incompatible exclusive decisions."}}, {}
            if "_declare_" in step and self.allocated[0] in step and "previous_contract\":null" not in prompt:
                calls.append("declare")
                result = {"nodes": [compiler.declaration("compatible_predecessor")]}
                RUNNER.validate_json_schema(result, schema); kwargs["validator"](result)
                return result, {}
            return base(run, step, prompt, schema, transport, **kwargs)
        def review(_run, _step, patch, *_args):
            reviews.append(copy.deepcopy(patch))
            if len(patch["nodes"][0]["successors"]) > 1:
                return {"supported": False, "reason": "These target cases require mutually exclusive decisions.",
                    "contract_repairs": {self.allocated[0]: ["purpose", "guarantees"]}, "connection_repairs": {}}
            return SUPPORTED
        original_outcomes = copy.deepcopy(self.state["nodes"])
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=request), mock.patch.object(
                RUNNER, "review_scaffold_connections", side_effect=review):
            patch = self.expand(None)
        self.assertEqual(len(reviews), 2)
        self.assertEqual(len(reviews[0]["nodes"][0]["successors"]), 2)
        self.assertEqual(len(patch["nodes"][0]["successors"]), 1)
        self.assertEqual(self.state["nodes"], original_outcomes)

    def test_cycle_exhaustion_reports_the_evaluated_revision_without_a_final_unreviewed_edit(self):
        calls, base = self.provider()
        def request(run, step, prompt, schema, transport, **kwargs):
            if "_declare_" in step and self.allocated[0] in step:
                context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
                if context["previous_contract"] is not None:
                    calls.append("declare")
                    result = {"nodes": [compiler.declaration("redeclaration_after_repeated_rejection")]}
                    kwargs["validator"](result)
                    return result, {}
            return base(run, step, prompt, schema, transport, **kwargs)
        review = {"supported": False, "reason": "The selected evidence still does not earn this transition.",
            "contract_repairs": {}, "connection_repairs": {self.allocated[0]: [self.outcomes[0]["node_id"]]}}
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=request), mock.patch.object(
                RUNNER, "review_scaffold_connections", return_value=review) as reviews, self.assertRaisesRegex(
                RUNNER.PausedError, "Four scaffold repair cycles.*Last evaluated revisions"):
            self.expand(None)
        self.assertEqual(reviews.call_count, 4)
        checkpoint = RUNNER.read_json(self.run / ".staging/scaffold_expand_00001.contracts.json")
        self.assertEqual(checkpoint["last_review"]["revisions"], checkpoint["revisions"])
        self.assertNotIn("accepted_patch", checkpoint)
        self.assertEqual(Counter(calls)["declare"], 5)


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
            schema = request["response_format"]["json_schema"]["schema"]
            fields = schema.get("properties", schema.get("anyOf", [{}])[0].get("properties", {}))
            prompt = request["messages"][1]["content"]
            if "selection" in fields:
                calls.append("targets")
                context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
                targets = context["frontier_contracts"]; scenes = [item for item in targets if item["kind"] == "scene"]
                targets = scenes[-1:] if scenes else targets
                value = {"selection": {"targets": {item["node_id"]: item["entry_cases"][0]["case_id"] for item in targets},
                    "causal_job": "Synthetic backward assignment."}}
            elif "nodes" in fields:
                calls.append("declare")
                context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
                value = {"nodes": [compiler.declaration(context["source_node_id"])]}
            elif "connections" in fields:
                calls.append("connect")
                context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
                value = compiler.selection(context["predecessor"], context["successor_interfaces"])
            else:
                calls.append("amend")
                value = {identifier: {"guarantees": ["Synthetic amended guarantee."]} for identifier in fields}
            return fixtures.api_response(value)
        def review(_run, _step, patch, *_args):
            if phase == "amend" and patch["nodes"][0]["guarantees"][0]["description"] != "Synthetic amended guarantee.":
                return {"supported": False, "reason": "The first guarantee needs correction.",
                    "contract_repairs": {self.allocated[0]: ["guarantees"]}, "connection_repairs": {}}
            return SUPPORTED
        write = RUNNER.write_json
        def interrupt_write(path, value, **kwargs):
            if path.name == "scaffold_expand_00001.contracts.json" and not interrupted[0]:
                ready = (phase == "targets" and len(value["assignments"]) == 1 and not value["declarations"] or
                    phase == "declare" and len(value["declarations"]) == 1 and not value["connections"] or
                    phase == "amend" and value["revisions"].get(self.allocated[0]) == 1)
                if ready:
                    interrupted[0] = True
                    raise KeyboardInterrupt("Synthetic accepted-response/checkpoint interruption")
            return write(path, value, **kwargs)
        expand = lambda: RUNNER.prepare_scaffold_expansion(self.run, self.state, self.core,
            [item["node_id"] for item in self.state["nodes"]], self.allocated, transport)
        with mock.patch.object(RUNNER, "review_scaffold_connections", side_effect=review), mock.patch.object(RUNNER, "write_json", side_effect=interrupt_write):
            with self.assertRaises(KeyboardInterrupt): expand()
            originals = {path: path.read_bytes() for path in (self.run / "raw").glob("*.api.json")}
            prefix = (self.run / "ledger.jsonl").read_bytes()
            result = expand()
        self.assertEqual(Counter(calls)["targets"], 4)
        self.assertEqual(Counter(calls)["declare"], 4)
        self.assertEqual(Counter(calls)["connect"], 6 if phase == "amend" else 4)
        self.assertEqual(Counter(calls)["amend"], 1 if phase == "amend" else 0)
        self.assertEqual([item["node_id"] for item in result["nodes"]], self.allocated)
        self.assertTrue((self.run / "ledger.jsonl").read_bytes().startswith(prefix))
        for path, original in originals.items(): self.assertEqual(path.read_bytes(), original)
        state = RUNNER.load_state(self.run)
        self.assertEqual((state["input_tokens"], state["output_tokens"], state["analysis_step_count"]), (11 * len(calls), 7 * len(calls), len(calls)))

    def test_accepted_target_selection_replays_without_another_call(self): self.checkpoint_replay("targets")
    def test_accepted_declaration_replays_without_another_call(self): self.checkpoint_replay("declare")
    def test_accepted_amendment_replays_without_another_call(self): self.checkpoint_replay("amend")


if __name__ == "__main__":
    unittest.main()
