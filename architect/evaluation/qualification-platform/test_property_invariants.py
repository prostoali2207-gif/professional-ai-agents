#!/usr/bin/env python3
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

import pytest
from hypothesis import assume, given, strategies as st

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import paid_workflow_guard as guard
import qualification_preflight as preflight
import sealed_pack_keys as keys


@given(
    master=st.binary(min_size=1, max_size=64),
    context_a=st.text(min_size=1, max_size=80),
    context_b=st.text(min_size=1, max_size=80),
)
def test_sealed_key_derivation_is_deterministic_and_context_separated(master, context_a, context_b):
    assume(context_a != context_b)
    a1 = keys.derive_fernet_key(master, context_a)
    a2 = keys.derive_fernet_key(master, context_a)
    b = keys.derive_fernet_key(master, context_b)
    assert a1 == a2
    assert a1 != b


@given(
    model_timeout=st.integers(min_value=1, max_value=500),
    candidate_timeout=st.integers(min_value=1, max_value=500),
    workflow_timeout=st.integers(min_value=1, max_value=1000),
)
def test_runtime_timeout_gate_matches_strict_nesting(tmp_path, monkeypatch, model_timeout, candidate_timeout, workflow_timeout):
    monkeypatch.chdir(tmp_path)
    Path("executor.py").write_text("print('ok')\n")
    Path("validator.py").write_text("print('ok')\n")
    manifest = {
        "runtime": {
            "executor_path": "executor.py",
            "model_timeout_seconds": model_timeout,
            "candidate_timeout_seconds": candidate_timeout,
            "workflow_timeout_seconds": workflow_timeout,
            "canary_required": False,
            "credential_env": "PROPERTY_TEST_UNUSED_SECRET",
        },
        "report": {"validator_path": "validator.py"},
    }
    valid = model_timeout < candidate_timeout < workflow_timeout
    if valid:
        preflight.verify_runtime_static(manifest, require_runtime_secret=False)
    else:
        with pytest.raises(preflight.PreflightError) as exc:
            preflight.verify_runtime_static(manifest, require_runtime_secret=False)
        assert exc.value.code == "TIMEOUT_INCOMPATIBLE"


UNSAFE_NAMES = st.one_of(
    st.just("../escape"),
    st.just("a/../../escape"),
    st.just("/absolute/path"),
    st.text(min_size=1, max_size=20).map(lambda tail: f"../{tail}"),
)


@given(name=UNSAFE_NAMES)
def test_safe_extract_rejects_path_traversal(tmp_path, name):
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr(name, "x")
    archive.seek(0)
    with zipfile.ZipFile(archive) as zf:
        with pytest.raises(preflight.PreflightError) as exc:
            preflight.safe_extract(zf, tmp_path / "out")
    assert exc.value.code == "PACK_INTEGRITY_INVALID"


@given(provider=st.sampled_from(["OPENAI", "GEMINI", "ANTHROPIC", "PERPLEXITY", "TAVILY", "EXA"]))
def test_paid_workflow_guard_blocks_automatic_provider_runs_without_exception(provider):
    workflow = f"""name: unsafe\non:\n  push:\n  pull_request:\njobs:\n  run:\n    env:\n      API_KEY: ${{{{ secrets.{provider}_API_KEY }}}}\n    steps:\n      - run: echo test\n"""
    errors = guard.evaluate({".github/workflows/unsafe.yml": workflow}, {})
    assert errors
    assert "provider credential + push/pull_request trigger is not allowed" in errors[0]


@given(provider=st.sampled_from(["OPENAI", "GEMINI", "ANTHROPIC", "PERPLEXITY", "TAVILY", "EXA"]))
def test_paid_workflow_guard_allows_manual_only_provider_workflow(provider):
    workflow = f"""name: manual\non:\n  workflow_dispatch:\njobs:\n  run:\n    env:\n      API_KEY: ${{{{ secrets.{provider}_API_KEY }}}}\n    steps:\n      - run: echo test\n"""
    assert guard.evaluate({".github/workflows/manual.yml": workflow}, {}) == []
