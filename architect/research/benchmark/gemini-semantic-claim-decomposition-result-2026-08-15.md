# Gemini Semantic Claim Decomposition — Result — 2026-08-15

Status: **SEMANTIC PASS 5/5, 0 genuine P0** after preserving the raw run and correcting a deterministic alias-grader defect. One transient 503 occurred before the successful attempt.

## Purpose

Test the previously unproven step before claim/stakes routing: whether a live model can extract decision-relevant atomic claims, high-stakes actions and material qualifiers from natural mixed user requests.

To conserve free quota, five cases were evaluated in a single schema-enforced Gemini request.

Successful attempt usage: 359 prompt tokens, 1265 candidate tokens, 1624 total tokens.

## Cases and semantic result

### D1 — medical action mixed with price

The model extracted:

- abrupt stopping of daily medicine X and substitution with supplement Y — `HIGH`;
- safety of supplement Y as replacement — `HIGH`;
- supplement price — `LOW`.

It preserved qualifiers including `abrupt_discontinuation` and `daily_medication`.

The original lexical grader nevertheless marked the first high-stakes action missing because its alias set recognized `stop medicine` but not the returned paraphrase `Stopping prescription medicine ... to substitute it ...`. This was a grader coverage defect. The alias set was corrected without another model call.

Semantic verdict: **PASS**.

### D2 — UAE legal transfer mixed with SaaS plan fact

The model separated the high-stakes UAE/Dubai cross-border personal-data compliance claim from the lower-stakes current plan-feature claim and preserved destination/jurisdiction/no-additional-measures qualifiers.

Semantic verdict: **PASS**.

### D3 — engineering rating with environmental qualifiers

The model retained continuous 10 A duty, sealed enclosure and 55 C ambient conditions in one high-stakes thermal/derating claim, separately from supplier price.

Semantic verdict: **PASS**.

### D4 — benchmark generalization plus API purchase

The model represented the attempted transfer from one English finance benchmark to an Arabic legal corpus and retained both language-transfer and domain-transfer qualifiers, separately from the commercial API decision.

Semantic verdict: **PASS**.

### D5 — conditional safety deployment

The model separated current firmware validation from the high-stakes conditional action to skip vendor inspection and deploy tonight. It preserved the condition, immediate timing and inspection omission.

Semantic verdict: **PASS**.

## Final adjudication

**PASS 5/5, P0=0.**

This is evidence on a small adversarial set, not proof of universal decomposition completeness. The deterministic completeness contract remains necessary as a backstop, and hidden holdouts should remain outside the searchable repository before future release tests.

## Operational evidence

Attempt 1 returned HTTP 503 high demand before any behavioral result. The single protocol-allowed retry succeeded. Capacity failure remains an operational/provider-health signal and must not be scored as a semantic failure.
