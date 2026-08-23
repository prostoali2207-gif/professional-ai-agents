#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, subprocess, sys, tempfile

V03_SHA = "dff87c22a4c39cf6300dc3b36b6cedfc7448c47d"
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
    # F5/F6/F7/F12 are direct repair targets. F2 is retained because the v0.3
    # cross-cutting commercial-truth firewall and hook rule can affect this family.
    for src in full["fixtures"]:
        if src["family"] in TARGET:
            row = dict(src)
            row["trial_count"] = 3 if row["family"] in STOCHASTIC else 1
            row["regression_scope"] = "TARGETED_OR_COUPLED"
            ordered.append(row)
    for src in full["fixtures"]:
        if src["family"] in P0_EXTRA:
            row = dict(src)
            row["trial_count"] = 1
            row["regression_scope"] = "P0_EXTRA"
            ordered.append(row)

    full["candidate_sha"] = V03_SHA
    full["fixtures"] = ordered
    full["evaluator_class"] = "independent-held-out-regression"
    full["regression_policy"] = {
        "direct_target_families": ["F5", "F6", "F7", "F12"],
        "coupled_target_families": ["F2"],
        "stochastic_repeats": 3,
        "p0_extra_families": sorted(P0_EXTRA),
        "candidate": V03_SHA,
    }
    (out / "manifest.json").write_text(
        json.dumps(full, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps({
        "status": "PASS",
        "candidate_sha": V03_SHA,
        "fixture_records": len(ordered),
        "run_count": sum(int(x.get("trial_count", 1)) for x in ordered),
        "target_families": sorted(TARGET),
        "p0_extra_families": sorted(P0_EXTRA),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
