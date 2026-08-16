import json
from pathlib import Path

from run_semantic_smoke import (
    INTERACTIONS_ENDPOINT,
    extract_interaction_output_text,
    interaction_payload,
    response_format,
)

HERE = Path(__file__).resolve().parent


def cases():
    return json.loads((HERE / "semantic_cases.json").read_text(encoding="utf-8"))


def test_frozen_case_manifest_shape():
    loaded = cases()
    assert [c["id"] for c in loaded] == ["RES-RCE-S1", "RES-RCE-S2"]
    for case in loaded:
        assert case["facts"]
        assert case["required_decision"]
        assert case["critical_rationale"]


def test_case_1_fails_closed_under_unknown_dependence_and_reserve_pressure():
    case = cases()[0]
    assert case["required_decision"] == "ESCALATE_OR_DEFER"
    assert {"unknown_dependence_not_independence", "protected_reserve", "no_false_support"}.issubset(case["critical_rationale"])


def test_case_2_direct_primary_bypasses_discovery_quota():
    case = cases()[1]
    assert case["required_decision"] == "DIRECT_PRIMARY_INSPECTION"
    assert {"known_official_url", "cheapest_sufficient_eligible_route", "no_blind_retry"}.issubset(case["critical_rationale"])


def test_interactions_payload_uses_top_level_structured_response_format():
    fmt = response_format()
    assert INTERACTIONS_ENDPOINT.endswith("/v1beta/interactions")
    assert fmt["type"] == "text"
    assert fmt["mime_type"] == "application/json"
    schema = fmt["schema"]
    assert schema["type"] == "object"
    assert schema["required"] == ["decision", "rationale_codes"]
    assert schema["additionalProperties"] is False

    payload = interaction_payload(cases()[0], "frozen", "gemini-3.6-flash")
    assert payload["model"] == "gemini-3.6-flash"
    assert payload["response_format"] == fmt
    assert payload["store"] is False
    assert "generationConfig" not in payload


def test_interactions_output_requires_observable_model_output_step():
    raw = {
        "steps": [
            {"type": "user_input", "content": [{"type": "text", "text": "input"}]},
            {"type": "model_output", "content": [{"type": "text", "text": '{"decision":"SUPPORTED","rationale_codes":["citation_entailment"]}'}]},
        ]
    }
    text = extract_interaction_output_text(raw)
    assert json.loads(text)["decision"] == "SUPPORTED"
