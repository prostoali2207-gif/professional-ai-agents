#!/usr/bin/env python3
"""Reusable Gemini Interactions background transport for eligible evaluation calls.

This module owns transport reliability only. It does not own professional fixtures,
judges, thresholds, candidate behavior, or release semantics.

Background Interactions require retrievable server-side state. Callers must opt in
explicitly with ``store=True`` after deciding that provider retention is compatible
with the evaluation data. Hidden/sealed material must not be routed through this
helper merely to avoid a synchronous timeout.
"""
from __future__ import annotations

import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable

DEFAULT_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
DEFAULT_API_REVISION = "2026-05-20"


@dataclass
class GeminiBackgroundTransportError(RuntimeError):
    code: str
    message: str
    interaction_id: str | None = None

    def __str__(self) -> str:
        suffix = f" interaction_id={self.interaction_id}" if self.interaction_id else ""
        return f"{self.code}: {self.message}{suffix}"


class _TransportFailure(RuntimeError):
    def __init__(self, message: str, *, status: int | None = None, transient: bool = False):
        super().__init__(message)
        self.status = status
        self.transient = transient


def _decode_response(response: Any) -> dict[str, Any]:
    try:
        payload = json.loads(response.read().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise _TransportFailure(f"invalid JSON response: {exc}") from None
    if not isinstance(payload, dict):
        raise _TransportFailure("response must be a JSON object")
    return payload


def _request_json(
    req: urllib.request.Request,
    *,
    timeout: float,
    opener: Callable[..., Any],
) -> dict[str, Any]:
    try:
        with opener(req, timeout=timeout) as response:
            return _decode_response(response)
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", "replace")[-1000:]
        except Exception:
            detail = ""
        transient = exc.code in (408, 429) or 500 <= exc.code < 600
        raise _TransportFailure(
            f"HTTP {exc.code}: {detail or exc.reason}", status=exc.code, transient=transient
        ) from None
    except (TimeoutError, socket.timeout) as exc:
        raise _TransportFailure(f"timeout: {exc}", transient=True) from None
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", exc)
        transient = isinstance(reason, (TimeoutError, socket.timeout, OSError))
        raise _TransportFailure(f"URL error: {reason}", transient=transient) from None
    except OSError as exc:
        raise _TransportFailure(f"network error: {exc}", transient=True) from None


def _status(payload: dict[str, Any]) -> str:
    value = payload.get("status")
    if not isinstance(value, str) or not value.strip():
        raise GeminiBackgroundTransportError("MALFORMED_RESPONSE", "interaction status missing")
    return value.strip().lower()


def run_background_interaction(
    body: dict[str, Any],
    *,
    api_key: str,
    endpoint: str = DEFAULT_ENDPOINT,
    api_revision: str = DEFAULT_API_REVISION,
    create_timeout_seconds: float = 30.0,
    poll_timeout_seconds: float = 30.0,
    poll_interval_seconds: float = 5.0,
    overall_timeout_seconds: float = 600.0,
    max_consecutive_poll_transport_failures: int = 3,
    opener: Callable[..., Any] = urllib.request.urlopen,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """Create one background interaction and poll it to a terminal state.

    Safety/idempotency contract:
    - the create POST is submitted exactly once; an ambiguous create transport
      failure is never retried automatically because that could duplicate a
      paid/model call;
    - only idempotent GET polling may retry transient transport failures;
    - a bounded overall deadline applies to the whole operation, including create;
    - every non-completed terminal/unknown state fails closed.
    """
    if not isinstance(body, dict):
        raise GeminiBackgroundTransportError("INVALID_REQUEST", "body must be an object")
    if not api_key or not api_key.strip():
        raise GeminiBackgroundTransportError("CREDENTIAL_MISSING", "Gemini API key missing")
    if body.get("store") is not True:
        raise GeminiBackgroundTransportError(
            "STORAGE_NOT_AUTHORIZED",
            "background execution requires explicit store=True after retention/privacy review",
        )
    if create_timeout_seconds <= 0 or poll_timeout_seconds <= 0:
        raise GeminiBackgroundTransportError("INVALID_TIMEOUT", "HTTP timeouts must be positive")
    if poll_interval_seconds < 0 or overall_timeout_seconds <= 0:
        raise GeminiBackgroundTransportError("INVALID_TIMEOUT", "poll/overall timeout invalid")
    if max_consecutive_poll_transport_failures < 0:
        raise GeminiBackgroundTransportError("INVALID_RETRY_BUDGET", "poll retry budget must be >= 0")

    start = monotonic()
    deadline = start + overall_timeout_seconds
    request_body = dict(body)
    request_body["background"] = True

    headers = {
        "x-goog-api-key": api_key.strip(),
        "Content-Type": "application/json",
        "Api-Revision": api_revision,
        "User-Agent": "professional-ai-agents-qualification/1.0",
    }
    create_req = urllib.request.Request(
        endpoint,
        data=json.dumps(request_body, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers=headers,
    )

    remaining_for_create = deadline - monotonic()
    if remaining_for_create <= 0:
        raise GeminiBackgroundTransportError(
            "BACKGROUND_DEADLINE_EXCEEDED", "overall background deadline exceeded before create"
        )

    # Intentionally single-submit. A timeout here is ambiguous: the server may
    # have accepted the model call even though the client did not receive its ID.
    try:
        payload = _request_json(
            create_req,
            timeout=min(create_timeout_seconds, max(0.001, remaining_for_create)),
            opener=opener,
        )
    except _TransportFailure as exc:
        raise GeminiBackgroundTransportError("CREATE_TRANSPORT_UNCERTAIN", str(exc)) from None

    interaction_id = payload.get("id")
    if not isinstance(interaction_id, str) or not interaction_id.strip():
        raise GeminiBackgroundTransportError("MALFORMED_RESPONSE", "interaction id missing")
    interaction_id = interaction_id.strip()

    try:
        status = _status(payload)
    except GeminiBackgroundTransportError as exc:
        exc.interaction_id = interaction_id
        raise
    if status == "completed":
        return payload
    if status != "in_progress":
        raise GeminiBackgroundTransportError(
            "TERMINAL_NON_COMPLETED", f"interaction ended with status {status}", interaction_id
        )

    poll_url = endpoint.rstrip("/") + "/" + urllib.parse.quote(interaction_id, safe="")
    consecutive_poll_failures = 0

    while True:
        remaining = deadline - monotonic()
        if remaining <= 0:
            raise GeminiBackgroundTransportError(
                "BACKGROUND_DEADLINE_EXCEEDED", "overall background deadline exceeded", interaction_id
            )
        if poll_interval_seconds:
            sleep(min(poll_interval_seconds, remaining))
        if monotonic() >= deadline:
            raise GeminiBackgroundTransportError(
                "BACKGROUND_DEADLINE_EXCEEDED", "overall background deadline exceeded", interaction_id
            )

        get_req = urllib.request.Request(
            poll_url,
            method="GET",
            headers={
                "x-goog-api-key": api_key.strip(),
                "Api-Revision": api_revision,
                "Accept": "application/json",
                "User-Agent": "professional-ai-agents-qualification/1.0",
            },
        )
        try:
            payload = _request_json(
                get_req,
                timeout=min(poll_timeout_seconds, max(0.001, deadline - monotonic())),
                opener=opener,
            )
            consecutive_poll_failures = 0
        except _TransportFailure as exc:
            if not exc.transient:
                raise GeminiBackgroundTransportError(
                    "POLL_TRANSPORT_FAILED", str(exc), interaction_id
                ) from None
            consecutive_poll_failures += 1
            if consecutive_poll_failures > max_consecutive_poll_transport_failures:
                raise GeminiBackgroundTransportError(
                    "POLL_RETRY_BUDGET_EXHAUSTED", str(exc), interaction_id
                ) from None
            continue

        try:
            status = _status(payload)
        except GeminiBackgroundTransportError as exc:
            exc.interaction_id = interaction_id
            raise
        if status == "completed":
            return payload
        if status == "in_progress":
            continue
        raise GeminiBackgroundTransportError(
            "TERMINAL_NON_COMPLETED", f"interaction ended with status {status}", interaction_id
        )
