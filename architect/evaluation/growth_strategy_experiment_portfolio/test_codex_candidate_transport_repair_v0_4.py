from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import codex_candidate_adapter_v0_1 as adapter
import codex_candidate_canary_gate_v0_4 as gate


class CandidateTransportRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repair = json.loads((HERE / "qualification-codex-candidate-transport-repair-v0.4.json").read_text(encoding="utf-8"))
        cls.base = json.loads((HERE / "qualification-codex-migration-v0.1.json").read_text(encoding="utf-8"))

    def test_sanitizer_removes_credentials_paths_and_protected_inputs(self):
        raw = "Bearer secret-token\nC:\\sealed\\grader.json\napi_key=paid-secret\nPUBLIC TASK CONTENT"
        clean = adapter.sanitize_diagnostic(raw, ("PUBLIC TASK CONTENT",))
        for forbidden in ("secret-token", "C:\\sealed", "paid-secret", "PUBLIC TASK CONTENT"):
            self.assertNotIn(forbidden, clean)
        self.assertIn("<protected-input>", clean)

    def test_structured_schema_failure_envelope_retains_diagnostics_not_raw_lines(self):
        nested = {"error": {"type": "invalid_request_error", "code": "invalid_json_schema", "message": "bad schema", "status": 400}}
        stdout = "not-json-sensitive-line\n" + json.dumps({"type": "thread.started", "thread_id": "thread-secret"}) + "\n" + json.dumps({"type": "error", "message": json.dumps(nested)})
        envelope = adapter.candidate_failure_envelope(1, stdout, "C:\\protected\\file", stage="codex_exec")
        self.assertEqual(envelope["classification"], "LAUNCHER_OR_SCHEMA_CONFIGURATION")
        self.assertEqual(envelope["returncode"], 1)
        self.assertEqual(envelope["stdout_diagnostics"]["unparsed_line_count"], 1)
        serialized = json.dumps(envelope)
        self.assertNotIn("not-json-sensitive-line", serialized)
        self.assertNotIn("thread-secret", serialized)
        self.assertNotIn("C:\\\\protected", serialized)
        self.assertIn("invalid_json_schema", serialized)

    def test_timeout_is_independently_classified_transient(self):
        exc = adapter.CandidateTransportFailure(None, "", "timeout", stage="codex_exec_timeout", forced_classification="TRANSIENT_TRANSPORT")
        self.assertEqual(exc.envelope["classification"], "TRANSIENT_TRANSPORT")
        self.assertIsNone(exc.envelope["returncode"])

    def test_success_path_preserves_frozen_answer_and_transport_contract(self):
        answer = {field: [] for field in adapter.output_schema()["required"]}
        answer["decision"] = "TEST"

        def completed(cmd, **kwargs):
            result_path = Path(cmd[cmd.index("--output-last-message") + 1])
            result_path.write_text(json.dumps(answer), encoding="utf-8")
            stdout = "\n".join((
                json.dumps({"type": "thread.started", "thread_id": "fresh-thread"}),
                json.dumps({"type": "turn.completed", "usage": {"input_tokens": 1, "output_tokens": 1}}),
            ))
            return subprocess.CompletedProcess(cmd, 0, stdout, "")

        with mock.patch.object(adapter.subprocess, "run", side_effect=completed):
            observed, transport = adapter.run_codex("frozen candidate", "public canary", adapter.DEFAULT_MODEL, 1)
        self.assertEqual(observed, answer)
        self.assertEqual(transport["thread_id"], "fresh-thread")

    def test_missing_runtime_output_is_nonretryable_but_counted_as_model_attempt(self):
        completed = subprocess.CompletedProcess(["codex"], 0, json.dumps({"type": "turn.completed"}), "")
        with mock.patch.object(adapter.subprocess, "run", return_value=completed):
            with self.assertRaises(adapter.CandidateTransportFailure) as caught:
                adapter.run_codex("frozen candidate", "public canary", adapter.DEFAULT_MODEL, 1)
        self.assertEqual(caught.exception.envelope["classification"], "RUNTIME_OUTPUT")
        self.assertEqual(caught.exception.envelope["stage"], "codex_exec_output")

    def test_launcher_retains_failure_envelope(self):
        envelope = adapter.candidate_failure_envelope(1, json.dumps({"type": "error", "message": "connection reset"}), "", stage="codex_exec")
        proc = subprocess.CompletedProcess(["candidate"], 2, json.dumps({"status": "runtime_error", "failure_envelope": envelope}), "")
        with mock.patch.object(gate.subprocess, "run", return_value=proc):
            with self.assertRaises(gate.CandidateInvocationFailure) as caught:
                gate.invoke_candidate_once(["candidate"], cwd=HERE, env={}, timeout=1)
        self.assertEqual(caught.exception.envelope["classification"], "TRANSIENT_TRANSPORT")

    def test_only_transient_failure_gets_one_retry_and_original_is_retained(self):
        transient = gate.CandidateInvocationFailure(adapter.candidate_failure_envelope(1, json.dumps({"type": "error", "message": "connection reset"}), "", stage="codex_exec"))
        retry = {"remaining": 1}
        attempts = []
        with mock.patch.object(gate, "invoke_candidate_once", side_effect=[transient, {"status": "completed"}]), mock.patch.object(gate.time, "sleep"):
            gate.run_candidate_with_bounded_retry(["candidate"], cwd=HERE, env={}, retry=retry, attempts=attempts, timeout=1)
        self.assertEqual(retry["remaining"], 0)
        self.assertEqual([row["outcome"] for row in attempts], ["TECHNICAL_FAILURE", "COMPLETED"])
        self.assertIn("failure_envelope", attempts[0])

        nonretryable = gate.CandidateInvocationFailure(adapter.candidate_failure_envelope(1, json.dumps({"type": "error", "message": "invalid_json_schema"}), "", stage="codex_exec"))
        retry = {"remaining": 1}
        attempts = []
        with mock.patch.object(gate, "invoke_candidate_once", side_effect=nonretryable):
            with self.assertRaises(RuntimeError):
                gate.run_candidate_with_bounded_retry(["candidate"], cwd=HERE, env={}, retry=retry, attempts=attempts, timeout=1)
        self.assertEqual(retry["remaining"], 1)

    def test_frozen_candidate_and_release_invariants_are_unchanged(self):
        frozen = self.repair["frozen_invariants"]
        self.assertEqual(frozen["strategist_candidate_commit"], self.base["candidate"]["commit"])
        self.assertEqual(frozen["strategist_candidate_digest"], self.base["candidate"]["digest"])
        for key in ("candidate_identity_or_content_changed", "professional_constructs_or_families_changed", "thresholds_changed", "hard_fails_changed", "release_decision_semantics_changed", "grader_calibration_criteria_changed", "hidden_or_scored_fixture_used", "scored_qualification_authorized"):
            self.assertFalse(frozen[key])

    def test_minimum_gate_has_no_judge_or_scored_entry_point(self):
        source = (HERE / "codex_candidate_canary_gate_v0_4.py").read_text(encoding="utf-8")
        self.assertNotIn("calibrate(", source)
        self.assertNotIn("fixtures.json", source)
        self.assertNotIn("grader.json", source)
        self.assertNotIn("--pack-dir", source)
        self.assertLess(source.rindex("isolation_probe("), source.rindex("run_candidate_with_bounded_retry("))


if __name__ == "__main__":
    unittest.main()
