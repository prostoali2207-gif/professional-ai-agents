#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, shutil, tempfile, urllib.error, urllib.request, zipfile
from pathlib import Path
from cryptography.fernet import Fernet

ROOT=Path.cwd(); BASE=ROOT/'architect/evaluation/visual-design-art-direction/calibration'
CYCLE='visual-design-art-direction-0.1.0-independent-2026-08-29-r1-calibration'
AUTHOR_MODEL='gemini-3.5-flash-lite'; AUDIT_MODEL='qwen/qwen3.6-27b'
GEMINI='https://generativelanguage.googleapis.com/v1beta/interactions'; GROQ=os.environ.get('GROQ_BASE_URL','https://api.groq.com/openai/v1').rstrip('/')+'/chat/completions'
ARCHETYPES=['competent_generic','derivative_reference_copy','overdesigned_spectacle','function_damaging_novelty','collapsed_desktop_mobile','faithful_but_poor_render','craft_weak_hierarchy','justified_rule_breaking','advanced_media_justified','advanced_media_ornamental']
DIMS=['brief_appropriateness','reference_independence','concept_distinctiveness','craft','function_clarity','mobile_art_direction','advanced_media_judgment','authority_boundary']

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def parse(t):
    t=t.strip()
    if t.startswith('```'): t='\n'.join(t.splitlines()[1:-1]).strip()
    return json.loads(t)
def gtext(raw):
    if isinstance(raw.get('output_text'),str): return raw['output_text']
    for step in reversed(raw.get('steps') or []):
        if isinstance(step,dict) and step.get('type')=='model_output':
            c=step.get('content')
            if isinstance(c,str): return c
            for x in c or []:
                if isinstance(x,dict) and isinstance(x.get('text'),str): return x['text']
    raise RuntimeError('gemini returned no text')
def validate(items):
    if not isinstance(items,list) or len(items)!=len(ARCHETYPES): raise RuntimeError('calibration cardinality invalid')
    if {x.get('archetype') for x in items}!=set(ARCHETYPES): raise RuntimeError('archetypes invalid')
    for x in items:
        for k in ['id','archetype','brief','sample_strong','sample_challenger','expected_winner','relevant_dimensions']:
            if k not in x: raise RuntimeError(f'missing {k}')
        if x['expected_winner'] not in {'strong','challenger'}: raise RuntimeError('winner invalid')
        if not set(x['relevant_dimensions']).issubset(DIMS): raise RuntimeError('dimension invalid')
    return items

def author():
    key=os.environ.get('GEMINI_API_KEY','').strip()
    if not key: raise RuntimeError('GEMINI_API_KEY missing')
    prompt={'task':'Create a visual-design/art-direction judge calibration corpus for landing pages. Produce exactly one blinded comparison item for each requested archetype. Each item must contain a realistic brief plus two substantive practitioner outputs: one strong practitioner-quality response and one response exhibiting the named archetype, except justified_rule_breaking and advanced_media_justified where the unusual/advanced response should be the correct professional winner over a reflexively conservative alternative. Keep outputs detailed enough to test judgment, not keyword matching. Do not mention expected winner inside either sample. JSON array only.','archetypes':ARCHETYPES,'dimensions':DIMS,'schema':{'id':'CAL-01','archetype':'...','brief':'...','sample_strong':'...','sample_challenger':'...','expected_winner':'strong|challenger','relevant_dimensions':['...']}}
    body={'model':AUTHOR_MODEL,'system_instruction':'You are a senior landing-page art director and evaluation designer. Build authentic contrastive work samples. Return JSON only.','input':json.dumps(prompt,ensure_ascii=False),'store':False,'generation_config':{'thinking_level':'medium'}}
    req=urllib.request.Request(GEMINI,data=json.dumps(body,ensure_ascii=False).encode(),method='POST',headers={'x-goog-api-key':key,'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=240) as r:return validate(parse(gtext(json.loads(r.read().decode()))))

def audit_one(item):
    key=os.environ.get('GROQ_API_KEY','').strip()
    if not key: raise RuntimeError('GROQ_API_KEY missing')
    task={'task':'Audit and, only if needed, repair this single calibration pair before judge calibration. Preserve its archetype and schema. Ensure the expected winner is professionally defensible, the pair is realistic, contains no answer leakage, and tests causal art-direction judgment rather than verbosity. For justified_rule_breaking and advanced_media_justified, a professionally justified non-conservative response must be allowed to win. For advanced_media_ornamental, restraint should win. Return the repaired item as one JSON object only.','dimensions':DIMS,'item':item}
    body={'model':AUDIT_MODEL,'messages':[{'role':'system','content':'Act as an independent senior landing-page art-direction assessor and evaluation scientist. Return JSON only.'},{'role':'user','content':json.dumps(task,ensure_ascii=False)}],'response_format':{'type':'json_object'},'reasoning_format':'hidden','reasoning_effort':'default','temperature':0}
    req=urllib.request.Request(GROQ,data=json.dumps(body,ensure_ascii=False).encode(),method='POST',headers={'Authorization':f'Bearer {key}','Content-Type':'application/json','Accept':'application/json','User-Agent':'visual-calibration-auditor/0.1'})
    try:
        with urllib.request.urlopen(req,timeout=180) as r:
            return json.loads(json.loads(r.read().decode())['choices'][0]['message']['content'])
    except urllib.error.HTTPError as exc:
        detail=exc.read().decode('utf-8','replace')[-1500:]
        raise RuntimeError(f'Groq audit HTTP {exc.code}: {detail}') from None

def audit(items): return validate([audit_one(x) for x in items])

def main():
    master=os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY','').encode().strip()
    if not master: raise RuntimeError('QUALIFICATION_SEALED_PACK_MASTER_KEY missing')
    items=audit(author())
    import sys; sys.path.insert(0,str(ROOT/'architect/evaluation/qualification-platform'))
    from sealed_pack_keys import derive_fernet_key,key_fingerprint_sha256
    with tempfile.TemporaryDirectory(prefix='visual-calibration-') as td:
        d=Path(td); (d/'calibration.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
        freeze={'cycle_id':CYCLE,'item_count':len(items),'archetypes':ARCHETYPES,'dimensions':DIMS,'author_model':AUTHOR_MODEL,'audit_model':AUDIT_MODEL,'calibration_pass_policy':{'per_judge_expected_winner_rate_min':0.80,'combined_expected_winner_rate_min':0.90,'max_pair_disagreement_rate':0.25},'candidate_calls':0}
        (d/'freeze-record.json').write_text(json.dumps(freeze,indent=2,sort_keys=True)+'\n')
        z=d/'pack.zip'
        with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as q:q.write(d/'calibration.json','calibration.json'); q.write(d/'freeze-record.json','freeze-record.json')
        raw=z.read_bytes(); key=derive_fernet_key(master,CYCLE); token=Fernet(key).encrypt(raw)
    parts=BASE/'sealed/calibration-v0.1.parts'; shutil.rmtree(parts,ignore_errors=True); parts.mkdir(parents=True)
    txt=token.decode('ascii'); chunks=[txt[i:i+4000] for i in range(0,len(txt),4000)]
    for i,c in enumerate(chunks):(parts/f'{i:02d}').write_text(c)
    manifest={'version':1,'cycle_id':CYCLE,'part_count':len(chunks),'ciphertext_length':len(token),'ciphertext_sha256':sha(token),'key_fingerprint_sha256':key_fingerprint_sha256(key),'decrypted_zip_sha256':sha(raw),'item_count':len(items),'candidate_calls':0}
    (BASE/'sealed/calibration-v0.1.manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'CALIBRATION_PACK_SEALED','item_count':len(items),'part_count':len(chunks),'ciphertext_sha256':manifest['ciphertext_sha256'],'hidden_content_printed':False,'candidate_calls':0}))
if __name__=='__main__': main()
