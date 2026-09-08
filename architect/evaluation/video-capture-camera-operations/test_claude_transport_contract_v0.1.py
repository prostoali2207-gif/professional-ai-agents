#!/usr/bin/env python3
"""Deterministic regression for the 2026-09-08 Stage B transport defect.

Defect reproduced here (LOCAL_EXECUTION_FAIL, 0 candidate calls, 0 judge calls):
the Claude Code candidate/judge adapters passed `--bare`. In Claude Code
>= 2.1.x `--bare` restricts Anthropic auth to ANTHROPIC_API_KEY / apiKeyHelper
and never reads OAuth. Combined with this route's preregistered
subscription-only, no-metered-key contract, every child invocation died with
"Authentication error" before any model call, while the adapter preflight
still reported PASS because it only probed `claude --version` / `claude auth
status` and never the real invocation flag set.

These checks run with zero provider/model calls.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def load(name: str):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), HERE / name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(condition: bool, label: str, failures: list[str]) -> None:
    if condition:
        print(f"PASS {label}")
    else:
        print(f"FAIL {label}")
        failures.append(label)


def main() -> int:
    failures: list[str] = []
    candidate = load("claude_candidate_adapter_v0.1.py")
    judge = load("claude_judge_adapter_v0.1.py")

    for label, module in (("candidate", candidate), ("judge", judge)):
        flags = module.ISOLATION_FLAGS

        # The exact regression: --bare must never return to this route.
        check("--bare" not in flags, f"{label}: --bare absent (subscription auth preserved)", failures)

        # The isolation --bare was originally selected for must still hold.
        for required in ("--safe-mode", "--restricted", "--no-session-persistence",
                         "--strict-mcp-config", "--disable-slash-commands"):
            check(required in flags, f"{label}: {required} present", failures)
        check("--tools" in flags, f"{label}: --tools present", failures)
        check("mcp__*" in flags, f"{label}: MCP tools denied", failures)

        # Metered credentials must still be stripped from the child environment.
        check("ANTHROPIC_API_KEY" in module.FORBIDDEN_ENV,
              f"{label}: metered key stripped from child env", failures)

    # The preflight must reject a contract-violating flag set deterministically,
    # before any model call, instead of reporting PASS.
    original = candidate.ISOLATION_FLAGS
    try:
        candidate.ISOLATION_FLAGS = original + ("--bare",)
        try:
            candidate.assert_flag_contract()
            check(False, "preflight rejects --bare before model calls", failures)
        except RuntimeError:
            check(True, "preflight rejects --bare before model calls", failures)
    finally:
        candidate.ISOLATION_FLAGS = original

    try:
        candidate.assert_flag_contract()
        check(True, "preflight accepts the repaired flag set", failures)
    except RuntimeError as exc:
        check(False, f"preflight accepts the repaired flag set ({exc})", failures)

    if failures:
        print(f"\nFAILED: {len(failures)}")
        return 1
    print("\nOK: transport contract regression passed with 0 provider calls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
