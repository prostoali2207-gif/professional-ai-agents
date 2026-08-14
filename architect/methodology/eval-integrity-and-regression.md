# Evaluation Integrity and Regression Engineering

Status: v0.2.

## Threat model

An evaluation can improve while real capability does not. Agent Architect must defend against evaluation overfitting, leakage, contamination, grader drift, state/reset artifacts, security-test trivialization, stochastic inconsistency, and regression blindness.

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
2. identify root-cause layer;
3. create a regression test for the capability, not merely the exact wording;
4. repair the correct layer;
5. test nearby variants;
6. rerun holdout/practical evaluation where material.

## Leakage controls

Track whether eval cases or close paraphrases have entered:

- prompts/instructions;
- knowledge files;
- skills/procedural packages;
- worked examples/demonstrations;
- memory stores/checkpoints;
- development discussions;
- generated synthetic training/eval material.

If so, downgrade the independence of that evaluation.

## Benchmark contamination

External benchmark scores are evidence only with caveats. Training-data opacity and benchmark exposure can inflate apparent capability. Prefer fresh, domain-specific, procedurally generated, or expert-authored tasks when independent evaluation matters.

## Stateful evaluation integrity

Long-horizon and multi-session agents can be evaluated incorrectly if state is reset, leaked, or pre-populated in ways unlike deployment.

Record and control as relevant:

- initial session/memory state;
- seeded facts and their provenance;
- state changes during the run;
- checkpoint/restart boundaries;
- compaction/summarization events;
- memory writes/deletions;
- tool/database end state;
- whether previous trials can contaminate later trials.

A stateful benchmark must specify what persists between turns, sessions, tasks, users, and repeated trials.

## End-state and trajectory agreement

When a task changes external state, prefer direct end-state verification over conversational declarations of success. For interactive work, grade both final state and trajectory where policy/tool-use correctness matters.

A correct prose answer cannot compensate for the wrong persisted database/file/account state.

## Reliability across trials

For stochastic interactive agents, single-run success is weak evidence. Repeat representative tasks where inconsistency can change the release decision.

Use metrics appropriate to the claim, for example:

- per-task pass rate;
- critical-failure rate;
- distribution of cost/latency/actions;
- pass-across-repeated-trials style reliability measures when repeated success is required.

Do not quote a best run as system reliability.

## Grader drift

Version graders and rubrics. Recalibrate against expert judgments after meaningful rubric/model changes. Keep disagreements as diagnostic data rather than forcing artificial consensus.

## Security-eval integrity

Prompt-injection/security tests should not consist only of obvious strings such as `ignore previous instructions`.

Use varied attack locations and forms:

- external document/web content;
- retrieved records;
- tool output;
- memory entries;
- third-party skills/scripts;
- delegated agent output;
- paraphrased/obfuscated instructions.

Also test legitimate task completion. A system that passes by refusing all external content has not demonstrated useful robustness.

## Metamorphic and contrastive tests

Where exact gold answers are difficult, hold the underlying professional decision constant while perturbing irrelevant surface details, context order, distractors, source wording, or user confidence.

Use contrastive pairs to test whether the agent changes behavior when—and only when—a decision-relevant variable changes.

These tests help expose style matching, memorization, positional bias, and brittle capability selection.

## Anti-gaming tests

Include cases designed to expose:

- rubric keyword matching;
- verbose but unsupported answers;
- correct final answer reached through invalid evidence;
- memorized benchmark phrasing;
- refusal to admit uncertainty;
- superficial checklist compliance;
- state leakage between supposedly independent tasks;
- fake security compliance through blanket refusal;
- unbounded retry/reflection that eventually gets lucky.

## Replay and reproducibility

For consequential agent evals preserve enough observable run data to diagnose failures without requiring private chain-of-thought:

- task/eval version;
- agent/model/runtime/tool versions;
- initial state/checkpoint references;
- actions/tool calls and observations;
- material evidence references;
- approvals/errors/retries/replans;
- final verified state;
- cost/latency where material;
- termination reason.

Use `execution-control-and-remediation.md` for the run-record model.

## Gate

No agent may be declared competent solely because it passes tests that directly shaped its prompt/knowledge/skill fixes. At least one meaningful evaluation layer must remain independent of those fixes.

For stateful, security-sensitive, or interactive tool-using agents, benchmark PASS additionally requires representative tests in those modes rather than inference from static/conceptual evals.
