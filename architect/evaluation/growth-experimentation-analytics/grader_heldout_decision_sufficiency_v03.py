#!/usr/bin/env python3
"""Deterministic post-freeze heldout grader for Analytics v0.3 decision sufficiency."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("result must be an object")
    return value


def flatten(result: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ("rationale", "next_action"):
        value = result.get(key)
        if isinstance(value, str):
            parts.append(value)
    for key in ("data_integrity_findings", "claim_boundaries"):
        value = result.get(key)
        if isinstance(value, list):
            parts.extend(x for x in value if isinstance(x, str))
    for item in result.get("confounders", []):
        if isinstance(item, dict):
            parts.extend(str(item.get(k, "")) for k in ("name", "effect"))
    return "\n".join(parts).lower()


def anyp(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, re.I | re.S) for p in patterns)


def comp(result: dict[str, Any], name: str) -> float | None:
    for item in result.get("computations", []):
        if isinstance(item, dict) and item.get("name") == name:
            value = item.get("result")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return float(value)
    return None


def causal_ceiling(t: str) -> bool:
    return anyp(t, [
        r"causal (?:question|conclusion|effect).{0,100}(?:unresolved|not established|cannot|not identified)",
        r"(?:cannot|does not|not valid to).{0,100}(?:causal|attribute|incremental)",
        r"(?:descriptive|associational).{0,80}(?:only|comparison)",
    ])


def grade_h1(result: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    t = flatten(result)
    if result.get("recommendation") != "KILL":
        failures.append("H-DS-01 must KILL current B configuration rather than fund for causal certainty")
    if not causal_ceiling(t):
        failures.append("missing causal ceiling in confounded comparison")
    if not anyp(t, [r"(?:stop|pause|kill).{0,60}(?:configuration )?b", r"b.{0,60}(?:stop|pause|kill)"]):
        failures.append("missing operational stop of current B")
    if not anyp(t, [r"reversib"]):
        failures.append("missing reversibility")
    if not anyp(t, [r"continued.{0,50}spend.{0,50}(?:cost|real)", r"cost of (?:waiting|continuing)"]):
        failures.append("missing continued-spend cost")
    if anyp(t, [r"must continue.{0,80}(?:until|causal)", r"keep spending.{0,80}(?:until|cause)"]):
        failures.append("decision paralysis: continued spend demanded only for causal certainty")
    b = comp(result, "b_cost_per_qualified_outcome")
    ratio = comp(result, "cost_ratio_b_over_a")
    if b is None or abs(b - 32.0) > 0.02:
        failures.append("b_cost_per_qualified_outcome missing/incorrect")
    if ratio is None or abs(ratio - (32/15)) > 0.03:
        failures.append("cost_ratio_b_over_a missing/incorrect")
    return failures


def grade_h2(result: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    t = flatten(result)
    if result.get("recommendation") not in {"KILL", "ITERATE"}:
        failures.append("H-DS-02 must take a bounded operational action; SCALE and paralysis are not justified")
    if not causal_ceiling(t):
        failures.append("missing causal ceiling")
    if not anyp(t, [r"gross profit", r"downstream.{0,80}(?:sales|economics|value)"]):
        failures.append("missing decision-relevant downstream economics")
    if not anyp(t, [r"(?:not|cannot|does not).{0,100}scale", r"scale.{0,80}(?:blocked|not justified|unsupported|requires)"]):
        failures.append("missing refusal to SCALE from confounded evidence")
    if result.get("recommendation") == "KILL":
        if not anyp(t, [r"(?:stop|pause|kill).{0,60}(?:configuration )?a", r"configuration a.{0,80}(?:stop|pause|kill)"]):
            failures.append("KILL must target current A configuration, whose verified downstream economics are worse")
        if anyp(t, [r"(?:stop|pause|kill).{0,60}(?:configuration )?b.{0,80}(?:lead cost|cost per lead|cpl)"]):
            failures.append("must not KILL B because of higher lead acquisition cost alone")
    if anyp(t, [r"kill.{0,80}(?:because|solely).{0,80}(?:lead cost|cost per lead|cpl)"]):
        failures.append("dumb cost-gap KILL despite verified downstream economics")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result")
    args = parser.parse_args()
    result = load(args.result)
    fid = result.get("fixture_id")
    failures = grade_h1(result) if fid == "H-DS-01" else grade_h2(result) if fid == "H-DS-02" else [f"unsupported fixture: {fid}"]
    print(json.dumps({"fixture_id": fid, "pass": not failures, "failures": failures}, indent=2, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
