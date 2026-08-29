#!/usr/bin/env python3
"""Freeze / grader / generator / threshold non-weakening check for consolidated v1.0.

A consolidation cycle is the easiest place to quietly relax a gate: rewrite the candidate, and
while the freeze is being reissued, loosen a threshold or drop a freeze rule. This file makes that
mechanically impossible to do silently.

Everything here is deterministic. No provider calls.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

V08 = json.loads((HERE / "candidate-freeze-v0.8.json").read_text(encoding="utf-8"))
V10 = json.loads((HERE / "candidate-freeze-v1.0.json").read_text(encoding="utf-8"))
PREREG_V08 = json.loads(
    (HERE / "preregistration-v0.8-heldout-2026-08-30.json").read_text(encoding="utf-8"))


def blob(path: str) -> str:
    return subprocess.check_output(["git", "hash-object", path], text=True, cwd=ROOT).strip()


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class InstrumentIdenticalToV08(unittest.TestCase):
    def test_the_new_freeze_binds_the_same_instrument_blobs(self) -> None:
        self.assertEqual(V08["instrument"], V10["instrument"])

    def test_those_blobs_still_match_the_files_on_disk(self) -> None:
        for role, ref in V10["instrument"].items():
            with self.subTest(role=role):
                self.assertEqual(ref["git_blob_sha"], blob(ref["path"]))

    def test_the_output_contract_is_the_same_file_and_the_same_bytes(self) -> None:
        self.assertEqual(V08["output_contract_path"], V10["output_contract_path"])
        self.assertEqual(V08["output_contract_git_blob_sha"], V10["output_contract_git_blob_sha"])
        self.assertEqual(V10["output_contract_git_blob_sha"], blob(V10["output_contract_path"]))

    def test_the_fixture_contract_is_the_same_file(self) -> None:
        self.assertEqual(V08["fixture_contract_path"], V10["fixture_contract_path"])


class FreezeDisciplineNotRelaxed(unittest.TestCase):
    def test_every_v08_freeze_rule_survives_verbatim(self) -> None:
        for rule in V08["freeze_rules"]:
            with self.subTest(rule=rule[:48]):
                self.assertIn(rule, V10["freeze_rules"])

    def test_the_new_freeze_declares_a_fresh_gate_is_still_required(self) -> None:
        self.assertIn("NOT library-admitted until a valid gate passes", V10["qualification_scope"])
        self.assertEqual("frozen-candidate", V10["lifecycle"])

    def test_the_freeze_records_what_it_cannot_prove(self) -> None:
        limits = " ".join(V10["known_limits"])
        self.assertIn("only a fresh held-out gate can", limits)

    def test_the_digest_actually_covers_the_consolidated_document(self) -> None:
        import hashlib
        lines = "".join(f"{c['path']}:{c['git_blob_sha']}\n" for c in V10["assembly"])
        lines += f"{V10['output_contract_path']}:{blob(V10['output_contract_path'])}\n"
        self.assertEqual(V10["assembly_digest"],
                         "sha256:" + hashlib.sha256(lines.encode()).hexdigest())

    def test_the_assembly_components_hash_to_what_the_freeze_claims(self) -> None:
        for component in V10["assembly"]:
            with self.subTest(path=component["path"]):
                self.assertEqual(component["git_blob_sha"], blob(component["path"]))

    def test_the_freeze_names_every_document_it_consolidates(self) -> None:
        self.assertEqual([c["path"] for c in V08["assembly"]], V10["consolidates"])


class ThresholdsNotLowered(unittest.TestCase):
    """The gate's own bar: trials, retries, best-of-N, per-family count, abort behavior."""

    def test_the_v08_preregistration_bar_is_still_what_a_new_cycle_must_meet(self) -> None:
        self.assertEqual(3, int(PREREG_V08["trials_per_fixture"]))
        self.assertEqual(0, int(PREREG_V08["retries_permitted"]))
        self.assertEqual(2, int(PREREG_V08["per_family"]))
        self.assertEqual(5, len(PREREG_V08["families"]))
        self.assertIn("Any single trial failure ends this gate as FAIL", PREREG_V08["pass_rule"])
        self.assertIn("Best-of-N is not a pass", PREREG_V08["pass_rule"])

    def test_the_runner_still_fails_the_gate_on_one_discordant_fixture(self) -> None:
        source = (HERE / "run_heldout_gate_v07.py").read_text(encoding="utf-8")
        self.assertIn("DISCORDANT TRIALS ON", source)
        self.assertIn("GATE VERDICT", source)
        self.assertNotIn("best_of", source)
        self.assertIn("There is no", source)  # "There is no best-of-N and no retry"

    def test_the_grader_vocabularies_are_unchanged(self) -> None:
        grader = _load("grdfz", "grader_v07_structural.py")
        self.assertEqual(
            {"MATURE_DOWNSTREAM_ECONOMICS", "REGISTERED_PRIMARY_KPI", "ACQUISITION_COST",
             "GUARDRAIL", "CAPACITY", "NONE_DECIDABLE"},
            set(grader.DECISIVE))

    def test_every_family_oracle_still_asserts_a_scale_state(self) -> None:
        generator = _load("genfz", "heldout_generator_v07.py")
        _cases, oracle = generator.generate(PREREG_V08["heldout_seed"], PREREG_V08["per_family"])
        for fid, exp in oracle["expectations"].items():
            with self.subTest(fixture=fid):
                self.assertIn(exp["scale_state"], {"BLOCKED", "ELIGIBLE"})
                if exp["scale_state"] == "BLOCKED":
                    self.assertTrue(exp["scale_reasons_any"])

    def test_the_anti_gaming_control_still_requires_an_eligible_scale(self) -> None:
        """CLEAN_SCALABLE_WIN is the family that catches a candidate that always blocks SCALE."""
        generator = _load("genfz2", "heldout_generator_v07.py")
        _cases, oracle = generator.generate(PREREG_V08["heldout_seed"], PREREG_V08["per_family"])
        clean = [e for e in oracle["expectations"].values() if e["family"] == "CLEAN_SCALABLE_WIN"]
        self.assertTrue(clean)
        for exp in clean:
            self.assertEqual("ELIGIBLE", exp["scale_state"])
            self.assertEqual(["SCALE"], exp["action_in"])


class SupersededHistoryIntact(unittest.TestCase):
    def test_freeze_v07_and_v08_still_verify_against_disk(self) -> None:
        for name in ("candidate-freeze-v0.7.json", "candidate-freeze-v0.8.json"):
            freeze = json.loads((HERE / name).read_text(encoding="utf-8"))
            for component in freeze["assembly"]:
                with self.subTest(freeze=name, path=component["path"]):
                    self.assertEqual(component["git_blob_sha"], blob(component["path"]),
                                     "consolidation must not rewrite superseded documents")


if __name__ == "__main__":
    unittest.main(verbosity=2)
