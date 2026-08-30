#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

GATE_ID = "content-architecture-v0.4-codex-heldout-2026-08-30-r2"
BASE = Path(__file__).resolve().parents[1] / "content-architecture-v04-fresh" / "author_pack_v01.py"

spec = importlib.util.spec_from_file_location("content_architecture_r1_author", BASE)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)

# Preserve the frozen r1 construct templates and P0 semantics. Only the cycle binding
# changes, which produces a new secret-derived exact corpus identity/nonces for r2.
base.GATE_ID = GATE_ID

if __name__ == "__main__":
    base.main()
