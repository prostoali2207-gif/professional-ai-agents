# Resource & Cost Engineering deterministic evaluation

Status: research/evaluation instrument only. This package does not modify Agent Architect runtime behavior and does not change PR #1.

## Purpose

This harness tests mechanically inspectable Resource & Cost Engineering behavior without paid model calls. It is intentionally standard-library-only Python.

## Run

```bash
cd architect/evaluation/resource_cost_engineering
python -m unittest -v
```

## Covered gates

- RCE-B1: deterministic evidence blocks unnecessary LLM work;
- RCE-B2: fresh reusable evidence blocks duplicate work;
- RCE-B3: protected release reserve cannot be consumed by exploration;
- RCE-B4: affected targeted regression precedes a non-release full suite;
- RCE-B5: stale material pricing causes DEFER;
- RCE-B6: fresh authoritative pricing permits continuation when other gates pass;
- RCE-B7: privacy/security/provider eligibility dominates price;
- RCE-B8: a run with no expected decision-relevant information gain is blocked;
- RCE-B9: direct use of a stronger method is permitted when it has lower expected total cost than a cascade;
- RCE-B10: potentially material runs require stop and mid-run exhaustion semantics;
- RCE-B11: post-run accounting identifies low-information spend, duplicate hypotheses, and retry-budget violations;
- RCE-B12: regression for the 2026-08 Copilot validation incident: exploration must not consume protected capacity, and when capacity exists a known affected scope narrows to TARGET before full-suite execution.

## Evidence record

Local deterministic execution on 2026-08-15:

`Ran 12 tests in 0.001s — OK`

No model, provider API, paid subscription, or billing change was required for this execution.

## Boundary

Passing these tests does not prove that Agent Architect v1.2 has integrated the capability. It proves only that the proposed deterministic budget-gate semantics and fixtures are executable. Semantic/model-routing claims still require separate evidence where mechanical predicates are insufficient.
