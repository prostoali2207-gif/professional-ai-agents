#!/usr/bin/env python3
"""Deterministic, zero-provider-call qualification preflight.

This runs *before* any evaluator credential is bound and *before* any paid
provider call. It exists because Sales 0.3 burned rounds r4-r10 on the same
candidate without ever reaching a valid scored verdict: every round discovered
the next infrastructure defect only after credentials had been issued and
provider quota had been spent.

Hard invariants of this module:

* zero model/provider calls. Outbound sockets are blocked inside every probe
  interpreter and provider credentials are stripped from their environment;
* no step reads sealed-pack contents. The sealed-runner probes operate on a
  staging directory built from repository files only. Ciphertext, keys and
  hidden fixtures are never touched;
* every failure class has its own process exit code, so a caller can branch on
  the class without parsing text. See ``preflight-failure-codes.md``.

Checks performed (all deterministic, all offline):

1. ``py_compile`` of every declared runner/executor/cycle wrapper;
2. sealed-runner import resolution from the runner's own directory, walking the
   full loader chain exactly as ``python <pack>/runner.py`` would;
3. pack-relative root resolution -- the chain must resolve its pack data files
   inside the pack directory, not inside the evaluator source tree;
4. ``--qualification-contract`` handshake against the preregistration
   (contract version and provider);
5. preregistration <-> cycle-workflow env correspondence (cycle_id,
   fixture_count, thresholds);
6. existence of every file referenced by the manifest/spec reference set;
7. pacing configuration -- minimum request interval declared and non-zero.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import py_compile
import shutil
import subprocess
import sys
import tempfile

EXIT_PASS = 0
EXIT_SPEC_INVALID = 10
EXIT_COMPILE_FAILED = 11
EXIT_SEALED_RUNNER_IMPORT_UNRESOLVED = 12
EXIT_PACK_ROOT_UNRESOLVED = 13
EXIT_CONTRACT_HANDSHAKE_MISMATCH = 14
EXIT_PREREGISTRATION_ENV_MISMATCH = 15
EXIT_MANIFEST_REFERENCE_MISSING = 16
EXIT_PACING_CONFIG_INVALID = 17
EXIT_INTERNAL_ERROR = 20

FAILURE_CLASS = {
    EXIT_SPEC_INVALID: "PREFLIGHT_SPEC_INVALID",
    EXIT_COMPILE_FAILED: "COMPILE_FAILED",
    EXIT_SEALED_RUNNER_IMPORT_UNRESOLVED: "SEALED_RUNNER_IMPORT_UNRESOLVED",
    EXIT_PACK_ROOT_UNRESOLVED: "PACK_ROOT_UNRESOLVED",
    EXIT_CONTRACT_HANDSHAKE_MISMATCH: "CONTRACT_HANDSHAKE_MISMATCH",
    EXIT_PREREGISTRATION_ENV_MISMATCH: "PREREGISTRATION_ENV_MISMATCH",
    EXIT_MANIFEST_REFERENCE_MISSING: "MANIFEST_REFERENCE_MISSING",
    EXIT_PACING_CONFIG_INVALID: "PACING_CONFIG_INVALID",
    EXIT_INTERNAL_ERROR: "PREFLIGHT_INTERNAL_ERROR",
}

CHECK_ORDER = (
    "compile",
    "sealed_runner_chain",
    "contract_handshake",
    "preregistration_env",
    "manifest_references",
    "pacing",
)


class PreflightFailure(Exception):
    def __init__(self, code: int, check: str, message: str, detail: dict | None = None):
        super().__init__(message)
        self.code = code
        self.check = check
        self.detail = detail or {}


def fail(code: int, check: str, message: str, **detail) -> None:
    raise PreflightFailure(code, check, message, detail)


def spec_get(spec: dict, key: str, kind: type):
    if key not in spec:
        fail(EXIT_SPEC_INVALID, "spec", f"preflight spec is missing required key: {key}")
    value = spec[key]
    if not isinstance(value, kind):
        fail(EXIT_SPEC_INVALID, "spec", f"preflight spec key {key} must be {kind.__name__}")
    return value


def resolve_pointer(document, pointer: list, where: str):
    node = document
    for part in pointer:
        if not isinstance(node, dict) or part not in node:
            fail(
                EXIT_SPEC_INVALID,
                "spec",
                f"{where} pointer {'/'.join(str(x) for x in pointer)} does not resolve",
            )
        node = node[part]
    return node


# --------------------------------------------------------------------------
# 1. compilation
# --------------------------------------------------------------------------


def check_compile(spec: dict, root: Path) -> dict:
    paths = spec_get(spec, "compile_paths", list)
    if not paths:
        fail(EXIT_SPEC_INVALID, "compile", "compile_paths must not be empty")
    compiled = []
    with tempfile.TemporaryDirectory(prefix="qualification-preflight-pyc-") as td:
        for index, rel in enumerate(paths):
            source = root / rel
            if not source.is_file():
                fail(
                    EXIT_COMPILE_FAILED,
                    "compile",
                    f"declared source is missing: {rel}",
                    path=rel,
                )
            try:
                py_compile.compile(
                    str(source),
                    cfile=str(Path(td) / f"{index}.pyc"),
                    doraise=True,
                )
            except py_compile.PyCompileError as exc:
                fail(
                    EXIT_COMPILE_FAILED,
                    "compile",
                    f"python syntax invalid in {rel}: {exc.msg}",
                    path=rel,
                )
            compiled.append(rel)
    return {"compiled": compiled}


# --------------------------------------------------------------------------
# 2 + 3. sealed-runner loader chain (imports and pack-root resolution)
# --------------------------------------------------------------------------

# Executed in a fresh interpreter. It reproduces `python <pack>/runner.py`
# faithfully up to -- but never into -- the terminal runner's main(), so no
# fixture is read and no provider call can be made.
CHAIN_PROBE = r'''
import importlib.util, json, os, pathlib, sys, traceback

# Import the network stack before neutering it: ssl builds `class
# SSLSocket(socket)` at import time, so socket.socket must still be a class.
import socket, ssl, urllib.request  # noqa: E402,F401

CONFIG = json.loads(os.environ["QUALIFICATION_CHAIN_PROBE"])
PACK_DIR = pathlib.Path(CONFIG["pack_dir"]).resolve()
RUNNER = PACK_DIR / CONFIG["runner_name"]
CHAIN = [pathlib.Path(p).resolve() for p in CONFIG["loader_chain"]]
TERMINAL = CHAIN[-1]


class NetworkBlocked(RuntimeError):
    pass


def _blocked(*args, **kwargs):
    raise NetworkBlocked("deterministic preflight blocked an outbound network attempt")


# Block at the connect/resolve boundary rather than replacing socket.socket,
# so the type hierarchy the stdlib builds on stays intact.
socket.socket.connect = _blocked
socket.socket.connect_ex = _blocked
socket.create_connection = _blocked
socket.getaddrinfo = _blocked


class ChainComplete(Exception):
    def __init__(self, terminal_file):
        super().__init__("terminal runner reached")
        self.terminal_file = terminal_file


loaded = []
real_spec_from_file_location = importlib.util.spec_from_file_location


class TerminalLoader:
    """Wraps the terminal module's loader so main() becomes a tripwire.

    The module body still executes (that is the import check). main() is
    replaced *after* execution, so the caller's own __file__ rebinding still
    happens and is observable -- that is the pack-root check.
    """

    def __init__(self, inner):
        self._inner = inner

    def create_module(self, spec):
        return self._inner.create_module(spec)

    def exec_module(self, module):
        self._inner.exec_module(module)

        def tripwire(*args, **kwargs):
            raise ChainComplete(getattr(module, "__file__", None))

        module.main = tripwire


def patched_spec_from_file_location(name, location=None, *args, **kwargs):
    spec = real_spec_from_file_location(name, location, *args, **kwargs)
    try:
        resolved = pathlib.Path(location).resolve()
    except (TypeError, ValueError, OSError):
        return spec
    if spec is not None and resolved in CHAIN:
        loaded.append(str(resolved))
        if resolved == TERMINAL and spec.loader is not None:
            spec.loader = TerminalLoader(spec.loader)
    return spec


def emit(payload):
    payload["loaded_chain"] = loaded
    print(json.dumps(payload))


# sys.path[0] is what `python <pack>/runner.py` would set: the pack directory,
# not the evaluator source directory. This is the whole point of the probe.
sys.path[0] = str(PACK_DIR)
importlib.util.spec_from_file_location = patched_spec_from_file_location

try:
    runner_spec = real_spec_from_file_location("qualification_chain_probe_runner", RUNNER)
    if runner_spec is None or runner_spec.loader is None:
        emit({"status": "CHAIN_ERROR", "message": "cannot create sealed runner import spec"})
        raise SystemExit(0)
    loaded.append(str(CHAIN[0]))
    runner_module = importlib.util.module_from_spec(runner_spec)
    runner_spec.loader.exec_module(runner_module)
    if not callable(getattr(runner_module, "main", None)):
        emit({"status": "CHAIN_ERROR", "message": "sealed runner does not expose callable main()"})
        raise SystemExit(0)
    runner_module.main()
except ChainComplete as done:
    emit({"status": "CHAIN_COMPLETE", "terminal_file": done.terminal_file})
except NetworkBlocked as exc:
    emit({"status": "NETWORK_ATTEMPTED", "message": str(exc)})
except (ModuleNotFoundError, ImportError) as exc:
    emit({
        "status": "IMPORT_UNRESOLVED",
        "message": f"{type(exc).__name__}: {exc}",
        "missing_module": getattr(exc, "name", None),
        "traceback": traceback.format_exc()[-2000:],
    })
except FileNotFoundError as exc:
    emit({
        "status": "PACK_FILE_MISSING",
        "message": f"{type(exc).__name__}: {exc}",
        "missing_path": getattr(exc, "filename", None),
        "traceback": traceback.format_exc()[-2000:],
    })
except SystemExit:
    raise
except BaseException as exc:
    emit({
        "status": "CHAIN_ERROR",
        "message": f"{type(exc).__name__}: {exc}",
        "traceback": traceback.format_exc()[-2000:],
    })
else:
    emit({"status": "TERMINAL_NOT_REACHED", "message": "runner main() returned without reaching the terminal runner"})
'''


def check_sealed_runner_chain(spec: dict, root: Path) -> dict:
    section = spec_get(spec, "sealed_runner", dict)
    runner_rel = section.get("runner_path")
    chain_rel = section.get("loader_chain")
    if not isinstance(runner_rel, str) or not isinstance(chain_rel, list) or not chain_rel:
        fail(
            EXIT_SPEC_INVALID,
            "sealed_runner_chain",
            "sealed_runner requires runner_path and a non-empty loader_chain",
        )
    if chain_rel[0] != runner_rel:
        fail(
            EXIT_SPEC_INVALID,
            "sealed_runner_chain",
            "loader_chain must start with runner_path",
        )
    for rel in chain_rel:
        if not (root / rel).is_file():
            fail(
                EXIT_SPEC_INVALID,
                "sealed_runner_chain",
                f"declared loader-chain module is missing: {rel}",
            )

    with tempfile.TemporaryDirectory(prefix="qualification-preflight-pack-") as td:
        # A staging directory that mimics an extracted sealed pack. It contains
        # only a copy of a repository file. No sealed artifact is opened.
        pack_dir = Path(td) / "pack"
        pack_dir.mkdir()
        shutil.copyfile(root / runner_rel, pack_dir / "runner.py")
        expected_runner = str((pack_dir / "runner.py").resolve())

        config = {
            "pack_dir": str(pack_dir),
            "runner_name": "runner.py",
            "loader_chain": [str((root / rel).resolve()) for rel in chain_rel],
        }
        env = {k: v for k, v in os.environ.items() if not (k.endswith("_API_KEY") or k.endswith("_TOKEN"))}
        env["QUALIFICATION_CHAIN_PROBE"] = json.dumps(config)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        timeout = int(section.get("probe_timeout_seconds", 60))
        try:
            proc = subprocess.run(
                [sys.executable, "-c", CHAIN_PROBE],
                cwd=str(root),
                text=True,
                capture_output=True,
                timeout=timeout,
                env=env,
            )
        except subprocess.TimeoutExpired:
            fail(
                EXIT_SEALED_RUNNER_IMPORT_UNRESOLVED,
                "sealed_runner_chain",
                f"sealed-runner loader-chain probe timed out after {timeout}s",
            )

        report = None
        for line in reversed((proc.stdout or "").splitlines()):
            line = line.strip()
            if line.startswith("{"):
                try:
                    report = json.loads(line)
                except json.JSONDecodeError:
                    continue
                break
        if report is None:
            fail(
                EXIT_INTERNAL_ERROR,
                "sealed_runner_chain",
                "loader-chain probe produced no report",
                stderr=(proc.stderr or "")[-2000:],
            )

    status = report.get("status")
    if status == "IMPORT_UNRESOLVED":
        fail(
            EXIT_SEALED_RUNNER_IMPORT_UNRESOLVED,
            "sealed_runner_chain",
            "sealed-runner loader chain cannot resolve its imports from the pack directory: "
            + str(report.get("message")),
            missing_module=report.get("missing_module"),
            loaded_chain=report.get("loaded_chain"),
        )
    if status == "PACK_FILE_MISSING":
        fail(
            EXIT_PACK_ROOT_UNRESOLVED,
            "sealed_runner_chain",
            "sealed-runner loader chain resolved a pack file outside the pack directory: "
            + str(report.get("message")),
            missing_path=report.get("missing_path"),
        )
    if status != "CHAIN_COMPLETE":
        fail(
            EXIT_INTERNAL_ERROR,
            "sealed_runner_chain",
            f"sealed-runner loader-chain probe did not complete ({status}): {report.get('message')}",
            loaded_chain=report.get("loaded_chain"),
        )

    declared = [str((root / rel).resolve()) for rel in chain_rel]
    loaded_chain = report.get("loaded_chain") or []
    missing = [x for x in declared if x not in loaded_chain]
    if missing:
        fail(
            EXIT_SPEC_INVALID,
            "sealed_runner_chain",
            "declared loader-chain modules were never loaded at runtime; the spec has drifted",
            never_loaded=[str(Path(x).relative_to(root)) for x in missing],
        )

    terminal_file = report.get("terminal_file")
    if not terminal_file:
        fail(
            EXIT_PACK_ROOT_UNRESOLVED,
            "sealed_runner_chain",
            "terminal runner has no __file__ binding, so its pack root cannot resolve",
        )
    # The staging directory is already removed, so compare the recorded path
    # strings rather than re-resolving them from disk.
    if str(Path(terminal_file)) != expected_runner:
        fail(
            EXIT_PACK_ROOT_UNRESOLVED,
            "sealed_runner_chain",
            "terminal runner resolves its pack root outside the sealed pack: __file__ is "
            f"{terminal_file}, expected the extracted pack runner",
            terminal_file=terminal_file,
            expected_pack_runner=expected_runner,
        )
    return {"loader_chain": chain_rel, "pack_root_resolved": True}


# --------------------------------------------------------------------------
# 4. contract handshake
# --------------------------------------------------------------------------


def check_contract_handshake(spec: dict, root: Path, prereg: dict) -> dict:
    section = spec_get(spec, "contract", dict)
    argv = section.get("probe_argv")
    if not isinstance(argv, list) or not argv:
        fail(EXIT_SPEC_INVALID, "contract_handshake", "contract.probe_argv must be a non-empty list")
    bindings = section.get("preregistration_bindings")
    if not isinstance(bindings, dict) or not bindings:
        fail(
            EXIT_SPEC_INVALID,
            "contract_handshake",
            "contract.preregistration_bindings must map contract keys to preregistration pointers",
        )

    credential_env = section.get("credential_env")
    env = {k: v for k, v in os.environ.items() if not (k.endswith("_API_KEY") or k.endswith("_TOKEN"))}
    if isinstance(credential_env, str):
        env.pop(credential_env, None)
    timeout = int(section.get("probe_timeout_seconds", 60))
    try:
        proc = subprocess.run(
            argv,
            cwd=str(root),
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
        )
    except FileNotFoundError as exc:
        fail(EXIT_CONTRACT_HANDSHAKE_MISMATCH, "contract_handshake", f"contract probe is not executable: {exc}")
    except subprocess.TimeoutExpired:
        fail(EXIT_CONTRACT_HANDSHAKE_MISMATCH, "contract_handshake", f"contract probe timed out after {timeout}s")
    if proc.returncode != 0:
        fail(
            EXIT_CONTRACT_HANDSHAKE_MISMATCH,
            "contract_handshake",
            f"contract probe exited {proc.returncode}",
            stderr=(proc.stderr or "")[-2000:],
        )
    try:
        observed = json.loads(proc.stdout)
    except json.JSONDecodeError:
        fail(
            EXIT_CONTRACT_HANDSHAKE_MISMATCH,
            "contract_handshake",
            "contract probe did not return JSON on stdout",
        )
    if not isinstance(observed, dict):
        fail(EXIT_CONTRACT_HANDSHAKE_MISMATCH, "contract_handshake", "contract probe did not return a JSON object")

    checked = {}
    for contract_key, pointer in sorted(bindings.items()):
        if not isinstance(pointer, list):
            fail(
                EXIT_SPEC_INVALID,
                "contract_handshake",
                f"preregistration pointer for {contract_key} must be a list",
            )
        expected = resolve_pointer(prereg, pointer, "contract.preregistration_bindings")
        if contract_key not in observed:
            fail(
                EXIT_CONTRACT_HANDSHAKE_MISMATCH,
                "contract_handshake",
                f"executor contract does not declare {contract_key}",
                expected=expected,
            )
        actual = observed[contract_key]
        if actual != expected:
            fail(
                EXIT_CONTRACT_HANDSHAKE_MISMATCH,
                "contract_handshake",
                f"executor contract {contract_key} is {actual!r} but the preregistration declares {expected!r}",
                key=contract_key,
                expected=expected,
                observed=actual,
            )
        checked[contract_key] = actual
    return {"contract": checked}


# --------------------------------------------------------------------------
# 5. preregistration <-> cycle workflow env
# --------------------------------------------------------------------------


def load_workflow_env(root: Path, workflow_rel: str, job: str | None) -> dict:
    try:
        import yaml
    except ImportError:
        fail(EXIT_INTERNAL_ERROR, "preregistration_env", "PyYAML is required to read the cycle workflow")
    path = root / workflow_rel
    if not path.is_file():
        fail(EXIT_SPEC_INVALID, "preregistration_env", f"cycle workflow is missing: {workflow_rel}")
    try:
        # `on:` parses as the boolean True under YAML 1.1; that is harmless here
        # because only `env:` blocks are read.
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        fail(EXIT_SPEC_INVALID, "preregistration_env", f"cycle workflow is not valid YAML: {exc}")
    if not isinstance(document, dict):
        fail(EXIT_SPEC_INVALID, "preregistration_env", "cycle workflow did not parse to a mapping")
    merged: dict = {}
    top = document.get("env")
    if isinstance(top, dict):
        merged.update({str(k): v for k, v in top.items()})
    if job:
        jobs = document.get("jobs")
        if not isinstance(jobs, dict) or job not in jobs:
            fail(EXIT_SPEC_INVALID, "preregistration_env", f"cycle workflow has no job {job!r}")
        job_env = jobs[job].get("env") if isinstance(jobs[job], dict) else None
        if isinstance(job_env, dict):
            merged.update({str(k): v for k, v in job_env.items()})
    return merged


def coerce(value):
    """Normalize workflow-env strings and JSON scalars to a comparable form."""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    try:
        return float(text)
    except ValueError:
        return text


def check_preregistration_env(spec: dict, root: Path, prereg: dict) -> dict:
    section = spec_get(spec, "cycle_env", dict)
    workflow_rel = section.get("workflow_path")
    if not isinstance(workflow_rel, str):
        fail(EXIT_SPEC_INVALID, "preregistration_env", "cycle_env.workflow_path is required")
    bindings = section.get("bindings")
    if not isinstance(bindings, dict) or not bindings:
        fail(
            EXIT_SPEC_INVALID,
            "preregistration_env",
            "cycle_env.bindings must map workflow env names to preregistration pointers",
        )
    workflow_env = load_workflow_env(root, workflow_rel, section.get("job"))

    invariants = section.get("preregistration_invariants") or {}
    if not isinstance(invariants, dict):
        fail(EXIT_SPEC_INVALID, "preregistration_env", "preregistration_invariants must be an object")
    for label, rule in sorted(invariants.items()):
        if not isinstance(rule, dict) or not isinstance(rule.get("pointer"), list) or "equals" not in rule:
            fail(
                EXIT_SPEC_INVALID,
                "preregistration_env",
                f"preregistration invariant {label} needs a pointer list and an equals value",
            )
        actual = resolve_pointer(prereg, rule["pointer"], "preregistration_invariants")
        if actual != rule["equals"]:
            fail(
                EXIT_PREREGISTRATION_ENV_MISMATCH,
                "preregistration_env",
                f"preregistration invariant {label} is {actual!r}, expected {rule['equals']!r}",
                invariant=label,
                expected=rule["equals"],
                observed=actual,
            )

    checked = {}
    for name, pointer in sorted(bindings.items()):
        if not isinstance(pointer, list):
            fail(EXIT_SPEC_INVALID, "preregistration_env", f"pointer for {name} must be a list")
        expected = resolve_pointer(prereg, pointer, "cycle_env.bindings")
        if name not in workflow_env:
            fail(
                EXIT_PREREGISTRATION_ENV_MISMATCH,
                "preregistration_env",
                f"cycle workflow does not set {name}, which the preregistration binds",
                env_name=name,
                expected=expected,
            )
        actual = workflow_env[name]
        if coerce(actual) != coerce(expected):
            fail(
                EXIT_PREREGISTRATION_ENV_MISMATCH,
                "preregistration_env",
                f"cycle workflow {name}={actual!r} disagrees with the preregistration value {expected!r}",
                env_name=name,
                expected=expected,
                observed=actual,
            )
        # When the same variable is present in this process, it must agree too.
        process_value = os.environ.get(name)
        if process_value is not None and coerce(process_value) != coerce(expected):
            fail(
                EXIT_PREREGISTRATION_ENV_MISMATCH,
                "preregistration_env",
                f"runtime environment {name}={process_value!r} disagrees with the preregistration value {expected!r}",
                env_name=name,
                expected=expected,
                observed=process_value,
            )
        checked[name] = actual
    return {"workflow": workflow_rel, "env": checked, "invariants": sorted(invariants)}


# --------------------------------------------------------------------------
# 6. manifest reference set
# --------------------------------------------------------------------------


def collect_manifest_paths(node, out: set) -> None:
    if isinstance(node, dict):
        for value in node.values():
            collect_manifest_paths(value, out)
    elif isinstance(node, list):
        for value in node:
            collect_manifest_paths(value, out)
    elif isinstance(node, str):
        candidate = node.strip()
        if candidate.startswith("architect/") and "\n" not in candidate:
            out.add(candidate)


def check_manifest_references(spec: dict, root: Path) -> dict:
    section = spec.get("manifest_references")
    if section is None:
        return {"skipped": True}
    if not isinstance(section, dict):
        fail(EXIT_SPEC_INVALID, "manifest_references", "manifest_references must be an object")

    required = section.get("required_paths") or []
    if not isinstance(required, list):
        fail(EXIT_SPEC_INVALID, "manifest_references", "manifest_references.required_paths must be a list")
    referenced = set(str(x) for x in required)

    manifest_rel = section.get("manifest_path")
    manifest_scanned = False
    if isinstance(manifest_rel, str) and (root / manifest_rel).is_file():
        try:
            manifest = json.loads((root / manifest_rel).read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(
                EXIT_MANIFEST_REFERENCE_MISSING,
                "manifest_references",
                f"manifest is not valid JSON: {exc}",
                manifest=manifest_rel,
            )
        collect_manifest_paths(manifest, referenced)
        referenced.add(manifest_rel)
        manifest_scanned = True

    if not referenced:
        fail(
            EXIT_SPEC_INVALID,
            "manifest_references",
            "manifest_references declares no paths and no manifest was available to scan",
        )
    missing = sorted(rel for rel in referenced if not (root / rel).exists())
    if missing:
        fail(
            EXIT_MANIFEST_REFERENCE_MISSING,
            "manifest_references",
            f"{len(missing)} referenced path(s) do not exist: {', '.join(missing[:5])}",
            missing=missing,
        )
    return {"checked": len(referenced), "manifest_scanned": manifest_scanned}


# --------------------------------------------------------------------------
# 7. pacing
# --------------------------------------------------------------------------


def check_pacing(spec: dict, root: Path, prereg: dict) -> dict:
    section = spec_get(spec, "pacing", dict)
    pointer = section.get("preregistration_pointer")
    if not isinstance(pointer, list) or not pointer:
        fail(EXIT_SPEC_INVALID, "pacing", "pacing.preregistration_pointer must be a non-empty list")
    # A preregistration that declares no pacing policy at all is the Sales r7
    # class: the cycle went to the provider with no request spacing and was
    # stopped by an RPM quota. That is a pacing defect, not a spec defect.
    declared = prereg
    for part in pointer:
        if not isinstance(declared, dict) or part not in declared:
            fail(
                EXIT_PACING_CONFIG_INVALID,
                "pacing",
                "preregistration declares no minimum request interval at "
                + "/".join(str(x) for x in pointer),
                pointer=pointer,
            )
        declared = declared[part]
    try:
        declared_seconds = float(declared)
    except (TypeError, ValueError):
        fail(
            EXIT_PACING_CONFIG_INVALID,
            "pacing",
            f"preregistered minimum request interval is not numeric: {declared!r}",
        )
    if declared_seconds <= 0:
        fail(
            EXIT_PACING_CONFIG_INVALID,
            "pacing",
            f"preregistered minimum request interval must be greater than zero, got {declared_seconds}",
            declared=declared_seconds,
        )

    env_name = section.get("min_interval_env")
    if not isinstance(env_name, str) or not env_name:
        fail(EXIT_SPEC_INVALID, "pacing", "pacing.min_interval_env is required")
    workflow_rel = section.get("workflow_path")
    if not isinstance(workflow_rel, str):
        fail(EXIT_SPEC_INVALID, "pacing", "pacing.workflow_path is required")
    workflow_env = load_workflow_env(root, workflow_rel, section.get("job"))

    if env_name not in workflow_env:
        fail(
            EXIT_PACING_CONFIG_INVALID,
            "pacing",
            f"cycle workflow does not set the pacing interval variable {env_name}",
            env_name=env_name,
            declared=declared_seconds,
        )
    raw = str(workflow_env[env_name]).strip()
    if not raw:
        fail(EXIT_PACING_CONFIG_INVALID, "pacing", f"{env_name} is set but empty", env_name=env_name)
    try:
        configured = float(raw)
    except ValueError:
        fail(EXIT_PACING_CONFIG_INVALID, "pacing", f"{env_name}={raw!r} is not numeric", env_name=env_name)
    if configured <= 0:
        fail(
            EXIT_PACING_CONFIG_INVALID,
            "pacing",
            f"{env_name}={configured} disables pacing; a non-zero minimum interval is required",
            env_name=env_name,
            observed=configured,
        )
    if configured != declared_seconds:
        fail(
            EXIT_PACING_CONFIG_INVALID,
            "pacing",
            f"{env_name}={configured} disagrees with the preregistered interval {declared_seconds}",
            env_name=env_name,
            observed=configured,
            declared=declared_seconds,
        )

    pace_file_env = section.get("pace_file_env")
    if isinstance(pace_file_env, str) and pace_file_env:
        value = str(workflow_env.get(pace_file_env, "")).strip()
        if not value:
            fail(
                EXIT_PACING_CONFIG_INVALID,
                "pacing",
                f"cycle workflow does not set the pacing state file variable {pace_file_env}",
                env_name=pace_file_env,
            )
    return {"minimum_seconds_between_requests": configured}


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------


def load_json(path: Path, what: str) -> dict:
    if not path.is_file():
        fail(EXIT_SPEC_INVALID, "spec", f"{what} is missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(EXIT_SPEC_INVALID, "spec", f"{what} is not valid JSON: {exc}")
    if not isinstance(data, dict):
        fail(EXIT_SPEC_INVALID, "spec", f"{what} must be a JSON object")
    return data


def run(spec_path: Path, root: Path, only: tuple) -> dict:
    spec = load_json(spec_path, "preflight spec")
    if spec.get("spec_version") != 1:
        fail(EXIT_SPEC_INVALID, "spec", "preflight spec must declare spec_version=1")
    prereg_rel = spec_get(spec, "preregistration_path", str)
    prereg = load_json(root / prereg_rel, "preregistration")

    cycle_id = spec.get("cycle_id")
    if not isinstance(cycle_id, str) or not cycle_id:
        fail(EXIT_SPEC_INVALID, "spec", "preflight spec must declare a cycle_id")
    if prereg.get("cycle_id") != cycle_id:
        fail(
            EXIT_PREREGISTRATION_ENV_MISMATCH,
            "preregistration_env",
            f"preregistration cycle_id {prereg.get('cycle_id')!r} differs from spec cycle_id {cycle_id!r}",
            expected=cycle_id,
            observed=prereg.get("cycle_id"),
        )

    results = {}
    for check in CHECK_ORDER:
        if check not in only:
            continue
        if check == "compile":
            results[check] = check_compile(spec, root)
        elif check == "sealed_runner_chain":
            results[check] = check_sealed_runner_chain(spec, root)
        elif check == "contract_handshake":
            results[check] = check_contract_handshake(spec, root, prereg)
        elif check == "preregistration_env":
            results[check] = check_preregistration_env(spec, root, prereg)
        elif check == "manifest_references":
            results[check] = check_manifest_references(spec, root)
        elif check == "pacing":
            results[check] = check_pacing(spec, root, prereg)
    return {"cycle_id": cycle_id, "checks": results}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--spec", required=True, help="path to the cycle preflight spec JSON")
    parser.add_argument("--repo-root", default=".", help="repository root the spec paths are relative to")
    parser.add_argument(
        "--only",
        action="append",
        choices=CHECK_ORDER,
        help="run only the named check (repeatable); default runs all checks in order",
    )
    args = parser.parse_args(argv)
    only = tuple(args.only) if args.only else CHECK_ORDER

    try:
        payload = run(Path(args.spec), Path(args.repo_root).resolve(), only)
    except PreflightFailure as exc:
        print(
            json.dumps(
                {
                    "status": "FAIL",
                    "check": exc.check,
                    "failure_class": FAILURE_CLASS[exc.code],
                    "exit_code": exc.code,
                    "message": str(exc),
                    **exc.detail,
                },
                sort_keys=True,
            )
        )
        return exc.code
    except Exception as exc:  # noqa: BLE001 - deliberate catch-all with its own class
        print(
            json.dumps(
                {
                    "status": "FAIL",
                    "check": "preflight",
                    "failure_class": FAILURE_CLASS[EXIT_INTERNAL_ERROR],
                    "exit_code": EXIT_INTERNAL_ERROR,
                    "message": f"{type(exc).__name__}: {exc}",
                },
                sort_keys=True,
            )
        )
        return EXIT_INTERNAL_ERROR
    payload.update({"status": "PASS", "exit_code": EXIT_PASS, "provider_calls": 0, "sealed_pack_reads": 0})
    print(json.dumps(payload, sort_keys=True))
    return EXIT_PASS


if __name__ == "__main__":
    raise SystemExit(main())
