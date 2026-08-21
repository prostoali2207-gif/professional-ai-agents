#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("sales_responses_executor", HERE / "executor_responses.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ResponsesExecutorTests(unittest.TestCase):
    def test_tool_definition_uses_responses_shape(self):
        tools = MODULE.responses_tool_definitions({"tools": [{
            "name": "verify_price",
            "description": "Verify price",
            "parameters": {"type": "object", "properties": {}},
        }]})
        self.assertEqual(tools[0]["type"], "function")
        self.assertEqual(tools[0]["name"], "verify_price")
        self.assertNotIn("function", tools[0])

    def test_extracts_function_call(self):
        payload = {"output": [{
            "type": "function_call",
            "call_id": "call_123",
            "name": "verify_price",
            "arguments": "{}",
        }]}
        text, calls = MODULE.extract_response(payload)
        self.assertIsNone(text)
        self.assertEqual(calls, [{
            "call_id": "call_123",
            "name": "verify_price",
            "arguments": "{}",
        }])

    def test_extracts_output_text(self):
        payload = {"output": [{
            "type": "message",
            "content": [{"type": "output_text", "text": "54,000 AED"}],
        }]}
        text, calls = MODULE.extract_response(payload)
        self.assertEqual(text, "54,000 AED")
        self.assertEqual(calls, [])

    def test_usage_normalization_accepts_responses_fields(self):
        usage = MODULE.common.normalize_usage({
            "input_tokens": 500,
            "output_tokens": 40,
            "total_tokens": 540,
            "input_tokens_details": {"cached_tokens": 300},
        })
        self.assertEqual(usage["input_tokens"], 500)
        self.assertEqual(usage["output_tokens"], 40)
        self.assertEqual(usage["cached_input_tokens"], 300)


if __name__ == "__main__":
    unittest.main()
