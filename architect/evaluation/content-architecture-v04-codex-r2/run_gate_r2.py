#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json, os, re, shlex, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
GRADER_PATH = HERE / "grader_r2.py"
spec = importlib.util.spec_from_file_location("grader_r2", GRADER_PATH)
grader = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(grader)
GATE = grader.GATE_ID
SHA = grader.CANDIDATE_SHA


def read_jsonl(path: Path):
    if not path.exists(): return []
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def append(path: Path, obj):
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(obj, ensure_ascii=False, sort_keys=True) + "\n")


def runtime_error_category(proc):
    if proc is None:
        return "CANDIDATE_RUNTIME_EXCEPTION"
    for stream in (proc.stdout or "", proc.stderr or ""):
        for line in reversed(stream.splitlines()):
            try:
                obj = json.loads(line)
            except Exception:
                continue
            category = obj.get("error_category") if isinstance(obj, dict) else None
            if isinstance(category, str) and category:
                return category
    text = ((proc.stderr or "") + "\n" + (proc.stdout or ""))[:6000]
    if re.search(r"429|rate.?limit|quota", text, re.I): return "CODEX_QUOTA_OR_RATE_LIMIT"
    if re.search(r"timed? out|timeout", text, re.I): return "CODEX_TIMEOUT"
    return f"CANDIDATE_RUNTIME_EXIT_{proc.returncode}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--candidate-command", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=300)
    args = ap.parse_args()

    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    records = out / "records.jsonl"
    pack = grader.load_pack(Path(args.pack))
    done = {(r.get("fixture_id"), int(r.get("trial", 0))) for r in read_jsonl(records) if r.get("terminal_status") == "COMPLETED"}
    calls = 0

    command = shlex.split(args.candidate_command, posix=(os.name != "nt"))
    for fixture in pack["fixtures"]:
        for trial in range(1, int(fixture.get("trial_count", 1)) + 1):
            key = (fixture["fixture_id"], trial)
            if key in done: continue
            workspace = out / "workspaces" / f"{fixture['fixture_id']}-t{trial}"
            workspace.mkdir(parents=True, exist_ok=True)
            payload = {
                "protocol_version": 2,
                "candidate_sha": SHA,
                "workspace": str(workspace),
                "input": {**fixture["candidate_input"], "allowed_resources": [], "fixture_tools": {}},
            }
            started = time.time(); proc = None
            try:
                proc = subprocess.run(command, input=json.dumps(payload), text=True, capture_output=True, timeout=args.timeout, env=os.environ.copy())
                if proc.returncode != 0: raise RuntimeError("candidate runtime nonzero")
                raw = json.loads(proc.stdout)
                if raw.get("status") != "completed": raise RuntimeError("candidate runtime incomplete")
                ident = raw.get("candidate_identity", {})
                if ident.get("sha") != SHA: raise RuntimeError("candidate identity mismatch")
                rec = {
                    "gate_id": GATE, "fixture_id": fixture["fixture_id"], "family": fixture["family"],
                    "trial": trial, "trial_count": fixture.get("trial_count", 1), "candidate_sha": SHA,
                    "runtime_identity": ident, "final_response": raw.get("final_output", ""),
                    "observable": raw.get("observable", {}), "transport": raw.get("transport", {}),
                    "terminal_status": "COMPLETED", "duration_s": round(time.time()-started, 3),
                    "error": None, "runtime_error_category": None,
                }
                calls += 1
            except Exception as exc:
                rec = {
                    "gate_id": GATE, "fixture_id": fixture["fixture_id"], "family": fixture["family"],
                    "trial": trial, "trial_count": fixture.get("trial_count", 1), "candidate_sha": SHA,
                    "terminal_status": "ERROR", "duration_s": round(time.time()-started, 3),
                    "error": type(exc).__name__, "runtime_error_category": runtime_error_category(proc),
                }
            append(records, rec)
            if rec["terminal_status"] == "ERROR":
                print(json.dumps({"status":"NOT_EXECUTABLE","fixture_id":fixture["fixture_id"],"trial":trial,"candidate_calls_this_run":calls,"runtime_error_category":rec["runtime_error_category"]}))
                return 3

    report = out / "grade-report.json"
    proc = subprocess.run([sys.executable, str(GRADER_PATH), "--pack", args.pack, "--records", str(records), "--out", str(report)], text=True, capture_output=True, env=os.environ.copy())
    if proc.returncode != 0:
        print(proc.stdout); print(proc.stderr, file=sys.stderr); return proc.returncode
    summary = json.loads(report.read_text(encoding="utf-8"))["summary"]
    summary["candidate_calls_this_run"] = calls
    summary["run_records_total"] = len(read_jsonl(records))
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
