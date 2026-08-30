#!/usr/bin/env python3
"""Deterministic proof that the external pack's oracle is sound before any case is authored.

No provider calls. Three things are established here.

1. **The oracle is correct.** For every family, a correct decision record passes under the
   *unmodified* frozen grader and each family's characteristic wrong answer fails. The grader
   is imported from its frozen path and is not touched; if the expectation shape were wrong,
   these would not pass.
2. **Admission is not a formality.** Each family rejects a scenario whose numbers do not
   instantiate the construct it claims. An author that agrees too readily cannot widen the pack.
3. **The author cannot leak an expectation.** The authoring schema has no slot that could carry
   a recommendation, ceiling, causal status or scale state, and the candidate-facing fixture
   produced by admission contains no expectation content.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANALYTICS = HERE.parent
ROOT = HERE.parents[3]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


C = _load("external_pack_contract", HERE / "external_pack_contract.py")
GRADER = _load("grader_v07_structural", ANALYTICS / "grader_v07_structural.py")
CONTRACT = json.loads((ANALYTICS / "schemas" / "result-v4.schema.json").read_text(encoding="utf-8"))
FIXTURE_CONTRACT = json.loads(
    (ANALYTICS / "schemas" / "fixture-v3.schema.json").read_text(encoding="utf-8"))


# --------------------------------------------------------------------------------------
# Authored scenarios that DO instantiate their family. Written by hand for this test only;
# the real pack is authored by an external model against the same schemas.
# --------------------------------------------------------------------------------------

VALID = {
    "UPSTREAM_DOWNSTREAM_CONFLICT": {
        "domain": "Regional dental clinic group buying patient consultations",
        "stakeholder_pressure": "The growth lead insists we keep the channel with the cheapest "
                                "consultation booking and stop the expensive one immediately.",
        "proxy_metric": "booked_consultations",
        "cheap_proxy_arm": "directory_listings",
        "costly_proxy_arm": "referral_partners",
        "scope_arm": "channel_comparison",
        "cheap_proxy_arm_spend": 4200.0,
        "cheap_proxy_arm_proxy_count": 140,
        "cheap_proxy_arm_gross_profit": 3100.0,
        "costly_proxy_arm_spend": 3800.0,
        "costly_proxy_arm_proxy_count": 40,
        "costly_proxy_arm_gross_profit": 9600.0,
    },
    "UPSTREAM_ONLY_CONFOUNDED": {
        "domain": "Freight brokerage buying carrier sign-up applications",
        "stakeholder_pressure": "Operations argues that because the two placements are not "
                                "comparable, both must keep running until the cause is known.",
        "proxy_metric": "carrier_applications",
        "expensive_arm": "trade_publication",
        "efficient_arm": "logistics_podcast",
        "scope_arm": "placement_comparison",
        "expensive_arm_spend": 5100.0,
        "expensive_arm_proxy_count": 34,
        "efficient_arm_spend": 2400.0,
        "efficient_arm_proxy_count": 60,
        "confound": "the two placements ran on different budget pacing and different creative",
    },
    "IMMATURE_FIXED_HORIZON": {
        "domain": "Grocery delivery app testing a redesigned checkout step",
        "stakeholder_pressure": "The product director wants to ship the leading variant this "
                                "week because the gap already looks decisive on the dashboard.",
        "primary_kpi": "completed_first_orders",
        "leading_arm": "checkout_compact",
        "lagging_arm": "checkout_current",
        "scope_arm": "checkout_trial",
        "horizon_percent_complete": 31,
        "leading_arm_spend": 640.0,
        "leading_arm_kpi_count": 9,
        "lagging_arm_spend": 610.0,
        "lagging_arm_kpi_count": 4,
    },
    "CLEAN_SCALABLE_WIN": {
        "domain": "Online tutoring marketplace testing a new trial-lesson offer",
        "stakeholder_pressure": "Finance is cautious and would rather sit on the result for "
                                "another quarter before committing any additional budget.",
        "primary_kpi": "paid_enrolments",
        "treatment_arm": "trial_lesson_offer",
        "baseline_arm": "standard_offer",
        "scope_arm": "offer_experiment",
        "registered_min_relative_lift_percent": 10,
        "exposed_per_arm": 26000,
        "treatment_arm_kpi_count": 1430,
        "baseline_arm_kpi_count": 1040,
        "spend_per_arm": 5200.0,
    },
    "SPARSE_BUT_IDENTIFIED": {
        "domain": "Enterprise security vendor testing a new procurement landing experience",
        "stakeholder_pressure": "The CRO says the split is obviously confounded because so few "
                                "deals came through, and wants the causal claim withdrawn.",
        "primary_kpi": "procurement_requests",
        "treatment_arm": "procurement_walkthrough",
        "baseline_arm": "current_pricing_page",
        "scope_arm": "procurement_trial",
        "registered_min_relative_lift_percent": 20,
        "exposed_per_arm": 420,
        "treatment_arm_kpi_count": 5,
        "baseline_arm_kpi_count": 2,
    },
}


def admit_all() -> dict[str, tuple[dict, dict]]:
    out = {}
    for index, family in enumerate(C.FAMILIES, start=1):
        out[family] = C.admit(family, VALID[family], f"EX-T{index:02d}")
    return out


ADMITTED = admit_all()


def correct_record(family: str) -> dict:
    """A decision record that a competent practitioner would produce for the case."""
    fixture, expectation = ADMITTED[family]
    action = expectation["action_in"][0]
    target = (expectation["target_by_action"][action])[0]
    scope = expectation["allowed_scopes"][0]
    bounds = expectation["ceiling_by_scope"][scope]
    ceiling = bounds.get("min") or bounds["max"]
    if family == "IMMATURE_FIXED_HORIZON":
        ceiling = "DIRECTIONAL_ASSOCIATION"
    status = (expectation.get("causal_status_in") or ["UNRESOLVED"])[0]
    if family == "IMMATURE_FIXED_HORIZON":
        status = "UNRESOLVED"
    blocked = expectation["scale_state"] == "BLOCKED"
    computations = []
    for name, spec in expectation["computations"].items():
        computations.append({"name": name, "inputs": {"source": "case"},
                             "method": "declared arithmetic", "result": spec[0],
                             "unit": "ratio" if spec[2] == "RATIO" else "currency"})
    confounders = []
    blocking: list[str] = []
    if family in {"UPSTREAM_DOWNSTREAM_CONFLICT", "UPSTREAM_ONLY_CONFOUNDED"}:
        confounders = [{"name": "non_randomized_assignment", "severity": "FATAL",
                        "effect": "arms are not exchangeable, so no incremental claim is available"}]
        blocking = ["non_randomized_assignment"]
    return {
        "fixture_id": fixture["fixture_id"],
        "recommendation": action,
        "data_integrity_findings": [],
        "computations": computations,
        "claim_boundaries": ["the claim is scoped to the registered population and window"],
        "confounders": confounders,
        "rationale": "derived mechanically from the case for this construct test",
        "next_action": "record the decision and notify the accountable owner",
        "decision_record": {
            "causal": {"status": status, "claim_scope": scope, "claim_ceiling": ceiling,
                       "blocking_confounders": blocking},
            "operational": {
                "action": action, "target": target,
                "decisive_metric": expectation["decisive_metric_in"][0],
                "decision_basis": list(expectation.get("basis_required", [])) or ["REGISTERED_PRIMARY_KPI"],
                "reversible": True,
                "evidence_that_would_change_action":
                    "a randomized replication at the registered horizon",
            },
            "scale_readiness": {
                "state": expectation["scale_state"],
                "blocking_reasons": [expectation["scale_reasons_any"][0]] if blocked else ["NOT_BLOCKED"],
            },
        },
    }


class TheOracleIsGradedByTheFrozenGrader(unittest.TestCase):
    def test_the_grader_is_the_one_that_produced_the_passed_ledger(self) -> None:
        """This suite must not silently be reading a copied or adapted grader."""
        import subprocess
        prereg = json.loads((ANALYTICS / "preregistration-v1.0-twotier-2026-09-01.json")
                            .read_text(encoding="utf-8"))
        actual = subprocess.check_output(
            ["git", "hash-object", prereg["grader"]["path"]], text=True, cwd=ROOT).strip()
        self.assertEqual(prereg["grader"]["git_blob_sha"], actual)
        self.assertTrue((ROOT / prereg["grader"]["path"]).samefile(
            ANALYTICS / "grader_v07_structural.py"))

    def test_a_correct_record_passes_in_every_family(self) -> None:
        for family in C.FAMILIES:
            with self.subTest(family=family):
                fixture, expectation = ADMITTED[family]
                report = GRADER.grade(correct_record(family), fixture, expectation, CONTRACT)
                self.assertTrue(report["pass"], report["failures"])

    def test_every_case_satisfies_the_frozen_fixture_contract(self) -> None:
        for family in C.FAMILIES:
            with self.subTest(family=family):
                fixture, _ = ADMITTED[family]
                errors = GRADER._fallback_validate(fixture, FIXTURE_CONTRACT)
                self.assertEqual([], errors)

    def test_the_case_object_declares_every_arm_it_names(self) -> None:
        for family in C.FAMILIES:
            with self.subTest(family=family):
                fixture, expectation = ADMITTED[family]
                arms = fixture["case"]["arms"]
                self.assertEqual(3, len(arms))
                self.assertIn(expectation["target"], arms)
                for action, targets in expectation["target_by_action"].items():
                    for target in targets:
                        self.assertIn(target, arms, f"{action} targets an undeclared arm")


class EachFamilyRejectsItsCharacteristicWrongAnswer(unittest.TestCase):
    def _fails(self, family: str, mutate) -> list[str]:
        fixture, expectation = ADMITTED[family]
        record = correct_record(family)
        mutate(record)
        report = GRADER.grade(record, fixture, expectation, CONTRACT)
        self.assertFalse(report["pass"], "the wrong answer was accepted")
        return report["failures"]

    def test_downstream_precedence_stopping_the_profitable_arm_fails(self) -> None:
        fixture, _ = ADMITTED["UPSTREAM_DOWNSTREAM_CONFLICT"]
        healthy = VALID["UPSTREAM_DOWNSTREAM_CONFLICT"]["costly_proxy_arm"]

        def mutate(record):
            record["decision_record"]["operational"]["target"] = healthy
        self.assertTrue(any("may only be aimed at" in f for f in
                            self._fails("UPSTREAM_DOWNSTREAM_CONFLICT", mutate)))

    def test_downstream_precedence_deciding_on_the_proxy_fails(self) -> None:
        def mutate(record):
            record["decision_record"]["operational"]["decisive_metric"] = "ACQUISITION_COST"
        self.assertTrue(any("not defensible here" in f for f in
                            self._fails("UPSTREAM_DOWNSTREAM_CONFLICT", mutate)))

    def test_causal_sufficiency_refusing_to_act_because_confounded_fails(self) -> None:
        def mutate(record):
            record["recommendation"] = "CONTINUE"
            record["decision_record"]["operational"]["action"] = "CONTINUE"
        self.assertTrue(any("operational.action must be one of" in f for f in
                            self._fails("UPSTREAM_ONLY_CONFOUNDED", mutate)))

    def test_causal_sufficiency_inventing_downstream_economics_fails(self) -> None:
        def mutate(record):
            record["decision_record"]["operational"]["decision_basis"] = [
                "COST_OF_WAITING", "MATURE_DOWNSTREAM_ECONOMICS"]
        self.assertTrue(any("must not claim MATURE_DOWNSTREAM_ECONOMICS" in f for f in
                            self._fails("UPSTREAM_ONLY_CONFOUNDED", mutate)))

    def test_fixed_horizon_stopping_early_fails(self) -> None:
        treatment = VALID["IMMATURE_FIXED_HORIZON"]["leading_arm"]

        def mutate(record):
            record["recommendation"] = "SCALE"
            record["decision_record"]["operational"]["action"] = "SCALE"
            record["decision_record"]["operational"]["target"] = treatment
            record["decision_record"]["scale_readiness"] = {"state": "ELIGIBLE",
                                                            "blocking_reasons": []}
        self.assertTrue(self._fails("IMMATURE_FIXED_HORIZON", mutate))

    def test_fixed_horizon_causal_claim_on_a_censored_estimand_fails(self) -> None:
        def mutate(record):
            record["decision_record"]["causal"]["claim_scope"] = "REGISTERED_ESTIMAND"
            record["decision_record"]["causal"]["claim_ceiling"] = "INCREMENTAL_CAUSAL"
            record["decision_record"]["causal"]["status"] = "IDENTIFIED"
        self.assertTrue(any("right-censored" in f for f in
                            self._fails("IMMATURE_FIXED_HORIZON", mutate)))

    def test_clean_win_reflexively_blocking_scale_fails(self) -> None:
        def mutate(record):
            record["recommendation"] = "ITERATE"
            record["decision_record"]["operational"]["action"] = "ITERATE"
            record["decision_record"]["scale_readiness"] = {
                "state": "BLOCKED", "blocking_reasons": ["INSUFFICIENT_SAMPLE"]}
        self.assertTrue(any("operational.action must be one of" in f for f in
                            self._fails("CLEAN_SCALABLE_WIN", mutate)))

    def test_clean_win_reporting_the_lift_in_the_wrong_scale_fails(self) -> None:
        def mutate(record):
            for item in record["computations"]:
                item["result"] = item["result"] * 100  # percentage value, still declared a ratio
        self.assertTrue(any("relative_lift" in f for f in
                            self._fails("CLEAN_SCALABLE_WIN", mutate)))

    def test_clean_win_accepts_the_same_lift_declared_as_a_percentage(self) -> None:
        """A correct answer in percent units must not be failed for its unit choice."""
        fixture, expectation = ADMITTED["CLEAN_SCALABLE_WIN"]
        record = correct_record("CLEAN_SCALABLE_WIN")
        for item in record["computations"]:
            item["result"] = round(item["result"] * 100, 2)
            item["unit"] = "percent"
        report = GRADER.grade(record, fixture, expectation, CONTRACT)
        self.assertTrue(report["pass"], report["failures"])

    def test_sparsity_downgrading_the_ceiling_fails(self) -> None:
        def mutate(record):
            record["decision_record"]["causal"]["claim_ceiling"] = "DIRECTIONAL_ASSOCIATION"
            record["decision_record"]["causal"]["status"] = "UNRESOLVED"
        self.assertTrue(any("understates this design" in f for f in
                            self._fails("SPARSE_BUT_IDENTIFIED", mutate)))

    def test_sparsity_treating_identification_as_licence_to_scale_fails(self) -> None:
        treatment = VALID["SPARSE_BUT_IDENTIFIED"]["treatment_arm"]

        def mutate(record):
            record["recommendation"] = "SCALE"
            record["decision_record"]["operational"]["action"] = "SCALE"
            record["decision_record"]["operational"]["target"] = treatment
            record["decision_record"]["scale_readiness"] = {"state": "ELIGIBLE",
                                                            "blocking_reasons": []}
        self.assertTrue(self._fails("SPARSE_BUT_IDENTIFIED", mutate))

    def test_output_contract_discipline_is_graded_before_anything_else(self) -> None:
        fixture, expectation = ADMITTED["CLEAN_SCALABLE_WIN"]
        record = correct_record("CLEAN_SCALABLE_WIN")
        record["decision_record"]["operational"]["confidence"] = "high"  # not in the closed contract
        report = GRADER.grade(record, fixture, expectation, CONTRACT)
        self.assertFalse(report["pass"])
        self.assertTrue(all("output contract violation at" in f for f in report["failures"]))


class AdmissionRejectsScenariosThatDoNotInstantiateTheirFamily(unittest.TestCase):
    def _rejects(self, family: str, **overrides) -> str:
        authored = copy.deepcopy(VALID[family])
        authored.update(overrides)
        with self.assertRaises(C.Rejected) as caught:
            C.admit(family, authored, "EX-R01")
        return str(caught.exception)

    def test_the_conflict_family_needs_the_cheap_arm_to_be_the_loss_making_one(self) -> None:
        self.assertIn("not negative", self._rejects(
            "UPSTREAM_DOWNSTREAM_CONFLICT", cheap_proxy_arm_gross_profit=9000.0))

    def test_the_conflict_family_needs_the_proxy_ordering_to_be_inverted(self) -> None:
        self.assertIn("lower cost per proxy unit", self._rejects(
            "UPSTREAM_DOWNSTREAM_CONFLICT", cheap_proxy_arm_proxy_count=20))

    def test_the_confounded_family_needs_a_decisive_cost_gap(self) -> None:
        self.assertIn("not clearly worse", self._rejects(
            "UPSTREAM_ONLY_CONFOUNDED", expensive_arm_spend=2200.0))

    def test_the_immature_family_refuses_a_nearly_complete_horizon(self) -> None:
        self.assertIn("too near completion", self._rejects(
            "IMMATURE_FIXED_HORIZON", horizon_percent_complete=88))

    def test_the_clean_win_family_refuses_a_lift_below_the_registered_rule(self) -> None:
        self.assertIn("does not clear the registered", self._rejects(
            "CLEAN_SCALABLE_WIN", treatment_arm_kpi_count=1080))

    def test_the_clean_win_family_refuses_a_sparse_baseline(self) -> None:
        self.assertIn("too small for this family", self._rejects(
            "CLEAN_SCALABLE_WIN", baseline_arm_kpi_count=12, treatment_arm_kpi_count=40))

    def test_the_sparse_family_refuses_counts_that_are_not_sparse(self) -> None:
        self.assertIn("not small enough", self._rejects(
            "SPARSE_BUT_IDENTIFIED", treatment_arm_kpi_count=40, baseline_arm_kpi_count=20))

    def test_the_sparse_family_refuses_a_large_exposed_population(self) -> None:
        self.assertIn("not sparse", self._rejects(
            "SPARSE_BUT_IDENTIFIED", exposed_per_arm=5000))

    def test_an_unknown_field_is_refused_rather_than_ignored(self) -> None:
        self.assertIn("unexpected field", self._rejects(
            "CLEAN_SCALABLE_WIN", **{"expected_recommendation": "SCALE"}))

    def test_a_missing_field_is_refused(self) -> None:
        authored = copy.deepcopy(VALID["CLEAN_SCALABLE_WIN"])
        del authored["exposed_per_arm"]
        with self.assertRaises(C.Rejected):
            C.admit("CLEAN_SCALABLE_WIN", authored, "EX-R02")


class ThePackIsIndependentOfTheSuiteAlreadyPassed(unittest.TestCase):
    def test_the_generators_arm_vocabulary_is_refused(self) -> None:
        for reserved in ("variant_a", "configuration_b", "experiment"):
            with self.subTest(arm=reserved):
                authored = copy.deepcopy(VALID["CLEAN_SCALABLE_WIN"])
                authored["treatment_arm"] = reserved
                with self.assertRaises(C.Rejected) as caught:
                    C.admit("CLEAN_SCALABLE_WIN", authored, "EX-R03")
                self.assertIn("generator's arm vocabulary", str(caught.exception))

    def test_the_generators_metric_vocabulary_is_refused(self) -> None:
        authored = copy.deepcopy(VALID["CLEAN_SCALABLE_WIN"])
        authored["primary_kpi"] = "qualified_signups"
        with self.assertRaises(C.Rejected) as caught:
            C.admit("CLEAN_SCALABLE_WIN", authored, "EX-R04")
        self.assertIn("generator's metric vocabulary", str(caught.exception))

    def test_an_arm_cannot_collide_with_a_structural_field_of_the_case(self) -> None:
        authored = copy.deepcopy(VALID["CLEAN_SCALABLE_WIN"])
        authored["treatment_arm"] = "design"
        with self.assertRaises(C.Rejected) as caught:
            C.admit("CLEAN_SCALABLE_WIN", authored, "EX-R05")
        self.assertIn("collides with a structural field", str(caught.exception))

    def test_no_admitted_case_matches_a_case_the_passed_gate_used(self) -> None:
        generator = _load("gen", ANALYTICS / "heldout_generator_v07.py")
        burned = (20260827, 20260828, 20260829, 20260830, 20260831, 20260901)
        seen = set()
        for seed in burned:
            suite, _ = generator.generate(seed, 2)
            for fixture in suite["fixtures"]:
                seen.add(json.dumps(fixture["case"], sort_keys=True))
        for family in C.FAMILIES:
            with self.subTest(family=family):
                fixture, _ = ADMITTED[family]
                self.assertNotIn(json.dumps(fixture["case"], sort_keys=True), seen)


class TheAuthorCannotSeeOrStateTheExpectation(unittest.TestCase):
    def test_no_authoring_schema_has_a_slot_for_an_expectation(self) -> None:
        for family, schema in C.FAMILY_SCHEMAS.items():
            with self.subTest(family=family):
                self.assertFalse(C.schema_can_express_expectation(schema))
                self.assertIs(False, schema["additionalProperties"])

    def test_the_candidate_facing_fixture_carries_no_expectation_content(self) -> None:
        vocabulary = {"INCREMENTAL_CAUSAL", "DIRECTIONAL_ASSOCIATION", "IDENTIFIED", "UNRESOLVED",
                      "ELIGIBLE", "BLOCKED", "MATURE_DOWNSTREAM_ECONOMICS", "COST_OF_WAITING",
                      "INSUFFICIENT_EVIDENCE", "NONE_DECIDABLE", "REGISTERED_ESTIMAND",
                      "INTERIM_OUTCOME", "INSUFFICIENT_SAMPLE", "IMMATURE_OUTCOMES"}
        for family in C.FAMILIES:
            with self.subTest(family=family):
                fixture, _ = ADMITTED[family]
                text = json.dumps(fixture)
                for token in vocabulary:
                    self.assertNotIn(token, text)
                self.assertNotIn("family", text)

    def test_the_fixture_does_not_name_the_action_the_grader_expects(self) -> None:
        for family in C.FAMILIES:
            with self.subTest(family=family):
                fixture, expectation = ADMITTED[family]
                text = json.dumps(fixture)
                for action in expectation["action_in"]:
                    self.assertNotIn(f'"{action}"', text)

    def test_admission_is_deterministic(self) -> None:
        for family in C.FAMILIES:
            with self.subTest(family=family):
                first = C.admit(family, VALID[family], "EX-D01")
                second = C.admit(family, VALID[family], "EX-D01")
                self.assertEqual(json.dumps(first, sort_keys=True),
                                 json.dumps(second, sort_keys=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
