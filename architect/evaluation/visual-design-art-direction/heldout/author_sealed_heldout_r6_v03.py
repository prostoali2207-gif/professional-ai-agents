#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from cryptography.fernet import Fernet

ROOT = Path.cwd()
BASE = ROOT / 'architect/evaluation/visual-design-art-direction/heldout'
sys.path.insert(0, str(BASE))
import author_sealed_heldout_r2 as r2

CYCLE = 'visual-design-art-direction-0.3.0-independent-2026-09-01-r6-semantic'
CANDIDATE_COMMIT = 'b4793a66172d4de7fe0ade1b0001bc2621829db2'
FREEZE_INTEGRITY_COMMIT = '347491bbedeaee6fbda038db9639f16040a41301'
FREEZE_BLOB = '84db2da24f784591c7cc1feb5f1f9a9c22220e40'
SKILL_BLOB = 'bee4ee67a8aff43016e158f37a6f421cd079581a'
BASE_MODEL_BLOB = 'bbea595e299445cf79f798ed1e86eecd0b53cd50'
REPAIR_V02_MODEL_BLOB = 'bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50'
REPAIR_V03_MODEL_BLOB = 'dd42d50f07b804c1ddd3c93b96704e0c6256440c'
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

PAIR_CONTRACT_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'controlled_material_fact': {'type': 'string', 'minLength': 1},
        'case_1_value': {'type': 'string', 'minLength': 1},
        'case_2_value': {'type': 'string', 'minLength': 1},
        'held_constant_facts': {
            'type': 'array', 'minItems': 4,
            'items': {'type': 'string', 'minLength': 1},
        },
        'why_this_one_fact_can_change_professional_stance': {'type': 'string', 'minLength': 1},
    },
    'required': [
        'controlled_material_fact', 'case_1_value', 'case_2_value',
        'held_constant_facts', 'why_this_one_fact_can_change_professional_stance',
    ],
}

PAIRED_AUTHOR_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'pair_contract': PAIR_CONTRACT_SCHEMA,
        'cases': {
            'type': 'array',
            'minItems': 2,
            'maxItems': 2,
            'items': SEMANTIC_CASE_SCHEMA,
        },
    },
    'required': ['pair_contract', 'cases'],
}

UNPAIRED_AUTHOR_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'cases': {
            'type': 'array',
            'minItems': 2,
            'maxItems': 2,
            'items': SEMANTIC_CASE_SCHEMA,
        },
    },
    'required': ['cases'],
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_semantic_case(semantic: dict) -> None:
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


def validate_pair_contract(contract: dict) -> None:
    if not isinstance(contract, dict):
        raise ValueError('pair_contract_type')
    for field in (
        'controlled_material_fact', 'case_1_value', 'case_2_value',
        'why_this_one_fact_can_change_professional_stance',
    ):
        if not isinstance(contract.get(field), str) or not contract[field].strip():
            raise ValueError(f'pair_contract_{field}')
    if contract['case_1_value'].strip().casefold() == contract['case_2_value'].strip().casefold():
        raise ValueError('pair_contract_values_not_distinct')
    held = contract.get('held_constant_facts')
    if not isinstance(held, list) or len(held) < 4 or not all(isinstance(x, str) and x.strip() for x in held):
        raise ValueError('pair_contract_held_constants')
    normalized = [x.strip().casefold() for x in held]
    if len(set(normalized)) != len(normalized):
        raise ValueError('pair_contract_duplicate_constants')


def validate_and_bind(family: str, raw: dict) -> tuple[list[dict], dict | None]:
    cases = raw.get('cases')
    if not isinstance(cases, list) or len(cases) != 2:
        raise ValueError('schema_cardinality')

    contract = None
    if family in r2.PAIR_IDS:
        contract = raw.get('pair_contract')
        validate_pair_contract(contract)
    elif 'pair_contract' in raw:
        raise ValueError('unexpected_pair_contract')

    bound = []
    for idx, semantic in enumerate(cases, start=1):
        validate_semantic_case(semantic)
        case = dict(semantic)
        case['id'] = f'{family}-R6-{idx}'
        case['family'] = family
        case['pair_id'] = r2.PAIR_IDS.get(family)
        bound.append(case)
    return bound, contract


def author_family(family: str, attempt: int) -> tuple[list[dict], dict | None]:
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GEMINI_API_KEY missing')

    paired = family in r2.PAIR_IDS
    requirements = [
        'Exactly two self-contained realistic professional work cases; no trivia or rule recitation.',
        'Fresh wording and situations created after the corrected v0.3 freeze; do not copy, paraphrase, reconstruct, or reuse public development fixtures or any prior hidden corpus.',
        'Candidate-visible brief/context/constraints must not reveal expected answer, hidden criteria, P0 trigger, pair contract, or evaluation machinery.',
        'competent_generic_baseline must be plausible and safe but noticeably generic/shallower than strong practitioner work and must not itself contain a P0 violation.',
        'professional_criteria must contain at least three concrete practitioner criteria grounded only in supplied case facts.',
        'p0_guardrail is null unless a clear preregistered hard-fail is intentionally tested.',
        'Do not mention candidate changes, prior failures, repair details, hidden keys, or expected winner in candidate-visible fields.',
        'Do not narrowly target v0.3 public regression wording; assess the family construct broadly.',
    ]
    if paired:
        requirements.extend([
            'First define pair_contract. It must name exactly one decision-relevant material fact that changes between the two cases, two distinct values for that fact, and at least four decision-relevant facts that remain constant.',
            'Create case 1 under case_1_value, then derive case 2 by changing only controlled_material_fact to case_2_value. Hold every other decision-relevant fact constant, even if wording differs.',
            'The single controlled fact must be sufficient to justify a professional stance change under the supplied family requirement; do not smuggle in a second changed fact.',
            'The pair contract is evaluator-only metadata. Do not expose it or its expected stance-change rationale inside candidate-visible brief/context/constraints.',
        ])

    prompt = {
        'task': 'Author exactly two fresh sealed held-out cases for one family of a FULL landing-page Visual Design / Art Direction professional-core qualification.',
        'candidate_seen': False,
        'candidate_version_context': 'v0.3 is frozen; do not inspect, infer, target, or mention candidate changes',
        'historical_corpus_boundary': 'R3, R4 and R5 hidden cases are unavailable and forbidden. Public v0.1/v0.2/v0.3 development fixtures are not held-out source material. Create genuinely fresh situations.',
        'family': family,
        'attempt_number_for_budget_accounting_only': attempt,
        'family_requirement': r2.FAMILY_REQUIREMENTS[family],
        'declared_contrastive_pair': paired,
        'requirements': requirements,
        'allowed_p0_categories': sorted(r2.P0_CATEGORIES),
    }
    schema = PAIRED_AUTHOR_SCHEMA if paired else UNPAIRED_AUTHOR_SCHEMA
    body = {
        'model': GEMINI_MODEL,
        'system_instruction': 'You are an independent senior landing-page art director and evaluation designer. Build construct-valid adversarial work samples. Follow the supplied JSON schema exactly.',
        'input': json.dumps(prompt, ensure_ascii=False),
        'store': False,
        'generation_config': {'thinking_level': 'medium'},
        'response_format': {
            'type': 'text',
            'mime_type': 'application/json',
            'schema': schema,
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


def audit_paired_family(family: str, cases: list[dict], pair_contract: dict) -> bool:
    key = os.environ.get('GROQ_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GROQ_API_KEY missing')
    payload = {
        'family': family,
        'family_requirement': r2.FAMILY_REQUIREMENTS[family],
        'pair_contract': pair_contract,
        'cases': cases,
        'audit_task': (
            'Accept only if both hidden qualification cases are fresh, self-contained, professionally realistic, construct-valid and non-leaky; '
            'baselines are safe/generic rather than strong; hidden professional criteria are grounded in supplied facts; P0 declarations are unambiguous and preregistered. '
            'For this declared contrastive pair, independently verify that pair_contract identifies exactly one decision-relevant material fact, that the two cases instantiate its two distinct values, '
            'that the listed held-constant material facts truly remain constant, that no additional decision-relevant fact changes in a way that could explain the stance difference, and that the one controlled fact legitimately justifies the professional stance change. '
            'The pair contract is only an author claim and is not sufficient by itself: check the actual cases. Reject style-only grading, public-fixture paraphrase, impossible requirements, ambiguous P0 triggers, answer leakage, or multi-variable contrast. '
            'Do not assess or predict the frozen candidate.'
        ),
    }
    body = {
        'model': GROQ_MODEL,
        'messages': [{'role': 'user', 'content': json.dumps(payload, ensure_ascii=False)}],
        'response_format': {'type': 'json_schema', 'json_schema': {'name': 'heldout_r6_pair_audit', 'strict': True, 'schema': r2.AUDIT_SCHEMA}},
        'include_reasoning': False,
        'reasoning_effort': 'medium',
        'temperature': 0,
    }
    req = urllib.request.Request(
        r2.GROQ,
        data=json.dumps(body, ensure_ascii=False).encode(),
        method='POST',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'visual-heldout-r6-pair-audit/0.1'},
    )
    r2.pace_groq()
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            raw = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode('utf-8', 'replace')[-1200:]
        raise RuntimeError(f'Groq audit HTTP {exc.code}: {detail}') from None
    return bool(r2.parse_json(raw['choices'][0]['message']['content'])['accept'])


def main() -> None:
    accepted: list[dict] = []
    accepted_pair_contracts: dict[str, dict] = {}
    attempts_used: dict[str, int] = {}
    structural_rejections: dict[str, int] = {}
    audit_rejections: dict[str, int] = {}
    author_calls = 0
    audit_calls = 0

    for family in r2.FAMILIES:
        accepted_pair = None
        accepted_contract = None
        structural_rejections[family] = 0
        audit_rejections[family] = 0
        for attempt in range(1, MAX_ATTEMPTS_PER_FAMILY + 1):
            author_calls += 1
            attempts_used[family] = attempt
            try:
                pair, pair_contract = author_family(family, attempt)
            except (ValueError, json.JSONDecodeError):
                structural_rejections[family] += 1
                continue
            audit_calls += 1
            if family in r2.PAIR_IDS:
                accepted_by_audit = audit_paired_family(family, pair, pair_contract)
            else:
                accepted_by_audit = r2.audit_pair(family, pair)
            if accepted_by_audit:
                accepted_pair = pair
                accepted_contract = pair_contract
                break
            audit_rejections[family] += 1
        if accepted_pair is None:
            print(json.dumps({
                'status': 'NOT_EXECUTABLE_HELDOUT_AUTHORING_GATE_R6',
                'failed_family': family,
                'attempts_used': attempts_used,
                'structural_rejections': structural_rejections,
                'audit_rejections': audit_rejections,
                'author_calls': author_calls,
                'audit_calls': audit_calls,
                'candidate_calls': 0,
                'hidden_content_printed': False,
                'historical_r3_reused': False,
                'historical_r4_reused': False,
                'historical_r5_reused': False,
            }, sort_keys=True))
            raise SystemExit(20)
        accepted.extend(accepted_pair)
        if accepted_contract is not None:
            accepted_pair_contracts[family] = accepted_contract

    if len(accepted) != 20 or set(accepted_pair_contracts) != set(r2.PAIR_IDS):
        raise RuntimeError('aggregate cardinality or paired-contract coverage invalid')

    master = os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY', '').encode().strip()
    if not master:
        raise RuntimeError('QUALIFICATION_SEALED_PACK_MASTER_KEY missing')
    sys.path.insert(0, str(ROOT / 'architect/evaluation/qualification-platform'))
    from sealed_pack_keys import derive_fernet_key, key_fingerprint_sha256

    candidate_blobs = {
        'skill': SKILL_BLOB,
        'professional_model_base': BASE_MODEL_BLOB,
        'professional_model_repair_v02': REPAIR_V02_MODEL_BLOB,
        'professional_model_repair_v03': REPAIR_V03_MODEL_BLOB,
    }
    payload = {
        'cycle_id': CYCLE,
        'candidate_commit': CANDIDATE_COMMIT,
        'freeze_integrity_commit': FREEZE_INTEGRITY_COMMIT,
        'candidate_freeze_blob': FREEZE_BLOB,
        'candidate_blobs': candidate_blobs,
        'families': r2.FAMILIES,
        'pair_ids': r2.PAIR_IDS,
        'pair_contracts': accepted_pair_contracts,
        'cases': accepted,
        'author_model': GEMINI_MODEL,
        'construct_audit_model': GROQ_MODEL,
        'authoring_policy': {
            'mode': 'family_first_pass_schema_enforced_pair_contract_v1',
            'max_attempts_per_family': MAX_ATTEMPTS_PER_FAMILY,
        },
    }
    plaintext = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    key = derive_fernet_key(master, CYCLE)
    ciphertext = Fernet(key).encrypt(plaintext)

    out = BASE / 'sealed-r6-v03'
    out.mkdir(parents=True, exist_ok=True)
    parts = out / 'heldout-r6.parts'
    if parts.exists():
        import shutil
        shutil.rmtree(parts)
    parts.mkdir()
    token = ciphertext.decode('ascii')
    chunks = [token[i:i + 4000] for i in range(0, len(token), 4000)]
    for index, chunk in enumerate(chunks):
        (parts / f'{index:02d}').write_text(chunk)

    manifest = {
        'schema_version': '0.6',
        'cycle_id': CYCLE,
        'candidate_commit': CANDIDATE_COMMIT,
        'freeze_integrity_commit': FREEZE_INTEGRITY_COMMIT,
        'candidate_freeze_blob': FREEZE_BLOB,
        'candidate_blobs': candidate_blobs,
        'item_count': 20,
        'family_count': 10,
        'pair_count': 5,
        'pair_contract_count': len(accepted_pair_contracts),
        'pair_contract_schema_version': '0.1',
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
        'historical_r3_reused': False,
        'historical_r4_reused': False,
        'historical_r5_reused': False,
    }
    (out / 'heldout-r6.manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({
        'status': 'HELDOUT_R6_V03_AUTHORED_AUDITED_SEALED',
        'item_count': 20,
        'family_count': 10,
        'pair_count': 5,
        'pair_contract_count': len(accepted_pair_contracts),
        'ciphertext_sha256': manifest['ciphertext_sha256'],
        'attempts_used': attempts_used,
        'structural_rejections': structural_rejections,
        'audit_rejections': audit_rejections,
        'author_calls': author_calls,
        'audit_calls': audit_calls,
        'candidate_calls': 0,
        'hidden_content_printed': False,
        'historical_r3_reused': False,
        'historical_r4_reused': False,
        'historical_r5_reused': False,
    }, sort_keys=True))


if __name__ == '__main__':
    main()
