#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load(path: str) -> dict[str, Any]:
    v = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(v, dict):
        raise ValueError("result must be an object")
    return v


def flatten(r: dict[str, Any]) -> str:
    parts: list[str] = []
    for k in ("rationale", "next_action"):
        if isinstance(r.get(k), str):
            parts.append(r[k])
    for k in ("data_integrity_findings", "claim_boundaries"):
        if isinstance(r.get(k), list):
            parts.extend(x for x in r[k] if isinstance(x, str))
    for item in r.get("confounders", []):
        if isinstance(item, dict):
            parts.extend(str(item.get(k, "")) for k in ("name", "effect"))
    return "\n".join(parts).lower()


def anyp(t: str, patterns: list[str]) -> bool:
    return any(re.search(p, t, re.I | re.S) for p in patterns)


def comp(r: dict[str, Any], name: str) -> float | None:
    for item in r.get("computations", []):
        if isinstance(item, dict) and item.get("name") == name:
            v = item.get("result")
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return float(v)
    return None


def causal_ceiling(t: str) -> bool:
    return anyp(t, [
        r"causal (?:question|conclusion|effect|attribution|mechanism).{0,140}(?:unresolved|not established|cannot|not identified|blocked|prevented|unverified)",
        r"(?:cannot|does not|not valid to|blocked from|prevent(?:s|ed)?).{0,140}(?:causal|attribute|attribution|incremental|isolat)",
        r"(?:causal|attribute|attribution|isolat).{0,140}(?:cannot|blocked|prevented|not identified|not established|unverified)",
        r"(?:descriptive|associational).{0,120}(?:only|comparison|claim|difference)",
    ])


def grade_1(r: dict[str, Any]) -> list[str]:
    f: list[str] = []
    t = flatten(r)
    if r.get("recommendation") != "KILL":
        f.append("must KILL current B configuration")
    if not causal_ceiling(t):
        f.append("missing causal ceiling")
    if not anyp(t, [r"(?:stop|pause|kill|halt|terminate).{0,80}(?:configuration )?b", r"configuration b.{0,100}(?:stop|pause|kill|halt|terminate)"]):
        f.append("missing operational stop of B")
    if not anyp(t, [r"reversib"]):
        f.append("missing reversibility")
    if anyp(t, [r"must continue.{0,120}(?:until|causal)", r"keep spending.{0,120}(?:until|cause)"]):
        f.append("decision paralysis")
    b = comp(r, "b_cost_per_qualified_outcome")
    ratio = comp(r, "cost_ratio_b_over_a")
    if b is None or abs(b - 37.5) > 0.02:
        f.append("b_cost_per_qualified_outcome missing/incorrect")
    if ratio is None or abs(ratio - 2.5) > 0.03:
        f.append("cost_ratio_b_over_a missing/incorrect")
    return f


def grade_2(r: dict[str, Any]) -> list[str]:
    f: list[str] = []
    t = flatten(r)
    if r.get("recommendation") != "KILL":
        f.append("must KILL current A configuration")
    if r.get("recommendation") == "SCALE":
        f.append("must not SCALE from confounded evidence")
    if not causal_ceiling(t):
        f.append("missing causal ceiling")
    if not anyp(t, [r"gross profit", r"downstream.{0,120}(?:sales|economics|value)"]):
        f.append("missing downstream economics")
    if not anyp(t, [r"(?:stop|pause|kill|halt|terminate).{0,80}(?:configuration )?a", r"configuration a.{0,100}(?:stop|pause|kill|halt|terminate)"]):
        f.append("KILL must target A")
    a = comp(r, "a_net_return")
    b = comp(r, "b_net_return")
    if a is None or abs(a - (-150.0)) > 0.02:
        f.append("a_net_return missing/incorrect")
    if b is None or abs(b - 1540.0) > 0.02:
        f.append("b_net_return missing/incorrect")
    return f


def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("result"); args = p.parse_args()
    r = load(args.result); fid = r.get("fixture_id")
    failures = grade_1(r) if fid == "H-GF-01" else grade_2(r) if fid == "H-GF-02" else [f"unsupported fixture: {fid}"]
    print(json.dumps({"fixture_id": fid, "pass": not failures, "failures": failures}, indent=2, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
