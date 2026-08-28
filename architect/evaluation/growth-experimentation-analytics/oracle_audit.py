#!/usr/bin/env python3
"""Architect-level audit of the Analytics qualification oracle and harness.

Three consecutive gates (v0.4, v0.5, v0.6) failed on the instrument rather than the candidate.
This audits the instrument itself. It makes no provider calls and does not touch the candidate.

Checks are grouped as the audit brief asks:

  F  fixture completeness
  T  action -> target combinations
  U  units and normalization
  C  oracle consistency
  D  deterministic grading

Each check yields zero or more findings. A finding names the rule, the affected object, and
what a reader would have to know to judge it. Run as a CLI to print them.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import random
import re
from pathlib import Path
from typing import Any, Callable, Iterable

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

RATIO_LIKE = re.compile(r"(ratio|lift|rate|share|pct|percent|proportion|margin)", re.I)


def metric_token(name: str, arms: Iterable[str]) -> str:
    """Strip arm identifiers before testing a computation name.

    Without this, "net_return_configuration_b" matches the ratio pattern, because
    "configuration" contains "ratio". The audit must not manufacture its own false positives.
    """
    stripped = name
    for arm in sorted(arms, key=len, reverse=True):
        stripped = stripped.replace(arm, "")
    return stripped


# Actions differ in what they can sensibly be aimed at.
EXPERIMENT_SCOPED = {"INCONCLUSIVE", "CONTINUE"}
ARM_SCOPED = {"KILL", "SCALE"}


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class Finding:
    def __init__(self, rule: str, severity: str, subject: str, detail: str):
        self.rule, self.severity, self.subject, self.detail = rule, severity, subject, detail

    def key(self) -> str:
        return f"{self.rule}|{self.subject}"

    def __repr__(self) -> str:
        return f"[{self.severity}] {self.rule} {self.subject}: {self.detail}"

    def as_dict(self) -> dict[str, str]:
        return {"rule": self.rule, "severity": self.severity, "subject": self.subject, "detail": self.detail}


# ---------------------------------------------------------------------------------------
# A canonical satisfying result, derived from an expectation. Used for satisfiability and
# for the determinism checks. If this cannot be built, the expectation is unsatisfiable.
# ---------------------------------------------------------------------------------------

def build_passing_result(fixture: dict, expectation: dict, scope: str | None = None) -> dict:
    scopes = expectation.get("allowed_scopes") or ["REGISTERED_ESTIMAND"]
    scope = scope or scopes[0]
    bounds = (expectation.get("ceiling_by_scope") or {}).get(scope) \
        or (expectation.get("ceiling_by_scope") or {}).get(scopes[0]) or {}
    ceiling = bounds.get("min") or bounds.get("max") or "DESCRIPTIVE_ASSOCIATION"
    action = expectation["action_in"][0]
    identified = "IDENTIFIED" in expectation.get("causal_status_in", []) or ceiling == "INCREMENTAL_CAUSAL"
    state = expectation.get("scale_state", "BLOCKED")
    reasons = [expectation["scale_reasons_any"][0]] if state == "BLOCKED" and expectation.get("scale_reasons_any") \
        else (["NOT_BLOCKED"] if state == "ELIGIBLE" else ["INSUFFICIENT_SAMPLE"])
    return {
        "fixture_id": fixture["fixture_id"],
        "recommendation": action,
        "decision_record": {
            "causal": {"status": "IDENTIFIED" if identified else "UNRESOLVED",
                       "claim_scope": scope, "claim_ceiling": ceiling,
                       "blocking_confounders": [] if identified else ["design imbalance"]},
            "operational": {"action": action, "target": expectation["target"],
                            "decisive_metric": expectation["decisive_metric_in"][0],
                            "decision_basis": sorted({*expectation.get("basis_required", []), "REVERSIBILITY"}),
                            "reversible": True, "evidence_that_would_change_action": "x"},
            "scale_readiness": {"state": state, "blocking_reasons": reasons},
        },
        "data_integrity_findings": [],
        "computations": [{"name": n, "inputs": {}, "method": "m", "result": v[0], "unit": "u"}
                         for n, v in (expectation.get("computations") or {}).items()],
        "claim_boundaries": [],
        "confounders": [] if identified else [{"name": "design imbalance", "severity": "MATERIAL", "effect": "."}],
        "rationale": ".", "next_action": ".",
    }


# ---------------------------------------------------------------------------------------
# F -- fixture completeness
# ---------------------------------------------------------------------------------------

def check_fixtures(fixtures: dict, expectations: dict, fixture_schema: dict | None) -> list[Finding]:
    findings: list[Finding] = []
    for fid, fixture in fixtures.items():
        case = fixture.get("case", {})
        family = expectations[fid]["family"]

        if fixture_schema is not None:
            try:
                import jsonschema
                errors = list(jsonschema.Draft202012Validator(fixture_schema).iter_errors(fixture))
            except ImportError:
                errors = []
            for err in errors:
                findings.append(Finding("F1-schema", "HIGH", family,
                                        f"case violates the declared fixture contract at "
                                        f"{'.'.join(str(p) for p in err.absolute_path) or '$'}: {err.message}"))

        arms = case.get("arms")
        if not isinstance(arms, list) or not arms:
            findings.append(Finding("F2-arms", "HIGH", family, "case declares no arms"))
        elif expectations[fid].get("target") not in arms:
            findings.append(Finding("F2-arms", "HIGH", family,
                                    f"oracle target {expectations[fid].get('target')!r} is not among the "
                                    f"declared arms {arms}"))

        # A computation the candidate is never asked for cannot be graded fairly.
        instruction = fixture.get("instruction", "")
        for name in (expectations[fid].get("computations") or {}):
            if name not in instruction:
                findings.append(Finding("F3-unrequested-computation", "HIGH", family,
                                        f"oracle asserts computation {name!r} but the candidate-facing "
                                        f"instruction never asks for it"))
    return findings


def check_no_leakage(suite: dict) -> list[Finding]:
    blob = json.dumps(suite).lower()
    findings = []
    for token in ("expectation", "decisive_metric", "ceiling_by_scope", "allowed_scopes",
                  "action_in", "scale_state", "basis_required", "\"trap\""):
        if token in blob:
            findings.append(Finding("F4-leakage", "HIGH", "candidate-facing suite",
                                    f"suite contains oracle token {token!r}"))
    return findings


# ---------------------------------------------------------------------------------------
# T -- action -> target combinations
# ---------------------------------------------------------------------------------------

def check_action_target(expectations: dict) -> list[Finding]:
    findings = []
    for expectation in expectations.values():
        actions = expectation.get("action_in") or []
        if len(actions) > 1 and isinstance(expectation.get("target"), str) \
                and "target_by_action" not in expectation:
            spans = bool(set(actions) & EXPERIMENT_SCOPED) and bool(
                (set(actions) & ARM_SCOPED) or "ITERATE" in actions)
            findings.append(Finding(
                "T1-target-not-action-dependent", "HIGH" if spans else "MEDIUM", expectation["family"],
                f"permits actions {actions} but forces a single target {expectation['target']!r}"
                + (f"; those actions span experiment-scoped and arm-scoped meanings, so a candidate "
                   f"choosing a permitted action can be failed for its natural target"
                   if spans else
                   "; all permitted actions are arm-scoped here, so no divergence is observed yet, "
                   "but the expectation is still under-specified")))
    return findings


# ---------------------------------------------------------------------------------------
# U -- units and normalization
# ---------------------------------------------------------------------------------------

def check_units(expectations: dict, fixtures: dict) -> list[Finding]:
    findings = []
    for fid, expectation in expectations.items():
        arms = fixtures[fid]["case"].get("arms", [])
        for name, spec in (expectation.get("computations") or {}).items():
            value, tol = spec[0], spec[1]
            token = metric_token(name, arms)
            ratio_like = bool(RATIO_LIKE.search(token))
            if len(spec) < 3:
                sev = "HIGH" if ratio_like else "MEDIUM"
                findings.append(Finding("U1-unit-not-pinned", sev, expectation["family"],
                                        f"assertion {name!r} compares a bare number ({value}) with no unit; "
                                        f"the result schema carries a unit field and the assertion ignores it"))
            if ratio_like and value != 0:
                findings.append(Finding("U2-ratio-scale-ambiguity", "HIGH", expectation["family"],
                                        f"{name!r} is ratio-like and expects {value}; the same quantity as a "
                                        f"percentage is {value * 100}, which no assertion excludes"))
            if value and tol and abs(value) > 0 and (tol / abs(value)) < 1e-4:
                findings.append(Finding("U3-tolerance-scale", "LOW", expectation["family"],
                                        f"{name!r} tolerance {tol} is {tol / abs(value):.2e} of the magnitude "
                                        f"{value}; tolerance policy is absolute and therefore uneven across "
                                        f"assertions of different scale"))
    return findings


# ---------------------------------------------------------------------------------------
# C -- oracle consistency
# ---------------------------------------------------------------------------------------

def check_vocabularies(expectations: dict, grader) -> list[Finding]:
    findings = []
    vocab = {
        "decisive_metric_in": getattr(grader, "DECISIVE", set()),
        "causal_status_in": getattr(grader, "CAUSAL_STATUS", set()),
        "action_in": getattr(grader, "ACTIONS", set()),
        "allowed_scopes": getattr(grader, "SCOPES", set()),
    }
    ceilings = set(getattr(grader, "CEILINGS", []))
    for expectation in expectations.values():
        for field, allowed in vocab.items():
            if not allowed:
                continue
            for value in expectation.get(field, []) or []:
                if value not in allowed:
                    findings.append(Finding("C1-unknown-enum", "HIGH", expectation["family"],
                                            f"{field} contains {value!r}, absent from the grader vocabulary"))
        for scope, bounds in (expectation.get("ceiling_by_scope") or {}).items():
            for edge, value in bounds.items():
                if value not in ceilings:
                    findings.append(Finding("C1-unknown-enum", "HIGH", expectation["family"],
                                            f"ceiling_by_scope[{scope}][{edge}] = {value!r} is not a ceiling"))
    return findings


NO_CONFOUNDING = {"none", "none known", "none identified", "none observed", "not identified"}


def visible_identification_facts(case: dict) -> tuple:
    """Normalise the candidate-visible facts that bear on identification.

    Normalisation matters. The v0.5 oracle capped IMMATURE_FIXED_HORIZON below
    CLEAN_SCALABLE_WIN while both were randomized and unconfounded, and the two cases only
    ever differed in the *wording* of the confounding field -- "none known" versus "none
    identified". A key that compared those strings literally would place them in different
    buckets and report no inconsistency, which is how the defect survived to a paid gate.
    """
    design = case.get("design", {})
    raw = str(design.get("confounding", "")).strip().lower()
    if not raw:
        confounding = "UNSTATED"
    elif raw in NO_CONFOUNDING:
        confounding = "ABSENT"
    else:
        confounding = "PRESENT"
    window = case["registered_window_complete"] if "registered_window_complete" in case else "UNDECLARED"
    return (bool(design.get("randomized_split")), confounding, window)


def check_cross_family_consistency(samples: list[tuple[dict, dict]]) -> list[Finding]:
    """Identical candidate-visible identification facts must not map to different constraints."""
    caps: dict[tuple, dict[str, set]] = {}
    for fixtures, expectations in samples:
        for fid, expectation in expectations.items():
            key = visible_identification_facts(fixtures[fid]["case"])
            slot = caps.setdefault(key, {"cap": set(), "scale": set(), "scopes": set(), "families": set()})
            # Read both oracle shapes: v0.6 scopes the cap, v0.5 kept it flat. An audit that
            # only understands the current shape cannot check the history it exists to explain.
            bounds = (expectation.get("ceiling_by_scope") or {}).get("REGISTERED_ESTIMAND", {})
            cap = bounds.get("max", expectation.get("max_claim_ceiling"))
            if cap:
                slot["cap"].add(cap)
            slot["scale"].add(expectation.get("scale_state"))
            slot["scopes"].add(tuple(sorted(expectation.get("allowed_scopes", ["REGISTERED_ESTIMAND"]))))
            slot["families"].add(expectation["family"])
    findings = []
    for key, slot in caps.items():
        if len(slot["cap"]) > 1:
            undeclared = key[2] == "UNDECLARED"
            findings.append(Finding("C2-cap-inconsistency", "HIGH", " / ".join(sorted(slot["families"])),
                                    f"identical visible facts {key} map to different ceiling caps "
                                    f"{sorted(slot['cap'])}"
                                    + ("; the cap therefore varies on a fact the candidate-facing case "
                                       "never declares" if undeclared else "")))
        if len(slot["scopes"]) > 1:
            findings.append(Finding("C3-scope-inconsistency", "MEDIUM", " / ".join(sorted(slot["families"])),
                                    f"identical visible facts {key} offer different scope sets "
                                    f"{sorted(slot['scopes'])}"))
    return findings


def check_satisfiable_and_discriminating(fixtures: dict, expectations: dict, grader) -> list[Finding]:
    findings = []
    for fid, expectation in expectations.items():
        fixture = fixtures[fid]
        for scope in expectation.get("allowed_scopes", ["REGISTERED_ESTIMAND"]):
            try:
                report = grader.grade(build_passing_result(fixture, expectation, scope), fixture, expectation)
            except Exception as exc:
                findings.append(Finding("C4-unsatisfiable", "HIGH", expectation["family"],
                                        f"grading a canonical correct answer raised {exc!r}"))
                continue
            if not report["pass"]:
                findings.append(Finding("C4-unsatisfiable", "HIGH", expectation["family"],
                                        f"no canonical correct answer exists for scope {scope}: "
                                        f"{report['failures']}"))
        # A rule that nothing can violate is not a rule.
        wrong = build_passing_result(fixture, expectation)
        other = [a for a in fixture["case"]["arms"] if a != expectation["target"]]
        if other:
            wrong["decision_record"]["operational"]["target"] = other[0]
            if grader.grade(wrong, fixture, expectation)["pass"]:
                findings.append(Finding("C5-non-discriminating", "HIGH", expectation["family"],
                                        "an action aimed at a different arm still passes"))
    return findings


# ---------------------------------------------------------------------------------------
# D -- deterministic grading
# ---------------------------------------------------------------------------------------

def check_identity_binding(fixtures: dict, expectations: dict, grader) -> list[Finding]:
    """grade() is handed the fixture by the runner; does it verify the result belongs to it?"""
    findings = []
    ids = list(fixtures)
    for fid, expectation in expectations.items():
        impostor = build_passing_result(fixtures[fid], expectation)
        impostor["fixture_id"] = next(other for other in ids if other != fid)
        if grader.grade(impostor, fixtures[fid], expectation)["pass"]:
            findings.append(Finding("C6-identity-unchecked", "MEDIUM", expectation["family"],
                                    "a result carrying another case's fixture_id is graded as a pass; "
                                    "result-to-fixture identity is never verified inside grade()"))
    return findings


def check_determinism(fixtures: dict, expectations: dict, grader) -> list[Finding]:
    findings = []
    rng = random.Random(0)
    for fid, expectation in expectations.items():
        fixture = fixtures[fid]
        base = build_passing_result(fixture, expectation)

        first = grader.grade(copy.deepcopy(base), fixture, expectation)
        second = grader.grade(copy.deepcopy(base), fixture, expectation)
        if first != second:
            findings.append(Finding("D1-impure-grade", "HIGH", expectation["family"],
                                    "grading the same result twice produced different reports"))

        snapshot = copy.deepcopy(base)
        grader.grade(base, fixture, expectation)
        if base != snapshot:
            findings.append(Finding("D3-input-mutation", "HIGH", expectation["family"],
                                    "grade() mutated the result object it was given"))

        # Order of list-valued fields must not change a verdict.
        for _ in range(5):
            shuffled = copy.deepcopy(base)
            op = shuffled["decision_record"]["operational"]
            rng.shuffle(op["decision_basis"])
            rng.shuffle(shuffled["computations"])
            rng.shuffle(shuffled["confounders"])
            rng.shuffle(shuffled["decision_record"]["scale_readiness"]["blocking_reasons"])
            report = grader.grade(shuffled, fixture, expectation)
            if report["pass"] != first["pass"]:
                findings.append(Finding("D2-order-dependence", "HIGH", expectation["family"],
                                        "reordering list-valued fields changed the verdict"))
                break

        # Malformed input must fail closed rather than raise.
        for mutate in (lambda r: r.pop("decision_record"),
                       lambda r: r["decision_record"].pop("causal"),
                       lambda r: r.update({"computations": "not-a-list"}),
                       lambda r: r["decision_record"]["operational"].update({"target": None})):
            broken = copy.deepcopy(base)
            try:
                mutate(broken)
                report = grader.grade(broken, fixture, expectation)
                if report.get("pass"):
                    findings.append(Finding("D4-fails-open", "HIGH", expectation["family"],
                                            "a malformed result was graded as a pass"))
            except Exception as exc:
                findings.append(Finding("D5-crash-on-malformed", "MEDIUM", expectation["family"],
                                        f"grading a malformed result raised {exc!r} instead of failing closed"))
    return findings


# ---------------------------------------------------------------------------------------

def audit(generator, grader, seeds: Iterable[int], per_family: int,
          fixture_schema: dict | None) -> list[Finding]:
    findings: list[Finding] = []
    samples = []
    for seed in seeds:
        suite, oracle = generator.generate(seed, per_family)
        fixtures = {f["fixture_id"]: f for f in suite["fixtures"]}
        expectations = oracle["expectations"]
        samples.append((fixtures, expectations))
        if seed == list(seeds)[0]:
            findings += check_no_leakage(suite)
            findings += check_fixtures(fixtures, expectations, fixture_schema)
            findings += check_action_target(expectations)
            findings += check_units(expectations, fixtures)
            findings += check_vocabularies(expectations, grader)
            findings += check_satisfiable_and_discriminating(fixtures, expectations, grader)
            findings += check_identity_binding(fixtures, expectations, grader)
            findings += check_determinism(fixtures, expectations, grader)
    findings += check_cross_family_consistency(samples)

    unique: dict[str, Finding] = {}
    for finding in findings:
        unique.setdefault(finding.key(), finding)
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return sorted(unique.values(), key=lambda f: (order[f.severity], f.rule, f.subject))


def run(cycle: str = "v06", seeds: list[int] | None = None, per_family: int = 2) -> list[Finding]:
    if cycle == "v06":
        generator = load_module("gen06", "heldout_generator_v06.py")
        grader = load_module("grd06", "grader_v06_structural.py")
        schema_path = HERE / "schemas" / "fixture-v3.schema.json"
    else:
        generator = load_module("gen05", "heldout_generator_v05.py")
        grader = load_module("grd05", "grader_v05_structural.py")
        schema_path = HERE / "schemas" / "fixture-v2.schema.json"
    schema = json.loads(schema_path.read_text()) if schema_path.is_file() else None
    return audit(generator, grader, seeds or [20260828, 1, 2, 3, 7, 11], per_family, schema)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycle", default="v06", choices=["v05", "v06"])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    findings = run(args.cycle)
    if args.json:
        print(json.dumps([f.as_dict() for f in findings], indent=2))
    else:
        print(f"=== Analytics oracle/harness audit ({args.cycle}) — {len(findings)} finding(s) ===\n")
        for finding in findings:
            print(f"  {finding}\n")
    return 1 if any(f.severity == "HIGH" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
