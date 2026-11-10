"""Offline provider transport and preserved Architecture repair regressions."""

import contextlib
import copy
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

from test_cathedrals import RUNNER, architecture_core_payload, architecture_genesis_records, attractor


def valid_architecture_payload():
    value = architecture_core_payload()
    value["arcs"] = [copy.deepcopy(value["arcs"][0]) | {"arc_id": f"arc_{index}"} for index in range(4)]
    return value


def event(delta=None, finish=None, usage=None):
    value = {"choices": [] if usage else [{"index": 0, "delta": delta or {}, "finish_reason": finish}]}
    if usage:
        value["usage"] = usage
    return ("data: " + json.dumps(value, ensure_ascii=False) + "\r\n\r\n").encode()


class Stream(io.BytesIO):
    def __init__(self, data=b"", *, chunks=None, content_type="text/event-stream"):
        super().__init__(data)
        self.headers = {"Content-Type": content_type}
        self.chunks = iter(chunks) if chunks is not None else None

    def read1(self, size=-1):
        if self.chunks is None:
            return super().read1(size)
        value = next(self.chunks, b"")
        if isinstance(value, BaseException):
            raise value
        return value


class ProviderStreamingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        with mock.patch.object(RUNNER, "RUNTIME_ROOT", self.root / ".cathedrals"), mock.patch.object(
            RUNNER, "RUNS_ROOT", self.root / ".cathedrals/runs"
        ):
            self.run = RUNNER.create_run(RUNNER.FrozenInputs(possible_scene_count=20),
                "http://offline.invalid", "offline", output_fn=lambda _: None)

    def test_split_utf8_reasoning_and_usage_reconstruct_one_response(self):
        data = (b": heartbeat\r\n\r\n" + event({"role": "assistant"})
                + event({"reasoning_content": "Synthetic reasoning."})
                + event({"content": '{"snow":"雪"}'}) + event(finish="stop")
                + event(usage={"prompt_tokens": 11, "completion_tokens": 7,
                               "completion_tokens_details": {"reasoning_tokens": 2}})
                + b"data: [DONE]\n\n")
        archive = io.BytesIO()
        response = RUNNER.read_chat_stream(Stream(chunks=[bytes([value]) for value in data]), archive=archive, report=False)
        self.assertEqual(RUNNER.normalize_provider_response(response), '{"snow":"雪"}')
        self.assertEqual(response["choices"][0]["message"]["reasoning_content"], "Synthetic reasoning.")
        self.assertEqual(response["usage"]["completion_tokens_details"]["reasoning_tokens"], 2)
        self.assertEqual(archive.getvalue(), data)

    def test_multiline_events_and_reasoning_only_reference(self):
        data = b'data: {\n' + b'data: "choices":[{"delta":{"reasoning":"fact_01"},"finish_reason":"stop"}]}\n\n'
        response = RUNNER.read_chat_stream(Stream(data + b"data: [DONE]\n\n"), report=False)
        self.assertEqual(RUNNER.normalize_provider_response(response, plain_answers={"fact_01"}), "fact_01")

    def test_active_stream_can_take_longer_than_one_hour(self):
        clock = [0]
        chunks = iter([event({"content": "{}"}), event(finish="stop"), b"data: [DONE]\n\n"])

        def read(_size):
            clock[0] += 2000
            return next(chunks, b"")

        output = io.StringIO()
        with mock.patch.object(RUNNER.time, "monotonic", side_effect=lambda: clock[0]), contextlib.redirect_stderr(output):
            response = RUNNER.read_chat_stream(mock.Mock(read1=read))
        self.assertEqual(RUNNER.normalize_provider_response(response), "{}")
        self.assertIn("4000s elapsed", output.getvalue())
        self.assertIn("2 characters received", output.getvalue())
        self.assertNotIn("{}", output.getvalue())

    def test_explicit_token_limit_is_distinct_from_incomplete_stream(self):
        response = RUNNER.read_chat_stream(Stream(event({"content": "partial"}, "length") + b"data: [DONE]\n\n"), report=False)
        with self.assertRaises(RUNNER.TruncationError):
            RUNNER.normalize_provider_response(response)
        for data in (event({"content": "partial"}), event(finish="stop"), b"data: nonsense\n\n",
                     b'data: {"error":{"message":"failure"}}\n\n', b"data: [DONE]\n\n"):
            with self.subTest(data=data), self.assertRaises(RUNNER.IncompleteResponseError):
                RUNNER.read_chat_stream(Stream(data), report=False)

    def test_buffered_json_is_still_supported(self):
        value = {"choices": [{"finish_reason": "stop", "message": {"content": "{}"}}]}
        with mock.patch.object(RUNNER.urllib.request, "urlopen", return_value=Stream(json.dumps(value).encode(), content_type="application/json")), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(RUNNER.http_json("POST", "http://offline.invalid", {"stream": True}), value)
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.parse_structured_content('{"unfinished":')

    def test_context_refusal_preserves_full_error_and_names_the_loaded_capacity(self):
        detail = ('Engine protocol predict request returned 400: {"error":{"code":400,"message":'
            '"request (23308 tokens) exceeds the available context size (8192 tokens), try increasing it",'
            '"type":"exceed_context_size_error","n_prompt_tokens":23308,"n_ctx":8192}}')
        data = ('event: error\ndata: ' + json.dumps({"error": {"message": detail}}) + '\n\n').encode()
        archive = io.BytesIO()
        with self.assertRaises(RUNNER.IncompleteResponseError) as raised:
            RUNNER.read_chat_stream(Stream(data), archive=archive, report=False)
        error = raised.exception
        self.assertEqual(error.stage, "LM Studio context capacity")
        self.assertIn("23,308", error.reason)
        self.assertIn("8,192", error.reason)
        self.assertIn("64,148", error.reason)
        self.assertIn(detail, error.reason)
        self.assertNotIn("Invalid stream event", error.reason)
        self.assertEqual(archive.getvalue(), data)
        self.assertEqual(error.response["_cathedrals_provider_error"]["message"], detail)
        with self.assertRaises(RUNNER.IncompleteResponseError) as replayed:
            RUNNER.normalize_provider_response(error.response)
        self.assertEqual(replayed.exception.stage, error.stage)
        self.assertIn(detail, replayed.exception.reason)

    def test_context_refusal_archives_one_attempt_without_retrying(self):
        detail = "request (23308 tokens) exceeds the available context size (8192 tokens), try increasing it"
        data = ('data: ' + json.dumps({"error": {"message": detail}}) + '\n\n').encode()
        with mock.patch.object(RUNNER.urllib.request, "urlopen", return_value=Stream(data)) as post, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(RUNNER.IncompleteResponseError):
                RUNNER.request_record(self.run, expected_record_type="genesis_foundation", step_id="context_refused", phase="genesis",
                    prompt="prompt", context="context", branch_relation="root", temperature=0.8)
        post.assert_called_once()
        raw = self.run / "raw/context_refused-attempt1.api.json"
        self.assertIn(detail, RUNNER.read_json(raw)["_cathedrals_error"])
        self.assertEqual(raw.with_suffix(".sse").read_bytes(), data)
        self.assertEqual(len(RUNNER.step_entries(self.run, "context_refused")), 1)
        self.assertFalse((self.run / "state/inflight.json").exists())

    def test_interrupted_stream_saves_partial_evidence_and_resume_uses_new_attempt(self):
        prefix = event({"content": '{"name":'})
        arguments = dict(expected_record_type="genesis_foundation", step_id="stream_test", phase="genesis",
            prompt="prompt", context="context", branch_relation="root", temperature=0.8,
            response_definition="claimantAnchorPayload")
        with mock.patch.object(RUNNER.urllib.request, "urlopen", return_value=Stream(chunks=[prefix, TimeoutError("timed out")])) as post, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(RUNNER.IncompleteResponseError):
                RUNNER.request_record(self.run, **arguments)
        post.assert_called_once()
        raw = self.run / "raw/stream_test-attempt1.api.json"
        original = raw.read_bytes()
        partial = RUNNER.read_json(raw)
        self.assertFalse(partial["_cathedrals_stream_complete"])
        self.assertEqual(partial["choices"][0]["message"]["content"], '{"name":')
        self.assertEqual(raw.with_suffix(".sse").read_bytes(), prefix)
        self.assertFalse((self.run / "state/inflight.json").exists())
        self.assertEqual(RUNNER.ledger_entries(self.run)[-1]["failure_class"], "provider_incomplete_response")
        with self.assertRaises(RUNNER.IncompleteResponseError):
            RUNNER.normalize_provider_response(partial)
        response = {"choices": [{"finish_reason": "stop", "message": {"content": '{"name":"Synthetic","incident_role":"Witness"}'}}]}
        with self.assertRaises(RUNNER.PausedError):
            RUNNER.request_record(self.run, **arguments, transport=lambda *a, **kw: response,
                record_builder=mock.Mock(side_effect=RUNNER.PausedError("test", "before commit")))
        self.assertEqual(raw.read_bytes(), original)
        self.assertTrue((self.run / "raw/stream_test-attempt2.api.json").exists())
        self.assertEqual(len([e for e in RUNNER.ledger_entries(self.run) if e["failure_class"] == "provider_incomplete_response"]), 1)

    @mock.patch.object(RUNNER, "audit_scaffold_guarantees", new=lambda *args, **kwargs: None)
    def test_every_request_path_pauses_after_one_timeout(self):
        operations = [
            lambda: RUNNER.request_record(self.run, expected_record_type="genesis_foundation", step_id="creative_timeout",
                phase="genesis", prompt="prompt", context="context", branch_relation="root", temperature=0.8),
            lambda: RUNNER.request_architecture_analysis(self.run, "repair_timeout", "prompt", {"type": "object"}, RUNNER.http_json),
            lambda: RUNNER.resolve_named_reference(self.run, "reference_timeout", {"path": ["test"], "kind": "test",
                "invalid": "missing", "context": "synthetic", "candidates": {"fact_01": "Synthetic fact."}}),
            lambda: RUNNER.request_semantic_normalization(self.run, "semantic_timeout", {"scenes": [], "endings": []}, "context"),
        ]
        for operation in operations:
            before = len(RUNNER.ledger_entries(self.run))
            with self.subTest(operation=before), mock.patch.object(RUNNER.urllib.request, "urlopen", side_effect=urllib.error.URLError(TimeoutError("timed out"))) as post, contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises((RUNNER.IncompleteResponseError, RUNNER.PausedError)) as raised:
                    operation()
                self.assertEqual(raised.exception.failure_class, "provider_incomplete_response")
                post.assert_called_once()
                self.assertTrue(json.loads(post.call_args.args[0].data)["stream"])
                self.assertEqual(json.loads(post.call_args.args[0].data)["stream_options"], {"include_usage": True})
            self.assertEqual(len(RUNNER.ledger_entries(self.run)), before + 1)

    def test_completed_archive_replays_without_contacting_provider(self):
        path = self.root / "complete.sse"
        path.write_bytes(event({"content": "{}"}, "stop") + b"data: [DONE]\n\n")
        transport = mock.Mock(side_effect=AssertionError("network"))
        preserve = mock.Mock()
        _, content = RUNNER.provider_response(transport, "http://offline.invalid", {}, 3600, stream_path=path, preserve=preserve)
        self.assertEqual(content, "{}")
        transport.assert_not_called()
        preserve.assert_called_once()

    def test_resume_uses_its_frozen_transport_and_retains_injected_transports(self):
        run = self.root / "snapshot_test"
        launcher = run / "engine-snapshot/cathedrals"
        launcher.parent.mkdir(parents=True)
        launcher.write_text(
            "def http_json(*args, **kwargs):\n    pass\n"
            "def main(argv=None, **kwargs):\n    return kwargs['transport'] is http_json\n")
        self.assertTrue(RUNNER.run_snapshot_launcher(run, [], None, None, RUNNER.http_json))
        transport = mock.Mock(side_effect=AssertionError("network"))
        self.assertFalse(RUNNER.run_snapshot_launcher(run, [], None, None, transport))
        transport.assert_not_called()

    def test_resume_explains_a_different_snapshot_without_changing_it(self):
        run = self.root / "resume_snapshot"
        launcher = run / "engine-snapshot/cathedrals"
        launcher.parent.mkdir(parents=True)
        (launcher.parent / "engine").mkdir()
        for different in (True, False):
            with self.subTest(different=different):
                launcher.write_bytes(b"# Preserved older engine.\n" if different else Path(RUNNER.__file__).read_bytes())
                before = launcher.read_bytes()
                output = []
                with mock.patch.object(RUNNER, "ensure_runtime_layout"), mock.patch.object(RUNNER, "choose_resume", return_value=run), mock.patch.object(
                    RUNNER, "run_snapshot_launcher", return_value=2
                ) as delegate:
                    self.assertEqual(RUNNER.main([], output_fn=output.append), 2)
                delegate.assert_called_once()
                self.assertEqual(launcher.read_bytes(), before)
                self.assertEqual(any("Installation updates do not apply" in line for line in output), different)

    def test_connection_failures_retry_the_identical_request(self):
        calls = []

        def transport(_method, _url, payload, **_kwargs):
            calls.append(payload)
            if len(calls) == 1:
                raise RUNNER.CathedralsError("test", "connection refused", "transport_before_response")
            return {"choices": [{"finish_reason": "stop", "message": {"content": '{"name":"Synthetic","incident_role":"Witness"}'}}]}

        with self.assertRaises(RUNNER.PausedError):
            RUNNER.request_record(self.run, expected_record_type="genesis_foundation", step_id="connection_test",
                phase="genesis", prompt="prompt", context="context", branch_relation="root", temperature=0.8,
                response_definition="claimantAnchorPayload", transport=transport,
                record_builder=mock.Mock(side_effect=RUNNER.PausedError("test", "before commit")))
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0], calls[1])


    def test_repair_budget_is_enforced_before_a_provider_call(self):
        manifest = RUNNER.read_json(self.run / "run-manifest.json")
        manifest["budgets"]["max_cumulative_output_tokens"] = 0
        RUNNER.write_json(self.run / "run-manifest.json", manifest)
        transport = mock.Mock(side_effect=AssertionError("network"))
        with self.assertRaises(RUNNER.CathedralsError) as raised:
            RUNNER.request_architecture_analysis(self.run, "budget_test", "prompt", {"type": "object"}, transport)
        self.assertEqual(raised.exception.failure_class, "budget_exhaustion")
        transport.assert_not_called()




if __name__ == "__main__":
    unittest.main()
