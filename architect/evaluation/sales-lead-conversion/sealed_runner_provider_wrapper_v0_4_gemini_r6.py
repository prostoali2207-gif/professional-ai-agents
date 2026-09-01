#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess

CYCLE_ID = 'sales-0.4-fresh-independent-2026-08-30-r6-gemini-groq'
BASE = Path('architect/evaluation/sales-lead-conversion/sealed_runner_provider_wrapper_v0_3_gemini_r8.py')
EXPECTED_BASE_BLOB = '9bfdd0da131e67aa264e17cfa8e4cd45b34f6d4b'
CANDIDATE_COMMIT = 'd00bb8057ba0eaae24b918e13941fb61b0b8616d'
CANDIDATE_DIGEST = 'sha256:ce111538b204c4c694404a4b4ff13010c3909cc6918a9241600c818462fb62f0'


def main() -> int:
    actual = subprocess.check_output(['git', 'hash-object', str(BASE)], text=True).strip()
    if actual != EXPECTED_BASE_BLOB:
        raise RuntimeError(f'paced Gemini wrapper drift: {actual}')
    spec = importlib.util.spec_from_file_location('sales_v04_r6_paced_base', BASE)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load pinned paced Gemini wrapper')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.CYCLE_ID = CYCLE_ID
    original_load_provider = m.load_provider

    def load_provider_v04():
        provider = original_load_provider()
        original_load_base = provider.load_base

        def load_base_v04():
            runner = original_load_base()
            runner.CANDIDATE_COMMIT = CANDIDATE_COMMIT
            runner.CANDIDATE_DIGEST = CANDIDATE_DIGEST
            return runner

        provider.load_base = load_base_v04
        return provider

    m.load_provider = load_provider_v04
    m.__file__ = str(Path(__file__).resolve())
    return int(m.main())


if __name__ == '__main__':
    raise SystemExit(main())
