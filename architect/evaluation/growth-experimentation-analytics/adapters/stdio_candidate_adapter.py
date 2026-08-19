#!/usr/bin/env python3
"""Provider-neutral candidate adapter for Growth Experimentation & Measurement evals.

The harness owns fixtures and grading. This adapter owns only the execution boundary:
- load an externally supplied frozen candidate manifest;
- build one candidate request envelope;
- call an external executor command;
- require one JSON response;
- propagate failures rather than inventing a result.

No project-specific candidate is stored in this repository.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError(f"Expected object in {path}")
    return value


def load_manifest() -> dict[str, Any]:
    raw = os.environ.get("ANALYTICS_CANDIDATE_MANIFEST")
    if not raw:
        raise RuntimeError(
            "ANALYTICS_CANDIDATE_MANIFEST is required and must point to an external frozen candidate manifest"
        )
    return load_json(Path(raw))


def build_envelope(fixture: dict[str, Any]) -> dict[str, Any]:
    return {
        "protocol": "growth-experimentation-analytics-candidate-v1",
        "candidate": load_manifest(),
        "task": {
            "instruction": (
                "Analyze exactly one experiment fixture using the frozen Analytics candidate instructions. "
                "Return only one JSON object matching the candidate output schema. "
                "Do not invent unavailable facts."
            ),
            "fixture": fixture,
        },
    }


def execute(envelope: dict[str, Any]) -> dict[str, Any]:
    raw_cmd = os.environ.get("ANALYTICS_CANDIDATE_CMD")
    if not raw_cmd:
        raise RuntimeError(
            "ANALYTICS_CANDIDATE_CMD is required. It must name an executor that reads one JSON request "
            "from stdin and writes one JSON result to stdout."
        )

    completed = subprocess.run(
        shlex.split(raw_cmd),
        input=json.dumps(envelope, ensure_ascii=False),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=int(os.environ.get("ANALYTICS_CANDIDATE_TIMEOUT_SECONDS", "120")),
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
    return result


def main() -> int:
    try:
        fixture = json.load(sys.stdin)
        if not isinstance(fixture, dict):
            raise ValueError("Fixture must be one JSON object")
        result = execute(build_envelope(fixture))
        json.dump(result, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    except Exception as exc:
        print(f"adapter_error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
