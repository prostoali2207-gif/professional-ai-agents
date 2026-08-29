#!/usr/bin/env python3
"""Deterministic verification of the k=7 two-tier gate before it is run.

No provider calls. Confirms that the preregistration says exactly what the adopted stability
audit says, that the runner implements it rather than something adjacent, and that the candidate,
grader, generator, fixtures and both contracts are untouched.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

PREREG = json.loads((HERE / "preregistration-v1.0-twotier-2026-09-01.json").read_text(encoding="utf-8"))
FREEZE = json.loads((HERE / "candidate-freeze-v1.0.json").read_text(encoding="utf-8"))
RUNNER = HERE / "run_heldout_gate_v10_twotier.py"
BURNED_SEEDS = {20260827, 20260828, 20260829, 20260830, 20260831, 999999}


def blob(path: str) -> str:
    return subprocess.check_output(["git", "hash-object", path], text=True, cwd=ROOT).strip()


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


C = _load("toc", "trial_outcome_classifier.py")


class CriterionMatchesTheAdoptedAudit(unittest.TestCase):
    def test_k_is_seven_over_ten_fixtures(self) -> None:
        self.assertEqual(7, PREREG["trials_per_fixture"])
        self.assertEqual(2, PREREG["per_family"])
        self.assertEqual(5, len(PREREG["families"]))
        self.assertEqual(70, PREREG["total_trials"])

    def test_tier1_has_zero_tolerance(self) -> None:
        self.assertEqual(0, PREREG["tier1_tolerance"])

    def test_tier2_caps_are_two_per_fixture_and_six_total(self) -> None:
        self.assertEqual(2, PREREG["tier2_per_fixture_cap"])
        self.assertEqual(6, PREREG["tier2_total_cap"])

    def test_the_per_fixture_cap_leaves_at_least_five_judged_trials(self) -> None:
        """The masking guard: a fixture can never qualify on one observation of its judgment."""
        self.assertGreaterEqual(
            PREREG["trials_per_fixture"] - PREREG["tier2_per_fixture_cap"], 5)

    def test_no_retries_and_no_best_of_n(self) -> None:
        self.assertEqual(0, PREREG["retries_permitted"])
        self.assertFalse(PREREG["best_of_n"])
        self.assertIn("Best-of-N is not a pass", PREREG["pass_rule"])
        self.assertIn("no trial may be retried", PREREG["pass_rule"])

    def test_invalid_voids_the_gate_rather_than_passing_or_failing_it(self) -> None:
        self.assertIn("not PASS and not FAIL", PREREG["pass_rule"])

    def test_tier2_is_only_parse_and_schema_failures(self) -> None:
        t2 = PREREG["tier_definitions"]["TIER2"]
        self.assertIn("syntactic JSON parse failure", t2)
        self.assertIn("frozen-schema violation", t2)
        self.assertIn("never a judgment PASS", t2)

    def test_the_seed_is_new(self) -> None:
        self.assertNotIn(PREREG["heldout_seed"], BURNED_SEEDS)
        self.assertEqual(20260901, PREREG["heldout_seed"])

    def test_the_criterion_cites_the_audit_that_adopted_it(self) -> None:
        self.assertTrue(PREREG["criterion_authority"].endswith(
            "stability-criterion-audit-2026-08-31.md"))
        self.assertTrue((ROOT / PREREG["criterion_authority"]).exists())


class TierMapIsFrozenBeforeAnyResult(unittest.TestCase):
    def test_the_preregistration_pins_the_tier_map_digest(self) -> None:
        self.assertEqual(C.RULES_DIGEST, PREREG["tier_map_digest"])

    def test_the_runner_aborts_on_tier_map_drift(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("TIER MAP DRIFT", source)
        self.assertIn('classifier.RULES_DIGEST != prereg["tier_map_digest"]', source)

    def test_the_classifier_and_runner_blobs_are_bound(self) -> None:
        for key in ("generator", "grader", "classifier", "runner"):
            with self.subTest(key=key):
                self.assertEqual(PREREG[key]["git_blob_sha"], blob(PREREG[key]["path"]))

    def test_the_runner_verifies_all_four_apparatus_blobs_at_run_time(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn('for key in ("generator", "grader", "classifier", "runner")', source)


class RunnerImplementsTheCriterion(unittest.TestCase):
    def test_the_runner_delegates_classification_and_does_not_reimplement_it(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("classifier.classify_trial(", source)
        self.assertIn("classifier.gate_verdict(", source)
        for smuggled in ("429", "RESOURCE_EXHAUSTED", "output contract violation at",
                         "model returned invalid JSON"):
            with self.subTest(pattern=smuggled):
                self.assertNotIn(smuggled, source,
                                 "the runner must not carry its own copy of the tier map")

    def test_the_runner_reads_both_caps_from_the_preregistration(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn('prereg["tier2_per_fixture_cap"]', source)
        self.assertIn('prereg["tier2_total_cap"]', source)

    def test_the_runner_executes_each_trial_exactly_once(self) -> None:
        """No retry and no best-of-N, checked as structure rather than by word-hunting.

        There is exactly one place the candidate is invoked, it sits inside the per-trial loop,
        and every failure path leaves that trial recorded and moves on.
        """
        source = RUNNER.read_text(encoding="utf-8")
        self.assertEqual(1, source.count("subprocess.run("),
                         "more than one invocation site is a retry surface")
        self.assertEqual(1, source.count("for trial in range(1, trials + 1):"))
        # every early exit from a trial appends to the ledger before continuing
        for branch in ("if proc.returncode != 0:", "except json.JSONDecodeError:"):
            with self.subTest(branch=branch):
                window = source[source.find(branch):source.find(branch) + 700]
                self.assertIn("ledger.append(entry)", window)
                self.assertIn("continue", window)

    def test_the_runner_declares_retries_and_best_of_n_off_in_its_summary(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn('"retries_permitted": 0', source)
        self.assertIn('"best_of_n": False', source)

    def test_an_invalid_verdict_exits_with_a_code_that_is_neither_pass_nor_fail(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn('return {"PASS": 0, "FAIL": 1}.get(verdict, 2)', source)

    def test_the_runner_calls_the_frozen_grader_with_unchanged_arguments(self) -> None:
        new = RUNNER.read_text(encoding="utf-8")
        old = (HERE / "run_heldout_gate_v07.py").read_text(encoding="utf-8")
        call = "grader.grade(result, fixture, expectations[fixture_id], contract)"
        self.assertIn(call, new)
        self.assertIn(call, old)

    def test_the_executor_never_sees_the_expectations(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        idx = source.find("subprocess.run(")
        self.assertGreater(idx, 0)
        window = source[idx:idx + 400]
        self.assertIn("json.dumps(fixture", window)
        self.assertNotIn("expectations", window)

    def test_the_verdict_wiring_is_exercised_end_to_end(self) -> None:
        """The runner's aggregation shape must be what gate_verdict expects."""
        by_fixture = {f"HO-{i:02d}": [C.PASS] * 7 for i in range(10)}
        clean = C.gate_verdict(by_fixture, PREREG["tier2_per_fixture_cap"],
                               PREREG["tier2_total_cap"])
        self.assertEqual("PASS", clean["verdict"])
        self.assertEqual(70, clean["judgment_pass_trials"])

        by_fixture["HO-03"][2] = C.INVALID
        self.assertEqual(C.INVALID, C.gate_verdict(
            by_fixture, PREREG["tier2_per_fixture_cap"], PREREG["tier2_total_cap"])["verdict"])


class NothingProfessionalWasTouched(unittest.TestCase):
    def test_the_candidate_assembly_is_byte_identical_to_freeze_v10(self) -> None:
        for component in FREEZE["assembly"]:
            with self.subTest(path=component["path"]):
                self.assertEqual(component["git_blob_sha"], blob(component["path"]))
        self.assertEqual(PREREG["candidate_assembly_digest"], FREEZE["assembly_digest"])

    def test_grader_generator_and_both_contracts_are_unchanged(self) -> None:
        for role in ("generator", "grader"):
            with self.subTest(role=role):
                self.assertEqual(FREEZE["instrument"][role]["git_blob_sha"],
                                 blob(FREEZE["instrument"][role]["path"]))
        self.assertEqual(FREEZE["output_contract_git_blob_sha"],
                         blob(FREEZE["output_contract_path"]))
        self.assertEqual(PREREG["grader"]["git_blob_sha"],
                         FREEZE["instrument"]["grader"]["git_blob_sha"])
        self.assertEqual(PREREG["generator"]["git_blob_sha"],
                         FREEZE["instrument"]["generator"]["git_blob_sha"])

    def test_the_previous_runner_is_untouched(self) -> None:
        self.assertEqual(FREEZE["instrument"]["runner"]["git_blob_sha"],
                         blob(FREEZE["instrument"]["runner"]["path"]))

    def test_the_oracle_still_asserts_the_same_expectations_for_the_new_seed(self) -> None:
        """A new seed draws new cases from the SAME frozen generator and oracle."""
        gen = _load("gen", "heldout_generator_v07.py")
        _cases, oracle = gen.generate(PREREG["heldout_seed"], PREREG["per_family"])
        exps = oracle["expectations"]
        self.assertEqual(10, len(exps))
        self.assertEqual(set(PREREG["families"]), {e["family"] for e in exps.values()})
        for fid, e in exps.items():
            with self.subTest(fixture=fid):
                self.assertIn(e["scale_state"], {"BLOCKED", "ELIGIBLE"})
                self.assertTrue(e["action_in"])
        clean = [e for e in exps.values() if e["family"] == "CLEAN_SCALABLE_WIN"]
        self.assertTrue(clean)
        for e in clean:
            self.assertEqual("ELIGIBLE", e["scale_state"])
            self.assertEqual(["SCALE"], e["action_in"])

    def test_the_new_seed_generates_reproducibly(self) -> None:
        gen = _load("gen2", "heldout_generator_v07.py")
        a = gen.generate(PREREG["heldout_seed"], PREREG["per_family"])
        b = gen.generate(PREREG["heldout_seed"], PREREG["per_family"])
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
