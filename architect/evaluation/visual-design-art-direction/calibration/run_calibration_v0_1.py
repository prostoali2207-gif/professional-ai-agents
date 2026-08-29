#!/usr/bin/env python3
from __future__ import annotations
import json, os, random, tempfile, time, urllib.error, urllib.request, zipfile
from pathlib import Path
from cryptography.fernet import Fernet

ROOT=Path.cwd(); BASE=ROOT/'architect/evaluation/visual-design-art-direction/calibration'; CYCLE='visual-design-art-direction-0.1.0-independent-2026-08-29-r1-calibration'
GEMINI='https://generativelanguage.googleapis.com/v1beta/interactions'; GROQ=os.environ.get('GROQ_BASE_URL','https://api.groq.com/openai/v1').rstrip('/')+'/chat/completions'
JUDGES=[('gemini','gemini-3.5-flash-lite'),('groq','openai/gpt-oss-120b')]
JUDGE_SCHEMA={'type':'object','additionalProperties':False,'properties':{'winner':{'type':'string','enum':['A','B']}},'required':['winner']}

def parse(t):
    t=t.strip()
    if t.startswith('```'): t='\n'.join(t.splitlines()[1:-1]).strip()
    return json.loads(t)
def pace_groq():
    interval=float(os.environ.get('GROQ_MIN_INTERVAL_SECONDS','0')); p=Path(os.environ.get('GROQ_PACE_FILE','/tmp/visual-groq-pace'))
    if interval<=0:return
    if p.exists():
        try:last=float(p.read_text().strip()); delay=interval-(time.time()-last)
        except Exception:delay=0
        if delay>0: time.sleep(delay)
    p.write_text(str(time.time()))
def gt(raw):
    if isinstance(raw.get('output_text'),str): return raw['output_text']
    for step in reversed(raw.get('steps') or []):
        if isinstance(step,dict) and step.get('type')=='model_output':
            c=step.get('content')
            if isinstance(c,str): return c
            for x in c or []:
                if isinstance(x,dict) and isinstance(x.get('text'),str): return x['text']
    raise RuntimeError('gemini no text')
def decrypt():
    master=os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY','').encode().strip()
    if not master: raise RuntimeError('sealed master key missing')
    import sys; sys.path.insert(0,str(ROOT/'architect/evaluation/qualification-platform'))
    from sealed_pack_keys import derive_fernet_key
    m=json.load(open(BASE/'sealed/calibration-v0.1.manifest.json')); token=''.join(p.read_text() for p in sorted((BASE/'sealed/calibration-v0.1.parts').iterdir())).encode(); raw=Fernet(derive_fernet_key(master,CYCLE)).decrypt(token)
    if __import__('hashlib').sha256(raw).hexdigest()!=m['decrypted_zip_sha256']: raise RuntimeError('calibration pack digest mismatch')
    td=tempfile.TemporaryDirectory(prefix='visual-cal-run-'); z=Path(td.name)/'p.zip'; z.write_bytes(raw)
    with zipfile.ZipFile(z) as q:q.extractall(td.name)
    return td, json.load(open(Path(td.name)/'calibration.json')), json.load(open(Path(td.name)/'freeze-record.json'))
def judge(provider,model,brief,a,b,dims):
    payload={'role':'You are a blind senior landing-page art-direction assessor.','brief':brief,'output_A':a,'output_B':b,'dimensions':dims,'task':'Choose the professionally stronger landing-page visual-design/art-direction output. Judge causal appropriateness, craft, function, mobile behavior, reference independence and boundary discipline as relevant. Do not reward verbosity. Return only winner A or B in JSON.'}
    if provider=='gemini':
        key=os.environ.get('GEMINI_API_KEY','').strip()
        if not key: raise RuntimeError('GEMINI_API_KEY missing')
        body={'model':model,'system_instruction':'You are a blind senior art-direction assessor. Return JSON only as {"winner":"A"} or {"winner":"B"}.','input':json.dumps(payload,ensure_ascii=False),'store':False,'generation_config':{'thinking_level':'medium'}}
        req=urllib.request.Request(GEMINI,data=json.dumps(body,ensure_ascii=False).encode(),method='POST',headers={'x-goog-api-key':key,'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=180) as r:return parse(gt(json.loads(r.read().decode())))
    key=os.environ.get('GROQ_API_KEY','').strip()
    if not key: raise RuntimeError('GROQ_API_KEY missing')
    body={'model':model,'messages':[{'role':'user','content':json.dumps(payload,ensure_ascii=False)}],'response_format':{'type':'json_schema','json_schema':{'name':'visual_judgment','strict':True,'schema':JUDGE_SCHEMA}},'include_reasoning':False,'reasoning_effort':'medium','temperature':0}
    req=urllib.request.Request(GROQ,data=json.dumps(body,ensure_ascii=False).encode(),method='POST',headers={'Authorization':f'Bearer {key}','Content-Type':'application/json','Accept':'application/json','User-Agent':'visual-calibration-judge/0.3'})
    pace_groq()
    try:
        with urllib.request.urlopen(req,timeout=180) as r:return parse(json.loads(r.read().decode())['choices'][0]['message']['content'])
    except urllib.error.HTTPError as exc:
        detail=exc.read().decode('utf-8','replace')[-1500:]
        raise RuntimeError(f'Groq judge HTTP {exc.code}: {detail}') from None
def main():
    td,items,freeze=decrypt(); results=[]
    try:
        for item in items:
            swap=random.Random(f'{CYCLE}:{item["id"]}').choice([False,True])
            if swap: a,b=item['sample_challenger'],item['sample_strong']; expected='B' if item['expected_winner']=='strong' else 'A'
            else: a,b=item['sample_strong'],item['sample_challenger']; expected='A' if item['expected_winner']=='strong' else 'B'
            row={'id':item['id'],'archetype':item['archetype'],'expected':expected,'judges':{}}
            for provider,model in JUDGES:
                out=judge(provider,model,item['brief'],a,b,item['relevant_dimensions']); win=out.get('winner'); row['judges'][provider]={'model':model,'winner':win,'correct':win==expected}
            results.append(row)
        n=len(results); rates={p:sum(r['judges'][p]['correct'] for r in results)/n for p,_ in JUDGES}; combined=sum(r['judges'][p]['correct'] for r in results for p,_ in JUDGES)/(n*len(JUDGES)); disagree=sum(r['judges']['gemini']['winner']!=r['judges']['groq']['winner'] for r in results)/n
        pol=freeze['calibration_pass_policy']; passed=all(v>=pol['per_judge_expected_winner_rate_min'] for v in rates.values()) and combined>=pol['combined_expected_winner_rate_min'] and disagree<=pol['max_pair_disagreement_rate']
        report={'cycle_id':CYCLE,'status':'CALIBRATION_PASS' if passed else 'CALIBRATION_FAIL','candidate_calls':0,'item_count':n,'judge_models':dict(JUDGES),'per_judge_expected_winner_rate':rates,'combined_expected_winner_rate':combined,'pair_disagreement_rate':disagree,'policy':pol,'archetype_outcomes':[{'archetype':r['archetype'],'gemini_correct':r['judges']['gemini']['correct'],'groq_correct':r['judges']['groq']['correct'],'judges_disagree':r['judges']['gemini']['winner']!=r['judges']['groq']['winner']} for r in results]}
        Path('visual-calibration-sanitized-report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n'); print(json.dumps({'status':report['status'],'candidate_calls':0,'item_count':n,'combined_expected_winner_rate':combined,'pair_disagreement_rate':disagree})); raise SystemExit(0 if passed else 10)
    finally: td.cleanup()
if __name__=='__main__': main()
