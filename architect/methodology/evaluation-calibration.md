# Evaluation and Grader Calibration

Status: v0.1.

## Purpose

An agent is not ready because its files look comprehensive. It is ready only when representative and adversarial evaluation provides evidence of competence. Evaluation itself can fail, so graders and rubrics must also be tested.

## Evaluation stack

Use the cheapest reliable grader for each criterion, but do not force deterministic grading onto inherently judgment-heavy work.

Preferred order:

1. deterministic checks for exact, executable, or state-based requirements;
2. programmatic/structural checks for schema, tests, artifacts, traces, and invariants;
3. domain rubrics scored by calibrated model graders where appropriate;
4. blind expert judgment for subjective, high-stakes, or difficult criteria;
5. direct user/deployment evidence when real-world performance is the true target.

OpenAI's grader APIs support string checks, Python graders, label/score model graders, and compositions of multiple graders. This is evidence that heterogeneous grading is expected rather than one universal evaluator.

## Authentic task design

Each agent evaluation suite should contain realistic work products rather than only knowledge questions.

A representative set should cover:

- routine case;
- ambiguous case;
- conflicting requirements;
- insufficient information;
- bad user premise;
- tool failure;
- misleading evidence;
- time/version-sensitive information;
- downstream verification;
- recovery after an initial wrong move.

For long-horizon agents, grade both the final outcome and the trajectory: tool selection, evidence gathering, intermediate decisions, state changes, and recovery.

## Rubric engineering

A rubric criterion must describe observable evidence.

Bad:

`Shows good professional judgment.`

Better:

`Identifies that the supplied market examples are not comparable, separates new/GCC/export-only/used populations before estimating price, states residual uncertainty, and refuses to present an unsupported point estimate.`

Each criterion should define:

- target capability;
- observable pass evidence;
- material failure;
- severity/weight;
- whether partial credit is meaningful;
- required artifacts or traces;
- forbidden shortcuts.

## Grader calibration

Before trusting a model grader:

1. assemble a calibration set with clear passes, clear failures, and difficult boundary cases;
2. obtain an expert reference judgment where feasible;
3. run the grader blind to the desired outcome;
4. compare disagreement patterns, not only aggregate score;
5. refine the rubric before refining the grader prompt;
6. retest on held-out cases;
7. preserve cases where experts legitimately disagree instead of forcing false certainty.

A grader that merely agrees with the agent architect's own preferences is not calibrated.

## Inter-rater discipline

For judgment-heavy tasks, periodically use multiple independent graders or experts. Investigate systematic disagreement by criterion.

Possible causes:

- ambiguous rubric;
- missing domain context;
- criterion conflates multiple abilities;
- grader bias toward style/verbosity;
- evaluator lacks required expertise;
- genuine professional disagreement.

Do not hide disagreement inside an average score.

## Outcome vs process grading

Outcome grading answers: did the result work?

Process grading answers: was the route professionally defensible?

Both can matter. Examples:

- a correct answer reached through fabricated evidence is a process failure;
- a strong research process may still yield an incorrect implementation and therefore fail outcome criteria;
- an implementation that passes tests but violates an unstated critical contract exposes a missing eval, not automatic competence.

## Regression suite

Every confirmed agent failure should become one of:

- a new regression case;
- a broader adversarial family if the failure reveals a class of weakness;
- a revised criterion if the previous eval could not detect it.

Never optimize only for the exact wording of a failed case.

## Statistical caution

Benchmark scores are estimates, not metaphysical truth. NIST emphasizes explicit measurement targets, assumptions, uncertainty, representative conditions, and comparison against relevant benchmarks. For stochastic agents, repeat trials where variance can change the conclusion.

Record at minimum when relevant:

- model/version;
- agent version/commit;
- tools/environment;
- dataset/eval version;
- number of trials;
- score distribution or pass rate;
- important failure classes;
- grader version;
- unresolved uncertainty.

## Practical release gate

A professional agent should not pass solely on aggregate score. Require all critical criteria to pass.

Example:

`95% overall` cannot compensate for consistently fabricating citations, skipping downstream verification, or failing safety-critical escalation.

Use severity-aware gates:

- P0: catastrophic / integrity / safety failure — zero tolerance for release;
- P1: core professional capability failure — must be corrected;
- P2: meaningful quality weakness — may block depending on role;
- P3: polish or low-impact inconsistency.

## Red-team perspectives

Before declaring readiness, explicitly ask:

- What would a senior practitioner say this test suite fails to measure?
- What would an instructor say is being memorized rather than demonstrated?
- What would a hiring manager need to observe before trusting this agent with real work?
- Which shortcuts could score well while producing professionally weak work?

## Quality gate

Evaluation architecture passes only when:

- test tasks resemble the deployment context;
- critical competencies are independently observable;
- graders are calibrated on boundary cases;
- stochastic variance is considered where material;
- critical failures cannot be averaged away;
- failures feed regression and root-cause analysis;
- there is at least one direct practical task and one adversarial task per core competency cluster.
