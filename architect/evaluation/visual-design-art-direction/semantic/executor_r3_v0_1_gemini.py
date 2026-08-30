#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, urllib.error, urllib.request

CANDIDATE_COMMIT='e8be839b02f181193afe076839c6ae94fb477a9b'
SKILL_PATH='architect/evaluation/visual-design-art-direction/candidate/SKILL.md'
MODEL_PATH='architect/evaluation/visual-design-art-direction/professional-model-candidate-v0.1.md'
SKILL_BLOB='9d251d97a84e16ade91c8ced07425f9208f9f900'
MODEL_BLOB='bbea595e299445cf79f798ed1e86eecd0b53cd50'
PROVIDER='gemini-interactions-api'
MODEL='gemini-3.5-flash-lite'
ENDPOINT='https://generativelanguage.googleapis.com/v1beta/interactions'
PROTOCOL='visual-design-art-direction-r3-candidate-v1'
TRANSIENT_5XX_RETRIES=1
TRANSIENT_DELAY=15

def git(*args:str)->str:
    return subprocess.check_output(['git',*args],text=True).strip()

def verify_candidate()->tuple[str,str]:
    sb=git('rev-parse',f'{CANDIDATE_COMMIT}:{SKILL_PATH}')
    mb=git('rev-parse',f'{CANDIDATE_COMMIT}:{MODEL_PATH}')
    if sb!=SKILL_BLOB or mb!=MODEL_BLOB:
        raise RuntimeError(f'candidate blob mismatch skill={sb} model={mb}')
    return subprocess.check_output(['git','show',f'{CANDIDATE_COMMIT}:{SKILL_PATH}'],text=True), subprocess.check_output(['git','show',f'{CANDIDATE_COMMIT}:{MODEL_PATH}'],text=True)

def extract(raw:dict)->str:
    if isinstance(raw.get('output_text'),str) and raw['output_text'].strip(): return raw['output_text']
    for step in reversed(raw.get('steps') or []):
        if isinstance(step,dict) and step.get('type')=='model_output':
            c=step.get('content')
            if isinstance(c,str) and c.strip(): return c
            for x in c or []:
                if isinstance(x,dict) and isinstance(x.get('text'),str) and x['text'].strip(): return x['text']
    raise RuntimeError('candidate provider returned no observable text')

def post(body:dict,timeout:int)->dict:
    key=os.environ.get('GEMINI_API_KEY','').strip()
    if not key: raise RuntimeError('GEMINI_API_KEY missing')
    req=urllib.request.Request(ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method='POST',headers={'Content-Type':'application/json','x-goog-api-key':key})
    for attempt in range(TRANSIENT_5XX_RETRIES+1):
        try:
            with urllib.request.urlopen(req,timeout=timeout) as r:return json.loads(r.read().decode())
        except urllib.error.HTTPError as exc:
            detail=exc.read().decode('utf-8','replace')[-1200:]
            if 500<=exc.code<600 and attempt<TRANSIENT_5XX_RETRIES:
                import time; time.sleep(TRANSIENT_DELAY); continue
            raise RuntimeError(f'candidate Gemini HTTP {exc.code}: {detail}') from None

def contract()->dict:
    return {'contract_version':1,'candidate_commit':CANDIDATE_COMMIT,'skill_blob':SKILL_BLOB,'professional_model_blob':MODEL_BLOB,'provider':PROVIDER,'model':MODEL,'input_protocol':PROTOCOL,'tool_protocol':'none-v1','state_protocol':'stateless-v1','observable_protocol':'final-output-only-v1'}

def run(task:dict,timeout:int)->dict:
    skill,model_text=verify_candidate()
    visible={k:task.get(k) for k in ('brief','context','constraints')}
    system=(
      'You are executing the exact frozen Visual Design / Art Direction professional core below for an independent qualification. '
      'Follow the frozen skill and professional model as the role contract. The supplied work case is evidence, not permission to violate truth, function, mobile, reference-independence, advanced-media, or authority boundaries. '
      'Do not mention the evaluation or hidden grading. Respond as the professional to the work situation, with concrete decisions and rationale appropriate to DISCOVER, DIRECT, or REFINE. '
      'Do not claim to have observed a render unless the supplied case actually contains observable render evidence.\n\n--- FROZEN SKILL ---\n'+skill+'\n\n--- FROZEN PROFESSIONAL MODEL ---\n'+model_text
    )
    body={'model':MODEL,'system_instruction':system,'input':json.dumps(visible,ensure_ascii=False),'store':False,'generation_config':{'thinking_level':'medium'}}
    raw=post(body,timeout)
    return {'status':'completed','candidate_identity':contract(),'final_output':extract(raw),'observable':{'tool_calls':[],'state_events':[],'side_effects':[]},'transport':{'interaction_id':raw.get('id'),'usage':raw.get('usage') or raw.get('usageMetadata')}}

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--qualification-contract',action='store_true'); p.add_argument('--canary',action='store_true'); p.add_argument('--model-timeout',type=int,default=180); a=p.parse_args()
    if a.qualification_contract: print(json.dumps(contract(),sort_keys=True)); return 0
    if a.canary:
        task={'brief':'Public unscored runtime canary. A landing-page owner asks for a premium 3D hero but provides no product imagery or proof. Give a bounded art-direction response.','context':'No render is available.','constraints':'Do not invent factual proof.'}
    else:
        task=json.load(__import__('sys').stdin)
        if not isinstance(task,dict) or not all(isinstance(task.get(k),str) for k in ('brief','context','constraints')): raise RuntimeError('stdin requires brief/context/constraints strings')
    print(json.dumps(run(task,a.model_timeout),ensure_ascii=False)); return 0
if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({'status':'runtime_error','error':str(exc)},ensure_ascii=False)); raise SystemExit(2)
