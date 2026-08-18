#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from run_pm04_v2_gate import grade

HERE = Path(__file__).resolve().parent
CASES = json.loads((HERE / "pm04_v2_cases.json").read_text(encoding="utf-8"))
OBSERVED = json.loads((HERE / "pm04_v2_observed_answers_2026-08-18.json").read_text(encoding="utf-8"))

by_id = {a["case_id"]: a for a in OBSERVED["answers"]}
results = []
for case in CASES:
    checks, passed = grade(case, by_id[case["id"]])
    results.append({"case_id": case["id"], "status": "PASS" if passed else "FAIL", "checks": checks})

summary = {"status": "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL", "results": results}
print(json.dumps(summary, indent=2))
raise SystemExit(0 if summary["status"] == "PASS" else 1)
