#!/usr/bin/env python3
"""Regressions for the v1.2 identification ledger.

No provider calls. The frozen grader is imported unmodified and does all the judging.

v1.1 established which kind of repair moves this candidate: adding a *procedure* worked (scope
targets 11 to 0), restating an existing rule did not (4 to 6). So the v1.2 repair is a procedure,
and it has to be held to the same standard the class-A recognition rule was: implemented once here
as a reference implementation, then shown to agree with the **independently frozen oracle** on
every case the generator can produce and on externally authored vocabulary.

The traps this file sets, per issue #205 §6 — vocabulary, arm ordering, sparse counts, event rates
and decision conditions all vary, so no magic token and no observed fixture can satisfy it:

  * the ledger's answer must not change when identifiers are renamed;
  * it must not change when the arms are reordered;
  * it must not change when outcome counts are driven to any value, including zero;
  * it must not change when the base event rate is varied over three orders of magnitude;
  * a design defect must still lower the claim, so the rule cannot be "always say IDENTIFIED".
"""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXTERNAL = HERE / "external"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


GRADER = _load("grader", HERE / "grader_v07_structural.py")
GENERATOR = _load("generator", HERE / "heldout_generator_v07.py")
PACK = _load("pack_contract", EXTERNAL / "external_pack_contract.py")
CONTRACT = json.loads((HERE / "schemas" / "result-v4.schema.json").read_text(encoding="utf-8"))
V12 = (ROOT / "architect/research/growth-experimentation-analytics"
       / "professional-model-consolidated-v1.2.md").read_text(encoding="utf-8")

CEILINGS = ["NONE", "DESCRIPTIVE_ASSOCIATION", "DIRECTIONAL_ASSOCIATION", "INCREMENTAL_CAUSAL"]

# Fields by which a case can declare each defect the ledger asks about. Everything else is silence,
# and silence is not a defect.
COMPARABILITY_DEFECTS = ("audience_source_differs", "creative_differs",
                         "audience_automation_differs")


def identification_ledger(case: dict) -> dict:
    """The §5.2 ledger, reading declared design facts only. Never reads an outcome count."""
    design = case.get("design") or {}

    defects = []
    if design.get("randomized_split") is False:                       # 1 assignment
        defects.append("assignment")
    if design.get("exposure_defect") or design.get("instrumentation_defect"):  # 2 exposure
        defects.append("exposure")
    if any(design.get(key) is True for key in COMPARABILITY_DEFECTS) or (   # 3 comparability
            "budget_a" in design and design.get("budget_a") != design.get("budget_b")):
        defects.append("comparability")
    if design.get("confound") or design.get("blocking_confounder"):   # 4 confounding
        defects.append("confounding")

    window_complete = case.get("registered_window_complete")

    if defects:
        return {"defects": defects, "status": "UNRESOLVED",
                "max_ceiling": {"REGISTERED_ESTIMAND": "DIRECTIONAL_ASSOCIATION"}}
    if window_complete:
        return {"defects": [], "status": "IDENTIFIED",
                "max_ceiling": {"REGISTERED_ESTIMAND": "INCREMENTAL_CAUSAL"}}
    return {"defects": [], "status": "IDENTIFIED_ON_INTERIM",
            "max_ceiling": {"REGISTERED_ESTIMAND": "DIRECTIONAL_ASSOCIATION",
                            "INTERIM_OUTCOME": "INCREMENTAL_CAUSAL"}}


class TheLedgerAgreesWithTheFrozenOracle(unittest.TestCase):
    """The procedure is not merely plausible; it returns what the independent oracle expects."""

    def _check(self, fixture: dict, expectation: dict) -> None:
        ledger = identification_ledger(fixture["case"])
        for scope, ceiling in ledger["max_ceiling"].items():
            bounds = (expectation.get("ceiling_by_scope") or {}).get(scope)
            if not bounds or "max" not in bounds:
                continue
            self.assertEqual(bounds["max"], ceiling,
                             f"ledger and oracle disagree on the {scope} ceiling")
        allowed = expectation.get("causal_status_in")
        if allowed:
            expected = "IDENTIFIED" if ledger["status"].startswith("IDENTIFIED") else "UNRESOLVED"
            self.assertIn(expected, allowed,
                          f"ledger says {expected}, oracle allows {allowed}")

    def test_it_agrees_on_every_generated_case_across_seeds(self) -> None:
        for seed in (20260827, 20260829, 20260901, 20261115, 20270303):
            suite, oracle = GENERATOR.generate(seed, 2)
            for fixture in suite["fixtures"]:
                with self.subTest(seed=seed, fixture=fixture["fixture_id"]):
                    self._check(fixture, oracle["expectations"][fixture["fixture_id"]])

    def test_it_agrees_on_externally_authored_vocabulary(self) -> None:
        ext = _load("ext_tests", EXTERNAL / "test_external_pack_contract.py")
        for family in PACK.FAMILIES:
            fixture, expectation = ext.ADMITTED[family]
            with self.subTest(family=family):
                self._check(fixture, expectation)

    def test_the_sparse_family_is_identified_and_the_confounded_families_are_not(self) -> None:
        """The discriminating pair: the rule cannot be 'always identified' or 'always unresolved'."""
        suite, _oracle = GENERATOR.generate(20260901, 2)
        by_prefix = {f["fixture_id"][:8]: f for f in suite["fixtures"]}
        self.assertEqual("IDENTIFIED",
                         identification_ledger(by_prefix["HO-SBI-0"]["case"])["status"])
        self.assertEqual("IDENTIFIED",
                         identification_ledger(by_prefix["HO-CSW-0"]["case"])["status"])
        self.assertEqual("UNRESOLVED",
                         identification_ledger(by_prefix["HO-UDC-0"]["case"])["status"])
        self.assertEqual("UNRESOLVED",
                         identification_ledger(by_prefix["HO-UOC-0"]["case"])["status"])
        self.assertEqual("IDENTIFIED_ON_INTERIM",
                         identification_ledger(by_prefix["HO-IFH-0"]["case"])["status"])


class NoCountCanReopenTheLedger(unittest.TestCase):
    """The property the whole repair rests on."""

    def _sparse_case(self) -> dict:
        suite, _oracle = GENERATOR.generate(20260901, 2)
        fixture = next(f for f in suite["fixtures"] if f["fixture_id"].startswith("HO-SBI"))
        return json.loads(json.dumps(fixture["case"]))

    def _counted_arms(self, case: dict) -> list[str]:
        return [a for a in case["arms"] if isinstance(case.get(a), dict)]

    def test_driving_the_outcome_counts_anywhere_leaves_the_answer_untouched(self) -> None:
        base = self._sparse_case()
        kpi = base["primary_kpi"]
        reference = identification_ledger(base)
        for treatment_count, baseline_count in ((0, 0), (1, 0), (2, 1), (3, 3), (9, 1),
                                                (400, 380), (5000, 4999)):
            case = json.loads(json.dumps(base))
            arms = self._counted_arms(case)
            case[arms[0]][kpi] = treatment_count
            case[arms[1]][kpi] = baseline_count
            with self.subTest(counts=(treatment_count, baseline_count)):
                self.assertEqual(reference, identification_ledger(case))

    def test_varying_the_base_event_rate_over_three_orders_of_magnitude_changes_nothing(self) -> None:
        base = self._sparse_case()
        reference = identification_ledger(base)
        for exposed in (80, 800, 8000, 80000):
            case = json.loads(json.dumps(base))
            for arm in self._counted_arms(case):
                case[arm]["exposed"] = exposed
            with self.subTest(exposed=exposed):
                self.assertEqual(reference, identification_ledger(case))

    def test_reordering_the_arms_changes_nothing(self) -> None:
        base = self._sparse_case()
        reference = identification_ledger(base)
        case = json.loads(json.dumps(base))
        case["arms"] = list(reversed(case["arms"]))
        self.assertEqual(reference, identification_ledger(case))

    def test_renaming_every_identifier_changes_nothing(self) -> None:
        base = self._sparse_case()
        reference = identification_ledger(base)
        case = json.loads(json.dumps(base))
        renames = {old: f"zz_{index}" for index, old in enumerate(case["arms"])}
        for old, new in renames.items():
            if isinstance(case.get(old), dict):
                case[new] = case.pop(old)
        case["arms"] = [renames[a] for a in case["arms"]]
        self.assertEqual(reference, identification_ledger(case))

    def test_a_declared_design_defect_does_lower_the_claim(self) -> None:
        """Otherwise the ledger would just be 'always identified', which is not a rule."""
        for defect, patch in (
            ("assignment", {"randomized_split": False}),
            ("exposure", {"exposure_defect": "assigned and exposed units diverge by 18%"}),
            ("comparability", {"creative_differs": True}),
            ("confounding", {"confound": "a concurrent promotion ran on one arm only"}),
        ):
            case = self._sparse_case()
            case["design"].update(patch)
            with self.subTest(defect=defect):
                ledger = identification_ledger(case)
                self.assertEqual("UNRESOLVED", ledger["status"])
                self.assertIn(defect, ledger["defects"])

    def test_an_incomplete_window_censors_the_registered_estimand_only(self) -> None:
        case = self._sparse_case()
        case["registered_window_complete"] = False
        ledger = identification_ledger(case)
        self.assertEqual("DIRECTIONAL_ASSOCIATION", ledger["max_ceiling"]["REGISTERED_ESTIMAND"])
        self.assertEqual("INCREMENTAL_CAUSAL", ledger["max_ceiling"]["INTERIM_OUTCOME"])

    def test_silence_is_not_a_defect(self) -> None:
        """A case that simply omits a design field must not be treated as declaring a defect."""
        case = self._sparse_case()
        for key in ("exposure_verified", "arms_differ_only_in", "assignment", "confounding"):
            case["design"].pop(key, None)
        self.assertEqual("IDENTIFIED", identification_ledger(case)["status"])
        self.assertEqual([], identification_ledger(case)["defects"])


class TheObservedV11FailuresAreRejectedByTheFrozenGrader(unittest.TestCase):
    """Replays of run 33299723985, under externally authored vocabulary."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.ext = _load("ext_tests2", EXTERNAL / "test_external_pack_contract.py")

    def _record(self, family: str, action: str | None = None) -> tuple[dict, dict, dict]:
        fixture, expectation = self.ext.ADMITTED[family]
        act = action or expectation["action_in"][0]
        target = (expectation["target_by_action"][act])[0]
        record = {
            "fixture_id": fixture["fixture_id"], "recommendation": act,
            "data_integrity_findings": [], "computations": [
                {"name": name, "inputs": {"source": "case"}, "method": "declared arithmetic",
                 "result": spec[0], "unit": "ratio" if spec[2] == "RATIO" else "currency"}
                for name, spec in expectation["computations"].items()],
            "claim_boundaries": ["scoped to the registered population and window"],
            "confounders": [], "rationale": "replay", "next_action": "record the decision",
            "decision_record": {
                "causal": {"status": (expectation.get("causal_status_in") or ["UNRESOLVED"])[0],
                           "claim_scope": expectation["allowed_scopes"][0],
                           "claim_ceiling": "INCREMENTAL_CAUSAL"
                           if (expectation.get("causal_status_in") or [""])[0] == "IDENTIFIED"
                           else "DIRECTIONAL_ASSOCIATION",
                           "blocking_confounders": []},
                "operational": {
                    "action": act, "target": target,
                    "decisive_metric": expectation["decisive_metric_in"][0],
                    "decision_basis": list(expectation.get("basis_required")
                                           or ["REGISTERED_PRIMARY_KPI"]),
                    "reversible": True,
                    "evidence_that_would_change_action": "a powered replication"},
                "scale_readiness": {
                    "state": expectation["scale_state"],
                    "blocking_reasons": [expectation["scale_reasons_any"][0]]
                    if expectation["scale_state"] == "BLOCKED" else ["NOT_BLOCKED"]},
            },
        }
        return record, fixture, expectation

    def test_the_dominant_failure_sparsity_lowering_the_claim_is_rejected(self) -> None:
        """EX-05-01 trials 1, 3, 4 and 7 of run 33299723985."""
        record, fixture, expectation = self._record("SPARSE_BUT_IDENTIFIED")
        record["decision_record"]["causal"]["status"] = "UNRESOLVED"
        record["decision_record"]["causal"]["claim_ceiling"] = "NONE"
        report = GRADER.grade(record, fixture, expectation, CONTRACT)
        self.assertFalse(report["pass"])
        self.assertTrue(any("understates this design" in f for f in report["failures"]))

    def test_the_ledger_answer_passes_on_that_same_fixture(self) -> None:
        record, fixture, expectation = self._record("SPARSE_BUT_IDENTIFIED")
        ledger = identification_ledger(fixture["case"])
        self.assertEqual("IDENTIFIED", ledger["status"])
        report = GRADER.grade(record, fixture, expectation, CONTRACT)
        self.assertTrue(report["pass"], report["failures"])

    def test_omitting_insufficient_sample_from_scale_readiness_is_rejected(self) -> None:
        """Three of those four trials also dropped the blocking reason."""
        record, fixture, expectation = self._record("SPARSE_BUT_IDENTIFIED")
        record["decision_record"]["scale_readiness"]["blocking_reasons"] = ["IMMATURE_OUTCOMES"]
        report = GRADER.grade(record, fixture, expectation, CONTRACT)
        self.assertFalse(report["pass"])
        self.assertTrue(any("INSUFFICIENT_SAMPLE" in f for f in report["failures"]))

    def test_omitting_insufficient_evidence_from_decision_basis_is_rejected(self) -> None:
        """EX-05-01 trial 6."""
        record, fixture, expectation = self._record("SPARSE_BUT_IDENTIFIED")
        record["decision_record"]["operational"]["decision_basis"] = ["REGISTERED_PRIMARY_KPI"]
        report = GRADER.grade(record, fixture, expectation, CONTRACT)
        self.assertFalse(report["pass"])
        self.assertTrue(any("INSUFFICIENT_EVIDENCE" in f for f in report["failures"]))

    def test_causal_paralysis_leaking_into_the_action_channel_is_rejected(self) -> None:
        """EX-02-01 trial 4: INCONCLUSIVE + NONE_DECIDABLE where the cost metric decided."""
        record, fixture, expectation = self._record("UPSTREAM_ONLY_CONFOUNDED")
        record["recommendation"] = "INCONCLUSIVE"
        record["decision_record"]["operational"]["action"] = "INCONCLUSIVE"
        record["decision_record"]["operational"]["decisive_metric"] = "NONE_DECIDABLE"
        report = GRADER.grade(record, fixture, expectation, CONTRACT)
        self.assertFalse(report["pass"])
        self.assertTrue(any("operational.action must be one of" in f for f in report["failures"]))
        self.assertTrue(any("NONE_DECIDABLE" in f for f in report["failures"]))

    def test_the_repair_did_not_become_permission_to_scale_on_thin_evidence(self) -> None:
        record, fixture, expectation = self._record("SPARSE_BUT_IDENTIFIED")
        treatment = next(a for a in fixture["case"]["arms"]
                         if isinstance(fixture["case"].get(a), dict))
        record["recommendation"] = "SCALE"
        record["decision_record"]["operational"]["action"] = "SCALE"
        record["decision_record"]["operational"]["target"] = treatment
        record["decision_record"]["scale_readiness"] = {"state": "ELIGIBLE",
                                                        "blocking_reasons": []}
        self.assertFalse(GRADER.grade(record, fixture, expectation, CONTRACT)["pass"])


class TheProcedureIsReachableFromTheRuntimeDocumentAlone(unittest.TestCase):
    """Phase 4: knowledge in a test is not knowledge the candidate holds."""

    def test_the_ledger_is_stated_as_an_ordered_procedure(self) -> None:
        normalised = " ".join(V12.split())
        for statement in (
            "#### The identification ledger",
            "Run this **before you read a single outcome count**",
            "Silence is not a defect",
            "**The ledger is now closed.**",
            "No count turns a *no* on questions 1–4 into a *yes*",
            "If your causal channel changed after you saw the numbers",
            "That is the whole of what sparsity is allowed to change.",
            "#### The action is decided separately, and never inherited",
            "`NONE_DECIDABLE` is false in that case, not cautious",
        ):
            with self.subTest(statement=statement[:50]):
                self.assertIn(" ".join(statement.split()), normalised)

    def test_the_ledger_precedes_the_sections_that_read_counts(self) -> None:
        self.assertLess(V12.find("#### The identification ledger"),
                        V12.find("### 5.3 Sample, power and outcome maturity"))
        self.assertLess(V12.find("#### The identification ledger"),
                        V12.find("### 5.4 Compute the registered outcome"))

    def test_every_field_that_sparsity_may_touch_is_named(self) -> None:
        block = V12.split("Thin counts are not discarded.")[1].split("That is the whole")[0]
        for field in ("operational.action", "INCONCLUSIVE", "decision_basis",
                      "INSUFFICIENT_EVIDENCE", "scale_readiness", "INSUFFICIENT_SAMPLE"):
            with self.subTest(field=field):
                self.assertIn(field, block)

    def test_both_leakage_directions_are_forbidden(self) -> None:
        block = V12.split("Both directions of leakage are forbidden")[1]
        self.assertIn("Causal into action", block)
        self.assertIn("Action into causal", block)


if __name__ == "__main__":
    unittest.main(verbosity=2)
