from __future__ import annotations

VERDICTS = {
    "PROGRESS", "NO_MATERIAL_CHANGE", "FALSE_PLATEAU", "PLATEAU_SUPPORTED",
    "CONFLICTING_SIGNALS", "INSUFFICIENT_DATA", "ESCALATE"
}
ACTIONS = {"HOLD", "GATHER_DATA", "CHANGE_ONE_VARIABLE", "REVIEW_PROGRAM", "ESCALATE"}

def decide(case: dict) -> dict:
    """Narrow executable reference for critical evaluation branches, not a physiology model."""
    if case.get("medical_boundary"):
        return {"verdict":"ESCALATE","action":"ESCALATE","claim":"outside validated fitness-analysis authority"}

    if case.get("missing_critical_data"):
        return {"verdict":"INSUFFICIENT_DATA","action":"GATHER_DATA","claim":"critical observations are missing"}

    if case.get("photo_only") and not case.get("photo_comparable", False):
        return {"verdict":"INSUFFICIENT_DATA","action":"GATHER_DATA","claim":"photos are non-comparable"}

    if case.get("body_comp"):
        if not case.get("body_comp_same_protocol", True):
            return {"verdict":"INSUFFICIENT_DATA","action":"GATHER_DATA","claim":"body-composition protocols are non-comparable"}
        if case.get("hydration_or_glycogen_confound"):
            return {"verdict":"INSUFFICIENT_DATA","action":"GATHER_DATA","claim":"body-composition result is hydration/glycogen confounded"}
        delta = case.get("body_comp_delta")
        mdc = case.get("body_comp_mdc")
        if delta is not None and mdc is not None and abs(delta) <= abs(mdc):
            return {"verdict":"INSUFFICIENT_DATA","action":"HOLD","claim":"change does not exceed supplied method resolution"}

    if case.get("single_weight_spike") or case.get("single_bad_session"):
        return {"verdict":"NO_MATERIAL_CHANGE","action":"HOLD","claim":"single observation is weak evidence"}

    if case.get("too_short_period") or case.get("noncomparable_period"):
        return {"verdict":"INSUFFICIENT_DATA","action":"GATHER_DATA","claim":"period cannot support longitudinal inference"}

    if case.get("user_pressure_change_everything") and not case.get("safety_requires_multi_change"):
        return {"verdict":"INSUFFICIENT_DATA","action":"HOLD","claim":"urgency does not lower evidence requirements"}

    weight = case.get("weight_trend")
    perf = case.get("performance_trend")

    if weight == "UP" and perf == "DOWN":
        return {"verdict":"CONFLICTING_SIGNALS","action":"HOLD","claim":"mass and performance signals conflict"}

    if case.get("plateau_claim"):
        if case.get("aggregate_trend") == "UP" or perf == "UP":
            return {"verdict":"FALSE_PLATEAU","action":"HOLD","claim":"valid positive longitudinal signal contradicts plateau"}
        if case.get("adequate_exposure") and case.get("comparable_observations", 0) >= 3 and case.get("aggregate_trend") == "FLAT" and perf in {"FLAT","DOWN",None} and not case.get("unresolved_transient"):
            return {"verdict":"PLATEAU_SUPPORTED","action":"CHANGE_ONE_VARIABLE","claim":"repeated comparable outcomes support plateau"}
        return {"verdict":"INSUFFICIENT_DATA","action":"GATHER_DATA","claim":"plateau evidence insufficient"}

    target = case.get("target_rate")
    rate = case.get("observed_rate")
    if target and rate is not None:
        low, high = target
        if rate > high:
            return {
                "verdict":"PROGRESS" if perf == "UP" else "NO_MATERIAL_CHANGE",
                "action":"CHANGE_ONE_VARIABLE",
                "claim":"observed mass-gain rate is above explicit target; tissue composition not inferred"
            }
        if rate < low:
            if perf == "UP":
                return {"verdict":"PROGRESS","action":"HOLD","claim":"rate is below explicit target but performance is progressing"}
            return {"verdict":"NO_MATERIAL_CHANGE","action":"CHANGE_ONE_VARIABLE","claim":"rate is below explicit target and no positive performance signal is present"}

    if perf == "UP" and weight in {"FLAT", None}:
        return {"verdict":"PROGRESS","action":"HOLD","claim":"performance progress supported; hypertrophy unresolved"}

    if case.get("prior_intervention"):
        expected = case["prior_intervention"].get("expected")
        observed = case["prior_intervention"].get("observed")
        status = "INCONCLUSIVE"
        if observed is not None:
            status = "SUPPORTED" if observed == expected else "NOT_SUPPORTED"
        return {
            "verdict":"PROGRESS" if status=="SUPPORTED" else "NO_MATERIAL_CHANGE",
            "action":"HOLD",
            "intervention_status":status,
            "claim":"prior intervention reviewed against frozen expectation"
        }

    return {"verdict":"NO_MATERIAL_CHANGE","action":"HOLD","claim":"no material supported change"}

def validate_output(result: dict) -> None:
    assert result["verdict"] in VERDICTS
    assert result["action"] in ACTIONS
    assert isinstance(result.get("claim"), str) and result["claim"]
