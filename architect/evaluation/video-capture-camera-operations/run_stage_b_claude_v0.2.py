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
CANDIDATE = HERE / "claude_candidate_adapter_v0.2.py"
JUDGE = HERE / "claude_judge_adapter_v0.1.py"
METERED_ENV = ("ANTHROPIC_API_KEY","OPENAI_API_KEY","GEMINI_API_KEY","GROQ_API_KEY","XAI_API_KEY")

class RunFailure(RuntimeError):
    def __init__(self, message: str, classification: str, candidate_calls: int, judge_calls: int):
        super().__init__(message)
        self.classification = classification
        self.candidate_calls = candidate_calls
        self.judge_calls = judge_calls

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def classify_failure(text: str) -> str:
    value = text.lower()
    if any(x in value for x in ("no such file or directory: 'claude'", "claude code is not authenticated", "command not found")):
        return "RUNTIME_UNAVAILABLE"
    if any(x in value for x in ("unknown model", "model not found", "authentication", "unauthorized", "permission denied", "usage limit", "rate limit", "429")):
        return "PROVIDER_RUNTIME_FAIL"
    if any(x in value for x in ("timeout", "timed out", "temporarily unavailable", "connection reset", "http 500", "http 502", "http 503", "http 504")):
        return "TRANSIENT_TRANSPORT"
    return "LOCAL_EXECUTION_FAIL"

def invoke(script: Path, payload: dict, model: str, timeout: int) -> dict:
    proc = subprocess.run(
        [sys.executable,str(script),"--model",model,"--timeout",str(timeout)],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,capture_output=True,timeout=timeout+30
    )
    if proc.returncode != 0:
        raise RuntimeError(f"{script.name} failed: {proc.stderr[-1800:]}")
    return json.loads(proc.stdout)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase",choices=["B0","B1"],required=True)
    ap.add_argument("--candidate-model",default="sonnet")
    ap.add_argument("--judge-model",default="opus")
    ap.add_argument("--timeout",type=int,default=300)
    ap.add_argument("--out",default="")
    args = ap.parse_args()

    candidate_calls = 0
    judge_calls = 0

    try:
        if any(os.environ.get(k) for k in METERED_ENV):
            raise RunFailure(
                "metered API key present; Claude Code route requires subscription auth only",
                "LOCAL_EXECUTION_FAIL",candidate_calls,judge_calls
            )

        pack = load_json(FIXTURES)
        want_p0 = args.phase == "B0"
        cases = [x for x in pack["fixtures"] if (x["severity"] == "P0") == want_p0]
        expected = 4 if want_p0 else 8
        if len(cases) != expected:
            raise RunFailure(
                f"fixture cardinality mismatch:{len(cases)} expected={expected}",
                "EVALUATOR_CONSTRUCT_FAIL",candidate_calls,judge_calls
            )

        pre = subprocess.run(
            [sys.executable,str(CANDIDATE),"--preflight","--model",args.candidate_model],
            text=True,capture_output=True,timeout=60
        )
        if pre.returncode != 0:
            detail = pre.stderr[-1400:]
            raise RunFailure(
                f"candidate preflight failed before model calls:{detail}",
                classify_failure(detail),candidate_calls,judge_calls
            )

        rows = []
        verdict = "PASS"

        for case in cases:
            visible = {
                "fixture_id":case["id"],
                "approved_context":case["context"],
                "task":"Produce the bounded camera-capture professional response for this case."
            }
            try:
                cand = invoke(CANDIDATE,visible,args.candidate_model,args.timeout)
            except Exception as exc:
                raise RunFailure(str(exc),classify_failure(str(exc)),candidate_calls,judge_calls) from exc
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
            try:
                judged = invoke(JUDGE,judge_payload,args.judge_model,args.timeout)
            except Exception as exc:
                raise RunFailure(str(exc),classify_failure(str(exc)),candidate_calls,judge_calls) from exc
            judge_calls += 1

            decision = judged["judgment"]["decision"]
            rows.append({
                "id":case["id"],
                "severity":case["severity"],
                "decision":decision,
                "judgment":judged["judgment"]
            })
            if decision != "PASS":
                verdict = "REVISE"
                break

        report = {
            "schema_version":"1.0.0",
            "candidate_id":"video-capture-camera-operations-v0.2",
            "suite":pack["suite_id"],
            "phase":args.phase,
            "status":verdict,
            "candidate_model":args.candidate_model,
            "judge_model":args.judge_model,
            "provider":"claude-code-subscription",
            "api_keys_bound":False,
            "candidate_calls":candidate_calls,
            "judge_calls":judge_calls,
            "retries":0,
            "results":rows,
            "qualification_claim":False
        }
        text_out = json.dumps(report, ensure_ascii=False, indent=2)+"\n"
        if args.out:
            Path(args.out).write_text(text_out, encoding="utf-8")
        print(text_out, end="")
        return 0 if verdict == "PASS" else 3

    except RunFailure as exc:
        report = {
            "status":"NOT_EXECUTABLE",
            "classification":exc.classification,
            "error":str(exc),
            "candidate_calls":exc.candidate_calls,
            "judge_calls":exc.judge_calls,
            "retries":0,
            "qualification_claim":False
        }
        text_out = json.dumps(report, ensure_ascii=False, indent=2)+"\n"
        if args.out:
            Path(args.out).write_text(text_out, encoding="utf-8")
        print(text_out, end="", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
