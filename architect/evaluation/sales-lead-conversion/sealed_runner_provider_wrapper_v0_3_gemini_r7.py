#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path
import subprocess

CYCLE_ID='sales-0.3-fresh-independent-2026-08-23-r7-gemini'
BASE=Path('architect/evaluation/sales-lead-conversion/sealed_runner_provider_wrapper_v0_3_gemini_r6.py')
EXPECTED='33014b8df9c10113a74df7c88fdbccf1c0edd2cf'

def main():
    actual=subprocess.check_output(['git','hash-object',str(BASE)],text=True).strip()
    if actual!=EXPECTED: raise RuntimeError(f'r6 wrapper drift: {actual}')
    spec=importlib.util.spec_from_file_location('sales_gemini_r7_base',BASE)
    if spec is None or spec.loader is None: raise RuntimeError('cannot load r6 wrapper')
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.CYCLE_ID=CYCLE_ID
    m.__file__=str(Path(__file__).resolve())
    return int(m.main())

if __name__=='__main__': raise SystemExit(main())
