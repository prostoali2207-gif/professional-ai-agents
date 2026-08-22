import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).with_name("paid_workflow_guard.py")
spec = importlib.util.spec_from_file_location("paid_workflow_guard", MODULE_PATH)
g = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(g)


class PaidWorkflowGuardTests(unittest.TestCase):
    def test_manual_provider_workflow_passes(self):
        workflows = {
            ".github/workflows/manual.yml": """name: x\non:\n  workflow_dispatch:\njobs:\n  x:\n    env:\n      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}\n"""
        }
        self.assertEqual(g.evaluate(workflows, {}), [])

    def test_automatic_provider_workflow_fails(self):
        workflows = {
            ".github/workflows/auto.yml": """name: x\non:\n  push:\n    branches: [main]\njobs:\n  x:\n    env:\n      GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}\n"""
        }
        errors = g.evaluate(workflows, {})
        self.assertEqual(len(errors), 1)
        self.assertIn("provider credential + push/pull_request trigger", errors[0])

    def test_automatic_deterministic_workflow_passes(self):
        workflows = {
            ".github/workflows/static.yml": """name: x\non:\n  pull_request:\njobs:\n  x:\n    steps:\n      - run: python -m unittest\n"""
        }
        self.assertEqual(g.evaluate(workflows, {}), [])

    def test_reviewed_exception_requires_invariants(self):
        path = ".github/workflows/mixed.yml"
        text = """name: x\non:\n  pull_request:\n  workflow_dispatch:\njobs:\n  paid:\n    if: github.event_name == 'workflow_dispatch'\n    env:\n      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}\n"""
        rule = {
            "reason": "Automatic path is deterministic and paid job is manual-gated.",
            "required_substrings": ["if: github.event_name == 'workflow_dispatch'"],
        }
        self.assertEqual(g.evaluate({path: text}, {path: rule}), [])

        broken = text.replace("if: github.event_name == 'workflow_dispatch'", "if: always()")
        errors = g.evaluate({path: broken}, {path: rule})
        self.assertTrue(any("reviewed exception invariant missing" in e for e in errors))

    def test_stale_exception_fails_closed(self):
        path = ".github/workflows/manual.yml"
        text = """name: x\non:\n  workflow_dispatch:\njobs:\n  x:\n    env:\n      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}\n"""
        rule = {
            "reason": "This used to be automatic but is now manual-only and should be removed.",
            "required_substrings": ["workflow_dispatch"],
        }
        errors = g.evaluate({path: text}, {path: rule})
        self.assertTrue(any("stale exception" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
