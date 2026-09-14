# Social Content Creative — Expert Validation Pilot v0.1

Status: preregistration draft. No T2 claim has been earned.

## Why this pilot

Pilot the new Professional Trust Validation layer on `social-content-creative` 0.1.0 because:

- it is already internally qualified (T1 candidate baseline);
- the profession is materially judgment-heavy and creative, so AI-only grading has a meaningful construct-validity risk;
- its outputs can be evaluated through authentic short-form social work rather than trivia;
- the role is used in real downstream production, making a later T3 field-evidence loop feasible;
- professional corrections can be observed at decision/substance level rather than only surface style.

This pilot does not imply that Social Content Creative is weaker than every other qualified core. It is selected because it is a high-information validation target.

## Frozen target

Core:
- ID: `social-content-creative`
- version: `0.1.0`
- catalog lifecycle: `qualified`
- current trust evidence ceiling before this pilot: **T1 QUALIFIED**
- artifact digest: `sha256:ce5f537d336e6a6396f47c1ae492a687c4dc4b30ade8ab37bb4abb94d6251c0f`

If behavior-relevant files/runtime change before expert scoring, freeze a new exact target and do not transfer the pilot result mechanically.

## Primary question

Does the exact agent/core produce decisions and work that independent strong Social Content / Creative practitioners would accept as professionally strong for the stated role, without recurring substantive correction?

The pilot is not designed to prove universal superiority or safe blind autonomy.

## Validator profile

Recruit independent practitioners with current hands-on responsibility for short-form/social creative work.

Eligibility evidence should demonstrate a meaningful combination of:

- recent professional work in social creative/content;
- responsibility for concept/script/creative decisions rather than only posting/admin;
- evidence of shipped work and/or accountable commercial/communication outcomes;
- ability to explain decision rationale and distinguish preference from professional defect;
- relevant market/context familiarity for any context-sensitive task.

Do not qualify validators solely by title, followers, employer prestige or self-description.

For this judgment-heavy pilot, use multiple independent practitioners unless a later evidence review justifies otherwise.

Validators must not have authored this core, its hidden cases or the desired verdict.

## Blind packet

Prepare a validator packet that hides:

- desired verdict;
- candidate development history;
- internal PASS/FAIL history;
- hidden expected-answer wording;
- which comparison output is AI versus professional/baseline where comparison is used.

The packet may disclose the actual professional role and task context because validators need enough context to judge real work.

## Task families

Use authentic work samples representing the current core claim boundary.

At minimum sample across:

1. brief fidelity and prioritization;
2. truthful persuasion / unsupported claim pressure;
3. hook + payoff quality;
4. message sequencing;
5. creative divergence without pseudo-variation;
6. visual storytelling and shootability;
7. platform/context adaptation;
8. experiment-lock preservation;
9. critique/revision after a weak first concept;
10. bad user premise where agreeing would reduce professional quality.

Include both ordinary and difficult cases. At least one task should expose whether the agent is excessively safe/conventional when a strong professional should make a bolder but defensible creative decision.

Do not reuse public/development wording as hidden validation material.

## Comparison design

Where feasible, compare candidate work blindly against one or more strong practitioner reference responses or professionally accepted real-work baselines.

Comparison should focus on decision quality, not verbosity.

For creative work, allow multiple valid solutions. A reference is not a single canonical answer.

## Scoring dimensions

Validators assess, per task:

- brief appropriateness;
- professional decision quality;
- truth/claim discipline;
- strength of concept;
- distinctiveness versus generic/predictable work;
- communication clarity;
- production feasibility/shootability when relevant;
- platform/context fit;
- whether caution is proportionate or suppresses a better defensible solution;
- whether the work requires substantive professional correction before use.

For each material criticism, classify:

- preference/style difference;
- P3 polish;
- P2 meaningful quality weakness;
- P1 core professional failure;
- P0 integrity/safety/authority failure.

## Critical prompts to validators

Ask:

- Would you personally make or approve a materially similar decision?
- What did the candidate notice that a junior practitioner often misses?
- What did it miss that a strong practitioner should catch?
- Is it playing safe where a strong creative should take a justified risk?
- Is it shallow, generic or overly correct despite satisfying the brief?
- Would you trust this output to proceed to production without your substantive correction?
- If not, exactly what decision must change?

## AI-grader calibration

Use a subset of expert-judged cases as calibration material only after the professional judgments are frozen.

Then test the intended model grader on separate held-out expert-judged cases.

Inspect:

- false accept of professionally weak work;
- false reject of legitimate creative alternatives;
- bias toward verbosity/polish;
- failure to detect excessive caution/genericity;
- disagreement on P1/P0 classification.

Do not promote T2 if release-critical grader disagreement remains systematic.

## T2 decision rule

Freeze a quantitative/qualitative decision rule before candidate outputs are unblinded to validators.

The rule must include:

- zero tolerated P0;
- no repeated unresolved P1 failure family;
- no systematic expert finding that work needs substantive correction before normal use;
- acceptable inter-rater disagreement analysis;
- calibrated grader performance adequate for the criteria delegated to AI;
- explicit limitations and claim boundary.

Do not invent a convenient aggregate percentage in advance of the validator/task sampling design.

## Failure routing

If the pilot fails:

`expert finding -> reproduce/triangulate -> classify -> identify responsible profession/eval/knowledge/judgment/workflow layer -> repair -> targeted regression -> fresh affected expert validation`.

Do not patch the core merely to imitate one validator's style.

If strong practitioners legitimately disagree, preserve the decision boundary instead of forcing one taste preference into the core.

## T3 follow-on

Only after T2 passes, preregister a field phase using actual production tasks.

Capture:

- task context;
- exact agent/core/runtime;
- output;
- whether a human accepted, edited or rejected it;
- substantive correction and severity;
- reason for correction;
- downstream outcome where interpretable;
- incidents/near-misses;
- expert spot review on sampled work;
- distribution/drift changes.

Use:

- `architect/methodology/professional-trust-validation.md`;
- `architect/evaluation/field-evidence-feedback-gate.md`;
- `architect/methodology/production-incident-learning.md`.

No T3 claim exists until that field gate is executed and passed.

## Red-team before execution

Senior practitioner:
- could the packet reward polished mediocrity or punish unconventional strong work?

Educator/assessor:
- do tasks actually elicit the competencies rather than recognizable test patterns?

Hiring manager:
- is the evidence strong enough to hand this agent normal creative responsibility without requiring a non-expert owner to detect profession-specific mistakes?

Evaluation scientist:
- are validator selection, blinding, task sampling, disagreement handling and grader calibration defensible?

Material issues must be repaired before the first scored expert validation.
