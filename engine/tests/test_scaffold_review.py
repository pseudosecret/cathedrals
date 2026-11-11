"""Scaffold review tasks preserve ownership, source scope and response accounting."""
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
        nodes = RUNNER.compile_scaffold_declarations(declarations, self.identifiers)
        self.patch = {"nodes": [RUNNER.compile_scaffold_connections(source, self.frontier,
            selection(source, self.frontier), GENESIS) for source in nodes],
            "complete": False, "opening_node_id": None, "opening_support": []}

    def review(self, transport):
        return RUNNER.review_scaffold_connections(self.run, "scaffold_expand_00004", self.patch, self.frontier, transport)

    def test_rejection_is_bound_to_one_of_several_predecessors_of_the_same_case(self):
        responses, reviewed = {}, {}
        def transport(_method, _url, request, **kwargs):
            context = json.loads(request["messages"][1]["content"].split("LOCAL PLANNING CONTEXT\n\n", 1)[1])
            supports = {key: task for key, task in context["tasks"].items() if task["kind"] == "support"}
            self.assertLessEqual(len(context["tasks"]), 4)
            reviewed.update(supports)
            response = {"issues": {key: "The selected proof does not establish this case." for key, task in supports.items()
                if task["owner"] == self.identifiers[2]}}
            responses[json.dumps(response)] = response
            return api_response(response)
        result = self.review(transport)
        self.assertEqual(len(reviewed), 4)
        self.assertEqual({task["requirement"]["requirement_id"] for task in reviewed.values()}, {"prior_requirement"})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["owner"], self.identifiers[2])
        self.assertEqual(result[0]["requirement"]["requirement_id"], "prior_requirement")
        raw = next((self.run / "raw").glob("scaffold_expand_00004_review_*-attempt1.api.json"))
        prefix = (self.run / "ledger.jsonl").read_bytes()
        original = raw.read_bytes()
        forbidden = mock.Mock(side_effect=AssertionError("Accepted review was requested again"))
        self.assertEqual(self.review(forbidden), result)
        forbidden.assert_not_called()
        self.assertEqual((self.run / "ledger.jsonl").read_bytes(), prefix)
        self.assertEqual(raw.read_bytes(), original)
        self.assertIn(RUNNER.read_json(raw)["choices"][0]["message"]["content"], responses)
        state = RUNNER.load_state(self.run)
        self.assertEqual((state["input_tokens"], state["output_tokens"], state["analysis_step_count"]), (22, 14, 2))

    def test_review_cannot_select_arbitrary_contract_fields_or_invent_tasks(self):
        for response in ({"issues": {"preserves": "Invented task."}}, {"contract_repairs": {self.identifiers[0]: ["preserves"]}}):
            provider = mock.Mock(return_value=api_response(response))
            with self.assertRaises(RUNNER.PausedError):
                self.review(provider)
            self.assertEqual(provider.call_count, 3)

    def test_empty_case_with_no_hard_contract_has_no_review_request(self):
        target = node("unconditional_ending", "ending")
        self.frontier = [target]
        source = node("unconditional_scene")
        self.patch["nodes"] = [RUNNER.compile_scaffold_connections(source, [target], selection(source, [target]), GENESIS)]
        provider = mock.Mock(side_effect=AssertionError("Unconditional transition requested proof"))
        self.assertEqual(self.review(provider), [])
        provider.assert_not_called()

    def test_review_omits_older_routes_and_keeps_complete_patch_evidence(self):
        support = self.patch["nodes"][0]["successors"][0]["supports"][0]
        support["genesis_source_ids"] = ["genesis_patch"]
        source = {"source_id": "genesis_patch", "source_commit_id": "commit_genesis", "source_hash": "a" * 64,
            "record_pointer": "/constraint_delta/canonical_facts/0", "authority": "COMMITTED SOURCE EVIDENCE",
            "immutable_source": {"status": "contested", "value": " Synthetic complete evidence.\r\nKeep spacing and λ.  "}}
        before = RUNNER.canonical_json([self.patch, self.frontier, source])
        transport = mock.Mock(return_value=api_response({"issues": {}}))
        with mock.patch.object(RUNNER, "retrieve_original_sources", return_value=[source]) as retrieve:
            self.assertEqual(self.review(transport), [])
        retrieve.assert_called_once_with(self.run, [{"sources": [{"artifact_id": "genesis_patch"}]}],
            limit=None, strict=True, follow_sources=False)
        contexts = [json.loads(call.args[2]["messages"][1]["content"].split("LOCAL PLANNING CONTEXT\n\n", 1)[1]) for call in transport.call_args_list]
        self.assertEqual([item for context in contexts for item in context["committed_genesis_sources"]], [source])
        self.assertNotIn("older_genesis_citation", json.dumps(contexts))
        self.assertEqual(RUNNER.canonical_json([self.patch, self.frontier, source]), before)


if __name__ == "__main__":
    unittest.main()
