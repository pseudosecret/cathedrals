"""Bounded semantic extraction preserves authored prose and accepted metadata."""

import copy
import json
import socket
import unittest
from unittest import mock

from test_cathedrals import ROOT, RUNNER, architecture_genesis_records, genesis_semantic_payload, packet_payload
import test_reference_resolution as fixtures


class SemanticRecoveryTests(unittest.TestCase):
    def setUp(self):
        fixtures.ReferenceResolutionTests.setUp(self)
        records = architecture_genesis_records()
        for patch in (mock.patch.object(RUNNER, "committed_record", side_effect=lambda run, kind: records.get(kind)),
                      mock.patch.object(RUNNER, "committed_records", return_value=[]),
                      mock.patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden"))):
            patch.start()
            self.addCleanup(patch.stop)
        self.artistic = packet_payload(333, 87)
        self.step = "packet_semantic_test"
        RUNNER.preserve_artistic_payload(self.run, self.step, self.artistic, json.dumps(self.artistic), fixtures.api_response(self.artistic))
        self.preserved = {path: path.read_bytes() for path in (self.run / ".staging").glob("*.artistic.*")}

    def fact(self, index=0):
        return copy.deepcopy(genesis_semantic_payload("scene_slot_0001")["canonical_facts"][0]) | {
            "predicate": f"observed_{index}", "value": index}

    def empty(self):
        return {key: [] for key in RUNNER.SEMANTIC_CATEGORIES}

    def response(self, payload, *, truncated=False, text=False):
        response = fixtures.api_response(payload, text=text)
        if truncated:
            response["choices"][0]["finish_reason"] = "length"
        return response

    def normalize(self, transport):
        return RUNNER.request_semantic_normalization(self.run, self.step, self.artistic, "Synthetic full source context.", transport)

    def seed_facts(self):
        payload = self.empty()
        del payload["canonical_facts"]
        prefix = json.dumps(payload)[:-1] + ',"canonical_facts":['
        RUNNER.seed_semantic_recovery(self.run, self.step, self.artistic, self.response(prefix, truncated=True, text=True))

    def assert_prose_unchanged(self):
        for path, original in self.preserved.items():
            self.assertEqual(path.read_bytes(), original)

    def test_default_headroom_and_concise_instruction_leave_story_unchanged(self):
        transport = mock.Mock(return_value=self.response(self.empty()))
        self.assertEqual(self.normalize(transport), self.empty())
        request = transport.call_args.args[2]
        self.assertEqual(request["max_tokens"], 8192)
        self.assertIn("do not restate canon", request["messages"][1]["content"])
        self.assertEqual(RUNNER.packet_literary_word_count(self.artistic), 420)
        self.assert_prose_unchanged()

    def test_saved_failure_preserves_closed_categories_and_finishes_only_pending(self):
        fixture = RUNNER.read_json(ROOT / "engine/tests/fixtures/semantic-normalization-truncation.json")
        facts = [self.fact(index) for index in range(fixture["complete_categories"]["canonical_facts"])]
        knowledge = [{"source": {"technical_slot_id": "scene_slot_0001"}, "subject_id": "claimant_01", "relation": "knows",
            "proposition_id": f"fact_{index:02d}", "action": "establish", "relevance": {}} for index in range(1, 13)]
        motifs = [{"source": {"technical_slot_id": "scene_slot_0001"}, "motif_id": f"motif_{index}", "action": "establish",
            "current_function": "Synthetic recurrence.", "pressure": "Synthetic pressure.", "overuse_risk": "low", "relevance": {}} for index in range(5)]
        closed = {"canonical_facts": facts, "knowledge_changes": knowledge, "motif_events": motifs}
        prefix = json.dumps(closed)[:-1] + ',"new_soft_obligations":[{"description":"pending'
        partial = self.response(prefix, truncated=True, text=True)
        partial["usage"] = {"prompt_tokens": fixture["prompt_tokens"], "completion_tokens": fixture["output_limit_tokens"]}
        obligation = {"source": {"technical_slot_id": "scene_slot_0001"}, "kind": "branch_residue", "description": "Synthetic pending debt.",
            "requires": [], "universality": "local", "resolution_modes": ["revelation"], "range": "local", "termination_targets": [], "relevance": {}}
        calls = []
        def transport(method, url, request, **kwargs):
            name = request["response_format"]["json_schema"]["name"]
            calls.append(name)
            if name == "semanticDeltaPayload":
                return partial
            prompt = request["messages"][1]["content"]
            if "Continue ONLY new_soft_obligations" in prompt:
                return self.response({"items": [obligation], "complete": True})
            self.assertIn("Continue ONLY obligation_updates", prompt)
            return self.response({"items": [], "complete": True})
        result = self.normalize(transport)
        self.assertEqual(result, self.empty() | closed | {"new_soft_obligations": [obligation]})
        self.assertEqual(calls, ["semanticDeltaPayload", "semanticCategoryPage", "semanticCategoryPage"])
        entries = [entry for entry in RUNNER.ledger_entries(self.run) if entry["step_type"] == "analysis"]
        self.assertEqual(sum(entry["token_accounting"]["output_tokens"] for entry in entries), 4096 + 14)
        self.assertEqual(len(entries), 3)
        api = RUNNER.read_json(self.run / f".staging/{self.step}.semantic.api.json")
        self.assertTrue(api["_cathedrals_semantic_assembled"])
        self.assertEqual(api["usage"], {})
        self.assert_prose_unchanged()

    def test_multiple_fact_pages_keep_aliases_and_defer_local_motif_references(self):
        self.seed_facts()
        facts = [self.fact(index) for index in range(13)]
        facts[0]["relevance"]["motif_ids"] = ["motif_new"]
        knowledge = {"source": {"technical_slot_id": "scene_slot_0001"}, "subject_id": "claimant_01", "relation": "knows",
            "proposition_id": "fact_13", "action": "establish", "relevance": {}}
        motif = {"source": {"technical_slot_id": "scene_slot_0001"}, "motif_id": "motif_new", "action": "establish",
            "current_function": "Synthetic recurrence.", "pressure": "Synthetic pressure.", "overuse_risk": "low", "relevance": {}}
        state = RUNNER.read_json(self.run / f".staging/{self.step}.semantic-recovery.json")
        state["complete"]["knowledge_changes"] = state["complete"]["motif_events"] = False
        RUNNER.write_json(self.run / f".staging/{self.step}.semantic-recovery.json", state)
        pages = iter(({"items": facts[:8], "complete": False}, {"items": facts[8:], "complete": True},
                      {"items": [knowledge], "complete": True}, {"items": [motif], "complete": True}))
        transport = mock.Mock(side_effect=lambda *args, **kwargs: self.response(next(pages)))
        result = self.normalize(transport)
        self.assertEqual(result["canonical_facts"], facts)
        self.assertEqual(transport.call_count, 4)
        delta = RUNNER.build_semantic_delta(self.run, self.step, result, {"scene_slot_0001": ("scene", "scene_0001")})
        self.assertEqual(delta["knowledge_changes"][0]["proposition_id"], delta["canonical_facts"][12]["fact_id"])
        self.assert_prose_unchanged()

    def test_truncated_page_retains_prefix_and_reduces_next_page_size(self):
        self.seed_facts()
        facts = [self.fact(index) for index in range(8)]
        prefix = '{"items":' + json.dumps(facts[:2])[:-1] + ',{"predicate":"unfinished'
        responses = iter((self.response(prefix, truncated=True, text=True), self.response({"items": facts[2:6], "complete": False}), self.response({"items": facts[6:], "complete": True})))
        transport = mock.Mock(side_effect=lambda *args, **kwargs: next(responses))
        result = self.normalize(transport)
        self.assertEqual(result["canonical_facts"], facts)
        sizes = [call.args[2]["response_format"]["json_schema"]["schema"]["properties"]["items"]["maxItems"] for call in transport.call_args_list]
        self.assertEqual(sizes, [8, 4, 4])
        self.assert_prose_unchanged()

    def test_single_record_truncation_uses_existing_expanded_analysis_headroom(self):
        self.seed_facts()
        path = self.run / f".staging/{self.step}.semantic-recovery.json"
        state = RUNNER.read_json(path)
        state["page_size"]["canonical_facts"] = 1
        RUNNER.write_json(path, state)
        transport = mock.Mock(side_effect=[self.response('{"items":[', truncated=True, text=True), self.response({"items": [self.fact()], "complete": True})])
        result = self.normalize(transport)
        self.assertEqual(result["canonical_facts"], [self.fact()])
        self.assertEqual([call.args[2]["max_tokens"] for call in transport.call_args_list], [8192, 15000])

    def test_single_record_exhaustion_reports_expansion_and_actual_provider_attempts(self):
        self.seed_facts()
        path = self.run / f".staging/{self.step}.semantic-recovery.json"
        state = RUNNER.read_json(path)
        state["page_size"]["canonical_facts"] = 1
        RUNNER.write_json(path, state)
        transport = mock.Mock(return_value=self.response('{"items":[', truncated=True, text=True))
        with self.assertRaises(RUNNER.PausedError) as raised:
            self.normalize(transport)
        self.assertEqual(transport.call_count, 4)
        self.assertIn("3 page correction attempts", raised.exception.reason)
        self.assertIn("4 provider attempts", raised.exception.reason)
        self.assert_prose_unchanged()

    def test_no_progress_pauses_after_actual_attempts_and_resume_only_finishes_pending(self):
        self.seed_facts()
        transport = mock.Mock(return_value=self.response({"items": [], "complete": False}))
        with self.assertRaisesRegex(RUNNER.PausedError, "exhausted 3 page correction attempts"):
            self.normalize(transport)
        self.assertEqual(transport.call_count, 3)
        preserved = {path: path.read_bytes() for path in (self.run / "raw").glob("*.api.json")}
        resume = mock.Mock(return_value=self.response({"items": [], "complete": True}))
        self.assertEqual(self.normalize(resume), self.empty())
        self.assertEqual(resume.call_count, 1)
        for path, original in preserved.items():
            self.assertEqual(path.read_bytes(), original)
        self.assert_prose_unchanged()

    def test_interrupted_page_preserves_complete_records_before_pausing(self):
        self.seed_facts()
        interrupted = self.response({"items": [self.fact(0)], "complete": False})
        transport = mock.Mock(side_effect=RUNNER.IncompleteResponseError("Synthetic interrupted stream", interrupted))
        with self.assertRaises(RUNNER.PausedError):
            self.normalize(transport)
        self.assertEqual(transport.call_count, 1)
        state = RUNNER.read_json(self.run / f".staging/{self.step}.semantic-recovery.json")
        self.assertEqual(state["payload"]["canonical_facts"], [self.fact(0)])
        resume = mock.Mock(return_value=self.response({"items": [self.fact(1)], "complete": True}))
        result = self.normalize(resume)
        self.assertEqual(result["canonical_facts"], [self.fact(0), self.fact(1)])
        self.assertEqual(resume.call_count, 1)
        self.assert_prose_unchanged()

    def test_missing_items_cannot_be_inferred_as_an_empty_complete_category(self):
        self.seed_facts()
        transport = mock.Mock(return_value=self.response({"complete": True}))
        with self.assertRaises(RUNNER.PausedError):
            self.normalize(transport)
        self.assertEqual(transport.call_count, 3)
        state = RUNNER.read_json(self.run / f".staging/{self.step}.semantic-recovery.json")
        self.assertFalse(state["complete"]["canonical_facts"])

    def test_context_overflow_pauses_without_clipping_or_contacting_provider(self):
        transport = mock.Mock(side_effect=AssertionError("oversized request"))
        with self.assertRaises(RUNNER.PausedError) as raised:
            RUNNER.request_semantic_normalization(self.run, self.step, self.artistic, "x" * 220000, transport)
        self.assertIn("semantic normalization context", raised.exception.reason)
        transport.assert_not_called()
        self.assert_prose_unchanged()

    def test_event_budget_remains_hard_without_discarding_accepted_records(self):
        self.seed_facts()
        manifest = self.run / "run-manifest.json"
        value = RUNNER.read_json(manifest)
        value["budgets"]["max_constraint_events"] = 1
        transport = mock.Mock(return_value=self.response({"items": [self.fact(0), self.fact(1)], "complete": True}))
        read_json = RUNNER.read_json
        with mock.patch.object(RUNNER, "read_json", side_effect=lambda path: value if path == manifest else read_json(path)), self.assertRaises(RUNNER.CathedralsError) as raised:
            self.normalize(transport)
        self.assertNotIsInstance(raised.exception, RUNNER.PausedError)
        self.assertEqual(raised.exception.failure_class, "budget_exhaustion")
        self.assertEqual(transport.call_count, 1)
        state = RUNNER.read_json(self.run / f".staging/{self.step}.semantic-recovery.json")
        self.assertEqual(len(state["payload"]["canonical_facts"]), 2)
        self.assert_prose_unchanged()

    def test_recovery_rejects_a_different_artistic_source_without_provider_call(self):
        self.seed_facts()
        changed = copy.deepcopy(self.artistic)
        changed["scenes"][0]["prose_mdx"] += " Different source."
        transport = mock.Mock(side_effect=AssertionError("provider called for mismatched source"))
        with self.assertRaises(RUNNER.IntegrityError):
            RUNNER.request_semantic_normalization(self.run, self.step, changed, "context", transport)
        transport.assert_not_called()
        self.assert_prose_unchanged()

    def test_canonical_correction_revisits_only_rejected_category(self):
        original = self.empty()
        original["canonical_facts"] = [self.fact()]
        knowledge = {"source": {"technical_slot_id": "scene_slot_0001"}, "subject_id": "claimant_01", "relation": "knows",
                     "proposition_id": "fact_01", "action": "establish", "relevance": {}}
        original["knowledge_changes"] = [knowledge]
        RUNNER.seed_semantic_recovery(self.run, self.step, self.artistic, self.response(original, truncated=True))
        corrected = knowledge | {"relation": "believes"}
        def transport(method, url, request, **kwargs):
            if "response_format" not in request:
                return self.response("knowledge_changes", text=True)
            self.assertIn("Continue ONLY knowledge_changes", request["messages"][1]["content"])
            return self.response({"items": [corrected], "complete": True})
        transport = mock.Mock(side_effect=transport)
        build = RUNNER.build_semantic_delta
        calls = []
        def validate(*args, **kwargs):
            calls.append(True)
            if len(calls) == 1:
                raise RUNNER.SchemaError("Synthetic knowledge contradiction")
            return build(*args, **kwargs)
        with mock.patch.object(RUNNER, "build_semantic_delta", side_effect=validate):
            result = self.normalize(transport)
        self.assertEqual(result, original | {"knowledge_changes": [corrected]})
        self.assertEqual(transport.call_count, 2)
        self.assert_prose_unchanged()

    def test_compact_context_preserves_all_json_values_and_plain_text(self):
        content = {"prose": "Keep  intentional  spaces.\nAnd line breaks.", "entries": [{"value": index} for index in range(4)]}
        original = RUNNER.bounded_context([("PLAIN", "Exact plain prose.\n\nAnother paragraph."), ("JSON", content)], 10000)
        compact = RUNNER.compact_semantic_context(original)
        self.assertIn("Exact plain prose.\n\nAnother paragraph.", compact)
        self.assertEqual(json.loads(compact.split("===== JSON =====\n", 1)[1]), content)
        self.assertLess(len(compact), len(original))


if __name__ == "__main__":
    unittest.main()
