#!/usr/bin/env python3
import json,os,subprocess,sys
req={'task':'Unscored runtime canary. State only that this is a runtime check; do not invent customer evidence, guarantees, urgency, or conversion-lift claims.','context':{'canary':True},'constraints':['No commercial claim.']}
p=subprocess.run([sys.executable,'architect/evaluation/conversion_messaging_web_copy/executor_v0_1_gemini.py'],input=json.dumps(req),text=True,capture_output=True,env={**os.environ,'MESSAGING_MODEL':os.environ.get('MESSAGING_MODEL','gemini-3.5-flash-lite')},timeout=180)
if p.returncode!=0:
 print(p.stderr,file=sys.stderr); raise SystemExit(2)
x=json.loads(p.stdout)
assert x['candidate_identity']['commit']=='7019f6717b1b61806f4a221a297d049a4ad3b8cb'
assert x['candidate_identity']['artifact_digest']=='sha256:da7662f95dcf132d9a9875849b7bb5d5d831d1d54821f0b109b543a1f299e1d2'
assert x['runtime_identity']['provider']=='gemini-interactions-api'
assert x['model_usage']['api_calls']==1
print(json.dumps({'status':'PASS','provider':'gemini-interactions-api','model':x['runtime_identity']['model'],'api_calls':1}))
