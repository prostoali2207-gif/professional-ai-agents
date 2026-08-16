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
        self.assertEqual([f"PM-S{i}" for i in range(1, 13)], [c["id"] for c in self.cases])
        self.assertEqual(len(self.cases), len({c["id"] for c in self.cases}))
        for case in self.cases:
            self.assertTrue(case["allowed_actions"])
            self.assertTrue(case["required_flags"])
            self.assertIn("SCALE", case["forbidden_actions"])

    def test_required_user_requested_behaviors_are_covered(self) -> None:
        titles = " ".join(c["title"].lower() for c in self.cases)
        for concept in ["cheap leads", "broken conversion", "attribution", "budget", "experiment", "degradation", "sparse", "opportunity cost", "automation", "privacy", "authority", "vanity"]:
            self.assertIn(concept, titles)

    def test_no_application_specific_specialization(self) -> None:
        # Explicit exclusions may name forbidden application layers once. There must be no executable/domain procedure sections for them.
        forbidden_headings = ["UAE specialization", "Automotive specialization", "Meta Ads workflow", "Toyota Yaris"]
        for token in forbidden_headings:
            self.assertNotIn("## " + token, self.core)


if __name__ == "__main__":
    unittest.main()
