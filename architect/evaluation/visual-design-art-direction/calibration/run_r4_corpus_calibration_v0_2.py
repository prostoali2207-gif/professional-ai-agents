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

# Exact R4 / v0.2 bindings. Reuse the already-validated R3 calibration mechanism only.
base.PACK_DIR = Path('r4-source')
base.CYCLE = 'visual-design-art-direction-0.2.0-independent-2026-08-30-r4-corpus-calibration'
base.SEMANTIC_CYCLE = 'visual-design-art-direction-0.2.0-independent-2026-08-30-r4-semantic'
base.CANDIDATE_COMMIT = '0116d20f99fde919fa6e39c700726d16310d010b'
base.SKILL_BLOB = 'b230a06aeca3cc67d0c275889a65b8b7403b59c0'
BASE_MODEL_BLOB = 'bbea595e299445cf79f798ed1e86eecd0b53cd50'
REPAIR_MODEL_BLOB = 'bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50'
base.SOURCE_RUN_ID = '33306265227'
base.SOURCE_HEAD_SHA = '147f1581c1ff24c51b71169aaad7770d6d27f3ce'
base.SOURCE_ARTIFACT_ID = '9730714845'
base.SOURCE_ARTIFACT_NAME = 'visual-design-art-direction-v0-2-encrypted-heldout-pack-r4'
base.SOURCE_ARTIFACT_DIGEST = 'sha256:fbe4b03ffc1eede30b3e36dcaa13e7bf96e29c28cf40d722ae2e376355f0e73e'
EXPECTED_CIPHERTEXT_SHA256 = 'b6147b01b838aa447fcaff711668771d6347a329f97ac21c7c97f9c9d6e85bf6'
base.CHECKPOINT = Path('visual-r4-corpus-calibration-checkpoint.enc')
base.PROGRESS = Path('visual-r4-corpus-calibration-progress.json')
base.REPORT = Path('visual-r4-corpus-calibration-sanitized-report.json')

# Frozen release judges/thresholds remain inherited from base:
# gemini-3.5-flash-lite, openai/gpt-oss-120b, 0.80 / 0.90 / 0.25.


def load_pack_r4() -> tuple[dict, dict]:
    manifest_path = base.PACK_DIR / 'heldout-r4.manifest.json'
    parts_path = base.PACK_DIR / 'heldout-r4.parts'
    manifest = json.load(open(manifest_path))
    expected_blobs = {
        'skill': base.SKILL_BLOB,
        'professional_model_base': BASE_MODEL_BLOB,
        'professional_model_repair': REPAIR_MODEL_BLOB,
    }
    assert manifest['cycle_id'] == base.SEMANTIC_CYCLE
    assert manifest['candidate_commit'] == base.CANDIDATE_COMMIT
    assert manifest['candidate_blobs'] == expected_blobs
    assert manifest['item_count'] == 20 and manifest['family_count'] == 10 and manifest['pair_count'] == 5
    assert manifest['candidate_calls'] == 0 and manifest['hidden_content_printed'] is False
    assert manifest.get('historical_r3_reused') is False
    assert manifest['ciphertext_sha256'] == EXPECTED_CIPHERTEXT_SHA256

    ciphertext = ''.join(p.read_text() for p in sorted(parts_path.iterdir())).encode()
    assert len(ciphertext) == manifest['ciphertext_length']
    assert hashlib.sha256(ciphertext).hexdigest() == EXPECTED_CIPHERTEXT_SHA256
    plaintext = Fernet(base.derive_key(base.SEMANTIC_CYCLE)).decrypt(ciphertext)
    assert hashlib.sha256(plaintext).hexdigest() == manifest['plaintext_sha256']
    payload = json.loads(plaintext)
    assert payload['cycle_id'] == base.SEMANTIC_CYCLE
    assert payload['candidate_commit'] == base.CANDIDATE_COMMIT
    assert payload['candidate_blobs'] == expected_blobs
    cases = payload['cases']
    assert len(cases) == 20
    counts = {family: 0 for family in base.FAMILIES}
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
            assert p0['category'] in base.P0_CATEGORIES and p0['trigger']
    assert all(value == 2 for value in counts.values())
    return manifest, payload


base.load_pack = load_pack_r4

if __name__ == '__main__':
    base.main()
