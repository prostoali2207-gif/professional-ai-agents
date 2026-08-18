#!/usr/bin/env python3
"""OpenAI Responses API executor for the Growth Experimentation & Measurement harness.

Reads one JSON object from stdin and writes one JSON object to stdout.
Expected input fields:
- instructions: frozen candidate instructions
- fixture: structured experiment fixture
- output_schema: JSON Schema for the candidate result
- model: optional model override

Requires OPENAI_API_KEY. Never prints the key. Uses store=False so eval payloads are not intentionally persisted by this executor.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any


def fail(message: str, code: int = 2) -> None:
    print(json.dumps({"executor_error": message}, ensure_ascii=False))
    raise SystemExit(code)


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        fail("OPENAI_API_KEY is not configured")

    try:
        payload: dict[str, Any] = json.load(sys.stdin)
    except Exception as exc:
        fail(f"invalid stdin JSON: {exc}")

    instructions = payload.get("instructions")
    fixture = payload.get("fixture")
    output_schema = payload.get("output_schema")
    model = payload.get("model") or os.environ.get("ANALYTICS_EVAL_MODEL") or "gpt-5.6"

    if not isinstance(instructions, str) or not instructions.strip():
        fail("missing candidate instructions")
    if not isinstance(fixture, dict):
        fail("missing fixture object")
    if not isinstance(output_schema, dict):
        fail("missing output_schema object")

    try:
        from openai import OpenAI
    except Exception:
        fail("openai Python package is not installed")

    client = OpenAI()

    user_input = (
        "Evaluate the experiment fixture below strictly according to the frozen Analytics "
        "instructions. Return only the structured result required by the supplied schema. "
        "Do not invent missing values.\n\nFIXTURE:\n"
        + json.dumps(fixture, ensure_ascii=False, sort_keys=True)
    )

    try:
        response = client.responses.create(
            model=model,
            instructions=instructions,
            input=user_input,
            store=False,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "analytics_eval_result",
                    "strict": True,
                    "schema": output_schema,
                }
            },
        )
    except Exception as exc:
        fail(f"OpenAI Responses API call failed: {exc}")

    raw = getattr(response, "output_text", None)
    if not isinstance(raw, str) or not raw.strip():
        fail("model returned no output_text")

    try:
        result = json.loads(raw)
    except Exception as exc:
        fail(f"model output was not valid JSON: {exc}")

    print(json.dumps({"model": model, "result": result}, ensure_ascii=False))


if __name__ == "__main__":
    main()
