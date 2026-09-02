#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE = Path("architect/evaluation/content-architecture-v04-practical-handoff/run_practical_handoff_v01.py")
OLD_GATE = "content-architecture-v0.4-practical-handoff-2026-09-02-r1"
NEW_GATE = "content-architecture-v0.4-practical-handoff-2026-09-02-r2"
OLD_FIXTURE_SHA = "9a9cbc3ecec8acaa1f3f6fa76d7311e584202f43"
NEW_FIXTURE_SHA = "bee85c8be6b7cfea25d9bfd3c3dff70ba9969701"
OLD_FIXTURE_PATH = "architect/evaluation/content-architecture-v04-practical-handoff/practical-fixture-v0.1.json"
NEW_FIXTURE_PATH = "architect/evaluation/content-architecture-v04-practical-handoff-r2/practical-fixture-v0.1.json"


def main() -> int:
    src = SOURCE.read_text(encoding="utf-8")
    for old, new in [
        (OLD_GATE, NEW_GATE),
        (OLD_FIXTURE_SHA, NEW_FIXTURE_SHA),
        (OLD_FIXTURE_PATH, NEW_FIXTURE_PATH),
    ]:
        if old not in src:
            raise SystemExit(f"expected frozen r1 token missing: {old}")
        src = src.replace(old, new)
    with tempfile.TemporaryDirectory(prefix="ca-practical-r2-") as td:
        generated = Path(td) / "run_practical_handoff_r2_generated.py"
        generated.write_text(src, encoding="utf-8")
        p = subprocess.run([sys.executable, str(generated), *sys.argv[1:]])
        return p.returncode


if __name__ == "__main__":
    raise SystemExit(main())
