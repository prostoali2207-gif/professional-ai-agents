#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

GATE_ID = "content-architecture-v0.4-practical-handoff-2026-09-02-r1"
FIXTURE_SHA = "9a9cbc3ecec8acaa1f3f6fa76d7311e584202f43"

ANALYST_CORE_SHA = "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
ANALYST_SPECIALIZATION_SHA = "7f41c2d1ba40c3b4c59e3eba2fb264c04162c320"
ANALYST_BINDING_SHA = "82694481f857e9c318317adc0cf81b6e50d877e2"
ANALYST_SCHEMA_SHA = "35bddc15f19ce4af666247cd2dd229c7a7eabe34"

CREATOR_MANIFEST_SHA = "0fcc7bed521aa575a126ee1eea2b28a29a38ad77"
CREATOR_CORE_MODEL_SHA = "d8eee4c6f9141f362d91a340c37dcae6ad6bfa71"
CREATOR_BINDING_SHA = "8b2b5ef822387f4e1f006dc036a08f2e42113d1f"
CREATOR_SPECIALIZATION_SHA = "01fa57c40d01a79752af1a7f7f5290859521615b"
CREATOR_BRIDGE_SHA = "845959e914b2db531f7507b2a1f14b6987767bfa"
CREATOR_SCHEMA_SHA = "7fea2f60b87198ec2f7ee15cd34c84260914ff2f"

ADAPTER = Path("architect/evaluation/harness/adapters/codex_frozen_artifact_adapter.py")
POSITIVE_UNSUPPORTED = [
    "accident free", "no accident", "original paint", "one owner",
    "full service history", "guaranteed", "lowest price", "best price",
    "finance available", "installments available", "discounted", "limited time"
]


def canon(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def parse_json(text: str) -> dict:
    text = (text or "").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1]).strip()
    try:
        obj = json.loads(text)
    except Exception:
        s, e = text.find("{"), text.rfind("}")
        if s < 0 or e <= s:
            raise ValueError("no JSON object in model output")
        obj = json.loads(text[s:e + 1])
    if not isinstance(obj, dict):
        raise ValueError("model output is not a JSON object")
    return obj


def git_blob(sha: str) -> str:
    kind = subprocess.run(["git", "cat-file", "-t", sha], capture_output=True, text=True)
    if kind.returncode != 0 or kind.stdout.strip() != "blob":
        raise RuntimeError(f"missing frozen blob {sha}")
    p = subprocess.run(["git", "cat-file", "-p", sha], capture_output=True, text=False)
    if p.returncode != 0:
        raise RuntimeError(f"cannot read frozen blob {sha}")
    return p.stdout.decode("utf-8")


def materialize(parts: list[tuple[str, str]], label: str) -> tuple[str, str]:
    chunks = []
    for name, sha in parts:
        chunks.append(f"--- BEGIN {name} ({sha}) ---\n{git_blob(sha).rstrip()}\n--- END {name} ---")
    text = "\n\n".join(chunks) + "\n"
    p = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=text.encode("utf-8"), capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"cannot materialize {label}")
    blob_sha = p.stdout.decode().strip()
    identity = hashlib.sha256((label + "|" + "|".join(sha for _, sha in parts) + "|" + blob_sha).encode()).hexdigest()
    return blob_sha, identity


def call_artifact(sha: str, task: str, workspace: Path, timeout: int) -> dict:
    workspace.mkdir(parents=True, exist_ok=True)
    payload = {
        "protocol_version": 2,
        "candidate_sha": sha,
        "workspace": str(workspace.resolve()),
        "input": {"task": task, "allowed_resources": [], "fixture_tools": {}, "max_tool_rounds": 2},
    }
    p = subprocess.run(
        [sys.executable, str(ADAPTER)],
        input=json.dumps(payload), capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=timeout + 30,
    )
    if p.returncode != 0:
        raise RuntimeError("artifact runtime failed: " + ((p.stdout or "") + "\n" + (p.stderr or ""))[-1800:])
    raw = parse_json(p.stdout)
    if raw.get("status") != "completed":
        raise RuntimeError("artifact runtime did not complete")
    if (raw.get("candidate_identity") or {}).get("sha") != sha:
        raise RuntimeError("artifact identity mismatch")
    return raw


def schema_type_ok(value, expected) -> bool:
    if isinstance(expected, list):
        return any(schema_type_ok(value, x) for x in expected)
    if expected == "object": return isinstance(value, dict)
    if expected == "array": return isinstance(value, list)
    if expected == "string": return isinstance(value, str)
    if expected == "boolean": return isinstance(value, bool)
    if expected == "integer": return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number": return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null": return value is None
    return True


def validate_schema(schema: dict, value, path: str = "$") -> list[str]:
    failures: list[str] = []
    st = schema.get("type")
    if st is not None and not schema_type_ok(value, st):
        return [f"{path}: type"]
    if "enum" in schema and value not in schema["enum"]:
        failures.append(f"{path}: enum")
    if isinstance(value, str) and "minLength" in schema and len(value) < schema["minLength"]:
        failures.append(f"{path}: minLength")
    if isinstance(value, (int, float)) and not isinstance(value, bool) and "minimum" in schema and value < schema["minimum"]:
        failures.append(f"{path}: minimum")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            failures.append(f"{path}: minItems")
        if schema.get("uniqueItems") and len({canon(x) for x in value}) != len(value):
            failures.append(f"{path}: uniqueItems")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, item in enumerate(value):
                failures.extend(validate_schema(item_schema, item, f"{path}[{i}]"))
    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                failures.append(f"{path}.{key}: required")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    failures.append(f"{path}.{key}: additionalProperty")
        for key, item in value.items():
            if key in props:
                failures.extend(validate_schema(props[key], item, f"{path}.{key}"))
    return failures


def analyst_task(fixture: dict) -> str:
    return (
        "FINAL PRACTICAL HANDOFF. This is synthetic evaluation data, not a live business offer.\n"
        "Act only as the frozen Content Architecture / Content Analyst composition.\n"
        "Return ONLY one JSON object valid against the v2 output contract embedded in your artifact.\n"
        "The input is complete: produce READY_FOR_CREATOR. Preserve experiment_id exactly, tested variable exactly as DISCLOSURE_TIMING, and every LOCK_* id verbatim in locked_variables and creator_handoff.must_preserve.\n"
        "Use only the supplied synthetic fact_ids for proof. Do not invent condition/history/finance/warranty/value claims. Exact public wording, script, caption, shots and CTA phrasing belong to Content Creator. Do not take Analytics, Strategist, post-production or publishing authority.\n"
        "The approved CTA destination is fixed; preserve it exactly. Keep asset_gaps empty because the fixture supplies required proof assets.\n\n"
        "SYNTHETIC STRATEGY + FACT PACKET:\n" + json.dumps(fixture, ensure_ascii=False, indent=2)
    )


def creator_task(fixture: dict, spec: dict) -> str:
    return (
        "FINAL PRACTICAL HANDOFF DOWNSTREAM ACCEPTANCE. This is synthetic evaluation data, not a live business offer.\n"
        "Act as the qualified Social Content Creative core with the UAE specialization and the Content Analyst v0.4 compatibility bridge embedded in your artifact.\n"
        "Consume the exact v2 Content Analyst spec below. Return ONLY one JSON object valid against creator-deliverable.schema.json embedded in your artifact.\n"
        "Return READY_FOR_REVIEW. Preserve experiment_id/content_spec_id, upstream block IDs and order, tested variable/locks, proof scope, and the single Instagram DM keyword TESTCAR CTA. Use variant_id DISCLOSURE_EARLY and tracking.vehicle_ids [\"SYN-UNIT-001\"].\n"
        "You own exact script/copy/shot execution, but may not change strategy, offer, CTA destination, proof scope or experiment controls. Every material factual claim must map to a supplied CONFIRMED fact_id. No MATERIAL or INVALIDATES_TEST deviation is acceptable.\n\n"
        "SYNTHETIC FACT/PRODUCTION PACKET:\n" + json.dumps({"facts": fixture["facts"], "production_constraints": fixture["production_constraints"]}, ensure_ascii=False, indent=2)
        + "\n\nCONTENT ANALYST V2 SPEC:\n" + json.dumps(spec, ensure_ascii=False, indent=2)
    )


def public_text_from_creator(obj: dict) -> str:
    parts = [obj.get("final_script_or_copy") or "", obj.get("cta") or "", obj.get("caption") or ""]
    for row in obj.get("onscreen_text") or []:
        if isinstance(row, dict): parts.append(row.get("text") or "")
    return "\n".join(parts).lower()


def accept_analyst(fixture: dict, obj: dict) -> list[str]:
    failures = validate_schema(json.loads(git_blob(ANALYST_SCHEMA_SHA)), obj)
    strategy = fixture["strategy"]
    if obj.get("status") != "READY_FOR_CREATOR": failures.append("analyst.status")
    if obj.get("experiment_id") != strategy["experiment_id"]: failures.append("analyst.experiment_id")
    cm = obj.get("constraint_model") or {}
    if cm.get("tested_variable") != "DISCLOSURE_TIMING": failures.append("analyst.tested_variable")
    locks = set(cm.get("locked_variables") or [])
    required = set(fixture["required_lock_ids"])
    if not required.issubset(locks): failures.append("analyst.locked_variables")
    handoff = obj.get("creator_handoff") or {}
    if not required.issubset(set(handoff.get("must_preserve") or [])): failures.append("analyst.creator_handoff.must_preserve")
    objective = obj.get("content_objective") or {}
    if objective.get("platform") != ["INSTAGRAM"]: failures.append("analyst.platform")
    if objective.get("primary_funnel_role") != "LEAD": failures.append("analyst.funnel_role")
    cta = obj.get("offer_and_cta") or {}
    if cta.get("cta_destination") != strategy["cta_destination"]: failures.append("analyst.cta_destination")
    if (obj.get("visual_communication_requirements") or {}).get("asset_gaps") != []: failures.append("analyst.asset_gaps")
    fact_ids = {x["fact_id"] for x in fixture["facts"]}
    for i, row in enumerate(obj.get("proof_architecture") or []):
        ref = row.get("evidence_reference") if isinstance(row, dict) else None
        if ref not in fact_ids: failures.append(f"analyst.proof[{i}].evidence_reference")
        claim = (row.get("claim_or_implication") or "").lower() if isinstance(row, dict) else ""
        for phrase in POSITIVE_UNSUPPORTED:
            if phrase in claim: failures.append(f"analyst.unsupported_claim:{phrase}")
    forbidden_keys = {"primary_kpi", "success_threshold", "failure_threshold", "minimum_sample", "test_window", "decision_rule", "analytics_handoff", "final_script_or_copy", "caption", "shot_list"}
    if forbidden_keys.intersection(obj): failures.append("analyst.authority_or_copy_takeover")
    return sorted(set(failures))


def accept_creator(fixture: dict, spec: dict, obj: dict) -> list[str]:
    failures = validate_schema(json.loads(git_blob(CREATOR_SCHEMA_SHA)), obj)
    if obj.get("status") != "READY_FOR_REVIEW": failures.append("creator.status")
    if obj.get("experiment_id") != fixture["strategy"]["experiment_id"]: failures.append("creator.experiment_id")
    if obj.get("content_spec_id") != spec.get("content_spec_id"): failures.append("creator.content_spec_id")
    if obj.get("variant_id") != fixture["required_creator_variant_id"]: failures.append("creator.variant_id")
    if obj.get("platform") != "INSTAGRAM": failures.append("creator.platform")
    expected_blocks = [x["block_id"] for x in spec.get("structural_timeline") or []]
    actual_blocks = [x.get("block_id") for x in obj.get("block_execution") or [] if isinstance(x, dict)]
    if actual_blocks != expected_blocks: failures.append("creator.block_order")
    tracking = obj.get("tracking") or {}
    if tracking.get("experiment_id") != fixture["strategy"]["experiment_id"]: failures.append("creator.tracking.experiment_id")
    if tracking.get("content_spec_id") != spec.get("content_spec_id"): failures.append("creator.tracking.content_spec_id")
    if tracking.get("vehicle_ids") != ["SYN-UNIT-001"]: failures.append("creator.tracking.vehicle_ids")
    if "TESTCAR" not in (obj.get("cta") or ""): failures.append("creator.cta")
    for row in obj.get("deviations") or []:
        if isinstance(row, dict) and row.get("impact") in {"MATERIAL", "INVALIDATES_TEST"}: failures.append("creator.material_deviation")
    known = {x["fact_id"] for x in fixture["facts"]}
    used = set()
    for i, row in enumerate(obj.get("fact_usage") or []):
        if not isinstance(row, dict): continue
        if row.get("status") != "CONFIRMED": failures.append(f"creator.fact_usage[{i}].status")
        if row.get("fact_id") not in known: failures.append(f"creator.fact_usage[{i}].unknown")
        else: used.add(row.get("fact_id"))
    for required in ["SYN-REPAIR-001", "SYN-CTA-001"]:
        if required not in used: failures.append(f"creator.required_fact:{required}")
    serialized = canon(obj)
    if "SYN-PROOF-REPAIR-001" not in serialized: failures.append("creator.repair_proof_not_used")
    for row in obj.get("creator_checks") or []:
        if isinstance(row, dict) and row.get("result") == "FAIL": failures.append("creator_check_fail")
    public = public_text_from_creator(obj)
    for phrase in POSITIVE_UNSUPPORTED:
        if phrase in public: failures.append(f"creator.unsupported_public_claim:{phrase}")
    return sorted(set(failures))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--preflight-only", action="store_true")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    if subprocess.run(["git", "hash-object", "architect/evaluation/content-architecture-v04-practical-handoff/practical-fixture-v0.1.json"], capture_output=True, text=True).stdout.strip() != FIXTURE_SHA:
        raise SystemExit("fixture identity mismatch")
    fixture = json.loads(git_blob(FIXTURE_SHA))
    if fixture.get("gate_id") != GATE_ID: raise SystemExit("gate identity mismatch")

    analyst_sha, analyst_identity = materialize([
        ("CONTENT ARCHITECTURE CORE V0.4", ANALYST_CORE_SHA),
        ("UAE AUTOMOTIVE SPECIALIZATION V0.2", ANALYST_SPECIALIZATION_SHA),
        ("CONTENT ANALYST V0.4 BINDING", ANALYST_BINDING_SHA),
        ("CONTENT SPEC V2 OUTPUT CONTRACT", ANALYST_SCHEMA_SHA),
    ], "content-analyst-v04-practical-composition-v1")
    creator_sha, creator_identity = materialize([
        ("QUALIFIED SOCIAL CONTENT CREATIVE MANIFEST", CREATOR_MANIFEST_SHA),
        ("QUALIFIED SOCIAL CONTENT CREATIVE MODEL", CREATOR_CORE_MODEL_SHA),
        ("CONTENT CREATOR QUALIFIED CORE BINDING", CREATOR_BINDING_SHA),
        ("CONTENT CREATOR UAE SPECIALIZATION", CREATOR_SPECIALIZATION_SHA),
        ("CONTENT ANALYST V0.4 COMPATIBILITY BRIDGE", CREATOR_BRIDGE_SHA),
        ("CREATOR DELIVERABLE OUTPUT CONTRACT", CREATOR_SCHEMA_SHA),
    ], "qualified-creator-ca-v04-practical-composition-v1")

    freeze = {
        "gate_id": GATE_ID, "status": "FROZEN_PRE_SCORE", "candidate_calls": 0, "creator_calls": 0,
        "fixture_blob_sha": FIXTURE_SHA,
        "analyst_composed_blob_sha": analyst_sha, "analyst_composed_identity_sha256": analyst_identity,
        "creator_composed_blob_sha": creator_sha, "creator_composed_identity_sha256": creator_identity,
        "analyst_core_sha": ANALYST_CORE_SHA, "analyst_specialization_sha": ANALYST_SPECIALIZATION_SHA,
        "creator_core_model_sha": CREATOR_CORE_MODEL_SHA, "creator_bridge_sha": CREATOR_BRIDGE_SHA,
    }
    (out / "freeze-evidence.json").write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(freeze, sort_keys=True))
    if args.preflight_only:
        return 0

    started = time.time()
    try:
        analyst_raw = call_artifact(analyst_sha, analyst_task(fixture), out / "analyst-work", args.timeout)
        analyst_obj = parse_json(analyst_raw.get("final_output", ""))
        analyst_failures = accept_analyst(fixture, analyst_obj)
        if analyst_failures:
            report = {"gate_id": GATE_ID, "verdict": "FAIL", "stage": "CONTENT_ANALYST", "candidate_calls": 1, "creator_calls": 0, "analyst_failures": analyst_failures, "duration_s": round(time.time()-started,3)}
            (out / "qualification-report.json").write_text(json.dumps(report, indent=2, sort_keys=True)+"\n", encoding="utf-8")
            (out / "analyst-output.json").write_text(json.dumps(analyst_obj, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
            print(json.dumps(report, sort_keys=True)); return 20

        creator_raw = call_artifact(creator_sha, creator_task(fixture, analyst_obj), out / "creator-work", args.timeout)
        creator_obj = parse_json(creator_raw.get("final_output", ""))
        creator_failures = accept_creator(fixture, analyst_obj, creator_obj)
        verdict = "PASS" if not creator_failures else "FAIL"
        report = {
            "gate_id": GATE_ID, "verdict": verdict, "stage": "COMPLETE" if verdict == "PASS" else "CONTENT_CREATOR_HANDOFF",
            "candidate_calls": 1, "creator_calls": 1,
            "analyst_schema_valid": True, "analyst_acceptance_pass": True,
            "creator_acceptance_pass": not creator_failures,
            "creator_failures": creator_failures,
            "analyst_content_spec_id": analyst_obj.get("content_spec_id"),
            "analyst_composed_identity_sha256": analyst_identity,
            "creator_composed_identity_sha256": creator_identity,
            "duration_s": round(time.time()-started,3),
        }
        (out / "qualification-report.json").write_text(json.dumps(report, indent=2, sort_keys=True)+"\n", encoding="utf-8")
        (out / "analyst-output.json").write_text(json.dumps(analyst_obj, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
        (out / "creator-output.json").write_text(json.dumps(creator_obj, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
        print(json.dumps(report, sort_keys=True))
        return 0 if verdict == "PASS" else 20
    except Exception as exc:
        failure = {"gate_id": GATE_ID, "verdict": "NOT_EXECUTABLE", "candidate_calls": 0, "creator_calls": 0, "error_type": type(exc).__name__, "error": str(exc)}
        (out / "runtime-failure.json").write_text(json.dumps(failure, indent=2, sort_keys=True)+"\n", encoding="utf-8")
        print(json.dumps(failure, sort_keys=True)); return 30


if __name__ == "__main__":
    raise SystemExit(main())
