import asyncio
import json
import os
import time
import urllib.request
from datetime import datetime, timezone

from mcp import Client

OUT = "architect/research/benchmark/runs/paired-pilot-v0.1.json"
EXA_URL = "https://mcp.exa.ai/mcp"
TAVILY_URL = "https://api.tavily.com/search"
TAVILY_KEY = os.environ["TAVILY_API_KEY"]

CASES = [
    {
        "id": "P1-OBSCURE-NIST-GAI",
        "query": "official NIST Generative AI Profile NIST AI 600-1 DOI risks actions PDF",
        "gold": ["nist.gov", "10.6028/NIST.AI.600-1"],
        "purpose": "obscure authoritative evidence recall",
    },
    {
        "id": "P1-COUNTER-BM25",
        "query": "evidence benchmark showing BM25 can outperform dense semantic retrieval financial text table documents 2026",
        "gold": ["2604.01733", "BM25"],
        "purpose": "counterevidence discovery against semantic-search-always-wins claim",
    },
    {
        "id": "P1-XLI-UAE-AI-AR",
        "query": "official Arabic UAE artificial intelligence strategy 2031 100% services data analysis Arabic government source",
        "gold": ["u.ae", "استراتي"],
        "purpose": "cross-lingual authoritative retrieval",
    },
    {
        "id": "P1-CITE-BERT",
        "query": "BERT NAACL 2019 version of record DOI Devlin Chang Lee Toutanova ACL Anthology",
        "gold": ["10.18653/v1/N19-1423", "aclanthology.org"],
        "purpose": "citation candidate identity integrity",
    },
    {
        "id": "P1-RAW-NIST-600-1",
        "query": "NIST AI 600-1 official PDF Generative AI Profile full document",
        "gold": ["nist.gov", "NIST.AI.600-1"],
        "purpose": "raw-document candidate access",
    },
]


def ser(x):
    if hasattr(x, "model_dump"):
        return x.model_dump(mode="json")
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    if isinstance(x, dict):
        return {str(k): ser(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [ser(v) for v in x]
    return repr(x)


def tavily_search(query):
    body = json.dumps({
        "api_key": TAVILY_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": 5,
        "include_answer": False,
        "include_raw_content": False,
    }).encode()
    req = urllib.request.Request(TAVILY_URL, data=body, headers={"Content-Type": "application/json"})
    t = time.perf_counter()
    with urllib.request.urlopen(req, timeout=45) as r:
        data = json.loads(r.read().decode())
    return data, round(time.perf_counter() - t, 3)


async def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    rec = {
        "schema": "paired-pilot-v0.1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "providers": ["Exa hosted MCP anonymous", "Tavily Search API basic"],
        "cases": [],
    }
    async with Client(EXA_URL) as exa:
        for case in CASES:
            row = {"case": case}
            t = time.perf_counter()
            try:
                er = await exa.call_tool("web_search_exa", {"query": case["query"], "numResults": 5})
                row["exa"] = {"status": "ok", "latency_s": round(time.perf_counter()-t, 3), "result": ser(er)}
            except Exception as e:
                row["exa"] = {"status": "error", "error": f"{type(e).__name__}: {e}"}
            try:
                tr, latency = tavily_search(case["query"])
                row["tavily"] = {"status": "ok", "latency_s": latency, "result": tr}
            except Exception as e:
                row["tavily"] = {"status": "error", "error": f"{type(e).__name__}: {e}"}
            rec["cases"].append(row)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
