#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess

CYCLE_ID = "sales-0.3-fresh-independent-2026-08-23-r5-gemini"
PROVIDER_WRAPPER = Path("architect/evaluation/sales-lead-conversion/sealed_runner_provider_wrapper_v0_3_gemini.py")
EXPECTED_WRAPPER_BLOB = "dbb30da2f7be61f5ae8f8bf9ed922dbf00e92cdd"


def main() -> int:
    actual = subprocess.check_output(["git", "hash-object", str(PROVIDER_WRAPPER)], text=True).strip()
    if actual != EXPECTED_WRAPPER_BLOB:
        raise RuntimeError(f"provider wrapper drift: {actual}")
    spec = importlib.util.spec_from_file_location("sales_gemini_r5_provider", PROVIDER_WRAPPER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pinned Gemini provider wrapper")
    provider = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(provider)
    provider.CYCLE_ID = CYCLE_ID
    original_load_base = provider.load_base

    def load_base_from_sealed_pack():
        module = original_load_base()
        # Base runner locates fixtures/grader relative to its __file__.
        # Bind that path to this sealed runner, not the public base module.
        module.__file__ = str(Path(__file__).resolve())
        return module

    provider.load_base = load_base_from_sealed_pack
    return int(provider.main())


if __name__ == "__main__":
    raise SystemExit(main())
