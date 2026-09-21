from __future__ import annotations
import json, pathlib, sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
base = root / "architect/evaluation/training-recovery-fatigue-management"
skill = (base / "candidate/SKILL.md").read_text(encoding="utf-8")
cases = json.loads((base / "development-cases-v0.1.json").read_text(encoding="utf-8"))
assert len(cases["cases"]) == 12

requirements = {
    "D01": ["SINGLE-OBSERVATION GATE", "TRANSIENT_UNDERPERFORMANCE"],
    "D02": ["LOCAL_MUSCLE_FATIGUE", "do not label whole-body/systemic fatigue"],
    "D03": ["UNDER_RECOVERY_TREND", "SYSTEMIC_FATIGUE_PATTERN", "recent volume increase"],
    "D04": ["## Wearable policy", "Never make a structural decision solely from:"],
    "D05": ["one missed PR", "plateau"],
    "D06": ["PLATEAU_CANDIDATE", "do not default to deload"],
    "D07": ["DELOAD_CANDIDATE", "No mandatory deload every N weeks"],
    "D08": ["NORMAL_ADAPTIVE_FATIGUE", "LOCAL_MUSCLE_FATIGUE"],
    "D09": ["SAFETY GATE", "MEDICAL_ESCALATION"],
    "D10": ["diagnose overtraining syndrome", "medical exclusion diagnosis"],
    "D11": ["HISTORY GATE", "previous result", "Do not repeat it reflexively"],
    "D12": ["nutrition/hydration uncertainty", "Do not infer a specific medical or nutritional diagnosis", "INSUFFICIENT_EVIDENCE"],
}

present = {c["id"] for c in cases["cases"]}
assert present == set(requirements)
failures = {}
for cid, markers in requirements.items():
    missing = [m for m in markers if m not in skill]
    if missing:
        failures[cid] = missing
assert not failures, failures

for forbidden in [
    "deload every 4 weeks",
    "deload every 6 weeks",
    "HRV threshold",
    "recovery score threshold",
]:
    assert forbidden not in skill

print("TRFM_ADVERSARIAL_POLICY_COVERAGE_PASS")
print("cases=12")
print("hard_fail_families=covered_by_explicit_policy")
print("provider_calls=0")
print("behavioral_qualification_claim=false")
