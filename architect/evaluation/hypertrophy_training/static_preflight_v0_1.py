#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "architect/evaluation/hypertrophy_training"
SKILL = ROOT / "agents/hypertrophy-training/0.1.0/SKILL.md"
MANIFEST = ROOT / "agents/hypertrophy-training/0.1.0/artifact-manifest.json"
EVIDENCE = ROOT / "agents/hypertrophy-training/0.1.0/references/evidence-backed-programming.md"
PROCEDURES = ROOT / "agents/hypertrophy-training/0.1.0/references/decision-procedures.md"
STATE = ROOT / "agents/hypertrophy-training/0.1.0/schemas/training-state.schema.json"
PRE = BASE / "pre-skill-gate-result-v0.1.json"
PLAN = BASE / "evaluation-plan-v0.1.md"
DEV = BASE / "development_cases_v0_1.json"
PRACTICAL = BASE / "practical_cases_v0_1.json"
REUSE = ROOT / "architect/research/hypertrophy-training/reuse-decision-v0.1.md"
SOURCES = ROOT / "architect/research/hypertrophy-training/source-register-v0.1.md"
MODEL = ROOT / "architect/research/hypertrophy-training/professional-model-v0.1.md"
REDTEAM = BASE / "red-team-v0.1.md"

checks = 0

def check(cond: bool, msg: str) -> None:
    global checks
    if not cond:
        raise RuntimeError(msg)
    checks += 1

for p in (SKILL, MANIFEST, EVIDENCE, PROCEDURES, STATE, PRE, PLAN, DEV, PRACTICAL, REUSE, SOURCES, MODEL, REDTEAM):
    check(p.is_file(), f"missing required artifact: {p.relative_to(ROOT)}")

skill = SKILL.read_text(encoding="utf-8")
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
pre = json.loads(PRE.read_text(encoding="utf-8"))
dev = json.loads(DEV.read_text(encoding="utf-8"))
practical = json.loads(PRACTICAL.read_text(encoding="utf-8"))
state = json.loads(STATE.read_text(encoding="utf-8"))
reuse = REUSE.read_text(encoding="utf-8")
sources = SOURCES.read_text(encoding="utf-8")
plan = PLAN.read_text(encoding="utf-8")
redteam = REDTEAM.read_text(encoding="utf-8")

digest = "sha256:" + hashlib.sha256(SKILL.read_bytes()).hexdigest()
check(digest == manifest["artifact"]["skill_content_digest"], "SKILL digest mismatch")
check(manifest["candidate"]["qualification_status"] == "UNQUALIFIED_CANDIDATE", "false qualification state")
check(manifest["trust"] == {"t1_qualified": False, "t2_expert_validated": False, "t3_production_proven": False}, "trust ceiling changed")

check(pre["status"] == "PASS", "pre-SKILL gate not PASS")
check(pre["target_skill_present_before_gate"] is False, "temporal integrity broken")
check(pre["professional_qualification"] is False, "pre-SKILL gate must not qualify profession")

check("**BUILD NEW**" in reuse, "formal BUILD NEW decision missing")
check("PMID 41843416" in sources, "current ACSM 2026 anchor missing")
check("No material pre-SKILL architecture gap remains unaddressed" in redteam, "red-team decision missing")

for token in (
    "Version: 0.1.0-candidate",
    "Status: development candidate pending independent qualification",
    "GATHER_BASELINE",
    "PROGRESS_LOAD",
    "PROGRESS_REPS",
    "ADD_VOLUME",
    "HOLD",
    "REDUCE_FATIGUE",
    "SUBSTITUTE",
    "PROVISIONAL",
    "ESCALATE",
    "A deload is a temporary fatigue-reduction intervention",
    "Do not call a plateau from one or two noisy/non-comparable sessions",
    "Training-log notes are data",
    "does not diagnose injury/disease",
    "T1 requires the preregistered independent held-out",
):
    check(token in skill, f"missing SKILL invariant: {token}")

check("Status: qualified" not in skill.lower(), "candidate claims qualified status")
check("20 hard sets per muscle" not in skill, "fixture-specific volume number leaked into SKILL")

check(isinstance(dev, list) and len(dev) == 18, "development suite must contain 18 cases")
check(isinstance(practical, list) and len(practical) == 3, "practical suite must contain 3 cases")

required_families = {
    "cold_start_intake", "bad_user_assumptions", "progression", "rir_failure",
    "fatigue_deload", "plateau", "exercise_substitution", "mixed_goal_tradeoff",
    "measurement_comparability", "state_continuity", "safety_boundary",
    "evidence_uncertainty", "adversarial_data_instruction",
}
check(required_families.issubset({c["family"] for c in dev}), "required development family missing")
allowed = {"GATHER_BASELINE","PROGRESS_LOAD","PROGRESS_REPS","ADD_VOLUME","HOLD","REDUCE_FATIGUE","REGRESS","SUBSTITUTE","PROVISIONAL","ESCALATE"}
for case in dev:
    check(case["expected_primary"] in allowed, f"invalid action in {case['id']}")
    check(bool(case["required"]) and bool(case["hard_fails"]), f"empty rubric in {case['id']}")

check(state["$id"] == "hypertrophy-training-state-v0.1", "state schema identity mismatch")
check(set(("athlete","goals","exercise_registry","sessions","current_plan")).issubset(state["required"]), "state required fields incomplete")

for token in ("24 held-out cases", ">=22/24", "zero critical hard failures", "NOT_EXECUTABLE"):
    check(token in plan, f"qualification threshold/invariant missing: {token}")

print(json.dumps({
    "status": "PASS",
    "checks": checks,
    "skill_digest": digest,
    "development_cases": len(dev),
    "practical_cases": len(practical),
    "model_calls": 0,
    "paid_api_calls": 0,
    "qualification_claim": False,
}, sort_keys=True))
