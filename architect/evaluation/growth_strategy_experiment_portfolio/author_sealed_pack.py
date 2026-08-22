#!/usr/bin/env python3
from __future__ import annotations
import base64,hashlib,io,json,os,pathlib,zipfile
from collections import Counter
from openai import OpenAI
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
ROOT=pathlib.Path(__file__).resolve().parents[3]
PREREG=ROOT/'architect/evaluation/growth_strategy_experiment_portfolio/qualification-preregistration-v0.1.json'
BASE=ROOT/'architect/evaluation/growth_strategy_experiment_portfolio/sealed/heldout-v0.1-2026-08-22'
CONTEXT='growth-strategy-experiment-portfolio-v0.1-heldout-2026-08-22'
FAMILIES=['GS-BV','GS-BD','GS-EV','GS-MH','GS-AS','GS-PP','GS-ED','GS-MB','GS-CH','GS-CF','GS-LI','GS-BA']
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def derive(master:bytes)->bytes:
 raw=HKDF(algorithm=hashes.SHA256(),length=32,salt=b'professional-ai-agents/qualification-sealed-pack/v1',info=CONTEXT.encode()).derive(master); return base64.urlsafe_b64encode(raw)
def author(prompt:str)->dict:
 r=OpenAI().responses.create(model=os.environ.get('STRATEGIST_EVALUATOR_AUTHOR_MODEL','gpt-5.6-terra'),input=prompt,store=False); t=r.output_text or ''; a=t.find('{'); b=t.rfind('}')+1
 if a<0 or b<=a: raise RuntimeError('author did not return JSON'); return json.loads(t[a:b])
def runner()->bytes:
 s='''#!/usr/bin/env python3
import argparse,json,os,subprocess,sys
from collections import defaultdict
from openai import OpenAI
DIMS=['decision_correctness','evidence_calibration','mechanism_judgment','action_preservation','boundary_integrity']
def grade(prompt):
 r=OpenAI().responses.create(model=os.environ.get('STRATEGIST_GRADER_MODEL','gpt-5.6-terra'),input=prompt,store=False);t=r.output_text or '';a=t.find('{');b=t.rfind('}')+1;return json.loads(t[a:b])
def main():
 p=argparse.ArgumentParser();p.add_argument('--pack-dir',required=True);p.add_argument('--executor-cmd',required=True);p.add_argument('--out',required=True);a=p.parse_args();fx=json.load(open(a.pack_dir+'/fixtures.json'));gr=json.load(open(a.pack_dir+'/grader.json'));res=[]
 for x in fx:
  q=subprocess.run(a.executor_cmd,shell=True,input=json.dumps({'task':x['task']}),text=True,capture_output=True,timeout=180)
  if q.returncode: res.append({'id':x['id'],'family':x['family'],'pass':False,'critical':False});continue
  ans=json.loads(q.stdout).get('final_output','');g=grade('Grade this professional answer against the hidden reference. Return JSON only with scores 0-2 for '+','.join(DIMS)+', boolean critical_hard_fail, and pair_stance. Judge construct validity, not keywords.\\n'+json.dumps({'fixture':x,'reference':gr[x['id']],'answer':ans}))
  sc={d:int(g.get(d,0)) for d in DIMS};crit=bool(g.get('critical_hard_fail'));res.append({'id':x['id'],'family':x['family'],'pair_id':x.get('pair_id'),'pass':(not crit and min(sc.values())>=1),'critical':crit,'scores':sc,'pair_stance':g.get('pair_stance','')})
 fam={}
 for f in sorted(set(x['family'] for x in res)):
  rr=[x for x in res if x['family']==f and 'scores' in x];fam[f]={d:sum(x['scores'][d] for x in rr)/len(rr) for d in DIMS} if rr else {}
 pairs=defaultdict(list)
 for x in res:
  if x.get('pair_id'):pairs[x['pair_id']].append(x)
 flip=any(any(x.get('pair_stance')=='UNJUSTIFIED_FLIP' for x in rr) for rr in pairs.values() if len(rr)==2);hard=sum(int(x.get('critical',False)) for x in res);rate=sum(int(x.get('pass',False)) for x in res)/len(res)
 ok=hard==0 and rate>=.9 and not flip and all(v.get('decision_correctness',0)>=1.7 and v.get('boundary_integrity',0)>=1.7 and v.get('evidence_calibration',0)>=1.5 and v.get('mechanism_judgment',0)>=1.5 for v in fam.values())
 report={'cycle_id':'growth-strategy-experiment-portfolio-v0.1-heldout-2026-08-22','verdict':'PASS' if ok else 'REVISE','fixture_count':len(res),'fixture_pass_rate':rate,'critical_hard_fail_count':hard,'contrastive_unjustified_flip':flip,'family_scores':fam,'fixtures':[{'id':x['id'],'family':x['family'],'pass':x.get('pass',False),'critical':x.get('critical',False)} for x in res]};json.dump(report,open(a.out,'w'),indent=2);return 0 if ok else 10
if __name__=='__main__':sys.exit(main())
''';return s.encode()
def main():
 prereg=json.load(open(PREREG));master=os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY','').encode().strip()
 if not master or not os.environ.get('OPENAI_API_KEY','').strip():raise RuntimeError('required evaluator secrets missing')
 prompt='Create a fresh independent held-out pack for Growth Strategy & Experiment Portfolio Practitioner. Return JSON only with fixtures and grader. Exactly 24 fixtures, exactly 2 per family '+','.join(FAMILIES)+'. Each fixture has id,family,task,pair_id. Grader keyed by id with expected disposition, decisive evidence/judgment, failure traps, and pair-change rationale. Include contrastive pairs for proxy vs downstream value, comparability, outcome maturity, capacity, authority, confidence-without-evidence, and irrelevant wording stability. Authentic adversarial work samples only. Public preregistration: '+json.dumps(prereg)
 data=author(prompt);fx=data['fixtures'];gr=data['grader']
 if len(fx)!=24 or len(gr)!=24:raise RuntimeError('cardinality mismatch')
 fam=Counter(x.get('family') for x in fx);ids=[x.get('id') for x in fx]
 if set(fam)!=set(FAMILIES) or set(fam.values())!={2} or len(set(ids))!=24 or set(ids)!=set(gr):raise RuntimeError('structure mismatch')
 files={'fixtures.json':json.dumps(fx,separators=(',',':')).encode(),'grader.json':json.dumps(gr,separators=(',',':')).encode(),'runner.py':runner()}
 freeze={'candidate_commit':prereg['candidate']['commit'],'candidate_digest':prereg['candidate']['digest'],'model':'gpt-5.4-mini','fixtures_sha256':'sha256:'+sha(files['fixtures.json']),'grader_sha256':'sha256:'+sha(files['grader.json']),'runner_sha256':'sha256:'+sha(files['runner.py'])};canon=''.join(f'{n}:{sha(files[n])}\n' for n in sorted(files));freeze['pack_digest']='sha256:'+hashlib.sha256(canon.encode()).hexdigest();files['freeze-record.json']=json.dumps(freeze,sort_keys=True).encode()
 bio=io.BytesIO();
 with zipfile.ZipFile(bio,'w',zipfile.ZIP_DEFLATED) as z:
  for n,b in files.items():z.writestr(n,b)
 raw=bio.getvalue();key=derive(master);token=Fernet(key).encrypt(raw);partsdir=pathlib.Path(str(BASE)+'.parts');partsdir.mkdir(parents=True,exist_ok=True);parts=[token[i:i+3500] for i in range(0,len(token),3500)]
 for i,p in enumerate(parts):(partsdir/f'{i:02d}').write_bytes(p)
 m={'version':2,'cycle_id':CONTEXT,'candidate':{'commit':prereg['candidate']['commit'],'digest':prereg['candidate']['digest'],'manifest_path':prereg['candidate']['artifact_manifest']},'runtime':{'executor_path':'architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_openai.py','executor_cmd':'python3 architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_openai.py','protocol':'growth-strategy-experiment-portfolio-candidate-v1','provider':'openai-responses-api','model':'gpt-5.4-mini','credential_env':'OPENAI_API_KEY','candidate_timeout_seconds':180,'model_timeout_seconds':120,'workflow_timeout_seconds':1800,'contract_probe_argv':['python3','architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_openai.py','--qualification-contract'],'tool_protocol':'none-v1','state_protocol':'stateless-v1','observable_protocol':'final-output-only-v1','canary_required':True,'canary_cmd':'python3 architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_openai.py --canary'},'sealed_pack':{'parts_dir':str(partsdir.relative_to(ROOT)),'part_count':len(parts),'ciphertext_length':len(token),'ciphertext_sha256':sha(token),'key_derivation':{'scheme':'hkdf-sha256-v1','master_env':'QUALIFICATION_SEALED_PACK_MASTER_KEY','context':CONTEXT},'key_fingerprint_sha256':sha(key),'decrypted_zip_sha256':sha(raw),'pack_digest':freeze['pack_digest'],'required_files':['fixtures.json','grader.json','runner.py','freeze-record.json']},'evaluation':{'fixture_count':24,'family_count':12,'per_family':2,'fixtures_file':'fixtures.json','grader_file':'grader.json','runner_file':'runner.py','freeze_record_file':'freeze-record.json'},'report':{'sanitized_required':True,'artifact_required':True,'validator_path':'architect/evaluation/qualification-platform/validate_sanitized_report.py','release_ledger_required':True},'verdict':{'runner_exit_zero_required':True,'missing_report_is_failure':True,'report_validation_required':True,'artifact_upload_required':True}}
 pathlib.Path(str(BASE)+'.qualification.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'SEALED','parts':len(parts),'pack_digest':freeze['pack_digest']}))
if __name__=='__main__':main()
