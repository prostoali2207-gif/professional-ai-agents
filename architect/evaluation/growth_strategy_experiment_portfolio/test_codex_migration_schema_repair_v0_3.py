from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import codex_judge_adapter_v0_1 as judge


def assert_strict_required(test: unittest.TestCase, schema: dict) -> None:
    if schema.get("type") == "object":
        properties = schema.get("properties") or {}
        test.assertEqual(set(schema.get("required") or []), set(properties))
        test.assertFalse(schema.get("additionalProperties", True))
        for value in properties.values():
            assert_strict_required(test, value)
    if schema.get("type") == "array":
        assert_strict_required(test, schema["items"])


class CodexMigrationSchemaRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repair = json.loads((HERE / "qualification-codex-migration-schema-repair-v0.3.json").read_text(encoding="utf-8"))
        cls.base = json.loads((HERE / "qualification-codex-migration-v0.1.json").read_text(encoding="utf-8"))

    def test_calibration_schema_omits_pair_results_and_is_strict(self):
        schema = judge.schema("calibration")
        self.assertEqual(set(schema["properties"]), {"results"})
        self.assertEqual(schema["required"], ["results"])
        assert_strict_required(self, schema)

    def test_heldout_schema_retains_pair_results_and_is_strict(self):
        schema = judge.schema("heldout")
        self.assertEqual(set(schema["properties"]), {"results", "pair_results"})
        self.assertEqual(set(schema["required"]), {"results", "pair_results"})
        assert_strict_required(self, schema)

    def test_repair_preserves_candidate_and_release_invariants(self):
        unchanged = self.repair["unchanged"]
        self.assertEqual(unchanged["strategist_candidate_commit"], self.base["candidate"]["commit"])
        self.assertEqual(unchanged["strategist_candidate_digest"], self.base["candidate"]["digest"])
        for key in ("candidate_content_changed", "professional_constructs_changed", "thresholds_changed", "hard_fails_changed", "release_criteria_changed", "scored_qualification_authorized"):
            self.assertFalse(unchanged[key])

    def test_transport_observability_and_bounded_retry_are_inherited(self):
        inherited = self.repair["inherited_controls"]
        self.assertEqual(inherited["sanitized_failure_envelope"], "UNCHANGED")
        self.assertEqual(inherited["shared_retry_budget"], 1)
        self.assertEqual(inherited["retry_eligible_only_for"], "TRANSIENT_TRANSPORT")
        self.assertEqual(inherited["candidate_canary_retry_count"], 0)
        self.assertEqual(self.repair["pre_run_budget"]["scored_model_calls_authorized"], 0)


if __name__ == "__main__":
    unittest.main()
