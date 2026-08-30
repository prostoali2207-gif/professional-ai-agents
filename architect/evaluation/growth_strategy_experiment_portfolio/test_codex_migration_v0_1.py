from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


candidate = load_module("codex_candidate_adapter", "codex_candidate_adapter_v0_1.py")
judge = load_module("codex_judge_adapter", "codex_judge_adapter_v0_1.py")
runner = load_module("sealed_runner_codex", "sealed_runner_codex_v0_1.py")


class CodexMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.migration = json.loads((HERE / "qualification-codex-migration-v0.1.json").read_text(encoding="utf-8"))
        cls.source = json.loads((HERE / "qualification-preregistration-v0.1.json").read_text(encoding="utf-8"))

    def test_frozen_candidate_identity_is_unchanged_and_verifiable(self):
        self.assertEqual(self.migration["candidate"]["commit"], self.source["candidate"]["commit"])
        self.assertEqual(self.migration["candidate"]["digest"], self.source["candidate"]["digest"])
        self.assertFalse(self.migration["candidate"]["content_changed"])
        self.assertFalse(self.migration["candidate"]["identity_changed"])
        text = candidate.verify_candidate()
        self.assertIn("Growth Strategy & Experiment Portfolio Practitioner", text)

    def test_construct_thresholds_trials_and_aggregation_are_frozen(self):
        unchanged = self.migration["unchanged"]
        grading = self.source["grading"]
        heldout = self.source["heldout"]
        self.assertEqual(unchanged["families"], heldout["families"])
        self.assertEqual(unchanged["fixture_count"], heldout["fixture_count"])
        self.assertEqual(unchanged["fixtures_per_family"], heldout["per_family"])
        self.assertEqual(unchanged["trial_count_per_fixture"], heldout["trial_count_per_fixture"])
        self.assertEqual(unchanged["professional_failure_retry_count"], heldout["professional_failure_retry_count"])
        thresholds = grading["release_thresholds"]
        for key in (
            "critical_hard_fail_count", "minimum_mean_decision_correctness_per_family",
            "minimum_mean_boundary_integrity_per_family", "minimum_mean_evidence_calibration_per_family",
            "minimum_mean_mechanism_judgment_per_family", "minimum_overall_fixture_pass_rate",
            "contrastive_pairs_must_have_no_unjustified_stance_flip",
        ):
            self.assertEqual(unchanged[key], thresholds[key])
        self.assertEqual(len(self.source["contrastive_requirements"]), unchanged["contrastive_pair_count"])

    def test_only_subscription_runtime_and_no_paid_api_fallback(self):
        changed = self.migration["changed"]
        self.assertEqual(changed["candidate_runtime"]["to"]["provider"], "codex-subscription")
        self.assertTrue(all(j["provider"] == "codex-subscription" for j in changed["judges"]))
        forbidden = set(self.migration["authentication_and_cost"]["forbidden_fallbacks"])
        self.assertTrue({"OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "GROQ_API_KEY"}.issubset(forbidden))
        with mock.patch.dict(os.environ, {
            "OPENAI_API_KEY": "secret", "ANTHROPIC_API_KEY": "secret",
            "GEMINI_API_KEY": "secret", "GROQ_API_KEY": "secret",
            "QUALIFICATION_KEY": "secret", "PATH": os.environ.get("PATH", ""),
        }, clear=True):
            self.assertEqual(set(candidate.sanitized_env()), {"PATH"})
            self.assertEqual(set(judge.sanitized_env()), {"PATH"})
            self.assertEqual(set(runner.candidate_env()), {"PATH"})

    def test_candidate_contract_accepts_task_only_and_declares_no_tools(self):
        contract = candidate.contract(candidate.DEFAULT_MODEL)
        self.assertEqual(contract["tool_protocol"], "none-v1")
        self.assertEqual(contract["state_protocol"], "stateless-v1")
        self.assertEqual(contract["candidate_digest"], self.source["candidate"]["digest"])
        self.assertEqual(self.migration["isolation"]["candidate_input_fields"], ["task"])
        self.assertIn("hidden_reference", self.migration["isolation"]["candidate_forbidden_context"])
        self.assertEqual(contract["required_boundary"], self.migration["isolation"]["candidate_boundary"])

    def test_adapters_use_ephemeral_clean_context_and_read_only_sandbox(self):
        for filename in ("codex_candidate_adapter_v0_1.py", "codex_judge_adapter_v0_1.py"):
            source = (HERE / filename).read_text(encoding="utf-8")
            for flag in ("--ephemeral", "--ignore-user-config", "--ignore-rules", "read-only", "approval_policy"):
                self.assertIn(flag, source)
            self.assertNotIn("urllib.request", source)
            self.assertNotIn("from openai", source)

    def test_calibration_and_call_budget_are_exact_and_fail_closed(self):
        calibration = self.migration["calibration"]
        budget = self.migration["authentication_and_cost"]["future_exact_model_call_budget"]
        self.assertEqual(calibration["public_anchor_count"], 6)
        self.assertEqual(calibration["required_pass_rate_per_judge"], 1.0)
        self.assertTrue(calibration["hidden_or_heldout_calibration_forbidden"])
        self.assertEqual(budget, {
            "candidate_canary": 1, "public_calibration_batches": 2, "scored_candidate": 24,
            "scored_judging_batches": 2, "total": 29,
        })
        self.assertEqual(self.migration["authentication_and_cost"]["authorized_canary_phase_model_calls"], 3)
        self.assertIn("stop", self.migration["exact_release_gate_order"][4].lower())

    def test_contract_command_is_zero_cost(self):
        proc = subprocess.run(
            [sys.executable, str(HERE / "codex_candidate_adapter_v0_1.py"), "--qualification-contract"],
            cwd=ROOT, text=True, capture_output=True, check=True,
        )
        contract = json.loads(proc.stdout)
        self.assertEqual(contract["provider"], "codex-subscription")
        self.assertEqual(contract["required_boundary"], self.migration["isolation"]["candidate_boundary"])

    def test_native_windows_boundary_is_executable_and_fail_closed(self):
        isolation = self.migration["isolation"]
        self.assertEqual(isolation["candidate_boundary"], "native-windows-elevated-sandbox-plus-sensitive-root-deny-acl-v1")
        profile = (HERE / "codex_candidate_permission_profile_v0_1.toml").read_text(encoding="utf-8")
        gate = (HERE / "codex_canary_gate_v0_1.py").read_text(encoding="utf-8")
        self.assertIn('":root" = "deny"', profile)
        self.assertIn("CodexSandboxOffline", gate)
        self.assertIn('"icacls"', gate)
        self.assertIn("finally:", gate)
        self.assertNotIn("fixtures.json", gate)
        self.assertNotIn("grader.json", gate)
        self.assertIn("STRATEGIST_CODEX_CANDIDATE_ROOT", (HERE / "codex_candidate_adapter_v0_1.py").read_text(encoding="utf-8"))

    def test_runner_loads_hidden_grader_only_after_all_candidate_calls(self):
        source = (HERE / "sealed_runner_codex_v0_1.py").read_text(encoding="utf-8")
        candidate_call = source.index("for index, fixture in enumerate(fixtures):")
        grader_load = source.index('grader = json.loads(grader_path.read_text')
        self.assertLess(candidate_call, grader_load)
        for field in self.migration["run_record_required_fields"]:
            self.assertIn(f'"{field}"', source)


if __name__ == "__main__":
    unittest.main()
