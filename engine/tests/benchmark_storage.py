#!/usr/bin/env python3
"""Offline storage benchmark. Synthetic metadata only; all outputs live in /tmp."""

import argparse
import importlib.machinery
import importlib.util
import json
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).parents[2]
loader = importlib.machinery.SourceFileLoader("storage_benchmark_runner", str(ROOT / "cathedrals"))
spec = importlib.util.spec_from_loader(loader.name, loader)
RUNNER = importlib.util.module_from_spec(spec)
sys.modules[loader.name] = RUNNER
loader.exec_module(RUNNER)


def packet(generation_id, number):
    scene_id = f"scene_{number:06d}"
    source = {"artifact_type": "scene", "artifact_id": scene_id, "source_locator": "prose_mdx"}
    fact = {"fact_id": f"fact_{number:06d}", "subject": scene_id, "predicate": "fixture_value",
            "value": number, "status": "established", "sources": [source], "relevance": {}}
    if number > 1 and number % 10 == 0:
        fact["supersedes_fact_id"] = f"fact_{number - 1:06d}"
    delta = {key: [] for key in ("canonical_facts", "knowledge_changes", "new_obligations",
                                "obligation_updates", "motif_events", "potential_foreclosures")}
    delta.update(canonical_facts=[fact], knowledge_changes=[{
        "knowledge_id": f"knowledge_{number:06d}", "subject_id": "character_fixture",
        "relation": "knows", "proposition_id": "fact_000001",
        "action": "retract" if number % 3 == 0 else "establish", "sources": [source], "relevance": {},
    }], motif_events=[{
        "motif_event_id": f"motif_event_{number:06d}", "motif_id": "motif_fixture",
        "action": "establish" if number == 1 else "appear", "current_function": "Synthetic tracking",
        "pressure": "Synthetic pressure", "overuse_risk": "low", "sources": [source], "relevance": {},
    }])
    return {
        "record_type": "creative_packet", "protocol_version": RUNNER.PROTOCOL_VERSION,
        "generation_id": generation_id, "commit_id": f"commit_{number:06d}",
        "architecture_core_commit_id": "fixture_core", "packet_plan_commit_id": "fixture_plan",
        "story_format": "web", "packet_slot_id": f"packet_{number:06d}", "packet_kind": "literary",
        "packet_sequence": number, "obligations_advanced": [], "scenes": [{
            "technical_slot_id": f"scene_slot_{number:06d}", "scene_id": scene_id, "arc_id": "arc_fixture",
            "title": "Synthetic storage fixture", "scene_type": "exploration", "beat_jobs": ["fixture", "tracking"],
            "branch_depth": 1, "claimant_focus_ids": [], "epistemic_dependencies": [],
            "threshold_figure": "1-1-1-1", "threshold_resultant": None, "state_inputs": [], "state_effects": [],
            "artifact_ids": [], "choice_edge_ids": [], "major_decision": False, "hesitation_consequence": None,
            "web_composition": {"surface_mode": "prose", "artifact_behavior": "none", "navigational_discovery": "Fixture"},
            "prose_mdx": f"Synthetic storage placeholder {number}.",
        }], "artifacts": [], "endings": [], "decision_edges": [], "formal_compositions": [], "constraint_delta": delta,
    }


def commit(run, number, *, needle=False):
    record = packet(run.name, number)
    if needle:
        record["scenes"][0]["prose_mdx"] += " rehearsalneedle"
    return RUNNER.commit_record(run, record, RUNNER.canonical_json(record).decode(), {},
        planned_step_id=f"fixture_{number:06d}", attempt=1, step_phase="literary_packet",
        prompt="Synthetic benchmark", context="Synthetic benchmark", parameters={"seed": "fixture"}, branch_relation="fixture")


def worker(count):
    with tempfile.TemporaryDirectory(prefix="cathedrals-storage-") as temporary:
        root = Path(temporary)
        with mock.patch.object(RUNNER, "RUNTIME_ROOT", root), mock.patch.object(RUNNER, "RUNS_ROOT", root / "runs"):
            run = RUNNER.create_run(RUNNER.FrozenInputs(possible_scene_count=max(20, count)), "http://offline.invalid", "offline", output_fn=lambda _: None)
        archive_reads = {"opens": 0, "bytes": 0}
        original_open = Path.open

        def measured_open(path, mode="r", *args, **kwargs):
            if mode in {"r", "rb"} and path.is_relative_to(run):
                relative = path.relative_to(run)
                if relative.parts[0] in {"committed", "constraints", "planning"} or relative.name == "ledger.jsonl":
                    archive_reads["opens"] += 1
                    archive_reads["bytes"] += path.stat().st_size
            return original_open(path, mode, *args, **kwargs)

        started = time.perf_counter()
        batch_start = started
        with mock.patch.object(Path, "open", measured_open):
            for number in range(1, count + 1):
                commit(run, number, needle=number == 1)
                # Include noncreative entries: a 5,000-scene archive crosses ledger sequence 9,999.
                RUNNER.append_deterministic_step(run, f"audit_{number:06d}", "validation", "c" * 64)
                if number % 100 == 0 or number == count:
                    now = time.perf_counter()
                    print(json.dumps({"progress": number, "elapsed_seconds": now - started, "batch_seconds": now - batch_start}), flush=True)
                    batch_start = now
        commit_seconds = time.perf_counter() - started
        events = [json.loads(line) for line in (run / "constraints/constraint-events.jsonl").read_text().splitlines()]
        expected = RUNNER.project_constraint_state(events)
        for name, value in zip(("canonical-facts.json", "knowledge-state.json", "obligations.json", "motifs.json", "foreclosure-candidates.json"), expected):
            assert RUNNER._read_state_map(run, name) == value, name
        retrieval = {}
        if hasattr(RUNNER, "search_history"):
            plan = {"packet_slot_id": "next_fixture", "packet_kind": "literary", "scene_slot_ids": ["next_scene"],
                "ending_slot_ids": [], "artifact_count": 0, "formal_composition_count": 0, "depends_on_packet_slot_ids": [],
                "advance_obligation_ids": [], "may_satisfy_obligation_ids": [], "attractor_ids": [],
                "relevance": {"keywords": ["rehearsalneedle"]}, "soft_guidance": [], "branch_path_relation": "fixture"}
            architecture = {"obligation_graph": [], "attractors": [], "packet_plans": []}
            # This is the pre-FTS metadata selection algorithm, using the same current SQL storage.
            started = time.perf_counter()
            baseline_events = RUNNER.constraint_events(run)
            baseline = sorted(((RUNNER.relevance_score(event, plan, architecture, set(), len(baseline_events)), event)
                for event in baseline_events), key=lambda item: (-item[0],item[1]["constraint_event_sequence"]))[:96]
            retrieval["baseline_metadata_scan_seconds"] = time.perf_counter() - started
            retrieval["baseline_events_deserialized"] = len(baseline_events)
            started = time.perf_counter()
            trace = {}
            selected = RUNNER.select_relevant_constraints(run, architecture, plan, trace=trace)
            retrieval["indexed_constraint_seconds"] = time.perf_counter() - started
            retrieval["indexed_events_deserialized"] = trace["constraint_candidate_counts"]["deserialized"]
            started = time.perf_counter()
            hits = RUNNER.search_history(run, RUNNER.search_query(plan))
            retrieval["source_search_seconds"] = time.perf_counter() - started
            assert hits and hits[0]["source_id"] == "scene_000001"
            retrieval["unextracted_source_rank"] = 1
            retrieval["baseline_selected_original_source"] = any(source["artifact_id"] == "scene_000001" for score,event in baseline if score > 0 for source in event["sources"])
            receipt = {}
            with mock.patch.object(RUNNER, "committed_record", return_value={"record_type": "genesis", "claimants": [], "characters": []}), mock.patch.object(
                RUNNER, "ensure_frozen_geomancy", return_value={"assignments": []}
            ), mock.patch.object(RUNNER, "scoped_root_sources", return_value=[]
            ):
                started = time.perf_counter()
                context = RUNNER.relevant_packet_context(run, architecture, plan, receipt=receipt)
                retrieval["context_seconds"] = time.perf_counter() - started
            assert "rehearsalneedle" in context
            retrieval["context_bytes"] = receipt["context_bytes"]
            retrieval["estimated_context_tokens"] = receipt["estimated_context_tokens"]
            # Hold required coverage constant when measuring formatting/metadata compaction.
            required = [("FIXED LAW", "Synthetic law."), ("EXACT REQUIRED RECORDS", events[:24])]
            compact = {"omissions": []}
            RUNNER.pack_packet_context(required, [], 49152, compact)
            assert compact["required_compact_bytes"] <= compact["required_pretty_bytes"]
            retrieval["same_coverage_pretty_bytes"] = compact["required_pretty_bytes"]
            retrieval["same_coverage_compact_bytes"] = compact["required_compact_bytes"]
        started = time.perf_counter()
        RUNNER.reconcile_run(run)
        verify_seconds = time.perf_counter() - started
        started = time.perf_counter()
        RUNNER.build_prospective_plan(run, {"obligation_graph": [], "attractors": [], "packet_plans": []}, f"commit_{count:06d}")
        planning_seconds = time.perf_counter() - started
        for name, value in zip(("canonical-facts.json", "knowledge-state.json", "obligations.json", "motifs.json", "foreclosure-candidates.json"), expected):
            assert RUNNER._read_state_map(run, name) == value, name
        rebuild_seconds = None
        database = run / "state/index.sqlite3"
        database_bytes = database.stat().st_size if database.exists() else 0
        if database.exists():
            database.unlink()
            started = time.perf_counter()
            RUNNER.reconcile_run(run)
            rebuild_seconds = time.perf_counter() - started
            for name, value in zip(("canonical-facts.json", "knowledge-state.json", "obligations.json", "motifs.json", "foreclosure-candidates.json"), expected):
                assert RUNNER._read_state_map(run, name) == value, name
            if retrieval:
                rebuilt_hits = RUNNER.search_history(run, RUNNER.search_query(plan))
                assert [(hit["commit_id"], hit["pointer"], hit["bm25"]) for hit in rebuilt_hits] == [
                    (hit["commit_id"], hit["pointer"], hit["bm25"]) for hit in hits]
        print(json.dumps({"scenes": count, "events": len(events), "commit_seconds": commit_seconds,
                          "verify_seconds": verify_seconds, "planning_scan_seconds": planning_seconds,
                          "rebuild_seconds": rebuild_seconds, "database_bytes": database_bytes,
                          "archive_read_opens_during_commits": archive_reads["opens"],
                          "archive_read_bytes_during_commits": archive_reads["bytes"],
                          "retrieval": retrieval,
                          "python": sys.version.split()[0], "sqlite": sqlite3.sqlite_version}), flush=True)


def main():
    global RUNNER
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenes", nargs="+", type=int, default=[150, 1000, 5000])
    parser.add_argument("--timeout", type=int, default=60, help="Seconds allowed per size; use 0 for no limit")
    parser.add_argument("--worker", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--launcher", type=Path, default=ROOT / "cathedrals", help="Launcher revision to measure; uses this checkout's engine inputs")
    args = parser.parse_args()
    if args.timeout < 0 or any(count < 1 for count in args.scenes) or args.worker is not None and args.worker < 1:
        parser.error("Scene counts must be positive and timeout must be nonnegative")
    if args.launcher != ROOT / "cathedrals":
        selected_loader = importlib.machinery.SourceFileLoader("storage_benchmark_revision", str(args.launcher))
        selected_spec = importlib.util.spec_from_loader(selected_loader.name, selected_loader)
        RUNNER = importlib.util.module_from_spec(selected_spec)
        sys.modules[selected_loader.name] = RUNNER
        selected_loader.exec_module(RUNNER)
        RUNNER.ROOT = ROOT
    if args.worker is not None:
        worker(args.worker)
        return
    for count in args.scenes:
        try:
            result = subprocess.run([sys.executable, "-B", __file__, "--worker", str(count), "--launcher", str(args.launcher)], capture_output=True,
                                    text=True, timeout=args.timeout or None)
            print(result.stdout, end="", flush=True)
            if result.returncode:
                sys.stderr.write(result.stderr)
                raise SystemExit(result.returncode)
        except subprocess.TimeoutExpired as error:
            output = error.stdout or b""
            if isinstance(output, bytes):
                output = output.decode()
            print(output, end="")
            print(json.dumps({"scenes": count, "timeout_seconds": args.timeout, "completed": False}), flush=True)


if __name__ == "__main__":
    main()
