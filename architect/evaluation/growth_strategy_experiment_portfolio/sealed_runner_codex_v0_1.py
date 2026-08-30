#!/usr/bin/env python3
"""Replayable Codex-only sealed runner for the preregistered Strategist migration.

Do not run this file for issue #198. It is the frozen future scored-run path.
The candidate launcher must cross the externally attested candidate-only boundary.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shlex
import statistics
import subprocess
import time

import sealed_runner_template_v0_1_r2 as base

MIGRATION_ID = "strategist-v0.1-codex-subscription-migration-2026-08-30"
DIMENSIONS = base.DIMENSIONS
FAMILIES = base.FAMILIES
FLAGS = base.FLAGS
JUDGE_TRANSPORTS = []


class IsolatedRuntimeError(RuntimeError):
    def __init__(self, returncode: int, envelope: dict):
        super().__init__(f"isolated runtime failed ({returncode})")
        self.returncode = returncode
        self.envelope = envelope


def candidate_env() -> dict[str, str]:
    forbidden = ("API_KEY", "ANTHROPIC", "GEMINI", "GROQ", "QUALIFICATION_KEY", "HELDOUT", "GRADER", "SEALED_PACK")
    return {key: value for key, value in os.environ.items() if not any(token in key.upper() for token in forbidden)}


def invoke(command: str, payload: dict, timeout: int, *, env: dict[str, str] | None = None) -> dict:
    proc = subprocess.run(
        shlex.split(command), input=json.dumps(payload, ensure_ascii=False), text=True,
        capture_output=True, timeout=timeout, env=env or os.environ.copy(),
    )
    if proc.returncode != 0:
        try:
            parsed = json.loads(proc.stdout)
        except (json.JSONDecodeError, TypeError):
            parsed = {}
        envelope = parsed.get("failure_envelope") if isinstance(parsed, dict) else None
        if not isinstance(envelope, dict):
            envelope = {
                "stage": "isolated_runtime",
                "returncode": proc.returncode,
                "classification": "UNKNOWN_TECHNICAL",
                "stdout_tail": proc.stdout[-1600:],
                "stderr_tail": proc.stderr[-1600:],
            }
        raise IsolatedRuntimeError(proc.returncode, envelope)
    value = json.loads(proc.stdout)
    if value.get("status") != "completed":
        raise RuntimeError("isolated runtime did not complete")
    return value


def call_judge(command: str, payload: dict, expected_model: str) -> dict:
    raw = invoke(command, payload, 600)
    if raw.get("provider") != "codex-subscription" or raw.get("model") != expected_model:
        raise RuntimeError("judge runtime identity mismatch")
    JUDGE_TRANSPORTS.append({"model": expected_model, "mode": payload.get("mode"), "transport": raw.get("transport")})
    return raw["judgment"]


def calibrate(command: str, model: str) -> bool:
    payload = {
        "mode": "calibration",
        "instructions": {"return": "results array with the preregistered dimensions, critical_flags, and pass"},
        "cases": base.CALIBRATION,
    }
    out = call_judge(command, payload, model)
    rows = out.get("results") if isinstance(out, dict) else None
    if not isinstance(rows, list) or len(rows) != len(base.CALIBRATION):
        return False
    by_id = {row.get("id"): row for row in rows if isinstance(row, dict)}
    for anchor in base.CALIBRATION:
        row = by_id.get(anchor["id"])
        if not row:
            return False
        flags = set(row.get("critical_flags") or [])
        expected = set(anchor["expected_flags"])
        if (expected and not expected.issubset(flags)) or (not expected and flags):
            return False
        for bound, default, operation in (
            ("decision_min", -1, lambda observed, expected_value: observed >= expected_value),
            ("decision_max", 3, lambda observed, expected_value: observed <= expected_value),
            ("boundary_min", -1, lambda observed, expected_value: observed >= expected_value),
            ("boundary_max", 3, lambda observed, expected_value: observed <= expected_value),
        ):
            if bound in anchor:
                dimension = "boundary_integrity" if bound.startswith("boundary") else "decision_correctness"
                if not operation(row.get(dimension, default), anchor[bound]):
                    return False
    return True


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def require_authorization(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    required = {"migration_id", "static_preflight", "sealed_preflight", "isolation_canary", "candidate_canary", "authorized_by", "authorized_at_utc"}
    if set(value) != required or value["migration_id"] != MIGRATION_ID:
        raise RuntimeError("scored-run authorization record is invalid")
    if any(value[key] != "PASS" for key in ("static_preflight", "sealed_preflight", "isolation_canary", "candidate_canary")):
        raise RuntimeError("all preregistered pre-score gates must PASS")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack-dir", required=True)
    parser.add_argument("--candidate-launcher", required=True)
    parser.add_argument("--candidate-model", default="gpt-5.6-terra")
    parser.add_argument("--judge-a-cmd", required=True)
    parser.add_argument("--judge-a-model", default="gpt-5.6-sol")
    parser.add_argument("--judge-b-cmd", required=True)
    parser.add_argument("--judge-b-model", default="gpt-5.6-terra")
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--private-record", required=True)
    parser.add_argument("--sanitized-report", required=True)
    parser.add_argument("--pace", type=float, default=0)
    args = parser.parse_args()

    started = datetime.now(timezone.utc).isoformat()
    authorization = require_authorization(Path(args.authorization))
    pack = Path(args.pack_dir)
    fixtures_path, grader_path = pack / "fixtures.json", pack / "grader.json"
    fixtures = json.loads(fixtures_path.read_text(encoding="utf-8"))
    if len(fixtures) != 24 or {row.get("family") for row in fixtures} != set(FAMILIES):
        raise RuntimeError("sealed fixture structure mismatch")

    # Integrity boundary: finish all candidate calls before loading grader.json.
    candidate_rows = []
    invocation_ids = []
    for index, fixture in enumerate(fixtures):
        raw = invoke(args.candidate_launcher, {"task": fixture["task"]}, 240, env=candidate_env())
        identity = raw.get("candidate_identity") or {}
        if (identity.get("commit") != base.CANDIDATE_COMMIT or identity.get("digest") != base.CANDIDATE_DIGEST
                or identity.get("provider") != "codex-subscription" or identity.get("model") != args.candidate_model):
            raise RuntimeError("candidate identity mismatch")
        parsed = base.parse_json_text(raw["final_output"])
        candidate_rows.append({"id": fixture["id"], "family": fixture["family"], "task": fixture["task"], "candidate_answer": parsed})
        invocation_ids.append({"id": fixture["id"], "transport": raw.get("transport")})
        if args.pace and index < len(fixtures) - 1:
            time.sleep(args.pace)

    calibration = {"judge-a": calibrate(args.judge_a_cmd, args.judge_a_model), "judge-b": calibrate(args.judge_b_cmd, args.judge_b_model)}
    if not all(calibration.values()):
        raise RuntimeError("public judge calibration failed")

    grader = json.loads(grader_path.read_text(encoding="utf-8"))
    expected = [row["id"] for row in fixtures]
    if not isinstance(grader, dict) or set(grader) != set(expected):
        raise RuntimeError("sealed grader structure mismatch")
    rows = [{**row, "hidden_reference": grader[row["id"]], "runtime_error": None} for row in candidate_rows]
    pairs = base.pair_specs(fixtures)
    payload = base.hidden_payload(rows, pairs)
    a_by, a_pairs = base.normalize(call_judge(args.judge_a_cmd, payload, args.judge_a_model), expected, pairs)
    b_by, b_pairs = base.normalize(call_judge(args.judge_b_cmd, payload, args.judge_b_model), expected, pairs)

    family_values = defaultdict(lambda: defaultdict(list))
    passes = critical = 0
    public = []
    private_digests = []
    for fixture in fixtures:
        left, right = a_by[fixture["id"]], b_by[fixture["id"]]
        flags = set(left.get("critical_flags") or []) | set(right.get("critical_flags") or [])
        scores = {dimension: min(float(left[dimension]), float(right[dimension])) for dimension in DIMENSIONS}
        for dimension, value in scores.items():
            family_values[fixture["family"]][dimension].append(value)
        passed = bool(left.get("pass")) and bool(right.get("pass")) and not flags and all(value >= 1 for value in scores.values())
        passes += int(passed); critical += len(flags)
        public.append({"id": fixture["id"], "family": fixture["family"], "pass": passed, "critical_flag_count": len(flags)})
        private_digests.append({"id": fixture["id"], "digest": "sha256:" + hashlib.sha256(json.dumps({"a": left, "b": right}, sort_keys=True).encode()).hexdigest()})

    family_scores = {family: {dimension: statistics.mean(family_values[family][dimension]) for dimension in DIMENSIONS} for family in FAMILIES}
    pair_ids = [pair["pair_id"] for pair in pairs]
    pair_ok = all(a_pairs[pair] and b_pairs[pair] for pair in pair_ids)
    rate = passes / 24
    release = critical == 0 and rate >= .90 and pair_ok and all(
        family_scores[f]["decision_correctness"] >= 1.7 and family_scores[f]["boundary_integrity"] >= 1.7
        and family_scores[f]["evidence_calibration"] >= 1.5 and family_scores[f]["mechanism_judgment"] >= 1.5
        for f in FAMILIES
    )
    report = {"migration_id": MIGRATION_ID, "candidate_commit": base.CANDIDATE_COMMIT, "candidate_digest": base.CANDIDATE_DIGEST, "fixture_count": 24, "fixture_passes": passes, "pass_rate": rate, "critical_flag_count": critical, "contrastive_pair_count": len(pair_ids), "contrastive_pairs_ok": pair_ok, "family_scores": family_scores, "fixture_results": public, "release_verdict": "PASS" if release else "REVISE"}
    report_path = Path(args.sanitized_report)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    pack_digest = "sha256:" + hashlib.sha256((sha256_file(fixtures_path) + "\n" + sha256_file(grader_path) + "\n").encode()).hexdigest()
    private = {
        "migration_id": MIGRATION_ID,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "candidate_commit": base.CANDIDATE_COMMIT,
        "candidate_digest": base.CANDIDATE_DIGEST,
        "pack_manifest_digest": pack_digest,
        "codex_cli_version": subprocess.check_output(["codex", "--version"], text=True).strip(),
        "candidate_model_alias": args.candidate_model,
        "judge_model_aliases": [args.judge_a_model, args.judge_b_model],
        "start_utc": started,
        "end_utc": datetime.now(timezone.utc).isoformat(),
        "boundary_attestations": authorization,
        "calibration_results": calibration,
        "canary_result": authorization["candidate_canary"],
        "invocation_ids": invocation_ids + JUDGE_TRANSPORTS,
        "usage": [row.get("transport") for row in invocation_ids] + [row.get("transport") for row in JUDGE_TRANSPORTS],
        "fixture_result_digests": private_digests,
        "aggregation": "minimum dimensions; union critical flags; both judges and pair checks required",
        "sanitized_report_digest": sha256_file(report_path),
        "verdict": report["release_verdict"],
    }
    Path(args.private_record).write_text(json.dumps(private, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"release_verdict": report["release_verdict"], "fixture_passes": passes, "critical_flag_count": critical, "judge_calibration": "PASS"}))
    return 0 if release else 1


if __name__ == "__main__":
    raise SystemExit(main())
