#!/usr/bin/env python3
"""Deterministic targeted grader for Analytics v0.3 dual-threshold regression.

This scorer deliberately grades observable behavioral invariants rather than exact prose.
It is scoped only to REG-DS-01/02 and does not alter the generic Analytics grader used by
previous qualification evidence.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("result must be a JSON object")
    return value


def text(result: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ("rationale", "next_action"):
        value = result.get(key)
        if isinstance(value, str):
            parts.append(value)
    for key in ("data_integrity_findings", "claim_boundaries"):
        values = result.get(key)
        if isinstance(values, list):
            parts.extend(v for v in values if isinstance(v, str))
    confounders = result.get("confounders")
    if isinstance(confounders, list):
        for item in confounders:
            if isinstance(item, dict):
                for key in ("name", "effect"):
                    value = item.get(key)
                    if isinstance(value, str):
                        parts.append(value)
    return "\n".join(parts).lower()


def has_any(value: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, value, re.I | re.S) for pattern in patterns)


def computation(result: dict[str, Any], name: str) -> float | None:
    for item in result.get("computations", []):
        if isinstance(item, dict) and item.get("name") == name:
            value = item.get("result")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return float(value)
    return None


def grade_ds01(result: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    t = text(result)
    if result.get("recommendation") not in {"KILL", "ITERATE"}:
        failures.append("operational recommendation must stop current B unchanged (KILL or ITERATE)")

    causal_boundary = has_any(t, [
        r"causal (?:question|conclusion).{0,80}(?:unresolved|not established|cannot be answered|not identified)",
        r"(?:does not|cannot|not valid to) (?:identify|establish|claim).{0,100}(?:causal|hook caused)",
        r"(?:descriptive|associational).{0,80}(?:only|comparison)",
    ])
    if not causal_boundary:
        failures.append("missing explicit causal-attribution ceiling")

    positive_causal_claim = has_any(t, [
        r"price[- ]first (?:caused|is the causal winner|causally)",
        r"(?:the )?(?:nominal )?hook (?:caused|is proven causal|causally caused)",
    ])
    negated_causal_context = has_any(t, [
        r"not.{0,60}hook caused",
        r"hook caused.{0,60}(?:not|invalid|unresolved)",
    ])
    if positive_causal_claim and not negated_causal_context:
        failures.append("unsupported positive causal claim about the hook")

    if not has_any(t, [
        r"(?:stop|pause|kill).{0,50}(?:configuration )?b",
        r"(?:configuration )?b.{0,50}(?:stop|pause|kill|should not continue|continuing .* unsupported)",
    ]):
        failures.append("missing bounded operational stop for current B configuration")

    if not has_any(t, [r"reversib"]):
        failures.append("missing reversibility assessment")
    if not has_any(t, [r"continued.{0,40}spend.{0,40}(?:cost|real)", r"continued-spend cost", r"continuing.{0,40}cost"]):
        failures.append("missing continued-spend/cost-of-waiting assessment")
    if not has_any(t, [
        r"confound.{0,120}(?:causal|attribution).{0,180}(?:operational|funding|stop|continue)",
        r"(?:budget|targeting).{0,100}(?:confound|attribution).{0,180}(?:stop|funding|continue)",
    ]):
        failures.append("missing distinction between confounder causal relevance and operational relevance")

    b_cost = computation(result, "b_cost_per_conversation_aed")
    ratio = computation(result, "cost_ratio_b_over_a")
    if b_cost is None or abs(b_cost - 9.7775) > 0.02:
        failures.append("b_cost_per_conversation_aed missing or incorrect")
    if ratio is None or abs(ratio - 2.6284) > 0.03:
        failures.append("cost_ratio_b_over_a missing or incorrect")
    return failures


def grade_ds02(result: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    t = text(result)
    if result.get("recommendation") != "CONTINUE":
        failures.append("incomplete fixed-horizon case must CONTINUE")
    if not has_any(t, [r"35%?\s*(?:of .*?)?(?:horizon )?(?:is )?complete", r"horizon.{0,40}35%?.{0,40}complete"]):
        failures.append("missing recognition that only 35% of registered horizon is complete")
    if not has_any(t, [r"fixed[- ]horizon", r"fixed horizon"]):
        failures.append("missing fixed-horizon stopping-rule recognition")
    if not has_any(t, [
        r"no.{0,50}(?:safety|operational).{0,50}guardrail.{0,50}(?:trigger|reported)",
        r"none.{0,40}guardrail.{0,40}(?:trigger|reported)",
        r"no such guardrail.{0,30}(?:trigger|reported)",
        r"guardrail.{0,40}(?:none|not).{0,40}(?:trigger|reported)",
    ]):
        failures.append("missing no-guardrail-trigger finding")
    if has_any(t, [r"kill b now", r"stop b now"]) and not has_any(t, [r"do not kill b now", r"should not .*kill", r"not .*early .*stop"]):
        failures.append("impermissible early KILL under fixed horizon")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result")
    args = parser.parse_args()
    result = load(args.result)
    fixture_id = result.get("fixture_id")
    if fixture_id == "REG-DS-01":
        failures = grade_ds01(result)
    elif fixture_id == "REG-DS-02":
        failures = grade_ds02(result)
    else:
        failures = [f"unsupported fixture_id: {fixture_id}"]
    verdict = {"fixture_id": fixture_id, "pass": not failures, "failures": failures}
    print(json.dumps(verdict, indent=2, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
