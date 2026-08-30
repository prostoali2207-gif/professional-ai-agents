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
        raise RuntimeError("No observable specialist output")
    return result


def main() -> int:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")

    skill = git_show("architect/evaluation/visual-design-art-direction/candidate/SKILL.md")
    base = git_show("architect/evaluation/visual-design-art-direction/professional-model-candidate-v0.1.md")
    repair = git_show("architect/evaluation/visual-design-art-direction/professional-model-p0-repair-v0.2.md")
    agents = Path("spline/AGENTS.md").read_text()
    design = Path("spline/DESIGN.md").read_text()
    taste = Path("spline/.agents/skills/visual-taste-agent/SKILL.md").read_text()

    system = (
        "You are a fresh, isolated execution of the frozen Visual Design / Art Direction professional core v0.2. "
        "Act as the Spline Visual Taste specialist for a narrow post-render review. Use direct rendered evidence as primary truth. "
        "Do not inherit any previous assistant verdict or score. Do not redesign for novelty. Decide independently whether the current production render should be kept or narrowly refined. "
        "Respect function, mobile viability, truth, authority boundaries, and project visual contracts.\n\n"
        "--- FROZEN PROFESSIONAL CORE ---\n" + skill
        + "\n\n--- PROFESSIONAL MODEL BASE ---\n" + base
        + "\n\n--- P0 REPAIR MODEL ---\n" + repair
    )

    spline_commit = os.environ["SPLINE_COMMIT"]
    spline_url = os.environ["SPLINE_URL"]
    prompt = f"""Review the exact current production render of Spline at commit {spline_commit}.

The user is specifically asking whether the mobile design still needs work after V7 refinement. This is a NARROW REFINE decision, not permission for another reset.

The supplied images are, in order:
1. current 390px full-page production render;
2. current 390px process-section crop;
3. current 1440px full-page production render.

Project source-of-truth context follows.

--- SPLINE AGENTS ---
{agents}

--- SPLINE DESIGN CONTRACT ---
{design}

--- VISUAL TASTE PROJECT SKILL ---
{taste}

Return a concise professional review using exactly these headings:
VERDICT: KEEP | REFINE | RESET
P0
P1
P2
HERO
PROCESS
EVIDENCE_CHAPTER
REQUEST_FORM
EXACT_CHANGE_CONTRACT

Rules:
- Base every finding on visible render evidence or the supplied contracts.
- If there is no P1, write NONE.
- If REFINE, give only the minimum exact changes needed; identify elements that must not be touched.
- Do not write CSS or implementation code.
- Do not invent benchmark observations, business facts, or unsupported claims.
"""

    body = {
        "model": MODEL,
        "system_instruction": system,
        "input": [
            {"type": "text", "text": prompt},
            image_part("mobile-full.png"),
            image_part("mobile-process.png"),
            image_part("desktop-full.png"),
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
    Path("visual-taste-output.md").write_text(output)
    blob = subprocess.check_output(
        ["git", "rev-parse", f"{CANDIDATE_COMMIT}:architect/evaluation/visual-design-art-direction/candidate/SKILL.md"],
        text=True,
    ).strip()
    Path("visual-taste-metadata.json").write_text(
        json.dumps(
            {
                "runtime": "fresh-provider-backed-multimodal",
                "provider": "gemini-interactions-api",
                "model": MODEL,
                "candidate_commit": CANDIDATE_COMMIT,
                "candidate_skill_blob": blob,
                "spline_commit": spline_commit,
                "production_url": spline_url,
                "interaction_id": raw.get("id"),
            },
            indent=2,
        )
    )
    print("VISUAL_SPECIALIST_COMPLETED")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
