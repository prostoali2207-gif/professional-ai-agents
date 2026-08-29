#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

from cryptography.fernet import Fernet

ROOT = Path.cwd()
BASE = ROOT / 'architect/evaluation/visual-design-art-direction/heldout'
sys.path.insert(0, str(BASE))
import author_sealed_heldout_r2 as r2

CYCLE = 'visual-design-art-direction-0.1.0-independent-2026-08-29-r3-semantic'
CANDIDATE_COMMIT = r2.CANDIDATE_COMMIT
SKILL_BLOB = r2.SKILL_BLOB
MODEL_BLOB = r2.MODEL_BLOB
GEMINI_MODEL = r2.GEMINI_MODEL
GROQ_MODEL = r2.GROQ_MODEL
MAX_ATTEMPTS_PER_FAMILY = 3

SEMANTIC_CASE_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'brief': {'type': 'string', 'minLength': 1},
        'context': {'type': 'string', 'minLength': 1},
        'constraints': {
            'type': 'array', 'minItems': 1,
            'items': {'type': 'string', 'minLength': 1},
        },
        'competent_generic_baseline': {'type': 'string', 'minLength': 1},
        'professional_criteria': {
            'type': 'array', 'minItems': 3,
            'items': {'type': 'string', 'minLength': 1},
        },
        'p0_guardrail': {
            'type': ['object', 'null'],
            'additionalProperties': False,
            'properties': {
                'category': {'type': 'string', 'enum': sorted(r2.P0_CATEGORIES)},
                'trigger': {'type': 'string', 'minLength': 1},
            },
            'required': ['category', 'trigger'],
        },
    },
    'required': [
        'brief', 'context', 'constraints', 'competent_generic_baseline',
        'professional_criteria', 'p0_guardrail',
    ],
}
AUTHOR_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'cases': {
            'type': 'array',
            'minItems': 2,
            'maxItems': 2,
            'items': SEMANTIC_CASE_SCHEMA,
        }
    },
    'required': ['cases'],
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_and_bind(family: str, raw: dict) -> list[dict]:
    cases = raw.get('cases')
    if not isinstance(cases, list) or len(cases) != 2:
        raise ValueError('schema_cardinality')
    bound = []
    for idx, semantic in enumerate(cases, start=1):
        if not isinstance(semantic, dict):
            raise ValueError('schema_case_type')
        criteria = semantic.get('professional_criteria')
        constraints = semantic.get('constraints')
        if not isinstance(criteria, list) or len(criteria) < 3 or not all(isinstance(x, str) and x.strip() for x in criteria):
            raise ValueError('schema_professional_criteria')
        if not isinstance(constraints, list) or not constraints or not all(isinstance(x, str) and x.strip() for x in constraints):
            raise ValueError('schema_constraints')
        for field in ('brief', 'context', 'competent_generic_baseline'):
            if not isinstance(semantic.get(field), str) or not semantic[field].strip():
                raise ValueError(f'schema_{field}')
        p0 = semantic.get('p0_guardrail')
        if p0 is not None:
            if not isinstance(p0, dict) or p0.get('category') not in r2.P0_CATEGORIES or not isinstance(p0.get('trigger'), str) or not p0['trigger'].strip():
                raise ValueError('schema_p0')
        case = dict(semantic)
        case['id'] = f'{family}-R3-{idx}'
        case['family'] = family
        case['pair_id'] = r2.PAIR_IDS.get(family)
        bound.append(case)
    return bound


def author_family(family: str, attempt: int) -> list[dict]:
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GEMINI_API_KEY missing')
    prompt = {
        'task': 'Author exactly two fresh sealed held-out cases for one family of a FULL landing-page Visual Design / Art Direction professional-core qualification.',
        'candidate_seen': False,
        'family': family,
        'attempt_number_for_budget_accounting_only': attempt,
        'family_requirement': r2.FAMILY_REQUIREMENTS[family],
        'declared_contrastive_pair': family in r2.PAIR_IDS,
        'requirements': [
            'Exactly two self-contained realistic professional work cases; no trivia or rule recitation.',
            'Fresh wording and situations created after candidate freeze; do not copy or paraphrase public development fixtures or prior rejected hidden cases.',
            'Candidate-visible brief/context/constraints must not reveal expected answer, hidden criteria or P0 trigger.',
            'competent_generic_baseline must be plausible and safe but noticeably generic/shallower than strong practitioner work and must not itself contain a P0 violation.',
            'professional_criteria must contain at least three concrete practitioner criteria grounded only in supplied case facts.',
            'p0_guardrail is null unless a clear preregistered hard-fail is intentionally tested.',
            'For a declared contrastive family, the two cases must differ by one decision-relevant material fact and that fact must justify the professional stance change; avoid multiple simultaneous changes.',
            'Do not mention evaluation machinery, candidate instructions, hidden keys or expected winner in candidate-visible fields.',
        ],
        'allowed_p0_categories': sorted(r2.P0_CATEGORIES),
    }
    body = {
        'model': GEMINI_MODEL,
        'system_instruction': 'You are an independent senior landing-page art director and evaluation designer. Build construct-valid adversarial work samples. Follow the supplied JSON schema exactly.',
        'input': json.dumps(prompt, ensure_ascii=False),
        'store': False,
        'generation_config': {'thinking_level': 'medium'},
        'response_format': {
            'type': 'text',
            'mime_type': 'application/json',
            'schema': AUTHOR_SCHEMA,
        },
    }
    req = urllib.request.Request(
        r2.GEMINI,
        data=json.dumps(body, ensure_ascii=False).encode(),
        method='POST',
        headers={'x-goog-api-key': key, 'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=240) as response:
        interaction = json.loads(response.read().decode())
    return validate_and_bind(family, json.loads(r2.gemini_text(interaction)))


def main() -> None:
    accepted: list[dict] = []
    attempts_used: dict[str, int] = {}
    structural_rejections: dict[str, int] = {}
    audit_rejections: dict[str, int] = {}
    author_calls = 0
    audit_calls = 0

    for family in r2.FAMILIES:
        accepted_pair = None
        structural_rejections[family] = 0
        audit_rejections[family] = 0
        for attempt in range(1, MAX_ATTEMPTS_PER_FAMILY + 1):
            author_calls += 1
            attempts_used[family] = attempt
            try:
                pair = author_family(family, attempt)
            except (ValueError, json.JSONDecodeError):
                structural_rejections[family] += 1
                continue
            audit_calls += 1
            if r2.audit_pair(family, pair):
                accepted_pair = pair
                break
            audit_rejections[family] += 1
        if accepted_pair is None:
            print(json.dumps({
                'status': 'NOT_EXECUTABLE_HELDOUT_AUTHORING_GATE_R3',
                'failed_family': family,
                'attempts_used': attempts_used,
                'structural_rejections': structural_rejections,
                'audit_rejections': audit_rejections,
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
    sys.path.insert(0, str(ROOT / 'architect/evaluation/qualification-platform'))
    from sealed_pack_keys import derive_fernet_key, key_fingerprint_sha256

    payload = {
        'cycle_id': CYCLE,
        'candidate_commit': CANDIDATE_COMMIT,
        'candidate_blobs': {'skill': SKILL_BLOB, 'professional_model': MODEL_BLOB},
        'families': r2.FAMILIES,
        'pair_ids': r2.PAIR_IDS,
        'cases': accepted,
        'author_model': GEMINI_MODEL,
        'construct_audit_model': GROQ_MODEL,
        'authoring_policy': {
            'mode': 'family_first_pass_schema_enforced',
            'max_attempts_per_family': MAX_ATTEMPTS_PER_FAMILY,
        },
    }
    plaintext = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    key = derive_fernet_key(master, CYCLE)
    ciphertext = Fernet(key).encrypt(plaintext)

    out = BASE / 'sealed-r3'
    out.mkdir(parents=True, exist_ok=True)
    parts = out / 'heldout-r3.parts'
    if parts.exists():
        import shutil
        shutil.rmtree(parts)
    parts.mkdir()
    token = ciphertext.decode('ascii')
    chunks = [token[i:i + 4000] for i in range(0, len(token), 4000)]
    for index, chunk in enumerate(chunks):
        (parts / f'{index:02d}').write_text(chunk)

    manifest = {
        'schema_version': '0.3',
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
        'structural_rejections': structural_rejections,
        'audit_rejections': audit_rejections,
        'author_calls': author_calls,
        'audit_calls': audit_calls,
        'part_count': len(chunks),
        'ciphertext_length': len(ciphertext),
        'ciphertext_sha256': sha256(ciphertext),
        'plaintext_sha256': sha256(plaintext),
        'key_fingerprint_sha256': key_fingerprint_sha256(key),
        'candidate_calls': 0,
        'hidden_content_printed': False,
    }
    (out / 'heldout-r3.manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({
        'status': 'HELDOUT_R3_AUTHORED_AUDITED_SEALED',
        'item_count': 20,
        'family_count': 10,
        'pair_count': 5,
        'ciphertext_sha256': manifest['ciphertext_sha256'],
        'attempts_used': attempts_used,
        'structural_rejections': structural_rejections,
        'audit_rejections': audit_rejections,
        'author_calls': author_calls,
        'audit_calls': audit_calls,
        'candidate_calls': 0,
        'hidden_content_printed': False,
    }, sort_keys=True))


if __name__ == '__main__':
    main()
