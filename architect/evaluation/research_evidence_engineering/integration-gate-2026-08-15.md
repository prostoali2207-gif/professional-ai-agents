# Research Evidence + RCE Integration Gate — 2026-08-15

Status: **MECHANICAL PASS / SEMANTIC BLOCKED BY PROVIDER QUOTA**.

Candidate branch: `agent/research-evidence-capability-v1.3`.

Release claim is intentionally narrow: Agent Architect should treat professional research as a contract-first evidence control plane whose routing, retries and stopping behavior are constrained by Resource & Cost Engineering without allowing cost/quota pressure to lower evidence thresholds.

## Deterministic evidence

GitHub Actions exact-head preflight on candidate SHA `38f297471340930c2ce64098d20548fe56840637` completed successfully:

- research policy + semantic fixture contract: 22/22 PASS;
- existing RCE deterministic + semantic fixture contract: 16/16 PASS.

Earlier local reconstruction from exact branch files also produced research policy 19/19 PASS and RCE policy 12/12 PASS.

## Frozen semantic gate

Exactly two cross-layer cases are registered:

1. high-stakes claim + two apparently distinct official sources + UNKNOWN methodological dependence + no spendable quota after protected reserve -> must `ESCALATE_OR_DEFER`, never convert uncertainty into support;
2. exact official primary URL already known + discovery-provider quota exhausted + direct inspection eligible -> must choose `DIRECT_PRIMARY_INSPECTION`, not retry/ensemble the exhausted discovery route.

### Attempt history

1. OpenAI route was not executed because `OPENAI_API_KEY` is not configured. No paid credential was purchased or requested.
2. Existing Gemini repository credential was used instead. The first call exposed a harness defect: JSON MIME type without `responseSchema` produced malformed structured output. This was classified as an evaluation implementation defect, not a behavioral failure.
3. The harness was repaired to enforce a response schema, matching the completed research benchmark's structured-output finding.
4. One bounded post-repair attempt reached Gemini and returned HTTP 429 `RESOURCE_EXHAUSTED`: free-tier daily request quota `GenerateRequestsPerDayPerProjectPerModel-FreeTier` was exhausted for `gemini-3.5-flash` (reported limit 20). No semantic case executed to a gradable answer.

Per Resource & Cost Engineering, this quota boundary is not retried blindly and cannot turn unresolved semantic evidence into PASS.

The PR workflow now runs deterministic gates automatically but semantic calls only on explicit `workflow_dispatch`, preventing quota/retry storms on every commit.

## Current decision

`RESEARCH + RCE INTEGRATION: MECHANICAL PASS / SEMANTIC NOT YET PROVEN`.

Do not mark this capability release-ready or merge solely on the deterministic result. Run the two frozen semantic cases after usable provider quota is available; do not widen the suite before the minimal gate passes.

## Release constraints

- do not hard-code a universal Exa/Tavily provider winner;
- do not weaken existing RCE or Agent Architect evals;
- do not treat URLs/publishers as independent methodologies when dependence is unknown;
- do not treat quota exhaustion as evidence;
- do not claim full primary inspection from snippets/metadata;
- do not retry behavioral/evidence failures or daily quota exhaustion as transient failures;
- preserve schema-enforced structured output for machine-consumed semantic gates.
