#!/usr/bin/env python3
"""No-API startup probe for an extracted qualification sealed runner.

Loads the runner exactly far enough to execute top-level imports/bindings while
never calling runner.main(). This catches packaging/import-path defects before a
provider canary or scored execution.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys


def probe(runner: Path, timeout: int) -> None:
    runner = runner.resolve()
    if not runner.is_file():
        raise RuntimeError(f"sealed runner missing: {runner}")

    # Use a fresh interpreter so success cannot depend on modules/sys.path leaked
    # from qualification_preflight.py. sys.path[0] is set to the sealed runner
    # directory, matching `python /path/to/runner.py`, but __main__ is not invoked.
    code = r'''
import importlib.util, os, pathlib, sys
p = pathlib.Path(os.environ["QUALIFICATION_RUNNER_PROBE_PATH"]).resolve()
sys.path[0] = str(p.parent)
spec = importlib.util.spec_from_file_location("qualification_sealed_startup_probe", p)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot create sealed runner import spec")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
if not callable(getattr(m, "main", None)):
    raise RuntimeError("sealed runner does not expose callable main()")
'''
    env = os.environ.copy()
    env["QUALIFICATION_RUNNER_PROBE_PATH"] = str(runner)
    # Provider credentials are deliberately stripped. Import/startup validation
    # must not require or spend them.
    for name in list(env):
        if name.endswith("_API_KEY") or name.endswith("_TOKEN"):
            env.pop(name, None)
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"sealed runner startup probe timed out after {timeout}s") from exc
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise RuntimeError(f"sealed runner startup failed before main(): {detail[-2000:]}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runner", required=True)
    ap.add_argument("--timeout", type=int, default=30)
    args = ap.parse_args()
    try:
        probe(Path(args.runner), args.timeout)
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "failure_class": "SEALED_RUNNER_STARTUP_INVALID", "message": str(exc)}))
        return 2
    print(json.dumps({"status": "PASS", "check": "sealed_runner_startup", "runner": args.runner}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
