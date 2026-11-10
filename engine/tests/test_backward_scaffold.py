"""Backward scaffold regressions. Operator-run only; no live provider is used."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_cathedrals import ROOT, RUNNER, architecture_core_payload, empty_delta
from test_completion_contract import scene_payload
from test_scale_rehearsal import scale_web_fixture


POLICY = RUNNER.CURRENT_EXECUTION_POLICY.copy()


def node(identifier, kind="scene", cases=None):
    return {"node_id": identifier, "kind": kind, "terminal_role": "final" if kind == "ending" else "none",
        "arc_id": "arc_001", "attractor_id": "attractor_001" if kind == "ending" else None,
        "purpose": f"Synthetic purpose {identifier}.", "intended_change": f"Synthetic development {identifier}.",
        "entry_cases": cases or [{"case_id": identifier + "_entry", "requirements": []}],
        "guarantees": [], "preserves": [], "successors": [], "prerequisite_obligation_ids": []}


def link(source, target, case=0, supports=None):
    source["successors"].append({"to_node_id": target["node_id"], "target_case_id": target["entry_cases"][case]["case_id"],
        "supports": supports or []})


def mixed_scaffold(count=8):
    scenes = [node(f"scaffold_scene_{index:05d}") for index in range(1, count + 1)]
    early, final = node("scaffold_outcome_0001", "ending"), node("scaffold_outcome_0002", "ending")
    early["terminal_role"] = "premature"
    link(scenes[0], scenes[1])  # One authored continuation, not a forced choice.
    link(scenes[1], scenes[2]); link(scenes[1], scenes[3]); link(scenes[1], early)
    scenes[4]["entry_cases"] = [{"case_id": "merge_left", "requirements": []}, {"case_id": "merge_right", "requirements": []}]
    link(scenes[2], scenes[4], 0); link(scenes[3], scenes[4], 1)
    for source, target in zip(scenes[4:], scenes[5:]):
        link(source, target)
    link(scenes[-1], final)
    scenes[0]["entry_cases"][0]["requirements"] = [{"requirement_id": "opening_genesis", "description": "The synthetic Genesis premise applies."}]
    value = {"version": 1, "opening_node_id": scenes[0]["node_id"], "opening_support": [{"requirement_id": "opening_genesis",
        "guarantee_ids": [], "genesis_source_ids": ["commit_genesis"], "reason": "Synthetic committed premise."}], "nodes": scenes + [early, final]}
    order, _roots = RUNNER.scaffold_order(value["nodes"])
    kinds = {item["node_id"]: item["kind"] for item in value["nodes"]}
    counters, slots = {"scene": 0, "ending": 0}, {}
    for identifier in order:
        kind = kinds[identifier]; counters[kind] += 1
        slots[identifier] = f"{kind}_slot_{counters[kind]:04d}"
    return value | {"slot_ids": slots}


def core_fixture(scaffold=None, cap=150):
    payload = architecture_core_payload()
    commitment = {"possible_scene_count": cap, "planned_scene_count": cap,
        "planned_ending_count": RUNNER.derive_scope(cap)["scope"]["ending_target"],
        "planned_artifact_count": RUNNER.derive_scope(cap)["scope"]["artifact_target"],
        "planned_formal_composition_count": RUNNER.derive_scope(cap)["scope"]["formal_composition_target"],
        "saturation_rationale": payload.pop("saturation_rationale")}
    core = payload | {"record_type": "architecture_core", "protocol_version": "6.0", "generation_id": "synthetic_run",
        "commit_id": "commit_core", "genesis_commit_id": "commit_genesis", "story_format": "web",
        "scope_commitment": commitment, "constraint_delta": empty_delta(), "topology": RUNNER.scaffold_macro_topology()}
    core["arcs"] = [core["arcs"][0] | {"arc_id": f"arc_{index:03d}"} for index in range(1, 5)]
    core["attractors"][0]["attractor_id"] = "attractor_001"
    if scaffold:
        actual = sum(item["kind"] == "scene" for item in scaffold["nodes"])
        guidance = RUNNER.derive_scope(actual)["scope"]
        core["scope_commitment"] |= {"planned_scene_count": actual, "planned_ending_count": 2,
            "planned_artifact_count": guidance["artifact_target"], "planned_formal_composition_count": guidance["formal_composition_target"]}
        core["causal_scaffold"] = scaffold
    return core


class BackwardScaffoldTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        self.run = Path(temporary.name)
        (self.run / ".staging").mkdir()
        RUNNER.write_json(self.run / "generation-brief.json", {"generation_seed": "synthetic_seed"})
        RUNNER.write_json(self.run / "run-manifest.json", RUNNER.derive_scope(150) | {"execution_policy": POLICY})

    def test_linear_chapters_mixed_widths_and_optional_shared_endings(self):
        scaffold = mixed_scaffold()
        order, roots = RUNNER.validate_scaffold(scaffold, RUNNER.derive_scope(150)["scope"], {"commit_genesis"}, complete=True)
        self.assertEqual(roots, [scaffold["opening_node_id"]]); self.assertEqual(len(order), 10)
        self.assertEqual(len(scaffold["nodes"][0]["successors"]), 1)
        self.assertEqual(len(scaffold["nodes"][1]["successors"]), 3)
        self.assertEqual(len(scaffold["nodes"][4]["entry_cases"]), 2)
        core = core_fixture(scaffold)
        plans = RUNNER.scaffold_packet_plans(core)
        self.assertEqual(len(plans[-1]["ending_slot_ids"]), 1)
        for index, plan in enumerate(plans):
            self.assertTrue(set(plan["depends_on_packet_slot_ids"]).issubset({prior["packet_slot_id"] for prior in plans[:index]}))
        planned = core | {"packet_plans": plans}
        self.assertTrue(RUNNER.navigation_contract_route(planned))
        self.assertEqual(len(plans[0]["required_navigation"]["scene_slot_0001"]), 1)

    def test_orphans_79_to_100_cannot_be_frozen(self):
        scaffold = mixed_scaffold(100)
        by_id = {item["node_id"]: item for item in scaffold["nodes"]}
        source = by_id["scaffold_scene_00078"]
        source["successors"] = []
        link(source, by_id["scaffold_outcome_0002"])
        with self.assertRaisesRegex(RUNNER.SchemaError, "disconnected frontier"):
            RUNNER.validate_scaffold(scaffold, RUNNER.derive_scope(100)["scope"], {"commit_genesis"}, complete=True)

    def test_frontier_retains_unfilled_entry_cases_after_first_parent(self):
        scaffold = mixed_scaffold()
        merge = scaffold["nodes"][4]
        scaffold["nodes"][3]["successors"][0]["target_case_id"] = "merge_left"
        self.assertIn(merge["node_id"], RUNNER.scaffold_frontier(scaffold["nodes"]))
        scaffold["nodes"][3]["successors"][0]["target_case_id"] = "merge_right"
        self.assertNotIn(merge["node_id"], RUNNER.scaffold_frontier(scaffold["nodes"]))
        merge["entry_cases"] = merge["entry_cases"][:1]
        scaffold["nodes"][3]["successors"][0]["target_case_id"] = "merge_left"
        routes = RUNNER.scaffold_entry_routes(core_fixture(scaffold), merge)
        self.assertEqual(routes, [("merge_left", "scene_slot_0003"), ("merge_left", "scene_slot_0004")])

    def test_cycles_unknown_successors_and_incomplete_case_support_are_rejected(self):
        for problem in ("cycle", "unknown", "support", "unused_case"):
            scaffold = mixed_scaffold(); scenes = scaffold["nodes"]
            if problem == "cycle":
                link(scenes[-3], scenes[0])
            elif problem == "unknown":
                scenes[0]["successors"][0]["to_node_id"] = "missing_scene"
            elif problem == "support":
                scenes[1]["entry_cases"][0]["requirements"] = [{"requirement_id": "required_clue", "description": "Synthetic clue."}]
            else:
                scenes[4]["entry_cases"].append({"case_id": "unsupported_alternative", "requirements": []})
            with self.subTest(problem=problem), self.assertRaises(RUNNER.SchemaError):
                RUNNER.validate_scaffold(scaffold, RUNNER.derive_scope(150)["scope"], {"commit_genesis"}, complete=True)

    def test_budget_reserves_capacity_for_a_single_grounded_opening(self):
        scaffold = mixed_scaffold()
        # A disconnected new predecessor consumes the last slot without closing the frontier.
        extra = node("extra_scene"); link(extra, scaffold["nodes"][-1]); scaffold["nodes"].append(extra)
        with self.assertRaisesRegex(RUNNER.SchemaError, "scene slots to close"):
            RUNNER.validate_scaffold(scaffold, RUNNER.derive_scope(9)["scope"], {"commit_genesis"})

    def test_complete_checkpoint_compiles_below_cap_and_resumes_without_provider(self):
        scaffold = mixed_scaffold(); final = scaffold["nodes"][-1]
        final["prerequisite_obligation_ids"] = ["obligation_one"]
        core = core_fixture()
        final["entry_cases"][0]["requirements"] = [{"requirement_id": "ending_requirement", "description":
            RUNNER.scaffold_prerequisite_requirements(core["obligation_graph"], ["obligation_one"])[0]}]
        predecessor = next(node for node in scaffold["nodes"] if any(edge["to_node_id"] == final["node_id"] for edge in node["successors"]))
        predecessor["successors"][0]["supports"] = [{"requirement_id": "ending_requirement", "guarantee_ids": [],
            "genesis_source_ids": ["commit_genesis"], "reason": "Synthetic prerequisite evidence."}]
        RUNNER.write_json(self.run / ".staging/architecture_core.planning.json", {"payload": {}, "record": core})
        state = {key: value for key, value in scaffold.items() if key != "slot_ids"} | {"round": 2, "complete": True}
        RUNNER.write_json(self.run / ".staging/causal-scaffold.json", state)
        def save(run, step, draft): RUNNER.write_json(run / ".staging" / f"{step}.planning.json", draft)
        forbidden = mock.Mock(side_effect=AssertionError("completed planning was repeated"))
        with mock.patch.object(RUNNER, "genesis_reference_catalog", return_value={"commit_genesis": "Synthetic committed premise."}), mock.patch.object(RUNNER, "save_planning_draft", side_effect=save):
            compiled = RUNNER.prepare_causal_scaffold(self.run, core, forbidden)
            again = RUNNER.prepare_causal_scaffold(self.run, compiled, forbidden)
        self.assertEqual(compiled, again); forbidden.assert_not_called()
        self.assertEqual(compiled["scope_commitment"]["planned_scene_count"], 8)
        self.assertEqual(compiled["scope_commitment"]["planned_ending_count"], 2)
        outcomes = [item for item in compiled["attractors"] if item["kind"] == "ending"]
        self.assertEqual([item["prerequisite_obligation_ids"] for item in outcomes], [[], ["obligation_one"]])
        RUNNER.validate_json_schema(compiled["causal_scaffold"], RUNNER.definition_schema("causalScaffold"))
        with mock.patch.object(RUNNER, "committed_records", return_value=[]), mock.patch.object(RUNNER, "save_planning_draft", side_effect=save):
            records = RUNNER.compile_scaffold_batches(self.run, compiled)
        for record in records:
            RUNNER.validate_json_schema(record, RUNNER.definition_schema("architecturePlanBatch"))
        with mock.patch.object(RUNNER, "committed_records", return_value=records), mock.patch.object(RUNNER, "save_planning_draft") as saved:
            self.assertEqual(RUNNER.compile_scaffold_batches(self.run, compiled), records)
        saved.assert_not_called()


    def test_reader_reconvergence_checks_both_alternative_states(self):
        scaffold = mixed_scaffold(); core = core_fixture(scaffold)
        core["packet_plans"] = RUNNER.scaffold_packet_plans(core)
        content = {}
        for plan in core["packet_plans"]:
            for slot, targets in plan["required_navigation"].items():
                item = scene_payload(slot, targets[0]); item["state_inputs"] = []
                item["choices"] = [copy.deepcopy(item["choices"][0]) | {"destination": {"kind": "technical_slot", "id": target}} for target in targets]
                content[slot] = item
        destination = lambda choice: choice["destination"]["id"]
        RUNNER.validate_scaffold_reader_states(core, content, destination)
        slots = scaffold["slot_ids"]
        left, right, merge = [slots[f"scaffold_scene_{index:05d}"] for index in (3, 4, 5)]
        content[left]["state_effects"] = [{"key": "path", "operation": "set", "value": "left"}]
        content[right]["state_effects"] = [{"key": "path", "operation": "set", "value": "right"}]
        arrivals = RUNNER.validate_scaffold_reader_states(core, content, destination)
        self.assertEqual({state["path"] for state in arrivals[merge].values()}, {"left", "right"})
        content[merge]["state_inputs"] = [{"key": "path", "operator": "equals", "value": "left"}]
        with self.assertRaisesRegex(RUNNER.SchemaError, "rejects a reachable incoming state"):
            RUNNER.validate_scaffold_reader_states(core, content, destination)

    def test_packet_schema_does_not_force_a_branch_or_allow_terminal_redirect(self):
        core = core_fixture(mixed_scaffold()); plans = RUNNER.scaffold_packet_plans(core)
        plan = RUNNER.single_content_packet_plans(plans[0])[0]
        with mock.patch.object(RUNNER, "execution_policy", return_value=POLICY), mock.patch.object(RUNNER, "committed_record", return_value=core):
            schema = RUNNER.packet_payload_schema(self.run, plan)
            self.assertEqual(schema["$defs"]["scenePayload"]["properties"]["choices"]["minItems"], 1)
            self.assertEqual(schema["$defs"]["scenePayload"]["properties"]["choices"]["maxItems"], 1)
            ending_schema = RUNNER.packet_payload_schema(self.run, RUNNER.single_content_packet_plans(plans[-1])[0])
        self.assertEqual(ending_schema["$defs"]["endingPayload"]["properties"]["redirect_destination"], {"type": "null"})

    def test_unsupported_guarantee_fails_without_changing_literary_bytes(self):
        core = core_fixture(mixed_scaffold()); plans = RUNNER.scaffold_packet_plans(core)
        node_value = core["causal_scaffold"]["nodes"][0]
        node_value["guarantees"] = [{"requirement_id": "must_be_earned", "description": "A synthetic event occurred."}]
        plan = RUNNER.single_content_packet_plans(plans[0])[0]
        item = scene_payload("scene_slot_0001", "scene_slot_0002")
        item["prose_mdx"] = "Synthetic preserved text.\r\nThe event has not occurred."
        artistic = {"scenes": [item], "endings": []}; before = RUNNER.canonical_json(artistic)
        def request(_run, _step, _prompt, schema, _transport, **kwargs):
            result = {"tasks": {identifier: {"supported": False, "reason": "The source does not establish it.", "evidence_quotes": []}
                for identifier in schema["properties"]["tasks"]["properties"]}}
            kwargs["validator"](result)
            return result, {}
        with mock.patch.object(RUNNER, "execution_policy", return_value=POLICY), mock.patch.object(RUNNER, "committed_record", return_value=core), mock.patch.object(
                RUNNER, "request_architecture_analysis", side_effect=request), mock.patch.object(RUNNER, "preserve_planning_result"), mock.patch.object(
                RUNNER, "scaffold_inherited_evidence", return_value={"inherited_guarantee_evidence": [], "immutable_source_units": {"commit_genesis": ["Synthetic committed premise."]}}):
            with self.assertRaisesRegex(RUNNER.CathedralsError, "remains unsupported after one evidence reconsideration"):
                RUNNER.audit_scaffold_guarantees(self.run, "synthetic_packet", artistic, plan, None)
        self.assertEqual(RUNNER.canonical_json(artistic), before)

    def test_audit_rejects_evidence_from_an_exclusive_entry_case(self):
        core = core_fixture(mixed_scaffold())
        node_value = core["causal_scaffold"]["nodes"][4]
        node_value["guarantees"] = [{"requirement_id": "shared_promise", "description": "Synthetic shared promise."}]
        slot = core["causal_scaffold"]["slot_ids"][node_value["node_id"]]
        local = {"nodes": [node_value], "opening_support": [], "immutable_source_units": {
            "scene_slot_0003": ["Synthetic left evidence."], "scene_slot_0004": ["Synthetic right evidence."]},
            "incoming": [{"from_slot_id": f"scene_slot_000{number}", "target_case_id": case["case_id"],
                "supports": [{"guarantee_ids": [f"guarantee_{number}"], "genesis_source_ids": []}]}
                for number, case in zip((3, 4), node_value["entry_cases"])],
            "inherited_guarantee_evidence": [{"from_slot_id": f"scene_slot_000{number}", "check_id": f"guarantee_{number}",
                "evidence_quotes": [{"source_id": f"scene_slot_000{number}"}]} for number in (3, 4)]}
        artistic = {"scenes": [scene_payload(slot, "scene_slot_0006")], "endings": []}
        def request(_run, _step, _prompt, schema, _transport, **kwargs):
            result = {"tasks": {identifier: {"supported": True, "reason": "Synthetic attempted cross-case citation.",
                "evidence_quotes": [{"source_id": "scene_slot_0004", "quote": "Synthetic right evidence."}]}
                for identifier in schema["properties"]["tasks"]["properties"]}}
            kwargs["validator"](result)
            return result, {}
        with mock.patch.object(RUNNER, "execution_policy", return_value=POLICY), mock.patch.object(RUNNER, "committed_record", return_value=core), mock.patch.object(
                RUNNER, "scaffold_packet_context", return_value=local), mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=request):
            with self.assertRaisesRegex(RUNNER.SchemaError, "permitted immutable evidence"):
                RUNNER.audit_scaffold_guarantees(self.run, "synthetic_merge", artistic, {}, None)

    def test_large_scope_retains_derived_ending_limit_above_sixteen(self):
        scaffold = mixed_scaffold(100)
        for index in range(3, 18):
            outcome = node(f"scaffold_outcome_{index:04d}", "ending")
            link(scaffold["nodes"][index], outcome)
            scaffold["nodes"].append(outcome)
        order, roots = RUNNER.validate_scaffold(scaffold, RUNNER.derive_scope(150)["scope"], {"commit_genesis"}, complete=True)
        self.assertEqual(len(order), 117); self.assertEqual(len(roots), 1)

    def test_long_linear_scaffold_uses_iterative_graph_validation(self):
        scaffold = mixed_scaffold(5000)
        order, roots = RUNNER.validate_scaffold(scaffold, RUNNER.derive_scope(5000)["scope"], {"commit_genesis"}, complete=True)
        self.assertEqual(len(order), 5002); self.assertEqual(len(roots), 1)

    def test_static_publication_preserves_source_for_100_and_150_scene_fixtures(self):
        for count in (100, 150):
            scaffold = mixed_scaffold(count); core = core_fixture(scaffold, cap=count)
            plans = RUNNER.scaffold_packet_plans(core)
            self.assertTrue(RUNNER.navigation_contract_route(core | {"packet_plans": plans}))
            fixture = scale_web_fixture()
            scenes = [item for record in fixture["packets"] for item in record["scenes"]][:count]
            endings = [item for record in fixture["packets"] for item in record["endings"]][:2]
            for index, scene in enumerate(scenes, 1): scene["technical_slot_id"] = f"scene_slot_{index:04d}"
            for index, ending in enumerate(endings, 1):
                ending["technical_slot_id"] = f"ending_slot_{index:04d}"; ending["redirect_destination"] = None
            content = scenes + endings
            ids = {item["technical_slot_id"]: item.get("scene_id", item.get("ending_id")) for item in content}
            edges = []
            for plan in plans:
                for slot, targets in plan["required_navigation"].items():
                    for target in targets:
                        edges.append({"edge_id": f"fixture_edge_{len(edges):04d}", "from_content_id": ids[slot],
                            "destination": {"kind": "technical_slot", "id": target}, "label": "Synthetic onward route",
                            "availability": "playable", "kind": "progression", "major_decision": False,
                            "decision_group_id": None, "state_conditions": [], "state_effects": []})
            resolved, endings = RUNNER.resolve_cross_packet_links(scenes, endings, edges)
            for scene in scenes:
                scene["choice_edge_ids"] = [edge["edge_id"] for edge in resolved if edge["from_content_id"] == scene["scene_id"]]
                scene["artifact_ids"] = []
            work = {"generation_id": "synthetic_run", "project_name": "Synthetic fixture", "generated_title": "Synthetic fixture",
                "scenes": scenes, "endings": endings, "decision_edges": resolved, "artifacts": [], "entry_content_id": scenes[0]["scene_id"]}
            project = self.run / f"web_{count}"
            RUNNER.write_json(project / "public/work.json", work)
            for name in ("style.css", "state.js", "theme.js"):
                RUNNER.write_atomic(project / "public" / name, b"/* synthetic test asset */")
            for item in content:
                identifier = item.get("scene_id", item.get("ending_id"))
                RUNNER.write_atomic(project / "public/source" / f"{identifier}.md", item["prose_mdx"].encode())
            RUNNER.build_static_baseline(project)
            self.assertEqual(RUNNER.static_build_problems(project, work), [])
            self.assertEqual(len(list((project / "dist/scenes").glob("*/index.html"))), count)


if __name__ == "__main__":
    unittest.main()
