# Offline rehearsal harness for the Social Content Creative 0.1.0 qualification cycle.
# Zero provider calls. Synthetic placeholder fixtures only - never qualification evidence.
"""Offline dry run of the sealed runner with both judges stubbed.
Zero provider calls. Proves the runner's control flow, structure checks,
judge-normalisation contract, scoring math, report shape and exit code."""
import importlib.util, json, os, sys
from pathlib import Path

pack = Path(sys.argv[1]); out = Path(sys.argv[2])
os.environ["SOCIAL_CONTENT_MIN_REQUEST_INTERVAL"] = "0"   # rehearsal only; pacing tested separately
runner_path = pack / "runner.py"
sys.path.insert(0, str(pack))
spec = importlib.util.spec_from_file_location("sealed_runner", runner_path)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def fake(payload):
    if payload.get("mode") == "calibration":
        rows = []
        for c in m.CALIBRATION:
            rows.append({"id": c["id"],
                         "scores": {d: 2 for d in m.DIMS},
                         "critical_flags": list(c["expected_flags"]),
                         "pass": not c["expected_flags"]})
        return {"results": rows}
    rows = []
    for c in payload["cases"]:
        rows.append({"id": c["id"], "family": c["family"],
                     "scores": {d: 2 for d in m.DIMS},
                     "critical_flags": [], "pass": True, "reason_code": "stub"})
    return {"results": rows}

m.call_gemini = fake; m.call_groq = fake
sys.argv = ["runner.py", "--pack-dir", str(pack),
            "--executor-cmd", f"{sys.executable} {Path(__file__).with_name('stub_executor.py')}",
            "--model", "gemini-3.5-flash-lite", "--out", str(out)]
try:
    code = m.main()
except SystemExit as e:
    code = e.code
except Exception as exc:
    print(json.dumps({"release_verdict": "NOT_EXECUTABLE", "error": f"{type(exc).__name__}: {exc}"})); code = 2
print("runner_exit_code=", code)
