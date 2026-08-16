#!/usr/bin/env python3
"""Rate-aware transport wrapper for gemini_interactions_adapter.

The behavioral/tool adapter remains provider-neutral and fixture-independent.
This wrapper adds provider-health/model-runtime policy only:
- proactive cross-process request pacing;
- optional official Interactions `generation_config.thinking_level`;
- one bounded retry for a 429 only when the provider supplies a short retry-in
  duration, or for one 503 capacity transient;
- repeated/ambiguous quota exhaustion remains non-retriable and creates a shared
  provider block so later fixture processes do not create a retry storm.
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request

import gemini_interactions_adapter as base

LAST_CALL = base.ROOT / ".tmp" / "gemini-adapter-last-call.txt"
MIN_INTERVAL_SECONDS = float(os.environ.get("GEMINI_MIN_REQUEST_INTERVAL", "13"))
MAX_TRANSIENT_RETRY_SECONDS = float(os.environ.get("GEMINI_MAX_TRANSIENT_RETRY", "60"))


def wait_for_rate_slot() -> None:
    LAST_CALL.parent.mkdir(parents=True, exist_ok=True)
    last = 0.0
    if LAST_CALL.exists():
        try:
            last = float(LAST_CALL.read_text(encoding="utf-8").strip())
        except Exception:
            last = 0.0
    wait = MIN_INTERVAL_SECONDS - (time.time() - last)
    if wait > 0:
        time.sleep(wait)
    LAST_CALL.write_text(str(time.time()), encoding="utf-8")


def provider_retry_seconds(body: str) -> float | None:
    match = re.search(r"retry\s+in\s+([0-9]+(?:\.[0-9]+)?)s", body, flags=re.IGNORECASE)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def configured_payload(payload: dict) -> dict:
    value = dict(payload)
    thinking = os.environ.get("GEMINI_THINKING_LEVEL", "").strip().lower()
    if thinking:
        if thinking not in {"minimal", "low", "medium", "high"}:
            base.fail(f"unsupported GEMINI_THINKING_LEVEL: {thinking}")
        cfg = dict(value.get("generation_config") or {})
        cfg["thinking_level"] = thinking
        value["generation_config"] = cfg
    return value


def api_call(payload: dict, *, allow_one_503_retry: bool = True) -> dict:
    if base.PROVIDER_BLOCK.exists():
        block = base.load_json(base.PROVIDER_BLOCK, {})
        base.fail(f"provider calls blocked after prior non-retriable failure in this run: {json.dumps(block, ensure_ascii=False)}")
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        base.fail("GEMINI_API_KEY is not configured")
    request_body = configured_payload(payload)

    for attempt in range(2):
        wait_for_rate_slot()
        req = urllib.request.Request(
            base.INTERACTIONS_ENDPOINT,
            data=json.dumps(request_body).encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json", "x-goog-api-key": key},
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                raw = json.loads(response.read().decode("utf-8"))
            if not isinstance(raw, dict):
                base.fail("Gemini Interactions returned non-object JSON")
            return raw
        except urllib.error.HTTPError as exc:
            body = exc.read().decode(errors="replace")
            failure_class = base.classify_http_error(exc.code, body)
            retry_s = provider_retry_seconds(body)
            record = {
                "http_status": exc.code,
                "failure_class": failure_class,
                "provider_retry_seconds": retry_s,
                "body": body[:4000],
            }
            short_429 = (
                exc.code == 429
                and retry_s is not None
                and 0 < retry_s <= MAX_TRANSIENT_RETRY_SECONDS
                and attempt == 0
            )
            transient_503 = exc.code == 503 and allow_one_503_retry and attempt == 0
            if short_429:
                time.sleep(retry_s + 1.0)
                continue
            if transient_503:
                time.sleep(2.0)
                continue
            if exc.code in {401, 403, 404, 429}:
                base.save_json(base.PROVIDER_BLOCK, record)
            base.fail(f"Gemini Interactions failure: {json.dumps(record, ensure_ascii=False)}")
        except urllib.error.URLError as exc:
            base.fail(f"Gemini transport failure: {exc}")
        except json.JSONDecodeError as exc:
            base.fail(f"Gemini response JSON parse failure: {exc}")

    base.fail("Gemini call exhausted bounded retry policy")


def main() -> int:
    base.api_call = api_call
    return base.main()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        base.fail(f"Gemini rate-aware adapter failed: {exc}")
