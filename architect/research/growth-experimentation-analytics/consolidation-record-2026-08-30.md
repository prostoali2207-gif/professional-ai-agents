# Analytics consolidation record — v0.1–v0.8 → consolidated v1.0

Date: 2026-08-30. Authority: `architect/SKILL.md` Phase 13 (`FAIL -> classify -> root cause ->
repair responsible layer -> regression test`), Phase 4 (knowledge must be proven available at
runtime), Phase 5 (a principle carries its applicability conditions), Phase 6A (resource cost of
a material assembly), Phase 12 (the assembled artifact orchestrates rather than accumulates).

This record is **not** part of the runtime document. It exists so the consolidation is auditable
without reading eight superseded files.

## 1. Why consolidate rather than add v0.9

Gate `33243263001` (v0.8, seed 20260830, Gemini, 3 trials, 0 retries) returned 28/30 with a FAIL
verdict on discordance. Harness defects 0, provider defects 0. Two residual losses:

- `HO-IFH-02` trial 2 — `decision_basis must record REGISTERED_PRIMARY_KPI`;
- `HO-SBI-02` trial 2 — malformed JSON from the model, surfaced as `EXECUTION_ERROR`.

Neither is a gap in professional judgement. Both are expression failures on a candidate assembled
from seven documents written across six cycles. The `REGISTERED_PRIMARY_KPI` loss is the **same
defect class as the v0.8 root cause**: the v0.4 overlay introduced `decision_basis` and enumerated
four of its ten permitted values, omitting the one the frozen oracle most often requires. The rule
lived in the schema and the oracle and was never mirrored into the candidate — exactly what Phase
4 forbids.

An eighth overlay would have added an eighth place for the next rule to be half-stated. The
preregistered stop condition for v0.8 anticipated this and named consolidation as the response.

Assembly size before: 606 lines / 5133 words across 7 files. After: 538 lines / 4429 words in one
file — 14% fewer words, while **adding** 21 previously undocumented closed-vocabulary members
(§5). The saving is bookkeeping, provenance and restatement; the additions are rules the candidate
was missing. Size was never the objective and the gain is modest: coherence is the objective, and
§2–§5 below account for every rule and where it went.

## 2. Duplicates removed

| # | Rule | Stated in | Kept as |
| --- | --- | --- | --- |
| D1 | Sparse outcomes never lower the causal ceiling | v0.6 §"Sparse outcomes…", v0.8 §3 | §5.6 (identification side) + §5.3 (action side). Two statements survive **by design** because the rule fires in two channels; each names the other. This is the reconciliation, not a duplicate. |
| D2 | Anti-pattern "lowers ceiling because counts are small" | v0.6 anti-patterns, v0.8 anti-patterns | §7, once |
| D3 | Registered-estimand preservation | v0.2 invariant, v0.6 back-reference | Invariant 2, once |
| D4 | "SCALE safeguards are unchanged / not weakened" | v0.4, v0.5, v0.6 | §5.8. These were change notes about overlays, not rules; the rule is the SCALE gate itself. |
| D5 | Scale readiness is evaluated independently of the action | v0.4 `scale_readiness`, v0.4 prose | §5.8, once, with the contract field pointing at it |
| D6 | `target` must be one declared identifier, not a phrase | v0.5 contract v3, v0.5 anti-patterns | §6.2 `target` + §6.3 + §7 anti-pattern (contract, validity rule, failure mode — three roles, not three copies) |
| D7 | Overlay bookkeeping — "Base assembly: … Apply this overlay last", "Status: CANDIDATE", "Qualification consequence", per-overlay repair-scope narratives | all six overlays | Removed from runtime. Status kept once at the head; qualification obligations kept once in §9. |
| D8 | Incident forensics — the H-GDS-02 arm figures (v0.5), the v0.7 run/seed analysis (v0.8), the v0.3 incident narrative | v0.3, v0.5, v0.8 | Removed from runtime; they are derivation, not rule. The **rationale** each carried is load-bearing and is retained: the early-vs-late-converter bias argument (§5.6), the diagnostic-vs-decisive classification (§5.7), the confounder-action-relevance test (§5.9). |

## 3. Conflicts resolved

**C1 — action scope. v0.5 vs v0.8.**
v0.5 contract v3: *"an action applies to one arm"*, with the whole-experiment case as a
conditional afterthought. v0.8 §1: `KILL`/`SCALE` act on one arm, `CONTINUE`/`INCONCLUSIVE` are
verdicts on the comparison, `ITERATE` may be either. These are in direct conflict for three of the
five actions, and the v0.5 formulation is the one that misled the v0.7 gate.
**Resolved:** the v0.8 mapping is normative and is stated once as a table in §5.9. The v0.5
sentence is not carried forward in the form that conflicts; its surviving content — that a target
is exactly one structural identifier — is in §6.2, where it never conflicted.
**Direction of the resolution: stricter.** The table constrains every action; the old text
constrained one shape of action and left three unspecified.

**C2 — insufficient power. v0.1 vs v0.6.**
v0.1 §8 lists *"insufficient power"* among the reasons the registered question cannot be answered.
v0.6 states that sparse outcomes never lower the causal ceiling. Both are correct and they govern
different channels, but they sat five overlays apart with no cross-reference and fire at the same
moment. Carrying "insufficient power" into the identification channel was the v0.7 P0.
**Resolved:** both statements are kept, and the reconciliation is written at **both** points where
they fire — §5.3 (power/maturity) and §5.9 (the `INCONCLUSIVE` definition, inline at the exact
phrase "insufficient power"), each pointing at the other. Neither rule is weakened.

**C3 — `INCONCLUSIVE`: verdict or paralysis. v0.1 vs v0.3 vs v0.8.**
v0.1 defines `INCONCLUSIVE` as a legitimate verdict; v0.3 warns it must not become a universal
action-paralysis label and says to prefer the justified operational recommendation; v0.8 §2 gives
the single designated expression for genuinely unanswerable. Three partial statements of one rule.
**Resolved:** §5.9 states the verdict, the anti-paralysis constraint and the designated expression
in sequence, and invariant 13 points at §5.9 rather than restating it.

**C4 — where non-contract content goes. v0.3 vs v0.4.**
v0.3: *"If the runtime schema lacks dedicated fields, encode these distinctly in claim
boundaries/rationale/next action **until the schema is versioned**."* v0.4 §"Output contract v2"
explicitly closes that deferral; v0.8 §4 says the contract is closed and names the same prose
fields as the place for surplus narrative.
**Resolved:** see D9 below — the deferral is dead and removed; the closed-contract rule with the
same named prose fields is stated once in §6.1.

## 4. Dead dependencies removed

| # | Dead text | Why it is dead |
| --- | --- | --- |
| D9 | v0.3: "until the schema is versioned" | The schema **was** versioned: result-v2 (v0.4) → v3 (v0.5) → v4 (v0.6). The instruction now invites encoding decision-record content as prose, which is the exact v0.3→v0.4 failure mode. Removed. |
| D10 | v0.4: "alongside — not instead of — the existing prose fields" framed as a transition from a prose-only regime | The prose-only regime no longer exists. The surviving rule — prose fields are the human account, `decision_record` is the decision — is in §6.1 as a standing rule, not a migration note. |
| D11 | v0.4 §"What this overlay does not change", v0.5/v0.6/v0.8 equivalents | Statements about what an overlay did to a prior overlay. Meaningless in a single document; the referenced rules are all present on their own. |
| D12 | Every "Base assembly: v0.1 + v0.2-overlay + … Apply this overlay last" | There is one document; there is no application order. |

## 5. Gaps closed — closed vocabularies that existed only in the instrument

These are the residual-failure repairs. None adds professional judgement: every value below is
already in the frozen output contract `result-v4.schema.json` and already enforced by the frozen
grader. The candidate was simply never told they exist.

| Vocabulary | Members in the frozen contract | Members documented in v0.1–v0.8 | Now |
| --- | --- | --- | --- |
| `operational.decision_basis` | 10 | **4** (v0.4 named `COST_OF_WAITING`, `MATURE_DOWNSTREAM_ECONOMICS`, `ACQUISITION_COST_DIAGNOSTIC`, `INSUFFICIENT_EVIDENCE`) | all 10, §6.2, each with the condition that triggers it |
| `operational.decisive_metric` | 6 | **0** (v0.5 said "from the closed vocabulary" and never listed it) | all 6, §6.2 |
| `scale_readiness.blocking_reasons` | 8 | **0** (v0.4 said "from the closed vocabulary" and never listed it) | all 8, §6.2 |
| `causal.status` | 3 | **2** (`NOT_APPLICABLE` never mentioned) | all 3, §6.2 |

`REGISTERED_PRIMARY_KPI` is the member whose absence closed gate 33243263001. Its trigger
condition in §6.2 is read from rules the assembly already contained — invariant 1
(pre-registration integrity), invariant 2 (registered-estimand preservation), and the `SCALE` /
`CONTINUE` / `KILL` definitions in §5.9, all of which turn on the registered success rule, the
registered failure rule, or the completeness of the registered collection window. No frozen
family's expectation changes as a result: the oracle already required this value on
`IMMATURE_FIXED_HORIZON` and `CLEAN_SCALABLE_WIN`, and still does.

`NOT_APPLICABLE` is documented for completeness of the closed vocabulary. No family in the frozen
generator uses it, so documenting it cannot change graded behavior on the frozen oracle.

## 6. Malformed JSON

The rule was already correct and complete in v0.8 §4 and is carried forward verbatim into §6.1.
Consolidation changes only its **position**: it is now the first paragraph of the output contract
rather than the fourth subsection of the seventh document. Position is not semantics, and no claim
is made here that repositioning fixes the failure — only a gate can show that.

One observation is recorded rather than acted on: a model that emits unparseable JSON currently
surfaces as `EXECUTION_ERROR` (the executor exits 2) rather than `FAIL`, because the executor
parses before the runner does. Both are non-`PASS` and neither can be mistaken for a pass, so no
gate is weakened by it — but the label attributes a candidate defect to the infrastructure. The
instrument was **not** changed here: this cycle's mandate is consolidation, the instrument is
frozen, and `run_heldout_gate_v07.py` already grades a non-JSON body reaching it as `FAIL`. The
regression added in `test_consolidation_residual_modes_v10.py` locks that malformed output is
never scored `PASS` in **either** channel. Whether to reclassify the executor's exit path is a
separate, instrument-scoped decision for a future cycle.

## 7. What was deliberately not done

- No professional rule was added, removed, relaxed or re-scoped.
- No threshold moved.
- The grader, generator, runner, output contract and fixture contract are byte-identical to those
  bound by freeze v0.8.
- The v0.1–v0.8 documents are untouched on disk; freeze v0.7 and v0.8 still verify against them.
- No provider call was made in this cycle.
