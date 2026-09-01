#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys

BASE = Path('architect/evaluation/sales-lead-conversion/executor_v0_3_gemini.py')
EXPECTED_BASE_BLOB = '687942c914253be472a338fcd033f86ced0caa2d'
FROZEN_COMMIT = '2b8a397d16f2b0e8d7ad93c341f0031ec7dce4df'
FROZEN_DIGEST = 'sha256:0e7b46f186269968df12d09f64d48c88e173196a8b59f69a4e1ba1a049f4f1d9'
MANIFEST_PATH = 'architect/library/cores/sales-lead-conversion/0.5.0/manifest.json'
EXECUTOR_ID = 'sales-lead-conversion/executor_v0_5_gemini_contract_v1.py@v1-paced'


def load_base():
    actual = subprocess.check_output(['git', 'hash-object', str(BASE)], text=True).strip()
    if actual != EXPECTED_BASE_BLOB:
        raise RuntimeError(f'base Gemini executor drift: {actual}')
    spec = importlib.util.spec_from_file_location('sales_v05_gemini_base', BASE)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load pinned Gemini executor')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.common.FROZEN_COMMIT = FROZEN_COMMIT
    m.common.FROZEN_DIGEST = FROZEN_DIGEST
    m.common.MANIFEST_PATH = MANIFEST_PATH
    m.EXECUTOR_ID = EXECUTOR_ID
    return m


def contract() -> dict:
    return {
        'contract_version': 1,
        'candidate_commit': FROZEN_COMMIT,
        'candidate_digest': FROZEN_DIGEST,
        'core': 'sales-lead-conversion/0.5.0',
        'executor': EXECUTOR_ID,
        'provider': 'gemini-interactions-api',
        'input_protocol': 'sales-lead-conversion-candidate-v1',
        'tool_protocol': 'sales-deterministic-tools-v1',
        'state_protocol': 'sales-state-checkpoint-v1',
        'observable_protocol': 'sales-observable-ledger-v1',
        'quota_policy': 'project-paced-6s-one-transient-retry-before-result',
    }


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == '--qualification-contract':
        json.dump(contract(), sys.stdout, sort_keys=True)
        sys.stdout.write('\n')
        return 0

    request_text = sys.stdin.read()
    m = load_base()
    old_stdin, old_stdout = sys.stdin, sys.stdout
    capture = io.StringIO()
    try:
        sys.stdin = io.StringIO(request_text)
        sys.stdout = capture
        rc = int(m.main())
    finally:
        sys.stdin, sys.stdout = old_stdin, old_stdout
    if rc != 0:
        return rc
    out = json.loads(capture.getvalue())
    ident = out.get('candidate_identity') or {}
    ident['commit'] = FROZEN_COMMIT
    ident['artifact_digest'] = FROZEN_DIGEST
    ident['manifest_path'] = MANIFEST_PATH
    ident['core'] = 'sales-lead-conversion/0.5.0'
    out['candidate_identity'] = ident
    runtime = out.get('runtime_identity') or {}
    runtime['executor'] = EXECUTOR_ID
    out['runtime_identity'] = runtime
    json.dump(out, sys.stdout, ensure_ascii=False)
    sys.stdout.write('\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
