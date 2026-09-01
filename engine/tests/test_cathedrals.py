#!/usr/bin/env python3
"""Offline checks for the end-user executable; no creative call is made."""

import dataclasses
import importlib.machinery
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from subprocess import CompletedProcess
from unittest import mock


ROOT = Path(__file__).parents[2]
LOADER = importlib.machinery.SourceFileLoader("cathedrals_runner", str(ROOT / "cathedrals"))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
RUNNER = importlib.util.module_from_spec(SPEC)
sys.modules[LOADER.name] = RUNNER
LOADER.exec_module(RUNNER)


def answers(*values):
    values = iter(values)
    return lambda _prompt="": next(values)


class CathedralsRunnerTests(unittest.TestCase):
    def test_four_inputs_and_defaults(self):
        output = []
        brief = RUNNER.collect_inputs(answers("", "", "", "web"), output.append)
        self.assertEqual(brief.project_name, "Cathedrals")
        self.assertEqual(brief.genre_flavor, "existential mystery")
        self.assertEqual(brief.possible_scene_count, 150)
        self.assertEqual(brief.story_format, "web")
        self.assertFalse(brief.mutable)

    def test_scene_count_rejects_nonpositive_and_noninteger(self):
        for value in ("0", "-1", "3.5", "many"):
            with self.assertRaises(ValueError):
                RUNNER.parse_scene_count(value)
        self.assertEqual(RUNNER.parse_scene_count("151"), 151)

    def test_format_aliases_are_accepted_but_effective_output_is_web(self):
        for alias in ("visualnovel", "visual novel", "visual-novel", "vn"):
            self.assertEqual(RUNNER.normalize_requested_format(alias), "visualnovel")
            self.assertEqual(RUNNER.renderer_for(alias), "astro")
            self.assertEqual(RUNNER.active_format_contract(alias).name, "web.md")
        with self.assertRaises(ValueError):
            RUNNER.normalize_requested_format("")

    def test_generation_inputs_are_frozen(self):
        brief = RUNNER.FrozenInputs()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            brief.genre_flavor = "changed"

    def test_lm_studio_url_default_and_override(self):
        self.assertEqual(RUNNER.configured_lm_studio_url({"UNRELATED": "1"}), "http://127.0.0.1:1234")
        self.assertEqual(
            RUNNER.configured_lm_studio_url({"CATHEDRALS_LM_STUDIO_URL": "http://127.0.0.1:5555/"}),
            "http://127.0.0.1:5555",
        )

    def test_unreachable_lm_studio_fails_in_preflight(self):
        def unreachable(*_args, **_kwargs):
            raise RUNNER.CathedralsError("test", "offline", "transport_before_response")

        with self.assertRaisesRegex(RUNNER.CathedralsError, "Open LM Studio on Windows"):
            RUNNER.lm_studio_preflight("http://127.0.0.1:1234", transport=unreachable)

    def test_model_discovery_and_selection(self):
        payload = {"data": [{"id": "writer"}, {"id": "embedder", "type": "embedding"}]}
        self.assertEqual(RUNNER.usable_model_ids(payload), ["writer"])
        self.assertEqual(RUNNER.choose_model(["writer"]), "writer")
        self.assertEqual(RUNNER.choose_model(["a", "b"], input_fn=answers("2"), output_fn=lambda _line: None), "b")
        with self.assertRaises(RUNNER.CathedralsError):
            RUNNER.choose_model(["writer"], override="missing")

    def test_scope_is_dynamic_not_clamped_to_profiles(self):
        scope = RUNNER.derive_scope(150)["scope"]
        self.assertEqual(scope["possible_scene_count"], 150)
        self.assertEqual(scope["profile_guidance"], "cathedral")
        self.assertGreater(scope["literary_packet_target"], 16)

    def test_toolchain_state_is_ignored_and_renpy_is_deferred(self):
        self.assertIn(".cathedrals/", (ROOT / ".gitignore").read_text().splitlines())
        self.assertEqual(RUNNER.renderer_for("visualnovel"), "astro")
        self.assertFalse((RUNNER.RUNTIME_ROOT / "toolchains/renpy").exists())

    def test_web_bootstrap_reuses_compatible_system_node(self):
        def located(name):
            return f"/usr/bin/{name}" if name in {"node", "npm"} else None

        with mock.patch.object(RUNNER.shutil, "which", side_effect=located), mock.patch.object(
            RUNNER, "run_command", return_value=CompletedProcess([], 0, "v22.12.0\n", "")
        ):
            node, npm = RUNNER.ensure_node(output_fn=lambda _line: None)
        self.assertEqual(node, Path("/usr/bin/node"))
        self.assertEqual(npm, Path("/usr/bin/npm"))

    def test_web_projection_creates_static_route_families_without_changing_source(self):
        scene = {
            "technical_slot_id": "scene_slot_0001",
            "scene_id": "scene_fixture",
            "title": "Fixture",
            "prose_mdx": "fixture prose bytes",
            "artifact_ids": ["artifact_fixture"],
            "choice_edge_ids": ["edge_fixture"],
            "state_effects": [],
        }
        artifact = {"artifact_id": "artifact_fixture", "title": "Evidence", "body_mdx": "fixture evidence bytes"}
        ending = {"ending_id": "ending_fixture", "title": "End", "prose_mdx": "fixture ending bytes", "state_effects": []}
        edge = {"edge_id": "edge_fixture", "from_content_id": "scene_fixture", "to_content_id": "ending_fixture"}
        packet = {"record_type": "creative_packet", "scenes": [scene], "artifacts": [artifact], "endings": [ending], "decision_edges": [edge]}
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "generation_fixture"
            run.mkdir()
            RUNNER.write_json(run / "run-manifest.json", {"generation_brief": {"project_name": "Fixture"}})
            with mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: {"work_canon": {"generated_title": "Fixture Work"}} if kind == "genesis" else {"topology": {}}), mock.patch.object(
                RUNNER, "all_committed_records", return_value=[packet]
            ), mock.patch.object(RUNNER, "append_deterministic_step"):
                project, counts = RUNNER.project_web(run)
            self.assertEqual(counts, {"scenes": 1, "artifacts": 1, "endings": 1})
            self.assertEqual((project / "public/source/scene_fixture.md").read_text(), "fixture prose bytes")
            for route in ("scenes/[sceneId].astro", "artifacts/[artifactId].astro", "endings/[endingId].astro"):
                self.assertTrue((project / "src/pages" / route).exists())

    def test_append_helpers_refuse_rewrite_and_preserve_ledger_prefix(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            (run / "state").mkdir()
            RUNNER.save_state(run, RUNNER.initial_run_state("generation_test", "generation/test", "a" * 64, "b" * 64, "model"))
            RUNNER.append_deterministic_step(run, "preflight", "preflight", "c" * 64)
            first = (run / "ledger.jsonl").read_bytes()
            RUNNER.append_deterministic_step(run, "preflight", "preflight", "d" * 64)
            self.assertEqual((run / "ledger.jsonl").read_bytes(), first)
            immutable = run / "committed.json"
            RUNNER.write_json(immutable, {"value": 1}, exclusive=True)
            with self.assertRaises(RUNNER.IntegrityError):
                RUNNER.write_json(immutable, {"value": 2}, exclusive=True)

    def test_terminal_schema_has_no_partial_play_state(self):
        protocol = RUNNER.load_protocol()
        statuses = protocol["$defs"]["finalization"]["properties"]["run_status"]["enum"]
        self.assertEqual(set(statuses), {"READY_TO_PLAY", "FAILED_GENERATION"})
        barrier = protocol["$defs"]["runManifest"]["properties"]["complete_work_barrier"]["properties"]
        self.assertEqual(barrier["partial_play_allowed"]["const"], False)
        self.assertEqual(barrier["runtime_generation_allowed"]["const"], False)
        invalid_ready = {
            "record_type": "finalization",
            "protocol_version": "2.0",
            "generation_id": "generation_test",
            "run_status": "READY_TO_PLAY",
            "run_manifest_hash": "a" * 64,
            "generation_brief_hash": "b" * 64,
            "completed_at": "2026-01-01T00:00:00Z",
            "creative_step_count": 0,
            "analysis_or_index_step_count": 0,
            "human_intervention_count": 0,
            "committed_rewrite_count": 0,
            "committed_regeneration_count": 0,
            "backtrack_count": 0,
            "ledger_head_hash": "c" * 64,
            "committed_record_hashes": {"run_manifest": "d" * 64},
            "memory_event_stream_hash": "e" * 64,
            "token_accounting": {"input_tokens": 0, "output_tokens": 0, "cost": None, "currency": None},
            "mechanical_validation": {"result": "NOT_RUN", "reasons": ["partial"]},
            "artistic_acceptance": {"result": "NOT_RUN", "reasons": ["partial"]},
            "static_build_validation": {"result": "NOT_RUN", "reasons": ["partial"]},
            "complete_work_barrier_satisfied": False,
            "playable": False,
            "failure_class": "none",
        }
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_json_schema(invalid_ready, protocol["$defs"]["finalization"], protocol)


if __name__ == "__main__":
    unittest.main()
