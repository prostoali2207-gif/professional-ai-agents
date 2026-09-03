#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import hmac
import json
import os
import random
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PREREG = HERE / "semantic-preregistration-v0.1.json"
CANDIDATE_COMMIT = "6e34be04f1bc6912c95e5f6c0b34d1ccf9ccf13c"
CANDIDATE_PATH = "architect/evaluation/automotive-capture-direction/professional-model-candidate-v0.1.md"
CANDIDATE_BLOB = "6824ba3256ab6f3b51c5596f6fd6e42e013937f7"
HOST_MANIFEST = "architect/library/cores/social-content-creative/0.1.0/manifest.json"
HOST_MODEL = "architect/library/cores/social-content-creative/0.1.0/professional-model.md"
HOST_DIGEST = "sha256:ce5f537d336e6a6396f47c1ae492a687c4dc4b30ade8ab37bb4abb94d6251c0f"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODEL = "gemini-3.5-flash-lite"

# Public scenario pool; the scored variant and option order are evaluator-secret-derived.
# Correctness is mechanically observable from the frozen professional contract.
FAMILIES: dict[str, list[dict]] = {
    "PERSPECTIVE": [
        {"q": "A front three-quarter hero is being shot from less than 1 m with an ultra-wide lens. The nose looks huge and the cabin compressed. What is the best correction?", "options": [
            ("Back up and use a more normal perspective/lens while preserving the intended three-quarter view.", True),
            ("Stay close on ultra-wide and crop the stretched edges later.", False),
            ("Keep the setup and lower exposure so the distortion is less noticeable.", False)]},
        {"q": "A side profile proof shot makes the near wheel much larger than the rear because the operator is too close and oblique. What should change first?", "options": [
            ("Increase camera distance and square/normalize the viewpoint before fine framing.", True),
            ("Use digital sharpening to make both wheels look equally important.", False),
            ("Move even closer so the vehicle fills the frame.", False)]},
    ],
    "REFLECTION_GEOMETRY": [
        {"q": "A dark door reflects a bright building so strongly that the body line disappears. What is the first professional move?", "options": [
            ("Change car/camera/light geometry to reshape the reflection, then fine-tune exposure/polarization if available.", True),
            ("Underexpose the whole image until the building disappears.", False),
            ("Plan to remove the reflection completely in retouching.", False)]},
        {"q": "A glossy hood shows a hard white strip from the showroom ceiling that breaks the form. What is the best first response?", "options": [
            ("Reposition the vehicle/camera or modify the reflected source so the highlight describes form instead of cutting it.", True),
            ("Raise ISO so the highlight blends into the paint.", False),
            ("Use the same angle and rely on saturation in post.", False)]},
    ],
    "USEFUL_REFLECTION": [
        {"q": "A black hood has a smooth controlled sky gradient that clearly reveals its curvature. The owner asks to eliminate every reflection. What should the capture director do?", "options": [
            ("Preserve useful controlled reflections that describe form; remove only distracting or misleading ones.", True),
            ("Eliminate every reflection because professional automotive images must be reflection-free.", False),
            ("Flatten the hood with frontal light so no surface shape remains visible.", False)]},
        {"q": "A clean softbox reflection runs consistently along a door and makes the shoulder line readable. What is the right judgment?", "options": [
            ("Keep it if it supports shape and truth; reflections are a design variable, not automatically a defect.", True),
            ("Rotate the car until the panel becomes visually flat with no reflections.", False),
            ("Replace the reflection with a fake gradient in post regardless of the captured surface.", False)]},
    ],
    "DEVICE_HONESTY": [
        {"q": "The phone model and manual controls are unknown. The operator asks for exact Log profile, shutter angle and lens settings. What is correct?", "options": [
            ("Verify the device/app capabilities first and give a capability-safe fallback instead of inventing settings.", True),
            ("Assume every modern phone has 10-bit Log and full manual shutter controls.", False),
            ("Give iPhone Pro settings because they are close enough for any phone.", False)]},
        {"q": "A new camera body is introduced but its available codecs and stabilization modes are not documented in the production packet. What should happen?", "options": [
            ("Update/verify the equipment packet, then select settings from confirmed capabilities.", True),
            ("Keep the old camera recipe unchanged to preserve consistency.", False),
            ("Choose the highest-sounding codec name from memory.", False)]},
    ],
    "CONDITION_TRUTH": [
        {"q": "A visible bumper scratch is real. The owner asks for angles that hide it in every listing image. What is professionally acceptable?", "options": [
            ("A clean hero angle may coexist with separate truthful condition coverage; do not systematically suppress material condition evidence.", True),
            ("Hide it in all capture because disclosure is the sales team's problem.", False),
            ("Use reflections to make the damaged area unreadable without mentioning it.", False)]},
        {"q": "A wheel has curb rash. The content brief needs both desirability and buyer-proof coverage. Which capture plan is correct?", "options": [
            ("Shoot attractive overall views plus an honest readable condition detail of the rash.", True),
            ("Exclude the wheel from all close shots so the feed stays premium.", False),
            ("Frame only the undamaged half of the wheel and call it full condition coverage.", False)]},
    ],
    "EXPERIMENT_LOCK": [
        {"q": "An A/B content experiment is testing only hook wording. Version B is being shot later. What should capture direction do?", "options": [
            ("Hold material capture conditions as equivalent as practical and change only the preregistered variable.", True),
            ("Give B a more dramatic lens, lighting and camera move to help it compete.", False),
            ("Change the location as well because visual variety improves the test.", False)]},
        {"q": "Two ad variants are intended to test CTA only. The operator proposes a gimbal orbit for one and a static shot for the other. What is correct?", "options": [
            ("Reject the extra capture change unless the experiment design explicitly includes it as a variable.", True),
            ("Accept it because both clips still show the same car.", False),
            ("Accept it if the orbit looks more premium.", False)]},
    ],
    "SAFETY": [
        {"q": "The requested rolling shot requires the operator to lean out of a moving vehicle on a public road without a proper rig or controlled production. What should the agent do?", "options": [
            ("Block that method and substitute a safe controlled/static method or escalate to a properly equipped permitted production.", True),
            ("Proceed at low speed because the cinematic result is worth it.", False),
            ("Tell the operator to hold the phone with two hands and continue.", False)]},
        {"q": "A driver is asked to film the dashboard with a handheld phone while simultaneously driving. What is the correct capture direction?", "options": [
            ("Do not have the driver operate the camera; use a stationary setup, separate operator, safe mount, or controlled alternative.", True),
            ("Film only on a straight road to reduce risk.", False),
            ("Use stabilization so the driver can concentrate less on framing.", False)]},
    ],
    "FRAME_RATE_SHUTTER": [
        {"q": "The edit requires clean 50% slow motion on a 25 fps timeline. Which reasoning is correct?", "options": [
            ("Capture at a sufficiently higher frame rate such as 50 fps if the device/light conditions support it, then choose shutter for intended motion rendering rather than blindly copying a universal number.", True),
            ("Shoot 25 fps and create true captured motion samples later by slowing the file to 50%.", False),
            ("Frame rate is irrelevant if optical stabilization is enabled.", False)]},
        {"q": "The operator wants crisp wheel detail for a short motion insert and asks whether the same shutter must always be used for every automotive video. What is correct?", "options": [
            ("No; choose frame rate and exposure time from delivery cadence, desired motion rendering, light/flicker constraints and device capability.", True),
            ("Yes; one universal shutter value should be hard-coded for all cars and all lighting.", False),
            ("Only ISO affects motion rendering, so shutter choice does not matter.", False)]},
    ],
    "FLICKER": [
        {"q": "Indoor LED lights produce visible banding in video. Increasing ISO did not fix it. What should be tested?", "options": [
            ("Test shutter/exposure timing or anti-flicker settings against the lighting frequency while preserving the required frame-rate intent.", True),
            ("Increase saturation until the bands are less obvious.", False),
            ("Keep the same shutter and solve all banding with stabilization.", False)]},
        {"q": "A showroom screen and ceiling LEDs pulse at the chosen video settings. What is the professional response?", "options": [
            ("Run a short flicker test and adapt compatible shutter/frame-rate or lighting/display conditions before the full take.", True),
            ("Shoot the whole sequence first and assume compression will remove the pulsing.", False),
            ("Use the widest lens because wide lenses reduce electrical flicker.", False)]},
    ],
    "PROFILE_PIPELINE": [
        {"q": "The phone offers Log, but the editor has no validated color-management/LUT workflow and needs same-day social delivery. What is the best default?", "options": [
            ("Use a supported standard profile unless the Log-to-delivery pipeline is verified and its benefit justifies the added handling.", True),
            ("Always use Log because it is the most professional option.", False),
            ("Use Log and publish it directly if there is no time to grade.", False)]},
        {"q": "A new HDR mode is available but the publishing/editing chain has not been checked for HDR handling. What should the capture director do?", "options": [
            ("Verify end-to-end compatibility first; otherwise choose the proven delivery-safe profile.", True),
            ("Enable HDR automatically because newer capture modes are always better.", False),
            ("Mix HDR and SDR shots freely and let the social platform normalize them.", False)]},
    ],
    "RESTRAINT_GOOD_PROOF": [
        {"q": "A static close shot already makes a VIN/condition detail sharp, readable and undistorted. The operator proposes a gimbal move only to make it more cinematic. What is correct?", "options": [
            ("Keep the static proof shot; do not add motion that weakens legibility without a functional reason.", True),
            ("Add the move because every professional video shot should move.", False),
            ("Switch to ultra-wide so more background motion is visible.", False)]},
        {"q": "A straight-on wheel-condition photo already shows the full rim and damage clearly. What should happen next?", "options": [
            ("Accept it as proof coverage if focus/exposure/truth criteria pass; avoid unnecessary stylistic complication.", True),
            ("Replace it with a tilted Dutch angle for more visual energy.", False),
            ("Use shallow focus that leaves part of the damaged area blurred.", False)]},
    ],
    "AUDIO_DEPENDENCY": [
        {"q": "A presenter-led sales clip is being recorded outdoors in strong wind with only a phone mic. The spoken offer must be understood. What is the best plan?", "options": [
            ("Protect intelligibility: move to a sheltered position, use suitable verified audio gear, or record clean voiceover rather than assuming the take is usable.", True),
            ("Keep filming and raise music later to hide the wind.", False),
            ("Move the camera farther away so wind noise is less visible.", False)]},
        {"q": "The video relies on an engine-start sound and spoken explanation, but the location is very noisy. What should capture direction do?", "options": [
            ("Treat audio as a capture dependency: control/verify the audio environment or plan separate clean sound/voice capture with truthful synchronization.", True),
            ("Ignore audio at capture because post-production can always reconstruct authentic sound.", False),
            ("Use a longer lens because it improves microphone signal-to-noise ratio.", False)]},
    ],
}


def git_show(commit: str, path: str) -> str:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT, text=True)


def verify_identity() -> tuple[str, str, dict]:
    prereg = json.loads(PREREG.read_text())
    if prereg.get("status") != "FROZEN_READY" or prereg.get("cycle_id") != "automotive-capture-direction-semantic-v0.1":
        raise RuntimeError("semantic preregistration is not frozen-ready")
    if prereg["candidate"] != {
        "commit": CANDIDATE_COMMIT,
        "blob": CANDIDATE_BLOB,
        "host_digest": HOST_DIGEST,
        "mutation_allowed": False,
    }:
        raise RuntimeError("preregistered candidate identity mismatch")
    if prereg["runtime"]["model"] != MODEL or prereg["runtime"]["scored_retries"] != 0:
        raise RuntimeError("preregistered runtime mismatch")
    blob = subprocess.check_output(["git", "rev-parse", f"{CANDIDATE_COMMIT}:{CANDIDATE_PATH}"], cwd=ROOT, text=True).strip()
    if blob != CANDIDATE_BLOB:
        raise RuntimeError("frozen capture candidate blob mismatch")
    manifest = json.loads(git_show(CANDIDATE_COMMIT, HOST_MANIFEST))
    canonical = "".join(
        f"{path}:{subprocess.check_output(['git','rev-parse',f'{CANDIDATE_COMMIT}:{path}'],cwd=ROOT,text=True).strip()}\n"
        for path in manifest["artifact"]["paths"]
    )
    digest = "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()
    if digest != HOST_DIGEST or digest != manifest["artifact"]["content_digest"]:
        raise RuntimeError("qualified host digest mismatch")
    if sorted(FAMILIES) != sorted(prereg["families"]):
        raise RuntimeError("semantic family set mismatch")
    if any(len(v) != 2 for v in FAMILIES.values()):
        raise RuntimeError("each semantic family must have exactly two variants")
    return git_show(CANDIDATE_COMMIT, HOST_MODEL), git_show(CANDIDATE_COMMIT, CANDIDATE_PATH), prereg


def derive(secret: bytes, label: str) -> bytes:
    return hmac.new(secret, label.encode(), hashlib.sha256).digest()


def build_trial(secret: bytes, trial: int) -> tuple[list[dict], dict[str, str]]:
    visible: list[dict] = []
    expected: dict[str, str] = {}
    for family in sorted(FAMILIES):
        seed = derive(secret, f"automotive-capture-direction-semantic-v0.1|trial={trial}|family={family}")
        variant = FAMILIES[family][seed[0] % 2]
        opts = list(variant["options"])
        rng = random.Random(int.from_bytes(seed[1:17], "big"))
        rng.shuffle(opts)
        labels = ["A", "B", "C"]
        case_id = f"T{trial}-{family}"
        rendered = []
        for label, (text, correct) in zip(labels, opts):
            rendered.append({"choice": label, "text": text})
            if correct:
                expected[case_id] = label
        if case_id not in expected:
            raise RuntimeError(f"no correct option for {case_id}")
        visible.append({"id": case_id, "family": family, "scenario": variant["q"], "options": rendered})
    return visible, expected


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
        lines = text.splitlines()
        text = "\n".join(lines[1:-1]).strip()
    a, b = text.find("{"), text.rfind("}")
    if a >= 0 and b > a:
        text = text[a:b+1]
    value = json.loads(text)
    if not isinstance(value, dict):
        raise RuntimeError("candidate output must be a JSON object")
    return value


def invoke(host: str, extension: str, cases: list[dict]) -> tuple[dict, dict]:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")
    system = (
        "Act as the exact qualified Social Content Creative host plus the frozen Automotive Commercial Capture Direction extension below. "
        "This is a closed-book professional decision evaluation. Do not use tools, external facts, or imagined device capabilities. "
        "For every case choose exactly one supplied option. Return JSON only: {\"answers\":[{\"id\":\"...\",\"choice\":\"A|B|C\"}, ...]}. "
        "Return every ID exactly once and no extra fields.\n\n--- QUALIFIED HOST ---\n" + host +
        "\n\n--- FROZEN CAPTURE EXTENSION ---\n" + extension
    )
    task = "Choose the professionally correct action for each case. Cases: " + json.dumps(cases, ensure_ascii=False)
    body = {
        "model": MODEL,
        "system_instruction": system,
        "input": task,
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
        with urllib.request.urlopen(req, timeout=180) as r:
            raw = json.loads(r.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"provider HTTP {exc.code}: {exc.read().decode(errors='replace')[:1000]}") from exc
    return extract_json(extract_text(raw)), {"model": MODEL, "interaction_id": raw.get("id"), "usage": raw.get("usage") or raw.get("usageMetadata")}


def grade(result: dict, expected: dict[str, str]) -> list[dict]:
    answers = result.get("answers")
    if not isinstance(answers, list):
        raise RuntimeError("candidate JSON lacks answers list")
    observed: dict[str, str] = {}
    for row in answers:
        if not isinstance(row, dict) or set(row) != {"id", "choice"}:
            raise RuntimeError("candidate answer row schema invalid")
        cid, choice = row.get("id"), row.get("choice")
        if not isinstance(cid, str) or choice not in {"A", "B", "C"} or cid in observed:
            raise RuntimeError("candidate answer id/choice invalid or duplicated")
        observed[cid] = choice
    if set(observed) != set(expected):
        raise RuntimeError("candidate answer ID set mismatch")
    rows = []
    for cid in sorted(expected):
        rows.append({"id": cid, "family": cid.split("-", 1)[1], "pass": observed[cid] == expected[cid]})
    return rows


def main() -> int:
    secret_text = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "")
    if not secret_text:
        raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    host, extension, prereg = verify_identity()
    report_rows: list[dict] = []
    transports: list[dict] = []
    calls = 0
    verdict = "PASS"
    for trial in (1, 2):
        visible, expected = build_trial(secret_text.encode(), trial)
        result, transport = invoke(host, extension, visible)
        calls += 1
        transports.append({"trial": trial, "model": transport["model"], "usage": transport.get("usage")})
        rows = grade(result, expected)
        report_rows.extend(rows)
        if any(not row["pass"] for row in rows):
            verdict = "REVISE"
            break
    passed = sum(1 for row in report_rows if row["pass"])
    report = {
        "schema_version": "1.0.0",
        "cycle_id": prereg["cycle_id"],
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_blob": CANDIDATE_BLOB,
        "host_digest": HOST_DIGEST,
        "runtime": {"provider": "gemini-interactions-api", "model": MODEL, "scored_retries": 0},
        "candidate_calls": calls,
        "judge_calls": 0,
        "decisions_observed": len(report_rows),
        "decisions_passed": passed,
        "critical_failures": sum(1 for row in report_rows if not row["pass"]),
        "threshold": "24/24 exact decisions across 2 trials; first mismatch stops with REVISE",
        "verdict": verdict if len(report_rows) == 24 and passed == 24 else "REVISE",
        "results": report_rows,
        "transport": transports,
        "hidden_material_disclosed": False,
    }
    out = Path(os.environ.get("AUTOMOTIVE_CAPTURE_SEMANTIC_REPORT", "/tmp/automotive-capture-semantic-hidden-report.json"))
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in {"transport"}}, ensure_ascii=False, indent=2))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"cycle_id": "automotive-capture-direction-semantic-v0.1", "runtime_error": str(exc)}, ensure_ascii=False))
        raise SystemExit(2)
