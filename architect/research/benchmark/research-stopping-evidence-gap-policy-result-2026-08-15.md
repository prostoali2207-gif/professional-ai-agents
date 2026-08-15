# Research Stopping / Evidence-Gap Policy Result — 2026-08-15

## Verdict

**PASS (deterministic policy contract), scoped.**

Run: GitHub Actions `Research Stopping Evidence Gap Policy v0.1`, run `31877422904`.

Frozen cases passed: **10/10**.

The gate distinguishes:

- `CONTINUE` — a concrete next action can close a material evidence gap;
- `STOP` — required evidence is adequate and remaining retrieval is low-value duplication;
- `STOP_WITH_LIMITATION` — remaining gaps are non-critical or cannot justify additional resource spend;
- `CLARIFY_FIRST` — missing user/context information dominates retrieval;
- `ESCALATE_OR_DEFER` — a high-stakes critical gap remains but resource/provider access prevents adequate verification.

## Required rules

1. Stopping is based on **open evidence gaps**, not arbitrary source counts.
2. More URLs from the same lineage do not create marginal evidentiary value.
3. Live material conflicts, missing required primary evidence, and lifecycle uncertainty remain continuation triggers when a viable next action exists.
4. Resource exhaustion or provider failure is an operational state, not evidence that a claim is resolved.
5. A high-stakes claim with a critical unresolved gap must not be downgraded merely to save money; the correct action is escalation, deferral, or explicit abstention.
6. If jurisdiction, target version, or other prerequisite context is missing, clarification may be cheaper and more informative than another search.
7. Marginal value is categorical in v0.1 (`HIGH/MEDIUM/LOW/NONE`); it is **not** a calibrated probability or utility estimate.

## Failure modes covered

- endless search after a claim is already adequately supported;
- counting duplicate/syndicated evidence as reason to continue;
- stopping too early on unresolved primary-source or lifecycle gaps;
- retry storms after quota/provider failures;
- spending retrieval budget when a clarification is required first;
- hiding high-stakes uncertainty because the free quota is exhausted.

## Red-team / unresolved gaps

A senior researcher or evaluation scientist would still require empirical calibration of marginal-search value across real tasks. The policy does not yet prove that a specific grouped or split query has the optimal expected value.

A resource/cost engineer would require explicit provider budgets, latency ceilings, retry budgets, cache hit-rate observability, and task-level cost telemetry when this architecture is implemented.

A security engineer would require that retrieved content cannot manipulate the stopping state, gap severity, or budget class. Those values must remain inside the trusted orchestration boundary.

Therefore the scoped verdict is:

**STOPPING POLICY CONTRACT — PASS**  
**EMPIRICAL MARGINAL-VALUE CALIBRATION — NOT YET VALIDATED**

The workflow was converted to `workflow_dispatch` only after PASS to avoid unnecessary CI consumption.
