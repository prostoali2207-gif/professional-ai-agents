#!/usr/bin/env python3
"""One-call unscored runtime canary for Conversion Messaging & Web Copy 0.1.0."""
from __future__ import annotations
import json, os, subprocess, sys

EXECUTOR = "architect/evaluation/conversion_messaging_web_copy/executor_v0_1_responses.py"


def main() -> int:
    env = os.environ.copy()
    env.setdefault("MESSAGING_MODEL", "gpt-5.6-terra")
    payload = {
        "task": "Canary only. Return a concise bounded copy decision: do not invent a customer testimonial when none is supplied.",
        "context": {"verified_facts": ["No customer testimonial is available."]},
        "constraints": ["Do not fabricate evidence."],
    }
    proc = subprocess.run(
        [sys.executable, EXECUTOR],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        env=env,
        timeout=180,
    )
    if proc.returncode != 0:
        print(proc.stderr[-2000:], file=sys.stderr)
        return proc.returncode or 2
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print("canary executor output is not JSON", file=sys.stderr)
        return 2
    if out.get("protocol") != "conversion-messaging-web-copy-candidate-v1" or not isinstance(out.get("final_response"), str):
        print("canary runtime protocol mismatch", file=sys.stderr)
        return 2
    print(json.dumps({"status": "PASS", "api_calls": out.get("model_usage", {}).get("api_calls", 0)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
