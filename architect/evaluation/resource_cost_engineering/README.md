# Resource & Cost Engineering evaluation

Status: **v1.2 integration PASS**.

## Purpose

This package evaluates Resource & Cost Engineering at two levels:

1. mechanically inspectable budget/routing/accounting invariants with standard-library Python and zero model calls;
2. frozen semantic/adversarial professional-judgment cases where deterministic predicates are insufficient.

It qualifies only the RCE integration surface. It does not make volatile provider pricing/quota durable knowledge and does not qualify any applied agent automatically.

## Deterministic run

```bash
cd architect/evaluation/resource_cost_engineering
python -m unittest -v test_rce.py test_semantic_cases.py
```

Current rebased-candidate result:

`Ran 16 tests ... OK`

The mechanical GitHub Actions gate explicitly records `model/API generation calls = 0`.

## Covered mechanical gates

- RCE-B1: deterministic evidence blocks unnecessary LLM work;
- RCE-B2: fresh reusable evidence blocks duplicate work;
- RCE-B3: protected release reserve cannot be consumed by exploration;
- RCE-B4: affected targeted regression precedes a non-release full suite;
- RCE-B5: stale material pricing causes DEFER;
- RCE-B6: fresh authoritative pricing permits continuation when other gates pass;
- RCE-B7: privacy/security/provider eligibility dominates price;
- RCE-B8: a run with no expected decision-relevant information gain is blocked;
- RCE-B9: a stronger method is permitted when expected total resource/rework cost beats a cascade;
- RCE-B10: potentially material runs require stop and mid-run exhaustion semantics;
- RCE-B11: post-run accounting identifies low-information spend, duplicate hypotheses, and retry-budget violations;
- RCE-B12: regression for the 2026-08 Copilot validation incident: exploration must not consume protected capacity, and a known affected scope narrows to targeted regression before a full release suite when valid.

The deterministic suite also validates the exact frozen RCE-S1–S10 case set, required fields, false-economy coverage, and absence of embedded named-provider price-memory tables.

## Semantic/adversarial gate

`semantic_eval_contract.md` preregisters RCE-S1 through RCE-S10. All ten are P0 for the integration claim.

A corrected minimal semantic smoke first passed RCE-S1 and RCE-S2 on exact candidate SHA `a92b05281f1dfe9e4cc697fa70391b19347357f2` with two model calls and zero application retries.

The final sealed integration run then executed all ten frozen cases on exact candidate SHA `d0d5b4fcc7613c1139acfbb190d1020cce5f783d`:

- RCE-S1–RCE-S10: **10/10 PASS**;
- planned model calls: 10;
- application retries: 0;
- model used only as evaluation transport: `gemini-3.5-flash-lite`, `medium` thinking;
- workflow run: `31944762944`;
- job: `95158971938`;
- artifact ID: `9262997828`;
- artifact digest: `sha256:75164af32dfe077b72d225b91e141d875cea7c8ba70b7c8cc5bc8a51a50c2a96`.

The qualifying run preserved candidate-hidden expected decisions and mechanically required every case to pass its frozen decision/rationale predicate.

## Resource-control behavior of the eval itself

The semantic evaluator follows the capability it measures:

- deterministic lint/preflight before model use;
- minimal affected smoke before the full integration suite;
- exact candidate binding;
- live model-eligibility probe with zero generation calls;
- paced one-shot calls for the final ten-case suite;
- no application-level retries;
- semantic workflows returned to manual-only after qualification so ordinary commits cannot consume quota.

The full release run used 10 model calls and provider-reported 73,624 total tokens, including 66,804 input tokens. It produced mandatory independent release evidence and is not classified as waste simply because the smaller smoke had already passed.

## Boundary

RCE v1.2 PASS means the current Agent Architect RCE integration met its specified deterministic and semantic gates. It does not prove every future resource decision is optimal, establish a permanent cheapest provider/model, or permit exact pricing/free-tier/quota claims from memory.

Volatile pricing, billing tier, account allowance, provider health, and quota remain live evidence. Any behavior-relevant change to RCE instructions, semantic fixtures/expectations, grader, or evaluator requires impact analysis and appropriate regression/release revalidation.

Canonical evidence record: `integration-candidate-validation-2026-08-15.md`.
