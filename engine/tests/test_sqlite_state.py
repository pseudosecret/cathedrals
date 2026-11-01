"""Real archived commits and SQLite recovery; no model or network access."""

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from benchmark_storage import RUNNER, commit, packet


class SQLiteStateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        with mock.patch.object(RUNNER, "RUNTIME_ROOT", root), mock.patch.object(RUNNER, "RUNS_ROOT", root / "runs"):
            self.run = RUNNER.create_run(RUNNER.FrozenInputs(possible_scene_count=20), "http://offline.invalid", "offline", output_fn=lambda _: None)

    def assert_projection(self):
        events = [json.loads(line) for line in (self.run / "constraints/constraint-events.jsonl").read_text().splitlines()]
        expected = RUNNER.project_constraint_state(events)
        for name, value in zip(RUNNER.STATE_MAPS, expected):
            actual = RUNNER._read_state_map(self.run, name)
            self.assertEqual(actual, value, name)
            self.assertEqual(list(actual), list(value), name)
        self.assertEqual(RUNNER.index_checkpoint(self.run)["event_sequence"], len(events))
        return events

    def test_automatic_initialization_incremental_updates_and_replay(self):
        self.assertTrue(RUNNER.index_path(self.run).is_file())
        for number in range(1, 13):
            commit(self.run, number)
            self.assert_projection()
        self.assertNotIn("fact_000009", RUNNER._read_state_map(self.run, "canonical-facts.json"))
        self.assertEqual(RUNNER._read_state_map(self.run, "knowledge-state.json")["character_fixture"]["knows"], {})
        self.assertEqual(len(RUNNER._read_state_map(self.run, "motifs.json")["motif_fixture"]["appearances"]), 12)
        index_before = RUNNER.index_path(self.run).read_bytes()
        RUNNER.reconcile_run(self.run)
        self.assertEqual(RUNNER.index_path(self.run).read_bytes(), index_before)
        self.assertEqual(RUNNER.load_state(self.run)["creative_step_count"], 12)

    def test_commit_never_scans_old_archives_or_the_full_ledger(self):
        commit(self.run, 1)
        read_json = RUNNER.read_json

        def bounded_read(path):
            self.assertNotIn("committed", path.relative_to(self.run).parts)
            return read_json(path)

        with mock.patch.object(RUNNER, "committed_directories", side_effect=AssertionError("archive scan")), mock.patch.object(
            RUNNER, "ledger_entries", side_effect=AssertionError("full ledger")
        ), mock.patch.object(RUNNER, "reconcile_run", side_effect=AssertionError("full replay")), mock.patch.object(
            RUNNER, "read_json", side_effect=bounded_read
        ):
            commit(self.run, 2)
            RUNNER.append_deterministic_step(self.run, "audit_two", "validation", "a" * 64)
        self.assert_projection()

    def test_recover_archive_rename_before_ledger_append(self):
        with mock.patch.object(RUNNER, "append_ledger_entry", side_effect=RuntimeError("interrupted")):
            with self.assertRaises(RuntimeError):
                commit(self.run, 1)
        self.assertFalse(RUNNER.step_is_committed(self.run, "fixture_000001"))
        RUNNER.reconcile_run(self.run)
        ledger = (self.run / "ledger.jsonl").read_bytes()
        RUNNER.reconcile_run(self.run)
        self.assertEqual((self.run / "ledger.jsonl").read_bytes(), ledger)
        self.assertEqual(RUNNER.load_state(self.run)["creative_step_count"], 1)
        self.assert_projection()

    def test_database_transaction_rolls_back_and_recovers_durable_commit(self):
        apply_event = RUNNER.index_event
        calls = 0

        def interrupted(db, event):
            nonlocal calls
            apply_event(db, event)
            calls += 1
            if calls == 2:
                raise sqlite3.OperationalError("synthetic disk full")

        with mock.patch.object(RUNNER, "index_event", side_effect=interrupted):
            with self.assertRaises(RUNNER.PausedError):
                commit(self.run, 1)
        self.assertEqual(RUNNER.index_checkpoint(self.run)["event_sequence"], 0)
        self.assertEqual(RUNNER._source_index(self.run), {})
        RUNNER.pause_run(self.run, RUNNER.PausedError("SQLite state", "synthetic failure"))
        RUNNER.reconcile_run(self.run)
        self.assertTrue(RUNNER.step_is_committed(self.run, "fixture_000001"))
        self.assert_projection()

    def test_partial_ledger_and_constraint_appends_recover_only_exact_known_bytes(self):
        with mock.patch.object(RUNNER, "append_ledger_entry", side_effect=RuntimeError("interrupted")):
            with self.assertRaises(RuntimeError):
                commit(self.run, 1)
        directory = RUNNER.committed_directories(self.run)[0]
        meta = RUNNER.read_json(directory / "commit-meta.json")
        ledger = self.run / "ledger.jsonl"
        prefix = ledger.read_bytes()
        expected = RUNNER.canonical_json(meta["ledger_entry"])
        ledger.write_bytes(prefix + expected[:137])
        constraint_path = self.run / "constraints/constraint-events.jsonl"
        constraint_path.write_bytes(RUNNER.canonical_json(meta["constraint_events"][0])[:41])
        RUNNER.reconcile_run(self.run)
        self.assertEqual(ledger.read_bytes(), prefix + expected)
        self.assert_projection()
        ledger.write_bytes(ledger.read_bytes() + b'{"unknown_partial":')
        with self.assertRaisesRegex(RUNNER.IntegrityError, "no exact immutable"):
            RUNNER.reconcile_run(self.run)

    def test_rebuild_missing_corrupt_incompatible_foreign_and_stale_databases(self):
        commit(self.run, 1)
        archive = {str(path.relative_to(self.run)): path.read_bytes() for directory in RUNNER.committed_directories(self.run) for path in directory.iterdir()}
        for damage in ("missing", "corrupt", "version", "identity", "row", "payload", "checkpoint"):
            with self.subTest(damage=damage):
                path = RUNNER.index_path(self.run)
                if damage == "missing":
                    path.unlink()
                elif damage == "corrupt":
                    path.write_bytes(b"synthetic corruption")
                else:
                    with sqlite3.connect(path) as db:
                        query = {
                            "version": "PRAGMA user_version=999",
                            "identity": "UPDATE identity SET generation_id='another_generation'",
                            "row": "UPDATE ledger SET step_id='changed' WHERE sequence=1",
                            "payload": "UPDATE projection SET payload='{'",
                            "checkpoint": "UPDATE checkpoint SET event_sequence=999",
                        }[damage]
                        db.execute(query)
                RUNNER.reconcile_run(self.run)
                self.assert_projection()
                self.assertEqual({name: (self.run / name).read_bytes() for name in archive}, archive)
        RUNNER.index_path(self.run).unlink()
        self.assertEqual(len(RUNNER._read_state_map(self.run, "canonical-facts.json")), 1)

    def test_changed_sources_and_truncated_ledger_are_integrity_failures(self):
        directory = commit(self.run, 1)
        raw = directory / "raw-response.txt"
        original = raw.read_bytes()
        raw.chmod(0o644)
        raw.write_bytes(b"changed")
        with self.assertRaises(RUNNER.IntegrityError):
            RUNNER.reconcile_run(self.run)
        raw.write_bytes(original)
        RUNNER.append_deterministic_step(self.run, "last_audit", "validation", "a" * 64)
        ledger = self.run / "ledger.jsonl"
        ledger.write_bytes(b"".join(ledger.read_bytes().splitlines(keepends=True)[:-1]))
        with self.assertRaisesRegex(RUNNER.IntegrityError, "truncated"):
            RUNNER.reconcile_run(self.run)

    def test_direct_evidence_lookup_reads_only_the_referenced_commit(self):
        directory = commit(self.run, 1)
        for number in range(2, 5):
            commit(self.run, number)
        event = RUNNER.constraint_events(self.run)[0]
        with mock.patch.object(RUNNER, "all_committed_records", side_effect=AssertionError("full scan")), mock.patch.object(
            RUNNER, "committed_directories", side_effect=AssertionError("archive scan")
        ):
            evidence = RUNNER.retrieve_original_sources(self.run, [event])
        self.assertEqual(evidence[0]["immutable_source"]["prose_mdx"], "Synthetic storage placeholder 1.")
        record = directory / "record.json"
        record.chmod(0o644)
        record.write_bytes(b"changed")
        with self.assertRaises(RUNNER.IntegrityError):
            RUNNER.retrieve_original_sources(self.run, [event])

    def test_duplicates_do_not_change_archives_and_accounting_is_exactly_once(self):
        commit(self.run, 1)
        before = (self.run / "ledger.jsonl").read_bytes()
        with self.assertRaises(RUNNER.IntegrityError):
            commit(self.run, 1)
        self.assertEqual((self.run / "ledger.jsonl").read_bytes(), before)
        RUNNER.append_failed_attempt(self.run, step_id="failed_analysis", attempt=1, phase="validation", prompt="fixture",
            context="fixture", parameters={"seed": "fixture"}, started_at=RUNNER.utc_now(), failure_class="malformed_response",
            step_type="analysis", usage={"prompt_tokens": 11, "completion_tokens": 7})
        RUNNER.reconcile_run(self.run)
        RUNNER.reconcile_run(self.run)
        state = RUNNER.load_state(self.run)
        self.assertEqual((state["input_tokens"], state["output_tokens"], state["analysis_step_count"]), (11, 7, 0))

    def test_obligation_resolution_and_foreclosure_match_full_replay(self):
        first = packet(self.run.name, 1)
        source = first["constraint_delta"]["canonical_facts"][0]["sources"][0]
        first["constraint_delta"]["new_obligations"] = [{
            "obligation_id": "obligation_fixture", "kind": "promise", "description": "Synthetic obligation",
            "status": "active", "created_by_ids": ["scene_000001"], "requires": [], "hardness": "hard",
            "universality": "local", "resolution_modes": ["consequence"], "range": "local", "termination_targets": [],
            "sources": [source], "relevance": {},
        }]
        second = packet(self.run.name, 2)
        second["constraint_delta"]["obligation_updates"] = [{
            "update_id": "update_fixture", "obligation_id": "obligation_fixture", "status": "satisfied",
            "reason": "Synthetic resolution", "evidence_sources": [source],
        }]
        second["constraint_delta"]["potential_foreclosures"] = [{
            "foreclosure_id": "foreclosure_fixture", "attractor_id": "attractor_fixture",
            "negated_prerequisite_obligation_ids": ["obligation_fixture"], "reason": "Synthetic foreclosure", "sources": [source],
        }]
        for number, record in enumerate((first, second), 1):
            RUNNER.commit_record(self.run, record, "synthetic", {}, planned_step_id=f"fixture_{number:06d}", attempt=1,
                step_phase="literary_packet", prompt="fixture", context="fixture", parameters={"seed": "fixture"}, branch_relation="fixture")
            self.assert_projection()
        self.assertEqual(RUNNER._read_state_map(self.run, "obligations.json")["obligation_fixture"]["data"]["status"], "satisfied")
        self.assertIn("foreclosure_fixture", RUNNER._read_state_map(self.run, "foreclosure-candidates.json"))

    def test_commit_directory_order_is_numeric(self):
        for name in ("9999-nine", "10000-ten", "10001-eleven"):
            (self.run / "committed" / name).mkdir()
        self.assertEqual([path.name for path in RUNNER.committed_directories(self.run)], ["9999-nine", "10000-ten", "10001-eleven"])

    def test_recover_plan_history_append_before_ledger_and_missing_plan_after_commit(self):
        commit(self.run, 1)
        architecture = {"commit_id": "fixture_core", "obligation_graph": [], "attractors": [], "packet_plans": []}
        with mock.patch.object(RUNNER, "committed_record", return_value=architecture), mock.patch.object(
            RUNNER, "append_deterministic_step", side_effect=RuntimeError("interrupted")
        ):
            with self.assertRaises(RuntimeError):
                RUNNER.recompute_prospective_plan(self.run, "commit_000001")
        with mock.patch.object(RUNNER, "committed_record", return_value=architecture):
            RUNNER.reconcile_run(self.run)
            RUNNER.reconcile_run(self.run)
        history = self.run / "planning/prospective-plans.jsonl"
        self.assertEqual(len(history.read_text().splitlines()), 1)
        self.assertEqual(RUNNER._read_state_map(self.run, "prospective-plan.json")["recomputed_after_commit_id"], "commit_000001")
        commit(self.run, 2)
        with mock.patch.object(RUNNER, "committed_record", return_value=architecture):
            RUNNER.reconcile_run(self.run)
        self.assertEqual(len(history.read_text().splitlines()), 2)
        self.assertEqual(RUNNER._read_state_map(self.run, "prospective-plan.json")["recomputed_after_commit_id"], "commit_000002")


if __name__ == "__main__":
    unittest.main()
