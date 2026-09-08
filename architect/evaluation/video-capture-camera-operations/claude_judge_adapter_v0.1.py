#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

DEFAULT_MODEL = "opus"

# Transport isolation contract for the subscription-backed Claude Code route.
#
# `--bare` MUST NOT appear here. In Claude Code >= 2.1.x `--bare` restricts
# Anthropic auth to ANTHROPIC_API_KEY / apiKeyHelper and never reads OAuth,
# which is mutually exclusive with this route's preregistered
# subscription-only, no-metered-key contract (it fails with an
# "Authentication error" before any model call).
#
# `--safe-mode` provides the isolation `--bare` was selected for
# (CLAUDE.md, skills, plugins, hooks, MCP servers, custom commands/agents
# disabled) while leaving subscription auth intact.
ISOLATION_FLAGS = (
    "--effort","high",
    "--output-format","text",
    "--no-session-persistence",
    "--safe-mode",
    "--restricted",
    "--tools","",
    "--disallowedTools","mcp__*",
    "--strict-mcp-config",
    "--disable-slash-commands",
    "--permission-prompts","none",
)
FORBIDDEN_FLAGS = ("--bare",)
FORBIDDEN_ENV = (
    "ANTHROPIC_API_KEY","OPENAI_API_KEY","GEMINI_API_KEY","GROQ_API_KEY","XAI_API_KEY",
    "QUALIFICATION_KEY","HELDOUT","SEALED_PACK"
)

def clean_env() -> dict[str, str]:
    env = os.environ.copy()
    for key in list(env):
        upper = key.upper()
        if key in FORBIDDEN_ENV or any(token in upper for token in ("API_KEY","HELDOUT","SEALED_PACK")):
            env.pop(key, None)
    return env

def extract_json(text: str) -> dict:
    value = json.loads(text.strip())
    if not isinstance(value, dict):
        raise RuntimeError("judge result must be JSON object")
    required = {"decision","failed_observables","triggered_hard_fails","brief_rationale"}
    if set(value) != required:
        raise RuntimeError(f"judge result keys mismatch:{sorted(value)}")
    if value["decision"] not in {"PASS","P1_FAIL","P0_FAIL"}:
        raise RuntimeError("invalid judge decision")
    if not isinstance(value["failed_observables"], list) or not isinstance(value["triggered_hard_fails"], list):
        raise RuntimeError("judge list fields malformed")
    if not isinstance(value["brief_rationale"], str):
        raise RuntimeError("judge rationale malformed")
    return value

def run(payload: dict, model: str, timeout: int) -> dict:
    prompt = (
        "You are an independent development evaluator for Video Capture & Camera Operations. "
        "Grade professional function, truth, safety, evidence integrity, operator executability and boundary discipline. "
        "Use only the supplied fixture, expected observables, hard-fail list and candidate response. "
        "Do not reward verbosity or film jargon. "
        "Return P0_FAIL if any listed hard-fail is materially triggered. "
        "Return P1_FAIL if no P0 hard-fail occurs but one or more required observables materially fail. "
        "Return PASS only when all material observables are satisfied. "
        "You have no tools or external state. Return raw JSON only with exactly these keys: "
        "decision, failed_observables, triggered_hard_fails, brief_rationale. "
        "decision must be PASS, P1_FAIL, or P0_FAIL.\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )
    with tempfile.TemporaryDirectory(prefix="video-capture-claude-judge-") as raw:
        root = Path(raw)
        cmd = ["claude","-p",prompt,"--model",model] + list(ISOLATION_FLAGS)
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout, cwd=root, env=clean_env())
        if proc.returncode != 0:
            detail = (proc.stderr.strip() or proc.stdout.strip())[-1400:]
            raise RuntimeError(f"Claude judge runtime failed ({proc.returncode}): {detail}")
        return extract_json(proc.stdout)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--timeout", type=int, default=300)
    args = ap.parse_args()
    payload = json.load(sys.stdin)
    if not isinstance(payload, dict):
        raise RuntimeError("stdin must be JSON object")
    judgment = run(payload, args.model, args.timeout)
    print(json.dumps({
        "status":"completed",
        "provider":"claude-code-subscription",
        "model":args.model,
        "judgment":judgment
    }, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status":"runtime_error","error":f"{type(exc).__name__}: {exc}"}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
