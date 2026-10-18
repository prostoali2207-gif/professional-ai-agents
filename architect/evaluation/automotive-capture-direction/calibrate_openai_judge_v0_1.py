#!/usr/bin/env python3
from __future__ import annotations

import json, os, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("AUTOMOTIVE_CAPTURE_OPENAI_JUDGE_MODEL", "gpt-5.6-terra")
ENDPOINT = "https://api.openai.com/v1/chat/completions"
PACE = float(os.environ.get("AUTOMOTIVE_CAPTURE_OPENAI_JUDGE_PACE", "3"))

PAIRS = [
    {
        "id": "CAL-PERSPECTIVE",
        "task": "Only a phone is available. For a front 3/4 hero, the owner asks the operator to stand very close and use 0.6x because it looks aggressive.",
        "criteria": [
            "Perspective is diagnosed primarily through camera position/distance rather than focal-length folklore.",
            "A bounded phone-executable alternative uses greater distance and an available narrower field of view when feasible.",
            "No unavailable lens/device feature is invented."
        ],
        "good": "Do not make close 0.6x the default hero. The main problem is camera position: standing very close exaggerates the nose relative to the rear. Step back several metres, keep the camera around headlight-to-beltline height, and use the normal/main view if the phone has one. If the front still looks disproportionately large, step back again before changing framing. I cannot prescribe an unavailable focal view without knowing the phone.",
        "bad": "Use 0.6x and stand as close as possible. A wider focal length always creates better aggressive automotive perspective. Tilt the phone upward and crop later."
    },
    {
        "id": "CAL-DEVICE-HONESTY",
        "task": "The operator has an unknown Android phone. Give exact LOG, shutter, ISO, white balance and lens settings.",
        "criteria": [
            "Does not fabricate LOG, manual shutter, manual WB or lens availability.",
            "Requests/checks device capabilities when exact settings are material.",
            "Provides a bounded fallback based on observable controls and stable capture behavior."
        ],
        "good": "The phone model and camera controls are unknown, so I cannot give truthful LOG/shutter/ISO/WB values. First identify the phone and available camera modes. Until then use the main rear camera, avoid digital zoom, keep one consistent video mode, tap/hold to stabilize focus/exposure if the camera supports it, and watch the preview for exposure or white-balance pumping. If those controls are unavailable, keep the light and camera direction stable rather than inventing manual settings.",
        "bad": "Enable Apple Log, set 1/48 shutter, ISO 50, 5600K white balance and the 24 mm 1x lens. Every modern Android has equivalents, so these settings are safe."
    },
    {
        "id": "CAL-TRUTH",
        "task": "A sales car has a visible rear-door scratch. The owner asks for lighting and angle that hide it completely so buyers think the car is clean.",
        "criteria": [
            "Rejects capture chosen to create a materially misleading condition impression.",
            "Preserves truthful condition/proof coverage.",
            "Does not use a separate defect shot as permission to falsify the normal presentation."
        ],
        "good": "Do not design the normal sales coverage to make the scratch disappear in order to imply clean condition. We can make a well-composed beauty shot without deliberately falsifying the panel, and we need a separate clear condition shot that locates and shows the scratch honestly. If the approved brief requires a clean-condition claim, that claim must be corrected or escalated before shooting.",
        "bad": "Turn the scratched door away from the key light and expose for the highlights so the scratch disappears. Then film a quick defect close-up later; that makes it acceptable for the hero to imply perfect condition."
    },
    {
        "id": "CAL-EXECUTABILITY",
        "task": "A novice with a phone needs one front 3/4 hero shot. Give the instruction.",
        "criteria": [
            "The operator can determine where to stand and approximate height/distance or a reproducible cue.",
            "The instruction states what should be in/out of frame and what visual cue means success/failure.",
            "It avoids empty premium/cinematic adjectives as the only direction."
        ],
        "good": "Park the car with enough space to step back. Stand off the front corner so you see the front and the full near side. Start about 3–4 large walking paces farther back than the point where the car just fills the frame; hold the phone around headlight height and keep it level. Use the main rear camera, then move your feet—not digital zoom—to frame it. Accept when the nose does not look oversized, both wheels have clean separation, no pole/sign grows out of the roof, and the main body reflection is continuous. If the nose dominates, step back before changing anything else.",
        "bad": "Find a premium cinematic angle, make the stance powerful, keep reflections clean and shoot it like a luxury commercial. Use your eye to know when it looks expensive."
    },
    {
        "id": "CAL-RESTRAINT",
        "task": "A static proof shot is sharp, level, readable, reflection-safe and has sufficient handles. The owner wants an orbit because movement feels more professional.",
        "criteria": [
            "Accepts an already-good proof shot instead of changing it by habit.",
            "Separates proof clarity from optional beauty/desire motion.",
            "Does not equate movement with professionalism."
        ],
        "good": "Accept the static proof take. It already performs the proof job, so an orbit would add risk without improving evidence. If the brief also needs a desire/beauty shot, capture a separate controlled moving take for that different job and keep the accepted proof source unchanged.",
        "bad": "Reshoot it as a full gimbal orbit. Static shots look amateur and movement is always more cinematic and professional."
    }
]


def call_judge(pair: dict) -> dict:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENAI_API_KEY missing")
    system = (
        "You are calibrating as an independent evaluator of professional automotive commercial capture direction. "
        "Two anonymized responses answer the same task. Evaluate each against the explicit criteria, not prose polish or keyword count. "
        "A professional answer must be causally correct, physically executable where relevant, truthful about equipment and vehicle condition, and restrained when no change is needed. "
        "Return JSON only: {\"A\":{\"pass\":bool,\"reason\":string},\"B\":{\"pass\":bool,\"reason\":string}}."
    )
    user = json.dumps({"task": pair["task"], "criteria": pair["criteria"], "response_A": pair["good"], "response_B": pair["bad"]}, ensure_ascii=False)
    body = {
        "model": MODEL,
        "messages": [{"role":"system","content":system},{"role":"user","content":user}],
        "reasoning_effort": "low",
        "max_completion_tokens": 700,
        "response_format": {"type":"json_object"}
    }
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(), method="POST", headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw=json.loads(r.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"OpenAI judge HTTP {exc.code}: {exc.read().decode(errors='replace')[:1200]}") from exc
    text=raw.get("choices",[{}])[0].get("message",{}).get("content","")
    if not text:
        raise RuntimeError(f"OpenAI judge returned no content; usage={raw.get('usage')}")
    out=json.loads(text)
    return {"verdict":out,"usage":raw.get("usage") or {}}


def main() -> int:
    rows=[]
    for i,pair in enumerate(PAIRS):
        res=call_judge(pair)
        v=res["verdict"]
        passed=(v.get("A",{}).get("pass") is True and v.get("B",{}).get("pass") is False)
        rows.append({"id":pair["id"],"pass":passed,"A":v.get("A"),"B":v.get("B"),"usage":res["usage"]})
        if i < len(PAIRS)-1: time.sleep(PACE)
    report={
        "suite":"automotive-capture-openai-judge-calibration-v0.1",
        "model":MODEL,
        "generation_calls":len(rows),
        "pair_count":len(rows),
        "passed_pairs":sum(1 for r in rows if r["pass"]),
        "calibration_pass":all(r["pass"] for r in rows),
        "scope":"semantic/public calibration only; does not calibrate subjective artifact taste",
        "rows":rows
    }
    out=Path(os.environ.get("AUTOMOTIVE_CAPTURE_JUDGE_CALIBRATION_REPORT","/tmp/automotive-capture-openai-judge-calibration.json"))
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report["calibration_pass"] else 1

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"suite":"automotive-capture-openai-judge-calibration-v0.1","runtime_error":str(exc)},ensure_ascii=False))
        raise SystemExit(2)
