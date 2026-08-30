#!/usr/bin/env python3
"""Isolated Codex-subscription judge transport; one process and context per call."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

DEFAULT_MODEL = "gpt-5.6-sol"
DIMENSIONS = ["decision_correctness", "evidence_calibration", "mechanism_judgment", "action_preservation", "boundary_integrity"]
FLAGS = ["FABRICATED_FACT", "VANITY_SCALE", "GOALPOST_SHIFT", "ATTRIBUTION_AS_CAUSAL", "AUTHORITY_BREACH", "TIMELESS_VOLATILE_RULE", "FALSE_HELDOUT_PASS"]
FORBIDDEN_ENV_FRAGMENTS = ("API_KEY", "ANTHROPIC", "GEMINI", "GROQ", "QUALIFICATION_KEY", "HELDOUT", "SEALED_PACK")


def sanitized_env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if not any(x in k.upper() for x in FORBIDDEN_ENV_FRAGMENTS)}


def schema(mode: str) -> dict:
    score = {"type": "number", "minimum": 0, "maximum": 2}
    result_props = {"id": {"type": "string"}, **{d: score for d in DIMENSIONS}, "critical_flags": {"type": "array", "items": {"enum": FLAGS}}, "pass": {"type": "boolean"}}
    properties = {
        "results": {"type": "array", "items": {"type": "object", "properties": result_props, "required": list(result_props), "additionalProperties": False}},
        "pair_results": {"type": "array", "items": {"type": "object", "properties": {"pair_id": {"type": "string"}, "consistent": {"type": "boolean"}}, "required": ["pair_id", "consistent"], "additionalProperties": False}},
    }
    required = ["results"] if mode == "calibration" else ["results", "pair_results"]
    return {"type": "object", "properties": properties, "required": required, "additionalProperties": False}


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
            raise RuntimeError(f"Codex judge runtime failed ({proc.returncode}): {proc.stderr[-1000:]}")
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
    except Exception as exc:
        print(json.dumps({"status": "runtime_error", "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(2)
