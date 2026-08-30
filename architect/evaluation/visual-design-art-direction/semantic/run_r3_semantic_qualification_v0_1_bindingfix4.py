#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import json
import os
import urllib.request
from pathlib import Path

PREV = Path(__file__).with_name('run_r3_semantic_qualification_v0_1_bindingfix3.py')
spec = importlib.util.spec_from_file_location('visual_r3_semantic_bindingfix3', PREV)
if spec is None or spec.loader is None:
    raise RuntimeError('cannot load frozen binding-fix3 scorer')
fix3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fix3)
module = fix3.module

# Evaluator-infrastructure judge transport correction #4 only. Run 33299286470
# preserved one completed candidate response in the encrypted checkpoint, then
# stopped before any completed judgment because Gemini returned an object whose
# winner did not satisfy the already-frozen JUDGE_SCHEMA. Keep the exact judge
# model, prompt payload, thinking level, criteria, A/B ordering and validation;
# add only Gemini-native schema enforcement for the frozen JSON contract.
_original_judge = module.judge

def judge_with_gemini_schema(provider: str, model: str, case: dict, a: str, b: str) -> dict:
    if provider != 'gemini':
        return _original_judge(provider, model, case, a, b)
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GEMINI_API_KEY missing')
    payload = {
        'role': 'You are a blind calibrated senior landing-page art-direction assessor.',
        'brief': case['brief'],
        'context': case['context'],
        'constraints': case['constraints'],
        'professional_criteria': case['professional_criteria'],
        'p0_guardrail': case.get('p0_guardrail'),
        'relevant_dimensions': module.FAMILY_DIMENSIONS[case['family']],
        'output_A': a,
        'output_B': b,
        'task': 'Choose the professionally stronger output using the supplied criteria and relevant dimensions. Do not reward verbosity or generic polish. Separately flag p0 only when one output actually exhibits the supplied preregistered hard-fail behavior. Return JSON only.',
    }
    body = {
        'model': model,
        'system_instruction': 'Blind senior art-direction assessor. Return JSON only.',
        'input': json.dumps(payload, ensure_ascii=False),
        'store': False,
        'generation_config': {'thinking_level': 'medium'},
        'response_format': {
            'type': 'text',
            'mime_type': 'application/json',
            'schema': module.JUDGE_SCHEMA,
        },
    }
    req = urllib.request.Request(
        module.GEMINI,
        data=json.dumps(body, ensure_ascii=False).encode(),
        method='POST',
        headers={'x-goog-api-key': key, 'Content-Type': 'application/json'},
    )
    with module.http(req, 'Gemini judge', 180) as response:
        out = module.parse(module.gemini_text(json.loads(response.read().decode())))
    if out.get('winner') not in ('A', 'B'):
        raise RuntimeError('judge winner invalid')
    if bool(out.get('p0_triggered')) and out.get('p0_category') not in module.P0_CATEGORIES:
        raise RuntimeError('judge p0 invalid')
    if not out.get('p0_triggered') and out.get('p0_category') is not None:
        raise RuntimeError('judge p0 null contract invalid')
    return out

module.judge = judge_with_gemini_schema

if __name__ == '__main__':
    raise SystemExit(module.main())
