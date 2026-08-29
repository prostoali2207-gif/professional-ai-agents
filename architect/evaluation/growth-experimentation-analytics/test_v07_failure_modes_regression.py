#!/usr/bin/env python3
"""Targeted regressions for the four candidate failure modes observed in gate v0.7.

Run 33239983604, seed 20260829. No provider calls, and no oracle or harness change: the
grader used here is the one the gate ran, unmodified, because the audit found no instrument
defect behind these failures.

Scope, stated honestly. These tests lock two things:

  * **detection** -- each observed failure is replayed as a concrete result and must be
    rejected, so a recurrence cannot slip through a future gate;
  * **rule presence** -- the v0.8 overlay states each rule the candidate was missing, so the
    repair cannot be silently dropped.

They cannot show the candidate now behaves correctly. Nothing short of a fresh gate can.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OVERLAY = ROOT / "architect/research/growth-experimentation-analytics/professional-model-candidate-v0.8-overlay.md"


def overlay_text() -> str:
    """Whitespace-normalised, so a content assertion tests the rule rather than the line wrap.

    Reflowing the document to satisfy a brittle assertion would be fitting the artifact to the
    test; normalising the assertion is the correct direction.
    """
    return " ".join(OVERLAY.read_text(encoding="utf-8").split())


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


grader = _load("grd07", "grader_v07_structural.py")
generator = _load("gen07", "heldout_generator_v07.py")
audit = _load("oracle_audit", "oracle_audit.py")

GATE_SEED = 20260829
GATE_PER_FAMILY = 2


def gate_suite():
    cases, oracle = generator.generate(GATE_SEED, GATE_PER_FAMILY)
    return {f["fixture_id"]: f for f in cases["fixtures"]}, oracle["expectations"]


def correct(fixtures, expectations, fid):
    return audit.build_passing_result(fixtures[fid], expectations[fid])


class FailureA_InconclusiveAimedAtAnArm(unittest.TestCase):
    """3 trials: HO-SBI-01 t1, t2 and HO-SBI-02 t3."""

    def test_the_observed_failure_is_rejected(self) -> None:
        fixtures, expectations = gate_suite()
        for fid in ("HO-SBI-01", "HO-SBI-02"):
            arm = next(a for a in fixtures[fid]["case"]["arms"] if a != "experiment")
            observed = correct(fixtures, expectations, fid)
            observed["recommendation"] = "INCONCLUSIVE"
            observed["decision_record"]["operational"].update({"action": "INCONCLUSIVE", "target": arm})
            with self.subTest(fixture=fid):
                report = grader.grade(observed, fixtures[fid], expectations[fid])
                self.assertFalse(report["pass"])
                self.assertTrue(any("may only be aimed at" in f for f in report["failures"]), report["failures"])

    def test_the_corrected_form_is_accepted(self) -> None:
        fixtures, expectations = gate_suite()
        for fid in ("HO-SBI-01", "HO-SBI-02"):
            fixed = correct(fixtures, expectations, fid)
            fixed["recommendation"] = "INCONCLUSIVE"
            fixed["decision_record"]["operational"].update({"action": "INCONCLUSIVE", "target": "experiment"})
            with self.subTest(fixture=fid):
                self.assertTrue(grader.grade(fixed, fixtures[fid], expectations[fid])["pass"])

    def test_iterate_at_an_arm_remains_available(self) -> None:
        """The repair must not push the candidate into never naming an arm."""
        fixtures, expectations = gate_suite()
        fid = "HO-SBI-01"
        arm = next(a for a in expectations[fid]["target_by_action"]["ITERATE"] if a != "experiment")
        result = correct(fixtures, expectations, fid)
        result["recommendation"] = "ITERATE"
        result["decision_record"]["operational"].update({"action": "ITERATE", "target": arm})
        self.assertTrue(grader.grade(result, fixtures[fid], expectations[fid])["pass"])

    def test_the_overlay_states_the_scope_mapping(self) -> None:
        text = overlay_text()
        self.assertIn("verdicts on the **registered comparison as a whole**", text)
        self.assertIn("`KILL` and `SCALE` act on **one arm**", text)
        self.assertIn("`ITERATE` may act on either", text)


class FailureB_SparsityDowngradedIdentification(unittest.TestCase):
    """1 trial, P0: HO-SBI-02 t2."""

    def test_the_observed_failure_is_rejected(self) -> None:
        fixtures, expectations = gate_suite()
        fid = "HO-SBI-02"
        observed = correct(fixtures, expectations, fid)
        observed["decision_record"]["causal"].update(
            {"status": "UNRESOLVED", "claim_ceiling": "DESCRIPTIVE_ASSOCIATION"})
        report = grader.grade(observed, fixtures[fid], expectations[fid])
        self.assertFalse(report["pass"])
        self.assertTrue(any("precision problem" in f for f in report["failures"]), report["failures"])

    def test_identification_is_kept_while_the_action_stays_bounded(self) -> None:
        """The corrected shape: identified and INCREMENTAL_CAUSAL, action INCONCLUSIVE, SCALE blocked."""
        fixtures, expectations = gate_suite()
        fid = "HO-SBI-02"
        fixed = correct(fixtures, expectations, fid)
        causal = fixed["decision_record"]["causal"]
        self.assertEqual(causal["status"], "IDENTIFIED")
        self.assertEqual(causal["claim_ceiling"], "INCREMENTAL_CAUSAL")
        self.assertEqual(fixed["decision_record"]["scale_readiness"]["state"], "BLOCKED")
        self.assertIn("INSUFFICIENT_SAMPLE", fixed["decision_record"]["scale_readiness"]["blocking_reasons"])
        self.assertTrue(grader.grade(fixed, fixtures[fid], expectations[fid])["pass"])

    def test_a_real_design_problem_still_lowers_identification(self) -> None:
        """The reconciliation must not make the ceiling unlowerable."""
        fixtures, expectations = gate_suite()
        fid = "HO-UDC-01"
        overclaim = correct(fixtures, expectations, fid)
        overclaim["decision_record"]["causal"].update(
            {"status": "IDENTIFIED", "claim_ceiling": "INCREMENTAL_CAUSAL", "blocking_confounders": []})
        overclaim["confounders"] = []
        self.assertFalse(grader.grade(overclaim, fixtures[fid], expectations[fid])["pass"])

    def test_the_overlay_reconciles_the_two_rules(self) -> None:
        text = overlay_text()
        self.assertIn("insufficient power", text.lower())
        self.assertIn("bears on the action", text)
        self.assertIn("A count problem never does", text)


class FailureC_UnpermittedField(unittest.TestCase):
    """1 trial: HO-UDC-02 t2 added `none_decidable_reason`."""

    def test_the_observed_failure_is_rejected(self) -> None:
        fixtures, expectations = gate_suite()
        fid = "HO-UDC-02"
        observed = correct(fixtures, expectations, fid)
        observed["decision_record"]["operational"]["none_decidable_reason"] = "counts too small"
        report = grader.grade(observed, fixtures[fid], expectations[fid])
        self.assertFalse(report["pass"])
        self.assertTrue(any("Additional properties" in f or "unexpected property" in f
                            for f in report["failures"]), report["failures"])

    def test_any_invented_field_anywhere_is_rejected(self) -> None:
        fixtures, expectations = gate_suite()
        fid = "HO-UDC-02"
        for path in (["decision_record", "causal"], ["decision_record", "operational"],
                     ["decision_record", "scale_readiness"], ["decision_record"], []):
            observed = correct(fixtures, expectations, fid)
            node = observed
            for key in path:
                node = node[key]
            node["smuggled_note"] = "x"
            with self.subTest(location="/".join(path) or "$"):
                self.assertFalse(grader.grade(observed, fixtures[fid], expectations[fid])["pass"])

    def test_the_prose_fields_remain_the_place_for_extra_narrative(self) -> None:
        fixtures, expectations = gate_suite()
        fid = "HO-UDC-02"
        verbose = correct(fixtures, expectations, fid)
        verbose["rationale"] = "counts too small to estimate; recorded here rather than as a new field"
        verbose["claim_boundaries"] = ["nothing decidable beyond the stated ceiling"]
        self.assertTrue(grader.grade(verbose, fixtures[fid], expectations[fid])["pass"])

    def test_the_overlay_states_the_contract_is_closed(self) -> None:
        text = overlay_text()
        self.assertIn("The output contract is **closed**", text)
        self.assertIn("Inventing a field does not add information", text)


class FailureD_InvalidJson(unittest.TestCase):
    """1 execution error: HO-SBI-02 t1 returned unparseable output."""

    def test_unparseable_output_is_never_scored_as_a_pass(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            standin = Path(td) / "broken.py"
            standin.write_text("import sys; sys.stdout.write('{\"fixture_id\": \"HO-SBI-01\",}'); sys.exit(0)\n")
            proc = subprocess.run(
                [sys.executable, str(HERE / "adapters" / "stdio_candidate_adapter.py")],
                input=json.dumps({"fixture_id": "HO-SBI-01"}), text=True, capture_output=True, cwd=ROOT,
                env={**__import__("os").environ,
                     "ANALYTICS_CANDIDATE_MANIFEST": "architect/evaluation/growth-experimentation-analytics/candidate-freeze-v0.7.json",
                     "ANALYTICS_CANDIDATE_CMD": f"{sys.executable} {standin}"}, timeout=60)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("non-JSON", proc.stderr)

    def test_the_overlay_states_output_validity(self) -> None:
        text = overlay_text()
        self.assertIn("exactly one JSON object that parses on the first attempt", text)
        self.assertIn("is not a weaker answer, it is no answer", text)


class RepairIsMinimalAndAdditive(unittest.TestCase):
    def test_no_frozen_v01_to_v06_component_was_modified(self) -> None:
        frozen = json.loads((HERE / "candidate-freeze-v0.7.json").read_text())
        for component in frozen["assembly"]:
            actual = subprocess.check_output(["git", "hash-object", component["path"]],
                                             text=True, cwd=ROOT).strip()
            with self.subTest(path=component["path"]):
                self.assertEqual(actual, component["git_blob_sha"],
                                 "v0.8 must be additive; the frozen v0.1-v0.6 components are untouched")

    def test_the_overlay_adds_no_new_professional_judgement(self) -> None:
        text = overlay_text()
        self.assertIn("adds **no new professional judgement**", text)
        self.assertIn("Nothing in v0.1–v0.6 is relaxed", text)

    def test_the_oracle_and_harness_were_not_touched(self) -> None:
        """The audit found no instrument defect behind these failures, so none was changed."""
        changed = subprocess.check_output(
            ["git", "status", "--short", "architect/evaluation/growth-experimentation-analytics/"],
            text=True, cwd=ROOT).splitlines()
        touched = [line.split()[-1] for line in changed if line.strip()]
        for path in touched:
            with self.subTest(path=path):
                self.assertTrue(path.endswith("test_v07_failure_modes_regression.py"),
                                f"unexpected instrument change: {path}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
