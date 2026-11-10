"""Scaffold compiler regressions; no live model is required."""
import copy
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

from test_cathedrals import RUNNER
from test_backward_scaffold import POLICY, core_fixture, node


GENESIS = {"commit_genesis": "Synthetic immutable premise."}


def declaration(label="one", *, requirement="Synthetic continuity."):
    return {"arc_id": "arc_001", "purpose": f"Synthetic purpose {label}.", "intended_change": f"Synthetic change {label}.",
        "entry_cases": [{"requirements": [requirement]}], "guarantees": ["Synthetic continuity."], "preserves": []}


def selection(source, targets):
    evidence = source["guarantees"][0]["requirement_id"] if source["guarantees"] else "commit_genesis"
    return {"connections": {target["node_id"]: {"entry_case_id": target["entry_cases"][0]["case_id"],
        "supports": {requirement["requirement_id"]: {"evidence_ids": [evidence], "reason": "Synthetic support."}
            for requirement in target["entry_cases"][0]["requirements"]}} for target in targets}}


class ScaffoldCompilerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        self.run = Path(temporary.name); (self.run / ".staging").mkdir()
        RUNNER.write_json(self.run / "run-manifest.json", RUNNER.derive_scope(150) | {"execution_policy": POLICY})
        RUNNER.write_json(self.run / "generation-brief.json", {"generation_seed": "synthetic_seed"})
        self.core = core_fixture()
        self.allocated = [f"scaffold_scene_{index:05d}" for index in range(1, 5)]
        self.outcomes = [node(f"scaffold_outcome_{index:04d}", "ending") for index in (1, 2)]
        self.state = {"version": 1, "round": 0, "nodes": self.outcomes, "complete": False,
            "opening_node_id": None, "opening_support": [], "outcomes_complete": True}
        for patch in (mock.patch.object(RUNNER, "planning_core", return_value=self.core),
                mock.patch.object(RUNNER, "genesis_reference_catalog", return_value=GENESIS),
                mock.patch.object(RUNNER, "committed_record", return_value={}),
                mock.patch.object(RUNNER, "preserve_planning_result")):
            patch.start(); self.addCleanup(patch.stop)

    def test_declaration_ids_are_assigned_by_owner_and_revision(self):
        wire = [declaration(), declaration()]
        nodes = RUNNER.compile_scaffold_declarations(wire, self.allocated)
        identities = [identifier for item in nodes for identifier in [item["node_id"], item["entry_cases"][0]["case_id"],
            item["entry_cases"][0]["requirements"][0]["requirement_id"], item["guarantees"][0]["requirement_id"]]]
        self.assertEqual(len(identities), len(set(identities)))
        revised = RUNNER.compile_scaffold_declarations(wire, self.allocated, revisions={self.allocated[0]: 1})
        self.assertEqual(nodes[1], revised[1]); self.assertEqual(nodes[0]["node_id"], revised[0]["node_id"])
        self.assertNotEqual(nodes[0]["entry_cases"], revised[0]["entry_cases"])
        bad = {"nodes": [declaration() | {"node_id": "invented_node"}]}
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_json_schema(bad, RUNNER.scaffold_declaration_schema(self.run, 4))

    def test_destination_case_requirement_and_evidence_are_bound_together(self):
        source, target = RUNNER.compile_scaffold_declarations([declaration("source"), declaration("target")], self.allocated)
        valid = selection(source, [target]); schema = RUNNER.scaffold_connection_schema(source, [target], GENESIS)
        RUNNER.validate_json_schema(valid, schema)
        compiled = RUNNER.compile_scaffold_connections(source, [target], valid, GENESIS)
        edge = compiled["successors"][0]
        self.assertEqual(edge["target_case_id"], target["entry_cases"][0]["case_id"])
        self.assertEqual(edge["supports"][0]["requirement_id"], target["entry_cases"][0]["requirements"][0]["requirement_id"])
        self.assertEqual(edge["supports"][0]["guarantee_ids"], [source["guarantees"][0]["requirement_id"]])
        for mistake in ("source_case", "source_requirement", "foreign_guarantee", "empty_evidence", "early_complete", "unknown_destination"):
            bad = copy.deepcopy(valid); value = bad["connections"][target["node_id"]]
            if mistake == "source_case": value["entry_case_id"] = source["entry_cases"][0]["case_id"]
            elif mistake == "source_requirement":
                value["supports"] = {source["entry_cases"][0]["requirements"][0]["requirement_id"]: next(iter(value["supports"].values()))}
            elif mistake == "foreign_guarantee": next(iter(value["supports"].values()))["evidence_ids"] = [target["guarantees"][0]["requirement_id"]]
            elif mistake == "empty_evidence": next(iter(value["supports"].values()))["evidence_ids"] = []
            elif mistake == "early_complete": bad["complete"] = True
            else: bad["connections"]["unknown_scene"] = bad["connections"].pop(target["node_id"])
            with self.subTest(mistake=mistake), self.assertRaises(RUNNER.SchemaError):
                RUNNER.validate_json_schema(bad, schema)

    def test_connection_schema_does_not_repeat_the_evidence_catalog_per_requirement(self):
        declarations = [declaration(str(index)) for index in range(4)]
        declarations[1]["entry_cases"] = [{"requirements": [f"Synthetic case {case} condition {index}." for index in range(8)]} for case in range(5)]
        nodes = RUNNER.compile_scaffold_declarations(declarations, self.allocated)
        schema = RUNNER.scaffold_connection_schema(nodes[0], nodes[1:], GENESIS)
        self.assertEqual(json.dumps(schema).count('"commit_genesis"'), 1)
        RUNNER.validate_json_schema(selection(nodes[0], nodes[1:]), schema)

    def test_connection_errors_report_the_selected_shape_instead_of_requesting_an_amendment(self):
        source, target = RUNNER.compile_scaffold_declarations([declaration("source"), declaration("target")], self.allocated)
        schema = RUNNER.scaffold_connection_schema(source, [target], GENESIS)
        malformed = {"connections": {target["node_id"]: {"entry_case_id": source["entry_cases"][0]["case_id"],
            "supports": {"wrong_requirement": {"evidence_ids": [], "reason": ""}}}}}
        with self.assertRaises(RUNNER.SchemaError) as error: RUNNER.validate_json_schema(malformed, schema)
        self.assertIn("entry_case_id", error.exception.reason)
        self.assertNotIn("contract_issue", error.exception.reason)

    def test_linear_connections_and_five_destination_ceiling(self):
        source = RUNNER.compile_scaffold_declarations([declaration()], self.allocated)[0]
        targets = [node(f"known_target_{index}", "ending") for index in range(6)]
        for count in (1, 2, 5):
            RUNNER.validate_json_schema(selection(source, targets[:count]), RUNNER.scaffold_connection_schema(source, targets, GENESIS))
        with self.assertRaisesRegex(RUNNER.SchemaError, "at most 5 properties"):
            RUNNER.validate_json_schema(selection(source, targets), RUNNER.scaffold_connection_schema(source, targets, GENESIS))

    def test_duplicate_json_properties_are_rejected_in_plain_and_fenced_responses(self):
        for text in ('{"connections":{},"connections":{"a":1}}', '```json\n{"a":1,"a":2}\n```'):
            with self.subTest(text=text), self.assertRaisesRegex(RUNNER.SchemaError, "duplicate JSON property"):
                RUNNER.parse_structured_content(text)

    def provider(self, *, interrupt=None):
        calls, interrupted = [], [False]
        def request(_run, step, prompt, schema, _transport, **kwargs):
            context = json.loads(prompt.split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
            if "_targets_" in step:
                calls.append("targets")
                earlier = [target for target in context["frontier_contracts"] if target["kind"] == "scene"]
                chosen = earlier[-1:] if earlier else context["frontier_contracts"]
                result = {"selection": {"targets": {target["node_id"]: target["entry_cases"][0]["case_id"] for target in chosen},
                    "causal_job": "Synthetic predecessor assignment."}}
            elif "_declare_" in step:
                calls.append("declare")
                authored = declaration(context["source_node_id"], requirement="Synthetic entry premise.")
                authored["guarantees"] += context["required_exit_guarantees"]
                result = {"nodes": [authored]}
            elif "_connect_" in step:
                owner = context["predecessor"]["node_id"]
                calls.append(owner)
                if owner == interrupt and not interrupted[0]:
                    interrupted[0] = True
                    raise RUNNER.PausedError("Scaffold connections", "Synthetic interruption")
                result = {"bindings": {identifier: {"evidence_ids": ["commit_genesis"],
                    "reason": "Synthetic premise support."} for identifier in context["requirements"]}}
            else:
                raise AssertionError("Unexpected provider request: " + step)
            RUNNER.validate_json_schema(result, schema)
            if kwargs.get("validator"):
                kwargs["validator"](result)
            return result, {}
        return calls, request

    def expand(self, provider):
        return RUNNER.prepare_scaffold_expansion(self.run, self.state, self.core,
            [node["node_id"] for node in self.outcomes], self.allocated, provider)

    def test_connections_resume_without_redeclaring_or_repeating_accepted_work(self):
        calls, provider = self.provider(interrupt=self.allocated[2])
        review = []
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=provider), mock.patch.object(
                RUNNER, "review_scaffold_connections", return_value=review):
            with self.assertRaisesRegex(RUNNER.PausedError, "Synthetic interruption"): self.expand(None)
            checkpoint = RUNNER.read_json(self.run / ".staging/scaffold_expand_00001.contracts.json")
            self.assertEqual(len(checkpoint["declarations"]), 3); self.assertEqual(len(checkpoint["assignments"]), 3)
            self.assertEqual(sum(bool(value) for value in checkpoint["bindings"].values()), 1)
            result = self.expand(None)
        self.assertEqual(Counter(calls), Counter({"targets": 4, "declare": 4, self.allocated[1]: 1, self.allocated[2]: 2, self.allocated[3]: 1}))
        self.assertFalse(result["complete"])
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=AssertionError("Repeated accepted request")), mock.patch.object(
                RUNNER, "review_scaffold_connections", side_effect=AssertionError("Repeated accepted review")):
            self.assertEqual(self.expand(None), result)
        with self.assertRaisesRegex(RUNNER.IntegrityError, "different planner, frontier"):
            changed = copy.deepcopy(self.state); changed["nodes"][0]["purpose"] = "Changed checkpoint input."
            RUNNER.prepare_scaffold_expansion(self.run, changed, self.core, [node["node_id"] for node in self.outcomes], self.allocated, None)

    def test_outcomes_targets_declarations_connections_and_opening_compile_together(self):
        RUNNER.write_json(self.run / ".staging/architecture_core.planning.json", {"record": self.core, "payload": {}})
        calls, base_provider = self.provider()
        def provider(run, step, prompt, schema, transport, **kwargs):
            if step.startswith("scaffold_outcomes_"):
                result = {"nodes": [declaration(f"outcome_{index}") | {"terminal_role": "final" if index == 0 else "premature",
                    "attractor_id": "attractor_001", "prerequisite_obligation_ids": []} for index in range(2)], "complete": True}
            elif "_opening_" in step:
                context = json.loads(prompt.split("\n", 1)[1]); case = context["opening"]["entry_cases"][0]
                result = {"opening": {"supports": {requirement["requirement_id"]: {
                    "evidence_ids": ["commit_genesis"], "reason": "Synthetic Genesis grounding."} for requirement in case["requirements"]}}}
            else:
                return base_provider(run, step, prompt, schema, transport, **kwargs)
            RUNNER.validate_json_schema(result, schema)
            if kwargs.get("validator"): kwargs["validator"](result)
            return result, {}
        def save(run, step, draft): RUNNER.write_json(run / ".staging" / f"{step}.planning.json", draft)
        review = []
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=provider), mock.patch.object(
                RUNNER, "review_scaffold_connections", return_value=review), mock.patch.object(RUNNER, "save_planning_draft", side_effect=save):
            compiled = RUNNER.prepare_causal_scaffold(self.run, self.core, None)
        RUNNER.validate_json_schema(compiled["causal_scaffold"], RUNNER.definition_schema("causalScaffold"))
        RUNNER.validate_scaffold(compiled["causal_scaffold"], RUNNER.derive_scope(150)["scope"], set(GENESIS), complete=True)
        self.assertEqual(compiled["scope_commitment"]["planned_scene_count"], 8)
        self.assertEqual(compiled["scope_commitment"]["planned_ending_count"], 2)
        self.assertEqual(Counter(calls)["declare"], 8)

    def test_opening_is_only_offered_after_global_structural_readiness(self):
        outcomes = copy.deepcopy(self.outcomes)
        scenes = RUNNER.compile_scaffold_declarations([declaration(str(index)) for index in range(8)],
            [f"scaffold_scene_{index:05d}" for index in range(1, 9)])
        for index, source in enumerate(scenes):
            target = scenes[index - 1:index] if index else outcomes
            scenes[index] = RUNNER.compile_scaffold_connections(source, target, selection(source, target), GENESIS)
        base = self.state | {"nodes": outcomes + scenes[:-1]}
        self.assertEqual(RUNNER.scaffold_opening_candidate(base, scenes[-1:])["node_id"], scenes[-1]["node_id"])
        self.assertIsNone(RUNNER.scaffold_opening_candidate(self.state, scenes[:4]))
        broken = copy.deepcopy(base); broken["nodes"][0]["entry_cases"].append({"case_id": "missing_alternative", "requirements": []})
        self.assertIsNone(RUNNER.scaffold_opening_candidate(broken, scenes[-1:]))

    def test_audit_task_schema_prevents_cross_case_and_cross_route_answers(self):
        tasks = {"task_left": {"source_ids": ["left_source"]}, "task_right": {"source_ids": ["right_source"]}}
        valid = {"tasks": {identifier: {"supported": True, "reason": "Synthetic support.",
            "evidence_quotes": [{"source_id": task["source_ids"][0], "quote": "Synthetic evidence."}]} for identifier, task in tasks.items()}}
        schema = RUNNER.scaffold_audit_task_schema(tasks); RUNNER.validate_json_schema(valid, schema)
        for issue in ("wrong_source", "wrong_task", "missing_task", "invented_case", "empty_evidence"):
            bad = copy.deepcopy(valid)
            if issue == "wrong_source": bad["tasks"]["task_left"]["evidence_quotes"][0]["source_id"] = "right_source"
            elif issue == "wrong_task": bad["tasks"]["invented_task"] = bad["tasks"].pop("task_left")
            elif issue == "missing_task": del bad["tasks"]["task_right"]
            elif issue == "invented_case": bad["tasks"]["task_left"]["case_id"] = "wrong_case"
            else: bad["tasks"]["task_left"]["evidence_quotes"] = []
            with self.subTest(issue=issue), self.assertRaises(RUNNER.SchemaError): RUNNER.validate_json_schema(bad, schema)

    def test_audit_tasks_page_and_compile_back_to_the_saved_receipt_format(self):
        checks = [(f"synthetic_check_{index}", "Synthetic hard promise.") for index in range(9)]
        entries = [("case_one", "source_one"), ("case_two", "source_two")]
        permitted = {entry: {entry[1]} for entry in entries}
        units = {"source_one": ["Synthetic left evidence."], "source_two": ["Synthetic right evidence."]}
        contract = node("synthetic_scene"); contract["entry_cases"] = [{"case_id": case, "requirements": []} for case, _entry in entries]
        local = {"incoming": [], "inherited_guarantee_evidence": [], "opening_support": []}
        sizes = []
        def request(_run, _step, _prompt, schema, _transport, **kwargs):
            fields = schema["properties"]["tasks"]["properties"]; sizes.append(len(fields))
            result = {"tasks": {identifier: {"supported": True, "reason": "Synthetic source support.", "evidence_quotes": [{
                "source_id": fields[identifier]["properties"]["evidence_quotes"]["items"]["properties"]["source_id"]["enum"][0],
                "quote": units[fields[identifier]["properties"]["evidence_quotes"]["items"]["properties"]["source_id"]["enum"][0]][0]}]} for identifier in fields}}
            RUNNER.validate_json_schema(result, schema); kwargs["validator"](result)
            return result, {}
        before = copy.deepcopy(units)
        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=request):
            result, response = RUNNER.request_scaffold_audit_tasks(self.run, "synthetic_step", "synthetic_audit", contract, local,
                checks, entries, permitted, units, None)
        self.assertEqual(sizes, [8, 8, 2]); self.assertEqual(len(result["checks"]), 18)
        self.assertEqual({(item["check_id"], item["case_id"], item["entry_from_slot"]) for item in result["checks"]},
            {(check, case, entry) for check, _description in checks for case, entry in entries})
        self.assertEqual(response["_cathedrals_request"]["parameters"]["assembly"], "scaffold_audit_tasks")
        self.assertEqual(units, before)


if __name__ == "__main__":
    unittest.main()
