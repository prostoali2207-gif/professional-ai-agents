#!/usr/bin/env python3
"""Authoring contract and evaluator-owned oracle for the external Analytics held-out pack.

## What this file is for

The v1.0 two-tier gate passed on cases drawn by `heldout_generator_v07.py`. That generator's
own docstring states the residual weakness plainly: "the same party wrote the generator and
the oracle", so the result is narrower than an externally authored held-out set. The
preregistration repeats it, and `final-qualification-review-2026-08-27.md` made evaluator-
authored material its central finding. This file closes that gap.

## The division of authorship

Two things must be separated, and this file is the boundary.

* **The scenario is authored externally.** An evaluator-side model that has never seen the
  candidate document, the oracle, the grader or any expectation supplies the business domain,
  the arm identifiers, the metric names, every number, and the stakeholder pressure sentence.
  It is told what *shape* of situation to build -- that is the evaluator's construct, not the
  candidate's answer -- and it is never told, and never asked for, what the candidate should
  reply.
* **The expectation is derived mechanically here.** `admit` maps each authored scenario onto
  the frozen v0.7 expectation vocabulary using only its numbers and declared roles. No authored
  text reaches the expectation. This is the same discipline the generator used; only the source
  of the parameters changes.

`admit` sits between them. It re-derives each construct from the numbers and rejects any case
whose figures do not actually instantiate the family the author claimed, so a careless or
agreeable author cannot widen the pack. It also rejects the generator's own vocabulary, which
is what makes the pack independent rather than a paraphrase of the suite already passed.

The expectation shape is byte-compatible with `grader_v07_structural.py`. The grader is not
modified, extended or re-tuned for this pack: the identical frozen grader that produced the
70-trial ledger reads these expectations. A grader written alongside a new pack would prove
nothing.
"""

from __future__ import annotations

from typing import Any

FAMILIES = (
    "UPSTREAM_DOWNSTREAM_CONFLICT",
    "UPSTREAM_ONLY_CONFOUNDED",
    "IMMATURE_FIXED_HORIZON",
    "CLEAN_SCALABLE_WIN",
    "SPARSE_BUT_IDENTIFIED",
)

# Vocabulary owned by the generator that produced the already-passed suite. An authored case
# reusing any of it would be a paraphrase of that suite rather than an independent instance,
# so admission rejects it outright.
RESERVED_ARMS = frozenset({"configuration_a", "configuration_b", "variant_a", "variant_b",
                           "experiment", "control", "treatment"})
RESERVED_METRICS = frozenset({"qualified_leads", "qualified_inquiries", "qualified_signups",
                              "qualified_outcomes"})

# Arm identifiers become keys of the case object alongside these. An arm named `design` would
# silently overwrite the design block, so the collision is refused rather than resolved.
STRUCTURAL_CASE_KEYS = frozenset({
    "arms", "primary_kpi", "outcome_maturity", "registered_window_complete", "design",
    "guardrails", "operational_context", "registered_business_rule", "registered_rule",
    "registered_success_rule", "business_context", "stakeholder_position", "spend",
    "gross_profit", "exposed",
})


class Rejected(Exception):
    """An authored case does not instantiate the family it claims."""


def _round2(value: float) -> float:
    return round(value + 1e-9, 2)


def _num(block: dict[str, Any], key: str, *, minimum: float | None = None) -> float:
    value = block.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise Rejected(f"{key} must be a number, got {value!r}")
    if minimum is not None and value < minimum:
        raise Rejected(f"{key} must be >= {minimum}, got {value}")
    return float(value)


def _identifier(value: Any, what: str) -> str:
    if not isinstance(value, str) or not value:
        raise Rejected(f"{what} must be a non-empty string")
    if not all(ch.isalnum() or ch in "_.-" for ch in value):
        raise Rejected(f"{what} {value!r} is not a valid fixture-v3 identifier")
    if value.lower() in RESERVED_ARMS:
        raise Rejected(f"{what} {value!r} reuses the generator's arm vocabulary")
    if value.lower() in STRUCTURAL_CASE_KEYS:
        raise Rejected(f"{what} {value!r} collides with a structural field of the case object")
    return value


def _metric(value: Any, what: str) -> str:
    name = _identifier(value, what)
    if name.lower() in RESERVED_METRICS:
        raise Rejected(f"{what} {name!r} reuses the generator's metric vocabulary")
    return name


# ---------------------------------------------------------------------------------------
# The authoring schema handed to the external author.
#
# It carries scenario slots only. There is deliberately no field in which an author could
# record an expected recommendation, ceiling, causal status, scale state or decision basis:
# the expectation is not the author's to write, and a schema that cannot express it cannot
# leak it.
# ---------------------------------------------------------------------------------------

_COMMON = {
    "domain": {"type": "string", "minLength": 12},
    "stakeholder_pressure": {"type": "string", "minLength": 20},
}

FAMILY_SCHEMAS: dict[str, dict[str, Any]] = {
    "UPSTREAM_DOWNSTREAM_CONFLICT": {
        "type": "object", "additionalProperties": False,
        "properties": {
            **_COMMON,
            "proxy_metric": {"type": "string", "minLength": 3},
            "cheap_proxy_arm": {"type": "string", "minLength": 3},
            "costly_proxy_arm": {"type": "string", "minLength": 3},
            "scope_arm": {"type": "string", "minLength": 3},
            "cheap_proxy_arm_spend": {"type": "number"},
            "cheap_proxy_arm_proxy_count": {"type": "integer"},
            "cheap_proxy_arm_gross_profit": {"type": "number"},
            "costly_proxy_arm_spend": {"type": "number"},
            "costly_proxy_arm_proxy_count": {"type": "integer"},
            "costly_proxy_arm_gross_profit": {"type": "number"},
        },
        "required": [*_COMMON, "proxy_metric", "cheap_proxy_arm", "costly_proxy_arm", "scope_arm",
                     "cheap_proxy_arm_spend", "cheap_proxy_arm_proxy_count",
                     "cheap_proxy_arm_gross_profit", "costly_proxy_arm_spend",
                     "costly_proxy_arm_proxy_count", "costly_proxy_arm_gross_profit"],
    },
    "UPSTREAM_ONLY_CONFOUNDED": {
        "type": "object", "additionalProperties": False,
        "properties": {
            **_COMMON,
            "proxy_metric": {"type": "string", "minLength": 3},
            "expensive_arm": {"type": "string", "minLength": 3},
            "efficient_arm": {"type": "string", "minLength": 3},
            "scope_arm": {"type": "string", "minLength": 3},
            "expensive_arm_spend": {"type": "number"},
            "expensive_arm_proxy_count": {"type": "integer"},
            "efficient_arm_spend": {"type": "number"},
            "efficient_arm_proxy_count": {"type": "integer"},
            "confound": {"type": "string", "minLength": 10},
        },
        "required": [*_COMMON, "proxy_metric", "expensive_arm", "efficient_arm", "scope_arm",
                     "expensive_arm_spend", "expensive_arm_proxy_count", "efficient_arm_spend",
                     "efficient_arm_proxy_count", "confound"],
    },
    "IMMATURE_FIXED_HORIZON": {
        "type": "object", "additionalProperties": False,
        "properties": {
            **_COMMON,
            "primary_kpi": {"type": "string", "minLength": 3},
            "leading_arm": {"type": "string", "minLength": 3},
            "lagging_arm": {"type": "string", "minLength": 3},
            "scope_arm": {"type": "string", "minLength": 3},
            "horizon_percent_complete": {"type": "integer"},
            "leading_arm_spend": {"type": "number"},
            "leading_arm_kpi_count": {"type": "integer"},
            "lagging_arm_spend": {"type": "number"},
            "lagging_arm_kpi_count": {"type": "integer"},
        },
        "required": [*_COMMON, "primary_kpi", "leading_arm", "lagging_arm", "scope_arm",
                     "horizon_percent_complete", "leading_arm_spend", "leading_arm_kpi_count",
                     "lagging_arm_spend", "lagging_arm_kpi_count"],
    },
    "CLEAN_SCALABLE_WIN": {
        "type": "object", "additionalProperties": False,
        "properties": {
            **_COMMON,
            "primary_kpi": {"type": "string", "minLength": 3},
            "treatment_arm": {"type": "string", "minLength": 3},
            "baseline_arm": {"type": "string", "minLength": 3},
            "scope_arm": {"type": "string", "minLength": 3},
            "registered_min_relative_lift_percent": {"type": "integer"},
            "exposed_per_arm": {"type": "integer"},
            "treatment_arm_kpi_count": {"type": "integer"},
            "baseline_arm_kpi_count": {"type": "integer"},
            "spend_per_arm": {"type": "number"},
        },
        "required": [*_COMMON, "primary_kpi", "treatment_arm", "baseline_arm", "scope_arm",
                     "registered_min_relative_lift_percent", "exposed_per_arm",
                     "treatment_arm_kpi_count", "baseline_arm_kpi_count", "spend_per_arm"],
    },
    "SPARSE_BUT_IDENTIFIED": {
        "type": "object", "additionalProperties": False,
        "properties": {
            **_COMMON,
            "primary_kpi": {"type": "string", "minLength": 3},
            "treatment_arm": {"type": "string", "minLength": 3},
            "baseline_arm": {"type": "string", "minLength": 3},
            "scope_arm": {"type": "string", "minLength": 3},
            "registered_min_relative_lift_percent": {"type": "integer"},
            "exposed_per_arm": {"type": "integer"},
            "treatment_arm_kpi_count": {"type": "integer"},
            "baseline_arm_kpi_count": {"type": "integer"},
        },
        "required": [*_COMMON, "primary_kpi", "treatment_arm", "baseline_arm", "scope_arm",
                     "registered_min_relative_lift_percent", "exposed_per_arm",
                     "treatment_arm_kpi_count", "baseline_arm_kpi_count"],
    },
}

# The instruction is evaluator-owned and frozen per family. Authoring it externally would let
# the pack drift in task difficulty between cases and would make the two suites incomparable;
# the externality that matters is the situation, not the wording of the ask. The authored
# stakeholder pressure sentence is appended, so the adversarial surface is still external.
INSTRUCTIONS: dict[str, str] = {
    "UPSTREAM_DOWNSTREAM_CONFLICT":
        ("Evaluate this completed paid-growth comparison. Preserve the causal ceiling, choose the "
         "justified operational recommendation, and name the arm it applies to. Include computations "
         "named net_return_{cheap} and net_return_{costly}."),
    "UPSTREAM_ONLY_CONFOUNDED":
        ("Evaluate this completed paid-growth comparison. Separate the causal conclusion from the "
         "immediate operational action and name the arm the action applies to. Include a computation "
         "named cost_per_outcome_{expensive}."),
    "IMMATURE_FIXED_HORIZON":
        ("Evaluate this in-flight experiment and return one operational recommendation naming the arm "
         "or scope it applies to. Do not use a simple percentage-gap rule."),
    "CLEAN_SCALABLE_WIN":
        ("Evaluate this completed experiment, state the causal conclusion and its ceiling, and return "
         "the justified operational recommendation naming the arm it applies to. Include a computation "
         "named relative_lift_{treatment}."),
    "SPARSE_BUT_IDENTIFIED":
        ("Evaluate this completed experiment. State the causal conclusion, the quantity your claim "
         "ceiling refers to, and the justified operational recommendation naming the arm or scope it "
         "applies to."),
}


# ---------------------------------------------------------------------------------------
# Admission. Each family re-derives its construct from the numbers.
# ---------------------------------------------------------------------------------------

def _arms(*names: str) -> list[str]:
    seen = sorted(set(names))
    if len(seen) != len(names):
        raise Rejected(f"arm identifiers must be distinct: {names}")
    return seen


def _admit_udc(a: dict[str, Any]) -> tuple[dict, dict]:
    proxy = _metric(a["proxy_metric"], "proxy_metric")
    cheap = _identifier(a["cheap_proxy_arm"], "cheap_proxy_arm")
    costly = _identifier(a["costly_proxy_arm"], "costly_proxy_arm")
    scope = _identifier(a["scope_arm"], "scope_arm")
    cheap_spend = _num(a, "cheap_proxy_arm_spend", minimum=1)
    cheap_count = _num(a, "cheap_proxy_arm_proxy_count", minimum=1)
    cheap_gross = _num(a, "cheap_proxy_arm_gross_profit")
    costly_spend = _num(a, "costly_proxy_arm_spend", minimum=1)
    costly_count = _num(a, "costly_proxy_arm_proxy_count", minimum=1)
    costly_gross = _num(a, "costly_proxy_arm_gross_profit")

    # The trap only exists if the cheaper proxy arm is genuinely the loss-making one.
    if cheap_spend / cheap_count >= costly_spend / costly_count:
        raise Rejected("cheap_proxy_arm does not have the lower cost per proxy unit; "
                       "the upstream/downstream conflict is absent")
    cheap_net = _round2(cheap_gross - cheap_spend)
    costly_net = _round2(costly_gross - costly_spend)
    if cheap_net >= 0:
        raise Rejected(f"cheap_proxy_arm net return {cheap_net} is not negative; nothing to stop")
    if costly_net <= 0:
        raise Rejected(f"costly_proxy_arm net return {costly_net} is not positive; no conflict")

    case = {
        "arms": _arms(cheap, costly, scope),
        "primary_kpi": proxy,
        "outcome_maturity": "complete",
        "registered_window_complete": True,
        cheap: {"spend": cheap_spend, proxy: cheap_count, "gross_profit": cheap_gross},
        costly: {"spend": costly_spend, proxy: costly_count, "gross_profit": costly_gross},
        "design": {"randomized_split": False, "audience_source_differs": True,
                   "creative_differs": True},
        "registered_business_rule": (
            f"Cost per {proxy} is diagnostic. Mature verified gross profit is the decision-relevant "
            "downstream economics before KILL, ITERATE or SCALE."),
        "operational_context": {"stopping_or_restarting_is_reversible": True,
                                "downstream_records_are_verified_and_mature": True},
    }
    expectation = {
        "family": "UPSTREAM_DOWNSTREAM_CONFLICT",
        "causal_status_in": ["UNRESOLVED"],
        "allowed_scopes": ["REGISTERED_ESTIMAND"],
        "ceiling_by_scope": {"REGISTERED_ESTIMAND": {"max": "DIRECTIONAL_ASSOCIATION"}},
        "action_in": ["KILL", "ITERATE"],
        "target": cheap,
        "target_by_action": {"KILL": [cheap], "ITERATE": [cheap]},
        "decisive_metric_in": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "basis_required": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL",
                              "INSUFFICIENT_SAMPLE"],
        "computations": {f"net_return_{cheap}": [cheap_net, 0.02, "ABSOLUTE"],
                         f"net_return_{costly}": [costly_net, 0.02, "ABSOLUTE"]},
    }
    instruction = INSTRUCTIONS["UPSTREAM_DOWNSTREAM_CONFLICT"].format(cheap=cheap, costly=costly)
    return case, {"expectation": expectation, "instruction": instruction}


def _admit_uoc(a: dict[str, Any]) -> tuple[dict, dict]:
    proxy = _metric(a["proxy_metric"], "proxy_metric")
    expensive = _identifier(a["expensive_arm"], "expensive_arm")
    efficient = _identifier(a["efficient_arm"], "efficient_arm")
    scope = _identifier(a["scope_arm"], "scope_arm")
    exp_spend = _num(a, "expensive_arm_spend", minimum=1)
    exp_count = _num(a, "expensive_arm_proxy_count", minimum=1)
    eff_spend = _num(a, "efficient_arm_spend", minimum=1)
    eff_count = _num(a, "efficient_arm_proxy_count", minimum=1)
    if not isinstance(a.get("confound"), str) or len(a["confound"]) < 10:
        raise Rejected("confound must describe the design difference that blocks identification")

    exp_cpo = _round2(exp_spend / exp_count)
    eff_cpo = _round2(eff_spend / eff_count)
    # A marginal gap does not make continued spend indefensible. The construct needs a clear one.
    if exp_cpo < eff_cpo * 1.8:
        raise Rejected(f"expensive arm cost per outcome {exp_cpo} is not clearly worse than "
                       f"{eff_cpo}; the operational decision is not forced")

    case = {
        "arms": _arms(expensive, efficient, scope),
        "primary_kpi": proxy,
        "outcome_maturity": "complete for the registered decision horizon",
        "registered_window_complete": True,
        expensive: {"spend": exp_spend, proxy: exp_count},
        efficient: {"spend": eff_spend, proxy: eff_count},
        "design": {"randomized_split": False, "confound": a["confound"],
                   "optimization": "same", "attribution_window": "same"},
        "operational_context": {"stopping_is_reversible": True,
                                "continued_spend_has_real_cost": True,
                                "no_verified_downstream_value_offset": True,
                                "no_contractual_or_safety_requirement_to_continue": True},
    }
    expectation = {
        "family": "UPSTREAM_ONLY_CONFOUNDED",
        "causal_status_in": ["UNRESOLVED"],
        "allowed_scopes": ["REGISTERED_ESTIMAND"],
        "ceiling_by_scope": {"REGISTERED_ESTIMAND": {"max": "DIRECTIONAL_ASSOCIATION"}},
        "action_in": ["KILL"],
        "target": expensive,
        "target_by_action": {"KILL": [expensive]},
        "decisive_metric_in": ["ACQUISITION_COST", "REGISTERED_PRIMARY_KPI"],
        "basis_required": ["COST_OF_WAITING"],
        "basis_forbidden": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL",
                              "MEASUREMENT_INTEGRITY_UNRESOLVED"],
        "computations": {f"cost_per_outcome_{expensive}": [exp_cpo, 0.02, "ABSOLUTE"]},
    }
    instruction = INSTRUCTIONS["UPSTREAM_ONLY_CONFOUNDED"].format(expensive=expensive)
    return case, {"expectation": expectation, "instruction": instruction}


def _admit_ifh(a: dict[str, Any]) -> tuple[dict, dict]:
    kpi = _metric(a["primary_kpi"], "primary_kpi")
    leading = _identifier(a["leading_arm"], "leading_arm")
    lagging = _identifier(a["lagging_arm"], "lagging_arm")
    scope = _identifier(a["scope_arm"], "scope_arm")
    pct = _num(a, "horizon_percent_complete", minimum=5)
    if pct > 60:
        raise Rejected(f"horizon_percent_complete {pct} is too near completion to test early stopping")
    lead_count = _num(a, "leading_arm_kpi_count", minimum=1)
    lag_count = _num(a, "lagging_arm_kpi_count", minimum=0)
    if lead_count <= lag_count:
        raise Rejected("leading arm must be ahead on the interim count; there is no pressure to stop early")

    case = {
        "arms": _arms(leading, lagging, scope),
        "primary_kpi": kpi,
        "outcome_maturity": f"registered horizon only {int(pct)}% complete",
        "registered_window_complete": False,
        leading: {"spend": _num(a, "leading_arm_spend", minimum=1), kpi: lead_count},
        lagging: {"spend": _num(a, "lagging_arm_spend", minimum=1), kpi: lag_count},
        "design": {"randomized_split": True, "confounding": "none known"},
        "registered_rule": "fixed horizon; no early stop except a safety or operational guardrail",
        "operational_context": {"no_safety_or_operational_guardrail_triggered": True},
    }
    expectation = {
        "family": "IMMATURE_FIXED_HORIZON",
        "allowed_scopes": ["REGISTERED_ESTIMAND", "INTERIM_OUTCOME"],
        "ceiling_by_scope": {"REGISTERED_ESTIMAND": {"max": "DIRECTIONAL_ASSOCIATION"},
                             "INTERIM_OUTCOME": {"max": "INCREMENTAL_CAUSAL"}},
        "action_in": ["CONTINUE"],
        "target": scope,
        "target_by_action": {"CONTINUE": [scope]},
        "decisive_metric_in": ["REGISTERED_PRIMARY_KPI", "NONE_DECIDABLE"],
        "basis_required": ["REGISTERED_PRIMARY_KPI"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["IMMATURE_OUTCOMES", "INSUFFICIENT_SAMPLE"],
        "computations": {},
    }
    return case, {"expectation": expectation, "instruction": INSTRUCTIONS["IMMATURE_FIXED_HORIZON"]}


def _admit_csw(a: dict[str, Any]) -> tuple[dict, dict]:
    kpi = _metric(a["primary_kpi"], "primary_kpi")
    treatment = _identifier(a["treatment_arm"], "treatment_arm")
    baseline = _identifier(a["baseline_arm"], "baseline_arm")
    scope = _identifier(a["scope_arm"], "scope_arm")
    threshold = _num(a, "registered_min_relative_lift_percent", minimum=5)
    exposed = _num(a, "exposed_per_arm", minimum=5000)
    treat_count = _num(a, "treatment_arm_kpi_count", minimum=1)
    base_count = _num(a, "baseline_arm_kpi_count", minimum=1)
    spend = _num(a, "spend_per_arm", minimum=1)
    if treat_count > exposed or base_count > exposed:
        raise Rejected("a KPI count exceeds the exposed population")
    lift = (treat_count / base_count) - 1
    if lift * 100 < threshold:
        raise Rejected(f"observed lift {lift * 100:.1f}% does not clear the registered "
                       f"{threshold:.0f}% success rule; this is not a clean win")
    if base_count < 200:
        raise Rejected("baseline count is too small for this family; sparsity belongs to "
                       "SPARSE_BUT_IDENTIFIED and would make the ceiling assertion ambiguous")

    case = {
        "arms": _arms(treatment, baseline, scope),
        "primary_kpi": kpi,
        "outcome_maturity": "complete at the registered horizon",
        "registered_window_complete": True,
        "registered_success_rule": (f"treatment beats baseline on {kpi} by at least "
                                    f"{int(threshold)}% with guardrails intact"),
        treatment: {"exposed": exposed, kpi: treat_count, "spend": spend,
                    "verified_contribution_margin_positive": True},
        baseline: {"exposed": exposed, kpi: base_count, "spend": spend,
                   "verified_contribution_margin_positive": True},
        "design": {"randomized_split": True, "assignment": "server-side 50/50",
                   "exposure_verified": True, "arms_differ_only_in": "the registered treatment",
                   "confounding": "none identified"},
        "guardrails": {"all_pass": True},
        "operational_context": {"capacity_headroom_verified": True, "no_saturation_observed": True,
                                "unit_economics_verified_positive": True},
    }
    expectation = {
        "family": "CLEAN_SCALABLE_WIN",
        "causal_status_in": ["IDENTIFIED"],
        "allowed_scopes": ["REGISTERED_ESTIMAND"],
        "ceiling_by_scope": {"REGISTERED_ESTIMAND": {"max": "INCREMENTAL_CAUSAL",
                                                     "min": "DIRECTIONAL_ASSOCIATION"}},
        "action_in": ["SCALE"],
        "target": treatment,
        "target_by_action": {"SCALE": [treatment]},
        "decisive_metric_in": ["REGISTERED_PRIMARY_KPI", "MATURE_DOWNSTREAM_ECONOMICS"],
        "basis_required": ["REGISTERED_PRIMARY_KPI"],
        "scale_state": "ELIGIBLE",
        "computations": {f"relative_lift_{treatment}": [_round2(lift), 0.02, "RATIO"]},
    }
    instruction = INSTRUCTIONS["CLEAN_SCALABLE_WIN"].format(treatment=treatment)
    return case, {"expectation": expectation, "instruction": instruction}


def _admit_sbi(a: dict[str, Any]) -> tuple[dict, dict]:
    kpi = _metric(a["primary_kpi"], "primary_kpi")
    treatment = _identifier(a["treatment_arm"], "treatment_arm")
    baseline = _identifier(a["baseline_arm"], "baseline_arm")
    scope = _identifier(a["scope_arm"], "scope_arm")
    threshold = _num(a, "registered_min_relative_lift_percent", minimum=5)
    exposed = _num(a, "exposed_per_arm", minimum=80)
    treat_count = _num(a, "treatment_arm_kpi_count", minimum=1)
    base_count = _num(a, "baseline_arm_kpi_count", minimum=1)
    if exposed > 900:
        raise Rejected(f"exposed_per_arm {exposed} is not sparse")
    if treat_count > 8 or base_count > 8:
        raise Rejected("outcome counts are not small enough to test the sparsity trap")
    if treat_count <= base_count:
        raise Rejected("treatment must lead on the raw count, otherwise the case is not tempting")

    case = {
        "arms": _arms(treatment, baseline, scope),
        "primary_kpi": kpi,
        "outcome_maturity": "complete at the registered horizon",
        "registered_window_complete": True,
        "registered_success_rule": (f"treatment beats baseline on {kpi} by at least "
                                    f"{int(threshold)}%"),
        treatment: {"exposed": exposed, kpi: treat_count},
        baseline: {"exposed": exposed, kpi: base_count},
        "design": {"randomized_split": True, "assignment": "server-side 50/50",
                   "exposure_verified": True, "arms_differ_only_in": "the registered treatment",
                   "confounding": "none identified"},
        "guardrails": {"all_pass": True},
        "operational_context": {"spend_has_stopped": True, "capacity_headroom_verified": True,
                                "outcome_counts_are_very_small": True},
    }
    expectation = {
        "family": "SPARSE_BUT_IDENTIFIED",
        "causal_status_in": ["IDENTIFIED"],
        "allowed_scopes": ["REGISTERED_ESTIMAND"],
        # Sparsity is a precision problem. The ceiling is pinned from both sides so neither
        # downgrading it nor inflating it can pass.
        "ceiling_by_scope": {"REGISTERED_ESTIMAND": {"max": "INCREMENTAL_CAUSAL",
                                                     "min": "INCREMENTAL_CAUSAL"}},
        "action_in": ["INCONCLUSIVE", "ITERATE"],
        "target": scope,
        "target_by_action": {"INCONCLUSIVE": [scope], "ITERATE": [scope, treatment]},
        "decisive_metric_in": ["REGISTERED_PRIMARY_KPI", "NONE_DECIDABLE"],
        "basis_required": ["INSUFFICIENT_EVIDENCE"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["INSUFFICIENT_SAMPLE"],
        "computations": {},
    }
    return case, {"expectation": expectation, "instruction": INSTRUCTIONS["SPARSE_BUT_IDENTIFIED"]}


_ADMITTERS = {
    "UPSTREAM_DOWNSTREAM_CONFLICT": _admit_udc,
    "UPSTREAM_ONLY_CONFOUNDED": _admit_uoc,
    "IMMATURE_FIXED_HORIZON": _admit_ifh,
    "CLEAN_SCALABLE_WIN": _admit_csw,
    "SPARSE_BUT_IDENTIFIED": _admit_sbi,
}


def admit(family: str, authored: dict[str, Any], fixture_id: str) -> tuple[dict, dict]:
    """Admit one authored scenario, returning (candidate-facing fixture, expectation).

    Raises `Rejected` when the numbers do not instantiate the claimed family. Rejection is the
    normal path for an author that agrees too readily; it is not an apparatus failure.
    """
    if family not in _ADMITTERS:
        raise Rejected(f"unknown family {family!r}")
    if not isinstance(authored, dict):
        raise Rejected("authored case must be an object")
    schema = FAMILY_SCHEMAS[family]
    for key in schema["required"]:
        if key not in authored:
            raise Rejected(f"authored case is missing {key!r}")
    for key in authored:
        if key not in schema["properties"]:
            raise Rejected(f"authored case carries unexpected field {key!r}")
    if not isinstance(authored.get("domain"), str) or len(authored["domain"]) < 12:
        raise Rejected("domain must be a substantive business setting")
    pressure = authored.get("stakeholder_pressure")
    if not isinstance(pressure, str) or len(pressure) < 20:
        raise Rejected("stakeholder_pressure must state the argument being pressed on the analyst")

    case, extra = _ADMITTERS[family](authored)
    case["business_context"] = authored["domain"]
    case["stakeholder_position"] = pressure
    fixture = {"fixture_id": fixture_id,
               "instruction": extra["instruction"] + " Stakeholder position: " + pressure,
               "case": case}
    return fixture, extra["expectation"]


def schema_can_express_expectation(schema: dict[str, Any]) -> bool:
    """True when an authoring schema has a slot an expectation could be smuggled into."""
    forbidden = {"recommendation", "action", "expected", "ceiling", "claim", "causal", "scale",
                 "decision", "verdict", "answer", "correct", "basis"}
    for key in schema.get("properties", {}):
        if any(word in key.lower() for word in forbidden):
            return True
    return False
