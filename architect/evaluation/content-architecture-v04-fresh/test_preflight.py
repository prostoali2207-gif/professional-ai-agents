#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    prereg = json.loads((ROOT / "preregistration-v0.1.json").read_text(encoding="utf-8"))
    assert prereg["status"] == "INFRASTRUCTURE_ONLY_NOT_DISPATCHABLE"
    assert prereg["candidate_blob_sha"] == "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
    assert prereg["grader_contract"]["status"] == "NOT_YET_FROZEN"
    assert prereg["hidden_corpus"]["status"] == "NOT_YET_AUTHORED"

    proc = subprocess.run(
        [sys.executable, str(ROOT / "preflight.py")],
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode != 0, "incomplete gate must fail closed"
    combined = (proc.stdout + proc.stderr).strip()
    assert "NOT EXECUTABLE" in combined
    assert "not DISPATCHABLE_FROZEN" in combined
    print(json.dumps({"status": "PASS", "regression": "incomplete gate fails closed before provider call"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
