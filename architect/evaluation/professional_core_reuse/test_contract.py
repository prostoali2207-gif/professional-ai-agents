import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CASES = HERE / "semantic_cases.json"


class ProfessionalCoreReuseContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(CASES.read_text(encoding="utf-8"))
        cls.skill = (ROOT / "architect/SKILL.md").read_text(encoding="utf-8")
        cls.method = (ROOT / "architect/methodology/professional-core-reuse.md").read_text(encoding="utf-8")

    def test_router_reaches_methodology(self):
        self.assertIn("methodology/professional-core-reuse.md", self.skill)

    def test_required_decision_vocabulary_is_executable(self):
        for token in ("REUSE", "ADAPT", "EXTEND", "FORK", "BUILD NEW", "REJECT"):
            self.assertIn(token, self.skill)
            self.assertIn(token, self.method)

    def test_compatibility_and_pass_inheritance_rules_are_reachable(self):
        for phrase in ("compatibility", "Historical PASS", "delta"):
            self.assertIn(phrase.lower(), self.skill.lower())
        self.assertIn("Historical PASS evidence is prior evidence, not a transferable certificate", self.method)

    def test_exact_frozen_case_set(self):
        self.assertEqual([c["id"] for c in self.cases], [f"PCR-S{i}" for i in range(1, 7)])

    def test_cases_have_hidden_grader_contract(self):
        required = {"id", "title", "facts", "allowed_decisions", "forbidden_decisions", "required_flags"}
        for case in self.cases:
            self.assertTrue(required.issubset(case), case["id"])
            self.assertTrue(case["allowed_decisions"])
            self.assertTrue(case["required_flags"])

    def test_cases_cover_core_failure_modes(self):
        joined = json.dumps(self.cases).lower()
        for term in ("title", "stale", "project", "historical", "domain", "cheap"):
            self.assertIn(term, joined)


if __name__ == "__main__":
    unittest.main()
