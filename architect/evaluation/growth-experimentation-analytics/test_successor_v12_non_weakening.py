#!/usr/bin/env python3
"""Proof that consolidated v1.2 adds the identification ledger without weakening v1.1 or v1.0.

No provider calls. The containment chain is v1.2 ⊇ v1.1 ⊇ v1.0, and it is proved line by line:
**every non-blank line of v1.1 appears verbatim in v1.2 except the title.** That is a stronger
claim than the v1.1 successor could make — v1.1 had three permitted replacements — and it is why
this file is short. Nothing was rewrapped, nothing was rephrased, nothing was moved.

The v1.0 rule register, its hedge detector and its invalidity checks are then re-run against v1.2,
and the v1.1 repairs are asserted still present, so a gain from either earlier cycle cannot have
been quietly dropped while adding this one.
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
V12 = RESEARCH / "professional-model-consolidated-v1.2.md"


def norm(text: str) -> str:
    return " ".join(text.split())


V10_TEXT = V10.read_text(encoding="utf-8")
V11_TEXT = V11.read_text(encoding="utf-8")
V12_TEXT = V12.read_text(encoding="utf-8")
V12_NORM = norm(V12_TEXT)

TITLE_V11 = "# Growth Experimentation & Measurement — professional model v1.1 (consolidated)"
TITLE_V12 = "# Growth Experimentation & Measurement — professional model v1.2 (consolidated)"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class TheSuccessorIsPurelyAdditive(unittest.TestCase):
    def test_the_title_is_the_only_line_of_v11_that_does_not_survive(self) -> None:
        v12_lines = set(V12_TEXT.splitlines())
        lost = [line for line in V11_TEXT.splitlines()
                if line.strip() and line not in v12_lines and line != TITLE_V11]
        self.assertEqual([], lost, f"v1.1 content dropped by the successor: {lost}")
        self.assertIn(TITLE_V12, V12_TEXT)
        self.assertNotIn(TITLE_V11, V12_TEXT)

    def test_the_v10_containment_still_holds_transitively(self) -> None:
        """v1.2 ⊇ v1.1 ⊇ v1.0, checked directly against v1.0 rather than assumed."""
        v11 = _load("v11_proof", HERE / "test_successor_v11_non_weakening.py")
        v12_lines = set(V12_TEXT.splitlines())
        lost = [line for line in V10_TEXT.splitlines()
                if line.strip() and line not in v12_lines
                and line not in v11.PERMITTED_REPLACEMENTS]
        self.assertEqual([], lost, f"v1.0 content dropped by the successor: {lost}")

    def test_no_relaxing_language_was_introduced(self) -> None:
        added = "\n".join(line for line in V12_TEXT.splitlines()
                          if line not in set(V11_TEXT.splitlines()))
        for hedge in ("where possible", "if practical", "you may omit", "is optional",
                      "no longer required", "need not", "unless inconvenient", "best effort",
                      "prefer not to", "should avoid", "ideally"):
            with self.subTest(hedge=hedge):
                self.assertNotIn(hedge, added.lower())

    def test_the_addition_is_a_procedure_rather_than_a_restatement(self) -> None:
        """v1.1's evidence: restating a rule did not change behavior; adding a procedure did."""
        added = "\n".join(line for line in V12_TEXT.splitlines()
                          if line not in set(V11_TEXT.splitlines()))
        self.assertIn("Run this **before you read a single outcome count**", added)
        self.assertIn("Read the ledger off those answers", added)
        # An ordered, answerable question list, not prose about the principle.
        for numbered in ("1. **Assignment**", "2. **Exposure and instrumentation**",
                         "3. **Comparability**", "4. **Confounding**", "5. **Window**"):
            with self.subTest(question=numbered):
                self.assertIn(numbered, added)


class NothingFromEitherEarlierCycleWasWeakened(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.equiv = _load("equiv_v10", HERE / "test_consolidation_equivalence_v10.py")

    def test_every_v10_registered_rule_still_survives(self) -> None:
        missing = [(rid, src) for rid, _mod, src, anchor in self.equiv.REGISTER
                   if norm(anchor) not in V12_NORM]
        self.assertEqual([], missing, f"rules dropped by the successor: {missing}")

    def test_the_register_is_not_stubbed(self) -> None:
        self.assertGreaterEqual(len(self.equiv.REGISTER), 100)

    def test_every_antipattern_still_survives_as_a_hard_failure(self) -> None:
        section = V12_NORM.split("## 7. Anti-patterns")[-1]
        missing = [(aid, src) for aid, src, anchor in self.equiv.ANTIPATTERNS
                   if norm(anchor) not in section]
        self.assertEqual([], missing, f"anti-patterns dropped or demoted: {missing}")

    def test_prohibitions_are_still_prohibitions(self) -> None:
        for rid, modality, _src, anchor in self.equiv.REGISTER:
            if modality != "PROHIBITION":
                continue
            with self.subTest(rule=rid):
                index = V12_NORM.find(norm(anchor))
                self.assertGreaterEqual(index, 0, f"{rid} missing")
                window = V12_NORM[max(0, index - 260):index + len(norm(anchor))]
                for hedge in self.equiv.NoModalityWeakened.HEDGES:
                    self.assertNotIn(hedge, window.lower(), f"{rid} was hedged with {hedge!r}")

    def test_invalidity_rules_still_render_a_result_invalid(self) -> None:
        section = V12_NORM.split("### 6.3 Internal consistency")[-1].split("### 6.4")[0]
        self.assertIn("A result is invalid, not merely imperfect, when", section)
        for rid, modality, _src, anchor in self.equiv.REGISTER:
            if modality != "INVALIDITY":
                continue
            with self.subTest(rule=rid):
                self.assertTrue(norm(anchor) in section or norm(anchor) in V12_NORM,
                                f"{rid} no longer stated")

    def test_the_v11_class_a_repair_is_intact(self) -> None:
        """The gain that took scope-target failures from 11 to 0 must not be lost."""
        for phrase in (
            "**The declared identifier that keys no such block is the registered comparison as a whole.**",
            "An identifier is not the comparison because it is called `experiment`",
            "The `fixture_id` is **not** an identifier you may target",
            "the case declares no comparison-level scope",
        ):
            with self.subTest(phrase=phrase[:48]):
                self.assertIn(norm(phrase), V12_NORM)

    def test_the_v11_consistency_couplings_are_intact(self) -> None:
        consistency = norm(V12_TEXT.split("### 6.3 Internal consistency")[1].split("### 6.4")[0])
        for phrase in (
            "`action` is `CONTINUE` or `INCONCLUSIVE` and `target` names an arm",
            "`decision_basis` omits `INSUFFICIENT_EVIDENCE`",
            "`decision_basis` omits `COST_OF_WAITING`",
            "`scale_readiness` is nested inside `operational`",
            "where the only adverse fact is small outcome counts",
        ):
            with self.subTest(phrase=phrase[:48]):
                self.assertIn(norm(phrase), consistency)

    def test_the_gates_the_repair_touches_are_not_loosened(self) -> None:
        for phrase in (
            "Sparse outcome counts never lower it",
            "evaluated independently of the chosen action",
            "MUST NOT be used as a universal action-paralysis label",
            "Re-scoping to the interim outcome is a statement about evidence, never a licence to act",
            "The contract is **closed**",
        ):
            with self.subTest(phrase=phrase[:44]):
                self.assertIn(norm(phrase), V12_NORM)

    def test_the_predecessors_are_left_alone(self) -> None:
        for path in (V10, V11):
            with self.subTest(document=path.name):
                head = subprocess.check_output(
                    ["git", "show", f"HEAD:architect/research/growth-experimentation-analytics/"
                                    f"{path.name}"], text=True, cwd=ROOT)
                self.assertEqual(head, path.read_text(encoding="utf-8"),
                                 f"{path.name} must not be edited by this repair")


if __name__ == "__main__":
    unittest.main(verbosity=2)
