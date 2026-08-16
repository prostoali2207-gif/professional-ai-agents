# Resource & Cost Engineering semantic/adversarial evaluation contract

Status: pre-integration evaluation design. This file does not modify Agent Architect runtime behavior.

## Purpose

The deterministic RCE-B1–B12 suite proves only mechanically inspectable budget-gate semantics. This contract defines the minimum professional-judgment cases that must pass before Resource & Cost Engineering can be claimed as integrated and behaviorally validated.

## Independence rule

Do not count prose written by the capability designer as behavioral evidence. A valid run requires:

- a frozen integration candidate;
- candidate output produced without access to expected decisions;
- sealed or independently held expected decisions;
- an independent grader or mechanical predicate wherever possible;
- candidate/version binding;
- preserved raw outputs and grading artifacts.

Self-graded narrative is invalid evidence.

## Cases

`semantic_cases.json` defines RCE-S1 through RCE-S10.

The cases cover:

1. stronger model despite higher price when the cheap model misses a critical quality floor;
2. rejection of fresh-but-scope-incompatible cached evidence;
3. privacy/security eligibility overriding free-provider economics;
4. synchronous execution when batching would break adaptive control flow;
5. direct strong-model execution when total cost including human repair beats a cheap cascade;
6. full-suite execution when a shared dependency creates broad regression risk;
7. required independent release evidence not being mislabeled as waste merely because the decision did not change;
8. deferral when public pricing is fresh but account-specific quota is unknown and the run is quota-sensitive;
9. authoritative primary evidence overriding a cheaper inadequate source;
10. latency/SLO overriding a cheaper batch route.

## Required response shape

A candidate should emit, at minimum:

```json
{
  "case_id": "RCE-S1",
  "decision": "STRONG_DIRECT",
  "binding_constraints": ["quality_floor"],
  "resource_tradeoff": "...",
  "rejected_alternative": "...",
  "escalation_or_stop_condition": "..."
}
```

The exact prose is not graded. The decision and binding constraints are.

## Criticality

All ten cases are P0 for the integration claim because each protects against a known class of false economy that can damage quality, reliability, security, evidence validity, release integrity, or operational continuity.

## Pass criteria

- 10/10 required decisions correct on the first sealed run;
- no case may violate its forbidden shortcut;
- required binding rationale must be present for every case;
- no fabricated pricing/quota precision;
- no substitution of a cheaper but ineligible provider/source/method;
- no universal `small model first`, `always batch`, `always target`, or `unchanged decision = waste` rule.

If a candidate fails any case:

`FAIL -> classify root cause -> repair responsible architecture layer -> rerun affected semantic case -> only after affected PASS consider broader regression`.

Do not weaken expected decisions to obtain PASS.

## Cost-control rule for this eval

The suite itself must follow RCE discipline:

1. lint fixtures deterministically first;
2. run one affected semantic case after each repair;
3. run all ten only at the integration gate or after changes that can affect multiple cases;
4. reserve quota for the final sealed 10-case run;
5. record planned vs actual model/tool calls and whether each run produced decision-relevant evidence.

## Boundary

Creating and linting this contract does not count as semantic PASS. PASS becomes possible only after there is an executable Agent Architect integration candidate to test.
