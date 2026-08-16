#!/usr/bin/env python3
"""Provider wrapper for the frozen v1.1 release driver.

This changes only the protocol-v2 transport from OpenAI Responses to Gemini
Interactions. Fixture hashes, thresholds, graders, sequencing, and candidate
instructions remain owned by run_v1_1_release_v5.py.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import run_v1_1_release_v5 as release

HERE = Path(__file__).resolve().parent
release.ADAPTER = HERE / "adapters" / "gemini_interactions_adapter_v2.py"


def requested_out_root() -> Path:
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--out-root" and i + 2 <= len(sys.argv[1:]):
            return Path(sys.argv[1:][i + 1])
        if arg.startswith("--out-root="):
            return Path(arg.split("=", 1)[1])
    return release.ROOT / ".tmp" / "architect-v1_1-release-v5"


def correct_transport_metadata(out_root: Path) -> None:
    grade_path = out_root / "full" / "v1.1-release-v5-grade.json"
    if not grade_path.exists():
        return
    try:
        value = json.loads(grade_path.read_text(encoding="utf-8"))
    except Exception:
        return
    if isinstance(value, dict):
        value["runtime"] = "gemini-interactions-adapter-v2"
        grade_path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    rc = release.main()
    correct_transport_metadata(requested_out_root())
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
