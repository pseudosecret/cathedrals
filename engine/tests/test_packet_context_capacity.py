"""Packet capacity regressions using synthetic sizes from the saved first-packet pause."""

import contextlib
import copy
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_cathedrals import RUNNER, packet_plan
from test_fts5_retrieval import decode_context


def source_record(index, size):
    record = {"commit_id": f"commit_fixture_{index}", "record_type": (
        "genesis_foundation", "genesis_cast", "genesis_constraints")[index], "payload": ""}
    record["payload"] = "x" * (size - len(RUNNER.compact_context_value(record)))
    return {"source_id": record["commit_id"], "source_commit_id": record["commit_id"],
        "source_hash": RUNNER.sha256_bytes(RUNNER.canonical_json(record)), "record_pointer": "",
        "authority": "GENERATED ROOT CANON", "immutable_source": record}


class PacketContextCapacityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        with mock.patch.object(RUNNER, "RUNTIME_ROOT", self.root), mock.patch.object(RUNNER, "RUNS_ROOT", self.root / "runs"):
            self.run = RUNNER.create_run(RUNNER.FrozenInputs(possible_scene_count=25), "http://offline.invalid", "offline",
                output_fn=lambda _: None, model_context_window_tokens=102656)
        self.sources = [source_record(index, size) for index, size in enumerate((10053, 22707, 14742))]

    def required(self):
        law, _ = RUNNER.instruction_profile(self.run)
        citations = [copy.deepcopy(self.sources[index]) | {"source_id": f"cited_entity_{number}", "source_locator": f"Synthetic locator {number}"}
            for number, index in enumerate((0, 2, 2, 1, 2, 2, 1, 1))]
        return [("FROZEN ENGINE LAW", law), ("FROZEN GENERATION BRIEF", {"genre_flavor": "synthetic"}),
            ("IMMUTABLE GENERATED ROOT CANON", self.sources),
            ("CURRENT PACKET STRUCTURAL POSITION", {"assignment": "x" * 3630}),
            ("ACTIVE HARD FUTURE OBLIGATIONS", [{"required": "x" * 6741}]),
            ("OBLIGATIONS THIS PACKET MAY SATISFY", [{"required": "x" * 9426}]),
            ("IMMUTABLE PAST CONSTRAINTS", [{"required": "x" * 2432}]),
            ("CHARACTER KNOWLEDGE / BELIEF CONSTRAINTS", [{"required": "x" * 1866}]),
            ("ENDING / BRANCH ATTRACTORS EXERTING PRESSURE", [{"required": "x" * 966}]),
            ("FROZEN THRESHOLD GEOMANCY", [{"required": "x" * 398}]),
            ("REQUIRED PREREQUISITE SOURCE EVIDENCE", citations)]

    def test_saved_sizes_fit_writing_and_normalization_with_complete_source_roles(self):
        plan = RUNNER.single_content_packet_plans(packet_plan(advance_obligation_ids=[], may_satisfy_obligation_ids=[]))[0]
        architecture = {"architecture_core_commit_id": "fixture_core", "arcs": [{"arc_id": "arc_fixture"}]}
        receipt = {"omissions": []}
        required = self.required()

        def assemble(_run, _architecture, _plan, **kwargs):
            self.assertLess(kwargs["prompt_overhead_tokens"], 14000)
            return RUNNER.pack_packet_context(required, [], RUNNER.packet_input_limit(self.run) - kwargs["prompt_overhead_tokens"], receipt)

        with mock.patch.object(RUNNER, "plan_batch_for", return_value={"commit_id": "fixture_batch"}), mock.patch.object(
            RUNNER, "relevant_packet_context", side_effect=assemble
        ), mock.patch.object(RUNNER, "committed_record", return_value=architecture
        ):
            prompt, context = RUNNER.packet_prompt(self.run, architecture, plan)
        self.assertLessEqual(RUNNER.estimated_prompt_tokens(RUNNER.RECORD_SYSTEM_PROMPT + prompt), 49152)
        decoded = decode_context(context)
        self.assertEqual(decoded["IMMUTABLE GENERATED ROOT CANON"], self.sources)
        self.assertEqual(decoded["REQUIRED PREREQUISITE SOURCE EVIDENCE"], required[-1][1])
        for source in self.sources:
            self.assertEqual(context.count(RUNNER.compact_context_value(source["immutable_source"])), 1)
        self.assertEqual(receipt["shared_source_count"], 3)
        self.assertEqual(receipt["source_reference_count"], 11)
        self.assertGreater(receipt["source_payload_bytes_saved"], 130000)
        self.assertIn("SHARED SOURCE RECORDS", receipt["required_components"])
        artistic = {"scenes": [{"technical_slot_id": plan["scene_slot_ids"][0], "prose_mdx": "placeholder " * 1200}], "endings": []}
        for accepted in (None, {"canonical_facts": [{"value": "Synthetic accepted metadata."}] * 8}):
            semantic = RUNNER.semantic_prompt(artistic, context, "Return the semantic delta.", accepted, run_dir=self.run)
            self.assertLessEqual(RUNNER.estimated_prompt_tokens(semantic), 49152)
            RUNNER.semantic_output_limit(self.run, semantic, {"type": "object"})
            for source in self.sources:
                self.assertEqual(semantic.count(RUNNER.compact_context_value(source["immutable_source"])), 1)
        normalized = decode_context(RUNNER.compact_semantic_context(context, self.run))
        for label in decoded.keys() - {"FROZEN ENGINE LAW"}:
            if not label.startswith("engine/"):
                self.assertEqual(normalized[label], decoded[label])

    def test_profiles_keep_binding_sections_and_derive_from_frozen_inputs(self):
        packet, provenance = RUNNER.instruction_profile(self.run)
        semantic, semantic_provenance = RUNNER.instruction_profile(self.run, "semantic")
        self.assertNotIn("milestone_control:", packet)
        self.assertNotIn("execution_phase:", packet)
        self.assertNotIn("generation_budget:", packet)
        self.assertNotIn("## 1. Frozen Request and Preflight", packet)
        for section in RUNNER.PACKET_WORK_SECTIONS:
            self.assertIn(section + ":", packet)
        for heading in RUNNER.PACKET_WORKFLOW_SECTIONS:
            self.assertIn("## " + heading, packet)
        self.assertNotIn("canon/style-rules.md", semantic)
        self.assertIn("canon/ontology.md", semantic)
        for section in RUNNER.SEMANTIC_WORK_SECTIONS:
            self.assertIn(section + ":", semantic)
        self.assertEqual(provenance["hash"], RUNNER.sha256_bytes(packet.encode()))
        self.assertEqual(semantic_provenance["hash"], RUNNER.sha256_bytes(semantic.encode()))
        path = RUNNER.engine_root(self.run) / "data/work-instance.yaml"
        self.assertEqual(provenance["sources"]["data/work-instance.yaml"]["hash"], RUNNER.sha256_file(path))
        path.chmod(0o644)
        path.write_text(path.read_text().replace("authorship_boundary:", "missing_section:"))
        with self.assertRaises(RUNNER.IntegrityError):
            RUNNER.instruction_profile(self.run)

    def test_shared_identity_conflicts_fail_and_pointers_do_not_alias(self):
        original = self.sources[0]
        conflict = copy.deepcopy(original)
        conflict["immutable_source"]["payload"] = "Changed source."
        with self.assertRaises(RUNNER.IntegrityError):
            RUNNER.pack_packet_context([("SOURCE", [original, conflict])], [], 49152, {"omissions": []})
        other = conflict | {"record_pointer": "/different_unit"}
        receipt = {"omissions": []}
        context = RUNNER.pack_packet_context([("SOURCE", [original, other])], [], 49152, receipt)
        self.assertEqual(decode_context(context)["SOURCE"], [original, other])
        self.assertEqual(receipt["shared_source_count"], 2)

    def test_original_root_loader_verifies_each_archive_and_requires_three_records(self):
        db = sqlite3.connect(":memory:")
        self.addCleanup(db.close)
        db.execute("CREATE TABLE records(commit_id,record_type,sequence,path,record_hash)")
        for index, source in enumerate(self.sources):
            directory = self.run / "committed" / str(index)
            path = directory / "record.json"
            RUNNER.write_json(path, source["immutable_source"])
            db.execute("INSERT INTO records VALUES (?,?,?,?,?)", (source["source_commit_id"], source["immutable_source"]["record_type"],
                index, str(directory.relative_to(self.run)), RUNNER.sha256_file(path)))
        with mock.patch.object(RUNNER, "index_connection", side_effect=lambda _run: contextlib.nullcontext(db)):
            loaded = RUNNER.packet_root_sources(self.run)
            self.assertEqual([item["immutable_source"] for item in loaded], [item["immutable_source"] for item in self.sources])
            changed = self.run / "committed/1/record.json"
            changed.write_text("changed")
            with self.assertRaises(RUNNER.IntegrityError):
                RUNNER.packet_root_sources(self.run)
            db.execute("DELETE FROM records WHERE sequence=1")
            with self.assertRaises(RUNNER.IntegrityError):
                RUNNER.packet_root_sources(self.run)

    def test_unicode_capacity_uses_bytes_and_optional_overflow_preserves_required_content(self):
        receipt = {"omissions": []}
        text = RUNNER.pack_packet_context([("REQUIRED", [{"value": "雪" * 40}])], [("OPTIONAL", [{"value": "x" * 1000}])], 100, receipt)
        self.assertEqual(decode_context(text)["REQUIRED"], [{"value": "雪" * 40}])
        self.assertEqual(receipt["estimated_context_tokens"], RUNNER.estimated_prompt_tokens(text))
        self.assertTrue(receipt["omissions"])
        with self.assertRaises(RUNNER.PausedError):
            RUNNER.pack_packet_context([("REQUIRED", ["雪" * 100])], [], 100, {"omissions": []})

    def test_output_safety_and_feedback_are_checked_before_dispatch(self):
        manifest = RUNNER.read_json(self.run / "run-manifest.json")
        manifest["budgets"]["max_prepared_context_tokens"] = 300
        RUNNER.write_json(self.run / "run-manifest.json", manifest)
        provider = mock.Mock(return_value={"choices": [{"finish_reason": "stop", "message": {
            "content": json.dumps({"name": 42, "incident_role": "x" * 1500})}}]})
        with self.assertRaisesRegex(RUNNER.PausedError, "No request was sent"):
            RUNNER.request_record(self.run, expected_record_type="genesis_foundation", step_id="feedback_capacity", phase="genesis",
                prompt="prompt", context="context", branch_relation="root", temperature=0.8,
                response_definition="claimantAnchorPayload", transport=provider)
        self.assertEqual(provider.call_count, 1)
        self.assertEqual(len(RUNNER.step_entries(self.run, "feedback_capacity")), 1)
        self.assertTrue((self.run / "raw/feedback_capacity-attempt1.api.json").exists())
        state = RUNNER.load_state(self.run)
        state["model_context_window_tokens"] = 12000
        RUNNER.save_state(self.run, state)
        with self.assertRaises(RUNNER.PausedError):
            RUNNER.request_record(self.run, expected_record_type="genesis_foundation", step_id="no_capacity", phase="genesis",
                prompt="prompt", context="context", branch_relation="root", temperature=0.8, transport=provider)
        self.assertEqual(provider.call_count, 1)


class SelectedModelCapacityTests(unittest.TestCase):
    def model(self, key, instances):
        return {"type": "llm", "key": key, "max_context_length": 262144,
            "loaded_instances": [{"id": name, "config": {"context_length": limit}} for name, limit in instances]}

    def capacity(self, selected, models):
        transport = mock.Mock(return_value={"models": models})
        return RUNNER.preflight_model_capacity("http://offline.invalid", selected, lambda _: None, transport)

    def test_unloaded_selected_model_never_borrows_another_loaded_models_capacity(self):
        with self.assertRaisesRegex(RUNNER.PausedError, "not loaded"):
            self.capacity("bonsai", [self.model("qwen", [("qwen", 80384)]), self.model("bonsai", [])])

    def test_loaded_limit_is_required_and_theoretical_maximum_is_not_a_fallback(self):
        for limit in (8192, None, True, "80384"):
            with self.subTest(limit=limit), self.assertRaises(RUNNER.PausedError):
                self.capacity("bonsai", [self.model("bonsai", [("bonsai", limit)])])

    def test_ambiguous_keys_require_exact_instance_and_other_instances_cannot_raise_its_limit(self):
        models = [self.model("bonsai", [("small", 8192), ("large", 80384)])]
        with self.assertRaisesRegex(RUNNER.PausedError, "multiple"):
            self.capacity("bonsai", models)
        with self.assertRaisesRegex(RUNNER.PausedError, "8,192"):
            self.capacity("small", models)
        self.assertEqual(self.capacity("large", models), 80384)
        self.assertEqual(self.capacity("bonsai", [self.model("bonsai", [("bonsai", 102656)])]), 102656)


if __name__ == "__main__":
    unittest.main()
