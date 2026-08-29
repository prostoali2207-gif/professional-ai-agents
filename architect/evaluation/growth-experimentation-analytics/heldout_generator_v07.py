#!/usr/bin/env python3
"""Seeded held-out case generator for Analytics v0.7.

Cases are sampled after the freeze and their expected decisions are *derived* from the
sampled parameters by a mechanical oracle, not authored case by case. This removes two
weaknesses of the previous cycles: the specific cases cannot have been written to match an
observed output, and which arm is the culpable one is randomised, so a candidate cannot
anchor on a position.

v0.7 changes the oracle only as the 2026-08-28 oracle audit requires: every expectation states
which targets each permitted action may name, and every computation assertion declares whether
its value is a ratio or an absolute quantity. Neither touches the candidate.

v0.6 changed the oracle only as the 2026-08-28 adjudication required: every case declares
`registered_window_complete`; the immature family accepts BOTH claim scopings, because both
are professionally correct once the scope is stated; and a new sparse-but-identified family
asserts that sparsity does NOT lower the ceiling. That last family is a loosening as well as a
tightening, which is what separates a principled rule from one reverse-engineered to fail the
outputs observed in v0.5.

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
        "registered_window_complete": True,
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
        "allowed_scopes": ["REGISTERED_ESTIMAND"],
        "ceiling_by_scope": {"REGISTERED_ESTIMAND": {"max": "DIRECTIONAL_ASSOCIATION"}},
        "action_in": ["KILL", "ITERATE"],
        "target": culprit,
        # Both permitted actions are aimed at the culpable arm here, but the mapping is stated
        # rather than left implicit.
        "target_by_action": {"KILL": [culprit], "ITERATE": [culprit]},
        "decisive_metric_in": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "basis_required": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL", "INSUFFICIENT_SAMPLE"],
        "computations": {f"net_return_{culprit}": [_round2(culprit_gross - culprit_spend), 0.02, "ABSOLUTE"],
                         f"net_return_{healthy}": [_round2(healthy_gross - healthy_spend), 0.02, "ABSOLUTE"]},
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
        "registered_window_complete": True,
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
        "allowed_scopes": ["REGISTERED_ESTIMAND"],
        "ceiling_by_scope": {"REGISTERED_ESTIMAND": {"max": "DIRECTIONAL_ASSOCIATION"}},
        "action_in": ["KILL"],
        "target": culprit,
        "target_by_action": {"KILL": [culprit]},
        "decisive_metric_in": ["ACQUISITION_COST", "REGISTERED_PRIMARY_KPI"],
        "basis_required": ["COST_OF_WAITING"],
        "basis_forbidden": ["MATURE_DOWNSTREAM_ECONOMICS"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL",
                              "MEASUREMENT_INTEGRITY_UNRESOLVED"],
        "computations": {f"cost_per_outcome_{culprit}": [_round2(culprit_spend / culprit_outcomes), 0.02,
                                                         "ABSOLUTE"]},
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
        "registered_window_complete": False,
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
        "allowed_scopes": ["REGISTERED_ESTIMAND", "INTERIM_OUTCOME"],
        "ceiling_by_scope": {
            # The registered estimand is right-censored, so no causal claim about it.
            "REGISTERED_ESTIMAND": {"max": "DIRECTIONAL_ASSOCIATION"},
            # Randomization still identifies the effect on what has actually been observed.
            "INTERIM_OUTCOME": {"max": "INCREMENTAL_CAUSAL"},
        },
        "action_in": ["CONTINUE"],
        "target": EXPERIMENT,
        "target_by_action": {"CONTINUE": [EXPERIMENT]},
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
        "registered_window_complete": True,
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
        "allowed_scopes": ["REGISTERED_ESTIMAND"],
        "ceiling_by_scope": {"REGISTERED_ESTIMAND": {"max": "INCREMENTAL_CAUSAL",
                                                     "min": "DIRECTIONAL_ASSOCIATION"}},
        "action_in": ["SCALE"],
        "target": treatment,
        "target_by_action": {"SCALE": [treatment]},
        "decisive_metric_in": ["REGISTERED_PRIMARY_KPI", "MATURE_DOWNSTREAM_ECONOMICS"],
        "basis_required": ["REGISTERED_PRIMARY_KPI"],
        "scale_state": "ELIGIBLE",
        # RATIO: the same quantity as a percentage is 100x this value, so the candidate's declared
        # unit decides which number is correct. An assertion on a bare number cannot.
        "computations": {f"relative_lift_{treatment}": [_round2(observed_lift), 0.02, "RATIO"]},
        "trap": "Reflexively blocking SCALE or declaring the causal question unresolved fails this case.",
    }
    return {"fixture_id": f"HO-CSW-{index:02d}", "instruction": instruction, "case": case}, expectation


def sparse_but_identified(rng: random.Random, index: int) -> tuple[dict, dict]:
    """Randomized, window-complete, and deliberately sparse.

    The discriminator is the ceiling, not the action. A candidate that treats small counts as an
    identification failure downgrades the ceiling and fails; one that treats identification as a
    licence to act scales and fails. Without this family the v0.6 rule would only ever be tested
    in the direction that tightens.
    """
    treatment, control = rng.sample(["variant_a", "variant_b"], 2)
    exposed = rng.choice([260, 320, 380])
    control_conv = rng.randint(1, 2)
    treatment_conv = control_conv + rng.randint(1, 2)
    case = {
        "arms": sorted([treatment, control]) + [EXPERIMENT],
        "primary_kpi": "qualified_signups",
        "outcome_maturity": "complete at the registered horizon",
        "registered_window_complete": True,
        "registered_success_rule": "treatment beats control on qualified_signups by at least 20%",
        treatment: {"exposed": exposed, "qualified_signups": treatment_conv},
        control: {"exposed": exposed, "qualified_signups": control_conv},
        "design": {"randomized_split": True, "assignment": "server-side 50/50", "exposure_verified": True,
                   "arms_differ_only_in": "the registered treatment", "confounding": "none identified"},
        "guardrails": {"all_pass": True},
        "operational_context": {"spend_has_stopped": True, "capacity_headroom_verified": True,
                                "outcome_counts_are_very_small": True},
    }
    instruction = ("Evaluate this completed experiment. State the causal conclusion, the quantity your claim "
                   "ceiling refers to, and the justified operational recommendation naming the arm or scope it "
                   "applies to.")
    expectation = {
        "family": "SPARSE_BUT_IDENTIFIED",
        "causal_status_in": ["IDENTIFIED"],
        "allowed_scopes": ["REGISTERED_ESTIMAND"],
        # Sparsity is a precision problem. The ceiling must NOT be downgraded for it.
        "ceiling_by_scope": {"REGISTERED_ESTIMAND": {"max": "INCREMENTAL_CAUSAL",
                                                     "min": "INCREMENTAL_CAUSAL"}},
        "action_in": ["INCONCLUSIVE", "ITERATE"],
        "target": EXPERIMENT,
        # INCONCLUSIVE says the registered question cannot be answered and scopes to the
        # experiment. ITERATE says run a properly powered test and may sensibly name either the
        # experiment or the treatment arm. Forcing one target for both failed five v0.6 trials.
        "target_by_action": {"INCONCLUSIVE": [EXPERIMENT], "ITERATE": [EXPERIMENT, treatment]},
        "decisive_metric_in": ["REGISTERED_PRIMARY_KPI", "NONE_DECIDABLE"],
        "basis_required": ["INSUFFICIENT_EVIDENCE"],
        "scale_state": "BLOCKED",
        "scale_reasons_any": ["INSUFFICIENT_SAMPLE"],
        "computations": {},
        "trap": "Downgrading the ceiling because counts are small confuses precision with identification.",
    }
    return {"fixture_id": f"HO-SBI-{index:02d}", "instruction": instruction, "case": case}, expectation


FAMILIES = [upstream_downstream_conflict, upstream_only_confounded, immature_fixed_horizon,
            clean_scalable_win, sparse_but_identified]


def generate(seed: int, per_family: int) -> tuple[dict[str, Any], dict[str, Any]]:
    rng = random.Random(seed)
    cases, expectations = [], {}
    for family in FAMILIES:
        for i in range(1, per_family + 1):
            case, expectation = family(rng, i)
            cases.append(case)
            expectations[case["fixture_id"]] = expectation
    suite = {"suite_id": f"analytics-heldout-v0.7-seed{seed}", "seed": seed,
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
