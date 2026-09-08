#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "stage-b-development-fixtures-v0.1.json"
CANDIDATE = HERE / "codex_candidate_adapter_v0.1.py"
JUDGE = HERE / "codex_judge_adapter_v0.1.py"
API_ENV = ("OPENAI_API_KEY","ANTHROPIC_API_KEY","GEMINI_API_KEY","GROQ_API_KEY","XAI_API_KEY")

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def invoke(script: Path, payload: dict, model: str, timeout: int) -> dict:
    proc = subprocess.run(
        [sys.executable,str(script),"--model",model,"--timeout",str(timeout)],
        input=json.dumps(payload,ensure_ascii=False),text=True,capture_output=True,timeout=timeout+30
    )
    if proc.returncode != 0:
        raise RuntimeError(f"{script.name} failed: {proc.stderr[-1600:]}")
    return json.loads(proc.stdout)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase",choices=["B0","B1"],required=True)
    ap.add_argument("--candidate-model",default="gpt-5.6-terra")
    ap.add_argument("--judge-model",default="gpt-5.6-sol")
    ap.add_argument("--timeout",type=int,default=300)
    ap.add_argument("--out",default="")
    args = ap.parse_args()

    if any(os.environ.get(k) for k in API_ENV):
        raise RuntimeError("metered API key present; Stage B route requires ChatGPT-subscription Codex only")

    pack = load_json(FIXTURES)
    want_p0 = args.phase == "B0"
    cases = [x for x in pack["fixtures"] if (x["severity"] == "P0") == want_p0]
    expected = 4 if want_p0 else 8
    if len(cases) != expected:
        raise RuntimeError(f"fixture cardinality mismatch:{len(cases)} expected={expected}")

    pre = subprocess.run(
        [sys.executable,str(CANDIDATE),"--preflight","--model",args.candidate_model],
        text=True,capture_output=True,timeout=60
    )
    if pre.returncode != 0:
        raise RuntimeError(f"candidate preflight failed before model calls: {pre.stderr[-1200:]}")

    rows = []
    candidate_calls = 0
    judge_calls = 0
    verdict = "PASS"

    for case in cases:
        visible = {
            "fixture_id":case["id"],
            "approved_context":case["context"],
            "task":"Produce the bounded camera-capture professional response for this case."
        }
        cand = invoke(CANDIDATE,visible,args.candidate_model,args.timeout)
        candidate_calls += 1
        judge_payload = {
            "fixture":{
                "id":case["id"],
                "severity":case["severity"],
                "context":case["context"],
                "expected_observables":case.get("expected_observables",[]),
                "hard_fail":case.get("hard_fail",[])
            },
            "candidate_response":cand["final_response"]
        }
        judged = invoke(JUDGE,judge_payload,args.judge_model,args.timeout)
        judge_calls += 1
        decision = judged["judgment"]["decision"]
        rows.append({
            "id":case["id"],
            "severity":case["severity"],
            "decision":decision,
            "judgment":judged["judgment"],
            "candidate_usage":cand.get("transport",{}).get("usage"),
            "judge_usage":judged.get("transport",{}).get("usage")
        })
        if decision != "PASS":
            verdict = "REVISE"
            if decision == "P0_FAIL" or want_p0:
                break

    report = {
        "schema_version":"1.0.0",
        "suite":pack["suite_id"],
        "phase":args.phase,
        "status":verdict,
        "candidate_model":args.candidate_model,
        "judge_model":args.judge_model,
        "provider":"codex-subscription-chatgpt-auth",
        "api_keys_bound":False,
        "candidate_calls":candidate_calls,
        "judge_calls":judge_calls,
        "retries":0,
        "results":rows,
        "qualification_claim":False
    }
    text = json.dumps(report,ensure_ascii=False,indent=2)+"\n"
    if args.out:
        Path(args.out).write_text(text,encoding="utf-8")
    print(text,end="")
    return 0 if verdict == "PASS" else 3

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({
            "status":"NOT_EXECUTABLE",
            "classification":"LOCAL_EXECUTION_FAIL_OR_RUNTIME_UNAVAILABLE",
            "error":f"{type(exc).__name__}: {exc}",
            "candidate_calls":0,
            "judge_calls":0
        },ensure_ascii=False),file=sys.stderr)
        raise SystemExit(2)
