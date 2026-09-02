#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
import urllib.error

import gemini_background_transport as g


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


class FakeOpener:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = []

    def __call__(self, req, timeout):
        self.calls.append((req.get_method(), req.full_url, timeout, req.data))
        if not self.outcomes:
            raise AssertionError("unexpected HTTP call")
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return FakeResponse(outcome)


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class GeminiBackgroundTransportTests(unittest.TestCase):
    def run_call(self, opener, clock=None, **kwargs):
        clock = clock or FakeClock()
        return g.run_background_interaction(
            {
                "model": "gemini-3.7-flash",
                "input": "public development fixture",
                "store": True,
                "generation_config": {"thinking_level": "medium"},
            },
            api_key="test-key",
            opener=opener,
            sleep=clock.sleep,
            monotonic=clock.monotonic,
            poll_interval_seconds=1,
            overall_timeout_seconds=30,
            **kwargs,
        )

    def test_create_once_then_poll_until_completed(self):
        opener = FakeOpener([
            {"id": "v1_abc", "status": "in_progress"},
            {"id": "v1_abc", "status": "in_progress"},
            {"id": "v1_abc", "status": "completed", "output_text": "done"},
        ])
        result = self.run_call(opener)
        self.assertEqual(result["output_text"], "done")
        self.assertEqual([call[0] for call in opener.calls], ["POST", "GET", "GET"])
        posted = json.loads(opener.calls[0][3].decode("utf-8"))
        self.assertIs(posted["background"], True)
        self.assertIs(posted["store"], True)

    def test_poll_timeout_is_retryable_without_duplicate_create(self):
        opener = FakeOpener([
            {"id": "v1_retry", "status": "in_progress"},
            TimeoutError("The read operation timed out"),
            {"id": "v1_retry", "status": "completed", "output_text": "done"},
        ])
        result = self.run_call(opener, max_consecutive_poll_transport_failures=1)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(sum(1 for call in opener.calls if call[0] == "POST"), 1)
        self.assertEqual(sum(1 for call in opener.calls if call[0] == "GET"), 2)

    def test_create_timeout_is_not_retried(self):
        opener = FakeOpener([TimeoutError("The read operation timed out")])
        with self.assertRaises(g.GeminiBackgroundTransportError) as ctx:
            self.run_call(opener)
        self.assertEqual(ctx.exception.code, "CREATE_TRANSPORT_UNCERTAIN")
        self.assertEqual(len(opener.calls), 1)
        self.assertEqual(opener.calls[0][0], "POST")

    def test_create_http_timeout_is_clamped_by_overall_deadline(self):
        opener = FakeOpener([{"id": "v1_fast", "status": "completed", "output_text": "done"}])
        clock = FakeClock()
        result = g.run_background_interaction(
            {"model": "gemini-3.7-flash", "input": "public", "store": True},
            api_key="test-key",
            opener=opener,
            sleep=clock.sleep,
            monotonic=clock.monotonic,
            create_timeout_seconds=30,
            overall_timeout_seconds=5,
        )
        self.assertEqual(result["status"], "completed")
        self.assertEqual(len(opener.calls), 1)
        self.assertEqual(opener.calls[0][0], "POST")
        self.assertEqual(opener.calls[0][2], 5)

    def test_terminal_non_completed_status_fails_closed(self):
        for status in ("failed", "cancelled", "incomplete", "requires_action"):
            with self.subTest(status=status):
                opener = FakeOpener([{"id": "v1_terminal", "status": status}])
                with self.assertRaises(g.GeminiBackgroundTransportError) as ctx:
                    self.run_call(opener)
                self.assertEqual(ctx.exception.code, "TERMINAL_NON_COMPLETED")

    def test_overall_deadline_is_bounded(self):
        opener = FakeOpener([{"id": "v1_slow", "status": "in_progress"}])
        clock = FakeClock()
        with self.assertRaises(g.GeminiBackgroundTransportError) as ctx:
            g.run_background_interaction(
                {"model": "gemini-3.7-flash", "input": "public", "store": True},
                api_key="test-key",
                opener=opener,
                sleep=clock.sleep,
                monotonic=clock.monotonic,
                poll_interval_seconds=2,
                overall_timeout_seconds=1,
            )
        self.assertEqual(ctx.exception.code, "BACKGROUND_DEADLINE_EXCEEDED")
        self.assertEqual([call[0] for call in opener.calls], ["POST"])

    def test_storage_requires_explicit_opt_in(self):
        for body in (
            {"model": "gemini-3.7-flash", "input": "public"},
            {"model": "gemini-3.7-flash", "input": "public", "store": False},
        ):
            with self.subTest(body=body):
                opener = FakeOpener([])
                with self.assertRaises(g.GeminiBackgroundTransportError) as ctx:
                    g.run_background_interaction(body, api_key="test-key", opener=opener)
                self.assertEqual(ctx.exception.code, "STORAGE_NOT_AUTHORIZED")
                self.assertEqual(opener.calls, [])

    def test_nontransient_poll_http_failure_does_not_retry(self):
        http_error = urllib.error.HTTPError(
            "https://example.test/v1", 400, "bad request", {}, None
        )
        opener = FakeOpener([
            {"id": "v1_bad", "status": "in_progress"},
            http_error,
        ])
        with self.assertRaises(g.GeminiBackgroundTransportError) as ctx:
            self.run_call(opener)
        self.assertEqual(ctx.exception.code, "POLL_TRANSPORT_FAILED")
        self.assertEqual([call[0] for call in opener.calls], ["POST", "GET"])


if __name__ == "__main__":
    unittest.main()
