#!/usr/bin/env python3
"""Seeded held-out case generator for Analytics v0.5.

Cases are sampled after the freeze and their expected decisions are *derived* from the
sampled parameters by a mechanical oracle, not authored case by case. This removes two
weaknesses of the previous cycles: the specific cases cannot have been written to match an
observed output, and which arm is the culpable one is randomised, so a candidate cannot
anchor on a position.

It does not make the evaluation fully independent -- the same party wrote the generator and
the oracle -- so the qualification boundary stays narrower than an externally authored
held-out set. See `methodology/eval-integrity-and-regression.md`, which admits
"procedurally generated" tasks as an independence mechanism alongside expert authorship.

Writes two files. `cases.json` is candidate-facing and contains no expectations.
`expectations.json` is grader-only and must never reach an executor.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

EXPERIMENT = "experiment"


def _round2(value: float) -> float:
    return round(value + 1e-9, 2)


def upstream_downstream_conflict(rng: random.Random, index: int) -> tuple[dict, dict]:
    """The H-GDS-02 class: the arm with the better acquisition cost is the loss-making one.

    A candidate that lets the diagnostic metric select the target stops the profitable arm.
    """
    culprit, healthy = rng.sample(["configuration_a", "configuration_b"], 2)

    culprit_leads = rng.randint(18, 40)
    culprit_cost_per_lead = rng.choice([16.0, 18.0, 20.0, 22.0, 25.0])
    culprit_spend = _round2(culprit_leads * culprit_cost_per_lead)
    culprit_gross = _round2(culprit_spend - rng.choice([90, 120, 160, 210, 280]))

    healthy_leads = rng.randint(5, 10)
    healthy_cost_per_lead = _round2(culprit_cost_per_lead * rng.choice([2.4, 2.8, 3.2, 3.6]))
    healthy_spend = _round2(healthy_leads * healthy_cost_per_lead)
    healthy_gross = _round2(healthy_spend + rng.choice([900, 1200, 1500, 1900]))

    case = {
        "arms": sorted([culprit, healthy]) + [EXPERIMENT],
        "primary_kpi": "qualified_leads",
        "outcome_maturity": "complete",
        culprit: {"spend": culprit_spend, "qualified_leads": culprit_leads,
                  "sales": rng.randint(1, 2), "gross_profit": culprit_gross},
        healthy: {"spend": healthy_spend, "qualified_leads": healthy_leads,
                  "sales": rng.randint(3, 5), "gross_profit": healthy_gross},
        "design": {"randomized_split": False, "audience_source_differs": True, "creative_differs": True},
        "registered_business_rule": ("Acquisition cost is diagnostic. Mature verified sales and gross profit "
                                     "are the decision-relevant downstream economics before KILL, ITERATE or SCALE."),
        "operational_context": {"stopping_or_restarting_is_reversible": True,
                                "downstream_records_are_verified_and_mature": True},
    }
    instruction = ("Evaluate this completed paid-growth comparison. Preserve the causal ceiling, choose the "
                   "justified operational recommendation, and name the arm it applies to. Include computations "
                   f"named net_return_{culprit} and net_return_{healthy}.")
    expectation = {
        "family": "UPSTREAM_DOWNSTREAM_CONFLICT",
        "causal_status_in": ["UNRESOLVED"],
        "max_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "action_in": ["KILL", "ITERATE"],
        "target": culprit,
        "decisive_metric_in": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "basis_required": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL", "INSUFFICIENT_SAMPLE"],
        "computations": {f"net_return_{culprit}": [_round2(culprit_gross - culprit_spend), 0.02],
                         f"net_return_{healthy}": [_round2(healthy_gross - healthy_spend), 0.02]},
        "trap": "The arm with the better cost per lead is the loss-making one.",
    }
    return {"fixture_id": f"HO-UDC-{index:02d}", "instruction": instruction, "case": case}, expectation


def upstream_only_confounded(rng: random.Random, index: int) -> tuple[dict, dict]:
    """No downstream economics exist, so the acquisition metric is legitimately decisive."""
    culprit, healthy = rng.sample(["configuration_a", "configuration_b"], 2)
    healthy_outcomes = rng.randint(12, 22)
    healthy_cost = rng.choice([12.0, 14.0, 15.0, 16.0])
    healthy_spend = _round2(healthy_outcomes * healthy_cost)
    culprit_outcomes = rng.randint(3, 5)
    culprit_cost = _round2(healthy_cost * rng.choice([2.2, 2.5, 2.8, 3.0]))
    culprit_spend = _round2(culprit_outcomes * culprit_cost)

    case = {
        "arms": sorted([culprit, healthy]) + [EXPERIMENT],
        "primary_kpi": "qualified_inquiries",
        "outcome_maturity": "complete for the registered decision horizon",
        culprit: {"spend": culprit_spend, "qualified_outcomes": culprit_outcomes},
        healthy: {"spend": healthy_spend, "qualified_outcomes": healthy_outcomes},
        "design": {"randomized_split": False, "budget_a": "lifetime", "budget_b": "daily",
                   "audience_automation_differs": True, "optimization": "same", "attribution_window": "same"},
        "operational_context": {"stopping_is_reversible": True, "continued_spend_has_real_cost": True,
                                "no_verified_downstream_value_offset": True,
                                "no_contractual_or_safety_requirement_to_continue": True},
    }
    instruction = ("Evaluate this completed paid-growth comparison. The stakeholder argues that because the "
                   "comparison is confounded, both arms must keep spending until the cause is known. Separate the "
                   "causal conclusion from the immediate operational action and name the arm the action applies to. "
                   f"Include a computation named cost_per_outcome_{culprit}.")
    expectation = {
        "family": "UPSTREAM_ONLY_CONFOUNDED",
        "causal_status_in": ["UNRESOLVED"],
        "max_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "action_in": ["KILL"],
        "target": culprit,
        "decisive_metric_in": ["ACQUISITION_COST", "REGISTERED_PRIMARY_KPI"],
        "basis_required": ["COST_OF_WAITING"],
        "basis_forbidden": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL",
                              "MEASUREMENT_INTEGRITY_UNRESOLVED"],
        "computations": {f"cost_per_outcome_{culprit}": [_round2(culprit_spend / culprit_outcomes), 0.02]},
        "trap": "No downstream economics exist; claiming them as decisive is a fabrication.",
    }
    return {"fixture_id": f"HO-UOC-{index:02d}", "instruction": instruction, "case": case}, expectation


def immature_fixed_horizon(rng: random.Random, index: int) -> tuple[dict, dict]:
    """Fixed-horizon discipline: an early stop is the failure mode under test."""
    lagging, leading = rng.sample(["variant_a", "variant_b"], 2)
    pct = rng.choice([28, 33, 37, 42])
    case = {
        "arms": sorted([lagging, leading]) + [EXPERIMENT],
        "primary_kpi": "qualified_leads",
        "outcome_maturity": f"registered horizon only {pct}% complete",
        leading: {"spend": _round2(rng.uniform(30, 60)), "qualified_leads": rng.randint(3, 6)},
        lagging: {"spend": _round2(rng.uniform(18, 30)), "qualified_leads": rng.randint(0, 1)},
        "design": {"randomized_split": True, "confounding": "none known"},
        "registered_rule": "fixed horizon; no early stop except a safety or operational guardrail",
        "operational_context": {"no_safety_or_operational_guardrail_triggered": True},
    }
    instruction = ("Evaluate this in-flight experiment and return one operational recommendation naming the arm "
                   "or scope it applies to. Do not use a simple percentage-gap rule.")
    expectation = {
        "family": "IMMATURE_FIXED_HORIZON",
        "max_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "action_in": ["CONTINUE"],
        "target": EXPERIMENT,
        "decisive_metric_in": ["REGISTERED_PRIMARY_KPI", "NONE_DECIDABLE"],
        "basis_required": ["REGISTERED_PRIMARY_KPI"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["IMMATURE_OUTCOMES", "INSUFFICIENT_SAMPLE"],
        "computations": {},
        "trap": "Counts look lopsided but the registered horizon is incomplete and no guardrail fired.",
    }
    return {"fixture_id": f"HO-IFH-{index:02d}", "instruction": instruction, "case": case}, expectation


def clean_scalable_win(rng: random.Random, index: int) -> tuple[dict, dict]:
    """Anti-gaming control: a candidate that always blocks SCALE and always says UNRESOLVED fails here."""
    treatment, control = rng.sample(["variant_a", "variant_b"], 2)
    control_rate = rng.choice([0.040, 0.045, 0.050])
    lift = rng.choice([0.35, 0.42, 0.50])
    exposed = rng.choice([18000, 24000, 30000])
    control_conv = int(exposed * control_rate)
    treatment_conv = int(exposed * control_rate * (1 + lift))
    case = {
        "arms": sorted([treatment, control]) + [EXPERIMENT],
        "primary_kpi": "qualified_signups",
        "outcome_maturity": "complete at the registered horizon",
        "registered_success_rule": "treatment beats control on qualified_signups by at least 10% with guardrails intact",
        treatment: {"exposed": exposed, "qualified_signups": treatment_conv,
                    "spend": _round2(exposed * 0.02), "verified_contribution_margin_positive": True},
        control: {"exposed": exposed, "qualified_signups": control_conv,
                  "spend": _round2(exposed * 0.02), "verified_contribution_margin_positive": True},
        "design": {"randomized_split": True, "assignment": "server-side 50/50", "exposure_verified": True,
                   "arms_differ_only_in": "the registered treatment", "confounding": "none identified"},
        "guardrails": {"refund_rate": "within threshold", "support_load": "within threshold",
                       "latency": "within threshold", "all_pass": True},
        "operational_context": {"capacity_headroom_verified": True, "no_saturation_observed": True,
                                "unit_economics_verified_positive": True},
    }
    instruction = ("Evaluate this completed experiment, state the causal conclusion and its ceiling, and return the "
                   f"justified operational recommendation naming the arm it applies to. Include a computation named "
                   f"relative_lift_{treatment}.")
    observed_lift = (treatment_conv / control_conv) - 1
    expectation = {
        "family": "CLEAN_SCALABLE_WIN",
        "causal_status_in": ["IDENTIFIED"],
        "max_claim_ceiling": "INCREMENTAL_CAUSAL",
        "min_claim_ceiling": "DIRECTIONAL_ASSOCIATION",
        "action_in": ["SCALE"],
        "target": treatment,
        "decisive_metric_in": ["REGISTERED_PRIMARY_KPI", "MATURE_DOWNSTREAM_ECONOMICS"],
        "basis_required": ["REGISTERED_PRIMARY_KPI"],
        "scale_state": "ELIGIBLE",
        "computations": {f"relative_lift_{treatment}": [_round2(observed_lift), 0.02]},
        "trap": "Reflexively blocking SCALE or declaring the causal question unresolved fails this case.",
    }
    return {"fixture_id": f"HO-CSW-{index:02d}", "instruction": instruction, "case": case}, expectation


FAMILIES = [upstream_downstream_conflict, upstream_only_confounded, immature_fixed_horizon, clean_scalable_win]


def generate(seed: int, per_family: int) -> tuple[dict[str, Any], dict[str, Any]]:
    rng = random.Random(seed)
    cases, expectations = [], {}
    for family in FAMILIES:
        for i in range(1, per_family + 1):
            case, expectation = family(rng, i)
            cases.append(case)
            expectations[case["fixture_id"]] = expectation
    suite = {"suite_id": f"analytics-heldout-v0.5-seed{seed}", "seed": seed,
             "per_family": per_family, "fixtures": cases}
    return suite, {"seed": seed, "expectations": expectations}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--per-family", type=int, default=2)
    parser.add_argument("--cases-out", required=True)
    parser.add_argument("--expectations-out", required=True)
    args = parser.parse_args()
    suite, expectations = generate(args.seed, args.per_family)
    Path(args.cases_out).write_text(json.dumps(suite, indent=2) + "\n", encoding="utf-8")
    Path(args.expectations_out).write_text(json.dumps(expectations, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(suite['fixtures'])} held-out cases from seed {args.seed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
