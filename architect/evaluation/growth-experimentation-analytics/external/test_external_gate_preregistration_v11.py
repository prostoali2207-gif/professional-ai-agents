#!/usr/bin/env python3
"""Deterministic verification of the v1.1 external release gate before it is run.

No provider calls. The obligation specific to this cycle: **only the candidate changed.** If a
repair cycle also moved the grader, the oracle, the authoring schemas or any threshold, a better
result would not be attributable to the repair. Each of those is asserted byte-identical to the
cycle that produced run 33293694601.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANALYTICS = HERE.parent
ROOT = HERE.parents[3]

PREREG = json.loads((HERE / "preregistration-external-v1.1-2026-09-05.json")
                    .read_text(encoding="utf-8"))
PREVIOUS = json.loads((HERE / "preregistration-external-2026-09-02.json").read_text(encoding="utf-8"))
FREEZE = json.loads((ANALYTICS / "candidate-freeze-v1.1.json").read_text(encoding="utf-8"))
FREEZE_V10 = json.loads((ANALYTICS / "candidate-freeze-v1.0.json").read_text(encoding="utf-8"))
RUNNER = HERE / "run_external_heldout_gate_v11.py"
AUTHOR = HERE / "author_external_heldout_v1.py"


def blob(path: str) -> str:
    return subprocess.check_output(["git", "hash-object", path], text=True, cwd=ROOT).strip()


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


C = _load("classifier", ANALYTICS / "trial_outcome_classifier.py")
NOVELTY = _load("novelty", HERE / "external_pack_novelty_v11.py")
PACK = _load("pack_contract", HERE / "external_pack_contract.py")


class OnlyTheCandidateChanged(unittest.TestCase):
    def test_the_grader_is_byte_identical_to_the_previous_cycle(self) -> None:
        self.assertEqual(PREVIOUS["grader"]["git_blob_sha"], PREREG["grader"]["git_blob_sha"])
        self.assertEqual(PREREG["grader"]["git_blob_sha"], blob(PREREG["grader"]["path"]))

    def test_the_classifier_and_tier_map_are_byte_identical(self) -> None:
        self.assertEqual(PREVIOUS["classifier"]["git_blob_sha"],
                         PREREG["classifier"]["git_blob_sha"])
        self.assertEqual(C.RULES_DIGEST, PREREG["tier_map_digest"])
        self.assertEqual(PREVIOUS["tier_map_digest"], PREREG["tier_map_digest"])

    def test_the_authoring_schemas_and_oracle_are_byte_identical(self) -> None:
        self.assertEqual(PREVIOUS["pack_contract"]["git_blob_sha"],
                         PREREG["pack_contract"]["git_blob_sha"])

    def test_every_threshold_is_unchanged(self) -> None:
        for key in ("trials_per_fixture", "total_trials", "per_family", "families",
                    "retries_permitted", "best_of_n", "tier1_tolerance",
                    "tier2_per_fixture_cap", "tier2_total_cap", "pass_rule", "tier_definitions"):
            with self.subTest(key=key):
                self.assertEqual(PREVIOUS[key], PREREG[key])

    def test_the_output_and_fixture_contracts_are_unchanged(self) -> None:
        for key in ("output_contract_path", "output_contract_git_blob_sha",
                    "fixture_contract_path"):
            with self.subTest(key=key):
                self.assertEqual(FREEZE_V10[key], FREEZE[key])

    def test_the_candidate_is_the_thing_that_moved(self) -> None:
        self.assertNotEqual(FREEZE_V10["assembly_digest"], FREEZE["assembly_digest"])
        self.assertEqual(FREEZE_V10["assembly_digest"], PREREG["supersedes_candidate_digest"])
        self.assertEqual(FREEZE["assembly_digest"], PREREG["candidate_assembly_digest"])

    def test_the_frozen_candidate_is_the_repaired_document(self) -> None:
        self.assertEqual(1, len(FREEZE["assembly"]))
        component = FREEZE["assembly"][0]
        self.assertTrue(component["path"].endswith("professional-model-consolidated-v1.1.md"))
        self.assertEqual(component["git_blob_sha"], blob(component["path"]))

    def test_the_instrument_is_byte_identical_to_freeze_v10(self) -> None:
        self.assertEqual(FREEZE_V10["instrument"], FREEZE["instrument"])
        for role, ref in FREEZE["instrument"].items():
            with self.subTest(role=role):
                self.assertEqual(ref["git_blob_sha"], blob(ref["path"]))


class TheNoveltyGuardIsRealAndBound(unittest.TestCase):
    def test_the_guard_is_enforced_and_bound_as_apparatus(self) -> None:
        self.assertTrue(PREREG["novelty_guard"]["enforced"])
        self.assertIn("novelty", PREREG["bound_apparatus"])
        self.assertEqual(PREREG["novelty"]["git_blob_sha"], blob(PREREG["novelty"]["path"]))
        self.assertEqual(PREREG["novelty_guard"]["module"], PREREG["novelty"]["path"])

    def test_it_refuses_every_identifier_the_previous_ledger_named(self) -> None:
        for observed in ("ui_experiment", "ui_refresh", "legacy_ui", "pricing_test", "price_opt",
                         "bundle_off", "sort_algorithm_test", "personalized_sort",
                         "guided_tour_flow", "onboarding_experience_test",
                         "signup_channel_analysis", "email_marketing_cpc"):
            with self.subTest(identifier=observed):
                with self.assertRaises(NOVELTY.NotNovel):
                    NOVELTY.check_identifier(observed, "arm")

    def test_it_refuses_the_repositorys_own_public_construct_scenarios(self) -> None:
        for public in ("directory_listings", "checkout_compact", "trial_lesson_offer",
                       "procurement_walkthrough", "trade_publication"):
            with self.subTest(identifier=public):
                with self.assertRaises(NOVELTY.NotNovel):
                    NOVELTY.check_identifier(public, "arm")

    def test_it_admits_an_unseen_identifier(self) -> None:
        self.assertEqual("warehouse_pick_path",
                         NOVELTY.check_identifier("warehouse_pick_path", "arm"))

    def test_it_is_case_insensitive_and_does_not_choke_on_non_strings(self) -> None:
        with self.assertRaises(NOVELTY.NotNovel):
            NOVELTY.check_identifier("UI_Experiment", "arm")
        NOVELTY.check_case({"domain": "ui_experiment is discussed here", "spend": 12}, "F")

    def test_prose_fields_are_exempt_so_a_domain_sentence_cannot_trip_it(self) -> None:
        NOVELTY.check_case({"domain": "a pricing_test for a retailer",
                            "stakeholder_pressure": "ship the ui_refresh now",
                            "confound": "legacy_ui ran on different budget pacing"}, "F")

    def test_the_author_applies_the_guard_when_the_preregistration_requires_it(self) -> None:
        source = AUTHOR.read_text(encoding="utf-8")
        self.assertIn("novelty.check_case(one, family)", source)
        self.assertIn("if enforce_novelty:", source)
        self.assertIn('bool(prereg.get("novelty_guard", {}).get("enforced"))', source)

    def test_the_runner_refuses_a_pack_authored_without_the_guard(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("the preregistration requires the novelty", source)


class TheCycleIdentityIsCarriedByTheDocumentNotTheCode(unittest.TestCase):
    """Hardcoding the cycle in the author is how a pack gets sealed against the wrong candidate."""

    def test_the_author_carries_no_hardcoded_cycle_or_digest(self) -> None:
        source = AUTHOR.read_text(encoding="utf-8")
        self.assertNotIn("analytics-external-heldout-2026-09-02", source)
        self.assertNotIn("3f4f3e133e81b00a1536fc6c72f1f59c24ef9f7b4c50c762c3c6c5bf6c4dd63d", source)
        self.assertIn('prereg["gate_id"]', source)
        self.assertIn('prereg["candidate_assembly_digest"]', source)

    def test_the_runner_rejects_a_pack_sealed_for_another_cycle_or_candidate(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("PACK CYCLE MISMATCH", source)
        self.assertIn("PACK WAS AUTHORED AGAINST A DIFFERENT CANDIDATE", source)

    def test_the_gate_id_is_new(self) -> None:
        self.assertNotEqual(PREVIOUS["gate_id"], PREREG["gate_id"])
        self.assertEqual(PREVIOUS["gate_id"], PREREG["supersedes_cycle"])


class TheRepairIsDeclaredAndTraceable(unittest.TestCase):
    def test_the_predecessor_verdict_is_not_reinterpreted(self) -> None:
        text = PREREG["candidate_repair_under_test"]["predecessor_result"]
        self.assertIn("INVALID", text)
        self.assertIn("is not converted to a FAIL", text)

    def test_all_four_classes_are_named_with_their_counts(self) -> None:
        classes = PREREG["candidate_repair_under_test"]["classes_repaired"]
        self.assertEqual({"A", "B", "C", "D"}, set(classes))
        self.assertIn("11 tier-1", classes["A"])
        self.assertIn("8 tier-2", classes["D"])

    def test_the_non_weakening_proof_and_regressions_exist(self) -> None:
        block = PREREG["candidate_repair_under_test"]
        for key in ("non_weakening_proof", "targeted_regressions"):
            with self.subTest(key=key):
                path = block[key].split(" -- ")[0].strip()
                self.assertTrue((ROOT / path).is_file(), path)

    def test_the_adjudication_is_cited(self) -> None:
        self.assertTrue((ROOT / PREREG["repair_authority"]).is_file())

    def test_the_criterion_weakness_is_recorded_rather_than_corrected(self) -> None:
        note = PREREG["criterion_unchanged_from"]
        self.assertIn("deliberately left uncorrected", note)
        self.assertIn("fitting the criterion to an outcome", note)

    def test_the_cross_model_protocol_is_reused_without_reopening(self) -> None:
        block = PREREG["cross_model_requirement"]
        self.assertEqual("REUSED WITHOUT REOPENING", block["resolution"])
        self.assertTrue((ROOT / block["revision_record"]).is_file())
        self.assertIn("the protocol was not the blocker", block["basis"])


class PolicyIsStated(unittest.TestCase):
    def test_the_post_gate_policy_forbids_a_further_repair_cycle(self) -> None:
        policy = PREREG["post_gate_policy"]
        self.assertIn("no further repair cycle after the result", policy)
        self.assertIn("A FAIL ends the cycle", policy)

    def test_the_execution_policy_forbids_retry_and_best_of_n(self) -> None:
        policy = PREREG["execution_policy"]
        self.assertIn("No retry on any failure class", policy)
        self.assertIn("No best-of-N", policy)
        self.assertIn("never the expectations", policy)

    def test_the_author_is_not_told_the_candidate_was_repaired(self) -> None:
        self.assertFalse(PREREG["external_authorship"]["author_sees_the_repair"])
        source = AUTHOR.read_text(encoding="utf-8")
        for leak in ("repair", "v1.1", "tier-1", "failed", "previous cycle"):
            with self.subTest(leak=leak):
                self.assertNotIn(leak, source[source.find("FAMILY_BRIEFS"):
                                              source.find("def sha256_hex")])

    def test_the_hard_fails_cover_the_novelty_and_provenance_guards(self) -> None:
        joined = " ".join(PREREG["hard_fails"]).lower()
        for topic in ("tier-1", "tier-2", "candidate call", "family", "novelty guard", "drift"):
            with self.subTest(topic=topic):
                self.assertIn(topic, joined)

    def test_the_on_pass_actions_leave_one_unambiguous_status(self) -> None:
        joined = " ".join(PREREG["on_pass"]).lower()
        for action in ("manifest", "qualification record", "catalog", "supersede", "limitation"):
            with self.subTest(action=action):
                self.assertIn(action, joined)


if __name__ == "__main__":
    unittest.main(verbosity=2)
