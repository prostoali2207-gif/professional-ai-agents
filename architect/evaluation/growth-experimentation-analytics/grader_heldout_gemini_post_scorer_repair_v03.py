#!/usr/bin/env python3
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
            v = item.get("result")
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return float(v)
    return None


def causal_ceiling(text: str) -> bool:
    return anyp(text, [
        r"causal (?:question|conclusion|effect|attribution).{0,120}(?:unresolved|not established|cannot|not identified|blocked|prevented)",
        r"(?:cannot|does not|not valid to|blocked from|prevent(?:s|ed)?).{0,120}(?:causal|attribute|attribution|incremental|isolat)",
        r"(?:causal|attribute|attribution|isolat).{0,120}(?:cannot|blocked|prevented|not identified|not established)",
        r"(?:descriptive|associational).{0,100}(?:only|comparison|claim)",
    ])


def grade_h1(r: dict[str, Any]) -> list[str]:
    f: list[str] = []
    t = flatten(r)
    if r.get("recommendation") != "KILL":
        f.append("must KILL current B configuration")
    if not causal_ceiling(t):
        f.append("missing causal ceiling")
    if not anyp(t, [r"(?:stop|pause|kill|halt).{0,70}(?:configuration )?b", r"configuration b.{0,90}(?:stop|pause|kill|halt)"]):
        f.append("missing operational stop of B")
    if not anyp(t, [r"reversib"]):
        f.append("missing reversibility")
    if anyp(t, [r"must continue.{0,100}(?:until|causal)", r"keep spending.{0,100}(?:until|cause)"]):
        f.append("decision paralysis")
    b = comp(r, "b_cost_per_qualified_outcome")
    ratio = comp(r, "cost_ratio_b_over_a")
    if b is None or abs(b - 33.0) > 0.02:
        f.append("b_cost_per_qualified_outcome missing/incorrect")
    if ratio is None or abs(ratio - (33.0 / 15.5)) > 0.03:
        f.append("cost_ratio_b_over_a missing/incorrect")
    return f


def grade_h2(r: dict[str, Any]) -> list[str]:
    f: list[str] = []
    t = flatten(r)
    if r.get("recommendation") != "KILL":
        f.append("must KILL current A configuration on mature downstream economics")
    if not causal_ceiling(t):
        f.append("missing causal ceiling")
    if not anyp(t, [r"gross profit", r"downstream.{0,100}(?:sales|economics|value)"]):
        f.append("missing downstream economics")
    if not anyp(t, [r"(?:not|cannot|does not).{0,120}scale", r"scale.{0,100}(?:blocked|not justified|unsupported|requires)"]):
        f.append("missing refusal to SCALE from confounded evidence")
    if not anyp(t, [r"(?:stop|pause|kill|halt).{0,70}(?:configuration )?a", r"configuration a.{0,90}(?:stop|pause|kill|halt)"]):
        f.append("KILL must target A")
    a = comp(r, "a_net_return")
    b = comp(r, "b_net_return")
    if a is None or abs(a - (-120.0)) > 0.02:
        f.append("a_net_return missing/incorrect")
    if b is None or abs(b - 1440.0) > 0.02:
        f.append("b_net_return missing/incorrect")
    return f


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("result")
    args = p.parse_args()
    r = load(args.result)
    fid = r.get("fixture_id")
    failures = grade_h1(r) if fid == "H-GDS-01" else grade_h2(r) if fid == "H-GDS-02" else [f"unsupported fixture: {fid}"]
    print(json.dumps({"fixture_id": fid, "pass": not failures, "failures": failures}, indent=2, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
