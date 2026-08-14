# Agent Architect External Benchmark — 2026-08-14

Status: **REVISE after benchmark; architecture repairs applied, behavioral validation pending.**

## Objective

Benchmark the current Agent Architect against strong contemporary agent-engineering systems, evaluation research, memory/control work, open-source agent implementations, and professional competency/assessment frameworks.

The question is not whether the repository contains many good ideas. The question is whether it models the layers required to build and validate professional agents that remain competent under long-horizon, stateful, tool-using, adversarial, and changing conditions.

## Evidence discipline

Sources were classified as:

- **generalizable engineering evidence** — recurrent mechanism across independent systems or empirical research;
- **platform-specific implementation** — useful implementation evidence, not universal law;
- **research evidence** — empirical or benchmark findings with scope limits;
- **professional/assessment framework** — evidence for profession reconstruction or validity of competence inference;
- **house style/opinion** — useful hypothesis only unless supported independently.

Vendor documentation was not treated as universal truth.

## Systems and implementations inspected

### Anthropic

Reviewed current Agent Skills / Claude skill architecture and agent-evaluation guidance. Skills use discoverable folders with instructions, scripts, and resources and progressive disclosure rather than placing all procedure in one prompt. Anthropic's agent security guidance also treats externally supplied content as an injection surface.

Representative sources:

- https://www.anthropic.com/engineering/building-effective-agents
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- https://support.claude.com/en/articles/12512176-what-are-skills
- https://www.anthropic.com/research/prompt-injection-defenses

### OpenAI / Codex

Reviewed current Codex/Skills material. Codex skills package instructions, resources, and scripts; current Codex practice emphasizes tool execution, validation of actual results, sandboxing/approvals/network policy, and agent-native telemetry rather than prose-only operation.

Representative sources:

- https://openai.com/index/introducing-the-codex-app/
- https://openai.com/academy/skills/
- https://openai.com/index/introducing-upgrades-to-codex/
- https://openai.com/index/running-codex-safely-at-openai/

### Google / DeepMind

Reviewed Google Agent Development Kit architecture and DeepMind's AI co-scientist work. ADK separates agents, workflows, session/memory services, long-running pause/resume, state, evaluation, and multi-agent composition. The AI co-scientist uses specialized generation/reflection/ranking/evolution/meta-review roles plus external scientific evidence and experimental validation; this is task-specific evidence for structured critique/search, not a universal multi-agent prescription.

Representative sources:

- https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/
- https://google.github.io/adk-docs/
- https://deepmind.google/discover/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/

### Microsoft

Reviewed current Microsoft Agent Framework and Magentic-One/Magentic-UI architecture. Agent Framework explicitly separates agents, harness, session state, context/memory providers, planning/todo state, compaction, workflows, checkpointing, human review, skills, observability, and tool approval. Magentic-One uses a Task Ledger and Progress Ledger with stall detection and replanning.

Representative sources:

- https://learn.microsoft.com/en-us/agent-framework/overview/
- https://learn.microsoft.com/en-us/agent-framework/get-started/harness
- https://arxiv.org/abs/2411.04468
- https://arxiv.org/abs/2507.22358

### Open-source engineering/scientific agents

Reviewed architecture rather than only project claims:

- **SWE-agent** — Agent-Computer Interface design; constrained file viewing/search/editing, lint-aware edits, explicit action/observation trajectories and reproducible configuration. Interface design itself materially changes agent performance.
- **OpenHands** — event-driven Action/Observation loop with AgentController, State, EventStream, Runtime/Sandbox, browser/shell/file tools, and replayable execution state.
- **Agent Laboratory** — staged literature-review, experimentation and report-writing workflow with specialized roles and executable scientific tooling.

These systems show that professional capability depends on the runtime/control/tool interface around the model, not just instructions and knowledge.

### Academic agent research

Key evidence reviewed:

- ReAct: interleaved reasoning/action with environment feedback — https://arxiv.org/abs/2210.03629
- Reflexion: feedback-driven episodic reflection can improve some tasks — https://arxiv.org/abs/2303.11366
- *Large Language Models Cannot Self-Correct Reasoning Yet*: intrinsic correction without external feedback can fail or degrade — https://arxiv.org/abs/2310.01798
- AgentBench: multi-environment interactive evaluation — https://arxiv.org/abs/2308.03688
- WebArena: realistic long-horizon environment and functional outcome evaluation — https://arxiv.org/abs/2307.13854
- GAIA: real-world tool-using assistant tasks — https://arxiv.org/abs/2311.12983
- tau-bench: user + tool + policy interaction, database end-state grading and multi-trial reliability — https://arxiv.org/abs/2406.12045
- LongMemEval: multi-session extraction, reasoning, temporal update and abstention — https://arxiv.org/abs/2410.10813
- contemporary surveys on agent evaluation, architecture and memory were used for coverage discovery, but primary systems/papers were preferred for material conclusions.

### Professional competency and assessment

Reviewed O*NET Content Model and Evidence-Centered Design (ECD) material. O*NET reinforces that profession models include work activities, tasks, work context, knowledge/skills, and occupational requirements rather than isolated topic lists. ECD contributes a critical validity chain:

`proficiency/competency claim -> observable evidence -> task designed to elicit evidence`.

Representative sources:

- https://www.onetcenter.org/content.html
- https://www.ets.org/research/policy_research_reports/publications/report/2002/ijzv.html

## What the pre-benchmark Architect already does strongly

### Stronger than typical vendor agent guidance

1. **Profession reconstruction before prompt/skill authoring.** CTA/CDM, tacit cues, expert-vs-average discrimination and adjacent-competency discovery are substantially deeper than generic agent frameworks.
2. **Evidence epistemics.** Claim-dependent authority, provenance, freshness, empirical construct validity and comparator compatibility go beyond most agent product documentation.
3. **Professional judgment.** The repository distinguishes rule, causal rationale, scope, exceptions, trade-offs and justified violations rather than relying on checklists.
4. **High-stakes authority.** `competence != delegable authority` and independent-reviewability are unusually strong professional-governance concepts.
5. **Creative-profession architecture.** Divergence/convergence, reference literacy, taste as observable comparative judgment, artifact-first critique and calibrated subjective evaluation avoid the common `best practices = taste` failure.
6. **Evaluation integrity.** Authentic tasks, outcome + trajectory grading, holdouts, contamination controls, grader calibration, stochastic caution and failure-to-regression loops are strong foundations.
7. **Anti-complexity discipline.** The least-complex-sufficient architecture rule is consistent with evidence that extra agents/coordination are not automatically beneficial.
8. **Production-learning discipline.** Incidents and user feedback are treated as evidence to validate and route to a root-cause layer, not automatic prompt additions.

## Gap analysis

Severity:

- **P0** — release-invalidating integrity/security/catastrophic architecture gap;
- **P1** — material core architecture gap; must repair before benchmark PASS;
- **P2** — meaningful weakness that should be strengthened;
- **P3** — low-impact refinement.

### 1. Architecture gap analysis

**P1 — runtime harness/control architecture was implicit.**

The prior architecture described workflow, tools and recovery, but not a complete long-horizon execution-control substrate: persistent task state, progress evidence, replan triggers, checkpoint/resume, bounded retries and termination semantics. Microsoft Harness, Magentic-One and event-driven open-source agents make these mechanisms explicit.

Repair: added `execution-control-and-remediation.md` and `runtime-state-memory-context.md` and routed them from `SKILL.md`.

### 2. Knowledge-model gap analysis

**P1 — procedural knowledge packaging was under-modeled.**

The prior model was strong on declarative source/knowledge engineering but weaker on the distinction among router metadata, procedural instructions, references, scripts, schemas, examples/assets and tool bindings. Modern skill systems independently converge on staged/progressive loading of these artifacts.

Repair: added `procedural-skill-packaging.md`.

### 3. Professional-judgment gap analysis

**P2 — judgment representation was strong, but runtime judgment revision lacked explicit information-gain policy.**

A professional can revise after new evidence; ritual self-reflection without new evidence is not equivalent. Empirical self-correction literature shows intrinsic correction can degrade reasoning.

Repair: runtime remediation now requires a discrepancy/evidence/verifier trigger and bounded correction loop.

### 4. Evidence / epistemics gap analysis

**P2 — competence evidence needed a more explicit inference chain.**

The repository already has authentic task/rubric engineering, but ECD makes the validity claim sharper: a competence claim must identify the observable evidence that warrants it and the task that elicits that evidence.

Required follow-up: strengthen `competency-assessment.md` and future eval templates with the explicit claim -> evidence -> task -> verifier chain. This is not yet enough of a blocker to justify a separate framework layer.

### 5. Tool-use / verification gap analysis

**P1 — tool interface model lacked enough execution semantics.**

Current `tool-human-factors.md` correctly models observable state, failure signals, side effects, reversibility and downstream verification. SWE-agent demonstrates that interface ergonomics and constrained, decision-relevant observations can materially change performance.

Remaining strengthening needed: typed schemas/errors, idempotency, timeout/retry semantics, partial-transaction/atomicity, stable machine-observable success criteria and empirical interface ablation when tool design is consequential.

### 6. Memory / context / retrieval gap analysis

**P1 — retrieval existed; memory/context did not exist as a first-class lifecycle.**

Missing concerns included: working vs session vs persistent state; write gates; temporal supersession; contradictions; compaction loss; checkpoint/resume; forgetting/deletion; memory poisoning; multi-session evaluation.

LongMemEval demonstrates that multi-session extraction, temporal reasoning, updates and abstention are separate capabilities and that long histories materially degrade existing systems.

Repair: added `runtime-state-memory-context.md`.

### 7. Evaluation / adversarial-testing gap analysis

**P1 — current cross-domain evaluations are strong conceptual architecture tests but do not yet exercise the newly discovered runtime layers.**

Existing evaluations test software, empirical analysis, creative work and high-stakes decision support. However, benchmark-relevant stateful/security/control-loop failures need executable or strongly simulated tests with observable state, not only conceptual PASS assertions.

Required before PASS:

- multi-session state/update/abstention test;
- compaction/checkpoint/resume test;
- stall/replan/bounded-retry test;
- prompt-injection/tool-output hijacking test with useful-task completion;
- memory poisoning/persistence test;
- procedural skill selection/resource-loading test;
- multi-trial reliability measurement for at least one interactive task.

### 8. Self-correction / remediation gap analysis

**P1 — development-time failure repair was strong; runtime repair was shallow.**

`FAIL -> root cause -> repair -> regression` is excellent for development. Runtime agents additionally need to detect that progress has stopped or an assumption was falsified and choose retry/replan/rollback/escalate without an infinite introspection loop.

Repair: added `execution-control-and-remediation.md`.

### 9. Portability / vendor-neutrality gap analysis

**P2 — philosophy was vendor-neutral, but capability portability was not explicit.**

A `SKILL.md` folder can be syntactically portable while behavior depends on memory, tool schemas, sandbox, approvals or context management that another runtime lacks.

Repair: new procedural and state layers require capability manifests, substitutes/unsupported environments, and cross-runtime testing before portability claims.

### 10. Unknown-unknowns pass

The most important missing layer a strong agent engineer would notice was **control-state architecture around the model**. The repository was stronger at reconstructing the human profession than at reconstructing the runtime machinery required for that professional model to remain coherent over long, interrupted, adversarial execution.

A second unknown-unknown was **trust provenance for procedural capability itself**: a third-party skill/script/reference package is part of the attack surface and can poison both runtime actions and persistent memory.

## Security/trust gap

**P0/P1 depending on authority — indirect prompt injection and capability supply-chain trust were insufficiently modeled.**

Operational governance already had least privilege, confidentiality and blast radius, but it did not independently model data-vs-instruction-vs-authority trust boundaries. Tool-using agents that browse, retrieve documents, read email/issues, or load third-party skills can be redirected by untrusted content.

Repair: added `agent-security-and-trust.md` and routed it before operational authority decisions.

For agents without external/untrusted content this may be non-material; for browser/email/retrieval/computer-use/write-capable agents it is release-critical.

## Red-team

### Senior AI agent engineer

Critique:

- v1.0 had excellent professional-domain modeling but under-specified the harness/runtime that keeps long tasks coherent.
- `workflow` was too conceptual without state, checkpoints, retries, progress and termination contracts.
- memory and tool interfaces needed stronger execution semantics.

Disposition: four architecture layers added. Runtime eval still required.

### Agent-evaluation researcher

Critique:

- cross-domain conceptual retests can overstate evidence because the method being evaluated also generates the PASS reasoning.
- single-run success is weak evidence for interactive stochastic agents.
- new capabilities need stateful, adversarial, multi-trial and end-state tests.

Disposition: accepted. Benchmark status remains REVISE until held-out practical gates run.

### Competency modeling / professional education specialist

Critique:

- competency definitions are strong but the inference model should be more explicit: which observed behavior licenses which mastery claim?
- work context and stakeholder/interpersonal constraints should be treated as profession evidence, not afterthoughts.

Disposition: `SKILL.md` now explicitly requires competency -> evidence -> task -> verifier. `competency-assessment.md` should receive a later focused ECD refinement rather than a new oversized layer.

### Real user of Agent Architect

Critique:

- the framework risks becoming bureaucratic if every layer is mandatory for every small agent.
- users need the architecture to decide when memory, security, multi-agent coordination or deep evaluation are unnecessary.

Disposition: preserve risk-proportionate routing. New files explicitly say not every agent needs every mechanism. Complexity must earn its operational value.

## Ideas from external systems that should NOT be copied

1. **Default multi-agent decomposition.** Co-scientist/Magentic-style specialization is powerful for some workflows, but coordination tax and shared-state risk remain. Keep least-complex-sufficient architecture.
2. **Vendor-specific runtime as methodology.** Microsoft Harness, Google ADK, Codex and Claude are implementation examples, not professional laws. Encode capability contracts, not dependencies.
3. **Unlimited reflection/self-correction.** Evidence shows intrinsic self-correction without external feedback can degrade performance. Require new information or verifier signals and bounded loops.
4. **Memory volume as capability.** Long context/vector storage is not reliable memory. Evaluate write, temporal update, contradiction, retrieval, use and forgetting separately.
5. **One scalar LLM judge.** Current mixed grading remains superior for professional competence and subjective creative work.
6. **Third-party skills as trusted because they follow a standard.** File-format interoperability does not establish code/instruction provenance or security.
7. **Benchmark score as authority to automate high-stakes decisions.** Existing high-stakes architecture correctly rejects this inference.

## Files changed in this benchmark revision

Added:

- `methodology/runtime-state-memory-context.md`
- `methodology/execution-control-and-remediation.md`
- `methodology/procedural-skill-packaging.md`
- `methodology/agent-security-and-trust.md`
- this benchmark audit

Strengthened/rerouted:

- `SKILL.md`
- `README.md`
- additional lifecycle/source/evaluation files as recorded in the branch history.

## Recheck against benchmarks after repair

### Anthropic/OpenAI skill pattern

Now represented: progressive loading, distinct instructions/resources/scripts, selection/dependency evaluation, procedural package security, portable capability contracts.

Remaining: run selection/resource-loading evals.

### Microsoft/Google long-horizon pattern

Now represented: session/working/persistent state distinctions, compaction, checkpoint/resume, progress tracking, replanning, bounded loops, observability/run records.

Remaining: execute stateful/resume/control tests.

### Open-source engineering-agent pattern

Now represented: observable Action/Observation-style run record, tool-interface semantics, downstream verification, runtime recovery.

Remaining: strengthen typed/idempotent tool contract guidance and run interface-ablation tests where material.

### Academic evaluation/memory/self-correction evidence

Now represented: multi-session memory abilities, end-state verification, multi-trial reliability requirement, external-feedback-driven correction and bounded remediation.

Remaining: construct held-out benchmark cases and collect behavioral results.

### Professional competency/assessment frameworks

The Architect remains strong on CTA and authentic tasks. The ECD inference chain is now exposed in the router, but a dedicated refinement of competency assessment evidence models remains P2.

## Decision

The benchmark found no reason to discard the core premise of Agent Architect. The profession-first/evidence-first foundation is unusually strong and should be retained.

However, the pre-benchmark v1.0 release claim was too broad because runtime memory/state, execution control, procedural packaging and agent security were not first-class layers and the evaluation suite did not test them behaviorally.

Architecture repair is complete enough to proceed to a new validation phase, but documentation repair is not equivalent to demonstrated capability.

**AGENT ARCHITECT BENCHMARK: REVISE**
