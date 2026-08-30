#!/usr/bin/env python3
"""Proof that consolidated v1.1 repairs the observed failures without weakening v1.0.

No provider calls. Three obligations, in order of strength.

1. **Nothing was removed.** Every non-blank line of v1.0 appears verbatim in v1.1, except three
   lines that are enumerated here with their replacements and shown to be a version string, a
   re-wrap, and one bullet's terminal punctuation. A line-level containment proof is stronger than
   any phrase register, because it cannot miss a rule the register forgot to list.
2. **Nothing was weakened.** The 118-entry rule register written for the v1.0 consolidation is
   re-run against v1.1, together with its modality and gate-strength checks. If v1.1 had softened
   a prohibition or dropped an invalidity condition, those checks fail on v1.1 exactly as they
   would have on a bad v1.0.
3. **The repairs are actually present**, are vocabulary-independent, and are reachable by a reader
   of the runtime document alone.
"""

from __future__ import annotations

import importlib.util
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESEARCH = ROOT / "architect/research/growth-experimentation-analytics"

V10 = RESEARCH / "professional-model-consolidated-v1.0.md"
V11 = RESEARCH / "professional-model-consolidated-v1.1.md"
ADJUDICATION = RESEARCH / "failure-adjudication-2026-08-30.md"


def norm(text: str) -> str:
    return " ".join(text.split())


V10_TEXT, V11_TEXT = V10.read_text(encoding="utf-8"), V11.read_text(encoding="utf-8")
V11_NORM = norm(V11_TEXT)

# The complete set of v1.0 lines that do not survive byte-identically, each with the v1.1 line
# that replaces it. Any other removal fails the containment test below.
PERMITTED_REPLACEMENTS = {
    "# Growth Experimentation & Measurement — professional model v1.0 (consolidated)":
        "# Growth Experimentation & Measurement — professional model v1.1 (consolidated)",
    "no professional judgement, removes no rule, and weakens no gate. Where two documents stated the":
        "no professional judgement, removes no rule, and weakens no gate.",
    "- `target` is not one of the declared identifiers, or names more than one.":
        "- `target` is not one of the declared identifiers, or names more than one;",
}


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class NothingWasRemoved(unittest.TestCase):
    def test_every_v10_line_survives_in_v11(self) -> None:
        v11_lines = set(V11_TEXT.splitlines())
        lost = [line for line in V10_TEXT.splitlines()
                if line.strip() and line not in v11_lines
                and line not in PERMITTED_REPLACEMENTS]
        self.assertEqual([], lost, f"v1.0 content dropped by the successor: {lost}")

    def test_each_permitted_replacement_is_present_and_is_not_a_rule_change(self) -> None:
        for original, replacement in PERMITTED_REPLACEMENTS.items():
            with self.subTest(line=original[:60]):
                self.assertIn(replacement, V11_TEXT)
                self.assertNotIn(original, V11_TEXT)
        # The three are, respectively: a version string; a sentence re-wrapped because a paragraph
        # was inserted after it, whose continuation is still present; and one bullet's full stop
        # becoming a semicolon because the list now continues.
        self.assertIn("same rule, one statement survives.", V11_TEXT)

    def test_the_successor_is_strictly_longer(self) -> None:
        self.assertGreater(len(V11_TEXT.splitlines()), len(V10_TEXT.splitlines()))

    def test_no_relaxing_language_was_introduced(self) -> None:
        added = "\n".join(line for line in V11_TEXT.splitlines()
                          if line not in set(V10_TEXT.splitlines()))
        for hedge in ("where possible", "if practical", "you may omit", "is optional",
                      "no longer required", "need not", "unless inconvenient", "best effort"):
            with self.subTest(hedge=hedge):
                self.assertNotIn(hedge, added.lower())


class NothingWasWeakened(unittest.TestCase):
    """The v1.0 consolidation register, re-run against the successor."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.equiv = _load("equiv_v10", HERE / "test_consolidation_equivalence_v10.py")

    def test_every_registered_rule_still_survives(self) -> None:
        missing = [(rid, src) for rid, _mod, src, anchor in self.equiv.REGISTER
                   if norm(anchor) not in V11_NORM]
        self.assertEqual([], missing, f"rules dropped by the successor: {missing}")

    def test_the_register_is_not_empty_or_stubbed(self) -> None:
        self.assertGreaterEqual(len(self.equiv.REGISTER), 100)

    def test_every_antipattern_still_survives_as_a_hard_failure(self) -> None:
        section = V11_NORM.split("## 7. Anti-patterns")[-1]
        missing = [(aid, src) for aid, src, anchor in self.equiv.ANTIPATTERNS
                   if norm(anchor) not in section]
        self.assertEqual([], missing, f"anti-patterns dropped or demoted: {missing}")

    def test_prohibitions_are_still_prohibitions(self) -> None:
        """The v1.0 hedge detector, pointed at the successor."""
        for rid, modality, _src, anchor in self.equiv.REGISTER:
            if modality != "PROHIBITION":
                continue
            with self.subTest(rule=rid):
                index = V11_NORM.find(norm(anchor))
                self.assertGreaterEqual(index, 0, f"{rid} missing")
                window = V11_NORM[max(0, index - 260):index + len(norm(anchor))]
                for hedge in self.equiv.NoModalityWeakened.HEDGES:
                    self.assertNotIn(hedge, window.lower(), f"{rid} was hedged with {hedge!r}")

    def test_invalidity_rules_still_render_a_result_invalid(self) -> None:
        section = V11_NORM.split("### 6.3 Internal consistency")[-1].split("### 6.4")[0]
        self.assertIn("A result is invalid, not merely imperfect, when", section)
        for rid, modality, _src, anchor in self.equiv.REGISTER:
            if modality != "INVALIDITY":
                continue
            with self.subTest(rule=rid):
                self.assertTrue(norm(anchor) in section or norm(anchor) in V11_NORM,
                                f"{rid} no longer stated")

    def test_the_gates_that_the_repair_touches_are_not_loosened(self) -> None:
        for phrase in (
            "Sparse outcome counts never lower it",
            "evaluated independently of the chosen action",
            "MUST NOT be used as a universal action-paralysis label",
            "The diagnostic ranking must not select the target",
            "The contract is **closed**",
        ):
            with self.subTest(phrase=phrase[:44]):
                self.assertIn(norm(phrase), V11_NORM)


class ClassARecognitionIsEncodedAndVocabularyFree(unittest.TestCase):
    def test_the_scope_rule_v10_already_stated_is_untouched(self) -> None:
        for phrase in (
            "| `CONTINUE` | the registered comparison as a whole | the experiment-level identifier |",
            "| `INCONCLUSIVE` | the registered comparison as a whole | the experiment-level identifier |",
            "`CONTINUE` and `INCONCLUSIVE` are not statements about one arm",
        ):
            with self.subTest(phrase=phrase[:44]):
                self.assertIn(norm(phrase), V11_NORM)

    def test_the_recognition_procedure_is_structural_not_lexical(self) -> None:
        self.assertIn(norm("**The declared identifier that keys no such block is the registered "
                           "comparison as a whole.**"), V11_NORM)
        self.assertIn(norm("Never decide this from the words"), V11_NORM)

    def test_the_document_forbids_treating_experiment_as_a_magic_token(self) -> None:
        self.assertIn(norm("An identifier is not the comparison because it is called `experiment`"),
                      V11_NORM)

    def test_the_fixture_id_is_excluded_explicitly(self) -> None:
        self.assertIn(norm("The `fixture_id` is **not** an identifier you may target"), V11_NORM)

    def test_the_no_scope_case_escalates_rather_than_falling_back_to_an_arm(self) -> None:
        self.assertIn(norm("the honest response is to say the evidence is insufficient — not to "
                           "aim it at an arm"), V11_NORM)


class ClassesBCDAreCheckableAtEmitTime(unittest.TestCase):
    """The couplings were normative in v1.0; v1.1 gathers them where the result is checked."""

    def setUp(self) -> None:
        self.consistency = norm(V11_TEXT.split("### 6.3 Internal consistency")[1]
                                .split("### 6.4")[0])

    def test_a_comparison_level_action_aimed_at_an_arm_is_invalid(self) -> None:
        self.assertIn(norm("`action` is `CONTINUE` or `INCONCLUSIVE` and `target` names an arm"),
                      self.consistency)

    def test_inconclusive_without_insufficient_evidence_is_invalid(self) -> None:
        self.assertIn(norm("`action` is `INCONCLUSIVE` and `decision_basis` omits "
                           "`INSUFFICIENT_EVIDENCE`"), self.consistency)

    def test_none_decidable_against_mature_downstream_economics_is_invalid(self) -> None:
        self.assertIn(norm("`decisive_metric` is `NONE_DECIDABLE` although the case supplies "
                           "verified, matured downstream economics"), self.consistency)

    def test_a_stop_on_cost_of_waiting_must_record_it(self) -> None:
        self.assertIn(norm("`decision_basis` omits `COST_OF_WAITING`"), self.consistency)

    def test_lowering_the_causal_claim_for_sparsity_is_invalid(self) -> None:
        self.assertIn(norm("where the only adverse fact is small outcome counts"), self.consistency)
        self.assertIn(norm("Sparsity is a precision property of the sample and never an "
                           "identification failure"), self.consistency)

    def test_the_sparsity_rule_still_routes_to_the_action_channel(self) -> None:
        """Repairing C2 must not turn into permission to overclaim."""
        self.assertIn(norm("Say the registered question cannot be answered through the action "
                           "channel"), self.consistency)

    def test_scale_readiness_nesting_is_named_invalid(self) -> None:
        self.assertIn(norm("`scale_readiness` is nested inside `operational` rather than sitting "
                           "beside it"), self.consistency)

    def test_prose_brevity_is_required_with_its_reason(self) -> None:
        self.assertIn(norm("Keep every prose field short"), V11_NORM)
        self.assertIn(norm("a result that fails to parse scores nothing"), V11_NORM)

    def test_the_additions_are_declared_to_add_no_new_professional_rule(self) -> None:
        self.assertIn(norm("Nothing in this list is a new professional rule"), self.consistency)
        for section in ("§4", "§5.3", "§5.7", "§5.9"):
            with self.subTest(section=section):
                self.assertIn(section, self.consistency)


class TheRepairIsTraceable(unittest.TestCase):
    def test_the_adjudication_record_exists_and_separates_evidence_grades(self) -> None:
        text = ADJUDICATION.read_text(encoding="utf-8")
        for label in ("**FACT", "**INFERENCE", "**HYPOTHESIS"):
            with self.subTest(label=label):
                self.assertIn(label, text)

    def test_the_adjudication_settles_class_a_without_citing_the_oracle_as_authority(self) -> None:
        text = ADJUDICATION.read_text(encoding="utf-8")
        self.assertIn("It is not a stricter rule invented by the evaluator; it is the candidate's "
                      "own invariant", norm(text))

    def test_the_successor_points_at_its_adjudication(self) -> None:
        self.assertIn("failure-adjudication-2026-08-30.md", V11_TEXT)

    def test_the_predecessor_and_its_results_are_left_alone(self) -> None:
        head = subprocess.check_output(
            ["git", "show", f"HEAD:architect/research/growth-experimentation-analytics/"
                            f"professional-model-consolidated-v1.0.md"], text=True, cwd=ROOT)
        self.assertEqual(head, V10_TEXT, "v1.0 must not be edited by this repair")
        self.assertIn("Neither is reinterpreted by this repair", V11_TEXT)


if __name__ == "__main__":
    unittest.main(verbosity=2)
