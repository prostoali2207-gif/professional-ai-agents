#!/usr/bin/env python3
"""Deterministic verification of the external release gate before it is run.

No provider calls. Establishes that the preregistration says what the adopted stability audit and
the closure record say, that the runner implements it rather than something adjacent, that the
author cannot reach the candidate, and that nothing professional was touched.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANALYTICS = HERE.parent
ROOT = HERE.parents[3]

PREREG = json.loads((HERE / "preregistration-external-2026-09-02.json").read_text(encoding="utf-8"))
PASSED = json.loads((ANALYTICS / "preregistration-v1.0-twotier-2026-09-01.json")
                    .read_text(encoding="utf-8"))
FREEZE = json.loads((ANALYTICS / "candidate-freeze-v1.0.json").read_text(encoding="utf-8"))
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
PACK = _load("pack_contract", HERE / "external_pack_contract.py")


class TheCriterionIsTheOneAlreadyAdopted(unittest.TestCase):
    """Re-tuning the criterion for a new pack would be indistinguishable from fitting it."""

    def test_every_threshold_matches_the_gate_that_passed(self) -> None:
        for key in ("trials_per_fixture", "total_trials", "per_family", "retries_permitted",
                    "best_of_n", "tier1_tolerance", "tier2_per_fixture_cap", "tier2_total_cap",
                    "tier_map_digest"):
            with self.subTest(key=key):
                self.assertEqual(PASSED[key], PREREG[key])

    def test_the_family_set_matches(self) -> None:
        self.assertEqual(sorted(PASSED["families"]), sorted(PREREG["families"]))
        self.assertEqual(sorted(PACK.FAMILIES), sorted(PREREG["families"]))

    def test_the_pass_rule_is_the_same_sentence(self) -> None:
        self.assertEqual(PASSED["pass_rule"], PREREG["pass_rule"])

    def test_the_per_fixture_cap_leaves_at_least_five_judged_trials(self) -> None:
        self.assertGreaterEqual(
            PREREG["trials_per_fixture"] - PREREG["tier2_per_fixture_cap"], 5)

    def test_the_criterion_and_closure_authorities_exist(self) -> None:
        for key in ("criterion_authority", "closure_authority"):
            with self.subTest(key=key):
                self.assertTrue((ROOT / PREREG[key]).is_file(), PREREG[key])


class TheCrossModelRequirementIsResolvedBeforeExecution(unittest.TestCase):
    def test_the_revision_is_recorded_rather_than_implied(self) -> None:
        block = PREREG["cross_model_requirement"]
        self.assertEqual("FORMALLY REVISED BEFORE EXECUTION", block["resolution"])
        self.assertTrue((ROOT / block["revision_record"]).is_file())
        self.assertIn("ChatGPT", block["historical_rule"])
        self.assertIn("Claude", block["historical_rule"])

    def test_every_excluded_family_carries_its_reason(self) -> None:
        findings = " ".join(PREREG["cross_model_requirement"]["eligibility_findings"])
        for family in ("Gemini", "Groq", "OpenAI", "Claude"):
            with self.subTest(family=family):
                self.assertIn(family, findings)

    def test_the_claim_is_narrowed_rather_than_the_bar_lowered(self) -> None:
        block = PREREG["cross_model_requirement"]
        self.assertIn("revalidation trigger", block["claim_narrowing"])
        self.assertIn("scoped to the Gemini candidate runtime family", block["claim_narrowing"])
        boundary = " ".join(PREREG["qualification_boundary"])
        self.assertIn("Cross-runtime portability is untested", boundary)

    def test_authorship_independence_replaces_it_and_has_no_fallback(self) -> None:
        block = PREREG["external_authorship"]
        self.assertTrue(block["required"])
        self.assertIsNone(block["fallback_author_family"])
        self.assertFalse(block["author_sees_candidate"])
        self.assertFalse(block["author_may_state_an_expectation"])
        self.assertTrue(block["candidate_model_family_must_differ"])
        self.assertNotEqual(block["author_family"], PREREG["candidate_model_family"])
        self.assertIn("hard_fail_on_fallback", block)
        self.assertIn("INVALID / NOT EXECUTABLE", block["hard_fail_on_fallback"])


class TheAuthorCannotReachTheCandidate(unittest.TestCase):
    def test_the_author_source_has_no_candidate_execution_path(self) -> None:
        source = AUTHOR.read_text(encoding="utf-8")
        for forbidden in ("executor_gemini", "stdio_candidate_adapter",
                          "ANALYTICS_CANDIDATE_CMD", "ANALYTICS_CANDIDATE_MANIFEST",
                          "professional-model-consolidated"):
            with self.subTest(pattern=forbidden):
                self.assertNotIn(forbidden, source)

    def test_the_author_reports_zero_candidate_calls(self) -> None:
        source = AUTHOR.read_text(encoding="utf-8")
        self.assertIn('"candidate_calls": 0', source)

    def test_the_author_has_no_route_to_the_candidates_own_family(self) -> None:
        """A fallback to Gemini would put author and candidate on one family, so none exists."""
        author = _load("author2", AUTHOR)
        source = AUTHOR.read_text(encoding="utf-8")
        self.assertNotIn("generativelanguage", source)
        self.assertNotIn("GEMINI_API_KEY", source)
        self.assertEqual("Groq", PREREG["external_authorship"]["author_family"])
        self.assertEqual(PREREG["external_authorship"]["author_model"], author.AUTHOR_MODEL)
        self.assertIn("api.groq.com", author.AUTHOR_ENDPOINT)
        self.assertIn("there is no Gemini fallback for authoring", source)

    def test_the_authoring_request_identifies_itself(self) -> None:
        """Regression for run 33293517671.

        urllib's default agent is banned by Cloudflare on api.groq.com (error 1010), which killed
        that run at the authoring step before a single case existed. Every working Groq call in
        this repository sets an explicit agent.
        """
        source = AUTHOR.read_text(encoding="utf-8")
        self.assertIn('"User-Agent"', source)
        self.assertNotIn("Python-urllib", source)
        index = source.find('headers={"Authorization"')
        self.assertGreater(index, 0)
        self.assertIn('"User-Agent"', source[index:index + 400])

    def test_the_burn_record_for_the_voided_run_is_present(self) -> None:
        self.assertEqual(
            ["architect/evaluation/growth-experimentation-analytics/external/"
             "burn-record-33293517671.md"], PREREG["burn_records"])
        record = (ROOT / PREREG["burn_records"][0]).read_text(encoding="utf-8")
        self.assertIn("INVALID", record)
        self.assertIn("Zero Gemini calls", record.replace("zero Gemini calls", "Zero Gemini calls"))
        self.assertIn("Nothing about the candidate", record)

    def test_the_authoring_schema_cannot_carry_an_expectation(self) -> None:
        author = _load("author3", AUTHOR)
        for family in PACK.FAMILIES:
            with self.subTest(family=family):
                schema = author.author_schema_for(family)
                item = schema["properties"]["cases"]["items"]
                self.assertFalse(PACK.schema_can_express_expectation(item))
                # Groq strict json_schema requires a closed object with every property required.
                self.assertIs(False, item["additionalProperties"])
                self.assertEqual(sorted(item["properties"]), sorted(item["required"]))


class RunnerImplementsTheCriterion(unittest.TestCase):
    def test_the_runner_delegates_classification_and_does_not_reimplement_it(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("classifier.classify_trial(", source)
        self.assertIn("classifier.gate_verdict(", source)
        for smuggled in ("429", "RESOURCE_EXHAUSTED", "output contract violation at",
                         "model returned invalid JSON"):
            with self.subTest(pattern=smuggled):
                self.assertNotIn(smuggled, source)

    def test_the_runner_executes_each_trial_exactly_once(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertEqual(1, source.count("subprocess.run("),
                         "more than one invocation site is a retry surface")
        self.assertEqual(1, source.count("for trial in range(1, trials + 1):"))
        for branch in ("if proc.returncode != 0:", "except json.JSONDecodeError:"):
            with self.subTest(branch=branch):
                window = source[source.find(branch):source.find(branch) + 700]
                self.assertIn("ledger.append(entry)", window)
                self.assertIn("continue", window)

    def test_the_runner_calls_the_frozen_grader_with_unchanged_arguments(self) -> None:
        call = "grader.grade(result, fixture, expectations[fixture_id], contract)"
        self.assertIn(call, RUNNER.read_text(encoding="utf-8"))
        self.assertIn(call, (ANALYTICS / "run_heldout_gate_v07.py").read_text(encoding="utf-8"))

    def test_the_executor_never_sees_the_expectations(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        index = source.find("subprocess.run(")
        self.assertGreater(index, 0)
        window = source[index:index + 400]
        self.assertIn("json.dumps(fixture", window)
        self.assertNotIn("expectations", window)

    def test_an_invalid_verdict_exits_with_a_code_that_is_neither_pass_nor_fail(self) -> None:
        self.assertIn('return {"PASS": 0, "FAIL": 1}.get(verdict, 2)',
                      RUNNER.read_text(encoding="utf-8"))

    def test_the_runner_refuses_a_pack_that_fails_any_provenance_hard_fail(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        for guard in ("PACK CYCLE MISMATCH", "PACK WAS AUTHORED AGAINST A DIFFERENT CANDIDATE",
                      "the author called the candidate",
                      "author and candidate share a model family",
                      "PACK CARDINALITY MISMATCH", "PACK FAMILY SET MISMATCH",
                      "PACK IS INTERNALLY INCONSISTENT"):
            with self.subTest(guard=guard):
                self.assertIn(guard, source)

    def test_the_runner_prints_the_pack_digest_before_the_first_trial(self) -> None:
        """The log must prove the pack predates every result."""
        source = RUNNER.read_text(encoding="utf-8")
        digest_line = source.find('pack ciphertext sha256')
        first_trial = source.find("for trial in range(1, trials + 1):")
        self.assertGreater(digest_line, 0)
        self.assertLess(digest_line, first_trial)

    def test_every_bound_blob_matches_the_file_on_disk(self) -> None:
        for key in ("grader", "classifier", "pack_contract", "author", "runner"):
            with self.subTest(key=key):
                self.assertEqual(PREREG[key]["git_blob_sha"], blob(PREREG[key]["path"]))

    def test_the_runner_verifies_all_five_apparatus_blobs_at_run_time(self) -> None:
        self.assertIn('for key in ("grader", "classifier", "pack_contract", "author", "runner")',
                      RUNNER.read_text(encoding="utf-8"))


class NothingProfessionalWasTouched(unittest.TestCase):
    def test_the_candidate_assembly_is_byte_identical_to_freeze_v10(self) -> None:
        for component in FREEZE["assembly"]:
            with self.subTest(path=component["path"]):
                self.assertEqual(component["git_blob_sha"], blob(component["path"]))
        self.assertEqual(PREREG["candidate_assembly_digest"], FREEZE["assembly_digest"])

    def test_the_grader_is_the_one_that_produced_the_passed_ledger(self) -> None:
        self.assertEqual(PASSED["grader"]["git_blob_sha"], PREREG["grader"]["git_blob_sha"])
        self.assertEqual(FREEZE["instrument"]["grader"]["git_blob_sha"],
                         PREREG["grader"]["git_blob_sha"])

    def test_the_classifier_is_the_one_that_produced_the_passed_ledger(self) -> None:
        self.assertEqual(PASSED["classifier"]["git_blob_sha"], PREREG["classifier"]["git_blob_sha"])
        self.assertEqual(C.RULES_DIGEST, PREREG["tier_map_digest"])

    def test_both_contracts_are_unchanged(self) -> None:
        self.assertEqual(FREEZE["output_contract_git_blob_sha"],
                         blob(FREEZE["output_contract_path"]))
        self.assertEqual(FREEZE["instrument"]["generator"]["git_blob_sha"],
                         blob(FREEZE["instrument"]["generator"]["path"]))

    def test_the_runner_that_produced_the_passed_ledger_is_untouched(self) -> None:
        self.assertEqual(PASSED["runner"]["git_blob_sha"], blob(PASSED["runner"]["path"]))

    def test_the_new_pack_does_not_load_the_old_generator(self) -> None:
        """The pack must be independent of the suite already passed, not a wrapper around it.

        Prose may refer to the generator -- the module docstring explains why this pack exists --
        so the check is against executable source with the docstring removed.
        """
        for path in (AUTHOR, HERE / "external_pack_contract.py", RUNNER):
            with self.subTest(path=path.name):
                source = path.read_text(encoding="utf-8")
                docstring = ast.get_docstring(ast.parse(source))
                code = source.replace(docstring, "") if docstring else source
                self.assertNotIn("heldout_generator_v07", code)


class HardFailsAndPolicyAreStated(unittest.TestCase):
    def test_every_hard_fail_has_a_guard(self) -> None:
        self.assertGreaterEqual(len(PREREG["hard_fails"]), 7)
        joined = " ".join(PREREG["hard_fails"]).lower()
        for topic in ("tier-1", "tier-2", "candidate call", "family", "digest", "drift"):
            with self.subTest(topic=topic):
                self.assertIn(topic, joined)

    def test_the_post_gate_policy_forbids_repair_and_rerun(self) -> None:
        policy = PREREG["post_gate_policy"]
        self.assertIn("No automatic repair and no automatic rerun", policy)
        self.assertIn("A FAIL ends the cycle", policy)

    def test_the_execution_policy_forbids_retry_and_best_of_n(self) -> None:
        policy = PREREG["execution_policy"]
        self.assertIn("No retry on any failure class", policy)
        self.assertIn("No best-of-N", policy)
        self.assertIn("never the expectations", policy)

    def test_the_on_pass_actions_leave_one_unambiguous_status(self) -> None:
        joined = " ".join(PREREG["on_pass"]).lower()
        for action in ("manifest", "qualification record", "catalog", "supersede", "limitation"):
            with self.subTest(action=action):
                self.assertIn(action, joined)


if __name__ == "__main__":
    unittest.main(verbosity=2)
