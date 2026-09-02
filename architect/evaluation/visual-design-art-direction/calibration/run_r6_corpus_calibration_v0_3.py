#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from cryptography.fernet import Fernet

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_r3_corpus_calibration_v0_1 as base

# Exact R6 / v0.3 bindings. Reuse the validated exact-corpus calibration
# mechanism; this adapter changes transport/schema identity only.
base.PACK_DIR = Path('r6-source')
base.CYCLE = 'visual-design-art-direction-0.3.0-independent-2026-09-01-r6-corpus-calibration'
base.SEMANTIC_CYCLE = 'visual-design-art-direction-0.3.0-independent-2026-09-01-r6-semantic'
base.CANDIDATE_COMMIT = 'b4793a66172d4de7fe0ade1b0001bc2621829db2'
FREEZE_INTEGRITY_COMMIT = '347491bbedeaee6fbda038db9639f16040a41301'
FREEZE_BLOB = '84db2da24f784591c7cc1feb5f1f9a9c22220e40'
base.SKILL_BLOB = 'bee4ee67a8aff43016e158f37a6f421cd079581a'
BASE_MODEL_BLOB = 'bbea595e299445cf79f798ed1e86eecd0b53cd50'
REPAIR_V02_MODEL_BLOB = 'bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50'
REPAIR_V03_MODEL_BLOB = 'dd42d50f07b804c1ddd3c93b96704e0c6256440c'
base.MODEL_BLOB = BASE_MODEL_BLOB
base.SOURCE_RUN_ID = '33500210303'
base.SOURCE_HEAD_SHA = '7e506c6afb85489758bbf8c2ad08ede75264fd1d'
base.SOURCE_ARTIFACT_ID = '9797673448'
base.SOURCE_ARTIFACT_NAME = 'visual-design-art-direction-v0-3-encrypted-heldout-pack-r6'
base.SOURCE_ARTIFACT_DIGEST = 'sha256:9e6286ec436031aa121e631f0613216236322598ed71d8ae8c22938050886142'
EXPECTED_CIPHERTEXT_SHA256 = 'ffecad8a5087bda276a95825a1e0071ca18640392a12dbb26f0f8ec5ba78cdeb'
base.CHECKPOINT = Path('visual-r6-v03-corpus-calibration-checkpoint.enc')
base.PROGRESS = Path('visual-r6-v03-corpus-calibration-progress.json')
base.REPORT = Path('visual-r6-v03-corpus-calibration-sanitized-report.json')

EXPECTED_BLOBS = {
    'skill': base.SKILL_BLOB,
    'professional_model_base': BASE_MODEL_BLOB,
    'professional_model_repair_v02': REPAIR_V02_MODEL_BLOB,
    'professional_model_repair_v03': REPAIR_V03_MODEL_BLOB,
}
PAIRED_FAMILIES = {
    'REFERENCE', 'MOBILE', 'TRUTH', 'ADVANCED_MEDIA_ROUTING', 'AUTHORITY_BOUNDARY',
}
EXPECTED_PAIR_IDS = {
    'REFERENCE': 'PAIR_REFERENCE',
    'MOBILE': 'PAIR_MOBILE',
    'TRUTH': 'PAIR_TRUTH',
    'ADVANCED_MEDIA_ROUTING': 'PAIR_MEDIA',
    'AUTHORITY_BOUNDARY': 'PAIR_AUTHORITY',
}

# Frozen release judges/thresholds are inherited unchanged from base:
# gemini-3.5-flash-lite, openai/gpt-oss-120b, 0.80 / 0.90 / 0.25.


def _validate_pair_contract(contract: dict) -> None:
    assert isinstance(contract, dict)
    for field in (
        'controlled_material_fact', 'case_1_value', 'case_2_value',
        'why_this_one_fact_can_change_professional_stance',
    ):
        assert isinstance(contract.get(field), str) and contract[field].strip()
    assert contract['case_1_value'].strip().casefold() != contract['case_2_value'].strip().casefold()
    held = contract.get('held_constant_facts')
    assert isinstance(held, list) and len(held) >= 4
    assert all(isinstance(value, str) and value.strip() for value in held)
    normalized = [value.strip().casefold() for value in held]
    assert len(normalized) == len(set(normalized))


def load_pack_r6() -> tuple[dict, dict]:
    manifest_path = base.PACK_DIR / 'heldout-r6.manifest.json'
    parts_path = base.PACK_DIR / 'heldout-r6.parts'
    manifest = json.load(open(manifest_path))

    assert manifest['schema_version'] == '0.6'
    assert manifest['cycle_id'] == base.SEMANTIC_CYCLE
    assert manifest['candidate_commit'] == base.CANDIDATE_COMMIT
    assert manifest['freeze_integrity_commit'] == FREEZE_INTEGRITY_COMMIT
    assert manifest['candidate_freeze_blob'] == FREEZE_BLOB
    assert manifest['candidate_blobs'] == EXPECTED_BLOBS
    assert manifest['item_count'] == 20
    assert manifest['family_count'] == 10
    assert manifest['pair_count'] == 5
    assert manifest['pair_contract_count'] == 5
    assert manifest['pair_contract_schema_version'] == '0.1'
    assert manifest['author_model'] == base.GEMINI_MODEL
    assert manifest['construct_audit_model'] == base.GROQ_MODEL
    assert manifest['authoring_policy'] == {
        'mode': 'family_first_pass_schema_enforced_pair_contract_v1',
        'max_attempts_per_family': 3,
    }
    assert manifest['candidate_calls'] == 0
    assert manifest['hidden_content_printed'] is False
    assert manifest['historical_r3_reused'] is False
    assert manifest['historical_r4_reused'] is False
    assert manifest['historical_r5_reused'] is False
    assert manifest['ciphertext_sha256'] == EXPECTED_CIPHERTEXT_SHA256

    ciphertext = ''.join(p.read_text() for p in sorted(parts_path.iterdir())).encode()
    assert len(ciphertext) == manifest['ciphertext_length']
    assert hashlib.sha256(ciphertext).hexdigest() == EXPECTED_CIPHERTEXT_SHA256
    plaintext = Fernet(base.derive_key(base.SEMANTIC_CYCLE)).decrypt(ciphertext)
    assert hashlib.sha256(plaintext).hexdigest() == manifest['plaintext_sha256']
    payload = json.loads(plaintext)

    assert payload['cycle_id'] == base.SEMANTIC_CYCLE
    assert payload['candidate_commit'] == base.CANDIDATE_COMMIT
    assert payload['freeze_integrity_commit'] == FREEZE_INTEGRITY_COMMIT
    assert payload['candidate_freeze_blob'] == FREEZE_BLOB
    assert payload['candidate_blobs'] == EXPECTED_BLOBS
    assert payload['author_model'] == base.GEMINI_MODEL
    assert payload['construct_audit_model'] == base.GROQ_MODEL
    assert payload['authoring_policy'] == manifest['authoring_policy']
    assert payload['pair_ids'] == EXPECTED_PAIR_IDS

    pair_contracts = payload.get('pair_contracts')
    assert isinstance(pair_contracts, dict)
    assert set(pair_contracts) == PAIRED_FAMILIES
    assert len(pair_contracts) == 5
    for contract in pair_contracts.values():
        _validate_pair_contract(contract)

    cases = payload['cases']
    assert len(cases) == 20
    counts = {family: 0 for family in base.FAMILIES}
    ids = set()
    pair_members = {family: [] for family in PAIRED_FAMILIES}
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
            assert p0['category'] in base.P0_CATEGORIES and p0['trigger']
        if case['family'] in PAIRED_FAMILIES:
            assert case['pair_id'] == EXPECTED_PAIR_IDS[case['family']]
            pair_members[case['family']].append(case['id'])
        else:
            assert case['pair_id'] is None
    assert all(value == 2 for value in counts.values())
    assert all(len(members) == 2 for members in pair_members.values())
    return manifest, payload


base.load_pack = load_pack_r6

if __name__ == '__main__':
    base.main()
