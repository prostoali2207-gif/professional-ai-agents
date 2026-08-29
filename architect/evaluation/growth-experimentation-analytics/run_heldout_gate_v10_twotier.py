#!/usr/bin/env python3
"""Preregistered held-out gate runner, two-tier criterion with an INVALID class.

Same execution loop as `run_heldout_gate_v07.py`: it generates the held-out cases from the
preregistered seed at run time, executes k trials per case, and grades each against the
generator's oracle with the frozen grader. The executor receives one candidate-facing fixture at
a time and never the expectations. Every trial is recorded. There is no best-of-N and no retry.

What differs is only the verdict arithmetic, per the stability-criterion audit of 2026-08-31:

  * every recorded trial is classified by `trial_outcome_classifier.py` -- a frozen, pure,
    total function of the failure text alone;
  * **INVALID** (provider transport/HTTP failure, unusable envelope, harness misconfiguration)
    means no candidate output exists. Any INVALID trial voids the whole gate: the verdict is
    INVALID, never PASS and never FAIL, and the seed is preserved;
  * **TIER1** (professional judgment) has zero tolerance across the whole gate;
  * **TIER2** (output is not a valid instance of the frozen contract) is capped per fixture and
    in total, and is never counted as a judgment PASS.

Nothing about the candidate, the professional model, the grader, the generator, the fixtures or
the output contract is changed by this file. It is measurement arithmetic only.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ADAPTER = HERE / "adapters" / "stdio_candidate_adapter.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def blob(path: str) -> str:
    return subprocess.check_output(["git", "hash-object", path], text=True, cwd=ROOT).strip()


def verify_frozen(prereg: dict[str, Any], freeze: dict[str, Any]) -> None:
    for component in freeze["assembly"]:
        actual = blob(component["path"])
        if actual != component["git_blob_sha"]:
            raise SystemExit(f"FROZEN CANDIDATE DRIFT: {component['path']} "
                             f"{actual} != {component['git_blob_sha']}")
    if blob(freeze["output_contract_path"]) != freeze["output_contract_git_blob_sha"]:
        raise SystemExit(f"OUTPUT CONTRACT DRIFT: {freeze['output_contract_path']}")
    if prereg["candidate_assembly_digest"] != freeze["assembly_digest"]:
        raise SystemExit("PREREGISTRATION DIGEST MISMATCH")
    # Generator, grader, classifier and this runner are all bound by the preregistration, so a
    # post-hoc edit to the measuring apparatus cannot pass unnoticed.
    for key in ("generator", "grader", "classifier", "runner"):
        ref = prereg[key]
        if blob(ref["path"]) != ref["git_blob_sha"]:
            raise SystemExit(f"{key.upper()} DRIFT: {ref['path']} was edited after preregistration")
    print("FROZEN CANDIDATE, OUTPUT CONTRACT, GENERATOR, GRADER, CLASSIFIER AND RUNNER VERIFIED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preregistration", required=True)
    parser.add_argument("--trials", type=int, default=None)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--pace-seconds", type=float,
                        default=float(os.environ.get("ANALYTICS_PACE_SECONDS", "3")))
    args = parser.parse_args()

    prereg = json.loads(Path(args.preregistration).read_text(encoding="utf-8"))
    freeze = json.loads((ROOT / os.environ["ANALYTICS_CANDIDATE_MANIFEST"]).read_text(encoding="utf-8"))
    verify_frozen(prereg, freeze)

    generator = load_module("gen", ROOT / prereg["generator"]["path"])
    grader = load_module("grader", ROOT / prereg["grader"]["path"])
    classifier = load_module("classifier", ROOT / prereg["classifier"]["path"])

    if classifier.RULES_DIGEST != prereg["tier_map_digest"]:
        raise SystemExit(f"TIER MAP DRIFT: {classifier.RULES_DIGEST} != {prereg['tier_map_digest']}")

    contract_path = freeze.get("output_contract_path")
    contract = json.loads((ROOT / contract_path).read_text(encoding="utf-8")) if contract_path else None
    suite, oracle = generator.generate(prereg["heldout_seed"], prereg["per_family"])
    expectations = oracle["expectations"]
    fixtures = {f["fixture_id"]: f for f in suite["fixtures"]}
    trials = args.trials or int(prereg["trials_per_fixture"])
    cap_fixture = int(prereg["tier2_per_fixture_cap"])
    cap_total = int(prereg["tier2_total_cap"])

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "heldout-cases.json").write_text(json.dumps(suite, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(fixtures)} held-out cases from preregistered seed {prereg['heldout_seed']}")
    print(f"criterion: k={trials}, tier1=0, tier2 <= {cap_fixture}/fixture and <= {cap_total} total, "
          f"any INVALID voids the gate")
    print(f"tier map: {classifier.RULES_DIGEST}\n")

    ledger: list[dict[str, Any]] = []
    for fixture_id, fixture in fixtures.items():
        for trial in range(1, trials + 1):
            entry: dict[str, Any] = {"fixture_id": fixture_id, "trial": trial,
                                     "family": expectations[fixture_id]["family"]}
            proc = subprocess.run(
                [sys.executable, str(ADAPTER)],
                input=json.dumps(fixture, ensure_ascii=False),
                text=True, capture_output=True, cwd=ROOT, env=os.environ.copy(), timeout=300,
            )
            if proc.returncode != 0:
                detail = (proc.stderr or "").strip()[-600:]
                outcome = classifier.classify_trial("EXECUTION_ERROR", detail=detail)
                entry.update(status="EXECUTION_ERROR", detail=detail, outcome=outcome)
                ledger.append(entry)
                print(f"  {fixture_id} trial {trial}: {outcome:8} {detail or '(no stderr)'}")
                time.sleep(args.pace_seconds)
                continue

            (outdir / f"{fixture_id}-t{trial}.json").write_text(proc.stdout, encoding="utf-8")
            try:
                result = json.loads(proc.stdout)
            except json.JSONDecodeError:
                failures = ["candidate returned non-JSON"]
                outcome = classifier.classify_trial("FAIL", failures=failures)
                entry.update(status="FAIL", failures=failures, outcome=outcome)
                ledger.append(entry)
                print(f"  {fixture_id} trial {trial}: {outcome:8} {failures}")
                time.sleep(args.pace_seconds)
                continue

            report = grader.grade(result, fixture, expectations[fixture_id], contract)
            status = "PASS" if report["pass"] else "FAIL"
            failures = report.get("failures", [])
            outcome = classifier.classify_trial(status, failures=failures)
            entry.update(status=status, failures=failures, outcome=outcome)
            ledger.append(entry)
            print(f"  {fixture_id} trial {trial}: {outcome:8}"
                  + (f" {failures}" if failures else ""))
            time.sleep(args.pace_seconds)

    by_fixture: dict[str, list[str]] = {}
    for entry in ledger:
        by_fixture.setdefault(entry["fixture_id"], []).append(entry["outcome"])

    print("\n=== per-fixture outcomes (every trial recorded, no best-of-N, no retry) ===")
    for fixture_id, outcomes in sorted(by_fixture.items()):
        family = expectations[fixture_id]["family"]
        n_pass = outcomes.count(classifier.PASS)
        n_t1 = outcomes.count(classifier.TIER1)
        n_t2 = outcomes.count(classifier.TIER2)
        n_inv = outcomes.count(classifier.INVALID)
        print(f"  {fixture_id:12} {family:28} judged-pass {n_pass}/{len(outcomes)}   "
              f"tier1 {n_t1}  tier2 {n_t2}  invalid {n_inv}")

    result = classifier.gate_verdict(by_fixture, cap_fixture, cap_total)
    verdict = result["verdict"]

    summary = {
        "gate_id": prereg["gate_id"],
        "candidate_assembly_digest": prereg["candidate_assembly_digest"],
        "heldout_seed": prereg["heldout_seed"],
        "model": os.environ.get("ANALYTICS_MODEL"),
        "trials_per_fixture": trials,
        "criterion": {
            "tier1_tolerance": 0,
            "tier2_per_fixture_cap": cap_fixture,
            "tier2_total_cap": cap_total,
            "retries_permitted": 0,
            "best_of_n": False,
            "tier_map_digest": classifier.RULES_DIGEST,
        },
        **result,
        "ledger": ledger,
    }
    (outdir / "gate-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(f"\ntier-1 (professional judgment) failures : {result['tier1_trials']}")
    print(f"tier-2 (contract-invalid output)        : {result['tier2_total']} of {len(ledger)}"
          f"   per fixture: { {k: v for k, v in result['tier2_per_fixture'].items() if v} }")
    print(f"INVALID (apparatus did not measure)     : {result['invalid_trials']}")
    print(f"\nGATE VERDICT: {verdict}")
    print(f"REASON: {result['reason']}")

    # INVALID is not a candidate verdict. Exit 2 so it can never be read as a pass or a fail.
    return {"PASS": 0, "FAIL": 1}.get(verdict, 2)


if __name__ == "__main__":
    raise SystemExit(main())
