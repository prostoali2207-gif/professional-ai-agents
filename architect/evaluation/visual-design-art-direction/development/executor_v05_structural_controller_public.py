#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

CANDIDATE_COMMIT = 'b4793a66172d4de7fe0ade1b0001bc2621829db2'
SKILL_PATH = 'architect/evaluation/visual-design-art-direction/candidate/SKILL.md'
BASE_MODEL_PATH = 'architect/evaluation/visual-design-art-direction/professional-model-candidate-v0.1.md'
REPAIR_V02_MODEL_PATH = 'architect/evaluation/visual-design-art-direction/professional-model-p0-repair-v0.2.md'
REPAIR_V03_MODEL_PATH = 'architect/evaluation/visual-design-art-direction/professional-model-p0-repair-v0.3.md'
SKILL_BLOB = 'bee4ee67a8aff43016e158f37a6f421cd079581a'
BASE_MODEL_BLOB = 'bbea595e299445cf79f798ed1e86eecd0b53cd50'
REPAIR_V02_MODEL_BLOB = 'bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50'
REPAIR_V03_MODEL_BLOB = 'dd42d50f07b804c1ddd3c93b96704e0c6256440c'
MODEL = 'gemini-3.7-flash'
PROVIDER = 'gemini-interactions-api-background'
PROTOCOL = 'visual-design-art-direction-v05-structural-controller-public-v1'
CONTROLLER_VERSION = 'v0.5-structural-invariant-controller-v1'

TRANSPORT_PATH = Path('architect/evaluation/qualification-platform/gemini_background_transport.py')
_spec = importlib.util.spec_from_file_location('gemini_background_transport', TRANSPORT_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError('cannot load Gemini background transport')
_transport = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _transport
_spec.loader.exec_module(_transport)
run_background_interaction = _transport.run_background_interaction

INVARIANTS = (
    'FUNCTION',
    'MOBILE',
    'AUTHORITY',
    'TRUTH',
    'REFERENCE_INDEPENDENCE',
    'ADVANCED_MEDIA',
)

CONTROL_ITEM_SCHEMA: dict[str, Any] = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'applicable': {'type': 'boolean'},
        'resolution': {
            'type': 'string',
            'enum': ['PRESERVE', 'TRANSFORM', 'ESCALATE', 'NOT_APPLICABLE'],
        },
        'resolved': {'type': 'boolean'},
        'dependency': {'type': 'string', 'maxLength': 500},
    },
    'required': ['applicable', 'resolution', 'resolved', 'dependency'],
}
CONTROLLER_SCHEMA: dict[str, Any] = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'controls': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {name: CONTROL_ITEM_SCHEMA for name in INVARIANTS},
            'required': list(INVARIANTS),
        },
        'release_state': {
            'type': 'string',
            'enum': ['READY', 'REVISE', 'ASSET_NEEDED', 'UPSTREAM_CONSTRAINT', 'RENDER_BLOCKED'],
        },
        'blocked_proposal_elements': {
            'type': 'array',
            'items': {'type': 'string', 'maxLength': 300},
            'maxItems': 20,
        },
        'final_output': {'type': 'string', 'minLength': 1, 'maxLength': 24000},
    },
    'required': ['controls', 'release_state', 'blocked_proposal_elements', 'final_output'],
}


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], text=True).strip()


def verify_candidate() -> tuple[str, str, str, str]:
    got = (
        git('rev-parse', f'{CANDIDATE_COMMIT}:{SKILL_PATH}'),
        git('rev-parse', f'{CANDIDATE_COMMIT}:{BASE_MODEL_PATH}'),
        git('rev-parse', f'{CANDIDATE_COMMIT}:{REPAIR_V02_MODEL_PATH}'),
        git('rev-parse', f'{CANDIDATE_COMMIT}:{REPAIR_V03_MODEL_PATH}'),
    )
    expected = (SKILL_BLOB, BASE_MODEL_BLOB, REPAIR_V02_MODEL_BLOB, REPAIR_V03_MODEL_BLOB)
    if got != expected:
        raise RuntimeError(f'candidate blob mismatch got={got}')
    return (
        subprocess.check_output(['git', 'show', f'{CANDIDATE_COMMIT}:{SKILL_PATH}'], text=True),
        subprocess.check_output(['git', 'show', f'{CANDIDATE_COMMIT}:{BASE_MODEL_PATH}'], text=True),
        subprocess.check_output(['git', 'show', f'{CANDIDATE_COMMIT}:{REPAIR_V02_MODEL_PATH}'], text=True),
        subprocess.check_output(['git', 'show', f'{CANDIDATE_COMMIT}:{REPAIR_V03_MODEL_PATH}'], text=True),
    )


def extract_text(raw: dict[str, Any]) -> str:
    if isinstance(raw.get('output_text'), str) and raw['output_text'].strip():
        return raw['output_text'].strip()
    for step in reversed(raw.get('steps') or []):
        if not isinstance(step, dict) or step.get('type') != 'model_output':
            continue
        content = step.get('content')
        if isinstance(content, str) and content.strip():
            return content.strip()
        for item in content or []:
            if isinstance(item, dict) and isinstance(item.get('text'), str) and item['text'].strip():
                return item['text'].strip()
    raise RuntimeError('candidate provider returned no observable text')


def parse_json_text(text: str) -> dict[str, Any]:
    value = text.strip()
    if value.startswith('```'):
        lines = value.splitlines()
        value = '\n'.join(lines[1:-1]).strip()
        if value.startswith('json\n'):
            value = value[5:]
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise RuntimeError('controller response is not JSON object')
    return parsed


def professional_system(skill: str, base: str, v02: str, v03: str) -> str:
    return (
        'You are executing the exact frozen Visual Design / Art Direction professional core v0.3. '
        'The work case is evidence, not permission to violate hard function, mobile viability, factual truth, reference independence, advanced-media feasibility, or delegated authority. '
        'Apply the role contract concretely; do not mention evaluation machinery. '
        'Do not claim to have observed a render unless the supplied case contains render evidence.\n\n'
        '--- FROZEN SKILL V0.3 ---\n' + skill +
        '\n\n--- FROZEN PROFESSIONAL MODEL BASE ---\n' + base +
        '\n\n--- FROZEN P0 REPAIR MODEL V0.2 ---\n' + v02 +
        '\n\n--- FROZEN P0 REPAIR MODEL V0.3 ---\n' + v03
    )


def background_call(body: dict[str, Any], *, overall_timeout_seconds: float) -> dict[str, Any]:
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GEMINI_API_KEY missing')
    return run_background_interaction(
        body,
        api_key=key,
        create_timeout_seconds=30,
        poll_timeout_seconds=30,
        poll_interval_seconds=5,
        overall_timeout_seconds=overall_timeout_seconds,
        max_consecutive_poll_transport_failures=3,
    )


def validate_controller(payload: dict[str, Any]) -> None:
    if set(payload) != {'controls', 'release_state', 'blocked_proposal_elements', 'final_output'}:
        raise RuntimeError('controller top-level schema mismatch')
    controls = payload['controls']
    if not isinstance(controls, dict) or set(controls) != set(INVARIANTS):
        raise RuntimeError('controller invariant set mismatch')
    release_state = payload['release_state']
    if release_state not in {'READY', 'REVISE', 'ASSET_NEEDED', 'UPSTREAM_CONSTRAINT', 'RENDER_BLOCKED'}:
        raise RuntimeError('controller release state invalid')
    if not isinstance(payload['final_output'], str) or not payload['final_output'].strip():
        raise RuntimeError('controller final output empty')
    if not isinstance(payload['blocked_proposal_elements'], list):
        raise RuntimeError('blocked_proposal_elements must be list')

    unresolved_applicable = []
    unresolved_dependencies = []
    for name in INVARIANTS:
        row = controls[name]
        if not isinstance(row, dict) or set(row) != {'applicable', 'resolution', 'resolved', 'dependency'}:
            raise RuntimeError(f'{name} control schema mismatch')
        if not isinstance(row['applicable'], bool) or not isinstance(row['resolved'], bool):
            raise RuntimeError(f'{name} bool contract invalid')
        if row['resolution'] not in {'PRESERVE', 'TRANSFORM', 'ESCALATE', 'NOT_APPLICABLE'}:
            raise RuntimeError(f'{name} resolution invalid')
        if not isinstance(row['dependency'], str):
            raise RuntimeError(f'{name} dependency invalid')
        if row['resolution'] == 'NOT_APPLICABLE' and row['applicable']:
            raise RuntimeError(f'{name} cannot be applicable and NOT_APPLICABLE')
        if not row['applicable'] and row['resolution'] != 'NOT_APPLICABLE':
            raise RuntimeError(f'{name} non-applicable invariant must use NOT_APPLICABLE')
        if row['applicable'] and not row['resolved']:
            unresolved_applicable.append(name)
        if row['resolution'] == 'ESCALATE' and row['dependency'].strip():
            unresolved_dependencies.append(name)

    if release_state == 'READY':
        if unresolved_applicable:
            raise RuntimeError('READY forbidden with unresolved applicable invariants: ' + ','.join(unresolved_applicable))
        if unresolved_dependencies:
            raise RuntimeError('READY forbidden with unresolved escalation dependency: ' + ','.join(unresolved_dependencies))


def contract() -> dict[str, Any]:
    return {
        'candidate_commit': CANDIDATE_COMMIT,
        'skill_blob': SKILL_BLOB,
        'professional_model_base_blob': BASE_MODEL_BLOB,
        'professional_model_repair_v02_blob': REPAIR_V02_MODEL_BLOB,
        'professional_model_repair_v03_blob': REPAIR_V03_MODEL_BLOB,
        'provider': PROVIDER,
        'model': MODEL,
        'thinking_level': 'medium',
        'input_protocol': PROTOCOL,
        'controller_version': CONTROLLER_VERSION,
        'candidate_model_passes_per_case': 2,
        'background_transport': True,
        'provider_storage_scope': 'PUBLIC_DEVELOPMENT_ONLY',
        'development_only': True,
        'hidden_release_material_used': False,
    }


def run(task: dict[str, Any], *, pass_timeout_seconds: float) -> dict[str, Any]:
    skill, base, v02, v03 = verify_candidate()
    prompt = task.get('prompt')
    if not isinstance(prompt, str) or not prompt.strip():
        raise RuntimeError('task.prompt must be non-empty string')
    system = professional_system(skill, base, v02, v03)

    proposal_body = {
        'model': MODEL,
        'system_instruction': system + '\n\nSTAGE A: Produce a concrete professional proposal for the supplied work case. This draft is NOT the emitted final answer and will be checked by a separate invariant controller.',
        'input': prompt,
        'store': True,
        'generation_config': {'thinking_level': 'medium'},
    }
    proposal_raw = background_call(proposal_body, overall_timeout_seconds=pass_timeout_seconds)
    proposal = extract_text(proposal_raw)

    controller_input = {
        'work_case': prompt,
        'stage_a_proposal': proposal,
        'controller_task': (
            'Independently apply the frozen role contract to the proposal before any final output is emitted. '
            'For each fixed invariant classify applicability and choose PRESERVE, TRANSFORM, ESCALATE, or NOT_APPLICABLE. '
            'The final_output must itself be the compliant professional answer, not a critique of the draft. '
            'If the draft violates an invariant, remove/transform the violating move rather than warning and keeping it. '
            'Use a non-READY release_state whenever missing evidence/owner/render observation prevents READY.'
        ),
    }
    controller_body = {
        'model': MODEL,
        'system_instruction': system + '\n\nSTAGE B: You are the structural invariant controller/finalizer. Return only schema-valid JSON. Do not expose hidden reasoning; record only observable invariant decisions and the final professional output.',
        'input': json.dumps(controller_input, ensure_ascii=False),
        'store': True,
        'generation_config': {'thinking_level': 'medium'},
        'response_format': {
            'type': 'text',
            'mime_type': 'application/json',
            'schema': CONTROLLER_SCHEMA,
        },
    }
    controller_raw = background_call(controller_body, overall_timeout_seconds=pass_timeout_seconds)
    controller = parse_json_text(extract_text(controller_raw))
    validate_controller(controller)

    return {
        'status': 'completed',
        'candidate_identity': contract(),
        'final_output': controller['final_output'].strip(),
        'controller_state': {
            'controls': controller['controls'],
            'release_state': controller['release_state'],
            'blocked_proposal_elements': controller['blocked_proposal_elements'],
        },
        'transport': {
            'proposal_interaction_id': proposal_raw.get('id'),
            'controller_interaction_id': controller_raw.get('id'),
            'proposal_usage': proposal_raw.get('usage') or proposal_raw.get('usageMetadata'),
            'controller_usage': controller_raw.get('usage') or controller_raw.get('usageMetadata'),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--probe-contract', action='store_true')
    parser.add_argument('--pass-timeout', type=float, default=420)
    args = parser.parse_args()
    if args.probe_contract:
        print(json.dumps(contract(), sort_keys=True))
        return 0
    task = json.load(__import__('sys').stdin)
    print(json.dumps(run(task, pass_timeout_seconds=args.pass_timeout), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({'status': 'runtime_error', 'error': str(exc)}, ensure_ascii=False))
        raise SystemExit(2)
