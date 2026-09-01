#!/usr/bin/env python3
from __future__ import annotations

import argparse, base64, hashlib, hmac, json, os, subprocess, sys, time
from pathlib import Path
from cryptography.fernet import Fernet

HERE = Path(__file__).resolve().parent
GATE_ID = "content-architecture-v0.4-universal-release-2026-09-01-r1"
CANDIDATE_SHA = "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
JUDGES = {
    "senior_practitioner": "99bf30695e502b154d76f1d27b80ebc01ea5b4fd",
    "competency_assessor": "e726fdf8534ced97ea8c4fd4060f5eeb058d6f75",
}
ADAPTER = Path("architect/evaluation/harness/adapters/codex_frozen_artifact_adapter.py")


def derive(master: bytes, label: bytes) -> bytes:
    return hmac.new(master, GATE_ID.encode() + b"|" + label, hashlib.sha256).digest()


def canon(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def load_pack(path: Path) -> dict:
    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode()
    if not master:
        raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    key = base64.urlsafe_b64encode(derive(master, b"fernet"))
    raw = Fernet(key).decrypt(path.read_bytes())
    pack = json.loads(raw)
    if pack.get("gate_id") != GATE_ID or pack.get("candidate_sha") != CANDIDATE_SHA:
        raise RuntimeError("sealed pack identity mismatch")
    return pack


def parse_json(text: str) -> dict:
    text = (text or "").strip()
    if text.startswith("```"):
        lines = text.splitlines(); text = "\n".join(lines[1:-1]).strip()
    try:
        obj = json.loads(text)
    except Exception:
        start = text.find("{"); end = text.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("no JSON object")
        obj = json.loads(text[start:end+1])
    if not isinstance(obj, dict):
        raise ValueError("JSON output is not an object")
    return obj


def call_artifact(artifact_sha: str, task: str, workspace: Path, timeout: int) -> dict:
    workspace.mkdir(parents=True, exist_ok=True)
    payload = {
        "protocol_version": 2,
        "candidate_sha": artifact_sha,
        "workspace": str(workspace.resolve()),
        "input": {"task": task, "allowed_resources": [], "fixture_tools": {}, "max_tool_rounds": 2},
    }
    proc = subprocess.run(
        [sys.executable, str(ADAPTER)], input=json.dumps(payload), capture_output=True,
        text=True, encoding="utf-8", errors="replace", timeout=timeout,
    )
    if proc.returncode != 0:
        detail = (proc.stdout or "") + "\n" + (proc.stderr or "")
        raise RuntimeError("artifact runtime failed: " + detail[-1200:])
    raw = parse_json(proc.stdout)
    if raw.get("status") != "completed":
        raise RuntimeError("artifact runtime did not complete")
    ident = raw.get("candidate_identity") or {}
    if ident.get("sha") != artifact_sha:
        raise RuntimeError("artifact identity mismatch")
    return raw


def mechanical_contract(obj: dict) -> list[str]:
    failures = []
    allowed_status = {"READY_WITH_BOUNDS", "BLOCKED", "NEEDS_UPSTREAM"}
    if obj.get("status") not in allowed_status:
        failures.append("status invalid")
    required_types = {
        "attention_contract": dict,
        "block_sequence": list,
        "proof_architecture": list,
        "pacing": dict,
        "creator_handoff": dict,
        "structural_observability": dict,
        "boundary_notes": list,
    }
    for key, typ in required_types.items():
        if not isinstance(obj.get(key), typ):
            failures.append(f"{key} wrong type or missing")
    ac = obj.get("attention_contract") if isinstance(obj.get("attention_contract"), dict) else {}
    for key in ["opening_job","viewer_question_or_tension","payoff_obligation","evidence_dependency"]:
        if key not in ac: failures.append(f"attention_contract.{key} missing")
    blocks = obj.get("block_sequence") if isinstance(obj.get("block_sequence"), list) else []
    if not blocks: failures.append("block_sequence empty")
    else:
        for i, block in enumerate(blocks):
            if not isinstance(block, dict): failures.append(f"block_sequence[{i}] not object"); continue
            for key in ["block_id","job","information_required","proof_requirement","position_band","transition_job"]:
                if key not in block: failures.append(f"block_sequence[{i}].{key} missing")
    pacing = obj.get("pacing") if isinstance(obj.get("pacing"), dict) else {}
    for key in ["mode","macro_zones","notes"]:
        if key not in pacing: failures.append(f"pacing.{key} missing")
    handoff = obj.get("creator_handoff") if isinstance(obj.get("creator_handoff"), dict) else {}
    for key in ["must_preserve","bounded","may_choose","must_escalate"]:
        if not isinstance(handoff.get(key), list): failures.append(f"creator_handoff.{key} missing/wrong type")
    obs = obj.get("structural_observability") if isinstance(obj.get("structural_observability"), dict) else {}
    for key in ["hook_family_or_job","block_order","proof_positions","tested_or_locked_variables"]:
        if key not in obs: failures.append(f"structural_observability.{key} missing")
    return failures


def calibration_task(pair: dict, dimensions: dict, a: str, b: str) -> str:
    relevant = {k: dimensions[k] for k in pair["dimensions"]}
    return (
        "MODE: CALIBRATE\n\n"
        + "Brief:\n" + pair["brief"] + "\n\n"
        + "Relevant dimensions:\n" + json.dumps(relevant, ensure_ascii=False, indent=2) + "\n\n"
        + "Artifact A:\n" + a + "\n\nArtifact B:\n" + b + "\n\n"
        + "Choose the professionally stronger artifact. Return only the calibration JSON required by your assessor instructions."
    )


def assess_task(case: dict, dimensions: dict, artifact: str) -> str:
    relevant = {k: dimensions[k] for k in case["relevant_dimensions"]}
    return (
        "MODE: ASSESS\n\n"
        + "Brief:\n" + case["brief"] + "\n\n"
        + "Relevant dimensions:\n" + json.dumps(relevant, ensure_ascii=False, indent=2) + "\n\n"
        + "Submitted artifact:\n" + artifact + "\n\n"
        + "Assess only this artifact against the brief and rubric. Return only the assessment JSON required by your assessor instructions."
    )


def run_calibration(pack: dict, out: Path, timeout: int) -> int:
    rows = []
    judge_correct = {name: 0 for name in JUDGES}
    judge_total = {name: 0 for name in JUDGES}
    disagreements = 0
    for pair in pack["calibration_pairs"]:
        winners = {}
        for judge_name, judge_sha in JUDGES.items():
            swap = int(hashlib.sha256(f"{GATE_ID}|{pair['id']}|{judge_name}".encode()).hexdigest()[:2], 16) % 2 == 1
            a, b = (pair["challenger"], pair["strong"]) if swap else (pair["strong"], pair["challenger"])
            expected = "B" if swap else "A"
            raw = call_artifact(judge_sha, calibration_task(pair, pack["dimensions"], a, b), out / "calibration-work" / pair["id"] / judge_name, timeout)
            obj = parse_json(raw.get("final_output", ""))
            winner = obj.get("winner")
            if winner not in {"A","B"}:
                raise RuntimeError("invalid calibration judge output")
            winners[judge_name] = winner
            judge_total[judge_name] += 1
            if winner == expected: judge_correct[judge_name] += 1
        if len(set(winners.values())) > 1: disagreements += 1
        rows.append({"id": pair["id"], "judges": winners})
    n = len(pack["calibration_pairs"])
    rates = {j: judge_correct[j] / judge_total[j] for j in JUDGES}
    combined = sum(judge_correct.values()) / sum(judge_total.values())
    disagreement_rate = disagreements / n if n else 1.0
    policy = pack["release_policy"]
    passed = (
        all(v >= policy["calibration_per_judge_expected_winner_rate_min"] for v in rates.values())
        and combined >= policy["calibration_combined_expected_winner_rate_min"]
        and disagreement_rate <= policy["calibration_max_pair_disagreement_rate"]
    )
    report = {
        "gate_id": GATE_ID,
        "status": "CALIBRATION_PASS" if passed else "CALIBRATION_FAIL",
        "candidate_calls": 0,
        "judge_calls": sum(judge_total.values()),
        "per_judge_expected_winner_rate": rates,
        "combined_expected_winner_rate": combined,
        "pair_disagreement_rate": disagreement_rate,
        "policy": {k:v for k,v in policy.items() if k.startswith("calibration_")},
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "calibration-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if passed else 10


def validate_assessment(obj: dict, relevant: list[str]) -> list[str]:
    failures = []
    if not isinstance(obj.get("hard_failures"), list): failures.append("hard_failures not list")
    scores = obj.get("scores")
    if not isinstance(scores, dict): failures.append("scores not object"); scores = {}
    for dim in relevant:
        val = scores.get(dim)
        if not isinstance(val, int) or isinstance(val, bool) or val < 0 or val > 3:
            failures.append(f"invalid score for {dim}")
    if set(scores) - set(relevant): failures.append("unexpected score dimensions")
    if obj.get("release_recommendation") not in {"PASS","FAIL"}: failures.append("invalid release_recommendation")
    return failures


def run_score(pack: dict, out: Path, timeout: int) -> int:
    out.mkdir(parents=True, exist_ok=True)
    full_records = []
    sanitized_cases = []
    all_mechanical = True
    judge_score_values = {j: [] for j in JUDGES}
    hard_failures_total = 0
    all_case_judge_pass = True

    for case in pack["work_samples"]:
        started = time.time()
        raw = call_artifact(CANDIDATE_SHA, case["task"], out / "candidate-work" / case["id"], timeout)
        artifact_text = raw.get("final_output", "")
        artifact_obj = parse_json(artifact_text)
        mechanical_failures = mechanical_contract(artifact_obj)
        if mechanical_failures: all_mechanical = False
        judge_rows = {}
        for judge_name, judge_sha in JUDGES.items():
            jraw = call_artifact(judge_sha, assess_task(case, pack["dimensions"], artifact_text), out / "judge-work" / case["id"] / judge_name, timeout)
            assessment = parse_json(jraw.get("final_output", ""))
            shape_failures = validate_assessment(assessment, case["relevant_dimensions"])
            if shape_failures:
                raise RuntimeError(f"invalid judge assessment shape {judge_name}: {shape_failures}")
            scores = assessment["scores"]
            for dim in case["relevant_dimensions"]:
                judge_score_values[judge_name].append(scores[dim])
            hard_count = len(assessment["hard_failures"])
            hard_failures_total += hard_count
            judge_pass = assessment["release_recommendation"] == "PASS" and hard_count == 0 and all(scores[d] >= pack["release_policy"]["per_case_each_judge_min_dimension"] for d in case["relevant_dimensions"])
            if not judge_pass: all_case_judge_pass = False
            judge_rows[judge_name] = {
                "scores": scores,
                "hard_failure_count": hard_count,
                "release_recommendation": assessment["release_recommendation"],
                "shape_pass": True,
            }
        full_records.append({
            "id": case["id"], "candidate_output": artifact_text, "candidate_runtime_identity": raw.get("candidate_identity"),
            "candidate_transport": raw.get("transport"), "mechanical_failures": mechanical_failures, "judges": judge_rows,
            "duration_s": round(time.time() - started, 3),
        })
        sanitized_cases.append({"id": case["id"], "mechanical_pass": not mechanical_failures, "judges": judge_rows})

    policy = pack["release_policy"]
    mechanical_rate = sum(1 for r in sanitized_cases if r["mechanical_pass"]) / len(sanitized_cases)
    aggregate_means = {j: (sum(vals) / len(vals) if vals else 0.0) for j, vals in judge_score_values.items()}
    passed = (
        mechanical_rate >= policy["mechanical_contract_pass_rate"]
        and hard_failures_total <= policy["hard_failures_allowed"]
        and all_case_judge_pass
        and all(v >= policy["per_judge_aggregate_mean_min"] for v in aggregate_means.values())
    )
    verdict = "PASS" if passed else "REVISE"
    report = {
        "gate_id": GATE_ID,
        "candidate_sha": CANDIDATE_SHA,
        "verdict": verdict,
        "work_sample_count": len(sanitized_cases),
        "candidate_calls": len(sanitized_cases),
        "judge_calls": len(sanitized_cases) * len(JUDGES),
        "mechanical_contract_pass_rate": mechanical_rate,
        "hard_failure_count": hard_failures_total,
        "all_cases_each_judge_release_pass": all_case_judge_pass,
        "per_judge_aggregate_mean": aggregate_means,
        "policy": policy,
        "cases": sanitized_cases,
        "prior_reliability_evidence": {
            "r4_gate_id": "content-architecture-v0.4-codex-targeted-2026-09-01-r4",
            "r4_scored_trials": 40,
            "r4_repeats_all_pass": True,
            "r4_p0_count": 0,
            "reuse_scope": "unchanged targeted/stochastic behavioral reliability only; not substituted for these universal work samples",
        },
    }
    (out / "qualification-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode()
    raw_records = canon(full_records)
    records_identity = hashlib.sha256(raw_records).hexdigest()
    key = base64.urlsafe_b64encode(derive(master, b"run-records"))
    cipher = Fernet(key).encrypt(raw_records)
    (out / "sealed-run-records.bin").write_bytes(cipher)
    (out / "run-records-manifest.json").write_text(json.dumps({"identity_sha256": records_identity, "sealed_sha256": hashlib.sha256(cipher).hexdigest(), "record_count": len(full_records)}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k != "cases"}, sort_keys=True))
    return 0 if passed else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["calibrate","score"], required=True)
    ap.add_argument("--pack", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=300)
    args = ap.parse_args()
    try:
        pack = load_pack(Path(args.pack))
        if args.mode == "calibrate":
            return run_calibration(pack, Path(args.out), args.timeout)
        return run_score(pack, Path(args.out), args.timeout)
    except Exception as exc:
        out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
        err = {"gate_id": GATE_ID, "status": "NOT_EXECUTABLE", "error_type": type(exc).__name__, "error": str(exc)[:1200]}
        (out / "runtime-error.json").write_text(json.dumps(err, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(err, sort_keys=True))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
