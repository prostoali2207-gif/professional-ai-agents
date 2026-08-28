#!/usr/bin/env python3
"""Structural grader for Analytics v0.5.

Grades the decision record against generator-derived expectations. Two changes from v0.4:

  * the action target is resolved by set membership against the fixture's declared `arms`,
    not by parsing a string. In the v0.4 gate six of seven behavioral failures were target
    values a parser could not resolve or that named two arms at once, and one of those --
    `variant_b`, the fixture's own name for the arm -- was a defect in the parser rather
    than in the decision;
  * `decisive_metric` is asserted, so the H-GDS-02 failure mode (stopping the arm that the
    decisive metric favours) is observable directly rather than inferred.

Nothing here reads prose.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

CEILINGS = ["NONE", "DESCRIPTIVE_ASSOCIATION", "DIRECTIONAL_ASSOCIATION", "INCREMENTAL_CAUSAL"]
CAUSAL_STATUS = {"IDENTIFIED", "UNRESOLVED", "NOT_APPLICABLE"}
ACTIONS = {"CONTINUE", "ITERATE", "SCALE", "KILL", "INCONCLUSIVE"}
DECISIVE = {"MATURE_DOWNSTREAM_ECONOMICS", "REGISTERED_PRIMARY_KPI", "ACQUISITION_COST",
            "GUARDRAIL", "CAPACITY", "NONE_DECIDABLE"}


def load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def computation(result: dict[str, Any], name: str) -> float | None:
    for item in result.get("computations", []):
        if isinstance(item, dict) and item.get("name") == name:
            value = item.get("result")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return float(value)
    return None


def universal_invariants(result: dict[str, Any], arms: list[str]) -> list[str]:
    failures: list[str] = []
    record = result.get("decision_record")
    if not isinstance(record, dict):
        return ["decision_record missing"]
    causal = record.get("causal") if isinstance(record.get("causal"), dict) else {}
    operational = record.get("operational") if isinstance(record.get("operational"), dict) else {}
    scale = record.get("scale_readiness") if isinstance(record.get("scale_readiness"), dict) else {}
    if not causal or not operational or not scale:
        return ["decision_record must contain causal, operational and scale_readiness"]

    status, ceiling = causal.get("status"), causal.get("claim_ceiling")
    blocking = causal.get("blocking_confounders") if isinstance(causal.get("blocking_confounders"), list) else []
    action, target = operational.get("action"), operational.get("target")
    decisive = operational.get("decisive_metric")
    basis = operational.get("decision_basis")
    state = scale.get("state")
    reasons = scale.get("blocking_reasons") if isinstance(scale.get("blocking_reasons"), list) else []

    if status not in CAUSAL_STATUS:
        failures.append(f"causal.status not in closed vocabulary: {status!r}")
    if ceiling not in CEILINGS:
        failures.append(f"causal.claim_ceiling not in closed vocabulary: {ceiling!r}")
    if action not in ACTIONS:
        failures.append(f"operational.action not in closed vocabulary: {action!r}")
    if decisive not in DECISIVE:
        failures.append(f"operational.decisive_metric not in closed vocabulary: {decisive!r}")
    if not isinstance(basis, list) or not basis:
        failures.append("operational.decision_basis must be a non-empty list")

    # Target resolution is a lookup, not a parse.
    if not isinstance(target, str) or target not in arms:
        failures.append(f"operational.target {target!r} is not one of the declared arms {arms}")

    if action != result.get("recommendation"):
        failures.append(f"operational.action {action!r} disagrees with recommendation {result.get('recommendation')!r}")

    declared = {c.get("name") for c in result.get("confounders", []) if isinstance(c, dict)}
    for name in blocking:
        if name not in declared:
            failures.append(f"blocking confounder {name!r} is not declared in confounders[]")
    if status == "IDENTIFIED" and blocking:
        failures.append("causal.status IDENTIFIED while blocking confounders are named")
    if ceiling == "INCREMENTAL_CAUSAL" and status != "IDENTIFIED":
        failures.append("claim_ceiling INCREMENTAL_CAUSAL requires causal.status IDENTIFIED")

    substantive = [r for r in reasons if r != "NOT_BLOCKED"]
    if state == "BLOCKED" and not substantive:
        failures.append("scale_readiness BLOCKED requires at least one substantive blocking reason")
    if state == "ELIGIBLE" and substantive:
        failures.append("scale_readiness ELIGIBLE cannot carry substantive blocking reasons")
    if result.get("recommendation") == "SCALE" and state != "ELIGIBLE":
        failures.append("recommendation SCALE requires scale_readiness ELIGIBLE")
    if not isinstance(operational.get("reversible"), bool):
        failures.append("operational.reversible must be a boolean")
    if not str(operational.get("evidence_that_would_change_action") or "").strip():
        failures.append("operational.evidence_that_would_change_action must be non-empty")
    return failures


def grade(result: dict[str, Any], fixture: dict[str, Any], expectation: dict[str, Any]) -> dict[str, Any]:
    arms = list(fixture["case"]["arms"])
    failures = universal_invariants(result, arms)
    record = result.get("decision_record")
    if not isinstance(record, dict) or failures[:1] == ["decision_record missing"]:
        return {"fixture_id": result.get("fixture_id"), "pass": False, "failures": failures}

    causal = record.get("causal", {})
    operational = record.get("operational", {})
    scale = record.get("scale_readiness", {})
    basis = set(operational.get("decision_basis") or [])

    if "causal_status_in" in expectation and causal.get("status") not in expectation["causal_status_in"]:
        failures.append(f"causal.status must be one of {expectation['causal_status_in']}, got {causal.get('status')!r}")
    if "max_claim_ceiling" in expectation and causal.get("claim_ceiling") in CEILINGS:
        if CEILINGS.index(causal["claim_ceiling"]) > CEILINGS.index(expectation["max_claim_ceiling"]):
            failures.append(f"claim_ceiling {causal['claim_ceiling']!r} exceeds what this design supports "
                            f"(max {expectation['max_claim_ceiling']})")
    if "min_claim_ceiling" in expectation and causal.get("claim_ceiling") in CEILINGS:
        if CEILINGS.index(causal["claim_ceiling"]) < CEILINGS.index(expectation["min_claim_ceiling"]):
            failures.append(f"claim_ceiling {causal['claim_ceiling']!r} understates this design "
                            f"(min {expectation['min_claim_ceiling']})")
    if "action_in" in expectation and operational.get("action") not in expectation["action_in"]:
        failures.append(f"operational.action must be one of {expectation['action_in']}, got {operational.get('action')!r}")
    if "target" in expectation and operational.get("target") in arms:
        if operational["target"] != expectation["target"]:
            failures.append(f"operational.target is {operational['target']!r}, but the justified action applies "
                            f"to {expectation['target']!r}")
    if "decisive_metric_in" in expectation and operational.get("decisive_metric") in DECISIVE:
        if operational["decisive_metric"] not in expectation["decisive_metric_in"]:
            failures.append(f"decisive_metric {operational['decisive_metric']!r} is not defensible here; "
                            f"expected one of {expectation['decisive_metric_in']}")
    for required in expectation.get("basis_required", []):
        if required not in basis:
            failures.append(f"decision_basis must record {required}")
    for forbidden in expectation.get("basis_forbidden", []):
        if forbidden in basis:
            failures.append(f"decision_basis must not claim {forbidden} for this case")
    if "scale_state" in expectation and scale.get("state") != expectation["scale_state"]:
        failures.append(f"scale_readiness.state must be {expectation['scale_state']}, got {scale.get('state')!r}")
    if "scale_reasons_any" in expectation:
        if not (set(scale.get("blocking_reasons") or []) & set(expectation["scale_reasons_any"])):
            failures.append(f"scale_readiness must cite at least one of {expectation['scale_reasons_any']}")
    for name, (expected, tolerance) in expectation.get("computations", {}).items():
        actual = computation(result, name)
        if actual is None or abs(actual - expected) > tolerance:
            failures.append(f"computation {name} missing or incorrect (expected ~{expected}, got {actual})")

    return {"fixture_id": result.get("fixture_id"), "family": expectation.get("family"),
            "pass": not failures, "failures": failures}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result")
    parser.add_argument("--cases", required=True)
    parser.add_argument("--expectations", required=True)
    args = parser.parse_args()
    result = load(args.result)
    suite = load(args.cases)
    expectations = load(args.expectations)["expectations"]
    fixture_id = result.get("fixture_id")
    fixture = next((f for f in suite["fixtures"] if f["fixture_id"] == fixture_id), None)
    if fixture is None or fixture_id not in expectations:
        print(json.dumps({"fixture_id": fixture_id, "pass": False,
                          "failures": [f"unknown fixture {fixture_id!r}"]}, indent=2))
        return 1
    report = grade(result, fixture, expectations[fixture_id])
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
