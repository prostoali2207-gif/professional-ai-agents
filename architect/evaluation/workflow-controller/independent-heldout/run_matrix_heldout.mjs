import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';

const candidateDir = path.resolve(process.argv[2] ?? '');
const outPath = process.argv[3];
if (!candidateDir || !outPath) throw new Error('usage: node run_matrix_heldout.mjs <candidate-dir> <report>');

const EXPECTED_COMMIT = 'd7430fa99c10cfc89dd0f12872970e4b629bf9e6';
const candidate = await import(pathToFileURL(path.join(candidateDir, 'scripts/orchestrator-policy.mjs')).href);
const families = new Map();
const failures = [];
function stat(f){ if(!families.has(f)) families.set(f,{total:0,passed:0}); return families.get(f); }
function check(f, condition){ const s=stat(f); s.total++; if(condition) s.passed++; else failures.push(f); }
function eq(a,b){ return JSON.stringify(a)===JSON.stringify(b); }

const graph={
INTAKE:['STRATEGY_REQUIRED','BLOCKED','CANCELLED'],STRATEGY_REQUIRED:['STRATEGY_IN_PROGRESS','BLOCKED'],STRATEGY_IN_PROGRESS:['EXPERIMENT_APPROVAL_REQUIRED','RESEARCH_REQUIRED','BLOCKED'],RESEARCH_REQUIRED:['RESEARCH_IN_PROGRESS','BLOCKED'],RESEARCH_IN_PROGRESS:['STRATEGY_REQUIRED','BLOCKED'],EXPERIMENT_APPROVAL_REQUIRED:['CONTENT_ANALYSIS_REQUIRED','PARKED','CANCELLED'],CONTENT_ANALYSIS_REQUIRED:['CONTENT_ANALYSIS_IN_PROGRESS','BLOCKED'],CONTENT_ANALYSIS_IN_PROGRESS:['CREATIVE_REQUIRED','STRATEGY_REQUIRED','BLOCKED'],CREATIVE_REQUIRED:['CREATIVE_IN_PROGRESS','BLOCKED'],CREATIVE_IN_PROGRESS:['POST_PRODUCTION_REQUIRED','CONTENT_ANALYSIS_REQUIRED','STRATEGY_REQUIRED','BLOCKED'],POST_PRODUCTION_REQUIRED:['POST_PRODUCTION_IN_PROGRESS','BLOCKED'],POST_PRODUCTION_IN_PROGRESS:['CREATIVE_APPROVAL_REQUIRED','CREATIVE_REQUIRED','CONTENT_ANALYSIS_REQUIRED','STRATEGY_REQUIRED','BLOCKED'],CREATIVE_APPROVAL_REQUIRED:['READY_TO_PUBLISH','POST_PRODUCTION_REQUIRED','CANCELLED'],READY_TO_PUBLISH:['PUBLISHING','BLOCKED'],PUBLISHING:['PUBLISHED','BLOCKED'],PUBLISHED:['MEASUREMENT_WAIT','BLOCKED'],MEASUREMENT_WAIT:['ANALYTICS_REQUIRED','BLOCKED'],ANALYTICS_REQUIRED:['ANALYTICS_IN_PROGRESS','BLOCKED'],ANALYTICS_IN_PROGRESS:['STRATEGIST_DECISION_REQUIRED','BLOCKED'],STRATEGIST_DECISION_REQUIRED:['SCALE_APPROVAL_REQUIRED','ITERATION_REQUIRED','KILLED','PARKED','MEASUREMENT_WAIT'],SCALE_APPROVAL_REQUIRED:['SCALED','PARKED'],ITERATION_REQUIRED:['CONTENT_ANALYSIS_REQUIRED','RESEARCH_REQUIRED','BLOCKED'],SCALED:[],KILLED:[],PARKED:['STRATEGY_REQUIRED'],BLOCKED:['RESUME_LAST_VALID'],CANCELLED:[]};
const states=Object.keys(graph);
const owners={INTAKE:'ORCHESTRATOR',STRATEGY_REQUIRED:'ORCHESTRATOR',STRATEGY_IN_PROGRESS:'STRATEGIST',RESEARCH_REQUIRED:'ORCHESTRATOR',RESEARCH_IN_PROGRESS:'MARKET_INTELLIGENCE',EXPERIMENT_APPROVAL_REQUIRED:'HUMAN',CONTENT_ANALYSIS_REQUIRED:'ORCHESTRATOR',CONTENT_ANALYSIS_IN_PROGRESS:'CONTENT_ANALYST',CREATIVE_REQUIRED:'ORCHESTRATOR',CREATIVE_IN_PROGRESS:'CONTENT_CREATOR',POST_PRODUCTION_REQUIRED:'ORCHESTRATOR',POST_PRODUCTION_IN_PROGRESS:'VIDEO_POST_PRODUCTION',CREATIVE_APPROVAL_REQUIRED:'HUMAN',READY_TO_PUBLISH:'ORCHESTRATOR',PUBLISHING:'PUBLISHER',PUBLISHED:'ORCHESTRATOR',MEASUREMENT_WAIT:'ORCHESTRATOR',ANALYTICS_REQUIRED:'ORCHESTRATOR',ANALYTICS_IN_PROGRESS:'ANALYTICS',STRATEGIST_DECISION_REQUIRED:'STRATEGIST',SCALE_APPROVAL_REQUIRED:'HUMAN',ITERATION_REQUIRED:'STRATEGIST',SCALED:'NONE',KILLED:'NONE',PARKED:'NONE',BLOCKED:'DYNAMIC_BLOCKER_OWNER',CANCELLED:'NONE'};
for(const [s,o] of Object.entries(owners)){ check('ownership',candidate.expectedOwner(s,'HUMAN')===(o==='DYNAMIC_BLOCKER_OWNER'?'HUMAN':o)); }
check('ownership',candidate.expectedOwner('BOGUS','HUMAN')===null);

for(const from of states){ if(['BLOCKED','PARKED'].includes(from)) continue; for(const to of states){ const ok=graph[from].includes(to); check('transitions',eq(candidate.canTransition(from,to),{ok,code:ok?'LEGAL_TRANSITION':'ILLEGAL_TRANSITION'})); }}
check('transitions',eq(candidate.canTransition('BOGUS','INTAKE'),{ok:false,code:'UNKNOWN_STATE'}));
check('transitions',eq(candidate.canTransition('INTAKE','BOGUS'),{ok:false,code:'UNKNOWN_TARGET_STATE'}));

for(const prior of states.filter(s=>!['BLOCKED','SCALED','KILLED','CANCELLED'].includes(s))){
 check('recovery',candidate.canTransition('BLOCKED',prior,{}).code==='MISSING_BLOCKED_FROM_STATE');
 check('recovery',candidate.canTransition('BLOCKED',prior,{blockedFromState:prior,blockers:[{status:'OPEN'}]}).code==='BLOCKER_STILL_OPEN');
 check('recovery',candidate.canTransition('BLOCKED',prior,{blockedFromState:prior,blockers:[{status:'RESOLVED'}]}).ok===true);
 const wrong=prior==='INTAKE'?'STRATEGY_REQUIRED':'INTAKE';
 check('recovery',candidate.canTransition('BLOCKED',wrong,{blockedFromState:prior,blockers:[{status:'RESOLVED'}]}).code==='INVALID_BLOCKED_RESUME');
}
for(const trigger of [null,'ORCHESTRATOR','STRATEGIST','HUMAN']){
 const r=candidate.canTransition('PARKED','STRATEGY_REQUIRED',{reopenTrigger:trigger});
 check('recovery',trigger==='STRATEGIST'||trigger==='HUMAN'?r.ok===true:r.code==='PARKED_REOPEN_TRIGGER_REQUIRED');
}
for(const to of states.filter(s=>s!=='STRATEGY_REQUIRED')) check('recovery',candidate.canTransition('PARKED',to,{reopenTrigger:'STRATEGIST'}).code==='ILLEGAL_TRANSITION');

const taskOwners={RESEARCH:'MARKET_INTELLIGENCE',DESIGN_EXPERIMENT:'STRATEGIST',APPROVE_EXPERIMENT:'HUMAN',ANALYZE_CONTENT:'CONTENT_ANALYST',CREATE_CONTENT:'CONTENT_CREATOR',POST_PRODUCE_VIDEO:'VIDEO_POST_PRODUCTION',APPROVE_CREATIVE:'HUMAN',PUBLISH:'PUBLISHER',HANDLE_LEAD:'SALES_LEAD_AGENT',COLLECT_MEASUREMENT:'ORCHESTRATOR',ANALYZE_EXPERIMENT:'ANALYTICS',DECIDE_PORTFOLIO:'STRATEGIST',APPROVE_SCALE:'HUMAN'};
const forbidden=new Set(['RESEARCH','DESIGN_EXPERIMENT','ANALYZE_CONTENT','CREATE_CONTENT','POST_PRODUCE_VIDEO','HANDLE_LEAD','ANALYZE_EXPERIMENT','DECIDE_PORTFOLIO']);
const actors=['ORCHESTRATOR','MARKET_INTELLIGENCE','STRATEGIST','CONTENT_ANALYST','CONTENT_CREATOR','VIDEO_POST_PRODUCTION','PUBLISHER','SALES_LEAD_AGENT','ANALYTICS','HUMAN'];
for(const [task,owner] of Object.entries(taskOwners)){ for(const actor of actors){ const r=candidate.validateTaskAuthority(actor,task); let pass; if(actor==='ORCHESTRATOR'&&forbidden.has(task)) pass=r.ok===false&&r.code==='CONTROLLER_SPECIALIST_OVERREACH'&&r.expectedOwner===owner; else if(actor===owner) pass=r.ok===true&&r.expectedOwner===owner; else pass=r.ok===false&&r.code==='WRONG_TASK_OWNER'&&r.expectedOwner===owner; check('authority',pass); }}
for(const task of ['REPAIR_DATA','RESOLVE_CONTRACT_VIOLATION']){ check('authority',candidate.validateTaskAuthority('HUMAN',task).code==='DYNAMIC_OWNER_REQUIRED'); for(const owner of ['HUMAN','STRATEGIST','ANALYTICS']){ for(const actor of actors){ const r=candidate.validateTaskAuthority(actor,task,{dynamicOwner:owner}); check('authority',actor===owner?r.ok===true:r.ok===false&&r.code==='WRONG_TASK_OWNER'); } }}
check('authority',candidate.validateTaskAuthority('ORCHESTRATOR','UNKNOWN_TASK').code==='UNKNOWN_TASK_TYPE');

for(const [a,b] of [[1,1],[7,7],[1,2],[9,8],[0,0],[-1,-1]]){ const r=candidate.validateRevision(a,b); check('concurrency',a===b?r.ok===true:r.code==='REVISION_CONFLICT'); }
for(const [a,b] of [[3,3.2],[3,'3'],[null,3]]) check('concurrency',candidate.validateRevision(a,b).code==='INVALID_REVISION');

for(let attempt=1;attempt<=6;attempt++){ const r=candidate.retryDirective('TRANSIENT_TOOL',attempt); const rem=Math.max(0,2-(attempt-1)); check('retry',r.retriesRemaining===rem&&r.automatic===(rem>0)&&r.sameIdempotencyKey===true); }
const retryDirectives={DATA_NOT_READY:'SCHEDULE_WAKEUP',CONTRACT:'RETURN_ONCE_THEN_ESCALATE',BUSINESS_FACT:'REQUEST_AUTHORITATIVE_RESOLUTION',PERMISSION:'REQUEST_AUTHORITY',LOGIC:'BLOCK_AND_ESCALATE',SAFETY_COMPLIANCE:'BLOCK_AND_ESCALATE',UNKNOWN_EXCEPTION:'BLOCK_AND_ESCALATE'};
for(const [c,d] of Object.entries(retryDirectives)) check('retry',candidate.retryDirective(c,99).directive===d&&candidate.retryDirective(c,99).automatic===false);
check('retry',candidate.retryDirective('ALIEN_FAILURE',1).code==='UNKNOWN_ERROR_CLASS');

const sideEffects=['PUBLISH','HANDLE_LEAD','CREATE_APPOINTMENT','SEND_OUTBOUND_MESSAGE','RESERVE_VEHICLE','TAKE_DEPOSIT'];
for(const t of [...sideEffects,'DESIGN_EXPERIMENT','COLLECT_MEASUREMENT','ANALYZE_EXPERIMENT']) for(const known of [true,false,null]){ const r=candidate.requiresReconciliation(t,known); const req=sideEffects.includes(t)&&known!==true; check('side_effects',r.required===req); }

const refs=[{artifact_id:'A',version:'1',sha256_or_revision:'ha'},{artifact_id:'B',version:'2',sha256_or_revision:'hb'}];
const scope={experiment_id:'E',experiment_version:'7',artifact_refs:refs};
check('approvals',candidate.validateApproval({status:'APPROVED',approvalScope:scope,currentScope:{...scope,artifact_refs:[...refs].reverse()}}).ok===true);
check('approvals',candidate.validateApproval({status:'PENDING',approvalScope:scope,currentScope:scope}).code==='APPROVAL_NOT_APPROVED');
check('approvals',candidate.validateApproval({status:'APPROVED',expired:true,approvalScope:scope,currentScope:scope}).code==='APPROVAL_EXPIRED');
check('approvals',candidate.validateApproval({status:'APPROVED',approvalScope:scope,currentScope:{experiment_id:'X',experiment_version:'7',artifact_refs:refs}}).code==='APPROVAL_EXPERIMENT_SCOPE_MISMATCH');
check('approvals',candidate.validateApproval({status:'APPROVED',approvalScope:scope,currentScope:{experiment_id:'E',experiment_version:'7',artifact_refs:[refs[0],{artifact_id:'B',version:'2',sha256_or_revision:'changed'}]}}).code==='APPROVAL_ARTIFACT_SCOPE_MISMATCH');

const valid=[{artifact_id:'A',version:'1',sha256_or_revision:'h1',experiment_id:'E',experiment_version:'1',validation_status:'VALID'},{artifact_id:'B',version:'1',sha256_or_revision:'h2',experiment_id:'E',experiment_version:'1',validation_status:'VALID'}];
check('artifacts',candidate.validateArtifactJoin(valid).ok===true);
check('artifacts',candidate.validateArtifactJoin([]).code==='NO_ARTIFACTS');
for(const f of ['artifact_id','version','sha256_or_revision']){ const x={...valid[0],[f]:''}; check('artifacts',candidate.validateArtifactJoin([x]).code==='ARTIFACT_IDENTITY_INCOMPLETE'); }
check('artifacts',candidate.validateArtifactJoin([valid[0],{...valid[1],experiment_id:'X'}]).code==='EXPERIMENT_ID_MISMATCH');
check('artifacts',candidate.validateArtifactJoin([valid[0],{...valid[1],experiment_version:'2'}]).code==='EXPERIMENT_VERSION_MISMATCH');
check('artifacts',candidate.validateArtifactJoin([{...valid[0],validation_status:'STALE'}]).code==='INVALID_OR_STALE_ARTIFACT');

for(const state of states){ const no=candidate.routeInquiry({inquiryExists:false,currentExperimentState:state}); const yes=candidate.routeInquiry({inquiryExists:true,currentExperimentState:state}); check('sales_parallel',no.dispatch===false&&yes.dispatch===true&&yes.targetOwner==='SALES_LEAD_AGENT'&&yes.preserveExperimentState===state); }
check('exceptions',eq(candidate.unknownExceptionDirective(),{action:'BLOCK',targetOwner:'HUMAN',code:'UNKNOWN_EXCEPTION'}));

const schema=JSON.parse(fs.readFileSync(path.join(candidateDir,'data-schemas/orchestrator-workflow.schema.json'),'utf8'));
const approval=schema.$defs?.approval; const blocker=schema.properties?.blockers?.items; const retry=schema.properties?.retry_state;
check('schema',schema.required?.includes('blocked_from_state'));
check('schema',approval?.required?.includes('scope')&&approval?.properties?.scope?.required?.includes('artifact_refs'));
check('schema',blocker?.required?.includes('status'));
check('schema',retry?.properties?.idempotency_key!==undefined&&retry?.properties?.reconciliation_status!==undefined);

const head=execFileSync('git',['-C',candidateDir,'rev-parse','HEAD'],{encoding:'utf8'}).trim();
check('freeze',head===EXPECTED_COMMIT);

const familyObject=Object.fromEntries([...families.entries()]);
const report={cycle_id:'workflow-controller-independent-heldout-2026-08-22',evaluator:'cross-repo exhaustive reference implementation',candidate_commit:head,expected_candidate_commit:EXPECTED_COMMIT,case_count:[...families.values()].reduce((n,x)=>n+x.total,0),families:familyObject,failure_count:failures.length,critical_failure_count:failures.length,verdict:failures.length===0?'PASS':'REVISE'};
fs.writeFileSync(outPath,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({cycle_id:report.cycle_id,case_count:report.case_count,failure_count:report.failure_count,verdict:report.verdict,families:report.families},null,2));
process.exit(failures.length===0?0:1);
