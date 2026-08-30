#!/usr/bin/env python3
"""Novelty guard for the v1.1 external held-out cycle.

Issue #196 §7: the fresh pack "must not reuse observed cases verbatim". The previous pack was
sealed and its cases were never printed, so almost nothing about them is public — but the failure
lines in the run `33293694601` ledger did name identifiers, and those identifiers are therefore
the part of the previous pack that a repaired candidate could conceivably have been tuned toward.
They are refused here.

This is a guarantee, not a heuristic. The author is a different model called fresh at temperature
1 on a later date and would be very unlikely to reproduce a scenario anyway; that is an argument,
and an argument is not a control. The control is that admission fails closed on any of these
strings.

Nothing in this module relaxes anything. It only adds refusals, and it is bound by the v1.1
preregistration so it cannot be edited after the pack is authored.
"""

from __future__ import annotations

# Every identifier that appeared in the run 33293694601 ledger, verbatim. Arms, scope identifiers
# and metric names alike -- the distinction does not matter for a novelty check.
OBSERVED_IN_RUN_33293694601 = frozenset({
    # IMMATURE_FIXED_HORIZON
    "legacy_ui", "ui_experiment", "ui_refresh",
    "bundle_off", "price_opt", "pricing_test",
    # SPARSE_BUT_IDENTIFIED
    "personalized_sort", "sort_algorithm_test",
    "guided_tour_flow", "onboarding_experience_test",
    # UPSTREAM_DOWNSTREAM_CONFLICT
    "signup_channel_analysis", "email_marketing_cpc",
})

# The evaluator's own hand-written construct-test scenarios in test_external_pack_contract.py are
# public in the repository, so a pack that reproduced them would not be held out either.
PUBLIC_IN_REPOSITORY = frozenset({
    "directory_listings", "referral_partners", "channel_comparison", "booked_consultations",
    "trade_publication", "logistics_podcast", "placement_comparison", "carrier_applications",
    "checkout_compact", "checkout_current", "checkout_trial", "completed_first_orders",
    "trial_lesson_offer", "standard_offer", "offer_experiment", "paid_enrolments",
    "procurement_walkthrough", "current_pricing_page", "procurement_trial",
    "procurement_requests",
})

REFUSED = OBSERVED_IN_RUN_33293694601 | PUBLIC_IN_REPOSITORY


class NotNovel(Exception):
    """An authored case reuses an identifier that is already observed or already public."""


def check_identifier(value: str, what: str) -> str:
    """Refuse any identifier already seen in a scored run or already published in the repo."""
    if isinstance(value, str) and value.strip().lower() in REFUSED:
        raise NotNovel(
            f"{what} {value!r} appeared in run 33293694601 or in the repository's public "
            "construct tests; this pack must be held out from both")
    return value


def check_case(authored: dict, family: str) -> None:
    """Refuse a whole authored scenario if any of its identifier fields is not novel."""
    for key, value in authored.items():
        if key in ("domain", "stakeholder_pressure", "confound"):
            continue  # prose, not identifiers
        if isinstance(value, str):
            check_identifier(value, f"{family}.{key}")
