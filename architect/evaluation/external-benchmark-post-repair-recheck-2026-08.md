# External Benchmark Post-Repair Recheck — 2026-08-14

Status: **architecture/routing recheck PASS; behavioral benchmark remains REVISE.**

This file records the final state after the benchmark report was written and subsequent P1/P2 repairs were applied on the same branch. Where the earlier report says a focused strengthening is still needed for competency evidence modeling or tool execution contracts, this recheck supersedes that implementation-status sentence.

## Static architecture recheck

### Router reachability — PASS

`architect/SKILL.md` now routes all material benchmark-derived layers:

- `methodology/procedural-skill-packaging.md`;
- `methodology/runtime-state-memory-context.md`;
- `methodology/execution-control-and-remediation.md`;
- `methodology/agent-security-and-trust.md`;
- existing tool, retrieval, governance, evaluation and production-learning layers.

No new methodology layer is intentionally orphaned from the executable router.

### Lifecycle/status coherence — PASS

Current top-level claims agree:

- `SKILL.md`: v1.1 benchmark candidate;
- `README.md`: v1.1 benchmark candidate;
- `methodology/agent-architect-methodology.md`: v1.1 benchmark candidate;
- `references/source-register.md`: active register for v1.1 benchmark candidate.

Historical v1.0 evaluation files remain historical evidence; they are not current release claims.

### Competency-evidence inference — REPAIRED

`methodology/competency-assessment.md` now explicitly requires:

`competency/proficiency claim -> observable evidence -> task/situation -> grader/verifier`

and asks whether success can be explained by memorization, leakage, luck, or invalid process. Stateful and security/trust task families were also added where relevant.

### Tool/interface execution semantics — REPAIRED

`methodology/tool-human-factors.md` now includes typed/structured inputs where feasible, idempotency, partial-success/atomicity concerns, timeout/retry semantics, machine-observable success criteria, bounded observations, duplicate-action risk, state reconciliation, and empirical interface ablation where consequential.

### Evaluation integrity — REPAIRED AT ARCHITECTURE LEVEL

`methodology/eval-integrity-and-regression.md` now covers state/reset contamination, checkpoint/compaction state, end-state verification, repeated-trial reliability, security-eval usefulness, metamorphic/contrastive tests, and replayable observable run records.

### Production incident routing — REPAIRED

`methodology/production-incident-learning.md` can now route memory/state/context, checkpoint/compaction, execution-control, procedural-capability, prompt-injection/trust-boundary, skill-supply-chain, and permission/authority failures to their responsible layers rather than defaulting to prompt edits.

## What remains genuinely unproven

The remaining blocker is behavioral, not missing documentation.

Before benchmark PASS, execute the held-out gates in `v1.1-benchmark-validation-gate.md`, especially:

- multi-session update/abstention;
- compaction + checkpoint/resume;
- stall detection + bounded replan;
- non-idempotent partial-success recovery;
- indirect prompt injection while still completing useful work;
- memory poisoning resistance;
- procedural capability selection/progressive loading;
- capability-degradation/portability behavior;
- repeated-trial interactive reliability.

## Recheck decision

The external benchmark no longer exposes an un-routed P0/P1 documentation architecture gap in the repaired branch.

However, the new runtime/security/control mechanisms have not yet earned empirical release evidence. The correct status therefore remains:

`AGENT ARCHITECT BENCHMARK: REVISE`.
