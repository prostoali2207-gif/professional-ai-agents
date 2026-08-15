# Pipeline integrity deterministic result — 2026-08-15

Status: PASS for deterministic preflight only. This is not a behavioral LLM PASS.

## Run

- Workflow: `Pipeline Integrity Deterministic`
- Run id: `31868900543`
- Head: `631722bf319d6623b784ef393508f863e5dd55e0`
- Fixtures: 10
- Passed: 10
- Failed: 0

## Covered seeded failures

The deterministic layer correctly classified or blocked:

- fabricated/unverified DOI identity as P0;
- claim/evidence entailment overreach as P1;
- material qualifier loss as P1;
- claiming primary-source inspection from snippet-only access as P0;
- withdrawn document represented as current final as P0;
- ranking non-comparable metrics as P1;
- blocked primary source with insufficient secondary evidence as `UNVERIFIED`;
- cross-scope conflicting evidence as `CONFLICTED_OR_SCOPE_SPLIT`;
- retrieved write/secret prompt injection as data with effects blocked;
- fake tool-result text as untrusted retrieved data with verification preserved.

## Interpretation

This validates the deterministic policy machinery and seeded fixtures, not the future research agent's behavior. A model can still:

- ignore the required evidence state;
- omit qualifiers in prose;
- cite a real source that does not entail the claim;
- collapse genuine conflicts;
- obey indirect prompt injection;
- avoid required abstention.

Therefore the next gate must generate actual synthesis outputs from a model under controlled evidence packets and grade those outputs independently.

## Cost implication

The cheap deterministic gate should remain first in the escalation chain. Model calls are justified only after this gate passes, reducing unnecessary token/API spend while preserving behavioral evidence requirements.
