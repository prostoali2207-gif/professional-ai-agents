#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

CANDIDATE_COMMIT = "0116d20f99fde919fa6e39c700726d16310d010b"
MODEL = "gemini-3.5-flash-lite"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"


def git_show(path: str) -> str:
    return subprocess.check_output(["git", "show", f"{CANDIDATE_COMMIT}:{path}"], text=True)


def image_part(path: str) -> dict:
    return {
        "type": "image",
        "data": base64.b64encode(Path(path).read_bytes()).decode(),
        "mime_type": "image/png",
    }


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
                x["text"]
                for x in content
                if isinstance(x, dict) and isinstance(x.get("text"), str)
            )
    result = "\n".join(x for x in chunks if x.strip())
    if not result.strip():
        raise RuntimeError("No observable UI Guard output")
    return result


def read_optional(path: str) -> str:
    p = Path(path)
    return p.read_text() if p.exists() else "NOT PRESENT"


def main() -> int:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")

    frozen_skill = git_show("architect/evaluation/visual-design-art-direction/candidate/SKILL.md")
    base = git_show("architect/evaluation/visual-design-art-direction/professional-model-candidate-v0.1.md")
    repair = git_show("architect/evaluation/visual-design-art-direction/professional-model-p0-repair-v0.2.md")
    agents = Path("spline/AGENTS.md").read_text()
    design = Path("spline/DESIGN.md").read_text()
    guard = Path("spline/.agents/skills/ui-guard/SKILL.md").read_text()
    scorecard = read_optional("spline/docs/visual-quality-scorecard.md")

    system = (
        "You are a fresh, isolated independent UI Guard for the Spline auto-parts landing. "
        "You are not the Visual Taste author and you receive no prior Visual Taste verdict. "
        "Judge only the supplied exact rendered evidence and authoritative project contracts. "
        "The frozen Visual Design / Art Direction core is professional judgment support, while the Spline UI Guard SKILL defines your review authority and PASS/REVISE/BLOCK semantics. "
        "Do not approve work to validate prior effort. Do not redesign. Do not invent facts or benchmark observations.\n\n"
        "--- FROZEN VISUAL PROFESSIONAL CORE ---\n" + frozen_skill
        + "\n\n--- PROFESSIONAL MODEL BASE ---\n" + base
        + "\n\n--- P0 REPAIR MODEL ---\n" + repair
    )

    head = os.environ["SPLINE_HEAD"]
    base_sha = os.environ["SPLINE_BASE"]
    preview = os.environ["SPLINE_PREVIEW_URL"]
    prompt = f"""Independently review Spline PR head {head} against base {base_sha}.

This is a narrow rendered re-review after a mobile process-layout correction. Do not assume the correction worked. The images supplied are:
1. 390px full-page preview;
2. 390px process crop;
3. 768px full-page preview;
4. 1440px full-page preview.

The changed scope is intentionally narrow: mobile process number/copy separation. The landing's request endpoint, payload, validation, CRM semantics, hero, evidence chapter, and form content were not intended to change. Review the whole visible page for regressions, but do not demand unrelated redesign.

--- SPLINE AGENTS ---
{agents}

--- SPLINE DESIGN CONTRACT ---
{design}

--- INDEPENDENT UI GUARD SKILL ---
{guard}

--- VISUAL QUALITY SCORECARD ---
{scorecard}

Return exactly these headings:
VERDICT: PASS | REVISE | BLOCK
P0
P1
P2
PROCESS_COLLISION
HERO
EVIDENCE_CHAPTER
REQUEST_FORM
MOBILE_390
INTERMEDIATE_768
DESKTOP_1440
SCORECARD
RELEASE_DECISION

Requirements:
- Explicitly state whether 01/02/03 numbers overlap or collide with their labels/copy at 390px.
- PASS requires no unresolved P0/P1.
- SCORECARD must list all 12 UI Guard dimensions from its SKILL, each 1-10, plus overall visual and overall commercial-landing scores.
- Findings must be grounded in visible render evidence or supplied contract text.
- If a section has no issue, say intact/none rather than inventing polish work.
- Do not write CSS or implementation code.
"""

    body = {
        "model": MODEL,
        "system_instruction": system,
        "input": [
            {"type": "text", "text": prompt},
            image_part("mobile-390-full.png"),
            image_part("mobile-390-process.png"),
            image_part("intermediate-768-full.png"),
            image_part("desktop-1440-full.png"),
        ],
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
    Path("ui-guard-output.md").write_text(output)
    blob = subprocess.check_output(
        ["git", "rev-parse", f"{CANDIDATE_COMMIT}:architect/evaluation/visual-design-art-direction/candidate/SKILL.md"],
        text=True,
    ).strip()
    Path("ui-guard-metadata.json").write_text(
        json.dumps(
            {
                "runtime": "fresh-independent-provider-backed-multimodal-ui-guard",
                "provider": "gemini-interactions-api",
                "model": MODEL,
                "candidate_commit": CANDIDATE_COMMIT,
                "candidate_skill_blob": blob,
                "spline_base": base_sha,
                "spline_head": head,
                "preview_url": preview,
                "interaction_id": raw.get("id"),
            },
            indent=2,
        )
    )
    print("UI_GUARD_COMPLETED")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
