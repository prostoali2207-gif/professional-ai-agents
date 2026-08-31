#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

MAX_TOOL_ROUNDS = 16

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()

def send(proc, payload):
    proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
    proc.stdin.flush()

def recv(proc):
    line = proc.stdout.readline()
    if not line:
        stderr = proc.stderr.read()
        raise RuntimeError(f"executor terminated without response: {stderr}")
    try:
        return json.loads(line)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"executor returned invalid JSON: {line!r}") from e

def resolve_tool_call(call, stage, ledger, approvals):
    call_id = call.get("call_id")
    name = call.get("name")
    args = call.get("args", {})
    scripted = stage.get("tool_results", {})
    key = call.get("fixture_key") or name
    if key not in scripted:
        return {
            "call_id": call_id,
            "name": name,
            "status": "unavailable",
            "error": "No controlled fixture result exists for this call"
        }

    result = scripted[key]
    entry = {
        "call_id": call_id,
        "name": name,
        "args": args,
        "result": result
    }

    if name == "approval.request":
        approvals.append(entry)
    if name in {"social.execute", "notify.send", "state.write"}:
        ledger.append(entry)
    return entry

def main():
    ap = argparse.ArgumentParser(description="Qualification harness for frozen Professional Core bundles")
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--fixture-manifest", required=True)
    ap.add_argument("--bundle-manifest", required=True)
    ap.add_argument("--candidate-commit", required=True)
    ap.add_argument("--executor-cmd", required=True, nargs=argparse.REMAINDER)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    if len(args.candidate_commit) != 40 or any(c not in "0123456789abcdef" for c in args.candidate_commit):
        raise SystemExit("candidate commit must be a 40-character lowercase hex SHA")

    fixture = load_json(args.fixture)
    fixture_manifest = load_json(args.fixture_manifest)
    bundle_manifest = load_json(args.bundle_manifest)

    actual_fixture_digest = sha256_file(args.fixture)
    expected_fixture_digest = fixture_manifest.get("fixture_digest")
    if actual_fixture_digest != expected_fixture_digest:
        raise SystemExit(f"fixture digest mismatch: expected {expected_fixture_digest}, got {actual_fixture_digest}")

    if fixture_manifest.get("contamination_status") not in {"clean-declared", "clean"}:
        raise SystemExit("fixture contamination status is not clean-declared")

    if bundle_manifest.get("status") != "frozen-test-only":
        raise SystemExit("qualification bundle is not frozen-test-only")

    proc = subprocess.Popen(
        args.executor_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    tool_trace = []
    approval_trace = []
    side_effect_ledger = []
    events = []
    initial_state = fixture.get("initial_state", {})
    final_state = initial_state

    try:
        send(proc, {
            "type": "init",
            "core_id": bundle_manifest["core_id"],
            "core_version": bundle_manifest["core_version"],
            "core_digest": bundle_manifest["core_digest"],
            "bundle_digest": bundle_manifest["bundle_digest"],
            "capability_profile": fixture["capability_profile"],
            "trusted_context": fixture.get("trusted_context", {}),
            "initial_state": initial_state,
        })
        init_response = recv(proc)
        if init_response.get("type") != "ready":
            raise RuntimeError(f"executor did not acknowledge init: {init_response}")

        for stage in fixture.get("stages", []):
            stage_id = stage["stage_id"]
            send(proc, {
                "type": "stage",
                "stage_id": stage_id,
                "visible_input": stage.get("visible_input"),
                "untrusted_input": stage.get("untrusted_input"),
                "time": stage.get("time"),
                "capabilities": stage.get("capabilities", []),
            })

            stage_record = None
            for _ in range(MAX_TOOL_ROUNDS):
                response = recv(proc)
                rtype = response.get("type")
                if rtype == "tool_calls":
                    results = []
                    for call in response.get("calls", []):
                        result = resolve_tool_call(call, stage, side_effect_ledger, approval_trace)
                        tool_trace.append({
                            "stage_id": stage_id,
                            "call": call,
                            "result": result,
                        })
                        results.append(result)
                    send(proc, {"type": "tool_results", "stage_id": stage_id, "results": results})
                    continue
                if rtype == "stage_output":
                    stage_record = response.get("record", {})
                    break
                raise RuntimeError(f"unexpected executor response for {stage_id}: {response}")
            if stage_record is None:
                raise RuntimeError(f"tool round limit exceeded for {stage_id}")
            events.append({"stage_id": stage_id, "record": stage_record})
            if "observable_state" in stage_record:
                final_state = stage_record["observable_state"]

        send(proc, {"type": "finalize"})
        final_response = recv(proc)
        if final_response.get("type") != "final_output":
            raise RuntimeError(f"executor did not return final_output: {final_response}")

        final_record = final_response.get("record", {})
        if "observable_state" in final_record:
            final_state = final_record["observable_state"]

        run_record = {
            "run_id": fixture.get("run_id") or f"run-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "candidate_commit": args.candidate_commit,
            "core_digest": bundle_manifest["core_digest"],
            "bundle_digest": bundle_manifest["bundle_digest"],
            "fixture_ref": fixture_manifest["fixture_id"],
            "fixture_digest": actual_fixture_digest,
            "grader_ref": fixture_manifest["grader_id"],
            "grader_digest": fixture_manifest["grader_digest"],
            "capability_profile": fixture["capability_profile"],
            "runtime": fixture.get("runtime", "external-executor-jsonl-v1"),
            "model_or_executor": fixture.get("model_or_executor", "external"),
            "initial_state": initial_state,
            "events": events,
            "tool_trace": tool_trace,
            "approval_trace": approval_trace,
            "side_effect_ledger": side_effect_ledger,
            "final_state": final_state,
            "grader_results": [],
            "termination_reason": final_record.get("termination_reason", "executor-finalized"),
            "contamination_status": fixture_manifest.get("contamination_status", "unknown"),
            "result": "INVALID"
        }

        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(run_record, f, ensure_ascii=False, indent=2)
            f.write("\n")

        print(args.out)
        print("Run captured. Grading is intentionally separate; result remains INVALID until frozen graders are applied.")
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()

if __name__ == "__main__":
    main()
