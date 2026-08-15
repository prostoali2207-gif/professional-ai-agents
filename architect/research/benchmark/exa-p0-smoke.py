import asyncio
import json
import os
import time
from datetime import datetime, timezone

from mcp import Client

OUT = "architect/research/benchmark/runs/exa-p0-smoke.json"
URL = "https://mcp.exa.ai/mcp"
QUERY = "Model Context Protocol 2026-07-28 specification final release official"


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
        "case_id": "P0-1-AUTH-FRESH-CONNECTIVITY-SHAKEOUT",
        "query": QUERY,
        "status": "STARTED",
    }
    started = time.perf_counter()
    try:
        async with Client(URL) as client:
            tools = await client.list_tools()
            record["tools"] = serializable(tools)

            tool_list = getattr(tools, "tools", None)
            if tool_list is None and isinstance(tools, list):
                tool_list = tools
            tool_list = tool_list or []

            names = [getattr(t, "name", None) for t in tool_list]
            record["tool_names"] = names
            if "web_search_exa" not in names:
                raise RuntimeError(f"web_search_exa unavailable; tools={names}")

            selected = next(t for t in tool_list if getattr(t, "name", None) == "web_search_exa")
            schema = getattr(selected, "input_schema", None) or getattr(selected, "inputSchema", None) or {}
            record["web_search_exa_schema"] = serializable(schema)

            properties = schema.get("properties", {}) if isinstance(schema, dict) else {}
            args = {"query": QUERY}
            if "numResults" in properties:
                args["numResults"] = 5
            elif "num_results" in properties:
                args["num_results"] = 5

            record["call_args"] = args
            call_started = time.perf_counter()
            result = await client.call_tool("web_search_exa", args)
            record["search_latency_seconds"] = round(time.perf_counter() - call_started, 3)
            record["result"] = serializable(result)
            record["status"] = "PASS_CONNECTIVITY"
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
