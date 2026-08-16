#!/usr/bin/env python3
"""Provider-aware controlled Copilot SDK adapter for Agent Architect validation.

Default behavior is unchanged: use the GitHub/Copilot token path. When
AGENT_ARCHITECT_BYOK_PROVIDER and AGENT_ARCHITECT_BYOK_API_KEY are supplied,
the adapter injects an official Copilot SDK BYOK provider into the same
controlled session. This bypasses Copilot premium-request quota without
changing the evaluator-defined custom tools, state semantics, or grader.

Supported provider values here are intentionally narrow: ``openai`` and
``anthropic``. The model must be explicitly set through AGENT_ARCHITECT_MODEL
for BYOK runs; ``auto`` is not accepted because provider model availability is
not implied by the harness.
"""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from typing import Any


BASE_PATH = Path(__file__).with_name("copilot_sdk_adapter.py")
_spec = importlib.util.spec_from_file_location("agent_architect_copilot_sdk_adapter_base", BASE_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load base adapter: {BASE_PATH}")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)


# Keep the v2 telemetry hardening: SDK enums and similar metadata must never
# crash candidate execution merely because json.dumps cannot serialize them.
def safe_append_jsonl(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str) + "\n")


base._append_jsonl = safe_append_jsonl
_REAL_CLIENT = base.CopilotClient


def _provider_from_env() -> dict[str, Any] | None:
    provider_type = os.environ.get("AGENT_ARCHITECT_BYOK_PROVIDER", "").strip().lower()
    api_key = os.environ.get("AGENT_ARCHITECT_BYOK_API_KEY", "").strip()
    if not provider_type and not api_key:
        return None
    if not provider_type or not api_key:
        raise RuntimeError("BYOK requires both AGENT_ARCHITECT_BYOK_PROVIDER and AGENT_ARCHITECT_BYOK_API_KEY")

    model = os.environ.get("AGENT_ARCHITECT_MODEL", "auto").strip()
    if not model or model == "auto":
        raise RuntimeError("BYOK requires an explicit AGENT_ARCHITECT_MODEL; auto is not provider-portable")

    if provider_type == "openai":
        return {
            "type": "openai",
            "base_url": os.environ.get("AGENT_ARCHITECT_BYOK_BASE_URL", "https://api.openai.com/v1"),
            "api_key": api_key,
            "wire_api": os.environ.get("AGENT_ARCHITECT_BYOK_WIRE_API", "responses"),
        }
    if provider_type == "anthropic":
        return {
            "type": "anthropic",
            "base_url": os.environ.get("AGENT_ARCHITECT_BYOK_BASE_URL", "https://api.anthropic.com"),
            "api_key": api_key,
        }
    raise RuntimeError(f"unsupported AGENT_ARCHITECT_BYOK_PROVIDER: {provider_type}")


class ProviderAwareCopilotClient:
    """Thin proxy that injects BYOK only when explicitly configured."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._provider = _provider_from_env()
        if self._provider is not None:
            # The provider key, not GitHub Copilot identity/quota, authenticates
            # model calls in BYOK mode. Preserve every other client constraint.
            kwargs.pop("github_token", None)
        self._inner = _REAL_CLIENT(*args, **kwargs)

    async def start(self) -> Any:
        return await self._inner.start()

    async def stop(self) -> Any:
        return await self._inner.stop()

    async def create_session(self, *args: Any, **kwargs: Any) -> Any:
        if self._provider is not None:
            kwargs["provider"] = self._provider
        return await self._inner.create_session(*args, **kwargs)


base.CopilotClient = ProviderAwareCopilotClient


if __name__ == "__main__":
    raise SystemExit(base.main())
