#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OLD = json.loads((HERE / "issue225-sealed-prerequisite-prereg-v0.1.json").read_text(encoding="utf-8"))
NEW = json.loads((HERE / "issue225-sealed-prerequisite-prereg-v0.2.json").read_text(encoding="utf-8"))
RUNNER = HERE / "issue225_codex_author_review_seal_v0_3.py"
BASE = HERE / "issue225_codex_author_review_seal_v0_2.py"

checks = 0

def check(cond: bool, message: str) -> None:
    global checks
    if not cond:
        raise RuntimeError(message)
    checks += 1

# Professional construct and candidate identity must be byte-for-byte equivalent as data.
check(NEW["candidate"] == OLD["candidate"], "candidate drift")
check(NEW["construct"] == OLD["construct"], "construct/threshold drift")
check(NEW["authoring"] == OLD["authoring"], "author/reviewer drift")
check(NEW["runtime_isolation"] == OLD["runtime_isolation"], "runtime isolation drift")
check(NEW["retry_policy"] == OLD["retry_policy"], "retry policy drift")
check(NEW["budget_gate"] == OLD["budget_gate"], "budget gate drift")
check(NEW["cycle_id"].endswith("codex-r2"), "r2 cycle id not fresh")
check(NEW.get("supersedes_unexecuted_cycle") == OLD["cycle_id"], "supersession binding missing")

sealing = NEW["sealing"]
check(sealing.get("key_mode") == "direct-per-cycle-key-env", "direct key mode not frozen")
check(sealing.get("key_env") == "MESSAGING_ISSUE225_SEALED_PACK_KEY", "unexpected key env")
check("master_env" not in sealing and "key_derivation" not in sealing, "shared master dependency remains")
check(sealing.get("secret_visible_to_author_or_reviewer") is False, "secret visibility must be false")

source = RUNNER.read_text(encoding="utf-8")
for bad in ("urllib.request", "api.openai.com", "generativelanguage.googleapis.com", "api.groq.com", "api.anthropic.com"):
    check(bad not in source, f"metered API transport present: {bad}")
for required in ("MESSAGING_ISSUE225_SEALED_PACK_KEY", "key_bytes(p)", "base.cli_facts()", "base.invoke", "Fernet(key).encrypt", '"key_env": key_env'):
    check(required in source, f"missing direct-key transport invariant: {required}")

# Verify the inherited child-environment sanitizer strips the new secret before author/reviewer Codex calls.
spec = importlib.util.spec_from_file_location("issue225_base", BASE)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot import issue225 base")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
os.environ[sealing["key_env"]] = "test-secret-must-not-reach-child"
child = base.clean_env()
check(sealing["key_env"] not in child, "direct pack key leaks into child Codex environment")
os.environ.pop(sealing["key_env"], None)

# Verify generic qualification-platform direct-key resolver remains compatible with the frozen key_env shape.
sys.path.insert(0, str(ROOT / "architect/evaluation/qualification-platform"))
from sealed_pack_keys import resolve_effective_key
valid_key = b"MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA="
os.environ[sealing["key_env"]] = valid_key.decode()
resolved = resolve_effective_key({"key_env": sealing["key_env"]})
check(resolved == valid_key, "generic direct-key resolver incompatibility")
os.environ.pop(sealing["key_env"], None)

print(json.dumps({
    "status": "PASS",
    "checks": checks,
    "model_calls": 0,
    "candidate_calls": 0,
    "scored_calls": 0,
    "paid_api_calls": 0,
    "old_cycle": OLD["cycle_id"],
    "new_cycle": NEW["cycle_id"],
}, sort_keys=True))
