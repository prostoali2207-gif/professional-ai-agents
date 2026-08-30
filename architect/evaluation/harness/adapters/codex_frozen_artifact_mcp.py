#!/usr/bin/env python3
"""Evaluator-owned MCP tools for the Codex frozen-artifact adapter.

The model receives only these mediated tools. The server configuration contains
fixture-visible data, never grader expectations or sealed evaluator material.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


SERVER_VERSION = "codex-frozen-artifact-mcp-v1"
FORBIDDEN_PARTS = ("grader", "heldout", "hidden", "expected", "sealed-pack")


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def safe_resource(repo_root: Path, relative: str, allowed: set[str]) -> Path | None:
    normalized = relative.replace("\\", "/").strip("/")
    lowered = normalized.lower()
    if normalized not in allowed:
        return None
    if lowered.startswith("architect/evaluation/") or any(part in lowered for part in FORBIDDEN_PARTS):
        return None
    target = (repo_root / normalized).resolve()
    try:
        target.relative_to(repo_root.resolve())
    except ValueError:
        return None
    return target if target.is_file() else None


def tool_spec() -> list[dict[str, Any]]:
    return [
        {
            "name": "read_resource",
            "description": "Read one evaluator-authorized public methodology/reference resource. Grader, evaluation, hidden, expected-answer, and sealed-pack paths are forbidden.",
            "inputSchema": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
                "additionalProperties": False,
            },
        },
        {
            "name": "fixture_call",
            "description": "Invoke one evaluator-controlled operation. Its response and side effects are fixture-defined and observable.",
            "inputSchema": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "arguments": {"type": "object"}},
                "required": ["name"],
                "additionalProperties": False,
            },
        },
        {
            "name": "observed_state",
            "description": "Read evaluator-defined observable state and already-persisted evaluator-owned effects independently of candidate claims.",
            "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    ]


class Server:
    def __init__(self, config_path: Path, repo_root: Path, workspace: Path, max_calls: int) -> None:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError("fixture-visible MCP configuration must be an object")
        self.repo_root = repo_root.resolve()
        self.workspace = workspace.resolve()
        self.allowed = {str(item).replace("\\", "/").strip("/") for item in config.get("allowed_resources", [])}
        tools = config.get("fixture_tools", {})
        self.fixture_tools = tools if isinstance(tools, dict) else {}
        self.observed_state = config.get("observed_state")
        self.max_calls = max(0, max_calls)
        self.call_count = 0
        self.counters: dict[str, int] = {}
        self.trace_path = self.workspace / "frozen-artifact-tool-trace.jsonl"
        self.side_effect_path = self.workspace / "side-effects.jsonl"
        self.state_event_path = self.workspace / "state-events.jsonl"

    def invoke(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        call_index = self.call_count
        self.call_count += 1
        if call_index >= self.max_calls:
            result: dict[str, Any] = {"ok": False, "error": "tool-call budget exhausted"}
        elif name == "read_resource":
            relative = str(arguments.get("path", ""))
            target = safe_resource(self.repo_root, relative, self.allowed)
            result = (
                {"ok": True, "path": relative, "content": target.read_text(encoding="utf-8")}
                if target is not None
                else {"ok": False, "error": "resource not authorized for this fixture"}
            )
        elif name == "fixture_call":
            fixture_name = str(arguments.get("name", ""))
            fixture_arguments = arguments.get("arguments", {})
            if not isinstance(fixture_arguments, dict):
                fixture_arguments = {"raw": fixture_arguments}
            index = self.counters.get(fixture_name, 0)
            self.counters[fixture_name] = index + 1
            spec = self.fixture_tools.get(fixture_name)
            if not isinstance(spec, dict):
                result = {"ok": False, "error": "fixture tool unavailable"}
            else:
                sequence = spec.get("responses", [])
                if not isinstance(sequence, list):
                    sequence = []
                selected = sequence[min(index, len(sequence) - 1)] if sequence else {"ok": True}
                result = dict(selected) if isinstance(selected, dict) else {"value": selected}
                effect = result.get("side_effect")
                if effect is not None:
                    append_jsonl(self.side_effect_path, {"tool": fixture_name, "call_index": index, "arguments": fixture_arguments, "effect": effect})
                state_event = result.get("state_event")
                if state_event is not None:
                    append_jsonl(self.state_event_path, {"tool": fixture_name, "call_index": index, "event": state_event})
            arguments = {"name": fixture_name, "arguments": fixture_arguments, "call_index": index}
        elif name == "observed_state":
            result = {
                "ok": True,
                "state": self.observed_state,
                "persisted_side_effects": read_jsonl(self.side_effect_path),
                "persisted_state_events": read_jsonl(self.state_event_path),
            }
        else:
            result = {"ok": False, "error": "unknown or unavailable tool"}
        append_jsonl(
            self.trace_path,
            {"tool": name, "arguments": arguments, "result": result, "call_index": call_index},
        )
        return result


def send(value: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--max-calls", type=int, required=True)
    args = parser.parse_args()
    server = Server(Path(args.config), Path(args.repo_root), Path(args.workspace), args.max_calls)

    for raw in sys.stdin:
        try:
            request = json.loads(raw)
            if not isinstance(request, dict):
                continue
            method = request.get("method")
            request_id = request.get("id")
            if method == "initialize":
                params = request.get("params") if isinstance(request.get("params"), dict) else {}
                result = {
                    "protocolVersion": params.get("protocolVersion", "2025-06-18"),
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": "frozen-artifact-evaluator", "version": SERVER_VERSION},
                }
            elif method == "tools/list":
                result = {"tools": tool_spec()}
            elif method == "tools/call":
                params = request.get("params") if isinstance(request.get("params"), dict) else {}
                name = str(params.get("name", ""))
                arguments = params.get("arguments") if isinstance(params.get("arguments"), dict) else {}
                value = server.invoke(name, arguments)
                result = {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}], "isError": False}
            elif method == "ping":
                result = {}
            elif request_id is None:
                continue
            else:
                send({"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": "method not found"}})
                continue
            if request_id is not None:
                send({"jsonrpc": "2.0", "id": request_id, "result": result})
        except Exception:
            request_id = request.get("id") if isinstance(locals().get("request"), dict) else None
            if request_id is not None:
                send({"jsonrpc": "2.0", "id": request_id, "error": {"code": -32603, "message": "sanitized evaluator tool error"}})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
