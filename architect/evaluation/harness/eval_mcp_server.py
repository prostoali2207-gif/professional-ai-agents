#!/usr/bin/env python3
"""Controlled MCP server for Agent Architect behavioral evaluation.

The server exposes only inspectable evaluation capabilities. It reads one step
configuration written by the candidate adapter and stores durable state / tool
side effects in the harness workspace, independently of model prose.

stdout is reserved for MCP stdio protocol. Diagnostics belong on stderr.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from mcp.server import MCPServer

mcp = MCPServer("EvalHarness")


def env_path(name: str) -> Path:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"missing required environment variable {name}")
    return Path(value).resolve()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")


def config() -> dict[str, Any]:
    value = load_json(env_path("AA_EVAL_STEP_CONFIG"), {})
    if not isinstance(value, dict):
        raise RuntimeError("step config must be an object")
    return value


def workspace() -> Path:
    return env_path("AA_EVAL_WORKSPACE")


def capability(name: str) -> bool:
    caps = config().get("capability_profile") or {}
    return bool(caps.get(name, False)) if isinstance(caps, dict) else False


def trace(event: dict[str, Any]) -> None:
    append_jsonl(workspace() / "mcp-tool-trace.jsonl", event)


@mcp.tool()
def read_resource(path: str) -> dict[str, Any]:
    """Read an authorized Agent Architect methodology/reference resource."""
    cfg = config()
    allowed = cfg.get("allowed_resources") or []
    if path not in allowed:
        result = {"ok": False, "error": "resource not authorized for this fixture"}
        trace({"tool": "read_resource", "path": path, "result": result})
        return result
    root = env_path("AA_EVAL_REPO_ROOT")
    target = (root / path).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        result = {"ok": False, "error": "path escapes repository"}
        trace({"tool": "read_resource", "path": path, "result": result})
        return result
    if not target.is_file() or path.startswith("architect/evaluation/"):
        result = {"ok": False, "error": "resource unavailable"}
    else:
        result = {"ok": True, "path": path, "content": target.read_text(encoding="utf-8")}
    trace({"tool": "read_resource", "path": path, "result": {"ok": result.get("ok")}})
    return result


@mcp.tool()
def memory_read() -> dict[str, Any]:
    """Read persistent evaluation memory when that capability is enabled."""
    if not capability("persistent_memory"):
        result = {"ok": False, "error": "persistent_memory capability unavailable"}
    else:
        result = {"ok": True, "memory": load_json(workspace() / "persistent-memory.json", {})}
    trace({"tool": "memory_read", "result": result})
    return result


@mcp.tool()
def memory_write(key: str, value_json: str, provenance: str, classification: str) -> dict[str, Any]:
    """Persist one inspectable memory entry after applying the candidate's write gate."""
    if not capability("persistent_memory"):
        result = {"ok": False, "error": "persistent_memory capability unavailable"}
        trace({"tool": "memory_write", "key": key, "result": result})
        return result
    try:
        value = json.loads(value_json)
    except json.JSONDecodeError:
        value = value_json
    path = workspace() / "persistent-memory.json"
    memory = load_json(path, {})
    if not isinstance(memory, dict):
        memory = {}
    memory[key] = {
        "value": value,
        "provenance": provenance,
        "classification": classification,
    }
    save_json(path, memory)
    event = {"op": "write", "key": key, "provenance": provenance, "classification": classification}
    append_jsonl(workspace() / "memory-events.jsonl", event)
    trace({"tool": "memory_write", **event, "result": {"ok": True}})
    return {"ok": True}


@mcp.tool()
def memory_delete(key: str) -> dict[str, Any]:
    """Delete an inspectable persistent memory entry when invalidated or expired."""
    if not capability("persistent_memory"):
        result = {"ok": False, "error": "persistent_memory capability unavailable"}
        trace({"tool": "memory_delete", "key": key, "result": result})
        return result
    path = workspace() / "persistent-memory.json"
    memory = load_json(path, {})
    if not isinstance(memory, dict):
        memory = {}
    existed = key in memory
    memory.pop(key, None)
    save_json(path, memory)
    event = {"op": "delete", "key": key, "existed": existed}
    append_jsonl(workspace() / "memory-events.jsonl", event)
    trace({"tool": "memory_delete", **event, "result": {"ok": True, "existed": existed}})
    return {"ok": True, "existed": existed}


@mcp.tool()
def fixture_call(name: str, arguments_json: str = "{}") -> dict[str, Any]:
    """Call one fixture-controlled professional/tool operation by name.

    The fixture controls the response sequence and any mechanically recorded side
    effect. This permits no-progress routes, ambiguous commit responses, and
    deterministic downstream-state probes without giving the model the grader key.
    """
    cfg = config()
    fixture_tools = cfg.get("fixture_tools") or {}
    if not isinstance(fixture_tools, dict) or name not in fixture_tools:
        result = {"ok": False, "error": "fixture tool unavailable"}
        trace({"tool": "fixture_call", "name": name, "result": result})
        return result
    try:
        arguments = json.loads(arguments_json)
    except json.JSONDecodeError:
        arguments = {"raw": arguments_json}
    counters_path = workspace() / "fixture-tool-counters.json"
    counters = load_json(counters_path, {})
    if not isinstance(counters, dict):
        counters = {}
    index = int(counters.get(name, 0))
    counters[name] = index + 1
    save_json(counters_path, counters)

    spec = fixture_tools[name]
    sequence = spec.get("responses", []) if isinstance(spec, dict) else []
    if sequence:
        response = sequence[min(index, len(sequence) - 1)]
    else:
        response = {"ok": True}
    if not isinstance(response, dict):
        response = {"value": response}

    if "side_effect" in response:
        side = {
            "tool": name,
            "call_index": index,
            "arguments": arguments,
            "effect": response["side_effect"],
        }
        append_jsonl(workspace() / "side-effects.jsonl", side)

    trace({"tool": "fixture_call", "name": name, "call_index": index, "arguments": arguments, "result": response})
    return response


@mcp.tool()
def observed_state() -> dict[str, Any]:
    """Query fixture-defined observable downstream state without trusting prior prose."""
    cfg = config()
    state = cfg.get("observed_state")
    result = {"ok": True, "state": state}
    trace({"tool": "observed_state", "result": result})
    return result


if __name__ == "__main__":
    mcp.run(transport="stdio")
