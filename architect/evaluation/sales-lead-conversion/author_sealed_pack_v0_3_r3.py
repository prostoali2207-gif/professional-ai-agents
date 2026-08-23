#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import tempfile
from typing import Any

ROOT = Path.cwd()
BASE_FILE = ROOT / "architect/evaluation/sales-lead-conversion/author_sealed_pack_v0_3_r2.py"
BASE_DIR = ROOT / "architect/evaluation/sales-lead-conversion"
BASE_RUNNER = BASE_DIR / "sealed_runner_template_v0_3_r2.py"
CYCLE = "sales-0.3-fresh-independent-2026-08-23-r3"
R2_CYCLE = "sales-0.3-fresh-independent-2026-08-23-r2"


def load_base():
    spec = importlib.util.spec_from_file_location("sales_r3_author_base", BASE_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load base Sales held-out author")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_envelope(cases: list[dict[str, Any]]) -> None:
    """Normalize only nullable transport/envelope fields; never repair hidden semantics."""
    for case in cases:
        if not isinstance(case, dict):
            continue
        if case.get("initial_state") is None:
            case["initial_state"] = {}
        scenario = case.get("tool_scenario")
        if scenario is None:
            case["tool_scenario"] = {"authority": {"mode": "draft_only"}, "tools": []}
        elif isinstance(scenario, dict):
            if scenario.get("authority") is None:
                scenario["authority"] = {"mode": "draft_only"}
            if scenario.get("tools") is None:
                scenario["tools"] = []


def materialize_self_contained_runner() -> Path:
    text = BASE_RUNNER.read_text()
    if R2_CYCLE not in text:
        raise RuntimeError("base runner cycle binding not found")
    text = text.replace(R2_CYCLE, CYCLE)
    fd, name = tempfile.mkstemp(prefix="sales-r3-runner-", suffix=".py")
    os.close(fd)
    path = Path(name)
    path.write_text(text)
    return path


def main() -> int:
    module = load_base()
    module.CYCLE = CYCLE
    module.PREREG = BASE_DIR / "qualification-preregistration-v0_3-r3.json"
    module.OUT_ROOT = BASE_DIR / "sealed/runtime-sales-0.3-r3"
    module.PARTS = module.OUT_ROOT / "parts"
    module.MANIFEST = module.OUT_ROOT / "qualification.json"

    original_validate = module.validate_cases

    def hardened_validate(cases):
        normalize_envelope(cases)
        return original_validate(cases)

    module.validate_cases = hardened_validate
    runner = materialize_self_contained_runner()
    module.RUNNER_TEMPLATE = runner
    try:
        return int(module.main())
    finally:
        runner.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
