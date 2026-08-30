#!/usr/bin/env python3
from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess

ROOT = Path.cwd()
R4_PATH = ROOT / 'architect/evaluation/sales-lead-conversion/author_sealed_pack_v0_5_r4_gemini_groq.py'
R4_BLOB = '014a4baad3aa7777e70b2a34eb49fc8d85e2aa44'
ASSEMBLER_PATH = ROOT / 'architect/evaluation/sales-lead-conversion/effective_prereg_v0_5_r5.py'
ASSEMBLER_BLOB = '99bda7ddaad179534339ef75cc5b7439d207f0cd'
DELTA = ROOT / 'architect/evaluation/sales-lead-conversion/qualification-preregistration-v0_5-r5-gemini-groq.json'
DELTA_BLOB = 'bd130a6b080fee6bd78ad2347d6494a0efd4f175'
CYCLE = 'sales-0.5-fresh-independent-2026-08-30-r5-gemini-groq'
OUT_ROOT = ROOT / 'architect/evaluation/sales-lead-conversion/sealed/runtime-sales-0.5-r5-author'
COMMIT = '2b8a397d16f2b0e8d7ad93c341f0031ec7dce4df'
DIGEST = 'sha256:0e7b46f186269968df12d09f64d48c88e173196a8b59f69a4e1ba1a049f4f1d9'


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


def main() -> int:
    actual_delta = subprocess.check_output(['git', 'hash-object', str(DELTA)], text=True).strip()
    if actual_delta != DELTA_BLOB:
        raise RuntimeError(f'r5 prereg drift: {actual_delta}')
    delta = json.loads(DELTA.read_text())
    if delta.get('cycle_id') != CYCLE:
        raise RuntimeError('sales 0.5 r5 cycle mismatch')
    frozen = delta.get('frozen_candidate', {})
    if frozen.get('commit') != COMMIT or frozen.get('artifact_digest') != DIGEST:
        raise RuntimeError('sales 0.5 r5 frozen candidate mismatch')
    r4_evidence = delta.get('prior_sanitized_evidence', {}).get('r4', {})
    if r4_evidence.get('run_id') != 33315346775 or r4_evidence.get('pack_reuse_for_scoring_allowed') is not False:
        raise RuntimeError('sales 0.5 r5 r4 evidence mismatch')
    if r4_evidence.get('checkpoint_available') is not False or r4_evidence.get('sanitized_report_written') is not False:
        raise RuntimeError('sales 0.5 r5 r4 non-resumable evidence mismatch')
    split = delta.get('execution_split_remediation', {})
    if split.get('fresh_r5_pack_required') is not True or split.get('r4_pack_reuse_allowed') is not False:
        raise RuntimeError('sales 0.5 r5 fresh-pack contract invalid')
    for key in (
        'candidate_change_allowed', 'grader_change_allowed', 'threshold_change_allowed',
        'hard_fail_change_allowed', 'candidate_provider_change_allowed',
        'candidate_model_change_allowed', 'professional_retry_change_allowed',
    ):
        if split.get(key) is not False:
            raise RuntimeError(f'sales 0.5 r5 forbidden mutation: {key}')

    r4 = load_module(R4_PATH, R4_BLOB, 'sales_v05_r5_r4_transport')
    load_module(ASSEMBLER_PATH, ASSEMBLER_BLOB, 'sales_v05_r5_prereg_probe')
    r4.ASSEMBLER_PATH = ASSEMBLER_PATH
    r4.ASSEMBLER_BLOB = ASSEMBLER_BLOB
    r4.DELTA = DELTA
    r4.DELTA_BLOB = DELTA_BLOB
    r4.OUT_ROOT = OUT_ROOT
    r4.CYCLE = CYCLE
    r4.COMMIT = COMMIT
    r4.DIGEST = DIGEST

    captured = io.StringIO()
    with redirect_stdout(captured):
        rc = int(r4.main())
    for line in captured.getvalue().splitlines():
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                status = obj.get('status')
                if isinstance(status, str):
                    obj['status'] = status.replace('V05_R4', 'V05_R5').replace('_R4', '_R5').replace('r4', 'r5')
                obj['cycle_id'] = CYCLE
            print(json.dumps(obj, sort_keys=True))
        except Exception:
            print(line)
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
