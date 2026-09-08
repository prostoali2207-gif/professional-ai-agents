#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLE_PATH = HERE / "blind-bundle-v0.2.json"
CYCLE = "qre-v01-cycle2-b2a-blind-review-r1"
LEVELS = {"UNSAFE_NAIVE","MECHANICAL_SHALLOW","STAFF_STRONG","OVERENGINEERED","CORRECT_GO_CONTROL"}
P0S = {f"P0-{i:02d}" for i in range(1, 11)}
TOP_KEYS = {"version","cycle","source_bundle_sha256","reviewer","judgments"}
REVIEWER_KEYS = {"fresh_context","author_key_seen","candidate_outputs_seen"}
J_KEYS = {"reference_id","predicted_level","p0_triggers","material_strengths","material_failures","uncertainty","release_eligible"}

class ValidationError(ValueError):
    pass

def _exact_keys(obj, expected, where):
    if not isinstance(obj, dict) or set(obj) != expected:
        raise ValidationError(f"{where}: keys must be exactly {sorted(expected)}")

def _strings(value, where, allow_empty=True):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValidationError(f"{where}: expected list of non-empty strings")
    if not allow_empty and not value:
        raise ValidationError(f"{where}: must not be empty")

def load_bundle():
    raw = BUNDLE_PATH.read_bytes()
    bundle = json.loads(raw)
    sha = hashlib.sha256(raw).hexdigest()
    refs = [r["reference_id"] for c in bundle["cases"] for r in c["reference_exemplars"]]
    if len(refs) != 48 or len(set(refs)) != 48:
        raise ValidationError("bundle reference identity failure")
    return bundle, sha, refs

def validate(data):
    bundle, bundle_sha, refs = load_bundle()
    _exact_keys(data, TOP_KEYS, "root")
    if data["version"] != "0.2" or data["cycle"] != CYCLE:
        raise ValidationError("version/cycle mismatch")
    if data["source_bundle_sha256"] != bundle_sha:
        raise ValidationError("source bundle SHA mismatch")
    _exact_keys(data["reviewer"], REVIEWER_KEYS, "reviewer")
    if data["reviewer"] != {"fresh_context": True, "author_key_seen": False, "candidate_outputs_seen": False}:
        raise ValidationError("reviewer independence flags invalid")
    js = data["judgments"]
    if not isinstance(js, list) or len(js) != 48:
        raise ValidationError("judgments must contain exactly 48 entries")
    seen = []
    for i, j in enumerate(js):
        _exact_keys(j, J_KEYS, f"judgments[{i}]")
        rid = j["reference_id"]
        if not isinstance(rid, str):
            raise ValidationError("reference_id must be string")
        seen.append(rid)
        if j["predicted_level"] not in LEVELS:
            raise ValidationError(f"{rid}: illegal predicted_level")
        _strings(j["p0_triggers"], f"{rid}.p0_triggers")
        if len(j["p0_triggers"]) != len(set(j["p0_triggers"])) or not set(j["p0_triggers"]) <= P0S:
            raise ValidationError(f"{rid}: illegal/duplicate P0")
        _strings(j["material_strengths"], f"{rid}.material_strengths")
        _strings(j["material_failures"], f"{rid}.material_failures")
        if not isinstance(j["uncertainty"], str):
            raise ValidationError(f"{rid}: uncertainty must be string")
        if not isinstance(j["release_eligible"], bool):
            raise ValidationError(f"{rid}: release_eligible must be boolean")
    if len(set(seen)) != 48 or set(seen) != set(refs):
        raise ValidationError("reference IDs must match bundle exactly once")
    return {"status":"PASS","bundle_sha256":bundle_sha,"judgments":48}

def validate_template(data):
    bundle, bundle_sha, refs = load_bundle()
    _exact_keys(data, TOP_KEYS, "root")
    if data["version"] != "0.2" or data["cycle"] != CYCLE or data["source_bundle_sha256"] != bundle_sha:
        raise ValidationError("template identity mismatch")
    _exact_keys(data["reviewer"], REVIEWER_KEYS, "reviewer")
    js=data["judgments"]
    if len(js)!=48:
        raise ValidationError("template must have 48 entries")
    seen=[]
    for j in js:
        _exact_keys(j,J_KEYS,"template judgment")
        seen.append(j["reference_id"])
        if j["predicted_level"]!="" or j["p0_triggers"]!=[] or j["material_strengths"]!=[] or j["material_failures"]!=[] or j["uncertainty"]!="" or j["release_eligible"] is not None:
            raise ValidationError("template placeholders mutated")
    if len(set(seen))!=48 or set(seen)!=set(refs):
        raise ValidationError("template reference IDs mismatch")
    return {"status":"TEMPLATE_PASS","bundle_sha256":bundle_sha,"judgments":48}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--template", action="store_true")
    args=ap.parse_args()
    data=json.loads(Path(args.path).read_bytes())
    result=validate_template(data) if args.template else validate(data)
    print(json.dumps(result,sort_keys=True))

if __name__=="__main__":
    main()
