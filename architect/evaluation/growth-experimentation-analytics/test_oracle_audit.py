#!/usr/bin/env python3
"""Property and regression tests for the Analytics oracle/harness audit.

No provider calls. Two jobs:

  * lock the harness invariants that currently hold, so they cannot silently regress;
  * lock the *finding set* against a baseline, so a new oracle defect turns the suite red and a
    repaired one forces the baseline to be updated deliberately.

The audit exists because three consecutive gates failed on the instrument rather than the
candidate. A detector that is not itself tested would just move the problem one layer up, so
the detector is also tested against the historical defect it was written to explain.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = json.loads((HERE / "oracle-audit-baseline.json").read_text())


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


audit = _load("oracle_audit", "oracle_audit.py")
generator = _load("gen06", "heldout_generator_v06.py")
grader = _load("grd06", "grader_v06_structural.py")


def suite(seed: int = 20260828, per_family: int = 2):
    cases, oracle = generator.generate(seed, per_family)
    return {f["fixture_id"]: f for f in cases["fixtures"]}, oracle["expectations"], cases


class FindingBaseline(unittest.TestCase):
    def test_no_finding_outside_the_accepted_baseline(self) -> None:
        for cycle in ("v05", "v06", "v07"):
            found = {f.key() for f in audit.run(cycle)}
            new = sorted(found - set(BASELINE[cycle]))
            with self.subTest(cycle=cycle):
                self.assertFalse(new, f"new oracle/harness defects not in the baseline: {new}")

    def test_baseline_entries_still_reproduce(self) -> None:
        for cycle in ("v05", "v06", "v07"):
            found = {f.key() for f in audit.run(cycle)}
            gone = sorted(set(BASELINE[cycle]) - found)
            with self.subTest(cycle=cycle):
                self.assertFalse(gone, f"baselined findings no longer reproduce; update the baseline: {gone}")

    def test_the_repaired_oracle_carries_no_high_findings(self) -> None:
        high = [str(f) for f in audit.run("v07") if f.severity == "HIGH"]
        self.assertFalse(high, high)


class DetectorIsItselfCorrect(unittest.TestCase):
    """A detector nobody tests is just a second place for defects to hide."""

    def test_it_catches_the_defect_that_burned_the_v05_gate(self) -> None:
        keys = {f.key() for f in audit.run("v05")}
        self.assertIn("C2-cap-inconsistency|CLEAN_SCALABLE_WIN / IMMATURE_FIXED_HORIZON", keys,
                      "the audit must reproduce the inconsistent ceiling cap that cost the v0.5 cycle")

    def test_it_is_silent_about_that_defect_on_v06(self) -> None:
        keys = {f.key() for f in audit.run("v06")}
        self.assertFalse([k for k in keys if k.startswith("C2-")],
                         "v0.6 declares the discriminator, so no cap inconsistency should be reported")

    def test_it_does_not_manufacture_ratio_false_positives(self) -> None:
        """'configuration' contains 'ratio'. An audit that trips on that is worthless."""
        arms = ["configuration_a", "configuration_b", "experiment"]
        self.assertFalse(audit.RATIO_LIKE.search(audit.metric_token("net_return_configuration_b", arms)))
        self.assertFalse(audit.RATIO_LIKE.search(audit.metric_token("cost_per_outcome_configuration_a", arms)))
        self.assertTrue(audit.RATIO_LIKE.search(audit.metric_token("relative_lift_variant_b",
                                                                   ["variant_a", "variant_b"])))

    def test_consistency_key_normalises_equivalent_wordings(self) -> None:
        a = {"design": {"randomized_split": True, "confounding": "none known"}, "registered_window_complete": True}
        b = {"design": {"randomized_split": True, "confounding": "none identified"}, "registered_window_complete": True}
        self.assertEqual(audit.visible_identification_facts(a), audit.visible_identification_facts(b),
                         "two wordings of 'no confounding' must land in the same bucket")

    def test_consistency_key_separates_real_confounding(self) -> None:
        clean = {"design": {"randomized_split": True, "confounding": "none known"}, "registered_window_complete": True}
        dirty = {"design": {"randomized_split": True, "confounding": "audience source differs"},
                 "registered_window_complete": True}
        self.assertNotEqual(audit.visible_identification_facts(clean), audit.visible_identification_facts(dirty))


class HarnessInvariantsThatHold(unittest.TestCase):
    """These pass today. The point is that they keep passing."""

    def test_grading_is_pure_and_order_independent(self) -> None:
        fixtures, expectations, _ = suite()
        for fid, expectation in expectations.items():
            base = audit.build_passing_result(fixtures[fid], expectation)
            snapshot = copy.deepcopy(base)
            first = grader.grade(base, fixtures[fid], expectation)
            with self.subTest(fixture=fid):
                self.assertEqual(base, snapshot, "grade() mutated its input")
                self.assertEqual(first, grader.grade(copy.deepcopy(base), fixtures[fid], expectation))
                shuffled = copy.deepcopy(base)
                shuffled["decision_record"]["operational"]["decision_basis"].reverse()
                shuffled["computations"].reverse()
                shuffled["decision_record"]["scale_readiness"]["blocking_reasons"].reverse()
                self.assertEqual(grader.grade(shuffled, fixtures[fid], expectation)["pass"], first["pass"])

    def test_every_expectation_is_satisfiable_under_every_allowed_scope(self) -> None:
        fixtures, expectations, _ = suite()
        for fid, expectation in expectations.items():
            for scope in expectation["allowed_scopes"]:
                report = grader.grade(audit.build_passing_result(fixtures[fid], expectation, scope),
                                      fixtures[fid], expectation)
                with self.subTest(fixture=fid, scope=scope):
                    self.assertTrue(report["pass"], report["failures"])

    def test_every_oracle_target_is_a_declared_arm(self) -> None:
        for seed in range(8):
            fixtures, expectations, _ = suite(seed)
            for fid, expectation in expectations.items():
                with self.subTest(seed=seed, fixture=fid):
                    self.assertIn(expectation["target"], fixtures[fid]["case"]["arms"])

    def test_every_asserted_computation_is_requested_of_the_candidate(self) -> None:
        for seed in range(8):
            fixtures, expectations, _ = suite(seed)
            for fid, expectation in expectations.items():
                for name in (expectation.get("computations") or {}):
                    with self.subTest(seed=seed, computation=name):
                        self.assertIn(name, fixtures[fid]["instruction"],
                                      "a computation the candidate is never asked for cannot be graded fairly")

    def test_expectation_enums_are_all_known_to_the_grader(self) -> None:
        fixtures, expectations, _ = suite()
        self.assertFalse([f for f in audit.check_vocabularies(expectations, grader)])

    def test_candidate_facing_suite_never_leaks_the_oracle(self) -> None:
        for seed in range(8):
            _, _, cases = suite(seed)
            with self.subTest(seed=seed):
                self.assertFalse([f.rule for f in audit.check_no_leakage(cases)])

    def test_fixtures_satisfy_the_declared_fixture_contract(self) -> None:
        import jsonschema
        schema = json.loads((HERE / "schemas" / "fixture-v3.schema.json").read_text())
        for seed in range(8):
            fixtures, _, _ = suite(seed)
            for fid, fixture in fixtures.items():
                with self.subTest(seed=seed, fixture=fid):
                    jsonschema.Draft202012Validator(schema).validate(fixture)


if __name__ == "__main__":
    unittest.main(verbosity=2)
