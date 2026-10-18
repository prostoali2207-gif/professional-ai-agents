#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=Path(__file__).resolve().parents[3]
MODEL=(HERE/"professional-model-extension-candidate-v0.1.md").read_text(encoding="utf-8")
SKILL=(HERE/"candidate"/"SKILL.md").read_text(encoding="utf-8")
CASES=json.loads((HERE/"semantic-cases.json").read_text(encoding="utf-8"))

PARENT="sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b"

assert PARENT in MODEL
assert "NOT QUALIFIED" in MODEL
assert "candidate-not-qualified" in SKILL
assert len(CASES)==10
ids=[c["id"] for c in CASES]
assert len(ids)==len(set(ids))
for c in CASES:
    assert c["allowed_actions"]
    assert c["forbidden_actions"]
    assert c["required_flags"]
    assert set(c["allowed_actions"]).isdisjoint(set(c["forbidden_actions"]))
assert any(c["id"]=="CSD-S9" and "READY_FOR_REAL_MEDIA_REVIEW" in c["forbidden_actions"] for c in CASES)
assert any(c["id"]=="CSD-S3" and "truth_preserving_sound" in c["required_flags"] for c in CASES)
print("commercial-sound-design deterministic contract: PASS")
