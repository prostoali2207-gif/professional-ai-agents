#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("qre_readiness_candidate", HERE / "validate_readiness_report.py")
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)
SCHEMA = HERE / "readiness-report.schema.json"


def base_report():
    return {
        "version": "0.1",
        "execution_chain": {"cycle": "candidate-v0.1", "stage": "public-development", "evaluator_transport_path": "deterministic->representative-canary->scored", "technical_repair_consumed": False, "eligible_retry_remaining": True},
        "identities": {"candidate": "sha256:candidate", "evaluator": "eval-v1", "runtime": "runtime-v1"},
        "mechanical_evidence": {"static_preflight": "PASS", "runtime_contract": "PASS", "fault_injection": "PASS", "artifact_identity": "PASS"},
        "canary": {"required": False, "representativeness_assessed": False, "evidence_status": "NOT_APPLICABLE", "rationale": "No irreducible live runtime uncertainty remains."},
        "budget": {"max_candidate_calls": 12, "max_judge_calls": 12, "max_retries": 1, "max_wall_clock_seconds": 1800, "stop_condition": "Stop on any P0 infrastructure defect or exhausted chain budget."},
        "privacy": {"heldout_material": False, "provider_storage_required": False, "provider_storage_authorized": False},
        "risks": [{"id": "optional-observability-improvement", "severity": "P2", "status": "ACCEPTED_BACKLOG", "deterministically_detectable": True, "evidence": "Does not affect current evidence validity."}],
        "decision": {"verdict": "GO", "reason": "All release-critical infrastructure gates passed."}
    }


class CandidateReadinessGuardTests(unittest.TestCase):
    def test_clean_go_passes(self):
        self.assertEqual(mod.validate(base_report(), SCHEMA), [])

    def test_open_p0_blocks_go(self):
        r = base_report()
        r["risks"].append({"id": "missing-secret-check", "severity": "P0", "status": "OPEN", "deterministically_detectable": True, "evidence": "Credential path not validated."})
        with self.assertRaises(mod.ReadinessError):
            mod.validate(r, SCHEMA)

    def test_failed_mechanical_gate_blocks_go(self):
        r = base_report(); r["mechanical_evidence"]["runtime_contract"] = "FAIL"
        with self.assertRaises(mod.ReadinessError):
            mod.validate(r, SCHEMA)

    def test_required_canary_must_be_assessed_and_pass(self):
        r = base_report(); r["canary"] = {"required": True, "representativeness_assessed": False, "evidence_status": "NOT_RUN", "rationale": ""}
        with self.assertRaises(mod.ReadinessError):
            mod.validate(r, SCHEMA)

    def test_assessed_canary_passes_mechanical_guard(self):
        r = base_report(); r["canary"] = {"required": True, "representativeness_assessed": True, "evidence_status": "PASS", "rationale": "Professional review established failure-relevant equivalence."}
        self.assertEqual(mod.validate(r, SCHEMA), [])

    def test_unauthorized_storage_blocks_go(self):
        r = base_report(); r["privacy"] = {"heldout_material": True, "provider_storage_required": True, "provider_storage_authorized": False}
        with self.assertRaises(mod.ReadinessError):
            mod.validate(r, SCHEMA)

    def test_exhausted_chain_blocks_go(self):
        r = base_report(); r["execution_chain"]["technical_repair_consumed"] = True; r["execution_chain"]["eligible_retry_remaining"] = False
        with self.assertRaises(mod.ReadinessError):
            mod.validate(r, SCHEMA)

    def test_open_p1_does_not_automatically_block_go(self):
        r = base_report(); r["risks"].append({"id": "bounded-residual-risk", "severity": "P1", "status": "OPEN", "deterministically_detectable": False, "evidence": "Professional owner documented why it does not threaten this claim."})
        self.assertEqual(mod.validate(r, SCHEMA), [])

    def test_negative_budget_rejected_by_schema(self):
        r = base_report(); r["budget"]["max_candidate_calls"] = -1
        with self.assertRaises(mod.ReadinessError):
            mod.validate(r, SCHEMA)


if __name__ == "__main__":
    unittest.main()
