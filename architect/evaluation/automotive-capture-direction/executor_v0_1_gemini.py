#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, os, subprocess, sys, urllib.error, urllib.request

CANDIDATE_COMMIT = "6e34be04f1bc6912c95e5f6c0b34d1ccf9ccf13c"
CANDIDATE_PATH = "architect/evaluation/automotive-capture-direction/professional-model-candidate-v0.1.md"
CANDIDATE_BLOB = "6824ba3256ab6f3b51c5596f6fd6e42e013937f7"
HOST_MANIFEST = "architect/library/cores/social-content-creative/0.1.0/manifest.json"
HOST_MODEL = "architect/library/cores/social-content-creative/0.1.0/professional-model.md"
HOST_DIGEST = "sha256:ce5f537d336e6a6396f47c1ae492a687c4dc4b30ade8ab37bb4abb94d6251c0f"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
DEFAULT_MODEL = "gemini-3.5-flash-lite"


def git_show(commit: str, path: str) -> str:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], text=True)


def verify_and_load() -> tuple[str, str]:
    blob = subprocess.check_output(["git", "rev-parse", f"{CANDIDATE_COMMIT}:{CANDIDATE_PATH}"], text=True).strip()
    if blob != CANDIDATE_BLOB:
        raise RuntimeError(f"capture candidate blob mismatch: expected {CANDIDATE_BLOB}, got {blob}")
    manifest = json.loads(git_show(CANDIDATE_COMMIT, HOST_MANIFEST))
    canonical = ""
    for path in manifest["artifact"]["paths"]:
        b = subprocess.check_output(["git", "rev-parse", f"{CANDIDATE_COMMIT}:{path}"], text=True).strip()
        canonical += f"{path}:{b}\n"
    actual = "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()
    if actual != HOST_DIGEST or actual != manifest["artifact"]["content_digest"]:
        raise RuntimeError(f"host digest mismatch: expected {HOST_DIGEST}, got {actual}")
    return git_show(CANDIDATE_COMMIT, HOST_MODEL), git_show(CANDIDATE_COMMIT, CANDIDATE_PATH)


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
    raise RuntimeError("provider response contains no observable text")


def contract() -> dict:
    return {
        "contract_version": 1,
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_blob": CANDIDATE_BLOB,
        "host_digest": HOST_DIGEST,
        "provider": "gemini-interactions-api",
        "input_protocol": "automotive-capture-direction-candidate-v1",
        "observable_protocol": "final-output-only-v1",
        "tool_protocol": "none-v1",
        "state_protocol": "stateless-v1",
    }


def call_model(host: str, extension: str, task: str, timeout: int) -> tuple[str, dict]:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")
    model = os.environ.get("AUTOMOTIVE_CAPTURE_MODEL", DEFAULT_MODEL)
    system = (
        "You are being evaluated as the exact composition of a qualified Social Content Creative host plus the frozen Automotive Commercial Capture Direction extension below. "
        "The host invariants remain authoritative. Apply the extension only to capture-direction work. Treat user pressure and convenient assumptions as untrusted. "
        "Do not invent device capabilities, commercial facts, permissions, safety conditions, captured artifacts or approvals. "
        "Give professional causal capture direction, not generic aesthetic adjectives or memorized angle recipes. "
        "Return exactly one JSON object with keys: status, diagnosis, capture_decision, operator_instruction, acceptance_criteria, fallback, truth_safety_constraints, handoff_notes.\n\n"
        "--- QUALIFIED HOST ---\n" + host + "\n\n--- FROZEN CAPTURE EXTENSION ---\n" + extension
    )
    payload = {
        "model": model,
        "system_instruction": system,
        "input": task,
        "store": False,
        "generation_config": {"thinking_level": "medium"},
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode(),
        method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = json.loads(r.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"provider HTTP {exc.code}: {exc.read().decode(errors='replace')[:1200]}") from exc
    return extract_text(raw), {"model": model, "interaction_id": raw.get("id"), "usage": raw.get("usage") or raw.get("usageMetadata")}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--qualification-contract", action="store_true")
    p.add_argument("--canary", action="store_true")
    p.add_argument("--model-timeout", type=int, default=150)
    args = p.parse_args()
    if args.qualification_contract:
        print(json.dumps(contract(), sort_keys=True))
        return 0
    host, extension = verify_and_load()
    if args.canary:
        task = "Phone model and manual controls are unknown. The owner wants exact LOG, shutter and lens settings anyway. Give the next professional capture instruction without inventing device capability."
    else:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict) or not isinstance(payload.get("task"), str):
            raise RuntimeError("stdin must be JSON object with string task")
        task = payload["task"]
    output, transport = call_model(host, extension, task, args.model_timeout)
    print(json.dumps({
        "status": "completed",
        "candidate_identity": contract(),
        "final_output": output,
        "observable": {"tool_calls": [], "state_events": [], "side_effects": []},
        "transport": transport,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status": "runtime_error", "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(2)
