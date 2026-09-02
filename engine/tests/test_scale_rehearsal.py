#!/usr/bin/env python3
"""Cathedral-scale deterministic rehearsal; never contacts a model or authors fiction."""

import copy
import importlib.machinery
import importlib.util
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).parents[2]
LOADER = importlib.machinery.SourceFileLoader("cathedrals_scale_runner", str(ROOT / "cathedrals"))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
RUNNER = importlib.util.module_from_spec(SPEC)
sys.modules[LOADER.name] = RUNNER
LOADER.exec_module(RUNNER)

SCENE_COUNT = 150
PACKET_COUNT = 50
ARTIFACT_COUNT = 30
ENDING_COUNT = 6


def attractor_id(number):
    return "attractor_branch_04" if number == 4 else f"attractor_ending_{number:02d}"


def art_direction():
    return {
        "visual_thesis": "Synthetic presentation fixture; no narrative facts.",
        "typography": {
            "body_family_class": "archival_serif",
            "heading_family_class": "severe_sans",
            "scale": "balanced",
            "tracking": "narrow",
        },
        "palette": {
            "background": "#101820",
            "surface": "#18232d",
            "text": "#f4f1e8",
            "muted": "#c7c2b5",
            "accent": "#d9b66f",
            "danger": "#ef8d8d",
        },
        "spatial_density": "balanced",
        "border_language": "institutional",
        "surface_language": "archival",
        "artifact_treatment": "ledger",
        "scene_transition_treatment": "segmented",
        "ending_treatment": "ceremonial",
        "route_pressure": "moderate",
    }


def scale_web_fixture():
    scene_ids = {number: f"synthetic_content_{number:04d}_z" for number in range(1, SCENE_COUNT + 1)}
    ending_ids = {number: f"synthetic_terminal_{number:02d}_q" for number in range(1, ENDING_COUNT + 1)}
    outgoing = {number: [] for number in scene_ids}
    edges = []

    def add_edge(source, destination, suffix):
        edge = {
            "edge_id": f"edge_{source:04d}_{suffix}",
            "from_content_id": scene_ids[source],
            "destination": {"kind": "technical_slot", "id": destination},
            "label": f"Synthetic route {source:04d}-{suffix}",
            "kind": "progression",
            "availability": "playable",
            "decision_group_id": None,
            "major_decision": False,
            "state_conditions": [],
            "state_effects": [{"operation": "increment", "key": "indecision_count", "value": 1}],
        }
        outgoing[source].append(edge)
        edges.append(edge)

    for number in range(1, SCENE_COUNT):
        add_edge(number, f"scene_slot_{number + 1:04d}", "next")
    add_edge(SCENE_COUNT, "ending_slot_0001", "ending")
    add_edge(4, "scene_slot_0008", "branch_a")
    add_edge(4, "scene_slot_0012", "branch_b")
    for number in range(15, 136, 15):
        add_edge(number, f"scene_slot_{number + 7:04d}", "cross")
    for offset, number in enumerate(range(145, 150), 2):
        add_edge(number, f"ending_slot_{offset:04d}", f"ending_{offset:02d}")
    for number, group in outgoing.items():
        if len(group) > 1:
            for edge in group:
                edge["kind"] = "decision"
                edge["decision_group_id"] = f"decision_group_{number:04d}"

    artifacts = {
        number: {
            "artifact_id": f"synthetic_artifact_{number:03d}",
            "title": f"Synthetic Artifact {number:03d}",
            "body_mdx": "## Synthetic artifact\n\n- metadata\n- fixture",
        }
        for number in range(1, ARTIFACT_COUNT + 1)
    }
    scenes = []
    for number in range(1, SCENE_COUNT + 1):
        artifact_number = number // 5 if number % 5 == 0 and number <= ARTIFACT_COUNT * 5 else None
        markdown = (
            "# Synthetic heading\n\nSynthetic *emphasis* and **strong text**.\n\n"
            "> Synthetic quotation.\n\n- one\n- two"
            if number == 1 else f"Synthetic placeholder for scene slot {number:04d}."
        )
        scenes.append({
            "technical_slot_id": f"scene_slot_{number:04d}",
            "scene_id": scene_ids[number],
            "title": f"Synthetic Scene {number:04d}",
            "prose_mdx": markdown,
            "artifact_ids": [artifacts[artifact_number]["artifact_id"]] if artifact_number else [],
            "choice_edge_ids": [edge["edge_id"] for edge in outgoing[number]],
            "state_effects": [{"operation": "increment", "key": "contamination", "value": 1}],
        })
    endings = [
        {
            "technical_slot_id": f"ending_slot_{number:04d}",
            "ending_id": ending_ids[number],
            "title": f"Synthetic Ending {number:02d}",
            "prose_mdx": f"Synthetic ending placeholder {number:02d}.",
            "state_effects": [],
            "redirect_destination": (
                {"kind": "technical_slot", "id": "scene_slot_0130"} if number == ENDING_COUNT else None
            ),
        }
        for number in range(1, ENDING_COUNT + 1)
    ]
    packets = []
    for packet_number in range(1, PACKET_COUNT + 1):
        packet_scenes = scenes[(packet_number - 1) * 3:packet_number * 3]
        scene_names = {scene["scene_id"] for scene in packet_scenes}
        packet_artifacts = [artifact for artifact in artifacts.values() if any(artifact["artifact_id"] in scene["artifact_ids"] for scene in packet_scenes)]
        packets.append({
            "record_type": "creative_packet",
            "commit_id": f"commit_packet_{packet_number:03d}",
            "packet_slot_id": f"packet_slot_{packet_number:03d}",
            "scenes": packet_scenes,
            "artifacts": packet_artifacts,
            "endings": [],
            "decision_edges": [edge for edge in edges if edge["from_content_id"] in scene_names],
            "formal_compositions": [],
            "constraint_delta": {},
        })
    packets.append({
        "record_type": "creative_packet",
        "commit_id": "commit_endings",
        "packet_slot_id": "packet_slot_endings",
        "scenes": [],
        "artifacts": [],
        "endings": endings,
        "decision_edges": [],
        "formal_compositions": [],
        "constraint_delta": {},
    })
    return {
        "manifest": {"generation_brief": {"project_name": "Synthetic Scale", "possible_scene_count": SCENE_COUNT}},
        "genesis": {"work_canon": {"generated_title": "Synthetic Scale Fixture"}, "web_art_direction": art_direction()},
        "architecture": {"fixture_kind": "nonliterary_scale_metadata", "scene_slots": SCENE_COUNT},
        "packets": packets,
        "scenes": scenes,
        "endings": endings,
        "edges": edges,
    }


def source(scene_number):
    return {
        "artifact_type": "scene",
        "artifact_id": f"synthetic_content_{scene_number:04d}_z",
        "source_locator": "prose_mdx#synthetic",
        "source_commit_id": f"commit_packet_{(scene_number - 1) // 3 + 1:03d}",
        "source_hash": f"{scene_number:064x}"[-64:],
    }


def obligation(number, *, hardness=None, universality=None, target=None):
    hardness = hardness or ("hard" if number <= 30 else "soft")
    universality = universality or ("universal" if number == 1 else "attractor_scoped" if hardness == "hard" else "local")
    target = target or (attractor_id(min(4, (number - 1) // 8 + 1)) if hardness == "hard" else f"packet_slot_{min(PACKET_COUNT, number):03d}")
    return {
        "obligation_id": f"obligation_{number:03d}",
        "kind": "ending_prerequisite" if hardness == "hard" else "thematic_pressure",
        "description": f"Synthetic obligation {number:03d}",
        "status": "active",
        "created_by_ids": [target],
        "requires": [f"obligation_{number - 1:03d}"] if 1 < number <= 8 else [],
        "hardness": hardness,
        "universality": universality,
        "resolution_modes": ["transformation"],
        "range": "long_range" if hardness == "hard" else "local",
        "termination_targets": [target],
        "relevance": {"branch_ids": ["branch_crucial" if number == 12 else f"branch_{number % 6:02d}"], "keywords": ["synthetic"]},
    }


def scale_constraint_fixture():
    obligations = [obligation(number) for number in range(1, 121)]
    attractors = []
    ending_slot_groups = ((1, 2), (3, 4), (5, 6), ())
    for number in range(1, 5):
        attractors.append({
            "attractor_id": attractor_id(number),
            "kind": "ending" if number <= 3 else "branch",
            "terminal_transformation": f"Synthetic transformation {number:02d}",
            "thematic_function": "Exercise backward prerequisites.",
            "emotional_register": "synthetic",
            "foreclosable": number != 1,
            "prerequisite_obligation_ids": [f"obligation_{(number - 1) * 8 + 1:03d}"],
            "soft_seed_conditions": ["synthetic condition"],
            "unresolved_realization": ["synthetic realization"],
            "ending_slot_ids": [f"ending_slot_{slot:04d}" for slot in ending_slot_groups[number - 1]],
            "relevance": {"branch_ids": [f"branch_{number:02d}"]},
        })
    plans = []
    for number in range(1, PACKET_COUNT + 1):
        start = (number - 1) * 3 + 1
        plans.append({
            "packet_slot_id": f"packet_slot_{number:03d}",
            "packet_kind": "literary",
            "initial_priority": number,
            "scene_slot_ids": [f"scene_slot_{item:04d}" for item in range(start, start + 3)],
            "ending_slot_ids": [],
            "artifact_count": 1 if number <= ARTIFACT_COUNT else 0,
            "formal_composition_count": 2 if number == 1 else 0,
            "depends_on_packet_slot_ids": [f"packet_slot_{number - 1:03d}"] if number > 1 else [],
            "branch_path_relation": f"branch_{number % 6:02d}",
            "attractor_ids": [attractor_id(number % 4 + 1)],
            "relevance": {
                "branch_ids": ["branch_crucial" if number >= 44 else f"branch_{number % 6:02d}"],
                "character_ids": [f"character_{number % 5 + 1:02d}"],
                "location_ids": ["location_old_evidence" if number >= 44 else f"location_{number % 8:02d}"],
                "keywords": ["crucial", "archive"] if number >= 44 else ["synthetic"],
            },
            "soft_guidance": ["Retrieve crucial archive evidence." if number >= 44 else "Synthetic packet pressure."],
        })
    all_literary = [plan["packet_slot_id"] for plan in plans]
    for number, attractor in enumerate(attractors, 1):
        if attractor["kind"] != "ending":
            continue
        plans.append({
            "packet_slot_id": f"packet_slot_ending_{number:02d}",
            "packet_kind": "ending",
            "initial_priority": PACKET_COUNT + number,
            "scene_slot_ids": [],
            "ending_slot_ids": attractor["ending_slot_ids"],
            "artifact_count": 0,
            "formal_composition_count": 0,
            "depends_on_packet_slot_ids": all_literary,
            "branch_path_relation": f"ending_{number:02d}",
            "attractor_ids": [attractor["attractor_id"]],
            "relevance": {"branch_ids": [f"branch_{number:02d}"], "keywords": ["synthetic"]},
            "soft_guidance": ["Synthetic terminal pressure."],
        })
    architecture = {"commit_id": "commit_architecture", "obligation_graph": obligations, "attractors": attractors, "packet_plans": plans}
    events = []

    def event(kind, constraint_class, identifier, data, scene_number):
        events.append({
            "record_type": "constraint_event",
            "protocol_version": "3.0",
            "generation_id": "synthetic_scale",
            "constraint_event_sequence": len(events) + 1,
            "origin_step_id": f"packet_slot_{max(1, (scene_number - 1) // 3 + 1):03d}",
            "constraint_id": identifier,
            "constraint_class": constraint_class,
            "constraint_kind": kind,
            "action": "establish",
            "data": data,
            "sources": [source(scene_number)],
        })

    for number in range(1, SCENE_COUNT + 1):
        relevance = {
            "branch_ids": ["branch_crucial" if number == 12 else f"branch_recent_{number % 7:02d}"],
            "location_ids": ["location_old_evidence" if number == 12 else f"location_{number % 8:02d}"],
            "keywords": ["crucial", "archive"] if number == 12 else ["synthetic", "recent"],
        }
        fact_id = f"fact_scene_{number:04d}"
        event("canonical_fact", "past_constraint", fact_id, {
            "fact_id": fact_id, "subject": f"synthetic_subject_{number:04d}", "predicate": "fixture_value",
            "value": number, "status": "established", "relevance": relevance,
        }, number)
        event("knowledge_state", "past_constraint", f"knowledge_scene_{number:04d}", {
            "knowledge_id": f"knowledge_scene_{number:04d}", "subject_id": f"character_{number % 5 + 1:02d}",
            "relation": "explicitly_does_not_know" if number == 12 else "suspects",
            "proposition_id": fact_id, "action": "establish", "relevance": {"character_ids": [f"character_{number % 5 + 1:02d}"]},
        }, number)
        event("motif_state", "motif_pressure", f"motif_event_{number:04d}", {
            "motif_event_id": f"motif_event_{number:04d}", "motif_id": f"motif_{number % 12:02d}",
            "action": "appear", "current_function": "synthetic tracking", "pressure": "transform before reuse",
            "overuse_risk": "elevated" if number % 4 == 0 else "low", "relevance": {"motif_ids": [f"motif_{number % 12:02d}"]},
        }, number)
    for number, debt in enumerate(obligations, 1):
        event("obligation", "future_obligation", debt["obligation_id"], debt, min(number, SCENE_COUNT))
    records = []
    web = scale_web_fixture()
    for packet in web["packets"][:PACKET_COUNT]:
        records.append({
            "record_type": "creative_packet",
            "commit_id": packet["commit_id"],
            "packet_slot_id": packet["packet_slot_id"],
            "scenes": [{"scene_id": scene["scene_id"], "prose_mdx": scene["prose_mdx"]} for scene in packet["scenes"]],
            "artifacts": [], "endings": [], "formal_compositions": [], "decision_edges": [], "constraint_delta": {},
        })
    return architecture, events, records


def tree_hash(root):
    digest = RUNNER.hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


class ScaleRehearsalTests(unittest.TestCase):
    def test_150_scene_constraint_retrieval_context_and_prospective_planning(self):
        architecture, events, records = scale_constraint_fixture()
        plan = architecture["packet_plans"][43] | {"advance_obligation_ids": [], "may_satisfy_obligation_ids": []}
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "synthetic_scale"
            for name in ("constraints", "state", "planning"):
                (run / name).mkdir(parents=True)
            (run / "constraints/constraint-events.jsonl").write_bytes(b"".join(RUNNER.canonical_json(item) for item in events))
            selected = RUNNER.select_relevant_constraints(run, architecture, plan, records=records)
            selected_ids = {item["constraint_id"] for item in selected}
            self.assertIn("fact_scene_0012", selected_ids)
            retrieved = RUNNER.retrieve_original_sources(run, selected, records=records)
            self.assertIn("synthetic_content_0012_z", {item["source_id"] for item in retrieved})
            facts, knowledge, obligations, motifs, _ = RUNNER.project_constraint_state(events)
            self.assertEqual(facts["fact_scene_0012"]["data"]["value"], 12)
            self.assertIn("fact_scene_0012", knowledge["character_03"]["explicitly_does_not_know"])
            self.assertEqual(len(obligations), 120)
            self.assertEqual(len(motifs), 12)

            RUNNER.save_state(run, RUNNER.initial_run_state("synthetic_scale", "generation/synthetic_scale", "a" * 64, "b" * 64, "offline"))
            RUNNER.write_json(run / "state/obligations.json", obligations)
            RUNNER.write_json(run / "state/foreclosure-candidates.json", {})
            committed = []
            original_sources = [RUNNER.canonical_json(record) for record in records]
            started = time.perf_counter()
            with mock.patch.object(RUNNER, "committed_record", return_value=architecture), mock.patch.object(
                RUNNER, "all_committed_records", side_effect=lambda _run: committed
            ):
                for number, record in enumerate(records, 1):
                    committed.append(record)
                    RUNNER.recompute_prospective_plan(run, f"commit_scale_{number:03d}")
                blocked = RUNNER.read_json(run / "state/prospective-plan.json")
                self.assertFalse(any(item["packet_slot_id"].startswith("packet_slot_ending") for item in blocked["packet_order"]))
                obligations["obligation_001"] = copy.deepcopy(obligations["obligation_001"])
                obligations["obligation_001"]["data"]["status"] = "satisfied"
                obligations["obligation_001"]["resolution_event"] = {"sources": [source(150)]}
                RUNNER.write_json(run / "state/obligations.json", obligations)
                eligible = RUNNER.recompute_prospective_plan(run, "commit_satisfaction")
            elapsed = time.perf_counter() - started
            self.assertIn("packet_slot_ending_01", {item["packet_slot_id"] for item in eligible["packet_order"]})
            self.assertEqual(original_sources, [RUNNER.canonical_json(record) for record in records])
            self.assertEqual(len((run / "planning/prospective-plans.jsonl").read_text().splitlines()), PACKET_COUNT + 1)
            state = RUNNER.load_state(run)
            self.assertEqual([state[key] for key in ("committed_rewrite_count", "committed_regeneration_count", "backtrack_count")], [0, 0, 0])
            self.assertLess(elapsed, 10)

            impossible = copy.deepcopy(obligations)
            impossible["obligation_009"]["data"]["status"] = "impossible"
            candidate = {
                "constraint_id": "foreclosure_candidate_01", "data": {
                    "attractor_id": "attractor_ending_02", "negated_prerequisite_obligation_ids": ["obligation_009"],
                    "reason": "Synthetic immutable negation.",
                }, "sources": [source(120)],
            }
            feasibility = RUNNER.evaluate_feasibility(architecture, impossible, {"foreclosure_candidate_01": candidate})
            self.assertEqual(next(item for item in feasibility if item["attractor_id"] == "attractor_ending_02")["status"], "foreclosed")
            universal = copy.deepcopy(obligations)
            universal["obligation_001"]["data"]["status"] = "impossible"
            universal_status = RUNNER.evaluate_feasibility(architecture, universal, {})[0]["status"]
            self.assertEqual(universal_status, "universally_required_but_impossible")

    def test_context_packing_keeps_whole_hard_records_and_reports_pressure(self):
        architecture, events, records = scale_constraint_fixture()
        plan = architecture["packet_plans"][43] | {"advance_obligation_ids": [], "may_satisfy_obligation_ids": []}
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            (run / "constraints").mkdir()
            (run / "constraints/constraint-events.jsonl").write_bytes(b"".join(RUNNER.canonical_json(item) for item in events))
            selected = RUNNER.select_relevant_constraints(run, architecture, plan, records=records)
            positive = [item for item in events if RUNNER.relevance_score(item, plan, architecture, set(), len(events)) > 0]
            retrieved = RUNNER.retrieve_original_sources(run, selected, records=records)
            hard = [{"id": f"hard_{number:02d}", "class": "hard", "payload": "x" * 40} for number in range(8)]
            soft = [{"id": f"soft_{number:03d}", "class": "soft", "payload": "y" * 300} for number in range(100)]
            packed = RUNNER.bounded_context([("HARD", hard), ("SOFT", soft), ("RECENT", soft[-5:])], 500)
            self.assertTrue(all(item["id"] in packed for item in hard))
            self.assertNotIn('"id": "soft_099"', packed)
            self.assertNotIn("…", packed)
            self.assertLessEqual(len(packed), 500 * 4)
            self.assertEqual(len(selected), min(96, len(positive)))
            self.assertLessEqual(len(retrieved), 24)

    def test_technical_slots_and_projection_scale_without_source_mutation(self):
        fixture = scale_web_fixture()
        before = RUNNER.canonical_json(fixture["edges"])
        resolved, resolved_endings = RUNNER.resolve_cross_packet_links(fixture["scenes"], fixture["endings"], fixture["edges"])
        self.assertEqual(len(resolved), len(fixture["edges"]))
        self.assertEqual(resolved_endings[-1]["resolved_redirect_content_id"], "synthetic_content_0130_z")
        self.assertEqual(before, RUNNER.canonical_json(fixture["edges"]))
        duplicate = copy.deepcopy(fixture["endings"][0])
        duplicate["technical_slot_id"] = "scene_slot_0001"
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.resolve_cross_packet_links(fixture["scenes"], fixture["endings"] + [duplicate], fixture["edges"])
        broken = copy.deepcopy(fixture["edges"])
        broken[0]["destination"]["id"] = "scene_slot_missing"
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.resolve_cross_packet_links(fixture["scenes"], fixture["endings"], broken)
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.resolve_cross_packet_links([scene for scene in fixture["scenes"] if scene["technical_slot_id"] != "scene_slot_0002"], fixture["endings"], fixture["edges"])
        self.assertEqual(next(edge for edge in resolved if edge["edge_id"] == "edge_0150_ending")["resolved_content_id"], "synthetic_terminal_01_q")
        self.assertEqual(next(edge for edge in resolved if edge["edge_id"] == "edge_0015_cross")["resolved_content_id"], "synthetic_content_0022_z")

        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "synthetic_scale"
            run.mkdir()
            RUNNER.write_json(run / "run-manifest.json", fixture["manifest"])
            with mock.patch.object(RUNNER, "reconcile_run"), mock.patch.object(
                RUNNER, "committed_record", side_effect=lambda _run, kind: fixture[kind]
            ), mock.patch.object(RUNNER, "all_committed_records", return_value=fixture["packets"]), mock.patch.object(
                RUNNER, "append_deterministic_step"
            ):
                project, counts = RUNNER.project_web(run)
            self.assertEqual(counts, {"scenes": SCENE_COUNT, "artifacts": ARTIFACT_COUNT, "endings": ENDING_COUNT})
            source_markdown = fixture["scenes"][0]["prose_mdx"].encode()
            self.assertEqual((project / "public/source/synthetic_content_0001_z.md").read_bytes(), source_markdown)
            self.assertEqual(RUNNER.read_json(project / "public/work.json")["decision_edges"][0]["resolved_content_id"], "synthetic_content_0002_z")
            RUNNER.validate_markdown_source(source_markdown.decode(), "Synthetic fixture")
            with self.assertRaises(RUNNER.SchemaError):
                RUNNER.validate_markdown_source("<script>alert(1)</script>", "Synthetic fixture")

    def test_resume_replays_prefixes_without_regeneration(self):
        architecture, events, records = scale_constraint_fixture()
        fixture = scale_web_fixture()
        _, _, obligations, _, _ = RUNNER.project_constraint_state(events)
        record_bytes = [RUNNER.canonical_json(record) for record in records]
        checkpoints = (0, 1, PACKET_COUNT // 3, PACKET_COUNT * 2 // 3, PACKET_COUNT)
        previous_ledger = b""
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "synthetic_resume"
            (run / "state").mkdir(parents=True)
            (run / "planning").mkdir()
            RUNNER.save_state(run, RUNNER.initial_run_state("synthetic_resume", "generation/synthetic_resume", "a" * 64, "b" * 64, "offline"))
            RUNNER.write_json(run / "state/obligations.json", obligations)
            RUNNER.write_json(run / "state/foreclosure-candidates.json", {})
            for checkpoint in checkpoints:
                prefix = record_bytes[:checkpoint]
                ledger = b"".join(RUNNER.canonical_json({"sequence": number + 1, "record_hash": RUNNER.sha256_bytes(value)}) for number, value in enumerate(prefix))
                self.assertTrue(ledger.startswith(previous_ledger))
                self.assertEqual(prefix, record_bytes[:checkpoint])
                event_cutoff = min(len(events), checkpoint * 9)
                first = RUNNER.project_constraint_state(events[:event_cutoff])
                second = RUNNER.project_constraint_state(events[:event_cutoff])
                self.assertEqual(first, second)
                committed_packets = fixture["packets"][:checkpoint]
                committed_scenes = [scene for packet in committed_packets for scene in packet["scenes"]]
                slot_state = RUNNER.technical_slot_map(committed_scenes, [])
                self.assertEqual(len(slot_state), checkpoint * 3)
                with mock.patch.object(RUNNER, "all_committed_records", return_value=records[:checkpoint]):
                    first_plan = RUNNER.build_prospective_plan(run, architecture, f"checkpoint_{checkpoint:03d}")
                    resumed_plan = RUNNER.build_prospective_plan(run, architecture, f"checkpoint_{checkpoint:03d}")
                self.assertEqual(first_plan["feasibility"], resumed_plan["feasibility"])
                self.assertEqual(first_plan["obligation_assignments"], resumed_plan["obligation_assignments"])
                self.assertEqual(first_plan["packet_order"], resumed_plan["packet_order"])
                previous_ledger = ledger
        stale = RUNNER.project_constraint_state(events[:90])
        reconciled = RUNNER.project_constraint_state(events[:99])
        self.assertGreater(len(reconciled[0]), len(stale[0]))
        state = RUNNER.initial_run_state("synthetic_scale", "generation/synthetic_scale", "a" * 64, "b" * 64, "offline")
        self.assertEqual([state[key] for key in ("committed_rewrite_count", "committed_regeneration_count", "backtrack_count")], [0, 0, 0])

    def test_diagnostic_failure_remains_nonplayable_and_unpublished(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = root / ".cathedrals/runs/synthetic_scale"
            for name in ("state", "validation", "committed", "projection/web/dist"):
                (run / name).mkdir(parents=True)
            (run / "projection/web/dist/index.html").write_text("synthetic diagnostic")
            RUNNER.write_json(run / "run-manifest.json", {"synthetic": True})
            state = RUNNER.initial_run_state("synthetic_scale", "generation/synthetic_scale", "a" * 64, RUNNER.sha256_file(run / "run-manifest.json"), "offline")
            RUNNER.save_state(run, state)
            RUNNER.append_deterministic_step(run, "synthetic_complete", "validation", "c" * 64)
            for name, result in (("mechanical", "PASS"), ("build", "PASS"), ("artistic", "FAIL GENERATION")):
                RUNNER.write_json(run / f"validation/{name}.json", {"result": result, "reasons": ["synthetic verdict"]})
            with mock.patch.object(RUNNER, "ROOT", root):
                finalization = RUNNER.finalize_failure(run, RUNNER.CathedralsError("Whole-work artistic acceptance", "synthetic rejection", "artistic_rejection"))
            self.assertEqual(finalization["run_status"], "FAILED_GENERATION")
            self.assertFalse(finalization["playable"])
            self.assertFalse(finalization["complete_work_barrier_satisfied"])
            self.assertTrue((run / "projection/web/dist/index.html").exists())
            self.assertFalse((root / "generated-work").exists())

    def test_disposable_git_generations_share_main_parent_and_publish_only_their_work(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)

            def command(*args, check=True):
                result = subprocess.run(args, cwd=repo, text=True, capture_output=True)
                if check and result.returncode:
                    self.fail(result.stderr or result.stdout)
                return result.stdout.strip()

            command("git", "init", "-b", "main")
            command("git", "config", "user.name", "Synthetic Rehearsal")
            command("git", "config", "user.email", "synthetic@example.invalid")
            (repo / ".gitignore").write_text(".cathedrals/\nnode_modules/\n")
            (repo / "engine.txt").write_text("synthetic engine\n")
            command("git", "add", ".gitignore", "engine.txt")
            command("git", "commit", "-m", "synthetic engine base")
            base = command("git", "rev-parse", "HEAD")

            def run_command(args, *, cwd=None, env=None, capture=True):
                return subprocess.run([str(item) for item in args], cwd=cwd or repo, env=env, text=True, capture_output=capture)

            with mock.patch.object(RUNNER, "ROOT", repo), mock.patch.object(RUNNER, "run_command", side_effect=run_command):
                for identifier in ("synthetic_a", "synthetic_b"):
                    branch, branch_base = RUNNER.prepare_generation_branch(identifier)
                    self.assertEqual(branch_base, base)
                    run = repo / f".cathedrals/runs/{identifier}"
                    (run / "state").mkdir(parents=True)
                    RUNNER.save_state(run, RUNNER.initial_run_state(identifier, branch, "a" * 64, "b" * 64, "offline"))
                    destination = repo / f"generated-work/{identifier}"
                    destination.mkdir(parents=True)
                    (destination / "index.html").write_text("synthetic publication\n")
                    if identifier == "synthetic_b":
                        (repo / "unrelated.txt").write_text("must remain untracked\n")
                        (repo / ".cathedrals/cache.bin").write_text("ignored runtime cache\n")
                    RUNNER.commit_published_generation(run, destination)
                    self.assertEqual(command("git", "rev-parse", f"{branch}^"), base)
                    changed = command("git", "diff-tree", "--no-commit-id", "--name-only", "-r", branch).splitlines()
                    self.assertEqual(changed, [f"generated-work/{identifier}/index.html"])
            self.assertEqual(command("git", "rev-list", "--count", "main..generation/synthetic_a"), "1")
            self.assertEqual(command("git", "rev-list", "--count", "main..generation/synthetic_b"), "1")
            self.assertIn("?? unrelated.txt", command("git", "status", "--short"))
            self.assertEqual(command("git", "check-ignore", ".cathedrals/cache.bin"), ".cathedrals/cache.bin")


if __name__ == "__main__":
    unittest.main()
