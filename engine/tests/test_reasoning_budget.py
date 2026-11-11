"""Reasoning uses physical context; quotas and resumable review pages count final output."""
import copy
import json
import unittest
from unittest import mock

from test_cathedrals import RUNNER
from test_backward_scaffold import node
import test_reference_resolution as fixtures
from test_reference_resolution import api_response


class ReasoningBudgetTests(unittest.TestCase):
    def setUp(self):
        fixtures.ReferenceResolutionTests.setUp(self)

    def response(self, value, *, truncated=False):
        response = api_response(value)
        response["usage"] = {"prompt_tokens": 11, "completion_tokens": 35000,
            "completion_tokens_details": {"reasoning_tokens": 34998}}
        response["choices"][0]["finish_reason"] = "length" if truncated else "stop"
        return response

    def test_provider_generation_space_covers_reasoning_and_complete_envelope(self):
        request = {"messages": [{"role": "system", "content": "Test"}, {"role": "user", "content": "Test JSON"}],
            "response_format": {"type": "json_schema", "json_schema": {"schema": {"type": "object"}}}}
        parameters = {"max_tokens": 3072}
        window = RUNNER.read_json(self.run / "run-manifest.json")["budgets"]["model_context_window_tokens"]
        limit = RUNNER.set_provider_output_limit(self.run, request, parameters, "Test")
        self.assertGreater(limit, 15000)
        self.assertEqual(limit, parameters["max_tokens"])
        self.assertEqual(limit + RUNNER.provider_input_tokens(request) + 4096 + 16, window)
        state = RUNNER.load_state(self.run)
        state["model_context_window_tokens"] = 4096
        RUNNER.save_state(self.run, state)
        with self.assertRaisesRegex(RUNNER.PausedError, "Complete request leaves"):
            RUNNER.set_provider_output_limit(self.run, request, parameters, "Test")

    def test_final_usage_is_separate_and_missing_reasoning_is_labeled_estimate(self):
        response = self.response({"issues": {}})
        before = copy.deepcopy(response)
        usage = RUNNER.provider_usage(response)
        self.assertEqual(usage["final_output_tokens"], 2)
        self.assertFalse(usage["final_output_tokens_estimated"])
        self.assertEqual(response, before)
        unknown = api_response("answer", text=True)
        unknown["choices"][0]["message"]["reasoning_content"] = "reason " * 10000
        usage = RUNNER.provider_usage(unknown)
        self.assertEqual(usage["final_output_tokens"], RUNNER.estimated_prompt_tokens("answer"))
        self.assertTrue(usage["final_output_tokens_estimated"])
        self.assertEqual(usage["completion_tokens"], 7)
        unknown["choices"][0]["message"]["content"] = None
        unknown["choices"][0]["message"]["tool_calls"] = [{"function": {"name": "get_records", "arguments": "{}"}}]
        self.assertGreater(RUNNER.provider_usage(unknown)["final_output_tokens"], 0)
        unknown["_cathedrals_semantic_assembled"] = True
        self.assertEqual(RUNNER.provider_usage(unknown), {})
        self.assertEqual(RUNNER.provider_usage({"choices": [{"message": {"content": ["invalid"]}}]})["final_output_tokens"], 0)

    def test_reasoning_does_not_spend_final_output_quota_and_replay_does_not_spend_twice(self):
        manifest = RUNNER.read_json(self.run / "run-manifest.json")
        manifest["budgets"]["max_cumulative_output_tokens"] = 4000
        RUNNER.write_json(self.run / "run-manifest.json", manifest)
        schema = {"type": "object", "required": ["ok"], "properties": {"ok": {"const": True}}, "additionalProperties": False}
        provider = mock.Mock(side_effect=lambda *_args, **_kwargs: self.response({"ok": True}))
        for query in ("reason_first", "reason_second"):
            result, response = RUNNER.request_architecture_analysis(self.run, query, "Small task", schema,
                provider, planning_mode=True, max_tokens=3072)
            RUNNER.preserve_planning_result(self.run, "architecture_core", query, result, response, kind="test")
        self.assertEqual(RUNNER.load_state(self.run)["output_tokens"], 70000)
        self.assertEqual(RUNNER.final_output_token_total(self.run), 4)
        before = (self.run / "ledger.jsonl").read_bytes()
        forbidden = mock.Mock(side_effect=AssertionError("Accepted response requested again"))
        result, response = RUNNER.request_architecture_analysis(self.run, "reason_second", "Small task", schema,
            forbidden, planning_mode=True, max_tokens=3072)
        RUNNER.preserve_planning_result(self.run, "architecture_core", "reason_second", result, response, kind="test")
        self.assertEqual((self.run / "ledger.jsonl").read_bytes(), before)
        forbidden.assert_not_called()

    def pages(self, tasks, provider, prepare=None):
        def default_prepare(page):
            return json.dumps({"tasks": page}), {"type": "object", "required": ["issues"], "additionalProperties": False,
                "properties": {"issues": {"type": "object", "additionalProperties": False,
                    "properties": {key: {"type": "string"} for key in page}}}}, None
        return RUNNER.request_analysis_task_pages(self.run, "architecture_core", "test_review", tasks,
            prepare or default_prepare, provider, result_key="issues", kind="scaffold_connection_review", max_tokens=3072,
            pause_stage="Scaffold causal support")

    def test_sixteen_task_review_splits_truncations_and_reuses_complete_pages(self):
        ledger_start = len(RUNNER.ledger_entries(self.run))
        tasks = {f"task_{index:02d}": {"owner": f"scene_{index}"} for index in range(16)}
        sizes = []
        def provider(_method, _url, request, **_kwargs):
            page = json.loads(request["messages"][1]["content"])["tasks"]
            sizes.append(len(page))
            self.assertGreater(request["max_tokens"], 3072)
            return self.response({"issues": {min(page): "Needs a stronger proof."}}, truncated=len(page) == 4)
        result = self.pages(tasks, provider)
        self.assertEqual(sizes, [4, 2, 2] * 4)
        self.assertEqual(len(result), 8)
        self.assertEqual(len(RUNNER.ledger_entries(self.run)) - ledger_start, 12)
        self.assertEqual(RUNNER.final_output_token_total(self.run), 24)
        checkpoint = RUNNER.read_json(self.run / ".staging/test_review.pages.json")
        self.assertEqual(len(checkpoint["splits"]), 4)
        before = (self.run / "ledger.jsonl").read_bytes()
        forbidden = mock.Mock(side_effect=AssertionError("Replayed split or accepted page"))
        self.assertEqual(self.pages(tasks, forbidden), result)
        forbidden.assert_not_called()
        self.assertEqual((self.run / "ledger.jsonl").read_bytes(), before)

    def test_interruption_preserves_accepted_pages_and_single_task_exhaustion_pauses(self):
        tasks = {f"task_{index:02d}": {} for index in range(8)}
        provider = mock.Mock(side_effect=[self.response({"issues": {}}), RUNNER.IncompleteResponseError("Offline", {})])
        with self.assertRaisesRegex(RUNNER.PausedError, "Offline"):
            self.pages(tasks, provider)
        resumed = mock.Mock(return_value=self.response({"issues": {}}))
        self.assertEqual(self.pages(tasks, resumed), {})
        resumed.assert_called_once()
        self.assertEqual(RUNNER.final_output_token_total(self.run), 4)
        singleton = {"only_task": {}}
        exhausted = mock.Mock(return_value=self.response({"issues": {}}, truncated=True))
        for _ in range(2):
            with self.assertRaisesRegex(RUNNER.PausedError, "only_task.*exhausted"):
                self.pages(singleton, exhausted)
        exhausted.assert_called_once()

    def test_writing_audit_splits_and_keeps_exact_sources_scoped_to_each_page(self):
        entries = [(f"case_{index}", f"source_{index}") for index in range(6)]
        contract = node("audit_scene", cases=[{"case_id": case, "requirements": []} for case, _source in entries])
        local = {"incoming": [], "inherited_guarantee_evidence": [], "opening_support": []}
        units = {source: [f"  Complete evidence {source}.\nKeep λ.  "] for _case, source in entries}
        allowed = {entry: {entry[1]} for entry in entries}
        sizes = []
        def provider(_method, _url, request, **_kwargs):
            context = json.loads(request["messages"][1]["content"].split("LOCAL AUDIT CONTEXT\n\n", 1)[1])
            tasks = context["tasks"]
            sizes.append(len(tasks))
            sources = {source for task in tasks.values() for source in task["source_ids"]}
            self.assertEqual(context["immutable_source_units"], {source: units[source] for source in sorted(sources)})
            if len(tasks) == 4:
                return self.response({"tasks": {}}, truncated=True)
            return self.response({"tasks": {identifier: {"supported": True, "reason": "Exact immutable source.",
                "evidence_quotes": [{"source_id": task["source_ids"][0], "quote": units[task["source_ids"][0]][0]}]}
                for identifier, task in tasks.items()}})
        def audit(transport):
            return RUNNER.request_scaffold_audit_tasks(self.run, "packet_test", "audit_test", contract, local,
                [("guarantee", "Evidence applies.")], entries, allowed, units, transport)
        result, _assembled = audit(provider)
        self.assertEqual(sizes, [4, 2, 2, 2])
        self.assertEqual(len(result["checks"]), 6)
        before = (self.run / "ledger.jsonl").read_bytes()
        forbidden = mock.Mock(side_effect=AssertionError("Accepted audit requested again"))
        self.assertEqual(audit(forbidden)[0], result)
        forbidden.assert_not_called()
        self.assertEqual((self.run / "ledger.jsonl").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
