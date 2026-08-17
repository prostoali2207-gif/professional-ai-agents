import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "architect/library/cores/video-editing-post-production/0.1.0"
CASES = Path(__file__).with_name("semantic_cases.json")


class VideoEditingCandidateContract(unittest.TestCase):
    def test_candidate_files_exist(self):
        for name in ("professional-model.md", "evidence-and-reuse.md", "manifest.json"):
            self.assertTrue((CORE / name).is_file(), name)

    def test_manifest_is_explicitly_unqualified(self):
        manifest = json.loads((CORE / "manifest.json").read_text())
        self.assertEqual(manifest["id"], "video-editing-post-production")
        self.assertEqual(manifest["lifecycle"], "candidate")
        self.assertEqual(manifest["qualification_refs"], [])
        self.assertRegex(manifest["artifact"]["content_digest"], r"^sha256:[a-f0-9]{64}$")

    def test_catalog_registers_candidate_without_qualification(self):
        catalog = json.loads((ROOT / "architect/library/catalog.json").read_text())
        entry = next(item for item in catalog["entries"] if item["id"] == "video-editing-post-production")
        manifest = json.loads((CORE / "manifest.json").read_text())
        self.assertEqual(entry["lifecycle"], "candidate")
        self.assertEqual(entry["qualification_refs"], [])
        self.assertEqual(entry["artifact_digest"], manifest["artifact"]["content_digest"])

    def test_critical_professional_controls_are_reachable(self):
        model = (CORE / "professional-model.md").read_text()
        for phrase in (
            "truth preservation", "Artifact-first QC", "If the runtime can only write instructions",
            "Fast is not synonymous with engaging", "final creative/fact approval"
        ):
            self.assertIn(phrase, model)

    def test_frozen_case_constructs_are_unique_and_complete(self):
        cases = json.loads(CASES.read_text())
        self.assertEqual(len(cases), 12)
        self.assertEqual(len({case["id"] for case in cases}), 12)
        for case in cases:
            self.assertTrue(case["facts"])
            self.assertTrue(case["allowed_actions"])
            self.assertTrue(case["forbidden_actions"])
            self.assertTrue(case["required_flags"])

    def test_release_gate_is_bounded_and_has_positive_control(self):
        runner = (Path(__file__).with_name("run_semantic_gate.py")).read_text()
        workflow = (ROOT / ".github/workflows/video-editing-post-production-qualification.yml").read_text()
        cases = json.loads(CASES.read_text())
        positive = next(case for case in cases if case["id"] == "VE-S12")
        self.assertEqual(positive["allowed_actions"], ["PROCEED_TO_FINISHING"])
        self.assertIn("single gate invocation exceeds 3-call budget", runner)
        self.assertIn("exactly 3 model calls", workflow)
        self.assertIn("application_retries", runner)


if __name__ == "__main__":
    unittest.main()
