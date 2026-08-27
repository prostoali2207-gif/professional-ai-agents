#!/usr/bin/env python3
"""Offline stand-in for the frozen candidate executor. Emits the same envelope
shape without contacting any provider. Used only to exercise infrastructure."""
import json, sys
payload = json.load(sys.stdin)
print(json.dumps({
    "status": "completed",
    "candidate_identity": {"commit": "163f68671288fe5035a8d09197334ec9df728b93",
                           "digest": "sha256:ce5f537d336e6a6396f47c1ae492a687c4dc4b30ade8ab37bb4abb94d6251c0f",
                           "runtime": "social-content-creative-gemini-v1",
                           "provider": "gemini-interactions-api", "model": "stub"},
    "final_output": json.dumps({"status": "blocked", "blockers": ["offline rehearsal stub"]}),
    "observable": {"tool_calls": [], "state_events": [], "side_effects": []},
    "transport": {"provider": "stub", "model": "stub"}}, ensure_ascii=False))
