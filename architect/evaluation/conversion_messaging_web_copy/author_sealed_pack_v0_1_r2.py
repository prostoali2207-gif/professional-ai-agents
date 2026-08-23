#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter
import hashlib,json,os,shutil,tempfile,urllib.error,urllib.request,zipfile
from pathlib import Path
from cryptography.fernet import Fernet
ROOT=Path.cwd(); BASE=ROOT/'architect/evaluation/conversion_messaging_web_copy'
CYCLE='conversion-messaging-web-copy-v0.1-heldout-2026-08-23-r2'
COMMIT='7019f6717b1b61806f4a221a297d049a4ad3b8cb'; DIGEST='sha256:da7662f95dcf132d9a9875849b7bb5d5d831d1d54821f0b109b543a1f299e1d2'
PARTS=BASE/'sealed/heldout-v0.1-2026-08-23-r2.parts'; MANIFEST=BASE/'sealed/heldout-v0.1-2026-08-23-r2.qualification.json'; RUNNER=BASE/'sealed_runner_template_v0_1_r2.py'
GEMINI='gemini-3.5-flash-lite'; GROQ='qwen/qwen3.6-27b'; FAMILIES=['CM-EV','CM-CL','CM-MH','CM-DV','CM-OP','CM-UX','CM-PL','CM-CR','CM-EX','CM-BD','CM-PR','CM-E2E']; PAIRS={'P-EVIDENCE':'CM-EV','P-CLAIM':'CM-CL','P-UX':'CM-UX','P-BOUNDARY':'CM-BD'}
def h(b): return hashlib.sha256(b).hexdigest()
def parse(t):
 t=t.strip();
 if t.startswith('```'): t='\n'.join(t.splitlines()[1:-1]).strip()
 return json.loads(t)
def gtext(x):
 if isinstance(x.get('output_text'),str): return x['output_text']
 for s in reversed(x.get('steps') or []):
  if isinstance(s,dict) and s.get('type')=='model_output':
   c=s.get('content');
   if isinstance(c,str): return c
   if isinstance(c,list):
    z=''.join(i.get('text','') for i in c if isinstance(i,dict));
    if z:return z
 raise RuntimeError('Gemini returned no text')
def validate(cases):
 if not isinstance(cases,list) or len(cases)!=24: raise RuntimeError('fixture cardinality invalid')
 fam=Counter(x.get('family') for x in cases)
 if set(fam)!=set(FAMILIES) or set(fam.values())!={2}: raise RuntimeError('family structure invalid')
 ids=[x.get('id') for x in cases]
 if None in ids or len(ids)!=len(set(ids)): raise RuntimeError('ids invalid')
 for p,f in PAIRS.items():
  m=[x for x in cases if x.get('pair_id')==p]
  if len(m)!=2 or {x.get('family') for x in m}!={f}: raise RuntimeError('pair structure invalid')
 return cases
def author():
 k=os.environ.get('GEMINI_API_KEY','').strip()
 if not k: raise RuntimeError('GEMINI_API_KEY missing')
 prompt={'task':'Create exactly 24 fresh adversarial held-out work samples for frozen Conversion Messaging & Web Copy practitioner, two per declared family. Do not reuse public development wording. Include four contrastive pairs exactly as declared. Return JSON array only.','families':FAMILIES,'pairs':PAIRS,'required_fields':['id','family','pair_id','task','context','constraints','hidden_reference'],'hidden_reference_fields':['professional_disposition','evidence_boundaries','must_do','must_not_do','hard_fail_if','functional_craft_criteria','boundary_expectation'],'constructs':'customer-language provenance; contradictory/messy evidence; no-evidence refusal; bounded claims; fabricated social proof/urgency/guarantee pressure; hierarchy; genuine framing divergence; objection-proof matching; CTA/helper/error semantics under frozen UX; jargon translation; causal critique/revision; experiment hypothesis/metric/guardrail/falsifier; CRO/User Research/UX boundaries; multi-turn pressure represented in task context; anti-contrarian strong-evidence control; controlled-facts end-to-end landing messaging.'}
 body={'model':GEMINI,'system_instruction':'You are a senior conversion-copy practitioner and evaluation designer. Create authentic construct-valid work samples. JSON only.','input':json.dumps(prompt,ensure_ascii=False),'store':False,'generation_config':{'thinking_level':'medium'}}
 req=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/interactions',data=json.dumps(body).encode(),method='POST',headers={'x-goog-api-key':k,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=180) as r:return validate(parse(gtext(json.loads(r.read().decode()))))
def review(cases):
 k=os.environ.get('GROQ_API_KEY','').strip()
 if not k: raise RuntimeError('GROQ_API_KEY missing')
 body={'model':GROQ,'messages':[{'role':'system','content':'You are an independent evaluation scientist and senior conversion-copy assessor. Audit construct validity, ambiguity, leakage and overreach. Return only repaired JSON array.'},{'role':'user','content':json.dumps({'task':'Review and repair these hidden fixtures before candidate execution. Preserve exactly 24 cases, 12 families x2 and four declared pairs. Remove ambiguity, stylistic-only grading, impossible requirements, and references exceeding supplied facts. Strong-evidence controls must permit strong claims.','families':FAMILIES,'pairs':PAIRS,'cases':cases},ensure_ascii=False)}],'temperature':0,'reasoning_format':'hidden','response_format':{'type':'json_object'}}
 req=urllib.request.Request('https://api.groq.com/openai/v1/chat/completions',data=json.dumps(body).encode(),method='POST',headers={'Authorization':'Bearer '+k,'Content-Type':'application/json','Accept':'application/json','User-Agent':'professional-ai-agents-messaging-r2/1.0'})
 with urllib.request.urlopen(req,timeout=180) as r:
  raw=json.loads(r.read().decode()); t=raw['choices'][0]['message']['content']; v=json.loads(t)
  if isinstance(v,dict) and 'cases' in v:v=v['cases']
  return validate(v)
def main():
 master=os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY','').encode().strip()
 if not master: raise RuntimeError('QUALIFICATION_SEALED_PACK_MASTER_KEY missing')
 cases=review(author())
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)/'pack'; d.mkdir(); fixtures=[{k:x.get(k) for k in ['id','family','pair_id','task','context','constraints']} for x in cases]; grader={x['id']:x['hidden_reference'] for x in cases}
  (d/'fixtures.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)); (d/'grader.json').write_text(json.dumps(grader,ensure_ascii=False,indent=2)); shutil.copyfile(RUNNER,d/'runner.py')
  hs={n:h((d/n).read_bytes()) for n in ['fixtures.json','grader.json','runner.py']}; pack_digest='sha256:'+h(''.join(f'{n}:{hs[n]}\n' for n in sorted(hs)).encode())
  freeze={'cycle_id':CYCLE,'candidate_commit':COMMIT,'candidate_digest':DIGEST,'candidate_model':'gemini-3.5-flash-lite','judge_models':[GEMINI,GROQ],'fixture_count':24,'family_count':12,'per_family':2,'contrastive_pair_count':4,'fixtures_sha256':'sha256:'+hs['fixtures.json'],'grader_sha256':'sha256:'+hs['grader.json'],'runner_sha256':'sha256:'+hs['runner.py'],'pack_digest':pack_digest,'thresholds':{'minimum_fixture_passes':22,'hard_fail_count':0,'all_pairs_consistent':True,'family_dimension_min':{'evidence_integrity':1.5,'task_clarity':1.5,'professional_judgment':1.5,'functional_craft':1.25,'boundary_integrity':1.5}},'trial_count_per_fixture':1,'professional_failure_retry_count':0,'max_clean_run_model_calls':31}
  (d/'freeze-record.json').write_text(json.dumps(freeze,indent=2,sort_keys=True)); z=Path(td)/'pack.zip'
  with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as q:
   [q.write(d/n,arcname=n) for n in ['fixtures.json','grader.json','runner.py','freeze-record.json']]
  raw=z.read_bytes()
  import sys; sys.path.insert(0,str(ROOT/'architect/evaluation/qualification-platform')); from sealed_pack_keys import derive_fernet_key,key_fingerprint_sha256
  key=derive_fernet_key(master,CYCLE); token=Fernet(key).encrypt(raw)
 if PARTS.exists(): shutil.rmtree(PARTS)
 PARTS.mkdir(parents=True); s=token.decode(); chunks=[s[i:i+4000] for i in range(0,len(s),4000)]
 for i,c in enumerate(chunks):(PARTS/f'{i:02d}').write_text(c)
 manifest={'version':2,'cycle_id':CYCLE,'candidate':{'commit':COMMIT,'digest':DIGEST,'manifest_path':'agents/conversion-messaging-web-copy/0.1.0/artifact-manifest.json'},'runtime':{'executor_path':'architect/evaluation/conversion_messaging_web_copy/executor_v0_1_gemini.py','executor_cmd':'python3 architect/evaluation/conversion_messaging_web_copy/executor_v0_1_gemini.py','protocol':'conversion-messaging-web-copy-candidate-v1','provider':'gemini-interactions-api','model':'gemini-3.5-flash-lite','credential_env':'GEMINI_API_KEY','candidate_timeout_seconds':180,'model_timeout_seconds':120,'workflow_timeout_seconds':1800,'contract_probe_argv':['python3','architect/evaluation/conversion_messaging_web_copy/executor_v0_1_gemini.py','--qualification-contract'],'tool_protocol':'none-v1','state_protocol':'stateless-v1','observable_protocol':'text-response-usage-v1','canary_required':True,'canary_cmd':'python3 architect/evaluation/conversion_messaging_web_copy/canary_v0_1_gemini.py'},'sealed_pack':{'parts_dir':str(PARTS.relative_to(ROOT)),'part_count':len(chunks),'ciphertext_length':len(token),'ciphertext_sha256':h(token),'key_derivation':{'scheme':'hkdf-sha256-v1','master_env':'QUALIFICATION_SEALED_PACK_MASTER_KEY','context':CYCLE},'key_fingerprint_sha256':key_fingerprint_sha256(key),'decrypted_zip_sha256':h(raw),'pack_digest':freeze['pack_digest'],'required_files':['fixtures.json','grader.json','runner.py','freeze-record.json']},'evaluation':{'fixture_count':24,'family_count':12,'per_family':2,'fixtures_file':'fixtures.json','grader_file':'grader.json','runner_file':'runner.py','freeze_record_file':'freeze-record.json'},'report':{'sanitized_required':True,'artifact_required':True,'validator_path':'architect/evaluation/qualification-platform/validate_sanitized_report.py','release_ledger_required':True},'verdict':{'runner_exit_zero_required':True,'missing_report_is_failure':True,'report_validation_required':True,'artifact_upload_required':True}}
 MANIFEST.parent.mkdir(parents=True,exist_ok=True); MANIFEST.write_text(json.dumps(manifest,indent=2,sort_keys=True)); print(json.dumps({'status':'SEALED_PACK_AUTHORED','cycle_id':CYCLE,'fixture_count':24,'hidden_content_printed':False}))
if __name__=='__main__': main()
