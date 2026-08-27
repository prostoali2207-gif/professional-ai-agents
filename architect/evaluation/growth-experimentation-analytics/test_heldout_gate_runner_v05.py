#!/usr/bin/env python3
"""Harness verification for the v0.5 held-out gate runner. No provider calls.

Drives the whole pipeline with a scripted stand-in so the gate is known to work before any
quota is spent: it generates from the preregistered seed, fails closed on drift, records
every trial, catches the wrong-arm P0, and cannot report PASS from a best-of-N.
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
RUNNER = HERE / "run_heldout_gate_v05.py"
PREREG = HERE / "preregistration-v0.5-heldout-2026-08-27.json"
FREEZE = "architect/evaluation/growth-experimentation-analytics/candidate-freeze-v0.5.json"

STAND_IN = textwrap.dedent('''
    import importlib.util, json, os, sys
    D = os.environ["REPO_ROOT"] + "/architect/evaluation/growth-experimentation-analytics/"
    spec = importlib.util.spec_from_file_location("g", D + "heldout_generator_v05.py")
    g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
    _, oracle = g.generate(int(os.environ["SEED"]), int(os.environ["PER_FAMILY"]))
    env = json.load(sys.stdin)
    fid = env["task"]["fixture"]["fixture_id"]
    e = oracle["expectations"][fid]
    mode = os.environ.get("MODE", "correct")
    action, target = e["action_in"][0], e["target"]
    if mode == "wrong_arm" and e["family"] == "UPSTREAM_DOWNSTREAM_CONFLICT":
        arms = env["task"]["fixture"]["case"]["arms"]
        target = next(a for a in arms if a != target and a != "experiment")
    if mode == "flake_once":
        counter = os.environ["COUNTER"]
        seen = int(open(counter).read()) if os.path.exists(counter) else 0
        open(counter, "w").write(str(seen + 1))
        if seen == 0:
            target = "not_an_arm"
    identified = "IDENTIFIED" in e.get("causal_status_in", [])
    state = e.get("scale_state", "BLOCKED")
    print(json.dumps({
      "fixture_id": fid, "recommendation": action,
      "decision_record": {
        "causal": {"status": "IDENTIFIED" if identified else "UNRESOLVED",
                   "claim_ceiling": e.get("max_claim_ceiling", "DESCRIPTIVE_ASSOCIATION"),
                   "blocking_confounders": [] if identified else ["design imbalance"]},
        "operational": {"action": action, "target": target,
                        "decisive_metric": e["decisive_metric_in"][0],
                        "decision_basis": list({*e.get("basis_required", []), "REVERSIBILITY"}),
                        "reversible": True, "evidence_that_would_change_action": "x"},
        "scale_readiness": {"state": state,
                            "blocking_reasons": [e["scale_reasons_any"][0]] if state == "BLOCKED" else ["NOT_BLOCKED"]}},
      "data_integrity_findings": [],
      "computations": [{"name": n, "inputs": {}, "method": "m", "result": v[0], "unit": "u"}
                       for n, v in e.get("computations", {}).items()],
      "claim_boundaries": [],
      "confounders": [] if identified else [{"name": "design imbalance", "severity": "MATERIAL", "effect": "."}],
      "rationale": ".", "next_action": "."}))
''')


def run_gate(tmp: Path, mode: str = "correct", trials: int = 2, manifest: str = FREEZE):
    prereg = json.loads(PREREG.read_text())
    standin = tmp / "standin.py"
    standin.write_text(STAND_IN, encoding="utf-8")
    env = os.environ.copy()
    env.update(REPO_ROOT=str(ROOT), SEED=str(prereg["heldout_seed"]),
               PER_FAMILY=str(prereg["per_family"]), MODE=mode, COUNTER=str(tmp / "counter"),
               ANALYTICS_CANDIDATE_MANIFEST=manifest,
               ANALYTICS_CANDIDATE_CMD=f"{sys.executable} {standin}",
               ANALYTICS_MODEL="stand-in", ANALYTICS_PACE_SECONDS="0")
    proc = subprocess.run(
        [sys.executable, str(RUNNER), "--preregistration", str(PREREG),
         "--trials", str(trials), "--outdir", str(tmp / "out")],
        text=True, capture_output=True, cwd=ROOT, env=env, timeout=600)
    path = tmp / "out" / "gate-summary.json"
    return proc, (json.loads(path.read_text()) if path.exists() else None)


class HeldoutGateRunner(unittest.TestCase):
    def test_oracle_correct_decisions_pass_every_trial(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proc, summary = run_gate(Path(td))
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertEqual(summary["verdict"], "PASS")
            self.assertEqual(len(summary["ledger"]), 8 * 2)
            self.assertIn("GENERATOR AND GRADER VERIFIED", proc.stdout)

    def test_wrong_arm_on_the_conflict_family_fails(self) -> None:
        """The H-GDS-02 P0, at gate level."""
        with tempfile.TemporaryDirectory() as td:
            proc, summary = run_gate(Path(td), mode="wrong_arm")
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(summary["verdict"], "FAIL")
            failing = set(summary["fixtures_with_a_failing_trial"])
            self.assertTrue({"HO-UDC-01", "HO-UDC-02"}.issubset(failing), failing)

    def test_one_bad_trial_is_not_outvoted(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proc, summary = run_gate(Path(td), mode="flake_once", trials=3)
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(summary["verdict"], "FAIL")
            self.assertTrue(summary["fixtures_with_discordant_trials"])

    def test_fails_closed_on_candidate_drift(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            drifted = json.loads((ROOT / FREEZE).read_text())
            drifted["assembly"][0]["git_blob_sha"] = "0" * 40
            path = tmp / "drifted.json"
            path.write_text(json.dumps(drifted))
            proc, _ = run_gate(tmp, trials=1, manifest=str(path))
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("FROZEN CANDIDATE DRIFT", proc.stdout + proc.stderr)

    def test_culprit_arm_differs_across_the_two_gate_cases(self) -> None:
        """If both conflict cases put the culprit in the same position, the gate could be
        passed by anchoring rather than by applying metric precedence."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("g", HERE / "heldout_generator_v05.py")
        gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)
        prereg = json.loads(PREREG.read_text())
        _, oracle = gen.generate(prereg["heldout_seed"], prereg["per_family"])
        targets = [e["target"] for e in oracle["expectations"].values()
                   if e["family"] == "UPSTREAM_DOWNSTREAM_CONFLICT"]
        self.assertEqual(len(set(targets)), 2, f"culprit position not varied at the gate seed: {targets}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
