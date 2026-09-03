#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("stage_b_validator", HERE / "validate_calibration_manifest.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)
SCHEMA = HERE / "calibration-manifest.schema.json"


def valid_manifest():
    return {
        "version": "0.1",
        "evaluator_cycle": "qre-v01-independent-stage-b-calibration-r1",
        "candidate": {
            "merge_commit": "faafd25b554bcff2c22c30f8edbf76a895f05298",
            "freeze_record": "ed2e69405209813005ef08b1b4f086e011c3b2c8",
        },
        "independence": {
            "fresh_context": True,
            "candidate_outputs_seen": False,
            "candidate_skill_used_as_authoring_source": False,
            "authored_after_preregistration": True,
        },
        "pack": {
            "case_count": 12,
            "sha256": "a" * 64,
            "hidden_content_committed": False,
            "exact_answer_prose_frozen": False,
        },
        "mechanisms": sorted(mod.REQUIRED_MECHANISMS),
        "reference_levels": sorted(mod.REQUIRED_LEVELS),
        "rubric_dimensions": sorted(mod.REQUIRED_RUBRIC),
        "resources": {
            "candidate_calls": 0,
            "judge_calls": 0,
            "live_provider_calls": 0,
            "metered_api_calls": 0,
            "author_sessions": 1,
            "parallel_model_runs": 0,
        },
        "status": "B1_AUTHORED_NOT_CALIBRATED",
    }


class StageBCalibrationManifestTests(unittest.TestCase):
    def assert_rejected(self, manifest):
        with self.assertRaises(mod.CalibrationManifestError):
            mod.validate(manifest, SCHEMA)

    def test_valid_manifest_passes(self):
        mod.validate(valid_manifest(), SCHEMA)

    def test_missing_go_control_rejected(self):
        m = valid_manifest()
        m["mechanisms"].remove("CORRECT_GO_CONTROL")
        self.assert_rejected(m)

    def test_candidate_outputs_seen_rejected(self):
        m = valid_manifest()
        m["independence"]["candidate_outputs_seen"] = True
        self.assert_rejected(m)

    def test_candidate_skill_as_authoring_source_rejected(self):
        m = valid_manifest()
        m["independence"]["candidate_skill_used_as_authoring_source"] = True
        self.assert_rejected(m)

    def test_hidden_pack_commit_rejected(self):
        m = valid_manifest()
        m["pack"]["hidden_content_committed"] = True
        self.assert_rejected(m)

    def test_too_few_cases_rejected(self):
        m = valid_manifest()
        m["pack"]["case_count"] = 11
        self.assert_rejected(m)

    def test_second_author_session_rejected(self):
        m = valid_manifest()
        m["resources"]["author_sessions"] = 2
        self.assert_rejected(m)

    def test_metered_api_use_rejected(self):
        m = valid_manifest()
        m["resources"]["metered_api_calls"] = 1
        self.assert_rejected(m)

    def test_missing_staff_strong_rejected(self):
        m = valid_manifest()
        m["reference_levels"].remove("STAFF_STRONG")
        self.assert_rejected(m)

    def test_wrong_candidate_identity_rejected(self):
        m = valid_manifest()
        m["candidate"]["merge_commit"] = "0" * 40
        self.assert_rejected(m)


if __name__ == "__main__":
    unittest.main()
