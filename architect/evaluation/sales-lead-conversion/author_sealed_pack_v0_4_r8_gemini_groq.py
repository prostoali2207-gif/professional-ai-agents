#!/usr/bin/env python3
from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
from typing import Any

ROOT = Path.cwd()
R6_AUTHOR = ROOT / 'architect/evaluation/sales-lead-conversion/author_sealed_pack_v0_4_r6_gemini_groq.py'
R6_AUTHOR_BLOB = '555a4a3e3df2c2e7d94dd5165478b26f90b04a08'
R6_PREREG = ROOT / 'architect/evaluation/sales-lead-conversion/qualification-preregistration-v0_4-r6-gemini-groq.json'
R6_PREREG_BLOB = '65d826075ded39ab9e465bfaf0a7bb3a254d15f9'
PREREG = ROOT / 'architect/evaluation/sales-lead-conversion/qualification-preregistration-v0_4-r8-gemini-groq.json'
OUT_ROOT = ROOT / 'architect/evaluation/sales-lead-conversion/sealed/runtime-sales-0.4-r8-author'
CYCLE = 'sales-0.4-fresh-independent-2026-08-30-r8-gemini-groq'
COMMIT = 'd00bb8057ba0eaae24b918e13941fb61b0b8616d'
DIGEST = 'sha256:ce111538b204c4c694404a4b4ff13010c3909cc6918a9241600c818462fb62f0'
REASONS = [
    'schema_top_level','schema_cardinality','schema_case_type','schema_text_fields',
    'initial_state_json_parse','initial_state_json_type',
    'tool_scenario_json_parse','tool_scenario_json_type','tool_scenario_shape',
    'checkpoint_json_parse','checkpoint_json_type',
    'hidden_reference_json_parse','hidden_reference_json_type','professional_disposition',
    'rubric_cardinality','rubric_item','hard_fail_enum','boundary_expectation','alternative_interpretation_check',
]
STRUCTURAL: dict[str, list[str]] = {}


def load_r6():
    actual = subprocess.check_output(['git','hash-object',str(R6_AUTHOR)], text=True).strip()
    if actual != R6_AUTHOR_BLOB:
        raise RuntimeError(f'r6 author drift: {actual}')
    spec = importlib.util.spec_from_file_location('sales_v04_r8_r6', R6_AUTHOR)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load pinned r6 author')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def reject(group_key: str, code: str):
    if code not in REASONS:
        code = 'schema_text_fields'
    STRUCTURAL.setdefault(group_key, []).append(code)
    raise ValueError(code)


def decode_object(value: Any, group_key: str, parse_code: str, type_code: str):
    if not isinstance(value, str):
        reject(group_key, parse_code)
    try:
        parsed = json.loads(value)
    except Exception:
        reject(group_key, parse_code)
    if not isinstance(parsed, dict):
        reject(group_key, type_code)
    return parsed


def diagnostic_validate(group, raw, slots, repeat_slots, attempt, r5):
    group_key = '/'.join(group)
    if not isinstance(raw, dict):
        reject(group_key, 'schema_top_level')
    semantic_cases = raw.get('cases')
    positions = r5.ordered_slots(group, slots)
    if not isinstance(semantic_cases, list) or len(semantic_cases) != len(positions):
        reject(group_key, 'schema_cardinality')
    bound = []
    for (family, slot), semantic in zip(positions, semantic_cases, strict=True):
        if not isinstance(semantic, dict):
            reject(group_key, 'schema_case_type')
        task = semantic.get('task'); capability = semantic.get('capability_profile')
        if not isinstance(task, str) or not task.strip() or not isinstance(capability, str) or not capability.strip():
            reject(group_key, 'schema_text_fields')
        initial_state = decode_object(semantic.get('initial_state_json'), group_key, 'initial_state_json_parse', 'initial_state_json_type')
        tool_scenario = decode_object(semantic.get('tool_scenario_json'), group_key, 'tool_scenario_json_parse', 'tool_scenario_json_type')
        if not isinstance(tool_scenario.get('authority'), dict) or not isinstance(tool_scenario.get('tools'), list):
            reject(group_key, 'tool_scenario_shape')
        checkpoint_raw = semantic.get('checkpoint_json')
        if not isinstance(checkpoint_raw, str):
            reject(group_key, 'checkpoint_json_parse')
        try:
            checkpoint = json.loads(checkpoint_raw)
        except Exception:
            reject(group_key, 'checkpoint_json_parse')
        if checkpoint is not None and not isinstance(checkpoint, dict):
            reject(group_key, 'checkpoint_json_type')
        hidden_raw = semantic.get('hidden_reference_json')
        if not isinstance(hidden_raw, str):
            reject(group_key, 'hidden_reference_json_parse')
        try:
            ref = json.loads(hidden_raw)
        except Exception:
            reject(group_key, 'hidden_reference_json_parse')
        if not isinstance(ref, dict):
            reject(group_key, 'hidden_reference_json_type')
        disposition = ref.get('professional_disposition')
        rubric = ref.get('rubric')
        hard = ref.get('critical_hard_fail_triggers')
        boundary = ref.get('boundary_expectation')
        alternative = ref.get('alternative_interpretation_check')
        if not isinstance(disposition, str) or not disposition.strip():
            reject(group_key, 'professional_disposition')
        if not isinstance(rubric, list) or len(rubric) != 3:
            reject(group_key, 'rubric_cardinality')
        for item in rubric:
            if not isinstance(item, dict) or not all(isinstance(item.get(k), str) and item[k].strip() for k in ('name','pass_evidence','material_failure')):
                reject(group_key, 'rubric_item')
        if not isinstance(hard, list) or any(item not in r5.ALLOWED_HARD_FAILS for item in hard):
            reject(group_key, 'hard_fail_enum')
        if not isinstance(boundary, str) or not boundary.strip():
            reject(group_key, 'boundary_expectation')
        if not isinstance(alternative, str) or not alternative.strip():
            reject(group_key, 'alternative_interpretation_check')
        bound.append({
            'id': f'R8-{family}-{slot}-A{attempt}', 'family': family, 'slot': slot,
            'repeat_required': (family, slot) in repeat_slots, 'task': task,
            'initial_state': initial_state, 'capability_profile': capability,
            'tool_scenario': tool_scenario, 'checkpoint': checkpoint,
            'hidden_reference': {
                'professional_disposition': disposition, 'rubric': rubric,
                'critical_hard_fail_triggers': hard, 'boundary_expectation': boundary,
                'alternative_interpretation_check': alternative,
            },
        })
    return bound


def merged_prereg() -> Path:
    actual = subprocess.check_output(['git','hash-object',str(R6_PREREG)], text=True).strip()
    if actual != R6_PREREG_BLOB:
        raise RuntimeError(f'r6 prereg drift: {actual}')
    base = json.loads(R6_PREREG.read_text())
    current = json.loads(PREREG.read_text())
    if current.get('construct_inheritance', {}).get('base_preregistration_blob') != R6_PREREG_BLOB:
        raise RuntimeError('r8 inheritance blob mismatch')
    merged = deepcopy(base)
    merged['cycle_id'] = CYCLE
    merged['status'] = current['status']
    merged['frozen_candidate'] = current['frozen_candidate']
    merged['prior_cycle_evidence'] = dict(base.get('prior_cycle_evidence') or {}) | dict(current['prior_cycle_evidence'])
    merged['scope'] = current['scope']; merged['fixture_count'] = current['fixture_count']; merged['per_family'] = current['per_family']
    merged['thresholds'] = current['thresholds']
    route = deepcopy(base['heldout_authoring'])
    route['safe_structural_reason_codes'] = current['heldout_authoring']['safe_structural_reason_codes']
    route['native_schema_rule'] = current['heldout_authoring']['native_schema_rule']
    route['safe_observability'] = current['heldout_authoring']['safe_observability']
    merged['heldout_authoring'] = route
    merged['sealed_transport_contract']['derivation_context'] = CYCLE
    merged['release_rule'] = current['release_rule']
    path = Path('/tmp/sales-v04-r8-merged-prereg.json')
    path.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + '\n')
    return path


def main() -> int:
    current = json.loads(PREREG.read_text())
    if current.get('cycle_id') != CYCLE or current.get('frozen_candidate', {}).get('commit') != COMMIT or current.get('frozen_candidate', {}).get('artifact_digest') != DIGEST:
        raise RuntimeError('r8 frozen binding mismatch')
    if current.get('prior_cycle_evidence', {}).get('r7_run_id') != 33300320053 or current.get('prior_cycle_evidence', {}).get('candidate_calls') != 0:
        raise RuntimeError('r8 prior-cycle binding mismatch')
    if current.get('heldout_authoring', {}).get('safe_structural_reason_codes') != REASONS:
        raise RuntimeError('r8 reason-code drift')
    r6 = load_r6(); r5 = r6.load_r5(); temp = merged_prereg()
    original_validate = r6.validate_and_bind
    try:
        r6.PREREG = temp; r6.OUT_ROOT = OUT_ROOT; r6.CYCLE = CYCLE
        r6.validate_and_bind = lambda group, raw, slots, repeat_slots, attempt, r5_arg: diagnostic_validate(group, raw, slots, repeat_slots, attempt, r5_arg)
        captured = io.StringIO()
        with redirect_stdout(captured):
            rc = int(r6.main())
    finally:
        r6.validate_and_bind = original_validate
        try: temp.unlink()
        except FileNotFoundError: pass
    for line in captured.getvalue().splitlines():
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                status = obj.get('status')
                if isinstance(status, str): obj['status'] = status.replace('R6','R8').replace('r6','r8')
                if obj.get('candidate_calls') == 0 or str(obj.get('status','')).startswith('NOT_EXECUTABLE'):
                    obj['structural_reason_codes'] = STRUCTURAL
            print(json.dumps(obj, sort_keys=True))
        except Exception:
            print(line)
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
