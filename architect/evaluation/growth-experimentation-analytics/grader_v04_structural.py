#!/usr/bin/env python3
"""Structural grader for the Analytics v0.4 output contract.

Every P0/P1 assertion is made against `decision_record`, a closed-vocabulary decision
object. No qualified claim is graded by matching prose.

Why this exists
---------------
The v0.3 graders asserted P0 claims with regexes over `rationale` / `claim_boundaries` /
`next_action`. That made a verdict a function of phrasing rather than of the decision, in
both directions:

  * run 32563283125 marked H-DS-01 FAIL for "missing continued-spend cost" while the
    candidate had in fact written "real continued spend" and "real marginal spend to
    continue" -- the pattern `continued.{0,50}spend.{0,50}(?:cost|real)` requires the
    word order to be the other way round;
  * in the same job H-DS-02 PASSED the "refusal to SCALE" assertion by an incidental
    collision with "...does not override the registered requirement to use mature
    verified sales and gross profit for KILL/SCALE decisions", a sentence that refuses
    nothing, while the sentence that does refuse ("No SCALE recommendation is supported")
    matches neither pattern.

Prose is still returned by the candidate and is still worth reading. It is no longer the
evidence surface for a behavioral verdict.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

CAUSAL_STATUS = {"IDENTIFIED", "UNRESOLVED", "NOT_APPLICABLE"}
CEILINGS = ["NONE", "DESCRIPTIVE_ASSOCIATION", "DIRECTIONAL_ASSOCIATION", "INCREMENTAL_CAUSAL"]
ACTIONS = {"CONTINUE", "ITERATE", "SCALE", "KILL", "INCONCLUSIVE"}


def load(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("result must be a JSON object")
    return value


def identify_arm(target: str) -> str | None:
    """Resolve a free-text target to exactly one arm identifier.

    This is a closed identification problem, not a semantic one: the fixture names its
    arms. 'A', 'configuration A', 'Variant A (current)' all resolve to A. A target that
    names both arms or neither is ambiguous and fails -- an action aimed at an
    unidentifiable arm is not a decision.
    """
    letters = set(re.findall(r"\b(?:configuration|variant|arm|cell|group)?\s*([ab])\b", target, re.I))
    letters |= set(re.findall(r"\bconfiguration_([ab])\b", target, re.I))
    letters = {x.upper() for x in letters}
    return letters.pop() if len(letters) == 1 else None


def computation(result: dict[str, Any], name: str) -> float | None:
    for item in result.get("computations", []):
        if isinstance(item, dict) and item.get("name") == name:
            value = item.get("result")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return float(value)
    return None


def universal_invariants(result: dict[str, Any]) -> list[str]:
    """Internal consistency required of every result by the v0.4 overlay."""
    failures: list[str] = []
    record = result.get("decision_record")
    if not isinstance(record, dict):
        return ["decision_record missing"]

    causal = record.get("causal") if isinstance(record.get("causal"), dict) else {}
    operational = record.get("operational") if isinstance(record.get("operational"), dict) else {}
    scale = record.get("scale_readiness") if isinstance(record.get("scale_readiness"), dict) else {}
    if not causal or not operational or not scale:
        return ["decision_record must contain causal, operational and scale_readiness"]

    status = causal.get("status")
    ceiling = causal.get("claim_ceiling")
    blocking = causal.get("blocking_confounders")
    action = operational.get("action")
    basis = operational.get("decision_basis")
    state = scale.get("state")
    reasons = scale.get("blocking_reasons")

    if status not in CAUSAL_STATUS:
        failures.append(f"causal.status not in closed vocabulary: {status!r}")
    if ceiling not in CEILINGS:
        failures.append(f"causal.claim_ceiling not in closed vocabulary: {ceiling!r}")
    if action not in ACTIONS:
        failures.append(f"operational.action not in closed vocabulary: {action!r}")
    if not isinstance(basis, list) or not basis:
        failures.append("operational.decision_basis must be a non-empty list")
    if not isinstance(blocking, list):
        failures.append("causal.blocking_confounders must be a list")
        blocking = []
    if not isinstance(reasons, list):
        failures.append("scale_readiness.blocking_reasons must be a list")
        reasons = []

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


def grade_expectation(result: dict[str, Any], spec: dict[str, Any]) -> list[str]:
    """Apply one fixture's professional expectations to the structured record."""
    failures = universal_invariants(result)
    record = result.get("decision_record")
    if not isinstance(record, dict) or failures[:1] == ["decision_record missing"]:
        return failures

    causal = record.get("causal", {})
    operational = record.get("operational", {})
    scale = record.get("scale_readiness", {})
    basis = set(operational.get("decision_basis") or [])

    if "causal_status_in" in spec and causal.get("status") not in spec["causal_status_in"]:
        failures.append(f"causal.status must be one of {sorted(spec['causal_status_in'])}, got {causal.get('status')!r}")

    if "max_claim_ceiling" in spec:
        allowed = CEILINGS[: CEILINGS.index(spec["max_claim_ceiling"]) + 1]
        if causal.get("claim_ceiling") not in allowed:
            failures.append(
                f"claim_ceiling {causal.get('claim_ceiling')!r} exceeds the ceiling this design supports "
                f"(max {spec['max_claim_ceiling']})"
            )

    if "action_in" in spec and operational.get("action") not in spec["action_in"]:
        failures.append(f"operational.action must be one of {sorted(spec['action_in'])}, got {operational.get('action')!r}")

    if "target_arm" in spec:
        arm = identify_arm(str(operational.get("target") or ""))
        if arm is None:
            failures.append(f"operational.target does not identify exactly one arm: {operational.get('target')!r}")
        elif arm != spec["target_arm"]:
            failures.append(f"operational.target names arm {arm}, but the justified action targets arm {spec['target_arm']}")

    for required in spec.get("basis_required", []):
        if required not in basis:
            failures.append(f"decision_basis must record {required}")
    for forbidden in spec.get("basis_forbidden", []):
        if forbidden in basis:
            failures.append(f"decision_basis must not rest on {forbidden} for this decision")
    if "basis_not_only" in spec and basis and basis.issubset(set(spec["basis_not_only"])):
        failures.append(f"decision_basis must not rest only on {sorted(spec['basis_not_only'])}")

    if "scale_state" in spec and scale.get("state") != spec["scale_state"]:
        failures.append(f"scale_readiness.state must be {spec['scale_state']}, got {scale.get('state')!r}")
    if "scale_reasons_any" in spec:
        if not (set(scale.get("blocking_reasons") or []) & set(spec["scale_reasons_any"])):
            failures.append(f"scale_readiness must cite at least one of {sorted(spec['scale_reasons_any'])}")

    for name, (expected, tolerance) in spec.get("computations", {}).items():
        actual = computation(result, name)
        if actual is None or abs(actual - expected) > tolerance:
            failures.append(f"computation {name} missing or incorrect (expected ~{expected}, got {actual})")

    return failures


EXPECTATIONS: dict[str, dict[str, Any]] = {
    # Confounded acquisition-cost comparisons: causal identification is blocked, but a
    # reversible stop of the weaker current arm is operationally justified, and the cost
    # of continuing must be part of the recorded grounds.
    "H-DS-01": {
        "causal_status_in": {"UNRESOLVED"},
        "max_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "action_in": {"KILL"},
        "target_arm": "B",
        "basis_required": ["COST_OF_WAITING"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL", "MEASUREMENT_INTEGRITY_UNRESOLVED"],
        "computations": {"b_cost_per_qualified_outcome": (32.0, 0.02), "cost_ratio_b_over_a": (32 / 15, 0.03)},
    },
    "H-GF-01": {
        "causal_status_in": {"UNRESOLVED"},
        "max_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "action_in": {"KILL"},
        "target_arm": "B",
        "basis_required": ["COST_OF_WAITING"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL", "MEASUREMENT_INTEGRITY_UNRESOLVED"],
        "computations": {"b_cost_per_qualified_outcome": (37.5, 0.02), "cost_ratio_b_over_a": (2.5, 0.03)},
    },
    "H-GDS-01": {
        "causal_status_in": {"UNRESOLVED"},
        "max_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "action_in": {"KILL"},
        "target_arm": "B",
        "basis_required": ["COST_OF_WAITING"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL", "MEASUREMENT_INTEGRITY_UNRESOLVED"],
        "computations": {"b_cost_per_qualified_outcome": (33.0, 0.02), "cost_ratio_b_over_a": (33 / 15.5, 0.03)},
    },
    # Downstream-economics traps: the cheaper-acquisition arm is the loss-making one.
    # The action must target A and must not rest on the acquisition-cost diagnostic alone.
    "H-DS-02": {
        "causal_status_in": {"UNRESOLVED"},
        "max_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "action_in": {"KILL", "ITERATE"},
        "target_arm": "A",
        "basis_required": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "basis_not_only": ["ACQUISITION_COST_DIAGNOSTIC"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL", "INSUFFICIENT_SAMPLE"],
    },
    "H-GF-02": {
        "causal_status_in": {"UNRESOLVED"},
        "max_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "action_in": {"KILL", "ITERATE"},
        "target_arm": "A",
        "basis_required": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "basis_not_only": ["ACQUISITION_COST_DIAGNOSTIC"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL", "INSUFFICIENT_SAMPLE"],
        "computations": {"a_net_return": (-150.0, 0.02), "b_net_return": (1540.0, 0.02)},
    },
    "H-GDS-02": {
        "causal_status_in": {"UNRESOLVED"},
        "max_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "action_in": {"KILL", "ITERATE"},
        "target_arm": "A",
        "basis_required": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "basis_not_only": ["ACQUISITION_COST_DIAGNOSTIC"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL", "INSUFFICIENT_SAMPLE"],
        "computations": {"a_net_return": (-120.0, 0.02), "b_net_return": (1440.0, 0.02)},
    },
    "H-GFD-01": {
        "causal_status_in": {"UNRESOLVED"},
        "max_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "action_in": {"KILL", "ITERATE"},
        "target_arm": "A",
        "basis_required": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "basis_not_only": ["ACQUISITION_COST_DIAGNOSTIC"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL", "INSUFFICIENT_SAMPLE"],
        "computations": {"a_net_return": (-180.0, 0.02), "b_net_return": (1620.0, 0.02)},
    },
    # Development regression cases.
    "REG-DS-01": {
        "causal_status_in": {"UNRESOLVED"},
        "max_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "action_in": {"KILL"},
        "target_arm": "B",
        "basis_required": ["COST_OF_WAITING"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL", "MEASUREMENT_INTEGRITY_UNRESOLVED"],
        "computations": {"b_cost_per_conversation_aed": (9.7775, 0.02), "cost_ratio_b_over_a": (9.7775 / 3.7204, 0.05)},
    },
    # Fixed-horizon discipline: outcomes are immature and no guardrail fired, so an early
    # KILL is the failure mode under test.
    "REG-DS-02": {
        "action_in": {"CONTINUE"},
        "max_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["IMMATURE_OUTCOMES", "INSUFFICIENT_SAMPLE"],
    },
}


def grade(result: dict[str, Any]) -> dict[str, Any]:
    fixture_id = result.get("fixture_id")
    spec = EXPECTATIONS.get(fixture_id)
    if spec is None:
        failures = [f"unsupported fixture: {fixture_id!r}"]
    else:
        failures = grade_expectation(result, spec)
    return {"fixture_id": fixture_id, "pass": not failures, "failures": failures}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result")
    args = parser.parse_args()
    report = grade(load(args.result))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
