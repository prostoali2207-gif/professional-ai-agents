#!/usr/bin/env python3
"""Deterministic tests for frozen-artifact adapter identity loading.

No model/API call is made. These tests validate only Git-blob loading mechanics.
"""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ADAPTER = Path(__file__).parent / "adapters" / "openai_frozen_artifact_adapter.py"
spec = importlib.util.spec_from_file_location("frozen_adapter", ADAPTER)
assert spec and spec.loader
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class FrozenBlobIdentityTests(unittest.TestCase):
    def test_loads_exact_git_blob_content(self) -> None:
        original = Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            candidate = root / "candidate.md"
            expected = "# Candidate\n\nImmutable professional instruction.\n"
            candidate.write_text(expected, encoding="utf-8")
            sha = subprocess.run(
                ["git", "hash-object", "-w", "candidate.md"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            os.chdir(root)
            try:
                observed = adapter.load_git_blob(sha)
            finally:
                os.chdir(original)
            self.assertEqual(observed, expected)

    def test_rejects_commit_object_as_candidate(self) -> None:
        original = Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "eval@example.invalid"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Eval"], cwd=root, check=True)
            (root / "x").write_text("x", encoding="utf-8")
            subprocess.run(["git", "add", "x"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            commit = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True
            ).stdout.strip()
            os.chdir(root)
            try:
                with self.assertRaises(SystemExit):
                    adapter.load_git_blob(commit)
            finally:
                os.chdir(original)


if __name__ == "__main__":
    unittest.main()
