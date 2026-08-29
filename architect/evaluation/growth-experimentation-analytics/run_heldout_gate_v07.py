#!/usr/bin/env python3
"""Preregistered held-out gate runner for Analytics v0.7.

Generates the held-out cases from the preregistered seed at run time, executes N trials per
case, and grades each against the generator's oracle. Every trial is recorded. There is no
best-of-N and no retry: one behavioral failure fails the gate.

The executor receives one candidate-facing fixture at a time and never the expectations.
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
ABORT_AFTER_CONSECUTIVE_ERRORS = 3


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
            raise SystemExit(f"FROZEN CANDIDATE DRIFT: {component['path']} {actual} != {component['git_blob_sha']}")
    if blob(freeze["output_contract_path"]) != freeze["output_contract_git_blob_sha"]:
        raise SystemExit(f"OUTPUT CONTRACT DRIFT: {freeze['output_contract_path']}")
    if prereg["candidate_assembly_digest"] != freeze["assembly_digest"]:
        raise SystemExit("PREREGISTRATION DIGEST MISMATCH")
    for key in ("generator", "grader"):
        ref = prereg[key]
        if blob(ref["path"]) != ref["git_blob_sha"]:
            raise SystemExit(f"{key.upper()} DRIFT: {ref['path']} was edited after preregistration")
    print("FROZEN CANDIDATE, OUTPUT CONTRACT, GENERATOR AND GRADER VERIFIED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preregistration", required=True)
    parser.add_argument("--trials", type=int, default=None)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--pace-seconds", type=float, default=float(os.environ.get("ANALYTICS_PACE_SECONDS", "3")))
    args = parser.parse_args()

    prereg = json.loads(Path(args.preregistration).read_text(encoding="utf-8"))
    freeze = json.loads((ROOT / os.environ["ANALYTICS_CANDIDATE_MANIFEST"]).read_text(encoding="utf-8"))
    verify_frozen(prereg, freeze)

    generator = load_module("gen", ROOT / prereg["generator"]["path"])
    grader = load_module("grader", ROOT / prereg["grader"]["path"])
    # The contract the candidate was told to satisfy is the contract it is graded against.
    # Loading it from the freeze rather than a default keeps the two in step by construction.
    contract_path = freeze.get("output_contract_path")
    contract = json.loads((ROOT / contract_path).read_text(encoding="utf-8")) if contract_path else None
    suite, oracle = generator.generate(prereg["heldout_seed"], prereg["per_family"])
    expectations = oracle["expectations"]
    fixtures = {f["fixture_id"]: f for f in suite["fixtures"]}
    trials = args.trials or int(prereg["trials_per_fixture"])

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    # The candidate-facing suite is preserved; the oracle is not written next to it.
    (outdir / "heldout-cases.json").write_text(json.dumps(suite, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(fixtures)} held-out cases from preregistered seed {prereg['heldout_seed']}")

    ledger: list[dict[str, Any]] = []
    consecutive_errors = 0
    aborted = False
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
                entry.update(status="EXECUTION_ERROR", detail=detail)
                ledger.append(entry)
                print(f"  {fixture_id} trial {trial}: EXECUTION_ERROR  {detail or '(no stderr)'}")
                consecutive_errors += 1
                if consecutive_errors >= ABORT_AFTER_CONSECUTIVE_ERRORS:
                    print(f"\nABORTING: {consecutive_errors} consecutive execution errors. This is a "
                          f"configuration or runtime failure, not candidate evidence.")
                    aborted = True
                    break
                time.sleep(args.pace_seconds)
                continue
            consecutive_errors = 0

            result_path = outdir / f"{fixture_id}-t{trial}.json"
            result_path.write_text(proc.stdout, encoding="utf-8")
            try:
                result = json.loads(proc.stdout)
            except json.JSONDecodeError:
                entry.update(status="FAIL", failures=["candidate returned non-JSON"])
                ledger.append(entry)
                print(f"  {fixture_id} trial {trial}: FAIL  ['candidate returned non-JSON']")
                time.sleep(args.pace_seconds)
                continue

            report = grader.grade(result, fixture, expectations[fixture_id], contract)
            entry.update(status="PASS" if report["pass"] else "FAIL", failures=report.get("failures", []))
            ledger.append(entry)
            print(f"  {fixture_id} trial {trial}: {entry['status']}"
                  + (f"  {entry['failures']}" if entry["status"] == "FAIL" else ""))
            time.sleep(args.pace_seconds)
        if aborted:
            break

    by_fixture: dict[str, list[str]] = {}
    for entry in ledger:
        by_fixture.setdefault(entry["fixture_id"], []).append(entry["status"])

    print("\n=== per-fixture trial results (every trial recorded, no best-of-N) ===")
    failed, errored, discordant = [], [], []
    for fixture_id, statuses in sorted(by_fixture.items()):
        family = expectations[fixture_id]["family"]
        print(f"  {fixture_id:12} {family:28} {statuses.count('PASS')}/{len(statuses)} PASS   {statuses}")
        if "EXECUTION_ERROR" in statuses:
            errored.append(fixture_id)
        if "FAIL" in statuses:
            failed.append(fixture_id)
        if len({s for s in statuses if s != "EXECUTION_ERROR"}) > 1:
            discordant.append(fixture_id)

    verdict = "PASS" if not failed and not errored and not aborted and by_fixture else "FAIL"
    summary = {
        "gate_id": prereg["gate_id"],
        "candidate_assembly_digest": prereg["candidate_assembly_digest"],
        "heldout_seed": prereg["heldout_seed"],
        "model": os.environ.get("ANALYTICS_MODEL"),
        "trials_per_fixture": trials,
        "verdict": verdict,
        "aborted_on_consecutive_execution_errors": aborted,
        "fixtures_with_a_failing_trial": failed,
        "fixtures_with_an_execution_error": errored,
        "fixtures_with_discordant_trials": discordant,
        "ledger": ledger,
    }
    (outdir / "gate-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"\nGATE VERDICT: {verdict}")
    if discordant:
        print(f"DISCORDANT TRIALS ON: {discordant}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
