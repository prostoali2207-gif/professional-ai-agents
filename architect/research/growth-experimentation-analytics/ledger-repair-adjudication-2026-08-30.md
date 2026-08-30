# Analytics v1.2 — adjudication of the remaining blocker, 2026-08-30

Evidence: run `33299723985`, artifact `9728699042`, ledger recorded in
`architect/evaluation/growth-experimentation-analytics/external/external-gate-result-v1.1-2026-08-30.md`.
Candidate under review: `professional-model-consolidated-v1.1.md`,
assembly digest `sha256:3c83f266…9081`.

No provider calls were made for this adjudication. **Fact / Inference / Hypothesis are labelled
separately**, per the discipline the previous adjudication used.

---

## 1. What the v1.1 cycle actually established about repair method

**FACT.** The v1.1 repair made two structurally different changes and the clean 70-trial run
separated them:

| Repair | Kind | Observed |
|---|---|---|
| §5.9 recognition procedure for the comparison-level identifier | **new procedure** the candidate did not previously hold | class went **11 → 0** |
| §6.3 couplings for classes B and C | **no new rule** — existing rules restated as emit-time invalidity conditions | those classes went **4 → 6** |

**FACT.** v1.1 states the sparsity-versus-identification rule in three separate places, each
unambiguous: §5.3 ("Sample sparsity is a precision problem, not an identification problem… the
causal effect **is identified**"), §5.6 ("Sparse outcomes never lower the ceiling"), and §6.3 (as
an invalidity condition). The candidate still returned `causal.status: UNRESOLVED` with
`claim_ceiling: NONE` on a randomised, exposure-verified, window-complete design in four trials.

**INFERENCE.** A fourth statement of the same rule is the one repair the evidence positively
predicts will not work. Issue #205 §2 reaches the same conclusion independently. The repair must
be a procedure.

**INFERENCE — why a statement is not enough here.** §5.3 ends by telling the analyst to "ask which
kind of problem you have". That is an invitation to reflect, and it fires at a point in the
procedure where the counts have already been read: §5.1 validates the packet, §5.2 audits
integrity, §5.3 looks at sample and power, §5.4 computes, and only §5.6 writes the ceiling. By then
the thin counts are in view, and "we can't conclude anything" is the frame they invite. The rule
is competing with the reading order and losing.

## 2. The procedure

**The repair is to move the decision, not to repeat it.** The causal channel is determined at the
point where design facts are established — the end of §5.2, immediately after the integrity audit —
and is closed before any outcome count is read.

Five questions, each answerable from a declared field, each phrased as a **defect check**:
assignment, exposure/instrumentation, comparability, confounding, window. Then a decision table
from the answers, then the closure rule: *no count turns a no on questions 1–4 into a yes, because
not one of those questions is about counts.*

**FACT — the phrasing matters and was chosen deliberately.** The questions ask whether the case
*declares* a defect, not whether it declares soundness. A case that simply omits
`exposure_verified` has not declared an exposure defect. Phrased the other way round, the
`IMMATURE_FIXED_HORIZON` family — which declares randomisation and no confounding but says nothing
about exposure — would have been forced to `UNRESOLVED`, and that family currently passes 6/7 and
6/7. A repair that broke it would have traded one failure class for another.

**FACT.** The ledger reproduces the frozen oracle's causal expectations on all five families,
across five seeds and on externally authored vocabulary, verified in
`test_identification_ledger_regression_v12.py`. It was not fitted to them: it reads
`design.randomized_split`, declared defect fields, and `registered_window_complete`, and nothing
else.

## 3. The two residual failures, and why the same procedure covers them

Issue #205 §4 permits addressing them **only if the same root cause explains them**. It does.

**FACT.** `EX-05-01` trial 6 omitted `INSUFFICIENT_EVIDENCE` from `decision_basis`; three of the
four sparsity trials also omitted `INSUFFICIENT_SAMPLE` from `scale_readiness`.

**INFERENCE.** These are the other half of the same mistake. A candidate that has just written the
sparsity into the causal channel has already "expressed" it, and has nothing left to put in the
action channel. The ledger's closing clause names the four fields sparsity is allowed to touch and
says that is the whole of what it may change — so the expression has exactly one home and it is
enumerated.

**FACT.** `EX-02-01` trial 4 returned `INCONCLUSIVE` with `decisive_metric: NONE_DECIDABLE` on the
confounded family, where the acquisition-cost metric selected `KILL`.

**INFERENCE.** Also a channel-separation failure, in the opposite direction: the unresolved causal
verdict was allowed to write the action. The second half of the addition — *the action is decided
separately, and never inherited* — forbids both directions explicitly, with `NONE_DECIDABLE`
called out as false rather than cautious when the case supplies a deciding metric.

**No fixture-specific rule was added.** One procedure, two clauses, three failure modes.

## 4. What is preserved

**Verified mechanically**, not asserted: every non-blank line of v1.1 appears verbatim in v1.2
except the title. The v1.0 containment is rechecked transitively, the 118-entry v1.0 register with
its hedge detector and invalidity checks is re-run, and both v1.1 gains — the vocabulary-independent
scope recognition and the §6.3 couplings — are asserted intact. Downstream-over-proxy precedence,
fixed-horizon discipline, the dual threshold, the SCALE gate, output-contract discipline and the
commercial-truth boundaries are untouched.

The grader, tier map, thresholds and criterion are untouched, as issue #205 requires.

## 5. Residual risk, stated

**HYPOTHESIS, not acted on.** The ledger relocates the decision, but the candidate is still a
language model reading a document in order. If it skips ahead, or reconstructs the causal channel
at §5.6 from what it has since seen rather than from what it recorded, the failure can recur. The
closure clause is written to be self-checking against exactly that ("if your causal channel changed
after you saw the numbers… return to what you recorded"), but a self-check is weaker than a
mechanical constraint, and this document cannot impose a mechanical one on a free-text runtime.

**HYPOTHESIS.** The v1.1 failure was fixture-specific — `EX-05-01` scored 2/7 while `EX-05-02`
scored 7/7 on the same family. Whatever distinguished them is not visible in the failure text and
the pack is sealed, so the ledger is aimed at the failure mode rather than at whatever made one
case harder. If the distinguishing feature is something the ledger does not read, the repair may
not transfer. That is a real limit on what this cycle can promise, and it is why the gate is the
test rather than the argument.
