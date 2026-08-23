#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, subprocess, sys, tempfile

V04_SHA = "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
TARGET = {"F2", "F5", "F6", "F7", "F12"}
STOCHASTIC = {"F2", "F5", "F6", "F11", "F12"}
P0_EXTRA = {"F1", "F4", "F8", "F9", "F10"}
HISTORICAL_BUILDER_COMMIT = "76e48f778a2796b3dd4c67a528261b87ce8408f7"
HISTORICAL_BUILDER_PATH = "architect/evaluation/content-architecture-heldout/build_sealed_runtime.py"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--parts-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # Reuse the exact historical sealed-pack verifier/builder. This preserves the
    # registered component hashes and does not create or alter hidden fixtures.
    source = subprocess.check_output(
        ["git", "show", f"{HISTORICAL_BUILDER_COMMIT}:{HISTORICAL_BUILDER_PATH}"],
        text=True,
    )
    with tempfile.TemporaryDirectory() as td:
        legacy = pathlib.Path(td) / "legacy_builder.py"
        legacy.write_text(source, encoding="utf-8")
        subprocess.run(
            [sys.executable, str(legacy), "--parts-dir", args.parts_dir, "--out", args.out],
            check=True,
        )

    full = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    ordered = []
    for src in full["fixtures"]:
        if src["family"] in TARGET:
            row = dict(src)
            row["trial_count"] = 3 if row["family"] in STOCHASTIC else 1
            row["regression_scope"] = "TARGETED"
            ordered.append(row)
    for src in full["fixtures"]:
        if src["family"] in P0_EXTRA:
            row = dict(src)
            row["trial_count"] = 1
            row["regression_scope"] = "P0_EXTRA"
            ordered.append(row)

    full["candidate_sha"] = V04_SHA
    full["fixtures"] = ordered
    full["evaluator_class"] = "independent-held-out-regression"
    full["regression_policy"] = {
        "target_families": sorted(TARGET),
        "stochastic_repeats": 3,
        "p0_extra_families": sorted(P0_EXTRA),
        "candidate": V04_SHA,
    }
    (out / "manifest.json").write_text(
        json.dumps(full, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps({
        "status": "PASS",
        "candidate_sha": V04_SHA,
        "fixture_records": len(ordered),
        "run_count": sum(int(x.get("trial_count", 1)) for x in ordered),
        "target_families": sorted(TARGET),
        "p0_extra_families": sorted(P0_EXTRA),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
