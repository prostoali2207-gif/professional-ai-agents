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
    scorecard = Path("spline/docs/visual-quality-scorecard.md").read_text()

    system = (
        "You are a fresh, isolated execution of the frozen Visual Design / Art Direction professional core v0.2. "
        "Act as the Spline Visual Taste specialist. Direct rendered evidence is primary truth. "
        "Do not inherit any previous assistant conclusion, score, or proposed solution. Treat every proposed improvement as a hypothesis. "
        "This is a narrow professional refinement decision after V7, not permission to redesign for novelty or imitate competitors. "
        "Respect function, mobile viability, truth, authority boundaries, accessibility, and all project contracts.\n\n"
        "--- FROZEN PROFESSIONAL CORE ---\n" + skill
        + "\n\n--- PROFESSIONAL MODEL BASE ---\n" + base
        + "\n\n--- P0 REPAIR MODEL ---\n" + repair
    )

    spline_commit = os.environ["SPLINE_COMMIT"]
    spline_url = os.environ["SPLINE_URL"]
    prompt = f"""Review the exact Spline render built from commit {spline_commit}, together with four current user-supplied competitor/reference pages captured directly in Chromium.

USER QUESTION / DECISION TO MAKE
The user wants to continue improving the current V7 landing. Two possible gaps have been proposed, but they are hypotheses and MUST NOT be assumed true:
H1: the hero's exploded mechanical object may be too abstract and may need a more unmistakably automotive-part-specific identity.
H2: the request/form surface may visually fall below the art-direction level of the hero and may need stronger continuity.

Decide independently whether H1 and/or H2 are supported by the rendered evidence. If either is unsupported, explicitly reject it. This is visual-only unless a genuine release-critical usability problem is visible. Preserve the request flow, form fields, copy, validation, analytics, endpoint, CRM contract, success/error semantics and business claims by default.

IMAGE ORDER
1. Spline 390px full page.
2. Spline 390px hero crop.
3. Spline 390px request/form section crop.
4. Spline 1440px full page.
5. shamsiiii19/sh at 390px — user-supplied competitor/reference.
6. albinagas/lll at 390px — user-supplied competitor/reference.
7. samirka11/smm at 390px — user-supplied competitor/reference.
8. nissanr34ol/samirprobrand at 390px — user-supplied competitor/reference.

The competitor pages are different categories. Compare only transferable visual mechanisms: focal strength, direct product visuality, typography, scale contrast, section rhythm, CTA integration, perceived finish, and mobile composition. Do NOT copy their niche-specific motifs, proof, claims, card systems, gradients, or imagery merely because they exist.

--- SPLINE AGENTS ---
{agents}

--- SPLINE DESIGN CONTRACT ---
{design}

--- VISUAL TASTE PROJECT SKILL ---
{taste}

--- VISUAL QUALITY SCORECARD ---
{scorecard}

Return a concise implementation-ready professional review using exactly these headings:
VERDICT: KEEP | REFINE | RESET
REFERENCE_READ
P0
P1
P2
H1_HERO_OBJECT
H2_REQUEST_SURFACE
MOBILE
DESKTOP
TRANSFERABLE_MECHANISMS
DO_NOT_COPY
EXACT_CHANGE_CONTRACT
DO_NOT_TOUCH
VISUAL_TASTE_STATUS

Requirements:
- Base every finding on visible rendered evidence or supplied contracts.
- Do not reward novelty by itself and do not inflate scores to validate prior work.
- RESET requires compelling evidence that narrow refinement cannot solve the observed problem.
- If REFINE, prescribe the smallest coherent change set. Be exact about geometry, visual metaphor/object identity, framing, material treatment, section transition, form treatment, hierarchy and responsive behavior as applicable.
- If an automotive-specific hero object is warranted, specify what visual identity/category it should read as and why; do not invent a real product, supplier, fitment, price or availability claim.
- If request-surface continuity is warranted, specify visual changes without turning the form into CRM/dashboard UI or reducing field clarity/tapability.
- Identify elements that must remain untouched.
- Do not write CSS, JSX or implementation code.
- Do not invent benchmark observations or business facts.
- End VISUAL_TASTE_STATUS with exactly one of: VISUAL TASTE: READY FOR FRONTEND | VISUAL TASTE: RESEARCH / DIRECTION INSUFFICIENT | RENDER BLOCKED.
"""

    body = {
        "model": MODEL,
        "system_instruction": system,
        "input": [
            {"type": "text", "text": prompt},
            image_part("spline-mobile-full.png"),
            image_part("spline-mobile-hero.png"),
            image_part("spline-mobile-form.png"),
            image_part("spline-desktop-full.png"),
            image_part("competitor-sh-mobile.png"),
            image_part("competitor-lll-mobile.png"),
            image_part("competitor-smm-mobile.png"),
            image_part("competitor-samirprobrand-mobile.png"),
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
                "runtime": "fresh-provider-backed-multimodal-with-rendered-references",
                "provider": "gemini-interactions-api",
                "model": MODEL,
                "candidate_commit": CANDIDATE_COMMIT,
                "candidate_skill_blob": blob,
                "spline_commit": spline_commit,
                "spline_render_url": spline_url,
                "rendered_references": [
                    "https://shamsiiii19.github.io/sh/",
                    "https://albinagas.github.io/lll/",
                    "https://samirka11.github.io/smm/",
                    "https://nissanr34ol.github.io/samirprobrand/",
                ],
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
