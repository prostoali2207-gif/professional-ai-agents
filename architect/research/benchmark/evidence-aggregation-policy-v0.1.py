import json
import os
from datetime import datetime, timezone

OUT = "architect/research/benchmark/runs/evidence-aggregation-policy-v0.1.json"

# This gate intentionally avoids probabilistic confidence scores.
# It evaluates claim-state transitions from evidence properties.

CASES = [
    {
        "id": "A1-independent-support",
        "evidence": [
            {"id":"e1","stance":"SUPPORT","status":"VALID","authority":"PRIMARY","lineage":"L1","method_group":"M1","metadata":"SUFFICIENT"},
            {"id":"e2","stance":"SUPPORT","status":"VALID","authority":"PRIMARY","lineage":"L2","method_group":"M2","metadata":"SUFFICIENT"},
        ],
        "expected": "SUPPORTED",
        "reason": "two valid, independent, methodologically distinct primary lines",
    },
    {
        "id": "A2-dependent-replication",
        "evidence": [
            {"id":"e1","stance":"SUPPORT","status":"VALID","authority":"PRIMARY","lineage":"L1","method_group":"M1","metadata":"SUFFICIENT"},
            {"id":"e2","stance":"SUPPORT","status":"VALID","authority":"SECONDARY","lineage":"L1","method_group":"M1","metadata":"SUFFICIENT"},
            {"id":"e3","stance":"SUPPORT","status":"VALID","authority":"SECONDARY","lineage":"L1","method_group":"M1","metadata":"SUFFICIENT"},
        ],
        "expected": "PARTIAL",
        "reason": "three URLs but one evidentiary lineage/methodological root",
    },
    {
        "id": "A3-direct-conflict",
        "evidence": [
            {"id":"e1","stance":"SUPPORT","status":"VALID","authority":"PRIMARY","lineage":"L1","method_group":"M1","metadata":"SUFFICIENT"},
            {"id":"e2","stance":"CONTRADICT","status":"VALID","authority":"PRIMARY","lineage":"L2","method_group":"M2","metadata":"SUFFICIENT"},
        ],
        "expected": "CONFLICTED",
        "reason": "independent valid primary evidence directly conflicts",
    },
    {
        "id": "A4-retracted-support",
        "evidence": [
            {"id":"e1","stance":"SUPPORT","status":"RETRACTED","authority":"PRIMARY","lineage":"L1","method_group":"M1","metadata":"SUFFICIENT"},
            {"id":"e2","stance":"SUPPORT","status":"VALID","authority":"SECONDARY","lineage":"L1","method_group":"M1","metadata":"SUFFICIENT"},
        ],
        "expected": "UNVERIFIED",
        "reason": "support lineage is invalidated by retraction; descendants cannot rescue it",
    },
    {
        "id": "A5-missing-dependence-metadata",
        "evidence": [
            {"id":"e1","stance":"SUPPORT","status":"VALID","authority":"PRIMARY","lineage":"UNKNOWN","method_group":"UNKNOWN","metadata":"INSUFFICIENT"},
            {"id":"e2","stance":"SUPPORT","status":"VALID","authority":"PRIMARY","lineage":"UNKNOWN","method_group":"UNKNOWN","metadata":"INSUFFICIENT"},
        ],
        "expected": "PARTIAL",
        "reason": "multiple supporting sources but independence cannot be established",
    },
    {
        "id": "A6-superseded-current",
        "evidence": [
            {"id":"e1","stance":"SUPPORT","status":"SUPERSEDED","authority":"PRIMARY","lineage":"L1","method_group":"M1","metadata":"SUFFICIENT"},
            {"id":"e2","stance":"CONTRADICT","status":"VALID","authority":"PRIMARY","lineage":"L2","method_group":"M2","metadata":"SUFFICIENT","lifecycle":"CURRENT"},
        ],
        "expected": "CONTRADICTED",
        "reason": "superseded support does not create a live conflict with current primary evidence",
    },
    {
        "id": "A7-secondary-only",
        "evidence": [
            {"id":"e1","stance":"SUPPORT","status":"VALID","authority":"SECONDARY","lineage":"L1","method_group":"M1","metadata":"SUFFICIENT"},
            {"id":"e2","stance":"SUPPORT","status":"VALID","authority":"SECONDARY","lineage":"L2","method_group":"M2","metadata":"SUFFICIENT"},
        ],
        "expected": "PARTIAL",
        "reason": "independent secondary evidence can support discovery but not primary-source verification",
    },
]

INVALID_STATUSES = {"RETRACTED", "SUPERSEDED", "WITHDRAWN"}
HARD_LINEAGE_INVALIDATORS = {"RETRACTED", "WITHDRAWN"}


def aggregate(evidence):
    invalidated_support_lineages = {
        e.get("lineage")
        for e in evidence
        if e.get("stance") == "SUPPORT"
        and e.get("authority") == "PRIMARY"
        and e.get("status") in HARD_LINEAGE_INVALIDATORS
        and e.get("lineage") not in {None, "UNKNOWN"}
    }

    live = [
        e for e in evidence
        if e.get("status") == "VALID"
        and not (
            e.get("stance") == "SUPPORT"
            and e.get("lineage") in invalidated_support_lineages
        )
    ]
    invalid_support = [e for e in evidence if e.get("stance") == "SUPPORT" and e.get("status") in INVALID_STATUSES]

    support = [e for e in live if e.get("stance") == "SUPPORT"]
    contradict = [e for e in live if e.get("stance") == "CONTRADICT"]

    # A current contradiction against only superseded/withdrawn/retracted support is not a live conflict.
    if contradict and not support and invalid_support:
        return "CONTRADICTED"

    if support and contradict:
        return "CONFLICTED"

    if contradict and not support:
        return "CONTRADICTED"

    if not support:
        return "UNVERIFIED"

    # Independence cannot be invented from missing metadata.
    if any(e.get("metadata") != "SUFFICIENT" or e.get("lineage") == "UNKNOWN" or e.get("method_group") == "UNKNOWN" for e in support):
        return "PARTIAL"

    primary_support = [e for e in support if e.get("authority") == "PRIMARY"]
    if not primary_support:
        return "PARTIAL"

    lineage_roots = {e.get("lineage") for e in primary_support}
    method_roots = {e.get("method_group") for e in primary_support}

    if len(lineage_roots) >= 2 and len(method_roots) >= 2:
        return "SUPPORTED"

    return "PARTIAL"


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    rows = []
    for case in CASES:
        got = aggregate(case["evidence"])
        rows.append({
            "id": case["id"],
            "expected": case["expected"],
            "got": got,
            "passed": got == case["expected"],
            "reason": case["reason"],
        })

    forbidden_numeric_confidence = True
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gate": "evidence-aggregation-policy-v0.1",
        "policy": {
            "claim_states": ["SUPPORTED", "PARTIAL", "CONFLICTED", "CONTRADICTED", "UNVERIFIED"],
            "no_numeric_confidence": forbidden_numeric_confidence,
            "rules": [
                "Count independent evidentiary roots, not URLs.",
                "Do not treat dependent republishing as replication.",
                "Do not combine live contradictory primary evidence into a single consensus claim.",
                "Retracted/withdrawn primary support invalidates dependent supporting descendants in the same lineage.",
                "Superseded evidence is excluded from current support but does not automatically invalidate historical descendants outside the current-claim context.",
                "Unknown lineage or methodological metadata cannot be promoted to independence.",
                "Secondary-only support is PARTIAL when primary verification is required.",
                "No synthetic probability or pseudo-precision is produced by this gate."
            ],
        },
        "cases": rows,
        "status": "PASS" if all(r["passed"] for r in rows) else "FAIL",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
