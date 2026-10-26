"""Complete initial planning requests retain required inputs under the original guards."""

import copy
import json
import math
import re
import socket
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_cathedrals import ROOT, RUNNER, architecture_core_payload, architecture_genesis_records, packet_plan_annotation
from test_reference_resolution import api_response


def section(context, label):
    body = context.split(f"===== {label} =====\n", 1)[1]
    return re.split(r"(?m)^===== [^\n]+ =====\n", body, maxsplit=1)[0]


class PlanningContextTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RUNNER.read_json(ROOT / "engine/tests/fixtures/initial-planning-context-overflow.json")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        with mock.patch.object(RUNNER, "RUNTIME_ROOT", self.root / ".cathedrals"), mock.patch.object(
            RUNNER, "RUNS_ROOT", self.root / ".cathedrals/runs"
        ):
            self.run = RUNNER.create_run(RUNNER.FrozenInputs(possible_scene_count=self.fixture["possible_scene_count"]),
                "http://offline.invalid", "offline", output_fn=lambda value: None,
                model_context_window_tokens=self.fixture["model_context_window_tokens"])
        self.records = architecture_genesis_records()
        for patch in (
            mock.patch.object(RUNNER, "committed_record", side_effect=lambda run, kind: self.records.get(kind)),
            mock.patch.object(RUNNER, "committed_records", return_value=[]),
            mock.patch.object(RUNNER, "_source_index", return_value={"commit_foundation": {}}),
            mock.patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")),
        ):
            patch.start()
            self.addCleanup(patch.stop)
        payload = architecture_core_payload()
        payload["arcs"] = [copy.deepcopy(payload["arcs"][0]) | {"arc_id": f"arc_{index}"} for index in range(self.fixture["arc_count"])]
        payload["obligation_graph"] += [copy.deepcopy(payload["obligation_graph"][0]) | {"obligation_id": f"debt_{index}"}
                                        for index in range(1, self.fixture["obligation_count"])]
        payload["attractors"] += [copy.deepcopy(payload["attractors"][0]) | {"attractor_id": f"attractor_{index}"}
                                  for index in range(1, self.fixture["attractor_count"])]
        self.core = RUNNER.build_architecture_core(self.run, payload)
        self.pad(self.records["genesis"], self.fixture["genesis_compact_bytes"], 256)
        self.pad(self.core, self.fixture["core_compact_bytes"], 32)
        self.records["architecture_core"] = self.core
        self.batches = RUNNER.plan_batches(self.core)
        self.assignments = RUNNER.ensure_frozen_geomancy(self.run)["assignments"]

    def pad(self, value, size, count):
        value["synthetic_context"] = [{"note": "Synthetic metadata."} for _ in range(count)]
        value["padding"] = ""
        remaining = size - len(RUNNER.canonical_json(value))
        self.assertGreaterEqual(remaining, 0)
        value["padding"] = "x" * remaining
        self.assertEqual(len(RUNNER.canonical_json(value)), size)

    def test_complete_renderer_retains_json_types_unicode_and_authored_whitespace(self):
        values = {"JSON": {"text": "λ — Keep  two spaces.\nKeep this line.", "tail": [1, 2, "last"]},
                  "EMPTY": [], "FALSE": False, "ZERO": 0, "NULL": None}
        plain = "  Frozen law keeps its spaces.\n\nAnd its last line.  "
        context = RUNNER.complete_context([("PLAIN", plain), *values.items()])
        self.assertEqual(section(context, "PLAIN"), plain + "\n\n")
        for label, value in values.items():
            self.assertEqual(json.loads(section(context, label)), value)
        self.assertIn("λ", context)

    def test_large_initial_batch_retains_all_inputs_and_passes_existing_guard(self):
        prompt, context = RUNNER.architecture_plan_prompt(self.run, self.batches[0], 1, len(self.batches))
        self.assertEqual(json.loads(section(context, "IMMUTABLE GENESIS")), self.records["genesis"])
        self.assertEqual(json.loads(section(context, "VALIDATED STAGED ARCHITECTURE CORE")), self.core)
        self.assertEqual(json.loads(section(context, "PRIOR STAGED PACKET IDS")), [])
        assignments = json.loads(section(context, "THIS BATCH THRESHOLD GEOMANCY"))
        self.assertEqual(assignments, self.assignments)
        self.assertEqual(len(assignments), self.fixture["required_geomancy_assignments"])
        self.assertGreater(len(assignments), self.fixture["previously_rendered_geomancy_assignments"])
        allocation = json.loads(prompt.split("THIS BATCH'S EXACT ALLOCATIONS BEGIN\n\n", 1)[1].split("\n\nTHIS BATCH'S EXACT ALLOCATIONS END", 1)[0])
        self.assertEqual(allocation["packet_allocations"], self.batches[0])
        tokens = math.ceil(len(prompt.encode()) / 3)
        self.assertLess(tokens, self.fixture["max_prepared_context_tokens"])
        schema = RUNNER.architecture_plan_batch_schema(self.run, self.batches[0])
        payload = {"packet_plans": [packet_plan_annotation(spec["packet_slot_id"]) for spec in self.batches[0]]}
        transport = mock.Mock(return_value=api_response(payload))
        state = RUNNER.staged_planning_request(self.run, "architecture_plan_batch_0001", prompt, context, schema, transport)
        self.assertFalse(state["bulk_failed"])
        transport.assert_called_once()
        request = transport.call_args.args[2]
        self.assertEqual(request["messages"][1]["content"], prompt)
        self.assertEqual(request["max_tokens"], self.fixture["requested_output_tokens"])
        self.assertLessEqual(tokens + request["max_tokens"] + self.fixture["context_safety_reserve_tokens"], self.fixture["model_context_window_tokens"])
        self.assertEqual(RUNNER.read_json(self.run / "run-manifest.json")["budgets"]["max_prepared_context_tokens"], 49152)

    def test_initial_core_retains_law_manifest_and_complete_reference_catalogs(self):
        law = "Frozen law.\n\n  Keep  deliberate whitespace and λ.\nFinal required rule."
        with mock.patch.object(RUNNER, "engine_context", return_value=law):
            prompt, context = RUNNER.architecture_core_prompt(self.run)
        self.assertIn(law, context)
        self.assertEqual(json.loads(section(context, "FROZEN RUN MANIFEST")), RUNNER.read_json(self.run / "run-manifest.json"))
        self.assertEqual(json.loads(section(context, "IMMUTABLE GENESIS")), self.records["genesis"])
        catalog = RUNNER.genesis_reference_catalog(self.run)
        self.assertEqual(json.loads(section(context, "ALLOWED GENESIS CLAIMANTS")), [catalog["claimant_01"]])
        self.assertEqual(json.loads(section(context, "ALLOWED COMMITTED SOURCES")), [catalog["commit_foundation"]])
        self.assertIn("Final required rule.", prompt)

    def test_prior_packet_ids_are_preserved_in_order(self):
        prior = ["packet_first", "packet_last"]
        with mock.patch.object(RUNNER, "planning_batches_view", return_value=[
            {"batch_sequence": 1, "packet_plans": [{"packet_slot_id": key} for key in prior]},
            {"batch_sequence": 3, "packet_plans": [{"packet_slot_id": "future_packet"}]},
        ]):
            _, context = RUNNER.architecture_plan_prompt(self.run, self.batches[0], 2, 3)
        self.assertEqual(json.loads(section(context, "PRIOR STAGED PACKET IDS")), prior)

    def test_oversized_core_keeps_last_required_catalog_entry_and_pauses_before_post(self):
        catalog = RUNNER.genesis_reference_catalog(self.run)
        catalog["last_source"] = "λ" * 100000 + " LAST REQUIRED SOURCE"
        with mock.patch.object(RUNNER, "genesis_reference_catalog", return_value=catalog), mock.patch.object(
            RUNNER, "_source_index", return_value={"commit_foundation": {}, "last_source": {}}
        ):
            prompt, context = RUNNER.architecture_core_prompt(self.run)
        self.assertEqual(json.loads(section(context, "ALLOWED COMMITTED SOURCES"))[-1], catalog["last_source"])
        transport = mock.Mock(side_effect=AssertionError("oversized request posted"))
        with self.assertRaises(RUNNER.PausedError):
            RUNNER.staged_planning_request(self.run, "architecture_core", prompt, context,
                RUNNER.definition_schema("architectureCorePayload"), transport)
        transport.assert_not_called()
        self.assertFalse((self.run / "finalization.json").exists())

    def test_oversized_batch_does_not_omit_core_or_change_accepted_checkpoint(self):
        self.core["padding"] += "λ" * 100000
        checkpoint = self.run / ".staging/architecture_core.planning.json"
        RUNNER.write_json(checkpoint, {"record": self.core, "ready": True})
        original = checkpoint.read_bytes()
        prompt, context = RUNNER.architecture_plan_prompt(self.run, self.batches[0], 1, len(self.batches))
        self.assertEqual(json.loads(section(context, "VALIDATED STAGED ARCHITECTURE CORE")), self.core)
        self.assertEqual(json.loads(section(context, "THIS BATCH THRESHOLD GEOMANCY")), self.assignments)
        transport = mock.Mock(side_effect=AssertionError("oversized request posted"))
        with self.assertRaises(RUNNER.PausedError) as raised:
            RUNNER.staged_planning_request(self.run, "architecture_plan_batch_0001", prompt, context,
                RUNNER.architecture_plan_batch_schema(self.run, self.batches[0]), transport)
        self.assertEqual(raised.exception.failure_class, "budget_exhaustion")
        self.assertIn(str(math.ceil(len(prompt.encode()) / 3)), raised.exception.reason.replace(",", ""))
        transport.assert_not_called()
        self.assertEqual(checkpoint.read_bytes(), original)
        self.assertFalse((self.run / "finalization.json").exists())


if __name__ == "__main__":
    unittest.main()
