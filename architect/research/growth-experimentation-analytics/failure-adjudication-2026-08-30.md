# Analytics — adjudication of the external held-out failures, 2026-08-30

Evidence: run `33293694601`, artifact `9727031366`, ledger recorded in
`architect/evaluation/growth-experimentation-analytics/external/external-gate-result-2026-08-30.md`.
Candidate under review: `professional-model-consolidated-v1.0.md`, blob `828baa78`,
assembly digest `sha256:3f4f3e13…d63d`.

No provider calls were made for this adjudication. Every finding below is derived from the merged
ledger and from the candidate document itself.

**Fact / Inference / Hypothesis are labelled separately throughout, per issue #196 §2.**

---

## The finding that reframes the whole cycle

**FACT.** Every rule that classes A, B and C violated is already written in consolidated v1.0, in
normative form, at the point where it fires.

| Class | Observed failure | Where v1.0 already forbids it |
|---|---|---|
| A | `CONTINUE`/`INCONCLUSIVE` aimed at one arm | §5.9 scope table, and the sentence "`CONTINUE` and `INCONCLUSIVE` are not statements about one arm" |
| A | target = the fixture id | §6.2 `target` — "exactly one string taken from the case's declared `arms` list" |
| B | `INCONCLUSIVE` without `INSUFFICIENT_EVIDENCE` | §5.9 designated expression: "`operational.decision_basis`: includes `INSUFFICIENT_EVIDENCE`" |
| B | `KILL` on cost-of-waiting grounds without `COST_OF_WAITING` | §6.2 `decision_basis` — "Record every ground that bore on the action, not only the strongest" |
| C1 | `INCONCLUSIVE`/`NONE_DECIDABLE` despite mature downstream economics | §5.9 — "MUST NOT be used as a universal action-paralysis label" |
| C2 | sparsity lowering `status`/`claim_ceiling` | §5.3 and §6.2 — "Sparse outcome counts never lower it" |

**INFERENCE.** This is therefore **not** a cycle in which the professional model is missing
content and needs more of it. Restating these rules more forcefully would be patch-by-test-string
in prose form, and issue #196 §3 forbids exactly that. The repair must address *why correct,
present rules did not fire*, which is a different defect class.

**FACT.** The same frozen candidate scored 0 Tier 1 failures in 70 trials on the evaluator's own
generated suite (run `33264418604`) and 15 Tier 1 failures in 69 measured trials on the externally
authored suite. The rules were byte-identical across both. What differed was the surface: business
domain, metric names, and arm identifiers.

---

## Class A — the experiment-level identifier. **Adjudicated: the candidate is at fault, and there
is a genuine knowledge gap.**

Issue #196 requires this class be adjudicated independently of the external oracle, neither copying
its assertion because it failed nor relaxing it because it failed. The adjudication does not need
the oracle at all: the candidate's own document settles it.

**FACT.** §5.9 of consolidated v1.0 contains this table:

| Action | Scope | Name |
| --- | --- | --- |
| `CONTINUE` | the registered comparison as a whole | the experiment-level identifier |
| `INCONCLUSIVE` | the registered comparison as a whole | the experiment-level identifier |

followed by: "`CONTINUE` and `INCONCLUSIVE` are not statements about one arm — you do not declare
one arm inconclusive while the other is conclusive, and you do not continue one arm of a
fixed-horizon comparison."

**FACT.** The external oracle asserted precisely this and nothing more. It is not a stricter rule
invented by the evaluator; it is the candidate's own invariant.

**INFERENCE.** The professional question is therefore settled in the oracle's favour, and it is
settled on independent grounds. The rule is also correct on its merits: at an incomplete fixed
horizon, continuing *one arm* of a two-arm comparison is not "continuing the experiment" — it is
an unregistered change to the design, which is the same error as early stopping wearing different
clothes. Declaring one arm inconclusive while the other stands is incoherent for the same reason:
the registered estimand is a contrast, and a contrast cannot be inconclusive on one side only.

**FACT — the actual gap.** The document says *what* to name. It nowhere says *how to recognise
which of the declared identifiers is the experiment-level one.* In every case the evaluator's
generator produced, that identifier was the literal string `experiment`, so recognition was free
and the gap was invisible. The external author named it `ui_experiment`, `pricing_test`,
`sort_algorithm_test` and `onboarding_experience_test`.

**FACT.** On `EX-03-02` the candidate named the treatment arm `ui_refresh` for `CONTINUE` in five
of seven trials and named the fixture id `EX-03-02` in the other two — 0/7. On `EX-03-01`, same
family, it scored 6/7. Across `EX-05-01`/`EX-05-02` it aimed `INCONCLUSIVE` at a treatment arm in
three trials.

**INFERENCE.** This is a Phase 4 defect in the precise sense SKILL.md gives it: the knowledge
existed in the oracle — which knows the scope identifier by construction — and in the evaluator's
naming convention, but was never made available to the candidate at runtime. Knowledge in a grader
is not knowledge the candidate holds.

**FACT — the recognition rule is available in the case itself, without vocabulary.** In every
fixture of both suites, each declared identifier that denotes an arm also keys a per-arm outcome
block inside `case`; the comparison-level identifier keys nothing. Verified against both suites:

| Suite | `arms` | keyed blocks | unkeyed |
|---|---|---|---|
| generator | `configuration_a, configuration_b, experiment` | the two configurations | `experiment` |
| external | `legacy_ui, ui_experiment, ui_refresh` | `legacy_ui`, `ui_refresh` | `ui_experiment` |
| external | `bundle_off, price_opt, pricing_test` | `bundle_off`, `price_opt` | `pricing_test` |

**INFERENCE.** "The declared identifier that carries no per-arm outcome block is the comparison as
a whole; those that carry one are its arms" is a structural rule, independent of every word used to
name anything. It is also professionally correct rather than a parsing trick: an identifier with no
measurements attached to it is not a thing that was measured, so it cannot be an arm.

**Repair (class A):** encode that recognition procedure in §5.9, together with the explicit
statement that the `fixture_id` is not an arm and is never a legal target. Additive; nothing is
relaxed.

**HYPOTHESIS, not acted on.** The candidate may be treating `CONTINUE` as "keep spending on the
arm that is winning", which would be an early-stopping error rather than a naming error. The
ledger cannot separate the two, because both produce the same observable. The recognition rule
repairs the observable either way, and the fixed-horizon rule that forbids the underlying error is
already present and already tested. Recorded, not designed around.

---

## Class B — incomplete decision grounds. **Adjudicated: substantive, not cosmetic.**

**FACT.** Two trials: `EX-02-02` t7 omitted `COST_OF_WAITING`; `EX-05-01` t3 omitted
`INSUFFICIENT_EVIDENCE`. Both actions were otherwise correct.

**INFERENCE.** These are substantive. `decision_basis` is the record of *why* an action was taken,
and §6.2 requires "every ground that bore on the action, not only the strongest". A `KILL` that
rests on continued spend having real marginal cost, recorded without `COST_OF_WAITING`, is a
decision whose stated grounds do not support it — a reviewer reading the record cannot reconstruct
why stopping was justified rather than waiting. For `INCONCLUSIVE`, §5.9 does not merely recommend
`INSUFFICIENT_EVIDENCE`, it makes it part of the designated expression; omitting it produces an
`INCONCLUSIVE` that is indistinguishable from decision paralysis, which is the failure mode C1.

**Repair (class B):** the rules are correct and present. What is missing is that they are never
gathered where the candidate checks its work. See the common repair below.

---

## Class C — the two P0 errors. **Adjudicated: confirmed, not disputed.**

**FACT.** `EX-01-02` t1 returned `INCONCLUSIVE` with `decisive_metric: NONE_DECIDABLE` on a
completed comparison whose verified mature gross profit separated the arms decisively.

**INFERENCE.** Direct violation of the dual-threshold rule (§4) and of §5.9's prohibition on
`INCONCLUSIVE` as an action-paralysis label. The causal question was legitimately unresolved — the
design was not randomised — but operational sufficiency was met and the operational channel had to
carry the action. Returning `NONE_DECIDABLE` while mature verified downstream economics are present
in the case is self-contradictory: a metric that selects the action was available.

**FACT.** `EX-05-02` t6 returned `causal.status: UNRESOLVED` and `claim_ceiling: NONE` on a
randomised, exposure-verified, window-complete design with single-digit outcome counts.

**INFERENCE.** Direct violation of the identification/precision separation (§5.3, §5.6). Thin
counts are a precision fact about the sample; identification is a property of the design. This is
the exact confusion the v0.6 overlay was written to prevent and which the `SPARSE_BUT_IDENTIFIED`
family exists to test in the loosening direction as well as the tightening one.

**Repair (class C):** as with B — the rules are present and correct.

---

## The common repair for B and C

**FACT.** §6.3 "Internal consistency" already exists and already lists conditions that make a
result *invalid rather than merely imperfect*. Every condition it lists today is structural:
field-to-field agreement, vocabulary membership, scope-versus-window coherence.

**FACT.** None of the couplings violated by classes A, B and C appears in that list, although each
is stated normatively elsewhere in the document.

**INFERENCE.** This is the mechanism of the failure. The candidate holds each rule as a statement
made once, in the section that discusses that topic, and has no point at which it checks the
assembled result against them. The structural couplings that *are* in §6.3 were satisfied in all 69
measured trials; the couplings that are not in §6.3 were violated 15 times. That correlation is the
evidence for the repair.

**Repair (common):** extend §6.3 from structural consistency to include the action–grounds
couplings that are already normative elsewhere in the document. Specifically, a result is invalid
when a comparison-level action names an arm; when `INCONCLUSIVE` omits `INSUFFICIENT_EVIDENCE`;
when `decisive_metric` is `NONE_DECIDABLE` although the case supplies verified mature downstream
economics that separate the arms; and when `status`/`claim_ceiling` are lowered on a design the
case declares randomised, exposure-verified and window-complete.

**This adds no new professional rule.** Each condition restates, in checkable form and in one
place, a rule §4, §5.3, §5.7 or §5.9 already asserts. The repair is where the rules live, not what
they say.

---

## Class D — structural reliability

**FACT.** 8 Tier 2 of 70: five outputs that failed to parse, three that placed `scale_readiness`
inside `decision_record.operational` instead of `decision_record`. The v1.0 internal gate recorded
6/70 of this class; the preregistered total cap is 6.

**FACT.** The parse errors are `Expecting property name enclosed in double quotes` at char ~2749,
~2806, ~2866, ~3066 and `Expecting value` at char ~1424 — malformations inside a generated object,
not a truncated HTTP body. The transport delivered a complete response in all five cases; the
apparatus classified them TIER2, not INVALID, and that classification is correct.

**INFERENCE.** Candidate/runtime-contract discipline, not provider transport — which is the
determination issue #196 §D asks for. The `scale_readiness` misplacement is unambiguous: §6.2
declares it a sibling of `causal` and `operational` under `decision_record`, and nesting it one
level deeper is a contract violation the document never names as invalid.

**Repair (class D):** name the nesting violation in §6.3, and constrain prose-field length in §6.1.
The length constraint is the honest part of the fix and its expected effect is partial: every
malformation occurred deep in a long object, and shorter prose fields reduce the surface on which
that happens. It is not claimed to eliminate the class.

**HYPOTHESIS, recorded and not acted on.** The remaining parse failures may be irreducible at this
model/temperature. If so the Tier 2 cap, not the candidate, is the thing that eventually needs
review — but changing a threshold in the cycle whose result exposed it would be fitting the
criterion to the outcome, and the criterion is therefore left exactly as preregistered.

---

## What must not be repaired

**Preserved unchanged**, per issue #196 and verified mechanically by the successor's equivalence
test: the causal-versus-operational dual threshold; downstream-over-proxy precedence; fixed-horizon
discipline; the SCALE gate; the sparsity-versus-identification distinction; commercial-truth and
authority boundaries; every P0/P1 constraint; the closed output contract; and all thirteen
invariants of §3.

**Not touched at all**: the external held-out pack, its sealed oracle, the tier map, the grader,
the thresholds, the hard-fails, and every historical ledger. Run `33293694601` remains INVALID.

---

## Scope of the successor

One consolidated successor, `professional-model-consolidated-v1.1.md`, differing from v1.0 in four
localized, additive places:

1. **§5.9** — the recognition procedure for the comparison-level identifier, and the explicit
   exclusion of the fixture id. *New normative content; the one genuine knowledge gap.*
2. **§6.3** — the action–grounds couplings, restated as invalidity conditions. *No new rule.*
3. **§6.3** — `scale_readiness` nesting named as invalid. *No new rule.*
4. **§6.1** — prose-field brevity. *New constraint, tightening.*

No overlay. No new document beyond the successor itself. Every change is additive or tightening;
none removes, weakens or re-scopes any v1.0 rule, and a deterministic test proves it.
