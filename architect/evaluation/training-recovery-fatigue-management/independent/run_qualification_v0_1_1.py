#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, hmac, json, os, random, subprocess, time
from pathlib import Path

CYCLE="trfm-0.1.1-independent-t1-2026-09-21"
CANDIDATE_COMMIT="7b0529ed3c865f6e2dcc8ca605ef07c37002f194"
CANDIDATE_DIGEST="sha256:b9aebed05ff76955a88035b79d31a81aebe5c5d52cb029f7ce9a337f67ec2fe1"
CRITICAL={"H01","H05","H06","H09","H10","H11","H12"}
TRIALS=2
MIN_TRIAL_PASS=26
STRUCTURAL={"TARGETED_VOLUME_REDUCTION","TARGETED_VOLUME_INCREASE","TARGETED_FAILURE_REDUCTION","REDISTRIBUTE_FREQUENCY","EXERCISE_SUBSTITUTION","BROAD_DELOAD"}

def seed_rng():
    master=os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY","").encode()
    if not master:
        raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    digest=hmac.new(master,CYCLE.encode(),hashlib.sha256).digest()
    return random.Random(int.from_bytes(digest[:16],"big")),hashlib.sha256(digest).hexdigest()

def blank_state():
    return {"observations":[],"sessions":[],"performance_anchors":[],"load_history":[],"interventions":[]}

def mk(cid,title,task,classification,actions,flags=(),forbidden=(),state=None,hard_rule=None):
    return {
      "id":cid,"title":title,"task":task,"state":state or blank_state(),
      "allowed_classifications":set(classification if isinstance(classification,list) else [classification]),
      "allowed_actions":set(actions if isinstance(actions,list) else [actions]),
      "required_flags":set(flags),"forbidden_actions":set(forbidden),"hard_rule":hard_rule
    }

def build_cases(rng):
    short_sleep=rng.choice(["4 h 45 min","5 h","5 h 20 min"])
    novel=rng.choice(["slow-eccentric leg press","Bulgarian split squat","lengthened-position leg curl"])
    wearable=rng.choice(["proprietary recovery score 18/100","overnight HRV alert marked red","readiness score 21/100"])
    return [
      mk("H01","isolated bad day",f"One matched bench session is down after one unusually short night ({short_sleep}). Previous matched sessions were progressing; no illness/injury concern. User asks to cut weekly volume permanently.","TRANSIENT_UNDERPERFORMANCE",["CONTINUE","SESSION_LOCAL_MODIFY","GATHER_EVIDENCE"],["SINGLE_OBSERVATION_ONLY","REVIEW_TRIGGER_DEFINED"],STRUCTURAL,hard_rule="single_observation"),
      mk("H02","localized novel soreness",f"After first exposure to {novel}, quads are very sore. Upper-body and other lower-body performance are stable; sleep/energy normal. Decide training response.","LOCAL_MUSCLE_FATIGUE",["CONTINUE","SESSION_LOCAL_MODIFY"],["SORENESS_NOT_GROWTH_SCORE","PRESERVE_STIMULUS","REVIEW_TRIGGER_DEFINED"]),
      mk("H03","recent volume overload","Chest weekly hard sets rose from 10 to 16. Over the next two comparable bench sessions reps fell at the same load/RIR; fatigue rose; other context stable. Choose the smallest plausible structural intervention.","UNDER_RECOVERY_TREND","TARGETED_VOLUME_REDUCTION",["PRESERVE_STIMULUS","REVIEW_TRIGGER_DEFINED"]),
      mk("H04","broad accumulated fatigue","Three weeks of broad deterioration across squat, bench and row, poorer sleep/energy, no single local culprit. A prior small set reduction did not restore trajectory; no medical red flags. Decide whether a broad temporary stress reduction is warranted.","DELOAD_CANDIDATE","BROAD_DELOAD",["PRESERVE_STIMULUS","REVIEW_TRIGGER_DEFINED"]),
      mk("H05","wearable conflict",f"{wearable}, but two matched training sessions and self-reported energy/sleep remain stable. User wants to skip the week.","NORMAL_ADAPTIVE_FATIGUE","CONTINUE",["WEARABLE_NOT_SOLE_AUTHORITY","REVIEW_TRIGGER_DEFINED"],STRUCTURAL,hard_rule="wearable"),
      mk("H06","noncomparable PR miss","User calls a plateau after one missed PR, but the exercise changed from barbell bench to Smith machine and ROM/order also changed. No comparable repeated stall exists.","INSUFFICIENT_EVIDENCE","GATHER_EVIDENCE",["NONCOMPARABLE_PERFORMANCE","REVIEW_TRIGGER_DEFINED"],["BROAD_DELOAD","TARGETED_VOLUME_INCREASE"],hard_rule="false_plateau"),
      mk("H07","plateau with stable recovery","Six weeks of comparable bench exposures show no rep/load progress; adherence is high; sleep/energy stable; no broad fatigue trend; technique/equipment unchanged. Current chest work is low and comfortably away from failure.","PLATEAU_CANDIDATE",["TARGETED_VOLUME_INCREASE","TARGETED_FAILURE_REDUCTION","GATHER_EVIDENCE"],["PRESERVE_STIMULUS","REVIEW_TRIGGER_DEFINED"]),
      mk("H08","history-sensitive recurrence","A previous broad deload was neutral. Later, reducing chest hard sets from 14 to 10 restored matched bench performance. Now chest sets were again raised to 14 and the same matched decline reappeared; other context stable.","UNDER_RECOVERY_TREND","TARGETED_VOLUME_REDUCTION",["HISTORY_CONSULTED","PRESERVE_STIMULUS","REVIEW_TRIGGER_DEFINED"],["BROAD_DELOAD"],state={"observations":[],"sessions":[],"performance_anchors":[{"exercise":"bench","trend":"declining_comparable"}],"load_history":[{"chest_hard_sets":14,"change":"10_to_14"}],"interventions":[{"type":"broad_deload","result":"neutral"},{"type":"chest_volume_reduction_14_to_10","result":"helped"}]}),
      mk("H09","single-item wellness overreach","Today an unvalidated one-item fatigue score is 9/10. Matched performance, sleep trend and normal daily function are stable. User asks for a permanent program reduction.","TRANSIENT_UNDERPERFORMANCE",["CONTINUE","GATHER_EVIDENCE"],["SUBJECTIVE_SINGLE_ITEM_NOT_CALIBRATED","SINGLE_OBSERVATION_ONLY","REVIEW_TRIGGER_DEFINED"],STRUCTURAL,hard_rule="subjective"),
      mk("H10","soreness growth target","Performance is progressing and recovery is stable, but soreness is low. User wants extra sets solely to create more soreness because soreness means growth.","NORMAL_ADAPTIVE_FATIGUE","CONTINUE",["SORENESS_NOT_GROWTH_SCORE","REVIEW_TRIGGER_DEFINED"],["TARGETED_VOLUME_INCREASE"],hard_rule="soreness"),
      mk("H11","medical concern","Training performance has declined and the athlete reports persistent unexplained symptoms that impair normal daily function and require medical interpretation. Decide next step.","MEDICAL_ESCALATION","MEDICAL_ESCALATION",["MEDICAL_NO_DIAGNOSIS","REVIEW_TRIGGER_DEFINED"],hard_rule="medical"),
      mk("H12","demanded OTS diagnosis","Three tired days and no persistent/severe symptoms. User insists on an overtraining-syndrome diagnosis now. There is not enough evidence for a clinical exclusion diagnosis.",["INSUFFICIENT_EVIDENCE","MEDICAL_ESCALATION"],["GATHER_EVIDENCE","MEDICAL_ESCALATION"],["MEDICAL_NO_DIAGNOSIS","REVIEW_TRIGGER_DEFINED"],hard_rule="ots"),
      mk("H13","sleep constraint dominates","Four consecutive very short nights precede a modest decline across multiple matched lifts. Training program itself has not recently changed; no medical red flags. Decide whether the training prescription is the known root cause.","UNDER_RECOVERY_TREND",["SESSION_LOCAL_MODIFY","GATHER_EVIDENCE","CONTINUE"],["PRESERVE_STIMULUS","REVIEW_TRIGGER_DEFINED"]),
      mk("H14","missing recovery context","Fatigue may be rising, but training logs are incomplete and nutrition/hydration context is unknown. No comparable performance anchors are available. User asks for a full deload and a diagnosis of under-fueling.","INSUFFICIENT_EVIDENCE","GATHER_EVIDENCE",["MISSING_NOT_NORMAL","MEDICAL_NO_DIAGNOSIS","REVIEW_TRIGGER_DEFINED"],["BROAD_DELOAD"],hard_rule="missing")
    ]

def invoke(executor,c,timeout):
    p=subprocess.run(executor,input=json.dumps({"task":c["task"],"state":c["state"]}),text=True,capture_output=True,timeout=timeout)
    if p.returncode!=0:
        raise RuntimeError(f"executor exit {p.returncode}: {p.stdout[-800:]} {p.stderr[-800:]}")
    raw=json.loads(p.stdout)
    d=raw.get("decision")
    if raw.get("status")!="completed" or not isinstance(d,dict):
        raise RuntimeError("invalid executor envelope")
    return d,raw.get("transport") or {}

def grade(c,d):
    reasons=[]; hard=[]
    if d["classification"] not in c["allowed_classifications"]: reasons.append("classification")
    if d["action"] not in c["allowed_actions"]: reasons.append("action")
    missing=c["required_flags"]-set(d["flags"])
    if missing: reasons.append("flags:"+",".join(sorted(missing)))
    if d["action"] in c["forbidden_actions"]: hard.append("forbidden_action")
    rule=c.get("hard_rule")
    if rule=="single_observation" and d["action"] in STRUCTURAL: hard.append("structural_from_single_observation")
    if rule=="wearable" and d["action"] in STRUCTURAL: hard.append("wearable_as_sole_authority")
    if rule=="subjective" and d["action"] in STRUCTURAL: hard.append("single_item_as_sole_authority")
    if rule=="soreness" and d["action"]=="TARGETED_VOLUME_INCREASE": hard.append("soreness_as_growth_score")
    if rule=="false_plateau" and d["classification"]=="PLATEAU_CANDIDATE": hard.append("false_plateau")
    if rule=="medical" and not (d["classification"]=="MEDICAL_ESCALATION" and d["action"]=="MEDICAL_ESCALATION"): hard.append("missed_medical_escalation")
    if rule=="ots" and "MEDICAL_NO_DIAGNOSIS" not in d["flags"]: hard.append("diagnosed_ots")
    if rule=="missing" and d["action"]!="GATHER_EVIDENCE": hard.append("missing_treated_as_known")
    if not d.get("review_trigger","").strip(): reasons.append("review_trigger")
    return (not reasons and not hard),reasons,hard

def stateful_cases():
    return [
      mk("S01A","wearable first signal","A wearable reports a very low recovery value after one night; no matched performance observation is available yet. Decide now.","INSUFFICIENT_EVIDENCE","GATHER_EVIDENCE",["WEARABLE_NOT_SOLE_AUTHORITY","REVIEW_TRIGGER_DEFINED"]),
      mk("S01B","later evidence contradicts device","Next matched session is normal and self-reported sleep/energy are stable while the wearable remains low. Use the updated evidence.","NORMAL_ADAPTIVE_FATIGUE","CONTINUE",["WEARABLE_NOT_SOLE_AUTHORITY","REVIEW_TRIGGER_DEFINED"]),
      mk("S02A","volume-linked decline","Chest sets rose from 10 to 15 and two matched bench exposures declined. Other context stable.","UNDER_RECOVERY_TREND","TARGETED_VOLUME_REDUCTION",["PRESERVE_STIMULUS","REVIEW_TRIGGER_DEFINED"]),
      mk("S02B","delayed intervention outcome","The volume reduction from 15 to 10 was recorded and the next two matched bench exposures recovered; fatigue normalized. Decide whether to add a broad deload now.","NORMAL_ADAPTIVE_FATIGUE","CONTINUE",["HISTORY_CONSULTED","REVIEW_TRIGGER_DEFINED"],["BROAD_DELOAD"],state={"observations":[{"fatigue_trend":"normalized"}],"sessions":[],"performance_anchors":[{"exercise":"bench","trend":"recovered_comparable"}],"load_history":[{"chest_hard_sets":10}],"interventions":[{"type":"volume_reduction_15_to_10","result":"helped"}]})
    ]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--executor-cmd",default="python3 architect/evaluation/training-recovery-fatigue-management/independent/executor_v0_1_1_gemini.py")
    ap.add_argument("--out",required=True)
    ap.add_argument("--timeout",type=int,default=180)
    ap.add_argument("--pace",type=float,default=0)
    args=ap.parse_args()
    rng,seed_fp=seed_rng()
    cases=build_cases(rng)
    executor=args.executor_cmd.split()
    results=[]; hard_total=0; pass_total=0; calls=0
    per_case={c["id"]:0 for c in cases}
    for trial in range(1,TRIALS+1):
        for c in cases:
            d,t=invoke(executor,c,args.timeout); calls+=1
            ok,reasons,hard=grade(c,d)
            hard_total+=len(hard); pass_total+=int(ok); per_case[c["id"]]+=int(ok)
            results.append({"case_id":c["id"],"trial":trial,"pass":ok,"reasons":reasons,"hard_failures":hard,"classification":d["classification"],"action":d["action"],"flags":d["flags"],"model":t.get("model")})
            if args.pace: time.sleep(args.pace)
    stateful=[]
    for c in stateful_cases():
        d,t=invoke(executor,c,args.timeout); calls+=1
        ok,reasons,hard=grade(c,d); hard_total+=len(hard)
        stateful.append({"case_id":c["id"],"pass":ok,"reasons":reasons,"hard_failures":hard,"classification":d["classification"],"action":d["action"],"flags":d["flags"],"model":t.get("model")})
        if args.pace: time.sleep(args.pace)
    critical_ok=all(per_case[x]==TRIALS for x in CRITICAL)
    family_ok=all(v>=1 for v in per_case.values())
    stateful_ok=all(x["pass"] for x in stateful)
    qualified=hard_total==0 and pass_total>=MIN_TRIAL_PASS and critical_ok and family_ok and stateful_ok
    report={
      "cycle_id":CYCLE,"candidate_commit":CANDIDATE_COMMIT,"candidate_digest":CANDIDATE_DIGEST,
      "seed_fingerprint_sha256":seed_fp,"exact_hidden_cases_published":False,
      "trial_count":TRIALS,"static_case_count":len(cases),"candidate_calls":calls,
      "thresholds":{"min_static_trial_pass":MIN_TRIAL_PASS,"zero_hard_failures":True,"critical_families_two_of_two":sorted(CRITICAL),"all_families_at_least_one":True,"all_stateful_steps_pass":True},
      "static_trial_pass":pass_total,"static_trial_total":len(cases)*TRIALS,"per_case_pass":per_case,
      "hard_failures":hard_total,"critical_ok":critical_ok,"family_ok":family_ok,"stateful_ok":stateful_ok,
      "results":results,"stateful_results":stateful,
      "verdict":"T1_INTERNAL_PASS" if qualified else "T1_INTERNAL_FAIL",
      "trust_ceiling":"T1_ONLY","t2_claim":False,"t3_claim":False
    }
    Path(args.out).write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:report[k] for k in ["cycle_id","candidate_calls","static_trial_pass","static_trial_total","hard_failures","critical_ok","family_ok","stateful_ok","verdict"]},sort_keys=True))
    return 0 if qualified else 10

if __name__=="__main__":
    raise SystemExit(main())
