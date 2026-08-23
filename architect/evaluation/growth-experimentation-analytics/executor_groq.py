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


def fail(message: str) -> NoReturn:
    print(f"executor_error: {message}", file=sys.stderr)
    raise SystemExit(2)


def git_blob_sha(path: str) -> str:
    completed = subprocess.run(
        ["git", "hash-object", path], text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
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


def api_call(candidate_text: str, task: dict[str, Any]) -> str:
    key = os.environ.get("GROQ_API_KEY")
    model = os.environ.get("ANALYTICS_MODEL", "qwen/qwen3.6-27b")
    if not key:
        fail("GROQ_API_KEY is required")

    schema = Path(
        "architect/evaluation/growth-experimentation-analytics/schemas/result.schema.json"
    ).read_text(encoding="utf-8")

    system = (
        "You are the exact frozen Growth Experimentation & Measurement candidate under behavioral evaluation. "
        "Apply the candidate instructions exactly. Preserve causal-claim safeguards and registered stopping rules. "
        "Return only one JSON object matching the supplied result schema; no Markdown or commentary.\n\n"
        "CANDIDATE INSTRUCTIONS:\n" + candidate_text + "\n\nRESULT SCHEMA:\n" + schema
    )

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(task, ensure_ascii=False)},
        ],
        "response_format": {"type": "json_object"},
        "reasoning_format": "hidden",
        "reasoning_effort": "default",
        "temperature": 0,
    }

    request = urllib.request.Request(
        os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1").rstrip("/") + "/chat/completions",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "professional-ai-agents-groq-executor/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(
            request, timeout=int(os.environ.get("ANALYTICS_MODEL_TIMEOUT_SECONDS", "180"))
        ) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        fail(f"Groq API HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[-2000:]}")
    except Exception as exc:
        fail(f"Groq API failure: {exc}")

    try:
        text = payload["choices"][0]["message"]["content"]
    except Exception:
        fail("Groq API returned no message content")
    if not isinstance(text, str) or not text.strip():
        fail("Groq API returned empty message content")
    return text.strip()


def parse_json_object(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
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
