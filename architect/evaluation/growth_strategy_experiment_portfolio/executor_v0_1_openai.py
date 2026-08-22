#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess,sys,tempfile
CANDIDATE_COMMIT='1543bf774c795e33e3bedfd158491e4969806dfa'
CANDIDATE_DIGEST='sha256:721bb51c57a99ad31e7c282e1faedd3e99b48928753bd1cec69dfdfb5f847d0d'
CANDIDATE_BLOB='0f00c497a3be9e7601c3a007ebae4176f6b8ab40'
ADAPTER='architect/evaluation/harness/adapters/openai_frozen_artifact_adapter.py'
MODEL='gpt-5.4-mini'

def contract():
 return {'contract_version':1,'candidate_commit':CANDIDATE_COMMIT,'candidate_digest':CANDIDATE_DIGEST,'provider':'openai-responses-api','input_protocol':'growth-strategy-experiment-portfolio-candidate-v1','tool_protocol':'none-v1','state_protocol':'stateless-v1','observable_protocol':'final-output-only-v1'}

def run_task(task:str)->int:
 with tempfile.TemporaryDirectory() as td:
  payload={'protocol_version':2,'candidate_sha':CANDIDATE_BLOB,'workspace':td,'capability_profile':{},'input':{'task':task,'allowed_resources':[],'fixture_tools':{},'max_tool_rounds':0}}
  p=subprocess.run([sys.executable,ADAPTER],input=json.dumps(payload),text=True,capture_output=True)
  if p.stdout: print(p.stdout.strip())
  if p.returncode and p.stderr: print(p.stderr.strip(),file=sys.stderr)
  return p.returncode

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--qualification-contract',action='store_true');ap.add_argument('--canary',action='store_true');args=ap.parse_args()
 if args.qualification_contract: print(json.dumps(contract(),sort_keys=True)); return 0
 if args.canary: return run_task('Public unscored canary: views rose but downstream qualified-lead evidence is unavailable. Decide without inventing facts.')
 payload=json.load(sys.stdin); return run_task(str(payload['task']))
if __name__=='__main__': raise SystemExit(main())
