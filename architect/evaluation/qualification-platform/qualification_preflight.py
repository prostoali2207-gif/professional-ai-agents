#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import py_compile
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter


class PreflightError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def fail(code: str, message: str) -> None:
    raise PreflightError(code, message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as exc:
        fail("CANDIDATE_UNAVAILABLE", exc.output.strip() or "git object unavailable")


def validate_manifest_shape(m: dict) -> None:
    required = {"version", "cycle_id", "candidate", "runtime", "sealed_pack", "evaluation", "report", "verdict"}
    missing = required - set(m)
    if missing:
        fail("RUNTIME_CONTRACT_MISMATCH", f"manifest missing keys: {sorted(missing)}")
    if m.get("version") != 1:
        fail("RUNTIME_CONTRACT_MISMATCH", "unsupported qualification manifest version")
    c = m["candidate"]
    if len(c.get("commit", "")) != 40 or not c.get("digest", "").startswith("sha256:"):
        fail("RUNTIME_CONTRACT_MISMATCH", "invalid candidate identity declaration")
    r = m["runtime"]
    for key in ("executor_path", "executor_cmd", "protocol", "model", "credential_env"):
        if not r.get(key):
            fail("RUNTIME_CONTRACT_MISMATCH", f"runtime.{key} missing")
    s = m["sealed_pack"]
    for key in ("parts_dir", "key_env", "ciphertext_sha256", "key_fingerprint_sha256", "decrypted_zip_sha256", "pack_digest"):
        if not s.get(key):
            fail("RUNTIME_CONTRACT_MISMATCH", f"sealed_pack.{key} missing")
    if m["report"].get("sanitized_required") is not True or m["report"].get("artifact_required") is not True:
        fail("REPORT_INVALID", "sanitized report and artifact publication must be mandatory")
    if m["verdict"].get("runner_exit_zero_required") is not True or m["verdict"].get("missing_report_is_failure") is not True:
        fail("VERDICT_ENFORCEMENT_FAILED", "fail-closed verdict contract required")


def verify_candidate(m: dict) -> None:
    c = m["candidate"]
    commit = c["commit"]
    git("cat-file", "-e", f"{commit}^{{commit}}")
    try:
        raw = subprocess.check_output(["git", "show", f"{commit}:{c['manifest_path']}"], text=True)
        artifact_manifest = json.loads(raw)
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError) as exc:
        fail("CANDIDATE_UNAVAILABLE", f"cannot read candidate artifact manifest: {exc}")
    try:
        paths = artifact_manifest["artifact"]["paths"]
        declared = artifact_manifest["artifact"]["content_digest"]
    except KeyError as exc:
        fail("CANDIDATE_DIGEST_MISMATCH", f"candidate manifest lacks artifact digest data: {exc}")
    canonical = ""
    for path in paths:
        try:
            blob = subprocess.check_output(["git", "rev-parse", f"{commit}:{path}"], text=True).strip()
        except subprocess.CalledProcessError as exc:
            fail("CANDIDATE_UNAVAILABLE", f"candidate artifact path unavailable: {path}")
        canonical += f"{path}:{blob}\n"
    actual = "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()
    if actual != c["digest"] or actual != declared:
        fail("CANDIDATE_DIGEST_MISMATCH", f"expected {c['digest']}, got {actual}")


def verify_runtime_static(m: dict, require_runtime_secret: bool) -> None:
    r = m["runtime"]
    path = Path(r["executor_path"])
    if not path.is_file():
        fail("RUNTIME_CONTRACT_MISMATCH", f"executor missing: {path}")
    if path.suffix == ".py":
        try:
            with tempfile.TemporaryDirectory() as td:
                py_compile.compile(str(path), cfile=str(Path(td) / "executor.pyc"), doraise=True)
        except py_compile.PyCompileError as exc:
            fail("RUNTIME_CONTRACT_MISMATCH", f"executor syntax invalid: {exc.msg}")
    model_timeout = int(r["model_timeout_seconds"])
    candidate_timeout = int(r["candidate_timeout_seconds"])
    workflow_timeout = int(r["workflow_timeout_seconds"])
    if model_timeout >= candidate_timeout:
        fail("TIMEOUT_INCOMPATIBLE", "model timeout must be smaller than candidate timeout")
    if candidate_timeout >= workflow_timeout:
        fail("TIMEOUT_INCOMPATIBLE", "candidate timeout must be smaller than workflow timeout")
    if r.get("canary_required") and not r.get("canary_cmd"):
        fail("RUNTIME_CONTRACT_MISMATCH", "canary required but canary_cmd missing")
    if require_runtime_secret and not os.environ.get(r["credential_env"], "").strip():
        fail("CREDENTIAL_MISSING", f"required runtime credential missing: {r['credential_env']}")


def safe_extract(zf: zipfile.ZipFile, target: Path) -> None:
    for info in zf.infolist():
        p = PurePosixPath(info.filename)
        if p.is_absolute() or ".." in p.parts:
            fail("PACK_INTEGRITY_INVALID", "unsafe archive path detected")
    zf.extractall(target)


def verify_sealed_pack(m: dict, output_dir: Path) -> None:
    try:
        from cryptography.fernet import Fernet, InvalidToken
    except ImportError:
        fail("RUNTIME_CONTRACT_MISMATCH", "cryptography dependency missing for sealed verification")

    s = m["sealed_pack"]
    root = Path(s["parts_dir"])
    parts = [root / f"{i:02d}" for i in range(int(s["part_count"]))]
    if not all(p.is_file() for p in parts):
        fail("SEALED_TRANSPORT_INVALID", "sealed chunk missing")
    token = "".join(p.read_text() for p in parts).encode()
    if len(token) != int(s["ciphertext_length"]):
        fail("SEALED_TRANSPORT_INVALID", f"ciphertext length mismatch: {len(token)}")
    if sha256_bytes(token) != s["ciphertext_sha256"]:
        fail("SEALED_TRANSPORT_INVALID", "ciphertext sha256 mismatch")

    key = os.environ.get(s["key_env"], "").encode().strip()
    if not key:
        fail("CREDENTIAL_MISSING", f"sealed pack key missing: {s['key_env']}")
    if sha256_bytes(key) != s["key_fingerprint_sha256"]:
        fail("SEALED_KEY_MISMATCH", "sealed key fingerprint mismatch")
    try:
        raw = Fernet(key).decrypt(token)
    except (InvalidToken, ValueError) as exc:
        fail("SEALED_AUTH_FAILED", "sealed authentication/decryption failed")
    if sha256_bytes(raw) != s["decrypted_zip_sha256"]:
        fail("PACK_INTEGRITY_INVALID", "decrypted zip sha256 mismatch")

    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir.parent / (output_dir.name + ".zip")
    zip_path.write_bytes(raw)
    try:
        with zipfile.ZipFile(zip_path) as zf:
            safe_extract(zf, output_dir)
    except zipfile.BadZipFile:
        fail("PACK_INTEGRITY_INVALID", "decrypted payload is not a valid zip")

    required = s["required_files"]
    if not all((output_dir / name).is_file() for name in required):
        fail("PACK_INTEGRITY_INVALID", "required sealed pack file missing")

    e = m["evaluation"]
    freeze_path = output_dir / e["freeze_record_file"]
    try:
        freeze = json.loads(freeze_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail("PACK_INTEGRITY_INVALID", f"invalid freeze record: {exc}")

    if freeze.get("candidate_commit") != m["candidate"]["commit"] or freeze.get("candidate_digest") != m["candidate"]["digest"]:
        fail("PACK_INTEGRITY_INVALID", "freeze record candidate binding mismatch")
    if freeze.get("model") != m["runtime"]["model"]:
        fail("RUNTIME_CONTRACT_MISMATCH", "freeze record model differs from runtime model")

    component_fields = {
        e["fixtures_file"]: "fixtures_sha256",
        e["grader_file"]: "grader_sha256",
        e["runner_file"]: "runner_sha256",
    }
    hashes: dict[str, str] = {}
    for name, field in component_fields.items():
        h = sha256_bytes((output_dir / name).read_bytes())
        hashes[name] = h
        if freeze.get(field) != "sha256:" + h:
            fail("PACK_INTEGRITY_INVALID", f"component digest mismatch: {name}")
    canonical = "".join(f"{name}:{hashes[name]}\n" for name in sorted(hashes))
    actual_pack = "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()
    if actual_pack != s["pack_digest"] or freeze.get("pack_digest") != actual_pack:
        fail("PACK_INTEGRITY_INVALID", "pack digest mismatch")

    try:
        fixtures = json.loads((output_dir / e["fixtures_file"]).read_text())
        grader = json.loads((output_dir / e["grader_file"]).read_text())
    except json.JSONDecodeError as exc:
        fail("PACK_STRUCTURE_INVALID", f"invalid fixtures/grader JSON: {exc}")
    if len(fixtures) != int(e["fixture_count"]) or len(grader) != int(e["fixture_count"]):
        fail("PACK_STRUCTURE_INVALID", "fixture/grader cardinality mismatch")
    ids = [x.get("id") for x in fixtures]
    if None in ids or len(ids) != len(set(ids)) or set(ids) != set(grader):
        fail("PACK_STRUCTURE_INVALID", "fixture/grader ID mismatch")
    families = Counter(x.get("family") for x in fixtures)
    if None in families or len(families) != int(e["family_count"]):
        fail("PACK_STRUCTURE_INVALID", "family count mismatch")
    if set(families.values()) != {int(e["per_family"])}:
        fail("PACK_STRUCTURE_INVALID", "per-family cardinality mismatch")


def run_canary(m: dict) -> None:
    r = m["runtime"]
    if not r.get("canary_required"):
        return
    if not os.environ.get(r["credential_env"], "").strip():
        fail("CREDENTIAL_MISSING", f"required runtime credential missing: {r['credential_env']}")
    try:
        subprocess.run(r["canary_cmd"], shell=True, check=True, timeout=int(r["candidate_timeout_seconds"]))
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        fail("CANARY_FAILED", f"runtime canary failed: {exc}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--phase", choices=("static", "sealed", "canary", "all"), default="all")
    p.add_argument("--require-runtime-secret", action="store_true")
    p.add_argument("--out-dir")
    args = p.parse_args()
    try:
        m = json.loads(Path(args.manifest).read_text())
        validate_manifest_shape(m)
        if args.phase in ("static", "all"):
            verify_candidate(m)
            verify_runtime_static(m, args.require_runtime_secret)
        if args.phase in ("sealed", "all"):
            out = Path(args.out_dir or tempfile.mkdtemp(prefix="qualification-pack-"))
            verify_sealed_pack(m, out)
        if args.phase in ("canary", "all"):
            run_canary(m)
    except PreflightError as exc:
        print(json.dumps({"status": "FAIL", "failure_class": exc.code, "message": str(exc)}))
        return 2
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "failure_class": "QUALIFICATION_NOT_EXECUTABLE", "message": str(exc)}))
        return 3
    print(json.dumps({"status": "PASS", "phase": args.phase, "cycle_id": m["cycle_id"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
