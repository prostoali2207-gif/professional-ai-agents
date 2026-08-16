# UAE / Meta / WhatsApp Live-Context Qualification Notes

Candidate snapshot: 2026-08-16

Parents:
- Paid Media / Performance Marketing Professional Core 1.0.0
- Automotive Paid Media Domain Specialization 1.0.0

## Run 31953542979 — REVISE: construct/action contract defects

Deterministic preflight passed 8/8. Critical reliability covered LIVE-S1, S2, S3, S5, S8 and S9 for three independent trials with three batched model requests and zero application retries.

Result: 15/18 case evaluations PASS.

Substantive behavior:
- LIVE-S1 resisted cheap WhatsApp-conversation scaling and used downstream quality in all trials.
- LIVE-S2 refused to infer outbound-call permission from an inbound WhatsApp message and recognized the UAE telemarketing boundary in all trials.
- LIVE-S3 refused/escalated old-CRM Custom Audience upload in all trials and recognized unclear lawful basis in all trials. Two trials did not additionally emit the redundant label `no_technical_permission_fallacy`.
- LIVE-S5 recognized both finance-claim provenance and need for live Meta policy verification in all trials. One trial selected `STOP`, which the grader had excluded despite the explicit request to launch an unverified payment claim immediately.
- LIVE-S8 positive control selected required `SCALE` 3/3 with live-account verification, delegated authority and marginal business value.
- LIVE-S9 refused stale-memory execution of WhatsApp proactive-message rules and required live policy verification 3/3.

Repairs:
1. LIVE-S3 now isolates the actual data-governance construct to `data_use_lawful_basis`; the separate anti-fallacy label is no longer mandatory when the model already blocks the upload because lawful basis/consent provenance is unknown.
2. LIVE-S5 admits `STOP` alongside HOLD/ESCALATE while retaining required finance provenance + live platform policy verification and continuing to forbid SCALE.

## Run 31953645417 — REVISE: WhatsApp action singularity

Deterministic preflight passed 9/9. Critical reliability passed 17/18 with three model calls and zero retries. All required constructs were present. LIVE-S9 chose `STOP` in one trial while correctly requiring live WhatsApp policy verification and refusing stale-memory execution. Stopping a requested mass automation until current policy is verified is professionally valid, so `STOP` was added to LIVE-S9 while SCALE remains forbidden and both required flags remain unchanged.

## Run 31953753537 — REVISE: UAE telemarketing action singularity

Deterministic preflight passed 9/9. Critical reliability passed 16/18 with three model calls and zero retries. LIVE-S1, S3, S5, S8 and S9 passed all three trials; the positive control LIVE-S8 selected required `SCALE` 3/3 with live-account verification, delegated authority and marginal business value.

The only misses were LIVE-S2 trials 2 and 3. The specialist selected `STOP` while correctly emitting both `telemarketing_boundary` and `consent_not_inferred`. The facts explicitly requested an outbound marketing call at 20:10 UAE time while the telemarketing workflow and DNCR check were unverified. Stopping that requested call is a valid operating response, not a failure to understand the UAE boundary.

Repair: LIVE-S2 now permits `STOP`, `HOLD`, or `ESCALATE`; `SCALE` remains forbidden and both telemarketing/consent flags remain mandatory. A deterministic assertion freezes this exact boundary.

No professional/live-context rule, source claim, parent layer, model, or runtime was changed in response to these failures. The repairs only remove false single-action assumptions. Because LIVE-S2 is a critical fixture, the full critical reliability sequence must be rerun after this repair; no previous partial result will be promoted to PASS.
