import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
CASES = HERE / "semantic_cases.json"


class ToolResilienceSemanticCaseContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(CASES.read_text(encoding="utf-8"))

    def test_exact_case_set(self):
        self.assertEqual(
            [case["id"] for case in self.cases],
            [f"TRS-S{i}" for i in range(1, 11)],
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
            self.assertTrue(case["facts"], case["id"])
            self.assertTrue(case["required_decision"], case["id"])
            self.assertTrue(case["critical_rationale"], case["id"])
            self.assertTrue(case["forbidden_shortcut"], case["id"])

    def test_distinct_decisions(self):
        decisions = {case["required_decision"] for case in self.cases}
        self.assertGreaterEqual(len(decisions), 9)
        self.assertIn("DO_NOT_IMPROVISE_ESCALATE", decisions)
        self.assertIn("RETRY_BOUNDED_BEFORE_BUILDING_SUBSTITUTE", decisions)
        self.assertIn("USE_SPREADSHEET_OR_SCRIPT_AS_VALID_CROSS_DOMAIN_SUBSTITUTE", decisions)

    def test_contains_both_substitute_and_anti_substitute_cases(self):
        serialized = json.dumps(self.cases).lower()
        self.assertIn("cross_domain_transfer", serialized)
        self.assertIn("false_equivalence", serialized)
        self.assertIn("bounded_retry", serialized)
        self.assertIn("irreversibility", serialized)
        self.assertIn("graceful_degradation", serialized)
        self.assertIn("verification_after_substitution", serialized)

    def test_no_universal_novelty_rule(self):
        retry_case = next(c for c in self.cases if c["id"] == "TRS-S10")
        self.assertEqual(
            retry_case["required_decision"],
            "RETRY_BOUNDED_BEFORE_BUILDING_SUBSTITUTE",
        )
        irreversible_case = next(c for c in self.cases if c["id"] == "TRS-S7")
        self.assertEqual(irreversible_case["required_decision"], "DO_NOT_IMPROVISE_ESCALATE")


if __name__ == "__main__":
    unittest.main()
