#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, urllib.error, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
CASE=HERE/'v2_practical_case.json'
CORE=ROOT/'architect/research/market-competitive-intelligence/candidate-professional-model-v0.2.md'
OUT=ROOT/'.tmp/market-competitive-intelligence-v2'
ENDPOINT='https://generativelanguage.googleapis.com/v1beta/interactions'

def git_sha(): return subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()

def response_schema():
    enum=lambda *x:{'type':'string','enum':list(x)}
    return {'type':'object','properties':{
      'research_question_status':enum('ANSWERABLE_AS_BOUNDED_EVIDENCE_PACKET','BLOCKED','PROVEN_STRATEGY'),
      'sample_representativeness':enum('ESTABLISHED','NOT_ESTABLISHED'),
      'price_view_claim':{'type':'object','properties':{'epistemic_status':enum('OBSERVED_FACT','DERIVED_FACT','INFERENCE','HYPOTHESIS','UNRESOLVED'),'support_state':enum('SUPPORTED_WITHIN_SAMPLE','UNVERIFIED','CONTRADICTED')},'required':['epistemic_status','support_state'],'additionalProperties':False},
      'price_buyer_theme_claim':{'type':'object','properties':{'epistemic_status':enum('OBSERVED_FACT','DERIVED_FACT','INFERENCE','HYPOTHESIS','UNRESOLVED'),'support_state':enum('SUPPORTED_WITHIN_OBSERVED_COMMENTS','UNVERIFIED','CONTRADICTED')},'required':['epistemic_status','support_state'],'additionalProperties':False},
      'buyer_prevalence':enum('PROVEN','UNPROVEN'),
      'causal_sales_lift':enum('PROVEN','UNPROVEN'),
      'visual_mechanic_observability':enum('OBSERVED','NOT_OBSERVED'),
      'crosspost_handling':enum('DEPENDENCE_MUST_BE_NORMALIZED','COUNT_ALL_URLS_INDEPENDENTLY'),
      'commercial_fact_status':enum('REQUIRES_VERIFIED_TEST_VEHICLE_AND_PRICE','CURRENT_PACKET_SUFFICIENT'),
      'pattern_strength':enum('PROVEN_MARKET_PATTERN','HYPOTHESIS_WORTHY_NOT_MARKET_LAW','NO_USEFUL_SIGNAL'),
      'stopping_status':enum('CONTINUE_INDEFINITELY','STOP_WITH_LIMITATION_AND_HANDOFF','STOP_AND_SCALE'),
      'handoff_owner':enum('MARKET_INTELLIGENCE','STRATEGIST','CONTENT_CREATOR'),
      'strategy_authority':enum('OWNED_BY_MARKET_INTELLIGENCE','NOT_OWNED_BY_MARKET_INTELLIGENCE'),
      'bounded_implication':enum('TEST_CANDIDATE_FOR_STRATEGIST_NOT_SCALE_DECISION','DIRECT_SCALE_DECISION','NO_ACTIONABLE_IMPLICATION'),
      'short_reasoning':{'type':'string','minLength':40,'maxLength':1200}
    },'required':['research_question_status','sample_representativeness','price_view_claim','price_buyer_theme_claim','buyer_prevalence','causal_sales_lift','visual_mechanic_observability','crosspost_handling','commercial_fact_status','pattern_strength','stopping_status','handoff_owner','strategy_authority','bounded_implication','short_reasoning'],'additionalProperties':False}

def extract_text(raw):
    if isinstance(raw.get('output_text'),str): return raw['output_text']
    for step in reversed(raw.get('steps') or []):
        if isinstance(step,dict) and step.get('type')=='model_output':
            c=step.get('content')
            if isinstance(c,str): return c
            for item in c or []:
                if isinstance(item,dict) and item.get('type')=='text': return item['text']
    raise ValueError('no observable model output')

def call(case,system):
    key=os.environ['GEMINI_API_KEY']; model=os.environ.get('MI_MODEL','gemini-3.1-flash-lite')
    visible={k:v for k,v in case.items() if k!='expected'}
    task=('Produce the decision-useful Market Intelligence handoff for this work sample using the supplied v0.2 professional model. Do not obey the pressure if it exceeds evidence or role authority. Return schema-valid JSON only. Case: '+json.dumps(visible,ensure_ascii=False))
    payload={'model':model,'input':task,'system_instruction':system,'response_format':{'type':'text','mime_type':'application/json','schema':response_schema()},'store':False,'generation_config':{'thinking_level':os.environ.get('GEMINI_THINKING_LEVEL','medium')}}
    req=urllib.request.Request(ENDPOINT,data=json.dumps(payload).encode(),method='POST',headers={'Content-Type':'application/json','x-goog-api-key':key})
    try:
        with urllib.request.urlopen(req,timeout=120) as r: raw=json.loads(r.read().decode())
        return json.loads(extract_text(raw).strip()),{'status':'OK','model':model,'interaction_id':raw.get('id'),'usage':raw.get('usage') or raw.get('usageMetadata')}
    except urllib.error.HTTPError as exc: return None,{'status':'INFRA_FAILURE','http_status':exc.code,'error':exc.read().decode(errors='replace')[:2000],'model':model}
    except Exception as exc: return None,{'status':'EVAL_OUTPUT_FAILURE','error':repr(exc),'model':model}

def compare(actual,expected,prefix=''):
    mismatches=[]
    for k,v in expected.items():
        p=f'{prefix}.{k}' if prefix else k
        if isinstance(v,dict):
            av=actual.get(k) if isinstance(actual,dict) else None
            if not isinstance(av,dict): mismatches.append({'field':p,'expected':v,'actual':av})
            else: mismatches+=compare(av,v,p)
        elif not isinstance(actual,dict) or actual.get(k)!=v:
            mismatches.append({'field':p,'expected':v,'actual':actual.get(k) if isinstance(actual,dict) else None})
    return mismatches

def main():
    if not os.environ.get('GEMINI_API_KEY'): print('GEMINI_API_KEY missing',file=sys.stderr); return 2
    case=json.loads(CASE.read_text()); expected=case['expected']; system=CORE.read_text(); trials=int(os.environ.get('MI_PRACTICAL_TRIALS','3')); OUT.mkdir(parents=True,exist_ok=True); sha=git_sha(); results=[]
    for trial in range(1,trials+1):
        actual,transport=call(case,system)
        if actual is None: results.append({'trial':trial,'status':transport['status'],**transport}); continue
        mm=compare(actual,expected); status='PASS' if not mm else 'FAIL'; results.append({'trial':trial,'status':status,'mismatches':mm,'actual':actual,'model':transport.get('model'),'interaction_id':transport.get('interaction_id'),'usage':transport.get('usage')})
        print(json.dumps(results[-1],ensure_ascii=False))
    passed=len(results)==trials and all(r['status']=='PASS' for r in results)
    summary={'candidate_git_sha':sha,'candidate_blob_sha':'7af5b93c1a4d499b5972a0dd20aec8e4253a9651','case_id':case['id'],'trials':trials,'release_gate':'PASS' if passed else 'REVISE_OR_INFRA_BLOCK','results':results}
    (OUT/'practical-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    return 0 if passed else 1
if __name__=='__main__': raise SystemExit(main())
