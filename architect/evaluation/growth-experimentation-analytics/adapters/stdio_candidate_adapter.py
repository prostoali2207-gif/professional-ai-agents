#!/usr/bin/env python3
"""Provider-neutral candidate adapter for Growth Experimentation & Measurement evals.

The harness owns fixtures and grading. This adapter owns only the execution boundary:
- build a candidate request envelope;
- call an external executor command;
- require one JSON response;
- propagate failures rather than inventing a result.

The external executor may bind any eligible model/runtime. It must not receive grader
answers, expected decisions, or sealed fixture metadata beyond the candidate-facing case.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
EVAL_ROOT = HERE.parent
MANIFEST_PATH = EVAL_ROOT / "candidate-manifest.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError(f"Expected object in {path}")
    return value


def build_envelope(fixture: dict[str, Any]) -> dict[str, Any]:
    manifest = load_json(MANIFEST_PATH)
    return {
        "protocol": "growth-experimentation-analytics-candidate-v1",
        "candidate": manifest,
        "task": {
            "instruction": (
                "Analyze exactly one experiment fixture using the frozen Analytics "
                "candidate instructions. Return only one JSON object matching the "
                "candidate output schema. Do not invent unavailable facts."
            ),
            "fixture": fixture,
        },
    }


def execute(envelope: dict[str, Any]) -> dict[str, Any]:
    raw_cmd = os.environ.get("ANALYTICS_CANDIDATE_CMD")
    if not raw_cmd:
        raise RuntimeError(
            "ANALYTICS_CANDIDATE_CMD is required. It must name an executor that reads "
            "one JSON request from stdin and writes one JSON result to stdout."
        )

    cmd = shlex.split(raw_cmd)
    completed = subprocess.run(
        cmd,
        input=json.dumps(envelope, ensure_ascii=False),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=int(os.environ.get("ANALYTICS_CANDIDATE_TIMEOUT_SECONDS", "120")),
        check=False,
    )

    if completed.returncode != 0:
        raise RuntimeError(
            f"Candidate executor failed with exit code {completed.returncode}: "
            f"{completed.stderr[-4000:]}"
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
        envelope = build_envelope(fixture)
        result = execute(envelope)
        json.dump(result, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    except Exception as exc:  # fail closed at process boundary
        print(f"adapter_error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
