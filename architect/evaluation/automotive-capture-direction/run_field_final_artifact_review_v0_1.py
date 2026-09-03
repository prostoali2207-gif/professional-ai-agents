#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PREREG = HERE / "field-final-artifact-prerun-v0.1.json"
CANDIDATE_COMMIT = "6e34be04f1bc6912c95e5f6c0b34d1ccf9ccf13c"
CANDIDATE_PATH = "architect/evaluation/automotive-capture-direction/professional-model-candidate-v0.1.md"
CANDIDATE_BLOB = "6824ba3256ab6f3b51c5596f6fd6e42e013937f7"
HOST_MODEL = "architect/library/cores/social-content-creative/0.1.0/professional-model.md"
HOST_MANIFEST = "architect/library/cores/social-content-creative/0.1.0/manifest.json"
HOST_DIGEST = "sha256:ce5f537d336e6a6396f47c1ae492a687c4dc4b30ade8ab37bb4abb94d6251c0f"
MODEL = "gemini-3.5-flash-lite"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"


def git_show(commit: str, path: str) -> str:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT, text=True)


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_and_verify(prereg: dict) -> tuple[str, str]:
    if prereg.get("status") != "FROZEN_READY":
        raise RuntimeError("prerun is not frozen-ready")
    if prereg.get("cycle_id") != "automotive-capture-direction-human-field-final-review-v0.1":
        raise RuntimeError("cycle mismatch")
    c = prereg.get("candidate") or {}
    if c != {
        "commit": CANDIDATE_COMMIT,
        "blob": CANDIDATE_BLOB,
        "host_digest": HOST_DIGEST,
        "mutation_allowed": False,
    }:
        raise RuntimeError("candidate identity mismatch")
    r = prereg.get("runtime") or {}
    if r.get("provider") != "gemini-interactions-api" or r.get("model") != MODEL or r.get("candidate_calls_max") != 1 or r.get("judge_calls") != 0 or r.get("scored_retries") != 0:
        raise RuntimeError("runtime contract mismatch")
    blob = subprocess.check_output(["git", "rev-parse", f"{CANDIDATE_COMMIT}:{CANDIDATE_PATH}"], cwd=ROOT, text=True).strip()
    if blob != CANDIDATE_BLOB:
        raise RuntimeError("frozen candidate blob mismatch")
    manifest = json.loads(git_show(CANDIDATE_COMMIT, HOST_MANIFEST))
    canonical = "".join(
        f"{p}:{subprocess.check_output(['git','rev-parse',f'{CANDIDATE_COMMIT}:{p}'],cwd=ROOT,text=True).strip()}\n"
        for p in manifest["artifact"]["paths"]
    )
    digest = "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()
    if digest != HOST_DIGEST or digest != manifest["artifact"]["content_digest"]:
        raise RuntimeError("qualified host digest mismatch")
    return git_show(CANDIDATE_COMMIT, HOST_MODEL), git_show(CANDIDATE_COMMIT, CANDIDATE_PATH)


def extract_text(raw: dict) -> str:
    if isinstance(raw.get("output_text"), str):
        return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if not isinstance(step, dict) or step.get("type") != "model_output":
            continue
        content = step.get("content")
        if isinstance(content, str):
            return content
        for item in content or []:
            if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str):
                return item["text"]
    raise RuntimeError("provider response contains no observable text")


def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = "\n".join(text.splitlines()[1:-1]).strip()
    a, b = text.find("{"), text.rfind("}")
    if a >= 0 and b > a:
        text = text[a:b+1]
    value = json.loads(text)
    if not isinstance(value, dict):
        raise RuntimeError("candidate output is not JSON object")
    return value


def validate_output(value: dict, prereg: dict) -> None:
    if set(value) != {"artifacts", "handoff_notes", "truth_safety_constraints"}:
        raise RuntimeError("output top-level schema mismatch")
    rows = value.get("artifacts")
    if not isinstance(rows, list) or len(rows) != 3:
        raise RuntimeError("artifacts must contain exactly 3 rows")
    expected_ids = prereg["output_contract"]["artifact_ids_exact"]
    allowed = set(prereg["output_contract"]["decision_enum"])
    required = {
        "artifact_id",
        "decision",
        "visible_observation",
        "dominant_issue",
        "prioritized_correction",
        "preserve",
        "acceptance_cue",
    }
    seen = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != required:
            raise RuntimeError("artifact row schema mismatch")
        if row["decision"] not in allowed:
            raise RuntimeError("invalid decision")
        for k in required - {"artifact_id", "decision"}:
            if not isinstance(row[k], str):
                raise RuntimeError(f"{k} must be string")
        seen.append(row["artifact_id"])
    if seen != expected_ids:
        raise RuntimeError(f"artifact order/id mismatch: {seen}")
    if not isinstance(value["handoff_notes"], str) or not isinstance(value["truth_safety_constraints"], str):
        raise RuntimeError("overall fields must be strings")


def main() -> int:
    prereg = json.loads(PREREG.read_text())
    host, extension = load_and_verify(prereg)
    media_root = Path(os.environ["AUTOMOTIVE_CAPTURE_FIELD_MEDIA_ROOT"])
    media_inputs = []
    observed_media = []
    for spec in prereg["media"]:
        path = media_root / spec["local_name"]
        if not path.is_file():
            raise RuntimeError(f"missing media: {spec['local_name']}")
        actual = sha256(path)
        if actual != spec["sha256"]:
            raise RuntimeError(f"media digest mismatch for {spec['id']}: {actual}")
        media_inputs.append({
            "type": spec["media_type"],
            "data": base64.b64encode(path.read_bytes()).decode("ascii"),
            "mime_type": spec["mime_type"],
        })
        observed_media.append({"id": spec["id"], "sha256": actual, "bytes": path.stat().st_size})

    task = {
        "vehicle": prereg["vehicle"],
        "scope": "Directly inspect only the three supplied final artifacts from the real human field test. Do not infer unseen condition, device settings, permissions, history, price, or commercial facts.",
        "artifacts": [{"id": m["id"], "function": m["function"]} for m in prereg["media"]],
        "decision_rule": "For each artifact choose ACCEPT if it already satisfies its stated source function; RESHOOT only for a visible material capture problem with one prioritized physically executable correction; BLOCK only for a truthful material limitation that cannot be resolved within the declared phone-only stationary-vehicle setup.",
        "output": {
            "exact_json_shape": {
                "artifacts": [
                    {
                        "artifact_id": "F1_HERO_STILL_FINAL",
                        "decision": "ACCEPT|RESHOOT|BLOCK",
                        "visible_observation": "string",
                        "dominant_issue": "string; empty if none material",
                        "prioritized_correction": "string; empty if ACCEPT",
                        "preserve": "string",
                        "acceptance_cue": "string",
                    }
                ],
                "handoff_notes": "string",
                "truth_safety_constraints": "string",
            },
            "requirements": "Return all three artifact rows in the preregistered order and no extra keys."
        }
    }
    system = (
        "Act as the exact qualified Social Content Creative host plus the frozen Automotive Commercial Capture Direction extension below. "
        "This is an artifact-first field review. You have direct media access in this request. Base every artifact claim on what is actually visible. "
        "Do not infer capture device settings, unseen condition, accident history, unsafe behavior, permissions, price, availability, finance, warranty or other commercial facts. "
        "Use restraint: accept good source media instead of overcorrecting. For any RESHOOT, identify the visible causal problem, change one prioritized variable, preserve what is already good, and give an observable acceptance cue. "
        "Return JSON only.\n\n--- QUALIFIED HOST ---\n" + host + "\n\n--- FROZEN CAPTURE EXTENSION ---\n" + extension
    )
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")
    body = {
        "model": MODEL,
        "system_instruction": system,
        "input": media_inputs + [{"type": "text", "text": json.dumps(task, ensure_ascii=False)}],
        "store": False,
        "generation_config": {"thinking_level": "medium"},
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body, ensure_ascii=False).encode(),
        method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            raw = json.loads(r.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"provider HTTP {exc.code}: {exc.read().decode(errors='replace')[:1600]}") from exc
    output = extract_json(extract_text(raw))
    validate_output(output, prereg)
    report = {
        "schema_version": "1.0.0",
        "cycle_id": prereg["cycle_id"],
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_blob": CANDIDATE_BLOB,
        "host_digest": HOST_DIGEST,
        "runtime": {"provider": "gemini-interactions-api", "model": MODEL, "candidate_calls": 1, "judge_calls": 0, "scored_retries": 0},
        "observed_media": observed_media,
        "candidate_review": output,
        "interaction_id": raw.get("id"),
        "usage": raw.get("usage") or raw.get("usageMetadata"),
        "release_verdict_authorized": False,
        "release_boundary": prereg["release_boundary"],
    }
    out = Path(os.environ.get("AUTOMOTIVE_CAPTURE_FIELD_REVIEW_REPORT", "/tmp/automotive-capture-field-final-review.json"))
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in {"interaction_id", "usage"}}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"cycle_id": "automotive-capture-direction-human-field-final-review-v0.1", "runtime_error": str(exc)}, ensure_ascii=False))
        raise SystemExit(2)
