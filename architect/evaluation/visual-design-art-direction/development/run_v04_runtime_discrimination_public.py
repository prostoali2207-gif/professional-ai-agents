#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, time, urllib.error, urllib.request
from pathlib import Path
from typing import Any

ROOT=Path.cwd()
FIXTURES=ROOT/'architect/evaluation/visual-design-art-direction/fixtures-v0.3-targeted-regression.json'
EXECUTOR='architect/evaluation/visual-design-art-direction/development/executor_v03_gemini37_public_probe.py'
SELECTED=(
    'R30_MOBILE_PRECOMMIT_CONTROL',
    'R31_TRUTH_PROOF_OUTPUT_CONTROL',
    'R32_REFERENCE_INDEPENDENCE_CONTROL',
    'R33_AUTHORITY_PRECOMMIT_CONTROL',
    'R34_WARNING_ONLY_COMPLIANCE_TRAP',
    'R39_BOLD_REFERENCE_ADVANCED_MEDIA_NONREGRESSION',
)
GEMINI_MODEL='gemini-3.5-flash-lite'
GROQ_MODEL='openai/gpt-oss-120b'
GEMINI='https://generativelanguage.googleapis.com/v1beta/interactions'
GROQ=os.environ.get('GROQ_BASE_URL','https://api.groq.com/openai/v1').rstrip('/')+'/chat/completions'
TRANSIENT_5XX_RETRIES=1
TRANSIENT_RETRY_DELAY_SECONDS=15
REPORT=Path('visual-v04-runtime-discrimination-public-report.json')
DETAILS=Path('visual-v04-runtime-discrimination-public-details.json')
PROGRESS=Path('visual-v04-runtime-discrimination-public-progress.json')
JUDGE_SCHEMA={
    'type':'object',
    'additionalProperties':False,
    'properties':{
        'pass':{'type':'boolean'},
        'failure_type':{'type':'string','enum':['PASS','MISSING_REQUIRED_BEHAVIOR','FORBIDDEN_BEHAVIOR','AMBIGUOUS_OUTPUT']},
        'must_not_observe_triggered':{'type':'boolean'},
        'missing_required_count':{'type':'integer','minimum':0,'maximum':10},
        'concise_reason':{'type':'string','minLength':1,'maxLength':500},
    },
    'required':['pass','failure_type','must_not_observe_triggered','missing_required_count','concise_reason'],
}


def parse(text:str)->Any:
    value=text.strip()
    if value.startswith('```'):
        lines=value.splitlines()
        value='\n'.join(lines[1:-1]).strip()
        if value.startswith('json\n'):
            value=value[5:]
    return json.loads(value)


def gemini_text(payload:dict)->str:
    if isinstance(payload.get('output_text'),str) and payload['output_text'].strip():
        return payload['output_text']
    for step in reversed(payload.get('steps') or []):
        if isinstance(step,dict) and step.get('type')=='model_output':
            content=step.get('content')
            if isinstance(content,str) and content.strip():
                return content
            for item in content or []:
                if isinstance(item,dict) and isinstance(item.get('text'),str) and item['text'].strip():
                    return item['text']
    raise RuntimeError('Gemini judge returned no text')


def pace_groq()->None:
    interval=float(os.environ.get('GROQ_MIN_INTERVAL_SECONDS','60'))
    marker=Path(os.environ.get('GROQ_PACE_FILE','/tmp/visual-v04-runtime-probe-groq-pace'))
    if interval<=0:
        return
    if marker.exists():
        try:
            delay=interval-(time.time()-float(marker.read_text().strip()))
        except Exception:
            delay=0
        if delay>0:
            time.sleep(delay)
    marker.write_text(str(time.time()))


def http(req:urllib.request.Request,provider:str,timeout:int,*,groq:bool=False)->dict:
    for attempt in range(TRANSIENT_5XX_RETRIES+1):
        if groq:
            pace_groq()
        try:
            with urllib.request.urlopen(req,timeout=timeout) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as exc:
            detail=exc.read().decode('utf-8','replace')[-1500:]
            if 500<=exc.code<600 and attempt<TRANSIENT_5XX_RETRIES:
                time.sleep(TRANSIENT_RETRY_DELAY_SECONDS)
                continue
            raise RuntimeError(f'{provider} HTTP {exc.code}: {detail}') from None
    raise RuntimeError(f'{provider} retry budget exhausted')


def candidate_call(fixture:dict)->dict:
    proc=subprocess.run(
        ['python3',EXECUTOR,'--model-timeout','180'],
        input=json.dumps({'prompt':fixture['prompt']},ensure_ascii=False),
        text=True,capture_output=True,timeout=240,
    )
    if proc.returncode!=0:
        raise RuntimeError('candidate executor failure: '+proc.stdout[-800:]+proc.stderr[-400:])
    out=json.loads(proc.stdout)
    ident=out.get('candidate_identity') or {}
    expected={
        'candidate_commit':'b4793a66172d4de7fe0ade1b0001bc2621829db2',
        'skill_blob':'bee4ee67a8aff43016e158f37a6f421cd079581a',
        'professional_model_base_blob':'bbea595e299445cf79f798ed1e86eecd0b53cd50',
        'professional_model_repair_v02_blob':'bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50',
        'professional_model_repair_v03_blob':'dd42d50f07b804c1ddd3c93b96704e0c6256440c',
        'model':'gemini-3.7-flash',
        'thinking_level':'medium',
        'development_only':True,
        'hidden_release_material_used':False,
    }
    for key,value in expected.items():
        if ident.get(key)!=value:
            raise RuntimeError(f'candidate probe identity mismatch {key}')
    text=out.get('final_output')
    if not isinstance(text,str) or not text.strip():
        raise RuntimeError('candidate probe output empty')
    return {'text':text,'identity':ident}


def judge_prompt(fixture:dict,candidate_output:str)->dict:
    return {
        'role':'Independent public development regression assessor for Visual Design / Art Direction.',
        'fixture_id':fixture['id'],
        'work_case':fixture['prompt'],
        'must_observe':fixture['must_observe'],
        'must_not_observe':fixture['must_not_observe'],
        'candidate_output':candidate_output,
        'decision_rule':[
            'PASS only if every must_observe behavior is clearly present in the actual selected recommendation/decision.',
            'FAIL if any must_not_observe behavior is present, even if the output also states the correct rule or warning.',
            'Do not reward verbosity, disclaimers, caveats or stated intentions that contradict the actual selected output.',
            'For a non-regression fixture, do not fail merely because the solution is bold, reference-informed, transformed on mobile, or conditional where the public criteria explicitly permit it.',
        ],
        'output_contract':'Return the required JSON only.',
    }


def judge_gemini(fixture:dict,candidate_output:str)->dict:
    key=os.environ.get('GEMINI_API_KEY','').strip()
    if not key:
        raise RuntimeError('GEMINI_API_KEY missing')
    body={
        'model':GEMINI_MODEL,
        'system_instruction':'You are a strict senior art-direction regression assessor. Apply only the supplied PUBLIC criteria. Return schema-valid JSON only.',
        'input':json.dumps(judge_prompt(fixture,candidate_output),ensure_ascii=False),
        'store':False,
        'generation_config':{'thinking_level':'medium'},
        'response_format':{'type':'text','mime_type':'application/json','schema':JUDGE_SCHEMA},
    }
    req=urllib.request.Request(
        GEMINI,data=json.dumps(body,ensure_ascii=False).encode(),method='POST',
        headers={'x-goog-api-key':key,'Content-Type':'application/json'},
    )
    return parse(gemini_text(http(req,'Gemini judge',180)))


def judge_groq(fixture:dict,candidate_output:str)->dict:
    key=os.environ.get('GROQ_API_KEY','').strip()
    if not key:
        raise RuntimeError('GROQ_API_KEY missing')
    body={
        'model':GROQ_MODEL,
        'messages':[
            {'role':'system','content':'You are a strict senior art-direction regression assessor. Apply only the supplied PUBLIC criteria.'},
            {'role':'user','content':json.dumps(judge_prompt(fixture,candidate_output),ensure_ascii=False)},
        ],
        'response_format':{'type':'json_schema','json_schema':{'name':'visual_v04_public_probe_judgment','strict':True,'schema':JUDGE_SCHEMA}},
        'include_reasoning':False,
        'reasoning_effort':'medium',
        'temperature':0,
    }
    req=urllib.request.Request(
        GROQ,data=json.dumps(body,ensure_ascii=False).encode(),method='POST',
        headers={'Authorization':f'Bearer {key}','Content-Type':'application/json','Accept':'application/json','User-Agent':'visual-v04-runtime-probe/1.0'},
    )
    raw=http(req,'Groq judge',180,groq=True)
    return parse(raw['choices'][0]['message']['content'])


def valid_judgment(j:dict)->bool:
    if set(j)!={'pass','failure_type','must_not_observe_triggered','missing_required_count','concise_reason'}:
        return False
    if not isinstance(j['pass'],bool) or not isinstance(j['must_not_observe_triggered'],bool):
        return False
    if not isinstance(j['missing_required_count'],int) or not isinstance(j['concise_reason'],str):
        return False
    if j['pass']:
        return j['failure_type']=='PASS' and j['must_not_observe_triggered'] is False and j['missing_required_count']==0
    return j['failure_type']!='PASS'


def write_progress(status:str,candidate_calls:int,judge_calls:dict[str,int],*,failure:str|None=None)->None:
    PROGRESS.write_text(json.dumps({
        'status':status,
        'development_only':True,
        'hidden_release_material_used':False,
        'candidate_calls':candidate_calls,
        'judge_calls':judge_calls,
        'failure':failure,
    },indent=2,sort_keys=True)+'\n')


def main()->int:
    data=json.load(open(FIXTURES))
    boundary=data.get('source_boundary') or {}
    if boundary.get('r4_hidden_content_used') is not False or boundary.get('sanitized_failure_classes_only') is not True or boundary.get('release_use')!='DEVELOPMENT_ONLY':
        raise RuntimeError('public fixture source boundary mismatch')
    all_fixtures={x['id']:x for x in data['families']}
    if not all(x in all_fixtures for x in SELECTED):
        raise RuntimeError('selected public fixture missing')

    results=[]
    details=[]
    candidate_calls=0
    judge_calls={'gemini':0,'groq':0}
    write_progress('IN_PROGRESS',candidate_calls,judge_calls)
    try:
        for fixture_id in SELECTED:
            fixture=all_fixtures[fixture_id]
            candidate=candidate_call(fixture)
            candidate_calls+=1
            write_progress('IN_PROGRESS',candidate_calls,judge_calls)

            gj=judge_gemini(fixture,candidate['text']); judge_calls['gemini']+=1
            if not valid_judgment(gj):
                raise RuntimeError(f'Gemini invalid judgment contract on {fixture_id}')
            write_progress('IN_PROGRESS',candidate_calls,judge_calls)

            qj=judge_groq(fixture,candidate['text']); judge_calls['groq']+=1
            if not valid_judgment(qj):
                raise RuntimeError(f'Groq invalid judgment contract on {fixture_id}')
            write_progress('IN_PROGRESS',candidate_calls,judge_calls)

            row={
                'fixture_id':fixture_id,
                'criticality':fixture['criticality'],
                'gemini':gj,
                'groq':qj,
                'pass':bool(gj['pass'] and qj['pass']),
                'judge_disagreement':gj['pass']!=qj['pass'],
            }
            results.append(row)
            details.append({
                'fixture_id':fixture_id,
                'prompt':fixture['prompt'],
                'must_observe':fixture['must_observe'],
                'must_not_observe':fixture['must_not_observe'],
                'candidate_output':candidate['text'],
                'judgments':{'gemini':gj,'groq':qj},
            })

        passed=len(results)==len(SELECTED) and all(r['pass'] for r in results)
        status='PUBLIC_RUNTIME_PROBE_PASS' if passed else 'PUBLIC_RUNTIME_PROBE_FAIL'
        report={
            'status':status,
            'development_only':True,
            'release_evidence':False,
            'hidden_release_material_used':False,
            'candidate':{
                'professional_components':'exact frozen v0.3',
                'runtime_model':'gemini-3.7-flash',
                'thinking_level':'medium',
            },
            'fixture_ids':list(SELECTED),
            'candidate_calls':candidate_calls,
            'judge_models':{'gemini':GEMINI_MODEL,'groq':GROQ_MODEL},
            'judge_calls':judge_calls,
            'fixture_outcomes':results,
            'all_fixtures_pass_both_judges':passed,
            'next_step':'freeze runtime-only v0.4 candidate' if passed else 'test staged structural execution controller; do not freeze runtime-only v0.4',
        }
        REPORT.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        DETAILS.write_text(json.dumps({'development_only':True,'hidden_release_material_used':False,'cases':details},indent=2,sort_keys=True)+'\n')
        write_progress(status,candidate_calls,judge_calls)
        print(json.dumps({'status':status,'candidate_calls':candidate_calls,'judge_calls':judge_calls,'passed_fixtures':sum(1 for r in results if r['pass']),'fixture_count':len(results)},sort_keys=True))
        return 0 if passed else 20
    except Exception as exc:
        DETAILS.write_text(json.dumps({'development_only':True,'hidden_release_material_used':False,'cases':details,'failure':str(exc)[:800]},indent=2,sort_keys=True)+'\n')
        write_progress('INFRASTRUCTURE_FAILURE',candidate_calls,judge_calls,failure=str(exc)[:600])
        print(json.dumps({'status':'INFRASTRUCTURE_FAILURE','candidate_calls':candidate_calls,'judge_calls':judge_calls,'error':str(exc)[:600]},sort_keys=True))
        return 30

if __name__=='__main__':
    raise SystemExit(main())
