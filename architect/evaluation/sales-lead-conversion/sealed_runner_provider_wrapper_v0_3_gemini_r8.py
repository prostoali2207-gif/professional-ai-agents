#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request
from typing import Any

from gemini_rate_limiter import pace, retry_delay_seconds

CYCLE_ID="sales-0.3-fresh-independent-2026-08-23-r8-gemini-paced"
PROVIDER_WRAPPER=Path("architect/evaluation/sales-lead-conversion/sealed_runner_provider_wrapper_v0_3_gemini.py")
EXPECTED_WRAPPER_BLOB="dbb30da2f7be61f5ae8f8bf9ed922dbf00e92cdd"
ENDPOINT="https://generativelanguage.googleapis.com/v1beta/interactions"
MODEL="gemini-3.5-flash-lite"


def load_provider():
    actual=subprocess.check_output(["git","hash-object",str(PROVIDER_WRAPPER)],text=True).strip()
    if actual!=EXPECTED_WRAPPER_BLOB: raise RuntimeError(f"provider wrapper drift: {actual}")
    spec=importlib.util.spec_from_file_location("sales_gemini_r8_provider",PROVIDER_WRAPPER)
    if spec is None or spec.loader is None: raise RuntimeError("cannot load pinned Gemini provider wrapper")
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def structured_grade_call(provider,system:str,user:dict[str,Any]):
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key: raise RuntimeError("GEMINI_API_KEY missing for grader")
    schema={"type":"object","properties":{"scores":{"type":"array","items":{"type":"integer","minimum":0,"maximum":2},"minItems":3,"maxItems":3},"pass":{"type":"boolean"},"critical_hard_fails":{"type":"array","items":{"type":"string"}},"rationale_tags":{"type":"array","items":{"type":"string"}}},"required":["scores","pass","critical_hard_fails","rationale_tags"],"additionalProperties":False}
    body={"model":MODEL,"store":False,"input":[{"type":"user_input","content":[{"type":"text","text":json.dumps(user,ensure_ascii=False)}]}],"system_instruction":system+" Call submit_grade exactly once with the final grade. Do not return narrative text.","generation_config":{"thinking_level":os.environ.get("GEMINI_THINKING_LEVEL","medium")},"tools":[{"type":"function","name":"submit_grade","description":"Submit the final blinded qualification grade.","parameters":schema}]}
    for attempt in range(2):
        pace()
        req=urllib.request.Request(ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",headers={"Content-Type":"application/json","x-goog-api-key":key})
        try:
            with urllib.request.urlopen(req,timeout=120) as response: payload=json.loads(response.read().decode())
            break
        except urllib.error.HTTPError as exc:
            text=exc.read().decode('utf-8','replace')
            if exc.code==429 and attempt==0:
                time.sleep(retry_delay_seconds(exc.headers,text)); continue
            raise RuntimeError(f"Gemini grader HTTP {exc.code}: {text[-1200:]}") from exc
    else: raise RuntimeError("Gemini grader retry loop exhausted")
    calls=[x for x in (payload.get("steps") or []) if isinstance(x,dict) and x.get("type")=="function_call" and x.get("name")=="submit_grade"]
    if len(calls)!=1: raise RuntimeError(f"grader structured output expected exactly one submit_grade call, observed {len(calls)}")
    result=calls[0].get("arguments")
    if not isinstance(result,dict): raise RuntimeError("grader submit_grade arguments are not an object")
    return result,provider.normalize_usage(payload.get("usage") or payload.get("usageMetadata"))


def main()->int:
    provider=load_provider(); provider.CYCLE_ID=CYCLE_ID
    original=provider.load_base
    def load_base_from_sealed_pack():
        module=original(); module.__file__=str(Path(__file__).resolve()); return module
    provider.load_base=load_base_from_sealed_pack
    provider.gemini_call=lambda system,user: structured_grade_call(provider,system,user)
    return int(provider.main())

if __name__=="__main__": raise SystemExit(main())
