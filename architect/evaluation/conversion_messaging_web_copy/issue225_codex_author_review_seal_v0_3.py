#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import zipfile

from cryptography.fernet import Fernet

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
BASE_PATH = HERE / "issue225_codex_author_review_seal_v0_2.py"
PREREG_V2 = HERE / "issue225-sealed-prerequisite-prereg-v0.2.json"

spec = importlib.util.spec_from_file_location("issue225_r1_transport", BASE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("unable to load issue225 v0_2 transport")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.PREREG = PREREG_V2


def key_bytes(p: dict) -> bytes:
    name = str(p["sealing"]["key_env"])
    raw = os.environ.get(name, "").encode().strip()
    if not raw:
        raise base.GateError(f"direct sealed-pack key missing: {name}")
    try:
        Fernet(raw)
    except Exception as exc:
        raise base.GateError("direct sealed-pack key is not a valid Fernet key") from exc
    return raw


def direct_seal(p: dict, cases: list[dict]) -> dict:
    key = key_bytes(p)
    cycle = p["cycle_id"]
    with tempfile.TemporaryDirectory(prefix="msg225-r2-pack-") as raw:
        d = Path(raw) / "pack"
        d.mkdir()
        fixtures = [{k: x[k] for k in ("id", "family", "pair_id", "task", "context", "constraints")} for x in cases]
        grader = {x["id"]: x["hidden_reference"] for x in cases}
        (d / "fixtures.json").write_text(json.dumps(fixtures, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (d / "grader.json").write_text(json.dumps(grader, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        shutil.copyfile(base.RUNNER, d / "runner.py")
        hs = {n: base.h((d / n).read_bytes()) for n in ("fixtures.json", "grader.json", "runner.py")}
        pack_digest = "sha256:" + base.h("".join(f"{n}:{hs[n]}\n" for n in sorted(hs)).encode())
        freeze = {
            "cycle_id": cycle,
            "candidate_commit": p["candidate"]["commit"],
            "candidate_digest": p["candidate"]["artifact_digest"],
            "fixture_count": 24,
            "family_count": 12,
            "per_family": 2,
            "contrastive_pair_count": 4,
            "fixtures_sha256": "sha256:" + hs["fixtures.json"],
            "grader_sha256": "sha256:" + hs["grader.json"],
            "runner_sha256": "sha256:" + hs["runner.py"],
            "pack_digest": pack_digest,
            "thresholds": p["construct"]["thresholds"],
            "candidate_calls": 0,
            "scored_calls": 0,
        }
        (d / "freeze-record.json").write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        z = Path(raw) / "pack.zip"
        with zipfile.ZipFile(z, "w", compression=zipfile.ZIP_DEFLATED) as q:
            for n in ("fixtures.json", "grader.json", "runner.py", "freeze-record.json"):
                q.write(d / n, arcname=n)
        plain = z.read_bytes()
        token = Fernet(key).encrypt(plain)

    parts = ROOT / p["sealing"]["parts_dir"]
    manifest_path = ROOT / p["sealing"]["manifest_path"]
    if parts.exists():
        shutil.rmtree(parts)
    parts.mkdir(parents=True)
    text = token.decode("ascii")
    chunks = [text[i:i + 4000] for i in range(0, len(text), 4000)]
    for i, chunk in enumerate(chunks):
        (parts / f"{i:02d}").write_text(chunk, encoding="ascii")

    key_env = p["sealing"]["key_env"]
    manifest = {
        "version": 2,
        "cycle_id": cycle,
        "candidate": {
            "commit": p["candidate"]["commit"],
            "digest": p["candidate"]["artifact_digest"],
            "manifest_path": "agents/conversion-messaging-web-copy/0.1.0/artifact-manifest.json",
        },
        "runtime": {
            "provider": "codex-subscription-chatgpt-auth",
            "candidate_model": "gpt-5.6-terra",
            "candidate_adapter": "architect/evaluation/conversion_messaging_web_copy/codex_candidate_adapter_v0_1.py",
            "judge_adapter": "architect/evaluation/conversion_messaging_web_copy/codex_judge_adapter_v0_1.py",
            "tool_protocol": "none-v1",
            "state_protocol": "stateless-ephemeral-v1",
        },
        "sealed_pack": {
            "parts_dir": p["sealing"]["parts_dir"],
            "part_count": len(chunks),
            "ciphertext_length": len(token),
            "ciphertext_sha256": base.h(token),
            "key_env": key_env,
            "key_fingerprint_sha256": hashlib.sha256(key).hexdigest(),
            "decrypted_zip_sha256": base.h(plain),
            "pack_digest": freeze["pack_digest"],
            "required_files": ["fixtures.json", "grader.json", "runner.py", "freeze-record.json"],
        },
        "evaluation": {
            "fixture_count": 24,
            "family_count": 12,
            "per_family": 2,
            "contrastive_pair_count": 4,
            "thresholds": p["construct"]["thresholds"],
        },
        "authoring": {
            "provider": "codex-subscription-chatgpt-auth",
            "author_model": p["authoring"]["author_model"],
            "reviewer_model": p["authoring"]["reviewer_model"],
            "candidate_calls": 0,
            "paid_api_calls": 0,
        },
        "verdict": {"sealed_prerequisite_only": True, "candidate_scoring_authorized": False},
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "manifest": str(manifest_path.relative_to(ROOT)),
        "ciphertext_sha256": manifest["sealed_pack"]["ciphertext_sha256"],
        "pack_digest": freeze["pack_digest"],
        "part_count": len(chunks),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preflight", action="store_true")
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--timeout", type=int, default=900)
    args = ap.parse_args()
    if args.preflight == args.execute:
        raise base.GateError("choose exactly one mode")

    p = base.prereg()
    if p.get("status") != "PREREGISTERED":
        raise base.GateError("preregistration not frozen")
    for name in base.PAID_KEYS:
        if os.environ.get(name):
            raise base.GateError(f"separately billed API credential present: {name}")
    if not base.RUNNER.is_file():
        raise base.GateError("sealed runner template missing")

    if args.preflight:
        print(json.dumps({
            "status": "PASS",
            "model_calls": 0,
            "candidate_calls": 0,
            "scored_calls": 0,
            "paid_api_calls": 0,
            "cycle_id": p["cycle_id"],
            "key_mode": p["sealing"]["key_mode"],
        }, sort_keys=True))
        return 0

    # Fail before any subscription call if the evaluator-owned sealing key is absent/invalid.
    key_bytes(p)
    facts = base.cli_facts()
    retry_left = p["retry_policy"]["shared_transport_retry_budget"]
    calls = 0

    def bounded(role: str, model: str, prompt: str):
        nonlocal retry_left, calls
        while True:
            try:
                calls += 1
                return base.invoke(role, model, prompt, p, args.timeout)
            except base.CodexFailure as exc:
                cls = base.classify(exc.stdout, exc.stderr)
                if cls == "TRANSIENT_TRANSPORT" and retry_left > 0:
                    retry_left -= 1
                    continue
                raise base.GateError(json.dumps({
                    "role": role,
                    "classification": cls,
                    "returncode": exc.returncode,
                    "stdout_tail": base.redacted(exc.stdout),
                    "stderr_tail": base.redacted(exc.stderr),
                }))

    authored, author_transport = bounded("author", p["authoring"]["author_model"], base.author_prompt(p))
    reviewed, reviewer_transport = bounded("reviewer", p["authoring"]["reviewer_model"], base.review_prompt(p, authored))
    base.validate(reviewed, p)
    sealed = direct_seal(p, reviewed)
    print(json.dumps({
        "status": "SEALED_PREREQUISITE_READY",
        "cycle_id": p["cycle_id"],
        "subscription_calls": calls,
        "retry_used": p["retry_policy"]["shared_transport_retry_budget"] - retry_left,
        "candidate_calls": 0,
        "scored_calls": 0,
        "paid_api_calls": 0,
        "hidden_content_printed": False,
        "cli_version": facts["version"],
        "author_transport": author_transport,
        "reviewer_transport": reviewer_transport,
        **sealed,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({
            "status": "AUTHORING_INFRASTRUCTURE_FAIL",
            "error": base.redacted(f"{type(exc).__name__}: {exc}"),
            "candidate_calls": 0,
            "scored_calls": 0,
            "paid_api_calls": 0,
        }, ensure_ascii=False))
        raise SystemExit(2)
