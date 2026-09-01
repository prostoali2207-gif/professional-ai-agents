#!/usr/bin/env python3
from __future__ import annotations

import argparse, base64, hashlib, hmac, json, os, re
from pathlib import Path
from cryptography.fernet import Fernet

GATE_ID = "content-architecture-v0.4-codex-targeted-2026-09-01-r4"
CANDIDATE_SHA = "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
P0_FAMILY = "P0"
PER_FAMILY_MIN = 0.80
AGGREGATE_MIN = 0.90
DETERMINISTIC_INVARIANT_MIN = 1.0


def canon(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def derive(master: bytes, label: bytes) -> bytes:
    return hmac.new(master, GATE_ID.encode() + b"|" + label, hashlib.sha256).digest()


def load_pack(path: Path):
    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode()
    if not master:
        raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    key = base64.urlsafe_b64encode(derive(master, b"fernet"))
    plain = Fernet(key).decrypt(path.read_bytes())
    data = json.loads(plain)
    if data.get("gate_id") != GATE_ID or data.get("candidate_sha") != CANDIDATE_SHA:
        raise RuntimeError("sealed pack identity mismatch")
    if not isinstance(data.get("contracts"), dict):
        raise RuntimeError("sealed pack missing visible output contracts")
    return data


def parse_candidate(text: str):
    text = (text or "").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1]).strip()
    try:
        obj = json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, re.S)
        if not m:
            raise ValueError("candidate output does not contain JSON object")
        obj = json.loads(m.group(0))
    if not isinstance(obj, dict):
        raise ValueError("candidate output is not a JSON object")
    return obj


def validate_visible_contract(obj: dict, contract: dict):
    failures = []
    for field, spec in contract.items():
        if field not in obj:
            failures.append(f"missing published field {field}")
            continue
        actual = obj[field]
        typ = spec.get("type")
        if typ == "string":
            if not isinstance(actual, str) or actual not in spec.get("allowed", []):
                failures.append(f"{field} outside published vocabulary")
        elif typ == "boolean":
            if not isinstance(actual, bool):
                failures.append(f"{field} not boolean")
        elif typ == "number":
            if isinstance(actual, bool) or not isinstance(actual, (int, float)):
                failures.append(f"{field} not number")
            else:
                if actual < spec.get("min", float("-inf")):
                    failures.append(f"{field} below published minimum")
                if "max" in spec and actual > spec["max"]:
                    failures.append(f"{field} above published maximum")
        elif typ == "list":
            allowed = spec.get("allowed_items", [])
            if not isinstance(actual, list):
                failures.append(f"{field} not list")
            else:
                if len(actual) < int(spec.get("min_items", 0)):
                    failures.append(f"{field} shorter than published minimum")
                if any(item not in allowed for item in actual):
                    failures.append(f"{field} contains value outside published vocabulary")
        else:
            failures.append(f"{field} has invalid evaluator contract type")
    return failures


def grade_fields(obj: dict, exp: dict):
    failures = []
    for key, val in exp.items():
        if key == "family":
            continue
        if key.endswith("_contains"):
            field = key[:-9]
            actual = obj.get(field)
            if not isinstance(actual, list) or not all(x in actual for x in val):
                failures.append(f"{field} missing required members")
        elif key.endswith("_exact"):
            field = key[:-6]
            if obj.get(field) != val:
                failures.append(f"{field} decision/order mismatch")
        elif key.endswith("_min"):
            field = key[:-4]
            actual = obj.get(field)
            if isinstance(actual, bool) or not isinstance(actual, (int, float)) or actual < val:
                failures.append(f"{field} below decision minimum")
        elif isinstance(val, list):
            if obj.get(key) not in val:
                failures.append(f"{key} professional decision mismatch")
        else:
            if obj.get(key) != val:
                failures.append(f"{key} professional decision mismatch")
    return failures


def grade_record(record: dict, pack: dict):
    fid = record.get("fixture_id")
    base = {"fixture_id": fid, "family": None, "pass": False, "mechanical_pass": False, "p0": False, "mechanical_failures": [], "decision_failures": []}
    if fid not in pack.get("expectations", {}) or fid not in pack.get("contracts", {}):
        base["mechanical_failures"] = ["unknown fixture"]
        return base
    exp = pack["expectations"][fid]
    base["family"] = exp.get("family")
    if record.get("candidate_sha") != CANDIDATE_SHA:
        base["mechanical_failures"] = ["candidate identity mismatch"]
        return base
    if record.get("gate_id") != GATE_ID:
        base["mechanical_failures"] = ["gate identity mismatch"]
        return base
    if record.get("terminal_status") != "COMPLETED":
        base["mechanical_failures"] = ["record not completed"]
        return base
    try:
        obj = parse_candidate(record.get("final_response", ""))
    except Exception as exc:
        base["mechanical_failures"] = [f"invalid structured output: {type(exc).__name__}"]
        return base
    mechanical = validate_visible_contract(obj, pack["contracts"][fid])
    decision = grade_fields(obj, exp)
    base["mechanical_failures"] = mechanical
    base["decision_failures"] = decision
    base["mechanical_pass"] = not mechanical
    base["pass"] = not mechanical and not decision
    base["p0"] = exp.get("family") == P0_FAMILY and bool(mechanical or decision)
    return base


def expected_trial_keys(pack: dict):
    keys = []
    for fixture in pack["fixtures"]:
        for trial in range(1, int(fixture.get("trial_count", 1)) + 1):
            keys.append((fixture["fixture_id"], trial))
    return keys


def summarize(results: list[dict], records: list[dict], pack: dict):
    expected = expected_trial_keys(pack)
    actual = [(r.get("fixture_id"), int(r.get("trial", 0))) for r in records]
    complete = len(actual) == len(expected) and len(actual) == len(set(actual)) and set(actual) == set(expected)

    by_family: dict[str, list[dict]] = {}
    for result in results:
        by_family.setdefault(result.get("family"), []).append(result)

    p0_count = sum(1 for r in results if r.get("p0"))
    invariant_rate = sum(1 for r in results if r.get("mechanical_pass")) / len(results) if results else 0.0
    family_rates = {
        fam: sum(1 for r in rows if r.get("pass")) / len(rows)
        for fam, rows in by_family.items()
        if fam != P0_FAMILY
    }
    p1 = [r for r in results if r.get("family") != P0_FAMILY]
    aggregate = sum(1 for r in p1 if r.get("pass")) / len(p1) if p1 else 0.0

    repeats_ok = True
    grouped: dict[str, list[bool]] = {}
    trial_counts: dict[str, int] = {}
    for record, result in zip(records, results):
        fid = str(record.get("fixture_id"))
        grouped.setdefault(fid, []).append(bool(result.get("pass")))
        trial_counts[fid] = int(record.get("trial_count", 1))
    for fid, count in trial_counts.items():
        if count > 1 and (len(grouped.get(fid, [])) != count or not all(grouped[fid])):
            repeats_ok = False

    release = (
        complete
        and p0_count == 0
        and invariant_rate >= DETERMINISTIC_INVARIANT_MIN
        and len(family_rates) == 12
        and all(rate >= PER_FAMILY_MIN for rate in family_rates.values())
        and aggregate >= AGGREGATE_MIN
        and repeats_ok
    )
    return {
        "gate_id": GATE_ID,
        "candidate_sha": CANDIDATE_SHA,
        "records_complete": complete,
        "expected_trial_records": len(expected),
        "actual_trial_records": len(records),
        "p0_count": p0_count,
        "deterministic_invariant_pass_rate": invariant_rate,
        "family_pass_rates": family_rates,
        "aggregate_p1_pass_rate": aggregate,
        "repeats_all_pass": repeats_ok,
        "verdict": "PASS" if release else "REVISE",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--records", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    pack = load_pack(Path(args.pack))
    records = [json.loads(line) for line in Path(args.records).read_text(encoding="utf-8").splitlines() if line.strip()]
    if any(r.get("terminal_status") == "PENDING_EXTERNAL_GRADER" for r in records):
        raise SystemExit("invalid terminal status PENDING_EXTERNAL_GRADER")
    results = [grade_record(r, pack) for r in records]
    summary = summarize(results, records, pack)
    report = {"summary": summary, "results": results, "grader": {"version": "r4-v1", "mode": "visible-contract-deterministic-professional-decision-verifier"}}
    Path(args.out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
