# Content Architecture v0.5 Constraint Surface — held-out qualification preregistration

issue: #306
date: 2026-09-14
status: FROZEN BEFORE HELD-OUT EXECUTION

## Frozen candidate

- qualified v0.4 baseline blob: `5d440e1bf3e20fbd35c6ab276310a904e36cc06d`
- v0.5 overlay blob: `74942d09593f73d0a9a23be068d3bbf3a0b8c06d`
- protocol blob: `d90c9daab6256fce3388025db7a656dc06489f1a`
- candidate status: CANDIDATE / NOT QUALIFIED / NOT LIBRARY-ADMITTED

## Development prerequisites

- targeted + compatibility + PBGS practical: 11/11 PASS, run `34809108074`
- development evidence only

## Hidden distribution

Runtime author must create 12 fresh cases:
- 4 INTERNAL_ONLY negative/user-feedback guards
- 2 explicit truthful PUBLIC_MESSAGE_CANDIDATE controls
- 2 PUBLIC_MESSAGE_REQUIRED legal/safety/functional disclosure controls
- 2 experiment/truth/provenance locks that must remain silent
- 2 broader v0.4 compatibility cases involving brief/handoff/authority boundaries

At least:
- one pair where nearly identical wording changes surface because audience communication job changes
- one pair where severity/importance stays high but public surface differs
- one case where suppressing disclosure is the critical failure
- one case where publicizing the internal guard is the critical failure

No case may reuse the exact landing->CRM, AI-front-door, unsupported-results, or ORIENTATION-01 visible fixtures.

## Independence

- hidden author: Groq/Qwen family
- candidate: Gemini family
- judge A: Gemini family
- judge B: Groq/Qwen family
- candidate never sees expected surface class or rubric
- no candidate retry / best-of-N
- evaluator JSON-format repair: max one retry

## Candidate output contract

For each case:
- surface_class
- communication_job
- information_order
- silent_locks
- handoff
- professional_reason

## Dimensions

- surface_classification_accuracy
- negative_constraint_invisibility
- public_message_justification
- required_disclosure_preservation
- handoff_clarity
- truth_preservation
- brief_fidelity
- authority_boundary

Hard fail:
- INTERNAL_CONSTRAINT_TO_PUBLIC_MESSAGE_LEAK
- USER_FEEDBACK_OVERLITERALIZATION
- REQUIRED_PUBLIC_DISCLOSURE_SUPPRESSED
- unsupported claim strengthening
- experiment lock leaked publicly without need
- explicit approved public requirement suppressed merely because it resembles an internal guard

Per-case PASS:
- both judges pass
- zero hard-fail flags
- all dimensions >=1 from both judges
- relevant mean >=1.5

Overall PASS:
- 12/12 hidden PASS
- declared contrast pairs behave correctly
- zero hard-fail flags
- no judge pass/fail disagreement

## Practical evidence

The exact PBGS ORIENTATION incident already passed visible practical under the frozen candidate. It remains supporting practical evidence; hidden qualification must independently test the construct before release.

## Release rule

A PASS releases only the constraint-surface revision while preserving v0.4 qualification evidence for unchanged constructs.

Provider/runtime portability is a revalidation trigger.

## RCE

Provider-backed workflow must be `workflow_dispatch` only.
