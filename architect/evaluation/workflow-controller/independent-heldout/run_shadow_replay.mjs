import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';

const [mode, candidateDirArg, experimentDirArg, ledgerArg, checkpointArg, reportArg] = process.argv.slice(2);
if (!['start','resume','replay'].includes(mode)) throw new Error('mode must be start|resume|replay');
const candidateDir = path.resolve(candidateDirArg);
const experimentDir = path.resolve(experimentDirArg);
const ledgerPath = path.resolve(ledgerArg);
const checkpointPath = path.resolve(checkpointArg);
const reportPath = reportArg ? path.resolve(reportArg) : null;
const candidate = await import(pathToFileURL(path.join(candidateDir,'scripts/orchestrator-policy.mjs')).href);

const EXP_COMMIT='e864b2975eea12bfe2d6c0eaa636ba21e764c8c0';
const EXP='exp-20260811-elantra-gt-001';
const base=path.join(experimentDir,'experiments',EXP);
const realRefs={
 mi:path.join(base,'v1','market-intelligence-report.json'),
 strategy:path.join(base,'v3','strategy-experiment.json'),
 content:path.join(base,'v3','content-spec.json')
};
for (const p of Object.values(realRefs)) if (!fs.existsSync(p)) throw new Error(`missing real upstream artifact ${p}`);
const mi=JSON.parse(fs.readFileSync(realRefs.mi,'utf8'));
const strategy=JSON.parse(fs.readFileSync(realRefs.strategy,'utf8'));
const content=JSON.parse(fs.readFileSync(realRefs.content,'utf8'));
if(strategy.experiment_id!==EXP||strategy.status!=='APPROVED') throw new Error('real strategy invariant failed');
if(content.experiment_id!==EXP||content.status!=='READY_FOR_CREATOR') throw new Error('real content-spec invariant failed');

function readLedger(){ if(!fs.existsSync(ledgerPath)) return []; return fs.readFileSync(ledgerPath,'utf8').trim().split('\n').filter(Boolean).map(JSON.parse); }
function writeEvent(e){ fs.appendFileSync(ledgerPath,JSON.stringify(e)+'\n'); }
function checkpoint(obj){ fs.writeFileSync(checkpointPath,JSON.stringify(obj,null,2)+'\n'); }
function step(ctx,to,actor,evidenceRef,{blockedFromState=null,blockers=[],shadow=false,note=null}={}){
  const options={}; if(ctx.state==='BLOCKED'){options.blockedFromState=blockedFromState;options.blockers=blockers;}
  const legal=candidate.canTransition(ctx.state,to,options); if(!legal.ok) throw new Error(`illegal shadow transition ${ctx.state}->${to}: ${legal.code}`);
  const owner=candidate.expectedOwner(ctx.state,ctx.blockerOwner??null); if(owner!==actor) throw new Error(`owner mismatch ${ctx.state}: ${owner} != ${actor}`);
  ctx.revision+=1;
  writeEvent({kind:'transition',seq:readLedger().length+1,revision:ctx.revision,from:ctx.state,to,actor,evidence_ref:evidenceRef,shadow,external_side_effect:false,note,blocked_from_state:blockedFromState,blockers});
  ctx.state=to;
  return ctx;
}

if(mode==='start'){
  fs.writeFileSync(ledgerPath,'');
  let ctx={state:'INTAKE',revision:1,blockerOwner:null};
  writeEvent({kind:'meta',seq:1,experiment_id:EXP,experiment_commit:execFileSync('git',['-C',experimentDir,'rev-parse','HEAD'],{encoding:'utf8'}).trim(),candidate_commit:execFileSync('git',['-C',candidateDir,'rev-parse','HEAD'],{encoding:'utf8'}).trim(),simulation:true,external_side_effects_allowed:false});
  ctx=step(ctx,'STRATEGY_REQUIRED','ORCHESTRATOR','shadow://intake',{shadow:true});
  ctx=step(ctx,'STRATEGY_IN_PROGRESS','ORCHESTRATOR','shadow://dispatch/strategist',{shadow:true});
  ctx=step(ctx,'RESEARCH_REQUIRED','STRATEGIST','shadow://strategist/research-request',{shadow:true});
  ctx=step(ctx,'RESEARCH_IN_PROGRESS','ORCHESTRATOR','shadow://dispatch/market-intelligence',{shadow:true});
  ctx=step(ctx,'STRATEGY_REQUIRED','MARKET_INTELLIGENCE',`real://${EXP_COMMIT}/${path.relative(experimentDir,realRefs.mi)}`,{note:'historical real MI artifact'});
  ctx=step(ctx,'STRATEGY_IN_PROGRESS','ORCHESTRATOR','shadow://dispatch/strategist-after-research',{shadow:true});
  ctx=step(ctx,'EXPERIMENT_APPROVAL_REQUIRED','STRATEGIST',`real://${EXP_COMMIT}/${path.relative(experimentDir,realRefs.strategy)}`,{note:'historical real approved zero-spend strategy'});
  ctx=step(ctx,'CONTENT_ANALYSIS_REQUIRED','HUMAN',`real://${EXP_COMMIT}/${path.relative(experimentDir,realRefs.strategy)}`,{note:'historical preparation approval only'});
  ctx=step(ctx,'CONTENT_ANALYSIS_IN_PROGRESS','ORCHESTRATOR','shadow://dispatch/content-analyst',{shadow:true});
  ctx=step(ctx,'CREATIVE_REQUIRED','CONTENT_ANALYST',`real://${EXP_COMMIT}/${path.relative(experimentDir,realRefs.content)}`,{note:'historical real content spec'});
  ctx=step(ctx,'CREATIVE_IN_PROGRESS','ORCHESTRATOR','shadow://dispatch/content-creator',{shadow:true});
  ctx=step(ctx,'POST_PRODUCTION_REQUIRED','CONTENT_CREATOR','shadow://artifact/creator-deliverable',{shadow:true});
  ctx=step(ctx,'POST_PRODUCTION_IN_PROGRESS','ORCHESTRATOR','shadow://dispatch/video-post-production',{shadow:true});
  ctx=step(ctx,'CREATIVE_APPROVAL_REQUIRED','VIDEO_POST_PRODUCTION','shadow://artifact/post-production-deliverable',{shadow:true});
  ctx=step(ctx,'READY_TO_PUBLISH','HUMAN','shadow://approval/creative-only',{shadow:true,note:'qualification-only approval; no business authority'});
  ctx=step(ctx,'BLOCKED','ORCHESTRATOR','shadow://blocker/no-live-publish-authority',{shadow:true,note:'prove fail-closed before external side effect'});
  ctx.blockerOwner='HUMAN';
  checkpoint({...ctx,blockedFromState:'READY_TO_PUBLISH',blockers:[{code:'SHADOW_NO_LIVE_PUBLISH_AUTHORITY',owner:'HUMAN',status:'OPEN'}],restart_required:true});
  console.log(JSON.stringify({stage:'start',state:ctx.state,revision:ctx.revision,ledger_events:readLedger().length}));
}

if(mode==='resume'){
  let ctx=JSON.parse(fs.readFileSync(checkpointPath,'utf8'));
  const blockedTest=candidate.canTransition('BLOCKED',ctx.blockedFromState,{blockedFromState:ctx.blockedFromState,blockers:ctx.blockers});
  if(blockedTest.code!=='BLOCKER_STILL_OPEN') throw new Error('open blocker did not fail closed');
  ctx.blockers=ctx.blockers.map(b=>({...b,status:'RESOLVED'}));
  ctx=step(ctx,'READY_TO_PUBLISH','HUMAN','shadow://resolution/simulation-authorized',{blockedFromState:ctx.blockedFromState,blockers:ctx.blockers,shadow:true,note:'authorizes simulation only, never live publish'});
  ctx.blockerOwner=null;
  ctx=step(ctx,'PUBLISHING','ORCHESTRATOR','shadow://dispatch/publisher-simulator',{shadow:true});
  ctx=step(ctx,'PUBLISHED','PUBLISHER','shadow://publish-record/NO_EXTERNAL_PLATFORM',{shadow:true,note:'no network or platform action'});
  const route=candidate.routeInquiry({inquiryExists:true,currentExperimentState:ctx.state});
  if(!(route.dispatch&&route.targetOwner==='SALES_LEAD_AGENT'&&route.preserveExperimentState===ctx.state)) throw new Error('parallel Sales routing probe failed');
  writeEvent({kind:'probe',seq:readLedger().length+1,probe:'parallel_sales_route',shadow:true,synthetic_inquiry:true,result:{dispatch:route.dispatch,targetOwner:route.targetOwner,preserveExperimentState:route.preserveExperimentState},external_side_effect:false});
  ctx=step(ctx,'MEASUREMENT_WAIT','ORCHESTRATOR','shadow://measurement-window',{shadow:true});
  ctx=step(ctx,'ANALYTICS_REQUIRED','ORCHESTRATOR','shadow://checkpoint/reached',{shadow:true});
  ctx=step(ctx,'ANALYTICS_IN_PROGRESS','ORCHESTRATOR','shadow://dispatch/analytics',{shadow:true});
  ctx=step(ctx,'STRATEGIST_DECISION_REQUIRED','ANALYTICS','shadow://analytics-decision/INCONCLUSIVE',{shadow:true,note:'no fabricated performance data'});
  ctx=step(ctx,'PARKED','STRATEGIST','shadow://strategist-decision/PARKED',{shadow:true,note:'no real measurement; cannot SCALE or KILL'});
  checkpoint({...ctx,completed:true,restart_observed:true});
  console.log(JSON.stringify({stage:'resume',state:ctx.state,revision:ctx.revision,ledger_events:readLedger().length}));
}

if(mode==='replay'){
  const events=readLedger();
  const transitions=events.filter(e=>e.kind==='transition');
  if(events.length<2||transitions.length<20) throw new Error('shadow ledger too short');
  const meta=events.find(e=>e.kind==='meta');
  if(!meta||meta.experiment_commit!==EXP_COMMIT||meta.simulation!==true||meta.external_side_effects_allowed!==false) throw new Error('meta/freeze invariant failed');
  let state='INTAKE', rev=1, sawBlock=false, sawResume=false, realCount=0, shadowCount=0;
  for(const e of transitions){
    if(e.from!==state||e.revision!==rev+1) throw new Error(`replay ordering failed at ${e.seq}`);
    const opts={}; if(e.from==='BLOCKED'){opts.blockedFromState=e.blocked_from_state;opts.blockers=e.blockers;}
    const legal=candidate.canTransition(e.from,e.to,opts); if(!legal.ok) throw new Error(`replay illegal ${e.from}->${e.to}`);
    const blockerOwner=e.from==='BLOCKED'?'HUMAN':null;
    if(candidate.expectedOwner(e.from,blockerOwner)!==e.actor) throw new Error(`replay owner mismatch ${e.from}`);
    if(e.external_side_effect!==false) throw new Error('shadow run attempted external side effect');
    if(String(e.evidence_ref).startsWith('real://')) realCount++; else if(String(e.evidence_ref).startsWith('shadow://')) shadowCount++;
    if(e.to==='BLOCKED') sawBlock=true; if(e.from==='BLOCKED'&&e.to==='READY_TO_PUBLISH') sawResume=true;
    state=e.to; rev=e.revision;
  }
  const salesProbe=events.find(e=>e.kind==='probe'&&e.probe==='parallel_sales_route');
  const current=JSON.parse(fs.readFileSync(checkpointPath,'utf8'));
  const pass=state==='PARKED'&&current.completed===true&&current.restart_observed===true&&sawBlock&&sawResume&&realCount>=3&&shadowCount>=15&&salesProbe?.synthetic_inquiry===true&&events.every(e=>e.external_side_effect!==true);
  const report={cycle_id:'workflow-controller-durable-shadow-2026-08-22',experiment_id:EXP,experiment_commit:EXP_COMMIT,candidate_commit:meta.candidate_commit,transition_count:transitions.length,real_upstream_artifact_transitions:realCount,shadow_transitions:shadowCount,restart_resume_verified:sawResume,blocked_fail_closed_verified:sawBlock,parallel_sales_probe_verified:Boolean(salesProbe),external_side_effect_count:events.filter(e=>e.external_side_effect===true).length,fabricated_business_outcomes:false,final_state:state,verdict:pass?'PASS':'REVISE'};
  fs.writeFileSync(reportPath,JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report,null,2));
  process.exit(pass?0:1);
}
