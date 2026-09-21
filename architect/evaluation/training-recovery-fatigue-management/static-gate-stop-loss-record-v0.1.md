# Training Recovery & Fatigue Management — static gate stop-loss record v0.1

Date: 2026-09-21
Execution chain: candidate 0.1.0 / deterministic static preflight / local Python path
Generic qualification platform: issue #129 maintenance mode; NOT reopened.

## Frozen inputs for first execution

- candidate/SKILL.md blob: `503b05504a366ac5fa92c0d9ef9b095898e1a66b`
- candidate/state.schema.json blob: `06c5a2d44590b320944d7e21d7aae165d71d659c`
- development-cases-v0.1.json blob: `e99bb437d104dee57c56070c9251338a07792309`
- run_static_gate.py blob: `c709ebbdd4c1ddccc347c1dd780a9c5da2218b7f`

## First execution

Result: FAIL before PASS output.

Primary failure:
`AssertionError: wearable`

The static evaluator searched only literal hard-fail text for the token `wearable`.
Case D04 is the wearable adversarial case, but its hard-fail phrase is the semantically equivalent `device score governs training`.

This is not a professional candidate failure. The candidate itself explicitly contains a wearable policy and prohibits sole reliance on proprietary recovery/readiness scores.

Classification: `EVALUATOR_CONSTRUCT_FAIL`.

A host-side spreadsheet-runtime warmup warning also appeared on stderr, but execution continued through the TRFM evaluator to the deterministic assertion above. It did not prevent evidence generation and is not the primary failure class.

## Repair authorization

One bounded profession-specific evaluator repair is authorized:
- do not change candidate behavior;
- do not change development case meaning;
- do not weaken any hard fail or threshold;
- accept either `wearable` or `device score` for this semantic risk family.

No generic qualification-platform code may be changed.

After repair:
- rerun the exact deterministic gate once;
- if another non-professional technical/evaluator defect blocks this same chain, STOP under the chain rule and record NOT_EXECUTABLE for this preflight chain.
