# v0.7 gate failures — root cause, 2026-08-29

Gate `analytics-v0.7-heldout-2026-08-29`, run `33239983604`: 24/30 PASS, five behavioural
failures, one execution error, **zero oracle defects**. Classified per `architect/SKILL.md`
Phase 13: `FAIL -> classify -> root cause -> repair the responsible layer -> regression test`.

No instrument defect was found, so the harness and oracle are untouched.

## Classification

| # | Observed | Layer that owns it |
|---|---|---|
| A | `INCONCLUSIVE` aimed at an arm, 3 trials | **candidate — rule never given** |
| B | Causal status/ceiling downgraded on a sparse but identified design, 1 trial (P0) | **candidate — two rules unreconciled** |
| C | Invented `none_decidable_reason` on a closed object, 1 trial | **candidate — rule never given** |
| D | Invalid JSON returned, 1 execution error | **candidate — rule never given** |

## Root cause

**The instrument out-ran the model.** Three of the four failure modes are rules the candidate
was never given, and one is two rules it was given that pull in opposite directions at the same
decision point.

### A — the action-to-scope mapping exists only in the grader

`target_by_action` was added to the **oracle** on 2026-08-28 as audit repair 2. It was never
mirrored into the candidate. No overlay tells the candidate that `INCONCLUSIVE` and `CONTINUE`
are verdicts on the registered comparison while `KILL` and `SCALE` apply to an arm.

Worse, the only target guidance the candidate has pushes the other way. v0.5 states:

> "Do not return a phrase, a description of the comparison, or two arms joined together —
> **an action applies to one arm.**"

The whole-experiment case appears only as a conditional afterthought. So the candidate was
told an action applies to one arm, was never told which actions are exceptions, and was then
failed for naming an arm. That is an architect omission, not candidate incompetence.

### B — `insufficient power` and the sparsity rule are never reconciled

v0.1 line 157 lists `INCONCLUSIVE` as correct when the registered question cannot be answered
"because of missing/immature data, **insufficient power**, …".

v0.6 states "Sparse outcomes never lower the ceiling. Sample sparsity is a precision problem,
not an identification problem."

Both are correct and they are not contradictory: one governs the *action*, the other the
*causal ceiling*. But they sit five overlays apart, neither references the other, and they fire
at the same moment — a sparse case. A reader holding both, with no reconciliation, can carry
"insufficient power means we cannot answer" across from the action into the identification
channel. That is exactly the observed failure, and it is a knowledge-packaging defect rather
than a missing rule.

### C and D — constraints that live only in machine-readable or executor scaffolding

`additionalProperties: false` exists only inside the injected JSON Schema; no normative text
tells the candidate the contract is closed or what to do when it wants to say something the
contract has no field for. JSON-validity discipline exists only in the executor's system
preamble, which is scaffolding, not part of the frozen candidate.

`architect/SKILL.md` Phase 4 is explicit about this failure mode: *"Do not assume that research
retained in design notes, a source URL, or model priors will be available at runtime. Prove
discovery, routing, retrieval, depth, freshness, provenance, context fit, and safe failure
behavior for material knowledge dependencies."* Knowledge placed in the grader and in the
schema is not knowledge the candidate holds.

## What this is not

It is not a case for rewriting the core. v0.1–v0.6 professional judgement is not implicated:
the conflict, confounded, immature-horizon and clean-scale families passed 23/24, the
H-GDS-02 repair holds 17/18 across three fresh seeds, and the anti-gaming control passed 6/6.
Only expression and one unreconciled pair are at fault.

It is also not a case for loosening the oracle. Every failure is a real violation of a rule the
candidate should hold; the correct move is to give it the rule, not to stop checking.

## Repair, minimal

One overlay, v0.8, with two sections and no new professional judgement:

1. **Decision expression** — the action-to-scope mapping, the designated way to say "the
   registered question cannot be answered", the contract being closed, and output validity.
2. **Rule reconciliation** — `insufficient power` bears on the action and on `SCALE`, never on
   identification, stated at the point where both rules fire.

## Evaluation consequence

This repair changes candidate behaviour, so prior evidence does not transfer. It needs a new
freeze and a fresh seed before any qualification claim. Deterministic regressions can lock that
the failure modes remain detectable and that the rules are present; they cannot show the
candidate now behaves correctly. Only a fresh gate can.
