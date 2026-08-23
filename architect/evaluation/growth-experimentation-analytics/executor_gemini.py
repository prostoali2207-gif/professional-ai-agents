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

ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
DEFAULT_MODEL = "gemini-3.5-flash-lite"


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


def extract_text(raw: dict[str, Any]) -> str:
    if isinstance(raw.get("output_text"), str):
        return raw["output_text"].strip()
    for step in reversed(raw.get("steps") or []):
        if not isinstance(step, dict) or step.get("type") != "model_output":
            continue
        content = step.get("content")
        if isinstance(content, str):
            return content.strip()
        for item in content or []:
            if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str):
                return item["text"].strip()
    fail("Gemini Interactions returned no observable text output")


def api_call(candidate_text: str, task: dict[str, Any]) -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    model = os.environ.get("ANALYTICS_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    if not key:
        fail("GEMINI_API_KEY is required")

    schema = Path("architect/evaluation/growth-experimentation-analytics/schemas/result.schema.json").read_text(encoding="utf-8")
    system_instruction = (
        "You are the exact frozen Growth Experimentation & Measurement candidate under behavioral evaluation. "
        "Apply the candidate instructions exactly. Preserve causal-claim safeguards and registered stopping rules. "
        "Return only one JSON object matching the supplied result schema; no Markdown or commentary.\n\n"
        "CANDIDATE INSTRUCTIONS:\n" + candidate_text + "\n\nRESULT SCHEMA:\n" + schema
    )
    payload = {
        "model": model,
        "input": json.dumps(task, ensure_ascii=False),
        "system_instruction": system_instruction,
        "store": False,
        "generation_config": {"thinking_level": os.environ.get("GEMINI_THINKING_LEVEL", "medium")},
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    try:
        with urllib.request.urlopen(req, timeout=int(os.environ.get("ANALYTICS_MODEL_TIMEOUT_SECONDS", "180"))) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        fail(f"Gemini API HTTP {exc.code}: {body[-2000:]}")
    except Exception as exc:
        fail(f"Gemini API failure: {exc}")
    if not isinstance(raw, dict):
        fail("Gemini Interactions returned non-object payload")
    return extract_text(raw)


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
    result = parse_json_object(api_call(candidate_text, task))
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
