import json
import os
from datetime import datetime, timezone

OUT = "architect/research/benchmark/runs/decomposition-query-budget-policy-v0.1.json"

CASES = [
    {
        "id":"Q1-product-legal-shared-source",
        "claims":[
            {"id":"c1","route":"CURRENT_PRODUCT_PLATFORM_FACT","topic":"data-residency","source_family":"vendor-docs","action":"MUST_RESEARCH"},
            {"id":"c2","route":"LEGAL_REGULATORY","topic":"hr-lawfulness","source_family":"law-regulator","action":"MUST_RESEARCH"},
            {"id":"c3","route":"LEGAL_REGULATORY","topic":"dpa-change","source_family":"law-regulator","action":"SHARE_RETRIEVAL_WITH:c2"},
        ],
        "expected_external_queries":2,
    },
    {
        "id":"Q2-benchmark-derived-comparison",
        "claims":[
            {"id":"c1","route":"SCIENTIFIC_BENCHMARK","topic":"model-a-score","source_family":"benchmark-x","action":"MUST_RESEARCH"},
            {"id":"c2","route":"SCIENTIFIC_BENCHMARK","topic":"model-b-score","source_family":"benchmark-y","action":"MUST_RESEARCH"},
            {"id":"c3","route":"SCIENTIFIC_BENCHMARK","topic":"comparability","source_family":"derived","action":"DERIVE_AFTER_RETRIEVAL"},
            {"id":"c4","route":"SCIENTIFIC_BENCHMARK","topic":"overall-superiority","source_family":"derived","action":"DERIVE_AFTER_RETRIEVAL"},
        ],
        "expected_external_queries":2,
    },
    {
        "id":"Q3-unknown-jurisdiction",
        "claims":[
            {"id":"c1","route":"LEGAL_REGULATORY","topic":"retention","source_family":"law-regulator","action":"CLARIFY_FIRST"},
        ],
        "expected_external_queries":0,
    },
    {
        "id":"Q4-medical-no-fragmentation",
        "claims":[
            {"id":"c1","route":"MEDICAL_SAFETY","topic":"efficacy","source_family":"clinical-evidence","action":"MUST_RESEARCH"},
            {"id":"c2","route":"MEDICAL_SAFETY","topic":"drug-interaction","source_family":"clinical-evidence","action":"SHARE_RETRIEVAL_WITH:c1"},
            {"id":"c3","route":"MEDICAL_SAFETY","topic":"dose-action","source_family":"clinical-guidance","action":"MUST_RESEARCH"},
        ],
        "expected_external_queries":2,
    },
    {
        "id":"Q5-current-price-and-arithmetic",
        "claims":[
            {"id":"c1","route":"CURRENT_PRODUCT_PLATFORM_FACT","topic":"price","source_family":"official-pricing","action":"MUST_RESEARCH"},
            {"id":"c2","route":"LOW_STAKES_PRODUCT_HYPOTHESIS","topic":"20-percent-savings","source_family":"derived","action":"DERIVE_AFTER_RETRIEVAL"},
        ],
        "expected_external_queries":1,
    },
]


def plan(case):
    queries=[]
    shared=[]
    derived=[]
    clarify=[]
    for c in case["claims"]:
        a=c["action"]
        if a=="MUST_RESEARCH":
            queries.append(c["id"])
        elif a.startswith("SHARE_RETRIEVAL_WITH:"):
            shared.append({"claim":c["id"],"with":a.split(":",1)[1]})
        elif a=="DERIVE_AFTER_RETRIEVAL":
            derived.append(c["id"])
        elif a=="CLARIFY_FIRST":
            clarify.append(c["id"])
    return {"queries":queries,"shared":shared,"derived":derived,"clarify_first":clarify,"external_query_count":len(queries)}


def main():
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    rows=[]
    for case in CASES:
        p=plan(case)
        rows.append({"id":case["id"],"expected_external_queries":case["expected_external_queries"],"plan":p,"passed":p["external_query_count"]==case["expected_external_queries"]})

    # Negative control: naive one-query-per-claim overqueries every multi-claim case with derived/shared work.
    naive=[]
    for case in CASES:
        naive_count=len(case["claims"])
        optimal=case["expected_external_queries"]
        naive.append({"id":case["id"],"naive_count":naive_count,"budgeted_count":optimal,"overquery":naive_count>optimal})

    # High-stakes recall control: no HIGH-risk MUST_RESEARCH claim may be suppressed as a cost optimization.
    high_stakes_control = {
        "medical_action_research_preserved": "c3" in plan(CASES[3])["queries"],
        "legal_research_preserved": "c2" in plan(CASES[0])["queries"],
    }
    status="PASS" if all(r["passed"] for r in rows) and all(high_stakes_control.values()) else "FAIL"
    result={
        "timestamp_utc":datetime.now(timezone.utc).isoformat(),
        "gate":"decomposition-query-budget-policy-v0.1",
        "scope":"deterministic planning contract; empirical retrieval-quality/cost frontier not yet calibrated",
        "rules":[
            "Atomic claims do not imply one external query per claim.",
            "Claims sharing source family and scope may share retrieval while preserving separate adjudication.",
            "Derived comparisons/calculations run after evidence retrieval instead of triggering duplicate search.",
            "Missing routing-critical context triggers clarification before expensive retrieval.",
            "Cost optimization may not suppress a high-stakes must-research claim.",
            "Query budget is a ceiling/plan, not a reason to stop before evidence adequacy is reached."
        ],
        "cases":rows,
        "naive_query_comparison":naive,
        "high_stakes_control":high_stakes_control,
        "status":status,
        "expert_gap_discovery":[
            "The optimal grouping depends on retriever recall, query length, corpus structure, and provider pricing.",
            "Over-grouping can reduce recall just as over-decomposition can increase cost.",
            "A real planner needs a marginal-value stopping rule based on evidence gaps, not a fixed query count."
        ],
        "red_team":{
            "senior_researcher":"Would reject a budget that terminates research before contradictory or primary evidence is checked.",
            "information_retrieval_engineer":"Would require empirical recall/precision curves for grouped versus split queries.",
            "evaluation_scientist":"Would require cost-normalized task utility on hidden holdouts.",
            "security_engineer":"Would ensure hostile content cannot manufacture new queries or override the pre-retrieval budget."
        }
    }
    with open(OUT,"w",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if status!="PASS":
        raise SystemExit(2)

if __name__=="__main__":
    main()
