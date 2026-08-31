#!/usr/bin/env python3
"""Zero-provider structural preflight for the Visual Design / Art Direction candidate.

This does not grade creative quality. It only fails closed when release-critical
contracts, development-regression coverage, or the candidate freeze are inconsistent
before any model/judge spend.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[2]
SKILL = ROOT / "candidate" / "SKILL.md"
MODEL = ROOT / "professional-model-candidate-v0.1.md"
REPAIR_MODEL_V02 = ROOT / "professional-model-p0-repair-v0.2.md"
REPAIR_MODEL_V03 = ROOT / "professional-model-p0-repair-v0.3.md"
FIXTURES = ROOT / "fixtures-v0.1.json"
TARGETED_V02 = ROOT / "fixtures-v0.2-targeted-regression.json"
TARGETED_V03 = ROOT / "fixtures-v0.3-targeted-regression.json"
FREEZE_V03 = ROOT / "candidate-freeze-v0.3.json"
PLAN = ROOT / "qualification-plan-v0.1.md"


def fail(message: str) -> None:
    print(f"VISUAL_DESIGN_STATIC_PREFLIGHT_FAIL: {message}")
    raise SystemExit(1)


def require_text(path: Path, needles: list[str]) -> None:
    if not path.exists():
        fail(f"missing file: {path.relative_to(REPO_ROOT)}")
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            fail(f"{path.name}: missing required contract marker {needle!r}")


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.name} is not valid JSON: {exc}")


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def verify_freeze_blob(rel_path: str, expected_sha: str) -> None:
    path = REPO_ROOT / rel_path
    if not path.exists():
        fail(f"freeze references missing path: {rel_path}")
    actual = git_blob_sha(path)
    if actual != expected_sha:
        fail(f"freeze blob mismatch for {rel_path}: expected {expected_sha}, got {actual}")


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
            "Never fabricate business imagery",
            "Never issue the independent final product release PASS",
            "FUNCTION PASS",
            "MOBILE PASS",
            "AUTHORITY PASS",
            "TRUTH PASS",
            "ADVANCED-MEDIA PASS",
            "UPSTREAM_CONSTRAINT",
            "unusable collapsed desktop",
            "PRESERVE | TRANSFORM | ESCALATE",
            "Pre-commit control for release-critical moves",
            "reference influence is principle-level and mechanism-independent",
            "Never comply with a violating request and append a warning afterward",
            "actual assembled recommendation",
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
        REPAIR_MODEL_V02,
        [
            "ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE",
            "SPECTACLE_BREAKS_HARD_FUNCTION_CONSTRAINT",
            "UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE",
            "J-01 — Hard-function precedence veto",
            "J-02 — Mobile viability veto",
            "J-03 — Authority veto",
            "J-04 — Advanced-media feasibility before desirability",
            "J-05 — Ready-state gate",
            "fresh independent held-out corpus",
        ],
    )
    require_text(
        REPAIR_MODEL_V03,
        [
            "SEMANTIC_FAIL_P0",
            "ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE",
            "FABRICATED_FACTUAL_PROOF",
            "REFERENCE_IMITATION_AS_SOLUTION",
            "UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE",
            "J-06 — Pre-commit invariant control",
            "J-07 — Conflict-resolution precedence",
            "J-08 — Truth/proof firewall as an output constraint",
            "J-09 — Reference independence control",
            "J-10 — Mobile viability as authored transformation",
            "J-11 — Authority control on the actual recommendation",
            "J-12 — Final-output consistency gate",
            "PRESERVE | TRANSFORM | ESCALATE",
            "fresh independent held-out corpus",
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

    targeted_v02 = load_json(TARGETED_V02)
    boundary_v02 = targeted_v02.get("source_boundary", {})
    if boundary_v02.get("r3_hidden_content_used") is not False or boundary_v02.get("release_use") != "DEVELOPMENT_ONLY":
        fail("v0.2 targeted regression source boundary must explicitly exclude hidden R3 content and release use")
    if boundary_v02.get("fresh_heldout_required_for_v0_2_release") is not True:
        fail("v0.2 must require a fresh held-out release corpus")

    rows_v02 = targeted_v02.get("families")
    if not isinstance(rows_v02, list) or len(rows_v02) != 4:
        fail("expected exactly four targeted v0.2 regression families")
    ids_v02 = {row.get("id") for row in rows_v02}
    required_v02 = {
        "R20_MOBILE_FUNCTION_VETO",
        "R21_SPECTACLE_HARD_FUNCTION_VETO",
        "R22_AUTHORITY_UX_PRODUCT_VETO",
        "R23_JUSTIFIED_ADVANCED_MEDIA_NONREGRESSION",
    }
    if ids_v02 != required_v02:
        fail(f"v0.2 targeted regression ids mismatch: {sorted(ids_v02)}")
    p0_v02 = {row.get("id") for row in rows_v02 if row.get("criticality") == "P0"}
    if p0_v02 != required_v02 - {"R23_JUSTIFIED_ADVANCED_MEDIA_NONREGRESSION"}:
        fail("the three v0.2 repaired failure classes must remain P0 in development regression")

    targeted_v03 = load_json(TARGETED_V03)
    boundary_v03 = targeted_v03.get("source_boundary", {})
    if boundary_v03.get("r4_hidden_content_used") is not False:
        fail("v0.3 targeted regression must explicitly exclude hidden R4 content")
    if boundary_v03.get("sanitized_failure_classes_only") is not True:
        fail("v0.3 targeted regression must be based only on sanitized failure classes")
    if boundary_v03.get("release_use") != "DEVELOPMENT_ONLY":
        fail("v0.3 targeted regression cannot be release held-out evidence")
    if boundary_v03.get("fresh_heldout_required_for_v0_3_release") is not True:
        fail("v0.3 must require a fresh held-out release corpus")

    rows_v03 = targeted_v03.get("families")
    if not isinstance(rows_v03, list) or len(rows_v03) != 10:
        fail("expected exactly ten targeted v0.3 regression families")
    ids_v03 = {row.get("id") for row in rows_v03}
    required_v03 = {
        "R30_MOBILE_PRECOMMIT_CONTROL",
        "R31_TRUTH_PROOF_OUTPUT_CONTROL",
        "R32_REFERENCE_INDEPENDENCE_CONTROL",
        "R33_AUTHORITY_PRECOMMIT_CONTROL",
        "R34_WARNING_ONLY_COMPLIANCE_TRAP",
        "R35_AUTHORED_MOBILE_NONREGRESSION",
        "R36_TRUTH_PLACEHOLDER_NONREGRESSION",
        "R37_REFERENCE_ADAPTATION_NONREGRESSION",
        "R38_AUTHORITY_RECOMMENDATION_NONREGRESSION",
        "R39_BOLD_REFERENCE_ADVANCED_MEDIA_NONREGRESSION",
    }
    if ids_v03 != required_v03:
        fail(f"v0.3 targeted regression ids mismatch: {sorted(ids_v03)}")
    p0_v03 = {row.get("id") for row in rows_v03 if row.get("criticality") == "P0"}
    expected_p0_v03 = {
        "R30_MOBILE_PRECOMMIT_CONTROL",
        "R31_TRUTH_PROOF_OUTPUT_CONTROL",
        "R32_REFERENCE_INDEPENDENCE_CONTROL",
        "R33_AUTHORITY_PRECOMMIT_CONTROL",
        "R34_WARNING_ONLY_COMPLIANCE_TRAP",
    }
    if p0_v03 != expected_p0_v03:
        fail(f"v0.3 P0 regression set mismatch: {sorted(p0_v03)}")
    p1_v03 = {row.get("id") for row in rows_v03 if row.get("criticality") == "P1"}
    if p1_v03 != required_v03 - expected_p0_v03:
        fail(f"v0.3 non-regression contrastive set mismatch: {sorted(p1_v03)}")

    for row in rows_v03:
        if not isinstance(row.get("prompt"), str) or not row["prompt"].strip():
            fail(f"{row.get('id')}: missing v0.3 prompt")
        obs = row.get("must_observe")
        no = row.get("must_not_observe")
        if not isinstance(obs, list) or len(obs) < 3 or not all(isinstance(x, str) and x.strip() for x in obs):
            fail(f"{row.get('id')}: v0.3 must_observe must contain at least three non-empty observations")
        if not isinstance(no, list) or not no or not all(isinstance(x, str) and x.strip() for x in no):
            fail(f"{row.get('id')}: v0.3 must_not_observe must be non-empty")

    freeze = load_json(FREEZE_V03)
    if freeze.get("candidate_version") != "0.3.0-candidate":
        fail("v0.3 freeze candidate_version mismatch")
    if freeze.get("freeze_status") != "candidate-frozen-for-independent-qualification":
        fail("v0.3 freeze status mismatch")
    if freeze.get("current_verdict") != "NOT_QUALIFIED":
        fail("v0.3 must remain NOT_QUALIFIED before independent release evidence")
    base = freeze.get("base_candidate", {})
    if base.get("semantic_run") != 33388218997 or base.get("result") != "SEMANTIC_FAIL_P0":
        fail("v0.3 freeze must bind the exact prior terminal semantic failure")
    if base.get("sanitized_report_artifact_id") != 9756857311:
        fail("v0.3 freeze sanitized report artifact id mismatch")
    if base.get("sanitized_report_artifact_digest") != "sha256:98158107d57f8b59f468cf8aae12f9927c3eb4affd87a51d09427d974fb65d3d":
        fail("v0.3 freeze sanitized report artifact digest mismatch")
    if base.get("sanitized_report_payload_sha256") != "9011fb75429d67a58b6cfc495a4bdc498d382554360acdf7480e1a8cf3b975dd":
        fail("v0.3 freeze sanitized report payload hash mismatch")

    frozen_entries = freeze.get("components", []) + freeze.get("development_fixtures", [])
    if not frozen_entries:
        fail("v0.3 freeze has no frozen entries")
    frozen_paths = {row.get("path") for row in frozen_entries}
    required_frozen_paths = {
        "architect/evaluation/visual-design-art-direction/candidate/SKILL.md",
        "architect/evaluation/visual-design-art-direction/professional-model-candidate-v0.1.md",
        "architect/evaluation/visual-design-art-direction/professional-model-p0-repair-v0.2.md",
        "architect/evaluation/visual-design-art-direction/professional-model-p0-repair-v0.3.md",
        "architect/evaluation/visual-design-art-direction/fixtures-v0.1.json",
        "architect/evaluation/visual-design-art-direction/fixtures-v0.2-targeted-regression.json",
        "architect/evaluation/visual-design-art-direction/fixtures-v0.3-targeted-regression.json",
    }
    if frozen_paths != required_frozen_paths:
        fail(f"v0.3 freeze path set mismatch: {sorted(frozen_paths)}")
    for row in frozen_entries:
        rel = row.get("path")
        sha = row.get("git_blob_sha")
        if not isinstance(rel, str) or not isinstance(sha, str):
            fail("v0.3 freeze entry missing path or git_blob_sha")
        verify_freeze_blob(rel, sha)

    print(
        "VISUAL_DESIGN_STATIC_PREFLIGHT_PASS "
        f"families={len(families)} p0={len(p0)} targeted_v02={len(rows_v02)} targeted_v03={len(rows_v03)} "
        "provider_calls=0 creative_quality_claimed=false fresh_holdout_required=true candidate_version=0.3.0-candidate freeze_verified=true"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
