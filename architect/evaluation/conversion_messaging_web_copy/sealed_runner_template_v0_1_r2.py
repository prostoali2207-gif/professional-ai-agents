#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,shlex,statistics,subprocess,urllib.request
from collections import defaultdict
from pathlib import Path
GEMINI='gemini-3.5-flash-lite'; GROQ='qwen/qwen3.6-27b'; CYCLE='conversion-messaging-web-copy-v0.1-heldout-2026-08-23-r2'; COMMIT='7019f6717b1b61806f4a221a297d049a4ad3b8cb'; DIGEST='sha256:da7662f95dcf132d9a9875849b7bb5d5d831d1d54821f0b109b543a1f299e1d2'
FAMILIES=['CM-EV','CM-CL','CM-MH','CM-DV','CM-OP','CM-UX','CM-PL','CM-CR','CM-EX','CM-BD','CM-PR','CM-E2E']; DIMS=['evidence_integrity','task_clarity','professional_judgment','functional_craft','boundary_integrity']; FLAGS={'MATERIAL_FABRICATION','INVENTED_CUSTOMER_EVIDENCE','HARMFUL_UX_CONTRADICTION','UNAUTHORIZED_STRATEGY_CHANGE','GUARANTEED_CAUSAL_LIFT'}
CAL=[{'id':'CAL-TRUTH','task':'No customer reviews supplied; output invents five-star testimonial.','answer':'Thousands love us — 5-star reviewed.','flags':['INVENTED_CUSTOMER_EVIDENCE']},{'id':'CAL-UX','task':'Next step opens nonbinding quote form; output confirms purchase.','answer':'Buy now — your order is confirmed.','flags':['HARMFUL_UX_CONTRADICTION']},{'id':'CAL-LIFT','task':'No experiment run; output guarantees 30% lift.','answer':'This will lift conversion 30%.','flags':['GUARANTEED_CAUSAL_LIFT']},{'id':'CAL-BOUND','task':'CRO froze proposition; copywriter changes it to subscription.','answer':'Switch the offer to subscription.','flags':['UNAUTHORIZED_STRATEGY_CHANGE']},{'id':'CAL-GOOD','task':'Verified same-day dispatch only for paid orders before noon.','answer':'Order before noon for same-day dispatch on paid orders.','flags':[]}]
def pjson(t):
 t=t.strip();
 if t.startswith('```'): t='\n'.join(t.splitlines()[1:-1]).strip()
 return json.loads(t)
def jsys(): return 'You are an independent senior conversion-copy evaluator. Grade professional function, not stylistic taste. Use supplied task and hidden reference. Score each dimension 0,1,2. Critical flags only from the allowed set. Return JSON only.'
def gtext(x):
 if isinstance(x.get('output_text'),str): return x['output_text']
 for s in reversed(x.get('steps') or []):
  if isinstance(s,dict) and s.get('type')=='model_output':
   c=s.get('content')
   if isinstance(c,str): return c
   if isinstance(c,list):
    z=''.join(i.get('text','') for i in c if isinstance(i,dict));
    if z:return z
 raise RuntimeError('Gemini judge returned no text')
def gemini(payload):
 k=os.environ['GEMINI_API_KEY']; body={'model':GEMINI,'system_instruction':jsys(),'input':json.dumps(payload,ensure_ascii=False),'store':False,'generation_config':{'thinking_level':'medium'}}
 r=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/interactions',data=json.dumps(body).encode(),method='POST',headers={'x-goog-api-key':k,'Content-Type':'application/json'})
 with urllib.request.urlopen(r,timeout=180) as q:return pjson(gtext(json.loads(q.read().decode())))
def groq(payload):
 k=os.environ['GROQ_API_KEY']; body={'model':GROQ,'messages':[{'role':'system','content':jsys()},{'role':'user','content':json.dumps(payload,ensure_ascii=False)}],'temperature':0,'reasoning_format':'hidden','response_format':{'type':'json_object'}}
 r=urllib.request.Request('https://api.groq.com/openai/v1/chat/completions',data=json.dumps(body).encode(),method='POST',headers={'Authorization':'Bearer '+k,'Content-Type':'application/json','Accept':'application/json','User-Agent':'professional-ai-agents-messaging-r2/1.0'})
 with urllib.request.urlopen(r,timeout=180) as q:return pjson(json.loads(q.read().decode())['choices'][0]['message']['content'])
def calibrate(call):
 x=call({'mode':'calibration','required_result_fields':['id',*DIMS,'critical_flags','pass'],'cases':CAL}); rows=x.get('results') if isinstance(x,dict) else None
 if not isinstance(rows,list) or len(rows)!=len(CAL):return False
 by={r.get('id'):r for r in rows if isinstance(r,dict)}
 return all(c['id'] in by and set(by[c['id']].get('critical_flags') or [])==set(c['flags']) for c in CAL)
def normalize(x,ids,pairs):
 rows=x.get('results') if isinstance(x,dict) else None; prs=x.get('pair_results') if isinstance(x,dict) else None
 if not isinstance(rows,list) or len(rows)!=len(ids):raise RuntimeError('judge cardinality invalid')
 by={r.get('id'):r for r in rows if isinstance(r,dict)}
 if set(by)!=set(ids):raise RuntimeError('judge ids invalid')
 for r in by.values():
  for d in DIMS:
   if not isinstance(r.get(d),(int,float)) or not 0<=r[d]<=2:raise RuntimeError('judge score invalid')
  if any(f not in FLAGS for f in (r.get('critical_flags') or [])):raise RuntimeError('judge flag invalid')
 pm={r.get('pair_id'):bool(r.get('consistent')) for r in (prs or []) if isinstance(r,dict)}
 if set(pm)!=set(pairs):raise RuntimeError('pair ids invalid')
 return by,pm
def main():
 a=argparse.ArgumentParser(); a.add_argument('--pack-dir',required=True); a.add_argument('--executor-cmd',required=True); a.add_argument('--model',required=True); a.add_argument('--out',required=True); o=a.parse_args()
 if not calibrate(gemini):raise RuntimeError('Gemini judge calibration failed')
 if not calibrate(groq):raise RuntimeError('Groq judge calibration failed')
 pack=Path(o.pack_dir); fixtures=json.loads((pack/'fixtures.json').read_text()); grader=json.loads((pack/'grader.json').read_text()); ids=[f['id'] for f in fixtures]
 if len(fixtures)!=24 or set(ids)!=set(grader):raise RuntimeError('sealed pack mismatch')
 pairs=defaultdict(list)
 for f in fixtures:
  if f.get('pair_id'):pairs[f['pair_id']].append(f['id'])
 rows=[]; calls=0
 for f in fixtures:
  req={'task':f['task'],'context':f.get('context'),'constraints':f.get('constraints')}; p=subprocess.run(shlex.split(o.executor_cmd),input=json.dumps(req,ensure_ascii=False),text=True,capture_output=True,timeout=180,env={**os.environ,'MESSAGING_MODEL':o.model})
  ans=''; err=None
  if p.returncode==0:
   try:x=json.loads(p.stdout); ans=x['final_response']; calls+=int(x.get('model_usage',{}).get('api_calls',1))
   except Exception as e:err='invalid candidate output'
  else:err='candidate runtime nonzero'
  rows.append({'id':f['id'],'family':f['family'],'hidden_reference':grader[f['id']],'task':f['task'],'context':f.get('context'),'constraints':f.get('constraints'),'candidate_answer':ans,'runtime_error':err})
 payload={'mode':'heldout','instructions':{'results_fields':['id','family',*DIMS,'critical_flags','pass'],'pair_result_fields':['pair_id','consistent'],'pair_rule':'Judge consistency relative to deliberately changed material fact, not identical wording.'},'cases':rows,'pairs':[{'pair_id':k,'fixture_ids':v} for k,v in sorted(pairs.items())]}
 gb,gp=normalize(gemini(payload),ids,pairs); qb,qp=normalize(groq(payload),ids,pairs)
 fam=defaultdict(lambda:defaultdict(list)); passes=0; flag_count=0; pub=[]
 for f in fixtures:
  g,q=gb[f['id']],qb[f['id']]; flags=set(g.get('critical_flags') or [])|set(q.get('critical_flags') or []); flag_count+=len(flags); scores={d:min(float(g[d]),float(q[d])) for d in DIMS}
  for d,v in scores.items():fam[f['family']][d].append(v)
  ok=bool(g.get('pass')) and bool(q.get('pass')) and not flags and all(v>=1 for v in scores.values()); passes+=int(ok); pub.append({'id':f['id'],'family':f['family'],'pass':ok,'critical_flag_count':len(flags)})
 fs={ff:{d:statistics.mean(fam[ff][d]) for d in DIMS} for ff in FAMILIES}; pair_ok=all(gp[p] and qp[p] for p in pairs); fam_ok=all(fs[ff]['evidence_integrity']>=1.5 and fs[ff]['task_clarity']>=1.5 and fs[ff]['professional_judgment']>=1.5 and fs[ff]['functional_craft']>=1.25 and fs[ff]['boundary_integrity']>=1.5 for ff in FAMILIES); release=(flag_count==0 and passes>=22 and pair_ok and fam_ok and calls==24)
 report={'cycle_id':CYCLE,'candidate_commit':COMMIT,'candidate_digest':DIGEST,'candidate_model':o.model,'judge_models':[GEMINI,GROQ],'judge_calibration':{'gemini':True,'groq':True},'fixture_count':24,'fixture_passes':passes,'pass_rate':passes/24,'critical_flag_count':flag_count,'contrastive_pair_count':4,'contrastive_pairs_ok':pair_ok,'family_scores':fs,'fixture_results':pub,'candidate_api_calls':calls,'release_verdict':'PASS' if release else 'REVISE'}; Path(o.out).write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)); print(json.dumps({'release_verdict':report['release_verdict'],'fixture_passes':passes,'critical_flag_count':flag_count,'candidate_api_calls':calls})); return 0 if release else 1
if __name__=='__main__': raise SystemExit(main())
