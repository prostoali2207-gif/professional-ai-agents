#!/usr/bin/env python3
"""Repeated-trial runner for the Analytics v0.4 stability gate.

Records every trial. There is no best-of-N and no retry: a single behavioral failure
fails the gate, per the preregistration.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
ADAPTER = HERE / "adapters" / "stdio_candidate_adapter.py"


def verify_frozen(prereg: dict[str, Any], freeze: dict[str, Any]) -> None:
    """Fail closed if anything the preregistration bound has drifted."""
    def blob(path: str) -> str:
        return subprocess.check_output(["git", "hash-object", path], text=True, cwd=ROOT).strip()

    for component in freeze["assembly"]:
        actual = blob(component["path"])
        if actual != component["git_blob_sha"]:
            raise SystemExit(f"FROZEN CANDIDATE DRIFT: {component['path']} {actual} != {component['git_blob_sha']}")
    actual = blob(freeze["output_contract_path"])
    if actual != freeze["output_contract_git_blob_sha"]:
        raise SystemExit(f"OUTPUT CONTRACT DRIFT: {freeze['output_contract_path']}")
    if prereg["candidate_assembly_digest"] != freeze["assembly_digest"]:
        raise SystemExit("PREREGISTRATION DIGEST MISMATCH")
    for suite in prereg["suites"]:
        if blob(suite["path"]) != suite["git_blob_sha"]:
            raise SystemExit(f"FIXTURE DRIFT: {suite['path']}")
    if blob(prereg["grader"]["path"]) != prereg["grader"]["git_blob_sha"]:
        raise SystemExit("GRADER DRIFT: the gate's grader was edited after preregistration")
    print("FROZEN CANDIDATE, OUTPUT CONTRACT, FIXTURES AND GRADER VERIFIED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preregistration", required=True)
    parser.add_argument("--trials", type=int, default=None)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--pace-seconds", type=float, default=float(os.environ.get("ANALYTICS_PACE_SECONDS", "2")))
    args = parser.parse_args()

    prereg = json.loads(Path(args.preregistration).read_text(encoding="utf-8"))
    freeze = json.loads((ROOT / os.environ["ANALYTICS_CANDIDATE_MANIFEST"]).read_text(encoding="utf-8"))
    verify_frozen(prereg, freeze)

    trials = args.trials or int(prereg["trials_per_fixture"])
    grader_path = ROOT / prereg["grader"]["path"]
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    ledger: list[dict[str, Any]] = []
    for suite_ref in prereg["suites"]:
        suite = json.loads((ROOT / suite_ref["path"]).read_text(encoding="utf-8"))
        for fixture in suite["fixtures"]:
            fixture_id = fixture["fixture_id"]
            for trial in range(1, trials + 1):
                entry: dict[str, Any] = {"fixture_id": fixture_id, "trial": trial, "suite": suite["suite_id"]}
                proc = subprocess.run(
                    [sys.executable, str(ADAPTER)],
                    input=json.dumps(fixture, ensure_ascii=False),
                    text=True, capture_output=True, cwd=ROOT,
                    env=os.environ.copy(), timeout=300,
                )
                if proc.returncode != 0:
                    entry.update(status="EXECUTION_ERROR", detail=proc.stderr[-600:])
                    ledger.append(entry)
                    print(f"  {fixture_id} trial {trial}: EXECUTION_ERROR")
                    time.sleep(args.pace_seconds)
                    continue

                result_path = outdir / f"{fixture_id}-t{trial}.json"
                result_path.write_text(proc.stdout, encoding="utf-8")
                graded = subprocess.run(
                    [sys.executable, str(grader_path), str(result_path)],
                    text=True, capture_output=True, cwd=ROOT,
                )
                try:
                    report = json.loads(graded.stdout)
                except json.JSONDecodeError:
                    report = {"pass": False, "failures": ["grader produced no report"]}
                entry.update(status="PASS" if report.get("pass") else "FAIL", failures=report.get("failures", []))
                ledger.append(entry)
                print(f"  {fixture_id} trial {trial}: {entry['status']}"
                      + (f"  {entry['failures']}" if entry["status"] == "FAIL" else ""))
                time.sleep(args.pace_seconds)

    by_fixture: dict[str, list[str]] = {}
    for entry in ledger:
        by_fixture.setdefault(entry["fixture_id"], []).append(entry["status"])

    print("\n=== per-fixture trial results (every trial recorded, no best-of-N) ===")
    unstable, failed, errored = [], [], []
    for fixture_id, statuses in sorted(by_fixture.items()):
        passes = statuses.count("PASS")
        print(f"  {fixture_id:12} {passes}/{len(statuses)} PASS   {statuses}")
        if "EXECUTION_ERROR" in statuses:
            errored.append(fixture_id)
        if "FAIL" in statuses:
            failed.append(fixture_id)
        if len({s for s in statuses if s != "EXECUTION_ERROR"}) > 1:
            unstable.append(fixture_id)

    verdict = "PASS" if not failed and not errored else "FAIL"
    summary = {
        "gate_id": prereg["gate_id"],
        "candidate_assembly_digest": prereg["candidate_assembly_digest"],
        "model": os.environ.get("ANALYTICS_MODEL"),
        "trials_per_fixture": trials,
        "verdict": verdict,
        "fixtures_with_a_failing_trial": failed,
        "fixtures_with_an_execution_error": errored,
        "fixtures_with_discordant_trials": unstable,
        "ledger": ledger,
    }
    (outdir / "gate-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"\nGATE VERDICT: {verdict}")
    if unstable:
        print(f"DISCORDANT TRIALS ON: {unstable}  <-- the instability under repair is still present")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
