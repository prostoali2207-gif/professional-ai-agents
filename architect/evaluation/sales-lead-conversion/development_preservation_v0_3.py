#!/usr/bin/env python3
"""Small public preservation sanity check for Sales 0.3.0.

This is not held-out qualification evidence. It checks four previously strong
professional mechanisms after the 0.3 boundary/security rewrite, using fresh
public scenarios and compact observable JSON decisions.
"""
from __future__ import annotations
import json, os, pathlib, urllib.request, urllib.error
MODEL_PATH=pathlib.Path('architect/library/cores/sales-lead-conversion/0.3.0/professional-model.md')
EVIDENCE_PATH=pathlib.Path('architect/library/cores/sales-lead-conversion/0.3.0/evidence-and-reuse.md')
MODEL=os.environ.get('SALES_MODEL','gpt-5.6-terra')
TIMEOUT=int(os.environ.get('SALES_MODEL_TIMEOUT_SECONDS','180'))
CASES=[
 {"id":"preserve-grounding","family":"commercial-fact-grounding","scenario":"A buyer asks the current price. An old ad says AED 51,900, model memory suggests AED 52,000, and the authoritative current inventory record for the exact VIN says AED 54,000 verified now.","expect":{"reported_price":54000,"use_old_or_memory":False}},
 {"id":"preserve-next-commitment","family":"next-commitment","scenario":"A buyer will consider visiting only if a transferable warranty applies. Warranty status is currently unknown; a visit slot is available. Choose the smallest sufficient next commitment.","expect":{"next_commitment":"verify_fact","appointment_now":False}},
 {"id":"preserve-supersession","family":"state-supersession","scenario":"A prior authoritative price AED 52,000 for the same VIN has been explicitly replaced by a current authoritative record AED 54,000. A draft reply still contains AED 52,000.","expect":{"current_value":54000,"old_superseded":True,"replan_required":True}},
 {"id":"preserve-intent","family":"intent-readiness","scenario":"Two buyers ask the same product question. Buyer A writes a long polite message with emojis but gives no timeframe or next-step signal. Buyer B briefly says they want the exact car this week and asks for a test drive. Assess which has stronger purchase-readiness evidence.","expect":{"stronger_intent":"B","demographic_or_style_signal_used":False}}
]
SCHEMA='''Return JSON only, no chain-of-thought, use null when not applicable:\n{"reported_price":number|null,"use_old_or_memory":boolean|null,"next_commitment":string|null,"appointment_now":boolean|null,"current_value":number|null,"old_superseded":boolean|null,"replan_required":boolean|null,"stronger_intent":string|null,"demographic_or_style_signal_used":boolean|null,"brief_reason":string}\nFor next_commitment use verify_fact, appointment, answer_fact, ask_question, handoff, follow_up, close, or other.'''
def call(c):
 key=os.environ.get('OPENAI_API_KEY')
 if not key: raise RuntimeError('OPENAI_API_KEY missing')
 core=MODEL_PATH.read_text()+"\n\n"+EVIDENCE_PATH.read_text()
 body={"model":MODEL,"store":False,"input":[{"role":"developer","content":[{"type":"input_text","text":"Apply this Sales / Lead Conversion 0.3.0 professional core exactly.\n\n"+core}]},{"role":"user","content":[{"type":"input_text","text":c['scenario']+"\n\n"+SCHEMA}]}]}
 req=urllib.request.Request('https://api.openai.com/v1/responses',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
 try:
  with urllib.request.urlopen(req,timeout=TIMEOUT) as r:p=json.loads(r.read())
 except urllib.error.HTTPError as e:raise RuntimeError(e.read().decode()[-1200:])
 text='\n'.join(part.get('text','') for item in p.get('output',[]) if item.get('type')=='message' for part in item.get('content',[]) if part.get('type')=='output_text').strip()
 if text.startswith('```'):
  text=text.strip('`')
  if text.startswith('json\n'):text=text[5:]
 return json.loads(text.strip()),p.get('usage') or {}
def norm_intent(v):
 s=str(v or '').strip().lower().replace('_',' ').replace('-',' ')
 if s in ('b','buyer b','buyerb'): return 'B'
 if s in ('a','buyer a','buyera'): return 'A'
 return str(v or '').strip()
def grade(c,d):
 f=[]
 for k,v in c['expect'].items():
  actual=d.get(k)
  if k=='stronger_intent': actual=norm_intent(actual)
  if actual!=v:f.append(k)
 return not f,f
def main():
 rows=[]; usage={'api_calls':0,'input_tokens':0,'cached_input_tokens':0,'output_tokens':0,'total_tokens':0}
 for c in CASES:
  try:
   d,u=call(c);ok,f=grade(c,d);usage['api_calls']+=1
   usage['input_tokens']+=int(u.get('input_tokens',0) or 0);usage['cached_input_tokens']+=int(((u.get('input_tokens_details') or {}).get('cached_tokens')) or 0);usage['output_tokens']+=int(u.get('output_tokens',0) or 0);usage['total_tokens']+=int(u.get('total_tokens',0) or 0)
   row={'id':c['id'],'family':c['family'],'pass':ok,'failures':f}
   if not ok:row['decision']=d
   rows.append(row)
  except Exception as exc:rows.append({'id':c['id'],'family':c['family'],'pass':False,'runtime_error':str(exc)[-1000:]})
 passed=sum(bool(r.get('pass')) for r in rows);result={'development_only':True,'candidate':'sales-lead-conversion/0.3.0 working tree','planned':len(CASES),'passed':passed,'model':MODEL,'rows':rows,'usage':usage};print(json.dumps(result,indent=2));return 0 if passed==len(CASES) else 1
if __name__=='__main__':raise SystemExit(main())
