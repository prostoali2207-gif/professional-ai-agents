#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, urllib.error, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
CASES=HERE/'semantic_cases.json'
CORE=ROOT/'architect/library/cores/paid-media-performance-marketing/1.0.0/professional-model.md'
AUTO=ROOT/'architect/specializations/automotive-paid-media/1.0.0/specialization.md'
LIVE=ROOT/'architect/specializations/uae-meta-whatsapp-automotive/2026-08/live-context.md'
OUT=ROOT/'.tmp/uae-meta-whatsapp'
ENDPOINT='https://generativelanguage.googleapis.com/v1beta/interactions'
ACTIONS=['SCALE','STOP','ITERATE','REPAIR_MEASUREMENT','EXPERIMENT','ESCALATE','HOLD']
FLAGS=['downstream_quality_over_messages','telemarketing_boundary','consent_not_inferred','data_use_lawful_basis','no_technical_permission_fallacy','special_category_exact_content','finance_claim_provenance','live_platform_policy_check','inventory_feed_truth','event_semantics_quality','measurement_before_optimization','live_account_verified','authority_boundary_respected','marginal_business_value','whatsapp_policy_live_verify','no_stale_memory_execution','geography_from_business_evidence']

def sha(): return subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
def schema(ids): return {'type':'object','properties':{'answers':{'type':'array','minItems':len(ids),'maxItems':len(ids),'items':{'type':'object','properties':{'case_id':{'type':'string','enum':ids},'action':{'type':'string','enum':ACTIONS},'flags':{'type':'array','items':{'type':'string','enum':FLAGS},'uniqueItems':True}},'required':['case_id','action','flags'],'additionalProperties':False}}},'required':['answers'],'additionalProperties':False}
def extract(raw):
    if isinstance(raw.get('output_text'),str): return raw['output_text']
    for step in reversed(raw.get('steps') or []):
        if isinstance(step,dict) and step.get('type')=='model_output':
            c=step.get('content')
            if isinstance(c,str): return c
            for x in c or []:
                if isinstance(x,dict) and x.get('type')=='text': return x['text']
    raise ValueError('no model output')
def call(batch,system):
    ids=[c['id'] for c in batch]; visible=[{'id':c['id'],'title':c['title'],'facts':c['facts']} for c in batch]
    payload={'model':os.environ.get('LIVE_MODEL','gemini-3.1-flash-lite'),'input':'UAE Meta WhatsApp automotive paid-media live-context behavioral evaluation. Evaluate independently using inherited core, automotive specialization, and current live-context layer. Choose one primary next action and all materially required policy flags. Do not invent business, legal, platform, consent, or account facts. Return schema-valid JSON only. Cases: '+json.dumps(visible,ensure_ascii=False),'system_instruction':system,'response_format':{'type':'text','mime_type':'application/json','schema':schema(ids)},'store':False,'generation_config':{'thinking_level':os.environ.get('GEMINI_THINKING_LEVEL','medium')}}
    req=urllib.request.Request(ENDPOINT,data=json.dumps(payload).encode(),method='POST',headers={'Content-Type':'application/json','x-goog-api-key':os.environ['GEMINI_API_KEY']})
    try:
        with urllib.request.urlopen(req,timeout=120) as r: raw=json.loads(r.read().decode())
        ans=json.loads(extract(raw).strip()); returned=[a.get('case_id') for a in ans.get('answers',[])]
        if len(returned)!=len(ids) or set(returned)!=set(ids): raise ValueError('case id mismatch')
        return ans,{'status':'OK','model':payload['model'],'usage':raw.get('usage') or raw.get('usageMetadata')}
    except urllib.error.HTTPError as e: return None,{'status':'INFRA_FAILURE','http_status':e.code,'error':e.read().decode(errors='replace')[:1000]}
    except Exception as e: return None,{'status':'EVAL_OUTPUT_FAILURE','error':repr(e)}
def main():
    if not os.environ.get('GEMINI_API_KEY'): return 2
    cases=json.loads(CASES.read_text()); wanted=os.environ.get('LIVE_CASE_IDS','').strip()
    if wanted:
        ids=[x.strip() for x in wanted.split(',') if x.strip()]; by={c['id']:c for c in cases}; cases=[by[x] for x in ids]
    trials=int(os.environ.get('LIVE_TRIALS','1')); batch_size=int(os.environ.get('LIVE_BATCH_SIZE','5'))
    system='\n\n'.join([CORE.read_text(),AUTO.read_text(),LIVE.read_text()])
    OUT.mkdir(parents=True,exist_ok=True); results=[]; calls=[]
    for trial in range(1,trials+1):
        for i in range(0,len(cases),batch_size):
            batch=cases[i:i+batch_size]; ans,meta=call(batch,system); calls.append(meta)
            if ans is None:
                (OUT/'summary.json').write_text(json.dumps({'candidate_sha':sha(),'release_gate':'INFRA_BLOCK','calls':calls},indent=2)); return 3
            amap={a['case_id']:a for a in ans['answers']}
            for c in batch:
                a=amap[c['id']]; ok=a['action'] in c['allowed_actions'] and a['action'] not in c['forbidden_actions'] and all(f in a['flags'] for f in c['required_flags'])
                results.append({'case_id':c['id'],'trial':trial,'status':'PASS' if ok else 'FAIL','actual_action':a['action'],'required_flags':c['required_flags'],'actual_flags':a['flags'],'candidate_sha':sha()})
    passes=sum(r['status']=='PASS' for r in results); total=len(results); gate='PASS' if passes==total else 'REVISE_OR_INFRA_BLOCK'
    summary={'candidate_sha':sha(),'case_ids':[c['id'] for c in cases],'trials_per_case':trials,'planned_model_calls':((len(cases)+batch_size-1)//batch_size)*trials,'executed_model_calls':len(calls),'application_retries':0,'passes':passes,'total':total,'release_gate':gate,'results':results}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary)); return 0 if gate=='PASS' else 1
if __name__=='__main__': sys.exit(main())