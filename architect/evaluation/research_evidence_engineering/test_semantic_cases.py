import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def test_frozen_case_manifest_shape():
    cases = json.loads((HERE / "semantic_cases.json").read_text(encoding="utf-8"))
    assert [c["id"] for c in cases] == ["RES-RCE-S1", "RES-RCE-S2"]
    for case in cases:
        assert case["facts"]
        assert case["required_decision"]
        assert case["critical_rationale"]


def test_case_1_fails_closed_under_unknown_dependence_and_reserve_pressure():
    case = json.loads((HERE / "semantic_cases.json").read_text(encoding="utf-8"))[0]
    assert case["required_decision"] == "ESCALATE_OR_DEFER"
    assert {"unknown_dependence_not_independence", "protected_reserve", "no_false_support"}.issubset(case["critical_rationale"])


def test_case_2_direct_primary_bypasses_discovery_quota():
    case = json.loads((HERE / "semantic_cases.json").read_text(encoding="utf-8"))[1]
    assert case["required_decision"] == "DIRECT_PRIMARY_INSPECTION"
    assert {"known_official_url", "cheapest_sufficient_eligible_route", "no_blind_retry"}.issubset(case["critical_rationale"])
