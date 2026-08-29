#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, time, urllib.error, urllib.request
from collections import Counter
from pathlib import Path
from cryptography.fernet import Fernet

ROOT=Path.cwd(); BASE=ROOT/'architect/evaluation/visual-design-art-direction/heldout'
CYCLE='visual-design-art-direction-0.1.0-independent-2026-08-29-r1-semantic'
CANDIDATE_COMMIT='e8be839b02f181193afe076839c6ae94fb477a9b'
SKILL_BLOB='9d251d97a84e16ade91c8ced07425f9208f9f900'; MODEL_BLOB='bbea595e299445cf79f798ed1e86eecd0b53cd50'
GEMINI_MODEL='gemini-3.5-flash-lite'; GROQ_MODEL='openai/gpt-oss-120b'
GEMINI='https://generativelanguage.googleapis.com/v1beta/interactions'; GROQ='https://api.groq.com/openai/v1/chat/completions'
FAMILIES=['FRAMING','REFERENCE','DIVERGENCE','CRAFT_JUDGMENT','MOBILE','TRUTH','CONTRACT','CRITIQUE_REPAIR','ADVANCED_MEDIA_ROUTING','AUTHORITY_BOUNDARY']
PAIR_IDS={'REFERENCE':'PAIR_REFERENCE','MOBILE':'PAIR_MOBILE','TRUTH':'PAIR_TRUTH','ADVANCED_MEDIA_ROUTING':'PAIR_MEDIA','AUTHORITY_BOUNDARY':'PAIR_AUTHORITY'}
AUDIT_SCHEMA={'type':'object','additionalProperties':False,'properties':{'accept':{'type':'boolean'}},'required':['accept']}

def h(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def parse(t:str):
    t=t.strip()
    if t.startswith('```'):t='\n'.join(t.splitlines()[1:-1]).strip()
    return json.loads(t)
def gtext(raw):
    if isinstance(raw.get('output_text'),str):return raw['output_text']
    for step in reversed(raw.get('steps') or []):
        if isinstance(step,dict) and step.get('type')=='model_output':
            c=step.get('content')
            if isinstance(c,str):return c
            for x in c or []:
                if isinstance(x,dict) and isinstance(x.get('text'),str):return x['text']
    raise RuntimeError('Gemini author returned no text')
def pace_groq():
    interval=float(os.environ.get('GROQ_MIN_INTERVAL_SECONDS','60')); p=Path(os.environ.get('GROQ_PACE_FILE','/tmp/visual-heldout-groq-pace'))
    if p.exists():
        try:delay=interval-(time.time()-float(p.read_text().strip()))
        except Exception:delay=0
        if delay>0:time.sleep(delay)
    p.write_text(str(time.time()))
def validate(cases):
    if not isinstance(cases,list) or len(cases)!=20:raise RuntimeError('heldout cardinality invalid')
    ids=[x.get('id') for x in cases]; fam=Counter(x.get('family') for x in cases)
    if None in ids or len(ids)!=len(set(ids)):raise RuntimeError('heldout ids invalid')
    if set(fam)!=set(FAMILIES) or any(v!=2 for v in fam.values()):raise RuntimeError(f'family structure invalid {dict(fam)}')
    for x in cases:
        f=x['family']; expected_pair=PAIR_IDS.get(f)
        if x.get('pair_id')!=expected_pair:raise RuntimeError(f'pair_id invalid for {f}')
        for k in ['brief','context','constraints','competent_generic_baseline','professional_criteria']:
            if not x.get(k):raise RuntimeError(f'missing {k} in {x.get("id")}')
        if not isinstance(x['professional_criteria'],list) or len(x['professional_criteria'])<3:raise RuntimeError('criteria invalid')
        p0=x.get('p0_guardrail')
        if p0 is not None and (not isinstance(p0,dict) or not p0.get('category') or not p0.get('trigger')):raise RuntimeError('p0_guardrail invalid')
    return cases
def author():
    key=os.environ.get('GEMINI_API_KEY','').strip()
    if not key:raise RuntimeError('GEMINI_API_KEY missing')
    prompt={'task':'Author a fresh sealed FULL semantic qualification corpus for a frozen landing-page Visual Design / Art Direction professional core. Return JSON array only.','candidate_seen':False,'case_count':20,'families':FAMILIES,'exactly_two_per_family':True,'pair_ids':PAIR_IDS,'fields':['id','family','pair_id','brief','context','constraints','competent_generic_baseline','professional_criteria','p0_guardrail'],'requirements':['Fresh wording and situations created after candidate freeze; do not copy public development fixtures.','Each case must be self-contained and realistic professional work, not trivia or rule recitation.','The competent_generic_baseline must be plausible and safe but noticeably generic/shallower than strong practitioner work; it must not contain a P0 violation.','For the five paired families, the two cases must differ by one material fact so the professionally correct stance changes where justified.','REFERENCE pair: imitation pressure versus mechanism extraction with broad evidence.','MOBILE pair: collapsed-desktop failure versus an already authored narrow composition that should not be reset ceremonially.','TRUTH pair: missing proof versus verified supplied proof that should be used confidently.','ADVANCED_MEDIA_ROUTING pair: ornamental 3D versus materially explanatory spatial/assembly value.','AUTHORITY_BOUNDARY pair: visual decision inside authority versus requested CRO/product logic change outside authority.','Cover framing, real divergence, craft diagnosis, implementation contract, critique/root-cause repair, mobile-specific art direction and advanced-media routing.','p0_guardrail is null when no clear hard-fail is intentionally tested; otherwise {category,trigger} using only a preregistered P0 category.','Do not leak expected answers in candidate-visible brief/context/constraints. professional_criteria and p0_guardrail are hidden grader context.']}
    body={'model':GEMINI_MODEL,'system_instruction':'You are an independent senior landing-page art director and evaluation designer. Build construct-valid adversarial work samples. Return JSON only.','input':json.dumps(prompt,ensure_ascii=False),'store':False,'generation_config':{'thinking_level':'medium'}}
    req=urllib.request.Request(GEMINI,data=json.dumps(body,ensure_ascii=False).encode(),method='POST',headers={'x-goog-api-key':key,'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=240) as r:return validate(parse(gtext(json.loads(r.read().decode()))))
def audit_pair(family,cases):
    key=os.environ.get('GROQ_API_KEY','').strip()
    if not key:raise RuntimeError('GROQ_API_KEY missing')
    payload={'family':family,'cases':cases,'audit_task':'Accept only if these two hidden qualification cases are fresh, self-contained, construct-valid, non-leaky, professionally realistic; competent baselines are safe/generic rather than strong; hidden professional criteria are grounded in supplied facts; and any declared pair differs in one material fact with a justified stance change. Reject public-fixture paraphrases, style-only grading, impossible requirements or ambiguous P0 triggers.'}
    body={'model':GROQ_MODEL,'messages':[{'role':'user','content':json.dumps(payload,ensure_ascii=False)}],'response_format':{'type':'json_schema','json_schema':{'name':'heldout_audit','strict':True,'schema':AUDIT_SCHEMA}},'include_reasoning':False,'reasoning_effort':'medium','temperature':0}
    req=urllib.request.Request(GROQ,data=json.dumps(body,ensure_ascii=False).encode(),method='POST',headers={'Authorization':f'Bearer {key}','Content-Type':'application/json','Accept':'application/json','User-Agent':'visual-heldout-audit/0.1'})
    pace_groq()
    try:
        with urllib.request.urlopen(req,timeout=180) as r:return parse(json.loads(r.read().decode())['choices'][0]['message']['content'])['accept']
    except urllib.error.HTTPError as exc:
        detail=exc.read().decode('utf-8','replace')[-1200:]; raise RuntimeError(f'Groq audit HTTP {exc.code}: {detail}') from None
def main():
    cases=author()
    for family in FAMILIES:
        pair=[x for x in cases if x['family']==family]
        if not audit_pair(family,pair):raise RuntimeError(f'independent audit rejected family {family}')
    master=os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY','').encode().strip()
    if not master:raise RuntimeError('QUALIFICATION_SEALED_PACK_MASTER_KEY missing')
    import sys; sys.path.insert(0,str(ROOT/'architect/evaluation/qualification-platform'))
    from sealed_pack_keys import derive_fernet_key,key_fingerprint_sha256
    payload={'cycle_id':CYCLE,'candidate_commit':CANDIDATE_COMMIT,'candidate_blobs':{'skill':SKILL_BLOB,'professional_model':MODEL_BLOB},'families':FAMILIES,'pair_ids':PAIR_IDS,'cases':cases,'author_model':GEMINI_MODEL,'audit_model':GROQ_MODEL}
    raw=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode(); key=derive_fernet_key(master,CYCLE); token=Fernet(key).encrypt(raw)
    out=BASE/'sealed'; out.mkdir(parents=True,exist_ok=True); parts=out/'heldout-v0.1.parts'
    if parts.exists():
        import shutil; shutil.rmtree(parts)
    parts.mkdir(); text=token.decode('ascii'); chunks=[text[i:i+4000] for i in range(0,len(text),4000)]
    for i,c in enumerate(chunks):(parts/f'{i:02d}').write_text(c)
    manifest={'schema_version':'0.1','cycle_id':CYCLE,'candidate_commit':CANDIDATE_COMMIT,'candidate_blobs':payload['candidate_blobs'],'item_count':20,'family_count':10,'pair_count':5,'author_model':GEMINI_MODEL,'audit_model':GROQ_MODEL,'part_count':len(chunks),'ciphertext_length':len(token),'ciphertext_sha256':h(token),'plaintext_sha256':h(raw),'key_fingerprint_sha256':key_fingerprint_sha256(key),'candidate_calls':0,'hidden_content_printed':False}
    (out/'heldout-v0.1.manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'HELDOUT_AUTHORED_AUDITED_SEALED','item_count':20,'family_count':10,'pair_count':5,'ciphertext_sha256':manifest['ciphertext_sha256'],'candidate_calls':0,'hidden_content_printed':False}))
if __name__=='__main__':main()
