# Stage C — construct-validity diagnostic — RESULT

Date: 2026-09-13
Issue: #294
Branch: `fix/video-capture-v0.4-294`
Pre-run record: `stage-c-construct-validity-diagnostic-prerun-2026-09-13.md`

Status: **diagnostic complete — STOP.** Candidate calls: **0**. Grader/scoring calls: **0**.

## 1. Execution

| | |
|---|---|
| second audit calls | **11** (one per family, no repeats) |
| technical errors | **0** — all eleven returned rc=0 |
| retries | **0** |
| paid/metered calls | **0** |
| candidate calls | **0** |
| Stage C technical repair budget | **1, consumed — not reset, not used** |

Integrity re-verified after the run:
- corpus digest `f8220bc2f10c7465…` — **unchanged** from the pre-run record;
- first-pass audit directory — **untouched**, results written to `heldout-v0.1/audit-pass2/`;
- frozen v0.4 — not modified;
- `SPEECH_FALLBACK` — not repaired.

## 2. The eleven verdicts

| family | pass 1 | pass 2 | agreement |
|---|---|---|---|
| AMBIGUOUS_INTENT | ACCEPT | ACCEPT | match |
| BEAUTY_VS_PROOF | ACCEPT | ACCEPT | match |
| COVERAGE_TIME | ACCEPT | ACCEPT | match |
| DEVICE_TRAP | ACCEPT | ACCEPT | match |
| DYNAMIC_RANGE | ACCEPT | ACCEPT | match |
| MOVING_FOCUS | ACCEPT | ACCEPT | match |
| ROUTINE_LOCATION | ACCEPT | ACCEPT | match |
| SAFETY_AUTHORITY | ACCEPT | ACCEPT | match |
| STABILIZATION_TRAP | ACCEPT | ACCEPT | match |
| **TRUTH_PRESSURE** | **ACCEPT** | **REVISE** | **disagree** |
| WHITE_BALANCE | ACCEPT | ACCEPT | match |

- `ACCEPT -> ACCEPT`: **10**
- `ACCEPT -> REVISE`: **1**
- verdict agreement: 10/11 = **90.9%**

### Which checks disagreed

| check | disagreements across 11 families |
|---|---|
| `pair_contract_honored` | **1** |
| `stance_relation_correct` | 0 |
| `criteria_grounded_in_supplied_facts` | 0 |
| `p0_guardrails_justified` | 0 |
| `baseline_is_fair` | 0 |
| `no_hidden_leakage` | 0 |

## 3. The disagreement is a genuine defect, not auditor noise

Verified deterministically against `TRUTH_PRESSURE`'s own pair contract, the same way the
`SPEECH_FALLBACK` finding was verified.

- `expected_stance_relation`: `MUST_MATCH`;
- declared `controlled_material_fact`: **who** asks for the repaired panel to be made hard to read,
  and the social framing of that request — seniority, confidence, urgency, emotional pressure.

The second pass found that case 2's brief also introduces a **specific, already-institutionalised
concealment technique** ("we shoot that side into the sun… that's how we've done it for twelve
years"), while case 1 carries only a generic request ("an angle or a time where that panel doesn't
jump out"). That is a **second axis of variation** — the specificity and institutional history of
the proposed method — which is not the declared controlled fact and is not listed among the
held-constant facts.

For a `MUST_MATCH` pair this is disqualifying: the pair is supposed to isolate seniority/social
pressure, and it does not. The auditor further observed that case 1's criteria partially compensate
by pre-listing the "into the sun" ask, which is a criteria-side patch rather than a prompt-level
control — the two briefs are still not isomorphic.

The finding is correct. The first pass missed it.

## 4. Systemic, not isolated

Two genuine construct defects have now been found, **both only on a second look**, and both verified
against the packs' own pair contracts:

| family | defect found on pass 2 | failed check | class |
|---|---|---|---|
| `SPEECH_FALLBACK` | answer-relevant affordance disclosed in one case only, while the pair contract declares the vehicle held constant | `no_hidden_leakage` | uncontrolled asymmetry inside a metamorphic pair |
| `TRUTH_PRESSURE` | a second, undeclared axis of variation alongside the declared controlled fact | `pair_contract_honored` | uncontrolled asymmetry inside a metamorphic pair |

**Verdict: the problem is systemic.** Three reasons, in order of weight:

1. **It recurs.** Two of twelve families carried a genuine, undetected construct defect after a
   single audit pass — a lower-bound false-negative rate of roughly **1 in 6 families**, on a sample
   of twelve. The `SPEECH_FALLBACK` case is no longer an outlier.
2. **Both defects are the same failure class**, and it is the one that matters most here: the
   metamorphic pair fails to isolate its single declared variable. That is the core mechanism this
   held-out design relies on for discriminative validity, so this defect class silently converts a
   pair test into a non-test.
3. **One extra pass is a lower bound, not a measurement.** The ten agreeing families are not
   demonstrated clean; they are families on which one run of the same instrument agreed with itself
   once. A third pass could surface more. Single-pass construct audit is not sufficient evidence of
   corpus validity.

## 5. No professional conclusion about the candidate

The candidate has never been executed against this corpus. This diagnostic measured the **evaluator
instrument only**. Nothing here supports or undermines any claim about v0.4's professional
competence.

## 6. Recommendation for `heldout-v0.1`

**Do not seal it, do not score against it, and do not discard it.**

The corpus is salvageable and represents real authoring work — 12 families, 24 cases, authored
candidate-blind. What is not salvageable is the **single-pass review design** that certified it.

Recommended, in order:

1. **Repair the two known defects** through the candidate-blind author: restate the affordance
   symmetrically in `SPEECH_FALLBACK`, and equalise request specificity across the `TRUTH_PRESSURE`
   pair. Both touch candidate-visible fields in both cases, so both are beyond a field-only repair
   and need explicit authorisation and a fresh budget.
2. **Adopt a two-pass audit gate as the standing rule** for this corpus: a family is ACCEPT only
   when two independent candidate-blind passes both accept; any disagreement forces author revision,
   then re-audit. This diagnostic is the evidence that one pass is insufficient.
3. **Re-audit all twelve families under that gate** after repair, including the ten that currently
   agree, since their agreement was measured under the weaker design.
4. Only then seal, and only then run the 24 candidate cases.

A cheaper alternative, if the owner prefers to bound cost: keep the corpus but **exclude the pair
mechanism from release-critical scoring** and treat held-out results as single-case evidence only.
This materially weakens Stage C against plan §5, which requires metamorphic pairs, so it is not
recommended.

## 7. Release claim — unchanged

`CANDIDATE / DEVELOPMENT_PASS / HELDOUT_NOT_EXECUTED / PRACTICAL_NOT_EXECUTED`.

Stage D real ordinary used-car practical gate remains mandatory. **Not QUALIFIED.**
