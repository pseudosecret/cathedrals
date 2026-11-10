"""Dense continuity, authored navigation, ending readiness, and final-site regressions.

These tests exercise engine code only when explicitly run by the operator.
"""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_cathedrals import RUNNER, static_reader_fixture
from test_reference_resolution import api_response
from test_fts5_retrieval import decode_context
from benchmark_storage import packet
from test_scale_rehearsal import scale_web_fixture


POLICY = RUNNER.CURRENT_EXECUTION_POLICY.copy()


def architecture(count=3):
    slots = [f"scene_slot_{index:04d}" for index in range(1, count + 1)]
    ending = "ending_slot_0001"
    return {"attractors": [{"attractor_id": "attractor_001", "kind": "ending", "prerequisite_obligation_ids": ["obligation_one"]}],
        "packet_plans": [{"packet_slot_id": "literary_packet_0001", "packet_kind": "literary", "scene_slot_ids": slots,
            "ending_slot_ids": [], "required_navigation": {slot: [slots[index + 1] if index + 1 < len(slots) else ending] for index, slot in enumerate(slots)}},
            {"packet_slot_id": "ending_packet_0001", "packet_kind": "ending", "scene_slot_ids": [], "ending_slot_ids": [ending], "required_navigation": {}}]}


def scene_payload(slot, target, *, conditions=None, effects=None):
    return {"technical_slot_id": slot, "prose_mdx": "Synthetic source remains open.", "artifacts": [], "state_effects": effects or [],
        "choices": [{"destination": {"kind": "technical_slot", "id": target}, "availability": "playable",
                     "label": "Synthetic onward route", "state_conditions": conditions or [], "state_effects": []}]}


class CompletionContractTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        with mock.patch.object(RUNNER, "RUNTIME_ROOT", self.root), mock.patch.object(RUNNER, "RUNS_ROOT", self.root / "runs"):
            self.run = RUNNER.create_run(RUNNER.FrozenInputs(possible_scene_count=150), "http://offline.invalid", "offline",
                output_fn=lambda _: None, model_context_window_tokens=102656, execution_policy=POLICY)

    def obligations(self):
        return {"obligation_one": {"data": {"obligation_id": "obligation_one", "status": "active", "hardness": "hard",
            "requires": [], "range": "long_range", "description": "The synthetic judgment must occur."}}}

    def test_shared_metadata_expands_exactly_with_evidence_and_uncertainty(self):
        fact = {"fact_id": "fact_shared", "value": "A contested synthetic detail. " * 60,
                "status": "contested", "sources": [{"artifact_id": "scene_one", "source_locator": "original"}]}
        required = [("CONTRACT", [fact]), ("CURRENT", [{"data": fact}]), ("EVIDENCE", [fact])]
        before = copy.deepcopy(required)
        receipt = {"omissions": []}
        text = RUNNER.pack_packet_context(required, [], 49152, receipt)
        decoded = decode_context(text)
        for label, values in required:
            self.assertEqual(decoded[label], values)
        self.assertGreater(receipt["shared_value_bytes_saved"], 0)
        self.assertEqual(required, before)
        self.assertIn("contested", text)

    def test_similar_facts_are_not_collapsed_and_required_overflow_is_explicit(self):
        facts = [{"value": "Shared wording " * 50 + suffix} for suffix in ("first", "different")]
        receipt = {"omissions": []}
        text = RUNNER.pack_packet_context([("FACTS", facts)], [], 49152, receipt)
        self.assertEqual(decode_context(text)["FACTS"], facts)
        with self.assertRaises(RUNNER.PausedError):
            RUNNER.pack_packet_context([("MANDATORY", ["x" * 50000])], [], 1000, receipt)
        self.assertEqual(receipt["largest_required_units"][0]["section"], "MANDATORY")

    def test_packet_two_dense_predecessor_context_fits_without_repeating_entire_deltas(self):
        records = [packet(self.run.name, number) for number in range(1, 7)]
        facts = []
        for index in range(40):
            fact = copy.deepcopy(records[index % 6]["constraint_delta"]["canonical_facts"][0])
            fact |= {"fact_id": f"fact_dense_{index}", "value": f"Synthetic continuity {index}. " * 24}
            facts.append(fact)
        for index, record in enumerate(records):
            record["constraint_delta"]["canonical_facts"] = facts[index::6]
        catalog = {record["commit_id"]: {"hash": RUNNER.sha256_bytes(RUNNER.canonical_json(record))} for record in records}
        before = RUNNER.canonical_json(records)
        with mock.patch.object(RUNNER, "_source_index", side_effect=lambda _run, ids: {identifier: catalog[identifier] for identifier in ids}):
            contracts = RUNNER.predecessor_contracts(self.run, records)
        self.assertTrue(all("constraint_delta" not in contract for contract in contracts))
        required = [("FROZEN ENGINE LAW", "x" * 51616), ("DIRECT DEPENDENCIES", contracts),
                    ("CURRENT FACTS", [{"data": fact} for fact in facts]), ("REQUIRED EVIDENCE", facts)]
        receipt = {"omissions": []}
        text = RUNNER.pack_packet_context(required, [], 44290, receipt)
        self.assertLessEqual(RUNNER.estimated_prompt_tokens(text) + 4862, 49152)
        self.assertEqual(decode_context(text)["REQUIRED EVIDENCE"], facts)
        self.assertEqual(before, RUNNER.canonical_json(records))

    def test_dense_history_keeps_required_inputs_through_all_150_scenes(self):
        history = [{"fact_id": f"fact_{index}", "value": f"Synthetic historical record {index}. " * 20} for index in range(150)]
        before = RUNNER.canonical_json(history)
        for end in range(6, 151, 6):
            mandatory = history[end - 6:end]
            receipt = {"omissions": []}
            text = RUNNER.pack_packet_context([("LAW", "x" * 51616), ("REQUIRED", mandatory), ("PROOF", mandatory)],
                [("OPTIONAL HISTORY", history[:end - 6])], 22000, receipt)
            self.assertEqual(decode_context(text)["REQUIRED"], mandatory)
            self.assertLessEqual(receipt["estimated_context_tokens"], 22000)
        self.assertEqual(before, RUNNER.canonical_json(history))

    def test_loaded_capacity_is_hard_bound_and_full_wire_schema_counts(self):
        budgets = RUNNER.read_json(self.run / "run-manifest.json")["budgets"]
        self.assertEqual(budgets["normal_prepared_context_tokens"], 49152)
        self.assertEqual(RUNNER.packet_input_limit(self.run), 102656 - 10900 - 4096)
        self.assertEqual(RUNNER.packet_input_limit(self.run, 21800), 102656 - 21800 - 4096)
        plain = {"messages": [{"role": "user", "content": "Small prompt"}]}
        complete = plain | {"response_format": {"schema": {"description": "schema data " * 10000}}}
        self.assertGreater(RUNNER.provider_input_tokens(complete), RUNNER.provider_input_tokens(plain) + 20000)
        state = RUNNER.load_state(self.run)
        state["model_context_window_tokens"] = 64148
        RUNNER.save_state(self.run, state)
        self.assertEqual(RUNNER.packet_input_limit(self.run), 49152)

    def test_large_wire_schema_pauses_before_sending_or_creating_inflight_state(self):
        provider = mock.Mock(side_effect=AssertionError("Oversized envelope was sent"))
        with self.assertRaisesRegex(RUNNER.PausedError, "Complete provider envelope"):
            RUNNER.request_record(self.run, expected_record_type="genesis_foundation", step_id="wire_capacity", phase="genesis",
                prompt="Small prompt", context="Source context", branch_relation="synthetic", temperature=0,
                response_schema={"type": "object", "description": "schema " * 100000}, transport=provider)
        provider.assert_not_called()
        self.assertFalse((self.run / "state/inflight.json").exists())

    def test_expanded_retry_reserves_space_for_schema_and_correction_content(self):
        schema = {"type": "object", "description": "s" * 80000}
        prompt = "p" * 150000
        maximum = RUNNER.expanded_output_limit(self.run, prompt, "unwritten_step", schema)
        self.assertLess(maximum, RUNNER.EXPANDED_OUTPUT_TOKENS)
        self.assertGreater(maximum, RUNNER.BASE_OUTPUT_TOKENS)
        base = {"messages": [{"role": "user", "content": "Original request"}], "response_format": {"schema": schema}}
        corrected = base | {"messages": [{"role": "user", "content": "Original request\nCORRECTION\n" + "x" * 30000}]}
        self.assertGreater(RUNNER.provider_input_tokens(corrected), RUNNER.provider_input_tokens(base) + 9900)

    def test_navigation_contract_detects_disconnection_and_closed_loops(self):
        planned = architecture(150)
        self.assertEqual(len(RUNNER.navigation_contract_route(planned)), 151)
        broken = copy.deepcopy(planned)
        broken["packet_plans"][0]["required_navigation"]["scene_slot_0001"] = ["ending_slot_0001"]
        with self.assertRaisesRegex(RUNNER.SchemaError, "unreachable"):
            RUNNER.navigation_contract_route(broken)
        broken = copy.deepcopy(planned)
        broken["packet_plans"][0]["required_navigation"]["scene_slot_0150"] = ["scene_slot_0150", "ending_slot_0001"]
        self.assertEqual(len(RUNNER.navigation_contract_route(broken)), 151)
        trapped = architecture()
        trapped["packet_plans"][0]["required_navigation"] = {"scene_slot_0001": ["scene_slot_0002", "ending_slot_0001"],
            "scene_slot_0002": ["scene_slot_0003"], "scene_slot_0003": ["scene_slot_0003"]}
        with self.assertRaisesRegex(RUNNER.SchemaError, "no route to an ending"):
            RUNNER.navigation_contract_route(trapped)


    def test_empty_reserved_and_state_blocked_choices_fail_before_commit(self):
        planned = architecture()
        scene = scene_payload("scene_slot_0001", "scene_slot_0002")
        original = copy.deepcopy(scene)
        with mock.patch.object(RUNNER, "committed_records", return_value=[]):
            for choices in ([], [scene["choices"][0] | {"availability": "reserved"}]):
                with self.assertRaises(RUNNER.SchemaError):
                    RUNNER.validate_navigation_payload(self.run, planned, planned["packet_plans"][0],
                        {"scenes": [scene | {"choices": choices}], "endings": []})
            scene["choices"][0]["state_conditions"] = [{"key": "contamination", "operator": "gte", "value": 1}]
            with self.assertRaisesRegex(RUNNER.SchemaError, "Completion route is blocked"):
                RUNNER.validate_navigation_payload(self.run, planned, planned["packet_plans"][0], {"scenes": [scene], "endings": []})
            scene["state_effects"] = [{"operation": "increment", "key": "contamination", "value": 1}]
            RUNNER.validate_navigation_payload(self.run, planned, planned["packet_plans"][0], {"scenes": [scene], "endings": []})
        self.assertEqual(original["prose_mdx"], scene["prose_mdx"])

    def test_ending_prerequisite_schema_rejects_ambiguous_terminal_status(self):
        with mock.patch.object(RUNNER, "committed_record", return_value=architecture()), mock.patch.object(RUNNER, "_read_state_map", return_value=self.obligations()):
            schema = RUNNER.semantic_delta_schema(self.run, ["scene_slot_0001"], plan={})
        normalized = {key: [] for key in RUNNER.SEMANTIC_CATEGORIES}
        normalized["obligation_updates"] = [{"source": {"technical_slot_id": "scene_slot_0001"}, "obligation_id": "obligation_one",
            "status": "intentionally_unresolved", "reason": "The synthetic obligation remains active."}]
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_json_schema(normalized, schema)
        normalized["obligation_updates"][0]["status"] = "satisfied"
        RUNNER.validate_json_schema(normalized, schema)

    def test_resolution_audit_removes_ongoing_update_and_preserves_prose(self):
        artistic = {"scenes": [scene_payload("scene_slot_0001", "scene_slot_0002")], "endings": []}
        normalized = {key: [] for key in RUNNER.SEMANTIC_CATEGORIES}
        normalized["canonical_facts"] = [{"value": "Preserved metadata"}]
        normalized["obligation_updates"] = [{"obligation_id": "obligation_one", "status": "satisfied", "reason": "The question remains open."}]
        before = RUNNER.canonical_json(artistic)
        def audit(*args, validator=None, **kwargs):
            result = {"outcome": "ongoing", "reason": "The source poses the question.", "evidence_quotes": []}
            validator(result)
            return result, {}
        with mock.patch.object(RUNNER, "committed_record", return_value=architecture()), mock.patch.object(
                RUNNER, "_read_state_map", return_value=self.obligations()), mock.patch.object(
                RUNNER, "request_architecture_analysis", side_effect=audit), mock.patch.object(RUNNER, "preserve_planning_result"):
            result = RUNNER.audit_ending_resolutions(self.run, "fixture", artistic, normalized, mock.Mock())
        self.assertEqual(result["obligation_updates"], [])
        self.assertEqual(result["canonical_facts"], normalized["canonical_facts"])
        self.assertEqual(before, RUNNER.canonical_json(artistic))

    def test_resolution_audit_requires_exact_quotes_for_supported_satisfaction(self):
        artistic = {"scenes": [scene_payload("scene_slot_0001", "scene_slot_0002")], "endings": []}
        artistic["scenes"][0]["prose_mdx"] = "The synthetic judgment is complete."
        normalized = {key: [] for key in RUNNER.SEMANTIC_CATEGORIES}
        normalized["obligation_updates"] = [{"obligation_id": "obligation_one", "status": "satisfied", "reason": "The judgment occurred."}]
        quote = artistic["scenes"][0]["prose_mdx"]
        def audit(*args, validator=None, **kwargs):
            result = {"outcome": "satisfied", "reason": "The source states the completion.",
                "evidence_quotes": [{"technical_slot_id": "scene_slot_0001", "quote": quote}]}
            validator(result)
            return result, {}
        with mock.patch.object(RUNNER, "committed_record", return_value=architecture()), mock.patch.object(
                RUNNER, "_read_state_map", return_value=self.obligations()), mock.patch.object(
                RUNNER, "request_architecture_analysis", side_effect=audit), mock.patch.object(RUNNER, "preserve_planning_result"):
            self.assertEqual(RUNNER.audit_ending_resolutions(self.run, "fixture", artistic, normalized, mock.Mock()), normalized)
            quote = "This quote does not exist in the source."
            with self.assertRaisesRegex(RUNNER.SchemaError, "quote the immutable authored source exactly"):
                RUNNER.audit_ending_resolutions(self.run, "fixture", artistic, normalized, mock.Mock())

    def test_malformed_updates_are_left_for_existing_schema_recovery_without_audit_calls(self):
        provider = mock.Mock(side_effect=AssertionError("Malformed metadata must not invoke the resolution auditor"))
        for updates in (None, [None], [{"obligation_id": []}], [{"obligation_id": "obligation_one"}]):
            normalized = {key: [] for key in RUNNER.SEMANTIC_CATEGORIES} | {"obligation_updates": updates}
            with self.subTest(updates=updates), mock.patch.object(RUNNER, "committed_record", return_value=architecture()), mock.patch.object(
                    RUNNER, "_read_state_map", return_value=self.obligations()), mock.patch.object(RUNNER, "request_architecture_analysis", provider):
                result = RUNNER.audit_ending_resolutions(self.run, "fixture", {"scenes": [], "endings": []}, normalized, provider)
            self.assertEqual(result, normalized)
        provider.assert_not_called()

    def test_missing_future_prerequisite_opportunity_is_reported_early(self):
        planned = architecture()
        planned["packet_plans"] = planned["packet_plans"][1:]
        with mock.patch.object(RUNNER, "_read_state_map", side_effect=lambda _run, name:
                self.obligations() if name == "obligations.json" else {}), mock.patch.object(
                RUNNER, "evaluate_feasibility", return_value=[{"attractor_id": "attractor_001", "status": "viable"}]), mock.patch.object(
                RUNNER, "completed_packet_slots", return_value=set()), mock.patch.object(RUNNER, "all_committed_records", return_value=[]):
            with self.assertRaisesRegex(RUNNER.CathedralsError, "No remaining literary plan"):
                RUNNER.build_prospective_plan(self.run, planned, "commit_fixture")

    def test_final_scene_can_supply_omitted_metadata_or_fail_with_its_unsupported_condition(self):
        slot = "scene_slot_0001"
        scene = scene_payload(slot, "ending_slot_0001")
        scene["prose_mdx"] = "The judgment is complete."
        artistic = {"scenes": [scene], "endings": []}
        before = RUNNER.canonical_json(artistic)
        normalized = {key: [] for key in RUNNER.SEMANTIC_CATEGORIES}
        planned = architecture(1)
        plan = planned["packet_plans"][0]
        with mock.patch.object(RUNNER, "committed_record", return_value=planned), mock.patch.object(
                RUNNER, "committed_records", return_value=[]), mock.patch.object(RUNNER, "_read_state_map", side_effect=lambda _run, name:
                    self.obligations() if name == "obligations.json" else {}):
            provider = mock.Mock(return_value=api_response({"outcome": "satisfied", "reason": "Judgment occurred.",
                "evidence_quotes": [{"technical_slot_id": slot, "quote": scene["prose_mdx"]}]}))
            result = RUNNER.audit_ending_resolutions(self.run, "final_scene", artistic, normalized, provider, plan=plan)
            self.assertEqual(result["obligation_updates"], [{"obligation_id": "obligation_one", "status": "satisfied",
                "reason": "Judgment occurred.", "source": {"technical_slot_id": slot}}])
            self.assertEqual(RUNNER.audit_ending_resolutions(self.run, "final_scene", artistic, normalized, provider, plan=plan), result)
            provider.assert_called_once()
            provider = mock.Mock(return_value=api_response({"outcome": "unsupported", "reason": "Judgment never occurs.", "evidence_quotes": []}))
            with self.assertRaisesRegex(RUNNER.CathedralsError, "obligation_one: Judgment never occurs") as error:
                RUNNER.audit_ending_resolutions(self.run, "unsupported_final", artistic, normalized, provider, plan=plan)
            self.assertEqual(error.exception.failure_class, "continuity_impossibility")
            provider.assert_called_once()
        self.assertEqual(RUNNER.canonical_json(artistic), before)

    def test_long_range_payoff_is_optional_until_deadline_and_soft_pressure_stays_advisory(self):
        planned = architecture()
        planned["packet_plans"].insert(1, {"packet_slot_id": "literary_packet_0002", "packet_kind": "literary"})
        obligations = self.obligations() | {"soft_one": {"data": {"hardness": "soft", "requires": [], "range": "local"}}}
        prospective = {"feasibility": [], "packet_order": [{"packet_slot_id": "literary_packet_0001"}],
            "obligation_assignments": [{"packet_slot_id": "literary_packet_0001", "obligation_id": key} for key in obligations]}
        with mock.patch.object(RUNNER, "_read_state_map", side_effect=lambda _run, name: prospective if name == "prospective-plan.json" else obligations), mock.patch.object(
                RUNNER, "completed_packet_slots", return_value=set()), mock.patch.object(RUNNER, "all_committed_records", return_value=[]):
            selected = RUNNER.select_next_packet(self.run, planned)
        self.assertEqual(selected["advance_obligation_ids"], [])
        self.assertEqual(selected["may_satisfy_obligation_ids"], ["obligation_one"])

    def project_fixture(self, fixture=None):
        fixture = fixture or static_reader_fixture()
        work = {"generation_id": self.run.name, "project_name": "Synthetic fixture", "generated_title": "Synthetic fixture"}
        for field in ("scenes", "endings", "artifacts", "decision_edges"):
            work[field] = [item for record in fixture["packets"] for item in record[field]]
        work["scenes"][0]["prose_mdx"] += "\r\nSynthetic preserved newline."
        work["decision_edges"], work["endings"] = RUNNER.resolve_cross_packet_links(work["scenes"], work["endings"], work["decision_edges"])
        work["entry_content_id"] = work["scenes"][0]["scene_id"]
        project = self.root / "web"
        RUNNER.write_json(project / "public/work.json", work)
        for name in ("style.css", "state.js", "theme.js"):
            (project / "public" / name).write_text("")
        for field, identifier, text in (("scenes", "scene_id", "prose_mdx"), ("endings", "ending_id", "prose_mdx"), ("artifacts", "artifact_id", "body_mdx")):
            for item in work[field]:
                RUNNER.write_atomic(project / "public/source" / f"{item[identifier]}.md", item[text].encode())
        return project, work

    def test_full_150_scene_static_site_has_all_prose_routes_and_sources(self):
        fixture = scale_web_fixture()
        planned = {"packet_plans": [{"packet_slot_id": record["packet_slot_id"],
            "scene_slot_ids": [scene["technical_slot_id"] for scene in record["scenes"]],
            "ending_slot_ids": [ending["technical_slot_id"] for ending in record["endings"]],
            "required_navigation": {scene["technical_slot_id"]: [edge["destination"]["id"] for edge in record["decision_edges"]
                if edge["from_content_id"] == scene["scene_id"]] for scene in record["scenes"]}} for record in fixture["packets"]]}
        RUNNER.navigation_contract_route(planned)
        with mock.patch.object(RUNNER, "committed_records", return_value=fixture["packets"]):
            RUNNER.validate_navigation_payload(self.run, planned, {}, {"scenes": [], "endings": []})
        project, work = self.project_fixture(fixture)
        with mock.patch.object(RUNNER, "append_deterministic_step"):
            self.assertEqual(RUNNER.build_web(self.run, project)["result"], "PASS")
        self.assertEqual(len(work["scenes"]), 150)
        self.assertEqual(len(list((project / "dist/scenes").glob("*/index.html"))), 150)
        self.assertEqual(RUNNER.static_build_problems(project, work), [])

    def test_complete_baseline_contains_rendered_prose_and_exact_source_bytes(self):
        project, work = self.project_fixture()
        with mock.patch.object(RUNNER, "append_deterministic_step"):
            self.assertEqual(RUNNER.build_web(self.run, project)["result"], "PASS")
        self.assertEqual(RUNNER.static_build_problems(project, work), [])
        scene = work["scenes"][0]
        self.assertEqual((project / "dist/source" / f"{scene['scene_id']}.md").read_bytes(), scene["prose_mdx"].encode())
        path = project / "dist/scenes" / scene["scene_id"] / "index.html"
        path.write_text('<div class="prose">A placeholder.</div>')
        self.assertTrue(any("Rendered prose" in reason for reason in RUNNER.static_build_problems(project, work)))


    def test_final_build_detects_broken_links_assets_and_source_exports(self):
        project, work = self.project_fixture()
        RUNNER.build_static_baseline(project)
        scene = work["scenes"][0]
        path = project / "dist/scenes" / scene["scene_id"] / "index.html"
        path.write_text(path.read_text() + '<a href="/scenes/missing_scene/">Broken fixture</a>')
        (project / "dist/theme.js").write_text("Changed asset")
        (project / "dist/source" / f"{scene['scene_id']}.md").write_text("Changed source")
        reasons = RUNNER.static_build_problems(project, work)
        self.assertTrue(any("link has no target" in reason for reason in reasons))
        self.assertTrue(any("reader asset changed" in reason for reason in reasons))
        self.assertTrue(any("Published source changed" in reason for reason in reasons))


if __name__ == "__main__":
    unittest.main()
