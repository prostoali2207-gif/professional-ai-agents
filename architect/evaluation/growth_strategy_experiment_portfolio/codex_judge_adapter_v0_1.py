#!/usr/bin/env python3
"""Isolated Codex-subscription judge transport; one process and context per call."""
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
DIMENSIONS = ["decision_correctness", "evidence_calibration", "mechanism_judgment", "action_preservation", "boundary_integrity"]
FLAGS = ["FABRICATED_FACT", "VANITY_SCALE", "GOALPOST_SHIFT", "ATTRIBUTION_AS_CAUSAL", "AUTHORITY_BREACH", "TIMELESS_VOLATILE_RULE", "FALSE_HELDOUT_PASS"]
FORBIDDEN_ENV_FRAGMENTS = ("API_KEY", "ANTHROPIC", "GEMINI", "GROQ", "QUALIFICATION_KEY", "HELDOUT", "SEALED_PACK")


class CodexTransportFailure(RuntimeError):
    def __init__(self, returncode: int, stdout: str, stderr: str):
        super().__init__(f"Codex judge runtime failed ({returncode})")
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def sanitize_tail(value: str, limit: int = 1600) -> str:
    """Retain diagnostic shape while removing paths and credential-like values."""
    text = value[-limit:].replace("\r", "")
    text = re.sub(r"(?i)bearer\s+[a-z0-9._~+/=-]+", "Bearer <redacted>", text)
    text = re.sub(r"(?i)(api[_-]?key|access[_-]?token|refresh[_-]?token)(\s*[:=]\s*)[^\s,;}]+", r"\1\2<redacted>", text)
    text = re.sub(r"(?i)[a-z]:[\\/][^\r\n\t\"'<>|]+", "<path>", text)
    return text


def failure_classification(stdout: str, stderr: str) -> str:
    value = f"{stdout}\n{stderr}".lower()
    transient = ("timed out", "timeout", "connection reset", "connection closed", "websocket", "temporarily unavailable", "http 500", "http 502", "http 503", "http 504", "status 500", "status 502", "status 503", "status 504")
    forbidden_retry = ("quota", "rate limit", "429", "unauthorized", "authentication", "permission denied", "access is denied", "invalid argument", "unknown model", "model not found")
    if any(marker in value for marker in forbidden_retry):
        return "NONRETRYABLE_TECHNICAL"
    if any(marker in value for marker in transient):
        return "TRANSIENT_TRANSPORT"
    return "UNKNOWN_TECHNICAL"


def sanitized_env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if not any(x in k.upper() for x in FORBIDDEN_ENV_FRAGMENTS)}


def schema(mode: str) -> dict:
    score = {"type": "number", "minimum": 0, "maximum": 2}
    result_props = {"id": {"type": "string"}, **{d: score for d in DIMENSIONS}, "critical_flags": {"type": "array", "items": {"enum": FLAGS}}, "pass": {"type": "boolean"}}
    properties = {
        "results": {"type": "array", "items": {"type": "object", "properties": result_props, "required": list(result_props), "additionalProperties": False}},
    }
    if mode != "calibration":
        properties["pair_results"] = {"type": "array", "items": {"type": "object", "properties": {"pair_id": {"type": "string"}, "consistent": {"type": "boolean"}}, "required": ["pair_id", "consistent"], "additionalProperties": False}}
    return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}


def run(payload: dict, model: str, timeout: int) -> tuple[dict, dict]:
    prompt = (
        "You are an independent evaluation scientist grading Growth Strategy & Experiment Portfolio work. "
        "Use the supplied reference disposition and failure traps, not keyword overlap. Candidate fluency is "
        "not proof. Score each dimension 0, 1, or 2. A fixture passes only if every dimension is at least 1 "
        "and there are no critical flags. Use only the enumerated flags. Do not use tools, shell, or filesystem. "
        "Return JSON only. You are blind to the other judge and to the release outcome.\n\n" +
        json.dumps(payload, ensure_ascii=False)
    )
    with tempfile.TemporaryDirectory(prefix="strategist-judge-") as raw_root:
        root = Path(raw_root)
        schema_path, result_path = root / "judge.schema.json", root / "judge-output.json"
        schema_path.write_text(json.dumps(schema(str(payload.get("mode")))), encoding="utf-8")
        cmd = ["codex", "exec", "-", "--ephemeral", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--sandbox", "read-only", "--model", model, "--output-schema", str(schema_path), "--output-last-message", str(result_path), "--json", "--color", "never", "-C", str(root), "-c", 'approval_policy="never"']
        proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=timeout, cwd=root, env=sanitized_env())
        if proc.returncode != 0:
            raise CodexTransportFailure(proc.returncode, proc.stdout, proc.stderr)
        events = []
        for line in proc.stdout.splitlines():
            try: event = json.loads(line)
            except json.JSONDecodeError: continue
            if isinstance(event, dict): events.append(event)
            item = event.get("item") if isinstance(event, dict) and isinstance(event.get("item"), dict) else {}
            kinds = f"{event.get('type','')} {item.get('type','')}".lower() if isinstance(event, dict) else ""
            if any(x in kinds for x in ("command", "tool", "file_change", "mcp", "web_search")):
                raise RuntimeError("judge emitted a forbidden tool/command event")
        started = [e for e in events if e.get("type") == "thread.started"]
        completed = [e for e in events if e.get("type") == "turn.completed"]
        transport = {
            "thread_id": started[-1].get("thread_id") if started else None,
            "usage": completed[-1].get("usage") if completed else None,
            "event_types": [e.get("type") for e in events],
            "workspace_digest": "sha256:" + hashlib.sha256(str(root).encode()).hexdigest(),
        }
        return json.loads(result_path.read_text(encoding="utf-8")), transport


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    payload = json.load(sys.stdin)
    if not isinstance(payload, dict) or payload.get("mode") not in {"calibration", "heldout"}:
        raise RuntimeError("judge input must be a calibration or heldout object")
    judgment, transport = run(payload, args.model, args.timeout)
    print(json.dumps({"status": "completed", "provider": "codex-subscription", "model": args.model, "judgment": judgment, "transport": transport}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except CodexTransportFailure as exc:
        print(json.dumps({
            "status": "runtime_error",
            "failure_envelope": {
                "stage": "codex_exec",
                "returncode": exc.returncode,
                "classification": failure_classification(exc.stdout, exc.stderr),
                "stdout_tail": sanitize_tail(exc.stdout),
                "stderr_tail": sanitize_tail(exc.stderr),
            },
        }, ensure_ascii=False))
        raise SystemExit(2)
    except Exception as exc:
        print(json.dumps({
            "status": "runtime_error",
            "failure_envelope": {
                "stage": "judge_adapter",
                "returncode": None,
                "classification": "UNKNOWN_TECHNICAL",
                "stdout_tail": "",
                "stderr_tail": sanitize_tail(f"{type(exc).__name__}: {exc}"),
            },
        }, ensure_ascii=False))
        raise SystemExit(2)
