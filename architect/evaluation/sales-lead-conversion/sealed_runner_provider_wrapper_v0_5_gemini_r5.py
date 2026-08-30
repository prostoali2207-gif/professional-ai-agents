#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess

CYCLE_ID = 'sales-0.5-fresh-independent-2026-08-30-r5-gemini-groq'
BASE = Path('architect/evaluation/sales-lead-conversion/sealed_runner_provider_wrapper_v0_3_gemini_r8.py')
EXPECTED_BASE_BLOB = '9bfdd0da131e67aa264e17cfa8e4cd45b34f6d4b'
CANDIDATE_COMMIT = '2b8a397d16f2b0e8d7ad93c341f0031ec7dce4df'
CANDIDATE_DIGEST = 'sha256:0e7b46f186269968df12d09f64d48c88e173196a8b59f69a4e1ba1a049f4f1d9'


def main() -> int:
    actual = subprocess.check_output(['git', 'hash-object', str(BASE)], text=True).strip()
    if actual != EXPECTED_BASE_BLOB:
        raise RuntimeError(f'paced Gemini wrapper drift: {actual}')
    spec = importlib.util.spec_from_file_location('sales_v05_r5_paced_base', BASE)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load pinned paced Gemini wrapper')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.CYCLE_ID = CYCLE_ID
    original_load_provider = m.load_provider

    def load_provider_v05_r5():
        provider = original_load_provider()
        original_load_base = provider.load_base

        def load_base_v05_r5():
            runner = original_load_base()
            runner.CANDIDATE_COMMIT = CANDIDATE_COMMIT
            runner.CANDIDATE_DIGEST = CANDIDATE_DIGEST
            return runner

        provider.load_base = load_base_v05_r5
        return provider

    m.load_provider = load_provider_v05_r5
    m.__file__ = str(Path(__file__).resolve())
    return int(m.main())


if __name__ == '__main__':
    raise SystemExit(main())
