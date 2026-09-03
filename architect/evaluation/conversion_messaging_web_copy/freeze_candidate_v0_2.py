#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "agents/conversion-messaging-web-copy/0.2.0/SKILL.md"

if not SKILL.is_file():
    raise SystemExit("candidate SKILL missing")

raw = SKILL.read_bytes()
print(json.dumps({
    "candidate_path": str(SKILL.relative_to(ROOT)),
    "content_digest": "sha256:" + hashlib.sha256(raw).hexdigest(),
    "bytes": len(raw),
    "model_calls": 0,
    "scored_calls": 0,
    "paid_api_calls": 0,
}, sort_keys=True))
