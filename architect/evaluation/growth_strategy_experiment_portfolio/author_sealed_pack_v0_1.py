#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import urllib.error
import urllib.request
import zipfile

from cryptography.fernet import Fernet

ROOT = Path.cwd()
CYCLE = "growth-strategy-experiment-portfolio-v0.1-heldout-2026-08-22"
CANDIDATE_COMMIT = "4b84ef258b5d3d2b3fbc9549e77176b3359a501e"
CANDIDATE_DIGEST = "sha256:59dd74cb772f1259a7ed5f6b9da4aa40db7f48be21c380b605bdc044f4dd7b92"
MODEL = "gemini-3.5-flash-lite"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
FAMILIES = ["GS-BV","GS-BD","GS-EV","GS-MH","GS-AS","GS-PP","GS-ED","GS-MB","GS-CH","GS-CF","GS-LI","GS-BA"]
PAIR_PLAN = {
    "P-BV-PROXY": "GS-BV",
    "P-EV-COMPARABILITY": "GS-EV",
    "P-MB-MATURITY": "GS-MB",
    "P-PP-CAPACITY": "GS-PP",
    "P-BA-AUTHORITY": "GS-BA",
    "P-MH-CONFIDENCE": "GS-MH",
    "P-LI-WORDING": "GS-LI",
}
PARTS_DIR = ROOT / "architect/evaluation/growth_strategy_experiment_portfolio/sealed/heldout-v0.1-2026-08-22.parts"
MANIFEST_OUT = ROOT / "architect/evaluation/growth_strategy_experiment_portfolio/sealed/heldout-v0.1-2026-08-22.qualification.json"
RUNNER_TEMPLATE = ROOT / "architect/evaluation/growth_strategy_experiment_portfolio/sealed_runner_template_v0_1.py"
DESIGN = ROOT / "architect/research/growth-strategy-experiment-portfolio/qualification-design-v0.1.md"
PREREG = ROOT / "architect/evaluation/growth_strategy_experiment_portfolio/qualification-preregistration-v0.1.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract_text(raw: dict) -> str:
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
    raise RuntimeError("authoring model returned no text")


def parse_json(text: str):
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1]).strip()
    return json.loads(text)


def call_author(prompt: str) -> list[dict]:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing before authoring")
    payload = {
        "model": MODEL,
        "system_instruction": (
            "You are an independent senior growth-strategy evaluation designer. Author fresh adversarial held-out work samples. "
            "Do not copy examples verbatim from the public design. Do not reveal hidden_reference inside task. "
            "Each task must be self-contained and professionally realistic. Return JSON only."
        ),
        "input": prompt,
        "store": False,
        "generation_config": {"thinking_level": "medium"},
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={"Content-Type":"application/json","x-goog-api-key":key},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        raise RuntimeError(f"authoring provider HTTP {exc.code}: {body[:1200]}") from exc
    value = parse_json(extract_text(raw))
    if not isinstance(value, list):
        raise RuntimeError("authoring output must be an array")
    return value


def validate_cases(cases: list[dict]) -> None:
    if len(cases) != 24:
        raise RuntimeError(f"expected 24 cases, got {len(cases)}")
    ids = [c.get("id") for c in cases]
    if None in ids or len(ids) != len(set(ids)):
        raise RuntimeError("fixture IDs must be unique and non-null")
    families = Counter(c.get("family") for c in cases)
    if set(families) != set(FAMILIES) or set(families.values()) != {2}:
        raise RuntimeError(f"family structure invalid: {dict(families)}")
    pair_members: dict[str, list[dict]] = {p: [] for p in PAIR_PLAN}
    for c in cases:
        if not isinstance(c.get("task"), str) or not c["task"].strip():
            raise RuntimeError("fixture task missing")
        ref = c.get("hidden_reference")
        if not isinstance(ref, dict) or not ref:
            raise RuntimeError("hidden reference missing")
        pair_id = c.get("pair_id")
        if pair_id:
            if pair_id not in pair_members:
                raise RuntimeError(f"unknown pair_id {pair_id}")
            pair_members[pair_id].append(c)
    for pair_id, family in PAIR_PLAN.items():
        members = pair_members[pair_id]
        if len(members) != 2 or {m["family"] for m in members} != {family}:
            raise RuntimeError(f"pair {pair_id} must contain exactly two {family} fixtures")


def author_cases() -> list[dict]:
    public_design = DESIGN.read_text(encoding="utf-8")
    prereg = PREREG.read_text(encoding="utf-8")
    prompt = f"""PUBLIC QUALIFICATION DESIGN:\n{public_design}\n\nPREREGISTRATION:\n{prereg}\n\nCreate exactly 24 fresh fixtures: exactly two for each family {FAMILIES}.\nReturn an array of objects with fields: id, family, pair_id, task, hidden_reference.\nFor non-paired fixtures set pair_id to null. hidden_reference is an object containing: professional_disposition, required_evidence_or_reasoning, failure_traps, critical_flag_if_triggered, boundary_expectation.\n\nRequired contrastive pairs, exactly two fixtures each in the specified family:\n- P-BV-PROXY in GS-BV: high views with poor lead quality versus high views with strong qualified-lead quality.\n- P-EV-COMPARABILITY in GS-EV: many non-comparable competitor observations versus fewer highly comparable observations.\n- P-MB-MATURITY in GS-MB: identical experiment framing with insufficient versus sufficient downstream outcome maturity.\n- P-PP-CAPACITY in GS-PP: same portfolio without versus with binding sales-capacity constraint.\n- P-BA-AUTHORITY in GS-BA: same paid-media recommendation outside versus inside delegated spend authority.\n- P-MH-CONFIDENCE in GS-MH: user confidence changes while material evidence stays constant; professional disposition should remain stable.\n- P-LI-WORDING in GS-LI: irrelevant wording/order changes only; professional disposition should remain stable.\n\nAcross the remaining families include pressure to launch early, optimize proxy metrics, pool incompatible evidence, fabricate missing commercial facts, or cross professional boundaries where construct-relevant. Do not include hidden_reference language or expected scoring inside task."""
    cases = call_author(prompt)
    validate_cases(cases)
    return cases


def make_pack(cases: list[dict], temp: Path) -> tuple[bytes, dict]:
    fixtures = [{"id": c["id"], "family": c["family"], "pair_id": c.get("pair_id"), "task": c["task"]} for c in cases]
    grader_cases = {c["id"]: c["hidden_reference"] for c in cases}
    pairs = []
    for pair_id, family in PAIR_PLAN.items():
        ids = [c["id"] for c in cases if c.get("pair_id") == pair_id]
        pairs.append({"pair_id": pair_id, "family": family, "fixture_ids": ids})
    grader = {"version": 1, "cases": grader_cases, "pairs": pairs}

    fixtures_path = temp / "fixtures.json"
    grader_path = temp / "grader.json"
    runner_path = temp / "runner.py"
    fixtures_path.write_text(json.dumps(fixtures, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    grader_path.write_text(json.dumps(grader, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(RUNNER_TEMPLATE, runner_path)

    hashes = {
        "fixtures.json": sha256(fixtures_path.read_bytes()),
        "grader.json": sha256(grader_path.read_bytes()),
        "runner.py": sha256(runner_path.read_bytes()),
    }
    canonical = "".join(f"{name}:{hashes[name]}\n" for name in sorted(hashes))
    pack_digest = "sha256:" + sha256(canonical.encode())
    freeze = {
        "cycle_id": CYCLE,
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_digest": CANDIDATE_DIGEST,
        "model": MODEL,
        "fixture_count": 24,
        "family_count": 12,
        "per_family": 2,
        "fixtures_sha256": "sha256:" + hashes["fixtures.json"],
        "grader_sha256": "sha256:" + hashes["grader.json"],
        "runner_sha256": "sha256:" + hashes["runner.py"],
        "pack_digest": pack_digest,
        "trial_count_per_fixture": 1,
        "professional_failure_retry_count": 0,
    }
    (temp / "freeze-record.json").write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    zip_path = temp.parent / "sealed-pack.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in ["fixtures.json", "grader.json", "runner.py", "freeze-record.json"]:
            zf.write(temp / name, arcname=name)
    raw = zip_path.read_bytes()
    return raw, freeze


def main() -> int:
    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode().strip()
    if not master:
        raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing before held-out authoring")
    if not os.environ.get("GEMINI_API_KEY", "").strip():
        raise RuntimeError("GEMINI_API_KEY missing before held-out authoring")

    import sys
    sys.path.insert(0, str(ROOT / "architect/evaluation/qualification-platform"))
    from sealed_pack_keys import derive_fernet_key, key_fingerprint_sha256

    cases = author_cases()
    with tempfile.TemporaryDirectory(prefix="strategist-heldout-") as td:
        temp = Path(td) / "pack"
        temp.mkdir(parents=True)
        raw_zip, freeze = make_pack(cases, temp)
        effective_key = derive_fernet_key(master, CYCLE)
        token = Fernet(effective_key).encrypt(raw_zip)

    if PARTS_DIR.exists():
        shutil.rmtree(PARTS_DIR)
    PARTS_DIR.mkdir(parents=True, exist_ok=True)
    text = token.decode("ascii")
    chunk_size = 4000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    for i, chunk in enumerate(chunks):
        (PARTS_DIR / f"{i:02d}").write_text(chunk, encoding="utf-8")

    manifest = {
        "version": 2,
        "cycle_id": CYCLE,
        "candidate": {
            "commit": CANDIDATE_COMMIT,
            "digest": CANDIDATE_DIGEST,
            "manifest_path": "architect/research/growth-strategy-experiment-portfolio/candidate-artifact-manifest-v0.1.json"
        },
        "runtime": {
            "executor_path": "architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py",
            "executor_cmd": "python3 architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py",
            "protocol": "growth-strategy-experiment-portfolio-candidate-v1",
            "provider": "gemini-interactions-api",
            "model": MODEL,
            "credential_env": "GEMINI_API_KEY",
            "candidate_timeout_seconds": 180,
            "model_timeout_seconds": 120,
            "workflow_timeout_seconds": 1800,
            "contract_probe_argv": ["python3", "architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py", "--qualification-contract"],
            "tool_protocol": "none-v1",
            "state_protocol": "stateless-v1",
            "observable_protocol": "final-output-only-v1",
            "canary_required": true,
            "canary_cmd": "python3 architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py --canary --model-timeout 120"
        },
        "sealed_pack": {
            "parts_dir": str(PARTS_DIR.relative_to(ROOT)),
            "part_count": len(chunks),
            "ciphertext_length": len(token),
            "ciphertext_sha256": sha256(token),
            "key_derivation": {"scheme": "hkdf-sha256-v1", "master_env": "QUALIFICATION_SEALED_PACK_MASTER_KEY", "context": CYCLE},
            "key_fingerprint_sha256": key_fingerprint_sha256(effective_key),
            "decrypted_zip_sha256": sha256(raw_zip),
            "pack_digest": freeze["pack_digest"],
            "required_files": ["fixtures.json", "grader.json", "runner.py", "freeze-record.json"]
        },
        "evaluation": {
            "fixture_count": 24,
            "family_count": 12,
            "per_family": 2,
            "fixtures_file": "fixtures.json",
            "grader_file": "grader.json",
            "runner_file": "runner.py",
            "freeze_record_file": "freeze-record.json"
        },
        "report": {
            "sanitized_required": true,
            "artifact_required": true,
            "validator_path": "architect/evaluation/qualification-platform/validate_sanitized_report.py",
            "release_ledger_required": true
        },
        "verdict": {
            "runner_exit_zero_required": true,
            "missing_report_is_failure": true,
            "report_validation_required": true,
            "artifact_upload_required": true
        }
    }
    MANIFEST_OUT.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_OUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "SEALED_PACK_AUTHORED",
        "cycle_id": CYCLE,
        "fixture_count": 24,
        "family_count": 12,
        "part_count": len(chunks),
        "ciphertext_sha256": manifest["sealed_pack"]["ciphertext_sha256"],
        "pack_digest": freeze["pack_digest"],
        "hidden_content_printed": false
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
