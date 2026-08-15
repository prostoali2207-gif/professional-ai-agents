import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
CASES = HERE / "semantic_cases.json"


class SemanticCaseContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(CASES.read_text(encoding="utf-8"))

    def test_exact_case_set(self):
        self.assertEqual(
            [case["id"] for case in self.cases],
            [f"RCE-S{i}" for i in range(1, 11)],
        )

    def test_required_fields_present(self):
        required = {
            "id",
            "title",
            "risk_class",
            "facts",
            "required_decision",
            "critical_rationale",
            "forbidden_shortcut",
        }
        for case in self.cases:
            self.assertTrue(required.issubset(case), case["id"])
            self.assertTrue(case["critical_rationale"], case["id"])
            self.assertTrue(case["required_decision"], case["id"])
            self.assertTrue(case["forbidden_shortcut"], case["id"])

    def test_no_embedded_provider_price_memory(self):
        # These are synthetic fixture economics, not durable provider pricing tables.
        serialized = json.dumps(self.cases).lower()
        for provider in ("openai", "anthropic", "github copilot", "gemini", "vertex", "vercel"):
            self.assertNotIn(provider, serialized)

    def test_cases_cover_distinct_false_economy_classes(self):
        decisions = {case["required_decision"] for case in self.cases}
        self.assertIn("STRONG_DIRECT", decisions)
        self.assertIn("REJECT_CACHE_AND_RESEARCH", decisions)
        self.assertIn("REJECT_FREE_PROVIDER", decisions)
        self.assertIn("FULL_SUITE", decisions)
        self.assertIn("NOT_WASTE", decisions)
        self.assertIn("DEFER_FOR_ACCOUNT_TELEMETRY", decisions)
        self.assertIn("USE_OFFICIAL_SOURCE", decisions)
        self.assertIn("SYNCHRONOUS", decisions)


if __name__ == "__main__":
    unittest.main()
