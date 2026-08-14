#!/usr/bin/env python3
"""Diagnostic wrapper that preserves adapter stdout when a child exits non-zero.

Temporary compatibility shim for runner v2 observability. It does not change
candidate behavior; it only mirrors failure output to stderr so the harness run
record retains the root-cause message.
"""
import subprocess
import sys


def main() -> int:
    payload = sys.stdin.read()
    proc = subprocess.run(
        [sys.executable, "architect/evaluation/harness/adapters/github_models_adapter.py"],
        input=payload,
        text=True,
        capture_output=True,
    )
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    if proc.returncode != 0 and proc.stdout:
        sys.stderr.write("\nADAPTER_STDOUT_ON_FAILURE:\n" + proc.stdout)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
