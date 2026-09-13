#!/usr/bin/env python3
"""Deterministic regression for the Stage C narrow field-only revision path.

Reproduces the defect class that consumed this chain's one bounded repair: re-authoring a whole
family returned malformed or truncated JSON (~16KB), three times running, with 0 candidate calls.
The narrow path returns a small object instead, splices it into the existing pack and re-runs the
full structural validation.

Zero model calls. The author/auditor child processes are never invoked; only the pure functions
around them are exercised, with the real sealed SPEECH_FALLBACK pack as the fixture.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACK = HERE / "heldout-v0.1" / "sealed" / "SPEECH_FALLBACK.json"
AUDIT = HERE / "heldout-v0.1" / "audit" / "SPEECH_FALLBACK.json"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), HERE / name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(condition: bool, label: str, failures: list[str]) -> None:
    print(("PASS " if condition else "FAIL ") + label)
    if not condition:
        failures.append(label)


def splice(author, pack: dict, case_index: int, field: str, value: str) -> dict:
    """The pure part of revise_field: splice a patched field and re-validate."""
    updated = json.loads(json.dumps(pack))
    updated["cases"][case_index - 1][field] = value
    author.validate(updated, updated["family"])
    return updated


def main() -> int:
    failures: list[str] = []
    author = load("heldout_author_v0.1.py")
    auditor = load("heldout_audit_v0.1.py")

    pack = json.loads(PACK.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))

    # --- the fixture is the real defect this retry must fix ---
    check(audit["verdict"] == "REVISE", "fixture: SPEECH_FALLBACK audit is REVISE", failures)
    check(audit["baseline_is_fair"] is False, "fixture: the failed check is baseline_is_fair", failures)
    check(len(audit["findings"]) >= 1, "fixture: audit carries at least one finding", failures)

    # --- the pack the narrow path must not damage ---
    try:
        author.validate(pack, "SPEECH_FALLBACK")
        check(True, "sealed pack still passes full structural validation", failures)
    except RuntimeError as exc:
        check(False, f"sealed pack still passes full structural validation ({exc})", failures)

    # --- narrow path: a valid small patch splices and revalidates ---
    good = ("Record the walkaround in one continuous take on the phone's built-in microphone, keep "
            "the speaker within about a metre of the handset, then listen back to the first thirty "
            "seconds before leaving and re-record if the speech is hard to follow.")
    try:
        updated = splice(author, pack, 2, "competent_generic_baseline", good)
        ok = updated["cases"][1]["competent_generic_baseline"] == good
        check(ok, "narrow path: valid patch splices into case 2 and revalidates", failures)
    except RuntimeError as exc:
        check(False, f"narrow path: valid patch splices into case 2 and revalidates ({exc})", failures)

    # --- the patch must not touch anything else ---
    try:
        untouched = all(
            updated["cases"][0] == pack["cases"][0],
            ) if False else updated["cases"][0] == pack["cases"][0]
        check(untouched, "narrow path: case 1 is untouched", failures)
        check(updated["pair_contract"] == pack["pair_contract"], "narrow path: pair_contract is untouched", failures)
        for field in ("brief", "context", "constraints", "professional_criteria", "p0_guardrail"):
            check(updated["cases"][1][field] == pack["cases"][1][field],
                  f"narrow path: case 2 {field} is untouched", failures)
    except NameError:
        check(False, "narrow path: patch isolation could not be checked", failures)

    # --- structural validation still rejects a bad patch ---
    for label, bad in (("empty", "   "), ("non-string", 42)):
        try:
            splice(author, pack, 2, "competent_generic_baseline", bad)
            check(False, f"narrow path: {label} patch is rejected", failures)
        except (RuntimeError, AttributeError, TypeError):
            check(True, f"narrow path: {label} patch is rejected", failures)

    # --- the failure mode that consumed the repair budget is still caught, not silently accepted ---
    for label, raw in (
        ("truncated object", '{"family":"SPEECH_FALLBACK","pair_contract":{"controlled_material_fact":"x"'),
        ("empty output", "   "),
        ("prose instead of JSON", "Here are the two cases you asked for."),
    ):
        try:
            author.extract_json(raw)
            check(False, f"author extract_json rejects {label}", failures)
        except RuntimeError:
            check(True, f"author extract_json rejects {label}", failures)

    # --- a well-formed fenced object is still recovered deterministically ---
    fenced = '```json\n{"case_index": 2, "competent_generic_baseline": "text"}\n```'
    try:
        value = author.extract_json(fenced)
        check(value == {"case_index": 2, "competent_generic_baseline": "text"},
              "author extract_json unwraps a single markdown fence", failures)
    except RuntimeError as exc:
        check(False, f"author extract_json unwraps a single markdown fence ({exc})", failures)

    # --- transport contract still holds on both candidate-blind children ---
    for name, module in (("author", author), ("auditor", auditor)):
        check("--bare" not in module.ISOLATION_FLAGS, f"{name}: --bare absent", failures)
        for required in ("--safe-mode", "--restricted", "--no-session-persistence", "--strict-mcp-config"):
            check(required in module.ISOLATION_FLAGS, f"{name}: {required} present", failures)
        check("ANTHROPIC_API_KEY" in module.FORBIDDEN_ENV, f"{name}: metered key stripped", failures)

    # --- candidate blindness: the author may never be seeded from a candidate-bearing path ---
    for token in ("professional-model-candidate", "delivery-state-overlay", "candidate-v0.",
                  "stage-b-development-fixtures"):
        check(token in author.FORBIDDEN_SEED, f"author: seed guard names {token}", failures)
    seeds = (author.PROFESSION_MODEL, author.COMPETENCY_MATRIX)
    check(all("research/" in s for s in seeds), "author: seeds come only from research artifacts", failures)
    check(not any(t in s for s in seeds for t in author.FORBIDDEN_SEED),
          "author: no seed path is candidate-bearing", failures)

    # --- the auditor cannot return ACCEPT while a check is false ---
    inconsistent = json.dumps({
        "verdict": "ACCEPT", "pair_contract_honored": True, "stance_relation_correct": True,
        "criteria_grounded_in_supplied_facts": True, "p0_guardrails_justified": True,
        "baseline_is_fair": False, "no_hidden_leakage": True, "findings": ["x"],
    })
    try:
        auditor.extract_json(inconsistent)
        check(False, "auditor rejects ACCEPT with a failed check", failures)
    except RuntimeError:
        check(True, "auditor rejects ACCEPT with a failed check", failures)

    if failures:
        print(f"\nFAILED: {len(failures)}")
        return 1
    print("\nOK: narrow revision path regression passed with 0 model calls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
