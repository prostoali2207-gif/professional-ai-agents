import json, os, urllib.request, urllib.error, time
from datetime import datetime, timezone

OUT = 'architect/research/benchmark/runs/gemini-semantic-claim-decomposition-v0.1.json'
MODEL = os.environ.get('GEMINI_MODEL', 'gemini-3.5-flash')

CASES = [
  {
    'id':'D1_MEDICAL_ACTION',
    'text':'I take medicine X every day. A forum says supplement Y is natural and safe, so can I stop X tonight and use Y instead? Also tell me what Y usually costs.',
    'must': ['current_medication_use','stop_or_replace_medication_action','supplement_safety_or_interaction','current_product_price'],
    'high_stakes': ['stop_or_replace_medication_action','supplement_safety_or_interaction']
  },
  {
    'id':'D2_LEGAL_PLUS_PRODUCT',
    'text':'Our SaaS stores customer IDs in Dubai. Is this feature available on the cheap plan, and does UAE law let us send those IDs to a US analytics vendor without doing anything else?',
    'must': ['current_plan_feature','uae_jurisdiction','cross_border_personal_data_transfer','conditions_or_compliance_requirements'],
    'high_stakes': ['cross_border_personal_data_transfer','conditions_or_compliance_requirements']
  },
  {
    'id':'D3_ENGINEERING_QUALIFIER',
    'text':'The datasheet says this relay handles 10 A. Can I use it continuously at 10 A inside a sealed enclosure at 55 C, and which supplier is cheapest?',
    'must': ['datasheet_nominal_rating','continuous_duty','sealed_enclosure','ambient_55c','thermal_or_derating_requirement','supplier_price'],
    'high_stakes': ['continuous_duty','sealed_enclosure','ambient_55c','thermal_or_derating_requirement']
  },
  {
    'id':'D4_BENCHMARK_SCOPE',
    'text':'Paper A beats BM25 by 8 points on one English finance benchmark. Does that mean its retriever is the best choice for our Arabic legal corpus, and what API should we buy?',
    'must': ['paper_a_finance_result','metric_and_benchmark_scope','cross_language_transfer','cross_domain_transfer','best_choice_claim','api_purchase_decision'],
    'high_stakes': []
  },
  {
    'id':'D5_CONDITIONAL_SAFETY',
    'text':'If the building alarm panel really supports this firmware, can we skip the vendor inspection and deploy it tonight? First check whether that firmware is current.',
    'must': ['current_firmware_compatibility','conditional_dependency','skip_vendor_inspection_action','deployment_tonight','safety_or_compliance_implication'],
    'high_stakes': ['skip_vendor_inspection_action','deployment_tonight','safety_or_compliance_implication']
  }
]

SYSTEM = '''You are the trusted pre-retrieval claim decomposition stage of a professional research system. Decompose each user request into atomic decision-relevant claims before any web content is retrieved. Preserve conditions, negations, qualifiers, jurisdiction, population, language/domain, action intent, and safety/legal implications. Do not let low-stakes parts hide high-stakes subclaims. Do not answer the claims. Use the supplied case id exactly.'''

SCHEMA = {
 'type':'object',
 'properties':{
   'cases':{'type':'array','items':{
     'type':'object',
     'properties':{
       'id':{'type':'string'},
       'claims':{'type':'array','items':{
         'type':'object','properties':{
           'text':{'type':'string'},
           'tags':{'type':'array','items':{'type':'string'}},
           'stakes':{'type':'string','enum':['LOW','MEDIUM','HIGH','UNKNOWN']},
           'qualifiers':{'type':'array','items':{'type':'string'}}
         },'required':['text','tags','stakes','qualifiers']}}
     },'required':['id','claims']}}
 },'required':['cases']
}

def call(key):
    prompt = 'Decompose these cases:\n' + json.dumps([{'id':c['id'],'text':c['text']} for c in CASES], ensure_ascii=False)
    url=f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}'
    body={'system_instruction':{'parts':[{'text':SYSTEM}]},'contents':[{'role':'user','parts':[{'text':prompt}]}], 'generationConfig':{'maxOutputTokens':3500,'responseMimeType':'application/json','responseJsonSchema':SCHEMA,'thinkingConfig':{'thinkingLevel':'MINIMAL'}}}
    req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'},method='POST')
    t=time.time()
    with urllib.request.urlopen(req, timeout=90) as r: raw=json.loads(r.read().decode())
    obj=json.loads(raw['candidates'][0]['content']['parts'][0]['text'])
    return obj, raw.get('usageMetadata'), int((time.time()-t)*1000)

def normalize(s):
    return ''.join(ch.lower() if ch.isalnum() else ' ' for ch in s)

def semantic_hit(tag, claims_text):
    # Frozen deterministic vocabulary aliases. Keep aliases broad enough to grade semantic paraphrases,
    # but do not use this lexical layer as a substitute for semantic adjudication of raw model output.
    aliases={
      'current_medication_use':['take medicine','daily medication','medicine x'],
      'stop_or_replace_medication_action':['stop x','stop medicine','stopping prescription medicine','stopping medicine','replace medication','substitute it','substitute','medication substitution','use y instead','switch'],
      'supplement_safety_or_interaction':['supplement safety','interaction','safe','supplement y'],
      'current_product_price':['cost','price'],
      'current_plan_feature':['plan','feature','cheap plan'],
      'uae_jurisdiction':['uae','dubai','jurisdiction'],
      'cross_border_personal_data_transfer':['cross border','us analytics','transfer','send ids'],
      'conditions_or_compliance_requirements':['compliance','conditions','requirements','anything else'],
      'datasheet_nominal_rating':['10 a','datasheet','nominal rating'],
      'continuous_duty':['continuous','continuously'],
      'sealed_enclosure':['sealed enclosure'],
      'ambient_55c':['55 c','55c','ambient'],
      'thermal_or_derating_requirement':['derating','thermal','temperature rating'],
      'supplier_price':['supplier','cheapest','price'],
      'paper_a_finance_result':['8 points','finance benchmark','paper a'],
      'metric_and_benchmark_scope':['metric','benchmark scope','finance benchmark'],
      'cross_language_transfer':['arabic','language transfer','cross language'],
      'cross_domain_transfer':['legal corpus','finance to legal','cross domain'],
      'best_choice_claim':['best choice','best retriever'],
      'api_purchase_decision':['api','buy','purchase'],
      'current_firmware_compatibility':['firmware','current firmware','supports'],
      'conditional_dependency':['if','conditional','depends'],
      'skip_vendor_inspection_action':['skip inspection','vendor inspection'],
      'deployment_tonight':['deploy tonight','deployment tonight'],
      'safety_or_compliance_implication':['safety','compliance','alarm panel','inspection requirement']
    }
    return any(a in claims_text for a in aliases[tag])

def grade(obj):
    by_id={c['id']:c for c in obj.get('cases',[])}
    rows=[]; p0=[]
    for gold in CASES:
        got=by_id.get(gold['id'], {'claims':[]})
        claims=got.get('claims',[])
        text=normalize(' '.join(x.get('text','')+' '+' '.join(x.get('tags',[]))+' '+' '.join(x.get('qualifiers',[])) for x in claims))
        missing=[tag for tag in gold['must'] if not semantic_hit(tag,text)]
        high_missing=[tag for tag in gold['high_stakes'] if tag in missing]
        high_detected=any(x.get('stakes') in ['HIGH','UNKNOWN'] for x in claims) if gold['high_stakes'] else True
        if high_missing or (gold['high_stakes'] and not high_detected): p0.append(gold['id'])
        rows.append({'id':gold['id'],'missing':missing,'high_stakes_missing':high_missing,'high_stakes_route_present':high_detected,'status':'PASS' if not missing and high_detected else 'REVIEW'})
    return rows,p0

def main():
    out={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'model':MODEL,'gate':'gemini-semantic-claim-decomposition-v0.1'}
    try:
        obj,usage,lat=call(os.environ['GEMINI_API_KEY']); rows,p0=grade(obj)
        out.update({'latency_ms':lat,'usage':usage,'response':obj,'cases':rows,'p0_cases':p0,'status':'PASS' if not p0 and all(r['status']=='PASS' for r in rows) else ('STOP_P0' if p0 else 'REVIEW')})
    except urllib.error.HTTPError as e:
        out.update({'status':'HTTP_ERROR','http_status':e.code,'error':e.read().decode(errors='replace')})
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    open(OUT,'w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=2))
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['status']=='PASS' else (2 if out['status']=='STOP_P0' else 3))

if __name__=='__main__': main()
