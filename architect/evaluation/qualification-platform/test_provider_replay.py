#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import io
import json
import os
import urllib.error
from pathlib import Path

import pytest

RUNNER = Path('architect/evaluation/growth_strategy_experiment_portfolio/sealed_runner_template_v0_1_r2.py')
spec = importlib.util.spec_from_file_location('strategist_runner', RUNNER)
runner = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(runner)

class FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode()
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self): return self.payload


def test_groq_success_replay_parses_without_network(monkeypatch):
    os.environ['GROQ_API_KEY'] = 'synthetic-dev-key'
    seen = {}
    def fake_urlopen(req, timeout=0):
        seen['body'] = json.loads(req.data.decode())
        return FakeResponse({'choices':[{'message':{'content':'{"results":[]}'}}]})
    monkeypatch.setattr(runner.urllib.request, 'urlopen', fake_urlopen)
    out = runner.call_groq({'mode':'dev-replay'})
    assert out == {'results': []}
    assert seen['body']['model'] == runner.GROQ_JUDGE
    assert seen['body']['response_format'] == {'type':'json_object'}


def test_groq_400_replay_is_reproducible_without_network(monkeypatch):
    os.environ['GROQ_API_KEY'] = 'synthetic-dev-key'
    body = io.BytesIO(b'{"error":{"message":"synthetic bad request"}}')
    err = urllib.error.HTTPError(runner.GROQ_ENDPOINT, 400, 'Bad Request', {}, body)
    def fake_urlopen(req, timeout=0):
        raise err
    monkeypatch.setattr(runner.urllib.request, 'urlopen', fake_urlopen)
    with pytest.raises(urllib.error.HTTPError) as exc:
        runner.call_groq({'mode':'dev-replay'})
    assert exc.value.code == 400
