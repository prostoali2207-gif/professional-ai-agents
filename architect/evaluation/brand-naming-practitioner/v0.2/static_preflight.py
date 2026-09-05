#!/usr/bin/env python3
"""Zero-provider structural preflight for Brand Naming Practitioner v0.2 candidate."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
V02 = ROOT / "architect/evaluation/brand-naming-practitioner/v0.2"
MODEL = V02 / "professional-model-candidate-v0.2.md"
SKILL = V02 / "candidate/SKILL.md"
CASES = V02 / "development/semantic_cases.json"
DELTA = ROOT / "architect/research/brand-naming-practitioner/professional-delta-v0.2.md"
DOSSIER = ROOT / "architect/research/brand-naming-practitioner/production-failure-dossier-v0.2.md"
EVIDENCE = ROOT / "architect/research/brand-naming-practitioner/evidence-register-v0.2.md"
V01_TERMINAL = ROOT / "architect/evaluation/brand-naming-practitioner/terminal-record-v0.1-not-executable.json"

EXPECTED_FAMILIES = {
    "anti_anchoring",
    "standalone_divergence",
    "naturalness_vs_contrivance",
    "personal_identity_first_read",
    "role_vs_alias",
    "collision_relevance",
    "homophone_transcription",
    "lowercase_segmentation",
    "polysemy_first_meaning",
    "personal_handle_discovery_path",
    "metamorphic_consistency",
    "retained_boundaries",
    "decision_economy",
}

CHAT_EXACT_NAMES = {
    "nosignoutside",
    "pastthelastdoor",
    "halflitlanding",
    "lastlightupstairs",
    "stillcuring",
    "undertheprimer",
    "alioperator",
    "probablydeliberate",
    "moreorlessme",
}

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"FAIL: {msg}")

for path in [MODEL, SKILL, CASES, DELTA, DOSSIER, EVIDENCE, V01_TERMINAL]:
    require(path.exists(), f"missing {path.relative_to(ROOT)}")

model = MODEL.read_text(encoding="utf-8")
skill = SKILL.read_text(encoding="utf-8")
case_text = CASES.read_text(encoding="utf-8")
cases = json.loads(case_text)
terminal = json.loads(V01_TERMINAL.read_text(encoding="utf-8"))

require("Status: CANDIDATE / NOT QUALIFIED" in model, "v0.2 model status must remain candidate")
require("status: candidate-not-qualified" in skill, "v0.2 SKILL status must remain candidate")
require("version: 0.2.1-candidate" in skill, "v0.2.1 SKILL version missing")
require("QUALIFIED" not in skill.split("---", 2)[1], "front matter must not claim qualification")

for phrase in [
    "COUNTER-TERRITORY CHECK",
    "NATURALNESS / CONTRIVANCE CRITIQUE",
    "FIRST-READ + ORAL/TYPED TEST",
    "CONSISTENCY CHECK",
    "T0 — semantic/search noise",
    "person-alias",
    "lowercase segmentation",
]:
    require(phrase in model, f"missing v0.2 invariant: {phrase}")

require(isinstance(cases, list) and len(cases) == 13, "development suite must contain 13 cases")
families = {c.get("family") for c in cases}
require(families == EXPECTED_FAMILIES, f"unexpected development families: {families ^ EXPECTED_FAMILIES}")

lower_cases = case_text.lower()
for name in CHAT_EXACT_NAMES:
    require(name not in lower_cases, f"exact applied chat candidate leaked into dev fixture: {name}")

require(terminal.get("terminal_status") == "NOT_EXECUTABLE", "v0.1 terminal status changed")
require(terminal.get("candidate_release_state") == "FROZEN_NOT_QUALIFIED", "v0.1 release state changed")
require(terminal.get("professional_verdict") is None, "v0.1 professional verdict must remain null")

print("PASS: Brand Naming Practitioner v0.2 structural preflight")
print("PASS: v0.1 terminal state preserved")
print("PASS: 13/13 targeted development families structurally present")
