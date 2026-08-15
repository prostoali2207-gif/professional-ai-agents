import json
import os
from datetime import datetime, timezone

OUT = "architect/research/benchmark/runs/claim-class-stakes-policy-v0.1.json"

# This is a routing/abstention policy scaffold, not a domain-specific legal/medical standard.
# Thresholds are categorical and intentionally non-probabilistic.

POLICIES = {
    "LEGAL_REGULATORY": {
        "high_stakes": True,
        "required_authority": {"OFFICIAL_LAW", "REGULATOR", "COURT_OR_OFFICIAL_GUIDANCE"},
        "primary_required": True,
        "freshness": "CURRENT_REQUIRED",
        "lifecycle_required": True,
        "independent_replication_required": False,
        "domain_expert_escalation": "WHEN_INTERPRETIVE_OR_JURISDICTIONALLY_AMBIGUOUS",
        "abstain_if": {"NO_CURRENT_OFFICIAL_SOURCE", "JURISDICTION_UNKNOWN", "SOURCE_LIFECYCLE_UNKNOWN"},
    },
    "MEDICAL_SAFETY": {
        "high_stakes": True,
        "required_authority": {"CLINICAL_GUIDELINE", "REGULATOR", "SYSTEMATIC_REVIEW", "PRIMARY_STUDY"},
        "primary_required": False,
        "freshness": "CURRENT_REQUIRED",
        "lifecycle_required": True,
        "independent_replication_required": True,
        "domain_expert_escalation": "WHEN_PATIENT_SPECIFIC_OR_HIGH_RISK",
        "abstain_if": {"ONLY_LOW_QUALITY_SECONDARY", "MATERIAL_CONFLICT_UNRESOLVED", "RETRACTION_STATUS_UNKNOWN_FOR_CRITICAL_STUDY"},
    },
    "ENGINEERING_SAFETY_CRITICAL": {
        "high_stakes": True,
        "required_authority": {"STANDARD", "MANUFACTURER_SPEC", "REGULATOR", "VERIFIED_TEST"},
        "primary_required": True,
        "freshness": "VERSION_MATCH_REQUIRED",
        "lifecycle_required": True,
        "independent_replication_required": True,
        "domain_expert_escalation": "WHEN_FAILURE_CAN_CAUSE_HARM_OR_NONCOMPLIANCE",
        "abstain_if": {"STANDARD_VERSION_UNKNOWN", "ONLY_UNVERIFIED_BLOGS", "TEST_CONFIGURATION_MISMATCH"},
    },
    "SCIENTIFIC_BENCHMARK": {
        "high_stakes": False,
        "required_authority": {"PRIMARY_PAPER", "DATASET_CARD", "BENCHMARK_DOC", "REPRODUCTION"},
        "primary_required": True,
        "freshness": "VERSION_AND_DATE_REQUIRED",
        "lifecycle_required": True,
        "independent_replication_required": True,
        "domain_expert_escalation": "WHEN_METRICS_OR_PROTOCOLS_ARE_NOT_COMPARABLE",
        "abstain_if": {"METRIC_NOT_COMPARABLE", "BENCHMARK_VERSION_UNKNOWN", "ONLY_VENDOR_MARKETING"},
    },
    "CURRENT_PRODUCT_PLATFORM_FACT": {
        "high_stakes": False,
        "required_authority": {"OFFICIAL_DOCS", "OFFICIAL_CHANGELOG", "OFFICIAL_PRICING", "LIVE_PRODUCT"},
        "primary_required": True,
        "freshness": "LIVE_OR_RECENT_REQUIRED",
        "lifecycle_required": True,
        "independent_replication_required": False,
        "domain_expert_escalation": "RARE",
        "abstain_if": {"ONLY_OLD_DOCS", "CURRENT_STATE_NOT_VERIFIED", "PLAN_OR_REGION_AMBIGUOUS"},
    },
    "LOW_STAKES_PRODUCT_HYPOTHESIS": {
        "high_stakes": False,
        "required_authority": {"USER_RESEARCH", "EXPERIMENT", "ANALYTICS", "COMPETITIVE_EVIDENCE"},
        "primary_required": False,
        "freshness": "FIT_FOR_DECISION",
        "lifecycle_required": False,
        "independent_replication_required": False,
        "domain_expert_escalation": "OPTIONAL",
        "abstain_if": {"NO_EMPIRICAL_SIGNAL"},
    },
}

CASES = [
    {"id":"C1-legal-blog-only","claim_class":"LEGAL_REGULATORY","evidence":[{"authority":"BLOG","current":True,"lifecycle":"CURRENT","primary":False}],"context":{"jurisdiction_known":True},"expected":"UNVERIFIED"},
    {"id":"C2-legal-current-regulator","claim_class":"LEGAL_REGULATORY","evidence":[{"authority":"REGULATOR","current":True,"lifecycle":"CURRENT","primary":True}],"context":{"jurisdiction_known":True},"expected":"SUPPORTED"},
    {"id":"C3-medical-single-study-high-risk","claim_class":"MEDICAL_SAFETY","evidence":[{"authority":"PRIMARY_STUDY","current":True,"lifecycle":"CURRENT","primary":True,"lineage":"L1","method":"M1"}],"context":{"patient_specific":True,"high_risk":True},"expected":"PARTIAL"},
    {"id":"C4-engineering-old-standard","claim_class":"ENGINEERING_SAFETY_CRITICAL","evidence":[{"authority":"STANDARD","current":False,"lifecycle":"SUPERSEDED","primary":True,"lineage":"L1","method":"M1"}],"context":{"version_match":False},"expected":"UNVERIFIED"},
    {"id":"C5-scientific-noncomparable-metrics","claim_class":"SCIENTIFIC_BENCHMARK","evidence":[{"authority":"PRIMARY_PAPER","current":True,"lifecycle":"CURRENT","primary":True,"lineage":"L1","method":"M1"},{"authority":"REPRODUCTION","current":True,"lifecycle":"CURRENT","primary":True,"lineage":"L2","method":"M2"}],"context":{"metrics_comparable":False,"benchmark_version_known":True},"expected":"UNVERIFIED"},
    {"id":"C6-current-product-old-community-post","claim_class":"CURRENT_PRODUCT_PLATFORM_FACT","evidence":[{"authority":"COMMUNITY_POST","current":False,"lifecycle":"UNKNOWN","primary":False}],"context":{"current_state_verified":False},"expected":"UNVERIFIED"},
    {"id":"C7-current-product-live-official","claim_class":"CURRENT_PRODUCT_PLATFORM_FACT","evidence":[{"authority":"OFFICIAL_DOCS","current":True,"lifecycle":"CURRENT","primary":True}],"context":{"current_state_verified":True},"expected":"SUPPORTED"},
    {"id":"C8-low-stakes-one-experiment","claim_class":"LOW_STAKES_PRODUCT_HYPOTHESIS","evidence":[{"authority":"EXPERIMENT","current":True,"lifecycle":"CURRENT","primary":True}],"context":{},"expected":"PARTIAL"},
    {"id":"C9-medical-diverse-current","claim_class":"MEDICAL_SAFETY","evidence":[{"authority":"CLINICAL_GUIDELINE","current":True,"lifecycle":"CURRENT","primary":False,"lineage":"L1","method":"M1"},{"authority":"SYSTEMATIC_REVIEW","current":True,"lifecycle":"CURRENT","primary":False,"lineage":"L2","method":"M2"}],"context":{"patient_specific":False,"high_risk":False},"expected":"SUPPORTED"},
]


def evaluate(case):
    cls = case["claim_class"]
    p = POLICIES[cls]
    evidence = case["evidence"]
    ctx = case.get("context", {})

    if cls == "LEGAL_REGULATORY":
        if not ctx.get("jurisdiction_known", False):
            return "UNVERIFIED"
        valid = [e for e in evidence if e["authority"] in p["required_authority"] and e.get("current") and e.get("lifecycle") == "CURRENT"]
        return "SUPPORTED" if valid else "UNVERIFIED"

    if cls == "MEDICAL_SAFETY":
        valid = [e for e in evidence if e["authority"] in p["required_authority"] and e.get("current") and e.get("lifecycle") == "CURRENT"]
        if not valid:
            return "UNVERIFIED"
        if ctx.get("patient_specific") or ctx.get("high_risk"):
            return "PARTIAL"
        lineages = {e.get("lineage") for e in valid if e.get("lineage")}
        methods = {e.get("method") for e in valid if e.get("method")}
        return "SUPPORTED" if len(lineages) >= 2 and len(methods) >= 2 else "PARTIAL"

    if cls == "ENGINEERING_SAFETY_CRITICAL":
        if not ctx.get("version_match", False):
            return "UNVERIFIED"
        valid = [e for e in evidence if e["authority"] in p["required_authority"] and e.get("current") and e.get("lifecycle") == "CURRENT" and e.get("primary")]
        lineages = {e.get("lineage") for e in valid if e.get("lineage")}
        methods = {e.get("method") for e in valid if e.get("method")}
        return "SUPPORTED" if len(valid) >= 2 and len(lineages) >= 2 and len(methods) >= 2 else ("PARTIAL" if valid else "UNVERIFIED")

    if cls == "SCIENTIFIC_BENCHMARK":
        if not ctx.get("metrics_comparable", False) or not ctx.get("benchmark_version_known", False):
            return "UNVERIFIED"
        valid = [e for e in evidence if e["authority"] in p["required_authority"] and e.get("current") and e.get("lifecycle") == "CURRENT"]
        lineages = {e.get("lineage") for e in valid if e.get("lineage")}
        methods = {e.get("method") for e in valid if e.get("method")}
        return "SUPPORTED" if len(lineages) >= 2 and len(methods) >= 2 else ("PARTIAL" if valid else "UNVERIFIED")

    if cls == "CURRENT_PRODUCT_PLATFORM_FACT":
        if not ctx.get("current_state_verified", False):
            return "UNVERIFIED"
        valid = [e for e in evidence if e["authority"] in p["required_authority"] and e.get("current") and e.get("lifecycle") == "CURRENT"]
        return "SUPPORTED" if valid else "UNVERIFIED"

    if cls == "LOW_STAKES_PRODUCT_HYPOTHESIS":
        valid = [e for e in evidence if e["authority"] in p["required_authority"]]
        return "PARTIAL" if valid else "UNVERIFIED"

    return "UNVERIFIED"


def json_safe(value):
    if isinstance(value, set):
        return sorted(value)
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    return value


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    rows = []
    for case in CASES:
        got = evaluate(case)
        rows.append({"id":case["id"],"claim_class":case["claim_class"],"expected":case["expected"],"got":got,"passed":got == case["expected"]})

    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gate": "claim-class-stakes-policy-v0.1",
        "scope": "architectural routing/abstention scaffold; not domain-specific professional advice",
        "policies": json_safe(POLICIES),
        "cases": rows,
        "expert_gap_discovery": [
            "Claim class alone is insufficient: jurisdiction, user-specificity, reversibility, harm severity, and decision horizon also affect evidence requirements.",
            "A strong practitioner will distinguish authoritative source identity from interpretation quality.",
            "High-stakes claims may require licensed/domain-expert escalation even when evidence retrieval succeeds.",
            "Freshness must be expressed as lifecycle/version requirements, not arbitrary age cutoffs.",
            "The policy must support domain-specific plug-ins or profiles rather than encode one universal threshold table."
        ],
        "red_team": {
            "senior_researcher": "Would reject universal evidence thresholds that ignore study design quality and domain conventions.",
            "information_retrieval_engineer": "Would note that retrieval confidence cannot substitute for source adequacy or claim-type fit.",
            "evaluation_scientist": "Would require calibrated, adjudicated test cases before treating these categories as validated across domains.",
            "security_engineer": "Would require that high-stakes escalation cannot be bypassed by malicious source metadata claiming a lower-stakes class."
        },
        "status": "PASS" if all(r["passed"] for r in rows) else "FAIL"
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
