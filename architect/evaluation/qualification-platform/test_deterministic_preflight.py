#!/usr/bin/env python3
"""Regression suite for the deterministic qualification preflight.

Every case below is an infrastructure defect that really happened in the Sales
0.3 held-out chain and really burned a round on the same unchanged candidate
(commit 5adc0d31, digest sha256:a33bae7c...). Each one must fail the preflight
with its own exit code, and the repaired form of the same chain must pass.

Provenance is taken from the evaluator's own preregistration records, which name
the failing round and the round that repaired it:

  packaging / pack-root resolution
      exhibited by r6, repaired in r7
      ("deterministic packaging path normalization only")
      -> exit 13 PACK_ROOT_UNRESOLVED

  provider quota / missing pacing
      exhibited by r7, repaired in r8
      ("r7 ... stopped at unscored canary on provider RPM quota")
      -> exit 17 PACING_CONFIG_INVALID

  qualification-contract handshake
      exhibited by r8, repaired in r9
      ("qualification contract handshake compatibility only")
      -> exit 14 CONTRACT_HANDSHAKE_MISMATCH

  sealed-runner import path
      exhibited by r9, repaired in r10
      ("runner failed before fixture loading because a public paced helper
        module was outside import path")
      -> exit 12 SEALED_RUNNER_IMPORT_UNRESOLVED

None of these cases opens a sealed pack and none of them makes a provider call.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
PREFLIGHT = HERE / "deterministic_preflight.py"

SALES = "architect/evaluation/sales-lead-conversion"
R10_SPEC = f"{SALES}/preflight/sales-0_3-r10-gemini.json"

BASE_WRAPPER = f"{SALES}/sealed_runner_provider_wrapper_v0_3_gemini.py"
TEMPLATE = f"{SALES}/sealed_runner_template_v0_3_r2.py"


def run_preflight(spec: Path, only: list[str] | None = None) -> tuple[int, dict]:
    argv = [sys.executable, str(PREFLIGHT), "--spec", str(spec), "--repo-root", str(ROOT)]
    for check in only or []:
        argv += ["--only", check]
    proc = subprocess.run(argv, cwd=str(ROOT), text=True, capture_output=True, timeout=300)
    try:
        report = json.loads(proc.stdout.strip().splitlines()[-1])
    except (IndexError, json.JSONDecodeError):
        raise AssertionError(f"preflight produced no report\nstdout={proc.stdout}\nstderr={proc.stderr}")
    return proc.returncode, report


def write_spec(directory: Path, name: str, spec: dict) -> Path:
    path = directory / name
    path.write_text(json.dumps(spec, indent=2) + "\n")
    return path


def chain_spec(cycle_id: str, prereg: str, runner: str, chain: list[str]) -> dict:
    return {
        "spec_version": 1,
        "cycle_id": cycle_id,
        "preregistration_path": prereg,
        "compile_paths": [BASE_WRAPPER],
        "sealed_runner": {"runner_path": runner, "loader_chain": chain, "probe_timeout_seconds": 120},
    }


# --------------------------------------------------------------------------
# Repaired baseline: the r10 spec as committed must pass every check.
# --------------------------------------------------------------------------


def test_repaired_r10_passes() -> None:
    code, report = run_preflight(ROOT / R10_SPEC)
    assert code == 0, f"repaired r10 preflight must pass, got {code}: {report}"
    assert report["status"] == "PASS", report
    assert report["provider_calls"] == 0, report
    assert report["sealed_pack_reads"] == 0, report
    assert set(report["checks"]) == {
        "compile",
        "sealed_runner_chain",
        "contract_handshake",
        "preregistration_env",
        "manifest_references",
        "pacing",
    }, report["checks"]


# --------------------------------------------------------------------------
# r6 -> r7: packaging / pack-root resolution, exit 13
# --------------------------------------------------------------------------

# The r7 repair is one line: the sealed runner rebinds the loaded wrapper's
# __file__ to the extracted pack runner, so the terminal template resolves
# `Path(__file__).resolve().parent` inside the pack. Without it the chain looks
# for its pack data in the evaluator source tree instead.
R7_REPAIRED_RUNNER = """#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

BASE = Path({base!r})

def main():
    spec = importlib.util.spec_from_file_location('packaging_regression_base', BASE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.CYCLE_ID = 'packaging-regression'
    m.__file__ = str(Path(__file__).resolve())
    return int(m.main())

if __name__ == '__main__':
    raise SystemExit(main())
"""

R6_DEFECTIVE_RUNNER = R7_REPAIRED_RUNNER.replace(
    "    m.__file__ = str(Path(__file__).resolve())\n", ""
)


def test_r6_packaging_pack_root_unresolved() -> None:
    r6_wrapper = f"{SALES}/sealed_runner_provider_wrapper_v0_3_gemini_r6.py"
    chain_tail = [r6_wrapper, BASE_WRAPPER, TEMPLATE]
    with tempfile.TemporaryDirectory(prefix="preflight-r6-regression-") as td:
        work = Path(td)
        base_abs = str(ROOT / r6_wrapper)

        defective = work / "defective_runner.py"
        defective.write_text(R6_DEFECTIVE_RUNNER.format(base=base_abs))
        spec = write_spec(
            work,
            "r6.json",
            chain_spec(
                "sales-0.3-fresh-independent-2026-08-23-r6-gemini",
                f"{SALES}/qualification-preregistration-v0_3-r6-gemini.json",
                str(defective),
                [str(defective), *chain_tail],
            ),
        )
        code, report = run_preflight(spec, ["sealed_runner_chain"])
        assert code == 13, f"r6 packaging defect must exit 13, got {code}: {report}"
        assert report["failure_class"] == "PACK_ROOT_UNRESOLVED", report
        assert "outside the sealed pack" in report["message"], report

        repaired = work / "repaired_runner.py"
        repaired.write_text(R7_REPAIRED_RUNNER.format(base=base_abs))
        spec = write_spec(
            work,
            "r7.json",
            chain_spec(
                "sales-0.3-fresh-independent-2026-08-23-r6-gemini",
                f"{SALES}/qualification-preregistration-v0_3-r6-gemini.json",
                str(repaired),
                [str(repaired), *chain_tail],
            ),
        )
        code, report = run_preflight(spec, ["sealed_runner_chain"])
        assert code == 0, f"the r7 packaging repair must pass, got {code}: {report}"


# --------------------------------------------------------------------------
# r7 -> r8: provider quota / missing pacing, exit 17
# --------------------------------------------------------------------------


def pacing_spec(cycle_id: str, prereg: str, workflow: str) -> dict:
    return {
        "spec_version": 1,
        "cycle_id": cycle_id,
        "preregistration_path": prereg,
        "compile_paths": [BASE_WRAPPER],
        "pacing": {
            "workflow_path": workflow,
            "job": "qualify",
            "min_interval_env": "GEMINI_MIN_INTERVAL_SECONDS",
            "pace_file_env": "GEMINI_PACE_FILE",
            "preregistration_pointer": ["runtime_contract", "minimum_seconds_between_requests"],
        },
    }


def test_r7_provider_quota_pacing_invalid() -> None:
    with tempfile.TemporaryDirectory(prefix="preflight-r7-regression-") as td:
        work = Path(td)

        # r7 as it actually ran: neither the preregistration nor the workflow
        # declared any request spacing, so the cycle walked into the provider
        # RPM quota at the unscored canary.
        spec = write_spec(
            work,
            "r7.json",
            pacing_spec(
                "sales-0.3-fresh-independent-2026-08-23-r7-gemini",
                f"{SALES}/qualification-preregistration-v0_3-r7-gemini.json",
                ".github/workflows/sales-0-3-gemini-r7.yml",
            ),
        )
        code, report = run_preflight(spec, ["pacing"])
        assert code == 17, f"r7 unpaced cycle must exit 17, got {code}: {report}"
        assert report["failure_class"] == "PACING_CONFIG_INVALID", report
        assert "no minimum request interval" in report["message"], report

        # The r8 repair: a preregistered, non-zero interval mirrored by the
        # cycle workflow env.
        spec = write_spec(
            work,
            "r8.json",
            {
                "spec_version": 1,
                "cycle_id": "sales-0.3-fresh-independent-2026-08-23-r8-gemini-paced",
                "preregistration_path": f"{SALES}/qualification-preregistration-v0_3-r8-gemini.json",
                "compile_paths": [BASE_WRAPPER],
                "pacing": {
                    "workflow_path": ".github/workflows/sales-0-3-gemini-r8.yml",
                    "job": "qualify",
                    "min_interval_env": "GEMINI_MIN_INTERVAL_SECONDS",
                    "pace_file_env": "GEMINI_PACE_FILE",
                    "preregistration_pointer": [
                        "runtime_contract",
                        "project_quota_pacing",
                        "minimum_seconds_between_requests",
                    ],
                },
            },
        )
        code, report = run_preflight(spec, ["pacing"])
        assert code == 0, f"the r8 pacing repair must pass, got {code}: {report}"
        assert report["checks"]["pacing"]["minimum_seconds_between_requests"] == 6.0, report

        # A pacing variable that is present but zero is still an unpaced cycle.
        zero_workflow = work / "zero-pace.yml"
        zero_workflow.write_text(
            "name: zero pace\n"
            "on:\n  workflow_dispatch:\n"
            "env:\n"
            "  GEMINI_MIN_INTERVAL_SECONDS: '0'\n"
            "  GEMINI_PACE_FILE: /tmp/pace\n"
            "jobs:\n  qualify:\n    runs-on: ubuntu-latest\n    steps:\n      - run: 'true'\n"
        )
        spec = write_spec(
            work,
            "zero.json",
            pacing_spec(
                "sales-0.3-fresh-independent-2026-08-23-r10-gemini-paced",
                f"{SALES}/qualification-preregistration-v0_3-r10-gemini.json",
                str(zero_workflow),
            ),
        )
        code, report = run_preflight(spec, ["pacing"])
        assert code == 17, f"zero pacing interval must exit 17, got {code}: {report}"
        assert "disables pacing" in report["message"], report


# --------------------------------------------------------------------------
# r8 -> r9: qualification-contract handshake, exit 14
# --------------------------------------------------------------------------


def contract_spec(cycle_id: str, prereg: str, executor: str) -> dict:
    return {
        "spec_version": 1,
        "cycle_id": cycle_id,
        "preregistration_path": prereg,
        "compile_paths": [executor],
        "contract": {
            "probe_argv": [sys.executable, executor, "--qualification-contract"],
            "credential_env": "GEMINI_API_KEY",
            "probe_timeout_seconds": 120,
            "preregistration_bindings": {
                "contract_version": ["runtime_contract", "qualification_contract_version"],
                "provider": ["runtime_contract", "provider"],
            },
        },
    }


def test_r8_contract_handshake_mismatch() -> None:
    r9_prereg = f"{SALES}/qualification-preregistration-v0_3-r9-gemini.json"
    with tempfile.TemporaryDirectory(prefix="preflight-r8-regression-") as td:
        work = Path(td)

        # r8 bound the raw executor, which announces contract_version 2 while
        # the qualification contract the platform enforces is version 1.
        spec = write_spec(
            work,
            "r8.json",
            contract_spec(
                "sales-0.3-fresh-independent-2026-08-23-r9-gemini-paced",
                r9_prereg,
                f"{SALES}/executor_v0_3_gemini.py",
            ),
        )
        code, report = run_preflight(spec, ["contract_handshake"])
        assert code == 14, f"r8 contract handshake defect must exit 14, got {code}: {report}"
        assert report["failure_class"] == "CONTRACT_HANDSHAKE_MISMATCH", report
        assert report["key"] == "contract_version", report
        assert report["expected"] == 1 and report["observed"] == 2, report

        # The r9 repair: a contract-v1 shim in front of the same executor.
        spec = write_spec(
            work,
            "r9.json",
            contract_spec(
                "sales-0.3-fresh-independent-2026-08-23-r9-gemini-paced",
                r9_prereg,
                f"{SALES}/executor_v0_3_gemini_contract_v1.py",
            ),
        )
        code, report = run_preflight(spec, ["contract_handshake"])
        assert code == 0, f"the r9 handshake repair must pass, got {code}: {report}"
        assert report["checks"]["contract_handshake"]["contract"]["provider"] == "gemini-interactions-api", report


# --------------------------------------------------------------------------
# r9 -> r10: sealed-runner import path, exit 12
# --------------------------------------------------------------------------


def test_r9_sealed_runner_import_unresolved() -> None:
    chain_tail = [
        f"{SALES}/sealed_runner_provider_wrapper_v0_3_gemini_r8.py",
        BASE_WRAPPER,
        TEMPLATE,
    ]
    with tempfile.TemporaryDirectory(prefix="preflight-r9-regression-") as td:
        work = Path(td)

        # r9's sealed runner is syntactically valid and cold-starts cleanly: the
        # defect only appears one module deeper, where the r8 wrapper imports a
        # public paced helper that is not on the pack's import path.
        r9_runner = f"{SALES}/sealed_runner_provider_wrapper_v0_3_gemini_r9.py"
        spec = write_spec(
            work,
            "r9.json",
            chain_spec(
                "sales-0.3-fresh-independent-2026-08-23-r9-gemini-paced",
                f"{SALES}/qualification-preregistration-v0_3-r9-gemini.json",
                r9_runner,
                [r9_runner, *chain_tail],
            ),
        )
        code, report = run_preflight(spec, ["sealed_runner_chain"])
        assert code == 12, f"r9 import-path defect must exit 12, got {code}: {report}"
        assert report["failure_class"] == "SEALED_RUNNER_IMPORT_UNRESOLVED", report
        assert report["missing_module"] == "gemini_rate_limiter", report

        # The r10 repair: the runner puts its own evaluator directory on the
        # import path before loading the rest of the chain.
        r10_runner = f"{SALES}/sealed_runner_provider_wrapper_v0_3_gemini_r10.py"
        spec = write_spec(
            work,
            "r10.json",
            chain_spec(
                "sales-0.3-fresh-independent-2026-08-23-r10-gemini-paced",
                f"{SALES}/qualification-preregistration-v0_3-r10-gemini.json",
                r10_runner,
                [r10_runner, *chain_tail],
            ),
        )
        code, report = run_preflight(spec, ["sealed_runner_chain"])
        assert code == 0, f"the r10 import-path repair must pass, got {code}: {report}"


# --------------------------------------------------------------------------
# Remaining failure classes keep their own exit codes.
# --------------------------------------------------------------------------


def test_compile_and_reference_and_spec_classes() -> None:
    with tempfile.TemporaryDirectory(prefix="preflight-classes-") as td:
        work = Path(td)

        broken = work / "broken.py"
        broken.write_text("def main(:\n    return 0\n")
        spec = write_spec(
            work,
            "compile.json",
            {
                "spec_version": 1,
                "cycle_id": "sales-0.3-fresh-independent-2026-08-23-r10-gemini-paced",
                "preregistration_path": f"{SALES}/qualification-preregistration-v0_3-r10-gemini.json",
                "compile_paths": [str(broken)],
            },
        )
        code, report = run_preflight(spec, ["compile"])
        assert code == 11 and report["failure_class"] == "COMPILE_FAILED", report

        spec = write_spec(
            work,
            "refs.json",
            {
                "spec_version": 1,
                "cycle_id": "sales-0.3-fresh-independent-2026-08-23-r10-gemini-paced",
                "preregistration_path": f"{SALES}/qualification-preregistration-v0_3-r10-gemini.json",
                "compile_paths": [BASE_WRAPPER],
                "manifest_references": {"required_paths": [f"{SALES}/does_not_exist.py"]},
            },
        )
        code, report = run_preflight(spec, ["manifest_references"])
        assert code == 16 and report["failure_class"] == "MANIFEST_REFERENCE_MISSING", report

        spec = write_spec(work, "spec.json", {"spec_version": 99})
        code, report = run_preflight(spec, ["compile"])
        assert code == 10 and report["failure_class"] == "PREFLIGHT_SPEC_INVALID", report

        # A cycle whose workflow env contradicts its preregistration.
        drifted = work / "drift.yml"
        drifted.write_text(
            "name: drifted\n"
            "on:\n  workflow_dispatch:\n"
            "env:\n"
            "  CYCLE_ID: sales-0.3-fresh-independent-2026-08-23-r10-gemini-paced\n"
            "  QUALIFICATION_RELEASE_TASKS_PASSED_MIN: '30'\n"
            "jobs:\n  qualify:\n    runs-on: ubuntu-latest\n    steps:\n      - run: 'true'\n"
        )
        spec = write_spec(
            work,
            "env.json",
            {
                "spec_version": 1,
                "cycle_id": "sales-0.3-fresh-independent-2026-08-23-r10-gemini-paced",
                "preregistration_path": f"{SALES}/qualification-preregistration-v0_3-r10-gemini.json",
                "compile_paths": [BASE_WRAPPER],
                "cycle_env": {
                    "workflow_path": str(drifted),
                    "job": "qualify",
                    "bindings": {
                        "CYCLE_ID": ["cycle_id"],
                        "QUALIFICATION_RELEASE_TASKS_PASSED_MIN": ["thresholds", "release_tasks_passed_min"],
                    },
                },
            },
        )
        code, report = run_preflight(spec, ["preregistration_env"])
        assert code == 15 and report["failure_class"] == "PREREGISTRATION_ENV_MISMATCH", report
        assert report["observed"] == "30" and report["expected"] == 34, report


TESTS = (
    test_repaired_r10_passes,
    test_r6_packaging_pack_root_unresolved,
    test_r7_provider_quota_pacing_invalid,
    test_r8_contract_handshake_mismatch,
    test_r9_sealed_runner_import_unresolved,
    test_compile_and_reference_and_spec_classes,
)


def main() -> int:
    for test in TESTS:
        test()
        print(f"  ok {test.__name__}")
    print("DETERMINISTIC_PREFLIGHT_REGRESSION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
