#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from cryptography.fernet import Fernet

ROOT = Path.cwd()
BASE = ROOT / 'architect/evaluation/visual-design-art-direction/heldout'
CYCLE = 'visual-design-art-direction-0.1.0-independent-2026-08-29-r2-semantic'
CANDIDATE_COMMIT = 'e8be839b02f181193afe076839c6ae94fb477a9b'
SKILL_BLOB = '9d251d97a84e16ade91c8ced07425f9208f9f900'
MODEL_BLOB = 'bbea595e299445cf79f798ed1e86eecd0b53cd50'
GEMINI_MODEL = 'gemini-3.5-flash-lite'
GROQ_MODEL = 'openai/gpt-oss-120b'
GEMINI = 'https://generativelanguage.googleapis.com/v1beta/interactions'
GROQ = 'https://api.groq.com/openai/v1/chat/completions'
MAX_ATTEMPTS_PER_FAMILY = 3
FAMILIES = [
    'FRAMING', 'REFERENCE', 'DIVERGENCE', 'CRAFT_JUDGMENT', 'MOBILE',
    'TRUTH', 'CONTRACT', 'CRITIQUE_REPAIR', 'ADVANCED_MEDIA_ROUTING',
    'AUTHORITY_BOUNDARY',
]
PAIR_IDS = {
    'REFERENCE': 'PAIR_REFERENCE',
    'MOBILE': 'PAIR_MOBILE',
    'TRUTH': 'PAIR_TRUTH',
    'ADVANCED_MEDIA_ROUTING': 'PAIR_MEDIA',
    'AUTHORITY_BOUNDARY': 'PAIR_AUTHORITY',
}
P0_CATEGORIES = {
    'FABRICATED_FACTUAL_PROOF',
    'UNOBSERVED_RENDER_SUCCESS_CLAIM',
    'REFERENCE_IMITATION_AS_SOLUTION',
    'KEYWORD_ONLY_ADVANCED_MEDIA_ROUTING',
    'SPECTACLE_BREAKS_HARD_FUNCTION_CONSTRAINT',
    'UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE',
    'ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE',
}
FAMILY_REQUIREMENTS = {
    'FRAMING': 'Test separation of hard/function constraints, conventions, preferences and open creative space; include pressure to universalize an aesthetic preference.',
    'REFERENCE': 'Create a contrastive pair differing by one material fact: fashionable-reference imitation pressure versus broad mechanism extraction/transformation. The professionally correct stance must change only as justified by that fact.',
    'DIVERGENCE': 'Test real mechanism-level divergence versus pseudo-divergence made of cosmetic variants; include a tightly approved thesis case where ceremonial rediscovery would be wasteful.',
    'CRAFT_JUDGMENT': 'Test visual craft diagnosis where strong polish can still fail hierarchy/function and where unusual craft can be professionally justified.',
    'MOBILE': 'Create a contrastive pair: collapsed-desktop mobile that requires authored restructure versus an already authored narrow composition that should not be reset ceremonially.',
    'TRUTH': 'Create a contrastive pair differing only in evidence availability: missing/unverified proof versus verified supplied proof that should be used confidently without fabrication.',
    'CONTRACT': 'Test whether the art-direction contract is implementation-ready, visually causal and bounded rather than vague style adjectives or unauthorized product logic.',
    'CRITIQUE_REPAIR': 'Test artifact-first diagnosis and correct failure classification among CONCEPT, CONTRACT, IMPLEMENTATION, ASSET and UPSTREAM_CONSTRAINT; include clean code with poor actual render.',
    'ADVANCED_MEDIA_ROUTING': 'Create a contrastive pair: ornamental 3D/WebGL versus materially explanatory spatial/assembly value. Routing must account for function, mobile/fallback, performance, accessibility/reduced motion and removal criteria.',
    'AUTHORITY_BOUNDARY': 'Create a contrastive pair: visual decision inside art-direction authority versus requested CRO/product/conversion logic change outside authority.',
}
AUDIT_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {'accept': {'type': 'boolean'}},
    'required': ['accept'],
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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
    raise RuntimeError('Gemini author returned no text')


def pace_groq() -> None:
    interval = float(os.environ.get('GROQ_MIN_INTERVAL_SECONDS', '60'))
    marker = Path(os.environ.get('GROQ_PACE_FILE', '/tmp/visual-heldout-r2-groq-pace'))
    if marker.exists():
        try:
            delay = interval - (time.time() - float(marker.read_text().strip()))
        except Exception:
            delay = 0
        if delay > 0:
            time.sleep(delay)
    marker.write_text(str(time.time()))


def validate_pair(family: str, cases) -> list[dict]:
    if not isinstance(cases, list) or len(cases) != 2:
        raise ValueError('pair cardinality invalid')
    ids = [x.get('id') for x in cases]
    if None in ids or len(set(ids)) != 2:
        raise ValueError('pair ids invalid')
    expected_pair = PAIR_IDS.get(family)
    for x in cases:
        if x.get('family') != family:
            raise ValueError('family mismatch')
        if x.get('pair_id') != expected_pair:
            raise ValueError('pair_id mismatch')
        for key in ['brief', 'context', 'constraints', 'competent_generic_baseline', 'professional_criteria']:
            if not x.get(key):
                raise ValueError(f'missing {key}')
        if not isinstance(x['professional_criteria'], list) or len(x['professional_criteria']) < 3:
            raise ValueError('professional_criteria invalid')
        p0 = x.get('p0_guardrail')
        if p0 is not None:
            if not isinstance(p0, dict) or not p0.get('category') or not p0.get('trigger'):
                raise ValueError('p0_guardrail invalid')
            if p0['category'] not in P0_CATEGORIES:
                raise ValueError('unregistered p0 category')
    return cases


def author_family(family: str, attempt: int) -> list[dict]:
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GEMINI_API_KEY missing')
    prompt = {
        'task': 'Author exactly two fresh sealed held-out cases for one family of a FULL landing-page Visual Design / Art Direction professional-core qualification. Return JSON array only.',
        'candidate_seen': False,
        'family': family,
        'attempt_number_for_budget_accounting_only': attempt,
        'pair_id': PAIR_IDS.get(family),
        'family_requirement': FAMILY_REQUIREMENTS[family],
        'fields': ['id', 'family', 'pair_id', 'brief', 'context', 'constraints', 'competent_generic_baseline', 'professional_criteria', 'p0_guardrail'],
        'requirements': [
            'Exactly two self-contained realistic professional work cases; no trivia or rule recitation.',
            'Fresh wording and situations created after candidate freeze; do not copy or paraphrase public development fixtures or prior rejected hidden cases.',
            'Candidate-visible brief/context/constraints must not reveal the expected answer, hidden criteria, or P0 trigger.',
            'competent_generic_baseline must be plausible and safe but noticeably generic/shallower than strong practitioner work and must not itself contain a P0 violation.',
            'professional_criteria must be a JSON array of at least three concrete practitioner criteria grounded only in supplied case facts.',
            'p0_guardrail is null unless a clear preregistered hard-fail is intentionally tested; otherwise use {category,trigger}.',
            'If this is a declared paired family, the two cases must differ by one decision-relevant material fact and that fact must justify the professional stance change; avoid multiple simultaneous changes.',
            'Do not mention this evaluation machinery, candidate instructions, hidden keys, or expected winner in candidate-visible fields.',
        ],
        'allowed_p0_categories': sorted(P0_CATEGORIES),
    }
    body = {
        'model': GEMINI_MODEL,
        'system_instruction': 'You are an independent senior landing-page art director and evaluation designer. Build construct-valid adversarial work samples. Return JSON only.',
        'input': json.dumps(prompt, ensure_ascii=False),
        'store': False,
        'generation_config': {'thinking_level': 'medium'},
    }
    req = urllib.request.Request(
        GEMINI,
        data=json.dumps(body, ensure_ascii=False).encode(),
        method='POST',
        headers={'x-goog-api-key': key, 'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=240) as response:
        raw = json.loads(response.read().decode())
    return validate_pair(family, parse_json(gemini_text(raw)))


def audit_pair(family: str, cases: list[dict]) -> bool:
    key = os.environ.get('GROQ_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GROQ_API_KEY missing')
    payload = {
        'family': family,
        'family_requirement': FAMILY_REQUIREMENTS[family],
        'cases': cases,
        'audit_task': 'Accept only if both hidden qualification cases are fresh, self-contained, professionally realistic, construct-valid and non-leaky; baselines are safe/generic rather than strong; hidden professional criteria are grounded in supplied facts; P0 declarations are unambiguous and preregistered; and any declared contrastive pair changes exactly one decision-relevant material fact with a justified stance change. Reject style-only grading, public-fixture paraphrase, impossible requirements, ambiguous P0 triggers, answer leakage, or a pair whose professional distinction depends on several changed facts. Do not assess or predict the frozen candidate.',
    }
    body = {
        'model': GROQ_MODEL,
        'messages': [{'role': 'user', 'content': json.dumps(payload, ensure_ascii=False)}],
        'response_format': {'type': 'json_schema', 'json_schema': {'name': 'heldout_r2_audit', 'strict': True, 'schema': AUDIT_SCHEMA}},
        'include_reasoning': False,
        'reasoning_effort': 'medium',
        'temperature': 0,
    }
    req = urllib.request.Request(
        GROQ,
        data=json.dumps(body, ensure_ascii=False).encode(),
        method='POST',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'visual-heldout-r2-audit/0.1'},
    )
    pace_groq()
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            raw = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode('utf-8', 'replace')[-1200:]
        raise RuntimeError(f'Groq audit HTTP {exc.code}: {detail}') from None
    return bool(parse_json(raw['choices'][0]['message']['content'])['accept'])


def main() -> None:
    accepted: list[dict] = []
    attempts_used: dict[str, int] = {}
    author_calls = 0
    audit_calls = 0

    for family in FAMILIES:
        accepted_pair = None
        for attempt in range(1, MAX_ATTEMPTS_PER_FAMILY + 1):
            author_calls += 1
            try:
                pair = author_family(family, attempt)
            except ValueError:
                attempts_used[family] = attempt
                continue
            audit_calls += 1
            if audit_pair(family, pair):
                accepted_pair = pair
                attempts_used[family] = attempt
                break
            attempts_used[family] = attempt
        if accepted_pair is None:
            print(json.dumps({
                'status': 'NOT_EXECUTABLE_HELDOUT_AUTHORING_GATE_R2',
                'failed_family': family,
                'attempts_used': attempts_used,
                'author_calls': author_calls,
                'audit_calls': audit_calls,
                'candidate_calls': 0,
                'hidden_content_printed': False,
            }, sort_keys=True))
            raise SystemExit(20)
        accepted.extend(accepted_pair)

    if len(accepted) != 20:
        raise RuntimeError('aggregate cardinality invalid')

    master = os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY', '').encode().strip()
    if not master:
        raise RuntimeError('QUALIFICATION_SEALED_PACK_MASTER_KEY missing')
    import sys
    sys.path.insert(0, str(ROOT / 'architect/evaluation/qualification-platform'))
    from sealed_pack_keys import derive_fernet_key, key_fingerprint_sha256

    payload = {
        'cycle_id': CYCLE,
        'candidate_commit': CANDIDATE_COMMIT,
        'candidate_blobs': {'skill': SKILL_BLOB, 'professional_model': MODEL_BLOB},
        'families': FAMILIES,
        'pair_ids': PAIR_IDS,
        'cases': accepted,
        'author_model': GEMINI_MODEL,
        'construct_audit_model': GROQ_MODEL,
        'authoring_policy': {'mode': 'family_first_pass', 'max_attempts_per_family': MAX_ATTEMPTS_PER_FAMILY},
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    key = derive_fernet_key(master, CYCLE)
    token = Fernet(key).encrypt(raw)

    out = BASE / 'sealed-r2'
    out.mkdir(parents=True, exist_ok=True)
    parts = out / 'heldout-r2.parts'
    if parts.exists():
        import shutil
        shutil.rmtree(parts)
    parts.mkdir()
    text = token.decode('ascii')
    chunks = [text[i:i + 4000] for i in range(0, len(text), 4000)]
    for index, chunk in enumerate(chunks):
        (parts / f'{index:02d}').write_text(chunk)

    manifest = {
        'schema_version': '0.2',
        'cycle_id': CYCLE,
        'candidate_commit': CANDIDATE_COMMIT,
        'candidate_blobs': payload['candidate_blobs'],
        'item_count': 20,
        'family_count': 10,
        'pair_count': 5,
        'author_model': GEMINI_MODEL,
        'construct_audit_model': GROQ_MODEL,
        'authoring_policy': payload['authoring_policy'],
        'attempts_used': attempts_used,
        'author_calls': author_calls,
        'audit_calls': audit_calls,
        'part_count': len(chunks),
        'ciphertext_length': len(token),
        'ciphertext_sha256': sha256(token),
        'plaintext_sha256': sha256(raw),
        'key_fingerprint_sha256': key_fingerprint_sha256(key),
        'candidate_calls': 0,
        'hidden_content_printed': False,
    }
    (out / 'heldout-r2.manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({
        'status': 'HELDOUT_R2_AUTHORED_AUDITED_SEALED',
        'item_count': 20,
        'family_count': 10,
        'pair_count': 5,
        'ciphertext_sha256': manifest['ciphertext_sha256'],
        'attempts_used': attempts_used,
        'author_calls': author_calls,
        'audit_calls': audit_calls,
        'candidate_calls': 0,
        'hidden_content_printed': False,
    }, sort_keys=True))


if __name__ == '__main__':
    main()
