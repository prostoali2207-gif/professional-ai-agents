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

CYCLE='visual-design-art-direction-0.3.0-independent-2026-09-01-r6-semantic'
SCORE_CYCLE=CYCLE+'-scored-v1'
CANDIDATE_COMMIT='b4793a66172d4de7fe0ade1b0001bc2621829db2'
FREEZE_INTEGRITY_COMMIT='347491bbedeaee6fbda038db9639f16040a41301'
FREEZE_BLOB='84db2da24f784591c7cc1feb5f1f9a9c22220e40'
SKILL_BLOB='bee4ee67a8aff43016e158f37a6f421cd079581a'
BASE_MODEL_BLOB='bbea595e299445cf79f798ed1e86eecd0b53cd50'
REPAIR_V02_MODEL_BLOB='bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50'
REPAIR_V03_MODEL_BLOB='dd42d50f07b804c1ddd3c93b96704e0c6256440c'
SOURCE_RUN=33500210303
SOURCE_HEAD='7e506c6afb85489758bbf8c2ad08ede75264fd1d'
SOURCE_ARTIFACT_ID=9797673448
SOURCE_ARTIFACT_NAME='visual-design-art-direction-v0-3-encrypted-heldout-pack-r6'
SOURCE_ARTIFACT_DIGEST='sha256:9e6286ec436031aa121e631f0613216236322598ed71d8ae8c22938050886142'
SOURCE_CIPHERTEXT_SHA256='ffecad8a5087bda276a95825a1e0071ca18640392a12dbb26f0f8ec5ba78cdeb'
GENERAL_CALIBRATION_RUN=33262394565
R6_CALIBRATION_RUN=33580704653
R6_CALIBRATION_REPORT_ARTIFACT_ID=9829104778
R6_CALIBRATION_REPORT_ARTIFACT_DIGEST='sha256:b3d1a066465ae5bcd95363424e8c62f64e383b6e134388b8475c774773eedfe1'
R6_CALIBRATION_REPORT_SHA256='623697cb127501b3ef57f60716f980ae7d252037d5843aa1f90a0de030325239'
EXECUTOR='architect/evaluation/visual-design-art-direction/semantic/executor_r6_v0_3_gemini.py'
CHECKPOINT=Path('visual-r6-v03-semantic-checkpoint.enc')
REPORT=Path('visual-r6-v03-semantic-sanitized-report.json')
PROGRESS=Path('visual-r6-v03-semantic-progress.json')
PAIRED_FAMILIES={'REFERENCE','MOBILE','TRUTH','ADVANCED_MEDIA_ROUTING','AUTHORITY_BOUNDARY'}

# Rebind only release identity/transport data. Judge models, P0 categories,
# family dimensions, thresholds, A/B protocol, transient retry semantics and
# Gemini schema enforcement remain inherited from the already-calibrated path.
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
module.R3_CALIBRATION_RUN=R6_CALIBRATION_RUN
module.R3_CALIBRATION_REPORT_SHA256=R6_CALIBRATION_REPORT_SHA256
module.EXECUTOR=EXECUTOR
module.CHECKPOINT=CHECKPOINT
module.REPORT=REPORT
module.PROGRESS=PROGRESS

def decrypt_cases()->list[dict]:
    base=Path(os.environ.get('R6_PACK_DIR','r6-source'))
    manifest=json.load(open(base/'heldout-r6.manifest.json'))
    expected_blobs={
        'skill':SKILL_BLOB,
        'professional_model_base':BASE_MODEL_BLOB,
        'professional_model_repair_v02':REPAIR_V02_MODEL_BLOB,
        'professional_model_repair_v03':REPAIR_V03_MODEL_BLOB,
    }
    if manifest.get('schema_version')!='0.6':
        raise RuntimeError('R6 manifest schema mismatch')
    if manifest['cycle_id']!=CYCLE or manifest['candidate_commit']!=CANDIDATE_COMMIT or manifest['candidate_blobs']!=expected_blobs:
        raise RuntimeError('R6 manifest candidate/cycle mismatch')
    if manifest.get('freeze_integrity_commit')!=FREEZE_INTEGRITY_COMMIT or manifest.get('candidate_freeze_blob')!=FREEZE_BLOB:
        raise RuntimeError('R6 freeze identity mismatch')
    if manifest.get('item_count')!=20 or manifest.get('family_count')!=10 or manifest.get('pair_count')!=5:
        raise RuntimeError('R6 manifest cardinality mismatch')
    if manifest.get('pair_contract_count')!=5 or manifest.get('pair_contract_schema_version')!='0.1':
        raise RuntimeError('R6 pair-contract manifest mismatch')
    if manifest.get('candidate_calls')!=0 or manifest.get('hidden_content_printed') is not False:
        raise RuntimeError('R6 source contamination flag mismatch')
    if any(manifest.get(k) is not False for k in ('historical_r3_reused','historical_r4_reused','historical_r5_reused')):
        raise RuntimeError('R6 historical reuse flag mismatch')
    parts=base/'heldout-r6.parts'
    token=''.join(p.read_text() for p in sorted(parts.iterdir())).encode()
    if module.h(token)!=SOURCE_CIPHERTEXT_SHA256 or manifest['ciphertext_sha256']!=SOURCE_CIPHERTEXT_SHA256:
        raise RuntimeError('R6 ciphertext digest mismatch')
    master=os.environ.get('QUALIFICATION_SEALED_PACK_MASTER_KEY','').encode().strip()
    if not master:
        raise RuntimeError('sealed master key missing')
    sys.path.insert(0,str(module.ROOT/'architect/evaluation/qualification-platform'))
    from sealed_pack_keys import derive_fernet_key
    payload=json.loads(Fernet(derive_fernet_key(master,CYCLE)).decrypt(token))
    if payload.get('cycle_id')!=CYCLE or payload.get('candidate_commit')!=CANDIDATE_COMMIT or payload.get('candidate_blobs')!=expected_blobs:
        raise RuntimeError('R6 payload candidate/cycle mismatch')
    if payload.get('freeze_integrity_commit')!=FREEZE_INTEGRITY_COMMIT or payload.get('candidate_freeze_blob')!=FREEZE_BLOB:
        raise RuntimeError('R6 payload freeze identity mismatch')
    pair_contracts=payload.get('pair_contracts')
    if not isinstance(pair_contracts,dict) or set(pair_contracts)!=PAIRED_FAMILIES:
        raise RuntimeError('R6 evaluator-only pair-contract coverage mismatch')
    cases=payload.get('cases')
    if not isinstance(cases,list) or len(cases)!=20:
        raise RuntimeError('R6 case cardinality mismatch')
    fam={x.get('family') for x in cases}
    if fam!=set(module.FAMILIES) or any(sum(1 for x in cases if x.get('family')==f)!=2 for f in module.FAMILIES):
        raise RuntimeError('R6 family structure mismatch')
    return cases

def candidate_call(case:dict)->str:
    constraints=case.get('constraints')
    if not isinstance(constraints,list) or not constraints or not all(isinstance(x,str) and x for x in constraints):
        raise RuntimeError('R6 constraints adapter requires non-empty array[string]')
    encoded=json.dumps(constraints,ensure_ascii=False,separators=(',',':'))
    if json.loads(encoded)!=constraints:
        raise RuntimeError('R6 constraints adapter round-trip mismatch')
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
        'professional_model_repair_v02_blob':REPAIR_V02_MODEL_BLOB,
        'professional_model_repair_v03_blob':REPAIR_V03_MODEL_BLOB,
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
                'freeze_integrity_commit':FREEZE_INTEGRITY_COMMIT,
                'candidate_freeze_blob':FREEZE_BLOB,
                'skill_blob':SKILL_BLOB,
                'professional_model_base_blob':BASE_MODEL_BLOB,
                'professional_model_repair_v02_blob':REPAIR_V02_MODEL_BLOB,
                'professional_model_repair_v03_blob':REPAIR_V03_MODEL_BLOB,
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
                'exact_r6_run':R6_CALIBRATION_RUN,
                'exact_r6_report_artifact_id':R6_CALIBRATION_REPORT_ARTIFACT_ID,
                'exact_r6_report_artifact_digest':R6_CALIBRATION_REPORT_ARTIFACT_DIGEST,
                'exact_r6_report_sha256':R6_CALIBRATION_REPORT_SHA256,
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
            'pair_contract_exposed_to_candidate':False,
            'pair_contract_used_as_new_grading_signal':False,
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
