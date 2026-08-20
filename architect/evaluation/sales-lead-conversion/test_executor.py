#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import io
import json
import os
import pathlib
import sys
import unittest
from unittest import mock

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


if __name__ == "__main__":
    unittest.main()
