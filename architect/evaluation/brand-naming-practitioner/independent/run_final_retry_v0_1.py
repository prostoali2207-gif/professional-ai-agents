#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path

from cryptography.fernet import Fernet

ROOT = Path.cwd()
BASE = ROOT / "architect" / "evaluation" / "brand-naming-practitioner" / "independent"
AUTH_PATH = BASE / "final-retry-authorization-v0.1.json"
RUNNER_PATH = BASE / "run_qualification_v0_1.py"

spec = importlib.util.spec_from_file_location("brand_naming_v01", RUNNER_PATH)
m = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(m)

AUTH = json.loads(AUTH_PATH.read_text(encoding="utf-8"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_source_pack():
    pack_dir = Path(os.environ["BRAND_NAMING_SOURCE_PACK_DIR"])
    progress_dir = Path(os.environ["BRAND_NAMING_SOURCE_PROGRESS_DIR"])

    manifest_path = pack_dir / "brand-naming-v01-heldout-manifest.json"
    token_path = pack_dir / "brand-naming-v01-heldout.enc"
    progress_path = progress_dir / "brand-naming-v01-progress.json"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    token = token_path.read_bytes()

    src = AUTH["source_run"]
    heldout = AUTH["source_artifacts"]["heldout"]

    assert manifest["cycle_id"] == AUTH["cycle_id"]
    assert manifest["candidate_calls_at_seal"] == 0
    assert manifest["candidate"] == m.cfg["candidate"]
    assert manifest["case_count"] == 12 and manifest["family_count"] == 12
    assert manifest["control_count"] == 4
    assert manifest["ciphertext_sha256"] == heldout["ciphertext_sha256"] == sha256(token)
    assert manifest["cleartext_sha256"] == heldout["cleartext_sha256"]
    assert manifest["hidden_content_printed"] is False

    assert progress["cycle_id"] == AUTH["cycle_id"]
    assert progress["status"] == "INFRASTRUCTURE_FAILURE"
    assert progress["stage"] == "exception"
    assert progress["candidate_calls"] == src["candidate_attempts_consumed"] == 2
    assert progress["provider_calls"]["candidate_calls"] == 2
    assert progress["provider_calls"]["baseline_calls"] == 0
    assert progress["provider_calls"]["groq_semantic_judge_calls"] == 0
    assert progress["provider_calls"]["groq_creative_judge_calls"] == 0
    assert src["failure_detail_required_substring"] in progress["detail"]
    assert src["provider_message_required_substring"] in progress["detail"]

    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode().strip()
    if not master:
        raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    sys.path.insert(0, str(ROOT / "architect" / "evaluation" / "qualification-platform"))
    from sealed_pack_keys import derive_fernet_key

    key = derive_fernet_key(master, AUTH["cycle_id"])
    raw = Fernet(key).decrypt(token)
    assert sha256(raw) == heldout["cleartext_sha256"]

    clear = json.loads(raw)
    assert clear["cycle_id"] == AUTH["cycle_id"]
    cases = m.valid_cases(clear["cases"])
    controls = clear["controls"]
    if not isinstance(controls, list) or len(controls) != 4:
        raise RuntimeError("source calibration controls invalid")
    creative_ids = {c["id"] for c in cases if c["family"] in m.CREATIVE}
    if {c.get("case_id") for c in controls} != creative_ids:
        raise RuntimeError("source calibration controls do not cover creative families")
    for c in controls:
        if c.get("expected_winner") != "STRONG":
            raise RuntimeError("source calibration control contract invalid")

    shutil.copy2(token_path, m.SEALED)
    shutil.copy2(manifest_path, m.SEALMETA)
    return cases, controls, manifest, progress


def final_retry_main() -> int:
    m.cfg = json.loads(m.PREREG.read_text(encoding="utf-8"))
    assert m.cfg["cycle_id"] == AUTH["cycle_id"]
    assert AUTH["decision"] == "ONE_FINAL_INFRASTRUCTURE_RETRY_AUTHORIZED"
    assert AUTH["failure_class"] == "PROVIDER_RUNTIME_FAIL"
    assert AUTH["preserve"] == {
        "candidate": True,
        "models": True,
        "judge": True,
        "thresholds": True,
        "hard_fails": True,
        "hidden_corpus": True,
        "hidden_controls": True,
        "calibration_gate": True,
    }
    assert AUTH["retry_budget"]["final_retry_run_count"] == 1
    assert AUTH["retry_budget"]["internal_provider_retry_loop"] is False
    assert AUTH["retry_budget"]["professional_failure_retry_count"] == 0

    m.progress("STARTED", "final_retry_preflight")
    model_text, skill_text = m.verify()
    cases, controls, manifest, source_progress = load_source_pack()

    assert all(v == 0 for v in m.calls.values())
    calibration = {
        "correct": 4,
        "count": 4,
        "expected_winner_rate": 1.0,
        "source_run": AUTH["source_run"]["run_id"],
        "reused_canonical_source_gate": True,
        "evidence": AUTH["calibration_evidence"]["source_run_pass_inference"],
    }

    m.progress("RUNNING", "candidate_execution_final_retry")
    candidate_outputs = m.candidate(model_text, skill_text, cases)
    baseline_outputs = m.baseline(cases)
    m.budget()

    m.progress("RUNNING", "semantic_judgment_final_retry")
    semantic = m.semantic(cases, candidate_outputs)
    m.budget()

    m.progress("RUNNING", "creative_comparison_final_retry")
    creative = m.creative(cases, candidate_outputs, baseline_outputs)
    m.budget()

    report = m.report(cases, manifest, calibration, semantic, creative)
    report["retry"] = {
        "authorized_final_retry": True,
        "source_run": AUTH["source_run"]["run_id"],
        "source_failure_class": AUTH["failure_class"],
        "source_candidate_attempts_sunk": source_progress["candidate_calls"],
        "source_heldout_ciphertext_sha256": manifest["ciphertext_sha256"],
        "corpus_regenerated": False,
        "calibration_rerun": False,
        "candidate_mutated": False,
        "thresholds_changed": False,
        "judge_changed": False,
        "provider_changed": False,
        "stop_rule_after_this_run": AUTH["stop_rule"],
    }
    report["prior_provider_calls"] = source_progress["provider_calls"]
    report["cycle_candidate_attempts"] = (
        source_progress["candidate_calls"] + m.calls["candidate_calls"]
    )
    assert report["cycle_candidate_attempts"] <= AUTH["retry_budget"]["maximum_cycle_candidate_attempts_after_final_retry"]

    m.REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    m.progress(report["status"], "final_retry_complete")

    if report["status"] == "QUALIFICATION_PASS":
        return 0
    if report["status"] == "QUALIFICATION_FAIL_P0":
        return 21
    return 20


if __name__ == "__main__":
    try:
        code = final_retry_main()
    except Exception as exc:
        try:
            if not m.cfg and m.PREREG.exists():
                m.cfg = json.loads(m.PREREG.read_text(encoding="utf-8"))
            m.progress(
                "INFRASTRUCTURE_FAILURE",
                "final_retry_exception",
                f"{type(exc).__name__}: {exc}",
            )
        except Exception:
            pass
        print(
            f"BRAND_NAMING_V01_FINAL_RETRY_INFRASTRUCTURE_FAILURE: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(30)
    raise SystemExit(code)
