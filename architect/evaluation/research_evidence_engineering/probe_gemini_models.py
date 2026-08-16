#!/usr/bin/env python3
"""Non-generative Gemini provider-state probe for the Research + RCE gate.

Uses models.list only. It consumes no generateContent request and does not choose a
semantic winner. The resulting evidence is used to avoid stale model-memory and
blind retries before an evaluator explicitly selects an eligible model.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / ".tmp/research-rce-model-probe"
BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def normalize_model(model: dict) -> dict:
    return {
        "name": model.get("name"),
        "displayName": model.get("displayName"),
        "supportedGenerationMethods": sorted(model.get("supportedGenerationMethods") or []),
        "inputTokenLimit": model.get("inputTokenLimit"),
        "outputTokenLimit": model.get("outputTokenLimit"),
    }


def eligible_generate_content_models(models: list[dict]) -> list[dict]:
    rows = []
    for model in models:
        name = str(model.get("name") or "")
        methods = set(model.get("supportedGenerationMethods") or [])
        if name.startswith("models/gemini-") and "generateContent" in methods:
            rows.append(normalize_model(model))
    return sorted(rows, key=lambda row: str(row.get("name")))


def list_models(key: str) -> list[dict]:
    models: list[dict] = []
    page_token: str | None = None
    while True:
        query = {"key": key, "pageSize": "1000"}
        if page_token:
            query["pageToken"] = page_token
        url = BASE + "?" + urllib.parse.urlencode(query)
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as response:
            payload = json.loads(response.read().decode())
        models.extend(payload.get("models") or [])
        page_token = payload.get("nextPageToken")
        if not page_token:
            return models


def main() -> int:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("GEMINI_API_KEY is not configured; no provider probe attempted.")
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        raw_models = list_models(key)
        eligible = eligible_generate_content_models(raw_models)
        record = {
            "status": "PASS",
            "probe": "models.list",
            "generation_calls": 0,
            "eligible_generate_content_models": eligible,
            "observed_names": [row["name"] for row in eligible],
        }
        code = 0
    except urllib.error.HTTPError as exc:
        record = {
            "status": "INFRA_FAILURE",
            "probe": "models.list",
            "generation_calls": 0,
            "http_status": exc.code,
            "error": exc.read().decode(errors="replace"),
        }
        code = 1
    except Exception as exc:
        record = {
            "status": "INFRA_FAILURE",
            "probe": "models.list",
            "generation_calls": 0,
            "error": repr(exc),
        }
        code = 1
    (OUT / "models-list.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
