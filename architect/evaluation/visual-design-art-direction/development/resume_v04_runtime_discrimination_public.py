#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Callable

ROOT = Path.cwd()
BASE_PATH = ROOT / 'architect/evaluation/visual-design-art-direction/development/run_v04_runtime_discrimination_public.py'
spec = importlib.util.spec_from_file_location('visual_v04_public_probe_base', BASE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError('cannot load original v0.4 public probe runner')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

SOURCE_RUN = 33598852893
SOURCE_ARTIFACT_ID = 9834506275
SOURCE_ARTIFACT_NAME = 'visual-design-art-direction-v04-runtime-probe-details'
SOURCE_ARTIFACT_DIGEST = 'sha256:bd5f54a87b61f27db5cc6b1c80c23a678ebf67ff760b57fb3d5acbf391dc72bd'
CHECKPOINT_SHA256 = '6646e460ca76cade85985f9eaec6bb5664d0c4c670d6815fd72c496a35c1dee8'
CHECKPOINT = Path(os.environ.get('V04_CHECKPOINT_DETAILS', 'source-checkpoint/visual-v04-runtime-discrimination-public-details.json'))
COMPLETED = (
    'R30_MOBILE_PRECOMMIT_CONTROL',
    'R31_TRUTH_PROOF_OUTPUT_CONTROL',
    'R32_REFERENCE_INDEPENDENCE_CONTROL',
    'R33_AUTHORITY_PRECOMMIT_CONTROL',
)
REMAINING = (
    'R34_WARNING_ONLY_COMPLIANCE_TRAP',
    'R39_BOLD_REFERENCE_ADVANCED_MEDIA_NONREGRESSION',
)
REPORT = Path('visual-v04-runtime-discrimination-resume-report.json')
DETAILS = Path('visual-v04-runtime-discrimination-resume-details.json')
PROGRESS = Path('visual-v04-runtime-discrimination-resume-progress.json')


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_fixtures() -> dict[str, dict[str, Any]]:
    data = json.load(open(base.FIXTURES))
    boundary = data.get('source_boundary') or {}
    if boundary.get('r4_hidden_content_used') is not False or boundary.get('sanitized_failure_classes_only') is not True or boundary.get('release_use') != 'DEVELOPMENT_ONLY':
        raise RuntimeError('public fixture source boundary mismatch')
    return {x['id']: x for x in data['families']}


def checkpoint_rows(fixtures: dict[str, dict[str, Any]]) -> tuple[list[dict], list[dict]]:
    if not CHECKPOINT.exists():
        raise RuntimeError('canonical public checkpoint missing')
    if sha256(CHECKPOINT) != CHECKPOINT_SHA256:
        raise RuntimeError('canonical public checkpoint SHA256 mismatch')
    payload = json.load(open(CHECKPOINT))
    if payload.get('development_only') is not True or payload.get('hidden_release_material_used') is not False:
        raise RuntimeError('checkpoint source boundary mismatch')
    cases = payload.get('cases')
    if not isinstance(cases, list) or [x.get('fixture_id') for x in cases] != list(COMPLETED):
        raise RuntimeError('checkpoint completed-fixture identity mismatch')

    rows: list[dict] = []
    details: list[dict] = []
    for case in cases:
        fid = case['fixture_id']
        fixture = fixtures[fid]
        for field in ('prompt', 'must_observe', 'must_not_observe'):
            if case.get(field) != fixture.get(field):
                raise RuntimeError(f'checkpoint public fixture content mismatch: {fid}:{field}')
        judgments = case.get('judgments') or {}
        gj = judgments.get('gemini')
        qj = judgments.get('groq')
        if not isinstance(gj, dict) or not isinstance(qj, dict):
            raise RuntimeError(f'checkpoint judgment missing: {fid}')
        if not base.valid_judgment(gj) or not base.valid_judgment(qj):
            raise RuntimeError(f'checkpoint judgment contract invalid: {fid}')
        if not (gj['pass'] and qj['pass']):
            raise RuntimeError(f'checkpoint contains non-PASS completed fixture: {fid}')
        text = case.get('candidate_output')
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError(f'checkpoint candidate output missing: {fid}')
        rows.append({
            'fixture_id': fid,
            'criticality': fixture['criticality'],
            'gemini': gj,
            'groq': qj,
            'pass': True,
            'judge_disagreement': False,
            'source': 'canonical_checkpoint',
        })
        details.append(case)
    return rows, details


def retry_delay_from_error(text: str) -> float:
    m = re.search(r'Please retry in\s+([0-9]+(?:\.[0-9]+)?)s', text, flags=re.I)
    if m:
        return max(1.0, min(float(m.group(1)) + 1.0, 90.0))
    m = re.search(r'Retry-After[^0-9]*([0-9]+(?:\.[0-9]+)?)', text, flags=re.I)
    if m:
        return max(1.0, min(float(m.group(1)) + 1.0, 90.0))
    return 35.0


def call_with_one_429_retry(fn: Callable[[], Any], label: str) -> Any:
    for attempt in range(2):
        try:
            return fn()
        except RuntimeError as exc:
            message = str(exc)
            if '429' not in message or attempt == 1:
                raise
            # Provider returned no usable model output. Preregistered transport-only
            # continuation permits one exact-call retry after honoring quota guidance.
            time.sleep(retry_delay_from_error(message))
    raise RuntimeError(f'{label} 429 retry budget exhausted')


def write_progress(status: str, continuation_candidate_calls: int, continuation_judge_calls: dict[str, int], *, failure: str | None = None) -> None:
    PROGRESS.write_text(json.dumps({
        'status': status,
        'development_only': True,
        'hidden_release_material_used': False,
        'source_run': SOURCE_RUN,
        'checkpoint_completed_fixtures': list(COMPLETED),
        'remaining_fixtures': list(REMAINING),
        'checkpoint_candidate_calls': 4,
        'checkpoint_judge_calls': {'gemini': 4, 'groq': 4},
        'continuation_candidate_calls': continuation_candidate_calls,
        'continuation_judge_calls': continuation_judge_calls,
        'failure': failure,
    }, indent=2, sort_keys=True) + '\n')


def main() -> int:
    fixtures = load_fixtures()
    if any(fid not in fixtures for fid in COMPLETED + REMAINING):
        raise RuntimeError('required public fixture missing')
    results, details = checkpoint_rows(fixtures)
    candidate_calls = 0
    judge_calls = {'gemini': 0, 'groq': 0}
    write_progress('IN_PROGRESS', candidate_calls, judge_calls)

    try:
        for fixture_id in REMAINING:
            fixture = fixtures[fixture_id]
            candidate = call_with_one_429_retry(lambda: base.candidate_call(fixture), f'{fixture_id}:candidate')
            candidate_calls += 1
            write_progress('IN_PROGRESS', candidate_calls, judge_calls)

            gj = call_with_one_429_retry(lambda: base.judge_gemini(fixture, candidate['text']), f'{fixture_id}:gemini-judge')
            judge_calls['gemini'] += 1
            if not base.valid_judgment(gj):
                raise RuntimeError(f'Gemini invalid judgment contract on {fixture_id}')
            write_progress('IN_PROGRESS', candidate_calls, judge_calls)

            qj = call_with_one_429_retry(lambda: base.judge_groq(fixture, candidate['text']), f'{fixture_id}:groq-judge')
            judge_calls['groq'] += 1
            if not base.valid_judgment(qj):
                raise RuntimeError(f'Groq invalid judgment contract on {fixture_id}')
            write_progress('IN_PROGRESS', candidate_calls, judge_calls)

            results.append({
                'fixture_id': fixture_id,
                'criticality': fixture['criticality'],
                'gemini': gj,
                'groq': qj,
                'pass': bool(gj['pass'] and qj['pass']),
                'judge_disagreement': gj['pass'] != qj['pass'],
                'source': 'continuation',
            })
            details.append({
                'fixture_id': fixture_id,
                'prompt': fixture['prompt'],
                'must_observe': fixture['must_observe'],
                'must_not_observe': fixture['must_not_observe'],
                'candidate_output': candidate['text'],
                'judgments': {'gemini': gj, 'groq': qj},
            })

        if [x['fixture_id'] for x in results] != list(COMPLETED + REMAINING):
            raise RuntimeError('combined six-fixture ordering/coverage mismatch')
        passed = len(results) == 6 and all(r['pass'] for r in results)
        status = 'PUBLIC_RUNTIME_PROBE_PASS' if passed else 'PUBLIC_RUNTIME_PROBE_FAIL'
        report = {
            'status': status,
            'development_only': True,
            'release_evidence': False,
            'hidden_release_material_used': False,
            'continuation_of_run': SOURCE_RUN,
            'checkpoint': {
                'artifact_id': SOURCE_ARTIFACT_ID,
                'artifact_name': SOURCE_ARTIFACT_NAME,
                'artifact_digest': SOURCE_ARTIFACT_DIGEST,
                'extracted_json_sha256': CHECKPOINT_SHA256,
                'completed_fixture_ids': list(COMPLETED),
            },
            'candidate': {
                'professional_components': 'exact frozen v0.3',
                'runtime_model': 'gemini-3.7-flash',
                'thinking_level': 'medium',
            },
            'fixture_ids': list(COMPLETED + REMAINING),
            'candidate_calls': 6,
            'candidate_calls_reused_from_checkpoint': 4,
            'candidate_calls_new_in_continuation': candidate_calls,
            'judge_models': {'gemini': base.GEMINI_MODEL, 'groq': base.GROQ_MODEL},
            'judge_calls': {'gemini': 6, 'groq': 6},
            'judge_calls_reused_from_checkpoint': {'gemini': 4, 'groq': 4},
            'judge_calls_new_in_continuation': judge_calls,
            'fixture_outcomes': results,
            'all_fixtures_pass_both_judges': passed,
            'next_step': 'freeze runtime-only v0.4 candidate' if passed else 'test staged structural execution controller; do not freeze runtime-only v0.4',
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
        DETAILS.write_text(json.dumps({
            'development_only': True,
            'hidden_release_material_used': False,
            'continuation_of_run': SOURCE_RUN,
            'cases': details,
        }, indent=2, sort_keys=True) + '\n')
        write_progress(status, candidate_calls, judge_calls)
        print(json.dumps({
            'status': status,
            'checkpoint_fixtures': 4,
            'continuation_candidate_calls': candidate_calls,
            'continuation_judge_calls': judge_calls,
            'passed_fixtures': sum(1 for r in results if r['pass']),
            'fixture_count': len(results),
        }, sort_keys=True))
        return 0 if passed else 20
    except Exception as exc:
        DETAILS.write_text(json.dumps({
            'development_only': True,
            'hidden_release_material_used': False,
            'continuation_of_run': SOURCE_RUN,
            'cases': details,
            'failure': str(exc)[:800],
        }, indent=2, sort_keys=True) + '\n')
        write_progress('INFRASTRUCTURE_FAILURE', candidate_calls, judge_calls, failure=str(exc)[:600])
        print(json.dumps({
            'status': 'INFRASTRUCTURE_FAILURE',
            'checkpoint_fixtures': 4,
            'continuation_candidate_calls': candidate_calls,
            'continuation_judge_calls': judge_calls,
            'error': str(exc)[:600],
        }, sort_keys=True))
        return 30


if __name__ == '__main__':
    raise SystemExit(main())
