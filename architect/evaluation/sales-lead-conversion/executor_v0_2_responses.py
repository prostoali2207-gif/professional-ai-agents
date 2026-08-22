#!/usr/bin/env python3
"""Responses runtime bound to frozen Sales / Lead Conversion 0.2.0 candidate.

This wrapper reuses the already-qualified Responses execution mechanism while
rebinding only the frozen candidate identity. It does not read grader data or
sealed fixtures.
"""
from __future__ import annotations
import io, json, sys
import executor as common

common.FROZEN_COMMIT = "824216b9eb225a4509f98f1c31892a80935f3bd7"
common.FROZEN_DIGEST = "sha256:06b9adc5259cabdad5c4f7939db99b8cbcf0c45f8d88d42ceb437f786687a728"
common.MANIFEST_PATH = "architect/library/cores/sales-lead-conversion/0.2.0/manifest.json"

import executor_responses as impl


def main() -> int:
    original = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    try:
        code = impl.main()
    finally:
        sys.stdout = original
    if code != 0:
        return code
    data = json.loads(buf.getvalue())
    data["candidate_identity"]["core"] = "sales-lead-conversion/0.2.0"
    data["runtime_identity"]["executor"] = "sales-lead-conversion/executor_v0_2_responses.py@v1"
    json.dump(data, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
