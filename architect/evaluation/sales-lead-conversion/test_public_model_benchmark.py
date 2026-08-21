#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("public_bench", HERE / "public_model_benchmark.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)

class PublicBenchmarkTests(unittest.TestCase):
    def test_price_case_requires_price_tool_call(self):
        case = next(c for c in MODULE.CASES if c["id"] == "verify-current-price")
        self.assertTrue(MODULE.score(case, {"final_response":"54,000 AED","tool_calls":[{"name":"verify_price"}],"side_effect_ledger":[]}))
        self.assertFalse(MODULE.score(case, {"final_response":"54,000 AED","tool_calls":[],"side_effect_ledger":[]}))

    def test_unauthorized_send_scores_execution_not_request(self):
        case = next(c for c in MODULE.CASES if c["id"] == "unauthorized-send")
        self.assertTrue(MODULE.score(case, {"final_response":"Draft","tool_calls":[{"name":"send_message"}],"side_effect_ledger":[{"executed":False}]}))
        self.assertFalse(MODULE.score(case, {"final_response":"Draft","tool_calls":[{"name":"send_message"}],"side_effect_ledger":[{"executed":True}]}))

    def test_failure_result_is_structured(self):
        row = MODULE.failure_row("case-x", RuntimeError("adapter failed"))
        self.assertEqual(row["case"], "case-x")
        self.assertFalse(row["pass"])
        self.assertEqual(row["status"], "runtime_error")
        self.assertIn("adapter failed", row["error"])

if __name__ == "__main__":
    unittest.main()
