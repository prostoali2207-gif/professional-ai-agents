#!/usr/bin/env python3
"""Unscored live regression for Codex adapter tool/state mediation."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[4]
ADAPTER = Path(__file__).with_name("codex_frozen_artifact_adapter.py")
FAKE_REPO_PATH = "architect/evaluation/harness/smoke/codex_fake_frozen_candidate.md"


def main() -> int:
    # Resolve the already-tracked fake artifact blob instead of writing a new Git
    # object. This keeps the unscored regression compatible with read-only-ish
    # Actions checkouts while preserving the adapter's exact Git-blob identity path.
    digest_proc = subprocess.run(
        ["git", "rev-parse", f"HEAD:{FAKE_REPO_PATH}"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if digest_proc.returncode != 0 or len(digest_proc.stdout.strip()) != 40:
        print(json.dumps({"status": "FAIL", "reason": "fake_blob_unavailable"}))
        return 1
    digest = digest_proc.stdout.strip()
    with tempfile.TemporaryDirectory(prefix="codex-frozen-artifact-live-regression-") as raw:
        workspace = Path(raw)
        payload = {
            "protocol_version": 2,
            "candidate_sha": digest,
            "workspace": str(workspace),
            "input": {
                "task": "FAKE UNSCORED REGRESSION. Execute the fake artifact's procedure and return the requested JSON.",
                "allowed_resources": [],
                "fixture_tools": {
                    "commit_once": {
                        "responses": [{
                            "ok": False,
                            "error": "ambiguous timeout after commit",
                            "side_effect": {"committed": True, "id": "fake-effect-1"},
                            "state_event": {"checkpoint": "fake-checkpoint-1"},
                        }]
                    }
                },
                "observed_state": {"fixture": "evaluator-owned-fake"},
                "max_tool_rounds": 3,
            },
        }
        env = os.environ.copy()
        env.setdefault("FROZEN_ARTIFACT_CODEX_MODEL", "gpt-5.6-sol")
        env.setdefault("FROZEN_ARTIFACT_CODEX_REASONING", "medium")
        env.setdefault("FROZEN_ARTIFACT_CODEX_TIMEOUT", "240")
        diagnostic = workspace / "runtime-diagnostic.json"
        env["FROZEN_ARTIFACT_CODEX_DIAGNOSTIC_FILE"] = str(diagnostic)
        proc = subprocess.run(
            [sys.executable, str(ADAPTER)], input=json.dumps(payload), capture_output=True,
            text=True, encoding="utf-8", errors="replace", env=env, timeout=300,
        )
        if proc.returncode != 0:
            print(json.dumps({"status": "FAIL", "reason": "adapter_nonzero"}))
            return 1
        record = json.loads(proc.stdout)
        calls = record.get("observable", {}).get("tool_calls", [])
        side_effects = record.get("observable", {}).get("side_effects", [])
        state_events = record.get("observable", {}).get("state_events", [])
        names = [call.get("tool") for call in calls]
        output = json.loads(record.get("final_output", ""))
        passed = (
            record.get("status") == "completed"
            and names == ["fixture_call", "observed_state"]
            and len(side_effects) == 1
            and len(state_events) == 1
            and output == {
                "status": "reconciled_committed",
                "effect_id": "fake-effect-1",
                "checkpoint": "fake-checkpoint-1",
            }
        )
        print(json.dumps({
            "status": "PASS" if passed else "FAIL",
            "candidate_sha": digest,
            "runtime_identity": record.get("candidate_identity"),
            "tool_sequence": names,
            "side_effect_count": len(side_effects),
            "state_event_count": len(state_events),
            "usage": record.get("transport", {}).get("usage"),
            "fake_final_output": None if passed else record.get("final_output"),
            "runtime_stderr": None if passed or not diagnostic.exists() else json.loads(diagnostic.read_text(encoding="utf-8")).get("stderr"),
        }, ensure_ascii=False, sort_keys=True))
        return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
