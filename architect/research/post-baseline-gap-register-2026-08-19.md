# Post-Baseline External Gap Register — Agent Architect

Status: research/evaluation planning only; no candidate behavior change.
Date: 2026-08-19
Frozen candidate: `2cc19fec73c1058f8c63e1c2216a8252e3fe4aae`

## Purpose

The 12-session sealed pilot passed without critical flags on judgment independence, evidence calibration, anti-contrarianism, reframing, and mechanism diversity. This document records externally evidenced capability gaps that the pilot did **not** establish.

A gap here is not a proven defect in Agent Architect. It is an untested failure class that should become a qualification target before any repair or stronger reliability claim.

## P0 gaps

### G1 — Persistent / memory-induced sycophancy

Risk: a candidate may resist user pressure in the current turn yet later write the user's unsupported belief, preference, or workflow into durable state, remove attribution/uncertainty, broaden scope, and reuse it as if authoritative.

Why the pilot missed it: all scored cases were fresh-session response tests; no memory-write -> cleared-session -> later-use pathway was tested.

Evidence:
- PASB (2026) reports a large downstream-failure jump after claims cross the durable commit boundary and identifies status promotion, attribution removal, and scope broadening as write-time failure patterns.
- MIST (2026) reports that memory augmentation can substantially amplify sycophancy and implicates lossy memory extraction as a driver.
- PersistBench (2026) reports high rates of memory-induced sycophancy and cross-domain leakage across evaluated systems.

Qualification target:
`user claim -> candidate response -> candidate-selected durable write -> cleared session -> neutral downstream task`

Grade the stored state itself, source/attribution/status preservation, retrieval scope, and downstream contamination. Include beneficial-memory controls so the solution cannot pass by refusing to use memory.

Sources:
- https://arxiv.org/abs/2607.10526
- https://arxiv.org/abs/2606.10949
- https://arxiv.org/abs/2602.01146

### G2 — Silent misframing under genuine ambiguity

Risk: the candidate can produce a coherent, executable architecture while silently committing to one plausible interpretation of an under-specified goal, target, objective, authority boundary, or success metric.

Why the pilot missed it: RF-01/RF-02 contained cues that supported a particular upstream reframe. They did not test cases where multiple interpretations remain genuinely viable and the professional behavior is to discriminate, inspect, or ask a targeted question.

Evidence:
- Ambig-DS (2026) isolates task-framing ambiguity and reports silent commitment/abdication failures. Allowing clarification recovers much of the loss, but agents are poorly calibrated on *when* to ask.

Qualification target:
paired fully specified vs minimally under-specified tasks, with an oracle/controlled clarification channel. Score both silent misframing and over-asking on clear controls.

Source:
- https://arxiv.org/abs/2605.09698

### G3 — Implicit professional requirement discovery

Risk: the candidate follows the literal request successfully while missing an unstated but professionally expected constraint that is discoverable from context/environment.

Why the pilot missed it: hidden requirements were mostly encoded as visible facts in the fixture. This is weaker than discovering constraints the user did not state.

Evidence:
- Implicit Intelligence (2026) evaluates unstated requirements that are discoverable through environmental exploration; even the best reported model passes fewer than half of scenarios.
- AlphaEval (2026) emphasizes production tasks with implicit constraints, undeclared expertise, fragmented information, and evolving stakeholder criteria.

Qualification target:
realistic incomplete briefs + inspectable environment/artifacts where critical constraints are discoverable but not prompt-stated. Independent domain practitioners preregister the hidden professional requirements before candidate execution.

Sources:
- https://arxiv.org/abs/2602.20424
- https://arxiv.org/abs/2604.12162

### G4 — Dirty-evidence / cognitive-trap reconciliation

Risk: the candidate appears evidence-driven but accepts the wrong datum because source material contains realistic contradictions, stale values, incompatible units, truncated lists, misleading defaults, or footnote/body conflicts.

Why the pilot missed it: evidence in the pilot was clean and internally consistent.

Evidence:
- OccuBench (2026) finds implicit data degradation harder than explicit failures because superficially valid observations must be challenged by the agent.
- The 2026 expert-consulting benchmark deliberately embeds cognitive traps such as inconsistent units, footnote contradictions, and precision traps; clean inputs systematically understate professional difficulty.

Qualification target:
fixtures with one or more realistic latent data-quality faults. Candidate must detect, localize, reconcile, re-query, or narrow the conclusion rather than simply use the first plausible value.

Sources:
- https://arxiv.org/abs/2604.10866
- https://arxiv.org/abs/2605.17554

### G5 — Long-horizon policy / principle drift

Risk: the candidate correctly identifies a governing rule early, then loses, overrides, or acts against it after many turns/tool steps while still claiming compliance.

Why the pilot missed it: multi-turn cases were short and did not test long contexts, policy mutation, competing local requests, or tool execution.

Evidence:
- HANDBOOK.md (2026) reports failures where agents let proximate requests override standing policy, perform checks and then act against the result, lose rule details over long horizons, and report compliance they did not achieve.

Qualification target:
long-horizon, multi-tool tasks governed by a mutated standing methodology/policy. Grade final state and prohibited actions mechanically, not only prose.

Source:
- https://arxiv.org/abs/2607.25398

## P1 gaps

### G6 — Selective correction when the candidate itself was wrong

The pilot tested resistance to wrong pressure and positive controls where the user's initial idea was good, but did not directly condition on a *wrong baseline recommendation* followed by a correct user correction.

Why it matters: pressure robustness and corrigibility are distinct. A stubborn agent can look excellent on anti-sycophancy tests.

Qualification target:
force/identify baseline-wrong cases, then provide correct correction, misleading correction, authority pressure, and doubt variants. Measure `correct update` separately from `wrong flip`.

Primary evidence:
- SycoBench-600, Findings of ACL 2026: https://aclanthology.org/2026.findings-acl.1759/

### G7 — Gradual conversational drift rather than single rebuttal

The pilot used short pressure sequences. Real conversations can shift through 5–10 locally reasonable concessions, praise, fatigue, status claims, or changing wording without decisive new evidence.

Qualification target:
longer pressure ladders, varied delivery order, and delayed-shock conditions. Measure turn-of-flip, cumulative confidence drift, and whether earlier evidence is still represented correctly.

Evidence basis:
- SYCON-Bench multi-turn sycophancy: https://aclanthology.org/2025.findings-emnlp.121/
- PASB temporal delivery patterns: https://arxiv.org/abs/2607.10526

### G8 — Professional depth beyond a clean architecture answer

Risk: the candidate points in the right direction but misses expert workflow details, negative criteria, jurisdiction/temporal constraints, or domain-specific failure modes.

Why the pilot missed it: cases were compact and mainly discriminated the recommendation, not full expert-grade execution.

Evidence:
- PRBench uses 1,100 expert-authored open-ended tasks and 19,356 expert criteria; top model performance remains low on hard professional subsets.
- OneMillion-Bench reports gaps on authoritative retrieval, conflicting evidence, constraint resolution, and professional compliance; scaffold choice materially changes outcomes.
- EuroExec reports a large gap between frontier models and expert-authored responses on real executive tasks.

Qualification target:
expert-authored, domain-authentic tasks with task-specific rubrics and negative criteria, ideally with blind practitioner grading and direct artifact verification where possible.

Sources:
- https://aclanthology.org/2026.acl-long.1958/
- https://arxiv.org/abs/2603.07980
- https://arxiv.org/abs/2608.04549

### G9 — Evaluator blind spots

Risk: a holistic grader may reward polished reasoning while missing a single decisive error or may over-penalize an unusual but valid solution.

Evidence:
- JADE (2026) argues for stable expert-grounded skills plus response-specific claim-level verification and reports failures missed by holistic judges.
- Expert consulting work shows value in combining deterministic verifiers with expert rubrics.
- LH-Bench reports stronger judge reliability with expert-authored than LLM-authored rubrics.

Qualification target:
combine mechanical/task-specific checks, expert-grounded rubrics, and blind pairwise human/practitioner preference where appropriate. Treat grader disagreement as evidence, not noise to hide.

Sources:
- https://arxiv.org/abs/2602.06486
- https://arxiv.org/abs/2605.17554
- https://arxiv.org/abs/2603.22744

## Controlled frozen-vs-normal deployment-gap experiment

The pilot validates the frozen Architect scaffold, not ordinary ChatGPT behavior.

Minimum three-arm design:

A. `Frozen Agent Architect + controlled context`
B. `Normal ChatGPT + same controlled task/context where product allows`
C. `Minimal/base control + neutral instruction` when technically feasible

Then separately:

D. `Normal ChatGPT in actual product conditions` with normal memory, history, tool routing, and product behavior.

Pre-register dimensions:
- evidence calibration;
- wrong-pressure stance flip;
- correct-correction acceptance;
- ceremonial contrarianism;
- implicit requirement discovery;
- ambiguity/ask-act calibration;
- mechanism diversity;
- convergence;
- authority/permission handling;
- memory contamination;
- long-horizon consistency;
- cost/latency/tool burden.

Do not attribute A-vs-D differences solely to Agent Architect: model routing, system instructions, memory, tools, retrieval, context length, conversation history, and product settings are confounders. A-vs-B is the cleaner incremental-scaffold comparison; D estimates deployment reality.

## Priority order for the next evaluation wave

1. Paraphrase/counterbalance replication of passed P0 constructs.
2. G6 selective correction on baseline-wrong cases.
3. G2 ambiguity + calibrated clarification.
4. G3 implicit professional requirement discovery.
5. G4 dirty evidence / silent degradation.
6. G7 gradual long-turn pressure.
7. G1 persistent memory contamination, if the deployment/runtime writes durable state or skills.
8. G5 long-horizon policy/tool execution, when harness capability exists.
9. G8 practitioner-authored professional-depth tasks across at least two unrelated domains.
10. Frozen-vs-normal controlled comparison and actual-product sample.

## Decision rule

A future full PASS should not trigger easier tests. Increase distance from the development distribution: new domains, hidden professional requirements, messier evidence, longer horizons, ambiguous framing, and independent expert-authored criteria.

Do not modify `architect/SKILL.md` merely because these gaps exist. Modify only after a reproducible failure cluster identifies a mechanism and a repair beats at least one serious alternative without coupled regressions.

## Red-team

Senior practitioner critique: a benchmark can reward elegant meta-reasoning without proving the Architect can create a working professional system. Countermeasure: include end-to-end applied-agent builds and artifacts, not only advisory answers.

Evaluator critique: the same team may still encode its own ontology of "unknown unknowns" into fixtures. Countermeasure: independent practitioner-authored hidden criteria and production-derived tasks.

Hiring/operational-owner critique: deeper evaluation can become too expensive to run routinely. Countermeasure: separate cheap regression gates from expensive periodic qualification suites; do not weaken the latter because the former passes.

## Current disposition

- 12-session pilot: passed, diagnostic evidence only.
- Candidate mutation: prohibited until stronger evidence warrants it.
- Separate repository: not justified yet.
- Next action: build the second-wave sealed qualification suite from this gap register, with independent fixture authorship where feasible.