#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("universal_r1", HERE / "run_universal_r1.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)

valid = {
    "status": "READY_WITH_BOUNDS",
    "attention_contract": {"opening_job":"establish relevance","viewer_question_or_tension":"what changes","payoff_obligation":"resolve","evidence_dependency":[]},
    "block_sequence": [{"block_id":"B1","job":"open","information_required":[],"proof_requirement":"none","position_band":"opening","transition_job":"move to proof"}],
    "proof_architecture": [],
    "pacing": {"mode":"macro","macro_zones":["opening"],"notes":"bounded"},
    "creator_handoff": {"must_preserve":[],"bounded":[],"may_choose":[],"must_escalate":[]},
    "structural_observability": {"hook_family_or_job":"relevance","block_order":["B1"],"proof_positions":[],"tested_or_locked_variables":[]},
    "boundary_notes": [],
}
assert mod.mechanical_contract(valid) == []
invalid = dict(valid); invalid["status"] = "READY"
assert "status invalid" in mod.mechanical_contract(invalid)
assert mod.validate_assessment({"hard_failures":[],"scores":{"brief_fidelity":2},"release_recommendation":"PASS"}, ["brief_fidelity"]) == []
assert mod.validate_assessment({"hard_failures":[],"scores":{"brief_fidelity":4},"release_recommendation":"PASS"}, ["brief_fidelity"])
print("universal r1 deterministic tests: PASS")
