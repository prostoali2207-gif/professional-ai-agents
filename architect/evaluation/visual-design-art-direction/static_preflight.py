#!/usr/bin/env python3
"""Zero-provider structural preflight for the Visual Design / Art Direction candidate.

This does not grade creative quality. It fails closed when release-critical
contracts or public development-regression coverage are missing before any
model/judge spend.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "candidate" / "SKILL.md"
MODEL = ROOT / "professional-model-candidate-v0.1.md"
REPAIR_V02 = ROOT / "professional-model-p0-repair-v0.2.md"
REPAIR_V03 = ROOT / "professional-model-p0-execution-repair-v0.3.md"
FIXTURES = ROOT / "fixtures-v0.1.json"
TARGETED_V02 = ROOT / "fixtures-v0.2-targeted-regression.json"
TARGETED_V03 = ROOT / "fixtures-v0.3-targeted-regression.json"
PLAN = ROOT / "qualification-plan-v0.1.md"
REVISION_V03 = ROOT / "revision-r4-p0-v0.3.md"


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


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.name} is not valid JSON: {exc}")


def validate_rows(rows: list[dict], label: str) -> None:
    ids = [row.get("id") for row in rows]
    if len(ids) != len(set(ids)):
        fail(f"{label}: fixture ids must be unique")
    for row in rows:
        if not isinstance(row.get("prompt"), str) or not row["prompt"].strip():
            fail(f"{label}/{row.get('id')}: missing prompt")
        obs = row.get("must_observe")
        if not isinstance(obs, list) or len(obs) < 2 or not all(isinstance(x, str) and x.strip() for x in obs):
            fail(f"{label}/{row.get('id')}: must_observe must contain at least two non-empty observations")
        no = row.get("must_not_observe")
        if no is not None and (not isinstance(no, list) or not all(isinstance(x, str) and x.strip() for x in no)):
            fail(f"{label}/{row.get('id')}: must_not_observe must be a list of non-empty strings")


def main() -> int:
    require_text(
        SKILL,
        [
            "version: 0.3.0-candidate",
            "Status: **CANDIDATE — NOT QUALIFIED**",
            "DISCOVER",
            "DIRECT",
            "REFINE",
            "RENDER BLOCKED",
            "motion / 3D / WebGL",
            "Material-decision admission protocol",
            "FUNCTION PASS",
            "MOBILE PASS",
            "AUTHORITY PASS",
            "TRUTH PASS",
            "REFERENCE PASS",
            "ADVANCED-MEDIA PASS",
            "VERIFIED_SUPPLIED",
            "UNKNOWN_OR_UNVERIFIED",
            "CONCEPTUAL_NON_PROOF",
            "UPSTREAM_CONSTRAINT",
            "MOBILE INELIGIBLE",
            "derivative-distance question",
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
        REPAIR_V02,
        [
            "ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE",
            "SPECTACLE_BREAKS_HARD_FUNCTION_CONSTRAINT",
            "UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE",
            "J-01 — Hard-function precedence veto",
            "J-02 — Mobile viability veto",
            "J-03 — Authority veto",
            "J-04 — Advanced-media feasibility before desirability",
            "J-05 — Ready-state gate",
        ],
    )
    require_text(
        REPAIR_V03,
        [
            "ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE",
            "FABRICATED_FACTUAL_PROOF",
            "REFERENCE_IMITATION_AS_SOLUTION",
            "UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE",
            "J-06 — Material-decision admission control",
            "J-07 — Proof provenance firewall",
            "J-08 — Reference abstraction and derivative-distance test",
            "J-09 — Mobile task-equivalence admission",
            "J-10 — Authority mutation firewall",
            "J-11 — Gate evidence, not gate assertion",
            "fresh independent R5 held-out corpus",
        ],
    )
    require_text(
        REVISION_V03,
        [
            "SEMANTIC_FAIL_P0",
            "confirmed P0 count: 4",
            "No hidden R4 case content was inspected",
            "fresh independent R5 held-out semantic release cycle",
            "Rendered P1–P4 remains mandatory only after fresh semantic PASS",
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

    payload = load_json(FIXTURES)
    families = payload.get("families")
    if not isinstance(families, list) or len(families) < 12:
        fail("expected at least 12 development fixture families")
    validate_rows(families, "v0.1")

    ids = {row.get("id") for row in families}
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
        fail("release-critical v0.1 traps are not all marked P0")

    targeted_v02 = load_json(TARGETED_V02)
    boundary_v02 = targeted_v02.get("source_boundary", {})
    if boundary_v02.get("r3_hidden_content_used") is not False or boundary_v02.get("release_use") != "DEVELOPMENT_ONLY":
        fail("v0.2 regression source boundary must exclude hidden R3 content and release use")
    if boundary_v02.get("fresh_heldout_required_for_v0_2_release") is not True:
        fail("v0.2 must retain its historical fresh-heldout requirement")
    rows_v02 = targeted_v02.get("families")
    if not isinstance(rows_v02, list) or len(rows_v02) != 4:
        fail("expected exactly four targeted v0.2 regression families")
    validate_rows(rows_v02, "v0.2")
    ids_v02 = {row.get("id") for row in rows_v02}
    required_v02 = {
        "R20_MOBILE_FUNCTION_VETO",
        "R21_SPECTACLE_HARD_FUNCTION_VETO",
        "R22_AUTHORITY_UX_PRODUCT_VETO",
        "R23_JUSTIFIED_ADVANCED_MEDIA_NONREGRESSION",
    }
    if ids_v02 != required_v02:
        fail(f"targeted v0.2 regression ids mismatch: {sorted(ids_v02)}")

    targeted_v03 = load_json(TARGETED_V03)
    boundary_v03 = targeted_v03.get("source_boundary", {})
    if boundary_v03.get("r4_hidden_content_used") is not False:
        fail("v0.3 regression source boundary must explicitly exclude hidden R4 content")
    if boundary_v03.get("sanitized_failure_classes_only") is not True:
        fail("v0.3 regression must state sanitized failure classes only")
    if boundary_v03.get("release_use") != "DEVELOPMENT_ONLY":
        fail("v0.3 targeted regression must remain DEVELOPMENT_ONLY")
    if boundary_v03.get("fresh_heldout_required_for_v0_3_release") is not True:
        fail("v0.3 must require a fresh R5 held-out release corpus")

    rows_v03 = targeted_v03.get("families")
    if not isinstance(rows_v03, list) or len(rows_v03) != 6:
        fail("expected exactly six targeted v0.3 regression families")
    validate_rows(rows_v03, "v0.3")
    ids_v03 = {row.get("id") for row in rows_v03}
    required_v03 = {
        "R30_MOBILE_ADMISSION_BEFORE_SHORTLIST",
        "R31_PROOF_PROVENANCE_FIREWALL",
        "R32_REFERENCE_DERIVATIVE_DISTANCE",
        "R33_AUTHORITY_MUTATION_BEFORE_CONTRACT",
        "R34_REFERENCE_LITERACY_NONREGRESSION",
        "R35_CONCEPTUAL_NONPROOF_AND_ADVANCED_MEDIA_NONREGRESSION",
    }
    if ids_v03 != required_v03:
        fail(f"targeted v0.3 regression ids mismatch: {sorted(ids_v03)}")
    p0_v03 = {row.get("id") for row in rows_v03 if row.get("criticality") == "P0"}
    expected_p0_v03 = {
        "R30_MOBILE_ADMISSION_BEFORE_SHORTLIST",
        "R31_PROOF_PROVENANCE_FIREWALL",
        "R32_REFERENCE_DERIVATIVE_DISTANCE",
        "R33_AUTHORITY_MUTATION_BEFORE_CONTRACT",
    }
    if p0_v03 != expected_p0_v03:
        fail(f"v0.3 repaired P0 set mismatch: {sorted(p0_v03)}")

    print(
        "VISUAL_DESIGN_STATIC_PREFLIGHT_PASS "
        f"families={len(families)} p0={len(p0)} targeted_v02={len(rows_v02)} targeted_v03={len(rows_v03)} "
        "provider_calls=0 creative_quality_claimed=false fresh_r5_holdout_required=true"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
