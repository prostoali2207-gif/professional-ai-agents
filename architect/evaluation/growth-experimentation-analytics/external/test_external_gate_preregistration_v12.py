#!/usr/bin/env python3
"""Deterministic verification of the v1.2 external release gate before it is run.

No provider calls. Two obligations specific to this cycle:

* **only the candidate changed** — issue #205 forbids moving the grader, tier map, thresholds or
  criterion to chase a pass, and each is asserted identical to the cycle that produced run
  `33299723985`;
* **the repair is a procedure, not a fourth restatement** — the v1.1 ledger showed that restating
  an existing rule did not change behavior, so the addition is checked for the shape that did.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANALYTICS = HERE.parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))

PREREG = json.loads((HERE / "preregistration-external-v1.2-2026-09-09.json")
                    .read_text(encoding="utf-8"))
PREVIOUS = json.loads((HERE / "preregistration-external-v1.1-2026-09-05.json")
                      .read_text(encoding="utf-8"))
FREEZE = json.loads((ANALYTICS / "candidate-freeze-v1.2.json").read_text(encoding="utf-8"))
FREEZE_V11 = json.loads((ANALYTICS / "candidate-freeze-v1.1.json").read_text(encoding="utf-8"))
RUNNER = HERE / "run_external_heldout_gate_v11.py"
AUTHOR = HERE / "author_external_heldout_v1.py"
V11_EXECUTED_COMMIT = "b1818d580208b874b14e331803c3497c498d3675"


def blob(path: str) -> str:
    return subprocess.check_output(["git", "hash-object", path], text=True, cwd=ROOT).strip()


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


C = _load("classifier", ANALYTICS / "trial_outcome_classifier.py")
NOVELTY = _load("novelty_v12", HERE / "external_pack_novelty_v12.py")
NOVELTY_V11 = _load("novelty_v11", HERE / "external_pack_novelty_v11.py")


class OnlyTheCandidateChanged(unittest.TestCase):
    def test_the_grader_is_byte_identical_and_untouched(self) -> None:
        self.assertEqual(PREVIOUS["grader"]["git_blob_sha"], PREREG["grader"]["git_blob_sha"])
        self.assertEqual(PREREG["grader"]["git_blob_sha"], blob(PREREG["grader"]["path"]))

    def test_the_classifier_and_tier_map_are_byte_identical(self) -> None:
        self.assertEqual(PREVIOUS["classifier"], PREREG["classifier"])
        self.assertEqual(C.RULES_DIGEST, PREREG["tier_map_digest"])
        self.assertEqual(PREVIOUS["tier_map_digest"], PREREG["tier_map_digest"])

    def test_the_authoring_schemas_and_oracle_are_byte_identical_this_time(self) -> None:
        """Unlike the v1.1 cycle, the pack contract did not need to move at all."""
        self.assertEqual(PREVIOUS["pack_contract"]["git_blob_sha"],
                         PREREG["pack_contract"]["git_blob_sha"])
        self.assertEqual(PREREG["pack_contract"]["git_blob_sha"],
                         blob(PREREG["pack_contract"]["path"]))

    def test_every_threshold_and_the_criterion_are_unchanged(self) -> None:
        for key in ("trials_per_fixture", "total_trials", "per_family", "families",
                    "retries_permitted", "best_of_n", "tier1_tolerance",
                    "tier2_per_fixture_cap", "tier2_total_cap", "pass_rule", "tier_definitions",
                    "hard_fails", "execution_policy"):
            with self.subTest(key=key):
                self.assertEqual(PREVIOUS[key], PREREG[key])

    def test_the_runner_is_byte_identical(self) -> None:
        self.assertEqual(PREVIOUS["runner"], PREREG["runner"])
        self.assertEqual(PREREG["runner"]["git_blob_sha"], blob(PREREG["runner"]["path"]))

    def test_the_output_and_fixture_contracts_are_unchanged(self) -> None:
        for key in ("output_contract_path", "output_contract_git_blob_sha",
                    "fixture_contract_path"):
            with self.subTest(key=key):
                self.assertEqual(FREEZE_V11[key], FREEZE[key])
        self.assertEqual(FREEZE_V11["instrument"], FREEZE["instrument"])

    def test_the_candidate_is_the_thing_that_moved(self) -> None:
        self.assertNotEqual(FREEZE_V11["assembly_digest"], FREEZE["assembly_digest"])
        self.assertEqual(FREEZE_V11["assembly_digest"], PREREG["supersedes_candidate_digest"])
        self.assertEqual(FREEZE["assembly_digest"], PREREG["candidate_assembly_digest"])
        self.assertEqual(1, len(FREEZE["assembly"]))
        component = FREEZE["assembly"][0]
        self.assertTrue(component["path"].endswith("professional-model-consolidated-v1.2.md"))
        self.assertEqual(component["git_blob_sha"], blob(component["path"]))

    def test_every_bound_blob_matches_the_file_on_disk(self) -> None:
        for key in PREREG["bound_apparatus"]:
            with self.subTest(key=key):
                self.assertEqual(PREREG[key]["git_blob_sha"], blob(PREREG[key]["path"]))

    def test_the_only_apparatus_that_moved_is_the_novelty_guard_and_its_loader(self) -> None:
        moved = [key for key in PREREG["bound_apparatus"]
                 if key in PREVIOUS and PREREG[key]["git_blob_sha"]
                 != PREVIOUS[key]["git_blob_sha"]]
        self.assertEqual(["novelty", "author"], sorted(moved, key=["novelty", "author"].index))


class TheRepairIsAProcedureNotAFourthRestatement(unittest.TestCase):
    def test_the_preregistration_records_why_a_wording_patch_was_refused(self) -> None:
        block = PREREG["candidate_repair_under_test"]
        self.assertIn("11 to 0", block["why_not_another_wording_patch"])
        self.assertIn("4 to 6", block["why_not_another_wording_patch"])
        self.assertIn("does not state it a fourth", block["why_not_another_wording_patch"])

    def test_the_predecessor_verdict_is_not_reinterpreted(self) -> None:
        self.assertIn("FAIL", PREREG["candidate_repair_under_test"]["predecessor_result"])
        self.assertIn("stands and is not", PREREG["candidate_repair_under_test"]["predecessor_result"])

    def test_the_residuals_are_justified_by_one_root_cause(self) -> None:
        shape = PREREG["candidate_repair_under_test"]["repair_shape"]
        self.assertIn("channel-separation failures", shape)
        self.assertIn("no fixture-specific rule was added", shape.lower())

    def test_the_proofs_and_regressions_exist(self) -> None:
        block = PREREG["candidate_repair_under_test"]
        for key in ("non_weakening_proof", "targeted_regressions"):
            with self.subTest(key=key):
                path = block[key].split(" -- ")[0].strip()
                self.assertTrue((ROOT / path).is_file(), path)
        self.assertTrue((ROOT / PREREG["repair_authority"]).is_file())

    def test_the_adjudication_separates_evidence_grades_and_states_residual_risk(self) -> None:
        text = (ROOT / PREREG["repair_authority"]).read_text(encoding="utf-8")
        for label in ("**FACT", "**INFERENCE", "**HYPOTHESIS"):
            with self.subTest(label=label):
                self.assertIn(label, text)
        self.assertIn("a self-check is weaker than a mechanical constraint", " ".join(text.split()))


class TheNoveltyGuardGrewRatherThanReset(unittest.TestCase):
    def test_it_still_refuses_everything_the_previous_guard_refused(self) -> None:
        self.assertTrue(NOVELTY_V11.REFUSED.issubset(NOVELTY.REFUSED))

    def test_it_adds_the_identifiers_the_v11_ledger_named(self) -> None:
        for observed in ("plan_comparison_q3", "premium_plan"):
            with self.subTest(identifier=observed):
                with self.assertRaises(NOVELTY.NotNovel):
                    NOVELTY.check_identifier(observed, "arm")

    def test_it_admits_an_unseen_identifier(self) -> None:
        self.assertEqual("harbour_pilot_route",
                         NOVELTY.check_identifier("harbour_pilot_route", "arm"))

    def test_prose_fields_are_still_exempt(self) -> None:
        NOVELTY.check_case({"domain": "a premium_plan comparison",
                            "stakeholder_pressure": "ship plan_comparison_q3 now",
                            "confound": "ui_experiment ran concurrently"}, "F")

    def test_the_v11_module_was_not_edited(self) -> None:
        """The preregistration that bound it must still describe what that cycle ran."""
        at_run = subprocess.check_output(
            ["git", "rev-parse",
             f"{V11_EXECUTED_COMMIT}:{PREVIOUS['novelty']['path']}"], text=True, cwd=ROOT).strip()
        self.assertEqual(at_run, blob(PREVIOUS["novelty"]["path"]))

    def test_the_author_loads_the_guard_this_preregistration_names(self) -> None:
        source = AUTHOR.read_text(encoding="utf-8")
        self.assertIn('load_novelty(prereg["novelty"]["path"])', source)
        self.assertNotIn("import external_pack_novelty_v11 as novelty", source)
        self.assertNotIn("import external_pack_novelty_v12", source)

    def test_the_runner_still_refuses_a_pack_authored_without_the_guard(self) -> None:
        self.assertIn("the preregistration requires the novelty",
                      RUNNER.read_text(encoding="utf-8"))


class PolicyIsStated(unittest.TestCase):
    def test_the_post_gate_policy_forbids_a_further_repair_cycle(self) -> None:
        policy = PREREG["post_gate_policy"]
        self.assertIn("no further repair cycle after the result", policy)
        self.assertIn("A FAIL ends the cycle", policy)

    def test_the_gate_id_is_new_and_supersedes_the_previous_one(self) -> None:
        self.assertNotEqual(PREVIOUS["gate_id"], PREREG["gate_id"])
        self.assertEqual(PREVIOUS["gate_id"], PREREG["supersedes_cycle"])

    def test_the_author_is_not_told_the_candidate_was_repaired(self) -> None:
        self.assertFalse(PREREG["external_authorship"]["author_sees_the_repair"])
        self.assertIn("or that an identification ledger exists",
                      PREREG["external_authorship"]["rationale"])
        source = AUTHOR.read_text(encoding="utf-8")
        window = source[source.find("FAMILY_BRIEFS"):source.find("def sha256_hex")]
        for leak in ("ledger", "identification ledger", "repair", "v1.2", "tier-1"):
            with self.subTest(leak=leak):
                self.assertNotIn(leak, window)

    def test_the_on_pass_actions_leave_one_unambiguous_status(self) -> None:
        joined = " ".join(PREREG["on_pass"]).lower()
        for action in ("manifest", "qualification record", "catalog", "supersede", "limitation"):
            with self.subTest(action=action):
                self.assertIn(action, joined)


if __name__ == "__main__":
    unittest.main(verbosity=2)
