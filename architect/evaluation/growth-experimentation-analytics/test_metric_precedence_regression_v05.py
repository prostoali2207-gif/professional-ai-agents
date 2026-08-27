#!/usr/bin/env python3
"""Regressions against the failure modes that ended the v0.4 cycle.

Deterministic, zero provider calls. Four locks:

  1. metric precedence -- when a diagnostic metric and the decisive metric rank the arms
     oppositely, an action aimed at the arm the decisive metric favours must fail. This is
     the H-GDS-02 P0 failure, where the profitable arm was stopped because its cost per
     lead looked worse;
  2. structural target -- the target is resolved by membership in the fixture's declared
     arms. Prose, two arms at once, and an invented arm all fail; `variant_b`, which the
     v0.4 parser could not resolve and wrongly scored as a candidate failure, now passes;
  3. internal consistency -- claiming downstream economics as decisive while targeting the
     arm those economics favour is invalid;
  4. anti-gaming -- a candidate that always blocks SCALE and always reports UNRESOLVED
     fails the clean scalable win, so the other locks cannot be satisfied by reflex.
"""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


grader = _load("grader_v05", "grader_v05_structural.py")
generator = _load("heldout_gen_v05", "heldout_generator_v05.py")

SEED = 4242


def suite():
    cases, expectations = generator.generate(SEED, per_family=1)
    by_id = {f["fixture_id"]: f for f in cases["fixtures"]}
    return by_id, expectations["expectations"]


def correct_result(fixture: dict, expectation: dict) -> dict:
    """A result that satisfies the oracle, built from the expectation itself."""
    action = expectation["action_in"][0]
    scale_state = expectation.get("scale_state", "BLOCKED")
    reasons = ([expectation["scale_reasons_any"][0]] if scale_state == "BLOCKED"
               else ["NOT_BLOCKED"])
    identified = "IDENTIFIED" in expectation.get("causal_status_in", [])
    ceiling = expectation.get("max_claim_ceiling", "DESCRIPTIVE_ASSOCIATION")
    confounders = ([] if identified
                   else [{"name": "design imbalance", "severity": "MATERIAL", "effect": "."}])
    basis = list({*expectation.get("basis_required", []), "REVERSIBILITY"})
    return {
        "fixture_id": fixture["fixture_id"],
        "recommendation": action,
        "decision_record": {
            "causal": {
                "status": "IDENTIFIED" if identified else "UNRESOLVED",
                "claim_ceiling": ceiling,
                "blocking_confounders": [] if identified else ["design imbalance"],
            },
            "operational": {
                "action": action,
                "target": expectation["target"],
                "decisive_metric": expectation["decisive_metric_in"][0],
                "decision_basis": basis,
                "reversible": True,
                "evidence_that_would_change_action": "verified contradicting economics",
            },
            "scale_readiness": {"state": scale_state, "blocking_reasons": reasons},
        },
        "data_integrity_findings": [],
        "computations": [{"name": n, "inputs": {}, "method": "m", "result": v[0], "unit": "u"}
                         for n, v in expectation.get("computations", {}).items()],
        "claim_boundaries": [],
        "confounders": confounders,
        "rationale": ".",
        "next_action": ".",
    }


class Baseline(unittest.TestCase):
    def test_every_generated_family_has_a_satisfiable_correct_answer(self) -> None:
        """If the oracle were unsatisfiable the gate would be measuring nothing."""
        fixtures, expectations = suite()
        for fixture_id, expectation in expectations.items():
            fixture = fixtures[fixture_id]
            report = grader.grade(correct_result(fixture, expectation), fixture, expectation)
            with self.subTest(family=expectation["family"]):
                self.assertTrue(report["pass"], report["failures"])


class MetricPrecedence(unittest.TestCase):
    """Lock 1: the H-GDS-02 P0 failure."""

    def test_stopping_the_arm_the_decisive_metric_favours_fails(self) -> None:
        fixtures, expectations = suite()
        fixture_id = next(k for k, v in expectations.items() if v["family"] == "UPSTREAM_DOWNSTREAM_CONFLICT")
        fixture, expectation = fixtures[fixture_id], expectations[fixture_id]
        wrong = correct_result(fixture, expectation)
        other = next(a for a in fixture["case"]["arms"]
                     if a != expectation["target"] and a != "experiment")
        wrong["decision_record"]["operational"]["target"] = other
        report = grader.grade(wrong, fixture, expectation)
        self.assertFalse(report["pass"], "stopping the profitable arm must fail")
        self.assertTrue(any("justified action applies to" in f for f in report["failures"]), report["failures"])

    def test_acquisition_cost_cannot_be_decisive_when_downstream_economics_exist(self) -> None:
        fixtures, expectations = suite()
        fixture_id = next(k for k, v in expectations.items() if v["family"] == "UPSTREAM_DOWNSTREAM_CONFLICT")
        fixture, expectation = fixtures[fixture_id], expectations[fixture_id]
        wrong = correct_result(fixture, expectation)
        wrong["decision_record"]["operational"]["decisive_metric"] = "ACQUISITION_COST"
        self.assertFalse(grader.grade(wrong, fixture, expectation)["pass"])

    def test_downstream_economics_cannot_be_claimed_when_the_case_supplies_none(self) -> None:
        fixtures, expectations = suite()
        fixture_id = next(k for k, v in expectations.items() if v["family"] == "UPSTREAM_ONLY_CONFOUNDED")
        fixture, expectation = fixtures[fixture_id], expectations[fixture_id]
        wrong = correct_result(fixture, expectation)
        wrong["decision_record"]["operational"]["decision_basis"] = ["MATURE_DOWNSTREAM_ECONOMICS", "COST_OF_WAITING"]
        report = grader.grade(wrong, fixture, expectation)
        self.assertFalse(report["pass"], "fabricated downstream economics must fail")


class StructuralTarget(unittest.TestCase):
    """Lock 2: the six v0.4 target failures, and the parser defect that burned REG-DS-01."""

    def _conflict(self):
        fixtures, expectations = suite()
        fixture_id = next(k for k, v in expectations.items() if v["family"] == "UPSTREAM_DOWNSTREAM_CONFLICT")
        return fixtures[fixture_id], expectations[fixture_id]

    def test_prose_target_fails(self) -> None:
        fixture, expectation = self._conflict()
        for prose in ["Configuration A and Configuration B comparison setup",
                      "configuration_a and configuration_b comparison",
                      "Configuration A and B paid acquisition setup",
                      "the losing arm"]:
            wrong = correct_result(fixture, expectation)
            wrong["decision_record"]["operational"]["target"] = prose
            with self.subTest(target=prose):
                report = grader.grade(wrong, fixture, expectation)
                self.assertFalse(report["pass"])
                self.assertTrue(any("declared arms" in f for f in report["failures"]), report["failures"])

    def test_invented_arm_fails(self) -> None:
        fixture, expectation = self._conflict()
        wrong = correct_result(fixture, expectation)
        wrong["decision_record"]["operational"]["target"] = "configuration_c"
        self.assertFalse(grader.grade(wrong, fixture, expectation)["pass"])

    def test_underscored_arm_name_resolves(self) -> None:
        """`variant_b` was scored as a candidate failure by the v0.4 parser. It is the
        fixture's own name for the arm and must resolve by lookup."""
        fixtures, expectations = suite()
        fixture_id = next(k for k, v in expectations.items() if v["family"] == "IMMATURE_FIXED_HORIZON")
        fixture, expectation = fixtures[fixture_id], expectations[fixture_id]
        self.assertIn("variant_b", fixture["case"]["arms"])
        probe = correct_result(fixture, expectation)
        probe["decision_record"]["operational"]["target"] = "variant_b"
        report = grader.grade(probe, fixture, expectation)
        # It is the wrong arm for this family, but it must fail as a *decision*, never as
        # an unresolvable string.
        self.assertFalse(any("declared arms" in f for f in report["failures"]), report["failures"])

    def test_every_declared_arm_resolves_by_lookup(self) -> None:
        fixtures, expectations = suite()
        for fixture_id, expectation in expectations.items():
            fixture = fixtures[fixture_id]
            for arm in fixture["case"]["arms"]:
                probe = correct_result(fixture, expectation)
                probe["decision_record"]["operational"]["target"] = arm
                failures = grader.grade(probe, fixture, expectation)["failures"]
                with self.subTest(fixture=fixture_id, arm=arm):
                    self.assertFalse(any("declared arms" in f for f in failures), failures)


class AntiGaming(unittest.TestCase):
    """Lock 4: reflexive caution must not pass."""

    def test_always_blocking_scale_fails_the_clean_win(self) -> None:
        fixtures, expectations = suite()
        fixture_id = next(k for k, v in expectations.items() if v["family"] == "CLEAN_SCALABLE_WIN")
        fixture, expectation = fixtures[fixture_id], expectations[fixture_id]
        timid = correct_result(fixture, expectation)
        timid["recommendation"] = "CONTINUE"
        timid["decision_record"]["operational"]["action"] = "CONTINUE"
        timid["decision_record"]["scale_readiness"] = {
            "state": "BLOCKED", "blocking_reasons": ["UNIDENTIFIED_CAUSAL_EFFECT"]}
        self.assertFalse(grader.grade(timid, fixture, expectation)["pass"])

    def test_always_unresolved_fails_the_clean_win(self) -> None:
        fixtures, expectations = suite()
        fixture_id = next(k for k, v in expectations.items() if v["family"] == "CLEAN_SCALABLE_WIN")
        fixture, expectation = fixtures[fixture_id], expectations[fixture_id]
        timid = correct_result(fixture, expectation)
        timid["decision_record"]["causal"]["status"] = "UNRESOLVED"
        timid["decision_record"]["causal"]["claim_ceiling"] = "DESCRIPTIVE_ASSOCIATION"
        self.assertFalse(grader.grade(timid, fixture, expectation)["pass"])

    def test_wrong_arithmetic_still_fails(self) -> None:
        fixtures, expectations = suite()
        fixture_id = next(k for k, v in expectations.items() if v["family"] == "UPSTREAM_DOWNSTREAM_CONFLICT")
        fixture, expectation = fixtures[fixture_id], expectations[fixture_id]
        wrong = correct_result(fixture, expectation)
        wrong["computations"][0]["result"] += 5
        self.assertFalse(grader.grade(wrong, fixture, expectation)["pass"])


class ProseIndependence(unittest.TestCase):
    """Carried forward from v0.4: phrasing must never move a verdict."""

    def test_verdict_survives_prose_erasure_and_keyword_stuffing(self) -> None:
        fixtures, expectations = suite()
        for fixture_id, expectation in expectations.items():
            fixture = fixtures[fixture_id]
            bare = correct_result(fixture, expectation)
            stuffed = copy.deepcopy(bare)
            stuffed["rationale"] = ("cannot scale, gross profit, downstream economics, continued spend cost, "
                                   "reversible, cost of waiting")
            stuffed["next_action"] = "stop everything and do not scale"
            with self.subTest(fixture=fixture_id):
                self.assertEqual(grader.grade(bare, fixture, expectation)["pass"],
                                 grader.grade(stuffed, fixture, expectation)["pass"])


class GeneratorIntegrity(unittest.TestCase):
    def test_culprit_arm_position_is_randomised(self) -> None:
        """A fixed culprit position would let a candidate anchor instead of reasoning."""
        targets = set()
        for seed in range(40):
            _, expectations = generator.generate(seed, per_family=1)
            for expectation in expectations["expectations"].values():
                if expectation["family"] == "UPSTREAM_DOWNSTREAM_CONFLICT":
                    targets.add(expectation["target"])
        self.assertEqual(targets, {"configuration_a", "configuration_b"}, targets)

    def test_conflict_family_really_conflicts(self) -> None:
        """The diagnostic and decisive metrics must genuinely disagree, or the case is not a trap."""
        for seed in range(25):
            cases, expectations = generator.generate(seed, per_family=1)
            for fixture in cases["fixtures"]:
                expectation = expectations["expectations"][fixture["fixture_id"]]
                if expectation["family"] != "UPSTREAM_DOWNSTREAM_CONFLICT":
                    continue
                case = fixture["case"]
                culprit = expectation["target"]
                other = next(a for a in case["arms"] if a != culprit and a != "experiment")
                cpl = lambda arm: case[arm]["spend"] / case[arm]["qualified_leads"]
                net = lambda arm: case[arm]["gross_profit"] - case[arm]["spend"]
                with self.subTest(seed=seed):
                    self.assertLess(cpl(culprit), cpl(other), "culprit must look better on the diagnostic")
                    self.assertLess(net(culprit), 0, "culprit must be loss-making")
                    self.assertGreater(net(other), 0, "the other arm must be profitable")

    def test_cases_carry_no_expectations(self) -> None:
        cases, _ = generator.generate(7, per_family=2)
        blob = repr(cases).lower()
        for leak in ["expectation", "target\":", "decisive_metric", "scale_state", "trap", "action_in"]:
            self.assertNotIn(leak, blob, f"candidate-facing suite leaks {leak!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
