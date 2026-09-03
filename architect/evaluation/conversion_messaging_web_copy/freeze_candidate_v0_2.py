#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "agents/conversion-messaging-web-copy/0.2.0/SKILL.md"
MANIFEST = ROOT / "agents/conversion-messaging-web-copy/0.2.0/artifact-manifest.json"
EXPECTED_ASSEMBLY = "8eccb6fa161c0be33eb18ee0eb9397906a3533c6"

for p in (SKILL, MANIFEST):
    if not p.is_file():
        raise SystemExit(f"required freeze artifact missing: {p.relative_to(ROOT)}")

raw = SKILL.read_bytes()
digest = "sha256:" + hashlib.sha256(raw).hexdigest()
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
artifact = manifest.get("artifact", {})
candidate = manifest.get("candidate", {})

if artifact.get("paths") != ["agents/conversion-messaging-web-copy/0.2.0/SKILL.md"]:
    raise SystemExit("artifact path binding mismatch")
if artifact.get("content_digest") != digest:
    raise SystemExit("candidate content digest mismatch")
if candidate.get("version") != "0.2.0-candidate":
    raise SystemExit("candidate version mismatch")
if candidate.get("assembly_merge_commit") != EXPECTED_ASSEMBLY:
    raise SystemExit("candidate assembly commit mismatch")
if candidate.get("qualification_status") != "UNQUALIFIED_CANDIDATE":
    raise SystemExit("freeze must not claim qualification PASS")

print(json.dumps({
    "status": "PASS",
    "candidate_path": str(SKILL.relative_to(ROOT)),
    "content_digest": digest,
    "bytes": len(raw),
    "assembly_merge_commit": EXPECTED_ASSEMBLY,
    "model_calls": 0,
    "scored_calls": 0,
    "paid_api_calls": 0,
}, sort_keys=True))
