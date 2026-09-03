#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import socket
import subprocess
import urllib.request
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable
from unittest import mock

ROOT = Path(__file__).resolve().parents[4]
QRE = ROOT / "architect/evaluation/qualification-reliability-engineer"
FREEZE_PATH = QRE / "candidate-freeze-v0.1.json"
GUARD_PATH = QRE / "candidate/guard/validate_readiness_report.py"
SCHEMA_PATH = QRE / "candidate/guard/readiness-report.schema.json"

EVALUATOR_CYCLE = "qre-v01-independent-stage-a-r1"
EXPECTED_STAGE = "A_DETERMINISTIC_CANDIDATE_HARNESS_PROOF"


class HarnessError(RuntimeError):
    pass


def _git(*args: str) -> str:
    p = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False
    )
    if p.returncode != 0:
        raise HarnessError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p.stdout.strip()


def load_freeze() -> dict[str, Any]:
    value = json.loads(FREEZE_PATH.read_text())
    if not isinstance(value, dict):
        raise HarnessError("freeze record must be a JSON object")
    return value


def verify_frozen_identity() -> dict[str, str]:
    freeze = load_freeze()
    candidate_commit = freeze["candidate_merge_commit"]
    expected: dict[str, str] = {}
    expected.update(freeze["components"])
    expected.update(freeze["supporting_regression"])
    qp = freeze["qualification_plan"]
    expected[qp["path"]] = qp["blob"]

    observed: dict[str, str] = {}
    for path, blob in expected.items():
        source_blob = _git("rev-parse", f"{candidate_commit}:{path}")
        if source_blob != blob:
            raise HarnessError(
                f"freeze source mismatch for {path}: expected {blob}, got {source_blob}"
            )
        working_blob = _git("hash-object", path)
        if working_blob != blob:
            raise HarnessError(
                f"checked-out frozen component drift for {path}: expected {blob}, got {working_blob}"
            )
        observed[path] = working_blob

    if freeze.get("status") != "FROZEN_NOT_QUALIFIED":
        raise HarnessError("freeze status is not FROZEN_NOT_QUALIFIED")
    if freeze.get("release_state") != "NOT_QUALIFIED":
        raise HarnessError("release state unexpectedly changed")
    return observed


def load_guard_module():
    spec = importlib.util.spec_from_file_location("qre_frozen_guard", GUARD_PATH)
    if spec is None or spec.loader is None:
        raise HarnessError("cannot load frozen readiness guard")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def base_report() -> dict[str, Any]:
    freeze = load_freeze()
    return {
        "version": "0.1",
        "execution_chain": {
            "cycle": EVALUATOR_CYCLE,
            "stage": EXPECTED_STAGE,
            "evaluator_transport_path": "github-actions-python-zero-provider",
            "technical_repair_consumed": False,
            "eligible_retry_remaining": True,
        },
        "identities": {
            "candidate": freeze["candidate_merge_commit"],
            "evaluator": EVALUATOR_CYCLE,
            "runtime": "python-3.11-zero-provider-stage-a",
        },
        "mechanical_evidence": {
            "static_preflight": "PASS",
            "runtime_contract": "PASS",
            "fault_injection": "PASS",
            "artifact_identity": "PASS",
        },
        "canary": {
            "required": False,
            "representativeness_assessed": False,
            "evidence_status": "NOT_APPLICABLE",
            "rationale": "Stage A is deterministic and authorizes no live canary.",
        },
        "budget": {
            "max_candidate_calls": 0,
            "max_judge_calls": 0,
            "max_retries": 0,
            "max_wall_clock_seconds": 300,
            "stop_condition": "Stop on any provider/model call or failed Stage-A invariant.",
        },
        "privacy": {
            "heldout_material": False,
            "provider_storage_required": False,
            "provider_storage_authorized": False,
        },
        "risks": [
            {
                "id": "P1-observability-backlog",
                "severity": "P1",
                "status": "ACCEPTED_BACKLOG",
                "deterministically_detectable": True,
                "evidence": "Non-release-critical Stage-B observability refinement may remain backlog.",
            }
        ],
        "decision": {"verdict": "GO", "reason": "Stage A mechanical conditions pass."},
    }


def validate_envelope(
    envelope: dict[str, Any], *, expected_run_id: str, expected_candidate_commit: str
) -> None:
    required = {"run_id", "candidate_commit", "evaluator_cycle", "artifact_kind"}
    if set(envelope) != required:
        raise HarnessError("evidence envelope keys mismatch")
    if envelope["run_id"] != expected_run_id:
        raise HarnessError("stale/cross-run artifact run_id mismatch")
    if envelope["candidate_commit"] != expected_candidate_commit:
        raise HarnessError("artifact candidate identity mismatch")
    if envelope["evaluator_cycle"] != EVALUATOR_CYCLE:
        raise HarnessError("artifact evaluator-cycle mismatch")
    if not isinstance(envelope["artifact_kind"], str) or not envelope["artifact_kind"].strip():
        raise HarnessError("artifact kind missing")


def require_guard_rejects(
    validator: Callable[[dict[str, Any], Path], Any],
    report: dict[str, Any],
    expected_message: str,
) -> None:
    try:
        validator(report, SCHEMA_PATH)
    except Exception as exc:
        if expected_message not in str(exc):
            raise HarnessError(
                f"guard rejected for wrong reason; expected {expected_message!r}, got {exc!r}"
            ) from exc
        return
    raise HarnessError(f"fail-open guard accepted unsafe report: expected {expected_message}")


@contextmanager
def python_network_disabled():
    def blocked(*args, **kwargs):
        raise AssertionError("outbound Python network access is forbidden in QRE Stage A")

    with mock.patch.object(socket.socket, "connect", blocked), mock.patch.object(
        socket, "create_connection", blocked
    ), mock.patch.object(urllib.request, "urlopen", blocked):
        yield


def verify_guard_fault_paths() -> dict[str, str]:
    guard = load_guard_module()
    validator = guard.validate
    outcomes: dict[str, str] = {}

    with python_network_disabled():
        valid = base_report()
        notes = validator(valid, SCHEMA_PATH)
        if notes:
            raise HarnessError(f"valid GO negative control produced notes: {notes}")
        outcomes["valid_go_negative_control"] = "PASS"

        p0 = deepcopy(valid)
        p0["risks"].append(
            {
                "id": "P0-deterministic-blocker",
                "severity": "P0",
                "status": "OPEN",
                "deterministically_detectable": True,
                "evidence": "Synthetic open P0",
            }
        )
        require_guard_rejects(validator, p0, "open P0 risks")
        outcomes["open_p0_blocks_go"] = "PASS"

        stale = deepcopy(valid)
        stale["mechanical_evidence"]["artifact_identity"] = "FAIL"
        require_guard_rejects(validator, stale, "mechanical evidence failed")
        outcomes["failed_artifact_identity_blocks_go"] = "PASS"

        storage = deepcopy(valid)
        storage["privacy"].update(
            {
                "heldout_material": True,
                "provider_storage_required": True,
                "provider_storage_authorized": False,
            }
        )
        require_guard_rejects(validator, storage, "provider storage required but not authorized")
        outcomes["unauthorized_storage_blocks_go"] = "PASS"

        exhausted = deepcopy(valid)
        exhausted["execution_chain"]["technical_repair_consumed"] = True
        exhausted["execution_chain"]["eligible_retry_remaining"] = False
        require_guard_rejects(validator, exhausted, "repair/retry budget exhausted")
        outcomes["exhausted_stop_loss_blocks_go"] = "PASS"

    return outcomes


def verify_stale_evidence_fail_closed() -> dict[str, str]:
    freeze = load_freeze()
    candidate = freeze["candidate_merge_commit"]
    good = {
        "run_id": "stage-a-run-current",
        "candidate_commit": candidate,
        "evaluator_cycle": EVALUATOR_CYCLE,
        "artifact_kind": "stage-a-result",
    }
    validate_envelope(good, expected_run_id="stage-a-run-current", expected_candidate_commit=candidate)

    results = {"current_envelope": "PASS"}
    mutations = {
        "stale_run_id": {**good, "run_id": "stage-a-run-old"},
        "wrong_candidate": {**good, "candidate_commit": "0" * 40},
        "wrong_cycle": {**good, "evaluator_cycle": "candidate-authoring-cycle"},
    }
    for name, envelope in mutations.items():
        try:
            validate_envelope(
                envelope,
                expected_run_id="stage-a-run-current",
                expected_candidate_commit=candidate,
            )
        except HarnessError:
            results[name] = "PASS"
        else:
            raise HarnessError(f"stale evidence mutation failed open: {name}")
    return results


def verify_fail_open_discrimination() -> dict[str, str]:
    unsafe = base_report()
    unsafe["risks"].append(
        {
            "id": "P0-fail-open-mutation",
            "severity": "P0",
            "status": "OPEN",
            "deterministically_detectable": True,
            "evidence": "Mutation control",
        }
    )

    def permissive_validator(report: dict[str, Any], schema_path: Path):
        return []

    try:
        require_guard_rejects(permissive_validator, unsafe, "open P0 risks")
    except HarnessError as exc:
        if "fail-open guard accepted unsafe report" not in str(exc):
            raise
        return {"permissive_guard_mutation_detected": "PASS"}
    raise HarnessError("mutation discrimination self-test did not detect permissive guard")


def run_stage_a() -> dict[str, Any]:
    frozen = verify_frozen_identity()
    guard_paths = verify_guard_fault_paths()
    stale_paths = verify_stale_evidence_fail_closed()
    mutation = verify_fail_open_discrimination()
    return {
        "status": "PASS",
        "stage": EXPECTED_STAGE,
        "evaluator_cycle": EVALUATOR_CYCLE,
        "provider_calls": 0,
        "model_calls": 0,
        "judge_calls": 0,
        "frozen_components_verified": len(frozen),
        "guard_fault_paths": guard_paths,
        "stale_identity_paths": stale_paths,
        "mutation_discrimination": mutation,
        "next_stage_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = run_stage_a()
    except Exception as exc:
        result = {
            "status": "FAIL",
            "stage": EXPECTED_STAGE,
            "evaluator_cycle": EVALUATOR_CYCLE,
            "provider_calls": 0,
            "model_calls": 0,
            "judge_calls": 0,
            "error": str(exc),
            "next_stage_authorized": False,
        }
        code = 2
    else:
        code = 0
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if args.output:
        Path(args.output).write_text(text + "\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
