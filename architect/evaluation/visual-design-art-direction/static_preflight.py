#!/usr/bin/env python3
"""Zero-provider structural preflight for the Visual Design / Art Direction candidate.

This does not grade creative quality. It only fails closed when release-critical
contracts or development-fixture coverage are missing before any model/judge spend.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "candidate" / "SKILL.md"
MODEL = ROOT / "professional-model-candidate-v0.1.md"
FIXTURES = ROOT / "fixtures-v0.1.json"
PLAN = ROOT / "qualification-plan-v0.1.md"


def fail(message: str) -> None:
    print(f"VISUAL_DESIGN_STATIC_PREFLIGHT_FAIL: {message}")
    raise SystemExit(1)


def require_text(path: Path, needles: list[str]) -> None:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT.parent.parent.parent)}")
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            fail(f"{path.name}: missing required contract marker {needle!r}")


def main() -> int:
    require_text(
        SKILL,
        [
            "Status: **CANDIDATE — NOT QUALIFIED**",
            "DISCOVER",
            "DIRECT",
            "REFINE",
            "RENDER BLOCKED",
            "motion / 3D / WebGL",
            "Never fabricate business imagery",
            "Never issue the independent final product release PASS",
        ],
    )
    require_text(
        MODEL,
        [
            "VD-02 — Current reference research and benchmark extraction",
            "VD-03 — Creative divergence before convergence",
            "VD-07 — Mobile-first responsive art direction",
            "VD-09 — Rendered artifact critique and iterative refinement",
            "VD-10 — Motion / 3D / WebGL capability routing",
            "never invent customer logos, metrics, testimonials",
        ],
    )
    require_text(
        PLAN,
        [
            "P0 hard-fail behaviors",
            "Held-out professional judgment gate",
            "Practical rendered-artifact gate",
            "uncalibrated single LLM scalar score is not release evidence",
            "`NOT QUALIFIED`",
        ],
    )

    try:
        payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"fixtures are not valid JSON: {exc}")

    families = payload.get("families")
    if not isinstance(families, list) or len(families) < 12:
        fail("expected at least 12 development fixture families")

    ids = [row.get("id") for row in families]
    if len(ids) != len(set(ids)):
        fail("fixture ids must be unique")

    required = {
        "F02_REFERENCE_COPY_TRAP",
        "F03_PSEUDO_DIVERGENCE",
        "F04_GENERIC_SAAS_BIAS",
        "F05_FAKE_PROOF_ASSET",
        "F06_MOBILE_COLLAPSE",
        "F08_UNJUSTIFIED_3D",
        "F09_JUSTIFIED_3D_ROUTING",
        "F10_RENDER_HONESTY",
        "F11_RENDER_CONTRACT_MISMATCH",
        "F12_BOLDNESS_VS_FUNCTION",
    }
    missing = sorted(required.difference(ids))
    if missing:
        fail(f"missing critical development families: {missing}")

    p0 = {row.get("id") for row in families if row.get("criticality") == "P0"}
    p0_required = {
        "F02_REFERENCE_COPY_TRAP",
        "F05_FAKE_PROOF_ASSET",
        "F06_MOBILE_COLLAPSE",
        "F08_UNJUSTIFIED_3D",
        "F10_RENDER_HONESTY",
        "F12_BOLDNESS_VS_FUNCTION",
    }
    if not p0_required.issubset(p0):
        fail("release-critical traps are not all marked P0")

    for row in families:
        if not isinstance(row.get("prompt"), str) or not row["prompt"].strip():
            fail(f"{row.get('id')}: missing prompt")
        obs = row.get("must_observe")
        if not isinstance(obs, list) or len(obs) < 2 or not all(isinstance(x, str) and x.strip() for x in obs):
            fail(f"{row.get('id')}: must_observe must contain at least two non-empty observations")

    print(
        "VISUAL_DESIGN_STATIC_PREFLIGHT_PASS "
        f"families={len(families)} p0={len(p0)} provider_calls=0 creative_quality_claimed=false"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
