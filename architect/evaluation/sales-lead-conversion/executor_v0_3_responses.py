#!/usr/bin/env python3
"""Responses runtime bound to frozen Sales / Lead Conversion 0.3.0 candidate.

This wrapper reuses the existing Responses execution mechanism while rebinding
only the frozen candidate identity. It does not read grader data or sealed
fixtures. ``--qualification-contract`` is a deterministic no-API probe used by
qualification infrastructure before any scored model call.
"""
from __future__ import annotations
import io, json, sys
import executor as common

common.FROZEN_COMMIT = "5adc0d315f6f63bc92df0a921040954a3541ef89"
common.FROZEN_DIGEST = "sha256:a33bae7c2957e415669852d10135902349f20fdc9ae22090bf8d55278e0b15c2"
common.MANIFEST_PATH = "architect/library/cores/sales-lead-conversion/0.3.0/manifest.json"

import executor_responses as impl

CONTRACT = {
    "contract_version": 1,
    "candidate_commit": common.FROZEN_COMMIT,
    "candidate_digest": common.FROZEN_DIGEST,
    "core": "sales-lead-conversion/0.3.0",
    "executor": "sales-lead-conversion/executor_v0_3_responses.py@v1",
    "provider": "openai-responses-api",
    "input_protocol": "sales-lead-conversion-candidate-v1",
    "tool_protocol": "sales-deterministic-tools-v1",
    "state_protocol": "sales-state-checkpoint-v1",
    "observable_protocol": "sales-observable-ledger-v1",
}


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--qualification-contract":
        json.dump(CONTRACT, sys.stdout, ensure_ascii=False, sort_keys=True)
        sys.stdout.write("\n")
        return 0

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
    data["candidate_identity"]["core"] = "sales-lead-conversion/0.3.0"
    data["runtime_identity"]["executor"] = "sales-lead-conversion/executor_v0_3_responses.py@v1"
    json.dump(data, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
