#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

DEFAULT_MODEL = "gpt-5.6-sol"
FORBIDDEN_ENV = (
    "OPENAI_API_KEY","ANTHROPIC_API_KEY","GEMINI_API_KEY","GROQ_API_KEY","XAI_API_KEY",
    "QUALIFICATION_KEY","HELDOUT","SEALED_PACK"
)

def clean_env() -> dict[str,str]:
    env = os.environ.copy()
    for key in list(env):
        if key in FORBIDDEN_ENV or any(token in key.upper() for token in ("API_KEY","HELDOUT","SEALED_PACK")):
            env.pop(key,None)
    return env

def forbidden_event(event: dict) -> bool:
    item = event.get("item") if isinstance(event.get("item"),dict) else {}
    kinds = f"{event.get('type','')} {item.get('type','')}".lower()
    return any(x in kinds for x in ("command","tool","file_change","mcp","web_search"))

def schema() -> dict:
    return {
        "type":"object",
        "properties":{
            "decision":{"enum":["PASS","P1_FAIL","P0_FAIL"]},
            "failed_observables":{"type":"array","items":{"type":"string"}},
            "triggered_hard_fails":{"type":"array","items":{"type":"string"}},
            "brief_rationale":{"type":"string","maxLength":1200}
        },
        "required":["decision","failed_observables","triggered_hard_fails","brief_rationale"],
        "additionalProperties":False
    }

def run(payload: dict, model: str, timeout: int) -> tuple[dict,dict]:
    prompt = (
        "You are an independent development evaluator for Video Capture & Camera Operations. "
        "Grade professional function, truth, safety, evidence integrity, operator executability and boundary discipline; do not reward verbosity or film jargon. "
        "Use only the supplied visible fixture, expected observables, hard-fail list and candidate response. "
        "P0_FAIL if any listed hard-fail is materially triggered. P1_FAIL if no P0 hard-fail occurs but one or more required observables materially fail. "
        "PASS only when all material observables are satisfied. Do not use tools, shell, filesystem, web or MCP. Return schema-valid JSON only.\n\n"
        + json.dumps(payload,ensure_ascii=False)
    )
    with tempfile.TemporaryDirectory(prefix="video-capture-judge-") as raw:
        root = Path(raw)
        schema_path = root / "judge.schema.json"
        out = root / "judge.json"
        schema_path.write_text(json.dumps(schema()),encoding="utf-8")
        cmd = [
            "codex","exec","-","--json","--ephemeral","--ignore-user-config","--ignore-rules",
            "--skip-git-repo-check","--sandbox","read-only","--model",model,
            "--output-schema",str(schema_path),"--output-last-message",str(out),
            "--color","never","-C",str(root),"-c",'approval_policy="never"'
        ]
        proc = subprocess.run(cmd,input=prompt,text=True,capture_output=True,timeout=timeout,cwd=root,env=clean_env())
        if proc.returncode != 0:
            raise RuntimeError(f"Codex judge runtime failed ({proc.returncode}): {proc.stderr[-1200:]}")
        events = []
        for line in proc.stdout.splitlines():
            try: value = json.loads(line)
            except json.JSONDecodeError: continue
            if isinstance(value,dict): events.append(value)
        if any(forbidden_event(e) for e in events):
            raise RuntimeError("judge emitted forbidden tool/command event")
        if not out.is_file():
            raise RuntimeError("judge produced no result")
        completed = [e for e in events if e.get("type") == "turn.completed"]
        usage = completed[-1].get("usage") if completed else None
        return json.loads(out.read_text(encoding="utf-8")), {"usage":usage}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model",default=DEFAULT_MODEL)
    ap.add_argument("--timeout",type=int,default=300)
    args = ap.parse_args()
    payload = json.load(sys.stdin)
    if not isinstance(payload,dict):
        raise RuntimeError("stdin must be JSON object")
    judgment, transport = run(payload,args.model,args.timeout)
    print(json.dumps({
        "status":"completed",
        "provider":"codex-subscription-chatgpt-auth",
        "model":args.model,
        "judgment":judgment,
        "transport":transport
    },ensure_ascii=False))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status":"runtime_error","error":f"{type(exc).__name__}: {exc}"},ensure_ascii=False),file=sys.stderr)
        raise SystemExit(2)
