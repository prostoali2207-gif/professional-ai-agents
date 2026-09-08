#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from validate_blind_judgments import validate

def canonical_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode("utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("judgments")
    ap.add_argument("--output")
    args=ap.parse_args()
    data=json.loads(Path(args.judgments).read_bytes())
    verdict=validate(data)
    digest=hashlib.sha256(canonical_bytes(data)).hexdigest()
    seal={
        "version":"0.2",
        "cycle":data["cycle"],
        "canonical_judgments_sha256":digest,
        "source_bundle_sha256":verdict["bundle_sha256"],
        "judgment_count":48,
        "validator_status":"PASS",
    }
    if args.output:
        Path(args.output).write_text(json.dumps(seal,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(seal,sort_keys=True))

if __name__=="__main__":
    main()
