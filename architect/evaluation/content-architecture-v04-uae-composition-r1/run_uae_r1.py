#!/usr/bin/env python3
from __future__ import annotations

import argparse, base64, hashlib, hmac, json, os, subprocess, sys, time
from pathlib import Path
from cryptography.fernet import Fernet

HERE = Path(__file__).resolve().parent
GATE_ID = "content-architecture-v0.4-uae-composition-2026-09-01-r1"
CORE_SHA = "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
SPECIALIZATION_SHA = "7f41c2d1ba40c3b4c59e3eba2fb264c04162c320"
JUDGE_SHA = "669cdfcd0195d0507637d377b48f2650b4a870dd"
ADAPTER = Path("architect/evaluation/harness/adapters/codex_frozen_artifact_adapter.py")
ASSEMBLY_VERSION = "content-architecture-uae-composition-v1"


def derive(master: bytes, label: bytes) -> bytes:
    return hmac.new(master, GATE_ID.encode() + b"|" + label, hashlib.sha256).digest()


def canon(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def parse_json(text: str) -> dict:
    text = (text or "").strip()
    if text.startswith("```"):
        lines = text.splitlines(); text = "\n".join(lines[1:-1]).strip()
    try:
        obj = json.loads(text)
    except Exception:
        start = text.find("{"); end = text.rfind("}")
        if start < 0 or end <= start: raise ValueError("no JSON object")
        obj = json.loads(text[start:end+1])
    if not isinstance(obj, dict): raise ValueError("JSON output is not an object")
    return obj


def git_blob(sha: str) -> str:
    kind = subprocess.run(["git","cat-file","-t",sha], capture_output=True, text=True)
    if kind.returncode != 0 or kind.stdout.strip() != "blob": raise RuntimeError(f"missing blob {sha}")
    proc = subprocess.run(["git","cat-file","-p",sha], capture_output=True, text=False)
    if proc.returncode != 0: raise RuntimeError(f"cannot read blob {sha}")
    return proc.stdout.decode("utf-8")


def assemble_composed_blob() -> tuple[str, str]:
    core = git_blob(CORE_SHA)
    spec = git_blob(SPECIALIZATION_SHA)
    text = (
        core.rstrip() + "\n\n"
        + "--- BEGIN APPLIED UAE AUTOMOTIVE SPECIALIZATION ---\n"
        + spec.rstrip() + "\n"
        + "--- END APPLIED UAE AUTOMOTIVE SPECIALIZATION ---\n"
    )
    proc = subprocess.run(["git","hash-object","-w","--stdin"], input=text.encode("utf-8"), capture_output=True)
    if proc.returncode != 0: raise RuntimeError("cannot materialize composed blob")
    sha = proc.stdout.decode().strip()
    identity = hashlib.sha256((ASSEMBLY_VERSION + "|" + CORE_SHA + "|" + SPECIALIZATION_SHA + "|" + sha).encode()).hexdigest()
    return sha, identity


def load_pack(path: Path) -> dict:
    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode().strip()
    if not master: raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    key = base64.urlsafe_b64encode(derive(master, b"pack"))
    raw = Fernet(key).decrypt(path.read_bytes())
    pack = json.loads(raw)
    if pack.get("gate_id") != GATE_ID or pack.get("core_sha") != CORE_SHA or pack.get("specialization_sha") != SPECIALIZATION_SHA:
        raise RuntimeError("sealed pack identity mismatch")
    return pack


def call_artifact(sha: str, task: str, workspace: Path, timeout: int) -> dict:
    workspace.mkdir(parents=True, exist_ok=True)
    payload = {
        "protocol_version": 2,
        "candidate_sha": sha,
        "workspace": str(workspace.resolve()),
        "input": {"task": task, "allowed_resources": [], "fixture_tools": {}, "max_tool_rounds": 2},
    }
    proc = subprocess.run(
        [sys.executable, str(ADAPTER)], input=json.dumps(payload), capture_output=True,
        text=True, encoding="utf-8", errors="replace", timeout=timeout + 30,
    )
    if proc.returncode != 0:
        detail = (proc.stdout or "") + "\n" + (proc.stderr or "")
        raise RuntimeError("artifact runtime failed: " + detail[-1400:])
    raw = parse_json(proc.stdout)
    if raw.get("status") != "completed": raise RuntimeError("artifact runtime did not complete")
    if (raw.get("candidate_identity") or {}).get("sha") != sha: raise RuntimeError("artifact identity mismatch")
    return raw


def calibration_task(pair: dict, dimensions: dict, a: str, b: str) -> str:
    relevant = {k: dimensions[k] for k in pair["dimensions"]}
    return (
        "MODE: CALIBRATE\n\nBrief:\n" + pair["brief"]
        + "\n\nRelevant dimensions:\n" + json.dumps(relevant, ensure_ascii=False, indent=2)
        + "\n\nArtifact A:\n" + a + "\n\nArtifact B:\n" + b
        + "\n\nChoose the professionally stronger artifact. Return only the calibration JSON required by your assessor instructions."
    )


def assess_task(case: dict, dimensions: dict, artifact: str) -> str:
    relevant = {k: dimensions[k] for k in case["relevant_dimensions"]}
    return (
        "MODE: ASSESS\n\nSynthetic evaluation brief:\n" + case["task"]
        + "\n\nRelevant dimensions:\n" + json.dumps(relevant, ensure_ascii=False, indent=2)
        + "\n\nSubmitted architecture:\n" + artifact
        + "\n\nAssess only this architecture against the brief and rubric. Return only assessment JSON."
    )


def validate_candidate_shape(obj: dict) -> list[str]:
    failures = []
    if obj.get("status") not in {"READY_WITH_BOUNDS","BLOCKED","NEEDS_UPSTREAM"}: failures.append("invalid status")
    if not isinstance(obj.get("decision_results"), list): failures.append("decision_results missing")
    if not isinstance(obj.get("lock_results"), list): failures.append("lock_results missing")
    arch = obj.get("architecture")
    if not isinstance(arch, dict): failures.append("architecture missing"); arch = {}
    for k in ["attention_job","block_sequence","proof_requirements","pacing_intent"]:
        if k not in arch: failures.append(f"architecture.{k} missing")
    handoff = obj.get("creator_handoff")
    if not isinstance(handoff, dict): failures.append("creator_handoff missing"); handoff = {}
    for k in ["must_preserve","may_choose","blocked_portions","must_escalate"]:
        if not isinstance(handoff.get(k), list): failures.append(f"creator_handoff.{k} missing/wrong type")
    if not isinstance(obj.get("boundary_notes"), list): failures.append("boundary_notes missing")
    return failures


def mechanical_case(case: dict, obj: dict) -> dict:
    failures = validate_candidate_shape(obj)
    hard = []
    if obj.get("status") != "READY_WITH_BOUNDS": failures.append("overblocked_or_upstream_status")
    decisions = {}
    for row in obj.get("decision_results") or []:
        if isinstance(row, dict) and isinstance(row.get("decision_id"), str): decisions[row["decision_id"]] = row
    for did, exp in case["expected_decisions"].items():
        row = decisions.get(did)
        if not row:
            failures.append(f"missing decision {did}"); continue
        if row.get("disposition") != exp["disposition"]: failures.append(f"{did} disposition")
        if row.get("public_use") is not exp["public_use"]:
            failures.append(f"{did} public_use")
            if exp["public_use"] is False and row.get("public_use") is True: hard.append(f"unsafe public use {did}")
        if row.get("basis") not in exp["allowed_basis"]: failures.append(f"{did} basis")
    locks = {}
    for row in obj.get("lock_results") or []:
        if isinstance(row, dict) and isinstance(row.get("lock_id"), str): locks[row["lock_id"]] = row
    for lid in case["expected_locks"]:
        row = locks.get(lid)
        if not row: failures.append(f"missing lock {lid}")
        elif row.get("preserved") is not True:
            failures.append(f"lock not preserved {lid}"); hard.append(f"lock breach {lid}")
    return {"pass": not failures, "failures": failures, "hard_failures": hard}


def validate_assessment(obj: dict, dims: list[str]) -> list[str]:
    failures = []
    if not isinstance(obj.get("hard_failures"), list): failures.append("hard_failures not list")
    scores = obj.get("scores")
    if not isinstance(scores, dict): failures.append("scores not object"); scores = {}
    for d in dims:
        v = scores.get(d)
        if not isinstance(v, int) or isinstance(v, bool) or v < 0 or v > 3: failures.append(f"bad score {d}")
    if set(scores) - set(dims): failures.append("unexpected score dimension")
    if obj.get("release_recommendation") not in {"PASS","FAIL"}: failures.append("bad release_recommendation")
    return failures


def run_calibrate(pack: dict, out: Path, timeout: int) -> int:
    correct = 0; rows = []
    for pair in pack["calibration_pairs"]:
        swap = int(hashlib.sha256(f"{GATE_ID}|{pair['id']}".encode()).hexdigest()[:2], 16) % 2 == 1
        a, b = (pair["challenger"], pair["strong"]) if swap else (pair["strong"], pair["challenger"])
        expected = "B" if swap else "A"
        raw = call_artifact(JUDGE_SHA, calibration_task(pair, pack["dimensions"], a, b), out / "judge-calibration" / pair["id"], timeout)
        obj = parse_json(raw.get("final_output", "")); winner = obj.get("winner")
        if winner not in {"A","B"}: raise RuntimeError("invalid calibration output")
        ok = winner == expected; correct += int(ok); rows.append({"id": pair["id"], "correct": ok})
    rate = correct / len(pack["calibration_pairs"])
    passed = rate >= pack["release_policy"]["calibration_expected_winner_rate_min"]
    report = {"gate_id":GATE_ID,"status":"CALIBRATION_PASS" if passed else "CALIBRATION_FAIL","candidate_calls":0,"judge_calls":len(rows),"expected_winner_rate":rate,"policy":pack["release_policy"]["calibration_expected_winner_rate_min"]}
    out.mkdir(parents=True, exist_ok=True); (out/"calibration-report.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(report,sort_keys=True)); return 0 if passed else 10


def run_score(pack: dict, out: Path, timeout: int) -> int:
    composed_sha, composed_identity = assemble_composed_blob()
    out.mkdir(parents=True, exist_ok=True)
    cases_sanitized = []; full_records = []; score_values = []; mech_hard = 0; judge_hard = 0; all_judge_pass = True
    for case in pack["cases"]:
        started=time.time()
        raw = call_artifact(composed_sha, case["task"], out/"candidate-work"/case["id"], timeout)
        artifact_text = raw.get("final_output", ""); obj = parse_json(artifact_text)
        mech = mechanical_case(case, obj); mech_hard += len(mech["hard_failures"])
        jraw = call_artifact(JUDGE_SHA, assess_task(case, pack["dimensions"], artifact_text), out/"judge-work"/case["id"], timeout)
        assessment = parse_json(jraw.get("final_output", "")); shape = validate_assessment(assessment, case["relevant_dimensions"])
        if shape: raise RuntimeError(f"invalid judge assessment: {shape}")
        scores = assessment["scores"]; score_values.extend(scores[d] for d in case["relevant_dimensions"])
        hc = len(assessment["hard_failures"]); judge_hard += hc
        jpass = assessment["release_recommendation"]=="PASS" and hc==0 and all(scores[d]>=pack["release_policy"]["per_case_judge_min_dimension"] for d in case["relevant_dimensions"])
        all_judge_pass = all_judge_pass and jpass
        sanitized = {"id":case["id"],"mechanical_pass":mech["pass"],"mechanical_failure_count":len(mech["failures"]),"mechanical_hard_failure_count":len(mech["hard_failures"]),"judge_scores":scores,"judge_hard_failure_count":hc,"judge_release_recommendation":assessment["release_recommendation"]}
        cases_sanitized.append(sanitized)
        full_records.append({"id":case["id"],"candidate_output":artifact_text,"candidate_identity":raw.get("candidate_identity"),"candidate_transport":raw.get("transport"),"mechanical":mech,"judge":assessment,"duration_s":round(time.time()-started,3)})
    pol=pack["release_policy"]
    mech_rate=sum(1 for c in cases_sanitized if c["mechanical_pass"])/len(cases_sanitized)
    mean=sum(score_values)/len(score_values) if score_values else 0.0
    passed=(mech_rate>=pol["mechanical_case_pass_rate"] and mech_hard<=pol["mechanical_hard_failures_allowed"] and judge_hard<=pol["judge_hard_failures_allowed"] and all_judge_pass and mean>=pol["judge_aggregate_mean_min"])
    verdict="PASS" if passed else "REVISE"
    report={"gate_id":GATE_ID,"verdict":verdict,"core_sha":CORE_SHA,"specialization_sha":SPECIALIZATION_SHA,"assembly_version":ASSEMBLY_VERSION,"composed_blob_sha":composed_sha,"composed_identity_sha256":composed_identity,"case_count":len(cases_sanitized),"candidate_calls":len(cases_sanitized),"judge_calls":len(cases_sanitized),"mechanical_case_pass_rate":mech_rate,"mechanical_hard_failure_count":mech_hard,"judge_hard_failure_count":judge_hard,"all_cases_judge_release_pass":all_judge_pass,"judge_aggregate_mean":mean,"policy":pol,"cases":cases_sanitized,"universal_release_evidence":{"gate_id":"content-architecture-v0.4-universal-release-2026-09-01-r1","workflow_run_id":33501449175,"verdict":"PASS","reuse_scope":"universal professional quality; this gate tests only UAE composition delta"}}
    (out/"qualification-report.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    master=os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY","").encode().strip(); records=canon(full_records); rid=hashlib.sha256(records).hexdigest(); key=base64.urlsafe_b64encode(derive(master,b"run-records")); sealed=Fernet(key).encrypt(records)
    (out/"sealed-run-records.bin").write_bytes(sealed); (out/"run-records-manifest.json").write_text(json.dumps({"identity_sha256":rid,"sealed_sha256":hashlib.sha256(sealed).hexdigest(),"record_count":len(full_records)},indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"gate_id":GATE_ID,"verdict":verdict,"case_count":len(cases_sanitized),"mechanical_case_pass_rate":mech_rate,"mechanical_hard_failure_count":mech_hard,"judge_hard_failure_count":judge_hard,"judge_aggregate_mean":mean},sort_keys=True))
    return 0 if passed else 20


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=["calibrate","score"],required=True); ap.add_argument("--pack",required=True); ap.add_argument("--out",required=True); ap.add_argument("--timeout",type=int,default=300); args=ap.parse_args()
    try:
        pack=load_pack(Path(args.pack))
        return run_calibrate(pack,Path(args.out),args.timeout) if args.mode=="calibrate" else run_score(pack,Path(args.out),args.timeout)
    except Exception as exc:
        Path(args.out).mkdir(parents=True,exist_ok=True); report={"gate_id":GATE_ID,"status":"NOT_EXECUTABLE","error_type":type(exc).__name__,"error":str(exc)[:1200]}; (Path(args.out)/"runtime-failure.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(report,sort_keys=True)); return 1


if __name__=="__main__": raise SystemExit(main())
