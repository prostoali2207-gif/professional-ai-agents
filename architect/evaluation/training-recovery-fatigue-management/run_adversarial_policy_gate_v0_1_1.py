from __future__ import annotations
import json, pathlib, sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
base = root / "architect/evaluation/training-recovery-fatigue-management"
skill = (base / "candidate/SKILL.md").read_text(encoding="utf-8")
cases = json.loads((base / "development-cases-v0.1.1.json").read_text(encoding="utf-8"))

requirements = {
    "D01":["SINGLE-OBSERVATION GATE","TRANSIENT_UNDERPERFORMANCE"],
    "D02":["LOCAL_MUSCLE_FATIGUE","do not label whole-body/systemic fatigue"],
    "D03":["UNDER_RECOVERY_TREND","SYSTEMIC_FATIGUE_PATTERN","recent volume increase"],
    "D04":["## Wearable policy","Never make a structural decision solely from:"],
    "D05":["one missed PR","plateau"],
    "D06":["PLATEAU_CANDIDATE","do not default to deload"],
    "D07":["DELOAD_CANDIDATE","No mandatory deload every N weeks"],
    "D08":["NORMAL_ADAPTIVE_FATIGUE","LOCAL_MUSCLE_FATIGUE"],
    "D09":["SAFETY GATE","MEDICAL_ESCALATION"],
    "D10":["diagnose overtraining syndrome","medical exclusion diagnosis"],
    "D11":["HISTORY GATE","previous result","Do not repeat it reflexively"],
    "D12":["nutrition/hydration uncertainty","Do not infer a specific medical or nutritional diagnosis","INSUFFICIENT_EVIDENCE"],
    "D13":["one-item fatigue/readiness/wellness value","not assumed to be validated or physiologically calibrated","within-person trends"],
    "D14":["Soreness does not quantify muscle damage reliably and does not prove hypertrophy","soreness"],
}
present={c["id"] for c in cases["cases"]}
assert present==set(requirements), (present,set(requirements))
failures={}
for cid,markers in requirements.items():
    miss=[m for m in markers if m not in skill]
    if miss: failures[cid]=miss
assert not failures, failures

print("TRFM_V011_ADVERSARIAL_POLICY_PASS")
print("cases=14")
print("new_regressions=D13,D14")
print("provider_calls=0")
print("behavioral_qualification_claim=false")
