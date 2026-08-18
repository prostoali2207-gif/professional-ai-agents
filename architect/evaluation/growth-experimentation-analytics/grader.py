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


def find_fixture(suite, fixture_id):
    fixtures = suite.get("fixtures", [])
    for fixture in fixtures:
        if fixture.get("fixture_id") == fixture_id:
            return fixture
    raise KeyError(f"fixture not found in suite: {fixture_id}")


def grade(suite, key, result):
    failures = []
    fixture_id = result.get("fixture_id")

    if not isinstance(fixture_id, str) or not fixture_id:
        return {"fixture_id": fixture_id, "pass": False, "failures": ["missing fixture_id"]}

    try:
        find_fixture(suite, fixture_id)
    except KeyError as exc:
        return {"fixture_id": fixture_id, "pass": False, "failures": [str(exc)]}

    expected = key.get("fixtures", {}).get(fixture_id)
    if not isinstance(expected, dict):
        return {
            "fixture_id": fixture_id,
            "pass": False,
            "failures": ["grader key missing for fixture"],
        }

    allowed = expected.get("allowed_recommendations", [])
    if result.get("recommendation") not in allowed:
        failures.append(
            f"recommendation outside allowed set: {result.get('recommendation')} not in {allowed}"
        )

    text = flatten_text(result)

    for needle in expected.get("hard_fails", []):
        if needle.lower() in text:
            failures.append(f"hard-fail condition present: {needle}")

    for finding in expected.get("required_findings", []):
        if finding.lower() not in text:
            failures.append(f"required finding missing: {finding}")

    computations = {
        c.get("name"): c
        for c in result.get("computations", [])
        if isinstance(c, dict) and isinstance(c.get("name"), str)
    }

    for check in expected.get("required_computations", []):
        name = check.get("label")
        comp = computations.get(name)
        if not comp:
            failures.append(f"numeric check missing: {name}")
            continue

        value = comp.get("result")
        if not isinstance(value, (int, float)):
            failures.append(f"numeric result invalid: {name}")
            continue

        expected_value = check.get("expected")
        tolerance = check.get("tolerance", 0)
        if not isinstance(expected_value, (int, float)) or not isinstance(tolerance, (int, float)):
            failures.append(f"invalid grader numeric spec: {name}")
            continue

        if abs(value - expected_value) > tolerance:
            failures.append(
                f"numeric check failed: {name} expected {expected_value}±{tolerance} got {value}"
            )

    return {
        "fixture_id": fixture_id,
        "pass": not failures,
        "failures": failures,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Grade one Analytics result using a public fixture suite plus a separate grader key."
    )
    parser.add_argument("suite", help="fixture suite JSON; contains prompts/data but no answers")
    parser.add_argument("key", help="separate grader-key JSON")
    parser.add_argument("result", help="candidate result JSON")
    args = parser.parse_args()

    suite = load(args.suite)
    key = load(args.key)
    result = load(args.result)

    verdict = grade(suite, key, result)
    print(json.dumps(verdict, indent=2, ensure_ascii=False))
    return 0 if verdict["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
