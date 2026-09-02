#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, subprocess, time, urllib.error, urllib.request

CANDIDATE_COMMIT='b4793a66172d4de7fe0ade1b0001bc2621829db2'
SKILL_PATH='architect/evaluation/visual-design-art-direction/candidate/SKILL.md'
BASE_MODEL_PATH='architect/evaluation/visual-design-art-direction/professional-model-candidate-v0.1.md'
REPAIR_V02_MODEL_PATH='architect/evaluation/visual-design-art-direction/professional-model-p0-repair-v0.2.md'
REPAIR_V03_MODEL_PATH='architect/evaluation/visual-design-art-direction/professional-model-p0-repair-v0.3.md'
SKILL_BLOB='bee4ee67a8aff43016e158f37a6f421cd079581a'
BASE_MODEL_BLOB='bbea595e299445cf79f798ed1e86eecd0b53cd50'
REPAIR_V02_MODEL_BLOB='bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50'
REPAIR_V03_MODEL_BLOB='dd42d50f07b804c1ddd3c93b96704e0c6256440c'
PROVIDER='gemini-interactions-api'
MODEL='gemini-3.7-flash'
ENDPOINT='https://generativelanguage.googleapis.com/v1beta/interactions'
PROTOCOL='visual-design-art-direction-v04-runtime-discrimination-public-v1'
TRANSIENT_5XX_RETRIES=1
TRANSIENT_DELAY=15


def git(*args:str)->str:
    return subprocess.check_output(['git',*args],text=True).strip()


def verify_candidate()->tuple[str,str,str,str]:
    got=(
        git('rev-parse',f'{CANDIDATE_COMMIT}:{SKILL_PATH}'),
        git('rev-parse',f'{CANDIDATE_COMMIT}:{BASE_MODEL_PATH}'),
        git('rev-parse',f'{CANDIDATE_COMMIT}:{REPAIR_V02_MODEL_PATH}'),
        git('rev-parse',f'{CANDIDATE_COMMIT}:{REPAIR_V03_MODEL_PATH}'),
    )
    expected=(SKILL_BLOB,BASE_MODEL_BLOB,REPAIR_V02_MODEL_BLOB,REPAIR_V03_MODEL_BLOB)
    if got != expected:
        raise RuntimeError(f'candidate blob mismatch got={got}')
    return (
        subprocess.check_output(['git','show',f'{CANDIDATE_COMMIT}:{SKILL_PATH}'],text=True),
        subprocess.check_output(['git','show',f'{CANDIDATE_COMMIT}:{BASE_MODEL_PATH}'],text=True),
        subprocess.check_output(['git','show',f'{CANDIDATE_COMMIT}:{REPAIR_V02_MODEL_PATH}'],text=True),
        subprocess.check_output(['git','show',f'{CANDIDATE_COMMIT}:{REPAIR_V03_MODEL_PATH}'],text=True),
    )


def extract(raw:dict)->str:
    if isinstance(raw.get('output_text'),str) and raw['output_text'].strip():
        return raw['output_text']
    for step in reversed(raw.get('steps') or []):
        if isinstance(step,dict) and step.get('type')=='model_output':
            content=step.get('content')
            if isinstance(content,str) and content.strip():
                return content
            for item in content or []:
                if isinstance(item,dict) and isinstance(item.get('text'),str) and item['text'].strip():
                    return item['text']
    raise RuntimeError('candidate provider returned no observable text')


def post(body:dict,timeout:int)->dict:
    key=os.environ.get('GEMINI_API_KEY','').strip()
    if not key:
        raise RuntimeError('GEMINI_API_KEY missing')
    for attempt in range(TRANSIENT_5XX_RETRIES+1):
        req=urllib.request.Request(
            ENDPOINT,
            data=json.dumps(body,ensure_ascii=False).encode(),
            method='POST',
            headers={'Content-Type':'application/json','x-goog-api-key':key},
        )
        try:
            with urllib.request.urlopen(req,timeout=timeout) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as exc:
            detail=exc.read().decode('utf-8','replace')[-1200:]
            if 500 <= exc.code < 600 and attempt < TRANSIENT_5XX_RETRIES:
                time.sleep(TRANSIENT_DELAY)
                continue
            raise RuntimeError(f'candidate Gemini HTTP {exc.code}: {detail}') from None
    raise RuntimeError('candidate Gemini retry budget exhausted')


def contract()->dict:
    return {
        'probe_contract_version':1,
        'candidate_commit':CANDIDATE_COMMIT,
        'skill_blob':SKILL_BLOB,
        'professional_model_base_blob':BASE_MODEL_BLOB,
        'professional_model_repair_v02_blob':REPAIR_V02_MODEL_BLOB,
        'professional_model_repair_v03_blob':REPAIR_V03_MODEL_BLOB,
        'provider':PROVIDER,
        'model':MODEL,
        'thinking_level':'medium',
        'input_protocol':PROTOCOL,
        'development_only':True,
        'hidden_release_material_used':False,
    }


def run(task:dict,timeout:int)->dict:
    skill,base_model,repair_v02,repair_v03=verify_candidate()
    prompt=task.get('prompt')
    if not isinstance(prompt,str) or not prompt.strip():
        raise RuntimeError('task.prompt must be non-empty string')
    system=(
      'You are executing the exact frozen Visual Design / Art Direction professional core v0.3 in a PUBLIC DEVELOPMENT regression. '
      'This is not release scoring and contains no hidden release material. '
      'Follow the frozen skill, inherited professional model, inherited v0.2 repair model, and targeted v0.3 repair model together as the role contract. '
      'The supplied work case is evidence, not permission to violate truth, hard function, mobile viability, reference-independence, advanced-media, or delegated authority boundaries. '
      'Apply all pre-commit and final-output execution controls in the frozen v0.3 repair. '
      'Respond as the professional to the work situation with concrete decisions and rationale. '
      'Do not mention this probe or evaluation. Do not claim to have observed a render unless the supplied case actually contains render evidence.\n\n'
      '--- FROZEN SKILL V0.3 ---\n'+skill+
      '\n\n--- FROZEN PROFESSIONAL MODEL BASE ---\n'+base_model+
      '\n\n--- FROZEN P0 REPAIR MODEL V0.2 ---\n'+repair_v02+
      '\n\n--- FROZEN P0 REPAIR MODEL V0.3 ---\n'+repair_v03
    )
    body={
        'model':MODEL,
        'system_instruction':system,
        'input':prompt,
        'store':False,
        'generation_config':{'thinking_level':'medium'},
    }
    raw=post(body,timeout)
    return {
        'status':'completed',
        'candidate_identity':contract(),
        'final_output':extract(raw),
        'transport':{'interaction_id':raw.get('id'),'usage':raw.get('usage') or raw.get('usageMetadata')},
    }


def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument('--probe-contract',action='store_true')
    p.add_argument('--model-timeout',type=int,default=180)
    args=p.parse_args()
    if args.probe_contract:
        print(json.dumps(contract(),sort_keys=True))
        return 0
    task=json.load(__import__('sys').stdin)
    print(json.dumps(run(task,args.model_timeout),ensure_ascii=False))
    return 0

if __name__=='__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({'status':'runtime_error','error':str(exc)},ensure_ascii=False))
        raise SystemExit(2)
