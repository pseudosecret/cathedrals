"""Audited reliance corrections preserve literary bytes and the knowledge guard."""

import copy
import json
import socket
import unittest
from unittest import mock

from test_cathedrals import RUNNER, architecture_genesis_records, packet_payload
import test_reference_resolution as fixtures

api_response = fixtures.api_response


class EpistemicRecoveryTests(unittest.TestCase):
    def setUp(self):
        fixtures.ReferenceResolutionTests.setUp(self)
        self.records = architecture_genesis_records()
        self.records["genesis"]["claimants"] += [{"claimant_id": "claimant_02", "technical_slot_id": "claimant_slot_02", "name": "Lila Chen"}]
        self.facts = {key: {"data": {"fact_id": key, "subject": "logbook", "predicate": description,
                                   "value": True, "status": "established", "relevance": {}}}
                      for key, description in (("fact_known", "The logbook is on the desk"),
                                               ("fact_hidden", "The correction records the seal time"))}
        self.knowledge = {"claimant_02": {"explicitly_does_not_know": {"fact_hidden": {
            "data": {"subject_id": "claimant_02", "proposition_id": "fact_hidden", "relation": "explicitly_does_not_know"}}}}}
        read_state = RUNNER._read_state_map
        for patch in (
            mock.patch.object(RUNNER, "committed_record", side_effect=lambda run, kind: self.records.get(kind)),
            mock.patch.object(RUNNER, "committed_records", return_value=[]),
            mock.patch.object(RUNNER, "_read_state_map", side_effect=lambda run, name:
                self.facts if name == "canonical-facts.json" else self.knowledge if name == "knowledge-state.json" else read_state(run, name)),
            mock.patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")),
        ):
            patch.start()
            self.addCleanup(patch.stop)
        self.artistic = packet_payload(20, 5)
        self.artistic["scenes"][0]["prose_mdx"] = "Elias reads the seal logbook. The correction is blue."
        self.artistic["scenes"][0]["epistemic_dependencies"] = [
            {"subject_id": "claimant_02", "proposition_ids": ["fact_known", "fact_hidden"]},
            {"subject_id": "claimant_01", "proposition_ids": ["fact_known"]}]
        self.step = "packet_epistemic_test"
        self.empty = {key: [] for key in RUNNER.SEMANTIC_CATEGORIES}

    def conflict(self, artistic=None, semantic=None):
        conflicts = RUNNER.epistemic_conflicts((artistic or self.artistic)["scenes"], self.knowledge, semantic or self.empty)
        return RUNNER.EpistemicDependencyError(conflicts)

    def decision(self, action="repair_declaration", **updates):
        return {"scene_slot_id": "scene_slot_0001", "dependency_index": 0, "action": action,
                "replacement": [] if action == "repair_declaration" else None,
                "reason": "The source follows Elias; the Lila declaration is unsupported.",
                "evidence": [] if action == "unresolved" else [{
                    "source": "scene_slot_0001/prose_mdx", "quote": self.artistic["scenes"][0]["prose_mdx"]}]} | updates

    def repair(self, transport):
        return RUNNER.repair_epistemic_dependencies(self.run, self.step, self.artistic, self.conflict(), transport)

    def normalize(self, transport):
        # Exercise the actual conflict predicate and builder overlay at the normalization boundary.
        build = RUNNER.build_semantic_delta
        def validate(run, step, semantic, content_ids):
            effective = RUNNER.apply_epistemic_repairs(run, step, self.artistic)
            conflicts = RUNNER.epistemic_conflicts(effective["scenes"], self.knowledge, semantic)
            if conflicts:
                raise RUNNER.EpistemicDependencyError(conflicts)
            return build(run, step, semantic, content_ids)
        with mock.patch.object(RUNNER, "build_semantic_delta", side_effect=validate):
            return RUNNER.request_semantic_normalization(self.run, self.step, self.artistic, "Synthetic context.", transport)

    def preserve(self):
        RUNNER.preserve_artistic_payload(self.run, self.step, self.artistic, json.dumps(self.artistic), api_response(self.artistic))
        return {path: path.read_bytes() for path in (self.run / ".staging").glob("*.artistic.*")}

    def test_unsupported_declaration_is_removed_without_touching_other_fields_or_source(self):
        saved = self.preserve()
        original = copy.deepcopy(self.artistic)
        transport = mock.Mock(return_value=api_response({"decisions": [self.decision()]}))
        self.assertEqual(self.repair(transport), [])
        effective = RUNNER.apply_epistemic_repairs(self.run, self.step, self.artistic)
        expected = copy.deepcopy(original)
        expected["scenes"][0]["epistemic_dependencies"].pop(0)
        self.assertEqual(effective, expected)
        self.assertEqual(self.artistic, original)
        self.assertFalse(RUNNER.epistemic_conflicts(effective["scenes"], self.knowledge, self.empty))
        for path, value in saved.items():
            self.assertEqual(path.read_bytes(), value)
        state = RUNNER.read_json(self.run / f".staging/{self.step}.epistemic-repair.json")
        self.assertEqual(len(state["history"]), 1)
        self.assertEqual(state["history"][0]["decisions"][0]["evidence"], self.decision()["evidence"])
        self.assertEqual(RUNNER.epistemic_conflicts(original["scenes"], self.knowledge, self.empty)[0]["missing_proposition_ids"], ["fact_hidden"])

    def test_normalization_routes_known_conflict_directly_and_replays_without_calls(self):
        saved = self.preserve()
        calls = []
        def transport(_method, _url, request, **_kwargs):
            name = request["response_format"]["json_schema"]["name"]
            calls.append(name)
            return api_response(self.empty if name == "semanticDeltaPayload" else {"decisions": [self.decision()]})
        self.assertEqual(self.normalize(transport), self.empty)
        self.assertEqual(calls, ["semanticDeltaPayload", "epistemicCorrection"])
        forbidden = mock.Mock(side_effect=AssertionError("cached work repeated"))
        self.assertEqual(self.normalize(forbidden), self.empty)
        forbidden.assert_not_called()
        for path, value in saved.items():
            self.assertEqual(path.read_bytes(), value)

    def test_valid_replacement_keeps_unflagged_declarations(self):
        self.artistic["scenes"][0]["prose_mdx"] = "Elias reads the recorded seal time in the logbook."
        replacement = {"subject_id": "claimant_01", "proposition_ids": ["fact_hidden"]}
        transport = mock.Mock(return_value=api_response({"decisions": [self.decision(replacement=[replacement])]}))
        self.repair(transport)
        effective = RUNNER.apply_epistemic_repairs(self.run, self.step, self.artistic)
        self.assertEqual(effective["scenes"][0]["epistemic_dependencies"],
                         [replacement, self.artistic["scenes"][0]["epistemic_dependencies"][1]])
        self.assertFalse(RUNNER.epistemic_conflicts(effective["scenes"], self.knowledge, self.empty))

    def test_genuine_learning_preserves_dependency_and_repairs_exact_knowledge(self):
        self.artistic["scenes"][0]["prose_mdx"] = "Lila reads the correction and learns the recorded seal time."
        saved = self.preserve()
        learning = {"source": {"technical_slot_id": "scene_slot_0001"}, "subject_id": "claimant_02",
                    "proposition_id": "fact_hidden", "relation": "knows", "action": "establish", "relevance": {}}
        retraction = learning | {"relation": "explicitly_does_not_know", "action": "retract"}
        calls = []
        def transport(_method, _url, request, **_kwargs):
            name = request["response_format"]["json_schema"]["name"]
            calls.append(name)
            if name == "semanticDeltaPayload":
                return api_response(self.empty)
            if name == "epistemicCorrection":
                return api_response({"decisions": [self.decision("repair_knowledge", reason="The text shows Lila learning the seal time.")]})
            self.assertEqual(name, "semanticCategoryPage")
            prompt = request["messages"][1]["content"]
            self.assertIn("Continue ONLY knowledge_changes", prompt)
            self.assertIn("fact_hidden", prompt)
            return api_response({"items": [learning, retraction], "complete": True})
        result = self.normalize(transport)
        self.assertEqual(result, self.empty | {"knowledge_changes": [learning, retraction]})
        self.assertEqual(calls, ["semanticDeltaPayload", "epistemicCorrection", "semanticCategoryPage"])
        self.assertEqual(RUNNER.apply_epistemic_repairs(self.run, self.step, self.artistic), self.artistic)
        cached = mock.Mock(side_effect=AssertionError("learning disposition repeated"))
        self.assertTrue(self.repair(cached))
        cached.assert_not_called()
        for path, value in saved.items():
            self.assertEqual(path.read_bytes(), value)
        delta = RUNNER.build_semantic_delta(self.run, self.step, result, {"scene_slot_0001": ("scene", "scene_0001")})
        events = [{"constraint_kind": "knowledge_state", "data": {
            "subject_id": "claimant_02", "proposition_id": "fact_hidden", "relation": "explicitly_does_not_know", "action": "establish"}}]
        events += [{"constraint_kind": "knowledge_state", "data": item} for item in delta["knowledge_changes"]]
        _facts, knowledge, _obligations, _motifs, _foreclosures = RUNNER.project_constraint_state(events)
        self.assertNotIn("fact_hidden", knowledge["claimant_02"]["explicitly_does_not_know"])
        self.assertFalse(RUNNER.epistemic_conflicts(self.artistic["scenes"], knowledge, self.empty))

    def test_acquisition_must_retire_the_prior_negative_relation(self):
        self.artistic["scenes"][0]["prose_mdx"] = "Lila reads the correction and learns the recorded seal time."
        learning = {"source": {"technical_slot_id": "scene_slot_0001"}, "subject_id": "claimant_02",
                    "proposition_id": "fact_hidden", "relation": "knows", "action": "establish", "relevance": {}}
        calls = []
        def transport(_method, _url, request, **_kwargs):
            name = request["response_format"]["json_schema"]["name"]
            calls.append(name)
            if name == "semanticDeltaPayload":
                return api_response(self.empty)
            if name == "epistemicCorrection":
                return api_response({"decisions": [self.decision("repair_knowledge")]})
            values = [learning]
            if calls.count("semanticCategoryPage") > 1:
                values.append(learning | {"relation": "explicitly_does_not_know", "action": "retract"})
            return api_response({"items": values, "complete": True})
        result = self.normalize(transport)
        self.assertEqual(len(result["knowledge_changes"]), 2)
        self.assertEqual(calls, ["semanticDeltaPayload", "epistemicCorrection", "semanticCategoryPage", "semanticCategoryPage"])

    def test_genuine_contradiction_pauses_without_category_guess_or_metadata_bypass(self):
        self.artistic["scenes"][0]["prose_mdx"] = "Lila accuses Elias using the hidden seal time; she has not read the correction."
        saved = self.preserve()
        calls = []
        def transport(_method, _url, request, **_kwargs):
            name = request["response_format"]["json_schema"]["name"]
            calls.append(name)
            return api_response(self.empty if name == "semanticDeltaPayload" else {"decisions": [
                self.decision("unresolved", reason="The text requires Lila's unavailable seal time without showing acquisition.")]})
        with self.assertRaisesRegex(RUNNER.PausedError, "unresolved knowledge contradiction"):
            self.normalize(transport)
        self.assertEqual(calls, ["semanticDeltaPayload", "epistemicCorrection"])
        with self.assertRaises(RUNNER.PausedError):
            self.normalize(transport)
        self.assertEqual(calls, ["semanticDeltaPayload", "epistemicCorrection", "epistemicCorrection"])
        self.assertEqual(RUNNER.apply_epistemic_repairs(self.run, self.step, self.artistic), self.artistic)
        for path, value in saved.items():
            self.assertEqual(path.read_bytes(), value)

    def test_invalid_repairs_cannot_edit_unflagged_entries_invent_ids_or_fabricate_quotes(self):
        changes = ({"dependency_index": 1}, {"replacement": [{"subject_id": "missing", "proposition_ids": ["fact_known"]}]},
                   {"replacement": [{"subject_id": "claimant_01", "proposition_ids": ["fact_missing"]}]},
                   {"evidence": []}, {"evidence": [{"source": "scene_slot_0001/prose_mdx", "quote": "Invented learning."}]},
                   {"action": "repair_knowledge", "replacement": None,
                    "evidence": [{"source": "scene_slot_0001/prose_mdx", "quote": "Lila learns a secret."}]})
        for change in changes:
            with self.subTest(change=change):
                transport = mock.Mock(return_value=api_response({"decisions": [self.decision(**change)]}))
                with self.assertRaises(RUNNER.PausedError):
                    self.repair(transport)
                self.assertEqual(transport.call_count, 3)
        self.assertFalse((self.run / f".staging/{self.step}.epistemic-repair.json").exists())

    def test_mismatched_source_and_committed_content_are_rejected(self):
        transport = mock.Mock(return_value=api_response({"decisions": [self.decision()]}))
        self.repair(transport)
        changed = copy.deepcopy(self.artistic)
        changed["scenes"][0]["prose_mdx"] += " Changed."
        with self.assertRaises(RUNNER.IntegrityError):
            RUNNER.apply_epistemic_repairs(self.run, self.step, changed)
        forbidden = mock.Mock(side_effect=AssertionError("committed repair attempted"))
        with mock.patch.object(RUNNER, "committed_records", return_value=[{"scenes": self.artistic["scenes"]}]):
            with self.assertRaises(RUNNER.IntegrityError):
                self.repair(forbidden)
        forbidden.assert_not_called()

    def test_interrupted_correction_preserves_metadata_and_resumes_without_new_prose(self):
        saved = self.preserve()
        first = True
        def transport(_method, _url, request, **_kwargs):
            nonlocal first
            if request["response_format"]["json_schema"]["name"] == "semanticDeltaPayload":
                return api_response(self.empty)
            if first:
                first = False
                raise RUNNER.IncompleteResponseError("Interrupted correction", api_response({"decisions": []}))
            return api_response({"decisions": [self.decision()]})
        with self.assertRaises(RUNNER.PausedError):
            self.normalize(transport)
        resume = mock.Mock(side_effect=transport)
        self.assertEqual(self.normalize(resume), self.empty)
        resume.assert_called_once()
        self.assertEqual(resume.call_args.args[2]["response_format"]["json_schema"]["name"], "epistemicCorrection")
        for path, value in saved.items():
            self.assertEqual(path.read_bytes(), value)


if __name__ == "__main__":
    unittest.main()
