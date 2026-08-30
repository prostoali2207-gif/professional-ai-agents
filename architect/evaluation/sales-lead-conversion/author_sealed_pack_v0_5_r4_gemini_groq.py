#!/usr/bin/env python3
from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = Path.cwd()
R3_PATH = ROOT / 'architect/evaluation/sales-lead-conversion/author_sealed_pack_v0_5_r3_gemini_groq.py'
R3_BLOB = '0c3025e3710b46223a7b27540e4c8bd9f9a7a86f'
ASSEMBLER_PATH = ROOT / 'architect/evaluation/sales-lead-conversion/effective_prereg_v0_5_r4.py'
ASSEMBLER_BLOB = 'afd346067875140aa113d662e159dfd421e7160b'
DELTA = ROOT / 'architect/evaluation/sales-lead-conversion/qualification-preregistration-v0_5-r4-gemini-groq.json'
DELTA_BLOB = 'd7944144c73656839f7a0c7b965a70e9194f0dd5'
CYCLE = 'sales-0.5-fresh-independent-2026-08-30-r4-gemini-groq'
OUT_ROOT = ROOT / 'architect/evaluation/sales-lead-conversion/sealed/runtime-sales-0.5-r4-author'
COMMIT = '2b8a397d16f2b0e8d7ad93c341f0031ec7dce4df'
DIGEST = 'sha256:0e7b46f186269968df12d09f64d48c88e173196a8b59f69a4e1ba1a049f4f1d9'
MAX_GROQ_WAIT_SECONDS = 2700.0
SAFETY_BUFFER_SECONDS = 5.0


def load_module(path: Path, expected_blob: str, name: str):
    actual = subprocess.check_output(['git', 'hash-object', str(path)], text=True).strip()
    if actual != expected_blob:
        raise RuntimeError(f'{name} drift: {actual}')
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'cannot load {name}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_retry_wait_seconds(retry_after: str | None, detail: str) -> float | None:
    if retry_after:
        try:
            return max(0.0, float(retry_after))
        except Exception:
            pass
    match = re.search(r'try again in\s+(?:(\d+)m)?([0-9]+(?:\.[0-9]+)?)s', detail, re.IGNORECASE)
    if not match:
        return None
    minutes = float(match.group(1) or 0)
    seconds = float(match.group(2))
    return minutes * 60.0 + seconds


def main() -> int:
    actual_delta = subprocess.check_output(['git', 'hash-object', str(DELTA)], text=True).strip()
    if actual_delta != DELTA_BLOB:
        raise RuntimeError(f'r4 prereg drift: {actual_delta}')
    delta = json.loads(DELTA.read_text())
    if delta.get('cycle_id') != CYCLE:
        raise RuntimeError('sales 0.5 r4 cycle mismatch')
    frozen = delta.get('frozen_candidate', {})
    if frozen.get('commit') != COMMIT or frozen.get('artifact_digest') != DIGEST:
        raise RuntimeError('sales 0.5 r4 frozen candidate mismatch')
    r3_evidence = delta.get('prior_sanitized_evidence', {}).get('r3', {})
    if r3_evidence.get('run_id') != 33310578863 or r3_evidence.get('candidate_calls') != 0:
        raise RuntimeError('sales 0.5 r4 r3 evidence mismatch')
    resilience = delta.get('provider_resilience_remediation', {})
    if resilience.get('provider') != 'groq-openai-compatible-api' or resilience.get('model') != 'openai/gpt-oss-120b':
        raise RuntimeError('sales 0.5 r4 Groq identity drift')
    if resilience.get('retry_count') != 1 or float(resilience.get('maximum_wait_seconds', -1)) != MAX_GROQ_WAIT_SECONDS:
        raise RuntimeError('sales 0.5 r4 retry contract drift')
    if resilience.get('judge_identity_change') is not False or resilience.get('model_change') is not False:
        raise RuntimeError('sales 0.5 r4 judge mutation forbidden')

    r3 = load_module(R3_PATH, R3_BLOB, 'sales_v05_r4_r3_transport')
    load_module(ASSEMBLER_PATH, ASSEMBLER_BLOB, 'sales_v05_r4_prereg_probe')

    r3.ASSEMBLER_PATH = ASSEMBLER_PATH
    r3.ASSEMBLER_BLOB = ASSEMBLER_BLOB
    r3.DELTA = DELTA
    r3.OUT_ROOT = OUT_ROOT
    r3.CYCLE = CYCLE

    original_urlopen = urllib.request.urlopen
    delayed_retry_used = False

    def resilient_urlopen(req, *args, **kwargs):
        nonlocal delayed_retry_used
        url = getattr(req, 'full_url', '')
        if 'api.groq.com' not in url:
            return original_urlopen(req, *args, **kwargs)
        try:
            return original_urlopen(req, *args, **kwargs)
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or delayed_retry_used:
                raise
            detail = exc.read().decode('utf-8', 'replace')[-1200:]
            retry_after = exc.headers.get('Retry-After') if exc.headers else None
            wait = parse_retry_wait_seconds(retry_after, detail)
            if wait is None or wait > MAX_GROQ_WAIT_SECONDS:
                raise RuntimeError('GROQ_429_RETRY_WINDOW_UNAVAILABLE_OR_OUT_OF_BOUNDS') from None
            delayed_retry_used = True
            delay = wait + SAFETY_BUFFER_SECONDS
            print(json.dumps({
                'status': 'GROQ_429_DELAYED_RETRY',
                'wait_seconds': round(delay, 3),
                'retry_count': 1,
                'candidate_calls': 0,
                'hidden_content_printed': False,
            }, sort_keys=True), file=sys.stderr, flush=True)
            time.sleep(delay)
            try:
                return original_urlopen(req, *args, **kwargs)
            except urllib.error.HTTPError as retry_exc:
                if retry_exc.code == 429:
                    raise RuntimeError('GROQ_429_DELAYED_RETRY_EXHAUSTED') from None
                raise

    captured = io.StringIO()
    urllib.request.urlopen = resilient_urlopen
    try:
        try:
            with redirect_stdout(captured):
                rc = int(r3.main())
        except RuntimeError as exc:
            if str(exc) in {'GROQ_429_RETRY_WINDOW_UNAVAILABLE_OR_OUT_OF_BOUNDS', 'GROQ_429_DELAYED_RETRY_EXHAUSTED'}:
                print(json.dumps({
                    'status': 'NOT_EXECUTABLE_GROQ_PROVIDER_CAPACITY_R4',
                    'provider_failure_code': str(exc),
                    'candidate_calls': 0,
                    'hidden_content_printed': False,
                }, sort_keys=True))
                return 21
            raise
    finally:
        urllib.request.urlopen = original_urlopen

    for line in captured.getvalue().splitlines():
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                status = obj.get('status')
                if isinstance(status, str):
                    obj['status'] = status.replace('V05_R3', 'V05_R4').replace('v05_r3', 'v05_r4')
                obj['cycle_id'] = CYCLE
                obj['groq_delayed_retry_used'] = delayed_retry_used
            print(json.dumps(obj, sort_keys=True))
        except Exception:
            print(line)
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
