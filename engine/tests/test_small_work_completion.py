"""Small real-pipeline fixtures and one-pass failure/recovery boundaries; no live model."""
import copy
import json
import unittest
from unittest import mock

from test_cathedrals import RUNNER, obligation
from test_backward_scaffold import core_fixture, node
from test_completion_contract import scene_payload
import test_reference_resolution as fixtures
from test_scaffold_compiler import POLICY


class SmallWorkAcceptanceTests(unittest.TestCase):
    scene_count = 8
    ending_count = 2
    policy = POLICY
    interrupt_after_first_packet = True
    interrupt_after_publish = True
    setUp = fixtures.ReferenceResolutionTests.setUp
    test_complete_work = fixtures.ReferenceResolutionTests.test_full_twenty_scene_run_repairs_references_and_reaches_ready_without_resume


class SmallScopeTests(unittest.TestCase):
    scene_count = 8
    policy = POLICY
    setUp = fixtures.ReferenceResolutionTests.setUp

    def test_small_guidance_and_schema_allow_the_complete_minimal_work(self):
        for count in (8, 10, 12):
            scope = RUNNER.derive_scope(count)["scope"]
            self.assertEqual((scope["artifact_target"], scope["ending_target"], scope["ending_hard_max"],
                scope["formal_composition_target"], scope["branch_count_pressure"], scope["reconvergence_pressure"]), (1, 2, 2, 0, 1, 0))
            schema = RUNNER.load_protocol(self.run)
            RUNNER.validate_json_schema(scope, schema["$defs"]["runManifest"]["properties"]["scope"], schema)
        for count in (13, 30, 150):
            scope = RUNNER.derive_scope(count)["scope"]
            self.assertGreaterEqual(scope["artifact_target"], 5)
            self.assertGreaterEqual(scope["ending_target"], 5)
            self.assertGreaterEqual(scope["formal_composition_target"], 2)
            self.assertGreaterEqual(scope["reconvergence_pressure"], 1)

    def test_small_layout_caps_apply_before_any_core_is_authored(self):
        def inspect(_run, schema, _transport):
            for key, maximum in (("arcs", 2), ("attractors", 4), ("obligation_graph", 6)):
                self.assertEqual(schema["properties"][key]["minItems"], 1)
                self.assertEqual(schema["properties"][key]["maxItems"], maximum)
            raise KeyboardInterrupt("Inspected layout")
        with mock.patch.object(RUNNER, "allocate_core_draft", side_effect=inspect), self.assertRaisesRegex(KeyboardInterrupt, "Inspected layout"):
            RUNNER.prepare_core_draft(self.run, None)


class PrerequisitePlanningTests(unittest.TestCase):
    scene_count = 8
    policy = POLICY
    setUp = fixtures.ReferenceResolutionTests.setUp

    def declaration(self, prerequisites):
        return {"arc_id": "arc_001", "purpose": "Synthetic final outcome.", "intended_change": "Synthetic terminal change.",
            "terminal_role": "final", "attractor_id": "attractor_001", "prerequisite_obligation_ids": prerequisites,
            "entry_cases": [{"requirements": ["Synthetic left entry."]}, {"requirements": ["Synthetic right entry."]}],
            "guarantees": ["Synthetic outcome occurred."], "preserves": []}

    def test_prerequisite_closure_is_required_under_every_alternative_entry(self):
        graph = [obligation("setup", description="The missing signature was discovered.", hardness="soft"),
            obligation("reveal", description="The witness identified the signature.", requires=["setup"])]
        declarations = [self.declaration(["reveal"]), self.declaration([])]
        before = copy.deepcopy(declarations)
        nodes = RUNNER.compile_scaffold_declarations(declarations, ["outcome_one", "outcome_two"], seed=True, obligation_graph=graph)
        required = set(RUNNER.scaffold_prerequisite_requirements(graph, ["reveal"]))
        self.assertEqual(len(required), 2)
        for case in nodes[0]["entry_cases"]:
            self.assertTrue(required.issubset(item["description"] for item in case["requirements"]))
        self.assertEqual(len(nodes[1]["entry_cases"][0]["requirements"]), 1)
        self.assertEqual(declarations, before)
        RUNNER.validate_scaffold_prerequisites(nodes, graph)
        nodes[0]["entry_cases"][1]["requirements"].pop()
        with self.assertRaisesRegex(RUNNER.SchemaError, "omits required ending prerequisite"):
            RUNNER.validate_scaffold_prerequisites(nodes, graph)

    def test_unknown_or_oversized_prerequisites_cannot_be_silently_dropped(self):
        with self.assertRaisesRegex(RUNNER.SchemaError, "Unknown ending prerequisite"):
            RUNNER.compile_scaffold_declarations([self.declaration(["missing"])], ["outcome_one"], seed=True)
        graph = [obligation(f"prerequisite_{index}", description=f"Synthetic condition {index} occurred.") for index in range(8)]
        with self.assertRaisesRegex(RUNNER.SchemaError, "full prerequisite closure exceed"):
            RUNNER.compile_scaffold_declarations([self.declaration([item["obligation_id"] for item in graph])],
                ["outcome_one"], seed=True, obligation_graph=graph)

    def test_outcome_prompt_includes_actual_obligation_definitions(self):
        core = core_fixture(cap=8)
        def inspect(_run, _step, prompt, _schema, _transport, **_kwargs):
            context = json.loads(prompt.split("\n", 1)[1])
            self.assertEqual(context["obligations"], core["obligation_graph"])
            self.assertIn("BEFORE this outcome", prompt)
            raise KeyboardInterrupt("Inspected outcome context")
        with mock.patch.object(RUNNER, "planning_core", return_value=core), mock.patch.object(
                RUNNER, "genesis_reference_catalog", return_value={"commit_genesis": "Synthetic premise."}), mock.patch.object(
                RUNNER, "request_architecture_analysis", side_effect=inspect), self.assertRaisesRegex(KeyboardInterrupt, "Inspected outcome context"):
            RUNNER.prepare_causal_scaffold(self.run, core, None)


class SourceAuditRecoveryTests(unittest.TestCase):
    policy = POLICY
    setUp = fixtures.ReferenceResolutionTests.setUp

    def audit_fixture(self):
        contract = node("synthetic_scene")
        contract["guarantees"] = [{"requirement_id": "door_open", "description": "The door is open."}]
        slot = "scene_slot_0001"
        item = scene_payload(slot, "scene_slot_0002")
        item["prose_mdx"] = "Synthetic preserved text.\r\nThe door stood open."
        local = {"nodes": [contract], "incoming": [], "opening_support": [], "inherited_guarantee_evidence": [], "immutable_source_units": {}}
        architecture = {"causal_scaffold": {"nodes": [contract], "slot_ids": {contract["node_id"]: slot}}}
        return architecture, local, {"scenes": [item], "endings": []}

    def provider(self, supported, *, bad_quote=False):
        def request(_method, _url, body, **_kwargs):
            prompt = body["messages"][1]["content"]
            context = json.JSONDecoder().raw_decode(prompt.split("LOCAL AUDIT CONTEXT\n\n", 1)[1].lstrip())[0]
            reconsidering = "previous_unsupported_judgments" in context
            result = {}
            for identifier, task in context["tasks"].items():
                answer = supported and reconsidering
                result[identifier] = {"supported": answer,
                    "reason": "The original objection overlooked the explicit open door." if answer else "The door was never opened.",
                    "evidence_quotes": [{"source_id": task["source_ids"][0],
                        "quote": "Invented evidence." if bad_quote else "The door stood open."}] if answer else []}
            return fixtures.api_response({"tasks": result})
        return mock.Mock(side_effect=request)

    def audit(self, provider):
        architecture, local, artistic = self.audit_fixture()
        before = RUNNER.canonical_json(artistic)
        with mock.patch.object(RUNNER, "committed_record", return_value=architecture), mock.patch.object(
                RUNNER, "scaffold_packet_context", return_value=local):
            try:
                RUNNER.audit_scaffold_guarantees(self.run, "synthetic_packet", artistic, {}, provider)
            finally:
                self.assertEqual(RUNNER.canonical_json(artistic), before)

    def test_mistaken_rejection_gets_one_review_and_both_responses_replay_once(self):
        provider = self.provider(True)
        self.audit(provider)
        raw = {path: path.read_bytes() for path in (self.run / "raw").glob("*.api.json")}
        ledger = (self.run / "ledger.jsonl").read_bytes()
        self.audit(provider)
        self.assertEqual(provider.call_count, 2)
        self.assertEqual((self.run / "ledger.jsonl").read_bytes(), ledger)
        for path, content in raw.items(): self.assertEqual(path.read_bytes(), content)
        history = RUNNER.read_json(self.run / ".staging/synthetic_packet.repair.json")["history"]
        self.assertEqual([item["kind"] for item in history],
            ["scaffold_evidence_tasks", "scaffold_evidence_reconsideration", "scaffold_evidence"])
        self.assertEqual(history[0]["result"]["tasks"][next(iter(history[0]["result"]["tasks"]))]["supported"], False)
        receipt = RUNNER.read_json(self.run / ".staging/scaffold-evidence-scene_slot_0001.json")
        self.assertTrue(all(check["supported"] for check in receipt["audit"]["checks"]))

    def test_interruption_after_reconsideration_does_not_request_a_third_judgment(self):
        provider = self.provider(True)
        preserve = RUNNER.preserve_planning_result
        def checkpoint(*args, **kwargs):
            preserve(*args, **kwargs)
            if kwargs["kind"] == "scaffold_evidence_reconsideration":
                raise KeyboardInterrupt("Reconsideration recorded")
        with mock.patch.object(RUNNER, "preserve_planning_result", side_effect=checkpoint), self.assertRaisesRegex(KeyboardInterrupt, "recorded"):
            self.audit(provider)
        self.audit(provider)
        self.assertEqual(provider.call_count, 2)

    def test_sustained_rejection_is_terminal_and_names_the_promise_and_sources(self):
        provider = self.provider(False)
        for _ in range(2):
            with self.assertRaises(RUNNER.CathedralsError) as caught:
                self.audit(provider)
            self.assertNotIsInstance(caught.exception, RUNNER.PausedError)
            self.assertEqual(caught.exception.failure_class, "continuity_impossibility")
            self.assertIn("The door is open.", caught.exception.reason)
            self.assertIn("scene_slot_0001", caught.exception.reason)
            self.assertIn("resuming cannot fix", caught.exception.reason)
        self.assertEqual(provider.call_count, 2)
        path = self.run / ".staging/scaffold-evidence-scene_slot_0001.unsupported.json"
        failure = RUNNER.read_json(path)["unmet_checks"][0]
        self.assertEqual(failure["permitted_source_ids"], ["scene_slot_0001"])
        self.assertFalse((self.run / ".staging/scaffold-evidence-scene_slot_0001.json").exists())

    def test_reconsideration_cannot_pass_with_invented_quotations(self):
        with self.assertRaisesRegex(RUNNER.PausedError, "permitted immutable evidence"):
            self.audit(self.provider(True, bad_quote=True))
        self.assertFalse((self.run / ".staging/scaffold-evidence-scene_slot_0001.json").exists())


class PublicationRecoveryTests(unittest.TestCase):
    setUp = fixtures.ReferenceResolutionTests.setUp

    def published_fixture(self):
        project = self.run / "projection/web"
        (project / "public").mkdir(parents=True)
        (project / "dist").mkdir()
        RUNNER.write_json(project / "public/work.json", {"scenes": [{"scene_id": "synthetic_scene"}], "artifacts": [], "endings": []})
        (project / "dist/index.html").write_text("Synthetic publication fixture.")
        finalization = {"generation_id": self.run.name, "run_status": "READY_TO_PLAY", "completed_at": "original timestamp",
            "committed_record_hashes": {"synthetic_commit": "a" * 64}}
        for patch in (mock.patch.object(RUNNER, "ROOT", self.root), mock.patch.object(RUNNER, "reconcile_run"),
                mock.patch.object(RUNNER, "make_finalization", return_value=finalization | {"completed_at": "new timestamp"})):
            patch.start(); self.addCleanup(patch.stop)
        destination = RUNNER.publish_success(self.run, project, finalization)
        return project, destination, finalization

    def test_already_published_run_finishes_and_preserves_original_finalization(self):
        project, destination, finalization = self.published_fixture()
        before = {path: path.read_bytes() for path in destination.rglob("*") if path.is_file()}
        forbidden = mock.Mock(side_effect=AssertionError("Completed work invoked generation or republished"))
        with mock.patch.object(RUNNER, "execute_creative_phases", forbidden), mock.patch.object(RUNNER, "publish_success", forbidden):
            path, counts, _brief = RUNNER.execute_run(self.run, transport=forbidden)
            self.assertEqual(RUNNER.execute_run(self.run, transport=forbidden)[0], path)
        self.assertEqual(path, destination / "web/dist")
        self.assertEqual(counts, {"scenes": 1, "artifacts": 0, "endings": 0})
        self.assertEqual(RUNNER.read_json(self.run / "finalization.json"), finalization)
        self.assertEqual(RUNNER.load_state(self.run)["status"], "READY_TO_PLAY")
        for file, content in before.items(): self.assertEqual(file.read_bytes(), content)

    def test_resume_recovers_before_any_model_preflight(self):
        self.published_fixture()
        forbidden = mock.Mock(side_effect=AssertionError("Recovery contacted model or restarted generation"))
        with mock.patch.object(RUNNER, "__file__", str(RUNNER.snapshot_root(self.run) / "cathedrals")), mock.patch.object(
                RUNNER, "choose_resume", return_value=self.run), mock.patch.object(RUNNER, "ensure_resume_ready", forbidden), mock.patch.object(
                RUNNER, "execute_run", forbidden):
            self.assertEqual(RUNNER.main([], output_fn=lambda _: None, transport=forbidden), 0)

    def test_changed_site_or_provenance_is_never_overwritten_during_recovery(self):
        project, destination, finalization = self.published_fixture()
        published_page = destination / "web/dist/index.html"
        published_page.write_text("Changed after publication.")
        with self.assertRaisesRegex(RUNNER.IntegrityError, "files differ"):
            RUNNER.recover_published_run(self.run)
        self.assertEqual(published_page.read_text(), "Changed after publication.")
        published_page.write_bytes((project / "dist/index.html").read_bytes())
        RUNNER.write_json(destination / "provenance/finalization.json", finalization | {"committed_record_hashes": {}})
        with self.assertRaisesRegex(RUNNER.IntegrityError, "provenance does not match"):
            RUNNER.recover_published_run(self.run)
        self.assertFalse((self.run / "finalization.json").exists())
