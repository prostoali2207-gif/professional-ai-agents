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


def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("result"); args = p.parse_args()
    r = load(args.result); t = flatten(r); f: list[str] = []
    if r.get("fixture_id") != "H-GFD-01":
        f.append("unsupported fixture")
    if r.get("recommendation") not in {"KILL", "ITERATE"}:
        f.append("recommendation must be KILL or ITERATE")
    if r.get("recommendation") == "SCALE":
        f.append("must not SCALE from confounded evidence")
    if not causal_ceiling(t):
        f.append("missing causal ceiling")
    if not anyp(t, [r"gross profit", r"downstream.{0,120}(?:sales|economics|value)"]):
        f.append("missing downstream economics")
    if not anyp(t, [r"(?:stop|pause|kill|halt|terminate).{0,90}(?:configuration )?a", r"configuration a.{0,120}(?:stop|pause|kill|halt|terminate)"]):
        f.append("must stop current A configuration")
    a = comp(r, "a_net_return"); b = comp(r, "b_net_return")
    if a is None or abs(a - (-180.0)) > 0.02:
        f.append("a_net_return missing/incorrect")
    if b is None or abs(b - 1620.0) > 0.02:
        f.append("b_net_return missing/incorrect")
    print(json.dumps({"fixture_id": r.get("fixture_id"), "pass": not f, "failures": f}, indent=2, ensure_ascii=False))
    return 0 if not f else 1


if __name__ == "__main__":
    raise SystemExit(main())
