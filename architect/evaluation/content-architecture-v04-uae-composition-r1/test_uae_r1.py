#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('uae_runner',HERE/'run_uae_r1.py')
mod=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(mod)

case={
  'expected_decisions':{
    'X':{'disposition':'OMIT','public_use':False,'allowed_basis':['UNVERIFIED']},
    'Y':{'disposition':'ALLOW','public_use':True,'allowed_basis':['VERIFIED_BUSINESS_FACT']},
  },
  'expected_locks':['L1']
}
base={
  'status':'READY_WITH_BOUNDS',
  'decision_results':[
    {'decision_id':'X','disposition':'OMIT','public_use':False,'basis':'UNVERIFIED','note':'x'},
    {'decision_id':'Y','disposition':'ALLOW','public_use':True,'basis':'VERIFIED_BUSINESS_FACT','note':'y'},
  ],
  'lock_results':[{'lock_id':'L1','preserved':True,'note':'kept'}],
  'architecture':{'attention_job':'job','block_sequence':[],'proof_requirements':[],'pacing_intent':'macro'},
  'creator_handoff':{'must_preserve':[],'may_choose':[],'blocked_portions':[],'must_escalate':[]},
  'boundary_notes':[]
}
assert mod.mechanical_case(case,base)['pass'] is True
bad={**base,'decision_results':[
    {'decision_id':'X','disposition':'ALLOW','public_use':True,'basis':'UNVERIFIED','note':'bad'},
    {'decision_id':'Y','disposition':'ALLOW','public_use':True,'basis':'VERIFIED_BUSINESS_FACT','note':'y'},
]}
r=mod.mechanical_case(case,bad)
assert r['pass'] is False and r['hard_failures']
over={**base,'status':'BLOCKED'}
assert mod.mechanical_case(case,over)['pass'] is False
assert mod.validate_assessment({'hard_failures':[],'scores':{'commercial_truth':3},'release_recommendation':'PASS'},['commercial_truth'])==[]
assert mod.validate_assessment({'hard_failures':[],'scores':{'commercial_truth':4},'release_recommendation':'PASS'},['commercial_truth'])
print('uae composition deterministic tests: PASS')
