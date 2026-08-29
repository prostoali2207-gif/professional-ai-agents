#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess

BASE = Path('architect/evaluation/sales-lead-conversion/author_sealed_pack_v0_3_r2.py')
EXPECTED_BASE_BLOB = '929a19ed17993795ad2ba76933964c1a3c8a7663'
CYCLE = 'sales-0.4-fresh-independent-2026-08-29-r1-author'
COMMIT = 'd00bb8057ba0eaae24b918e13941fb61b0b8616d'
DIGEST = 'sha256:ce111538b204c4c694404a4b4ff13010c3909cc6918a9241600c818462fb62f0'
PREREG = Path('architect/evaluation/sales-lead-conversion/qualification-preregistration-v0_4-r1-gemini.json')
OUT_ROOT = Path('architect/evaluation/sales-lead-conversion/sealed/runtime-sales-0.4-r1-author')


def main() -> int:
    actual = subprocess.check_output(['git', 'hash-object', str(BASE)], text=True).strip()
    if actual != EXPECTED_BASE_BLOB:
        raise RuntimeError(f'held-out author base drift: {actual}')
    spec = importlib.util.spec_from_file_location('sales_v04_author_base', BASE)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load pinned held-out author')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.PREREG = PREREG
    m.OUT_ROOT = OUT_ROOT
    m.PARTS = OUT_ROOT / 'parts'
    m.MANIFEST = OUT_ROOT / 'qualification.json'
    m.CYCLE = CYCLE
    m.COMMIT = COMMIT
    m.DIGEST = DIGEST
    return int(m.main())


if __name__ == '__main__':
    raise SystemExit(main())
