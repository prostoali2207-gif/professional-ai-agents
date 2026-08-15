import json
import os
from datetime import datetime, timezone

OUT = "architect/research/benchmark/runs/research-stopping-evidence-gap-policy-v0.1.json"

CASES = [
    {"id":"S1-high-stakes-missing-primary","claim_state":"PARTIAL","high_stakes":True,"gaps":["PRIMARY_SOURCE_MISSING"],"next_action_value":"HIGH","expected":"CONTINUE"},
    {"id":"S2-live-conflict","claim_state":"CONFLICTED","high_stakes":False,"gaps":["MATERIAL_CONFLICT_UNRESOLVED"],"next_action_value":"HIGH","expected":"CONTINUE"},
    {"id":"S3-lifecycle-unknown-current-fact","claim_state":"PARTIAL","high_stakes":False,"gaps":["LIFECYCLE_UNKNOWN"],"next_action_value":"MEDIUM","expected":"CONTINUE"},
    {"id":"S4-supported-no-open-gap","claim_state":"SUPPORTED","high_stakes":False,"gaps":[],"next_action_value":"LOW","expected":"STOP"},
    {"id":"S5-duplicate-more-sources","claim_state":"SUPPORTED","high_stakes":False,"gaps":["ONLY_MORE_SAME_LINEAGE_AVAILABLE"],"next_action_value":"LOW","expected":"STOP"},
    {"id":"S6-low-stakes-partial-no-signal","claim_state":"PARTIAL","high_stakes":False,"gaps":["NO_EMPIRICAL_SIGNAL"],"next_action_value":"LOW","expected":"STOP_WITH_LIMITATION"},
    {"id":"S7-quota-blocked-noncritical","claim_state":"PARTIAL","high_stakes":False,"gaps":["OPTIONAL_REPLICATION"],"next_action_value":"MEDIUM","resource_state":"QUOTA_BLOCKED","expected":"STOP_WITH_LIMITATION"},
    {"id":"S8-quota-blocked-critical","claim_state":"PARTIAL","high_stakes":True,"gaps":["PRIMARY_SOURCE_MISSING"],"next_action_value":"HIGH","resource_state":"QUOTA_BLOCKED","expected":"ESCALATE_OR_DEFER"},
    {"id":"S9-unverified-but-clarification-needed","claim_state":"UNVERIFIED","high_stakes":False,"gaps":["JURISDICTION_UNKNOWN"],"next_action_value":"NONE","expected":"CLARIFY_FIRST"},
    {"id":"S10-repeated-provider-failure","claim_state":"PARTIAL","high_stakes":False,"gaps":["OPTIONAL_REPLICATION"],"next_action_value":"LOW","provider_failures":3,"expected":"STOP_WITH_LIMITATION"},
]

MANDATORY_CONTINUE_GAPS = {"PRIMARY_SOURCE_MISSING", "MATERIAL_CONFLICT_UNRESOLVED", "LIFECYCLE_UNKNOWN", "CRITICAL_RETRACTION_STATUS_UNKNOWN"}
CLARIFY_GAPS = {"JURISDICTION_UNKNOWN", "USER_CONTEXT_REQUIRED", "TARGET_VERSION_UNKNOWN"}
LOW_VALUE_GAPS = {"ONLY_MORE_SAME_LINEAGE_AVAILABLE", "OPTIONAL_REPLICATION", "NO_EMPIRICAL_SIGNAL"}


def decide(c):
    gaps = set(c.get("gaps", []))
    high = c.get("high_stakes", False)
    resource = c.get("resource_state", "AVAILABLE")
    failures = c.get("provider_failures", 0)
    value = c.get("next_action_value", "LOW")

    if gaps & CLARIFY_GAPS:
        return "CLARIFY_FIRST"

    critical_gap = bool(gaps & MANDATORY_CONTINUE_GAPS)
    if resource == "QUOTA_BLOCKED":
        return "ESCALATE_OR_DEFER" if (high and critical_gap) else "STOP_WITH_LIMITATION"

    if failures >= 3 and not (high and critical_gap):
        return "STOP_WITH_LIMITATION"

    if critical_gap:
        return "CONTINUE"

    if c.get("claim_state") == "SUPPORTED" and (not gaps or gaps <= LOW_VALUE_GAPS):
        return "STOP"

    if value == "LOW" or gaps <= LOW_VALUE_GAPS:
        return "STOP_WITH_LIMITATION" if c.get("claim_state") != "SUPPORTED" else "STOP"

    return "CONTINUE"


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    rows=[]
    for c in CASES:
        got=decide(c)
        rows.append({"id":c["id"],"expected":c["expected"],"got":got,"passed":got==c["expected"]})
    result={
        "timestamp_utc":datetime.now(timezone.utc).isoformat(),
        "gate":"research-stopping-evidence-gap-policy-v0.1",
        "principles":[
            "Stop decisions are gap-based, not source-count based.",
            "Continue only when a next action can close a material evidence gap.",
            "Distinct URLs from the same lineage do not justify continued search.",
            "High-stakes unresolved primary/lifecycle/conflict gaps cannot be hidden by cost limits; escalate or defer instead.",
            "Quota/capacity/provider failures are operational states, not evidence failures.",
            "Clarification can dominate retrieval when required context is missing.",
            "No synthetic marginal-value probability is claimed; action value is categorical until empirically calibrated."
        ],
        "cases":rows,
        "status":"PASS" if all(r["passed"] for r in rows) else "FAIL"
    }
    with open(OUT,"w",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["status"]!="PASS":
        raise SystemExit(2)

if __name__=="__main__":
    main()
