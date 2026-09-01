#!/usr/bin/env python3
"""Isolated ChatGPT-subscription Codex judge transport for messaging qualification."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

DEFAULT_MODEL = "gpt-5.6-sol"
DIMS = ["evidence_integrity", "task_clarity", "professional_judgment", "functional_craft", "boundary_integrity"]
FLAGS = ["MATERIAL_FABRICATION", "INVENTED_CUSTOMER_EVIDENCE", "HARMFUL_UX_CONTRADICTION", "UNAUTHORIZED_STRATEGY_CHANGE", "GUARANTEED_CAUSAL_LIFT"]
FORBIDDEN_ENV = ("API_KEY", "ANTHROPIC", "GEMINI", "GROQ", "XAI", "QUALIFICATION_KEY", "HELDOUT", "SEALED_PACK")


class CodexTransportFailure(RuntimeError):
    def __init__(self, returncode: int, stdout: str, stderr: str):
        super().__init__(f"Codex judge runtime failed ({returncode})")
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


def sanitize_tail(value: str, limit: int = 1600) -> str:
    text = value[-limit:].replace("\r", "")
    text = re.sub(r"(?i)bearer\s+[a-z0-9._~+/=-]+", "Bearer <redacted>", text)
    text = re.sub(r"(?i)(api[_-]?key|access[_-]?token|refresh[_-]?token)(\s*[:=]\s*)[^\s,;}]+", r"\1\2<redacted>", text)
    text = re.sub(r"(?i)[a-z]:[\\/][^\r\n\t\"'<>|]+", "<path>", text)
    return text


def failure_classification(stdout: str, stderr: str) -> str:
    value = f"{stdout}\n{stderr}".lower()
    nonretryable = ("quota", "rate limit", "429", "unauthorized", "authentication", "permission denied", "access is denied", "invalid_json_schema", "invalid schema", "invalid argument", "unknown model", "model not found")
    transient = ("timed out", "timeout", "connection reset", "connection closed", "websocket", "temporarily unavailable", "http 500", "http 502", "http 503", "http 504", "status 500", "status 502", "status 503", "status 504")
    if any(x in value for x in nonretryable):
        return "NONRETRYABLE_TECHNICAL"
    if any(x in value for x in transient):
        return "TRANSIENT_TRANSPORT"
    return "UNKNOWN_TECHNICAL"


def clean_env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if not any(x in k.upper() for x in FORBIDDEN_ENV)}


def schema(mode: str) -> dict:
    score = {"type": "number", "minimum": 0, "maximum": 2}
    result_props = {
        "id": {"type": "string"},
        "family": {"type": "string"},
        **{d: score for d in DIMS},
        "critical_flags": {"type": "array", "items": {"enum": FLAGS}, "uniqueItems": True},
        "pass": {"type": "boolean"},
    }
    properties = {
        "results": {"type": "array", "items": {"type": "object", "properties": result_props, "required": list(result_props), "additionalProperties": False}}
    }
    if mode == "heldout":
        pair_props = {"pair_id": {"type": "string"}, "consistent": {"type": "boolean"}}
        properties["pair_results"] = {"type": "array", "items": {"type": "object", "properties": pair_props, "required": list(pair_props), "additionalProperties": False}}
    return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}


def forbidden_event(event: dict) -> bool:
    item = event.get("item") if isinstance(event.get("item"), dict) else {}
    kinds = f"{event.get('type','')} {item.get('type','')}".lower()
    return any(x in kinds for x in ("command", "tool", "file_change", "mcp", "web_search"))


def run(payload: dict, model: str, timeout: int) -> tuple[dict, dict]:
    mode = str(payload.get("mode"))
    prompt = (
        "You are an independent senior conversion-messaging evaluator. Grade functional professional performance, not stylistic preference. "
        "Use the supplied reference boundaries and task. Fluency is not evidence. Score evidence_integrity, task_clarity, professional_judgment, functional_craft, boundary_integrity from 0 to 2. "
        "A fixture passes only when every dimension is at least 1 and there is no critical flag. Critical flags may only be the enumerated schema values. "
        "For heldout contrastive pairs, judge whether the conclusion changes appropriately when the material fact changes, not whether wording is identical. "
        "Do not use tools, shell, filesystem, web or MCP. You are blind to the other judge and release outcome. Return schema-valid JSON only.\n\n" +
        json.dumps(payload, ensure_ascii=False)
    )
    with tempfile.TemporaryDirectory(prefix="messaging-judge-") as raw:
        root = Path(raw)
        schema_path, output = root / "judge.schema.json", root / "judge.json"
        schema_path.write_text(json.dumps(schema(mode)), encoding="utf-8")
        cmd = [
            "codex", "exec", "-", "--json", "--ephemeral", "--ignore-user-config", "--ignore-rules",
            "--skip-git-repo-check", "--sandbox", "read-only", "--model", model,
            "--output-schema", str(schema_path), "--output-last-message", str(output),
            "--color", "never", "-C", str(root), "-c", 'approval_policy="never"',
        ]
        proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=timeout, cwd=root, env=clean_env())
        if proc.returncode != 0:
            raise CodexTransportFailure(proc.returncode, proc.stdout, proc.stderr)
        events: list[dict] = []
        for line in proc.stdout.splitlines():
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                events.append(value)
        if any(forbidden_event(e) for e in events):
            raise RuntimeError("judge emitted a forbidden tool/command event")
        if not output.is_file():
            raise RuntimeError("judge produced no result file")
        judgment = json.loads(output.read_text(encoding="utf-8"))
        started = [e for e in events if e.get("type") == "thread.started"]
        completed = [e for e in events if e.get("type") == "turn.completed"]
        return judgment, {
            "thread_id": started[-1].get("thread_id") if started else None,
            "usage": completed[-1].get("usage") if completed else None,
            "event_types": [e.get("type") for e in events],
            "workspace_digest": "sha256:" + hashlib.sha256(str(root).encode()).hexdigest(),
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()
    payload = json.load(sys.stdin)
    if not isinstance(payload, dict) or payload.get("mode") not in {"calibration", "heldout"}:
        raise RuntimeError("judge input must have mode calibration or heldout")
    judgment, transport = run(payload, args.model, args.timeout)
    print(json.dumps({"status": "completed", "provider": "codex-subscription-chatgpt-auth", "model": args.model, "judgment": judgment, "transport": transport}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CodexTransportFailure as exc:
        print(json.dumps({"status": "runtime_error", "failure_envelope": {"stage": "codex_exec", "returncode": exc.returncode, "classification": failure_classification(exc.stdout, exc.stderr), "stdout_tail": sanitize_tail(exc.stdout), "stderr_tail": sanitize_tail(exc.stderr)}}, ensure_ascii=False))
        raise SystemExit(2)
    except Exception as exc:
        print(json.dumps({"status": "runtime_error", "failure_envelope": {"stage": "judge_adapter", "returncode": None, "classification": "UNKNOWN_TECHNICAL", "stdout_tail": "", "stderr_tail": sanitize_tail(f"{type(exc).__name__}: {exc}")}}, ensure_ascii=False))
        raise SystemExit(2)
