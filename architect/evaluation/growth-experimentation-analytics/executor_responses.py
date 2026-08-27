#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, NoReturn


LEGACY_OUTPUT_CONTRACT = "architect/evaluation/growth-experimentation-analytics/schemas/result.schema.json"


def fail(message: str) -> NoReturn:
    print(f"executor_error: {message}", file=sys.stderr)
    raise SystemExit(2)


def git_blob_sha(path: str) -> str:
    completed = subprocess.run(
        ["git", "hash-object", path],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"cannot hash candidate component {path}: {completed.stderr.strip()}")
    return completed.stdout.strip()


def load_candidate(manifest: dict[str, Any]) -> str:
    assembly = manifest.get("assembly")
    if not isinstance(assembly, list) or not assembly:
        fail("candidate manifest assembly missing")
    chunks: list[str] = []
    for component in assembly:
        if not isinstance(component, dict):
            fail("invalid candidate component")
        path = component.get("path")
        expected = component.get("git_blob_sha")
        if not isinstance(path, str) or not isinstance(expected, str):
            fail("candidate component path/hash missing")
        actual = git_blob_sha(path)
        if actual != expected:
            fail(f"candidate component hash mismatch for {path}: {actual} != {expected}")
        chunks.append(Path(path).read_text(encoding="utf-8"))
    return "\n\n".join(chunks)


def load_output_contract(manifest: dict[str, Any]) -> str:
    """Read the output contract bound by the frozen manifest.

    v0.3 and earlier froze only the markdown components while the executor injected
    schemas/result.schema.json from a hardcoded path, so a contract edit could change
    candidate behavior without changing the frozen digest. v0.4 manifests bind the
    contract; its hash is verified like any other frozen component.
    """
    path = manifest.get("output_contract_path")
    if not isinstance(path, str) or not path:
        return Path(LEGACY_OUTPUT_CONTRACT).read_text(encoding="utf-8")
    expected = manifest.get("output_contract_git_blob_sha")
    if isinstance(expected, str) and expected:
        actual = git_blob_sha(path)
        if actual != expected:
            fail(f"output contract hash mismatch for {path}: {actual} != {expected}")
    return Path(path).read_text(encoding="utf-8")


def extract_text(payload: dict[str, Any]) -> str:
    texts: list[str] = []
    for item in payload.get("output") or []:
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for part in item.get("content") or []:
            if isinstance(part, dict) and part.get("type") == "output_text" and isinstance(part.get("text"), str):
                texts.append(part["text"])
    if not texts:
        fail("Responses API returned no output text")
    return "\n".join(texts).strip()


def api_call(candidate_text: str, schema: str, task: dict[str, Any]) -> str:
    key = os.environ.get("OPENAI_API_KEY")
    model = os.environ.get("ANALYTICS_MODEL", "gpt-5.6-terra")
    if not key:
        fail("OPENAI_API_KEY is required")
    developer = (
        "You are the exact frozen Growth Experimentation & Measurement candidate under behavioral evaluation. "
        "Apply the candidate instructions exactly. Preserve causal-claim safeguards and registered stopping rules. "
        "Return only one JSON object matching the supplied result schema; no Markdown or commentary.\n\n"
        "CANDIDATE INSTRUCTIONS:\n" + candidate_text + "\n\nRESULT SCHEMA:\n" + schema
    )
    body = {
        "model": model,
        "store": False,
        "input": [
            {"role": "developer", "content": [{"type": "input_text", "text": developer}]},
            {"role": "user", "content": [{"type": "input_text", "text": json.dumps(task, ensure_ascii=False)}]},
        ],
    }
    request = urllib.request.Request(
        os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/") + "/responses",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=int(os.environ.get("ANALYTICS_MODEL_TIMEOUT_SECONDS", "180"))) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        fail(f"model API HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[-2000:]}")
    except Exception as exc:
        fail(f"model API failure: {exc}")
    if not isinstance(payload, dict):
        fail("Responses API returned non-object payload")
    return extract_text(payload)


def parse_json_object(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            fail("model returned non-JSON output")
        try:
            value = json.loads(text[start:end + 1])
        except json.JSONDecodeError as exc:
            fail(f"model returned invalid JSON: {exc}")
    if not isinstance(value, dict):
        fail("model result must be a JSON object")
    return value


def main() -> int:
    envelope = json.load(sys.stdin)
    if not isinstance(envelope, dict) or envelope.get("protocol") != "growth-experimentation-analytics-candidate-v1":
        fail("invalid protocol")
    manifest = envelope.get("candidate")
    task = envelope.get("task")
    if not isinstance(manifest, dict) or not isinstance(task, dict):
        fail("candidate manifest or task missing")
    candidate_text = load_candidate(manifest)
    result = parse_json_object(api_call(candidate_text, load_output_contract(manifest), task))
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
