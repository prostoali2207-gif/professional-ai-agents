from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import codex_canary_gate_v0_1 as gate
import codex_judge_adapter_v0_1 as judge
import sealed_runner_codex_v0_1 as runner


class CodexMigrationRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repair = json.loads((HERE / "qualification-codex-migration-repair-v0.2.json").read_text(encoding="utf-8"))
        cls.base = json.loads((HERE / "qualification-codex-migration-v0.1.json").read_text(encoding="utf-8"))

    def test_repair_preserves_candidate_construct_and_release_invariants(self):
        unchanged = self.repair["unchanged"]
        self.assertEqual(unchanged["strategist_candidate_commit"], self.base["candidate"]["commit"])
        self.assertEqual(unchanged["strategist_candidate_digest"], self.base["candidate"]["digest"])
        for key in ("candidate_content_changed", "professional_constructs_changed", "thresholds_changed", "hard_fails_changed", "release_criteria_changed", "scored_qualification_authorized"):
            self.assertFalse(unchanged[key])

    def test_retry_budget_is_shared_bounded_and_excludes_quota_and_content(self):
        policy = self.repair["bounded_retry_policy"]
        self.assertEqual(policy["maximum_additional_calls"], 1)
        self.assertEqual(policy["maximum_calibration_calls"], 3)
        self.assertEqual(policy["candidate_canary_retry_count"], 0)
        self.assertIn("quota or rate limit", policy["ineligible_signals"])
        self.assertIn("calibration/content mismatch", policy["ineligible_signals"])
        self.assertEqual(self.repair["pre_run_budget"]["maximum_model_calls"], 4)
        self.assertEqual(self.repair["pre_run_budget"]["scored_model_calls_authorized"], 0)

    def test_failure_envelope_is_structured_bounded_and_sanitized(self):
        raw = "Bearer abc123\nC:\\Users\\person\\secret.txt\napi_key=topsecret"
        clean = judge.sanitize_tail(raw)
        self.assertNotIn("abc123", clean)
        self.assertNotIn("topsecret", clean)
        self.assertNotIn("C:\\Users", clean)
        self.assertLessEqual(len(clean), 1600)
        self.assertEqual(judge.failure_classification("", "HTTP 503 temporarily unavailable"), "TRANSIENT_TRANSPORT")
        self.assertEqual(judge.failure_classification("", "HTTP 429 quota"), "NONRETRYABLE_TECHNICAL")

    def test_runner_preserves_adapter_failure_envelope(self):
        envelope = {"stage": "codex_exec", "returncode": 1, "classification": "UNKNOWN_TECHNICAL", "stdout_tail": "x", "stderr_tail": "y"}
        completed = subprocess.CompletedProcess(["judge"], 2, json.dumps({"status": "runtime_error", "failure_envelope": envelope}), "")
        with mock.patch.object(runner.subprocess, "run", return_value=completed):
            with self.assertRaises(runner.IsolatedRuntimeError) as caught:
                runner.invoke("judge", {"mode": "calibration"}, 1)
        self.assertEqual(caught.exception.envelope, envelope)

    def test_only_transient_transport_gets_one_shared_retry(self):
        transient = runner.IsolatedRuntimeError(2, {"classification": "TRANSIENT_TRANSPORT"})
        retry = {"remaining": 1}
        attempts = []
        with mock.patch.object(gate.runner, "calibrate", side_effect=[transient, True]), mock.patch.object(gate.time, "sleep"):
            gate.calibrate_with_bounded_retry("judge", "gpt-5.6-sol", retry, attempts)
        self.assertEqual(retry["remaining"], 0)
        self.assertEqual([row["outcome"] for row in attempts], ["TECHNICAL_FAILURE", "PASS"])

        retry = {"remaining": 1}
        attempts = []
        unknown = runner.IsolatedRuntimeError(2, {"classification": "UNKNOWN_TECHNICAL"})
        with mock.patch.object(gate.runner, "calibrate", side_effect=unknown):
            with self.assertRaises(RuntimeError):
                gate.calibrate_with_bounded_retry("judge", "gpt-5.6-sol", retry, attempts)
        self.assertEqual(retry["remaining"], 1)

    def test_gate_order_is_calibration_then_judge_isolation_then_candidate(self):
        source = (HERE / "codex_canary_gate_v0_1.py").read_text(encoding="utf-8")
        calibration = source.index("calibrate_with_bounded_retry(judge_command")
        isolation = source.index('record["judge_isolation"] = verify_judge_isolation')
        candidate = source.index('proc = run_checked([str(python), str(candidate_adapter)')
        self.assertLess(calibration, isolation)
        self.assertLess(isolation, candidate)
        self.assertNotIn("fixtures.json", source)
        self.assertNotIn("grader.json", source)

    def test_judge_isolation_requires_distinct_threads_and_workspaces(self):
        transports = [
            {"model": "gpt-5.6-sol", "mode": "calibration", "transport": {"thread_id": "a", "workspace_digest": "x", "event_types": ["thread.started", "turn.completed"]}},
            {"model": "gpt-5.6-terra", "mode": "calibration", "transport": {"thread_id": "b", "workspace_digest": "y", "event_types": ["thread.started", "turn.completed"]}},
        ]
        self.assertEqual(gate.verify_judge_isolation(transports)["status"], "PASS")
        transports[1]["transport"]["thread_id"] = "a"
        with self.assertRaises(RuntimeError):
            gate.verify_judge_isolation(transports)


if __name__ == "__main__":
    unittest.main()
