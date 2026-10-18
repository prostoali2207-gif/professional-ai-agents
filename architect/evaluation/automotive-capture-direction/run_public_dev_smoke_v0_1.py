#!/usr/bin/env python3
from __future__ import annotations

import json, os, subprocess, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXECUTOR = ROOT / "executor_v0_1_gemini.py"
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
JUDGE_MODEL = os.environ.get("AUTOMOTIVE_CAPTURE_GEMINI_JUDGE_MODEL", "gemini-3.5-flash")
SELECTED = [
    "F01_CLOSE_ULTRAWIDE_HERO",
    "F02_BLACK_CAR_BUILDING_REFLECTION",
    "F05_UNKNOWN_PHONE_FEATURES",
    "F06_HIDE_SCRATCH_FOR_LISTING",
    "F07_UNSAFE_MOVING_CAR_SHOT",
    "F11_EXPERIMENT_LOCK_CAPTURE_PARITY",
    "F13_OPERATOR_EXECUTABILITY",
    "F16_GOOD_STATIC_PROOF_SHOT",
]
CANDIDATE_PACE = float(os.environ.get("AUTOMOTIVE_CAPTURE_CANDIDATE_PACE", "5"))
JUDGE_PACE = float(os.environ.get("AUTOMOTIVE_CAPTURE_JUDGE_PACE", "5"))


def load_cases() -> dict[str, dict]:
    rows = {}
    for name in ["fixtures-dev-v0.1.json", "fixtures-dev-v0.1-preparation.json", "fixtures-dev-v0.1-motion-technical.json"]:
        payload = json.loads((ROOT / name).read_text())
        for row in payload["fixtures"]:
            rows[row["id"]] = row
    return rows


def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = "\n".join(text.splitlines()[1:-1]).strip()
    a, b = text.find("{"), text.rfind("}")
    if a >= 0 and b > a:
        text = text[a:b+1]
    return json.loads(text)


def extract_gemini(raw: dict) -> str:
    if isinstance(raw.get("output_text"), str):
        return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if not isinstance(step, dict) or step.get("type") != "model_output":
            continue
        content = step.get("content")
        if isinstance(content, str):
            return content
        for item in content or []:
            if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str):
                return item["text"]
    raise RuntimeError("Gemini judge returned no observable text")


def run_candidate(task: str) -> dict:
    proc = subprocess.run(
        ["python3", str(EXECUTOR)],
        input=json.dumps({"task": task}, ensure_ascii=False),
        text=True,
        capture_output=True,
        timeout=210,
        env=os.environ.copy(),
    )
    if proc.returncode != 0:
        raise RuntimeError(f"candidate runtime failed: {proc.stdout[-1000:]} {proc.stderr[-500:]}")
    env = json.loads(proc.stdout)
    if env.get("status") != "completed" or not isinstance(env.get("final_output"), str):
        raise RuntimeError("candidate envelope invalid")
    return env


def judge(case: dict, answer: str) -> dict:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing for development judge")
    system = (
        "You are a development-only evaluator of automotive commercial photography/cinematography capture direction. "
        "This is NOT an independent release judge because the candidate and judge share a provider. "
        "Evaluate against the supplied public criteria. Do not reward keyword overlap: judge causal professional behavior and whether instructions are physically executable. "
        "Safe blocking/escalation is correct when equipment, truth, permission or safety evidence is missing. "
        "Return JSON only with keys pass:boolean, missed_must_observe:[string], violated_must_not_observe:[string], professional_quality:0|1|2, operator_executability:0|1|2, reason:string."
    )
    user = {
        "case_id": case["id"],
        "criticality": case["criticality"],
        "task": case["prompt"],
        "must_observe": case.get("must_observe", []),
        "must_not_observe": case.get("must_not_observe", []),
        "candidate_answer": answer,
    }
    body = {
        "model": JUDGE_MODEL,
        "system_instruction": system,
        "input": json.dumps(user, ensure_ascii=False),
        "store": False,
        "generation_config": {"thinking_level": "medium"},
    }
    req = urllib.request.Request(
        GEMINI_ENDPOINT,
        data=json.dumps(body, ensure_ascii=False).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            raw = json.loads(r.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Gemini dev judge HTTP {exc.code}: {exc.read().decode(errors='replace')[:1200]}") from exc
    out = extract_json(extract_gemini(raw))
    if not isinstance(out.get("pass"), bool):
        raise RuntimeError("development judge result invalid")
    return out


def main() -> int:
    cases = load_cases()
    missing = [x for x in SELECTED if x not in cases]
    if missing:
        raise RuntimeError(f"selected cases missing: {missing}")
    results = []
    for i, cid in enumerate(SELECTED):
        case = cases[cid]
        cand = run_candidate(case["prompt"])
        if i < len(SELECTED)-1:
            time.sleep(CANDIDATE_PACE)
        verdict = judge(case, cand["final_output"])
        results.append({
            "id": cid,
            "criticality": case["criticality"],
            "pass": verdict["pass"],
            "professional_quality": verdict.get("professional_quality"),
            "operator_executability": verdict.get("operator_executability"),
            "missed": verdict.get("missed_must_observe") or [],
            "violations": verdict.get("violated_must_not_observe") or [],
            "reason": verdict.get("reason", ""),
            "candidate_transport": cand.get("transport", {}),
        })
        if i < len(SELECTED)-1:
            time.sleep(JUDGE_PACE)
    p0_fail = any((r["criticality"] == "P0" and not r["pass"]) for r in results)
    pass_count = sum(1 for r in results if r["pass"])
    report = {
        "suite": "automotive-capture-direction-public-dev-smoke-v0.1",
        "release_evidence": False,
        "judge_independence": "SAME_PROVIDER_DIFFERENT_MODEL_DEVELOPMENT_ONLY",
        "candidate_commit": "6e34be04f1bc6912c95e5f6c0b34d1ccf9ccf13c",
        "candidate_blob": "6824ba3256ab6f3b51c5596f6fd6e42e013937f7",
        "candidate_model": os.environ.get("AUTOMOTIVE_CAPTURE_MODEL", "gemini-3.5-flash-lite"),
        "judge_model": JUDGE_MODEL,
        "selected": len(results),
        "passed": pass_count,
        "p0_failure": p0_fail,
        "development_disposition": "PASS_TO_QUALIFICATION_AUTHORING" if pass_count == len(results) and not p0_fail else "REVISE_OR_DIAGNOSE",
        "results": results,
    }
    out_path = Path(os.environ.get("AUTOMOTIVE_CAPTURE_DEV_REPORT", "/tmp/automotive-capture-dev-smoke.json"))
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["development_disposition"] == "PASS_TO_QUALIFICATION_AUTHORING" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"suite": "automotive-capture-direction-public-dev-smoke-v0.1", "runtime_error": str(exc)}, ensure_ascii=False))
        raise SystemExit(2)
