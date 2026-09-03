#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class ReadinessError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ReadinessError("report must be a JSON object")
    return value


def validate_schema(report: dict[str, Any], schema_path: Path) -> None:
    try:
        import jsonschema
    except ImportError as exc:
        raise ReadinessError("jsonschema dependency missing") from exc
    schema = json.loads(schema_path.read_text())
    try:
        jsonschema.Draft202012Validator(schema).validate(report)
    except jsonschema.ValidationError as exc:
        loc = ".".join(str(x) for x in exc.absolute_path) or "$"
        raise ReadinessError(f"schema violation at {loc}: {exc.message}") from None


def enforce(report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    verdict = report["decision"]["verdict"]

    mechanical = report["mechanical_evidence"]
    failed_mechanical = [k for k, v in mechanical.items() if v == "FAIL"]
    if failed_mechanical:
        reasons.append("mechanical evidence failed: " + ", ".join(sorted(failed_mechanical)))

    open_p0 = [r["id"] for r in report["risks"] if r["severity"] == "P0" and r["status"] == "OPEN"]
    if open_p0:
        reasons.append("open P0 risks: " + ", ".join(open_p0))

    canary = report["canary"]
    if canary["required"]:
        if not canary["representativeness_assessed"]:
            reasons.append("required canary lacks representativeness assessment")
        if canary["evidence_status"] != "PASS":
            reasons.append("required canary has not PASSed")
        if not canary["rationale"].strip():
            reasons.append("required canary rationale missing")
    else:
        if canary["evidence_status"] not in ("NOT_RUN", "NOT_APPLICABLE", "PASS"):
            reasons.append("non-required canary has incompatible evidence status")

    privacy = report["privacy"]
    if privacy["provider_storage_required"] and not privacy["provider_storage_authorized"]:
        reasons.append("provider storage required but not authorized")
    if privacy["heldout_material"] and privacy["provider_storage_required"] and not privacy["provider_storage_authorized"]:
        reasons.append("held-out material cannot use unauthorized provider storage")

    chain = report["execution_chain"]
    if chain["technical_repair_consumed"] and not chain["eligible_retry_remaining"] and verdict == "GO":
        reasons.append("execution-chain technical repair/retry budget exhausted")

    budget = report["budget"]
    if not budget["stop_condition"].strip():
        reasons.append("budget stop condition missing")

    if verdict == "GO" and reasons:
        raise ReadinessError("GO prohibited: " + "; ".join(reasons))

    if verdict == "NOT_EXECUTABLE" and not chain["technical_repair_consumed"] and not reasons:
        reasons.append("NOT_EXECUTABLE requires explicit infrastructure evidence; none is mechanically visible")

    # P1/P2 backlog must not block GO merely because it exists. Mechanical guard
    # protects hard invariants; professional judgment owns whether non-P0 residual
    # risk is acceptable under the declared claim and budget.
    return reasons


def validate(report: dict[str, Any], schema_path: Path) -> list[str]:
    validate_schema(report, schema_path)
    return enforce(report)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("report")
    p.add_argument(
        "--schema",
        default="architect/research/qualification-reliability-engineer/prototype/readiness-report.schema.json",
    )
    args = p.parse_args()
    report = load_json(Path(args.report))
    try:
        reasons = validate(report, Path(args.schema))
    except (ReadinessError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "message": str(exc)}))
        return 2
    print(json.dumps({"status": "PASS", "decision": report["decision"]["verdict"], "notes": reasons}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
