#!/usr/bin/env python3
"""Zero-provider structural preflight for Brand Naming Practitioner v0.1.

No network/model/provider calls. This gate verifies frozen candidate identity,
qualification-state integrity, required professional boundaries, and fixture contract.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[4]
BASE = ROOT / "architect" / "evaluation" / "brand-naming-practitioner"

FREEZE = BASE / "candidate-freeze-v0.1.json"
MODEL = BASE / "professional-model-candidate-v0.1.md"
SKILL = BASE / "candidate" / "SKILL.md"
PLAN = BASE / "qualification-plan-v0.1.md"
CASES = BASE / "development" / "semantic_cases.json"

errors: list[str] = []
checks = 0


def require(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def blob_sha(path: Path) -> str:
    rel = path.relative_to(ROOT)
    proc = subprocess.run(
        ["git", "hash-object", str(rel)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


for path in [FREEZE, MODEL, SKILL, PLAN, CASES]:
    require(path.exists(), f"missing required artifact: {path.relative_to(ROOT)}")

freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
model = MODEL.read_text(encoding="utf-8")
skill = SKILL.read_text(encoding="utf-8")
plan = PLAN.read_text(encoding="utf-8")
cases = json.loads(CASES.read_text(encoding="utf-8"))

require(freeze.get("status") == "FROZEN_NOT_QUALIFIED", "freeze status must remain FROZEN_NOT_QUALIFIED")
require(freeze.get("release_state") == "NOT_QUALIFIED", "release_state must remain NOT_QUALIFIED")
require(
    freeze.get("library_admission") == "PROHIBITED_UNTIL_INDEPENDENT_PASS",
    "library admission must be prohibited before independent PASS",
)
require(freeze.get("parent_issue") == 275, "freeze must bind issue #275")

components = freeze.get("components", {})
expected_paths = {
    "architect/evaluation/brand-naming-practitioner/professional-model-candidate-v0.1.md": MODEL,
    "architect/evaluation/brand-naming-practitioner/candidate/SKILL.md": SKILL,
}
require(set(components) == set(expected_paths), "freeze components must match exact behavior-bearing set")
for rel, path in expected_paths.items():
    require(components.get(rel) == blob_sha(path), f"frozen blob mismatch for {rel}")

required_model_markers = [
    "Status: CANDIDATE / NOT QUALIFIED",
    "Brief before names.",
    "Criteria before convergence.",
    "Availability is live evidence.",
    "Preliminary screening is not legal clearance.",
    "Personal-brand names cannot manufacture authority.",
    "UNVERIFIED",
    "RESEARCH_REQUIRED",
    "Legal -> formal trademark clearance",
    "Localization/native linguist",
]
for marker in required_model_markers:
    require(marker in model, f"candidate model missing required marker: {marker}")

required_skill_markers = [
    "status: candidate-not-qualified",
    "FRAME -> LOCK CRITERIA -> DIVERGE -> SCREEN -> STRESS TEST -> COMPARE -> HANDOFF",
    "present guessed availability as checked",
    "call a web search legal clearance",
    "invent identity/credentials",
    "UNVERIFIED",
]
for marker in required_skill_markers:
    require(marker in skill, f"candidate skill missing required marker: {marker}")

require("No qualification PASS claimed." in plan, "qualification plan must explicitly deny PASS claim")
require("P0: 0 tolerated." in plan, "qualification plan must preserve zero-tolerance P0 gate")
require("final qualification judgment cannot be produced by the same self-review" in plan, "qualification plan must preserve evaluator independence")
require("NOT_EXECUTABLE" in plan, "qualification plan must preserve infrastructure verdict")

require(isinstance(cases, list) and len(cases) >= 8, "development suite must contain at least 8 cases")
ids = [case.get("id") for case in cases]
require(len(ids) == len(set(ids)), "development fixture IDs must be unique")

required_families = {
    "personal_brand_missing_positioning",
    "stakeholder_favorite",
    "legal_boundary",
    "tool_failure",
    "linguistic_boundary",
    "domain_tradeoff",
    "divergence",
    "personal_brand_truth",
}
families = {case.get("family") for case in cases}
require(required_families.issubset(families), "development suite missing required fixture family")

for case in cases:
    require(bool(case.get("task_summary")), f"{case.get('id')} missing task_summary")
    require(bool(case.get("required_behaviors")), f"{case.get('id')} missing required_behaviors")
    require(bool(case.get("forbidden_behaviors")), f"{case.get('id')} missing forbidden_behaviors")

if errors:
    print(f"FAIL: {len(errors)} error(s) across {checks} checks")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(f"PASS: {checks}/{checks} zero-provider structural checks")
print("Candidate remains FROZEN / NOT QUALIFIED. This preflight is not professional qualification.")
