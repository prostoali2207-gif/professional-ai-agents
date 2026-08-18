#!/usr/bin/env python3
"""OpenAI Responses API executor for the Growth Experimentation & Measurement harness.

Reads one JSON object from stdin and writes one JSON object to stdout.
Expected input fields:
- instructions: frozen candidate instructions
- fixture: structured experiment fixture
- output_schema: JSON Schema for the candidate result
- model: optional model override

Requires OPENAI_API_KEY. Never prints the key. Uses store=False so eval payloads are not intentionally persisted by this executor.

Budget safety
-------------
The executor is fail-closed and enforces a conservative cumulative budget ledger.
Defaults:
- ANALYTICS_EVAL_MAX_USD=1.00
- ANALYTICS_EVAL_MAX_REQUESTS=14
- ANALYTICS_EVAL_MAX_OUTPUT_TOKENS=1200 per request
- ANALYTICS_EVAL_BUDGET_LEDGER=.analytics-eval-budget.json

Cost accounting intentionally uses a conservative ceiling rate rather than assuming the selected model is cheap:
- input ceiling: $5 / 1M tokens
- output ceiling: $30 / 1M tokens
These match GPT-5.6 Sol standard token prices as of 2026-08-18 and therefore overestimate Terra/Luna standard cost. Override only after verifying current official pricing.

Because exact input-token count is known only after execution, a request is admitted only if the remaining budget can cover the configured maximum output plus a conservative character-based input-token upper estimate. The post-call ledger uses the API's actual usage counts and refuses further calls once the cumulative ceiling estimate reaches the configured budget.
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path
from typing import Any

INPUT_USD_PER_MILLION_CEILING = float(os.environ.get("ANALYTICS_EVAL_INPUT_USD_PER_MILLION_CEILING", "5"))
OUTPUT_USD_PER_MILLION_CEILING = float(os.environ.get("ANALYTICS_EVAL_OUTPUT_USD_PER_MILLION_CEILING", "30"))
MAX_USD = float(os.environ.get("ANALYTICS_EVAL_MAX_USD", "1.00"))
MAX_REQUESTS = int(os.environ.get("ANALYTICS_EVAL_MAX_REQUESTS", "14"))
MAX_OUTPUT_TOKENS = int(os.environ.get("ANALYTICS_EVAL_MAX_OUTPUT_TOKENS", "1200"))
LEDGER_PATH = Path(os.environ.get("ANALYTICS_EVAL_BUDGET_LEDGER", ".analytics-eval-budget.json"))


def fail(message: str, code: int = 2) -> None:
    print(json.dumps({"executor_error": message}, ensure_ascii=False))
    raise SystemExit(code)


def load_ledger() -> dict[str, Any]:
    if not LEDGER_PATH.exists():
        return {"requests": 0, "input_tokens": 0, "output_tokens": 0, "ceiling_cost_usd": 0.0}
    try:
        data = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"budget ledger is unreadable: {exc}")
    for key in ("requests", "input_tokens", "output_tokens", "ceiling_cost_usd"):
        if key not in data:
            fail(f"budget ledger missing field: {key}")
    return data


def save_ledger(data: dict[str, Any]) -> None:
    tmp = LEDGER_PATH.with_suffix(LEDGER_PATH.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(LEDGER_PATH)


def ceiling_cost(input_tokens: int, output_tokens: int) -> float:
    return (
        input_tokens * INPUT_USD_PER_MILLION_CEILING / 1_000_000
        + output_tokens * OUTPUT_USD_PER_MILLION_CEILING / 1_000_000
    )


def conservative_input_upper_bound(text: str) -> int:
    # Deliberately conservative for ordinary UTF-8 prose/JSON: at most one token per character.
    # This substantially overestimates normal English/Russian prompt tokenization and is used
    # only as a pre-call financial safety bound, not for analytical inference.
    return len(text)


def get_usage(response: Any) -> tuple[int, int]:
    usage = getattr(response, "usage", None)
    if usage is None:
        fail("API response did not expose usage; cannot update budget safely")
    input_tokens = getattr(usage, "input_tokens", None)
    output_tokens = getattr(usage, "output_tokens", None)
    if not isinstance(input_tokens, int) or not isinstance(output_tokens, int):
        fail("API usage token counts are unavailable; cannot update budget safely")
    return input_tokens, output_tokens


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
    model = payload.get("model") or os.environ.get("ANALYTICS_EVAL_MODEL") or "gpt-5.6-luna"

    if not isinstance(instructions, str) or not instructions.strip():
        fail("missing candidate instructions")
    if not isinstance(fixture, dict):
        fail("missing fixture object")
    if not isinstance(output_schema, dict):
        fail("missing output_schema object")

    user_input = (
        "Evaluate the experiment fixture below strictly according to the frozen Analytics "
        "instructions. Return only the structured result required by the supplied schema. "
        "Do not invent missing values.\n\nFIXTURE:\n"
        + json.dumps(fixture, ensure_ascii=False, sort_keys=True)
    )

    ledger = load_ledger()
    if int(ledger["requests"]) >= MAX_REQUESTS:
        fail(f"budget guard: request limit reached ({MAX_REQUESTS})")
    if float(ledger["ceiling_cost_usd"]) >= MAX_USD:
        fail(f"budget guard: USD limit reached (${MAX_USD:.2f})")

    prompt_for_bound = instructions + "\n" + user_input + "\n" + json.dumps(output_schema, ensure_ascii=False)
    input_upper = conservative_input_upper_bound(prompt_for_bound)
    worst_next_cost = ceiling_cost(input_upper, MAX_OUTPUT_TOKENS)
    remaining = MAX_USD - float(ledger["ceiling_cost_usd"])
    if worst_next_cost > remaining:
        fail(
            "budget guard: next request could exceed remaining ceiling budget "
            f"(remaining=${remaining:.4f}, worst_next=${worst_next_cost:.4f})"
        )

    try:
        from openai import OpenAI
    except Exception:
        fail("openai Python package is not installed")

    client = OpenAI()

    try:
        response = client.responses.create(
            model=model,
            instructions=instructions,
            input=user_input,
            store=False,
            max_output_tokens=MAX_OUTPUT_TOKENS,
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

    input_tokens, output_tokens = get_usage(response)
    request_ceiling_cost = ceiling_cost(input_tokens, output_tokens)
    ledger = {
        "requests": int(ledger["requests"]) + 1,
        "input_tokens": int(ledger["input_tokens"]) + input_tokens,
        "output_tokens": int(ledger["output_tokens"]) + output_tokens,
        "ceiling_cost_usd": round(float(ledger["ceiling_cost_usd"]) + request_ceiling_cost, 8),
    }
    save_ledger(ledger)

    if float(ledger["ceiling_cost_usd"]) > MAX_USD + 1e-9:
        fail("budget guard invariant violated after API call; further calls are blocked")

    raw = getattr(response, "output_text", None)
    if not isinstance(raw, str) or not raw.strip():
        fail("model returned no output_text")

    try:
        result = json.loads(raw)
    except Exception as exc:
        fail(f"model output was not valid JSON: {exc}")

    print(
        json.dumps(
            {
                "model": model,
                "result": result,
                "usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "request_ceiling_cost_usd": round(request_ceiling_cost, 8),
                    "cumulative_ceiling_cost_usd": ledger["ceiling_cost_usd"],
                    "requests_used": ledger["requests"],
                    "requests_limit": MAX_REQUESTS,
                    "budget_limit_usd": MAX_USD,
                },
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
