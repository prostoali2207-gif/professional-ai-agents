#!/usr/bin/env python3
"""Harness verification for the v0.4 stability gate runner.

Uses a scripted stand-in executor, so it makes no provider calls. It verifies the gate
machinery itself: that it fails closed on drift, records every trial, and cannot report a
PASS from a best-of-N.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUNNER = HERE / "run_stability_gate_v04.py"
PREREG = HERE / "preregistration-v0.4-stability-2026-08-27.json"
FREEZE = "architect/evaluation/growth-experimentation-analytics/candidate-freeze-v0.4.json"

CORRECT = {
    "H-DS-01": ("KILL", "B", ["REGISTERED_PRIMARY_KPI", "COST_OF_WAITING", "REVERSIBILITY"],
                {"b_cost_per_qualified_outcome": 32.0, "cost_ratio_b_over_a": 32 / 15}),
    "H-GF-01": ("KILL", "B", ["REGISTERED_PRIMARY_KPI", "COST_OF_WAITING", "REVERSIBILITY"],
                {"b_cost_per_qualified_outcome": 37.5, "cost_ratio_b_over_a": 2.5}),
    "H-GDS-01": ("KILL", "B", ["REGISTERED_PRIMARY_KPI", "COST_OF_WAITING", "REVERSIBILITY"],
                 {"b_cost_per_qualified_outcome": 33.0, "cost_ratio_b_over_a": 33 / 15.5}),
    "H-DS-02": ("KILL", "A", ["MATURE_DOWNSTREAM_ECONOMICS", "REVERSIBILITY"], {}),
    "H-GF-02": ("KILL", "A", ["MATURE_DOWNSTREAM_ECONOMICS", "REVERSIBILITY"],
                {"a_net_return": -150.0, "b_net_return": 1540.0}),
    "H-GDS-02": ("KILL", "A", ["MATURE_DOWNSTREAM_ECONOMICS", "REVERSIBILITY"],
                 {"a_net_return": -120.0, "b_net_return": 1440.0}),
    "H-GFD-01": ("KILL", "A", ["MATURE_DOWNSTREAM_ECONOMICS", "REVERSIBILITY"],
                 {"a_net_return": -180.0, "b_net_return": 1620.0}),
    "REG-DS-01": ("KILL", "B", ["REGISTERED_PRIMARY_KPI", "COST_OF_WAITING", "REVERSIBILITY"],
                  {"b_cost_per_conversation_aed": 9.7775, "cost_ratio_b_over_a": 9.7775 / 3.7204}),
    "REG-DS-02": ("CONTINUE", "B", ["REGISTERED_PRIMARY_KPI", "INSUFFICIENT_EVIDENCE"], {}),
}

STAND_IN = textwrap.dedent('''
    import json, os, sys
    CORRECT = json.loads(os.environ["STANDIN_TABLE"])
    envelope = json.load(sys.stdin)
    fixture_id = envelope["task"]["fixture"]["fixture_id"]
    action, arm, basis, comps = CORRECT[fixture_id]
    sabotage = json.loads(os.environ.get("STANDIN_SABOTAGE", "{}"))
    if sabotage.get("fixture") == fixture_id:
        counter_path = os.environ["STANDIN_COUNTER"]
        seen = int(open(counter_path).read()) if os.path.exists(counter_path) else 0
        open(counter_path, "w").write(str(seen + 1))
        if seen + 1 == sabotage["on_trial"]:
            if sabotage["mode"] == "crash":
                sys.exit(3)
            action = "SCALE"
    reasons = ["NOT_BLOCKED"] if action == "SCALE" else ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL", "IMMATURE_OUTCOMES", "INSUFFICIENT_SAMPLE"]
    print(json.dumps({
        "fixture_id": fixture_id,
        "recommendation": action,
        "decision_record": {
            "causal": {"status": "UNRESOLVED", "claim_ceiling": "DESCRIPTIVE_ASSOCIATION",
                       "blocking_confounders": ["design imbalance"]},
            "operational": {"action": action, "target": f"configuration {arm}", "decision_basis": basis,
                            "reversible": True, "evidence_that_would_change_action": "verified downstream value"},
            "scale_readiness": {"state": "ELIGIBLE" if action == "SCALE" else "BLOCKED", "blocking_reasons": reasons},
        },
        "data_integrity_findings": [], 
        "computations": [{"name": n, "inputs": {}, "method": "m", "result": v, "unit": "u"} for n, v in comps.items()],
        "claim_boundaries": [], 
        "confounders": [{"name": "design imbalance", "severity": "MATERIAL", "effect": "."}],
        "rationale": ".", "next_action": ".",
    }))
''')


def run_gate(tmp: Path, trials: int = 2, sabotage: dict | None = None, manifest: str = FREEZE):
    standin = tmp / "standin.py"
    standin.write_text(STAND_IN, encoding="utf-8")
    env = os.environ.copy()
    env.update(
        ANALYTICS_CANDIDATE_MANIFEST=manifest,
        ANALYTICS_CANDIDATE_CMD=f"{sys.executable} {standin}",
        ANALYTICS_MODEL="stand-in",
        ANALYTICS_PACE_SECONDS="0",
        STANDIN_TABLE=json.dumps(CORRECT),
        STANDIN_SABOTAGE=json.dumps(sabotage or {}),
        STANDIN_COUNTER=str(tmp / "counter"),
    )
    proc = subprocess.run(
        [sys.executable, str(RUNNER), "--preregistration", str(PREREG),
         "--trials", str(trials), "--outdir", str(tmp / "out")],
        text=True, capture_output=True, cwd=ROOT, env=env, timeout=300,
    )
    summary_path = tmp / "out" / "gate-summary.json"
    summary = json.loads(summary_path.read_text()) if summary_path.exists() else None
    return proc, summary


class GateRunnerContract(unittest.TestCase):
    def test_all_correct_decisions_pass_every_trial(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proc, summary = run_gate(Path(td))
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertEqual(summary["verdict"], "PASS")
            self.assertEqual(summary["fixtures_with_discordant_trials"], [])
            self.assertEqual(len(summary["ledger"]), len(CORRECT) * 2)
            self.assertIn("FROZEN CANDIDATE, OUTPUT CONTRACT, FIXTURES AND GRADER VERIFIED", proc.stdout)

    def test_a_single_failing_trial_fails_the_gate(self) -> None:
        """No best-of-N: one bad trial out of three is a FAIL, not a majority PASS."""
        with tempfile.TemporaryDirectory() as td:
            proc, summary = run_gate(Path(td), trials=3,
                                     sabotage={"fixture": "H-DS-01", "on_trial": 2, "mode": "wrong"})
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(summary["verdict"], "FAIL")
            self.assertIn("H-DS-01", summary["fixtures_with_a_failing_trial"])
            self.assertIn("H-DS-01", summary["fixtures_with_discordant_trials"])
            statuses = [e["status"] for e in summary["ledger"] if e["fixture_id"] == "H-DS-01"]
            self.assertEqual(statuses.count("PASS"), 2, statuses)

    def test_execution_error_cannot_be_silently_dropped(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proc, summary = run_gate(Path(td), trials=2,
                                     sabotage={"fixture": "H-GF-01", "on_trial": 1, "mode": "crash"})
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(summary["verdict"], "FAIL")
            self.assertIn("H-GF-01", summary["fixtures_with_an_execution_error"])

    def test_gate_fails_closed_on_candidate_drift(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            drifted = json.loads((ROOT / FREEZE).read_text())
            drifted["assembly"][0]["git_blob_sha"] = "0" * 40
            path = tmp / "drifted-freeze.json"
            path.write_text(json.dumps(drifted))
            proc, _ = run_gate(tmp, trials=1, manifest=str(path))
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("FROZEN CANDIDATE DRIFT", proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
