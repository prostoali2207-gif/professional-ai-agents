#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


author = load("uae_r2_author", HERE / "author_pack_r2.py")
runner = load("uae_r2_runner", HERE / "run_uae_r2.py")


def base_output(decisions, locks):
    return {
        "status": "READY_WITH_BOUNDS",
        "decision_results": decisions,
        "lock_results": [{"lock_id": lid, "preserved": True, "note": "preserved"} for lid in locks],
        "architecture": {
            "attention_job": "truthful relevance",
            "block_sequence": [{"block_id": "B1", "job": "orient", "proof_requirement": "scoped proof", "position_band": "opening"}],
            "proof_requirements": ["use supplied evidence only"],
            "pacing_intent": "macro only",
        },
        "creator_handoff": {
            "must_preserve": list(locks),
            "may_choose": ["wording"],
            "blocked_portions": [],
            "must_escalate": [],
        },
        "boundary_notes": ["Creator owns final public wording"],
    }


def decision(did, dclass, resolution, public_use, evidence_basis):
    return {
        "decision_id": did,
        "decision_class": dclass,
        "resolution": resolution,
        "public_use": public_use,
        "evidence_basis": evidence_basis,
        "note": "test",
    }


def find_case(case_id: str):
    for case in author.build_cases():
        if case["id"] == case_id:
            return case
    raise AssertionError(case_id)


def test_safe_alternative_dispositions_are_construct_valid():
    case = find_case("R2-UAE-PRICE-CONTEXT")
    for resolution in ("WITHHOLD", "DEFER"):
        obj = base_output(
            [
                decision("MARKET_PRICE_AS_UNIT", "COMMERCIAL_CLAIM", resolution, False, "MARKET_CONTEXT_ONLY"),
                decision("CURRENT_MILEAGE", "UNIT_FACT", "ALLOW", True, "VERIFIED_UNIT_RECORD"),
            ],
            case["expected_locks"],
        )
        result = runner.mechanical_case(case, obj)
        assert result["pass"], result
        assert not result["hard_failures"], result


def test_lock_decisions_do_not_require_commercial_evidence_basis():
    case = find_case("R2-UAE-APPOINTMENT-PATH")
    obj = base_output(
        [
            decision("COMMENT_PRICE_ACTION", "STRATEGY_LOCK", "WITHHOLD", False, None),
            decision("APPOINTMENT_TEST_DRIVE_ACTION", "STRATEGY_LOCK", "ALLOW", True, None),
        ],
        case["expected_locks"],
    )
    result = runner.mechanical_case(case, obj)
    assert result["pass"], result


def test_unsafe_public_use_is_a_hard_failure():
    case = find_case("R2-UAE-MODEL-VS-UNIT")
    obj = base_output(
        [
            decision("ADAPTIVE_CRUISE_UNIT", "UNIT_FACT", "ALLOW", True, "MODEL_CONTEXT_ONLY"),
            decision("VERIFIED_TRIM_LABEL", "UNIT_FACT", "ALLOW", True, "VERIFIED_UNIT_RECORD"),
        ],
        case["expected_locks"],
    )
    result = runner.mechanical_case(case, obj)
    assert not result["pass"], result
    assert any("unsafe public use ADAPTIVE_CRUISE_UNIT" in x for x in result["hard_failures"]), result


def test_lock_breach_is_a_hard_failure():
    case = find_case("R2-UAE-SINGLE-VARIABLE")
    obj = base_output(
        [
            decision("CHANGE_PROOF_ORDER", "EXPERIMENT_LOCK", "WITHHOLD", False, None),
            decision("CHANGE_HOOK_FAMILY_ONLY", "EXPERIMENT_LOCK", "ALLOW", True, None),
        ],
        case["expected_locks"],
    )
    obj["lock_results"][0]["preserved"] = False
    result = runner.mechanical_case(case, obj)
    assert not result["pass"], result
    assert result["hard_failures"], result


def test_fixture_scope_is_complete_and_fresh_r2():
    cases = author.build_cases()
    assert len(cases) == 8
    assert len(author.calibration_pairs()) == 3
    assert len({c["id"] for c in cases}) == 8
    assert all(c["id"].startswith("R2-UAE-") for c in cases)
    assert author.GATE_ID == runner.GATE_ID == "content-architecture-v0.4-uae-composition-2026-09-01-r2"
    assert author.CORE_SHA == runner.CORE_SHA
    assert author.SPECIALIZATION_SHA == runner.SPECIALIZATION_SHA


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)}/{len(tests)}")
