import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "validate_sanitized_report.py"
spec = importlib.util.spec_from_file_location("validate_sanitized_report", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

PREREG = {
    "fixture_count": 36,
    "per_family": 3,
    "families": ["OWN", "LIFE", "MIX", "SEC", "FACT", "INTENT", "OBJ", "NEXT", "FUP", "STATE", "ID", "OPS"],
}


def report(tasks_attempted, family_attempted=None, execution_status="COMPLETED", verdict="REVISE"):
    family_attempted = family_attempted or {f: 3 for f in PREREG["families"]}
    return {
        "cycle_id": "sales-0.3-fresh-independent-2026-08-23-r10-gemini-paced",
        "execution_status": execution_status,
        "attempted": tasks_attempted,
        "verdict": verdict,
        "family_level_aggregate": {
            f: {"tasks_passed": 0, "tasks_total": 3, "attempted": n, "trials_attempted": n, "trials_passed": 0}
            for f, n in family_attempted.items()
        },
    }


def test_tasks_attempted_below_prereg_is_truncated():
    assert module.completeness_status(report(35), PREREG) == "TRUNCATED"


def test_family_attempted_below_per_family_is_truncated():
    families = {f: 3 for f in PREREG["families"]}
    families["OPS"] = 2
    assert module.completeness_status(report(36, families), PREREG) == "TRUNCATED"


def test_completed_with_incomplete_family_counter_is_truncated():
    families = {f: 3 for f in PREREG["families"]}
    families["OPS"] = 2
    assert module.completeness_status(report(36, families, execution_status="completed"), PREREG) == "TRUNCATED"


def test_complete_run_is_complete():
    assert module.completeness_status(report(36, execution_status="COMPLETED"), PREREG) == "COMPLETE"


def test_complete_revise_run_remains_a_valid_qualification_outcome():
    complete = report(36, execution_status="COMPLETED", verdict="REVISE")
    assert module.completeness_status(complete, PREREG) == "COMPLETE"
    assert complete["verdict"] == "REVISE"


def test_complete_pass_run_remains_a_valid_qualification_outcome():
    complete = report(36, execution_status="COMPLETED", verdict="PASS")
    assert module.completeness_status(complete, PREREG) == "COMPLETE"
    assert complete["verdict"] == "PASS"


def test_real_r10_run_32636661187_is_rejected():
    # Observed report: 17/36 tasks attempted.
    assert module.completeness_status(report(17), PREREG) == "TRUNCATED"


def test_real_r10_run_32636679740_is_rejected():
    # Observed report: 30/36 tasks attempted.
    assert module.completeness_status(report(30), PREREG) == "TRUNCATED"
