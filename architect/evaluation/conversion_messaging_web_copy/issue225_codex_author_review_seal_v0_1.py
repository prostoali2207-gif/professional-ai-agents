#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

from cryptography.fernet import Fernet

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PREREG = HERE / "issue225-sealed-prerequisite-prereg-v0.1.json"
RUNNER = HERE / "sealed_runner_template_v0_1.py"
PAID_KEYS = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "GROQ_API_KEY", "XAI_API_KEY")
SECRETISH = ("API_KEY", "ANTHROPIC", "GEMINI", "GROQ", "XAI", "QUALIFICATION", "HELDOUT", "SEALED_PACK", "GRADER")


class GateError(RuntimeError):
    pass


class CodexFailure(RuntimeError):
    def __init__(self, returncode: int, stdout: str, stderr: str):
        super().__init__(f"codex exit={returncode}")
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_prereg() -> dict:
    value = json.loads(PREREG.read_text(encoding="utf-8"))
    if value.get("status") != "PREREGISTERED":
        raise GateError("preregistration is not PREREGISTERED")
    return value


def clean_env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if not any(token in k.upper() for token in SECRETISH)}


def classify_failure(stdout: str, stderr: str) -> str:
    value = (stdout + "\n" + stderr).lower()
    nonretryable = ("quota", "rate limit", "429", "unauthorized", "authentication", "permission denied", "invalid_json_schema", "invalid schema", "invalid argument", "unknown model", "model not found")
    transient = ("timed out", "timeout", "connection reset", "connection closed", "websocket", "temporarily unavailable", "http 500", "http 502", "http 503", "http 504", "status 500", "status 502", "status 503", "status 504")
    if any(x in value for x in nonretryable):
        return "NONRETRYABLE_TECHNICAL"
    if any(x in value for x in transient):
        return "TRANSIENT_TRANSPORT"
    return "UNKNOWN_TECHNICAL"


def sanitize_tail(value: str, limit: int = 1200) -> str:
    text = value[-limit:].replace("\r", "")
    text = re.sub(r"(?i)bearer\s+[a-z0-9._~+/=-]+", "Bearer <redacted>", text)
    text = re.sub(r"(?i)(api[_-]?key|access[_-]?token|refresh[_-]?token)(\s*[:=]\s*)[^\s,;}]+", r"\1\2<redacted>", text)
    return text


def forbidden_event(event: dict) -> bool:
    item = event.get("item") if isinstance(event.get("item"), dict) else {}
    text = f"{event.get('type', '')} {item.get('type', '')}".lower()
    return any(x in text for x in ("command", "tool", "file_change", "mcp", "web_search"))


def case_schema(prereg: dict) -> dict:
    families = prereg["construct"]["families"]
    pair_ids = list(prereg["construct"]["pair_families"])
    hidden_props = {
        "professional_disposition": {"type": "string", "minLength": 20},
        "evidence_boundaries": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "must_do": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "must_not_do": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "hard_fail_if": {"type": "array", "items": {"enum": prereg["construct"]["hard_fails"]}, "uniqueItems": True},
        "functional_craft_criteria": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "boundary_expectation": {"type": "string", "minLength": 10}
    }
    props = {
        "id": {"type": "string", "minLength": 3},
        "family": {"enum": families},
        "pair_id": {"anyOf": [{"enum": pair_ids}, {"type": "null"}]},
        "task": {"type": "string", "minLength": 80},
        "context": {"type": "string"},
        "constraints": {"type": "array", "items": {"type": "string"}},
        "hidden_reference": {"type": "object", "properties": hidden_props, "required": list(hidden_props), "additionalProperties": False}
    }
    return {
        "type": "object",
        "properties": {"cases": {"type": "array", "minItems": 24, "maxItems": 24, "items": {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}}},
        "required": ["cases"],
        "additionalProperties": False
    }


def cli_facts() -> dict[str, str]:
    version = subprocess.check_output(["codex", "--version"], text=True).strip()
    proc = subprocess.run(["codex", "login", "status"], text=True, capture_output=True, check=True)
    login = (proc.stdout + proc.stderr).strip()
    if "Logged in using ChatGPT" not in login:
        raise GateError("Codex CLI is not authenticated with ChatGPT subscription")
    return {"version": version, "login": login}


def invoke(role: str, model: str, prompt: str, prereg: dict, timeout: int) -> tuple[list[dict], dict]:
    with tempfile.TemporaryDirectory(prefix=f"messaging-225-{role}-") as raw:
        workspace = Path(raw)
        schema_path = workspace / "output.schema.json"
        output_path = workspace / "result.json"
        schema_path.write_text(json.dumps(case_schema(prereg)), encoding="utf-8")
        cmd = [
            "codex", "exec", "-", "--json", "--ephemeral", "--ignore-user-config", "--ignore-rules",
            "--skip-git-repo-check", "--sandbox", "read-only", "--model", model,
            "--output-schema", str(schema_path), "--output-last-message", str(output_path),
            "--color", "never", "-C", str(workspace), "-c", 'approval_policy="never"'
        ]
        proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=timeout, cwd=workspace, env=clean_env())
        if proc.returncode != 0:
            raise CodexFailure(proc.returncode, proc.stdout, proc.stderr)
        events = []
        for line in proc.stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                events.append(event)
        if any(forbidden_event(event) for event in events):
            raise GateError(f"{role} emitted forbidden tool/command event")
        if not output_path.is_file():
            raise GateError(f"{role} produced no output")
        value = json.loads(output_path.read_text(encoding="utf-8"))
        cases = value.get("cases")
        validate_cases(cases, prereg)
        completed = [e for e in events if e.get("type") == "turn.completed"]
        return cases, {"model": model, "usage": completed[-1].get("usage") if completed else None, "event_types": [e.get("type") for e in events]}


def validate_cases(cases: object, prereg: dict) -> None:
    if not isinstance(cases, list) or len(cases) != 24:
        raise GateError("fixture cardinality invalid")
    families = prereg["construct"]["families"]
    pair_families = prereg["construct"]["pair_families"]
    counts = Counter(x.get("family") for x in cases if isinstance(x, dict))
    if set(counts) != set(families) or set(counts.values()) != {2}:
        raise GateError(f"family structure invalid: {dict(counts)}")
    ids = [x.get("id") for x in cases]
    if any(not isinstance(x, str) for x in ids) or len(ids) != len(set(ids)):
        raise GateError("fixture IDs invalid")
    paired = []
    for pair_id, family in pair_families.items():
        members = [x for x in cases if x.get("pair_id") == pair_id]
        if len(members) != 2 or {x.get("family") for x in members} != {family}:
            raise GateError(f"pair structure invalid: {pair_id}")
        paired.extend(members)
    if len(paired) != 8:
        raise GateError("paired fixture count invalid")
    if any(x.get("pair_id") is not None for x in cases if x.get("family") not in set(pair_families.values())):
        raise GateError("unexpected pair_id outside preregistered families")


def author_prompt(prereg: dict) -> str:
    c = prereg["construct"]
    return (
        "You are the hidden-test AUTHOR for a professional qualification. You are NOT the candidate and must not infer or seek candidate content. "
        "Do not use tools, filesystem, web, MCP, or external sources. Create fresh authentic work samples from the public profession construct below. "
        "Return schema-valid JSON only. Create exactly 24 cases: exactly 2 per family. Do not copy wording from public development examples or any prior rejected hidden corpus. "
        "Each hidden_reference must specify professional disposition, evidence boundaries, must-do, must-not-do, applicable hard-fail triggers, functional craft criteria, and boundary expectation. "
        "Use exactly four contrastive pairs: P-EVIDENCE/CM-EV, P-CLAIM/CM-CL, P-UX/CM-UX, P-BOUNDARY/CM-BD. In each pair, differ in one material fact and make the professionally correct stance change only where justified. "
        "Construct meanings: CM-EV customer-language provenance, messy contradiction, no-evidence refusal; CM-CL bounded claims, fabricated social proof/urgency/guarantee pressure plus strong-evidence control; CM-MH message hierarchy; CM-DV genuinely distinct framing mechanisms; CM-OP objection-proof matching; CM-UX CTA/helper/error semantics under frozen UX states; CM-PL jargon translation; CM-CR causal critique/revision; CM-EX hypothesis/metric/guardrail/falsifier discipline without guaranteed lift; CM-BD CRO/User Research/UX/legal authority boundaries; CM-PR later-turn stakeholder pressure represented inside one stateless work sample; CM-E2E controlled-facts end-to-end landing messaging. "
        f"Families: {json.dumps(c['families'])}. Hard-fail labels: {json.dumps(c['hard_fails'])}."
    )


def reviewer_prompt(prereg: dict, cases: list[dict]) -> str:
    return (
        "You are the INDEPENDENT CONSTRUCT REVIEWER for hidden professional qualification fixtures. You are not the candidate. "
        "Do not use tools, filesystem, web, MCP, or external sources. Audit the supplied authored cases for construct coverage, grading-boundary validity, pair validity, ambiguity, answer leakage, impossible requirements, stylistic-only grading, unsupported hidden expectations, and accidental candidate tailoring. "
        "Preserve exactly 24 cases, 2 per family, and the four preregistered pairs. Repair only the hidden corpus as needed. Strong-evidence controls must permit appropriately strong claims. "
        "Do not answer the cases. Return the complete reviewed corpus as schema-valid JSON only. Public construct and authored cases follow.\n" +
        json.dumps({"construct": prereg["construct"], "cases": cases}, ensure_ascii=False)
    )


def seal(prereg: dict, cases: list[dict]) -> dict:
    master = os.environ.get(prereg["sealing"]["master_env"], "").encode().strip()
    if not master:
        raise GateError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    sys.path.insert(0, str(ROOT / "architect/evaluation/qualification-platform"))
    from sealed_pack_keys import derive_fernet_key, key_fingerprint_sha256

    cycle = prereg["cycle_id"]
    with tempfile.TemporaryDirectory(prefix="messaging-225-pack-") as raw:
        pack_dir = Path(raw) / "pack"
        pack_dir.mkdir()
        fixtures = [{k: x[k] for k in ("id", "family", "pair_id", "task", "context", "constraints")} for x in cases]
        grader = {x["id"]: x["hidden_reference"] for x in cases}
        (pack_dir / "fixtures.json").write_text(json.dumps(fixtures, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (pack_dir / "grader.json").write_text(json.dumps(grader, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        shutil.copyfile(RUNNER, pack_dir / "runner.py")
        file_hashes = {name: sha256((pack_dir / name).read_bytes()) for name in ("fixtures.json", "grader.json", "runner.py")}
        pack_digest = "sha256:" + sha256("".join(f"{name}:{file_hashes[name]}\n" for name in sorted(file_hashes)).encode())
        freeze = {
            "cycle_id": cycle,
            "candidate_commit": prereg["candidate"]["commit"],
            "candidate_digest": prereg["candidate"]["artifact_digest"],
            "fixture_count": 24,
            "family_count": 12,
            "per_family": 2,
            "contrastive_pair_count": 4,
            "fixtures_sha256": "sha256:" + file_hashes["fixtures.json"],
            "grader_sha256": "sha256:" + file_hashes["grader.json"],
            "runner_sha256": "sha256:" + file_hashes["runner.py"],
            "pack_digest": pack_digest,
            "thresholds": prereg["construct"]["thresholds"],
            "candidate_calls": 0,
            "scored_calls": 0
        }
        (pack_dir / "freeze-record.json").write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        zip_path = Path(raw) / "pack.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name in ("fixtures.json", "grader.json", "runner.py", "freeze-record.json"):
                archive.write(pack_dir / name, arcname=name)
        plaintext = zip_path.read_bytes()
        key = derive_fernet_key(master, cycle)
        token = Fernet(key).encrypt(plaintext)

    parts_dir = ROOT / prereg["sealing"]["parts_dir"]
    manifest_path = ROOT / prereg["sealing"]["manifest_path"]
    if parts_dir.exists():
        shutil.rmtree(parts_dir)
    parts_dir.mkdir(parents=True)
    encoded = token.decode("ascii")
    chunks = [encoded[i:i + 4000] for i in range(0, len(encoded), 4000)]
    for idx, chunk in enumerate(chunks):
        (parts_dir / f"{idx:02d}").write_text(chunk, encoding="ascii")
    manifest = {
        "version": 2,
        "cycle_id": cycle,
        "candidate": {"commit": prereg["candidate"]["commit"], "digest": prereg["candidate"]["artifact_digest"], "manifest_path": "agents/conversion-messaging-web-copy/0.1.0/artifact-manifest.json"},
        "runtime": {"provider": "codex-subscription-chatgpt-auth", "candidate_model": "gpt-5.6-terra", "candidate_adapter": "architect/evaluation/conversion_messaging_web_copy/codex_candidate_adapter_v0_1.py", "judge_adapter": "architect/evaluation/conversion_messaging_web_copy/codex_judge_adapter_v0_1.py", "tool_protocol": "none-v1", "state_protocol": "stateless-ephemeral-v1"},
        "sealed_pack": {"parts_dir": prereg["sealing"]["parts_dir"], "part_count": len(chunks), "ciphertext_length": len(token), "ciphertext_sha256": sha256(token), "key_derivation": {"scheme": "hkdf-sha256-v1", "master_env": prereg["sealing"]["master_env"], "context": cycle}, "key_fingerprint_sha256": key_fingerprint_sha256(key), "decrypted_zip_sha256": sha256(plaintext), "pack_digest": freeze["pack_digest"], "required_files": ["fixtures.json", "grader.json", "runner.py", "freeze-record.json"]},
        "evaluation": {"fixture_count": 24, "family_count": 12, "per_family": 2, "contrastive_pair_count": 4, "thresholds": prereg["construct"]["thresholds"]},
        "authoring": {"provider": "codex-subscription-chatgpt-auth", "author_model": prereg["authoring"]["author_model"], "reviewer_model": prereg["authoring"]["reviewer_model"], "candidate_calls": 0, "paid_api_calls": 0},
        "verdict": {"sealed_prerequisite_only": true, "candidate_scoring_authorized": false}
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"manifest": str(manifest_path.relative_to(ROOT)), "ciphertext_sha256": manifest["sealed_pack"]["ciphertext_sha256"], "pack_digest": freeze["pack_digest"], "part_count": len(chunks)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preflight", action="store_true")
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--timeout", type=int, default=900)
    args = ap.parse_args()
    if args.preflight == args.execute:
        raise GateError("choose exactly one of --preflight or --execute")
    prereg = load_prereg()
    for name in PAID_KEYS:
        if os.environ.get(name):
            raise GateError(f"separately billed API credential present: {name}")
    if not RUNNER.is_file():
        raise GateError("sealed runner template missing")
    if args.preflight:
        print(json.dumps({"status": "PASS", "model_calls": 0, "candidate_calls": 0, "scored_calls": 0, "paid_api_calls": 0, "cycle_id": prereg["cycle_id"]}, sort_keys=True))
        return 0

    facts = cli_facts()
    retry_left = prereg["retry_policy"]["shared_transport_retry_budget"]
    calls = 0

    def bounded(role: str, model: str, prompt: str) -> tuple[list[dict], dict]:
        nonlocal retry_left, calls
        while True:
            try:
                calls += 1
                return invoke(role, model, prompt, prereg, args.timeout)
            except CodexFailure as exc:
                classification = classify_failure(exc.stdout, exc.stderr)
                if classification == "TRANSIENT_TRANSPORT" and retry_left > 0:
                    retry_left -= 1
                    continue
                raise GateError(json.dumps({"role": role, "classification": classification, "returncode": exc.returncode, "stdout_tail": sanitize_tail(exc.stdout), "stderr_tail": sanitize_tail(exc.stderr)}))

    authored, author_transport = bounded("author", prereg["authoring"]["author_model"], author_prompt(prereg))
    reviewed, reviewer_transport = bounded("reviewer", prereg["authoring"]["reviewer_model"], reviewer_prompt(prereg, authored))
    validate_cases(reviewed, prereg)
    sealed = seal(prereg, reviewed)
    print(json.dumps({"status": "SEALED_PREREQUISITE_READY", "cycle_id": prereg["cycle_id"], "subscription_calls": calls, "retry_used": prereg["retry_policy"]["shared_transport_retry_budget"] - retry_left, "candidate_calls": 0, "scored_calls": 0, "paid_api_calls": 0, "hidden_content_printed": false, "cli_version": facts["version"], "author_transport": author_transport, "reviewer_transport": reviewer_transport, **sealed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status": "AUTHORING_INFRASTRUCTURE_FAIL", "error": sanitize_tail(f"{type(exc).__name__}: {exc}"), "candidate_calls": 0, "scored_calls": 0, "paid_api_calls": 0}, ensure_ascii=False))
        raise SystemExit(2)
