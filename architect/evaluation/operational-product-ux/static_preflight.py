#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
SKILL = ROOT / "candidate" / "SKILL.md"
FIXTURES = ROOT / "fixtures-v0.1.json"
KNOWLEDGE = [
    ROOT / "candidate" / "knowledge" / "operational-interaction.md",
    ROOT / "candidate" / "knowledge" / "mobile-accessibility-rtl.md",
    ROOT / "candidate" / "knowledge" / "rendered-ux-review.md",
]

def fail(msg: str) -> None:
    print(f"OPERATIONAL_UX_STATIC_PREFLIGHT_FAIL: {msg}")
    raise SystemExit(1)

def require(path: Path, needles: list[str]) -> str:
    if not path.is_file():
        fail(f"missing {path.relative_to(REPO)}")
    text = path.read_text(encoding="utf-8")
    for n in needles:
        if n not in text:
            fail(f"{path.name}: missing marker {n!r}")
    return text

def main() -> int:
    skill = require(SKILL, [
        "name: operational-product-ux-core",
        "version: 0.1.0-candidate",
        "Status: **CANDIDATE — NOT QUALIFIED**",
        "TASK PASS", "AUTHORITY PASS", "STATE PASS", "RECOVERY PASS",
        "CONSEQUENCE PASS", "MOBILE PASS", "ACCESSIBILITY PASS", "TRUTH PASS",
        "UX CONTRACT READY", "RUNTIME UNVERIFIED",
        "Never issue independent final product release approval",
    ])
    for p in KNOWLEDGE:
        require(p, ["Serves:"])
    assembled = skill + "\n" + "\n".join(p.read_text(encoding="utf-8") for p in KNOWLEDGE)
    if "FleetDesk" in assembled:
        fail("reusable candidate contains FleetDesk-specific project coupling")

    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    if data.get("release_use") != "DEVELOPMENT_ONLY":
        fail("fixtures must be DEVELOPMENT_ONLY")
    boundary = data.get("source_boundary", {})
    if boundary.get("heldout_content_used") is not False:
        fail("development fixtures must exclude held-out content")
    if boundary.get("fresh_heldout_required_after_freeze") is not True:
        fail("fresh held-out must be required after freeze")
    rows = data.get("families")
    if not isinstance(rows, list) or len(rows) < 12:
        fail("expected at least 12 fixture families")
    ids = [r.get("id") for r in rows]
    if len(ids) != len(set(ids)):
        fail("fixture ids must be unique")
    required = {
        "UX04_RECOVERABLE_FAILURE_DATA_PRESERVATION",
        "UX05_PARTIAL_STALE_DISCONNECTED_STATE",
        "UX07_SELECT_ALL_SCOPE_TRAP",
        "UX08_CONSEQUENTIAL_GENERIC_CONFIRMATION",
        "UX10_COLLAPSED_DESKTOP_MOBILE",
        "UX11_ACCESSIBILITY_HOVER_DRAG_TRAP",
        "UX13_BOUNDARY_DOMAIN_RULE_TRAP",
        "UX14_RUNTIME_FALSE_PASS",
    }
    if not required.issubset(set(ids)):
        fail(f"missing required fixture families: {sorted(required-set(ids))}")
    p0 = {r.get("id") for r in rows if r.get("criticality") == "P0"}
    if not required.issubset(p0):
        fail("all release-critical required families must be P0")
    for row in rows:
        if not isinstance(row.get("prompt"), str) or not row["prompt"].strip():
            fail(f"{row.get('id')}: missing prompt")
        for key in ("must_observe", "must_not_observe"):
            vals = row.get(key)
            if not isinstance(vals, list) or not vals or not all(isinstance(x,str) and x.strip() for x in vals):
                fail(f"{row.get('id')}: invalid {key}")
    print(f"OPERATIONAL_UX_STATIC_PREFLIGHT_PASS families={len(rows)} p0={len(p0)} provider_calls=0 candidate_not_qualified=true fresh_holdout_required=true")
    return 0

if __name__ == "__main__":
    sys.exit(main())
