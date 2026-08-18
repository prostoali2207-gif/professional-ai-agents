#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def flatten_text(result):
    parts = [
        result.get("rationale", ""),
        result.get("next_action", ""),
        *result.get("data_integrity_findings", []),
        *result.get("claim_boundaries", []),
        *result.get("confounders", []),
    ]
    return "\n".join(str(x) for x in parts).lower()


def grade(fixture, result):
    failures = []
    expected = fixture["expected"]

    if result.get("fixture_id") != fixture.get("fixture_id"):
        failures.append("fixture_id mismatch")

    if result.get("recommendation") not in expected["allowed_recommendations"]:
        failures.append("recommendation outside allowed set")

    text = flatten_text(result)
    for needle in expected.get("hard_fail_contains", []):
        if needle.lower() in text:
            failures.append(f"hard-fail phrase present: {needle}")

    for finding in expected.get("required_findings", []):
        if finding.lower() not in text:
            failures.append(f"required finding missing: {finding}")

    computations = {c.get("name"): c for c in result.get("computations", []) if isinstance(c, dict)}
    for check in expected.get("numeric_checks", []):
        comp = computations.get(check["name"])
        if not comp:
            failures.append(f"numeric check missing: {check['name']}")
            continue
        value = comp.get("result")
        if not isinstance(value, (int, float)):
            failures.append(f"numeric result invalid: {check['name']}")
            continue
        if abs(value - check["expected"]) > check["tolerance"]:
            failures.append(
                f"numeric check failed: {check['name']} expected {check['expected']}±{check['tolerance']} got {value}"
            )

    return {
        "fixture_id": fixture.get("fixture_id"),
        "pass": not failures,
        "failures": failures,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture")
    parser.add_argument("result")
    args = parser.parse_args()
    verdict = grade(load(args.fixture), load(args.result))
    print(json.dumps(verdict, indent=2, ensure_ascii=False))
    return 0 if verdict["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
