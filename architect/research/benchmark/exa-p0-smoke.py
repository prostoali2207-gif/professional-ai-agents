import asyncio
import json
import os
import time
from datetime import datetime, timezone

from mcp import Client

OUT = "architect/research/benchmark/runs/exa-p0-smoke.json"
URL = "https://mcp.exa.ai/mcp"

CASES = [
    {
        "case_id": "P0-1-AUTH-FRESH",
        "tool": "web_search_exa",
        "args": {
            "query": "Model Context Protocol 2026-07-28 specification final stable release official",
            "numResults": 5,
        },
    },
    {
        "case_id": "P0-2-SCHOLAR",
        "tool": "web_search_exa",
        "args": {
            "query": "BERT Devlin Chang Lee Toutanova 2018 arXiv preprint 2019 NAACL version of record DOI",
            "numResults": 8,
        },
    },
    {
        "case_id": "P0-3-EXTRACT",
        "tool": "web_fetch_exa",
        "args": {
            "urls": ["https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf"],
            "maxCharacters": 16000,
        },
    },
    {
        "case_id": "P0-4-HOP",
        "tool": "web_search_exa",
        "args": {
            "query": "Why can a search system miss a document that is relevant in meaning when the query and the document use different words? Information retrieval research terminology and methods.",
            "numResults": 8,
        },
    },
]


def serializable(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    if isinstance(obj, dict):
        return {str(k): serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [serializable(v) for v in obj]
    return repr(obj)


async def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    record = {
        "provider": "Exa",
        "endpoint": URL,
        "mode": "hosted MCP anonymous",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "STARTED",
        "cases": [],
        "security_note": (
            "P0-5 prompt-injection compliance is not scored on raw Exa search/fetch primitives. "
            "The exposed tools are read-only retrieval primitives; injection compliance belongs to the consuming agent/synthesis layer."
        ),
    }
    started = time.perf_counter()
    try:
        async with Client(URL) as client:
            tools = await client.list_tools()
            tool_list = getattr(tools, "tools", None)
            if tool_list is None and isinstance(tools, list):
                tool_list = tools
            tool_list = tool_list or []
            names = [getattr(t, "name", None) for t in tool_list]
            record["tool_names"] = names
            record["tools"] = serializable(tools)

            for case in CASES:
                case_record = {
                    "case_id": case["case_id"],
                    "tool": case["tool"],
                    "args": case["args"],
                    "status": "STARTED",
                }
                call_started = time.perf_counter()
                try:
                    result = await client.call_tool(case["tool"], case["args"])
                    case_record["latency_seconds"] = round(time.perf_counter() - call_started, 3)
                    case_record["result"] = serializable(result)
                    case_record["status"] = "COMPLETED"
                except Exception as exc:
                    case_record["latency_seconds"] = round(time.perf_counter() - call_started, 3)
                    case_record["status"] = "ERROR"
                    case_record["error_type"] = type(exc).__name__
                    case_record["error"] = str(exc)
                record["cases"].append(case_record)

            record["status"] = "COMPLETED"
    except Exception as exc:
        record["status"] = "ERROR"
        record["error_type"] = type(exc).__name__
        record["error"] = str(exc)
        raise
    finally:
        record["total_latency_seconds"] = round(time.perf_counter() - started, 3)
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    asyncio.run(main())
