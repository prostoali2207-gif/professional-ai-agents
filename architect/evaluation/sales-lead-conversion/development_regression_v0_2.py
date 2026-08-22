#!/usr/bin/env python3
"""Public development regression for Sales core 0.2.0.

This is development evidence only. It uses novel public cases derived from the
professional failure families, not hidden qualification fixtures. The model is
asked for a compact JSON professional decision so mechanically observable
invariants can be graded without exposing chain-of-thought.
"""
from __future__ import annotations
import json, os, pathlib, urllib.request, urllib.error

MODEL_PATH=pathlib.Path('architect/library/cores/sales-lead-conversion/0.2.0/professional-model.md')
EVIDENCE_PATH=pathlib.Path('architect/library/cores/sales-lead-conversion/0.2.0/evidence-and-reuse.md')
MODEL=os.environ.get('SALES_MODEL','gpt-5.6-terra')
TIMEOUT=int(os.environ.get('SALES_MODEL_TIMEOUT_SECONDS','180'))

CASES=[
 {"id":"own-pure-complaint","family":"ownership-community-boundary","scenario":"A customer posts: 'Your service team damaged my previous car. I only mention the Yaris because that's what I was driving. Fix the complaint.' There is no request to buy another vehicle.","expect":{"primary_owner_in":["support","community","reputation"],"sales_progression_allowed":False}},
 {"id":"own-mixed-workstreams","family":"ownership-community-boundary","scenario":"A customer says: 'Your service team still owes me an answer about damage to my old car. Separately, I am considering buying the 2026 Yaris next week. Can you tell me what I should do?' The complaint is unresolved.","expect":{"mixed":True,"complaint_owner_in":["support","community","reputation"],"purchase_owner":"sales","sales_must_not_resolve_complaint":True}},
 {"id":"own-existing-owner","family":"ownership-community-boundary","scenario":"Support is already handling a customer's refund complaint. The same customer asks Sales about another car but also asks Sales to promise the refund outcome so they do not have to wait for Support.","expect":{"duplicate_owner":False,"refund_promise_by_sales":False}},
 {"id":"next-prerequisite-first","family":"next-commitment","scenario":"Buyer is interested in a vehicle but says the deciding issue is whether an advertised warranty still applies. The warranty status is not verified. A dealership visit is possible, but the buyer says they will only visit if the warranty applies.","expect":{"recommended":"verify_fact","appointment_now":False}},
 {"id":"next-ready-appointment","family":"next-commitment","scenario":"Buyer has already selected the exact vehicle, current price and availability are verified, location is known, prerequisites are satisfied, and the buyer explicitly asks to come tomorrow for a test drive.","expect":{"recommended":"appointment","ask_extra_qualification":False}},
 {"id":"next-smallest-sufficient","family":"next-commitment","scenario":"Buyer compares two verified cars and asks only which one has the larger boot because that decides their choice. Both boot capacities are already verified. A call and appointment are also available.","expect":{"recommended":"answer_fact","appointment_now":False}},
 {"id":"state-authoritative-replacement","family":"state-supersession","scenario":"CRM state stores price AED 52,000 from yesterday. The current authoritative inventory system explicitly states that the same vehicle's price is now AED 54,000 and replaces the previous price.","expect":{"current_value":54000,"old_superseded":True,"reconfirm_required":False}},
 {"id":"state-newer-weaker","family":"state-supersession","scenario":"The authoritative inventory system currently says AED 54,000. A newer customer message says 'I heard online it is 49,000' but provides no authoritative source.","expect":{"current_value":54000,"overwrite_by_recency":False,"conflict_or_verify":True}},
 {"id":"state-different-scope","family":"state-supersession","scenario":"System record says Vehicle A costs AED 54,000. A later authoritative record says Vehicle B costs AED 49,000. Names are similar but VINs differ.","expect":{"preserve_both":True,"supersession":False}},
 {"id":"state-dependent-replan","family":"state-supersession","scenario":"A draft reply and follow-up were prepared using an old authoritative price of AED 52,000. Before sending, the authoritative system explicitly replaces the price with AED 54,000 for the same vehicle.","expect":{"current_value":54000,"replan_required":True,"old_draft_safe_to_send":False}}
]

SCHEMA="""Return JSON only with these keys (use null when not applicable):
{
  "primary_owner": string|null,
  "mixed": boolean|null,
  "owner_by_workstream": object|null,
  "sales_progression_allowed": boolean|null,
  "sales_must_not_resolve_complaint": boolean|null,
  "duplicate_owner": boolean|null,
  "refund_promise_by_sales": boolean|null,
  "recommended_next_commitment": string|null,
  "appointment_now": boolean|null,
  "ask_extra_qualification": boolean|null,
  "current_value": number|null,
  "old_superseded": boolean|null,
  "reconfirm_required": boolean|null,
  "overwrite_by_recency": boolean|null,
  "conflict_or_verify": boolean|null,
  "preserve_both": boolean|null,
  "supersession": boolean|null,
  "replan_required": boolean|null,
  "old_draft_safe_to_send": boolean|null,
  "brief_reason": string
}
For recommended_next_commitment use one of: verify_fact, appointment, answer_fact, ask_question, specialist_handoff, follow_up, close, other.
For owner labels use sales/support/community/reputation or another concise role name.
Do not include chain-of-thought."""

def call(case):
 key=os.environ.get('OPENAI_API_KEY')
 if not key: raise RuntimeError('OPENAI_API_KEY missing')
 core=MODEL_PATH.read_text()+"\n\n"+EVIDENCE_PATH.read_text()
 body={"model":MODEL,"store":False,"input":[
  {"role":"developer","content":[{"type":"input_text","text":"You are the Sales / Lead Conversion 0.2.0 development candidate. Follow this professional core exactly.\n\n"+core}]},
  {"role":"user","content":[{"type":"input_text","text":case['scenario']+"\n\n"+SCHEMA}]}
 ]}
 req=urllib.request.Request('https://api.openai.com/v1/responses',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
 try:
  with urllib.request.urlopen(req,timeout=TIMEOUT) as r: p=json.loads(r.read())
 except urllib.error.HTTPError as e: raise RuntimeError(e.read().decode()[-1500:])
 texts=[]
 for item in p.get('output',[]):
  if item.get('type')=='message':
   for part in item.get('content',[]):
    if part.get('type')=='output_text': texts.append(part.get('text',''))
 text='\n'.join(texts).strip()
 if text.startswith('```'):
  text=text.strip('`').replace('json\n','',1).strip()
 return json.loads(text),p.get('usage') or {}

def norm_owner(v):
 s=str(v or '').lower()
 for x in ('support','community','reputation','sales'):
  if x in s:return x
 return s

def owner_for_workstream(obw, needles):
 if not isinstance(obw,dict): return ''
 for k,v in obw.items():
  lk=str(k).lower()
  if any(n in lk for n in needles): return norm_owner(v)
 return ''

def grade(case,d):
 e=case['expect']; failures=[]
 if 'primary_owner_in' in e and norm_owner(d.get('primary_owner')) not in e['primary_owner_in']: failures.append('primary_owner')
 if 'sales_progression_allowed' in e and d.get('sales_progression_allowed') is not e['sales_progression_allowed']: failures.append('sales_progression_allowed')
 if e.get('mixed') is True and d.get('mixed') is not True: failures.append('mixed')
 if 'complaint_owner_in' in e:
  owner=owner_for_workstream(d.get('owner_by_workstream'),('complaint','support','reputation','service'))
  if owner not in e['complaint_owner_in']: failures.append('complaint_owner')
 if 'purchase_owner' in e:
  owner=owner_for_workstream(d.get('owner_by_workstream'),('purchase','sales','commercial','buy'))
  if owner != e['purchase_owner']: failures.append('purchase_owner')
 for k in ('sales_must_not_resolve_complaint','duplicate_owner','refund_promise_by_sales','appointment_now','ask_extra_qualification','old_superseded','reconfirm_required','overwrite_by_recency','conflict_or_verify','preserve_both','supersession','replan_required','old_draft_safe_to_send'):
  if k in e and d.get(k) is not e[k]: failures.append(k)
 if 'recommended' in e and d.get('recommended_next_commitment') != e['recommended']: failures.append('recommended_next_commitment')
 if 'current_value' in e and d.get('current_value') != e['current_value']: failures.append('current_value')
 return not failures,failures

def main():
 rows=[]; totals={'input_tokens':0,'cached_input_tokens':0,'output_tokens':0,'total_tokens':0,'api_calls':0}
 for c in CASES:
  try:
   d,u=call(c); ok,failures=grade(c,d)
   totals['api_calls']+=1
   for k in ('input_tokens','cached_input_tokens','output_tokens','total_tokens'):
    if k=='cached_input_tokens': totals[k]+=int(((u.get('input_tokens_details') or {}).get('cached_tokens')) or 0)
    else: totals[k]+=int(u.get(k,0) or 0)
   row={'id':c['id'],'family':c['family'],'pass':ok,'failures':failures}
   if not ok: row['decision']=d
   rows.append(row)
  except Exception as exc:
   rows.append({'id':c['id'],'family':c['family'],'pass':False,'runtime_error':str(exc)[-1000:]})
 result={'development_only':True,'candidate':'sales-lead-conversion/0.2.0 working tree','model':MODEL,'planned':len(CASES),'passed':sum(r['pass'] for r in rows),'rows':rows,'usage':totals}
 print(json.dumps(result,indent=2))
 return 0 if result['passed']==len(CASES) else 1
if __name__=='__main__': raise SystemExit(main())
