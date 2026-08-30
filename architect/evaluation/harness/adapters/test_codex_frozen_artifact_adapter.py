from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[4]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


adapter = load("codex_adapter", Path(__file__).with_name("codex_frozen_artifact_adapter.py"))
mcp = load("codex_mcp", Path(__file__).with_name("codex_frozen_artifact_mcp.py"))


class CodexAdapterTests(unittest.TestCase):
    def test_exact_candidate_blob_is_loadable(self):
        source = adapter.load_git_blob("5d440e1bf3e20fbd35c6ab276310a904e36cc06d")
        self.assertIn("Content Architecture", source)

    def test_command_disables_unmediated_capabilities(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            command = adapter.build_command(
                model="gpt-5.6-sol", reasoning="medium", candidate_root=root / "candidate",
                config_path=root / "config.json", repo_root=ROOT, workspace=root, max_tool_calls=3,
            )
        joined = " ".join(command)
        for required in (
            "--ephemeral", "--ignore-user-config", "--ignore-rules", "features.shell_tool=false",
            "features.multi_agent=false", "apps._default.enabled=false", "tools.web_search=false",
            "sandbox_workspace_write.network_access=false", "mcp_servers.evaluator.required=true",
            "mcp_servers.evaluator.default_tools_approval_mode",
        ):
            self.assertIn(required, joined)

    def test_fake_fixture_tools_are_observable_and_persisted(self):
        with tempfile.TemporaryDirectory() as raw:
            workspace = Path(raw)
            config = workspace / "config.json"
            config.write_text(json.dumps({
                "allowed_resources": [],
                "observed_state": {"phase": "fake"},
                "fixture_tools": {"commit_once": {"responses": [{
                    "ok": False,
                    "error": "ambiguous timeout",
                    "side_effect": {"committed": True, "id": "fake-1"},
                    "state_event": {"checkpoint": "fake-1"},
                }]}},
            }), encoding="utf-8")
            server = mcp.Server(config, ROOT, workspace, 3)
            result = server.invoke("fixture_call", {"name": "commit_once", "arguments": {"value": 1}})
            self.assertEqual(result["error"], "ambiguous timeout")
            state = server.invoke("observed_state", {})
            self.assertEqual(state["persisted_side_effects"][0]["effect"]["id"], "fake-1")
            self.assertEqual(state["persisted_state_events"][0]["event"]["checkpoint"], "fake-1")
            self.assertEqual(len(mcp.read_jsonl(workspace / "frozen-artifact-tool-trace.jsonl")), 2)

    def test_forbidden_resource_is_denied_even_if_allowlisted(self):
        relative = "architect/evaluation/content-architecture-v04-fresh/grader_v01.py"
        self.assertIsNone(mcp.safe_resource(ROOT, relative, {relative}))


if __name__ == "__main__":
    unittest.main()
