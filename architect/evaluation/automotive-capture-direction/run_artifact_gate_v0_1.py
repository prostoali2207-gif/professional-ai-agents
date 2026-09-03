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
PREREG = HERE / "artifact-preregistration-v0.1.json"
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


def verify_identity(prereg: dict) -> tuple[str, str]:
    if prereg.get("status") != "FROZEN_READY" or prereg.get("cycle_id") != "automotive-capture-direction-artifact-v0.1":
        raise RuntimeError("artifact preregistration is not frozen-ready")
    c = prereg.get("candidate") or {}
    if c.get("commit") != CANDIDATE_COMMIT or c.get("blob") != CANDIDATE_BLOB or c.get("host_digest") != HOST_DIGEST or c.get("mutation_allowed") is not False:
        raise RuntimeError("candidate identity mismatch")
    r = prereg.get("runtime") or {}
    if r.get("model") != MODEL or r.get("scored_retries") != 0 or r.get("candidate_calls_max") != 2:
        raise RuntimeError("artifact runtime mismatch")
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
        raise RuntimeError("candidate output is not a JSON object")
    return value


def invoke(host: str, extension: str, media_path: Path, mime_type: str, media_type: str, task: dict) -> tuple[dict, dict]:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")
    system = (
        "Act as the exact qualified Social Content Creative host plus the frozen Automotive Commercial Capture Direction extension below. "
        "Evaluate only the supplied media and stated sales-content function. Do not use tools or external facts. "
        "Do not infer capture device, unseen condition, unsafe behavior, or production circumstances that are not visible. "
        "Choose exactly one supplied option for every question and return JSON only in this shape: "
        "{\"answers\":[{\"id\":\"...\",\"choice\":\"A|B|C\"},...]}. Return every ID once, no extra keys.\n\n"
        "--- QUALIFIED HOST ---\n" + host + "\n\n--- FROZEN CAPTURE EXTENSION ---\n" + extension
    )
    media = {
        "type": media_type,
        "data": base64.b64encode(media_path.read_bytes()).decode("ascii"),
        "mime_type": mime_type,
    }
    body = {
        "model": MODEL,
        "system_instruction": system,
        "input": [media, {"type": "text", "text": json.dumps(task, ensure_ascii=False)}],
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
        with urllib.request.urlopen(req, timeout=240) as r:
            raw = json.loads(r.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"provider HTTP {exc.code}: {exc.read().decode(errors='replace')[:1200]}") from exc
    return extract_json(extract_text(raw)), {"interaction_id": raw.get("id"), "usage": raw.get("usage") or raw.get("usageMetadata")}


def grade(result: dict, case: dict) -> list[dict]:
    answers = result.get("answers")
    if not isinstance(answers, list):
        raise RuntimeError("answers list missing")
    observed: dict[str, str] = {}
    for row in answers:
        if not isinstance(row, dict) or set(row) != {"id", "choice"}:
            raise RuntimeError("answer row schema invalid")
        cid, choice = row.get("id"), row.get("choice")
        if not isinstance(cid, str) or choice not in {"A", "B", "C"} or cid in observed:
            raise RuntimeError("answer id/choice invalid or duplicated")
        observed[cid] = choice
    expected = case["expected"]
    if set(observed) != set(expected):
        raise RuntimeError("answer ID set mismatch")
    return [{"id": cid, "pass": observed[cid] == expected[cid]} for cid in sorted(expected)]


def main() -> int:
    prereg = json.loads(PREREG.read_text())
    host, extension = verify_identity(prereg)
    media_root = Path(os.environ.get("AUTOMOTIVE_CAPTURE_ARTIFACT_MEDIA_ROOT", "/tmp/capture-artifact-media"))
    rows: list[dict] = []
    transports: list[dict] = []
    calls = 0
    verdict = "PASS"
    for case in prereg["cases"]:
        media_path = media_root / case["local_name"]
        if not media_path.is_file():
            raise RuntimeError(f"missing media file {case['local_name']}")
        if sha256(media_path) != case["sha256"]:
            raise RuntimeError(f"media digest mismatch for {case['id']}")
        result, transport = invoke(host, extension, media_path, case["mime_type"], case["media_type"], {"case_id": case["id"], "function": case["function"], "questions": case["questions"]})
        calls += 1
        graded = grade(result, case)
        rows.extend({"case_id": case["id"], **r} for r in graded)
        transports.append({"case_id": case["id"], "interaction_id": transport.get("interaction_id"), "usage": transport.get("usage")})
        if any(not r["pass"] for r in graded):
            verdict = "REVISE"
            break
    passed = sum(1 for r in rows if r["pass"])
    expected_total = sum(len(c["expected"]) for c in prereg["cases"])
    final = verdict if len(rows) == expected_total and passed == expected_total else "REVISE"
    report = {
        "schema_version": "1.0.0",
        "cycle_id": prereg["cycle_id"],
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_blob": CANDIDATE_BLOB,
        "host_digest": HOST_DIGEST,
        "runtime": {"provider": "gemini-interactions-api", "model": MODEL, "scored_retries": 0},
        "candidate_calls": calls,
        "judge_calls": 0,
        "decisions_observed": len(rows),
        "decisions_passed": passed,
        "critical_failures": sum(1 for r in rows if not r["pass"]),
        "threshold": f"{expected_total}/{expected_total} mechanically keyed artifact decisions; first mismatch stops REVISE",
        "verdict": final,
        "results": rows,
        "transport": transports,
        "media_expected_key_disclosed_to_candidate": False,
    }
    out = Path(os.environ.get("AUTOMOTIVE_CAPTURE_ARTIFACT_REPORT", "/tmp/automotive-capture-artifact-report.json"))
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "transport"}, ensure_ascii=False, indent=2))
    return 0 if final == "PASS" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"cycle_id": "automotive-capture-direction-artifact-v0.1", "runtime_error": str(exc)}, ensure_ascii=False))
        raise SystemExit(2)
