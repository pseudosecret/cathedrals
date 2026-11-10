"""Current policy initialization and the boundary around frozen legacy runtimes."""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_cathedrals import ROOT, RUNNER


class CurrentEngineTests(unittest.TestCase):
    def test_new_runs_always_freeze_the_current_planner(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with mock.patch.object(RUNNER, "RUNTIME_ROOT", root), mock.patch.object(RUNNER, "RUNS_ROOT", root / "runs"):
                run = RUNNER.create_run(RUNNER.FrozenInputs(), "http://offline.invalid", "offline", output_fn=lambda _: None)
            policy = RUNNER.read_json(run / "run-manifest.json")["execution_policy"]
            self.assertEqual(policy, RUNNER.CURRENT_EXECUTION_POLICY)

    def test_obsolete_policies_are_rejected_before_creating_a_run(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with mock.patch.object(RUNNER, "RUNTIME_ROOT", root), mock.patch.object(RUNNER, "RUNS_ROOT", root / "runs"):
                for policy in ({"scaffold_planning_version": 1}, {"scaffold_planning_version": 2}, {"bounded_planning": False},
                        {"scoped_sources": False}, {"completion_contract_version": True}):
                    with self.subTest(policy=policy), self.assertRaisesRegex(RUNNER.CathedralsError, "current engine requires"):
                        RUNNER.create_run(RUNNER.FrozenInputs(), "http://offline.invalid", "offline", execution_policy=policy)
            self.assertEqual(list(root.iterdir()), [])

    def test_missing_snapshot_does_not_validate_or_finalize_with_the_installed_engine(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            RUNNER.write_atomic(run / "state/run-state.json", b"preserve original state bytes")
            output = []
            forbidden = mock.Mock(side_effect=AssertionError("Installed engine touched an old run"))
            with mock.patch.object(RUNNER, "ensure_runtime_layout"), mock.patch.object(RUNNER, "choose_resume", return_value=run), mock.patch.object(
                    RUNNER, "ensure_resume_ready", forbidden), mock.patch.object(RUNNER, "finalize_failure", forbidden):
                self.assertEqual(RUNNER.main([], output_fn=output.append, transport=forbidden), 1)
            self.assertIn("saved engine snapshot is incomplete", "\n".join(output))
            self.assertEqual((run / "state/run-state.json").read_bytes(), b"preserve original state bytes")
            self.assertFalse((run / "finalization.json").exists())
            forbidden.assert_not_called()

    def test_legacy_resume_dispatches_before_current_policy_validation(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            snapshot = RUNNER.snapshot_root(run)
            (snapshot / "engine").mkdir(parents=True)
            (snapshot / "cathedrals").write_text("synthetic old engine")
            forbidden = mock.Mock(side_effect=AssertionError("Current schemas reached legacy run"))
            with mock.patch.object(RUNNER, "ensure_runtime_layout"), mock.patch.object(RUNNER, "choose_resume", return_value=run), mock.patch.object(
                    RUNNER, "run_snapshot_launcher", return_value=7) as dispatch, mock.patch.object(RUNNER, "load_protocol", forbidden):
                self.assertEqual(RUNNER.main([], output_fn=lambda _: None, transport=forbidden), 7)
            dispatch.assert_called_once()
            forbidden.assert_not_called()
