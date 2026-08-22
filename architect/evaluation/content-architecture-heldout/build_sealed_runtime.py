#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, zipfile
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

EXPECTED = {
  "preregistration-v0.1.json":"9038358b8c372e0f1ac2ece6313b4a2f4e7d97fbde08c57f753472d65ef92e13",
  "fixtures-v0.1.json":"9e15999dc114c2b0c7c008b5aceceeb539092d04b154a70c8f4ba03c6538f58e",
  "grader-key-v0.1.json":"cf926b173ceff19dcca35c4c67ef61405b6910f5dcb3cb42d705100e1e7c617e"
}
CANDIDATE_SHA="67ac707be93cd46c0303c54eef3d73122c72c876"
STOCHASTIC={"F2","F5","F6","F11","F12"}

def sha(path: Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--parts-dir", required=True)
    ap.add_argument("--out", required=True)
    args=ap.parse_args()
    key=os.environ.get("CONTENT_ARCHITECTURE_SEALED_PACK_KEY","").strip().encode()
    if not key:
        raise SystemExit("CONTENT_ARCHITECTURE_SEALED_PACK_KEY missing")
    parts_dir=Path(args.parts_dir)
    token=b"".join(p.read_bytes() for p in sorted(parts_dir.iterdir()) if p.is_file())
    if hashlib.sha256(token).hexdigest()!="d1d0fff046dfe0dae03e27a33cb5393a9d7e74b9a10d08bf4c20cf22a2f2b679":
        raise SystemExit("ciphertext digest mismatch")
    try:
        raw=Fernet(key).decrypt(token)
    except (InvalidToken, ValueError):
        raise SystemExit("sealed pack decryption failed")
    if hashlib.sha256(raw).hexdigest()!="9e13ee455e282ea32ea010260252af6aa9612450478d90853e2e45a6de98ac2e":
        raise SystemExit("decrypted zip digest mismatch")
    out=Path(args.out); out.mkdir(parents=True, exist_ok=True)
    zpath=out/"sealed.zip"; zpath.write_bytes(raw)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(out)
    for name, expected in EXPECTED.items():
        if sha(out/name)!=expected:
            raise SystemExit(f"restored sealed component mismatch: {name}")
    prereg=json.loads((out/"preregistration-v0.1.json").read_text())
    if prereg["candidate"]["blob_sha"]!=CANDIDATE_SHA:
        raise SystemExit("candidate binding mismatch")
    fixture_pack=json.loads((out/"fixtures-v0.1.json").read_text())
    fixture_dir=out/"protocol-fixtures"; fixture_dir.mkdir(exist_ok=True)
    metas=[]
    for item in fixture_pack["fixtures"]:
        if not item["id"].startswith("H"):
            continue
        payload={"candidate_input":{"task":item["scenario"]}}
        p=fixture_dir/f'{item["id"]}.json'
        p.write_text(json.dumps(payload,ensure_ascii=False,sort_keys=True),encoding="utf-8")
        metas.append({
          "id":item["id"], "family":item["family"], "priority":"P0/P1",
          "path":str(p.relative_to(out)),
          "sha256":sha(p),
          "trial_count":3 if item["family"] in STOCHASTIC else 1
        })
    manifest={
      "candidate_sha":CANDIDATE_SHA,
      "runner_version":"2",
      "trial_count":1,
      "fixtures":metas,
      "thresholds":prereg["thresholds"],
      "capability_profile":{"live_retrieval":False,"external_tools":False},
      "evaluator_class":"independent-held-out",
      "sealed_component_hashes":EXPECTED,
      "evaluation_id":prereg["evaluation_id"]
    }
    (out/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"status":"PASS","fixture_count":len(metas),"candidate_sha":CANDIDATE_SHA,"component_hashes":EXPECTED},sort_keys=True))
if __name__=="__main__":
    main()
