#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

MODEL = "gemini-3.5-flash-lite"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"


def extract(raw: dict) -> str:
    text = raw.get("output_text")
    if isinstance(text, str) and text.strip():
        return text
    chunks: list[str] = []
    for out in raw.get("outputs") or []:
        if isinstance(out, dict) and isinstance(out.get("text"), str):
            chunks.append(out["text"])
    for step in raw.get("steps") or []:
        if not isinstance(step, dict) or step.get("type") != "model_output":
            continue
        content = step.get("content")
        if isinstance(content, str):
            chunks.append(content)
        elif isinstance(content, list):
            chunks.extend(
                x["text"] for x in content
                if isinstance(x, dict) and isinstance(x.get("text"), str)
            )
    result = "\n".join(x for x in chunks if x.strip())
    if not result.strip():
        raise RuntimeError("No observable QA Agent output")
    return result


def main() -> int:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")

    qa_skill = Path("spline/.agents/skills/qa-agent/SKILL.md").read_text()
    agents = Path("spline/AGENTS.md").read_text()
    design = Path("spline/DESIGN.md").read_text()
    diff = Path("qa-diff.txt").read_text()
    e2e = Path("qa-e2e.log").read_text()
    smoke = Path("qa-real-crm-smoke.json").read_text()

    system = (
        "You are a fresh, isolated execution of the Spline QA Agent. "
        "You are independent from the frontend implementer, Visual Taste specialist, UI Guard, and the conversational assistant. "
        "Apply the QA SKILL literally. Judge only observable evidence supplied here and the authoritative contracts. "
        "Do not treat build success alone as QA PASS. Do not invent tests, CRM evidence, or security assurance.\n\n"
        "--- QA AGENT SKILL ---\n" + qa_skill
    )

    prompt = f"""Perform the independent pre-merge release gate for Spline PR #25.

Exact scope:
- base: {os.environ['SPLINE_BASE']}
- head: {os.environ['SPLINE_HEAD']}
- change intent: repair the 360/390 mobile process number/copy collision only.

Important evidence boundary:
- A fresh independent UI Guard runtime has already returned PASS on exact head at 390/768/1440, with P0 none, P1 none, and explicit confirmation that 01/02/03 no longer overlap copy. Treat that as an upstream visual-gate result, not as proof of functional QA.
- This QA run itself built and tested exact head, then made one clearly identified REAL browser submission from the exact locally served head to the existing production create-landing-request endpoint. The raw observable result is supplied below.
- Decide independently whether that evidence is sufficient for PASS under the narrow changed scope. If any required verification is missing, return BLOCKED rather than assuming.

--- PROJECT AGENTS ---
{agents}

--- DESIGN CONTRACT ---
{design}

--- EXACT BASE..HEAD DIFF EVIDENCE ---
{diff}

--- EXECUTED E2E LOG ---
{e2e}

--- REAL CRM-BACKED BROWSER SMOKE RESULT ---
{smoke}

Return exactly:
### Verdict
PASS | FAIL | BLOCKED

### Release-critical findings
Use NONE if none. Otherwise severity -> scenario -> expected -> actual -> evidence -> owner.

### Contract status
Conversion: PASS|FAIL|UNVERIFIED
UX: PASS|FAIL|UNVERIFIED
Visual: PASS|FAIL|UNVERIFIED
CRM: PASS|FAIL|UNVERIFIED

### Tested
List only scenarios actually evidenced by the supplied run artifacts.

### Unverified risks
List residual risks accurately; do not inflate unrelated unchanged scope into a blocker unless QA SKILL requires it.

### Retest
State exactly what, if anything, must run after merge in production.

Rules:
- Do not claim photo upload security is proven beyond the executed client-side tests.
- Distinguish mocked E2E success paths from the one real CRM-backed browser smoke.
- If the real smoke shows an accepted numbered request, CRM acceptance for that exact head is verified at the browser-to-endpoint boundary.
- Do not infer internal CRM field mapping beyond what the observable smoke proves unless explicit evidence is present.
"""

    body = {
        "model": MODEL,
        "system_instruction": system,
        "input": [{"type": "text", "text": prompt}],
        "store": False,
        "generation_config": {"thinking_level": "medium"},
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body, ensure_ascii=False).encode(),
        method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            raw = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[-1500:]
        raise RuntimeError(f"Gemini HTTP {exc.code}: {detail}") from None

    output = extract(raw)
    Path("qa-agent-output.md").write_text(output)
    Path("qa-agent-metadata.json").write_text(json.dumps({
        "runtime": "fresh-independent-provider-backed-qa-agent",
        "provider": "gemini-interactions-api",
        "model": MODEL,
        "spline_base": os.environ["SPLINE_BASE"],
        "spline_head": os.environ["SPLINE_HEAD"],
        "interaction_id": raw.get("id"),
    }, indent=2))
    print("QA_AGENT_COMPLETED")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
