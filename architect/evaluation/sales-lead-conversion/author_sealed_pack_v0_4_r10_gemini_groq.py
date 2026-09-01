#!/usr/bin/env python3
from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess

ROOT = Path.cwd()
R9_AUTHOR = ROOT / 'architect/evaluation/sales-lead-conversion/author_sealed_pack_v0_4_r9_gemini_groq.py'
R9_AUTHOR_BLOB = '5e5193039528da68930d9356396e629874eca29b'
PREREG = ROOT / 'architect/evaluation/sales-lead-conversion/qualification-preregistration-v0_4-r10-gemini-groq.json'
OUT_ROOT = ROOT / 'architect/evaluation/sales-lead-conversion/sealed/runtime-sales-0.4-r10-author'
CYCLE = 'sales-0.4-fresh-independent-2026-08-30-r10-gemini-groq'
COMMIT = 'd00bb8057ba0eaae24b918e13941fb61b0b8616d'
DIGEST = 'sha256:ce111538b204c4c694404a4b4ff13010c3909cc6918a9241600c818462fb62f0'


def load_r9():
    actual = subprocess.check_output(['git', 'hash-object', str(R9_AUTHOR)], text=True).strip()
    if actual != R9_AUTHOR_BLOB:
        raise RuntimeError(f'r9 author drift: {actual}')
    spec = importlib.util.spec_from_file_location('sales_v04_r10_r9', R9_AUTHOR)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load pinned r9 author')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    current = json.loads(PREREG.read_text())
    if current.get('cycle_id') != CYCLE:
        raise RuntimeError('r10 cycle mismatch')
    frozen = current.get('frozen_candidate', {})
    if frozen.get('commit') != COMMIT or frozen.get('artifact_digest') != DIGEST:
        raise RuntimeError('r10 frozen candidate mismatch')
    prior = current.get('prior_cycle_evidence', {})
    if prior.get('r9_run_id') != 33301068662 or prior.get('candidate_calls') != 0:
        raise RuntimeError('r10 prior-cycle binding mismatch')
    inheritance = current.get('construct_inheritance', {})
    if inheritance.get('authoring_implementation_blob') != R9_AUTHOR_BLOB:
        raise RuntimeError('r10 author implementation binding mismatch')

    r9 = load_r9()
    r9.PREREG = PREREG
    r9.OUT_ROOT = OUT_ROOT
    r9.CYCLE = CYCLE

    captured = io.StringIO()
    with redirect_stdout(captured):
        rc = int(r9.main())
    for line in captured.getvalue().splitlines():
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                status = obj.get('status')
                if isinstance(status, str):
                    obj['status'] = status.replace('R9', 'R10').replace('r9', 'r10')
                if obj.get('cycle_id') == 'sales-0.4-fresh-independent-2026-08-30-r9-gemini-groq':
                    obj['cycle_id'] = CYCLE
            print(json.dumps(obj, sort_keys=True))
        except Exception:
            print(line)
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
