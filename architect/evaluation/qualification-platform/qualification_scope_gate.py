#!/usr/bin/env python3
"""Conservative Resource & Cost Engineering gate for qualification scope.

This module does not infer professional impact from filenames or replace evaluator
judgment. The evaluator supplies the change surface, affected families, evidence
compatibility, and release requirement. The gate then prevents ad-hoc escalation
or accidental reuse outside those declared facts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

VALID_PURPOSES = {"development", "repair", "release"}
VALID_SURFACES = {"none", "infrastructure", "local", "shared", "unknown"}
VALID_EVIDENCE = {"none", "compatible", "incompatible"}


class ScopeGateError(ValueError):
    pass


def _require_bool(data: Dict[str, Any], key: str) -> bool:
    if key not in data or not isinstance(data[key], bool):
        raise ScopeGateError(f"{key} must be boolean")
    return data[key]


def decide(request: Dict[str, Any]) -> Dict[str, Any]:
    purpose = request.get("purpose")
    surface = request.get("change_surface")
    evidence = request.get("existing_evidence")
    families = request.get("affected_families", [])

    if purpose not in VALID_PURPOSES:
        raise ScopeGateError(f"purpose must be one of {sorted(VALID_PURPOSES)}")
    if surface not in VALID_SURFACES:
        raise ScopeGateError(f"change_surface must be one of {sorted(VALID_SURFACES)}")
    if evidence not in VALID_EVIDENCE:
        raise ScopeGateError(f"existing_evidence must be one of {sorted(VALID_EVIDENCE)}")
    if not isinstance(families, list) or any(not isinstance(x, str) or not x.strip() for x in families):
        raise ScopeGateError("affected_families must be a list of non-empty strings")

    full_release_required = _require_bool(request, "full_release_required")
    runtime_uncertainty = _require_bool(request, "runtime_uncertainty")
    professional_behavior_changed = _require_bool(request, "professional_behavior_changed")

    # Release evidence is evaluator-owned and cannot be optimized away.
    if purpose == "release" or full_release_required:
        return _result(
            "FULL",
            "Release claim or preregistered protocol requires the complete qualification suite.",
            families=[],
            canary=runtime_uncertainty,
        )

    # Reuse is allowed only when the professional behavior is unchanged and evidence
    # compatibility has been explicitly established by the evaluator.
    if not professional_behavior_changed and evidence == "compatible" and surface in {"none", "infrastructure"}:
        reason = (
            "Existing professional evidence is compatible and candidate behavior is unchanged. "
            "Run deterministic/static infrastructure checks as applicable; do not repurchase scored evidence."
        )
        return _result("REUSE", reason, families=[], canary=runtime_uncertainty)

    # A local professional/evaluator change may use the smallest declared affected regression.
    if surface == "local":
        if not families:
            return _result(
                "BLOCK",
                "Local scope was claimed but no affected evaluation families were declared; evaluator must classify impact first.",
                families=[],
                canary=False,
            )
        return _result(
            "TARGET",
            "Impact is explicitly local; run only the evaluator-declared affected regression families before broader escalation.",
            families=sorted(set(families)),
            canary=runtime_uncertainty,
        )

    # Shared/unknown coupling invalidates a narrow regression assumption.
    if surface in {"shared", "unknown"}:
        return _result(
            "FULL",
            "Affected surface is shared or unknown, so a narrow regression cannot safely establish coverage.",
            families=[],
            canary=runtime_uncertainty,
        )

    # Infrastructure-only changes with incompatible/no professional evidence should not
    # silently invent a professional test scope. Repair/establish evidence ownership first.
    if surface == "infrastructure":
        return _result(
            "BLOCK",
            "Infrastructure changed but reusable professional evidence was not established as compatible; resolve evidence compatibility before paid qualification.",
            families=[],
            canary=False,
        )

    # No declared change but no compatible evidence: do not buy a suite without a claim.
    return _result(
        "BLOCK",
        "No valid reusable evidence or affected professional scope was established; define the decision claim and evaluator-owned coverage first.",
        families=[],
        canary=False,
    )


def _result(scope: str, reason: str, families: list[str], canary: bool) -> Dict[str, Any]:
    return {
        "scope": scope,
        "reason": reason,
        "affected_families": families,
        "runtime_canary": "REQUIRED_IF_NOT_STATICALLY_RESOLVED" if canary else "NOT_REQUIRED_BY_SCOPE_GATE",
        "paid_scored_run_allowed": scope in {"TARGET", "FULL"},
        "release_pass_allowed_from_this_scope": scope == "FULL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path, help="JSON qualification-scope request")
    args = parser.parse_args()
    data = json.loads(args.request.read_text(encoding="utf-8"))
    try:
        result = decide(data)
    except ScopeGateError as exc:
        print(json.dumps({"scope": "BLOCK", "error": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["scope"] != "BLOCK" else 3


if __name__ == "__main__":
    raise SystemExit(main())
