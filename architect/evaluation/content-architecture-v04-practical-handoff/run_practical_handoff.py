#!/usr/bin/env python3
from __future__ import annotations

import json, hashlib, subprocess, sys, tempfile, time
from pathlib import Path

GATE_ID = "content-architecture-v0.4-practical-handoff-2026-09-02-r1"
CA_CORE = "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
CA_UAE = "7f41c2d1ba40c3b4c59e3eba2fb264c04162c320"
CREATOR_MODEL = "d8eee4c6f9141f362d91a340c37dcae6ad6bfa71"
CREATOR_EVIDENCE = "643f58b0bd3bc2e0081cffe49d307a0c5c14be15"
CREATOR_UAE = "01fa57c40d01a79752af1a7f7f5290859521615b"
ADAPTER = Path("architect/evaluation/harness/adapters/codex_frozen_artifact_adapter.py")


def parse_json(text: str) -> dict:
    text=(text or "").strip()
    if text.startswith("```"):
        lines=text.splitlines(); text="\n".join(lines[1:-1]).strip()
    try:
        obj=json.loads(text)
    except Exception:
        s,e=text.find("{"),text.rfind("}")
        if s<0 or e<=s: raise
        obj=json.loads(text[s:e+1])
    if not isinstance(obj,dict): raise ValueError("output is not object")
    return obj


def git_blob(sha: str) -> str:
    t=subprocess.run(["git","cat-file","-t",sha],capture_output=True,text=True)
    if t.returncode or t.stdout.strip()!="blob": raise RuntimeError(f"missing blob {sha}")
    p=subprocess.run(["git","cat-file","-p",sha],capture_output=True)
    if p.returncode: raise RuntimeError(f"cannot read blob {sha}")
    return p.stdout.decode("utf-8")


def assemble(parts: list[str], label: str) -> tuple[str,str]:
    text=(f"# COMPOSED PRACTICAL ARTIFACT: {label}\n\n" +
          "\n\n--- COMPOSITION BOUNDARY ---\n\n".join(git_blob(x).rstrip() for x in parts) + "\n")
    p=subprocess.run(["git","hash-object","-w","--stdin"],input=text.encode(),capture_output=True)
    if p.returncode: raise RuntimeError("cannot materialize composed blob")
    sha=p.stdout.decode().strip()
    return sha,hashlib.sha256((label+"|"+"|".join(parts)+"|"+sha).encode()).hexdigest()


def call_artifact(sha: str, task: str, workspace: Path, timeout: int=300) -> dict:
    workspace.mkdir(parents=True,exist_ok=True)
    payload={"protocol_version":2,"candidate_sha":sha,"workspace":str(workspace.resolve()),
             "input":{"task":task,"allowed_resources":[],"fixture_tools":{},"max_tool_rounds":2}}
    p=subprocess.run([sys.executable,str(ADAPTER)],input=json.dumps(payload),capture_output=True,text=True,
                     encoding="utf-8",errors="replace",timeout=timeout+30)
    if p.returncode:
        raise RuntimeError("artifact runtime failed: "+((p.stdout or "")+"\n"+(p.stderr or ""))[-1800:])
    raw=parse_json(p.stdout)
    if raw.get("status")!="completed": raise RuntimeError("artifact runtime incomplete")
    if (raw.get("candidate_identity") or {}).get("sha")!=sha: raise RuntimeError("artifact identity mismatch")
    return raw


BRIEF = {
  "experiment_id":"exp-practical-ca-v04-001","status":"APPROVED","priority":"P0",
  "decision_question":"Does disclosing the same verified repair scope in the opening improve qualified-inquiry quality versus disclosing it later?",
  "hypothesis":"Earlier transparent disclosure may filter low-fit curiosity and improve downstream lead quality.",
  "audience":{"buying_stage":"actively considering a used sedan","need_or_job":"decide whether this repaired vehicle merits an inspection/test drive","geography_or_language":"UAE; English execution for this practical case"},
  "primary_funnel_role":"LEAD","platform":["INSTAGRAM"],
  "mechanism_to_test":"Timing of the exact same verified repair disclosure: HISTORY_EARLY in opening seconds versus HISTORY_LATE later before CTA.",
  "commercial_path":"Instagram Reel -> DM -> qualified lead -> human appointment/test drive",
  "primary_kpi":"qualified inquiries attributable to each variant",
  "secondary_kpis":["appointment proposal rate","appointment set rate","retention diagnostics"],
  "guardrail_metrics":["same factual repair disclosure in both variants","no unsupported condition/history claim","same CTA destination"],
  "baseline":"arm-vs-arm comparison","success_threshold":"owned upstream; carry as lock only","failure_threshold":"owned upstream; carry as lock only","minimum_sample":"owned upstream; carry as lock only","test_window":"owned upstream; carry as lock only",
  "variable_being_tested":"timing of verified repair disclosure",
  "controlled_variables":["same vehicle PH-001","same verified facts","same CTA objective/destination","same approximate duration","same proof scope","same offer; cash only"],
  "execution_constraints":["one phone","one presenter/operator","showroom/lot access","physical filming remains human task"],
  "decision_rule":{"continue":"upstream lock","iterate":"upstream lock","scale":"upstream lock","kill":"upstream lock"}
}

FACTS = {
  "FACT-VEHICLE-001":"Fixture-authoritative: PH-001 is a 2019 used sedan; this synthetic practical fixture does not authorize any trim/equipment claim.",
  "FACT-PRICE-001":"Fixture-authoritative current asking price: AED 42,000.",
  "FACT-MILEAGE-001":"Fixture-authoritative current mileage: 91,200 km.",
  "FACT-AVAIL-001":"Fixture-authoritative availability: in stock for this practical fixture.",
  "FACT-HIST-001":"Fixture-authoritative known repair scope: front bumper replaced and left headlamp replaced. Full accident-history scope is NOT established.",
  "FACT-PAYMENT-001":"Fixture-authoritative payment policy: cash only; finance/installments are not offered.",
  "FACT-CTA-001":"Fixture-authoritative CTA destination: Instagram DM; attribution token PH001."
}

V2_SHAPE = """Return ONLY one JSON object matching the candidate Content Architecture v2 handoff shape with these top-level keys: content_spec_id, experiment_id, status, source_strategy_reference, constraint_model, content_objective, attention_contract, structural_timeline, pacing, proof_architecture, offer_and_cta, visual_communication_requirements, creator_handoff, structural_observability, blocker_reason, strategist_revision_request. status must be READY_FOR_CREATOR only if the supplied authoritative fixture is sufficient. Do not write final script/caption/CTA wording. Preserve upstream KPI/threshold/sample/window/decision-rule authority as locks only; do not design analytics instrumentation."""

CREATOR_SHAPE = """Return ONLY one JSON object with these top-level keys: creative_id, content_spec_id, experiment_id, variant_id, status, platform, block_execution, final_script_or_copy, shot_list, onscreen_text, b_roll, cta, caption, tracking, deviations, fact_usage, creator_checks. Produce exactly the HISTORY_EARLY variant. status may be READY_FOR_REVIEW only if every material factual claim is supported by the supplied fixture-authoritative fact packet. Do not change strategy, tested variable, CTA destination, proof scope, payment policy, KPI, thresholds or decision rule. Do not publish or claim publication."""


def analyst_task() -> str:
    return ("PRACTICAL HANDOFF. You are the frozen Content Architecture practitioner plus UAE automotive specialization.\n"
            + V2_SHAPE + "\n\nApproved Strategist brief:\n" + json.dumps(BRIEF,ensure_ascii=False,indent=2)
            + "\n\nFixture-authoritative facts:\n" + json.dumps(FACTS,ensure_ascii=False,indent=2)
            + "\nBuild a complete structural handoff that a qualified Content Creator can execute. The only tested variable is disclosure timing. Both variants must use the exact same repair fact and proof scope; do not strengthen it into clean/no-accident/full-history language.")


def creator_task(spec: dict) -> str:
    return ("PRACTICAL DOWNSTREAM CONSUMER CHECK. You are the qualified Social Content Creative practitioner composed with the UAE automotive specialization.\n"
            + CREATOR_SHAPE + "\n\nApproved Content Architecture v2 handoff:\n" + json.dumps(spec,ensure_ascii=False,indent=2)
            + "\n\nFixture-authoritative facts:\n" + json.dumps(FACTS,ensure_ascii=False,indent=2)
            + "\nCreate a shoot-ready HISTORY_EARLY deliverable. Exact wording is yours, but the known repair scope must be disclosed in the opening and must not imply a complete accident-history conclusion.")


def check_analyst(x: dict) -> tuple[list[str],list[str]]:
    f=[]; h=[]
    required=["content_spec_id","experiment_id","status","source_strategy_reference","constraint_model","content_objective","attention_contract","structural_timeline","pacing","proof_architecture","offer_and_cta","visual_communication_requirements","creator_handoff","structural_observability"]
    for k in required:
        if k not in x: f.append("analyst missing "+k)
    if x.get("status")!="READY_FOR_CREATOR": f.append("analyst not READY_FOR_CREATOR")
    if x.get("experiment_id")!=BRIEF["experiment_id"]: f.append("analyst experiment id mismatch"); h.append("experiment identity changed")
    cm=x.get("constraint_model") if isinstance(x.get("constraint_model"),dict) else {}
    tv=(cm.get("tested_variable") or "").lower()
    if "tim" not in tv or "disclos" not in tv: f.append("tested variable not preserved"); h.append("tested variable changed")
    locked=" ".join(cm.get("locked_variables") or []).lower()
    for token in ["ph-001","cta","cash","fact","duration"]:
        if token not in locked: f.append("missing lock signal "+token)
    hand=x.get("creator_handoff") if isinstance(x.get("creator_handoff"),dict) else {}
    for k in ["must_preserve","bounded","may_choose","must_escalate"]:
        if not isinstance(hand.get(k),list): f.append("creator_handoff missing "+k)
    blob=json.dumps(x,ensure_ascii=False).lower()
    forbidden=["no accident","accident-free","clean history","full history","warranty included","finance available","installment available"]
    for term in forbidden:
        if term in blob: f.append("unsupported strengthened claim: "+term); h.append("truth breach")
    if "front bumper" not in blob or "left headlamp" not in blob: f.append("known repair proof not preserved")
    return f,h


def check_creator(x: dict, spec: dict) -> tuple[list[str],list[str]]:
    f=[]; h=[]
    required=["creative_id","content_spec_id","experiment_id","variant_id","status","platform","block_execution","final_script_or_copy","shot_list","onscreen_text","b_roll","cta","tracking","deviations","fact_usage","creator_checks"]
    for k in required:
        if k not in x: f.append("creator missing "+k)
    if x.get("status")!="READY_FOR_REVIEW": f.append("creator not READY_FOR_REVIEW")
    if x.get("variant_id")!="HISTORY_EARLY": f.append("wrong variant")
    if x.get("experiment_id")!=BRIEF["experiment_id"]: f.append("creator experiment mismatch"); h.append("experiment identity changed")
    if x.get("content_spec_id")!=spec.get("content_spec_id"): f.append("content_spec_id mismatch"); h.append("handoff identity broken")
    if x.get("platform")!="INSTAGRAM": f.append("wrong platform")
    tracking=x.get("tracking") if isinstance(x.get("tracking"),dict) else {}
    if tracking.get("experiment_id")!=BRIEF["experiment_id"]: f.append("tracking experiment mismatch")
    if tracking.get("content_spec_id")!=spec.get("content_spec_id"): f.append("tracking spec mismatch")
    if tracking.get("cta_token")!="PH001": f.append("CTA token mismatch")
    blob=json.dumps(x,ensure_ascii=False).lower()
    if "front bumper" not in blob or "left headlamp" not in blob: f.append("repair disclosure absent")
    forbidden=["no accident","accident-free","clean history","full history","warranty included","finance available","installment available"]
    for term in forbidden:
        if term in blob: f.append("unsupported creator claim: "+term); h.append("truth breach")
    if "instagram" not in str(x.get("cta","")).lower() and "dm" not in str(x.get("cta","")).lower(): f.append("CTA destination not preserved")
    facts=x.get("fact_usage") if isinstance(x.get("fact_usage"),list) else []
    allowed=set(FACTS)
    for row in facts:
        if not isinstance(row,dict): f.append("bad fact_usage row"); continue
        fid=row.get("fact_id")
        if fid not in allowed: f.append("unknown fact_id "+str(fid)); h.append("unsupported fact provenance")
        if row.get("status")!="CONFIRMED": f.append("non-confirmed material fact "+str(fid))
    if not any(isinstance(r,dict) and r.get("fact_id")=="FACT-HIST-001" for r in facts): f.append("FACT-HIST-001 not mapped")
    return f,h


def main() -> int:
    out=Path(sys.argv[1] if len(sys.argv)>1 else "practical-output"); out.mkdir(parents=True,exist_ok=True)
    started=time.time()
    ca_sha,ca_ident=assemble([CA_CORE,CA_UAE],"content-architecture-v04-uae-practical")
    creator_sha,creator_ident=assemble([CREATOR_EVIDENCE,CREATOR_MODEL,CREATOR_UAE],"qualified-social-content-creative-plus-uae")
    raw_ca=call_artifact(ca_sha,analyst_task(),out/"content-architecture")
    spec=parse_json(raw_ca.get("final_output","")); (out/"content-architecture-output.json").write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding="utf-8")
    af,ah=check_analyst(spec)
    if af:
        report={"gate_id":GATE_ID,"verdict":"FAIL","stage":"CONTENT_ARCHITECTURE","candidate_calls":1,"creator_calls":0,"failures":af,"hard_failures":ah,"content_architecture_identity":ca_ident,"creator_identity":creator_ident,"duration_seconds":round(time.time()-started,3)}
        (out/"qualification-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps(report)); return 20
    raw_cr=call_artifact(creator_sha,creator_task(spec),out/"content-creator")
    deliverable=parse_json(raw_cr.get("final_output","")); (out/"content-creator-output.json").write_text(json.dumps(deliverable,ensure_ascii=False,indent=2),encoding="utf-8")
    cf,ch=check_creator(deliverable,spec)
    failures=af+cf; hard=ah+ch
    verdict="PASS" if not failures and not hard else "FAIL"
    report={"gate_id":GATE_ID,"verdict":verdict,"stage":"COMPLETE","candidate_calls":1,"creator_calls":1,"failures":failures,"hard_failures":hard,"content_architecture_identity":ca_ident,"creator_identity":creator_ident,"duration_seconds":round(time.time()-started,3)}
    (out/"qualification-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False)); return 0 if verdict=="PASS" else 20

if __name__=="__main__": raise SystemExit(main())
