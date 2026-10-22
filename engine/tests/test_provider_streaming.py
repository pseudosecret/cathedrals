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

    def test_every_request_path_pauses_after_one_timeout(self):
        operations = [
            lambda: RUNNER.request_record(self.run, expected_record_type="genesis_foundation", step_id="creative_timeout",
                phase="genesis", prompt="prompt", context="context", branch_relation="root", temperature=0.8),
            lambda: RUNNER.request_architecture_analysis(self.run, "repair_timeout", "prompt", {"type": "object"}, RUNNER.http_json),
            lambda: RUNNER.resolve_named_reference(self.run, "reference_timeout", {"path": ["test"], "kind": "test",
                "invalid": "missing", "context": "synthetic", "candidates": {"fact_01": "Synthetic fact."}}),
            lambda: RUNNER.request_semantic_normalization(self.run, "semantic_timeout", {"scenes": [], "endings": []}, "context"),
            lambda: RUNNER.request_analysis(self.run, "analysis_timeout", "prompt"),
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

    def test_invalid_focused_corrections_exhaust_without_regenerating_draft(self):
        payload = valid_architecture_payload()
        payload["obligation_graph"][0]["termination_targets"].append("attractor_missing")
        records = architecture_genesis_records()
        calls = []

        def transport(_method, _url, request, **_kwargs):
            schema = request["response_format"]["json_schema"]["schema"]
            calls.append(request["response_format"]["json_schema"]["name"])
            result = {"resolutions": {key: "UNRESOLVED" for key in schema["properties"]["resolutions"]["properties"]}} if "resolutions" in schema["properties"] else {}
            return {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(result)}}]}

        arguments = dict(expected_record_type="architecture_core", step_id="architecture_core", phase="architecture",
            prompt="prompt", context="context", branch_relation="root", temperature=0.7,
            response_definition="architectureCorePayload",
            payload_repairer=lambda step, value, content, response: RUNNER.repair_architecture_core_payload(
                self.run, step, value, content, response, transport))
        response = {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(payload)}}]}
        with mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: records.get(kind)), mock.patch.object(
            RUNNER, "_source_index", return_value={"commit_foundation": {}}
        ), self.assertRaisesRegex(RUNNER.PausedError, "exhausted 3 focused"):
            RUNNER.request_record(self.run, transport=lambda *a, **kw: response, **arguments)
        self.assertEqual(calls, ["architectureRepair"] * 4)
        self.assertEqual(RUNNER.read_json(self.run / ".staging/architecture_core.artistic.json"), payload)
        self.assertFalse((self.run / "finalization.json").exists())

    def test_repair_budget_is_enforced_before_a_provider_call(self):
        manifest = RUNNER.read_json(self.run / "run-manifest.json")
        manifest["budgets"]["max_cumulative_output_tokens"] = 0
        RUNNER.write_json(self.run / "run-manifest.json", manifest)
        transport = mock.Mock(side_effect=AssertionError("network"))
        with self.assertRaises(RUNNER.CathedralsError) as raised:
            RUNNER.request_architecture_analysis(self.run, "budget_test", "prompt", {"type": "object"}, transport)
        self.assertEqual(raised.exception.failure_class, "budget_exhaustion")
        transport.assert_not_called()

    def test_architecture_resume_reuses_draft_and_lookup_without_double_accounting(self):
        payload = valid_architecture_payload()
        payload["obligation_graph"][0]["termination_targets"].append("attractor_missing")
        arguments = dict(expected_record_type="architecture_core", step_id="architecture_core", phase="architecture",
            prompt="prompt", context="context", branch_relation="root", temperature=0.7,
            response_definition="architectureCorePayload",
            payload_repairer=lambda step, value, content, response: RUNNER.repair_architecture_core_payload(
                self.run, step, value, content, response, transport),
            record_builder=mock.Mock(side_effect=RUNNER.PausedError("test", "before commit")))
        calls = []

        def transport(_method, _url, request, **_kwargs):
            name = request["response_format"]["json_schema"]["name"]
            schema = request["response_format"]["json_schema"]["schema"]
            calls.append(name)
            if name == "architectureCorePayload":
                value = payload
            elif "resolutions" in schema["properties"]:
                value = {"resolutions": {key: "UNRESOLVED" for key in schema["properties"]["resolutions"]["properties"]}}
            elif calls.count("architectureRepair") == 2:
                raise RUNNER.IncompleteResponseError("simulated timeout")
            else:
                value = {"replacement": "attractor_missing", "new_obligation": None,
                    "new_attractor": copy.deepcopy(payload["attractors"][0]) | {"attractor_id": "attractor_missing"}}
            return {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(value)}}],
                    "usage": {"prompt_tokens": 11, "completion_tokens": 7}}

        records = architecture_genesis_records()
        with mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: records.get(kind)), mock.patch.object(
            RUNNER, "_source_index", return_value={"commit_foundation": {}}
        ):
            for _ in range(2):
                with self.assertRaises(RUNNER.PausedError):
                    RUNNER.request_record(self.run, transport=transport, **arguments)
        history = RUNNER.read_json(self.run / ".staging/architecture_core.repair.json")["history"]
        self.assertEqual(calls, ["architectureCorePayload", "architectureRepair", "architectureRepair", "architectureRepair"])
        self.assertEqual(len(history), 2)
        self.assertEqual(sum(item["api_response"]["usage"]["completion_tokens"] for item in history), 14)
        failures = [entry for entry in RUNNER.ledger_entries(self.run) if entry["failure_class"] == "provider_incomplete_response"]
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0]["step_type"], "analysis")

    def test_architecture_preserves_draft_with_a_reference_that_fails_id_pattern(self):
        payload = valid_architecture_payload()
        payload["arcs"][0]["claimant_pressures"] = ["Claimant One"]
        records = architecture_genesis_records()
        calls = []

        def transport(_method, _url, request, **_kwargs):
            schema = request["response_format"]["json_schema"]["schema"]
            calls.append(request["response_format"]["json_schema"]["name"])
            result = {"resolutions": {key: "claimant_01" for key in schema["properties"]["resolutions"]["properties"]}} if "resolutions" in schema["properties"] else payload
            return {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(result)}}]}

        with mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: records.get(kind)), mock.patch.object(
            RUNNER, "_source_index", return_value={"commit_foundation": {}}
        ), self.assertRaises(RUNNER.PausedError):
            RUNNER.request_record(self.run, expected_record_type="architecture_core", step_id="architecture_core", phase="architecture",
                prompt="prompt", context="context", branch_relation="root", temperature=0.7,
                response_definition="architectureCorePayload", transport=transport,
                payload_repairer=lambda step, value, content, response: RUNNER.repair_architecture_core_payload(
                    self.run, step, value, content, response, transport),
                record_builder=mock.Mock(side_effect=RUNNER.PausedError("test", "before commit")))
        self.assertEqual(calls, ["architectureCorePayload", "architectureRepair"])
        self.assertEqual(RUNNER.read_json(self.run / ".staging/architecture_core.artistic.json"), payload)
        repaired = RUNNER.read_json(self.run / ".staging/architecture_core.repair.json")["payload"]
        self.assertEqual(repaired["arcs"][0]["claimant_pressures"], ["claimant_01"])


class ArchitectureLocalRepairTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.run = Path(self.temporary.name)
        self.records = architecture_genesis_records()
        for patch in (mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: self.records.get(kind)),
                      mock.patch.object(RUNNER, "_source_index", return_value={"commit_foundation": {}})):
            patch.start()
            self.addCleanup(patch.stop)

    def test_missing_attractor_is_added_without_rewriting_the_draft(self):
        payload = valid_architecture_payload()
        payload["obligation_graph"][0]["termination_targets"].append("attractor_missing")
        original = copy.deepcopy(payload)
        addition = {key: value for key, value in attractor(attractor_id="attractor_missing").items() if key != "ending_slot_ids"}

        def repair(_run, _step, _prompt, schema, _transport, validator=None):
            self.assertTrue((self.run / ".staging/architecture_core.artistic.json").exists())
            if "resolutions" in schema["properties"]:
                result = {"resolutions": {key: "UNRESOLVED" for key in schema["properties"]["resolutions"]["properties"]}}
            else:
                result = {"replacement": "attractor_missing", "new_attractor": addition, "new_obligation": None}
            RUNNER.validate_json_schema(result, schema)
            if validator:
                validator(result)
            return result, {"usage": {"prompt_tokens": 11, "completion_tokens": 7}}

        with mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=repair) as requests:
            result = RUNNER.repair_architecture_core_payload(self.run, "architecture_core", payload, json.dumps(payload), {}, None)
            resumed = RUNNER.repair_architecture_core_payload(self.run, "architecture_core", payload, json.dumps(payload), {}, None)
        self.assertEqual(requests.call_count, 2)
        self.assertEqual(result, resumed)
        self.assertEqual(payload, original)
        self.assertEqual(result["attractors"][:-1], original["attractors"])
        self.assertEqual(result["arcs"], original["arcs"])
        self.assertEqual(result["topology"], original["topology"])
        self.assertEqual(RUNNER.read_json(self.run / ".staging/architecture_core.artistic.json"), original)

    def test_wrong_typed_optional_reference_can_be_removed(self):
        for identifier in ("motif_event_wrong", "attractor_one"):
            with self.subTest(identifier=identifier):
                payload = valid_architecture_payload()
                payload["topology"]["edges"][0]["hard_obligation_ids"] = [identifier]
                issue = RUNNER.architecture_reference_issues(payload, self.run)[0]
                result = RUNNER.apply_architecture_local_repair(payload, issue,
                    {"replacement": None, "new_obligation": None, "new_attractor": None}, self.run)
                self.assertEqual(result["topology"]["edges"][0]["hard_obligation_ids"], [])

    def test_new_obligation_and_relevance_reference_inventory(self):
        payload = valid_architecture_payload()
        payload["arcs"][0]["hard_obligation_ids"] = ["obligation_missing"]
        issue = RUNNER.architecture_reference_issues(payload, self.run)[0]
        addition = copy.deepcopy(payload["obligation_graph"][0]) | {"obligation_id": "obligation_missing"}
        result = RUNNER.apply_architecture_local_repair(payload, issue,
            {"replacement": "obligation_missing", "new_obligation": addition, "new_attractor": None}, self.run)
        self.assertEqual(result["obligation_graph"][-1]["obligation_id"], "obligation_missing")
        payload["attractors"][0]["relevance"] = {"claimant_ids": ["claimant_missing"], "arc_ids": ["arc_missing"]}
        fields = {RUNNER.reference_path(item["path"]) for item in RUNNER.architecture_reference_issues(payload, self.run)}
        self.assertIn("$.attractors[0].relevance.claimant_ids[0]", fields)
        self.assertIn("$.attractors[0].relevance.arc_ids[0]", fields)

    def test_local_repair_rejects_unrelated_changes_and_schema_overflow(self):
        payload = valid_architecture_payload()
        payload["obligation_graph"][0]["termination_targets"].append("attractor_missing")
        issue = RUNNER.architecture_reference_issues(payload, self.run)[0]
        addition = copy.deepcopy(payload["attractors"][0]) | {"attractor_id": "attractor_missing"}
        for replacement, record in (("attractor_missing", addition | {"attractor_id": "unrelated"}),
                                    ("invented", None)):
            with self.subTest(replacement=replacement), self.assertRaises(RUNNER.SchemaError):
                RUNNER.apply_architecture_local_repair(payload, issue,
                    {"replacement": replacement, "new_obligation": None, "new_attractor": record}, self.run)
        payload["attractors"] = [copy.deepcopy(payload["attractors"][0]) | {"attractor_id": f"attractor_{i}"} for i in range(16)]
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.apply_architecture_local_repair(payload, issue,
                {"replacement": "attractor_missing", "new_obligation": None, "new_attractor": addition}, self.run)


if __name__ == "__main__":
    unittest.main()
