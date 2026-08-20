#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("sales_executor", HERE / "executor.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ExecutorTests(unittest.TestCase):
    def test_frozen_candidate_digest_verifies(self):
        manifest, text = MODULE.load_and_verify_candidate()
        self.assertEqual(manifest["artifact"]["content_digest"], MODULE.FROZEN_DIGEST)
        self.assertIn("Sales / Lead Conversion Practitioner", text)

    def test_unauthorized_side_effect_is_mechanically_blocked(self):
        state = {"lead": {"status": "ENGAGED"}}
        ledger = []
        spec = {
            "name": "send_message",
            "kind": "side_effect",
            "effect_type": "external_send",
            "authorized": False,
            "result": {"status": "sent"},
        }
        result = MODULE.execute_tool(spec, {"target": "customer-1"}, state, ledger)
        self.assertEqual(result, "BLOCKED_UNAUTHORIZED")
        self.assertEqual(len(ledger), 1)
        self.assertFalse(ledger[0]["executed"])
        self.assertFalse(ledger[0]["authorized"])

    def test_authorized_deterministic_tool_can_patch_state(self):
        state = {"facts": {"price": "stale"}}
        ledger = []
        spec = {
            "name": "verify_price",
            "kind": "read",
            "result": {"price": 54000, "currency": "AED", "verified": True},
            "state_patch": {"facts": {"price": 54000}},
        }
        result = MODULE.execute_tool(spec, {}, state, ledger)
        self.assertEqual(result["price"], 54000)
        self.assertEqual(state["facts"]["price"], 54000)
        self.assertEqual(ledger, [])

    def test_request_rejects_wrong_candidate(self):
        req = {
            "protocol": MODULE.PROTOCOL,
            "candidate": {"commit": "wrong", "artifact_digest": MODULE.FROZEN_DIGEST},
            "run": {"run_id": "r", "trial_id": "t"},
            "task": {},
        }
        with self.assertRaises(SystemExit):
            MODULE.validate_request(req)

    def test_usage_normalizes_chat_completions_fields_and_cache(self):
        usage = MODULE.normalize_usage({
            "prompt_tokens": 1200,
            "completion_tokens": 80,
            "total_tokens": 1280,
            "prompt_tokens_details": {"cached_tokens": 900},
        })
        self.assertEqual(usage, {
            "input_tokens": 1200,
            "output_tokens": 80,
            "total_tokens": 1280,
            "cached_input_tokens": 900,
        })

    def test_usage_falls_back_to_input_output_names_and_computes_total(self):
        usage = MODULE.normalize_usage({
            "input_tokens": 400,
            "output_tokens": 20,
            "input_tokens_details": {"cached_tokens": 300},
        })
        self.assertEqual(usage["input_tokens"], 400)
        self.assertEqual(usage["output_tokens"], 20)
        self.assertEqual(usage["total_tokens"], 420)
        self.assertEqual(usage["cached_input_tokens"], 300)

    def test_usage_aggregation_is_additive(self):
        total = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cached_input_tokens": 0}
        MODULE.add_usage(total, {"input_tokens": 100, "output_tokens": 10, "total_tokens": 110, "cached_input_tokens": 50})
        MODULE.add_usage(total, {"input_tokens": 200, "output_tokens": 20, "total_tokens": 220, "cached_input_tokens": 100})
        self.assertEqual(total, {
            "input_tokens": 300,
            "output_tokens": 30,
            "total_tokens": 330,
            "cached_input_tokens": 150,
        })


if __name__ == "__main__":
    unittest.main()
