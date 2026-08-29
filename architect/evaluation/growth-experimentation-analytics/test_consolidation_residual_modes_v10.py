#!/usr/bin/env python3
"""Targeted regressions for the two residual failures of gate 33243263001 (v0.8, seed 20260830).

  * `HO-IFH-02` trial 2 -- FAIL `decision_basis must record REGISTERED_PRIMARY_KPI`
  * `HO-SBI-02` trial 2 -- malformed JSON from the model

Both are graded against the **unmodified** gate grader and generator: the gate found zero
harness and zero provider defects, so nothing in the instrument is changed here.

Scope, stated honestly, as for the v0.7 regressions:

  * **detection** -- each observed failure is replayed as a concrete result and must be rejected,
    so a recurrence cannot pass a future gate;
  * **rule presence** -- the consolidated document states the rule the candidate was missing, so
    the repair cannot be silently dropped.

They cannot show the candidate now behaves correctly. Only a fresh gate can.
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
CONSOLIDATED = ROOT / "architect/research/growth-experimentation-analytics/professional-model-consolidated-v1.0.md"


def doc() -> str:
    return " ".join(CONSOLIDATED.read_text(encoding="utf-8").split())


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


grader = _load("grd07r", "grader_v07_structural.py")
generator = _load("gen07r", "heldout_generator_v07.py")

GATE_SEED = 20260830          # the seed the v0.8 gate actually ran
GATE_PER_FAMILY = 2
CONTRACT = json.loads(
    (HERE / "schemas/result-v4.schema.json").read_text(encoding="utf-8"))


def gate_suite():
    cases, oracle = generator.generate(GATE_SEED, GATE_PER_FAMILY)
    fixtures = {f["fixture_id"]: f for f in cases["fixtures"]}
    return fixtures, oracle["expectations"]


FIXTURES, EXPECTATIONS = gate_suite()


def passing_result(fixture_id: str) -> dict:
    """A result the frozen grader accepts for this fixture, built from the frozen expectation.

    Built from the oracle rather than hand-written so a mutation test below is a mutation of a
    known-good result, not of an accidentally-invalid one.
    """
    fixture, exp = FIXTURES[fixture_id], EXPECTATIONS[fixture_id]
    scope = exp["allowed_scopes"][0]
    ceiling = exp["ceiling_by_scope"][scope]["max"]
    status = (exp.get("causal_status_in") or
              (["IDENTIFIED"] if ceiling == "INCREMENTAL_CAUSAL" else ["UNRESOLVED"]))[0]
    action = exp["action_in"][0]
    result = {
        "fixture_id": fixture_id,
        "recommendation": action,
        "decision_record": {
            "causal": {"status": status, "claim_scope": scope, "claim_ceiling": ceiling,
                       "blocking_confounders": []},
            "operational": {
                "action": action,
                "target": exp.get("target_by_action", {}).get(action, [exp["target"]])[0],
                "decisive_metric": exp["decisive_metric_in"][0],
                "decision_basis": list(exp.get("basis_required") or ["REGISTERED_PRIMARY_KPI"]),
                "reversible": True,
                "evidence_that_would_change_action": "a matured registered-window read",
            },
            "scale_readiness": {
                "state": exp["scale_state"],
                "blocking_reasons": ([exp["scale_reasons_any"][0]]
                                     if exp["scale_state"] == "BLOCKED" else ["NOT_BLOCKED"]),
            },
        },
        "data_integrity_findings": ["no blocking integrity defect identified"],
        # The contract is closed for computation items too: `assumptions` is not a permitted key.
        # An earlier draft of this builder added one and the frozen grader rejected the whole
        # result -- a live demonstration that the closed-contract rule bites where it is claimed to.
        "computations": [
            {"name": name, "inputs": {}, "method": "as registered", "result": spec[0],
             "unit": "ratio" if spec[2] == "RATIO" else "count"}
            for name, spec in (exp.get("computations") or {}).items()
        ],
        "claim_boundaries": ["scoped to the declared estimand"],
        "confounders": [],
        "rationale": "registered evidence assessed against the registered rule",
        "next_action": "hold to the registered horizon",
    }
    return result


class RegisteredPrimaryKpiBasis(unittest.TestCase):
    """HO-IFH-02 trial 2: the model omitted REGISTERED_PRIMARY_KPI from decision_basis.

    The value is in the frozen contract and required by the frozen oracle on two families. The
    v0.4 overlay enumerated four of the ten permitted values and never named this one -- the same
    Phase 4 defect class as the whole v0.7 root cause.
    """

    FAMILIES_REQUIRING_IT = ("IMMATURE_FIXED_HORIZON", "CLEAN_SCALABLE_WIN")

    def fixtures_requiring_it(self) -> list[str]:
        return [fid for fid, exp in EXPECTATIONS.items()
                if "REGISTERED_PRIMARY_KPI" in (exp.get("basis_required") or [])]

    def test_the_oracle_requires_it_on_the_families_it_always_required_it_on(self) -> None:
        """Consolidation must not have moved the oracle's requirement. It is frozen."""
        families = {EXPECTATIONS[fid]["family"] for fid in self.fixtures_requiring_it()}
        self.assertEqual(set(self.FAMILIES_REQUIRING_IT), families)

    def test_the_observed_failure_is_rejected(self) -> None:
        """Replay: everything correct except the omitted basis value."""
        for fid in self.fixtures_requiring_it():
            with self.subTest(fixture=fid):
                result = passing_result(fid)
                basis = result["decision_record"]["operational"]["decision_basis"]
                result["decision_record"]["operational"]["decision_basis"] = (
                    [b for b in basis if b != "REGISTERED_PRIMARY_KPI"] or ["MATERIALITY"])
                verdict = grader.grade(result, FIXTURES[fid], EXPECTATIONS[fid], CONTRACT)
                self.assertFalse(verdict["pass"])
                self.assertIn("decision_basis must record REGISTERED_PRIMARY_KPI",
                              verdict["failures"])

    def test_the_corrected_form_is_accepted(self) -> None:
        for fid in self.fixtures_requiring_it():
            with self.subTest(fixture=fid):
                verdict = grader.grade(passing_result(fid), FIXTURES[fid],
                                       EXPECTATIONS[fid], CONTRACT)
                self.assertTrue(verdict["pass"], verdict.get("failures"))

    def test_recording_it_alongside_other_grounds_is_still_accepted(self) -> None:
        """The rule is 'record every ground you used', not 'record only this one'."""
        for fid in self.fixtures_requiring_it():
            with self.subTest(fixture=fid):
                result = passing_result(fid)
                op = result["decision_record"]["operational"]
                op["decision_basis"] = sorted(set(op["decision_basis"]) |
                                              {"MATERIALITY", "REVERSIBILITY", "COST_OF_WAITING"})
                verdict = grader.grade(result, FIXTURES[fid], EXPECTATIONS[fid], CONTRACT)
                self.assertTrue(verdict["pass"], verdict.get("failures"))

    def test_it_is_not_required_where_the_oracle_does_not_require_it(self) -> None:
        """Guard against over-correction: this must not become 'always record it'."""
        others = [fid for fid in EXPECTATIONS if fid not in self.fixtures_requiring_it()]
        self.assertTrue(others)
        for fid in others:
            with self.subTest(fixture=fid):
                verdict = grader.grade(passing_result(fid), FIXTURES[fid],
                                       EXPECTATIONS[fid], CONTRACT)
                self.assertTrue(verdict["pass"], verdict.get("failures"))

    def test_the_consolidated_document_names_the_value_with_its_trigger(self) -> None:
        text = doc()
        self.assertIn("`REGISTERED_PRIMARY_KPI` — the registered primary KPI result is among the grounds",
                      text)
        self.assertIn("Closed vocabulary, all ten members", text)
        self.assertIn("Record every ground that bore on the action, not only the strongest", text)

    def test_the_document_makes_omitting_a_used_ground_a_hard_failure(self) -> None:
        section = doc().split("## 7. Anti-patterns")[-1]
        self.assertIn("omits a ground it actually used from `decision_basis`", section)
        self.assertIn("including the registered primary KPI result when that is what the action rests on",
                      section)


class MalformedJsonIsNeverAPass(unittest.TestCase):
    """HO-SBI-02 trial 2: the model emitted unparseable JSON.

    Two channels can see malformed output. The runner parses the adapter's stdout; the executor
    parses the provider's body first and exits non-zero. Both must be non-PASS. The instrument is
    NOT changed here -- these tests lock the behavior that already exists.
    """

    MALFORMED = [
        ("trailing comma", '{"fixture_id": "HO-SBI-01", "recommendation": "INCONCLUSIVE",}'),
        ("unquoted key", '{fixture_id: "HO-SBI-01"}'),
        ("markdown fence", '```json\n{"fixture_id": "HO-SBI-01"}\n```'),
        ("prose preamble", 'Here is the analysis:\n{"fixture_id": "HO-SBI-01"}'),
        ("truncated object", '{"fixture_id": "HO-SBI-01", "decision_record": {"causal": {'),
        ("two objects", '{"fixture_id": "a"}{"fixture_id": "b"}'),
        ("python literal", "{'fixture_id': 'HO-SBI-01'}"),
        ("observed shape", '{\n "a": 1,\n "b": {\n  "c": 2,\n }\n}'),
    ]

    def test_none_of_these_bodies_parse(self) -> None:
        for label, body in self.MALFORMED:
            with self.subTest(case=label):
                with self.assertRaises(json.JSONDecodeError):
                    json.loads(body)

    def test_the_runner_grades_an_unparseable_body_as_fail_not_pass(self) -> None:
        """The runner's own path: a non-JSON body reaching it is a candidate FAIL."""
        source = (HERE / "run_heldout_gate_v07.py").read_text(encoding="utf-8")
        self.assertIn("except json.JSONDecodeError:", source)
        self.assertIn('entry.update(status="FAIL", failures=["candidate returned non-JSON"])', source)

    def test_the_executor_refuses_an_unparseable_provider_body(self) -> None:
        """The executor's path: it exits non-zero rather than inventing a result."""
        source = (HERE / "executor_gemini.py").read_text(encoding="utf-8")
        self.assertIn("model returned invalid JSON", source)
        self.assertIn("raise SystemExit(2)", source)

    def test_the_adapter_never_substitutes_a_result_for_a_failed_executor(self) -> None:
        source = (HERE / "adapters/stdio_candidate_adapter.py").read_text(encoding="utf-8")
        self.assertIn("Candidate executor failed with exit code", source)
        self.assertNotIn("except Exception:\n        return {}", source)

    def test_an_unparseable_body_can_never_reach_the_grader_as_a_pass(self) -> None:
        """End-to-end on the grader itself: whatever survives parsing is still contract-checked."""
        fid = "HO-SBI-01"
        empty = grader.grade({}, FIXTURES[fid], EXPECTATIONS[fid], CONTRACT)
        self.assertFalse(empty["pass"])
        partial = grader.grade({"fixture_id": fid}, FIXTURES[fid], EXPECTATIONS[fid], CONTRACT)
        self.assertFalse(partial["pass"])

    def test_the_consolidated_document_states_json_validity_first_in_the_contract(self) -> None:
        text = doc()
        contract = text.split("## 6. Output contract")[-1]
        self.assertIn("Return exactly one JSON object that parses on the first attempt", contract)
        self.assertIn("is not a weaker answer, it is no answer", contract)
        # It leads the contract section rather than trailing it.
        self.assertLess(contract.find("parses on the first attempt"),
                        contract.find("### 6.2"))

    def test_the_document_forbids_every_shape_observed(self) -> None:
        text = doc()
        for forbidden in ("no Markdown fences", "no prose before or after", "no trailing commas",
                          "no comments", "no unquoted keys"):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, text)


class ConsolidationChangedNoGradedExpectation(unittest.TestCase):
    """The oracle is frozen. Consolidation must not have moved a single expectation."""

    def test_the_v08_gate_suite_regenerates_identically(self) -> None:
        cases_a, oracle_a = generator.generate(GATE_SEED, GATE_PER_FAMILY)
        cases_b, oracle_b = generator.generate(GATE_SEED, GATE_PER_FAMILY)
        self.assertEqual(json.dumps(cases_a, sort_keys=True), json.dumps(cases_b, sort_keys=True))
        self.assertEqual(json.dumps(oracle_a, sort_keys=True), json.dumps(oracle_b, sort_keys=True))

    def test_every_family_still_has_a_result_the_frozen_grader_accepts(self) -> None:
        """If consolidation had broken a family, this is where it would show."""
        for fid in FIXTURES:
            with self.subTest(fixture=fid):
                verdict = grader.grade(passing_result(fid), FIXTURES[fid],
                                       EXPECTATIONS[fid], CONTRACT)
                self.assertTrue(verdict["pass"], verdict.get("failures"))

    def test_the_five_families_are_unchanged(self) -> None:
        self.assertEqual(
            {"UPSTREAM_ONLY_CONFOUNDED", "UPSTREAM_DOWNSTREAM_CONFLICT", "IMMATURE_FIXED_HORIZON",
             "CLEAN_SCALABLE_WIN", "SPARSE_BUT_IDENTIFIED"},
            {exp["family"] for exp in EXPECTATIONS.values()})


if __name__ == "__main__":
    unittest.main(verbosity=2)
