#!/usr/bin/env python3
"""Reference adapter used only to test harness mechanics.

This is NOT Agent Architect and MUST NOT be counted as behavioral release evidence.
"""

import json
import sys

payload = json.load(sys.stdin)
result = {
    "candidate_identity": {
        "sha": payload["candidate_sha"],
        "runtime": "reference-smoke-adapter",
        "model": "none",
        "tools": [],
    },
    "status": "completed",
    "final_output": "harness smoke ok",
    "termination_reason": "fixture completed",
    "observable": {
        "tool_calls": [],
        "state_events": [],
        "resource_loads": [],
        "side_effects": [],
    },
    "smoke_marker": "AA_HARNESS_OK",
}
json.dump(result, sys.stdout)
