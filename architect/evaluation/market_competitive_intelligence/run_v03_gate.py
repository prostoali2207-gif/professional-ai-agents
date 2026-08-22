#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, urllib.error, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
CASES=HERE/'v03_fresh_cases.json'
BASE=ROOT/'architect/research/market-competitive-intelligence/candidate-professional-model-v0.2.md'
OVERLAY=ROOT/'architect/research/market-competitive-intelligence/epistemic-status-calibration-overlay-v0.1.md'
OUT=ROOT/'.tmp/market-competitive-intelligence-v03'
ENDPOINT='https://generativelanguage.googleapis.com/v1beta/interactions'

def git_sha():
    return subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()

def system_text():
    return BASE.read_text(encoding='utf-8')+'\n\n'+OVERLAY.read_text(encoding='utf-8')

def enum(*x): return {'type':'string','enum':list(x)}
def response_schema(ids):
    return {'type':'object','properties':{'answers':{'type':'array','minItems':len(ids),'maxItems':len(ids),'items':{'type':'object','properties':{
      'case_id':{'type':'string','enum':ids},
      'bounded_claim_status':enum('OBSERVED_FACT','DERIVED_FACT','INFERENCE','HYPOTHESIS','UNRESOLVED'),
      'population_generalization':enum('SUPPORTED','UNPROVEN','NOT_APPLICABLE'),
      'causal_claim':enum('SUPPORTED','UNPROVEN','NOT_APPLICABLE'),
      'comparability':enum('VALID_WITHIN_SAMPLE','LIMITED_BY_CONFOUNDING','NOT_COMPARABLE'),
      'strategy_owner':enum('STRATEGIST','MARKET_INTELLIGENCE')
    },'required':['case_id','bounded_claim_status','population_generalization','causal_claim','comparability','strategy_owner'],'additionalProperties':False}}},'required':['answers'],'additionalProperties':False}

def task(cases):
    visible=[{k:v for k,v in c.items() if k!='expected'} for c in cases]
    return ('Fresh held-out qualification for frozen Market & Competitive Intelligence v0.3 base-plus-overlay assembly. Classify the exact bounded claim separately from population transport, causal validity, comparability and strategy authority. Do not downgrade a true within-sample observation merely because external validity is weak. Do not broaden a bounded fact into a population or causal claim. Return exactly one schema-valid answer per case. Cases: '+json.dumps(visible,ensure_ascii=False))

def extract_text(raw):
    if isinstance(raw.get('output_text'),str): return raw['output_text']
    for step in reversed(raw.get('steps') or []):
        if isinstance(step,dict) and step.get('type')=='model_output':
            c=step.get('content')
            if isinstance(c,str): return c
            for item in c or []:
                if isinstance(item,dict) and item.get('type')=='text': return item['text']
    raise ValueError('no observable model output')

def call(cases,system):
    key=os.environ['GEMINI_API_KEY']; model=os.environ.get('MI_MODEL','gemini-3.1-flash-lite'); ids=[c['id'] for c in cases]
    payload={'model':model,'input':task(cases),'system_instruction':system,'response_format':{'type':'text','mime_type':'application/json','schema':response_schema(ids)},'store':False,'generation_config':{'thinking_level':os.environ.get('GEMINI_THINKING_LEVEL','medium')}}
    req=urllib.request.Request(ENDPOINT,data=json.dumps(payload).encode(),method='POST',headers={'Content-Type':'application/json','x-goog-api-key':key})
    try:
        with urllib.request.urlopen(req,timeout=120) as r: raw=json.loads(r.read().decode())
        answer=json.loads(extract_text(raw).strip()); returned=[x.get('case_id') for x in answer.get('answers',[]) if isinstance(x,dict)]
        if len(returned)!=len(ids) or len(set(returned))!=len(ids) or set(returned)!=set(ids): raise ValueError(f'case id mismatch expected={ids} actual={returned}')
        return answer,{'status':'OK','model':model,'usage':raw.get('usage') or raw.get('usageMetadata')}
    except urllib.error.HTTPError as exc:
        return None,{'status':'INFRA_FAILURE','http_status':exc.code,'error':exc.read().decode(errors='replace')[:2000],'model':model}
    except Exception as exc:
        return None,{'status':'EVAL_OUTPUT_FAILURE','error':repr(exc),'model':model}

def grade(case,item,transport,sha,trial):
    if item is None: return {'case_id':case['id'],'trial':trial,'status':transport['status'],'candidate_sha':sha,**transport}
    expected=case['expected']; actual={k:item.get(k) for k in expected}; mismatches=[{'field':k,'expected':v,'actual':actual.get(k)} for k,v in expected.items() if actual.get(k)!=v]
    return {'case_id':case['id'],'trial':trial,'status':'PASS' if not mismatches else 'FAIL','mismatches':mismatches,'actual':actual,'candidate_sha':sha,'model':transport.get('model'),'usage':transport.get('usage')}

def main():
    if not os.environ.get('GEMINI_API_KEY'): print('GEMINI_API_KEY missing',file=sys.stderr); return 2
    cases=json.loads(CASES.read_text()); trials=int(os.environ.get('MI_TRIALS','3')); system=system_text(); sha=git_sha(); OUT.mkdir(parents=True,exist_ok=True); results=[]
    for trial in range(1,trials+1):
        answer,transport=call(cases,system)
        if answer is None:
            results += [grade(c,None,transport,sha,trial) for c in cases]; break
        by={x['case_id']:x for x in answer['answers']}; r=[grade(c,by[c['id']],transport,sha,trial) for c in cases]; results+=r; print(json.dumps({'trial':trial,'results':r},ensure_ascii=False))
    expected_n=len(cases)*trials; passed=len(results)==expected_n and all(r['status']=='PASS' for r in results)
    summary={'candidate_git_sha':sha,'assembly':'market-competitive-intelligence-v0.3','base_blob':'7af5b93c1a4d499b5972a0dd20aec8e4253a9651','overlay_blob':'e0685f4a5a868cd2e2d119d9c01d8ad36bb59b21','case_ids':[c['id'] for c in cases],'trials':trials,'planned_case_evaluations':expected_n,'passes':sum(r['status']=='PASS' for r in results),'release_gate':'PASS' if passed else 'REVISE_OR_INFRA_BLOCK','results':results}
    (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    return 0 if passed else 1

if __name__=='__main__': raise SystemExit(main())
