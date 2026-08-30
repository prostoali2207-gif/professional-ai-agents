#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
BASE = ROOT / 'architect/evaluation/sales-lead-conversion/qualification-preregistration-v0_5-r1-gemini-groq.json'
BASE_BLOB = '1ca4bc61bdeb78364eae0d715ddd7243e9b4bd5c'
DELTA = ROOT / 'architect/evaluation/sales-lead-conversion/qualification-preregistration-v0_5-r3-gemini-groq.json'
CYCLE = 'sales-0.5-fresh-independent-2026-08-30-r3-gemini-groq'


def build() -> dict:
    actual = subprocess.check_output(['git', 'hash-object', str(BASE)], text=True).strip()
    if actual != BASE_BLOB:
        raise RuntimeError(f'r1 prereg drift: {actual}')
    base = json.loads(BASE.read_text())
    delta = json.loads(DELTA.read_text())
    if delta.get('cycle_id') != CYCLE:
        raise RuntimeError('r3 cycle mismatch')
    binding = delta.get('base_preregistration', {})
    if binding.get('path') != str(BASE.relative_to(ROOT)) or binding.get('blob') != BASE_BLOB:
        raise RuntimeError('r3 base prereg binding mismatch')

    effective = deepcopy(base)
    effective['cycle_id'] = CYCLE
    effective['status'] = delta['status']
    effective['frozen_candidate'] = delta['frozen_candidate']
    effective['prior_cycle_evidence'] = delta['prior_sanitized_evidence']
    effective['authoring_remediation'] = delta['authoring_remediation']

    route = deepcopy(base['heldout_authoring'])
    route['hidden_reference_transport'] = {
        'field_name': delta['authoring_remediation']['field_name'],
        'representation_change': delta['authoring_remediation']['representation_change'],
        'tagged_record_contract': delta['authoring_remediation']['tagged_record_contract'],
        'decoder_rule': delta['authoring_remediation']['decoder_rule'],
        'fresh_attempt_rule': delta['authoring_remediation']['fresh_attempt_rule'],
    }
    route['safe_structural_reason_codes'] = delta['authoring_remediation']['safe_structural_reason_codes']
    route['safe_observability'] = delta['authoring_remediation']['safe_observability']
    effective['heldout_authoring'] = route
    effective['sealed_transport_contract']['derivation_context'] = CYCLE
    effective['release_rule'] = delta['release_rule']
    return effective


def main() -> int:
    effective = build()
    if len(sys.argv) == 2:
        Path(sys.argv[1]).write_text(json.dumps(effective, ensure_ascii=False, indent=2) + '\n')
    else:
        json.dump(effective, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write('\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
