import asyncio, json, os, time
from datetime import datetime, timezone
from mcp import Client

OUT='architect/research/benchmark/runs/exa-p0-extract-deep.json'
URL='https://mcp.exa.ai/mcp'
PDF='https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf'


def ser(x):
    if hasattr(x,'model_dump'): return x.model_dump(mode='json')
    if isinstance(x,(str,int,float,bool)) or x is None: return x
    if isinstance(x,dict): return {str(k):ser(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [ser(v) for v in x]
    return repr(x)

async def main():
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    rec={'provider':'Exa','case_id':'P0-3-EXTRACT-DEEP','endpoint':URL,'timestamp_utc':datetime.now(timezone.utc).isoformat(),'url':PDF,'maxCharacters':120000}
    t=time.perf_counter()
    try:
        async with Client(URL) as c:
            r=await c.call_tool('web_fetch_exa',{'urls':[PDF],'maxCharacters':120000})
            rec['result']=ser(r); rec['status']='COMPLETED'
    except Exception as e:
        rec.update(status='ERROR',error_type=type(e).__name__,error=str(e)); raise
    finally:
        rec['latency_seconds']=round(time.perf_counter()-t,3)
        with open(OUT,'w',encoding='utf-8') as f: json.dump(rec,f,ensure_ascii=False,indent=2)

if __name__=='__main__': asyncio.run(main())
