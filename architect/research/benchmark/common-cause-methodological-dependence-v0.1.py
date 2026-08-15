import json
import os
from datetime import datetime, timezone

OUT = "architect/research/benchmark/runs/common-cause-methodological-dependence-v0.1.json"

DIMENSIONS = [
    "dataset",
    "measurement_pipeline",
    "population_geography",
    "funding_vendor_ecosystem",
    "time_window",
    "method_family",
]

FIXTURES = [
    {
        "case_id": "M1_SHARED_DATASET",
        "expected": "DEPENDENT",
        "sources": [
            {"id":"a","lineage":"L1","dataset":"D1","measurement_pipeline":"P1","population_geography":"US","funding_vendor_ecosystem":"independent","time_window":"2025Q1","method_family":"survey"},
            {"id":"b","lineage":"L2","dataset":"D1","measurement_pipeline":"P2","population_geography":"US","funding_vendor_ecosystem":"independent","time_window":"2025Q1","method_family":"regression"},
        ],
    },
    {
        "case_id": "M2_SHARED_VENDOR_TELEMETRY",
        "expected": "DEPENDENT",
        "sources": [
            {"id":"a","lineage":"L1","dataset":"vendor-telemetry-A","measurement_pipeline":"vendor-sdk-A","population_geography":"global-customers-A","funding_vendor_ecosystem":"vendor-A","time_window":"2026H1","method_family":"observational"},
            {"id":"b","lineage":"L2","dataset":"vendor-telemetry-A","measurement_pipeline":"vendor-sdk-A","population_geography":"global-customers-A","funding_vendor_ecosystem":"vendor-A","time_window":"2026H1","method_family":"observational"},
            {"id":"c","lineage":"L3","dataset":"vendor-telemetry-A","measurement_pipeline":"vendor-sdk-A","population_geography":"global-customers-A","funding_vendor_ecosystem":"vendor-A","time_window":"2026H1","method_family":"forecast"},
        ],
    },
    {
        "case_id": "M3_METHOD_DIVERSE",
        "expected": "INDEPENDENT",
        "sources": [
            {"id":"a","lineage":"L1","dataset":"gov-admin","measurement_pipeline":"agency-records","population_geography":"US","funding_vendor_ecosystem":"public","time_window":"2025","method_family":"administrative"},
            {"id":"b","lineage":"L2","dataset":"panel-B","measurement_pipeline":"survey-B","population_geography":"EU","funding_vendor_ecosystem":"academic","time_window":"2025","method_family":"survey"},
            {"id":"c","lineage":"L3","dataset":"experiment-C","measurement_pipeline":"lab-C","population_geography":"multi-country","funding_vendor_ecosystem":"academic","time_window":"2026","method_family":"experiment"},
        ],
    },
    {
        "case_id": "M4_UNKNOWN",
        "expected": "UNKNOWN",
        "sources": [
            {"id":"a","lineage":"L1","dataset":None,"measurement_pipeline":None,"population_geography":"global","funding_vendor_ecosystem":None,"time_window":"2026","method_family":"forecast"},
            {"id":"b","lineage":"L2","dataset":None,"measurement_pipeline":None,"population_geography":"global","funding_vendor_ecosystem":None,"time_window":"2026","method_family":"forecast"},
        ],
    },
    {
        "case_id": "M5_SHARED_POPULATION_ONLY",
        "expected": "PARTIALLY_DEPENDENT",
        "sources": [
            {"id":"a","lineage":"L1","dataset":"D1","measurement_pipeline":"P1","population_geography":"UAE-enterprise-customers","funding_vendor_ecosystem":"vendor-A","time_window":"2026Q1","method_family":"survey"},
            {"id":"b","lineage":"L2","dataset":"D2","measurement_pipeline":"P2","population_geography":"UAE-enterprise-customers","funding_vendor_ecosystem":"vendor-B","time_window":"2026Q1","method_family":"interviews"},
        ],
    },
]


def classify(sources):
    # Unknown if core provenance dimensions are missing across all sources.
    core = ["dataset", "measurement_pipeline", "funding_vendor_ecosystem"]
    if all(all(s.get(k) is None for k in core) for s in sources):
        return "UNKNOWN", {"reason": "core dependence dimensions unavailable"}

    shared = {}
    for d in DIMENSIONS:
        vals = [s.get(d) for s in sources if s.get(d) is not None]
        if len(vals) >= 2 and len(set(vals)) == 1:
            shared[d] = vals[0]

    hard = {"dataset", "measurement_pipeline", "funding_vendor_ecosystem"}
    if hard.intersection(shared):
        return "DEPENDENT", {"shared": shared}

    softer = {"population_geography", "time_window", "method_family"}
    if softer.intersection(shared):
        return "PARTIALLY_DEPENDENT", {"shared": shared}

    return "INDEPENDENT", {"shared": shared}


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gate": "common-cause-methodological-dependence-v0.1",
        "rules": [
            "Publication/source lineage independence does not imply methodological independence.",
            "Shared dataset, measurement pipeline, or vendor ecosystem creates common-cause dependence.",
            "Shared population/time/method family reduces diversity even when datasets differ.",
            "Unknown dependence metadata remains UNKNOWN rather than defaulting to INDEPENDENT.",
            "Evidence synthesis must report both lineage independence and methodological dependence state."
        ],
        "cases": [],
    }
    failures=[]
    for case in FIXTURES:
        got, detail = classify(case["sources"])
        row={
            "case_id":case["case_id"],
            "expected":case["expected"],
            "got":got,
            "passed":got==case["expected"],
            "detail":detail,
            "sources":case["sources"],
        }
        record["cases"].append(row)
        if not row["passed"]:
            failures.append(row)
    record["failures"]=failures
    record["status"]="PASS" if not failures else "FAIL"
    with open(OUT,"w",encoding="utf-8") as f:
        json.dump(record,f,ensure_ascii=False,indent=2)
    print(json.dumps(record,ensure_ascii=False,indent=2))
    if failures:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
