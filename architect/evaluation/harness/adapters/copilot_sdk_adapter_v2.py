#!/usr/bin/env python3
"""Runtime-hardening wrapper for the controlled Copilot SDK adapter.

The v1 adapter's observable session-event logger assumed every SDK event metadata
field was directly JSON serializable. Some SDK events expose Enum values such as
SessionEventType; telemetry must never be allowed to break candidate execution.
This wrapper replaces only the JSONL serialization helper with a `default=str`
variant, leaving candidate instructions, custom tools, fixtures, state semantics,
and permission boundaries unchanged.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


BASE_PATH = Path(__file__).with_name("copilot_sdk_adapter.py")
_spec = importlib.util.spec_from_file_location("agent_architect_copilot_sdk_adapter_v1", BASE_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load base adapter: {BASE_PATH}")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)


def safe_append_jsonl(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str) + "\n")


base._append_jsonl = safe_append_jsonl


if __name__ == "__main__":
    raise SystemExit(base.main())
