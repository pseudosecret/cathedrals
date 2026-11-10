"""Unexpected engine exceptions retain their origin and a local traceback."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_cathedrals import RUNNER


class GeneratorDiagnosticsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.run = Path(temporary.name) / "generation_diagnostic"
        self.run.mkdir()

    def missing_source(self):
        return {}["source_id"]

    def test_unexpected_error_preserves_type_origin_and_full_traceback(self):
        try:
            self.missing_source()
        except KeyError as error:
            wrapped = RUNNER.unexpected_generator_error(self.run, error)
        self.assertEqual(wrapped.stage, "Generator: missing_source")
        self.assertIn("KeyError: 'source_id'", wrapped.reason)
        self.assertIn("Location:", wrapped.reason)
        paths = list((self.run / "logs").glob("generator-error-*.json"))
        self.assertEqual(len(paths), 1)
        diagnostic = json.loads(paths[0].read_text())
        self.assertEqual(diagnostic["exception_type"], "KeyError")
        self.assertEqual(diagnostic["frames"][-1]["function"], "missing_source")
        self.assertIn("KeyError: 'source_id'", diagnostic["traceback"])
        self.assertIn(str(paths[0]), wrapped.reason)

    def test_diagnostic_write_failure_does_not_hide_original_exception(self):
        for failure in (OSError("Disk unavailable"), RUNNER.IntegrityError("Diagnostic already exists")):
            with self.subTest(failure=type(failure).__name__), mock.patch.object(RUNNER, "write_json", side_effect=failure):
                wrapped = RUNNER.unexpected_generator_error(self.run, KeyError("source_id"))
            self.assertIn("KeyError: 'source_id'", wrapped.reason)
            self.assertIn("Diagnostic could not be saved", wrapped.reason)
            self.assertIn(str(failure), wrapped.reason)

    def test_failure_report_accepts_builds_outside_the_installation(self):
        build = self.run / "projection/web/dist/index.html"
        build.parent.mkdir(parents=True)
        build.write_text("Diagnostic build placeholder")
        output = []
        with mock.patch.object(RUNNER, "ROOT", self.run / "other_installation"):
            RUNNER.print_failure(self.run, RUNNER.CathedralsError("Fixture", "A concrete failure"), output.append)
        self.assertIn(str(build.parent), "\n".join(output))

    def test_secondary_finalization_error_is_reported_with_original_error(self):
        state = self.run / "state/run-state.json"
        state.parent.mkdir()
        state.write_text("{}")
        output = []
        with mock.patch.object(RUNNER, "snapshot_root", return_value=RUNNER.ROOT), mock.patch.object(RUNNER, "ensure_runtime_layout"), mock.patch.object(RUNNER, "choose_resume", return_value=self.run), mock.patch.object(
                RUNNER, "ensure_resume_ready", side_effect=KeyError("source_id")), mock.patch.object(
                RUNNER, "finalize_failure", side_effect=RuntimeError("Cannot finalize")):
            status = RUNNER.main([], output_fn=output.append, transport=mock.Mock(side_effect=AssertionError("Provider forbidden")))
        self.assertEqual(status, 1)
        report = "\n".join(output)
        self.assertIn("KeyError: 'source_id'", report)
        self.assertIn("Failure finalization also failed: RuntimeError: Cannot finalize", report)


if __name__ == "__main__":
    unittest.main()
