#!/usr/bin/env python3
import argparse, json, os, subprocess, hashlib
from collections import defaultdict
from pathlib import Path

CANDIDATE_COMMIT = 'd7430fa99c10cfc89dd0f12872970e4b629bf9e6'
EVALUATOR_VERSION = 'workflow-controller-independent-heldout-v1'

STATES = {
 'INTAKE': ['STRATEGY_REQUIRED','BLOCKED','CANCELLED'],
 'STRATEGY_REQUIRED': ['STRATEGY_IN_PROGRESS','BLOCKED'],
 'STRATEGY_IN_PROGRESS': ['EXPERIMENT_APPROVAL_REQUIRED','RESEARCH_REQUIRED','BLOCKED'],
 'RESEARCH_REQUIRED': ['RESEARCH_IN_PROGRESS','BLOCKED'],
 'RESEARCH_IN_PROGRESS': ['STRATEGY_REQUIRED','BLOCKED'],
 'EXPERIMENT_APPROVAL_REQUIRED': ['CONTENT_ANALYSIS_REQUIRED','PARKED','CANCELLED'],
 'CONTENT_ANALYSIS_REQUIRED': ['CONTENT_ANALYSIS_IN_PROGRESS','BLOCKED'],
 'CONTENT_ANALYSIS_IN_PROGRESS': ['CREATIVE_REQUIRED','STRATEGY_REQUIRED','BLOCKED'],
 'CREATIVE_REQUIRED': ['CREATIVE_IN_PROGRESS','BLOCKED'],
 'CREATIVE_IN_PROGRESS': ['POST_PRODUCTION_REQUIRED','CONTENT_ANALYSIS_REQUIRED','STRATEGY_REQUIRED','BLOCKED'],
 'POST_PRODUCTION_REQUIRED': ['POST_PRODUCTION_IN_PROGRESS','BLOCKED'],
 'POST_PRODUCTION_IN_PROGRESS': ['CREATIVE_APPROVAL_REQUIRED','CREATIVE_REQUIRED','CONTENT_ANALYSIS_REQUIRED','STRATEGY_REQUIRED','BLOCKED'],
 'CREATIVE_APPROVAL_REQUIRED': ['READY_TO_PUBLISH','POST_PRODUCTION_REQUIRED','CANCELLED'],
 'READY_TO_PUBLISH': ['PUBLISHING','BLOCKED'],
 'PUBLISHING': ['PUBLISHED','BLOCKED'],
 'PUBLISHED': ['MEASUREMENT_WAIT','BLOCKED'],
 'MEASUREMENT_WAIT': ['ANALYTICS_REQUIRED','BLOCKED'],
 'ANALYTICS_REQUIRED': ['ANALYTICS_IN_PROGRESS','BLOCKED'],
 'ANALYTICS_IN_PROGRESS': ['STRATEGIST_DECISION_REQUIRED','BLOCKED'],
 'STRATEGIST_DECISION_REQUIRED': ['SCALE_APPROVAL_REQUIRED','ITERATION_REQUIRED','KILLED','PARKED','MEASUREMENT_WAIT'],
 'SCALE_APPROVAL_REQUIRED': ['SCALED','PARKED'],
 'ITERATION_REQUIRED': ['CONTENT_ANALYSIS_REQUIRED','RESEARCH_REQUIRED','BLOCKED'],
 'SCALED': [], 'KILLED': [], 'PARKED': ['STRATEGY_REQUIRED'], 'BLOCKED': ['RESUME_LAST_VALID'], 'CANCELLED': []
}
OWNERS = {
 'INTAKE':'ORCHESTRATOR','STRATEGY_REQUIRED':'ORCHESTRATOR','STRATEGY_IN_PROGRESS':'STRATEGIST',
 'RESEARCH_REQUIRED':'ORCHESTRATOR','RESEARCH_IN_PROGRESS':'MARKET_INTELLIGENCE','EXPERIMENT_APPROVAL_REQUIRED':'HUMAN',
 'CONTENT_ANALYSIS_REQUIRED':'ORCHESTRATOR','CONTENT_ANALYSIS_IN_PROGRESS':'CONTENT_ANALYST','CREATIVE_REQUIRED':'ORCHESTRATOR',
 'CREATIVE_IN_PROGRESS':'CONTENT_CREATOR','POST_PRODUCTION_REQUIRED':'ORCHESTRATOR','POST_PRODUCTION_IN_PROGRESS':'VIDEO_POST_PRODUCTION',
 'CREATIVE_APPROVAL_REQUIRED':'HUMAN','READY_TO_PUBLISH':'ORCHESTRATOR','PUBLISHING':'PUBLISHER','PUBLISHED':'ORCHESTRATOR',
 'MEASUREMENT_WAIT':'ORCHESTRATOR','ANALYTICS_REQUIRED':'ORCHESTRATOR','ANALYTICS_IN_PROGRESS':'ANALYTICS',
 'STRATEGIST_DECISION_REQUIRED':'STRATEGIST','SCALE_APPROVAL_REQUIRED':'HUMAN','ITERATION_REQUIRED':'STRATEGIST',
 'SCALED':'NONE','KILLED':'NONE','PARKED':'NONE','BLOCKED':'DYNAMIC_BLOCKER_OWNER','CANCELLED':'NONE'
}
TASK_OWNERS = {
 'RESEARCH':'MARKET_INTELLIGENCE','DESIGN_EXPERIMENT':'STRATEGIST','APPROVE_EXPERIMENT':'HUMAN','ANALYZE_CONTENT':'CONTENT_ANALYST',
 'CREATE_CONTENT':'CONTENT_CREATOR','POST_PRODUCE_VIDEO':'VIDEO_POST_PRODUCTION','APPROVE_CREATIVE':'HUMAN','PUBLISH':'PUBLISHER',
 'HANDLE_LEAD':'SALES_LEAD_AGENT','COLLECT_MEASUREMENT':'ORCHESTRATOR','ANALYZE_EXPERIMENT':'ANALYTICS','DECIDE_PORTFOLIO':'STRATEGIST',
 'APPROVE_SCALE':'HUMAN','REPAIR_DATA':'DYNAMIC_DATA_OWNER','RESOLVE_CONTRACT_VIOLATION':'DYNAMIC_PRODUCER_OR_HUMAN'
}
FORBIDDEN = {'RESEARCH','DESIGN_EXPERIMENT','ANALYZE_CONTENT','CREATE_CONTENT','POST_PRODUCE_VIDEO','HANDLE_LEAD','ANALYZE_EXPERIMENT','DECIDE_PORTFOLIO'}
ACTORS = ['ORCHESTRATOR','MARKET_INTELLIGENCE','STRATEGIST','CONTENT_ANALYST','CONTENT_CREATOR','VIDEO_POST_PRODUCTION','PUBLISHER','SALES_LEAD_AGENT','ANALYTICS','HUMAN']
RETRY = {
 'DATA_NOT_READY':'SCHEDULE_WAKEUP','CONTRACT':'RETURN_ONCE_THEN_ESCALATE','BUSINESS_FACT':'REQUEST_AUTHORITATIVE_RESOLUTION',
 'PERMISSION':'REQUEST_AUTHORITY','LOGIC':'BLOCK_AND_ESCALATE','SAFETY_COMPLIANCE':'BLOCK_AND_ESCALATE','UNKNOWN_EXCEPTION':'BLOCK_AND_ESCALATE'
}
SIDE_EFFECTS = {'PUBLISH','HANDLE_LEAD','CREATE_APPOINTMENT','SEND_OUTBOUND_MESSAGE','RESERVE_VEHICLE','TAKE_DEPOSIT'}

ops=[]; expected=[]; families=[]
def add(family, fn, args, exp):
    ops.append({'fn':fn,'args':args}); expected.append(exp); families.append(family)

# exhaustive owner checks
for s, owner in OWNERS.items():
    for blocker_owner in [None,'HUMAN','STRATEGIST']:
        exp = blocker_owner if owner == 'DYNAMIC_BLOCKER_OWNER' else owner
        add('ownership','expectedOwner',{'state':s,'blockerOwner':blocker_owner},exp)
add('ownership','expectedOwner',{'state':'UNKNOWN','blockerOwner':'HUMAN'},None)

# exhaustive ordinary graph edges
for src in STATES:
    if src in ('BLOCKED','PARKED'): continue
    for dst in STATES:
        ok = dst in STATES[src]
        add('transitions','canTransition',{'from':src,'to':dst,'options':{}},{'ok':ok,'code':'LEGAL_TRANSITION' if ok else 'ILLEGAL_TRANSITION'})
# invalid states/targets
add('transitions','canTransition',{'from':'NOT_A_STATE','to':'INTAKE','options':{}},{'ok':False,'code':'UNKNOWN_STATE'})
add('transitions','canTransition',{'from':'INTAKE','to':'NOT_A_STATE','options':{}},{'ok':False,'code':'UNKNOWN_TARGET_STATE'})
# blocked recovery contrastives
for prior in [s for s in STATES if s not in ('BLOCKED','SCALED','KILLED','CANCELLED')]:
    add('recovery','canTransition',{'from':'BLOCKED','to':prior,'options':{}},{'ok':False,'code':'MISSING_BLOCKED_FROM_STATE'})
    add('recovery','canTransition',{'from':'BLOCKED','to':prior,'options':{'blockedFromState':prior,'blockers':[{'status':'OPEN'}]}},{'ok':False,'code':'BLOCKER_STILL_OPEN'})
    add('recovery','canTransition',{'from':'BLOCKED','to':prior,'options':{'blockedFromState':prior,'blockers':[{'status':'RESOLVED'}]}},{'ok':True,'code':'LEGAL_BLOCKED_RESUME'})
    wrong = 'INTAKE' if prior != 'INTAKE' else 'STRATEGY_REQUIRED'
    add('recovery','canTransition',{'from':'BLOCKED','to':wrong,'options':{'blockedFromState':prior,'blockers':[{'status':'RESOLVED'}]}},{'ok':False,'code':'INVALID_BLOCKED_RESUME'})
# parked reopening
for dst in STATES:
    for trigger in [None,'ORCHESTRATOR','STRATEGIST','HUMAN']:
        if dst != 'STRATEGY_REQUIRED': exp={'ok':False,'code':'ILLEGAL_TRANSITION'}
        elif trigger in ('STRATEGIST','HUMAN'): exp={'ok':True,'code':'LEGAL_PARKED_REOPEN'}
        else: exp={'ok':False,'code':'PARKED_REOPEN_TRIGGER_REQUIRED'}
        add('recovery','canTransition',{'from':'PARKED','to':dst,'options':{'reopenTrigger':trigger}},exp)

# authority matrix
for task, owner in TASK_OWNERS.items():
    if owner.startswith('DYNAMIC_'):
        for dynamic in ['HUMAN','STRATEGIST','ANALYTICS']:
            for actor in ACTORS:
                if actor == dynamic: exp={'ok':True,'code':'AUTHORIZED_DYNAMIC_TASK_OWNER','expectedOwner':dynamic}
                else: exp={'ok':False,'code':'WRONG_TASK_OWNER','expectedOwner':dynamic}
                add('authority','validateTaskAuthority',{'actor':actor,'taskType':task,'options':{'dynamicOwner':dynamic}},exp)
        add('authority','validateTaskAuthority',{'actor':'HUMAN','taskType':task,'options':{}},{'ok':False,'code':'DYNAMIC_OWNER_REQUIRED'})
    else:
        for actor in ACTORS:
            if actor == 'ORCHESTRATOR' and task in FORBIDDEN:
                exp={'ok':False,'code':'CONTROLLER_SPECIALIST_OVERREACH','expectedOwner':owner}
            elif actor == owner:
                exp={'ok':True,'code':'AUTHORIZED_TASK_OWNER','expectedOwner':owner}
            else:
                exp={'ok':False,'code':'WRONG_TASK_OWNER','expectedOwner':owner}
            add('authority','validateTaskAuthority',{'actor':actor,'taskType':task,'options':{}},exp)
add('authority','validateTaskAuthority',{'actor':'ORCHESTRATOR','taskType':'UNKNOWN_TASK','options':{}},{'ok':False,'code':'UNKNOWN_TASK_TYPE'})

# revision/concurrency
for a,b in [(1,1),(7,7),(1,2),(9,8),(0,0),(-1,-1),(3,3.0),(3,'3'),(None,3)]:
    if not isinstance(a,int) or isinstance(a,bool) or not isinstance(b,int) or isinstance(b,bool): exp={'ok':False,'code':'INVALID_REVISION'}
    elif a != b: exp={'ok':False,'code':'REVISION_CONFLICT'}
    else: exp={'ok':True,'code':'REVISION_MATCH'}
    add('concurrency','validateRevision',{'expectedRevision':a,'submittedRevision':b},exp)

# retry policy
for attempt in range(1,7):
    rem=max(0,2-(attempt-1)); auto=rem>0
    add('retry','retryDirective',{'errorClass':'TRANSIENT_TOOL','attempt':attempt},{'automatic':auto,'directive':'RETRY_TRANSIENT' if auto else 'EXHAUSTED_BLOCK','retriesRemaining':rem,'sameIdempotencyKey':True,'code':'TRANSIENT_TOOL'})
for cls,directive in RETRY.items():
    for attempt in (1,3,99): add('retry','retryDirective',{'errorClass':cls,'attempt':attempt},{'automatic':False,'directive':directive,'code':cls})
add('retry','retryDirective',{'errorClass':'ALIEN_FAILURE','attempt':1},{'automatic':False,'directive':'BLOCK_AND_ESCALATE','code':'UNKNOWN_ERROR_CLASS'})

# side-effect reconciliation
for task in list(SIDE_EFFECTS)+['DESIGN_EXPERIMENT','COLLECT_MEASUREMENT','ANALYZE_EXPERIMENT']:
    for known in [True,False,None]:
        if task not in SIDE_EFFECTS: exp={'required':False,'code':'NO_SIDE_EFFECT_RECONCILIATION_REQUIRED'}
        elif known is True: exp={'required':False,'code':'SIDE_EFFECT_OUTCOME_KNOWN'}
        else: exp={'required':True,'code':'RECONCILE_BEFORE_RETRY'}
        add('side_effects','requiresReconciliation',{'taskType':task,'outcomeKnown':known},exp)

# approval exact identity and mutations
base_refs=[{'artifact_id':'A','version':'1','sha256_or_revision':'sha-a'},{'artifact_id':'B','version':'2','sha256_or_revision':'sha-b'}]
base_scope={'experiment_id':'E','experiment_version':'7','artifact_refs':base_refs}
def approval(payload, exp): add('approvals','validateApproval',{'payload':payload},exp)
approval({'status':'PENDING','expired':False,'approvalScope':base_scope,'currentScope':base_scope},{'ok':False,'code':'APPROVAL_NOT_APPROVED'})
approval({'status':'APPROVED','expired':True,'approvalScope':base_scope,'currentScope':base_scope},{'ok':False,'code':'APPROVAL_EXPIRED'})
approval({'status':'APPROVED','expired':False,'approvalScope':None,'currentScope':base_scope},{'ok':False,'code':'APPROVAL_SCOPE_MISSING'})
approval({'status':'APPROVED','expired':False,'approvalScope':base_scope,'currentScope':{'experiment_id':'X','experiment_version':'7','artifact_refs':base_refs}},{'ok':False,'code':'APPROVAL_EXPERIMENT_SCOPE_MISMATCH'})
approval({'status':'APPROVED','expired':False,'approvalScope':base_scope,'currentScope':{'experiment_id':'E','experiment_version':'8','artifact_refs':base_refs}},{'ok':False,'code':'APPROVAL_EXPERIMENT_SCOPE_MISMATCH'})
approval({'status':'APPROVED','expired':False,'approvalScope':base_scope,'currentScope':{'experiment_id':'E','experiment_version':'7','artifact_refs':list(reversed(base_refs))}},{'ok':True,'code':'APPROVAL_CURRENT'})
approval({'status':'APPROVED','expired':False,'approvalScope':base_scope,'currentScope':{'experiment_id':'E','experiment_version':'7','artifact_refs':[base_refs[0],{'artifact_id':'B','version':'2','sha256_or_revision':'changed'}]}},{'ok':False,'code':'APPROVAL_ARTIFACT_SCOPE_MISMATCH'})

# artifact joins
def art(refs, exp): add('artifacts','validateArtifactJoin',{'refs':refs},exp)
art([],{'ok':False,'code':'NO_ARTIFACTS'})
valid=[{'artifact_id':'A','version':'1','sha256_or_revision':'h1','experiment_id':'E','experiment_version':'1','validation_status':'VALID'},{'artifact_id':'B','version':'1','sha256_or_revision':'h2','experiment_id':'E','experiment_version':'1','validation_status':'VALID'}]
art(valid,{'ok':True,'code':'ARTIFACT_JOIN_VALID'})
for field in ('artifact_id','version','sha256_or_revision'):
    bad=[dict(valid[0])]; bad[0][field]=''; art(bad,{'ok':False,'code':'ARTIFACT_IDENTITY_INCOMPLETE'})
bad=[dict(valid[0]),dict(valid[1])]; bad[1]['experiment_id']='X'; art(bad,{'ok':False,'code':'EXPERIMENT_ID_MISMATCH'})
bad=[dict(valid[0]),dict(valid[1])]; bad[1]['experiment_version']='2'; art(bad,{'ok':False,'code':'EXPERIMENT_VERSION_MISMATCH'})
bad=[dict(valid[0])]; bad[0]['validation_status']='STALE'; art(bad,{'ok':False,'code':'INVALID_OR_STALE_ARTIFACT'})

# parallel inquiry routing
for s in STATES:
    add('sales_parallel','routeInquiry',{'payload':{'inquiryExists':False,'currentExperimentState':s}},{'dispatch':False,'code':'NO_INQUIRY'})
    add('sales_parallel','routeInquiry',{'payload':{'inquiryExists':True,'currentExperimentState':s}},{'dispatch':True,'targetOwner':'SALES_LEAD_AGENT','preserveExperimentState':s,'code':'ROUTE_SALES_IN_PARALLEL'})
add('exceptions','unknownExceptionDirective',{}, {'action':'BLOCK','targetOwner':'HUMAN','code':'UNKNOWN_EXCEPTION'})

# Run candidate through bridge once.
parser=argparse.ArgumentParser(); parser.add_argument('--candidate-dir',required=True); parser.add_argument('--out',required=True); args=parser.parse_args()
candidate_dir=Path(args.candidate_dir).resolve(); module=candidate_dir/'scripts/orchestrator-policy.mjs'; bridge=Path(__file__).with_name('candidate_bridge.mjs')
proc=subprocess.run(['node',str(bridge),str(module)],input=json.dumps(ops),text=True,capture_output=True,timeout=60)
if proc.returncode != 0:
    raise SystemExit(f'candidate bridge failed: {proc.stderr[:500]}')
actual=json.loads(proc.stdout)

failures=[]; fam=defaultdict(lambda:{'total':0,'passed':0})
for i,(row,exp,family) in enumerate(zip(actual,expected,families)):
    fam[family]['total']+=1
    passed = row.get('ok') is True and row.get('value') == exp
    if passed: fam[family]['passed']+=1
    else: failures.append({'index':i,'family':family})

# Cross-check schema obligations independently of executable policy.
schema=json.loads((candidate_dir/'data-schemas/orchestrator-workflow.schema.json').read_text())
props=schema['properties']; approval_props=props['approvals']['items']['properties']; blocker_props=props['blockers']['items']['properties']
schema_checks={
 'blocked_from_state_present':'blocked_from_state' in props,
 'approval_scope_present':'scope' in approval_props or 'artifact_refs' in approval_props or 'approved_artifact_refs' in approval_props,
 'blocker_status_present':'status' in blocker_props,
 'revision_required':'revision' in schema.get('required',[]),
}
for k,v in schema_checks.items():
    fam['schema']['total']+=1
    if v: fam['schema']['passed']+=1
    else: failures.append({'index':f'schema:{k}','family':'schema'})

# Verify exact candidate commit from checkout.
head=subprocess.check_output(['git','-C',str(candidate_dir),'rev-parse','HEAD'],text=True).strip()
commit_ok=head==CANDIDATE_COMMIT
fam['freeze']['total']+=1
if commit_ok: fam['freeze']['passed']+=1
else: failures.append({'index':'freeze:commit','family':'freeze'})

report={
 'cycle_id':'workflow-controller-independent-heldout-2026-08-22',
 'evaluator_version':EVALUATOR_VERSION,
 'candidate_commit':head,
 'expected_candidate_commit':CANDIDATE_COMMIT,
 'case_count':len(ops)+len(schema_checks)+1,
 'families':dict(fam),
 'failure_count':len(failures),
 'critical_failure_count':len(failures),
 'verdict':'PASS' if not failures else 'REVISE',
 'failure_indices':failures[:50],
 'case_fingerprint':hashlib.sha256(json.dumps(ops,sort_keys=True).encode()).hexdigest()
}
Path(args.out).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('cycle_id','case_count','failure_count','critical_failure_count','verdict')},indent=2))
raise SystemExit(0 if not failures else 1)
