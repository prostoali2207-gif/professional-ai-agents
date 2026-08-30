#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request
from typing import Any

ROOT = Path.cwd()
BASE = ROOT / 'architect/evaluation/sales-lead-conversion/author_sealed_pack_v0_3_r2.py'
EXPECTED_BASE_BLOB = '929a19ed17993795ad2ba76933964c1a3c8a7663'
PREREG = ROOT / 'architect/evaluation/sales-lead-conversion/qualification-preregistration-v0_4-r2-gemini-groq.json'
OUT_ROOT = ROOT / 'architect/evaluation/sales-lead-conversion/sealed/runtime-sales-0.4-r2-author'
CYCLE = 'sales-0.4-fresh-independent-2026-08-30-r2-gemini-groq'
COMMIT = 'd00bb8057ba0eaae24b918e13941fb61b0b8616d'
DIGEST = 'sha256:ce111538b204c4c694404a4b4ff13010c3909cc6918a9241600c818462fb62f0'
AUTHOR_MODEL = 'gemini-3.5-flash-lite'
AUDIT_MODEL = 'openai/gpt-oss-120b'
GEMINI_ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/interactions'
GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'
GEMINI_INTERVAL = 6.0
GROQ_INTERVAL = 60.0
AUDIT_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {'accept': {'type': 'boolean'}},
    'required': ['accept'],
}


def parse_json_text(text: str) -> Any:
    value = text.strip()
    if value.startswith('```'):
        lines = value.splitlines()
        value = '\n'.join(lines[1:-1]).strip()
        if value.startswith('json\n'):
            value = value[5:]
    return json.loads(value)


def gemini_text(payload: dict[str, Any]) -> str:
    if isinstance(payload.get('output_text'), str):
        return payload['output_text']
    for step in reversed(payload.get('steps') or []):
        if not isinstance(step, dict) or step.get('type') != 'model_output':
            continue
        content = step.get('content')
        if isinstance(content, str):
            return content
        for item in content or []:
            if isinstance(item, dict) and isinstance(item.get('text'), str):
                return item['text']
    raise RuntimeError('Gemini held-out author returned no output text')


def pace(marker_name: str, interval: float) -> None:
    marker = Path('/tmp') / marker_name
    if marker.exists():
        try:
            delay = interval - (time.time() - float(marker.read_text().strip()))
        except Exception:
            delay = 0.0
        if delay > 0:
            time.sleep(delay)
    marker.write_text(str(time.time()))


def urlopen_json(req: urllib.request.Request, *, timeout: int, label: str, retry_wait: float) -> dict[str, Any]:
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode('utf-8', 'replace')[-1200:]
            if exc.code == 429 and attempt == 0:
                retry_after = exc.headers.get('Retry-After') if exc.headers else None
                try:
                    delay = max(float(retry_after), retry_wait) if retry_after else retry_wait
                except Exception:
                    delay = retry_wait
                time.sleep(delay)
                continue
            raise RuntimeError(f'{label} HTTP {exc.code}: {detail}') from None
    raise RuntimeError(f'{label} retry budget exhausted')


def gemini_author_call(developer: str, user: str) -> dict[str, Any]:
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GEMINI_API_KEY missing before held-out authoring')
    pace('sales-v04-r2-gemini-author-pace', GEMINI_INTERVAL)
    body = {
        'model': AUTHOR_MODEL,
        'system_instruction': developer,
        'input': user,
        'store': False,
        'generation_config': {'thinking_level': 'medium'},
    }
    req = urllib.request.Request(
        GEMINI_ENDPOINT,
        data=json.dumps(body, ensure_ascii=False).encode('utf-8'),
        method='POST',
        headers={'x-goog-api-key': key, 'Content-Type': 'application/json'},
    )
    payload = urlopen_json(req, timeout=240, label='held-out Gemini author', retry_wait=15.0)
    return {'output_text': gemini_text(payload)}


def audit_group(group: list[str], cases: list[dict[str, Any]], prereg: dict[str, Any], slots: dict[str, list[str]]) -> None:
    key = os.environ.get('GROQ_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GROQ_API_KEY missing before held-out construct audit')
    if len(cases) != 3 * len(group):
        raise RuntimeError('authored group cardinality invalid before audit')
    payload = {
        'role': 'independent held-out construct auditor',
        'candidate_seen': False,
        'candidate_outputs_seen': False,
        'families': {family: prereg['construct']['families'][family] for family in group},
        'professional_invariants': prereg['construct']['professional_invariants'],
        'fixture_requirements': prereg['fixture_design']['requirements'],
        'requested_slots': {family: slots[family] for family in group},
        'allowed_critical_hard_fails': prereg['critical_hard_fail_policy'],
        'authored_cases': cases,
        'audit_task': (
            'Return accept=true only if all authored hidden cases are fresh, self-contained, realistic Sales/Lead-Conversion work samples; '
            'each family has exactly the requested three slots; candidate-visible fields do not leak expected answers; hidden references are grounded in supplied case facts and contain exactly three observable rubric dimensions; '
            'authority, identity, commercial-fact, state, mixed-workstream and operational-verification semantics follow the public construct; '
            'negative controls genuinely authorize action where required; critical hard-fail triggers are used only when the case facts unambiguously support them; '
            'and no case appears copied from or dependent on prior hidden Sales fixtures. Do not assess or predict the frozen candidate. '
            'If any condition fails, return accept=false. Return no rationale or hidden content.'
        ),
    }
    body = {
        'model': AUDIT_MODEL,
        'messages': [{'role': 'user', 'content': json.dumps(payload, ensure_ascii=False)}],
        'response_format': {'type': 'json_schema', 'json_schema': {'name': 'sales_r2_construct_audit', 'strict': True, 'schema': AUDIT_SCHEMA}},
        'include_reasoning': False,
        'reasoning_effort': 'medium',
        'temperature': 0,
    }
    pace('sales-v04-r2-groq-audit-pace', GROQ_INTERVAL)
    req = urllib.request.Request(
        GROQ_ENDPOINT,
        data=json.dumps(body, ensure_ascii=False).encode('utf-8'),
        method='POST',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'sales-v04-r2-heldout-audit/0.1'},
    )
    raw = urlopen_json(req, timeout=240, label='held-out Groq construct audit', retry_wait=60.0)
    result = parse_json_text(raw['choices'][0]['message']['content'])
    if result.get('accept') is not True:
        print(json.dumps({'status': 'NOT_EXECUTABLE_CONSTRUCT_AUDIT_REJECTED', 'group': group, 'candidate_calls': 0, 'hidden_content_printed': False}, sort_keys=True))
        raise SystemExit(20)


def main() -> int:
    actual = subprocess.check_output(['git', 'hash-object', str(BASE)], text=True).strip()
    if actual != EXPECTED_BASE_BLOB:
        raise RuntimeError(f'held-out author base drift: {actual}')
    if not os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY', '').strip():
        raise RuntimeError('QUALIFICATION_SEALED_PACK_MASTER_KEY missing before authoring')
    if not os.environ.get('GEMINI_API_KEY', '').strip():
        raise RuntimeError('GEMINI_API_KEY missing before authoring')
    if not os.environ.get('GROQ_API_KEY', '').strip():
        raise RuntimeError('GROQ_API_KEY missing before construct audit')

    prereg = json.loads(PREREG.read_text())
    if prereg.get('cycle_id') != CYCLE:
        raise RuntimeError('r2 preregistration cycle mismatch')
    if prereg.get('frozen_candidate', {}).get('commit') != COMMIT or prereg.get('frozen_candidate', {}).get('artifact_digest') != DIGEST:
        raise RuntimeError('r2 frozen candidate binding mismatch')
    route = prereg.get('heldout_authoring', {})
    if route.get('author_provider') != 'gemini-interactions-api' or route.get('author_model') != AUTHOR_MODEL:
        raise RuntimeError('r2 author route mismatch')
    if route.get('construct_audit_model') != AUDIT_MODEL:
        raise RuntimeError('r2 construct-audit route mismatch')

    spec = importlib.util.spec_from_file_location('sales_v04_r2_author_base', BASE)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load pinned held-out author base')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.PREREG = PREREG
    m.OUT_ROOT = OUT_ROOT
    m.PARTS = OUT_ROOT / 'parts'
    m.MANIFEST = OUT_ROOT / 'qualification.json'
    m.CYCLE = CYCLE
    m.COMMIT = COMMIT
    m.DIGEST = DIGEST
    m.MODEL = AUTHOR_MODEL
    m.responses_call = gemini_author_call

    original_author_group = m.author_group
    prereg_obj = prereg

    def audited_author_group(group: list[str], prereg_text: str) -> list[dict[str, Any]]:
        cases = original_author_group(group, prereg_text)
        audit_group(group, cases, prereg_obj, m.SLOTS)
        return cases

    m.author_group = audited_author_group

    # The pinned base checks OPENAI_API_KEY only because its original responses_call used OpenAI.
    # In r2 responses_call is replaced above; this process-local sentinel cannot authorize any network call.
    original_openai = os.environ.get('OPENAI_API_KEY')
    os.environ['OPENAI_API_KEY'] = 'r2-gemini-author-adapter-not-a-credential'
    try:
        rc = int(m.main())
    finally:
        if original_openai is None:
            os.environ.pop('OPENAI_API_KEY', None)
        else:
            os.environ['OPENAI_API_KEY'] = original_openai

    if rc != 0:
        return rc
    manifest = json.loads((OUT_ROOT / 'qualification.json').read_text())
    manifest['candidate']['manifest_path'] = 'architect/library/cores/sales-lead-conversion/0.4.0/manifest.json'
    manifest['runtime']['provider'] = 'gemini-interactions-api'
    manifest['runtime']['model'] = AUTHOR_MODEL
    manifest['runtime']['credential_env'] = 'GEMINI_API_KEY'
    (OUT_ROOT / 'qualification.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
