from __future__ import annotations
import json, pathlib, sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
base = root / "architect/evaluation/training-recovery-fatigue-management"
skill = (base / "candidate/SKILL.md").read_text(encoding="utf-8")
evidence = (root / "architect/research/training-recovery-fatigue-management/evidence-register-v0.2.md").read_text(encoding="utf-8")
overlay = (root / "architect/research/training-recovery-fatigue-management/professional-repair-overlay-v0.1.1.md").read_text(encoding="utf-8")
schema = json.loads((base / "candidate/state.schema.json").read_text(encoding="utf-8"))
cases = json.loads((base / "development-cases-v0.1.1.json").read_text(encoding="utf-8"))

required_skill_markers = [
    "version: 0.1.1-candidate",
    "evidence-register-v0.2.md",
    "professional-repair-overlay-v0.1.1.md",
    "SINGLE-OBSERVATION GATE",
    "TREND GATE",
    "Soreness does not quantify muscle damage reliably and does not prove hypertrophy",
    "A numeric one-item fatigue/readiness/wellness value is not assumed to be validated or physiologically calibrated",
    "proprietary recovery/readiness score",
    "MEDICAL_ESCALATION",
]
missing = [x for x in required_skill_markers if x not in skill]
assert not missing, f"missing skill markers: {missing}"

for marker in ["PMID: 32957081","PMID: 29282529","DOI: 10.5432/ijshs.1.1"]:
    assert marker in evidence, marker
for marker in ["Subjective monitoring calibration","Soreness interpretation"]:
    assert marker in overlay, marker

assert schema["properties"]["schema_version"]["const"] == "0.1.0"
for required in ["observations","sessions","performance_anchors","load_history","interventions"]:
    assert required in schema["required"], required

assert cases["schema_version"] == "0.1.1"
assert cases["status"] == "public_development_not_heldout"
assert len(cases["cases"]) == 14
ids = {c["id"] for c in cases["cases"]}
assert len(ids) == 14 and {"D13","D14"} <= ids
for c in cases["cases"]:
    assert c["expected"] and c["hard_fail"], c["id"]

text = " ".join(" ".join(c["hard_fail"]) for c in cases["cases"]).lower()
for concept in ["one day","device score","plateau","diagnosis","deload","single-item","soreness"]:
    assert concept in text, concept

print("TRFM_V011_STATIC_GATE_PASS")
print("cases=14")
print("provider_calls=0")
print("qualification_claim=false")
