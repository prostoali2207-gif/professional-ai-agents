#!/usr/bin/env python3
from __future__ import annotations

import argparse, base64, hashlib, hmac, json, os, subprocess, sys, time
from pathlib import Path
from cryptography.fernet import Fernet

GATE_ID = "content-architecture-v0.4-uae-composition-2026-09-02-r3"
CORE_SHA = "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
SPECIALIZATION_SHA = "7f41c2d1ba40c3b4c59e3eba2fb264c04162c320"
JUDGE_SHA = "669cdfcd0195d0507637d377b48f2650b4a870dd"
ADAPTER = Path("architect/evaluation/harness/adapters/codex_frozen_artifact_adapter.py")
ASSEMBLY_VERSION = "content-architecture-uae-composition-v1"
DECISION_CLASSES = {"COMMERCIAL_CLAIM", "UNIT_FACT", "PROOF_SCOPE"}
RESOLUTIONS = {"ALLOW", "WITHHOLD", "DEFER"}
EVIDENCE_BASES = {"VERIFIED_UNIT_RECORD", "CURRENT_UNIT_PROOF", "MODEL_CONTEXT_ONLY", "MARKET_CONTEXT_ONLY", "UNVERIFIED", "SUPERSEDED", None}


def derive(master: bytes, label: bytes) -> bytes:
    return hmac.new(master, GATE_ID.encode() + b"|" + label, hashlib.sha256).digest()


def canon(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def parse_json(text: str) -> dict:
    text = (text or "").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1]).strip()
    try:
        obj = json.loads(text)
    except Exception:
        s, e = text.find("{"), text.rfind("}")
        if s < 0 or e <= s:
            raise ValueError("no JSON object")
        obj = json.loads(text[s:e + 1])
    if not isinstance(obj, dict):
        raise ValueError("JSON output is not an object")
    return obj


def git_blob(sha: str) -> str:
    kind = subprocess.run(["git", "cat-file", "-t", sha], capture_output=True, text=True)
    if kind.returncode != 0 or kind.stdout.strip() != "blob":
        raise RuntimeError(f"missing blob {sha}")
    p = subprocess.run(["git", "cat-file", "-p", sha], capture_output=True, text=False)
    if p.returncode != 0:
        raise RuntimeError(f"cannot read blob {sha}")
    return p.stdout.decode("utf-8")


def assemble_composed_blob() -> tuple[str, str]:
    text = (
        git_blob(CORE_SHA).rstrip()
        + "\n\n--- BEGIN APPLIED UAE AUTOMOTIVE SPECIALIZATION ---\n"
        + git_blob(SPECIALIZATION_SHA).rstrip()
        + "\n--- END APPLIED UAE AUTOMOTIVE SPECIALIZATION ---\n"
    )
    p = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=text.encode(), capture_output=True)
    if p.returncode != 0:
        raise RuntimeError("cannot materialize composed blob")
    sha = p.stdout.decode().strip()
    ident = hashlib.sha256((ASSEMBLY_VERSION + "|" + CORE_SHA + "|" + SPECIALIZATION_SHA + "|" + sha).encode()).hexdigest()
    return sha, ident


def load_pack(path: Path) -> dict:
    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode().strip()
    if not master:
        raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    raw = Fernet(base64.urlsafe_b64encode(derive(master, b"pack"))).decrypt(path.read_bytes())
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
    p = subprocess.run(
        [sys.executable, str(ADAPTER)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout + 30,
    )
    if p.returncode != 0:
        raise RuntimeError("artifact runtime failed: " + ((p.stdout or "") + "\n" + (p.stderr or ""))[-1400:])
    raw = parse_json(p.stdout)
    if raw.get("status") != "completed":
        raise RuntimeError("artifact runtime did not complete")
    if (raw.get("candidate_identity") or {}).get("sha") != sha:
        raise RuntimeError("artifact identity mismatch")
    return raw


def validate_candidate_shape(obj: dict) -> list[str]:
    failures: list[str] = []
    if obj.get("status") not in {"READY_WITH_BOUNDS", "BLOCKED", "NEEDS_UPSTREAM"}:
        failures.append("invalid status")
    decisions = obj.get("decision_results")
    if not isinstance(decisions, list):
        failures.append("decision_results missing")
        decisions = []
    for i, row in enumerate(decisions):
        if not isinstance(row, dict):
            failures.append(f"decision_results[{i}] not object")
            continue
        if not isinstance(row.get("decision_id"), str):
            failures.append(f"decision_results[{i}].decision_id")
        if row.get("decision_class") not in DECISION_CLASSES:
            failures.append(f"decision_results[{i}].decision_class")
        if row.get("resolution") not in RESOLUTIONS:
            failures.append(f"decision_results[{i}].resolution")
        if not isinstance(row.get("public_use"), bool):
            failures.append(f"decision_results[{i}].public_use")
        if row.get("evidence_basis") not in EVIDENCE_BASES:
            failures.append(f"decision_results[{i}].evidence_basis")
    locks = obj.get("lock_results")
    if not isinstance(locks, list):
        failures.append("lock_results missing")
        locks = []
    for i, row in enumerate(locks):
        if not isinstance(row, dict):
            failures.append(f"lock_results[{i}] not object")
            continue
        if not isinstance(row.get("lock_id"), str):
            failures.append(f"lock_results[{i}].lock_id")
        if not isinstance(row.get("preserved"), bool):
            failures.append(f"lock_results[{i}].preserved")
    arch = obj.get("architecture")
    if not isinstance(arch, dict):
        failures.append("architecture missing")
        arch = {}
    for key in ["attention_job", "block_sequence", "proof_requirements", "pacing_intent"]:
        if key not in arch:
            failures.append(f"architecture.{key} missing")
    handoff = obj.get("creator_handoff")
    if not isinstance(handoff, dict):
        failures.append("creator_handoff missing")
        handoff = {}
    for key in ["must_preserve", "may_choose", "blocked_portions", "must_escalate"]:
        if not isinstance(handoff.get(key), list):
            failures.append(f"creator_handoff.{key}")
    if not isinstance(obj.get("boundary_notes"), list):
        failures.append("boundary_notes missing")
    return failures


def mechanical_case(case: dict, obj: dict) -> dict:
    failures = validate_candidate_shape(obj)
    hard: list[str] = []
    decisions = {
        row.get("decision_id"): row
        for row in (obj.get("decision_results") or [])
        if isinstance(row, dict) and isinstance(row.get("decision_id"), str)
    }
    expected_ids = set(case["expected_decisions"])
    unexpected = set(decisions) - expected_ids
    if unexpected:
        failures.append("unexpected proposition decisions: " + ",".join(sorted(unexpected)))
    for decision_id, expected in case["expected_decisions"].items():
        row = decisions.get(decision_id)
        if not row:
            failures.append(f"missing decision {decision_id}")
            continue
        if row.get("public_use") is not expected["public_use"]:
            failures.append(f"{decision_id} public_use")
            if expected["public_use"] is False and row.get("public_use") is True:
                hard.append(f"unsafe public use {decision_id}")
        if row.get("resolution") not in expected["allowed_resolutions"]:
            failures.append(f"{decision_id} resolution")
        if row.get("evidence_basis") not in expected["allowed_evidence_bases"]:
            failures.append(f"{decision_id} evidence_basis")
    locks = {
        row.get("lock_id"): row
        for row in (obj.get("lock_results") or [])
        if isinstance(row, dict) and isinstance(row.get("lock_id"), str)
    }
    for lock_id in case["expected_locks"]:
        row = locks.get(lock_id)
        if not row:
            failures.append(f"missing lock {lock_id}")
        elif row.get("preserved") is not True:
            failures.append(f"lock not preserved {lock_id}")
            hard.append(f"lock breach {lock_id}")
    return {"pass": not failures, "failures": failures, "hard_failures": hard}


def calibration_task(pair: dict, dimensions: dict, a: str, b: str) -> str:
    relevant = {k: dimensions[k] for k in pair["dimensions"]}
    return (
        "MODE: CALIBRATE\n\nBrief:\n" + pair["brief"]
        + "\n\nRelevant dimensions:\n" + json.dumps(relevant, ensure_ascii=False, indent=2)
        + "\n\nArtifact A:\n" + a + "\n\nArtifact B:\n" + b
        + "\n\nChoose the professionally stronger artifact. Return only calibration JSON."
    )


def assess_task(case: dict, dimensions: dict, artifact: str) -> str:
    relevant = {k: dimensions[k] for k in case["relevant_dimensions"]}
    return (
        "MODE: ASSESS\n\nSynthetic evaluation brief:\n" + case["task"]
        + "\n\nRelevant dimensions:\n" + json.dumps(relevant, ensure_ascii=False, indent=2)
        + "\n\nSubmitted architecture:\n" + artifact
        + "\n\nAssess only this architecture against the brief and rubric. Return only assessment JSON."
    )


def validate_assessment(obj: dict, dimensions: list[str]) -> list[str]:
    failures: list[str] = []
    if not isinstance(obj.get("hard_failures"), list):
        failures.append("hard_failures not list")
    scores = obj.get("scores")
    if not isinstance(scores, dict):
        failures.append("scores not object")
        scores = {}
    for dimension in dimensions:
        value = scores.get(dimension)
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 3:
            failures.append(f"bad score {dimension}")
    if set(scores) - set(dimensions):
        failures.append("unexpected score dimension")
    if obj.get("release_recommendation") not in {"PASS", "FAIL"}:
        failures.append("bad release_recommendation")
    return failures


def run_calibrate(pack: dict, out: Path, timeout: int) -> int:
    correct = 0
    for pair in pack["calibration_pairs"]:
        swap = int(hashlib.sha256(f"{GATE_ID}|{pair['id']}".encode()).hexdigest()[:2], 16) % 2 == 1
        a, b = (pair["challenger"], pair["strong"]) if swap else (pair["strong"], pair["challenger"])
        expected = "B" if swap else "A"
        raw = call_artifact(JUDGE_SHA, calibration_task(pair, pack["dimensions"], a, b), out / "judge-calibration" / pair["id"], timeout)
        winner = parse_json(raw.get("final_output", "")).get("winner")
        if winner not in {"A", "B"}:
            raise RuntimeError("invalid calibration output")
        correct += int(winner == expected)
    rate = correct / len(pack["calibration_pairs"])
    passed = rate >= pack["release_policy"]["calibration_expected_winner_rate_min"]
    report = {
        "gate_id": GATE_ID,
        "status": "CALIBRATION_PASS" if passed else "CALIBRATION_FAIL",
        "candidate_calls": 0,
        "judge_calls": len(pack["calibration_pairs"]),
        "expected_winner_rate": rate,
        "policy": pack["release_policy"]["calibration_expected_winner_rate_min"],
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "calibration-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if passed else 10


def run_score(pack: dict, out: Path, timeout: int) -> int:
    composed_sha, composed_identity = assemble_composed_blob()
    out.mkdir(parents=True, exist_ok=True)
    sanitized, records, scores_all = [], [], []
    mechanical_hard = judge_hard = 0
    all_judge_pass = True
    for case in pack["cases"]:
        started = time.time()
        raw = call_artifact(composed_sha, case["task"], out / "candidate-work" / case["id"], timeout)
        artifact = raw.get("final_output", "")
        candidate_obj = parse_json(artifact)
        mechanical = mechanical_case(case, candidate_obj)
        mechanical_hard += len(mechanical["hard_failures"])
        judge_raw = call_artifact(JUDGE_SHA, assess_task(case, pack["dimensions"], artifact), out / "judge-work" / case["id"], timeout)
        assessment = parse_json(judge_raw.get("final_output", ""))
        shape = validate_assessment(assessment, case["relevant_dimensions"])
        if shape:
            raise RuntimeError(f"invalid judge assessment: {shape}")
        scores = assessment["scores"]
        scores_all.extend(scores[d] for d in case["relevant_dimensions"])
        hard_count = len(assessment["hard_failures"])
        judge_hard += hard_count
        judge_pass = (
            assessment["release_recommendation"] == "PASS"
            and hard_count == 0
            and all(scores[d] >= pack["release_policy"]["per_case_judge_min_dimension"] for d in case["relevant_dimensions"])
        )
        all_judge_pass = all_judge_pass and judge_pass
        sanitized.append({
            "id": case["id"],
            "mechanical_pass": mechanical["pass"],
            "mechanical_failure_count": len(mechanical["failures"]),
            "mechanical_hard_failure_count": len(mechanical["hard_failures"]),
            "judge_scores": scores,
            "judge_hard_failure_count": hard_count,
            "judge_release_recommendation": assessment["release_recommendation"],
        })
        records.append({
            "id": case["id"],
            "candidate_output": artifact,
            "candidate_identity": raw.get("candidate_identity"),
            "candidate_transport": raw.get("transport"),
            "mechanical": mechanical,
            "judge": assessment,
            "duration_s": round(time.time() - started, 3),
        })
    policy = pack["release_policy"]
    mechanical_rate = sum(case["mechanical_pass"] for case in sanitized) / len(sanitized)
    mean = sum(scores_all) / len(scores_all) if scores_all else 0.0
    passed = (
        mechanical_rate >= policy["mechanical_case_pass_rate"]
        and mechanical_hard <= policy["mechanical_hard_failures_allowed"]
        and judge_hard <= policy["judge_hard_failures_allowed"]
        and all_judge_pass
        and mean >= policy["judge_aggregate_mean_min"]
    )
    verdict = "PASS" if passed else "REVISE"
    report = {
        "gate_id": GATE_ID,
        "verdict": verdict,
        "core_sha": CORE_SHA,
        "specialization_sha": SPECIALIZATION_SHA,
        "assembly_version": ASSEMBLY_VERSION,
        "composed_blob_sha": composed_sha,
        "composed_identity_sha256": composed_identity,
        "case_count": len(sanitized),
        "candidate_calls": len(sanitized),
        "judge_calls": len(sanitized),
        "mechanical_case_pass_rate": mechanical_rate,
        "mechanical_hard_failure_count": mechanical_hard,
        "judge_hard_failure_count": judge_hard,
        "all_cases_judge_release_pass": all_judge_pass,
        "judge_aggregate_mean": mean,
        "policy": policy,
        "cases": sanitized,
        "prior_evidence": {
            "universal_release_run_id": 33501449175,
            "universal_release_verdict": "PASS",
            "r1_composition_status": "CONSTRUCT_INVALID_DIAGNOSTIC_ONLY",
            "r2_composition_status": "CONSTRUCT_INVALID_DIAGNOSTIC_ONLY",
        },
        "stop_loss_scope": "FINAL_BOUNDED_PROFESSION_SPECIFIC_EVALUATOR_REPAIR",
    }
    (out / "qualification-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode().strip()
    record_raw = canon(records)
    key = base64.urlsafe_b64encode(derive(master, b"run-records"))
    sealed = Fernet(key).encrypt(record_raw)
    (out / "sealed-run-records.bin").write_bytes(sealed)
    (out / "run-records-manifest.json").write_text(
        json.dumps({
            "identity_sha256": hashlib.sha256(record_raw).hexdigest(),
            "sealed_sha256": hashlib.sha256(sealed).hexdigest(),
            "record_count": len(records),
        }, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "gate_id": GATE_ID,
        "verdict": verdict,
        "case_count": len(sanitized),
        "mechanical_case_pass_rate": mechanical_rate,
        "mechanical_hard_failure_count": mechanical_hard,
        "judge_hard_failure_count": judge_hard,
        "judge_aggregate_mean": mean,
    }, sort_keys=True))
    return 0 if passed else 20


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["calibrate", "score"], required=True)
    ap.add_argument("--pack", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=300)
    args = ap.parse_args()
    try:
        pack = load_pack(Path(args.pack))
        return run_calibrate(pack, Path(args.out), args.timeout) if args.mode == "calibrate" else run_score(pack, Path(args.out), args.timeout)
    except Exception as exc:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        failure = {
            "gate_id": GATE_ID,
            "mode": args.mode,
            "status": "RUNTIME_FAILURE",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        (out / "runtime-failure.json").write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, sort_keys=True), file=sys.stderr)
        return 30


if __name__ == "__main__":
    raise SystemExit(main())
