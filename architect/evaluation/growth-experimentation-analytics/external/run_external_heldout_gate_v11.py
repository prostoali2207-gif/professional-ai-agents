#!/usr/bin/env python3
"""Scored gate over the externally authored, sealed Analytics held-out pack.

The verdict arithmetic, the grader, the tier map and the trial count are the ones the v1.0
two-tier gate already ran under. Nothing about the criterion is re-tuned for this pack: that is
the whole point of running it. The single difference is where the cases come from -- a sealed
pack authored on a different model family by an author that never saw the candidate, instead of
the evaluator's own seeded generator.

Execution discipline, unchanged from `run_heldout_gate_v10_twotier.py`:

  * one invocation per trial, no retry, no best-of-N, every trial recorded;
  * the executor receives one candidate-facing fixture and never the expectations;
  * TIER1 has zero tolerance, TIER2 is capped per fixture and in total, any INVALID voids the
    gate and exits with a code that is neither PASS nor FAIL.

Ordering is deliberate and provable from the job log: the pack's ciphertext digest is printed
before the first candidate call, so no case can have been chosen after seeing a result.
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
ANALYTICS = HERE.parent
ROOT = HERE.parents[3]
ADAPTER = ANALYTICS / "adapters" / "stdio_candidate_adapter.py"


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
    for key in ("grader", "classifier", "pack_contract", "author", "runner"):
        ref = prereg[key]
        if blob(ref["path"]) != ref["git_blob_sha"]:
            raise SystemExit(f"{key.upper()} DRIFT: {ref['path']} was edited after preregistration")
    print("FROZEN CANDIDATE, OUTPUT CONTRACT, GRADER, CLASSIFIER, PACK CONTRACT, AUTHOR AND "
          "RUNNER VERIFIED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preregistration", required=True)
    parser.add_argument("--pack-dir", required=True)
    parser.add_argument("--trials", type=int, default=None)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--pace-seconds", type=float,
                        default=float(os.environ.get("ANALYTICS_PACE_SECONDS", "3")))
    args = parser.parse_args()

    prereg = json.loads(Path(args.preregistration).read_text(encoding="utf-8"))
    freeze = json.loads((ROOT / os.environ["ANALYTICS_CANDIDATE_MANIFEST"]).read_text(encoding="utf-8"))
    verify_frozen(prereg, freeze)

    grader = load_module("grader", ROOT / prereg["grader"]["path"])
    classifier = load_module("classifier", ROOT / prereg["classifier"]["path"])
    author = load_module("author", ROOT / prereg["author"]["path"])

    if classifier.RULES_DIGEST != prereg["tier_map_digest"]:
        raise SystemExit(f"TIER MAP DRIFT: {classifier.RULES_DIGEST} != {prereg['tier_map_digest']}")

    pack_dir = Path(args.pack_dir)
    manifest = json.loads((pack_dir / "external-heldout.manifest.json").read_text(encoding="utf-8"))
    pack = author.load_sealed_pack(pack_dir)

    if manifest["cycle_id"] != prereg["gate_id"]:
        raise SystemExit(f"PACK CYCLE MISMATCH: {manifest['cycle_id']} != {prereg['gate_id']}")
    if manifest["candidate_assembly_digest"] != prereg["candidate_assembly_digest"]:
        raise SystemExit("PACK WAS AUTHORED AGAINST A DIFFERENT CANDIDATE")
    if manifest["candidate_calls"] != 0:
        raise SystemExit("PACK PROVENANCE INVALID: the author called the candidate")
    if manifest["author_family"] == prereg["candidate_model_family"]:
        raise SystemExit("PACK PROVENANCE INVALID: author and candidate share a model family")
    if manifest["fixture_count"] != prereg["fixture_count"]:
        raise SystemExit(f"PACK CARDINALITY MISMATCH: {manifest['fixture_count']} fixtures, "
                         f"{prereg['fixture_count']} preregistered")
    if sorted(manifest["families"]) != sorted(prereg["families"]):
        raise SystemExit("PACK FAMILY SET MISMATCH")

    fixtures = {fixture["fixture_id"]: fixture for fixture in pack["fixtures"]}
    expectations = pack["expectations"]
    if set(fixtures) != set(expectations):
        raise SystemExit("PACK IS INTERNALLY INCONSISTENT: fixtures and expectations disagree")

    contract_path = freeze.get("output_contract_path")
    contract = json.loads((ROOT / contract_path).read_text(encoding="utf-8")) if contract_path else None
    trials = args.trials or int(prereg["trials_per_fixture"])
    cap_fixture = int(prereg["tier2_per_fixture_cap"])
    cap_total = int(prereg["tier2_total_cap"])

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Printed before the first candidate call, so the log proves the pack predates every result.
    print(f"external pack sealed by {manifest['author_model']} ({manifest['author_family']}); "
          f"candidate runs on {prereg['candidate_model_family']}")
    print(f"pack ciphertext sha256: {manifest['ciphertext_sha256']}")
    print(f"pack plaintext  sha256: {manifest['plaintext_sha256']}")
    print(f"{manifest['fixture_count']} externally authored fixtures across "
          f"{len(manifest['families'])} families; author calls {manifest['author_calls']}, "
          f"admission rejections {manifest['rejection_count']}")
    print(f"criterion: k={trials}, tier1=0, tier2 <= {cap_fixture}/fixture and <= {cap_total} "
          f"total, any INVALID voids the gate")
    print(f"tier map: {classifier.RULES_DIGEST}\n")

    ledger: list[dict[str, Any]] = []
    for fixture_id in sorted(fixtures):
        fixture = fixtures[fixture_id]
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
        print(f"  {fixture_id:12} {family:28} judged-pass {outcomes.count(classifier.PASS)}/"
              f"{len(outcomes)}   tier1 {outcomes.count(classifier.TIER1)}  "
              f"tier2 {outcomes.count(classifier.TIER2)}  "
              f"invalid {outcomes.count(classifier.INVALID)}")

    result = classifier.gate_verdict(by_fixture, cap_fixture, cap_total)
    verdict = result["verdict"]

    summary = {
        "gate_id": prereg["gate_id"],
        "candidate_assembly_digest": prereg["candidate_assembly_digest"],
        "pack": {"ciphertext_sha256": manifest["ciphertext_sha256"],
                 "plaintext_sha256": manifest["plaintext_sha256"],
                 "author_model": manifest["author_model"],
                 "author_family": manifest["author_family"],
                 "author_calls": manifest["author_calls"],
                 "rejection_count": manifest["rejection_count"],
                 "candidate_calls": manifest["candidate_calls"]},
        "model": os.environ.get("ANALYTICS_MODEL"),
        "trials_per_fixture": trials,
        "criterion": {"tier1_tolerance": 0, "tier2_per_fixture_cap": cap_fixture,
                      "tier2_total_cap": cap_total, "retries_permitted": 0, "best_of_n": False,
                      "tier_map_digest": classifier.RULES_DIGEST},
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
