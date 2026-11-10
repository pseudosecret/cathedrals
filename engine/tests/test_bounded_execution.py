"""Bounded planning, read tools, capability fallback and historical propositions."""
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_cathedrals import RUNNER, architecture_core_payload, architecture_genesis_records
from test_reference_resolution import api_response, planning_response
from test_provider_streaming import Stream, event

POLICY = {"bounded_planning": True, "scoped_sources": True, "retrieval_mode": "automatic", "max_tool_rounds": 2, "max_tool_calls": 8}


def call(name="get_plan_items", args=None, identity="call_one"):
    return {"id": identity, "type": "function", "function": {"name": name, "arguments": json.dumps(args or {"ids": ["arc_001"]})}}


def tool_response(calls):
    return {"choices": [{"finish_reason": "tool_calls", "message": {"role": "assistant", "content": None, "tool_calls": calls}}],
        "usage": {"prompt_tokens": 11, "completion_tokens": 7}}


class BoundedExecutionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        with mock.patch.object(RUNNER, "RUNTIME_ROOT", self.root), mock.patch.object(RUNNER, "RUNS_ROOT", self.root / "runs"):
            self.run = RUNNER.create_run(RUNNER.FrozenInputs(possible_scene_count=30), "http://offline.invalid", "offline",
                output_fn=lambda _: None, execution_policy=POLICY)

    def test_fragmented_multiple_tool_calls_require_complete_stream(self):
        data = event({"tool_calls": [{"index": 1, "id": "call_", "function": {"name": "get_", "arguments": '{"ids":['}}]})
        data += event({"tool_calls": [{"index": 0, **call(identity="call_zero")}]})
        data += event({"tool_calls": [{"index": 1, "id": "one", "function": {"name": "records", "arguments": '"arc_001"]}'}}]})
        data += event(finish="tool_calls") + b"data: [DONE]\n\n"
        response = RUNNER.read_chat_stream(Stream(chunks=[bytes([byte]) for byte in data]), report=False)
        calls = RUNNER.completed_tool_calls(response)
        self.assertEqual([value["id"] for value in calls], ["call_zero", "call_one"])
        self.assertEqual(calls[1]["function"]["name"], "get_records")
        self.assertEqual(json.loads(calls[1]["function"]["arguments"]), {"ids": ["arc_001"]})
        with self.assertRaises(RUNNER.IncompleteResponseError):
            RUNNER.read_chat_stream(Stream(data.removesuffix(b"data: [DONE]\n\n")), report=False)
        self.assertEqual(RUNNER.completed_tool_calls(response | {"_cathedrals_stream_complete": False}), [])

    def test_tentative_projection_rebuilds_from_checkpoint_and_rejects_sql(self):
        state = {"payload": {"arcs": [{"arc_id": "arc_001", "purpose": "Tentative purpose."}]}}
        RUNNER.save_planning_draft(self.run, "architecture_core", state)
        first = RUNNER.read_retrieval_tool(self.run, "get_plan_items", {"ids": ["arc_001"]})
        self.assertEqual(first[0]["authority"], "TENTATIVE PLAN")
        RUNNER.index_path(self.run).unlink()
        RUNNER.ensure_index(self.run)
        self.assertEqual(RUNNER.read_retrieval_tool(self.run, "get_plan_items", {"ids": ["arc_001"]}), first)
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.read_retrieval_tool(self.run, "get_records", {"ids": ["x'; DROP TABLE records;"]})
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.read_retrieval_tool(self.run, "execute_sql", {"sql": "DELETE FROM records"})

    def test_tool_rounds_replay_and_account_once(self):
        RUNNER.save_planning_draft(self.run, "architecture_core", {"payload": {"arcs": [{"arc_id": "arc_001", "purpose": "Test."}]}})
        transport = mock.Mock(side_effect=[tool_response([call()]), api_response("READY", text=True)])
        with mock.patch.object(RUNNER, "execution_policy", return_value=POLICY | {"retrieval_mode": "tools"}):
            result = RUNNER.retrieval_working_set(self.run, "test_task", "Get arc_001", transport)
            replay = RUNNER.retrieval_working_set(self.run, "test_task", "Get arc_001", transport)
        self.assertEqual(result, replay)
        self.assertEqual(result[0]["item"]["arc_id"], "arc_001")
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(RUNNER.load_state(self.run)["input_tokens"], 11)
        self.assertNotIn("response_format", transport.call_args.args[2])

    def test_invalid_arguments_get_one_correction_and_two_round_limit(self):
        transport = mock.Mock(return_value=tool_response([call(args={"ids": ["bad id"]})]))
        with mock.patch.object(RUNNER, "execution_policy", return_value=POLICY | {"retrieval_mode": "tools"}):
            result = RUNNER.retrieval_working_set(self.run, "bad_task", "Get records", transport)
        self.assertEqual(result, [])
        self.assertEqual(transport.call_count, 2)
        audit = RUNNER.read_json(self.run / "raw/bad_task.retrieval-session.json")
        self.assertEqual(audit["argument_errors"], 2)

    def test_preflight_freezes_fallback_or_tools_without_fiction(self):
        metadata = {"proposition": "The synthetic token is blue.", "subject": "synthetic_reader", "relation": "knows"}
        for first, mode in ((api_response("I cannot call tools", text=True), "automatic"),
                (tool_response([call("get_records", {"ids": ["synthetic_token"]})]), "tools")):
            transport = mock.Mock(side_effect=[first, api_response(metadata)])
            policy, artifacts = RUNNER.probe_execution_policy("http://offline.invalid", "offline", transport, lambda _: None)
            self.assertEqual(policy["retrieval_mode"], mode)
            self.assertEqual(policy["completion_contract_version"], 1)
            self.assertEqual(policy["scaffold_planning_version"], 1)
            self.assertEqual(len(artifacts), 2)
            self.assertNotIn("tools", transport.call_args.args[2])
        RUNNER.archive_preflight_probes(self.run, artifacts)
        self.assertEqual(RUNNER.load_state(self.run)["input_tokens"], 22)

    def test_superseded_proposition_remains_known(self):
        event_ = {"data": {"fact_id": "fact_historical"}, "constraint_kind": "canonical_fact"}
        with RUNNER.index_connection(self.run) as db:
            db.execute("INSERT INTO events VALUES (?,?,?,?)", (1, "constraint_test", "canonical_fact", json.dumps(event_)))
        self.assertIn("fact_historical", RUNNER.historical_fact_ids(self.run))
        self.assertNotIn("fact_historical", RUNNER._read_state_map(self.run, "canonical-facts.json"))

    def test_layout_allocates_ids_before_bounded_record_batches(self):
        records = architecture_genesis_records()
        desired = architecture_core_payload()
        desired["arcs"] = [copy.deepcopy(desired["arcs"][0]) | {"arc_id": f"arc_{i:03d}"} for i in range(1, 5)]
        aliases = {}
        for group, field, prefix in (("obligation_graph", "obligation_id", "obligation"), ("attractors", "attractor_id", "attractor"),
                ("nodes", "node_id", "architecture_node"), ("edges", "edge_id", "architecture_edge")):
            parent = desired["topology"] if group in {"nodes", "edges"} else desired
            aliases.update({value[field]: f"{prefix}_{i:03d}" for i, value in enumerate(parent[group], 1)})
        def remap(value):
            if isinstance(value, dict): return {key: remap(item) for key, item in value.items()}
            if isinstance(value, list): return [remap(item) for item in value]
            return aliases.get(value, value)
        desired = remap(desired)
        counts = {key: len(desired[key]) for key in ("arcs", "attractors", "obligation_graph")}
        counts.update({key: len(desired["topology"][key]) for key in ("nodes", "edges")})
        seen = []
        def transport(_method, _url, request, **kwargs):
            name = request["response_format"]["json_schema"]["name"]
            if name == "architectureLayout": return api_response(counts)
            seen.append(request)
            def resolve(path, _node):
                value = desired
                for part in path: value = value[part]
                return value
            return planning_response(request, resolve)
        with mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: records.get(kind)):
            schema = RUNNER.definition_schema("architectureCorePayload", RUNNER.load_protocol(self.run))
            schema["$defs"]["obligation"].pop("allOf", None)
            state = RUNNER.allocate_core_draft(self.run, schema, transport)
            self.assertEqual(state["payload"]["arcs"][0], {"arc_id": "arc_001"})
            RUNNER.constrain_planning_ids(schema, state["payload"], self.run)
            RUNNER.fill_planning_shape(self.run, "architecture_core", state, schema, transport)
            RUNNER.validate_json_schema(state["payload"], schema)
        self.assertGreater(len(seen), 1)
        for request in seen:
            response_schema = request["response_format"]["json_schema"]["schema"]
            if "value_001" in response_schema.get("properties", {}):
                self.assertLessEqual(len(response_schema["properties"]), 4)
            self.assertNotIn('"assembled_draft"', request["messages"][1]["content"])


if __name__ == "__main__":
    unittest.main()
