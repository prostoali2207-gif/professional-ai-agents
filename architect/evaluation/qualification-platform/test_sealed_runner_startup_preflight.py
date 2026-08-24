#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("startup_preflight", HERE / "sealed_runner_startup_preflight.py")
assert SPEC and SPEC.loader
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


def write(path: Path, text: str) -> Path:
    path.write_text(text)
    return path


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        good = write(root / "good.py", "def main():\n    return 0\n")
        m.probe(good, 5)

        # Regression for Sales r9: runner is syntactically valid but a public
        # helper is absent from its effective startup import path. Old static +
        # sealed checks passed this class of defect; the startup probe must not.
        bad = write(root / "r9_like.py", "from helper_outside_sealed_path import pace\ndef main():\n    return 0\n")
        try:
            m.probe(bad, 5)
        except RuntimeError as exc:
            assert "startup failed before main" in str(exc)
            assert "helper_outside_sealed_path" in str(exc)
        else:
            raise AssertionError("r9-like missing-import defect was not detected")

        no_main = write(root / "no_main.py", "VALUE = 1\n")
        try:
            m.probe(no_main, 5)
        except RuntimeError as exc:
            assert "callable main" in str(exc)
        else:
            raise AssertionError("runner without main() was not rejected")

    print("SEALED_RUNNER_STARTUP_REGRESSION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
