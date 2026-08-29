#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from cryptography.fernet import Fernet

ROOT = Path.cwd()
PACK_DIR = Path(os.environ.get('R3_PACK_DIR', 'r3-source'))
CYCLE = 'visual-design-art-direction-0.1.0-independent-2026-08-29-r3-corpus-calibration'
SEMANTIC_CYCLE = 'visual-design-art-direction-0.1.0-independent-2026-08-29-r3-semantic'
CANDIDATE_COMMIT = 'e8be839b02f181193afe076839c6ae94fb477a9b'
SKILL_BLOB = '9d251d97a84e16ade91c8ced07425f9208f9f900'
MODEL_BLOB = 'bbea595e299445cf79f798ed1e86eecd0b53cd50'
SOURCE_RUN_ID = '33265201398'
SOURCE_HEAD_SHA = 'af43f2d12187e1825c596239a7313fd8b7e5da63'
SOURCE_ARTIFACT_ID = '9718569692'
SOURCE_ARTIFACT_NAME = 'visual-design-art-direction-v0-1-encrypted-heldout-pack-r3'
SOURCE_ARTIFACT_DIGEST = 'sha256:04edc998022ae2ec524cec2e366c2644e46964c052030c5faddec320c7e94f1b'
GEMINI_MODEL = 'gemini-3.5-flash-lite'
GROQ_MODEL = 'openai/gpt-oss-120b'
GEMINI = 'https://generativelanguage.googleapis.com/v1beta/interactions'
GROQ = os.environ.get('GROQ_BASE_URL', 'https://api.groq.com/openai/v1').rstrip('/') + '/chat/completions'
PER_JUDGE_MIN = 0.80
COMBINED_MIN = 0.90
MAX_DISAGREEMENT = 0.25
TRANSIENT_5XX_RETRIES = 1
TRANSIENT_RETRY_DELAY_SECONDS = 15
CHECKPOINT = Path('visual-r3-corpus-calibration-checkpoint.enc')
PROGRESS = Path('visual-r3-corpus-calibration-progress.json')
REPORT = Path('visual-r3-corpus-calibration-sanitized-report.json')
FAMILIES = [
    'FRAMING', 'REFERENCE', 'DIVERGENCE', 'CRAFT_JUDGMENT', 'MOBILE',
    'TRUTH', 'CONTRACT', 'CRITIQUE_REPAIR', 'ADVANCED_MEDIA_ROUTING',
    'AUTHORITY_BOUNDARY',
]
P0_CATEGORIES = {
    'FABRICATED_FACTUAL_PROOF',
    'UNOBSERVED_RENDER_SUCCESS_CLAIM',
    'REFERENCE_IMITATION_AS_SOLUTION',
    'KEYWORD_ONLY_ADVANCED_MEDIA_ROUTING',
    'SPECTACLE_BREAKS_HARD_FUNCTION_CONSTRAINT',
    'UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE',
    'ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE',
}
ANCHOR_SCHEMA = {
    'type': 'object', 'additionalProperties': False,
    'properties': {'anchor': {'type': 'string'}}, 'required': ['anchor'],
}
AUDIT_SCHEMA = {
    'type': 'object', 'additionalProperties': False,
    'properties': {'accept': {'type': 'boolean'}}, 'required': ['accept'],
}
JUDGE_SCHEMA = {
    'type': 'object', 'additionalProperties': False,
    'properties': {'winner': {'type': 'string', 'enum': ['A', 'B']}},
    'required': ['winner'],
}


def parse_json(text: str):
    text = text.strip()
    if text.startswith('```'):
        text = '\n'.join(text.splitlines()[1:-1]).strip()
    return json.loads(text)


def gemini_text(raw: dict) -> str:
    if isinstance(raw.get('output_text'), str):
        return raw['output_text']
    for step in reversed(raw.get('steps') or []):
        if isinstance(step, dict) and step.get('type') == 'model_output':
            content = step.get('content')
            if isinstance(content, str):
                return content
            for item in content or []:
                if isinstance(item, dict) and isinstance(item.get('text'), str):
                    return item['text']
    raise RuntimeError('Gemini returned no text')


def master_key() -> bytes:
    value = os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY', '').encode().strip()
    if not value:
        raise RuntimeError('QUALIFICATION_SEALED_PACK_MASTER_KEY missing')
    return value


def derive_key(cycle: str) -> bytes:
    sys.path.insert(0, str(ROOT / 'architect/evaluation/qualification-platform'))
    from sealed_pack_keys import derive_fernet_key
    return derive_fernet_key(master_key(), cycle)


def pace_groq() -> None:
    interval = float(os.environ.get('GROQ_MIN_INTERVAL_SECONDS', '60'))
    marker = Path(os.environ.get('GROQ_PACE_FILE', '/tmp/visual-r3-corpus-calibration-groq-pace'))
    if interval <= 0:
        return
    if marker.exists():
        try:
            delay = interval - (time.time() - float(marker.read_text().strip()))
        except Exception:
            delay = 0
        if delay > 0:
            time.sleep(delay)
    marker.write_text(str(time.time()))


def http(req: urllib.request.Request, provider: str, timeout: int, *, groq: bool = False):
    for attempt in range(TRANSIENT_5XX_RETRIES + 1):
        if groq:
            pace_groq()
        try:
            return urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode('utf-8', 'replace')[-1200:]
            if 500 <= exc.code < 600 and attempt < TRANSIENT_5XX_RETRIES:
                time.sleep(TRANSIENT_RETRY_DELAY_SECONDS)
                continue
            raise RuntimeError(f'{provider} HTTP {exc.code}: {detail}') from None


def load_pack() -> tuple[dict, dict]:
    manifest_path = PACK_DIR / 'heldout-r3.manifest.json'
    parts_path = PACK_DIR / 'heldout-r3.parts'
    manifest = json.load(open(manifest_path))
    assert manifest['cycle_id'] == SEMANTIC_CYCLE
    assert manifest['candidate_commit'] == CANDIDATE_COMMIT
    assert manifest['candidate_blobs'] == {'skill': SKILL_BLOB, 'professional_model': MODEL_BLOB}
    assert manifest['item_count'] == 20 and manifest['family_count'] == 10 and manifest['pair_count'] == 5
    assert manifest['candidate_calls'] == 0 and manifest['hidden_content_printed'] is False
    ciphertext = ''.join(p.read_text() for p in sorted(parts_path.iterdir())).encode()
    assert len(ciphertext) == manifest['ciphertext_length']
    assert hashlib.sha256(ciphertext).hexdigest() == manifest['ciphertext_sha256']
    plaintext = Fernet(derive_key(SEMANTIC_CYCLE)).decrypt(ciphertext)
    assert hashlib.sha256(plaintext).hexdigest() == manifest['plaintext_sha256']
    payload = json.loads(plaintext)
    assert payload['cycle_id'] == SEMANTIC_CYCLE
    assert payload['candidate_commit'] == CANDIDATE_COMMIT
    assert payload['candidate_blobs'] == {'skill': SKILL_BLOB, 'professional_model': MODEL_BLOB}
    cases = payload['cases']
    assert len(cases) == 20
    counts = {family: 0 for family in FAMILIES}
    ids = set()
    for case in cases:
        assert case['family'] in counts
        counts[case['family']] += 1
        assert case['id'] not in ids
        ids.add(case['id'])
        assert isinstance(case['brief'], str) and case['brief'].strip()
        assert isinstance(case['context'], str) and case['context'].strip()
        assert isinstance(case['constraints'], list) and case['constraints']
        assert isinstance(case['competent_generic_baseline'], str) and case['competent_generic_baseline'].strip()
        assert isinstance(case['professional_criteria'], list) and len(case['professional_criteria']) >= 3
        p0 = case.get('p0_guardrail')
        if p0 is not None:
            assert p0['category'] in P0_CATEGORIES and p0['trigger']
    assert all(value == 2 for value in counts.values())
    return manifest, payload


def empty_state() -> dict:
    return {
        'cycle_id': CYCLE,
        'source_run_id': SOURCE_RUN_ID,
        'source_head_sha': SOURCE_HEAD_SHA,
        'source_artifact_id': SOURCE_ARTIFACT_ID,
        'source_artifact_name': SOURCE_ARTIFACT_NAME,
        'source_artifact_digest': SOURCE_ARTIFACT_DIGEST,
        'cases': {},
        'calls': {'gemini_anchor': 0, 'groq_anchor_audit': 0, 'gemini_judge': 0, 'groq_judge': 0},
        'candidate_calls': 0,
    }


def checkpoint_key() -> bytes:
    return derive_key(CYCLE)


def load_state() -> dict:
    if not CHECKPOINT.exists():
        return empty_state()
    state = json.loads(Fernet(checkpoint_key()).decrypt(CHECKPOINT.read_bytes()))
    expected = empty_state()
    for key in ('cycle_id', 'source_run_id', 'source_head_sha', 'source_artifact_id', 'source_artifact_name', 'source_artifact_digest'):
        assert state[key] == expected[key]
    assert state['candidate_calls'] == 0
    return state


def save_state(state: dict, *, status: str = 'IN_PROGRESS', failure: dict | None = None) -> None:
    CHECKPOINT.write_bytes(Fernet(checkpoint_key()).encrypt(json.dumps(state, ensure_ascii=False, sort_keys=True).encode()))
    completed_audits = sum(1 for row in state['cases'].values() if row.get('anchor_audit') is True)
    completed_judgments = sum(len(row.get('judges', {})) for row in state['cases'].values())
    progress = {
        'cycle_id': CYCLE,
        'status': status,
        'source_run_id': SOURCE_RUN_ID,
        'source_head_sha': SOURCE_HEAD_SHA,
        'source_artifact_id': SOURCE_ARTIFACT_ID,
        'source_artifact_name': SOURCE_ARTIFACT_NAME,
        'source_artifact_digest': SOURCE_ARTIFACT_DIGEST,
        'completed_anchor_audits': completed_audits,
        'completed_judgments': completed_judgments,
        'provider_calls': state['calls'],
        'candidate_calls': 0,
        'failure': failure,
        'hidden_content_printed': False,
    }
    PROGRESS.write_text(json.dumps(progress, indent=2, sort_keys=True) + '\n')


def gemini_anchor(case: dict) -> str:
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GEMINI_API_KEY missing')
    hidden_reference = {
        'brief': case['brief'], 'context': case['context'], 'constraints': case['constraints'],
        'professional_criteria': case['professional_criteria'], 'p0_guardrail': case.get('p0_guardrail'),
    }
    task = {
        'task': 'Produce one senior-practitioner Visual Design / Art Direction response to this exact professional case for evaluator calibration. Solve the case directly; respect every supplied constraint; preserve factual truth and delegated authority; make causal visual judgments; and avoid every stated hard-fail. Do not discuss evaluation or expected winners.',
        'case': hidden_reference,
    }
    body = {
        'model': GEMINI_MODEL,
        'system_instruction': 'You are a senior landing-page visual designer and art director producing a practitioner reference response. Return only JSON matching the schema.',
        'input': json.dumps(task, ensure_ascii=False), 'store': False,
        'generation_config': {'thinking_level': 'medium'},
        'response_format': {'type': 'text', 'mime_type': 'application/json', 'schema': ANCHOR_SCHEMA},
    }
    req = urllib.request.Request(GEMINI, data=json.dumps(body, ensure_ascii=False).encode(), method='POST', headers={'x-goog-api-key': key, 'Content-Type': 'application/json'})
    with http(req, 'Gemini anchor', 240) as response:
        out = parse_json(gemini_text(json.loads(response.read().decode())))
    anchor = out.get('anchor')
    if not isinstance(anchor, str) or not anchor.strip():
        raise RuntimeError('Gemini anchor invalid')
    return anchor


def groq_anchor_audit(case: dict, anchor: str) -> bool:
    key = os.environ.get('GROQ_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GROQ_API_KEY missing')
    payload = {
        'role': 'You are an independent senior landing-page art director and evaluation scientist.',
        'task': 'Accept only if the practitioner anchor is professionally defensible for the exact supplied case, materially addresses the hidden professional criteria, respects constraints and authority, and contains no declared P0 hard-fail. Do not rewrite or improve the case, criteria, baseline or anchor. Return accept only.',
        'brief': case['brief'], 'context': case['context'], 'constraints': case['constraints'],
        'professional_criteria': case['professional_criteria'], 'p0_guardrail': case.get('p0_guardrail'),
        'anchor': anchor,
    }
    body = {
        'model': GROQ_MODEL,
        'messages': [{'role': 'user', 'content': json.dumps(payload, ensure_ascii=False)}],
        'response_format': {'type': 'json_schema', 'json_schema': {'name': 'r3_anchor_audit', 'strict': True, 'schema': AUDIT_SCHEMA}},
        'include_reasoning': False, 'reasoning_effort': 'medium', 'temperature': 0,
    }
    req = urllib.request.Request(GROQ, data=json.dumps(body, ensure_ascii=False).encode(), method='POST', headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'visual-r3-corpus-calibration-audit/0.1'})
    with http(req, 'Groq anchor audit', 180, groq=True) as response:
        raw = json.loads(response.read().decode())
    return bool(parse_json(raw['choices'][0]['message']['content'])['accept'])


def blind_order(case_id: str, anchor: str, baseline: str) -> tuple[str, str, str]:
    swap = int(hashlib.sha256(f'{CYCLE}:{case_id}'.encode()).hexdigest(), 16) % 2 == 1
    if swap:
        return baseline, anchor, 'B'
    return anchor, baseline, 'A'


def judge_payload(case: dict, a: str, b: str) -> dict:
    return {
        'role': 'You are a blind senior landing-page art-direction assessor.',
        'brief': case['brief'], 'context': case['context'], 'constraints': case['constraints'],
        'output_A': a, 'output_B': b,
        'task': 'Choose the professionally stronger Visual Design / Art Direction response for the supplied facts. Judge causal appropriateness, craft/function reasoning, mobile implications, reference independence, truth and authority discipline as relevant. Do not reward verbosity. Return only winner A or B.',
    }


def gemini_judge(case: dict, a: str, b: str) -> str:
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GEMINI_API_KEY missing')
    body = {
        'model': GEMINI_MODEL,
        'system_instruction': 'You are a blind senior art-direction assessor. Return JSON only as {"winner":"A"} or {"winner":"B"}.',
        'input': json.dumps(judge_payload(case, a, b), ensure_ascii=False), 'store': False,
        'generation_config': {'thinking_level': 'medium'},
    }
    req = urllib.request.Request(GEMINI, data=json.dumps(body, ensure_ascii=False).encode(), method='POST', headers={'x-goog-api-key': key, 'Content-Type': 'application/json'})
    with http(req, 'Gemini judge', 180) as response:
        result = parse_json(gemini_text(json.loads(response.read().decode())))
    winner = result.get('winner')
    if winner not in {'A', 'B'}:
        raise RuntimeError('Gemini judge invalid winner')
    return winner


def groq_judge(case: dict, a: str, b: str) -> str:
    key = os.environ.get('GROQ_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GROQ_API_KEY missing')
    body = {
        'model': GROQ_MODEL,
        'messages': [{'role': 'user', 'content': json.dumps(judge_payload(case, a, b), ensure_ascii=False)}],
        'response_format': {'type': 'json_schema', 'json_schema': {'name': 'r3_visual_judgment', 'strict': True, 'schema': JUDGE_SCHEMA}},
        'include_reasoning': False, 'reasoning_effort': 'medium', 'temperature': 0,
    }
    req = urllib.request.Request(GROQ, data=json.dumps(body, ensure_ascii=False).encode(), method='POST', headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'visual-r3-corpus-calibration-judge/0.1'})
    with http(req, 'Groq judge', 180, groq=True) as response:
        raw = json.loads(response.read().decode())
    winner = parse_json(raw['choices'][0]['message']['content']).get('winner')
    if winner not in {'A', 'B'}:
        raise RuntimeError('Groq judge invalid winner')
    return winner


def main() -> None:
    manifest, payload = load_pack()
    state = load_state()
    save_state(state)
    case_by_id = {case['id']: case for case in payload['cases']}
    try:
        for case in payload['cases']:
            cid = case['id']
            row = state['cases'].setdefault(cid, {'family': case['family'], 'judges': {}})
            if 'anchor' not in row:
                row['anchor'] = gemini_anchor(case)
                state['calls']['gemini_anchor'] += 1
                save_state(state)
            if 'anchor_audit' not in row:
                row['anchor_audit'] = groq_anchor_audit(case, row['anchor'])
                state['calls']['groq_anchor_audit'] += 1
                save_state(state)
            if row['anchor_audit'] is not True:
                failure = {'class': 'CALIBRATION_NOT_EXECUTABLE_ANCHOR_VALIDITY', 'case_id': cid, 'family': case['family']}
                save_state(state, status='CALIBRATION_NOT_EXECUTABLE_ANCHOR_VALIDITY', failure=failure)
                print(json.dumps({'status': failure['class'], 'candidate_calls': 0, 'failed_case_id': cid, 'family': case['family'], 'hidden_content_printed': False}, sort_keys=True))
                raise SystemExit(12)
            a, b, expected = blind_order(cid, row['anchor'], case['competent_generic_baseline'])
            row['expected'] = expected
            if 'gemini' not in row['judges']:
                win = gemini_judge(case, a, b)
                state['calls']['gemini_judge'] += 1
                row['judges']['gemini'] = {'winner': win, 'correct': win == expected}
                save_state(state)
            if 'groq' not in row['judges']:
                win = groq_judge(case, a, b)
                state['calls']['groq_judge'] += 1
                row['judges']['groq'] = {'winner': win, 'correct': win == expected}
                save_state(state)

        rows = [state['cases'][cid] for cid in case_by_id]
        n = len(rows)
        assert n == 20 and all(row.get('anchor_audit') is True and len(row.get('judges', {})) == 2 for row in rows)
        rates = {
            'gemini': sum(row['judges']['gemini']['correct'] for row in rows) / n,
            'groq': sum(row['judges']['groq']['correct'] for row in rows) / n,
        }
        combined = sum(row['judges'][provider]['correct'] for row in rows for provider in ('gemini', 'groq')) / (n * 2)
        disagreement = sum(row['judges']['gemini']['winner'] != row['judges']['groq']['winner'] for row in rows) / n
        passed = all(rate >= PER_JUDGE_MIN for rate in rates.values()) and combined >= COMBINED_MIN and disagreement <= MAX_DISAGREEMENT
        family_outcomes = {}
        for family in FAMILIES:
            subset = [row for row in rows if row['family'] == family]
            family_outcomes[family] = {
                'item_count': len(subset),
                'gemini_correct': sum(row['judges']['gemini']['correct'] for row in subset),
                'groq_correct': sum(row['judges']['groq']['correct'] for row in subset),
                'judge_disagreements': sum(row['judges']['gemini']['winner'] != row['judges']['groq']['winner'] for row in subset),
            }
        report = {
            'cycle_id': CYCLE,
            'status': 'CALIBRATION_PASS' if passed else 'CALIBRATION_FAIL',
            'source': {
                'run_id': SOURCE_RUN_ID, 'head_sha': SOURCE_HEAD_SHA, 'artifact_id': SOURCE_ARTIFACT_ID,
                'artifact_name': SOURCE_ARTIFACT_NAME, 'artifact_digest': SOURCE_ARTIFACT_DIGEST,
                'sealed_ciphertext_sha256': manifest['ciphertext_sha256'],
            },
            'candidate': {'commit': CANDIDATE_COMMIT, 'skill_blob': SKILL_BLOB, 'professional_model_blob': MODEL_BLOB},
            'candidate_calls': 0,
            'item_count': n,
            'family_count': 10,
            'judge_models': {'gemini': GEMINI_MODEL, 'groq': GROQ_MODEL},
            'per_judge_expected_winner_rate': rates,
            'combined_expected_winner_rate': combined,
            'pair_disagreement_rate': disagreement,
            'policy': {
                'per_judge_expected_winner_rate_min': PER_JUDGE_MIN,
                'combined_expected_winner_rate_min': COMBINED_MIN,
                'max_pair_disagreement_rate': MAX_DISAGREEMENT,
            },
            'provider_calls': state['calls'],
            'family_outcomes': family_outcomes,
            'hidden_content_printed': False,
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
        save_state(state, status=report['status'])
        print(json.dumps({'status': report['status'], 'candidate_calls': 0, 'item_count': n, 'combined_expected_winner_rate': combined, 'pair_disagreement_rate': disagreement, 'hidden_content_printed': False}, sort_keys=True))
        raise SystemExit(0 if passed else 10)
    except SystemExit:
        raise
    except Exception as exc:
        failure = {'class': 'INFRASTRUCTURE_FAILURE', 'error': str(exc)[:500]}
        save_state(state, status='INFRASTRUCTURE_FAILURE', failure=failure)
        print(json.dumps({'status': 'INFRASTRUCTURE_FAILURE', 'candidate_calls': 0, 'hidden_content_printed': False, 'error_class': type(exc).__name__}, sort_keys=True))
        raise


if __name__ == '__main__':
    main()
