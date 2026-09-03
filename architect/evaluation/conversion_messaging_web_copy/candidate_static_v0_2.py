#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "agents/conversion-messaging-web-copy/0.2.0/SKILL.md"
DELTA = ROOT / "architect/evaluation/conversion_messaging_web_copy/professional-delta-v0.2.md"
SOURCES = ROOT / "architect/evaluation/conversion_messaging_web_copy/source-register-v0.2.md"
PLAN = ROOT / "architect/evaluation/conversion_messaging_web_copy/evaluation-plan-v0.2.md"

checks = 0

def check(cond: bool, msg: str) -> None:
    global checks
    if not cond:
        raise RuntimeError(msg)
    checks += 1

for p in (SKILL, DELTA, SOURCES, PLAN):
    check(p.is_file(), f"missing required artifact: {p.relative_to(ROOT)}")

s = SKILL.read_text(encoding="utf-8")
d = DELTA.read_text(encoding="utf-8")
e = PLAN.read_text(encoding="utf-8")

# Version/provenance and no false release claim.
check("Version: 0.2.0-candidate" in s, "candidate version missing")
check("Status: development candidate pending independent qualification" in s, "candidate status invalid")
check("v0.1 qualification terminated `NOT_EXECUTABLE`" in s, "v0.1 terminal provenance missing")
check("Status: qualified" not in s.lower(), "false qualified status present")

# Material delta D1-D3 must be behaviorally encoded, not only named in research notes.
for token in (
    "Acquisition-source and landing-message continuity",
    "source-message contract",
    "knowingly echo an unsupported acquisition-source claim",
    "CTA, links and microcopy",
    "labels/instructions",
    "detected-error states",
    "copy alone makes a composed interface WCAG-compliant",
    "Localization and translatability",
    "machine translation",
    "qualified translator/local reviewer/legal review",
):
    check(token in s, f"missing v0.2 behavior token: {token}")

# Preserved v0.1 release-critical mechanisms.
for token in (
    "VERIFIED",
    "BOUNDED",
    "HYPOTHESIS",
    "UNKNOWN",
    "PROHIBITED",
    "evidence ledger",
    "genuinely distinct message concepts",
    "Match proof to the objection",
    "Never promise lift",
    "User Research owns",
    "UX owns",
    "publish autonomously",
):
    check(token in s, f"missing preserved v0.1 invariant: {token}")

# Research-before-skill / new-cycle integrity markers.
check("V0_2_JUSTIFIED" in d, "Architect delta decision missing")
for family in ("CM-MM", "CM-A11Y", "CM-L10N"):
    check(family in e, f"new evaluation family missing: {family}")
check("stopped v0.1 #225/#237 chain remains terminal" in e, "stop-loss continuity missing")

print(json.dumps({
    "status": "PASS",
    "checks": checks,
    "model_calls": 0,
    "scored_calls": 0,
    "paid_api_calls": 0,
    "candidate": "conversion-messaging-web-copy/0.2.0-candidate",
}, sort_keys=True))
