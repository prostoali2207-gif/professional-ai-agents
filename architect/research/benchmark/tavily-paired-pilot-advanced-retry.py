import json, os, time, urllib.request
from datetime import datetime, timezone

OUT='architect/research/benchmark/runs/tavily-paired-pilot-advanced-retry.json'
KEY=os.environ['TAVILY_API_KEY']
URL='https://api.tavily.com/search'
CASES=[
 ('P1-OBSCURE-NIST-GAI','official NIST Generative AI Profile NIST AI 600-1 DOI risks actions PDF'),
 ('P1-XLI-UAE-AI-AR','official Arabic UAE artificial intelligence strategy 2031 100% services data analysis Arabic government source'),
 ('P1-RAW-NIST-600-1','NIST AI 600-1 official PDF Generative AI Profile full document'),
]

def search(q):
    body=json.dumps({'api_key':KEY,'query':q,'search_depth':'advanced','max_results':5,'include_answer':False,'include_raw_content':False}).encode()
    req=urllib.request.Request(URL,data=body,headers={'Content-Type':'application/json'})
    t=time.perf_counter()
    with urllib.request.urlopen(req,timeout=45) as r: data=json.loads(r.read().decode())
    return data,round(time.perf_counter()-t,3)

rec={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'provider':'Tavily','mode':'advanced','cases':[]}
for cid,q in CASES:
    try:
        r,l=search(q); rec['cases'].append({'id':cid,'query':q,'status':'ok','latency_s':l,'result':r})
    except Exception as e:
        rec['cases'].append({'id':cid,'query':q,'status':'error','error':f'{type(e).__name__}: {e}'})
os.makedirs(os.path.dirname(OUT),exist_ok=True)
with open(OUT,'w',encoding='utf-8') as f: json.dump(rec,f,ensure_ascii=False,indent=2)
