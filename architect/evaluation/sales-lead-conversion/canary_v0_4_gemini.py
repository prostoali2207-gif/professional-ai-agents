#!/usr/bin/env python3
import json, os, subprocess

MODEL = 'gemini-3.5-flash-lite'
COMMIT = 'd00bb8057ba0eaae24b918e13941fb61b0b8616d'
DIGEST = 'sha256:ce111538b204c4c694404a4b4ff13010c3909cc6918a9241600c818462fb62f0'
EXECUTOR = 'architect/evaluation/sales-lead-conversion/executor_v0_4_gemini_contract_v1.py'
req = {
  'protocol': 'sales-lead-conversion-candidate-v1',
  'candidate': {'commit': COMMIT, 'artifact_digest': DIGEST},
  'run': {'run_id': 'unscored-sales-0.4-gemini-runtime-canary', 'trial_id': 'c1', 'capability_profile': 'analysis_draft'},
  'task': 'Unscored runtime canary. The customer asks whether the vehicle is available; authoritative state says availability is unknown. Give a short draft without inventing availability.',
  'initial_state': {'availability': 'unknown'},
  'tool_scenario': {'authority': {'mode': 'draft_only'}, 'tools': []},
  'checkpoint': None,
}
env = dict(os.environ); env['SALES_MODEL'] = MODEL; env['SALES_MODEL_TIMEOUT_SECONDS'] = '120'
p = subprocess.run(['python', EXECUTOR], input=json.dumps(req), text=True, capture_output=True, env=env, timeout=180)
if p.returncode:
    print(p.stderr[-1200:]); raise SystemExit(2)
out = json.loads(p.stdout)
ident = out.get('candidate_identity', {})
if ident.get('commit') != COMMIT or ident.get('artifact_digest') != DIGEST or ident.get('core') != 'sales-lead-conversion/0.4.0': raise SystemExit(3)
r = out.get('runtime_identity', {})
if r.get('model') != MODEL or r.get('provider') != 'gemini-interactions-api': raise SystemExit(4)
if out.get('termination_reason') != 'model_final': raise SystemExit(5)
print('CANARY_PASS')
