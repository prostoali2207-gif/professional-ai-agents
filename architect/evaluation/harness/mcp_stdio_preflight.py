#!/usr/bin/env python3
"""Mechanical stdio handshake test for EvalHarness MCP.

This test does not involve a model. It proves that the server process starts,
completes the MCP handshake, advertises the required tools, and executes one
read_resource call that leaves an independent trace in the workspace.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import sys

from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client

REQUIRED_TOOLS = {
    "read_resource",
    "memory_read",
    "memory_write",
    "memory_delete",
    "fixture_call",
    "observed_state",
}


async def run(repo_root: Path, workspace: Path) -> dict:
    workspace.mkdir(parents=True, exist_ok=True)
    step_config = workspace / "preflight-step.json"
    step_config.write_text(
        json.dumps(
            {
                "capability_profile": {"persistent_memory": False},
                "allowed_resources": ["architect/methodology/runtime-state-memory-context.md"],
                "fixture_tools": {},
                "observed_state": None,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    params = StdioServerParameters(
        command=sys.executable,
        args=[str(repo_root / "architect" / "evaluation" / "harness" / "eval_mcp_server.py")],
        env={
            **os.environ,
            "AA_EVAL_STEP_CONFIG": str(step_config),
            "AA_EVAL_WORKSPACE": str(workspace),
            "AA_EVAL_REPO_ROOT": str(repo_root),
        },
    )

    async with Client(stdio_client(params)) as client:
        listed = await client.list_tools()
        names = {tool.name for tool in listed.tools}
        missing = sorted(REQUIRED_TOOLS - names)
        if missing:
            raise RuntimeError(f"EvalHarness missing tools: {missing}; observed={sorted(names)}")

        result = await client.call_tool(
            "read_resource",
            {"path": "architect/methodology/runtime-state-memory-context.md"},
        )

    trace = workspace / "mcp-tool-trace.jsonl"
    if not trace.exists():
        raise RuntimeError("EvalHarness call completed but no independent MCP trace was written")
    trace_text = trace.read_text(encoding="utf-8")
    if '"tool": "read_resource"' not in trace_text or '"ok": true' not in trace_text:
        raise RuntimeError(f"MCP trace does not prove successful read_resource call: {trace_text}")

    summary = {
        "status": "PASS",
        "tools": sorted(names),
        "call_result": result.model_dump(mode="json") if hasattr(result, "model_dump") else str(result),
        "trace_path": str(trace),
    }
    (workspace / "preflight-result.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    try:
        summary = asyncio.run(run(args.repo_root.resolve(), args.workspace.resolve()))
    except Exception as exc:
        print(f"MCP_PREFLIGHT_FAIL: {exc}", file=sys.stderr)
        return 1
    print("MCP_STDIO_PREFLIGHT_PASS")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
