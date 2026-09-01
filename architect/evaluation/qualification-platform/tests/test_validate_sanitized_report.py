import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "validate_sanitized_report.py"
spec = importlib.util.spec_from_file_location("validate_sanitized_report", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

FAMILIES = ["OWN", "LIFE", "MIX", "SEC", "FACT", "INTENT", "OBJ", "NEXT", "FUP", "STATE", "ID", "OPS"]
PREREG = {
    "fixture_count": 36,
    "per_family": 3,
    "families": FAMILIES,
}

R6_PREREG = {
    **PREREG,
    "fixture_design": {
        "repeated_fixture_slots": [
            "OWN-boundary",
            "SEC-injection",
            "FACT-conflict",
            "STATE-supersession",
            "ID-privacy",
            "OPS-operational-verification",
        ],
        "expected_candidate_runs_if_full": 42,
    },
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


def r6_report(attempted=42):
    repeated = {"OWN", "SEC", "FACT", "STATE", "ID", "OPS"}
    family_level = {}
    for family in FAMILIES:
        trials = 4 if family in repeated else 3
        family_level[family] = {
            "tasks_passed": 3,
            "tasks_total": 3,
            "trials_attempted": trials,
            "trials_passed": trials,
        }
    family_level["LIFE"]["tasks_passed"] = 2
    family_level["LIFE"]["trials_passed"] = 2
    return {
        "cycle_id": "sales-0.5-fresh-independent-2026-08-31-r6-gemini-groq",
        "execution_status": "COMPLETED",
        "attempted": attempted,
        "passed": 41 if attempted == 42 else attempted,
        "critical_hard_fails": [],
        "family_level_aggregate": family_level,
        "verdict": "PASS",
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
    assert module.completeness_status(report(17), PREREG) == "TRUNCATED"


def test_real_r10_run_32636679740_is_rejected():
    assert module.completeness_status(report(30), PREREG) == "TRUNCATED"


def test_current_runner_tasks_total_schema_is_accepted():
    assert module.completeness_status(r6_report(), R6_PREREG) == "COMPLETE"


def test_repeat_aware_prereg_requires_all_42_trials_to_be_attempted():
    assert module.completeness_status(r6_report(attempted=41), R6_PREREG) == "TRUNCATED"


def test_repeat_family_requires_its_fourth_trial_attempt():
    value = r6_report()
    value["family_level_aggregate"]["OPS"]["trials_attempted"] = 3
    assert module.completeness_status(value, R6_PREREG) == "TRUNCATED"
