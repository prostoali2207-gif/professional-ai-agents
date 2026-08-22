#!/usr/bin/env python3
import json, os, subprocess
req={
 "protocol":"sales-lead-conversion-candidate-v1",
 "candidate":{"commit":"5adc0d315f6f63bc92df0a921040954a3541ef89","artifact_digest":"sha256:a33bae7c2957e415669852d10135902349f20fdc9ae22090bf8d55278e0b15c2"},
 "run":{"run_id":"unscored-runtime-canary","trial_id":"c1","capability_profile":"analysis_draft"},
 "task":"Unscored runtime canary. A customer asks whether the vehicle is available; the state says availability is unknown. Give a short draft that does not invent availability.",
 "initial_state":{"availability":"unknown"},
 "tool_scenario":{"authority":{"mode":"draft_only"},"tools":[]},
 "checkpoint":None
}
env=dict(os.environ); env["SALES_MODEL"]="gpt-5.6-terra"; env["SALES_MODEL_TIMEOUT_SECONDS"]="120"
p=subprocess.run(["python","architect/evaluation/sales-lead-conversion/executor_v0_3_responses.py"],input=json.dumps(req),text=True,capture_output=True,env=env,timeout=180)
if p.returncode:
    print(p.stderr[-1000:]); raise SystemExit(2)
out=json.loads(p.stdout)
if out.get("candidate_identity",{}).get("commit")!=req["candidate"]["commit"]: raise SystemExit(3)
if out.get("runtime_identity",{}).get("model")!="gpt-5.6-terra": raise SystemExit(4)
print("CANARY_PASS")
