#!/usr/bin/env python3
"""Regression against the Analytics v0.3 grading instability.

The defect: the same frozen candidate, fixture and grader produced different behavioral
verdicts across runs, because every P0/P1 assertion was a regex over free prose. Sampling
paraphrases the prose, so the verdict tracked phrasing rather than the decision.

These tests are deterministic and make no provider calls. They lock in four properties:

  1. paraphrase invariance   -- semantically identical decisions grade identically,
                                whatever the prose says, including the real prose that
                                the v0.3 grader misjudged in both directions;
  2. prose independence      -- erasing every free-text field cannot change a verdict;
  3. contrastive teeth       -- mutating the *decision* still fails, so (1) and (2) were
                                not bought by weakening the gate;
  4. no return to prose      -- the grading path does not read prose fields at all.
"""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("grader_v04", HERE / "grader_v04_structural.py")
grader = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(grader)

PROSE_FIELDS = ("rationale", "next_action")


# --------------------------------------------------------------------------------------
# Canonical correct results. The decision content is fixed; only prose varies.
# --------------------------------------------------------------------------------------

def h_ds_01(rationale: str, next_action: str, claim_boundaries: list[str] | None = None) -> dict:
    """H-DS-01: confounded acquisition-cost comparison; reversible stop of B is justified."""
    return {
        "fixture_id": "H-DS-01",
        "recommendation": "KILL",
        "decision_record": {
            "causal": {
                "status": "UNRESOLVED",
                "claim_ceiling": "DESCRIPTIVE_ASSOCIATION",
                "blocking_confounders": ["budget-regime mismatch", "audience-expansion mismatch"],
            },
            "operational": {
                "action": "KILL",
                "target": "configuration B",
                "decision_basis": ["REGISTERED_PRIMARY_KPI", "COST_OF_WAITING", "REVERSIBILITY", "MATERIALITY"],
                "reversible": True,
                "evidence_that_would_change_action": "verified downstream value for B, or corrected comparable measurement",
            },
            "scale_readiness": {"state": "BLOCKED", "blocking_reasons": ["UNIDENTIFIED_CAUSAL_EFFECT", "NO_CREDIBLE_COUNTERFACTUAL"]},
        },
        "data_integrity_findings": ["The comparison is not randomized."],
        "computations": [
            {"name": "a_cost_per_qualified_outcome", "inputs": {"spend": 210.0, "qualified_outcomes": 14},
             "method": "spend / outcomes", "result": 15.0, "unit": "currency"},
            {"name": "b_cost_per_qualified_outcome", "inputs": {"spend": 96.0, "qualified_outcomes": 3},
             "method": "spend / outcomes", "result": 32.0, "unit": "currency"},
            {"name": "cost_ratio_b_over_a", "inputs": {"b": 32.0, "a": 15.0},
             "method": "b / a", "result": 32 / 15, "unit": "ratio"},
        ],
        "claim_boundaries": claim_boundaries if claim_boundaries is not None else ["Causal conclusion: unresolved."],
        "confounders": [
            {"name": "budget-regime mismatch", "severity": "MATERIAL", "effect": "pacing and delivery differ"},
            {"name": "audience-expansion mismatch", "severity": "MATERIAL", "effect": "audience composition differs"},
        ],
        "rationale": rationale,
        "next_action": next_action,
    }


def h_ds_02(rationale: str, next_action: str, claim_boundaries: list[str] | None = None) -> dict:
    """H-DS-02: the cheaper-acquisition arm A is the loss-making one; action must target A."""
    return {
        "fixture_id": "H-DS-02",
        "recommendation": "KILL",
        "decision_record": {
            "causal": {
                "status": "UNRESOLVED",
                "claim_ceiling": "DESCRIPTIVE_ASSOCIATION",
                "blocking_confounders": ["different_audience_sources", "different_creatives"],
            },
            "operational": {
                "action": "KILL",
                "target": "configuration A",
                "decision_basis": ["MATURE_DOWNSTREAM_ECONOMICS", "ACQUISITION_COST_DIAGNOSTIC", "REVERSIBILITY"],
                "reversible": True,
                "evidence_that_would_change_action": "verified additional mature downstream value for A",
            },
            "scale_readiness": {"state": "BLOCKED", "blocking_reasons": ["NO_CREDIBLE_COUNTERFACTUAL", "INSUFFICIENT_SAMPLE"]},
        },
        "data_integrity_findings": ["Sales counts are sparse."],
        "computations": [],
        "claim_boundaries": claim_boundaries if claim_boundaries is not None else ["Causal conclusion: unresolved."],
        "confounders": [
            {"name": "different_audience_sources", "severity": "FATAL", "effect": "audience composition may explain the difference"},
            {"name": "different_creatives", "severity": "FATAL", "effect": "creative is bundled with audience source"},
        ],
        "rationale": rationale,
        "next_action": next_action,
    }


# The prose the v0.3 grader actually mishandled, taken verbatim from run 32563283125.
REAL_H_DS_01_RATIONALE = (
    "The causal question is not identified because the comparison changes budget regime and audience expansion "
    "without randomization. However, causal uncertainty does not require continuing paid spend on B. The mature "
    "observed business evidence shows B costing 32 currency units per qualified trial start, 2.13 times A's 15, "
    "with 3 observed B outcomes, real marginal spend to continue, no verified downstream-value offset, no "
    "requirement to continue, and a reversible stop."
)
REAL_H_DS_01_CLAIMS = [
    "No registered success/failure threshold was provided; the recommendation is a bounded operational stop based "
    "on mature observed economics, real continued spend, reversibility, and absence of a supplied value offset."
]

# Paraphrases a competent analyst might equally write. Several of these are invisible to
# the v0.3 patterns; none of them changes the decision.
EQUIVALENT_PROSE = [
    ("continued spend on B carries a real cost", "Stop configuration B now."),
    ("real continued spend on B is a cost we would keep paying", "Pause B; the stop is reversible."),
    ("the cost of waiting for causal certainty exceeds its value here", "Halt B."),
    ("B burns budget every day we wait", "Terminate the current B configuration."),
    ("продолжение расходов на B имеет реальную стоимость", "Остановить конфигурацию B."),
    ("", "Stop B."),
]

EQUIVALENT_SCALE_PROSE = [
    "No SCALE recommendation is supported.",
    "Scaling is not justified from this confounded comparison.",
    "SCALE remains blocked until a credible counterfactual exists.",
    "We must not scale on this evidence.",
    "Qualified-lead acquisition cost does not override the requirement to use gross profit for KILL/SCALE decisions.",
]


class ParaphraseInvariance(unittest.TestCase):
    """Property 1: equivalent decisions grade equally regardless of prose."""

    def test_h_ds_01_passes_under_every_equivalent_phrasing(self) -> None:
        for rationale, next_action in EQUIVALENT_PROSE:
            with self.subTest(rationale=rationale[:40]):
                report = grader.grade(h_ds_01(rationale or "x", next_action))
                self.assertTrue(report["pass"], f"{rationale!r} -> {report['failures']}")

    def test_real_recorded_output_that_v03_failed_now_passes(self) -> None:
        """run 32563283125 failed this output for 'missing continued-spend cost'.

        The candidate had stated the continued-spend cost twice. Under the structured
        contract the decision is graded, so the historical verdict is corrected.
        """
        report = grader.grade(h_ds_01(REAL_H_DS_01_RATIONALE, "Pause current configuration B now.", REAL_H_DS_01_CLAIMS))
        self.assertTrue(report["pass"], report["failures"])

    def test_scale_refusal_phrasing_never_changes_the_verdict(self) -> None:
        for boundary in EQUIVALENT_SCALE_PROSE:
            with self.subTest(boundary=boundary[:40]):
                report = grader.grade(h_ds_02("downstream economics drive this", "Stop A.", [boundary]))
                self.assertTrue(report["pass"], f"{boundary!r} -> {report['failures']}")


class ProseIndependence(unittest.TestCase):
    """Property 2: erasing prose cannot move a verdict."""

    def test_verdict_survives_total_prose_erasure(self) -> None:
        for builder in (h_ds_01, h_ds_02):
            rich = builder("a long and eloquent rationale mentioning every magic word: "
                           "continued spend cost, cost of waiting, reversible, gross profit, cannot scale",
                           "an equally eloquent next action")
            bare = copy.deepcopy(rich)
            for field in PROSE_FIELDS:
                bare[field] = "."
            bare["claim_boundaries"] = []
            bare["data_integrity_findings"] = []
            for confounder in bare["confounders"]:
                confounder["effect"] = "."
            with self.subTest(fixture=rich["fixture_id"]):
                self.assertEqual(grader.grade(rich)["pass"], grader.grade(bare)["pass"])
                self.assertTrue(grader.grade(bare)["pass"], grader.grade(bare)["failures"])

    def test_magic_words_alone_cannot_buy_a_pass(self) -> None:
        """The v0.3 failure mode in reverse: keyword-stuffed prose over a wrong decision."""
        wrong = h_ds_02(
            "cannot scale, gross profit, downstream economics, continued spend cost, reversible",
            "stop configuration A, we do not scale from confounded evidence",
        )
        wrong["decision_record"]["operational"]["target"] = "configuration B"
        report = grader.grade(wrong)
        self.assertFalse(report["pass"])
        self.assertTrue(any("targets arm A" in f or "names arm B" in f for f in report["failures"]), report["failures"])


class ContrastiveTeeth(unittest.TestCase):
    """Property 3: the gate still fails genuinely wrong decisions."""

    def _mutate(self, builder, path: list[str], value) -> dict:
        result = builder("neutral prose", "neutral action")
        node = result
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = value
        return result

    def test_causal_overclaim_fails(self) -> None:
        report = grader.grade(self._mutate(h_ds_01, ["decision_record", "causal", "status"], "IDENTIFIED"))
        self.assertFalse(report["pass"], "IDENTIFIED causal status on a confounded design must fail")

    def test_incremental_causal_ceiling_fails(self) -> None:
        report = grader.grade(self._mutate(h_ds_01, ["decision_record", "causal", "claim_ceiling"], "INCREMENTAL_CAUSAL"))
        self.assertFalse(report["pass"], "INCREMENTAL_CAUSAL ceiling without identification must fail")

    def test_scale_eligible_on_confounded_evidence_fails(self) -> None:
        result = h_ds_01("neutral prose", "neutral action")
        result["decision_record"]["scale_readiness"] = {"state": "ELIGIBLE", "blocking_reasons": ["NOT_BLOCKED"]}
        self.assertFalse(grader.grade(result)["pass"], "SCALE must stay blocked on confounded evidence")

    def test_scale_recommendation_with_blocked_gate_fails(self) -> None:
        result = h_ds_01("neutral prose", "neutral action")
        result["recommendation"] = "SCALE"
        result["decision_record"]["operational"]["action"] = "SCALE"
        self.assertFalse(grader.grade(result)["pass"], "SCALE recommendation against a BLOCKED gate must fail")

    def test_decision_paralysis_fails(self) -> None:
        result = h_ds_01("neutral prose", "neutral action")
        result["recommendation"] = "INCONCLUSIVE"
        result["decision_record"]["operational"]["action"] = "INCONCLUSIVE"
        self.assertFalse(grader.grade(result)["pass"], "universal INCONCLUSIVE must not satisfy H-DS-01")

    def test_missing_cost_of_waiting_basis_fails(self) -> None:
        result = h_ds_01("neutral prose", "neutral action")
        basis = result["decision_record"]["operational"]["decision_basis"]
        result["decision_record"]["operational"]["decision_basis"] = [b for b in basis if b != "COST_OF_WAITING"]
        report = grader.grade(result)
        self.assertFalse(report["pass"])
        self.assertIn("decision_basis must record COST_OF_WAITING", report["failures"])

    def test_acquisition_cost_only_decision_fails(self) -> None:
        """The dumb cost-gap KILL: right label, wrong grounds."""
        result = h_ds_02("neutral prose", "neutral action")
        result["decision_record"]["operational"]["decision_basis"] = ["ACQUISITION_COST_DIAGNOSTIC"]
        self.assertFalse(grader.grade(result)["pass"])

    def test_wrong_arithmetic_fails(self) -> None:
        result = h_ds_01("neutral prose", "neutral action")
        for computation in result["computations"]:
            if computation["name"] == "b_cost_per_qualified_outcome":
                computation["result"] = 31.0
        self.assertFalse(grader.grade(result)["pass"])

    def test_undeclared_blocking_confounder_fails(self) -> None:
        result = h_ds_01("neutral prose", "neutral action")
        result["decision_record"]["causal"]["blocking_confounders"] = ["a confounder nobody identified"]
        self.assertFalse(grader.grade(result)["pass"])

    def test_action_disagreeing_with_recommendation_fails(self) -> None:
        result = h_ds_01("neutral prose", "neutral action")
        result["decision_record"]["operational"]["action"] = "ITERATE"
        self.assertFalse(grader.grade(result)["pass"])

    def test_ambiguous_target_fails(self) -> None:
        result = h_ds_01("neutral prose", "neutral action")
        result["decision_record"]["operational"]["target"] = "configuration A and configuration B"
        self.assertFalse(grader.grade(result)["pass"])

    def test_missing_decision_record_fails(self) -> None:
        result = h_ds_01("neutral prose", "neutral action")
        del result["decision_record"]
        self.assertFalse(grader.grade(result)["pass"])


class NoReturnToProseGrading(unittest.TestCase):
    """Property 4: the grading path must not read prose fields."""

    def test_grader_source_does_not_read_prose_fields(self) -> None:
        source = (HERE / "grader_v04_structural.py").read_text(encoding="utf-8")
        body = source.split('EXPECTATIONS: dict[str, dict[str, Any]] = {')[0]
        code = "\n".join(
            line for line in body.splitlines()
            if not line.lstrip().startswith("#") and not line.lstrip().startswith("*")
        )
        for field in ("rationale", "next_action", "claim_boundaries"):
            self.assertNotIn(f'"{field}"', code, f"grading path must not read the {field} prose field")
        self.assertNotIn('.get("effect")', code, "grading path must not read confounder prose")


if __name__ == "__main__":
    unittest.main(verbosity=2)
