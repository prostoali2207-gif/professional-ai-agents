#!/usr/bin/env python3
"""Structural grader for Analytics v0.7.

Grades the decision record against generator-derived expectations. Two changes from v0.4:

  * the action target is resolved by set membership against the fixture's declared `arms`,
    not by parsing a string. In the v0.4 gate six of seven behavioral failures were target
    values a parser could not resolve or that named two arms at once, and one of those --
    `variant_b`, the fixture's own name for the arm -- was a defect in the parser rather
    than in the decision;
  * `decisive_metric` is asserted, so the H-GDS-02 failure mode (stopping the arm that the
    decisive metric favours) is observable directly rather than inferred;
  * `claim_scope` is asserted and the ceiling is read against it. In v0.5 the oracle capped a
    randomized design below INCREMENTAL_CAUSAL without ever telling the candidate which
    estimand the ceiling referred to, and those cases were burned. The scope is now declared by
    the candidate and the window fact is declared by the case, so the constraint is checkable
    against stated facts on both sides.

Nothing here reads prose.

v0.7 applies the four repairs from the 2026-08-28 oracle audit. None touches the candidate.

  1. The result is validated against the output contract *before* anything else, which is the
     grading order the harness README has always documented and no grader had implemented. A
     structurally invalid result used to pass whenever the invalid field was one the
     expectation happened not to assert on.
  2. Action targets are read from `target_by_action`, so an expectation permitting several
     actions no longer forces one target across all of them.
  3. Computation assertions declare RATIO or ABSOLUTE. For a ratio the candidate's own `unit`
     decides whether the ratio or the percentage form is the correct number. A ratio is
     dimensionless, so an unitless declaration means the ratio form; an unrecognised one
     is a failure rather than a coin flip.
  4. The result must carry the fixture_id it is graded against.
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
SCOPES = {"REGISTERED_ESTIMAND", "INTERIM_OUTCOME"}


DEFAULT_CONTRACT = Path(__file__).resolve().parent / "schemas" / "result-v4.schema.json"

RATIO_UNITS = {"ratio", "x", "fraction", "multiplier", "index", "times", "unitless", "none", ""}
PERCENT_UNITS = {"percent", "percentage", "%", "pct", "percentage points", "percent lift"}


def load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------------------
# Repair 1 -- contract validity is grading step 0.
# ---------------------------------------------------------------------------------------

def _fallback_validate(value: Any, schema: dict, path: str = "$") -> list[str]:
    """A dependency-free subset validator driven by the same contract file.

    The scored path must not depend on jsonschema being installed on a runner. This covers the
    constructs the Analytics contract actually uses and fails closed on anything it cannot
    confirm, rather than passing by default.
    """
    errors: list[str] = []
    expected = schema.get("type")
    types = {"object": dict, "array": list, "string": str, "boolean": bool,
             "number": (int, float), "integer": int}
    if isinstance(expected, str) and expected in types:
        if expected == "number" and isinstance(value, bool):
            errors.append(f"{path}: expected number, got boolean")
            return errors
        if not isinstance(value, types[expected]):
            errors.append(f"{path}: expected {expected}, got {type(value).__name__}")
            return errors
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} is not one of {schema['enum']}")
    if isinstance(value, str) and "minLength" in schema and len(value) < schema["minLength"]:
        errors.append(f"{path}: shorter than minLength {schema['minLength']}")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required property {key!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{path}: unexpected property {key!r}")
        for key, sub in properties.items():
            if key in value:
                errors += _fallback_validate(value[key], sub, f"{path}.{key}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: fewer than minItems {schema['minItems']}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors += _fallback_validate(item, item_schema, f"{path}[{index}]")
    return errors


def validate_against_contract(result: Any, contract: dict | None = None) -> list[str]:
    schema = contract
    if schema is None:
        if not DEFAULT_CONTRACT.is_file():
            return ["output contract unavailable; cannot validate the result"]
        schema = json.loads(DEFAULT_CONTRACT.read_text(encoding="utf-8"))
    try:
        import jsonschema
    except ImportError:
        return [f"output contract violation at {message}" for message in _fallback_validate(result, schema)]
    errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(result),
                    key=lambda e: list(e.absolute_path))
    return [f"output contract violation at "
            f"{'.'.join(str(p) for p in error.absolute_path) or '$'}: {error.message}"
            for error in errors]


def computation(result: dict[str, Any], name: str) -> tuple[float, str] | None:
    for item in result.get("computations", []):
        if isinstance(item, dict) and item.get("name") == name:
            value = item.get("result")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return float(value), str(item.get("unit") or "").strip().lower()
    return None


def check_computation(result: dict[str, Any], name: str, spec: list) -> list[str]:
    """Compare a computation against its assertion, using the declared unit where scale is
    ambiguous.

    A ratio and the same quantity as a percentage differ by 100x. The result schema carries a
    unit field precisely so the two can be told apart; asserting a bare number cannot, which
    failed a correct v0.6 answer that reported 50.0 percent against an expected 0.5.
    """
    expected, tolerance = spec[0], spec[1]
    kind = spec[2] if len(spec) > 2 else "ABSOLUTE"
    found = computation(result, name)
    if found is None:
        return [f"computation {name} missing"]
    actual, unit = found
    if kind == "RATIO":
        if unit in PERCENT_UNITS:
            actual, tolerance = actual / 100.0, max(tolerance, abs(expected) * 0.01)
        elif unit in RATIO_UNITS:
            pass
        else:
            return [f"computation {name} is ratio-valued and declares unit {unit!r}; a ratio and the "
                    f"same quantity as a percentage differ by 100x, so the unit must say which"]
    if abs(actual - expected) > tolerance:
        return [f"computation {name} incorrect (expected ~{expected}, got {actual}"
                + (f" {unit}" if unit else "") + ")"]
    return []


def universal_invariants(result: dict[str, Any], arms: list[str], window_complete: bool | None = None) -> list[str]:
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
    scope = causal.get("claim_scope")
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

    # Scope invariants from the v0.6 overlay.
    if scope not in SCOPES:
        failures.append(f"causal.claim_scope not in closed vocabulary: {scope!r}")
    elif window_complete is not None:
        if scope == "INTERIM_OUTCOME" and window_complete:
            failures.append("claim_scope INTERIM_OUTCOME but the case declares the registered window complete; "
                            "there is no interim to scope to")
        if scope == "REGISTERED_ESTIMAND" and not window_complete and ceiling == "INCREMENTAL_CAUSAL":
            failures.append("claim_ceiling INCREMENTAL_CAUSAL about the REGISTERED_ESTIMAND while the registered "
                            "window is still open; the registered estimand is right-censored")

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


def grade(result: dict[str, Any], fixture: dict[str, Any], expectation: dict[str, Any],
          contract: dict | None = None) -> dict[str, Any]:
    # Step 0: the result must satisfy its own output contract. Everything downstream assumes a
    # well-formed object, so a violation here ends the grading rather than being scored around.
    contract_failures = validate_against_contract(result, contract)
    if result.get("fixture_id") != fixture.get("fixture_id"):
        contract_failures.append(f"result fixture_id {result.get('fixture_id')!r} does not match the "
                                 f"case being graded, {fixture.get('fixture_id')!r}")
    if contract_failures:
        return {"fixture_id": result.get("fixture_id") if isinstance(result, dict) else None,
                "family": expectation.get("family"), "pass": False, "failures": contract_failures}

    arms = list(fixture["case"]["arms"])
    window_complete = fixture["case"].get("registered_window_complete")
    failures = universal_invariants(result, arms, window_complete)
    record = result.get("decision_record")
    if not isinstance(record, dict) or failures[:1] == ["decision_record missing"]:
        return {"fixture_id": result.get("fixture_id"), "pass": False, "failures": failures}

    causal = record.get("causal", {})
    operational = record.get("operational", {})
    scale = record.get("scale_readiness", {})
    basis = set(operational.get("decision_basis") or [])

    if "causal_status_in" in expectation and causal.get("status") not in expectation["causal_status_in"]:
        failures.append(f"causal.status must be one of {expectation['causal_status_in']}, got {causal.get('status')!r}")

    scope = causal.get("claim_scope")
    if "allowed_scopes" in expectation and scope in SCOPES:
        if scope not in expectation["allowed_scopes"]:
            failures.append(f"claim_scope {scope!r} is not available for this case; "
                            f"expected one of {expectation['allowed_scopes']}")
    # The ceiling is read against the scope the candidate declared, so a case where two scopings
    # are both defensible is graded correctly under either.
    bounds = (expectation.get("ceiling_by_scope") or {}).get(scope)
    if bounds and causal.get("claim_ceiling") in CEILINGS:
        actual = CEILINGS.index(causal["claim_ceiling"])
        if "max" in bounds and actual > CEILINGS.index(bounds["max"]):
            failures.append(f"claim_ceiling {causal['claim_ceiling']!r} exceeds what this design supports for "
                            f"scope {scope} (max {bounds['max']})")
        if "min" in bounds and actual < CEILINGS.index(bounds["min"]):
            failures.append(f"claim_ceiling {causal['claim_ceiling']!r} understates this design for scope "
                            f"{scope} (min {bounds['min']}); sparse counts are a precision problem, "
                            f"not an identification failure")
    if "action_in" in expectation and operational.get("action") not in expectation["action_in"]:
        failures.append(f"operational.action must be one of {expectation['action_in']}, got {operational.get('action')!r}")
    if operational.get("target") in arms:
        by_action = expectation.get("target_by_action") or {}
        permitted = by_action.get(operational.get("action")) or (
            [expectation["target"]] if "target" in expectation else [])
        if permitted and operational["target"] not in permitted:
            failures.append(f"operational.target is {operational['target']!r}, but action "
                            f"{operational.get('action')!r} may only be aimed at {permitted}")
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
    for name, spec in expectation.get("computations", {}).items():
        failures += check_computation(result, name, spec)

    return {"fixture_id": result.get("fixture_id"), "family": expectation.get("family"),
            "pass": not failures, "failures": failures}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result")
    parser.add_argument("--cases", required=True)
    parser.add_argument("--expectations", required=True)
    parser.add_argument("--contract", default=None)
    args = parser.parse_args()
    result = load(args.result)
    contract = load(args.contract) if args.contract else None
    suite = load(args.cases)
    expectations = load(args.expectations)["expectations"]
    fixture_id = result.get("fixture_id")
    fixture = next((f for f in suite["fixtures"] if f["fixture_id"] == fixture_id), None)
    if fixture is None or fixture_id not in expectations:
        print(json.dumps({"fixture_id": fixture_id, "pass": False,
                          "failures": [f"unknown fixture {fixture_id!r}"]}, indent=2))
        return 1
    report = grade(result, fixture, expectations[fixture_id], contract)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
