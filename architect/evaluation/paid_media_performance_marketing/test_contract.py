from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CORE = ROOT / "architect/library/cores/paid-media-performance-marketing/1.0.0/professional-model.md"
CASES = HERE / "semantic_cases.json"


class PaidMediaCoreContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.core = CORE.read_text(encoding="utf-8")
        self.cases = json.loads(CASES.read_text(encoding="utf-8"))
        self.by_id = {c["id"]: c for c in self.cases}

    def test_core_has_required_professional_constructs(self) -> None:
        required = [
            "unit-economics", "Measurement architecture", "Attribution, incrementality and causal reasoning",
            "Experimentation and statistical judgment", "marginal allocation", "Auction, bidding and automation",
            "Creative testing", "Pacing", "Diagnosis", "stop-loss", "Privacy", "authority"
        ]
        for token in required:
            self.assertIn(token.lower(), self.core.lower(), token)

    def test_context_separation_is_explicit(self) -> None:
        for token in ["Stable core", "Domain specialization", "Jurisdiction / market / live context", "Organization / project context"]:
            self.assertIn(token, self.core)

    def test_fixture_set_is_frozen_and_complete(self) -> None:
        self.assertEqual([f"PM-S{i}" for i in range(1, 14)], [c["id"] for c in self.cases])
        self.assertEqual(len(self.cases), len({c["id"] for c in self.cases}))
        for case in self.cases:
            self.assertTrue(case["allowed_actions"])
            self.assertTrue(case["required_flags"])

    def test_fixture_set_tests_both_resisting_and_justified_scaling(self) -> None:
        scale_allowed = [c for c in self.cases if "SCALE" in c["allowed_actions"]]
        scale_forbidden = [c for c in self.cases if "SCALE" in c["forbidden_actions"]]
        self.assertTrue(scale_allowed, "A stop-only suite cannot establish scale judgment")
        self.assertTrue(scale_forbidden, "Suite must include pressure to resist unjustified scaling")
        self.assertEqual(["PM-S13"], [c["id"] for c in scale_allowed])

    def test_scale_requires_explicit_delegated_authority_control(self) -> None:
        self.assertIn("Pre-execution authority check", self.core)
        self.assertIn("every spend-increasing execution decision must explicitly verify", self.core)
        case = self.by_id["PM-S13"]
        self.assertEqual(["SCALE"], case["allowed_actions"])
        self.assertIn("authority_boundary_respected", case["required_flags"])

    def test_broken_measurement_fixture_tests_decision_validity_not_false_causal_construct(self) -> None:
        case = self.by_id["PM-S2"]
        self.assertIn("decision_signal_invalid", case["required_flags"])
        self.assertNotIn("causal_claim_blocked", case["required_flags"])

    def test_release_cases_isolate_their_target_constructs(self) -> None:
        self.assertEqual(["fault_tree_used", "measurement_incident_suspected"], self.by_id["PM-S6"]["required_flags"])
        self.assertNotIn("small_reversible_bet", self.by_id["PM-S7"]["required_flags"])
        self.assertEqual(["stop_loss_applied", "opportunity_cost_considered"], self.by_id["PM-S8"]["required_flags"])
        self.assertNotIn("fault_tree_used", self.by_id["PM-S10"]["required_flags"])
        self.assertIn("STOP", self.by_id["PM-S12"]["allowed_actions"])
        self.assertNotIn("no_fabricated_business_facts", self.by_id["PM-S12"]["required_flags"])

    def test_required_user_requested_behaviors_are_covered(self) -> None:
        titles = " ".join(c["title"].lower() for c in self.cases)
        for concept in ["cheap leads", "broken conversion", "attribution", "budget", "experiment", "degradation", "sparse", "opportunity cost", "automation", "privacy", "authority", "vanity", "scale"]:
            self.assertIn(concept, titles)

    def test_no_application_specific_specialization(self) -> None:
        forbidden_headings = ["UAE specialization", "Automotive specialization", "Meta Ads workflow", "Toyota Yaris"]
        for token in forbidden_headings:
            self.assertNotIn("## " + token, self.core)


if __name__ == "__main__":
    unittest.main()
