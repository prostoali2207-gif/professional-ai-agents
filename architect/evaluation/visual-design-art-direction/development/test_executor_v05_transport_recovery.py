#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import io
import json
import sys
import unittest
import urllib.error
from pathlib import Path

MODULE_PATH = Path(__file__).with_name('executor_v05_structural_controller_public.py')
spec = importlib.util.spec_from_file_location('visual_v05_executor_transport_test', MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError('cannot load v0.5 executor')
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return json.dumps(self.payload).encode('utf-8')


class FakeOpener:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = []

    def __call__(self, req, timeout):
        self.calls.append((req.get_method(), req.full_url, timeout, req.data))
        if not self.outcomes:
            raise AssertionError('unexpected HTTP call')
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


def http_error(code: int, payload: dict) -> urllib.error.HTTPError:
    body = json.dumps(payload).encode('utf-8')
    return urllib.error.HTTPError(
        'https://generativelanguage.googleapis.com/v1beta/interactions/v1_test',
        code,
        'error',
        {},
        io.BytesIO(body),
    )


class VisualV05TransportRecoveryTests(unittest.TestCase):
    def test_exact_generic_poll_400_is_eligible_only_with_existing_id(self):
        exc = mod.GeminiBackgroundTransportError(
            'POLL_TRANSPORT_FAILED',
            'HTTP 400: {"error":{"message":"Request contains an invalid argument.","code":"invalid_request"}}',
            'v1_existing',
        )
        self.assertTrue(mod._eligible_generic_poll_400(exc))
        exc.interaction_id = None
        self.assertFalse(mod._eligible_generic_poll_400(exc))

    def test_generic_400_recovers_with_get_only_polling(self):
        clock = FakeClock()
        opener = FakeOpener([
            http_error(400, {'error': {'message': mod.GENERIC_INVALID_REQUEST_MESSAGE, 'code': 'invalid_request'}}),
            {'id': 'v1_existing', 'status': 'in_progress'},
            {'id': 'v1_existing', 'status': 'completed', 'output_text': 'done'},
        ])
        result = mod.recover_existing_interaction(
            'v1_existing',
            api_key='test-key',
            grace_seconds=40,
            poll_interval_seconds=5,
            opener=opener,
            sleep=clock.sleep,
            monotonic=clock.monotonic,
        )
        self.assertEqual(result['status'], 'completed')
        self.assertEqual([call[0] for call in opener.calls], ['GET', 'GET', 'GET'])
        self.assertTrue(all(call[3] is None for call in opener.calls))

    def test_parameter_specific_400_fails_closed_without_retry(self):
        clock = FakeClock()
        opener = FakeOpener([
            http_error(400, {'error': {'message': 'Unknown name stream', 'code': 'invalid_request'}}),
        ])
        with self.assertRaises(RuntimeError) as ctx:
            mod.recover_existing_interaction(
                'v1_existing',
                api_key='test-key',
                grace_seconds=40,
                poll_interval_seconds=5,
                opener=opener,
                sleep=clock.sleep,
                monotonic=clock.monotonic,
            )
        self.assertIn('poll recovery HTTP 400', str(ctx.exception))
        self.assertEqual(len(opener.calls), 1)
        self.assertEqual(opener.calls[0][0], 'GET')

    def test_generic_400_grace_is_bounded(self):
        clock = FakeClock()
        generic = {'error': {'message': mod.GENERIC_INVALID_REQUEST_MESSAGE, 'code': 'invalid_request'}}
        opener = FakeOpener([http_error(400, generic), http_error(400, generic)])
        with self.assertRaises(RuntimeError) as ctx:
            mod.recover_existing_interaction(
                'v1_existing',
                api_key='test-key',
                grace_seconds=10,
                poll_interval_seconds=5,
                opener=opener,
                sleep=clock.sleep,
                monotonic=clock.monotonic,
            )
        self.assertIn('POLL_GENERIC_INVALID_REQUEST_GRACE_EXHAUSTED', str(ctx.exception))
        self.assertEqual([call[0] for call in opener.calls], ['GET'])


if __name__ == '__main__':
    unittest.main()
