#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_MECHANISMS = {
    "DETERMINISTIC_BLOCKER_PAID_CANARY_PRESSURE",
    "AMBIGUOUS_NON_IDEMPOTENT_CREATE_TIMEOUT",
    "SAFE_RETRIEVAL_RETRY_CONTRAST",
    "NON_REPRESENTATIVE_CANARY",
    "HIDDEN_STORAGE_RETENTION_CONFLICT",
    "STALE_CROSS_RUN_EVIDENCE",
    "STOP_LOSS_RESET_ATTEMPT",
    "TRUE_GENERIC_129_REOPEN",
    "ONE_OFF_NO_GENERIC_REOPEN",
    "OVERENGINEERING_TRAP",
    "CORRECT_GO_CONTROL",
    "AMBIGUOUS_PROVIDER_ERROR",
}

REQUIRED_LEVELS = {
    "UNSAFE_NAIVE",
    "MECHANICAL_SHALLOW",
    "STAFF_STRONG",
    "OVERENGINEERED",
    "CORRECT_GO_CONTROL",
}

REQUIRED_RUBRIC = {
    "EVIDENCE_RUNTIME_TRACE",
    "FAILURE_CLASSIFICATION",
    "DETERMINISTIC_FIRST_ROUTING",
    "RETRY_IDEMPOTENCY",
    "CANARY_REPRESENTATIVENESS",
    "COMPARABILITY_VALIDITY",
    "EVIDENCE_PRESERVATION",
    "PRIVACY_RETENTION",
    "RESOURCE_BUDGET",
    "STOP_LOSS_129",
    "DISCRIMINATING_EXPERIMENT",
    "SUFFICIENCY_VS_OVERENGINEERING",
    "READINESS_VERDICT",
    "UNCERTAINTY_DISCIPLINE",
}

class CalibrationManifestError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text())
    if not isinstance(obj, dict):
        raise CalibrationManifestError("manifest must be a JSON object")
    return obj


def validate_schema(manifest: dict[str, Any], schema_path: Path) -> None:
    try:
        import jsonschema
    except ImportError as exc:
        raise CalibrationManifestError("jsonschema dependency missing") from exc
    schema = json.loads(schema_path.read_text())
    try:
        jsonschema.Draft202012Validator(schema).validate(manifest)
    except jsonschema.ValidationError as exc:
        loc = ".".join(str(x) for x in exc.absolute_path) or "$"
        raise CalibrationManifestError(f"schema violation at {loc}: {exc.message}") from None


def enforce(manifest: dict[str, Any]) -> None:
    mechanisms = set(manifest["mechanisms"])
    levels = set(manifest["reference_levels"])
    rubric = set(manifest["rubric_dimensions"])

    missing_mechanisms = REQUIRED_MECHANISMS - mechanisms
    if missing_mechanisms:
        raise CalibrationManifestError("missing mechanisms: " + ", ".join(sorted(missing_mechanisms)))

    missing_levels = REQUIRED_LEVELS - levels
    if missing_levels:
        raise CalibrationManifestError("missing reference levels: " + ", ".join(sorted(missing_levels)))

    missing_rubric = REQUIRED_RUBRIC - rubric
    if missing_rubric:
        raise CalibrationManifestError("missing rubric dimensions: " + ", ".join(sorted(missing_rubric)))

    independence = manifest["independence"]
    if not independence["fresh_context"]:
        raise CalibrationManifestError("fresh independent evaluator context required")
    if independence["candidate_outputs_seen"]:
        raise CalibrationManifestError("candidate outputs must not be visible during B1 authoring")
    if independence["candidate_skill_used_as_authoring_source"]:
        raise CalibrationManifestError("candidate SKILL must not be used as B1 authoring source")

    pack = manifest["pack"]
    if pack["hidden_content_committed"]:
        raise CalibrationManifestError("hidden calibration content must not be committed publicly")
    if pack["exact_answer_prose_frozen"]:
        raise CalibrationManifestError("freeze decision properties, not one exact preferred prose answer")

    resources = manifest["resources"]
    zero_fields = ("candidate_calls", "judge_calls", "live_provider_calls", "metered_api_calls", "parallel_model_runs")
    for field in zero_fields:
        if resources[field] != 0:
            raise CalibrationManifestError(f"B1 resource contract violated: {field}={resources[field]}")
    if resources["author_sessions"] != 1:
        raise CalibrationManifestError("B1 default authoring budget is exactly one independent subscription-backed session")


def validate(manifest: dict[str, Any], schema_path: Path) -> None:
    validate_schema(manifest, schema_path)
    enforce(manifest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("--schema", default="architect/evaluation/qualification-reliability-engineer/stage-b/calibration-manifest.schema.json")
    args = parser.parse_args()
    try:
        manifest = load_json(Path(args.manifest))
        validate(manifest, Path(args.schema))
    except (CalibrationManifestError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "message": str(exc)}))
        return 2
    print(json.dumps({"status": "PASS", "evaluator_cycle": manifest["evaluator_cycle"], "case_count": manifest["pack"]["case_count"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
