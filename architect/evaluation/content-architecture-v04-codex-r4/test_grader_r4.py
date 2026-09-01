#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("grader_r4", HERE / "grader_r4.py")
g = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(g)


def fixture_pack():
    fid = "T1"
    return {
        "gate_id": g.GATE_ID,
        "candidate_sha": g.CANDIDATE_SHA,
        "fixtures": [{"fixture_id": fid, "family": "F1", "trial_count": 1}],
        "contracts": {fid: {"decision": {"type": "string", "allowed": ["PROCEED", "BLOCK"]}, "bounded": {"type": "boolean"}}},
        "expectations": {fid: {"family": "F1", "decision": ["PROCEED"], "bounded": True}},
    }


def record(output: str):
    return {"fixture_id": "T1", "trial": 1, "trial_count": 1, "gate_id": g.GATE_ID, "candidate_sha": g.CANDIDATE_SHA, "terminal_status": "COMPLETED", "final_response": output}


def main():
    pack = fixture_pack()
    good = g.grade_record(record('{"decision":"PROCEED","bounded":true}'), pack)
    assert good["mechanical_pass"] and good["pass"] and not good["p0"]

    wrong_but_valid = g.grade_record(record('{"decision":"BLOCK","bounded":true}'), pack)
    assert wrong_but_valid["mechanical_pass"] and not wrong_but_valid["pass"]
    assert not wrong_but_valid["mechanical_failures"] and wrong_but_valid["decision_failures"]

    hidden_synonym = g.grade_record(record('{"decision":"GO_AHEAD","bounded":true}'), pack)
    assert not hidden_synonym["mechanical_pass"] and not hidden_synonym["pass"]

    malformed = g.grade_record(record('not-json'), pack)
    assert not malformed["mechanical_pass"] and not malformed["pass"]

    summary = g.summarize([good], [record('{"decision":"PROCEED","bounded":true}')], pack)
    assert summary["records_complete"]
    assert summary["deterministic_invariant_pass_rate"] == 1.0
    print("r4 grader calibration: PASS")


if __name__ == "__main__":
    main()
