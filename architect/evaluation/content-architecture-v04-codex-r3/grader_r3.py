#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

GATE_ID = "content-architecture-v0.4-codex-heldout-2026-08-30-r3"
BASE = Path(__file__).resolve().parents[1] / "content-architecture-v04-fresh" / "grader_v01.py"

spec = importlib.util.spec_from_file_location("content_architecture_r1_grader", BASE)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)
base.GATE_ID = GATE_ID
CANDIDATE_SHA = base.CANDIDATE_SHA
P0_FAMILY = base.P0_FAMILY
load_pack = base.load_pack
parse_candidate = base.parse_candidate
check_value = base.check_value
grade_fields = base.grade_fields
grade_record = base.grade_record
summarize = base.summarize

if __name__ == "__main__":
    base.main()
