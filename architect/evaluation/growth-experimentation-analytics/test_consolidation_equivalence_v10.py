#!/usr/bin/env python3
"""Semantic-equivalence proof for the v0.1-v0.8 assembly -> consolidated v1.0.

What this proves, precisely:

  * **No rule lost.** Every normative rule in the superseded assembly is registered below with an
    anchor phrase, and each must be present in the consolidated document.
  * **No modality weakened.** Each registered rule carries the modality it had (PROHIBITION,
    REQUIREMENT, INVALIDITY, ANTIPATTERN). A rule that was a prohibition must still read as one;
    turning a MUST NOT into a "prefer not to" is the exact failure this guards.
  * **No gate loosened.** The SCALE gate, the causal ceiling, the registered-estimand rule, the
    stopping-rule discipline and the closed contract must all still be stated in their strict form.
  * **Vocabulary completeness.** Every member of every closed vocabulary in the FROZEN output
    contract must be documented in the consolidated candidate. This is the Phase 4 check that the
    v0.7 and v0.8 residual failures both violated: a value the grader enforces but the candidate
    was never told about.
  * **Nothing invented.** Every enum value named in the consolidated document must exist in the
    frozen contract, so consolidation cannot smuggle in a new vocabulary.
  * **Instrument untouched.** Grader, generator, runner, output contract and fixture contract are
    byte-identical to those bound by freeze v0.8.

What this does NOT prove, stated so it is not over-read: that the model now behaves correctly.
A document-level equivalence proof cannot establish runtime behavior. Only a fresh held-out gate
can, and none is run here.
"""

from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESEARCH = ROOT / "architect/research/growth-experimentation-analytics"

CONSOLIDATED = RESEARCH / "professional-model-consolidated-v1.0.md"
RECORD = RESEARCH / "consolidation-record-2026-08-30.md"
SUPERSEDED = [
    RESEARCH / "professional-model-candidate-v0.1.md",
    RESEARCH / "professional-model-candidate-v0.2-overlay.md",
    RESEARCH / "professional-model-candidate-v0.3-overlay.md",
    RESEARCH / "professional-model-candidate-v0.4-overlay.md",
    RESEARCH / "professional-model-candidate-v0.5-overlay.md",
    RESEARCH / "professional-model-candidate-v0.6-overlay.md",
    RESEARCH / "professional-model-candidate-v0.8-overlay.md",
]


def norm(text: str) -> str:
    """Whitespace-normalised so an assertion tests the rule, not the line wrap."""
    return " ".join(text.split())


CONSOLIDATED_TEXT = norm(CONSOLIDATED.read_text(encoding="utf-8"))


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True, cwd=ROOT).strip()


# --------------------------------------------------------------------------------------------
# The rule register.
#
# (rule_id, modality, source, anchor)  -- anchor is a phrase that carries the rule's operative
# content, taken from the superseded text wherever the wording survives. A rule whose anchor is
# absent from the consolidated document has been lost in consolidation.
# --------------------------------------------------------------------------------------------
REGISTER: list[tuple[str, str, str, str]] = [
    # --- v0.1 authority boundary: the seven prohibitions -------------------------------------
    ("AB-1", "PROHIBITION", "v0.1",
     "change the registered KPI, threshold, population, denominator, window or decision rule after seeing results"),
    ("AB-2", "PROHIBITION", "v0.1", "invent missing observations, business facts or statistical assumptions"),
    ("AB-3", "PROHIBITION", "v0.1", "treat missing/delayed/invalid data as zero"),
    ("AB-4", "PROHIBITION", "v0.1",
     "convert attribution into a causal incrementality claim without a valid counterfactual"),
    ("AB-5", "PROHIBITION", "v0.1", "rescue a failed primary result with post-hoc metrics or segments"),
    ("AB-6", "PROHIBITION", "v0.1",
     "make a scale decision from an upstream proxy when downstream guardrails or economics contradict"),
    ("AB-7", "PROHIBITION", "v0.1", "exceed the qualified computation/toolchain"),

    # --- v0.1 core invariants ----------------------------------------------------------------
    ("INV-1", "REQUIREMENT", "v0.1",
     "the primary question, KPI, population, threshold, test window and stopping rule stay frozen"),
    ("INV-3", "REQUIREMENT", "v0.1", "must be comparable enough for the intended claim"),
    ("INV-4", "REQUIREMENT", "v0.1",
     "every rate uses the eligible population that actually defines the quantity being estimated"),
    ("INV-5", "REQUIREMENT", "v0.1", "`NOT_APPLICABLE` are not interchangeable"),
    ("INV-6", "REQUIREMENT", "v0.1",
     "not treated as equivalent when definitions or measurement regimes differ"),
    ("INV-7", "REQUIREMENT", "v0.1", "favorable percentages alone do not justify a decision"),
    ("INV-8", "REQUIREMENT", "v0.1", "does not establish the counterfactual effect"),
    ("INV-9", "PROHIBITION", "v0.1", "cannot rewrite the original experiment verdict"),
    ("INV-10", "REQUIREMENT", "v0.1", "contamination defects can block a winner decision"),
    ("INV-11", "REQUIREMENT", "v0.1", "A positive effect is not automatically scalable"),
    ("INV-12", "REQUIREMENT", "v0.1",
     "it contributes `1` entity, so `n-1` records are duplicates. Do not subtract the whole cluster"),
    ("INV-12b", "REQUIREMENT", "v0.1",
     "bound the result or return `INCONCLUSIVE` rather than guessing"),
    ("INV-13", "REQUIREMENT", "v0.1", "weak or corrupted evidence is not forced into a win/loss label"),

    # --- v0.1 procedure ----------------------------------------------------------------------
    ("PR-1", "REQUIREMENT", "v0.1",
     "return `INCONCLUSIVE` or a pre-analysis block rather than filling it in after the fact"),
    ("PR-2", "REQUIREMENT", "v0.1", "distinguish at least assigned units, exposed units, and metric-observed units"),
    ("PR-2b", "PROHIBITION", "v0.1",
     "must not be silently treated as harmless variation at another"),
    ("PR-3", "REQUIREMENT", "v0.1",
     "treat them as immature/ right-censored rather than observed zeroes"),
    ("PR-4", "REQUIREMENT", "v0.1", "inputs; formula or named method; result; unit; assumptions/warnings"),
    ("PR-4b", "REQUIREMENT", "v0.1",
     "return a bounded/blocked result instead of fabricating a statistic"),
    ("PR-5", "PROHIBITION", "v0.1", "cannot replace the frozen primary KPI after results are seen"),
    ("PR-5b", "REQUIREMENT", "v0.1",
     "Post-hoc segments are exploratory unless a valid pre-specified inference procedure supports them"),
    ("PR-6", "REQUIREMENT", "v0.1",
     "report association and plausible alternatives rather than causal certainty"),
    ("PR-7", "REQUIREMENT", "v0.1",
     "An acquisition lift with materially worse downstream handling is not unrestricted scale evidence"),
    ("PR-8-SCALE", "REQUIREMENT", "v0.1",
     "registered success rule is met, evidence is mature enough, guardrails pass, integrity is adequate"),
    ("PR-8-CONTINUE", "REQUIREMENT", "v0.1",
     "more observation can resolve uncertainty without violating the stopping rule"),
    ("PR-8-ITERATE", "REQUIREMENT", "v0.1",
     "bounded mechanism, execution or measurement defect where one controlled change is justified"),
    ("PR-8-KILL", "REQUIREMENT", "v0.1",
     "meets the registered failure rule, violates a material guardrail, repeatedly fails"),
    ("PR-8-INCONCLUSIVE", "REQUIREMENT", "v0.1",
     "missing/immature data, insufficient power, invalid comparison, instrumentation failure"),

    # --- v0.1 knowledge/runtime + qualification ----------------------------------------------
    ("KR-1", "REQUIREMENT", "v0.1", "Embed only stable professional rules in the future core"),
    ("KR-2", "REQUIREMENT", "v0.1",
     "Escalate rather than improvise when assumptions or methods exceed the supported boundary"),
    ("QL-1", "REQUIREMENT", "v0.1", "Until then the only valid status is `CANDIDATE / NOT QUALIFIED`"),
    ("QL-2", "REQUIREMENT", "v0.1", "failures are repaired without teaching to fixture wording"),
    ("QL-3", "REQUIREMENT", "v0.1",
     "passes held-out qualification without repair from held-out answers"),

    # --- v0.2 registered-estimand preservation -----------------------------------------------
    ("RE-1", "REQUIREMENT", "v0.2",
     "remains the official primary estimand for that experiment unless a valid pre-specified amendment procedure"),
    ("RE-2", "PROHIBITION", "v0.2",
     "do **not** replace it with an alternative denominator, metric or estimand and call that replacement the primary result"),
    ("RE-3", "PROHIBITION", "v0.2",
     "do **not** reinterpret a diagnostic, ITT, per-exposed, per-assigned, per-observed, proxy or sensitivity calculation as the registered KPI"),
    ("RE-4", "REQUIREMENT", "v0.2",
     "use alternative calculations only as diagnostics/sensitivity evidence and label them explicitly as such"),
    ("RE-5", "REQUIREMENT", "v0.2",
     "close the experiment as unable to answer the registered question and require a new pre-registered experiment"),
    ("RE-6", "REQUIREMENT", "v0.2",
     "verify that the proposed action does not silently change the registered KPI, denominator, population, unit, window, threshold or stopping rule"),
    ("RE-7", "PROHIBITION", "v0.2",
     "cannot become the official primary comparison for the current experiment after results are observed"),

    # --- v0.3 dual threshold -----------------------------------------------------------------
    ("DT-1", "REQUIREMENT", "v0.3",
     "Low causal confidence MUST NOT automatically imply low operational decision sufficiency"),
    ("DT-2", "PROHIBITION", "v0.3",
     "an operationally justified stop/hold MUST NOT be rewritten as proof that the nominal tested variable caused the difference"),
    ("DT-3", "REQUIREMENT", "v0.3", "When causal attribution is blocked or degraded, do not stop at `INCONCLUSIVE`"),
    ("DT-4", "REQUIREMENT", "v0.3", "practical materiality relative to registered business thresholds or verified economics"),
    ("DT-5", "REQUIREMENT", "v0.3", "whether the decision is reversible and its blast radius"),
    ("DT-6", "REQUIREMENT", "v0.3", "marginal cost/risk of continued exposure or spend"),
    ("DT-7", "REQUIREMENT", "v0.3", "cost of waiting for more information"),
    ("DT-8", "REQUIREMENT", "v0.3",
     "whether additional information is likely to change the immediate action"),
    ("DT-9", "REQUIREMENT", "v0.3",
     "relevance to the **current operational action**, not only to causal attribution"),
    ("DT-10", "REQUIREMENT", "v0.3",
     "blocks an operational action only when it is plausibly capable of changing that action"),
    ("DT-11", "REQUIREMENT", "v0.3",
     "may still leave the current configuration commercially unacceptable"),
    ("DT-12", "PROHIBITION", "v0.3", "Do not loosen SCALE because a decision is reversible"),
    # Anchor lower-cased against v0.3: the same sentence sits mid-clause in the consolidated
    # KILL definition. Sentence-position capitalisation is not a modality change.
    ("DT-13", "REQUIREMENT", "v0.3",
     "state explicitly that the causal mechanism is not established"),
    ("DT-14", "PROHIBITION", "v0.3",
     "MUST NOT be used as a universal action-paralysis label"),

    # --- v0.4 output contract ----------------------------------------------------------------
    ("OC-1", "REQUIREMENT", "v0.4",
     "`IDENTIFIED` only when the design and evidence actually support attributing the outcome difference to the nominal treatment"),
    ("OC-2", "REQUIREMENT", "v0.4",
     "randomization is absent, arms differ on more than the nominal variable, exposure/denominator integrity is unresolved"),
    ("OC-3", "PROHIBITION", "v0.4", "Never state a ceiling stronger than the design supports"),
    ("OC-4", "REQUIREMENT", "v0.4", "Every name must also appear in `confounders[].name`"),
    ("OC-5", "REQUIREMENT", "v0.4", "It must equal the top-level `recommendation`"),
    ("OC-6", "REQUIREMENT", "v0.4", "the one that, if reversed, would change the decision"),
    ("OC-7", "REQUIREMENT", "v0.4",
     "`NOT_BLOCKED` is permitted only with `state: ELIGIBLE`"),
    ("OC-8", "PROHIBITION", "v0.4",
     "Do not treat the structured record as permission to shorten the professional analysis behind it"),
    ("OC-9", "REQUIREMENT", "v0.4",
     "it is diagnostic rather than decisive when mature downstream economics are available"),
    ("OC-10", "REQUIREMENT", "v0.4",
     "the honest answer is that no action is yet justified"),

    # --- v0.4 invalidity rules ---------------------------------------------------------------
    ("IV-1", "INVALIDITY", "v0.4", "`decision_record.operational.action` differs from `recommendation`"),
    ("IV-2", "INVALIDITY", "v0.4",
     "`decision_record.causal.blocking_confounders` names anything absent from `confounders[].name`"),
    ("IV-3", "INVALIDITY", "v0.4",
     "`decision_record.causal.status` is `IDENTIFIED` while `blocking_confounders` is non-empty"),
    ("IV-4", "INVALIDITY", "v0.4",
     "`decision_record.causal.claim_ceiling` is `INCREMENTAL_CAUSAL` while `causal.status` is `UNRESOLVED`"),
    ("IV-5", "INVALIDITY", "v0.4",
     "`decision_record.scale_readiness.state` is `BLOCKED` with no reason other than `NOT_BLOCKED`"),
    ("IV-6", "INVALIDITY", "v0.4",
     "`recommendation` is `SCALE` while `scale_readiness.state` is `BLOCKED`"),

    # --- v0.5 metric precedence --------------------------------------------------------------
    ("MP-1", "REQUIREMENT", "v0.5",
     "applies to **every** action and, in a multi-arm comparison, to **which arm the action names**"),
    ("MP-2", "REQUIREMENT", "v0.5",
     "cost per lead, cost per click, cost per qualified outcome, volume — are **diagnostic**"),
    ("MP-3", "REQUIREMENT", "v0.5", "the action targets the arm both condemn"),
    ("MP-4", "REQUIREMENT", "v0.5", "the action targets the arm that fails on the **decisive** metric"),
    ("MP-5", "PROHIBITION", "v0.5", "The diagnostic ranking must not select the target"),
    ("MP-6", "REQUIREMENT", "v0.5",
     "the best available upstream metric may be decisive for a bounded reversible action"),
    ("MP-7", "REQUIREMENT", "v0.5", "Record which metric was decisive"),
    ("MP-8", "INVALIDITY", "v0.5",
     "its target is the arm favoured by downstream economics is internally inconsistent and invalid"),
    ("MP-9", "REQUIREMENT", "v0.5",
     "exactly one string taken from the case's declared `arms` list"),
    ("MP-10", "PROHIBITION", "v0.5",
     "Do not return a phrase, a description of the comparison, or two identifiers joined together"),

    # --- v0.6 scoped ceiling -----------------------------------------------------------------
    ("SC-1", "REQUIREMENT", "v0.6",
     "Every causal claim ceiling is a claim about a specific quantity. Record which one"),
    ("SC-2", "REQUIREMENT", "v0.6",
     "This is a different quantity from the registered estimand, not an early view of it"),
    ("SC-3", "REQUIREMENT", "v0.6",
     "the ceiling is at most `DIRECTIONAL_ASSOCIATION` until the window matures"),
    ("SC-4", "REQUIREMENT", "v0.6",
     "must scope the claim to the interim outcome and say so"),
    ("SC-5", "REQUIREMENT", "v0.6",
     "the interim contrast is **biased** for the final contrast rather than merely noisy"),
    ("SC-6", "PROHIBITION", "v0.6",
     "does not permit an early `SCALE` or an early `KILL` where the registered rule forbids one"),
    ("SC-7", "REQUIREMENT", "v0.6",
     "retains an `INCREMENTAL_CAUSAL` ceiling even when the outcome counts are very small"),
    ("SC-8", "PROHIBITION", "v0.6",
     "conflates \"we cannot say how large the effect is\" with \"we cannot attribute the effect at all\""),
    ("SC-9", "INVALIDITY", "v0.6",
     "the case declares the registered window incomplete, and `claim_ceiling` is `INCREMENTAL_CAUSAL`"),
    ("SC-10", "INVALIDITY", "v0.6",
     "`INTERIM_OUTCOME` while the case declares the registered window complete"),
    ("SC-11", "INVALIDITY", "v0.6",
     "the action taken would violate the registered stopping rule, which re-scoping does not unlock"),

    # --- v0.8 scope mapping, designated expression, power, contract --------------------------
    ("V8-1", "REQUIREMENT", "v0.8", "`KILL` | one arm"),
    ("V8-2", "REQUIREMENT", "v0.8", "`SCALE` | one arm"),
    ("V8-3", "REQUIREMENT", "v0.8", "`CONTINUE` | the registered comparison as a whole"),
    ("V8-4", "REQUIREMENT", "v0.8", "`INCONCLUSIVE` | the registered comparison as a whole"),
    ("V8-5", "REQUIREMENT", "v0.8", "`ITERATE` | either"),
    ("V8-6", "PROHIBITION", "v0.8",
     "you do not declare one arm inconclusive while the other is conclusive"),
    ("V8-7", "PROHIBITION", "v0.8",
     "never a reason to invent an identifier or to aim a comparison-level verdict at whichever arm was most discussed"),
    ("V8-8", "REQUIREMENT", "v0.8", "This state has one designated expression. Use it and nothing else"),
    ("V8-9", "PROHIBITION", "v0.8",
     "Do **not** express it by lowering `causal.status` or `causal.claim_ceiling`"),
    ("V8-10", "REQUIREMENT", "v0.8",
     "`causal.status` stays `IDENTIFIED` and the ceiling stays `INCREMENTAL_CAUSAL`"),
    ("V8-11", "REQUIREMENT", "v0.8",
     "`SCALE`, which stays `BLOCKED` with `INSUFFICIENT_SAMPLE`"),
    ("V8-12", "REQUIREMENT", "v0.8", "A count problem never does"),
    ("V8-13", "REQUIREMENT", "v0.8",
     "The contract is **closed**. Emit exactly the fields it permits and no others"),
    ("V8-14", "REQUIREMENT", "v0.8",
     "put it in `rationale`, `next_action`, `claim_boundaries` or `data_integrity_findings`"),
    ("V8-15", "REQUIREMENT", "v0.8",
     "Return exactly one JSON object that parses on the first attempt"),
    ("V8-16", "REQUIREMENT", "v0.8", "is not a weaker answer, it is no answer"),
]

# Anti-patterns are registered separately: every one must survive as a hard failure.
ANTIPATTERNS: list[tuple[str, str, str]] = [
    ("AP-1", "v0.3", "declares the nominal treatment/hook a causal winner when material confounding blocks"),
    ("AP-2", "v0.3", "therefore no decision can be made` without separately evaluating operational sufficiency"),
    ("AP-3", "v0.3", "applies a universal percentage/cost gap threshold to KILL without sample maturity"),
    ("AP-4", "v0.3", "continues spending merely to obtain causal certainty"),
    ("AP-5", "v0.3", "uses an operational KILL as retrospective evidence that the nominal variable caused the loss"),
    ("AP-6", "v0.5", "stops, or recommends stopping, the arm with the better matured downstream economics"),
    ("AP-7", "v0.5", "records `decisive_metric: MATURE_DOWNSTREAM_ECONOMICS` while targeting the arm that downstream"),
    ("AP-8", "v0.5", "claims matured downstream economics as decisive when the case supplies none"),
    ("AP-9", "v0.6", "claims an incremental causal effect on the registered estimand while the registered window is still open"),
    ("AP-10", "v0.6", "silently reports an interim result as though it were the registered result"),
    ("AP-11", "v0.6", "uses an interim causal claim to justify acting before the registered horizon"),
    ("AP-12", "v0.6/v0.8", "because outcome counts are small in an otherwise identified, window-complete design"),
    ("AP-13", "v0.8", "aims `INCONCLUSIVE` or `CONTINUE` at a single arm"),
    ("AP-14", "v0.8", "adds any field the output contract does not permit"),
    ("AP-15", "v0.8", "returns output that is not a single valid JSON object"),
]


class NoRuleLost(unittest.TestCase):
    def test_every_registered_rule_survives(self) -> None:
        missing = [(rid, src) for rid, _mod, src, anchor in REGISTER
                   if norm(anchor) not in CONSOLIDATED_TEXT]
        self.assertEqual([], missing, f"rules dropped in consolidation: {missing}")

    def test_every_antipattern_survives_as_a_hard_failure(self) -> None:
        section = CONSOLIDATED_TEXT.split("## 7. Anti-patterns")[-1]
        missing = [(aid, src) for aid, src, anchor in ANTIPATTERNS if norm(anchor) not in section]
        self.assertEqual([], missing, f"anti-patterns dropped or demoted: {missing}")

    def test_the_register_covers_every_superseded_document(self) -> None:
        covered = {src.split("/")[0] for _rid, _mod, src, _a in REGISTER}
        self.assertEqual({"v0.1", "v0.2", "v0.3", "v0.4", "v0.5", "v0.6", "v0.8"}, covered)


class NoModalityWeakened(unittest.TestCase):
    """A prohibition that becomes advice is a weakened gate even if the words survive."""

    HEDGES = ("prefer not to", "should avoid", "where possible", "if convenient",
              "generally avoid", "try not to", "ideally")

    def test_prohibitions_are_still_prohibitions(self) -> None:
        for rid, modality, _src, anchor in REGISTER:
            if modality != "PROHIBITION":
                continue
            with self.subTest(rule=rid):
                idx = CONSOLIDATED_TEXT.find(norm(anchor))
                self.assertGreaterEqual(idx, 0, f"{rid} missing")
                window = CONSOLIDATED_TEXT[max(0, idx - 260):idx + len(norm(anchor))]
                for hedge in self.HEDGES:
                    self.assertNotIn(hedge, window.lower(),
                                     f"{rid} was hedged with {hedge!r}")

    def test_invalidity_rules_still_render_a_result_invalid(self) -> None:
        section = CONSOLIDATED_TEXT.split("### 6.3 Internal consistency")[-1].split("### 6.4")[0]
        self.assertIn("A result is invalid, not merely imperfect, when", section)
        for rid, modality, _src, anchor in REGISTER:
            if modality != "INVALIDITY":
                continue
            with self.subTest(rule=rid):
                # MP-8 states its own invalidity inline in the metric-precedence section.
                self.assertTrue(norm(anchor) in section or norm(anchor) in CONSOLIDATED_TEXT,
                                f"{rid} no longer stated")


class GatesNotLoosened(unittest.TestCase):
    def test_scale_gate_keeps_its_full_evidence_bar(self) -> None:
        for phrase in ("primary outcome threshold", "guardrails", "unit economics when verified and required",
                       "operational response/follow-up capacity", "downstream conversion deterioration",
                       "diminishing-return or saturation risk", "reversibility and cost of scaling"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, CONSOLIDATED_TEXT)

    def test_scale_readiness_is_still_independent_of_the_action(self) -> None:
        self.assertIn("evaluated and recorded **independently of the chosen action**", CONSOLIDATED_TEXT)
        self.assertIn("a `KILL` on one arm still requires an explicit scale-readiness state",
                      CONSOLIDATED_TEXT)

    def test_stopping_rule_discipline_survives_rescoping(self) -> None:
        self.assertIn("Re-scoping to the interim outcome is a statement about evidence, never a licence to act",
                      CONSOLIDATED_TEXT)

    def test_identification_and_precision_stay_separate_in_both_channels(self) -> None:
        """The v0.7 P0. The reconciliation must be stated where BOTH rules fire, not once."""
        action_side = CONSOLIDATED_TEXT.split("### 5.3")[-1].split("### 5.4")[0]
        ceiling_side = CONSOLIDATED_TEXT.split("### 5.6")[-1].split("### 5.7")[0]
        decision_side = CONSOLIDATED_TEXT.split("#### The five recommendations")[-1].split("#### Which scope")[0]
        self.assertIn("Insufficient power bears on the action, never on identification", action_side)
        self.assertIn("Sparse outcomes never lower the ceiling", ceiling_side)
        self.assertIn("it belongs to this action channel alone", decision_side)
        self.assertIn("never a reason to lower", decision_side)

    def test_the_dual_threshold_is_stated_before_the_procedure_reads_against_it(self) -> None:
        self.assertLess(CONSOLIDATED_TEXT.find("## 4. Two decisions, two thresholds"),
                        CONSOLIDATED_TEXT.find("## 5. Analysis procedure"))


class ClosedVocabularyCompleteness(unittest.TestCase):
    """Phase 4: a value the grader enforces that the candidate was never told about is a defect.

    This is the check that both residual v0.8 failures and the whole v0.7 root cause violated.
    """

    def setUp(self) -> None:
        freeze = json.loads((HERE / "candidate-freeze-v0.8.json").read_text(encoding="utf-8"))
        self.contract = json.loads((ROOT / freeze["output_contract_path"]).read_text(encoding="utf-8"))
        self.record = self.contract["properties"]["decision_record"]["properties"]

    def enums(self) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for channel, spec in self.record.items():
            for field, fspec in spec.get("properties", {}).items():
                values = fspec.get("enum") or (fspec.get("items") or {}).get("enum")
                if values:
                    out[f"{channel}.{field}"] = values
        out["recommendation"] = self.contract["properties"]["recommendation"]["enum"]
        return out

    def test_every_frozen_enum_member_is_documented(self) -> None:
        missing: list[str] = []
        for field, values in self.enums().items():
            for value in values:
                if f"`{value}`" not in CONSOLIDATED_TEXT:
                    missing.append(f"{field}={value}")
        self.assertEqual([], missing,
                         f"contract values the candidate is never told about: {missing}")

    def test_registered_primary_kpi_carries_a_trigger_condition(self) -> None:
        """The exact member whose absence closed gate 33243263001."""
        self.assertIn("REGISTERED_PRIMARY_KPI", [v for vs in self.enums().values() for v in vs])
        idx = CONSOLIDATED_TEXT.find("`REGISTERED_PRIMARY_KPI` — the registered primary KPI result is among the grounds")
        self.assertGreater(idx, 0, "decision_basis REGISTERED_PRIMARY_KPI has no trigger condition")
        window = CONSOLIDATED_TEXT[idx:idx + 460]
        self.assertIn("registered success rule", window)
        self.assertIn("registered failure rule", window)
        self.assertIn("completeness of the registered collection window", window)
        self.assertIn("rather than instead of it", window)

    def test_the_decision_basis_list_is_complete_and_marked_closed(self) -> None:
        values = self.enums()["operational.decision_basis"]
        self.assertEqual(10, len(values))
        self.assertIn("Closed vocabulary, all ten members", CONSOLIDATED_TEXT)

    def test_the_other_two_undocumented_vocabularies_are_now_listed(self) -> None:
        self.assertIn("Closed vocabulary, all six members", CONSOLIDATED_TEXT)
        self.assertIn("Closed vocabulary, all\neight members".replace("\n", " "), CONSOLIDATED_TEXT)

    def test_nothing_outside_the_frozen_contract_was_invented(self) -> None:
        """Consolidation may surface frozen vocabulary; it may not create new vocabulary."""
        permitted = {v for vs in self.enums().values() for v in vs}
        permitted |= {"OBSERVED", "MISSING", "NOT_COLLECTED", "DELAYED", "INVALID", "NOT_APPLICABLE"}
        permitted |= {"REGISTERED_ESTIMAND", "INTERIM_OUTCOME"}
        shouty = set(re.findall(r"`([A-Z][A-Z_]{3,})`", CONSOLIDATED_TEXT))
        self.assertEqual(set(), shouty - permitted,
                         f"vocabulary invented during consolidation: {sorted(shouty - permitted)}")


class InstrumentUntouched(unittest.TestCase):
    def setUp(self) -> None:
        self.v08 = json.loads((HERE / "candidate-freeze-v0.8.json").read_text(encoding="utf-8"))

    def test_grader_generator_and_runner_are_byte_identical_to_freeze_v08(self) -> None:
        for role, ref in self.v08["instrument"].items():
            with self.subTest(role=role):
                self.assertEqual(ref["git_blob_sha"], blob(ROOT / ref["path"]),
                                 f"{role} changed during a consolidation cycle")

    def test_the_output_contract_is_byte_identical_to_freeze_v08(self) -> None:
        self.assertEqual(self.v08["output_contract_git_blob_sha"],
                         blob(ROOT / self.v08["output_contract_path"]))

    def test_the_superseded_documents_are_untouched_on_disk(self) -> None:
        for component in self.v08["assembly"]:
            with self.subTest(path=component["path"]):
                self.assertEqual(component["git_blob_sha"], blob(ROOT / component["path"]),
                                 "consolidation must not rewrite history; v0.8 must still verify")


class ConsolidationIsDocumented(unittest.TestCase):
    def test_the_record_names_every_conflict_and_dead_dependency(self) -> None:
        text = norm(RECORD.read_text(encoding="utf-8"))
        for marker in ("C1 — action scope", "C2 — insufficient power",
                       "C3 — `INCONCLUSIVE`", "C4 — where non-contract content goes",
                       "until the schema is versioned", "Apply this overlay last"):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_the_record_states_what_consolidation_cannot_prove(self) -> None:
        text = norm(RECORD.read_text(encoding="utf-8"))
        self.assertIn("only a gate can show that", text)

    def test_the_runtime_document_points_at_the_record_without_carrying_it(self) -> None:
        self.assertIn("consolidation-record-2026-08-30.md", CONSOLIDATED_TEXT)
        self.assertIn("That record is not part of the runtime document", CONSOLIDATED_TEXT)
        for forensic in ("H-GDS-02", "33239983604", "seed 20260829", "Apply this overlay last"):
            with self.subTest(forensic=forensic):
                self.assertNotIn(forensic, CONSOLIDATED_TEXT)


if __name__ == "__main__":
    unittest.main(verbosity=2)
