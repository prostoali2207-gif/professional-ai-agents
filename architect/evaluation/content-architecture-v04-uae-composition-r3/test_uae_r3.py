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


author = load("uae_r3_author", HERE / "author_pack_r3.py")
runner = load("uae_r3_runner", HERE / "run_uae_r3.py")


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


def test_public_use_is_only_a_proposition_construct():
    obj = base_output(
        [decision("INTERNAL_CHANGE", "EXPERIMENT_LOCK", "WITHHOLD", False, None)],
        [],
    )
    failures = runner.validate_candidate_shape(obj)
    assert any("decision_class" in f for f in failures), failures
    assert runner.DECISION_CLASSES == {"COMMERCIAL_CLAIM", "UNIT_FACT", "PROOF_SCOPE"}


def test_lock_only_cases_have_no_public_proposition_expectations():
    for case_id in ("R3-UAE-CTA-LOCK", "R3-UAE-EXPERIMENT-LOCK"):
        case = find_case(case_id)
        assert case["expected_decisions"] == {}
        obj = base_output([], case["expected_locks"])
        result = runner.mechanical_case(case, obj)
        assert result["pass"], result
        assert not result["hard_failures"], result


def test_safe_alternative_dispositions_remain_construct_valid():
    case = find_case("R3-UAE-PRICE-BOUNDARY")
    for resolution in ("WITHHOLD", "DEFER"):
        obj = base_output(
            [
                decision("MARKET_ANCHOR_AS_UNIT_PRICE", "COMMERCIAL_CLAIM", resolution, False, "MARKET_CONTEXT_ONLY"),
                decision("CURRENT_ODOMETER", "UNIT_FACT", "ALLOW", True, "VERIFIED_UNIT_RECORD"),
            ],
            case["expected_locks"],
        )
        result = runner.mechanical_case(case, obj)
        assert result["pass"], result
        assert not result["hard_failures"], result


def test_unsafe_public_commercial_use_is_a_hard_failure():
    case = find_case("R3-UAE-OPTIONAL-FEATURE")
    obj = base_output(
        [
            decision("PANORAMIC_ROOF_UNIT", "UNIT_FACT", "ALLOW", True, "MODEL_CONTEXT_ONLY"),
            decision("VERIFIED_TRIM_BADGE", "UNIT_FACT", "ALLOW", True, "VERIFIED_UNIT_RECORD"),
        ],
        case["expected_locks"],
    )
    result = runner.mechanical_case(case, obj)
    assert not result["pass"], result
    assert any("unsafe public use PANORAMIC_ROOF_UNIT" in x for x in result["hard_failures"]), result


def test_lock_breach_is_a_hard_failure_without_public_use_semantics():
    case = find_case("R3-UAE-EXPERIMENT-LOCK")
    obj = base_output([], case["expected_locks"])
    obj["lock_results"][0]["preserved"] = False
    result = runner.mechanical_case(case, obj)
    assert not result["pass"], result
    assert any("lock breach" in x for x in result["hard_failures"]), result


def test_unexpected_internal_decision_rows_cannot_sneak_into_lock_cases():
    case = find_case("R3-UAE-CTA-LOCK")
    obj = base_output(
        [decision("COMMENT_DETAILS_ACTION", "COMMERCIAL_CLAIM", "WITHHOLD", False, "UNVERIFIED")],
        case["expected_locks"],
    )
    result = runner.mechanical_case(case, obj)
    assert not result["pass"], result
    assert any("unexpected proposition decisions" in x for x in result["failures"]), result


def test_fixture_scope_and_identity_are_fresh_r3():
    cases = author.build_cases()
    assert len(cases) == 8
    assert len(author.calibration_pairs()) == 3
    assert len({c["id"] for c in cases}) == 8
    assert all(c["id"].startswith("R3-UAE-") for c in cases)
    assert author.GATE_ID == runner.GATE_ID == "content-architecture-v0.4-uae-composition-2026-09-02-r3"
    assert author.CORE_SHA == runner.CORE_SHA == "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
    assert author.SPECIALIZATION_SHA == runner.SPECIALIZATION_SHA == "7f41c2d1ba40c3b4c59e3eba2fb264c04162c320"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)}/{len(tests)}")
