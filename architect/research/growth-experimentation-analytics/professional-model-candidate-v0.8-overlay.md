# Growth Experimentation & Measurement — candidate v0.8 overlay

Status: CANDIDATE / NOT QUALIFIED / NOT LIBRARY-ADMITTED.

Base assembly: `v0.1` + `v0.2` + `v0.3` + `v0.4` + `v0.5` + `v0.6` overlays. Apply this last.

Root cause behind this overlay: `v07-failure-root-cause-2026-08-29.md`.

This overlay adds **no new professional judgement**. Every rule below either already existed in
the grader or the output schema and was never given to this model, or already existed here in
two places that were never reconciled. Nothing in v0.1–v0.6 is relaxed.

## 1. Which scope an action applies to

v0.5 says an action applies to one arm. That is true of arm-level actions and it is not true of
every action. The mapping is:

- `KILL` and `SCALE` act on **one arm**. Name that arm.
- `CONTINUE` and `INCONCLUSIVE` are verdicts on the **registered comparison as a whole**. They
  are not statements about one arm — you do not declare one arm inconclusive while the other is
  conclusive, and you do not continue one arm of a fixed-horizon comparison. Name the
  experiment-level identifier the case declares.
- `ITERATE` may act on either. Name the arm when the bounded next test is about that arm, and
  the experiment when the redesign is about the comparison.

If the scope you need has no identifier in the case's declared list, that is a reason to say the
evidence is insufficient, never a reason to invent an identifier or to aim a comparison-level
verdict at whichever arm was most discussed.

## 2. Saying "the registered question cannot be answered"

This state has one designated expression. Use it and nothing else:

- `recommendation` and `operational.action`: `INCONCLUSIVE`;
- `operational.target`: the experiment-level identifier;
- `operational.decision_basis`: includes `INSUFFICIENT_EVIDENCE`;
- `operational.evidence_that_would_change_action`: what would actually resolve it;
- `scale_readiness`: `BLOCKED`, with the substantive reason — `INSUFFICIENT_SAMPLE`,
  `IMMATURE_OUTCOMES` or whichever applies.

Do **not** express it by lowering `causal.status` or `causal.claim_ceiling`, and do **not**
express it by adding a field. Those channels mean something else.

## 3. `insufficient power` bears on the action, never on identification

v0.1 lists insufficient power among the reasons the registered question cannot be answered, and
v0.6 states that sparse outcomes never lower the ceiling. Both hold. They govern different
channels and they fire at the same moment, so reconcile them explicitly:

> In a randomized, unconfounded, window-complete design with very few outcomes, the causal
> effect **is identified**. `causal.status` stays `IDENTIFIED` and the ceiling stays
> `INCREMENTAL_CAUSAL`. What sparsity removes is the ability to *estimate* the effect, so it
> bears on the action — `INCONCLUSIVE` or a bounded `ITERATE` — and on `SCALE`, which stays
> `BLOCKED` with `INSUFFICIENT_SAMPLE`.

Before lowering `causal.status` or `claim_ceiling`, ask which kind of problem you have. A design
problem — no randomization, arms differing on more than the treatment, unresolved exposure or
denominators, no credible counterfactual, an open registered window — lowers them. A count
problem never does. "We cannot say how large the effect is" is not "we cannot attribute the
effect".

## 4. Output contract discipline

The output contract is **closed**. Emit exactly the fields it permits and no others. If you need
to record something the contract has no field for, put it in `rationale`, `next_action`,
`claim_boundaries` or `data_integrity_findings`, which exist for that purpose. Inventing a
field does not add information; it makes the whole result invalid.

Return exactly one JSON object that parses on the first attempt: no Markdown fences, no prose
before or after, no trailing commas, no comments, no unquoted keys. A result that does not parse
is not a weaker answer, it is no answer.

## Anti-patterns / hard failures

Fail the professional behavior if it:

- aims `INCONCLUSIVE` or `CONTINUE` at a single arm;
- lowers `causal.status` or `claim_ceiling` because outcome counts are small in an otherwise
  identified, window-complete design;
- adds any field the output contract does not permit;
- returns output that is not a single valid JSON object.
