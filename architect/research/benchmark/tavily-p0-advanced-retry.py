import json, os, time, urllib.request
from datetime import datetime, timezone

OUT='architect/research/benchmark/runs/tavily-p0-advanced-retry.json'
API='https://api.tavily.com/search'
KEY=os.environ['TAVILY_API_KEY']
CASES=[
 ('P0-1-AUTH-FRESH','Model Context Protocol 2026-07-28 specification final release official'),
 ('P0-4-HOP','information retrieval why correct documents are missed when query and document use different terminology semantic lexical mismatch'),
]

def search(q):
    payload={'query':q,'search_depth':'advanced','max_results':5,'include_raw_content':True}
    req=urllib.request.Request(API,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Authorization':f'Bearer {KEY}'})
    t=time.perf_counter()
    with urllib.request.urlopen(req,timeout=60) as r: body=json.loads(r.read().decode())
    return body, round(time.perf_counter()-t,3)

def main():
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    rec={'provider':'Tavily','mode':'advanced search retry','timestamp_utc':datetime.now(timezone.utc).isoformat(),'cases':[],'status':'STARTED'}
    try:
        for cid,q in CASES:
            body,lat=search(q); rec['cases'].append({'case_id':cid,'query':q,'latency_seconds':lat,'result':body})
        rec['status']='COMPLETED'
    except Exception as e:
        rec.update(status='ERROR',error_type=type(e).__name__,error=str(e)); raise
    finally:
        with open(OUT,'w',encoding='utf-8') as f: json.dump(rec,f,ensure_ascii=False,indent=2)

if __name__=='__main__': main()
