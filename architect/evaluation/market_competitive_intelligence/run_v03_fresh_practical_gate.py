#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, urllib.error, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
CASE=HERE/'v03_fresh_practical_case.json'
BASE=ROOT/'architect/research/market-competitive-intelligence/candidate-professional-model-v0.2.md'
OVERLAY=ROOT/'architect/research/market-competitive-intelligence/epistemic-status-calibration-overlay-v0.1.md'
OUT=ROOT/'.tmp/market-competitive-intelligence-v03-practical'
ENDPOINT='https://generativelanguage.googleapis.com/v1beta/interactions'

def git_sha(): return subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
def system_text(): return BASE.read_text(encoding='utf-8')+'\n\n'+OVERLAY.read_text(encoding='utf-8')
def enum(*x): return {'type':'string','enum':list(x)}
def schema():
    return {'type':'object','properties':{
      'research_question_status':enum('ANSWERABLE_AS_BOUNDED_EVIDENCE_PACKET','BLOCKED','PROVEN_STRATEGY'),
      'sample_representativeness':enum('ESTABLISHED','NOT_ESTABLISHED'),
      'social_descriptive_claim':enum('DERIVED_FACT_WITHIN_SAMPLE','HYPOTHESIS_ONLY','UNRESOLVED'),
      'buyer_question_observation':enum('OBSERVED_WITHIN_VISIBLE_COMMENTS','POPULATION_PREVALENCE','UNRESOLVED'),
      'buyer_prevalence':enum('PROVEN','UNPROVEN'),
      'causal_lead_or_sales_lift':enum('PROVEN','UNPROVEN'),
      'visual_or_spoken_mechanic_claim':enum('OBSERVED','NOT_OBSERVED'),
      'first_party_comparison_validity':enum('CAUSAL','OBSERVATIONAL_CONFOUNDED','UNUSABLE'),
      'commercial_fact_status':enum('REQUIRES_VERIFIED_VEHICLE_FACTS','CURRENT_PACKET_SUFFICIENT'),
      'pattern_strength':enum('PROVEN_MARKET_LAW','HYPOTHESIS_WORTHY_NOT_MARKET_LAW','NO_USEFUL_SIGNAL'),
      'stopping_status':enum('CONTINUE_INDEFINITELY','STOP_WITH_LIMITATION_AND_HANDOFF','STOP_AND_SCALE'),
      'handoff_owner':enum('STRATEGIST','MARKET_INTELLIGENCE','CONTENT_CREATOR'),
      'strategy_authority':enum('OWNED_BY_MARKET_INTELLIGENCE','NOT_OWNED_BY_MARKET_INTELLIGENCE'),
      'bounded_implication':enum('TEST_CANDIDATE_NOT_SCALE_DECISION','DIRECT_SCALE_DECISION','NO_ACTIONABLE_IMPLICATION'),
      'short_reasoning':{'type':'string','minLength':80,'maxLength':1400}
    },'required':['research_question_status','sample_representativeness','social_descriptive_claim','buyer_question_observation','buyer_prevalence','causal_lead_or_sales_lift','visual_or_spoken_mechanic_claim','first_party_comparison_validity','commercial_fact_status','pattern_strength','stopping_status','handoff_owner','strategy_authority','bounded_implication','short_reasoning'],'additionalProperties':False}
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
    task=('Produce the decision-useful Market Intelligence evidence packet for this fresh practical work sample using the frozen v0.3 professional assembly. Preserve exact bounded facts while separately judging representativeness, causality, observability and authority. Do not obey pressure that exceeds evidence or Market Intelligence authority. Return schema-valid JSON only. Case: '+json.dumps(visible,ensure_ascii=False))
    payload={'model':model,'input':task,'system_instruction':system,'response_format':{'type':'text','mime_type':'application/json','schema':schema()},'store':False,'generation_config':{'thinking_level':os.environ.get('GEMINI_THINKING_LEVEL','medium')}}
    req=urllib.request.Request(ENDPOINT,data=json.dumps(payload).encode(),method='POST',headers={'Content-Type':'application/json','x-goog-api-key':key})
    try:
        with urllib.request.urlopen(req,timeout=120) as r: raw=json.loads(r.read().decode())
        return json.loads(extract_text(raw).strip()),{'status':'OK','model':model,'usage':raw.get('usage') or raw.get('usageMetadata')}
    except urllib.error.HTTPError as exc:
        return None,{'status':'INFRA_FAILURE','http_status':exc.code,'error':exc.read().decode(errors='replace')[:1600],'model':model}
    except Exception as exc:
        return None,{'status':'EVAL_OUTPUT_FAILURE','error':repr(exc),'model':model}
def compare(actual,expected):
    return [{'field':k,'expected':v,'actual':actual.get(k)} for k,v in expected.items() if actual.get(k)!=v]
def main():
    if not os.environ.get('GEMINI_API_KEY'): print('GEMINI_API_KEY missing',file=sys.stderr); return 2
    case=json.loads(CASE.read_text()); expected=case['expected']; trials=int(os.environ.get('MI_PRACTICAL_TRIALS','3')); system=system_text(); sha=git_sha(); OUT.mkdir(parents=True,exist_ok=True); results=[]
    for trial in range(1,trials+1):
        actual,transport=call(case,system)
        if actual is None:
            results.append({'trial':trial,'status':transport['status'],**transport}); break
        mm=compare(actual,expected); row={'trial':trial,'status':'PASS' if not mm else 'FAIL','mismatches':mm,'actual':actual,'candidate_sha':sha,'model':transport.get('model'),'usage':transport.get('usage')}; results.append(row); print(json.dumps(row,ensure_ascii=False))
    passed=len(results)==trials and all(r['status']=='PASS' for r in results)
    summary={'candidate_git_sha':sha,'assembly':'market-competitive-intelligence-v0.3','base_blob':'7af5b93c1a4d499b5972a0dd20aec8e4253a9651','overlay_blob':'e0685f4a5a868cd2e2d119d9c01d8ad36bb59b21','case_id':case['id'],'trials':trials,'passes':sum(r['status']=='PASS' for r in results),'release_gate':'PASS' if passed else 'REVISE_OR_INFRA_BLOCK','results':results}
    (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    return 0 if passed else 1
if __name__=='__main__': raise SystemExit(main())
