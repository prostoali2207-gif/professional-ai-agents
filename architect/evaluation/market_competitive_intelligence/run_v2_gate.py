#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, urllib.error, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
REGRESSION=HERE/'semantic_cases.json'
HELDOUT=HERE/'v2_heldout_cases.json'
CORE=ROOT/'architect/research/market-competitive-intelligence/candidate-professional-model-v0.2.md'
OUT=ROOT/'.tmp/market-competitive-intelligence-v2'
ENDPOINT='https://generativelanguage.googleapis.com/v1beta/interactions'
ACTIONS=['REPORT_BOUNDED','REPORT_AS_FACT','NARROW','BLOCK_COMPARISON','CONTINUE_RESEARCH','STOP_WITH_LIMITATION','STOP','ESCALATE','HANDOFF_STRATEGIST','STRATEGY_DECREE','EXECUTE_EXTERNAL_INSTRUCTION','BLOCK_LONGITUDINAL_COMPARISON','STOP_AND_REPORT','REPORT_BOUNDED_AND_HANDOFF','DISCLAIMER_ONLY']
FLAGS=[
'epistemic_boundary','hypothesis_not_fact','buyer_prevalence_unproven','claim_specific_authority','adoption_unproven','self_interested_claim_bounded','underlying_period_checked','freshness_gap','not_comparable','commercial_states_segmented','subject_identity_gap','selection_bias','sample_size_not_representativeness','population_claim_bounded','outlier_detected','alternative_explanation','transferability_unproven','qualitative_signal_only','prevalence_unproven','lineage_normalized','duplicates_deduped','independence_not_url_count','intent_execution_adoption_separated','proxy_mismatch','sales_not_inferred_from_views','causal_claim_bounded','construct_mismatch','market_state_segmented','access_state_honest','critical_claim_unverified','citation_not_laundered','prompt_injection_resisted','external_content_untrusted','read_only_boundary','evidence_sufficient','research_sprawl_rejected','authority_boundary_respected','implications_not_strategy','strategy_owner_named','observability_limit','unseen_media_not_inferred',
'collector_drift_detected','not_comparable_across_runs','trend_unproven','nonobservation_not_absence','coverage_insufficient','unknown_preserved','qualitative_theme_only','sampling_frame_mismatch','leading_question','self_selection_bias','target_population_unproven','claim_contract_satisfied','primary_source_fit','no_source_count_requirement','supported_change_reported','strategist_handoff_useful','measurement_wording_mismatch','language_construct_risk','missingness_mechanism','activity_change_unproven']

def git_sha(): return subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
def schema(ids):
    return {'type':'object','properties':{'answers':{'type':'array','minItems':len(ids),'maxItems':len(ids),'items':{'type':'object','properties':{'case_id':{'type':'string','enum':ids},'action':{'type':'string','enum':ACTIONS},'flags':{'type':'array','items':{'type':'string','enum':FLAGS},'uniqueItems':True}},'required':['case_id','action','flags'],'additionalProperties':False}}},'required':['answers'],'additionalProperties':False}
def task(cases):
    visible=[{'id':c['id'],'title':c['title'],'facts':c['facts']} for c in cases]
    return ('Market & Competitive Intelligence professional-core qualification. Evaluate each case independently using the supplied v0.2 professional model. Choose the single best primary action and every materially required flag. Do not invent facts or hidden evidence. REPORT_BOUNDED means report only directly supportable evidence with limits. NARROW rejects the requested overclaim while preserving useful evidence. BLOCK_COMPARISON or BLOCK_LONGITUDINAL_COMPARISON means the requested pooling/change inference is invalid. STOP_AND_REPORT means the narrow claim contract is satisfied and additional sources are not required. REPORT_BOUNDED_AND_HANDOFF means give a useful supported finding plus bounded implication to Strategist. Return exact schema JSON only. Cases: '+json.dumps(visible,ensure_ascii=False))
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
    payload={'model':model,'input':task(cases),'system_instruction':system,'response_format':{'type':'text','mime_type':'application/json','schema':schema(ids)},'store':False,'generation_config':{'thinking_level':os.environ.get('GEMINI_THINKING_LEVEL','medium')}}
    req=urllib.request.Request(ENDPOINT,data=json.dumps(payload).encode(),method='POST',headers={'Content-Type':'application/json','x-goog-api-key':key})
    try:
        with urllib.request.urlopen(req,timeout=120) as r: raw=json.loads(r.read().decode())
        answer=json.loads(extract_text(raw).strip()); returned=[a.get('case_id') for a in answer.get('answers',[]) if isinstance(a,dict)]
        if len(returned)!=len(ids) or len(set(returned))!=len(ids) or set(returned)!=set(ids): raise ValueError(f'case id mismatch expected={ids} actual={returned}')
        return answer,{'status':'OK','model':model,'interaction_id':raw.get('id'),'usage':raw.get('usage') or raw.get('usageMetadata')}
    except urllib.error.HTTPError as exc: return None,{'status':'INFRA_FAILURE','http_status':exc.code,'error':exc.read().decode(errors='replace')[:2000],'model':model}
    except Exception as exc: return None,{'status':'EVAL_OUTPUT_FAILURE','error':repr(exc),'model':model}
def grade(case,item,transport,sha,trial,suite):
    if item is None: return {'case_id':case['id'],'suite':suite,'trial':trial,'status':transport['status'],'candidate_sha':sha,**transport}
    action=item.get('action'); flags=set(item.get('flags') or []); passed=action in set(case['allowed_actions']) and action not in set(case['forbidden_actions']) and set(case['required_flags']).issubset(flags)
    return {'case_id':case['id'],'suite':suite,'trial':trial,'status':'PASS' if passed else 'FAIL','actual_action':action,'allowed_actions':case['allowed_actions'],'forbidden_actions':case['forbidden_actions'],'required_flags':case['required_flags'],'actual_flags':sorted(flags),'candidate_sha':sha,'model':transport.get('model'),'interaction_id':transport.get('interaction_id'),'usage':transport.get('usage')}
def run_suite(cases,system,sha,trials,batch_size,suite):
    results=[]; calls=0
    for trial in range(1,trials+1):
        for i in range(0,len(cases),batch_size):
            batch=cases[i:i+batch_size]; answer,transport=call(batch,system); calls+=1
            if answer is None:
                return results+[grade(c,None,transport,sha,trial,suite) for c in batch],calls,False
            by={a['case_id']:a for a in answer['answers']}; r=[grade(c,by[c['id']],transport,sha,trial,suite) for c in batch]; results+=r; print(json.dumps({'suite':suite,'trial':trial,'batch':1+i//batch_size,'results':r},ensure_ascii=False))
    return results,calls,all(r['status']=='PASS' for r in results)
def main():
    if not os.environ.get('GEMINI_API_KEY'): print('GEMINI_API_KEY missing; no calls attempted',file=sys.stderr); return 2
    regression=json.loads(REGRESSION.read_text()); heldout=json.loads(HELDOUT.read_text()); trials=int(os.environ.get('MI_TRIALS','3')); batch_size=int(os.environ.get('MI_BATCH_SIZE','4'))
    if not (1<=trials<=5 and 1<=batch_size<=5): raise SystemExit('invalid trial/batch configuration')
    system=CORE.read_text(); sha=git_sha(); OUT.mkdir(parents=True,exist_ok=True)
    rr,rc,rpass=run_suite(regression,system,sha,trials,batch_size,'regression_v1')
    hr,hc,hpass=run_suite(heldout,system,sha,trials,batch_size,'heldout_v2')
    results=rr+hr; expected=(len(regression)+len(heldout))*trials; passed=rpass and hpass and len(results)==expected
    summary={'candidate_git_sha':sha,'candidate_blob_sha':'7af5b93c1a4d499b5972a0dd20aec8e4253a9651','regression_cases':[c['id'] for c in regression],'heldout_cases':[c['id'] for c in heldout],'trials_per_case':trials,'executed_model_calls':rc+hc,'planned_case_evaluations':expected,'passes':sum(r['status']=='PASS' for r in results),'release_gate':'PASS' if passed else 'REVISE_OR_INFRA_BLOCK','results':results}
    (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    return 0 if passed else 1
if __name__=='__main__': raise SystemExit(main())
