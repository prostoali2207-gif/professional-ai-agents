"""Zero-call fault-injection contracts for qualification provider failures.

These tests exercise the provider boundary with synthetic failures only.
No network, model, quota, or provider credentials are used.
"""

from dataclasses import dataclass


@dataclass
class SyntheticProviderError(Exception):
    kind: str
    status: int | None = None


def classify_provider_failure(exc: Exception) -> str:
    if isinstance(exc, SyntheticProviderError):
        if exc.kind == "timeout":
            return "provider_timeout"
        if exc.kind == "connection_reset":
            return "provider_connection_reset"
        if exc.kind == "http_400":
            return "provider_bad_request"
    return "provider_unknown_failure"


def test_faults_are_classified_without_retry_permission():
    faults = [
        SyntheticProviderError("timeout"),
        SyntheticProviderError("connection_reset"),
        SyntheticProviderError("http_400", 400),
    ]
    assert [classify_provider_failure(f) for f in faults] == [
        "provider_timeout",
        "provider_connection_reset",
        "provider_bad_request",
    ]


def test_unknown_failure_is_fail_closed():
    assert classify_provider_failure(RuntimeError("synthetic")) == "provider_unknown_failure"
