#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "architect/evaluation/qualification-reliability-engineer"
SOURCE = BASE / "stage-b/calibration-pack-v0.1.json"
BUNDLE = BASE / "cycle-2/blind-bundle-v0.2.json"
TEMPLATE = BASE / "cycle-2/blind-judgment-template-v0.2.json"
EXPECTED_SOURCE_SHA = "0f3742de73dce04517ed93bb81d8114bb3c0b51a0b855f45b353a91f85af1103"
CYCLE = "qre-v01-cycle2-b2a-blind-review-r1"

def canonical_pretty(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def build():
    raw = SOURCE.read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != EXPECTED_SOURCE_SHA:
        raise SystemExit(f"source pack SHA mismatch: {got}")
    src = json.loads(raw)
    bundle = {
        "version": "0.2",
        "cycle": CYCLE,
        "source_pack_sha256": got,
        "p0_rules": src["policy"]["p0_rules"],
        "rubric": src["rubric"],
        "cases": [
            {
                "case_id": c["case_id"],
                "task": c["task"],
                "facts_observables": c["facts_observables"],
                "unknowns_misleading_cues": c["unknowns_misleading_cues"],
                "reference_exemplars": c["reference_exemplars"],
            }
            for c in src["cases"]
        ],
    }
    bundle_bytes = canonical_pretty(bundle)
    bundle_sha = hashlib.sha256(bundle_bytes).hexdigest()
    refs = [r["reference_id"] for c in bundle["cases"] for r in c["reference_exemplars"]]
    if len(refs) != 48 or len(set(refs)) != 48:
        raise SystemExit("expected 48 unique references")
    template = {
        "version": "0.2",
        "cycle": CYCLE,
        "source_bundle_sha256": bundle_sha,
        "reviewer": {
            "fresh_context": True,
            "author_key_seen": False,
            "candidate_outputs_seen": False,
        },
        "judgments": [
            {
                "reference_id": rid,
                "predicted_level": "",
                "p0_triggers": [],
                "material_strengths": [],
                "material_failures": [],
                "uncertainty": "",
                "release_eligible": None,
            }
            for rid in refs
        ],
    }
    return bundle_bytes, canonical_pretty(template), bundle_sha

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    bundle_bytes, template_bytes, bundle_sha = build()
    if args.check:
        if BUNDLE.read_bytes() != bundle_bytes:
            raise SystemExit("checked-in blind bundle differs from deterministic build")
        if TEMPLATE.read_bytes() != template_bytes:
            raise SystemExit("checked-in judgment template differs from deterministic build")
        print(f"QRE_CYCLE2_PACKAGE_BUILD_PASS bundle_sha256={bundle_sha}")
        return
    BUNDLE.write_bytes(bundle_bytes)
    TEMPLATE.write_bytes(template_bytes)
    print(bundle_sha)

if __name__ == "__main__":
    main()
