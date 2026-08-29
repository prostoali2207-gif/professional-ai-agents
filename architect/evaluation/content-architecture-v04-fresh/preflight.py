#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREREG = ROOT / "preregistration-v0.1.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(msg: str) -> None:
    raise SystemExit("NOT EXECUTABLE: " + msg)


def main() -> int:
    p = json.loads(PREREG.read_text(encoding="utf-8"))
    if p.get("candidate_blob_sha") != "5d440e1bf3e20fbd35c6ab276310a904e36cc06d":
        fail("candidate identity changed")
    if p.get("status") != "DISPATCHABLE_FROZEN":
        fail("preregistration is not DISPATCHABLE_FROZEN")

    grader = p.get("grader_contract") or {}
    hidden = p.get("hidden_corpus") or {}
    required_grader = ("implementation_path", "implementation_blob_sha", "calibration_evidence_path")
    missing = [k for k in required_grader if not grader.get(k)]
    if missing:
        fail("grader contract incomplete: " + ",".join(missing))
    if grader.get("status") != "FROZEN_EXECUTABLE":
        fail("grader implementation is not frozen executable")

    impl = (ROOT / grader["implementation_path"]).resolve()
    if ROOT.resolve() not in impl.parents and impl != ROOT.resolve():
        fail("grader implementation path escapes evaluator root")
    if not impl.is_file():
        fail("grader implementation missing")
    if sha256(impl) != grader["implementation_blob_sha"].removeprefix("sha256:"):
        fail("grader implementation digest mismatch")

    calibration = (ROOT / grader["calibration_evidence_path"]).resolve()
    if not calibration.is_file():
        fail("grader calibration evidence missing")

    if not hidden.get("identity_sha256") or not hidden.get("sealed_transport_path"):
        fail("fresh hidden corpus identity/transport is missing")
    if hidden.get("status") != "FROZEN_SEALED":
        fail("fresh hidden corpus is not frozen sealed")
    transport = (ROOT / hidden["sealed_transport_path"]).resolve()
    if ROOT.resolve() not in transport.parents and transport != ROOT.resolve():
        fail("sealed transport path escapes evaluator root")
    if not transport.exists():
        fail("sealed transport missing")

    if p.get("p0_hard_failures_allowed") != 0:
        fail("P0 threshold drift")
    if p.get("deterministic_invariant_pass_rate") != 1.0:
        fail("deterministic invariant threshold drift")
    if p.get("runtime_eligibility", {}).get("provider_backed_calls_allowed_before_dispatchable") is not False:
        fail("provider-spend guard drift")

    print(json.dumps({
        "status": "PASS",
        "gate_id": p["gate_id"],
        "candidate_blob_sha": p["candidate_blob_sha"],
        "grader_sha256": sha256(impl),
        "hidden_corpus_sha256": hidden["identity_sha256"]
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
