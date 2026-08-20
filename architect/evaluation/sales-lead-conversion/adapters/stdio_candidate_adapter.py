#!/usr/bin/env python3
"""Provider-neutral candidate adapter for Sales / Lead Conversion held-out evals.

The sealed harness owns fixtures, grading, controlled tools and trial orchestration.
This adapter owns only the execution boundary:
- load an externally supplied frozen candidate manifest;
- construct one candidate request envelope;
- call an external executor command;
- require one JSON response with observable run evidence;
- propagate failures rather than inventing a result.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

PROTOCOL = "sales-lead-conversion-candidate-v1"
EXPECTED_COMMIT = "b1a5f214a7cc9452e8a168f3292a2e9b613ecae0"
EXPECTED_DIGEST = "sha256:6107413b9d6699f249d15903918f0943d26348f206d9e898d37b7058dac6dfa6"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError(f"Expected object in {path}")
    return value


def load_candidate_manifest() -> dict[str, Any]:
    raw = os.environ.get("SALES_CANDIDATE_MANIFEST")
    if not raw:
        raise RuntimeError("SALES_CANDIDATE_MANIFEST is required")
    manifest = load_json(Path(raw))

    commit = manifest.get("commit") or manifest.get("candidate_commit")
    digest = manifest.get("artifact_digest")
    if commit != EXPECTED_COMMIT:
        raise RuntimeError(f"Frozen candidate commit mismatch: {commit!r}")
    if digest != EXPECTED_DIGEST:
        raise RuntimeError(f"Frozen candidate digest mismatch: {digest!r}")
    return manifest


def build_envelope(harness_request: dict[str, Any]) -> dict[str, Any]:
    if harness_request.get("protocol") not in (None, PROTOCOL):
        raise ValueError("Unsupported protocol")

    return {
        "protocol": PROTOCOL,
        "candidate": load_candidate_manifest(),
        "run": harness_request.get("run", {}),
        "task": harness_request.get("task", {}),
        "initial_state": harness_request.get("initial_state", {}),
        "tool_scenario": harness_request.get("tool_scenario", {}),
        "checkpoint": harness_request.get("checkpoint"),
    }


def execute(envelope: dict[str, Any]) -> dict[str, Any]:
    raw_cmd = os.environ.get("SALES_CANDIDATE_CMD")
    if not raw_cmd:
        raise RuntimeError(
            "SALES_CANDIDATE_CMD is required and must name an executor that reads one JSON request from stdin"
        )

    completed = subprocess.run(
        shlex.split(raw_cmd),
        input=json.dumps(envelope, ensure_ascii=False),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=int(os.environ.get("SALES_CANDIDATE_TIMEOUT_SECONDS", "120")),
        check=False,
    )

    if completed.returncode != 0:
        raise RuntimeError(
            f"Candidate executor failed with exit code {completed.returncode}: {completed.stderr[-4000:]}"
        )

    stdout = completed.stdout.strip()
    if not stdout:
        raise RuntimeError("Candidate executor returned empty stdout")

    try:
        result = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Candidate executor returned non-JSON stdout") from exc

    if not isinstance(result, dict):
        raise RuntimeError("Candidate executor result must be one JSON object")
    if result.get("protocol") != PROTOCOL:
        raise RuntimeError("Candidate executor protocol mismatch")

    required_observables = [
        "run_id",
        "trial_id",
        "candidate_identity",
        "tool_calls",
        "state_before",
        "state_after",
        "side_effect_ledger",
        "termination_reason",
        "runtime_identity",
    ]
    missing = [key for key in required_observables if key not in result]
    if missing:
        raise RuntimeError(f"Candidate executor omitted required observables: {missing}")

    return result


def main() -> int:
    try:
        harness_request = json.load(sys.stdin)
        if not isinstance(harness_request, dict):
            raise ValueError("Harness request must be one JSON object")
        result = execute(build_envelope(harness_request))
        json.dump(result, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    except Exception as exc:
        print(f"adapter_error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
