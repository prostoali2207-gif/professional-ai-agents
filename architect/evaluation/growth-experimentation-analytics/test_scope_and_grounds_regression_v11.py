#!/usr/bin/env python3
"""Targeted regressions for the four failure classes of external run `33293694601`.

No provider calls. The frozen grader `grader_v07_structural.py` is imported unmodified and does
all the judging; nothing here is a new scorer.

The point of class A is that `experiment` must never be a magic token. So the recognition rule the
successor encodes — *the declared identifier that keys no per-arm outcome block is the comparison
as a whole* — is implemented here once, as a reference implementation, and then run against:

  * every case the frozen generator produces, across several seeds;
  * cases whose identifiers are permuted into unrelated vocabulary;
  * an adversarial case in which the **treatment arm is literally named `experiment`** and the
    real scope identifier is named something else. A candidate matching on the word gets this
    exactly backwards; the structural rule gets it right.

Classes B, C and D are replayed as the observed failing records against the frozen grader: each
observed failure must still fail, and its corrected counterpart must pass. That is what stops the
repair from being prose that changed nothing.
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
V11 = (ROOT / "architect/research/growth-experimentation-analytics"
       / "professional-model-consolidated-v1.1.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------------------------
# The recognition rule, exactly as the successor states it.
# ---------------------------------------------------------------------------------------------

def comparison_level_identifier(case: dict) -> str | None:
    """Return the declared identifier that keys no per-arm outcome block, or None if ambiguous.

    This reads only the structure of the case. It never looks at what anything is called.
    """
    unkeyed = [arm for arm in case["arms"] if not isinstance(case.get(arm), dict)]
    return unkeyed[0] if len(unkeyed) == 1 else None


class TheRecognitionRuleIsDecidableOnEveryRealCase(unittest.TestCase):
    def test_it_finds_exactly_one_scope_identifier_in_every_generated_case(self) -> None:
        for seed in (20260827, 20260829, 20260901, 20261115):
            suite, oracle = GENERATOR.generate(seed, 2)
            for fixture in suite["fixtures"]:
                with self.subTest(seed=seed, fixture=fixture["fixture_id"]):
                    self.assertIsNotNone(comparison_level_identifier(fixture["case"]))

    def test_it_agrees_with_the_frozen_oracle_wherever_the_oracle_names_a_scope(self) -> None:
        """The rule is not merely decidable; it returns what the oracle independently expects."""
        checked = 0
        for seed in (20260827, 20260901, 20261115):
            suite, oracle = GENERATOR.generate(seed, 2)
            expectations = oracle["expectations"]
            for fixture in suite["fixtures"]:
                expectation = expectations[fixture["fixture_id"]]
                for action in ("CONTINUE", "INCONCLUSIVE"):
                    targets = (expectation.get("target_by_action") or {}).get(action)
                    if not targets:
                        continue
                    with self.subTest(seed=seed, fixture=fixture["fixture_id"], action=action):
                        self.assertIn(comparison_level_identifier(fixture["case"]), targets)
                        checked += 1
        self.assertGreater(checked, 10, "the agreement check exercised too few cases")

    def test_it_works_on_externally_authored_vocabulary(self) -> None:
        equivalence = _load("ext_tests", EXTERNAL / "test_external_pack_contract.py")
        for family in PACK.FAMILIES:
            fixture, expectation = equivalence.ADMITTED[family]
            with self.subTest(family=family):
                found = comparison_level_identifier(fixture["case"])
                self.assertIsNotNone(found)
                for action in ("CONTINUE", "INCONCLUSIVE"):
                    targets = (expectation.get("target_by_action") or {}).get(action)
                    if targets:
                        self.assertIn(found, targets)


class ExperimentIsNeverAMagicToken(unittest.TestCase):
    """The trap that the v1.0 gate could not have caught, because it never varied the vocabulary."""

    ALIASES = ("ui_experiment", "pricing_test", "sort_algorithm_test",
               "onboarding_experience_test", "alpha", "zzz_scope", "q3_rollout", "variant_c")

    def _renamed(self, mapping: dict[str, str]) -> dict:
        suite, _oracle = GENERATOR.generate(20260901, 2)
        fixture = next(f for f in suite["fixtures"] if f["fixture_id"].startswith("HO-IFH"))
        case = json.loads(json.dumps(fixture["case"]))
        for old, new in mapping.items():
            if old in case:
                case[new] = case.pop(old)
            case["arms"] = [new if arm == old else arm for arm in case["arms"]]
        return case

    def test_the_scope_identifier_is_found_under_every_alias(self) -> None:
        for alias in self.ALIASES:
            with self.subTest(alias=alias):
                case = self._renamed({"experiment": alias})
                self.assertEqual(alias, comparison_level_identifier(case))

    def test_an_arm_named_experiment_is_not_mistaken_for_the_scope(self) -> None:
        """The decisive trap: the word sits on an arm and the scope is called something else."""
        suite, _oracle = GENERATOR.generate(20260901, 2)
        fixture = next(f for f in suite["fixtures"] if f["fixture_id"].startswith("HO-IFH"))
        case = json.loads(json.dumps(fixture["case"]))
        arm = next(a for a in case["arms"] if a != "experiment" and isinstance(case.get(a), dict))
        case["experiment_scope"] = case.pop("experiment", None)
        case["arms"] = ["experiment_scope" if a == "experiment" else a for a in case["arms"]]
        case.pop("experiment_scope", None)
        case[  # the treatment arm now carries the word, and it keys real measurements
            "experiment"] = case.pop(arm)
        case["arms"] = ["experiment" if a == arm else a for a in case["arms"]]

        found = comparison_level_identifier(case)
        self.assertEqual("experiment_scope", found)
        self.assertNotEqual("experiment", found,
                            "the rule matched a word instead of reading the structure")

    def test_the_rule_refuses_rather_than_guesses_when_no_scope_is_declared(self) -> None:
        suite, _oracle = GENERATOR.generate(20260901, 2)
        fixture = next(f for f in suite["fixtures"] if f["fixture_id"].startswith("HO-IFH"))
        case = json.loads(json.dumps(fixture["case"]))
        case["arms"] = [a for a in case["arms"] if a != "experiment"]
        self.assertIsNone(comparison_level_identifier(case))

    def test_the_successor_states_the_refusal_path_for_that_case(self) -> None:
        self.assertIn("the case declares no comparison-level scope", V11)


# ---------------------------------------------------------------------------------------------
# Replays of the observed failures against the frozen grader.
# ---------------------------------------------------------------------------------------------

def base_record(fixture: dict, expectation: dict, action: str, target: str) -> dict:
    computations = [{"name": name, "inputs": {"source": "case"}, "method": "declared arithmetic",
                     "result": spec[0], "unit": "ratio" if spec[2] == "RATIO" else "currency"}
                    for name, spec in expectation["computations"].items()]
    blocked = expectation["scale_state"] == "BLOCKED"
    return {
        "fixture_id": fixture["fixture_id"],
        "recommendation": action,
        "data_integrity_findings": [],
        "computations": computations,
        "claim_boundaries": ["scoped to the registered population and window"],
        "confounders": [],
        "rationale": "replay",
        "next_action": "record the decision",
        "decision_record": {
            "causal": {"status": (expectation.get("causal_status_in") or ["UNRESOLVED"])[0],
                       "claim_scope": expectation["allowed_scopes"][0],
                       "claim_ceiling": "DIRECTIONAL_ASSOCIATION",
                       "blocking_confounders": []},
            "operational": {"action": action, "target": target,
                            "decisive_metric": expectation["decisive_metric_in"][0],
                            "decision_basis": list(expectation.get("basis_required") or
                                                   ["REGISTERED_PRIMARY_KPI"]),
                            "reversible": True,
                            "evidence_that_would_change_action": "a powered replication"},
            "scale_readiness": {
                "state": expectation["scale_state"],
                "blocking_reasons": [expectation["scale_reasons_any"][0]] if blocked
                else ["NOT_BLOCKED"]},
        },
    }


class ObservedFailuresStillFailAndTheirRepairsPass(unittest.TestCase):
    """Each replay uses external vocabulary, so none of it can pass on the token `experiment`."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.ext = _load("ext_tests2", EXTERNAL / "test_external_pack_contract.py")

    def _grade(self, family: str, mutate=None, action: str | None = None,
               target: str | None = None):
        fixture, expectation = self.ext.ADMITTED[family]
        act = action or expectation["action_in"][0]
        tgt = target or (expectation["target_by_action"][act])[0]
        record = base_record(fixture, expectation, act, tgt)
        if family in {"CLEAN_SCALABLE_WIN", "SPARSE_BUT_IDENTIFIED"}:
            record["decision_record"]["causal"]["claim_ceiling"] = "INCREMENTAL_CAUSAL"
            record["decision_record"]["causal"]["status"] = "IDENTIFIED"
        if mutate:
            mutate(record, fixture, expectation)
        return GRADER.grade(record, fixture, expectation, CONTRACT)

    # --- class A -----------------------------------------------------------------------------

    def test_A_continue_aimed_at_an_arm_fails(self) -> None:
        fixture, _ = self.ext.ADMITTED["IMMATURE_FIXED_HORIZON"]
        arm = next(a for a in fixture["case"]["arms"]
                   if isinstance(fixture["case"].get(a), dict))
        report = self._grade("IMMATURE_FIXED_HORIZON", target=arm)
        self.assertFalse(report["pass"])
        self.assertTrue(any("may only be aimed at" in f for f in report["failures"]))

    def test_A_continue_aimed_at_the_recognised_scope_passes(self) -> None:
        fixture, _ = self.ext.ADMITTED["IMMATURE_FIXED_HORIZON"]
        scope = comparison_level_identifier(fixture["case"])
        report = self._grade("IMMATURE_FIXED_HORIZON", target=scope)
        self.assertTrue(report["pass"], report["failures"])

    def test_A_inconclusive_aimed_at_an_arm_fails(self) -> None:
        fixture, _ = self.ext.ADMITTED["SPARSE_BUT_IDENTIFIED"]
        arm = next(a for a in fixture["case"]["arms"]
                   if isinstance(fixture["case"].get(a), dict))
        report = self._grade("SPARSE_BUT_IDENTIFIED", action="INCONCLUSIVE", target=arm)
        self.assertFalse(report["pass"])

    def test_A_the_fixture_id_as_target_fails(self) -> None:
        for family in ("IMMATURE_FIXED_HORIZON", "SPARSE_BUT_IDENTIFIED"):
            with self.subTest(family=family):
                fixture, _ = self.ext.ADMITTED[family]
                report = self._grade(family, target=fixture["fixture_id"])
                self.assertFalse(report["pass"])
                self.assertTrue(any("is not one of the declared arms" in f
                                    for f in report["failures"]))

    # --- class B -----------------------------------------------------------------------------

    def test_B_inconclusive_without_insufficient_evidence_fails(self) -> None:
        def mutate(record, _fixture, _expectation):
            record["decision_record"]["operational"]["decision_basis"] = ["REGISTERED_PRIMARY_KPI"]
        report = self._grade("SPARSE_BUT_IDENTIFIED", mutate=mutate, action="INCONCLUSIVE")
        self.assertFalse(report["pass"])
        self.assertTrue(any("INSUFFICIENT_EVIDENCE" in f for f in report["failures"]))

    def test_B_a_stop_without_cost_of_waiting_fails(self) -> None:
        def mutate(record, _fixture, _expectation):
            record["decision_record"]["operational"]["decision_basis"] = ["ACQUISITION_COST_DIAGNOSTIC"]
        report = self._grade("UPSTREAM_ONLY_CONFOUNDED", mutate=mutate)
        self.assertFalse(report["pass"])
        self.assertTrue(any("COST_OF_WAITING" in f for f in report["failures"]))

    def test_B_the_complete_grounds_pass(self) -> None:
        for family in ("SPARSE_BUT_IDENTIFIED", "UPSTREAM_ONLY_CONFOUNDED"):
            with self.subTest(family=family):
                self.assertTrue(self._grade(family)["pass"])

    # --- class C -----------------------------------------------------------------------------

    def test_C1_decision_paralysis_against_mature_downstream_economics_fails(self) -> None:
        """The EX-01-02 t1 failure, replayed."""
        fixture, expectation = self.ext.ADMITTED["UPSTREAM_DOWNSTREAM_CONFLICT"]
        scope = comparison_level_identifier(fixture["case"])
        record = base_record(fixture, expectation, "INCONCLUSIVE", scope)
        record["decision_record"]["operational"]["decisive_metric"] = "NONE_DECIDABLE"
        record["decision_record"]["operational"]["decision_basis"] = ["INSUFFICIENT_EVIDENCE"]
        report = GRADER.grade(record, fixture, expectation, CONTRACT)
        self.assertFalse(report["pass"])
        self.assertTrue(any("operational.action must be one of" in f for f in report["failures"]))
        self.assertTrue(any("NONE_DECIDABLE" in f for f in report["failures"]))

    def test_C1_acting_on_the_mature_downstream_economics_passes(self) -> None:
        self.assertTrue(self._grade("UPSTREAM_DOWNSTREAM_CONFLICT")["pass"])

    def test_C2_sparsity_lowering_the_causal_claim_fails(self) -> None:
        """The EX-05-02 t6 failure, replayed."""
        def mutate(record, _fixture, _expectation):
            record["decision_record"]["causal"]["status"] = "UNRESOLVED"
            record["decision_record"]["causal"]["claim_ceiling"] = "NONE"
        report = self._grade("SPARSE_BUT_IDENTIFIED", mutate=mutate)
        self.assertFalse(report["pass"])
        self.assertTrue(any("understates this design" in f for f in report["failures"]))

    def test_C2_keeping_identification_while_refusing_to_act_passes(self) -> None:
        report = self._grade("SPARSE_BUT_IDENTIFIED", action="INCONCLUSIVE")
        self.assertTrue(report["pass"], report["failures"])

    def test_C2_the_repair_did_not_become_permission_to_scale(self) -> None:
        """Repairing an understated ceiling must not license acting on thin evidence."""
        fixture, expectation = self.ext.ADMITTED["SPARSE_BUT_IDENTIFIED"]
        treatment = next(a for a in fixture["case"]["arms"]
                         if isinstance(fixture["case"].get(a), dict))
        record = base_record(fixture, expectation, "SCALE", treatment)
        record["decision_record"]["causal"] = {"status": "IDENTIFIED",
                                               "claim_scope": "REGISTERED_ESTIMAND",
                                               "claim_ceiling": "INCREMENTAL_CAUSAL",
                                               "blocking_confounders": []}
        record["decision_record"]["scale_readiness"] = {"state": "ELIGIBLE",
                                                        "blocking_reasons": []}
        self.assertFalse(GRADER.grade(record, fixture, expectation, CONTRACT)["pass"])

    # --- class D -----------------------------------------------------------------------------

    def test_D_scale_readiness_nested_under_operational_is_rejected(self) -> None:
        """The three misplacements observed; the frozen contract already refuses them."""
        fixture, expectation = self.ext.ADMITTED["CLEAN_SCALABLE_WIN"]
        record = base_record(fixture, expectation, "SCALE",
                             expectation["target_by_action"]["SCALE"][0])
        record["decision_record"]["causal"]["claim_ceiling"] = "INCREMENTAL_CAUSAL"
        record["decision_record"]["causal"]["status"] = "IDENTIFIED"
        record["decision_record"]["operational"]["scale_readiness"] = \
            record["decision_record"].pop("scale_readiness")
        report = GRADER.grade(record, fixture, expectation, CONTRACT)
        self.assertFalse(report["pass"])
        self.assertTrue(all("output contract violation at" in f for f in report["failures"]))

    def test_D_the_successor_names_the_nesting_violation(self) -> None:
        self.assertIn("`scale_readiness` is nested inside `operational`", V11)

    def test_D_the_successor_constrains_prose_length(self) -> None:
        self.assertIn("Keep every prose field short", V11)


class TheRepairedRulesAreReachableFromTheRuntimeDocumentAlone(unittest.TestCase):
    """Phase 4: knowledge in a grader is not knowledge the candidate holds."""

    def test_every_class_a_to_d_repair_is_stated_in_the_candidate_not_only_the_tests(self) -> None:
        for statement in (
            "The declared identifier that keys no such block is the registered comparison",
            "The `fixture_id` is **not** an identifier you may target",
            "`action` is `CONTINUE` or `INCONCLUSIVE` and `target` names an arm",
            "`decision_basis` omits `INSUFFICIENT_EVIDENCE`",
            "`decision_basis` omits `COST_OF_WAITING`",
            "`decisive_metric` is `NONE_DECIDABLE` although the case supplies",
            "where the only adverse fact is small outcome counts",
            "`scale_readiness` is nested inside `operational`",
            "Keep every prose field short",
        ):
            with self.subTest(statement=statement[:50]):
                self.assertIn(" ".join(statement.split()), " ".join(V11.split()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
