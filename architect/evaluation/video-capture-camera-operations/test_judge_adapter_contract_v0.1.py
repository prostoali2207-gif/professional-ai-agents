#!/usr/bin/env python3
"""Deterministic regression for the 2026-09-10 Stage B1 judge-adapter defect.

Defect reproduced here (LOCAL_EXECUTION_FAIL, 1 candidate call, 0 judge calls):
B1 died on its first judge call with

    JSONDecodeError: Expecting value: line 1 column 1 (char 0)

Two distinct code paths raised that identical message and the adapter kept no
raw output, so the real cause was unrecoverable from the artifact:
  1. `json.load(sys.stdin)` when the runner payload arrived empty;
  2. `json.loads(proc.stdout)` when the judge CLI exited 0 with empty or
     fenced output.
The child `claude` process also inherited the adapter's already-consumed stdin
pipe (observed live as "no stdin data received in 3s, proceeding without it").

These checks run with zero provider/model calls.
"""
from __future__ import annotations

import importlib.util
import inspect
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), HERE / name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(condition: bool, label: str, failures: list[str]) -> None:
    print(("PASS " if condition else "FAIL ") + label)
    if not condition:
        failures.append(label)


def main() -> int:
    failures: list[str] = []
    judge = load("claude_judge_adapter_v0.1.py")

    good = {"decision": "PASS", "failed_observables": [], "triggered_hard_fails": [],
            "brief_rationale": "ok"}

    # Raw JSON still parses unchanged -- the four B0 judgments are unaffected.
    check(judge.extract_json(json.dumps(good)) == good,
          "raw JSON judgment parses unchanged", failures)

    # A fenced object carries the identical judgment and is now unwrapped.
    check(judge.extract_json("```json\n" + json.dumps(good) + "\n```") == good,
          "fenced JSON judgment is unwrapped", failures)

    # Empty output must be named as such, not surfaced as an opaque decode error.
    for label, text in (("empty stdout", ""), ("whitespace-only stdout", "   \n  ")):
        try:
            judge.extract_json(text)
            check(False, f"{label} raises a named error", failures)
        except RuntimeError as exc:
            check("empty output" in str(exc), f"{label} raises a named error", failures)

    # Unparseable output must carry a raw sample so the cause is diagnosable.
    try:
        judge.extract_json("I cannot grade this fixture.")
        check(False, "non-JSON output reports a raw sample", failures)
    except RuntimeError as exc:
        check("raw sample" in str(exc) and "cannot grade" in str(exc),
              "non-JSON output reports a raw sample", failures)

    # Grading strictness is unchanged: schema and decision vocabulary still enforced.
    for label, bad in (
        ("extra key rejected", dict(good, extra=1)),
        ("missing key rejected", {k: v for k, v in good.items() if k != "brief_rationale"}),
        ("bad decision rejected", dict(good, decision="MAYBE")),
        ("malformed list rejected", dict(good, failed_observables="none")),
    ):
        try:
            judge.extract_json(json.dumps(bad))
            check(False, label, failures)
        except RuntimeError:
            check(True, label, failures)

    # The child must never inherit the adapter's consumed stdin pipe.
    src = inspect.getsource(judge.run)
    check("stdin=subprocess.DEVNULL" in src,
          "judge child gets DEVNULL stdin, not the consumed pipe", failures)

    # An empty runner payload must be distinguishable from an unparseable judgment.
    main_src = inspect.getsource(judge.main)
    check("empty stdin payload" in main_src,
          "empty runner payload raises its own distinct error", failures)

    if failures:
        print(f"\nFAILED: {len(failures)}")
        return 1
    print("\nOK: judge adapter contract regression passed with 0 provider calls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
