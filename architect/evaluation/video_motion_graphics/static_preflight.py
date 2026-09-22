#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

MODEL = HERE / "professional-model-candidate-v0.1.md"
SKILL = HERE / "candidate" / "SKILL.md"
FIXTURES = HERE / "semantic-fixtures-v0.1.json"
PRACTICAL = HERE / "practical-real-media-gate-v0.1.md"
PLAN = HERE / "evaluation-plan-v0.1.md"

PARENT_DIGEST = "sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b"
EXPECTED_P0 = {"MG-S2", "MG-S4", "MG-S7", "MG-S8"}
EXPECTED_SOURCE_SHA = "45de1fac61f9877289bca03867e3e7f91ba6685da775853466c30f43055a8209"

def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")

for p in [MODEL, SKILL, FIXTURES, PRACTICAL, PLAN]:
    if not p.exists():
        fail(f"missing {p.relative_to(ROOT)}")

model = MODEL.read_text(encoding="utf-8")
skill = SKILL.read_text(encoding="utf-8")
practical = PRACTICAL.read_text(encoding="utf-8")
plan = PLAN.read_text(encoding="utf-8")
fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))

if "NOT QUALIFIED" not in model:
    fail("candidate model is not explicitly NOT QUALIFIED")
if "status: candidate-not-qualified" not in skill:
    fail("candidate SKILL status drift")
if PARENT_DIGEST not in model or PARENT_DIGEST not in skill:
    fail("qualified parent digest not pinned in model + SKILL")
if len(fixtures) != 9:
    fail(f"expected 9 semantic fixtures, got {len(fixtures)}")

ids = [x.get("id") for x in fixtures]
if len(ids) != len(set(ids)):
    fail("duplicate semantic fixture IDs")
p0 = {x.get("id") for x in fixtures if x.get("priority") == "P0"}
if p0 != EXPECTED_P0:
    fail(f"P0 set drift: {sorted(p0)}")

families = {x.get("family") for x in fixtures}
expected_families = {"EXPLAIN","DATA_TRUTH","HIERARCHY","TYPE","MOTION","COMPOSITE","REFERENCE","TOOL_ROUTE","CRITIQUE"}
if families != expected_families:
    fail(f"family set drift: {sorted(families)}")

if EXPECTED_SOURCE_SHA not in practical:
    fail("real-media fixture SHA-256 binding missing")
if "FFmpeg primitive" not in practical and "drawtext/drawbox" not in practical:
    fail("renderer limitation gate missing")
if "Cyrillic" not in practical and "glyph" not in practical.lower():
    fail("Cyrillic/glyph gate missing")
if "independent perceptual" not in plan.lower() and "independent judgments" not in plan.lower():
    fail("independent perceptual review requirement missing")
if "competitor" not in model.lower():
    fail("reference anti-imitation rule missing")
if "fabricated" not in model.lower() or "quantitative" not in model.lower():
    fail("information-integrity hard rule missing")
if "Do not output `QUALIFIED`" not in skill:
    fail("qualification status ceiling missing")

digest = hashlib.sha256((model + "\n---SKILL---\n" + skill).encode("utf-8")).hexdigest()

print(json.dumps({
    "status": "PASS",
    "candidate_assembly_digest": f"sha256:{digest}",
    "semantic_fixture_count": len(fixtures),
    "p0_fixtures": sorted(p0),
    "families": sorted(families),
    "parent_digest": PARENT_DIGEST,
    "practical_source_sha256": EXPECTED_SOURCE_SHA,
    "model_calls": 0
}, ensure_ascii=False, indent=2))
