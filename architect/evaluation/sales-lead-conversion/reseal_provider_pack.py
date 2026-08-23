#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, os, shutil, sys, tempfile, zipfile
from pathlib import Path
from cryptography.fernet import Fernet


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-dir',required=True); ap.add_argument('--runner',required=True); ap.add_argument('--out',required=True); ap.add_argument('--cycle-id',required=True)
    args=ap.parse_args(); root=Path.cwd().resolve(); source=Path(args.source_dir).resolve(); out=Path(args.out).resolve(); runner=Path(args.runner).resolve()
    fixtures=(source/'fixtures.json').read_bytes(); grader=(source/'grader.json').read_bytes()
    sys.path.insert(0,str(root/'architect/evaluation/qualification-platform'))
    from sealed_pack_keys import derive_fernet_key,key_fingerprint_sha256
    if out.exists(): shutil.rmtree(out)
    parts=out/'parts'; parts.mkdir(parents=True)
    h=lambda b:hashlib.sha256(b).hexdigest()
    candidate_commit=os.environ['CANDIDATE_COMMIT']; candidate_digest=os.environ['CANDIDATE_DIGEST']; model=os.environ['SALES_MODEL']; source_digest=os.environ['SOURCE_PACK_DIGEST']
    with tempfile.TemporaryDirectory(prefix='sales-provider-reseal-') as td:
        p=Path(td); (p/'fixtures.json').write_bytes(fixtures); (p/'grader.json').write_bytes(grader); shutil.copyfile(runner,p/'runner.py')
        hashes={n:h((p/n).read_bytes()) for n in ('fixtures.json','grader.json','runner.py')}
        pack_digest='sha256:'+h(''.join(f'{n}:{hashes[n]}\n' for n in sorted(hashes)).encode())
        fx=json.loads(fixtures); repeats=sorted(x['id'] for x in fx if x.get('repeat_required'))
        freeze={'cycle_id':args.cycle_id,'candidate_commit':candidate_commit,'candidate_digest':candidate_digest,'model':model,'fixture_count':36,'family_count':12,'per_family':3,'repeat_fixture_count':6,'repeat_fixture_ids':repeats,'expected_candidate_runs_if_full':42,'fixtures_sha256':'sha256:'+hashes['fixtures.json'],'grader_sha256':'sha256:'+hashes['grader.json'],'runner_sha256':'sha256:'+hashes['runner.py'],'pack_digest':pack_digest,'release_tasks_passed_min':34,'per_family_min':2,'critical_hard_fails_max':0,'professional_failure_retry':0,'source_hidden_pack_digest':source_digest,'hidden_corpus_semantics_modified':False}
        (p/'freeze-record.json').write_text(json.dumps(freeze,indent=2,sort_keys=True)+'\n')
        zp=p/'pack.zip'
        with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for n in ('fixtures.json','grader.json','runner.py','freeze-record.json'): z.write(p/n,arcname=n)
        raw=zp.read_bytes(); key=derive_fernet_key(os.environ['QUALIFICATION_SEALED_PACK_MASTER_KEY'].encode().strip(),args.cycle_id); token=Fernet(key).encrypt(raw)
    text=token.decode('ascii'); chunks=[text[i:i+4000] for i in range(0,len(text),4000)]
    for i,c in enumerate(chunks): (parts/f'{i:02d}').write_text(c)
    manifest={'version':2,'cycle_id':args.cycle_id,'candidate':{'commit':candidate_commit,'digest':candidate_digest,'manifest_path':'architect/library/cores/sales-lead-conversion/0.3.0/manifest.json'},'runtime':{'executor_path':'architect/evaluation/sales-lead-conversion/executor_v0_3_gemini.py','executor_cmd':'python architect/evaluation/sales-lead-conversion/executor_v0_3_gemini.py','protocol':'sales-lead-conversion-candidate-v1','provider':'gemini-interactions-api','model':model,'credential_env':'GEMINI_API_KEY','candidate_timeout_seconds':180,'model_timeout_seconds':120,'workflow_timeout_seconds':5400,'contract_probe_argv':['python','architect/evaluation/sales-lead-conversion/executor_v0_3_gemini.py','--qualification-contract'],'tool_protocol':'sales-deterministic-tools-v1','state_protocol':'sales-state-checkpoint-v1','observable_protocol':'sales-observable-ledger-v1','canary_required':True,'canary_cmd':'python architect/evaluation/sales-lead-conversion/canary_v0_3_gemini.py'},'sealed_pack':{'parts_dir':str(parts.relative_to(root)),'part_count':len(chunks),'ciphertext_length':len(token),'ciphertext_sha256':h(token),'key_derivation':{'scheme':'hkdf-sha256-v1','master_env':'QUALIFICATION_SEALED_PACK_MASTER_KEY','context':args.cycle_id},'key_fingerprint_sha256':key_fingerprint_sha256(key),'decrypted_zip_sha256':h(raw),'pack_digest':pack_digest,'required_files':['fixtures.json','grader.json','runner.py','freeze-record.json']},'evaluation':{'fixture_count':36,'family_count':12,'per_family':3,'fixtures_file':'fixtures.json','grader_file':'grader.json','runner_file':'runner.py','freeze_record_file':'freeze-record.json'},'report':{'sanitized_required':True,'artifact_required':True,'validator_path':'architect/evaluation/qualification-platform/validate_sanitized_report.py','release_ledger_required':True},'verdict':{'runner_exit_zero_required':True,'missing_report_is_failure':True,'report_validation_required':True,'artifact_upload_required':True}}
    (out/'qualification.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'SEALED','cycle_id':args.cycle_id,'pack_digest':pack_digest,'fixture_count':36,'hidden_content_printed':False}))
    return 0

if __name__=='__main__': raise SystemExit(main())
