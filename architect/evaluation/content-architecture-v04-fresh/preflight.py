#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PREREG=ROOT/"preregistration-v0.1.json"
EXPECTED_CANDIDATE="5d440e1bf3e20fbd35c6ab276310a904e36cc06d"

def sha256(path: Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(65536),b""): h.update(chunk)
    return h.hexdigest()

def fail(msg): raise SystemExit("NOT EXECUTABLE: "+msg)

def safe(rel):
    p=(ROOT/rel).resolve(); p.relative_to(ROOT.resolve()); return p

def main():
    p=json.loads(PREREG.read_text())
    if p.get("candidate_blob_sha")!=EXPECTED_CANDIDATE: fail("candidate identity changed")
    if p.get("status")!="DISPATCHABLE_FROZEN": fail("preregistration is not DISPATCHABLE_FROZEN")
    grader=p.get("grader_contract") or {}; hidden=p.get("hidden_corpus") or {}
    for k in ("implementation_path","implementation_blob_sha","calibration_evidence_path","runner_path"):
        if not grader.get(k): fail("grader contract incomplete: "+k)
    if grader.get("status")!="FROZEN_EXECUTABLE": fail("grader not frozen executable")
    impl=safe(grader["implementation_path"]); cal=safe(grader["calibration_evidence_path"]); runner=safe(grader["runner_path"])
    if not impl.is_file() or not cal.is_file() or not runner.is_file(): fail("grader/calibration/runner file missing")
    if sha256(impl)!=grader["implementation_blob_sha"].removeprefix("sha256:"): fail("grader digest mismatch")
    if hidden.get("status")!="FROZEN_GENERATED_SEALED": fail("hidden corpus not frozen generated sealed")
    if not hidden.get("identity_sha256") or int(hidden.get("fixture_count",0))<1: fail("hidden corpus identity missing")
    author=safe(hidden.get("author_path",""))
    if not author.is_file(): fail("hidden corpus author missing")
    if sha256(author)!=hidden.get("author_sha256"): fail("hidden corpus author digest mismatch")
    if p.get("p0_hard_failures_allowed")!=0: fail("P0 threshold drift")
    if p.get("deterministic_invariant_pass_rate")!=1.0: fail("deterministic invariant threshold drift")
    if p.get("runtime_eligibility",{}).get("provider_backed_calls_allowed_before_dispatchable") is not False: fail("provider-spend guard drift")
    print(json.dumps({"status":"PASS","gate_id":p["gate_id"],"candidate_blob_sha":p["candidate_blob_sha"],"grader_sha256":sha256(impl),"hidden_corpus_sha256":hidden["identity_sha256"],"fixture_count":hidden["fixture_count"]},sort_keys=True))
    return 0
if __name__=="__main__": raise SystemExit(main())
