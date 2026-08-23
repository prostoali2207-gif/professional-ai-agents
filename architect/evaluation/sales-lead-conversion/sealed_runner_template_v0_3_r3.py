#!/usr/bin/env python3
from __future__ import annotations

import runpy

BASE = "architect/evaluation/sales-lead-conversion/sealed_runner_template_v0_3_r2.py"
CYCLE = "sales-0.3-fresh-independent-2026-08-23-r3"


def main() -> int:
    ns = runpy.run_path(BASE, run_name="sales_r3_runner_base")
    ns["CYCLE_ID"] = CYCLE
    # Function globals created by runpy point at the same namespace mapping.
    return int(ns["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
