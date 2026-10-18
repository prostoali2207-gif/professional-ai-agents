# Tool Resilience & Capability Substitution evaluation

Status: **CANDIDATE — NOT YET QUALIFIED**.

## Purpose

This package evaluates whether Agent Architect treats tools as implementations of professional capabilities rather than hard-coded product categories, and whether it can recover from tool failure without unsafe or semantically invalid improvisation.

It intentionally tests both creativity and restraint. Passing requires finding non-obvious valid substitutes when they exist, rejecting false substitutes when invariants are lost, choosing bounded retry when substitution is unnecessary, and escalating when a consequential action cannot be reproduced safely.

## Current deterministic fixture check

Run:

```bash
cd architect/evaluation/tool_resilience
python -m unittest -v test_semantic_cases.py
```

This checks the development fixture contract only. It uses zero model/API calls and is not behavioral evidence.

## Semantic development suite

`semantic_cases.json` contains TRS-S1–TRS-S10 covering:

- capability reconstruction from authoritative exports;
- private-state false equivalence;
- cross-domain tool transfer;
- shared-dependency fallback traps;
- multi-tool composition;
- graceful degradation;
- irreversible-action escalation;
- semantic/denominator incompatibility;
- verification after substitution;
- anti-overengineering bounded retry.

`semantic_eval_contract.md` defines the grading and release boundary.

## Evidence and design rationale

The capability is supported by broader reliability engineering practice rather than by product folklore: resilient systems use graceful degradation, avoid pathological retries, isolate failed dependencies, and verify fallback behavior. Agent Architect extends those principles to professional tool use by adding capability abstraction, substitution compatibility checks, and bounded cross-domain transfer.

External reliability guidance is design evidence only. It does not establish that the candidate actually behaves correctly.

## Required next gate

Before integration into `main`:

1. freeze the candidate SHA;
2. run deterministic fixture lint;
3. execute a small affected semantic smoke;
4. execute held-out/paraphrased semantic cases with expectations hidden from the candidate;
5. execute controlled tool-degradation cases with observable traces for equivalent substitute, false substitute, dependency independence, and irreversible boundary;
6. red-team against over-novelty and unsafe workarounds;
7. only after PASS, run coupled Agent Architect regressions and consider merge.

No integration PASS should be inferred from these files alone.
