#!/usr/bin/env python3
"""Regression against the ambiguity that burned the v0.5 immature-horizon family.

Deterministic, zero provider calls. The v0.5 oracle capped a randomized, unconfounded design
below INCREMENTAL_CAUSAL while permitting it for another randomized, unconfounded design, and
the discriminator it used -- outcome maturity -- was never a declared fact nor a stated rule.

These tests lock the adjudicated rule and, more importantly, lock the *shape* of the defect out:

  1. scope correctness   -- the ceiling is read against the declared claim_scope;
  2. sparsity is not identification -- small counts must not lower the ceiling;
  3. no hidden discriminator -- every fact the oracle uses to bound a ceiling must be visible
     in the candidate-facing case;
  4. oracle self-consistency -- cases whose candidate-visible identification facts are identical
     receive identical ceiling caps.
"""

from __future__ import annotations

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


grader = _load("grader_v06", "grader_v06_structural.py")
generator = _load("gen_v06", "heldout_generator_v06.py")

SEED = 777


def suite(seed: int = SEED, per_family: int = 1):
    cases, oracle = generator.generate(seed, per_family)
    return {f["fixture_id"]: f for f in cases["fixtures"]}, oracle["expectations"]


def result_for(fixture: dict, expectation: dict, *, scope: str | None = None,
               ceiling: str | None = None, action: str | None = None) -> dict:
    scope = scope or expectation["allowed_scopes"][0]
    # A scope with no bounds entry is one this case does not offer; the test is probing exactly
    # that, so fall back to the case's own scope for a well-formed ceiling.
    bounds = expectation["ceiling_by_scope"].get(
        scope, expectation["ceiling_by_scope"][expectation["allowed_scopes"][0]])
    ceiling = ceiling or bounds.get("min") or bounds["max"]
    action = action or expectation["action_in"][0]
    identified = "IDENTIFIED" in expectation.get("causal_status_in", []) or ceiling == "INCREMENTAL_CAUSAL"
    state = expectation.get("scale_state", "BLOCKED")
    return {
        "fixture_id": fixture["fixture_id"],
        "recommendation": action,
        "decision_record": {
            "causal": {"status": "IDENTIFIED" if identified else "UNRESOLVED",
                       "claim_scope": scope, "claim_ceiling": ceiling,
                       "blocking_confounders": [] if identified else ["design imbalance"]},
            "operational": {"action": action, "target": expectation["target"],
                            "decisive_metric": expectation["decisive_metric_in"][0],
                            "decision_basis": list({*expectation.get("basis_required", []), "REVERSIBILITY"}),
                            "reversible": True, "evidence_that_would_change_action": "x"},
            "scale_readiness": {"state": state,
                                "blocking_reasons": [expectation["scale_reasons_any"][0]]
                                if state == "BLOCKED" else ["NOT_BLOCKED"]},
        },
        "data_integrity_findings": [],
        "computations": [{"name": n, "inputs": {}, "method": "m", "result": v[0], "unit": "u"}
                         for n, v in expectation.get("computations", {}).items()],
        "claim_boundaries": [],
        "confounders": [] if identified else [{"name": "design imbalance", "severity": "MATERIAL", "effect": "."}],
        "rationale": ".", "next_action": ".",
    }


def pick(expectations: dict, family: str) -> str:
    return next(k for k, v in expectations.items() if v["family"] == family)


class Baseline(unittest.TestCase):
    def test_every_family_has_a_satisfiable_answer_under_each_allowed_scope(self) -> None:
        fixtures, expectations = suite()
        for fixture_id, expectation in expectations.items():
            for scope in expectation["allowed_scopes"]:
                report = grader.grade(result_for(fixtures[fixture_id], expectation, scope=scope),
                                      fixtures[fixture_id], expectation)
                with self.subTest(family=expectation["family"], scope=scope):
                    self.assertTrue(report["pass"], report["failures"])


class ScopedCeiling(unittest.TestCase):
    """Lock 1: the ceiling means nothing without the quantity it is about."""

    def test_causal_claim_about_a_censored_registered_estimand_fails(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "IMMATURE_FIXED_HORIZON")
        wrong = result_for(fixtures[fid], expectations[fid],
                           scope="REGISTERED_ESTIMAND", ceiling="INCREMENTAL_CAUSAL")
        report = grader.grade(wrong, fixtures[fid], expectations[fid])
        self.assertFalse(report["pass"])
        self.assertTrue(any("right-censored" in f or "max DIRECTIONAL" in f for f in report["failures"]),
                        report["failures"])

    def test_the_same_claim_scoped_to_the_interim_outcome_is_accepted(self) -> None:
        """The rule scopes a claim; it does not declare randomization broken."""
        fixtures, expectations = suite()
        fid = pick(expectations, "IMMATURE_FIXED_HORIZON")
        ok = result_for(fixtures[fid], expectations[fid],
                        scope="INTERIM_OUTCOME", ceiling="INCREMENTAL_CAUSAL")
        report = grader.grade(ok, fixtures[fid], expectations[fid])
        self.assertTrue(report["pass"], report["failures"])

    def test_interim_scope_on_a_closed_window_fails(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "CLEAN_SCALABLE_WIN")
        wrong = result_for(fixtures[fid], expectations[fid], scope="INTERIM_OUTCOME")
        report = grader.grade(wrong, fixtures[fid], expectations[fid])
        self.assertFalse(report["pass"])

    def test_missing_scope_fails(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "CLEAN_SCALABLE_WIN")
        wrong = result_for(fixtures[fid], expectations[fid])
        del wrong["decision_record"]["causal"]["claim_scope"]
        self.assertFalse(grader.grade(wrong, fixtures[fid], expectations[fid])["pass"])


class SparsityIsNotIdentification(unittest.TestCase):
    """Lock 2: the loosening half of the rule."""

    def test_downgrading_the_ceiling_for_small_counts_fails(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "SPARSE_BUT_IDENTIFIED")
        for weaker in ["DIRECTIONAL_ASSOCIATION", "DESCRIPTIVE_ASSOCIATION", "NONE"]:
            wrong = result_for(fixtures[fid], expectations[fid], ceiling=weaker)
            with self.subTest(ceiling=weaker):
                report = grader.grade(wrong, fixtures[fid], expectations[fid])
                self.assertFalse(report["pass"])
                self.assertTrue(any("precision problem" in f for f in report["failures"]), report["failures"])

    def test_identification_does_not_license_scaling_on_sparse_evidence(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "SPARSE_BUT_IDENTIFIED")
        wrong = result_for(fixtures[fid], expectations[fid], action="SCALE")
        self.assertFalse(grader.grade(wrong, fixtures[fid], expectations[fid])["pass"])


class NoHiddenDiscriminator(unittest.TestCase):
    """Lock 3: the v0.5 defect was a cap driven by a fact the candidate could not see."""

    IDENTIFICATION_FACTS = ("randomized_split", "confounding")

    def test_every_case_declares_the_facts_the_ceiling_depends_on(self) -> None:
        fixtures, _ = suite(per_family=2)
        for fixture_id, fixture in fixtures.items():
            case = fixture["case"]
            with self.subTest(fixture=fixture_id):
                self.assertIn("registered_window_complete", case,
                              "the window fact bounds the ceiling and must be declared, not implied by prose")
                self.assertIsInstance(case["registered_window_complete"], bool)
                self.assertIn("randomized_split", case.get("design", {}),
                              "identification depends on randomization, which must be declared")

    def test_ceiling_caps_agree_whenever_visible_identification_facts_agree(self) -> None:
        """The exact v0.5 failure shape: identical candidate-visible facts, different caps."""
        caps: dict[tuple, set] = {}
        for seed in range(12):
            fixtures, expectations = suite(seed, per_family=2)
            for fixture_id, expectation in expectations.items():
                case = fixtures[fixture_id]["case"]
                key = (bool(case["design"].get("randomized_split")),
                       str(case["design"].get("confounding", "unstated")),
                       bool(case["registered_window_complete"]))
                cap = expectation["ceiling_by_scope"]["REGISTERED_ESTIMAND"]["max"]
                caps.setdefault(key, set()).add(cap)
        for key, values in caps.items():
            with self.subTest(facts=key):
                self.assertEqual(len(values), 1,
                                 f"identical visible facts {key} map to different ceiling caps {values}")

    def test_scope_availability_follows_the_declared_window(self) -> None:
        for seed in range(12):
            fixtures, expectations = suite(seed, per_family=2)
            for fixture_id, expectation in expectations.items():
                complete = fixtures[fixture_id]["case"]["registered_window_complete"]
                with self.subTest(fixture=fixture_id, seed=seed):
                    self.assertEqual("INTERIM_OUTCOME" in expectation["allowed_scopes"], not complete)


class CarriedForward(unittest.TestCase):
    """The v0.5 locks must still hold under the v0.6 oracle."""

    def test_wrong_arm_on_the_conflict_family_still_fails(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "UPSTREAM_DOWNSTREAM_CONFLICT")
        wrong = result_for(fixtures[fid], expectations[fid])
        arms = fixtures[fid]["case"]["arms"]
        wrong["decision_record"]["operational"]["target"] = next(
            a for a in arms if a != expectations[fid]["target"] and a != "experiment")
        self.assertFalse(grader.grade(wrong, fixtures[fid], expectations[fid])["pass"])

    def test_prose_target_still_fails(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "UPSTREAM_DOWNSTREAM_CONFLICT")
        wrong = result_for(fixtures[fid], expectations[fid])
        wrong["decision_record"]["operational"]["target"] = "configuration A and B comparison"
        self.assertFalse(grader.grade(wrong, fixtures[fid], expectations[fid])["pass"])

    def test_reflexive_scale_blocking_still_fails_the_clean_win(self) -> None:
        fixtures, expectations = suite()
        fid = pick(expectations, "CLEAN_SCALABLE_WIN")
        timid = result_for(fixtures[fid], expectations[fid], action="CONTINUE")
        timid["decision_record"]["scale_readiness"] = {"state": "BLOCKED",
                                                       "blocking_reasons": ["UNIDENTIFIED_CAUSAL_EFFECT"]}
        self.assertFalse(grader.grade(timid, fixtures[fid], expectations[fid])["pass"])

    def test_cases_carry_no_expectations(self) -> None:
        cases, _ = generator.generate(5, 2)
        blob = repr(cases).lower()
        for leak in ["expectation", "decisive_metric", "ceiling_by_scope", "allowed_scopes", "trap", "action_in"]:
            self.assertNotIn(leak, blob)


if __name__ == "__main__":
    unittest.main(verbosity=2)
