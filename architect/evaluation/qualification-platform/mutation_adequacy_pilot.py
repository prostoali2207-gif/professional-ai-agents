#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = [
    "qualification_preflight.py",
    "sealed_pack_keys.py",
    "paid_workflow_guard.py",
    "test_property_invariants.py",
]

MUTATIONS = [
    (
        "timeout-equality-fail-open",
        "qualification_preflight.py",
        'if model_timeout >= candidate_timeout:',
        'if model_timeout > candidate_timeout:',
    ),
    (
        "zip-traversal-check-removed",
        "qualification_preflight.py",
        'if p.is_absolute() or ".." in p.parts:',
        'if p.is_absolute():',
    ),
    (
        "manual-provider-workflow-blocked",
        "paid_workflow_guard.py",
        'if not (provider and automatic):',
        'if not provider:',
    ),
]


def run_mutation(name: str, filename: str, old: str, new: str) -> tuple[str, bool, str]:
    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        for item in FILES:
            shutil.copy2(ROOT / item, work / item)

        target = work / filename
        source = target.read_text(encoding="utf-8")
        if source.count(old) != 1:
            return name, False, f"mutation target count={source.count(old)} expected=1"
        target.write_text(source.replace(old, new, 1), encoding="utf-8")

        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "test_property_invariants.py"],
            cwd=work,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
        )
        killed = proc.returncode != 0
        return name, killed, proc.stdout[-3000:]


def main() -> int:
    survived = []
    for mutation in MUTATIONS:
        name, killed, output = run_mutation(*mutation)
        print(f"{name}: {'KILLED' if killed else 'SURVIVED'}")
        if not killed:
            survived.append((name, output))

    if survived:
        print("MUTATION_ADEQUACY_FAIL")
        for name, output in survived:
            print(f"--- surviving mutation: {name} ---")
            print(output)
        return 1

    print(f"MUTATION_ADEQUACY_PASS killed={len(MUTATIONS)}/{len(MUTATIONS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
