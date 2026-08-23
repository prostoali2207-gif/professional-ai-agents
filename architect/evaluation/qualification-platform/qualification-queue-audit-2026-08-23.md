# Qualification Queue Scope Audit — 2026-08-23

## Purpose

Apply the current Agent Architect Resource & Cost Engineering and qualification scope policy to the active professional-core qualification queue before authorizing more paid scored runs.

This audit does **not** replace evaluator-owned professional judgment, hidden-fixture design, or preregistered release requirements. It records only classifications that are already supported by explicit candidate/evaluator records in the repository.

Scope outcomes:

- `REUSE` — compatible evidence already answers the current professional question;
- `TARGET` — only evaluator-declared affected regression families are justified during repair/development;
- `FULL` — a release requirement, shared/unknown impact, or new candidate requires broad qualification;
- `BLOCK` — the repository does not yet contain enough compatible impact/evidence information to justify paid execution.

## Queue

| Candidate | Current evidence / explicit evaluator requirement | Scope decision now | Paid action now | Next gate |
|---|---|---|---|---|
| **Content Architecture v0.2** | v0.1 release verdict was REVISE: 44 runs, 0 execution errors, failed F2/F5/F6/F7/F12. v0.2 freeze record explicitly limits the repair delta to those failed/coupled families and requires targeted regression + P0 preservation before a new universal release suite. | `TARGET` | **Do not run full release suite yet.** Run only F2/F5/F6/F7/F12 with registered repeats plus the explicit P0 preservation regression. | If targeted + P0 pass, escalate to `FULL` for a fresh sealed universal release qualification on exact v0.2 blob. |
| **Sales / Lead Conversion 0.3.0** | Issue #71 explicitly preregisters a **fresh independent held-out qualification** and requires full Sales construct coverage, not only repaired families. Prior 0.1/0.2 sealed packs cannot be reused as release evidence. | `FULL` | Full scored run remains required for release, but only after current static/sealed/no-API gates and the paid pre-run budget gate pass. No repeat execution-only trigger is justified merely because an earlier attempt failed infrastructurally. | Fresh full sealed qualification -> sanitized report -> release verdict. |
| **Growth Strategy & Experiment Portfolio / Strategist v0.1** | PR #80 is explicitly a fresh sealed independent qualification transport for a frozen candidate. Candidate behavior, thresholds, hard-fails and retry policy are frozen. | `FULL` | No targeted shortcut can produce release PASS. Keep paid execution manual and gated. | Static/no-API + sealed preflight -> exact runtime canary only if unresolved -> full scored release run. |
| **Social Content Creative 0.1.0** | PR #88 is a newly frozen candidate on current main and explicitly states lifecycle remains `candidate`; current qualification must follow the full generic qualification lifecycle. No compatible release PASS exists for this exact frozen candidate. | `FULL` | No paid run until static/sealed infrastructure is ready and budget gate is recorded. | Fresh held-out release qualification on exact frozen commit/digest. |
| **Analytics v0.3** | PR #47 records targeted provider-backed regression PASS and fresh post-freeze adversarial PASS for the repaired behavior. It also explicitly states prior Analytics release discipline requires fresh ChatGPT + Gemini + Claude qualification and that v0.3 remains candidate/not library-admitted until that cross-model requirement is satisfied. | `FULL` for formal release claim | **DEFER paid expansion until an eligible cross-model route exists.** Repeating the already-passed OpenAI targeted/adversarial evidence would add little decision value. | Satisfy the preregistered cross-model release requirement or formally revise that release protocol through an evaluator-owned process before execution. |
| **Social Community, Listening & Reputation Management** | PR #21 freezes the core and qualification bundle and explicitly requires a fresh post-freeze CG-06 held-out fixture plus executable **full and degraded** profiles with observable state/tool/approval traces and zero-P0/zero-P1 release rule. | `FULL` | Do not substitute prose/static checks or a narrow semantic smoke for the required behavioral qualification. | Fresh evaluator-authored sealed held-out -> full/degraded executable behavioral run -> qualification record. |

## Execution priority under RCE

Priority is based on **decision value per paid run**, not role importance.

1. **Content Architecture v0.2 — TARGET first.** It has an evaluator-declared local repair surface, so the smallest discriminating paid experiment is known. A full run before targeted/P0 PASS would violate the candidate's own freeze record and RCE policy.
2. **Resolve infrastructure/readiness for FULL candidates without scored calls.** Run static/no-API and sealed preflights for Sales, Strategist, Social Content Creative, and Social Community where available. Do not consume model quota to discover configuration defects.
3. **Analytics v0.3 — preserve existing PASS evidence; do not repurchase OpenAI evidence.** The unresolved release gap is cross-model eligibility, not the already-tested repaired behavior.
4. **Authorize FULL scored runs one at a time only after pre-run budget gate.** Prefer the candidate whose deterministic/sealed gates are green and whose result will change an immediate release/admission decision.

## Explicit non-decisions

- This audit does not infer affected families from filenames or branch names.
- It does not declare any candidate qualified.
- It does not weaken any preregistered full release gate.
- It does not claim that a cheaper model/provider is eligible without profession/evaluator compatibility evidence.
- It does not authorize retries after infrastructure, quota, or credential failure without a new reason to expect success.

## Immediate next action

Start with **Content Architecture v0.2 targeted regression**, because its evaluator-owned freeze record already specifies the exact limited families and P0 preservation checks. Before any provider call, run its deterministic/static preflight and record a compact pre-run budget gate. If the targeted/P0 gate fails, stop and repair; do not buy the universal release suite. If it passes, then and only then prepare a fresh full universal release qualification.
