# Evaluation Integrity and Regression Engineering

Status: v0.1.

## Threat model

An evaluation can improve while real capability does not. Agent Architect must defend against evaluation overfitting, leakage, contamination, grader drift, and regression blindness.

## Separate evaluation sets

Maintain conceptually distinct sets:

- **development evals**: visible, fast feedback during construction;
- **regression evals**: stable tests for previously discovered failures;
- **holdout/adversarial evals**: not used to tune individual fixes;
- **live/practical evals**: representative end-to-end work in the real or controlled target environment.

Do not repeatedly tune against the same small test set and then cite that set as independent evidence of competence.

## Failure-to-regression rule

When a production/practical failure reveals a generalizable defect:

1. capture the minimal reproducible case;
2. identify root cause layer;
3. create a regression test for the capability, not merely the exact wording;
4. repair the correct layer;
5. test nearby variants;
6. rerun holdout/practical evaluation where material.

## Leakage controls

Track whether eval cases or close paraphrases have entered:

- prompts/instructions;
- knowledge files;
- worked examples;
- few-shot demonstrations;
- development discussions;
- generated synthetic training/eval material.

If so, downgrade the independence of that evaluation.

## Benchmark contamination

External benchmark scores are evidence only with caveats. Training-data opacity and benchmark exposure can inflate apparent capability. Prefer fresh, domain-specific, procedurally generated, or expert-authored tasks when independent evaluation matters.

## Grader drift

Version graders and rubrics. Recalibrate against expert judgments after meaningful rubric/model changes. Keep disagreements as diagnostic data rather than forcing artificial consensus.

## Stochasticity

For stochastic systems, a single successful run is weak evidence. Repeat representative tasks where variance is material and report distributions/failure rates rather than only best-case examples.

## Anti-gaming tests

Include cases designed to expose:

- rubric keyword matching;
- verbose but unsupported answers;
- correct final answer reached through invalid evidence;
- memorized benchmark phrasing;
- refusal to admit uncertainty;
- superficial checklist compliance.

## Gate

No agent may be declared competent solely because it passes tests that directly shaped its prompt/knowledge fixes. At least one meaningful evaluation layer must remain independent of those fixes.