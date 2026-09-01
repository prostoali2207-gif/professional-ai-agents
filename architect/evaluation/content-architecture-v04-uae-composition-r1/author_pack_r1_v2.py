#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("uae_author_r1", HERE / "author_pack_r1.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)
mod.SPECIALIZATION_SHA = "7f41c2d1ba40c3b4c59e3eba2fb264c04162c320"

if __name__ == "__main__":
    mod.main()
