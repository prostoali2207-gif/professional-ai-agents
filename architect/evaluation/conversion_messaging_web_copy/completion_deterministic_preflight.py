#!/usr/bin/env python3
"""Deterministic completion preflight for Conversion Messaging & Web Copy 0.1.0.

This intentionally performs no model/API calls and does not inspect hidden held-out
fixtures. It proves only public/frozen identity, FULL scope, preregistered gate
invariants, and syntactic viability of the public executor/runner path.
"""

from __future__ import annotations

import hashlib
import json
import py_compile
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FROZEN_SHA = "7019f6717b1b61806f4a221a297d049a4ad3b8cb"
SKILL_PATH = "agents/conversion-messaging-web-copy/0.1.0/SKILL.md"
MANIFEST_PATH = "agents/conversion-messaging-web-copy/0.1.0/artifact-manifest.json"
EXPECTED_DIGEST = "sha256:da7662f95dcf132d9a9875849b7bb5d5d831d1d54821f0b109b543a1f299e1d2"


def git_show_bytes(ref: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return proc.stdout


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> None:
    # Gate 0a: frozen candidate object and manifest are reachable and unchanged.
    skill = git_show_bytes(FROZEN_SHA, SKILL_PATH)
    manifest_raw = git_show_bytes(FROZEN_SHA, MANIFEST_PATH)
    manifest = json.loads(manifest_raw.decode("utf-8"))

    calculated = "sha256:" + hashlib.sha256(skill).hexdigest()
    require(calculated == EXPECTED_DIGEST, f"candidate digest mismatch: {calculated}")
    require(
        manifest.get("artifact", {}).get("content_digest") == EXPECTED_DIGEST,
        "artifact manifest digest does not match frozen digest",
    )
    require(
        manifest.get("artifact", {}).get("paths") == [SKILL_PATH],
        "artifact manifest path set changed",
    )

    # Gate 0b: first-release scope remains FULL and reusable evidence remains incompatible.
    scope = json.loads(
        (ROOT / "architect/evaluation/conversion_messaging_web_copy/scope-request-v0.1.json").read_text(
            encoding="utf-8"
        )
    )
    require(scope.get("purpose") == "release", "scope purpose is not release")
    require(scope.get("full_release_required") is True, "FULL release requirement was weakened")
    require(scope.get("existing_evidence") == "incompatible", "existing evidence compatibility changed")

    # Gate 0c: public preregistration still carries the frozen release invariants.
    prereg = (
        ROOT / "architect/evaluation/conversion_messaging_web_copy/EVALUATOR-PREREGISTRATION-v0.1.md"
    ).read_text(encoding="utf-8")
    required_fragments = [
        FROZEN_SHA,
        EXPECTED_DIGEST,
        "24 work samples",
        "12 families",
        "zero hard fails",
        "at least 22/24 fixture passes",
        "MATERIAL_FABRICATION",
        "INVENTED_CUSTOMER_EVIDENCE",
        "HARMFUL_UX_CONTRADICTION",
        "UNAUTHORIZED_STRATEGY_CHANGE",
        "GUARANTEED_CAUSAL_LIFT",
        "functional_craft >= 1.25",
        "evidence_integrity >= 1.5",
        "task_clarity >= 1.5",
        "professional_judgment >= 1.5",
        "boundary_integrity >= 1.5",
        "scope is `FULL`",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in prereg]
    require(not missing, f"preregistration invariant(s) missing: {missing}")

    # Gate 1: public execution components at least parse/compile before any model spend.
    public_python = [
        "architect/evaluation/conversion_messaging_web_copy/executor_v0_1_responses.py",
        "architect/evaluation/conversion_messaging_web_copy/executor_v0_1_gemini.py",
        "architect/evaluation/conversion_messaging_web_copy/canary_v0_1.py",
        "architect/evaluation/conversion_messaging_web_copy/canary_v0_1_gemini.py",
        "architect/evaluation/conversion_messaging_web_copy/sealed_runner_template_v0_1.py",
        "architect/evaluation/conversion_messaging_web_copy/sealed_runner_template_v0_1_r2.py",
        "architect/evaluation/conversion_messaging_web_copy/author_sealed_pack_v0_1.py",
        "architect/evaluation/conversion_messaging_web_copy/author_sealed_pack_v0_1_r2.py",
    ]
    for relative in public_python:
        path = ROOT / relative
        require(path.is_file(), f"public qualification component missing: {relative}")
        py_compile.compile(str(path), doraise=True)

    print("PASS: messaging completion deterministic preflight")
    print(f"candidate={FROZEN_SHA}")
    print(f"digest={EXPECTED_DIGEST}")
    print("scope=FULL")
    print("model_calls=0")


if __name__ == "__main__":
    main()
