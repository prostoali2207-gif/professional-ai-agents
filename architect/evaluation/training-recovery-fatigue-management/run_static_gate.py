from __future__ import annotations
import json, pathlib, sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
base = root / "architect/evaluation/training-recovery-fatigue-management"
skill = (base / "candidate/SKILL.md").read_text(encoding="utf-8")
schema = json.loads((base / "candidate/state.schema.json").read_text(encoding="utf-8"))
cases = json.loads((base / "development-cases-v0.1.json").read_text(encoding="utf-8"))

required_skill_markers = [
    "CANDIDATE — NOT QUALIFIED",
    "SAFETY GATE",
    "COMPARABILITY GATE",
    "SINGLE-OBSERVATION GATE",
    "TREND GATE",
    "HISTORY GATE",
    "NORMAL_ADAPTIVE_FATIGUE",
    "LOCAL_MUSCLE_FATIGUE",
    "TRANSIENT_UNDERPERFORMANCE",
    "UNDER_RECOVERY_TREND",
    "SYSTEMIC_FATIGUE_PATTERN",
    "PLATEAU_CANDIDATE",
    "DELOAD_CANDIDATE",
    "MEDICAL_ESCALATION",
    "No mandatory deload every N weeks",
    "proprietary recovery/readiness score",
    "Missing is never silently converted to normal",
]
missing = [x for x in required_skill_markers if x not in skill]
assert not missing, f"missing SKILL markers: {missing}"

assert schema["properties"]["schema_version"]["const"] == "0.1.0"
for required in ["observations","sessions","performance_anchors","interventions"]:
    assert required in schema["required"], required

assert cases["status"] == "public_development_not_heldout"
assert len(cases["cases"]) == 12
ids = {c["id"] for c in cases["cases"]}
assert len(ids) == 12
for c in cases["cases"]:
    assert c["expected"], c["id"]
    assert c["hard_fail"], c["id"]

hard_fail_text = " ".join(" ".join(c["hard_fail"]) for c in cases["cases"]).lower()
for concept in ["one day","wearable","plateau","diagnosis","deload"]:
    assert concept in hard_fail_text, concept

print("TRFM_STATIC_GATE_PASS")
print("cases=12")
print("provider_calls=0")
print("qualification_claim=false")
