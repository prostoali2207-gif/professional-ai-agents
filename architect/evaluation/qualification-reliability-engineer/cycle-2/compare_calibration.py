#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from collections import Counter, defaultdict
from pathlib import Path
from validate_blind_judgments import validate

HERE=Path(__file__).resolve().parent
KEY=HERE.parent / "stage-b/calibration-reference-v0.1.md"

ROW=re.compile(r"^\| (B1-\d+) \| (R\d+) \| ([A-Z_]+) \| ([^\n]+) \| ([^\n]+) \|$",re.M)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("judgments")
    ap.add_argument("--expected-seal",required=True)
    args=ap.parse_args()
    data=json.loads(Path(args.judgments).read_bytes())
    validate(data)
    import hashlib
    canonical=json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
    got=hashlib.sha256(canonical).hexdigest()
    if got!=args.expected_seal:
        raise SystemExit(f"blind checkpoint seal mismatch: {got}")

    rows=ROW.findall(KEY.read_text(encoding="utf-8"))
    if len(rows)!=48:
        raise SystemExit(f"author key expected 48 rows, got {len(rows)}")
    author={rid:{"case_id":cid,"level":level,"p0":re.findall(r"P0-\d+",triggers)} for cid,rid,level,_,triggers in rows}
    blind={j["reference_id"]:j for j in data["judgments"]}
    if set(author)!=set(blind):
        raise SystemExit("author/blind reference mismatch")

    confusion=Counter()
    mismatches=[]
    unsafe_total=unsafe_rejected=0
    go_total=go_accepted=0
    over_total=over_not_promoted=0
    for rid,a in author.items():
        b=blind[rid]
        confusion[(a["level"],b["predicted_level"])]+=1
        if a["level"]!=b["predicted_level"]:
            mismatches.append({"reference_id":rid,"author_level":a["level"],"blind_level":b["predicted_level"],"release_eligible":b["release_eligible"],"blind_p0":b["p0_triggers"],"author_p0":a["p0"]})
        if a["level"]=="UNSAFE_NAIVE":
            unsafe_total+=1
            if b["release_eligible"] is False and b["p0_triggers"]:
                unsafe_rejected+=1
        if a["level"]=="CORRECT_GO_CONTROL":
            go_total+=1
            if b["release_eligible"] is True:
                go_accepted+=1
        if a["level"]=="OVERENGINEERED":
            over_total+=1
            if b["predicted_level"] not in {"STAFF_STRONG","CORRECT_GO_CONTROL"}:
                over_not_promoted+=1

    out={
        "status":"DETERMINISTIC_COMPARISON_COMPLETE_NOT_CALIBRATION_VERDICT",
        "blind_checkpoint_sha256":got,
        "exact_level_matches":sum(v for (a,b),v in confusion.items() if a==b),
        "total":48,
        "unsafe_p0_rejected":f"{unsafe_rejected}/{unsafe_total}",
        "correct_go_accepted":f"{go_accepted}/{go_total}",
        "overengineered_not_promoted":f"{over_not_promoted}/{over_total}",
        "confusion":[{"author":a,"blind":b,"count":n} for (a,b),n in sorted(confusion.items())],
        "mismatches":mismatches,
    }
    print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
