#!/usr/bin/env python3
"""Novelty guard for the v1.2 external held-out cycle.

Extends the v1.1 guard rather than replacing it: everything refused for the previous cycle stays
refused, and the identifiers that leaked into the run `33299723985` ledger are added. The v1.1
module is imported unchanged, so the preregistration that bound it still describes what that cycle
actually ran.

Only two identifiers leaked from the v1.1 run — its other failure lines named no arms — but the
guard is a control, not an estimate of how much leaked.
"""

from __future__ import annotations

import external_pack_novelty_v11 as v11

# Named in the run 33299723985 ledger, verbatim.
OBSERVED_IN_RUN_33299723985 = frozenset({"plan_comparison_q3", "premium_plan"})

REFUSED = v11.REFUSED | OBSERVED_IN_RUN_33299723985


class NotNovel(v11.NotNovel):
    """An authored case reuses an identifier that is already observed or already public."""


def check_identifier(value: str, what: str) -> str:
    if isinstance(value, str) and value.strip().lower() in REFUSED:
        raise NotNovel(
            f"{what} {value!r} appeared in run 33293694601 or 33299723985, or in the "
            "repository's public construct tests; this pack must be held out from all of them")
    return value


def check_case(authored: dict, family: str) -> None:
    for key, value in authored.items():
        if key in ("domain", "stakeholder_pressure", "confound"):
            continue  # prose, not identifiers
        if isinstance(value, str):
            check_identifier(value, f"{family}.{key}")
