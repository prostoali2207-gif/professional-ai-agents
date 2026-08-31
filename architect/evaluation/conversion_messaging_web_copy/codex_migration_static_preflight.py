#!/usr/bin/env python3
"""Zero-model deterministic gate for issue #222 migration preregistration."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import py_compile
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
ADDENDUM = HERE / "qualification-codex-migration-v0.1.json"
CANDIDATE = HERE / "codex_candidate_adapter_v0_1.py"
JUDGE = HERE / "codex_judge_adapter_v0_1.py"
OLD_PREREG = HERE / "EVALUATOR-PREREGISTRATION-v0.1.md"
FROZEN_COMMIT = "7019f6717b1b61806f4a221a297d049a4ad3b8cb"
FROZEN_DIGEST = "sha256:da7662f95dcf132d9a9875849b7bb5d5d831d1d54821f0b109b543a1f299e1d2"
FAMILIES = ["CM-EV", "CM-CL", "CM-MH", "CM-DV", "CM-OP", "CM-UX", "CM-PL", "CM-CR", "CM-EX", "CM-BD", "CM-PR", "CM-E2E"]
DIMS = ["evidence_integrity", "task_clarity", "professional_judgment", "functional_craft", "boundary_integrity"]
FLAGS = ["MATERIAL_FABRICATION", "INVENTED_CUSTOMER_EVIDENCE", "HARMFUL_UX_CONTRADICTION", "UNAUTHORIZED_STRATEGY_CHANGE", "GUARANTEED_CAUSAL_LIFT"]
FLOORS = {"evidence_integrity": 1.5, "task_clarity": 1.5, "professional_judgment": 1.5, "functional_craft": 1.25, "boundary_integrity": 1.5}
PAID_KEYS = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "GROQ_API_KEY", "XAI_API_KEY"]


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    check(spec is not None and spec.loader is not None, f"cannot import {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_frozen_candidate(add: dict) -> None:
    subprocess.run(["git", "cat-file", "-e", f"{FROZEN_COMMIT}^{{commit}}"], cwd=ROOT, check=True)
    frozen = add["frozen_candidate"]
    check(frozen["commit"] == FROZEN_COMMIT, "candidate commit changed")
    check(frozen["artifact_digest"] == FROZEN_DIGEST, "candidate digest changed")
    manifest = json.loads(subprocess.check_output(["git", "show", f"{FROZEN_COMMIT}:{frozen['manifest_path']}"], cwd=ROOT, text=True))
    canonical = ""
    for path in manifest["artifact"]["paths"]:
        blob = subprocess.check_output(["git", "rev-parse", f"{FROZEN_COMMIT}:{path}"], cwd=ROOT, text=True).strip()
        canonical += f"{path}:{blob}\n"
    import hashlib
    observed = "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()
    check(observed == FROZEN_DIGEST == manifest["artifact"]["content_digest"], "frozen artifact binding mismatch")


def verify_contract(add: dict) -> None:
    c = add["unchanged_professional_contract"]
    check(add["classification"] == "ROUTE_SUBSCRIPTION", "wrong migration classification")
    check(c["scope"] == "FULL", "FULL scope changed")
    check(c["families"] == FAMILIES, "families changed")
    check(c["scored_fixture_count"] == 24 and c["contrastive_pair_count"] == 4, "suite cardinality changed")
    check(c["dimensions"] == DIMS, "dimensions changed")
    check(c["hard_fails"] == FLAGS, "hard fails changed")
    threshold = c["release_threshold"]
    check(threshold["critical_hard_fails"] == 0, "hard-fail tolerance changed")
    check(threshold["minimum_fixture_passes"] == 22, "fixture pass threshold changed")
    check(threshold["all_contrastive_pairs_consistent"] is True, "pair threshold changed")
    check(threshold["family_floor"] == FLOORS, "family floors changed")
    old = OLD_PREREG.read_text(encoding="utf-8")
    for token in [FROZEN_COMMIT, FROZEN_DIGEST, "24 work samples", "12 families", "22/24", *DIMS, *FLAGS]:
        check(token in old, f"old preregistration no longer supports invariant {token}")


def verify_transport(add: dict) -> None:
    runtime = add["runtime"]
    check(runtime["provider"] == "codex-subscription-chatgpt-auth", "provider is not subscription Codex")
    check(runtime["paid_api_fallback"] == "FORBIDDEN", "paid API fallback enabled")
    check(runtime["forbidden_api_env"] == PAID_KEYS, "paid API deny-list drift")
    check(runtime["candidate_visible_fields"] == ["task", "context", "constraints"], "candidate visibility widened")
    for path in (CANDIDATE, JUDGE):
        source = path.read_text(encoding="utf-8")
        for forbidden in ("urllib.request", "api.openai.com", "generativelanguage.googleapis.com", "api.groq.com", "api.anthropic.com"):
            check(forbidden not in source, f"metered API transport found in {path.name}: {forbidden}")
        check("codex" in source and "--ephemeral" in source and "read-only" in source, f"isolated Codex CLI contract missing in {path.name}")
    candidate_source = CANDIDATE.read_text(encoding="utf-8")
    check("set(payload) - {\"task\", \"context\", \"constraints\"}" in candidate_source, "candidate evaluator-field rejection missing")
    check("EXPECTED_ANSWER" in candidate_source and "GRADER" in candidate_source and "SEALED_PACK" in candidate_source, "candidate environment sanitization incomplete")


def verify_judge_schema() -> None:
    judge = load_module(JUDGE, "messaging_codex_judge")
    cal = judge.schema("calibration")
    held = judge.schema("heldout")
    check(cal["required"] == ["results"] and "pair_results" not in cal["properties"], "calibration schema repeats Strategist pair_results defect")
    check(set(held["required"]) == {"results", "pair_results"}, "heldout pair_results is not required")
    result_required = held["properties"]["results"]["items"]["required"]
    check(result_required == ["id", "family", *DIMS, "critical_flags", "pass"], "judge result schema drift")
    flags = held["properties"]["results"]["items"]["properties"]["critical_flags"]["items"]["enum"]
    check(flags == FLAGS, "judge hard-fail enum drift")
    check(judge.failure_classification("HTTP 429 quota", "") == "NONRETRYABLE_TECHNICAL", "quota must not retry")
    check(judge.failure_classification("HTTP 503 temporarily unavailable", "") == "TRANSIENT_TRANSPORT", "transient transport classification broken")
    check(judge.failure_classification("invalid_json_schema", "") == "NONRETRYABLE_TECHNICAL", "schema failures must not retry")


def verify_budget_and_stop(add: dict) -> None:
    b = add["pre_run_budget_gate"]
    check(b["migration_issue_model_calls"] == 0 and b["scored_calls_authorized_here"] == 0, "issue #222 authorizes model calls")
    check(b.get("next_unscored_gate_max_calls") == 4, "next unscored gate budget must be exactly 4")
    r = add["retry_policy"]
    check(r["shared_unscored_transport_retry_budget"] == 1 and r["eligible_only"] == "TRANSIENT_TRANSPORT", "retry policy widened")
    check(r["scored_professional_retry_budget"] == 0, "professional retries enabled")
    check("zero-model" in add["migration_issue_stop_rule"].lower(), "zero-model stop rule missing")


def main() -> int:
    for path in (ADDENDUM, CANDIDATE, JUDGE, OLD_PREREG):
        check(path.is_file(), f"missing {path}")
    py_compile.compile(str(CANDIDATE), doraise=True)
    py_compile.compile(str(JUDGE), doraise=True)
    add = json.loads(ADDENDUM.read_text(encoding="utf-8"))
    verify_frozen_candidate(add)
    verify_contract(add)
    verify_transport(add)
    verify_judge_schema()
    verify_budget_and_stop(add)
    print(json.dumps({"status": "PASS", "checks": 5, "model_calls": 0, "scored_calls": 0, "paid_api_calls": 0, "migration_classification": "ROUTE_SUBSCRIPTION"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
