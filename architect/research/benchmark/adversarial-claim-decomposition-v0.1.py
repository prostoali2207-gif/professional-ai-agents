import json
import os
from datetime import datetime, timezone

OUT = "architect/research/benchmark/runs/adversarial-claim-decomposition-v0.1.json"

# This gate validates decomposition completeness contracts on frozen, adjudicated cases.
# It is NOT a validated natural-language semantic parser.

CASES = [
    {
        "id": "D1-product-plus-legal",
        "request": "Does this API plan include EU data residency, and can we use it for employee HR records in Germany without changing our DPA?",
        "gold_claims": [
            {"key":"plan_residency","class":"CURRENT_PRODUCT_PLATFORM_FACT","stakes":"MEDIUM","qualifiers":["EU","current plan"]},
            {"key":"lawful_hr_use","class":"LEGAL_REGULATORY","stakes":"HIGH","qualifiers":["Germany","employee HR records","without changing DPA"]},
        ],
        "candidate_claims": [
            {"key":"plan_residency","class":"CURRENT_PRODUCT_PLATFORM_FACT","stakes":"MEDIUM","qualifiers":["EU","current plan"]},
            {"key":"lawful_hr_use","class":"LEGAL_REGULATORY","stakes":"HIGH","qualifiers":["Germany","employee HR records","without changing DPA"]},
        ],
    },
    {
        "id": "D2-medical-action-hidden",
        "request": "This supplement says it lowers blood pressure. My father takes antihypertensives; is it okay if he doubles the dose for a week to test whether it works faster?",
        "gold_claims": [
            {"key":"efficacy_claim","class":"MEDICAL_SAFETY","stakes":"HIGH","qualifiers":["blood pressure"]},
            {"key":"interaction_risk","class":"MEDICAL_SAFETY","stakes":"HIGH","qualifiers":["antihypertensives","father"]},
            {"key":"dose_change_action","class":"MEDICAL_SAFETY","stakes":"HIGH","qualifiers":["double dose","one week","faster"]},
        ],
        "candidate_claims": [
            {"key":"efficacy_claim","class":"MEDICAL_SAFETY","stakes":"HIGH","qualifiers":["blood pressure"]},
            {"key":"interaction_risk","class":"MEDICAL_SAFETY","stakes":"HIGH","qualifiers":["antihypertensives","father"]},
            {"key":"dose_change_action","class":"MEDICAL_SAFETY","stakes":"HIGH","qualifiers":["double dose","one week","faster"]},
        ],
    },
    {
        "id": "D3-engineering-conditional",
        "request": "The bracket passed a 5 kN lab test. If we use it outdoors at -20 C on a lifting assembly, can we rate it for 5 kN?",
        "gold_claims": [
            {"key":"lab_test_result","class":"ENGINEERING_SAFETY_CRITICAL","stakes":"HIGH","qualifiers":["5 kN","lab test"]},
            {"key":"field_rating","class":"ENGINEERING_SAFETY_CRITICAL","stakes":"HIGH","qualifiers":["outdoors","-20 C","lifting assembly","5 kN"]},
            {"key":"test_to_field_comparability","class":"ENGINEERING_SAFETY_CRITICAL","stakes":"HIGH","qualifiers":["lab to field","environment/configuration"]},
        ],
        "candidate_claims": [
            {"key":"lab_test_result","class":"ENGINEERING_SAFETY_CRITICAL","stakes":"HIGH","qualifiers":["5 kN","lab test"]},
            {"key":"field_rating","class":"ENGINEERING_SAFETY_CRITICAL","stakes":"HIGH","qualifiers":["outdoors","-20 C","lifting assembly","5 kN"]},
            {"key":"test_to_field_comparability","class":"ENGINEERING_SAFETY_CRITICAL","stakes":"HIGH","qualifiers":["lab to field","environment/configuration"]},
        ],
    },
    {
        "id": "D4-benchmark-comparative",
        "request": "Model A scores 84 on Benchmark X and Model B scores 81 on Benchmark Y. Is A better overall, and is the difference meaningful?",
        "gold_claims": [
            {"key":"score_a","class":"SCIENTIFIC_BENCHMARK","stakes":"LOW","qualifiers":["84","Benchmark X"]},
            {"key":"score_b","class":"SCIENTIFIC_BENCHMARK","stakes":"LOW","qualifiers":["81","Benchmark Y"]},
            {"key":"comparability","class":"SCIENTIFIC_BENCHMARK","stakes":"MEDIUM","qualifiers":["Benchmark X vs Benchmark Y"]},
            {"key":"overall_superiority","class":"SCIENTIFIC_BENCHMARK","stakes":"MEDIUM","qualifiers":["better overall"]},
            {"key":"difference_meaningful","class":"SCIENTIFIC_BENCHMARK","stakes":"MEDIUM","qualifiers":["meaningful difference"]},
        ],
        "candidate_claims": [
            {"key":"score_a","class":"SCIENTIFIC_BENCHMARK","stakes":"LOW","qualifiers":["84","Benchmark X"]},
            {"key":"score_b","class":"SCIENTIFIC_BENCHMARK","stakes":"LOW","qualifiers":["81","Benchmark Y"]},
            {"key":"comparability","class":"SCIENTIFIC_BENCHMARK","stakes":"MEDIUM","qualifiers":["Benchmark X vs Benchmark Y"]},
            {"key":"overall_superiority","class":"SCIENTIFIC_BENCHMARK","stakes":"MEDIUM","qualifiers":["better overall"]},
            {"key":"difference_meaningful","class":"SCIENTIFIC_BENCHMARK","stakes":"MEDIUM","qualifiers":["meaningful difference"]},
        ],
    },
    {
        "id": "D5-current-price-plus-budget-action",
        "request": "What is the current API price, and should we switch our production workload today if it saves about 20 percent?",
        "gold_claims": [
            {"key":"current_price","class":"CURRENT_PRODUCT_PLATFORM_FACT","stakes":"LOW","qualifiers":["current API price"]},
            {"key":"savings_estimate","class":"LOW_STAKES_PRODUCT_HYPOTHESIS","stakes":"MEDIUM","qualifiers":["about 20 percent"]},
            {"key":"production_switch_decision","class":"LOW_STAKES_PRODUCT_HYPOTHESIS","stakes":"MEDIUM","qualifiers":["production workload","today"]},
        ],
        "candidate_claims": [
            {"key":"current_price","class":"CURRENT_PRODUCT_PLATFORM_FACT","stakes":"LOW","qualifiers":["current API price"]},
            {"key":"savings_estimate","class":"LOW_STAKES_PRODUCT_HYPOTHESIS","stakes":"MEDIUM","qualifiers":["about 20 percent"]},
            {"key":"production_switch_decision","class":"LOW_STAKES_PRODUCT_HYPOTHESIS","stakes":"MEDIUM","qualifiers":["production workload","today"]},
        ],
    },
    {
        "id": "D6-implicit-jurisdiction",
        "request": "Can our Dubai company store scanned customer passports in this SaaS, and for how long?",
        "gold_claims": [
            {"key":"product_storage_capability","class":"CURRENT_PRODUCT_PLATFORM_FACT","stakes":"MEDIUM","qualifiers":["scanned passports","SaaS"]},
            {"key":"lawful_storage","class":"LEGAL_REGULATORY","stakes":"HIGH","qualifiers":["Dubai company","customer passports"]},
            {"key":"retention_period","class":"LEGAL_REGULATORY","stakes":"HIGH","qualifiers":["how long","customer passports"]},
            {"key":"jurisdiction_resolution","class":"LEGAL_REGULATORY","stakes":"HIGH","qualifiers":["Dubai/UAE"]},
        ],
        "candidate_claims": [
            {"key":"product_storage_capability","class":"CURRENT_PRODUCT_PLATFORM_FACT","stakes":"MEDIUM","qualifiers":["scanned passports","SaaS"]},
            {"key":"lawful_storage","class":"LEGAL_REGULATORY","stakes":"HIGH","qualifiers":["Dubai company","customer passports"]},
            {"key":"retention_period","class":"LEGAL_REGULATORY","stakes":"HIGH","qualifiers":["how long","customer passports"]},
            {"key":"jurisdiction_resolution","class":"LEGAL_REGULATORY","stakes":"HIGH","qualifiers":["Dubai/UAE"]},
        ],
    },
]

SEVERITY_ORDER = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
HIGH_STAKES_CLASSES = {"LEGAL_REGULATORY", "MEDICAL_SAFETY", "ENGINEERING_SAFETY_CRITICAL"}


def normalize_claims(items):
    return {c["key"]: c for c in items}


def grade(case):
    gold = normalize_claims(case["gold_claims"])
    cand = normalize_claims(case["candidate_claims"])
    errors = []

    for key, g in gold.items():
        c = cand.get(key)
        if c is None:
            severity = "P0" if g["class"] in HIGH_STAKES_CLASSES or g["stakes"] == "HIGH" else "P1"
            errors.append({"severity": severity, "type":"MISSING_CLAIM", "claim": key})
            continue
        if c.get("class") != g.get("class"):
            severity = "P0" if g["class"] in HIGH_STAKES_CLASSES else "P1"
            errors.append({"severity": severity, "type":"CLASS_MISMATCH", "claim": key, "expected":g["class"], "got":c.get("class")})
        if SEVERITY_ORDER.get(c.get("stakes"), -1) < SEVERITY_ORDER[g["stakes"]]:
            severity = "P0" if g["stakes"] == "HIGH" else "P1"
            errors.append({"severity": severity, "type":"STAKES_DOWNGRADE", "claim": key, "expected":g["stakes"], "got":c.get("stakes")})
        missing_q = sorted(set(g.get("qualifiers", [])) - set(c.get("qualifiers", [])))
        if missing_q:
            severity = "P0" if g["class"] in HIGH_STAKES_CLASSES else "P1"
            errors.append({"severity": severity, "type":"MISSING_QUALIFIER", "claim": key, "missing":missing_q})

    extra = sorted(set(cand) - set(gold))
    return {
        "id": case["id"],
        "gold_count": len(gold),
        "candidate_count": len(cand),
        "extra_claims": extra,
        "errors": errors,
        "passed": len(errors) == 0,
    }


def negative_controls():
    # Seed known decomposition faults to prove the grader fails closed.
    case = CASES[1]
    broken = json.loads(json.dumps(case))
    broken["candidate_claims"] = [c for c in broken["candidate_claims"] if c["key"] != "dose_change_action"]
    missing_high = grade(broken)

    case2 = CASES[2]
    broken2 = json.loads(json.dumps(case2))
    for c in broken2["candidate_claims"]:
        if c["key"] == "field_rating":
            c["qualifiers"] = ["5 kN"]
    qualifier_loss = grade(broken2)

    return [
        {"control":"missing hidden medical action", "expected_p0":True, "observed_p0":any(e["severity"]=="P0" for e in missing_high["errors"]), "errors":missing_high["errors"]},
        {"control":"lost safety-critical environment qualifier", "expected_p0":True, "observed_p0":any(e["severity"]=="P0" for e in qualifier_loss["errors"]), "errors":qualifier_loss["errors"]},
    ]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    rows = [grade(c) for c in CASES]
    controls = negative_controls()
    controls_pass = all(c["expected_p0"] == c["observed_p0"] for c in controls)
    status = "PASS" if all(r["passed"] for r in rows) and controls_pass else "FAIL"
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gate":"adversarial-claim-decomposition-v0.1",
        "scope":"deterministic completeness contract over adjudicated decompositions; natural-language decomposition behavior not yet validated",
        "rules":[
            "Requests are decomposed into atomic decision-relevant claims before retrieval.",
            "High-stakes subclaims may not be omitted or merged into lower-stakes claims.",
            "Qualifiers that change scope, applicability, safety, jurisdiction, time, or comparability are first-class claim data.",
            "Actions can raise stakes even when surrounding factual claims are low-stakes.",
            "Uncertainty in decomposition must trigger stricter routing or clarification, never silent downgrading.",
            "Retrieved content cannot modify the trusted decomposition record."
        ],
        "cases": rows,
        "negative_controls": controls,
        "status": status,
        "expert_gap_discovery":[
            "Semantic entailment between user language and atomic claims is not established by this deterministic contract.",
            "Coreference, negation, temporal scope, nested conditionals, multilingual prompts, and domain jargon require behavioral validation.",
            "A decomposition can be complete yet frame the wrong decision question; decision relevance needs its own check.",
            "Over-decomposition creates unnecessary retrieval cost and may fragment evidence context."
        ],
        "red_team":{
            "senior_researcher":"Would require end-to-end adjudicated prompts, not only manually prepared candidate decompositions.",
            "information_retrieval_engineer":"Would ask whether decomposition improves retrieval recall without query explosion.",
            "evaluation_scientist":"Would require inter-rater agreement for gold atomic claims and hidden holdout prompts.",
            "security_engineer":"Would test whether retrieved text or tool metadata can mutate decomposition/stakes after the trusted boundary."
        }
    }
    with open(OUT,"w",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if status != "PASS":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
