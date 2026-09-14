# PBGS Cross-Core Judgment Heldout v0.1 — Execution Incident R1

date: 2026-09-14
run_id: GitHub Actions 34800847882
status: TECHNICAL_FAILURE / BOUNDED_REPAIR_AUTHORIZED
execution_chain: pbgs-cross-core-judgment-heldout-v0.1

## Observed failure

The first independent held-out execution reached the evaluator step, but the first Copilot SDK session failed before any hidden fixture was authored.

Failure:
`GitHub App Server-To-Server Tokens are not supported for this endpoint` during Copilot model resolution.

Therefore:
- hidden fixture authoring: NOT STARTED;
- candidate calls: 0;
- judge calls: 0;
- professional evidence: NONE;
- verdict: NOT_EXECUTABLE for R1.

## Classification

`AUTH_CONFIG / TRANSPORT_INELIGIBLE`.

The workflow used `${{ github.token }}` as a GitHub App server-to-server token. The Copilot model endpoint requires a different credential class.

Repository search found no configured user-scoped `COPILOT_GITHUB_TOKEN`/PAT secret.

## Stop-loss decision

Per `architect/methodology/qualification-stop-loss.md`:
- first technical failure in this execution chain: YES;
- bounded repair budget available: YES;
- allowed repair count after this record: ONE;
- eligible retry count after repair: ONE;
- any second technical defect in the same chain: STOP / NOT_EXECUTABLE.

## Bounded repair

Change evaluator-local transport only:
`Copilot SDK -> existing Gemini Interactions API path`.

Grounds:
- `GEMINI_API_KEY` is already an established provider secret used by multiple qualification workflows in this repository;
- Gemini Interactions transport is already implemented and used for professional evaluation;
- Groq is rejected for this assembled context because repository evidence records an 8k TPM limitation on a smaller ~10k-token assembly;
- OpenAI transport is unnecessary for this repair.

Preserved unchanged:
- frozen PBGS candidate SHA;
- exact professional resource blobs;
- hidden-case distribution;
- case count = 8;
- counterfactual-pair requirement;
- candidate output contract;
- two independent judge sessions;
- critical flags;
- thresholds;
- no candidate retry;
- evaluator parse retry limit;
- hidden fixture separation.

## Transport models for R2

- candidate: `gemini-3.5-flash-lite`;
- evaluator author: `gemini-3.5-flash`;
- judge A/B: `gemini-3.5-flash`.

Model choice is part of R2 execution provenance and does not imply that a PASS transfers automatically to ChatGPT deployment behavior.

## Retry rule

R2 is the single eligible retry.
If R2 encounters another technical execution defect, stop this chain and record `NOT_EXECUTABLE`; do not open a serial R3 repair.