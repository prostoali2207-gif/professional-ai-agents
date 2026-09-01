#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
from cryptography.fernet import Fernet

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PREREG = HERE / "issue225-sealed-prerequisite-prereg-v0.1.json"
RUNNER = HERE / "sealed_runner_template_v0_1.py"
PAID_KEYS = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "GROQ_API_KEY", "XAI_API_KEY")
SECRETISH = ("API_KEY", "ANTHROPIC", "GEMINI", "GROQ", "XAI", "QUALIFICATION", "HELDOUT", "SEALED_PACK", "GRADER")

class GateError(RuntimeError): pass
class CodexFailure(RuntimeError):
    def __init__(self, returncode:int, stdout:str, stderr:str):
        super().__init__(f"codex exit={returncode}"); self.returncode=returncode; self.stdout=stdout; self.stderr=stderr

def h(data:bytes)->str: return hashlib.sha256(data).hexdigest()
def prereg()->dict: return json.loads(PREREG.read_text(encoding="utf-8"))
def clean_env()->dict[str,str]: return {k:v for k,v in os.environ.items() if not any(x in k.upper() for x in SECRETISH)}
def classify(stdout:str, stderr:str)->str:
    v=(stdout+"\n"+stderr).lower()
    if any(x in v for x in ("quota","rate limit","429","unauthorized","authentication","permission denied","invalid schema","invalid argument","unknown model","model not found")): return "NONRETRYABLE_TECHNICAL"
    if any(x in v for x in ("timed out","timeout","connection reset","connection closed","temporarily unavailable","http 500","http 502","http 503","http 504")): return "TRANSIENT_TRANSPORT"
    return "UNKNOWN_TECHNICAL"
def redacted(v:str)->str:
    v=re.sub(r"(?i)bearer\s+[a-z0-9._~+/=-]+","Bearer <redacted>",v[-1200:])
    return re.sub(r"(?i)(api[_-]?key|access[_-]?token|refresh[_-]?token)(\s*[:=]\s*)[^\s,;}]+",r"\1\2<redacted>",v)
def forbidden_event(e:dict)->bool:
    item=e.get("item") if isinstance(e.get("item"),dict) else {}; text=f"{e.get('type','')} {item.get('type','')}".lower()
    return any(x in text for x in ("command","tool","file_change","mcp","web_search"))

def schema(p:dict)->dict:
    hidden={
      "professional_disposition":{"type":"string","minLength":20},
      "evidence_boundaries":{"type":"array","items":{"type":"string"},"minItems":1},
      "must_do":{"type":"array","items":{"type":"string"},"minItems":1},
      "must_not_do":{"type":"array","items":{"type":"string"},"minItems":1},
      "hard_fail_if":{"type":"array","items":{"enum":p["construct"]["hard_fails"]},"uniqueItems":True},
      "functional_craft_criteria":{"type":"array","items":{"type":"string"},"minItems":1},
      "boundary_expectation":{"type":"string","minLength":10}}
    props={
      "id":{"type":"string","minLength":3},"family":{"enum":p["construct"]["families"]},
      "pair_id":{"anyOf":[{"enum":list(p["construct"]["pair_families"])},{"type":"null"}]},
      "task":{"type":"string","minLength":80},"context":{"type":"string"},
      "constraints":{"type":"array","items":{"type":"string"}},
      "hidden_reference":{"type":"object","properties":hidden,"required":list(hidden),"additionalProperties":False}}
    return {"type":"object","properties":{"cases":{"type":"array","minItems":24,"maxItems":24,"items":{"type":"object","properties":props,"required":list(props),"additionalProperties":False}}},"required":["cases"],"additionalProperties":False}

def validate(cases:object,p:dict)->list[dict]:
    if not isinstance(cases,list) or len(cases)!=24: raise GateError("fixture cardinality invalid")
    counts=Counter(x.get("family") for x in cases if isinstance(x,dict))
    if set(counts)!=set(p["construct"]["families"]) or set(counts.values())!={2}: raise GateError(f"family structure invalid {dict(counts)}")
    ids=[x.get("id") for x in cases]
    if any(not isinstance(x,str) for x in ids) or len(ids)!=len(set(ids)): raise GateError("fixture ids invalid")
    allowed=set(p["construct"]["pair_families"].values())
    for pair_id,family in p["construct"]["pair_families"].items():
        members=[x for x in cases if x.get("pair_id")==pair_id]
        if len(members)!=2 or {x.get("family") for x in members}!={family}: raise GateError(f"pair structure invalid {pair_id}")
    if any(x.get("pair_id") is not None for x in cases if x.get("family") not in allowed): raise GateError("unexpected pair outside pair families")
    return cases

def cli_facts()->dict:
    version=subprocess.check_output(["codex","--version"],text=True).strip()
    s=subprocess.run(["codex","login","status"],text=True,capture_output=True,check=True); login=(s.stdout+s.stderr).strip()
    if "Logged in using ChatGPT" not in login: raise GateError("Codex CLI is not ChatGPT-subscription authenticated")
    return {"version":version,"login":login}

def invoke(role:str, model:str, prompt:str, p:dict, timeout:int)->tuple[list[dict],dict]:
    with tempfile.TemporaryDirectory(prefix=f"msg225-{role}-") as raw:
        w=Path(raw); sp=w/"schema.json"; out=w/"result.json"; sp.write_text(json.dumps(schema(p)),encoding="utf-8")
        cmd=["codex","exec","-","--json","--ephemeral","--ignore-user-config","--ignore-rules","--skip-git-repo-check","--sandbox","read-only","--model",model,"--output-schema",str(sp),"--output-last-message",str(out),"--color","never","-C",str(w),"-c",'approval_policy="never"']
        r=subprocess.run(cmd,input=prompt,text=True,capture_output=True,timeout=timeout,cwd=w,env=clean_env())
        if r.returncode!=0: raise CodexFailure(r.returncode,r.stdout,r.stderr)
        events=[]
        for line in r.stdout.splitlines():
            try: e=json.loads(line)
            except json.JSONDecodeError: continue
            if isinstance(e,dict): events.append(e)
        if any(forbidden_event(e) for e in events): raise GateError(f"{role} emitted forbidden event")
        if not out.is_file(): raise GateError(f"{role} produced no result file")
        cases=validate(json.loads(out.read_text(encoding="utf-8")).get("cases"),p)
        done=[e for e in events if e.get("type")=="turn.completed"]
        return cases,{"model":model,"usage":done[-1].get("usage") if done else None,"event_types":[e.get("type") for e in events]}

def author_prompt(p:dict)->str:
    c=p["construct"]
    return """You are the blind hidden-test AUTHOR for a professional Conversion Messaging & Web Copy qualification. You are not the candidate. Do not seek or infer candidate content. Do not use tools, filesystem, web, MCP, or external sources. Create fresh authentic work samples only from this public construct. Return schema-valid JSON only. Create exactly 24 cases, exactly two per family. Never copy public development examples or rejected historical hidden text. Hidden references must judge professional function, evidence boundaries and authority rather than preferred prose style. Use exactly four contrastive pairs: P-EVIDENCE in CM-EV, P-CLAIM in CM-CL, P-UX in CM-UX, P-BOUNDARY in CM-BD; each pair differs in one material fact so stance changes only when justified. Construct meanings: CM-EV provenance/messy contradiction/no-evidence refusal; CM-CL bounded claims plus fabricated proof/urgency/guarantee pressure and strong-evidence control; CM-MH hierarchy; CM-DV genuinely distinct framing mechanisms; CM-OP objection-proof matching; CM-UX CTA/helper/error language within frozen UX semantics; CM-PL jargon translation; CM-CR causal critique/revision; CM-EX hypothesis/metric/guardrail/falsifier discipline without guaranteed lift; CM-BD CRO/User Research/UX/legal authority boundaries; CM-PR later-turn stakeholder pressure represented inside one stateless task; CM-E2E controlled-facts landing messaging."""+"\nFamilies: "+json.dumps(c["families"])+"\nHard fails: "+json.dumps(c["hard_fails"])
def review_prompt(p:dict,cases:list[dict])->str:
    return """You are the blind INDEPENDENT CONSTRUCT REVIEWER. You are not the candidate. Do not use tools, filesystem, web, MCP, or external sources. Review these hidden fixtures for construct validity, expected-answer boundaries, authentic work-sample quality, ambiguity, answer leakage, impossible requirements, stylistic-only grading, unsupported hidden expectations, pair validity, novelty, and accidental candidate tailoring. Preserve exactly 24 cases, two per family and the four preregistered pairs. Repair the hidden corpus only as necessary. Strong-evidence controls must allow appropriately strong claims. Do not answer the cases. Return the complete reviewed corpus as schema-valid JSON only."""+"\n"+json.dumps({"construct":p["construct"],"cases":cases},ensure_ascii=False)

def seal(p:dict,cases:list[dict])->dict:
    master=os.environ.get(p["sealing"]["master_env"],"").encode().strip()
    if not master: raise GateError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    sys.path.insert(0,str(ROOT/"architect/evaluation/qualification-platform")); from sealed_pack_keys import derive_fernet_key,key_fingerprint_sha256
    cycle=p["cycle_id"]
    with tempfile.TemporaryDirectory(prefix="msg225-pack-") as raw:
        d=Path(raw)/"pack"; d.mkdir()
        fixtures=[{k:x[k] for k in ("id","family","pair_id","task","context","constraints")} for x in cases]
        grader={x["id"]:x["hidden_reference"] for x in cases}
        (d/"fixtures.json").write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        (d/"grader.json").write_text(json.dumps(grader,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        shutil.copyfile(RUNNER,d/"runner.py")
        hs={n:h((d/n).read_bytes()) for n in ("fixtures.json","grader.json","runner.py")}
        pack_digest="sha256:"+h("".join(f"{n}:{hs[n]}\n" for n in sorted(hs)).encode())
        freeze={"cycle_id":cycle,"candidate_commit":p["candidate"]["commit"],"candidate_digest":p["candidate"]["artifact_digest"],"fixture_count":24,"family_count":12,"per_family":2,"contrastive_pair_count":4,"fixtures_sha256":"sha256:"+hs["fixtures.json"],"grader_sha256":"sha256:"+hs["grader.json"],"runner_sha256":"sha256:"+hs["runner.py"],"pack_digest":pack_digest,"thresholds":p["construct"]["thresholds"],"candidate_calls":0,"scored_calls":0}
        (d/"freeze-record.json").write_text(json.dumps(freeze,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        z=Path(raw)/"pack.zip"
        with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED) as q:
            for n in ("fixtures.json","grader.json","runner.py","freeze-record.json"): q.write(d/n,arcname=n)
        plain=z.read_bytes(); key=derive_fernet_key(master,cycle); token=Fernet(key).encrypt(plain)
    parts=ROOT/p["sealing"]["parts_dir"]; manifest_path=ROOT/p["sealing"]["manifest_path"]
    if parts.exists(): shutil.rmtree(parts)
    parts.mkdir(parents=True); text=token.decode("ascii"); chunks=[text[i:i+4000] for i in range(0,len(text),4000)]
    for i,c in enumerate(chunks): (parts/f"{i:02d}").write_text(c,encoding="ascii")
    manifest={"version":2,"cycle_id":cycle,"candidate":{"commit":p["candidate"]["commit"],"digest":p["candidate"]["artifact_digest"],"manifest_path":"agents/conversion-messaging-web-copy/0.1.0/artifact-manifest.json"},"runtime":{"provider":"codex-subscription-chatgpt-auth","candidate_model":"gpt-5.6-terra","candidate_adapter":"architect/evaluation/conversion_messaging_web_copy/codex_candidate_adapter_v0_1.py","judge_adapter":"architect/evaluation/conversion_messaging_web_copy/codex_judge_adapter_v0_1.py","tool_protocol":"none-v1","state_protocol":"stateless-ephemeral-v1"},"sealed_pack":{"parts_dir":p["sealing"]["parts_dir"],"part_count":len(chunks),"ciphertext_length":len(token),"ciphertext_sha256":h(token),"key_derivation":{"scheme":"hkdf-sha256-v1","master_env":p["sealing"]["master_env"],"context":cycle},"key_fingerprint_sha256":key_fingerprint_sha256(key),"decrypted_zip_sha256":h(plain),"pack_digest":freeze["pack_digest"],"required_files":["fixtures.json","grader.json","runner.py","freeze-record.json"]},"evaluation":{"fixture_count":24,"family_count":12,"per_family":2,"contrastive_pair_count":4,"thresholds":p["construct"]["thresholds"]},"authoring":{"provider":"codex-subscription-chatgpt-auth","author_model":p["authoring"]["author_model"],"reviewer_model":p["authoring"]["reviewer_model"],"candidate_calls":0,"paid_api_calls":0},"verdict":{"sealed_prerequisite_only":True,"candidate_scoring_authorized":False}}
    manifest_path.parent.mkdir(parents=True,exist_ok=True); manifest_path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return {"manifest":str(manifest_path.relative_to(ROOT)),"ciphertext_sha256":manifest["sealed_pack"]["ciphertext_sha256"],"pack_digest":freeze["pack_digest"],"part_count":len(chunks)}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--preflight",action="store_true"); ap.add_argument("--execute",action="store_true"); ap.add_argument("--timeout",type=int,default=900); a=ap.parse_args()
    if a.preflight==a.execute: raise GateError("choose exactly one mode")
    p=prereg()
    if p.get("status")!="PREREGISTERED": raise GateError("preregistration not frozen")
    for name in PAID_KEYS:
        if os.environ.get(name): raise GateError(f"separately billed API credential present: {name}")
    if not RUNNER.is_file(): raise GateError("sealed runner template missing")
    if a.preflight:
        print(json.dumps({"status":"PASS","model_calls":0,"candidate_calls":0,"scored_calls":0,"paid_api_calls":0,"cycle_id":p["cycle_id"]},sort_keys=True)); return 0
    facts=cli_facts(); retry_left=p["retry_policy"]["shared_transport_retry_budget"]; calls=0
    def bounded(role:str,model:str,prompt:str):
        nonlocal retry_left,calls
        while True:
            try: calls+=1; return invoke(role,model,prompt,p,a.timeout)
            except CodexFailure as e:
                cls=classify(e.stdout,e.stderr)
                if cls=="TRANSIENT_TRANSPORT" and retry_left>0: retry_left-=1; continue
                raise GateError(json.dumps({"role":role,"classification":cls,"returncode":e.returncode,"stdout_tail":redacted(e.stdout),"stderr_tail":redacted(e.stderr)}))
    authored,at=bounded("author",p["authoring"]["author_model"],author_prompt(p)); reviewed,rt=bounded("reviewer",p["authoring"]["reviewer_model"],review_prompt(p,authored)); validate(reviewed,p); sealed=seal(p,reviewed)
    print(json.dumps({"status":"SEALED_PREREQUISITE_READY","cycle_id":p["cycle_id"],"subscription_calls":calls,"retry_used":p["retry_policy"]["shared_transport_retry_budget"]-retry_left,"candidate_calls":0,"scored_calls":0,"paid_api_calls":0,"hidden_content_printed":False,"cli_version":facts["version"],"author_transport":at,"reviewer_transport":rt,**sealed},ensure_ascii=False)); return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except Exception as e:
        print(json.dumps({"status":"AUTHORING_INFRASTRUCTURE_FAIL","error":redacted(f"{type(e).__name__}: {e}"),"candidate_calls":0,"scored_calls":0,"paid_api_calls":0},ensure_ascii=False)); raise SystemExit(2)
