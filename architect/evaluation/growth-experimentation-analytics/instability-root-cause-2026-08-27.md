# Analytics v0.3 instability — root cause and repair, 2026-08-27

Question: one frozen candidate, one fixture, one grader produced different behavioral
results across runs. Why?

## Root cause

**Every qualified P0/P1 claim was asserted by regex over free prose, so a verdict was a
function of phrasing rather than of the decision.**

`schemas/result.schema.json` (contract v1) exposed exactly one structured decision field:
`recommendation`. Everything else the graders asserted — the causal ceiling, the refusal to
SCALE, which arm an action targets, reversibility, cost of waiting, whether downstream
economics drove the call — existed only inside `rationale`, `claim_boundaries`,
`next_action` and `confounders[].effect`. Ordinary sampling paraphrases those fields freely.
Semantically identical decisions therefore drifted in and out of regex range at random.

This was a known, documented deferral. The v0.3 overlay's own "Required decision record"
section says:

> "If the runtime schema lacks dedicated fields, encode these distinctly in claim
> boundaries/rationale/next action **until the schema is versioned**."

The schema was never versioned. Qualification proceeded on the prose fallback.

## Direct evidence, not inference

### The gate failed a correct decision

Run `32563283125`, job `97008067505`, fixture `H-DS-01`. The candidate returned
`recommendation: "KILL"`, the correct causal ceiling, the operational stop of B,
reversibility, and both required computations exactly. The grader failed it on one
assertion: `"missing continued-spend cost"`.

The candidate had stated the continued-spend cost twice:

- rationale: *"…real marginal spend to continue, no verified downstream-value offset…"*
- claim boundary: *"…based on mature observed economics, **real continued spend**, reversibility…"*

The pattern is `continued.{0,50}spend.{0,50}(?:cost|real)`. It requires `cost` or `real`
to appear **after** `spend`. The candidate wrote `real continued spend`. Word order, nothing
else, produced the FAIL. This is the run whose retry became the cited OpenAI qualification
PASS.

### The gate passed a sentence that asserts nothing

Same job, fixture `H-DS-02`, P0 assertion "refusal to SCALE from confounded evidence",
pattern `(?:not|cannot|does not).{0,100}scale`. It matched:

> "…does **not** override the registered requirement to use mature verified sales and gross
> profit for KILL/**SCALE** decisions."

That sentence refuses nothing; it is about which metric is decisive. The sentence that does
refuse — *"No SCALE recommendation is supported…"* — matches neither pattern, because `No`
is not in the alternation. So does *"Scaling is not justified"*, because `Scaling` does not
contain the substring `scale`.

The P0 SCALE gate was wrong in both directions: a false positive on an unrelated clause and
a false negative on the real refusal. `eval-integrity-and-regression.md` names both under
anti-gaming: "rubric keyword matching" and "correct final answer reached through invalid
evidence".

### Isolated measurement

One fixed decision, one fixed set of every other output element, varying only the sentence
expressing the cost of waiting:

| sentence | v0.3 grader | v0.4 grader |
|---|---|---|
| "Continued spend on B has a real cost." | PASS | PASS |
| "There is a real continued spend on B we would keep paying." | **FAIL** | PASS |
| "The cost of waiting for causal certainty exceeds its value." | PASS | PASS |
| "Real marginal spend to continue B, with no verified downstream-value offset." | **FAIL** | PASS |
| "B burns budget every day we wait for certainty." | **FAIL** | PASS |
| "Продолжение расходов на B имеет реальную стоимость." | **FAIL** | PASS |

v0.3: 2/6. v0.4: 6/6.

## Contributing factor, not the cause

`executor_gemini.py` and `executor_responses.py` pinned no sampling parameters, so prose
varied maximally between trials. `executor_groq.py` already used `temperature: 0`.

Sampling is now pinned where the provider supports it, but this is deliberately **not**
presented as the fix: temperature 0 would have suppressed the symptom while leaving a P0
gate that still passes an unrelated clause and still fails a correct answer phrased in
another language or word order. The measurement was broken independently of the variance.

## Repair

The responsible layer is the output contract, so that is what was repaired.

`schemas/result-v2.schema.json` adds a required `decision_record`:

- `causal.status`, `causal.claim_ceiling`, `causal.blocking_confounders` — the ceiling
  becomes a machine-checkable enum, and named blockers must also appear in `confounders[]`,
  so a ceiling cannot be asserted without identified evidence behind it;
- `operational.action` (must equal `recommendation`), `target`, `decision_basis` from a
  closed vocabulary, `reversible`, `evidence_that_would_change_action`;
- `scale_readiness.state` plus substantive `blocking_reasons` — the SCALE gate is now
  explicit and cannot be satisfied or defeated by a sentence.

These are decision content, not self-attestation flags. `causal.status: IDENTIFIED` on a
confounded design is the overclaim failure mode and fails. An action targeting arm B when
the justified action targets arm A fails. A `KILL` resting only on
`ACQUISITION_COST_DIAGNOSTIC` when mature downstream economics contradict it fails. Each is
discriminating in a way a prose regex was not.

The v0.4 overlay adds no new professional judgment and no latitude anywhere. Registered
estimand, denominator and identity integrity, delayed-outcome maturity, fixed-horizon
discipline, the causal-claim ceiling, the SCALE evidence bar and every v0.3 anti-pattern are
unchanged.

`candidate-freeze-v0.4.json` additionally binds the output contract into the frozen
assembly. Under v0.3 the freeze covered only the three markdown components while executors
injected the schema from a hardcoded path, so editing the contract could change candidate
behavior without changing the frozen digest.

## What was deliberately not done

The graders' regexes were not broadened. Widening
`continued.{0,50}spend.{0,50}(?:cost|real)` until the observed output passed would be
fitting the instrument to the answer, and would leave the next paraphrase to fail. The
assertions were moved to a surface where paraphrase is not a variable.

No fixture's expected professional answer was weakened. The contrastive half of the
regression exists to prove that: mutating the decision still fails.
