#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, random, subprocess, sys, time, urllib.error, urllib.request
from pathlib import Path
from cryptography.fernet import Fernet

ROOT=Path.cwd()
CYCLE='visual-design-art-direction-0.1.0-independent-2026-08-29-r3-semantic'
SCORE_CYCLE=CYCLE+'-scored-v1'
CANDIDATE_COMMIT='e8be839b02f181193afe076839c6ae94fb477a9b'
SKILL_BLOB='9d251d97a84e16ade91c8ced07425f9208f9f900'
MODEL_BLOB='bbea595e299445cf79f798ed1e86eecd0b53cd50'
SOURCE_RUN=33265201398
SOURCE_HEAD='af43f2d12187e1825c596239a7313fd8b7e5da63'
SOURCE_ARTIFACT_ID=9718569692
SOURCE_ARTIFACT_NAME='visual-design-art-direction-v0-1-encrypted-heldout-pack-r3'
SOURCE_ARTIFACT_DIGEST='sha256:04edc998022ae2ec524cec2e366c2644e46964c052030c5faddec320c7e94f1b'
SOURCE_CIPHERTEXT_SHA256='04edc998022ae2ec524cec2e366c2644e46964c052030c5faddec320c7e94f1b'
GENERAL_CALIBRATION_RUN=33262394565
R3_CALIBRATION_RUN=33266432530
R3_CALIBRATION_REPORT_SHA256='88c731996b0c262883ff9b1950235f875870741522e918b6851079a55212c3f7'
EXECUTOR='architect/evaluation/visual-design-art-direction/semantic/executor_r3_v0_1_gemini.py'
GEMINI='https://generativelanguage.googleapis.com/v1beta/interactions'
GROQ='https://api.groq.com/openai/v1/chat/completions'
JUDGES=[('gemini','gemini-3.5-flash-lite'),('groq','openai/gpt-oss-120b')]
THRESH={'per_judge_candidate_preference_rate_min':0.8,'combined_candidate_preference_rate_min':0.9,'max_pair_disagreement_rate':0.25}
P0_CATEGORIES={'FABRICATED_FACTUAL_PROOF','UNOBSERVED_RENDER_SUCCESS_CLAIM','REFERENCE_IMITATION_AS_SOLUTION','KEYWORD_ONLY_ADVANCED_MEDIA_ROUTING','SPECTACLE_BREAKS_HARD_FUNCTION_CONSTRAINT','UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE','ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE'}
FAMILY_DIMENSIONS={
 'FRAMING':['brief_appropriateness','function_clarity','authority_boundary_discipline'],
 'REFERENCE':['brief_appropriateness','reference_independence'],
 'DIVERGENCE':['brief_appropriateness','concept_distinctiveness','divergence_quality'],
 'CRAFT_JUDGMENT':['visual_craft_reasoning','function_clarity'],
 'MOBILE':['mobile_art_direction','function_clarity'],
 'TRUTH':['truth_evidence_integrity'],
 'CONTRACT':['brief_appropriateness','implementation_contract_usefulness','authority_boundary_discipline'],
 'CRITIQUE_REPAIR':['visual_craft_reasoning','critique_root_cause_quality','function_clarity'],
 'ADVANCED_MEDIA_ROUTING':['advanced_media_routing','mobile_art_direction','function_clarity'],
 'AUTHORITY_BOUNDARY':['brief_appropriateness','authority_boundary_discipline']
}
FAMILIES=list(FAMILY_DIMENSIONS)
JUDGE_SCHEMA={'type':'object','additionalProperties':False,'properties':{'winner':{'type':'string','enum':['A','B']},'p0_triggered':{'type':'boolean'},'p0_category':{'anyOf':[{'type':'string','enum':sorted(P0_CATEGORIES)},{'type':'null'}]}},'required':['winner','p0_triggered','p0_category']}
CHECKPOINT=Path('visual-r3-semantic-checkpoint.enc'); REPORT=Path('visual-r3-semantic-sanitized-report.json'); PROGRESS=Path('visual-r3-semantic-progress.json')
TRANSIENT_5XX_RETRIES=1; TRANSIENT_DELAY=15

def h(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def parse(t:str):
 t=t.strip()
 if t.startswith('```'):t='\n'.join(t.splitlines()[1:-1]).strip()
 return json.loads(t)
def gemini_text(raw:dict)->str:
 if isinstance(raw.get('output_text'),str):return raw['output_text']
 for step in reversed(raw.get('steps') or []):
  if isinstance(step,dict) and step.get('type')=='model_output':
   c=step.get('content')
   if isinstance(c,str):return c
   for x in c or []:
    if isinstance(x,dict) and isinstance(x.get('text'),str):return x['text']
 raise RuntimeError('Gemini judge returned no text')
def pace_groq():
 interval=float(os.environ.get('GROQ_MIN_INTERVAL_SECONDS','60')); marker=Path(os.environ.get('GROQ_PACE_FILE','/tmp/visual-r3-semantic-groq-pace'))
 if marker.exists():
  try:delay=interval-(time.time()-float(marker.read_text().strip()))
  except Exception:delay=0
  if delay>0:time.sleep(delay)
 marker.write_text(str(time.time()))
def http(req,provider,timeout,*,groq=False):
 for attempt in range(TRANSIENT_5XX_RETRIES+1):
  if groq:pace_groq()
  try:return urllib.request.urlopen(req,timeout=timeout)
  except urllib.error.HTTPError as exc:
   detail=exc.read().decode('utf-8','replace')[-1200:]
   if 500<=exc.code<600 and attempt<TRANSIENT_5XX_RETRIES:time.sleep(TRANSIENT_DELAY);continue
   raise RuntimeError(f'{provider} HTTP {exc.code}: {detail}') from None
def checkpoint_key()->bytes:
 master=os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY','').encode().strip()
 if not master:raise RuntimeError('QUALIFICATION_SEALED_PACK_MASTER_KEY missing')
 sys.path.insert(0,str(ROOT/'architect/evaluation/qualification-platform'))
 from sealed_pack_keys import derive_fernet_key
 return derive_fernet_key(master,SCORE_CYCLE)
def save_state(state:dict):CHECKPOINT.write_bytes(Fernet(checkpoint_key()).encrypt(json.dumps(state,ensure_ascii=False,sort_keys=True).encode()))
def load_state()->dict:
 if not CHECKPOINT.exists():return {'candidate':{},'judges':{}}
 return json.loads(Fernet(checkpoint_key()).decrypt(CHECKPOINT.read_bytes()))
def write_progress(status,state,failure=None):
 payload={'cycle_id':SCORE_CYCLE,'status':status,'candidate_calls':len(state['candidate']),'completed_judgments':len(state['judges']),'failure':failure,'hidden_content_printed':False}
 PROGRESS.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
def decrypt_cases()->list[dict]:
 base=Path(os.environ.get('R3_PACK_DIR','r3-source-pack')); manifest=json.load(open(base/'heldout-r3.manifest.json'))
 if manifest['cycle_id']!=CYCLE or manifest['candidate_commit']!=CANDIDATE_COMMIT or manifest['candidate_blobs']!={'skill':SKILL_BLOB,'professional_model':MODEL_BLOB}:raise RuntimeError('R3 manifest candidate/cycle mismatch')
 parts=base/'heldout-r3.parts'; token=''.join(p.read_text() for p in sorted(parts.iterdir())).encode()
 if h(token)!=SOURCE_CIPHERTEXT_SHA256 or manifest['ciphertext_sha256']!=SOURCE_CIPHERTEXT_SHA256:raise RuntimeError('R3 ciphertext digest mismatch')
 master=os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY','').encode().strip()
 if not master:raise RuntimeError('sealed master key missing')
 sys.path.insert(0,str(ROOT/'architect/evaluation/qualification-platform'));from sealed_pack_keys import derive_fernet_key
 payload=json.loads(Fernet(derive_fernet_key(master,CYCLE)).decrypt(token)); cases=payload.get('cases')
 if not isinstance(cases,list) or len(cases)!=20:raise RuntimeError('R3 case cardinality mismatch')
 fam={x.get('family') for x in cases}
 if fam!=set(FAMILIES) or any(sum(1 for x in cases if x.get('family')==f)!=2 for f in FAMILIES):raise RuntimeError('R3 family structure mismatch')
 return cases
def candidate_call(case:dict)->str:
 proc=subprocess.run(['python3',EXECUTOR,'--model-timeout','180'],input=json.dumps({k:case[k] for k in ('brief','context','constraints')},ensure_ascii=False),text=True,capture_output=True,timeout=240)
 if proc.returncode!=0:raise RuntimeError('candidate executor failure: '+proc.stdout[-800:]+proc.stderr[-400:])
 out=json.loads(proc.stdout); ident=out.get('candidate_identity') or {}
 if ident.get('candidate_commit')!=CANDIDATE_COMMIT or ident.get('skill_blob')!=SKILL_BLOB or ident.get('professional_model_blob')!=MODEL_BLOB:raise RuntimeError('candidate identity mismatch')
 text=out.get('final_output')
 if not isinstance(text,str) or not text.strip():raise RuntimeError('candidate observable output empty')
 return text
def judge(provider,model,case,a,b)->dict:
 payload={'role':'You are a blind calibrated senior landing-page art-direction assessor.','brief':case['brief'],'context':case['context'],'constraints':case['constraints'],'professional_criteria':case['professional_criteria'],'p0_guardrail':case.get('p0_guardrail'),'relevant_dimensions':FAMILY_DIMENSIONS[case['family']],'output_A':a,'output_B':b,'task':'Choose the professionally stronger output using the supplied criteria and relevant dimensions. Do not reward verbosity or generic polish. Separately flag p0 only when one output actually exhibits the supplied preregistered hard-fail behavior. Return JSON only.'}
 if provider=='gemini':
  key=os.environ.get('GEMINI_API_KEY','').strip()
  if not key:raise RuntimeError('GEMINI_API_KEY missing')
  body={'model':model,'system_instruction':'Blind senior art-direction assessor. Return JSON only.','input':json.dumps(payload,ensure_ascii=False),'store':False,'generation_config':{'thinking_level':'medium'}}
  req=urllib.request.Request(GEMINI,data=json.dumps(body,ensure_ascii=False).encode(),method='POST',headers={'x-goog-api-key':key,'Content-Type':'application/json'})
  with http(req,'Gemini judge',180) as r:out=parse(gemini_text(json.loads(r.read().decode())))
 else:
  key=os.environ.get('GROQ_API_KEY','').strip()
  if not key:raise RuntimeError('GROQ_API_KEY missing')
  body={'model':model,'messages':[{'role':'user','content':json.dumps(payload,ensure_ascii=False)}],'response_format':{'type':'json_schema','json_schema':{'name':'visual_r3_semantic_judgment','strict':True,'schema':JUDGE_SCHEMA}},'include_reasoning':False,'reasoning_effort':'medium','temperature':0}
  req=urllib.request.Request(GROQ,data=json.dumps(body,ensure_ascii=False).encode(),method='POST',headers={'Authorization':f'Bearer {key}','Content-Type':'application/json','Accept':'application/json','User-Agent':'visual-r3-semantic-judge/0.1'})
  with http(req,'Groq judge',180,groq=True) as r:out=parse(json.loads(r.read().decode())['choices'][0]['message']['content'])
 if out.get('winner') not in ('A','B'):raise RuntimeError('judge winner invalid')
 if bool(out.get('p0_triggered')) and out.get('p0_category') not in P0_CATEGORIES:raise RuntimeError('judge p0 invalid')
 if not out.get('p0_triggered') and out.get('p0_category') is not None:raise RuntimeError('judge p0 null contract invalid')
 return out
def metrics(cases,state):
 rows=[]
 for case in cases:
  cid=case['id']; swap=random.Random(f'{SCORE_CYCLE}:{cid}').choice([False,True]); cand=state['candidate'][cid]; baseline=case['competent_generic_baseline']; expected='B' if swap else 'A'; js={p:state['judges'][f'{cid}:{p}'] for p,_ in JUDGES}; rows.append((case,expected,js))
 n=len(rows); rates={p:sum(js[p]['winner']==expected for _,expected,js in rows)/n for p,_ in JUDGES}; combined=sum(js[p]['winner']==expected for _,expected,js in rows for p,_ in JUDGES)/(n*2); disagree=sum(js['gemini']['winner']!=js['groq']['winner'] for _,_,js in rows)/n
 dims={}
 for d in sorted({x for v in FAMILY_DIMENSIONS.values() for x in v}):
  subset=[r for r in rows if d in FAMILY_DIMENSIONS[r[0]['family']]]; dn=len(subset); dr={p:sum(js[p]['winner']==e for _,e,js in subset)/dn for p,_ in JUDGES}; dc=sum(js[p]['winner']==e for _,e,js in subset for p,_ in JUDGES)/(dn*2); dd=sum(js['gemini']['winner']!=js['groq']['winner'] for _,_,js in subset)/dn; dims[d]={'case_count':dn,'per_judge_candidate_preference_rate':dr,'combined_candidate_preference_rate':dc,'disagreement_rate':dd,'pass':all(x>=THRESH['per_judge_candidate_preference_rate_min'] for x in dr.values()) and dc>=THRESH['combined_candidate_preference_rate_min'] and dd<=THRESH['max_pair_disagreement_rate']}
 p0=[]; adjudication=[]
 for case,_,js in rows:
  flags=[(p,js[p].get('p0_category')) for p,_ in JUDGES if js[p].get('p0_triggered')]
  if len(flags)==2 and flags[0][1]==flags[1][1]:p0.append({'family':case['family'],'category':flags[0][1]})
  elif flags:adjudication.append({'family':case['family'],'judge_flag_count':len(flags)})
 overall=all(x>=THRESH['per_judge_candidate_preference_rate_min'] for x in rates.values()) and combined>=THRESH['combined_candidate_preference_rate_min'] and disagree<=THRESH['max_pair_disagreement_rate']
 return rates,combined,disagree,dims,p0,adjudication,overall
def main()->int:
 cases=decrypt_cases(); state=load_state(); write_progress('IN_PROGRESS',state)
 try:
  for case in cases:
   cid=case['id']
   if cid not in state['candidate']:
    state['candidate'][cid]=candidate_call(case);save_state(state);write_progress('IN_PROGRESS',state)
   swap=random.Random(f'{SCORE_CYCLE}:{cid}').choice([False,True]); baseline=case['competent_generic_baseline']; cand=state['candidate'][cid]; a,b=(baseline,cand) if swap else (cand,baseline)
   for provider,model in JUDGES:
    key=f'{cid}:{provider}'
    if key not in state['judges']:
     state['judges'][key]=judge(provider,model,case,a,b);save_state(state);write_progress('IN_PROGRESS',state)
  rates,combined,disagree,dims,p0,adj,overall=metrics(cases,state)
  if p0:status='SEMANTIC_FAIL_P0'
  elif adj:status='SEMANTIC_ADJUDICATION_REQUIRED'
  elif overall and all(x['pass'] for x in dims.values()):status='SEMANTIC_PASS'
  else:status='SEMANTIC_REVISE'
  report={'cycle_id':SCORE_CYCLE,'status':status,'candidate':{'commit':CANDIDATE_COMMIT,'skill_blob':SKILL_BLOB,'professional_model_blob':MODEL_BLOB,'runtime_model':'gemini-3.5-flash-lite'},'source_artifact':{'run_id':SOURCE_RUN,'artifact_id':SOURCE_ARTIFACT_ID,'artifact_name':SOURCE_ARTIFACT_NAME,'artifact_digest':SOURCE_ARTIFACT_DIGEST,'source_head_sha':SOURCE_HEAD},'calibration':{'general_run':GENERAL_CALIBRATION_RUN,'exact_r3_run':R3_CALIBRATION_RUN,'exact_r3_report_sha256':R3_CALIBRATION_REPORT_SHA256},'judges':dict(JUDGES),'thresholds':THRESH,'case_count':20,'candidate_calls':len(state['candidate']),'judge_calls':{p:sum(1 for k in state['judges'] if k.endswith(':'+p)) for p,_ in JUDGES},'per_judge_candidate_preference_rate':rates,'combined_candidate_preference_rate':combined,'pair_disagreement_rate':disagree,'dimension_outcomes':dims,'confirmed_p0_count':len(p0),'p0_categories':sorted({x['category'] for x in p0}),'adjudication_required_count':len(adj),'family_adjudication_counts':{f:sum(1 for x in adj if x['family']==f) for f in FAMILIES},'hidden_content_printed':False,'rendered_gate_required_after_semantic_pass':True,'rendered_tasks':['P1_DISCOVER','P2_DIRECT','P3_REFINE','P4_ADVANCED_MEDIA_PAIR']}
  REPORT.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');write_progress(status,state);print(json.dumps({'status':status,'candidate_calls':len(state['candidate']),'combined_candidate_preference_rate':combined,'pair_disagreement_rate':disagree,'confirmed_p0_count':len(p0),'adjudication_required_count':len(adj)},sort_keys=True))
  return 0 if status=='SEMANTIC_PASS' else (20 if status=='SEMANTIC_REVISE' else 21 if status=='SEMANTIC_FAIL_P0' else 22)
 except Exception as exc:
  save_state(state);write_progress('INFRASTRUCTURE_FAILURE',state,{'error':str(exc)[:600]});print(json.dumps({'status':'INFRASTRUCTURE_FAILURE','candidate_calls':len(state['candidate']),'error':str(exc)[:600]}));return 30
if __name__=='__main__':raise SystemExit(main())
