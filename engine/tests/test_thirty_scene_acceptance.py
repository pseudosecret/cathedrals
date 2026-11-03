"""Exercise the bounded compiler and scoped context through a 30-scene publication."""
import unittest
from test_bounded_execution import POLICY
import test_reference_resolution as fixtures


class ThirtySceneAcceptanceTests(unittest.TestCase):
    scene_count = 30
    policy = POLICY
    setUp = fixtures.ReferenceResolutionTests.setUp
    test_complete_work = fixtures.ReferenceResolutionTests.test_full_twenty_scene_run_repairs_references_and_reaches_ready_without_resume
