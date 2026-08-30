#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import random
import subprocess
import sys
from pathlib import Path
from cryptography.fernet import Fernet

PREV = Path(__file__).with_name('run_r3_semantic_qualification_v0_1_bindingfix4.py')
spec = importlib.util.spec_from_file_location('visual_r3_semantic_transport_frozen', PREV)
if spec is None or spec.loader is None:
    raise RuntimeError('cannot load frozen R3 semantic transport')
fix4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fix4)
module = fix4.module

CYCLE='visual-design-art-direction-0.2.0-independent-2026-08-30-r4-semantic'
SCORE_CYCLE=CYCLE+'-scored-v1'
CANDIDATE_COMMIT='0116d20f99fde919fa6e39c700726d16310d010b'
SKILL_BLOB='b230a06aeca3cc67d0c275889a65b8b7403b59c0'
BASE_MODEL_BLOB='bbea595e299445cf79f798ed1e86eecd0b53cd50'
REPAIR_MODEL_BLOB='bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50'
SOURCE_RUN=33306265227
SOURCE_HEAD='147f1581c1ff24c51b71169aaad7770d6d27f3ce'
SOURCE_ARTIFACT_ID=9730714845
SOURCE_ARTIFACT_NAME='visual-design-art-direction-v0-2-encrypted-heldout-pack-r4'
SOURCE_ARTIFACT_DIGEST='sha256:fbe4b03ffc1eede30b3e36dcaa13e7bf96e29c28cf40d722ae2e376355f0e73e'
SOURCE_CIPHERTEXT_SHA256='b6147b01b838aa447fcaff711668771d6347a329f97ac21c7c97f9c9d6e85bf6'
GENERAL_CALIBRATION_RUN=33262394565
R4_CALIBRATION_RUN=33315348031
R4_CALIBRATION_REPORT_ARTIFACT_ID=9733259354
R4_CALIBRATION_REPORT_ARTIFACT_DIGEST='sha256:0586e0c43287a99a0991dc3d60bbe461f7701fcc7b43a0d030391d8face024a5'
R4_CALIBRATION_REPORT_SHA256='642b2cc24f7e34593d52208bb4f5fcb342471c04104ff145136e1da15d613409'
EXECUTOR='architect/evaluation/visual-design-art-direction/semantic/executor_r4_v0_2_gemini.py'
CHECKPOINT=Path('visual-r4-v02-semantic-checkpoint.enc')
REPORT=Path('visual-r4-v02-semantic-sanitized-report.json')
PROGRESS=Path('visual-r4-v02-semantic-progress.json')

# Rebind only release identity/transport data. Judge models, P0 categories,
# family dimensions, thresholds, A/B protocol, transient retry semantics and
# Gemini schema enforcement remain inherited from the already-calibrated R3 path.
module.CYCLE=CYCLE
module.SCORE_CYCLE=SCORE_CYCLE
module.CANDIDATE_COMMIT=CANDIDATE_COMMIT
module.SKILL_BLOB=SKILL_BLOB
module.MODEL_BLOB=BASE_MODEL_BLOB
module.SOURCE_RUN=SOURCE_RUN
module.SOURCE_HEAD=SOURCE_HEAD
module.SOURCE_ARTIFACT_ID=SOURCE_ARTIFACT_ID
module.SOURCE_ARTIFACT_NAME=SOURCE_ARTIFACT_NAME
module.SOURCE_ARTIFACT_DIGEST=SOURCE_ARTIFACT_DIGEST
module.SOURCE_CIPHERTEXT_SHA256=SOURCE_CIPHERTEXT_SHA256
module.GENERAL_CALIBRATION_RUN=GENERAL_CALIBRATION_RUN
module.R3_CALIBRATION_RUN=R4_CALIBRATION_RUN
module.R3_CALIBRATION_REPORT_SHA256=R4_CALIBRATION_REPORT_SHA256
module.EXECUTOR=EXECUTOR
module.CHECKPOINT=CHECKPOINT
module.REPORT=REPORT
module.PROGRESS=PROGRESS

def decrypt_cases()->list[dict]:
    base=Path(os.environ.get('R4_PACK_DIR','r4-source'))
    manifest=json.load(open(base/'heldout-r4.manifest.json'))
    expected_blobs={
        'skill':SKILL_BLOB,
        'professional_model_base':BASE_MODEL_BLOB,
        'professional_model_repair':REPAIR_MODEL_BLOB,
    }
    if manifest['cycle_id']!=CYCLE or manifest['candidate_commit']!=CANDIDATE_COMMIT or manifest['candidate_blobs']!=expected_blobs:
        raise RuntimeError('R4 manifest candidate/cycle mismatch')
    parts=base/'heldout-r4.parts'
    token=''.join(p.read_text() for p in sorted(parts.iterdir())).encode()
    if module.h(token)!=SOURCE_CIPHERTEXT_SHA256 or manifest['ciphertext_sha256']!=SOURCE_CIPHERTEXT_SHA256:
        raise RuntimeError('R4 ciphertext digest mismatch')
    master=os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY','').encode().strip()
    if not master:
        raise RuntimeError('sealed master key missing')
    sys.path.insert(0,str(module.ROOT/'architect/evaluation/qualification-platform'))
    from sealed_pack_keys import derive_fernet_key
    payload=json.loads(Fernet(derive_fernet_key(master,CYCLE)).decrypt(token))
    cases=payload.get('cases')
    if not isinstance(cases,list) or len(cases)!=20:
        raise RuntimeError('R4 case cardinality mismatch')
    fam={x.get('family') for x in cases}
    if fam!=set(module.FAMILIES) or any(sum(1 for x in cases if x.get('family')==f)!=2 for f in module.FAMILIES):
        raise RuntimeError('R4 family structure mismatch')
    return cases

def candidate_call(case:dict)->str:
    constraints=case.get('constraints')
    if not isinstance(constraints,list) or not constraints or not all(isinstance(x,str) and x for x in constraints):
        raise RuntimeError('R4 constraints adapter requires non-empty array[string]')
    encoded=json.dumps(constraints,ensure_ascii=False,separators=(',',':'))
    if json.loads(encoded)!=constraints:
        raise RuntimeError('R4 constraints adapter round-trip mismatch')
    task={'brief':case['brief'],'context':case['context'],'constraints':encoded}
    proc=subprocess.run(
        ['python3',EXECUTOR,'--model-timeout','180'],
        input=json.dumps(task,ensure_ascii=False),
        text=True,capture_output=True,timeout=240,
    )
    if proc.returncode!=0:
        raise RuntimeError('candidate executor failure: '+proc.stdout[-800:]+proc.stderr[-400:])
    out=json.loads(proc.stdout)
    ident=out.get('candidate_identity') or {}
    expected={
        'candidate_commit':CANDIDATE_COMMIT,
        'skill_blob':SKILL_BLOB,
        'professional_model_base_blob':BASE_MODEL_BLOB,
        'professional_model_repair_blob':REPAIR_MODEL_BLOB,
    }
    if any(ident.get(k)!=v for k,v in expected.items()):
        raise RuntimeError('candidate identity mismatch')
    text=out.get('final_output')
    if not isinstance(text,str) or not text.strip():
        raise RuntimeError('candidate observable output empty')
    return text

module.decrypt_cases=decrypt_cases
module.candidate_call=candidate_call

def main()->int:
    cases=decrypt_cases()
    state=module.load_state()
    module.write_progress('IN_PROGRESS',state)
    try:
        for case in cases:
            cid=case['id']
            if cid not in state['candidate']:
                state['candidate'][cid]=candidate_call(case)
                module.save_state(state)
                module.write_progress('IN_PROGRESS',state)
            swap=random.Random(f'{SCORE_CYCLE}:{cid}').choice([False,True])
            baseline=case['competent_generic_baseline']
            cand=state['candidate'][cid]
            a,b=(baseline,cand) if swap else (cand,baseline)
            for provider,model in module.JUDGES:
                key=f'{cid}:{provider}'
                if key not in state['judges']:
                    state['judges'][key]=module.judge(provider,model,case,a,b)
                    module.save_state(state)
                    module.write_progress('IN_PROGRESS',state)

        rates,combined,disagree,dims,p0,adj,overall=module.metrics(cases,state)
        if p0:
            status='SEMANTIC_FAIL_P0'
        elif adj:
            status='SEMANTIC_ADJUDICATION_REQUIRED'
        elif overall and all(x['pass'] for x in dims.values()):
            status='SEMANTIC_PASS'
        else:
            status='SEMANTIC_REVISE'
        report={
            'cycle_id':SCORE_CYCLE,
            'status':status,
            'candidate':{
                'commit':CANDIDATE_COMMIT,
                'skill_blob':SKILL_BLOB,
                'professional_model_base_blob':BASE_MODEL_BLOB,
                'professional_model_repair_blob':REPAIR_MODEL_BLOB,
                'runtime_model':'gemini-3.5-flash-lite',
            },
            'source_artifact':{
                'run_id':SOURCE_RUN,
                'artifact_id':SOURCE_ARTIFACT_ID,
                'artifact_name':SOURCE_ARTIFACT_NAME,
                'artifact_digest':SOURCE_ARTIFACT_DIGEST,
                'sealed_ciphertext_sha256':SOURCE_CIPHERTEXT_SHA256,
                'source_head_sha':SOURCE_HEAD,
            },
            'calibration':{
                'general_run':GENERAL_CALIBRATION_RUN,
                'exact_r4_run':R4_CALIBRATION_RUN,
                'exact_r4_report_artifact_id':R4_CALIBRATION_REPORT_ARTIFACT_ID,
                'exact_r4_report_artifact_digest':R4_CALIBRATION_REPORT_ARTIFACT_DIGEST,
                'exact_r4_report_sha256':R4_CALIBRATION_REPORT_SHA256,
            },
            'judges':dict(module.JUDGES),
            'thresholds':module.THRESH,
            'case_count':20,
            'candidate_calls':len(state['candidate']),
            'judge_calls':{p:sum(1 for k in state['judges'] if k.endswith(':'+p)) for p,_ in module.JUDGES},
            'per_judge_candidate_preference_rate':rates,
            'combined_candidate_preference_rate':combined,
            'pair_disagreement_rate':disagree,
            'dimension_outcomes':dims,
            'confirmed_p0_count':len(p0),
            'p0_categories':sorted({x['category'] for x in p0}),
            'adjudication_required_count':len(adj),
            'family_adjudication_counts':{f:sum(1 for x in adj if x['family']==f) for f in module.FAMILIES},
            'hidden_content_printed':False,
            'rendered_gate_required_after_semantic_pass':True,
            'rendered_tasks':['P1_DISCOVER','P2_DIRECT','P3_REFINE','P4_ADVANCED_MEDIA_PAIR'],
        }
        REPORT.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        module.write_progress(status,state)
        print(json.dumps({
            'status':status,
            'candidate_calls':len(state['candidate']),
            'combined_candidate_preference_rate':combined,
            'pair_disagreement_rate':disagree,
            'confirmed_p0_count':len(p0),
            'adjudication_required_count':len(adj),
        },sort_keys=True))
        return 0 if status=='SEMANTIC_PASS' else (20 if status=='SEMANTIC_REVISE' else 21 if status=='SEMANTIC_FAIL_P0' else 22)
    except Exception as exc:
        module.save_state(state)
        module.write_progress('INFRASTRUCTURE_FAILURE',state,{'error':str(exc)[:600]})
        print(json.dumps({'status':'INFRASTRUCTURE_FAILURE','candidate_calls':len(state['candidate']),'error':str(exc)[:600]}))
        return 30

if __name__=='__main__':
    raise SystemExit(main())
