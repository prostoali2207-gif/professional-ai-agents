# Agent Architect — Holistic End-to-End Factory Qualification Gate

Status: proposed independent qualification extension. This gate does **not** replace existing Architect behavioral, reuse, resource/cost, security, state, or applied-agent qualification gates. It tests whether the qualified pieces compose into a reliable agent-building system from an unfamiliar goal to an independently qualified output.

## Purpose

Test the whole Agent Architect pipeline as a factory, not merely isolated methodology clauses or local behaviors.

The construct under test is:

`unfamiliar goal -> profession reconstruction -> boundary decision -> reuse decision -> evidence/research -> competency model -> knowledge packaging -> judgment/workflow/tools/runtime/security -> evaluation design -> candidate -> independent executable qualification -> repair/regression -> release decision`

A polished design document is not sufficient evidence. The terminal evidence is whether the produced solution survives independent executable/practical qualification under the declared professional boundary.

## Independence rules

1. The candidate Architect must not see the held-out grader, expected architecture, reference solution, scoring keys, or hidden failure cases.
2. Test prompts must specify user goals and constraints, not the profession label or preferred architecture unless that is genuinely part of the user request.
3. The evaluator must not allow the Architect to self-award PASS.
4. Evaluation design produced by the Architect is itself an artifact under test and must be independently reviewed before it is used as release evidence.
5. Existing Architect release fixtures must not be weakened or rewritten to accommodate this gate.
6. Failures must be classified by responsible layer. Do not repair a factory-level defect by patching only the held-out profession candidate unless evidence shows the defect is profession-specific.
7. Model/provider choice, quotas, and cost controls follow the existing Resource & Cost Engineering rules. This gate does not justify unnecessary full-suite model consumption.

## Required held-out task families

Use at least four materially different tasks. The exact tasks and hidden evaluation cases must be frozen before candidate execution.

### H1 — Analytical / evidence-heavy profession

Select an unfamiliar analytical profession where strong work depends on source quality, construct validity, conflicting evidence, uncertainty, and defensible synthesis.

The task must force the Architect to distinguish professional knowledge from evidence-handling competence and to design tests that can expose invalid aggregation, weak inference, or authoritative-but-inapplicable evidence.

### H2 — Creative / judgment-heavy profession

Select an unfamiliar creative profession with genuine solution-space openness and meaningful craft judgment.

The task must test whether the Architect can preserve divergence before convergence, separate constraints from taste, encode professional critique without reducing quality to checklists, and design evaluation that distinguishes polished imitation from appropriate original work.

### H3 — Tool-heavy / stateful profession

Select an unfamiliar profession requiring external tools, multi-step state, recovery, permissions, and downstream verification.

The task must expose whether the Architect correctly specifies tool eligibility, authority, state persistence, checkpoint/resume, error recovery, side-effect control, and direct verification rather than relying on narrative claims.

### H4 — Agent-not-needed boundary case

Select a goal for which the strongest architecture is **not** a new autonomous professional agent. The best solution should plausibly be one of:

- deterministic software/workflow;
- existing reusable capability or professional core with thin specialization;
- human-controlled process with limited AI assistance;
- tool or integration rather than a new role;
- explicit rejection because the requested authority cannot be safely or professionally delegated.

The Architect must earn PASS by rejecting unnecessary agent creation and choosing the simpler boundary for evidence-based reasons. Creating a new agent merely because the repository builds agents is a factory-level failure.

## Per-task required observable artifacts

For each held-out task, capture at minimum:

1. **Goal and boundary reconstruction** — real work, outputs, stakeholders, authority, out-of-scope work, and whether an agent is actually warranted.
2. **Reuse/capability decision** — `REUSE | ADAPT | EXTEND | FORK | BUILD NEW | REJECT`, with compatibility evidence and delta.
3. **Research/evidence record** — material claims, source classes, freshness/applicability decisions, conflicts, unresolved uncertainty, and live-research routing.
4. **Competency model** — observable CORE and BOUNDARY-CRITICAL competencies with expert-vs-average discriminators.
5. **Knowledge packaging** — stable/runtime/live/tool-backed/escalated dependencies and proof that critical knowledge is available when needed.
6. **Professional judgment model** — cues, trade-offs, exceptions, failure modes, escalation triggers, and justified rule-breaking where relevant.
7. **Workflow/tools/runtime/security design** — only to the depth materially required by the task.
8. **Evaluation package** — development vs holdout separation, practical/adversarial cases, graders/verifiers, hard fails, thresholds, leakage controls, and executable evidence chains for critical behavioral claims.
9. **Candidate implementation or non-agent architecture** — the actual artifact to be tested.
10. **Independent qualification record** — direct execution evidence and final `PASS | REVISE | REJECT | NOT EXECUTABLE` decision.
11. **Repair/regression record** when any failure occurs.

## Cross-task factory scoring dimensions

Score factory behavior across the set, not only each profession independently.

### F1 — Profession reconstruction accuracy

PASS requires that the Architect identifies the real profession/system boundary without merely echoing the user's title or prematurely writing a prompt.

### F2 — Hidden-gap discovery

PASS requires material adjacent/tacit competencies, failure modes, and unknown-unknown search appropriate to consequence and coupling.

### F3 — Architecture selectivity

PASS requires the simplest sufficient architecture. Over-agentization and unjustified multi-agent decomposition are failures.

### F4 — Evidence discipline

PASS requires material decisions to follow evidence rather than user/AI preference, including appropriate live research when knowledge is volatile or uncertain.

### F5 — Reuse judgment

PASS requires compatibility-based reuse decisions rather than title matching or reflexive rebuilding.

### F6 — Runtime realism

PASS requires critical knowledge, tools, state, permissions, and recovery behavior to exist at runtime rather than only in research notes or prose.

### F7 — Evaluation construct validity

PASS requires tests to elicit the claimed competence and graders/verifiers to measure the intended behavior rather than surface polish.

### F8 — Independent outcome quality

PASS requires the produced candidate/non-agent solution to survive independent practical/adversarial qualification. Self-evaluation cannot satisfy this dimension.

### F9 — Failure localization and repair

When a case fails, the Architect must identify whether the defect belongs to Architect methodology/router, reusable core, domain specialization, runtime/tooling, evaluation infrastructure, or the held-out candidate, then repair the responsible layer and run affected regression.

### F10 — Boundary restraint

H4 must demonstrate that the Architect can conclude `no new agent` when warranted. This is a mandatory anti-bias check.

## Hard-fail conditions

Any of the following blocks a holistic factory PASS:

- writing the applied `SKILL.md` before profession/evidence/evaluation work is materially established;
- treating user or AI opinion as sufficient evidence for a material professional claim;
- choosing a new agent architecture in H4 without evidence that simpler mechanisms are insufficient;
- claiming a critical behavioral capability without executable/direct evidence when execution is available;
- allowing the Architect to grade its own final output as the sole release authority;
- leaking held-out grader keys, reference architecture, or hidden fixtures to the candidate;
- changing frozen thresholds/hidden fixtures after seeing candidate behavior to obtain PASS;
- packaging decision-critical knowledge only in temporary research/chat context while claiming runtime availability;
- unsafe authority expansion, unbounded side effects, or missing escalation on a consequential task;
- declaring factory PASS when any mandatory held-out family remains `REVISE`, `REJECT`, or `NOT EXECUTABLE`.

## Release rule

Holistic factory PASS requires:

- all four held-out families executed under frozen conditions;
- H1–H4 each independently qualified as PASS at the final candidate/non-agent boundary;
- no hard fail;
- F1–F10 all satisfied across the set;
- any discovered Architect-level defect repaired generally and followed by targeted regression plus any broader regression justified by coupling;
- a replayable run record identifying Architect candidate SHA, held-out task-pack digest/version, evaluator/grader versions, tool/provider assumptions, and final evidence.

A PASS here means only that the tested Architect version demonstrated end-to-end composition across these held-out families. It is not a certificate that every future profession will be modeled correctly, and it does not remove the requirement that every applied agent pass its own qualification.

## Cost-aware execution strategy

Do not begin with four expensive full builds if a cheaper discriminating stage can falsify the factory first.

Recommended sequence:

`static integrity/preflight -> H4 boundary case -> one highest-risk unfamiliar full case -> inspect failures -> repair if Architect-level -> targeted regression -> remaining held-out families -> final one-SHA factory release run`

Reuse valid unchanged evidence where allowed by the existing evaluation-integrity policy, but never reuse historical evidence for newly affected behavior merely to save quota.

## Evidence record template

For each run record:

- Architect candidate SHA
- task-pack version/digest
- held-out family
- provider/model/tool versions where material
- pre-run budget gate
- produced artifact SHAs
- evaluator identity/version and independence statement
- fixture/grader version/digest
- scores and hard fails
- direct execution evidence
- defect classification
- repair SHA if applicable
- regression evidence
- final decision

## Interpretation

This gate is an **additional composition test**, not evidence that previous Architect qualification was invalid. A failure becomes evidence against the affected factory claim only after root-cause analysis. A repeated cross-domain failure attributable to Architect itself should trigger Architect repair and impact analysis of previously built agents that depend on the defective behavior.