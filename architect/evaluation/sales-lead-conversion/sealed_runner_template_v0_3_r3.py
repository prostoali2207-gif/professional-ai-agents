#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

BASE = Path("architect/evaluation/sales-lead-conversion/sealed_runner_template_v0_3_r2.py")
CYCLE = "sales-0.3-fresh-independent-2026-08-23-r3"


def main() -> int:
    spec = importlib.util.spec_from_file_location("sales_r3_runner_base", BASE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load base Sales qualification runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CYCLE_ID = CYCLE
    return int(module.main())


if __name__ == "__main__":
    raise SystemExit(main())
