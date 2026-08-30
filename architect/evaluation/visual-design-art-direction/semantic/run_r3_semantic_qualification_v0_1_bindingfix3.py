#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import json
from pathlib import Path

PREV = Path(__file__).with_name('run_r3_semantic_qualification_v0_1_bindingfix2.py')
spec = importlib.util.spec_from_file_location('visual_r3_semantic_bindingfix2', PREV)
if spec is None or spec.loader is None:
    raise RuntimeError('cannot load frozen binding-fix2 scorer')
fix2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fix2)
module = fix2.fix1.module

# Evaluator-infrastructure input adapter correction #3 only. Run 33298985005
# stopped before the first scored candidate call because R3 authoring intentionally
# emits constraints as array[string], while the already-frozen candidate executor
# contract accepts brief/context/constraints strings. Preserve every constraint
# exactly by canonical JSON serialization before invoking the unchanged executor.
_original_candidate_call = module.candidate_call

def candidate_call_with_constraints_adapter(case: dict) -> str:
    constraints = case.get('constraints')
    if not isinstance(constraints, list) or not constraints or not all(isinstance(x, str) and x for x in constraints):
        raise RuntimeError('R3 constraints adapter requires non-empty array[string]')
    encoded = json.dumps(constraints, ensure_ascii=False, separators=(',', ':'))
    if json.loads(encoded) != constraints:
        raise RuntimeError('R3 constraints adapter round-trip mismatch')
    adapted = dict(case)
    adapted['constraints'] = encoded
    return _original_candidate_call(adapted)

module.candidate_call = candidate_call_with_constraints_adapter

if __name__ == '__main__':
    raise SystemExit(module.main())
