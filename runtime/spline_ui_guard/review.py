#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

MODEL = "gemini-3.5-flash-lite"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"


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


def main() -> int:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")

    agents = Path("spline/AGENTS.md").read_text()
    design = Path("spline/DESIGN.md").read_text()
    skill = Path("spline/.agents/skills/ui-guard/SKILL.md").read_text()
    scorecard = Path("spline/docs/visual-quality-scorecard.md").read_text()
    contract = Path("spline/docs/v7-product-specific-refinement.md").read_text()
    diff = Path("ui-guard-diff.txt").read_text()
    layouts = "\n".join(
        f"{p}: {Path(p).read_text()}" for p in [
            "ui-guard-390-layout.json", "ui-guard-768-layout.json", "ui-guard-1440-layout.json"
        ]
    )

    system = (
        "You are a fresh, isolated, independent UI Guard specialist for Spline. "
        "You did not create this implementation and you have not seen the creator model's review or scores. "
        "Judge the actual rendered output conservatively. Do not rubber-stamp the implementation or infer quality from green CI. "
        "Apply the project UI Guard skill, hard gates and visual scorecard exactly. "
        "The implementation contract describes intent only; it is not evidence that the intent succeeded."
    )

    head = os.environ["SPLINE_HEAD"]
    base = os.environ["SPLINE_BASE"]
    prompt = f"""Perform an independent rendered UI Guard release review of Spline exact head {head} against base {base}.

IMAGE ORDER
1. 390px full page
2. 390px hero
3. 390px request/form surface
4. 768px full page
5. 768px request/form surface
6. 1440px full page
7. 1440px hero
8. 1440px request/form surface

This is an independent gate after implementation. Do NOT assume the change is good because the contract asked for it. Verify directly whether the rendered result is coherent, intentional and launch-quality.

Pay special attention to:
- whether the hero object visibly reads as an automotive/mechanical part assembly rather than generic optics or abstract AI decoration;
- whether the dark request surface is visually coherent with V7 without becoming CRM/dashboard UI;
- whether form fields remain obvious, readable, tappable and calm;
- whether 390/768/1440 layouts have overlap, clipping, overflow, broken rhythm or accidental geometry;
- whether the hero/process/evidence/request sequence remains commercially clear and visually cohesive;
- whether truth/authority boundaries remain intact from visible content.

--- AGENTS ---
{agents}

--- DESIGN ---
{design}

--- UI GUARD SKILL ---
{skill}

--- SCORECARD ---
{scorecard}

--- IMPLEMENTATION CONTRACT (INTENT ONLY) ---
{contract}

--- EXACT BASE-TO-HEAD DIFF SUMMARY ---
{diff}

--- MECHANICAL LAYOUT MEASUREMENTS ---
{layouts}

Return exactly these headings:
VERDICT: PASS | REVISE | BLOCK
HARD_GATES
SCORECARD
OVERALL_VISUAL
OVERALL_COMMERCIAL
P0
P1
P2
MOBILE_390
TABLET_768
DESKTOP_1440
HERO_OBJECT
REQUEST_SURFACE
RETEST

Rules:
- HARD_GATES must explicitly report FUNCTION, MOBILE, AUTHORITY, TRUTH as PASS/BLOCK with one-line evidence.
- SCORECARD must score all 12 project dimensions from 0-10: Character, Clarity, Beauty, Visual lightness, Composition, Typography, Page rhythm, Perceived quality, Originality, Commercial direction, Trust credibility, Mobile visual UX.
- Use visible evidence, not design intent.
- Any unresolved P0/P1 means VERDICT cannot be PASS.
- P2 may coexist with PASS if non-blocking.
- If a target score is missed, explain whether it is P1 or P2 and why.
- Do not propose a redesign unless evidence requires it. Prescribe only the smallest fix needed for any P1.
- Do not invent business facts or infer backend success from screenshots.
- Do not cite or rely on any previous agent verdict, because none is provided here.
"""

    body = {
        "model": MODEL,
        "system_instruction": system,
        "input": [
            {"type": "text", "text": prompt},
            image_part("ui-guard-390-full.png"),
            image_part("ui-guard-390-hero.png"),
            image_part("ui-guard-390-request.png"),
            image_part("ui-guard-768-full.png"),
            image_part("ui-guard-768-request.png"),
            image_part("ui-guard-1440-full.png"),
            image_part("ui-guard-1440-hero.png"),
            image_part("ui-guard-1440-request.png"),
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
    Path("ui-guard-metadata.json").write_text(json.dumps({
        "runtime": "fresh-independent-provider-backed-ui-guard",
        "provider": "gemini-interactions-api",
        "model": MODEL,
        "spline_base": base,
        "spline_head": head,
        "interaction_id": raw.get("id"),
        "creator_output_in_prompt": False,
    }, indent=2))
    print("UI_GUARD_COMPLETED")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
