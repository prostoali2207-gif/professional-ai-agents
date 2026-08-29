#!/usr/bin/env python3
"""Regressions for the four oracle/harness repairs from the 2026-08-28 audit.

No provider calls. The Analytics candidate is unchanged by these repairs; only the instrument
moved. Each repair is tested in both directions -- the thing that used to be wrongly rejected
is now accepted, and the thing that must still be rejected still is -- because a repair that
only loosens is indistinguishable from fitting the instrument to the answers.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


grader = _load("grd07", "grader_v07_structural.py")
generator = _load("gen07", "heldout_generator_v07.py")
audit = _load("oracle_audit", "oracle_audit.py")

SEED = 4242


def suite(seed: int = SEED, per_family: int = 1):
    cases, oracle = generator.generate(seed, per_family)
    return {f["fixture_id"]: f for f in cases["fixtures"]}, oracle["expectations"]


def pick(expectations: dict, family: str) -> str:
    return next(k for k, v in expectations.items() if v["family"] == family)


def good(fixtures, expectations, fid, **kw):
    return audit.build_passing_result(fixtures[fid], expectations[fid], **kw)


class Repair1ContractValidity(unittest.TestCase):
    """Grading step 0. Previously absent, so a structurally invalid result could pass."""

    def test_a_valid_result_still_passes(self) -> None:
        fixtures, expectations = suite()
        for fid in expectations:
            with self.subTest(fixture=fid):
                self.assertTrue(grader.grade(good(fixtures, expectations, fid), fixtures[fid],
                                             expectations[fid])["pass"])

    def test_structurally_invalid_results_fail_closed(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "IMMATURE_FIXED_HORIZON")
        mutations = {
            "computations not an array": lambda r: r.update({"computations": "nope"}),
            "missing decision_record": lambda r: r.pop("decision_record"),
            "missing causal block": lambda r: r["decision_record"].pop("causal"),
            "enum outside the contract": lambda r: r["decision_record"]["causal"].update({"claim_ceiling": "WISHFUL"}),
            "unexpected property": lambda r: r.update({"smuggled": 1}),
            "null target": lambda r: r["decision_record"]["operational"].update({"target": None}),
            "reversible not boolean": lambda r: r["decision_record"]["operational"].update({"reversible": "yes"}),
        }
        for label, mutate in mutations.items():
            broken = good(fixtures, expectations, fid)
            mutate(broken)
            with self.subTest(mutation=label):
                report = grader.grade(broken, fixtures[fid], expectations[fid])
                self.assertFalse(report["pass"], f"{label} was graded as a pass")
                self.assertTrue(any("contract violation" in f or "fixture_id" in f for f in report["failures"]),
                                report["failures"])

    def test_the_dependency_free_validator_agrees_with_the_contract(self) -> None:
        """Runners may not have jsonschema. The fallback must not quietly pass everything."""
        schema = json.loads((HERE / "schemas" / "result-v4.schema.json").read_text())
        fixtures, expectations = suite()
        fid = pick(expectations, "CLEAN_SCALABLE_WIN")
        valid = good(fixtures, expectations, fid)
        self.assertEqual(grader._fallback_validate(valid, schema), [])
        for mutate in (lambda r: r.update({"computations": "nope"}),
                       lambda r: r.pop("recommendation"),
                       lambda r: r["decision_record"]["causal"].update({"claim_scope": "SOMEWHERE"}),
                       lambda r: r.update({"smuggled": 1})):
            broken = copy.deepcopy(valid)
            mutate(broken)
            self.assertTrue(grader._fallback_validate(broken, schema), "fallback validator passed invalid output")


class Repair2ActionDependentTarget(unittest.TestCase):
    """The defect that burned five v0.6 trials."""

    def _sbi(self):
        fixtures, expectations = suite()
        fid = pick(expectations, "SPARSE_BUT_IDENTIFIED")
        treatment = next(a for a in expectations[fid]["target_by_action"]["ITERATE"] if a != "experiment")
        return fixtures, expectations, fid, treatment

    def _with(self, fixtures, expectations, fid, action, target):
        result = good(fixtures, expectations, fid)
        result["recommendation"] = action
        result["decision_record"]["operational"].update({"action": action, "target": target})
        return grader.grade(result, fixtures[fid], expectations[fid])

    def test_iterate_may_name_the_treatment_arm(self) -> None:
        fixtures, expectations, fid, treatment = self._sbi()
        self.assertTrue(self._with(fixtures, expectations, fid, "ITERATE", treatment)["pass"])

    def test_iterate_may_also_name_the_experiment(self) -> None:
        fixtures, expectations, fid, _ = self._sbi()
        self.assertTrue(self._with(fixtures, expectations, fid, "ITERATE", "experiment")["pass"])

    def test_inconclusive_may_not_name_an_arm(self) -> None:
        """The repair must not become permission for any target."""
        fixtures, expectations, fid, treatment = self._sbi()
        report = self._with(fixtures, expectations, fid, "INCONCLUSIVE", treatment)
        self.assertFalse(report["pass"])
        self.assertTrue(any("may only be aimed at" in f for f in report["failures"]), report["failures"])

    def test_wrong_arm_on_the_conflict_family_still_fails(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "UPSTREAM_DOWNSTREAM_CONFLICT")
        arms = fixtures[fid]["case"]["arms"]
        other = next(a for a in arms if a not in expectations[fid]["target_by_action"]["KILL"] and a != "experiment")
        self.assertFalse(self._with(fixtures, expectations, fid, "KILL", other)["pass"])

    def test_every_expectation_declares_a_target_for_every_permitted_action(self) -> None:
        for seed in range(8):
            _, expectations = suite(seed, per_family=2)
            for fid, expectation in expectations.items():
                by_action = expectation.get("target_by_action", {})
                for action in expectation["action_in"]:
                    with self.subTest(seed=seed, fixture=fid, action=action):
                        self.assertIn(action, by_action)
                        self.assertTrue(by_action[action])


class Repair3Units(unittest.TestCase):
    """The defect that burned one v0.6 trial."""

    def _csw(self):
        fixtures, expectations = suite()
        fid = pick(expectations, "CLEAN_SCALABLE_WIN")
        name = next(iter(expectations[fid]["computations"]))
        return fixtures, expectations, fid, name, expectations[fid]["computations"][name][0]

    def _with_unit(self, fixtures, expectations, fid, name, value, unit):
        result = good(fixtures, expectations, fid)
        for computation in result["computations"]:
            if computation["name"] == name:
                computation["result"], computation["unit"] = value, unit
        return grader.grade(result, fixtures[fid], expectations[fid])

    def test_ratio_and_percentage_forms_are_both_accepted(self) -> None:
        fixtures, expectations, fid, name, value = self._csw()
        for reported, unit in [(value, "ratio"), (value, "unitless"), (value * 100, "percent"), (value * 100, "%")]:
            with self.subTest(value=reported, unit=unit):
                self.assertTrue(self._with_unit(fixtures, expectations, fid, name, reported, unit)["pass"])

    def test_a_percentage_labelled_as_a_ratio_fails(self) -> None:
        fixtures, expectations, fid, name, value = self._csw()
        self.assertFalse(self._with_unit(fixtures, expectations, fid, name, value * 100, "ratio")["pass"])

    def test_an_unrecognised_unit_on_a_ratio_fails(self) -> None:
        fixtures, expectations, fid, name, value = self._csw()
        report = self._with_unit(fixtures, expectations, fid, name, value, "widgets")
        self.assertFalse(report["pass"])
        self.assertTrue(any("100x" in f for f in report["failures"]), report["failures"])

    def test_a_wrong_ratio_still_fails_under_either_unit(self) -> None:
        fixtures, expectations, fid, name, value = self._csw()
        self.assertFalse(self._with_unit(fixtures, expectations, fid, name, value + 0.4, "ratio")["pass"])
        self.assertFalse(self._with_unit(fixtures, expectations, fid, name, (value + 0.4) * 100, "percent")["pass"])

    def test_absolute_assertions_are_not_rescaled(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "UPSTREAM_DOWNSTREAM_CONFLICT")
        name, spec = next(iter(expectations[fid]["computations"].items()))
        for unit in ("currency", "AED", ""):
            result = good(fixtures, expectations, fid)
            for computation in result["computations"]:
                if computation["name"] == name:
                    computation["unit"] = unit
            with self.subTest(unit=unit):
                self.assertTrue(grader.grade(result, fixtures[fid], expectations[fid])["pass"])
        wrong = good(fixtures, expectations, fid)
        for computation in wrong["computations"]:
            if computation["name"] == name:
                computation["result"] = spec[0] * 100
        self.assertFalse(grader.grade(wrong, fixtures[fid], expectations[fid])["pass"])

    def test_every_ratio_like_assertion_declares_its_kind(self) -> None:
        for seed in range(8):
            fixtures, expectations = suite(seed, per_family=2)
            for fid, expectation in expectations.items():
                arms = fixtures[fid]["case"]["arms"]
                for name, spec in (expectation.get("computations") or {}).items():
                    with self.subTest(seed=seed, computation=name):
                        self.assertEqual(len(spec), 3, "assertion must declare RATIO or ABSOLUTE")
                        if audit.RATIO_LIKE.search(audit.metric_token(name, arms)):
                            self.assertEqual(spec[2], "RATIO")


class Repair4IdentityBinding(unittest.TestCase):
    def test_a_result_for_another_case_is_rejected(self) -> None:
        fixtures, expectations = suite(per_family=2)
        ids = list(fixtures)
        for fid in ids:
            impostor = good(fixtures, expectations, fid)
            impostor["fixture_id"] = next(other for other in ids if other != fid)
            with self.subTest(fixture=fid):
                report = grader.grade(impostor, fixtures[fid], expectations[fid])
                self.assertFalse(report["pass"])
                self.assertTrue(any("does not match the case being graded" in f for f in report["failures"]))


class NothingWasLoosened(unittest.TestCase):
    """Every lock the v0.6 grader held must still hold under v0.7."""

    def test_causal_claim_on_a_censored_registered_estimand_still_fails(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "IMMATURE_FIXED_HORIZON")
        wrong = good(fixtures, expectations, fid, scope="REGISTERED_ESTIMAND")
        wrong["decision_record"]["causal"].update({"claim_ceiling": "INCREMENTAL_CAUSAL", "status": "IDENTIFIED"})
        wrong["decision_record"]["causal"]["blocking_confounders"] = []
        wrong["confounders"] = []
        self.assertFalse(grader.grade(wrong, fixtures[fid], expectations[fid])["pass"])

    def test_the_same_claim_scoped_to_the_interim_outcome_still_passes(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "IMMATURE_FIXED_HORIZON")
        self.assertTrue(grader.grade(good(fixtures, expectations, fid, scope="INTERIM_OUTCOME"),
                                     fixtures[fid], expectations[fid])["pass"])

    def test_downgrading_the_ceiling_for_sparse_counts_still_fails(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "SPARSE_BUT_IDENTIFIED")
        wrong = good(fixtures, expectations, fid)
        wrong["decision_record"]["causal"]["claim_ceiling"] = "DIRECTIONAL_ASSOCIATION"
        self.assertFalse(grader.grade(wrong, fixtures[fid], expectations[fid])["pass"])

    def test_reflexive_scale_blocking_still_fails_the_clean_win(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "CLEAN_SCALABLE_WIN")
        timid = good(fixtures, expectations, fid)
        timid["recommendation"] = "CONTINUE"
        timid["decision_record"]["operational"]["action"] = "CONTINUE"
        timid["decision_record"]["scale_readiness"] = {"state": "BLOCKED",
                                                       "blocking_reasons": ["UNIDENTIFIED_CAUSAL_EFFECT"]}
        self.assertFalse(grader.grade(timid, fixtures[fid], expectations[fid])["pass"])

    def test_prose_still_cannot_move_a_verdict(self) -> None:
        fixtures, expectations = suite()
        for fid in expectations:
            bare = good(fixtures, expectations, fid)
            stuffed = copy.deepcopy(bare)
            stuffed["rationale"] = "cannot scale, gross profit, cost of waiting, reversible, right-censored"
            stuffed["next_action"] = "stop everything"
            with self.subTest(fixture=fid):
                self.assertEqual(grader.grade(bare, fixtures[fid], expectations[fid])["pass"],
                                 grader.grade(stuffed, fixtures[fid], expectations[fid])["pass"])

    def test_grading_remains_pure_and_order_independent(self) -> None:
        fixtures, expectations = suite()
        for fid in expectations:
            base = good(fixtures, expectations, fid)
            snapshot = copy.deepcopy(base)
            first = grader.grade(base, fixtures[fid], expectations[fid])
            shuffled = copy.deepcopy(base)
            shuffled["decision_record"]["operational"]["decision_basis"].reverse()
            shuffled["computations"].reverse()
            with self.subTest(fixture=fid):
                self.assertEqual(base, snapshot)
                self.assertEqual(first, grader.grade(copy.deepcopy(base), fixtures[fid], expectations[fid]))
                self.assertEqual(grader.grade(shuffled, fixtures[fid], expectations[fid])["pass"], first["pass"])


class AuditIsCleanOnTheRepairedOracle(unittest.TestCase):
    def test_no_high_severity_findings_remain(self) -> None:
        high = [f for f in audit.run("v07") if f.severity == "HIGH"]
        self.assertFalse(high, f"unresolved HIGH findings: {[str(f) for f in high]}")

    def test_the_historical_audits_are_unchanged(self) -> None:
        """v0.5 and v0.6 are evidence records. Repairing v0.7 must not rewrite what they were."""
        baseline = json.loads((HERE / "oracle-audit-baseline.json").read_text())
        for cycle in ("v05", "v06"):
            with self.subTest(cycle=cycle):
                self.assertEqual(sorted(f.key() for f in audit.run(cycle)), sorted(baseline[cycle]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
