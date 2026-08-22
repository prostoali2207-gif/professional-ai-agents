#!/usr/bin/env python3
from __future__ import annotations
import base64, hashlib, io, json, os, pathlib, urllib.request, zipfile
from collections import Counter
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

ROOT=pathlib.Path(__file__).resolve().parents[3]
PREREG=ROOT/'architect/evaluation/growth_strategy_experiment_portfolio/qualification-preregistration-v0.1.json'
OUT=ROOT/'architect/evaluation/growth_strategy_experiment_portfolio/sealed/heldout-v0.1-2026-08-22'
CONTEXT='growth-strategy-experiment-portfolio-v0.1-heldout-2026-08-22'
MODEL=os.environ.get('STRATEGIST_EVALUATOR_AUTHOR_MODEL','gpt-5.6-terra')
FAMILIES=['GS-BV','GS-BD','GS-EV','GS-MH','GS-AS','GS-PP','GS-ED','GS-MB','GS-CH','GS-CF','GS-LI','GS-BA']

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def derive(master:bytes)->bytes:
    raw=HKDF(algorithm=hashes.SHA256(),length=32,salt=b'professional-ai-agents/qualification-sealed-pack/v1',info=CONTEXT.encode()).derive(master)
    return base64.urlsafe_b64encode(raw)

def call_author(prompt:str)->dict:
    key=os.environ['OPENAI_API_KEY'].strip()
    req=urllib.request.Request('https://api.openai.com/v1/responses',method='POST',headers={'Authorization':f'Bearer {key}','Content-Type':'application/json'},data=json.dumps({'model':MODEL,'input':prompt}).encode())
    with urllib.request.urlopen(req,timeout=240) as r: raw=json.load(r)
    text=raw.get('output_text')
    if not text:
        parts=[]
        for item in raw.get('output',[]):
            for c in item.get('content',[]):
                if c.get('type')=='output_text': parts.append(c.get('text',''))
        text=''.join(parts)
    start=text.find('{'); end=text.rfind('}')+1
    if start<0 or end<=start: raise RuntimeError('author did not return JSON object')
    return json.loads(text[start:end])

def runner_source()->str:
    return '''#!/usr/bin/env python3
import argparse,json,os,subprocess,urllib.request,collections,sys

def call_grader(model,prompt):
 key=os.environ['OPENAI_API_KEY'].strip(); req=urllib.request.Request('https://api.openai.com/v1/responses',method='POST',headers={'Authorization':f'Bearer {key}','Content-Type':'application/json'},data=json.dumps({'model':model,'input':prompt}).encode())
 with urllib.request.urlopen(req,timeout=180) as r: raw=json.load(r)
 t=raw.get('output_text') or ''.join(c.get('text','') for i in raw.get('output',[]) for c in i.get('content',[]) if c.get('type')=='output_text'); a=t.find('{'); b=t.rfind('}')+1; return json.loads(t[a:b])

def main():
 p=argparse.ArgumentParser();p.add_argument('--pack-dir',required=True);p.add_argument('--executor-cmd',required=True);p.add_argument('--model',required=True);p.add_argument('--grader-model',default='gpt-5.6-terra');p.add_argument('--out',required=True);a=p.parse_args()
 fixtures=json.load(open(a.pack_dir+'/fixtures.json')); grader=json.load(open(a.pack_dir+'/grader.json')); results=[]; hard=0
 for fx in fixtures:
  proc=subprocess.run(a.executor_cmd,shell=True,input=json.dumps({'task':fx['task']}),text=True,capture_output=True,timeout=180)
  if proc.returncode: results.append({'id':fx['id'],'family':fx['family'],'pass':False,'runtime_error':True}); continue
  env=json.loads(proc.stdout); answer=env.get('final_output','')
  gp='''+repr('You are an independent professional evaluator. Grade the candidate answer against the hidden reference. Return JSON only with integer scores 0-2 for decision_correctness,evidence_calibration,mechanism_judgment,action_preservation,boundary_integrity; boolean critical_hard_fail; string pair_stance; short rationale. Do not reward keyword overlap; judge professional construct validity.\n')+'''+json.dumps({'fixture':fx,'reference':grader[fx['id']],'candidate_answer':answer})
  g=call_grader(a.grader_model,gp); crit=bool(g.get('critical_hard_fail')); hard+=int(crit); scores={k:int(g.get(k,0)) for k in ['decision_correctness','evidence_calibration','mechanism_judgment','action_preservation','boundary_integrity']}; passed=(not crit and min(scores.values())>=1)
  results.append({'id':fx['id'],'family':fx['family'],'pair_id':fx.get('pair_id'),'pass':passed,'critical':crit,'scores':scores,'pair_stance':g.get('pair_stance','')})
 fam={}
 for f in sorted(set(x['family'] for x in results)):
  rr=[x for x in results if x['family']==f and 'scores' in x]; fam[f]={k:sum(x['scores'][k] for x in rr)/len(rr) for k in ['decision_correctness','evidence_calibration','mechanism_judgment','action_preservation','boundary_integrity']} if rr else {}
 pairflip=False
 pairs=collections.defaultdict(list)
 for x in results:
  if x.get('pair_id'): pairs[x['pair_id']].append(x)
 for _,rr in pairs.items():
  if len(rr)==2 and any(x.get('pair_stance')=='UNJUSTIFIED_FLIP' for x in rr): pairflip=True
 rate=sum(x.get('pass',False) for x in results)/len(results)
 release=hard==0 and rate>=0.9 and not pairflip and all(v.get('decision_correctness',0)>=1.7 and v.get('boundary_integrity',0)>=1.7 and v.get('evidence_calibration',0)>=1.5 and v.get('mechanism_judgment',0)>=1.5 for v in fam.values())
 report={'cycle_id':'growth-strategy-experiment-portfolio-v0.1-heldout-2026-08-22','verdict':'PASS' if release else 'REVISE','fixture_count':len(results),'fixture_pass_rate':rate,'critical_hard_fail_count':hard,'contrastive_unjustified_flip':pairflip,'family_scores':fam,'fixtures':[{'id':x['id'],'family':x['family'],'pass':x.get('pass',False),'critical':x.get('critical',False)} for x in results]}
 json.dump(report,open(a.out,'w'),indent=2);print(json.dumps({'verdict':report['verdict'],'fixture_pass_rate':rate,'critical_hard_fail_count':hard}));return 0 if release else 10
if __name__=='__main__':sys.exit(main())
'''

def main():
 prereg=json.load(open(PREREG)); master=os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY','').encode().strip(); api=os.environ.get('OPENAI_API_KEY','').strip()
 if not master or not api: raise RuntimeError('required evaluator secrets missing')
 prompt='''Create a fresh independent held-out qualification pack for a Growth Strategy & Experiment Portfolio Practitioner. Return JSON only: {"fixtures":[...],"grader":{...}}. Exactly 24 fixtures; exactly 2 for each family GS-BV,GS-BD,GS-EV,GS-MH,GS-AS,GS-PP,GS-ED,GS-MB,GS-CH,GS-CF,GS-LI,GS-BA. Every fixture: id, family, task, pair_id (nullable). Grader object keyed by fixture id; each reference contains expected professional disposition, decisive evidence/judgment, forbidden failure traps, and whether a stance change across its contrastive pair is justified. Include the preregistered contrastive requirements across the 24 cases. Cases must be authentic work samples, adversarial, fresh, and must not rely on keyword matching. Do not reveal or reuse candidate wording. Public preregistration follows:\n'''+json.dumps(prereg,ensure_ascii=False)
 data=call_author(prompt); fixtures=data['fixtures']; grader=data['grader']
 if len(fixtures)!=24 or len(grader)!=24: raise RuntimeError('cardinality mismatch')
 fam=Counter(x.get('family') for x in fixtures)
 if set(fam)!=set(FAMILIES) or set(fam.values())!={2}: raise RuntimeError('family structure mismatch')
 ids=[x.get('id') for x in fixtures]
 if None in ids or len(set(ids))!=24 or set(ids)!=set(grader): raise RuntimeError('id mismatch')
 files={'fixtures.json':json.dumps(fixtures,ensure_ascii=False,separators=(',',':')).encode(),'grader.json':json.dumps(grader,ensure_ascii=False,separators=(',',':')).encode(),'runner.py':runner_source().encode()}
 freeze={'candidate_commit':prereg['candidate']['commit'],'candidate_digest':prereg['candidate']['digest'],'model':'gemini-3.5-flash-lite','fixtures_sha256':'sha256:'+sha(files['fixtures.json']),'grader_sha256':'sha256:'+sha(files['grader.json']),'runner_sha256':'sha256:'+sha(files['runner.py'])}
 canonical=''.join(f'{n}:{sha(files[n])}\n' for n in sorted(files)); freeze['pack_digest']='sha256:'+hashlib.sha256(canonical.encode()).hexdigest(); files['freeze-record.json']=json.dumps(freeze,indent=2,sort_keys=True).encode()
 bio=io.BytesIO();
 with zipfile.ZipFile(bio,'w',zipfile.ZIP_DEFLATED) as z:
  for n,b in files.items(): z.writestr(n,b)
 raw=bio.getvalue(); key=derive(master); token=Fernet(key).encrypt(raw); OUT.mkdir(parents=True,exist_ok=True)
 chunk=3500; parts=[token[i:i+chunk] for i in range(0,len(token),chunk)]
 for i,p in enumerate(parts):(OUT/f'{i:02d}').write_bytes(p)
 manifest={'version':2,'cycle_id':CONTEXT,'candidate':{'commit':prereg['candidate']['commit'],'digest':prereg['candidate']['digest'],'manifest_path':prereg['candidate']['artifact_manifest']},'runtime':{'executor_path':'architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py','executor_cmd':'python3 architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py','protocol':'growth-strategy-experiment-portfolio-candidate-v1','provider':'gemini-interactions-api','model':'gemini-3.5-flash-lite','credential_env':'GEMINI_API_KEY','candidate_timeout_seconds':180,'model_timeout_seconds':120,'workflow_timeout_seconds':1800,'contract_probe_argv':['python3','architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py','--qualification-contract'],'tool_protocol':'none-v1','state_protocol':'stateless-v1','observable_protocol':'final-output-only-v1','canary_required':True,'canary_cmd':'python3 architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py --canary'},'sealed_pack':{'parts_dir':str(OUT.relative_to(ROOT))+'.parts','part_count':len(parts),'ciphertext_length':len(token),'ciphertext_sha256':sha(token),'key_derivation':{'scheme':'hkdf-sha256-v1','master_env':'QUALIFICATION_SEALED_PACK_MASTER_KEY','context':CONTEXT},'key_fingerprint_sha256':sha(key),'decrypted_zip_sha256':sha(raw),'pack_digest':freeze['pack_digest'],'required_files':['fixtures.json','grader.json','runner.py','freeze-record.json']},'evaluation':{'fixture_count':24,'family_count':12,'per_family':2,'fixtures_file':'fixtures.json','grader_file':'grader.json','runner_file':'runner.py','freeze_record_file':'freeze-record.json'},'report':{'sanitized_required':True,'artifact_required':True,'validator_path':'architect/evaluation/qualification-platform/validate_sanitized_report.py','release_ledger_required':True},'verdict':{'runner_exit_zero_required':True,'missing_report_is_failure':True,'report_validation_required':True,'artifact_upload_required':True}}
 # parts live in sibling .parts directory expected by platform
 partsdir=pathlib.Path(str(OUT)+'.parts'); partsdir.mkdir(parents=True,exist_ok=True)
 for i,p in enumerate(parts):(partsdir/f'{i:02d}').write_bytes(p)
 (pathlib.Path(str(OUT)+'.qualification.json')).write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'SEALED','fixture_count':24,'family_count':12,'part_count':len(parts),'pack_digest':freeze['pack_digest']}))
if __name__=='__main__': main()
