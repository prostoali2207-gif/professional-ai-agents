from probe_gemini_models import eligible_generate_content_models, normalize_model


def test_probe_filters_to_live_gemini_generate_content_capability():
    models = [
        {"name": "models/gemini-3.6-flash", "supportedGenerationMethods": ["generateContent", "countTokens"]},
        {"name": "models/gemini-3.5-flash", "supportedGenerationMethods": ["countTokens"]},
        {"name": "models/embedding-001", "supportedGenerationMethods": ["embedContent"]},
    ]
    rows = eligible_generate_content_models(models)
    assert [row["name"] for row in rows] == ["models/gemini-3.6-flash"]


def test_probe_does_not_infer_capability_from_model_name():
    rows = eligible_generate_content_models([
        {"name": "models/gemini-future-flash", "supportedGenerationMethods": []}
    ])
    assert rows == []


def test_probe_preserves_provider_capability_evidence():
    row = normalize_model({
        "name": "models/gemini-x",
        "displayName": "Gemini X",
        "supportedGenerationMethods": ["countTokens", "generateContent"],
        "inputTokenLimit": 100,
        "outputTokenLimit": 20,
    })
    assert row["supportedGenerationMethods"] == ["countTokens", "generateContent"]
    assert row["inputTokenLimit"] == 100
    assert row["outputTokenLimit"] == 20
