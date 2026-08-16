#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, urllib.error, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
CASES=HERE/'semantic_cases.json'
CORE=ROOT/'architect/library/cores/paid-media-performance-marketing/1.0.0/professional-model.md'
SPEC=ROOT/'architect/specializations/automotive-paid-media/1.0.0/specialization.md'
OUT=ROOT/'.tmp/automotive-paid-media'
ENDPOINT='https://generativelanguage.googleapis.com/v1beta/interactions'
ACTIONS=['SCALE','STOP','ITERATE','REPAIR_MEASUREMENT','EXPERIMENT','ESCALATE','HOLD']
FLAGS=['inventory_truth_checked','availability_over_proxy','downstream_sale_quality','business_value_over_proxy','crm_identity_stitching','measurement_validity_first','inventory_portfolio_economics','no_fabricated_business_facts','opportunity_cost_considered','merchandising_truth','claim_risk_escalated','sales_ops_dependency','fault_tree_used','offer_claim_provenance','authority_boundary_respected','marginal_not_average']

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
    payload={'model':os.environ.get('AUTO_MODEL','gemini-3.1-flash-lite'),'input':'Automotive paid-media specialization behavioral evaluation. Evaluate each case independently using the inherited core plus automotive specialization. Choose one primary next action and all materially required policy flags. Do not invent business facts. Return schema-valid JSON only. Cases: '+json.dumps(visible,ensure_ascii=False),'system_instruction':system,'response_format':{'type':'text','mime_type':'application/json','schema':schema(ids)},'store':False,'generation_config':{'thinking_level':os.environ.get('GEMINI_THINKING_LEVEL','medium')}}
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
    cases=json.loads(CASES.read_text()); wanted=os.environ.get('AUTO_CASE_IDS','').strip()
    if wanted:
        ids=[x.strip() for x in wanted.split(',') if x.strip()]; by={c['id']:c for c in cases}; cases=[by[x] for x in ids]
    trials=int(os.environ.get('AUTO_TRIALS','1')); batch_size=int(os.environ.get('AUTO_BATCH_SIZE','5'))
    batches=[cases[i:i+batch_size] for i in range(0,len(cases),batch_size)]
    system=CORE.read_text()+"\n\n--- AUTOMOTIVE SPECIALIZATION ---\n"+SPEC.read_text(); OUT.mkdir(parents=True,exist_ok=True)
    results=[]; calls=0; candidate=sha()
    for t in range(1,trials+1):
        for b in batches:
            ans,transport=call(b,system); calls+=1
            if ans is None:
                results += [{'case_id':c['id'],'trial':t,'status':transport['status'],'candidate_sha':candidate,**transport} for c in b]; break
            by={a['case_id']:a for a in ans['answers']}
            for c in b:
                a=by[c['id']]; flags=set(a['flags']); ok=a['action'] in c['allowed_actions'] and a['action'] not in c['forbidden_actions'] and set(c['required_flags']).issubset(flags)
                results.append({'case_id':c['id'],'trial':t,'status':'PASS' if ok else 'FAIL','actual_action':a['action'],'required_flags':c['required_flags'],'actual_flags':sorted(flags),'candidate_sha':candidate})
    planned=len(cases)*trials; passed=len(results)==planned and all(r['status']=='PASS' for r in results)
    summary={'candidate_sha':candidate,'case_ids':[c['id'] for c in cases],'trials_per_case':trials,'planned_model_calls':len(batches)*trials,'executed_model_calls':calls,'application_retries':0,'passes':sum(r['status']=='PASS' for r in results),'release_gate':'PASS' if passed else 'REVISE_OR_INFRA_BLOCK','results':results}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)); print(json.dumps(summary,ensure_ascii=False)); return 0 if passed else 1
if __name__=='__main__': raise SystemExit(main())
