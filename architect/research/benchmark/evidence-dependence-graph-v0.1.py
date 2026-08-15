import json
import os
from datetime import datetime, timezone
from itertools import combinations

OUT = "architect/research/benchmark/runs/evidence-dependence-graph-v0.1.json"

EVIDENCE = [
    {"id":"e1","dataset":"D1","population":"US-enterprise","time_window":"2026-H1","pipeline":"telemetry-A","annotators":"team-x","benchmark":"B1","synthetic_model":None},
    {"id":"e2","dataset":"D1","population":"US-enterprise","time_window":"2026-H1","pipeline":"telemetry-A","annotators":"team-y","benchmark":"B1","synthetic_model":None},
    {"id":"e3","dataset":"D2","population":"US-enterprise","time_window":"2026-H1","pipeline":"survey-B","annotators":"team-z","benchmark":None,"synthetic_model":None},
    {"id":"e4","dataset":"D3","population":"EU-consumer","time_window":"2025-H2","pipeline":"experiment-C","annotators":"team-q","benchmark":None,"synthetic_model":None},
    {"id":"e5","dataset":None,"population":None,"time_window":None,"pipeline":None,"annotators":None,"benchmark":None,"synthetic_model":None},
    {"id":"e6","dataset":"D4","population":"global-web","time_window":"2026-Q1","pipeline":"eval-D","annotators":"team-r","benchmark":"B2","synthetic_model":"model-Z"},
    {"id":"e7","dataset":"D5","population":"global-web","time_window":"2026-Q1","pipeline":"eval-E","annotators":"team-s","benchmark":"B2","synthetic_model":"model-Z"},
]

FIELDS = {
    "dataset": 1.0,
    "pipeline": 0.9,
    "benchmark": 0.8,
    "synthetic_model": 0.8,
    "population": 0.5,
    "time_window": 0.4,
    "annotators": 0.4,
}


def edge(a, b):
    shared = []
    score = 0.0
    known = 0
    for field, weight in FIELDS.items():
        av, bv = a.get(field), b.get(field)
        if av is not None and bv is not None:
            known += 1
            if av == bv:
                shared.append({"factor": field, "value": av, "weight": weight})
                score += weight
    if known == 0:
        return {"a": a["id"], "b": b["id"], "status": "UNKNOWN", "confidence": 0.0, "strength": None, "shared": []}
    max_score = sum(FIELDS.values())
    norm = round(score / max_score, 3)
    if score >= 1.7:
        status, strength = "DEPENDENT", "HIGH"
    elif score > 0:
        status, strength = "PARTIALLY_DEPENDENT", "MEDIUM" if score >= 0.8 else "LOW"
    else:
        status, strength = "NO_COMMON_CAUSE_OBSERVED", "NONE"
    confidence = round(min(1.0, known / len(FIELDS)), 3)
    return {"a": a["id"], "b": b["id"], "status": status, "confidence": confidence, "strength": strength, "shared": shared, "normalized_overlap": norm}


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    edges = [edge(a,b) for a,b in combinations(EVIDENCE,2)]
    by_pair = {(e["a"],e["b"]):e for e in edges}
    expectations = [
        (("e1","e2"), "DEPENDENT"),
        (("e1","e3"), "PARTIALLY_DEPENDENT"),
        (("e1","e4"), "NO_COMMON_CAUSE_OBSERVED"),
        (("e1","e5"), "UNKNOWN"),
        (("e6","e7"), "DEPENDENT"),
    ]
    checks=[]
    for pair, expected in expectations:
        got = by_pair[pair]["status"]
        checks.append({"pair":pair,"expected":expected,"got":got,"passed":got==expected})
    unknown_not_independent = by_pair[("e1","e5")]["status"] == "UNKNOWN"
    checks.append({"check":"unknown metadata is not promoted to independence","passed":unknown_not_independent})
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gate":"evidence-dependence-graph-v0.1",
        "rules":[
            "Source-lineage independence and methodological independence are separate.",
            "Dependence is represented as pairwise edges with explicit causes, strength, and confidence.",
            "Unknown metadata remains UNKNOWN.",
            "Shared benchmark/model/dataset can create common-cause dependence even across different organizations.",
            "Absence of observed overlap is not proof of causal independence when metadata coverage is low."
        ],
        "nodes":EVIDENCE,
        "edges":edges,
        "checks":checks,
        "status":"PASS" if all(c["passed"] for c in checks) else "FAIL"
    }
    with open(OUT,"w",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["status"] != "PASS":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
