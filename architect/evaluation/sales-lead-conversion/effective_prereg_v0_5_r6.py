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
DELTA = ROOT / 'architect/evaluation/sales-lead-conversion/qualification-preregistration-v0_5-r6-gemini-groq.json'
DELTA_BLOB = '70548ce27547f017777ef15b47cffdacdeb124ac'
CYCLE = 'sales-0.5-fresh-independent-2026-08-31-r6-gemini-groq'

def build() -> dict:
    if subprocess.check_output(['git','hash-object',str(BASE)], text=True).strip() != BASE_BLOB:
        raise RuntimeError('r1 prereg drift')
    if subprocess.check_output(['git','hash-object',str(DELTA)], text=True).strip() != DELTA_BLOB:
        raise RuntimeError('r6 prereg drift')
    base = json.loads(BASE.read_text())
    delta = json.loads(DELTA.read_text())
    if delta.get('cycle_id') != CYCLE:
        raise RuntimeError('r6 cycle mismatch')
    bind = delta.get('base_preregistration', {})
    if bind.get('path') != str(BASE.relative_to(ROOT)) or bind.get('blob') != BASE_BLOB:
        raise RuntimeError('r6 base binding mismatch')

    effective = deepcopy(base)
    effective['cycle_id'] = CYCLE
    effective['status'] = delta['status']
    effective['frozen_candidate'] = delta['frozen_candidate']
    effective['prior_cycle_evidence'] = delta['prior_sanitized_evidence']
    effective['authoring_transport_remediation'] = delta['authoring_transport_remediation']
    effective['provider_resilience_remediation'] = delta['provider_resilience_remediation']
    effective['execution_split_remediation'] = delta['execution_split_remediation']

    route = deepcopy(base['heldout_authoring'])
    route['hidden_reference_transport'] = delta['authoring_transport_remediation']['hidden_reference_normalization']
    route['json_string_normalization'] = delta['authoring_transport_remediation']['json_string_normalization']
    route['fresh_attempt_rule'] = delta['authoring_transport_remediation']['fresh_attempt_rule']
    route['safe_observability'] = delta['authoring_transport_remediation']['safe_observability']
    route['groq_429_retry'] = delta['provider_resilience_remediation']
    effective['heldout_authoring'] = route
    effective['sealed_transport_contract']['derivation_context'] = CYCLE
    effective['release_rule'] = delta['release_rule']
    return effective

def main() -> int:
    data = build()
    if len(sys.argv) == 2:
        Path(sys.argv[1]).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    else:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write('\n')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
