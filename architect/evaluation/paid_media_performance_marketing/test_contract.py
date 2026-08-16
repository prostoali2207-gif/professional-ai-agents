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

    def test_broken_measurement_fixture_tests_decision_validity_not_false_causal_construct(self) -> None:
        case = next(c for c in self.cases if c["id"] == "PM-S2")
        self.assertIn("decision_signal_invalid", case["required_flags"])
        self.assertNotIn("causal_claim_blocked", case["required_flags"])

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
