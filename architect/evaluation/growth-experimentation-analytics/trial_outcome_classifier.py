#!/usr/bin/env python3
"""Trial-outcome classification for the Analytics held-out gate.

This is a repair to the MEASUREMENT LOOP, not to the candidate. It changes nothing about the
professional model, the grader, the generator, the fixtures or the output contract, and it does
not by itself run or score anything.

## The defect it repairs

`executor_gemini.py` calls `fail()` and exits 2 for two categorically different events:

    executor_gemini.py:127   fail(f"Gemini API HTTP {exc.code}: ...")    # provider throttled/erred
    executor_gemini.py:145   fail(f"model returned invalid JSON: {exc}")  # candidate emitted junk

`run_heldout_gate_v07.py:100` records both as `status="EXECUTION_ERROR"`. A provider 429 and a
candidate-produced malformed result are therefore indistinguishable at the status level, and a
criterion that counts structural failures would count provider throttling as candidate behavior.
`SKILL.md` Phase 10: *do not score behavior observed under an invalid experimental setup.*

## The three outcomes

* **INVALID** — the measurement apparatus failed. The provider throttled, timed out, erred or
  returned an unusable envelope, or the harness itself was misconfigured. **No candidate output
  exists**, so there is nothing to score. Any INVALID trial makes the whole gate INVALID: not
  PASS, not FAIL. The seed is preserved and the cycle is re-run, because nothing about the
  candidate was measured.
* **TIER2** — the candidate produced output and that output is not a valid instance of the frozen
  contract: a syntactic parse failure, or a frozen-schema violation. This is candidate behavior
  and it is counted, but a TIER2 trial is **never a judgment PASS** — its professional content was
  never assessed.
* **TIER1** — the candidate produced a contract-valid result whose professional content the frozen
  grader rejected. Everything else.

## Why classification cannot be reinterpreted after a gate

`RULES` is an ordered, frozen table matched against the failure text the apparatus emits, and every
pattern below is copied from the source line that emits it. Classification is a pure function of
the failure text alone. It cannot see the fixture, the family, the trial number, how many other
trials failed, or whether the gate would otherwise pass. `RULES_DIGEST` pins the table so an edit
cannot pass unnoticed.

Unrecognised text classifies as **INVALID**, deliberately. Failing closed can only ever turn a
scored gate into an unscored one; it can never turn a candidate failure into a PASS.
"""

from __future__ import annotations

import hashlib
import json

PASS = "PASS"
TIER1 = "TIER1"
TIER2 = "TIER2"
INVALID = "INVALID"

OUTCOMES = (PASS, TIER1, TIER2, INVALID)

# Ordered. First matching pattern wins. Each entry is (pattern, outcome, emitting source).
# Patterns are substrings of text the apparatus actually produces; the source column is the line
# that produces it, so the table can be re-derived rather than trusted.
RULES: tuple[tuple[str, str, str], ...] = (
    # --- provider transport and API-level failure: no candidate output exists -----------------
    ("Gemini API HTTP ",                          INVALID, "executor_gemini.py:127"),
    ("Gemini API failure: ",                      INVALID, "executor_gemini.py:129"),
    ("Gemini Interactions returned no observable text output",
                                                  INVALID, "executor_gemini.py:88"),
    ("Gemini Interactions returned non-object payload",
                                                  INVALID, "executor_gemini.py:131"),
    ("Groq API HTTP ",                            INVALID, "executor_groq.py (parallel path)"),
    ("Groq API failure: ",                        INVALID, "executor_groq.py (parallel path)"),
    # --- harness misconfiguration or freeze drift: the setup is invalid -----------------------
    ("GEMINI_API_KEY is required",                INVALID, "executor_gemini.py:95"),
    ("GROQ_API_KEY is required",                  INVALID, "executor_groq.py (parallel path)"),
    ("candidate component hash mismatch for ",    INVALID, "executor_gemini.py:52"),
    ("output contract hash mismatch for ",        INVALID, "executor_gemini.py:72"),
    ("cannot hash candidate component ",          INVALID, "executor_gemini.py:34"),
    ("candidate manifest assembly missing",       INVALID, "executor_gemini.py:41"),
    ("invalid candidate component",               INVALID, "executor_gemini.py:45"),
    ("candidate component path/hash missing",     INVALID, "executor_gemini.py:49"),
    ("candidate manifest or task missing",        INVALID, "executor_gemini.py:158"),
    ("invalid protocol",                          INVALID, "executor_gemini.py:154"),
    ("ANALYTICS_CANDIDATE_CMD is required",       INVALID, "stdio_candidate_adapter.py:60"),
    ("ANALYTICS_CANDIDATE_MANIFEST is required",  INVALID, "stdio_candidate_adapter.py:36"),
    ("Candidate executor returned empty stdout",  INVALID, "stdio_candidate_adapter.py:82"),
    # --- candidate produced output that is not a valid instance of the frozen contract --------
    ("model returned invalid JSON: ",             TIER2,   "executor_gemini.py:145"),
    ("model returned non-JSON output",            TIER2,   "executor_gemini.py:141"),
    ("model result must be a JSON object",        TIER2,   "executor_gemini.py:147"),
    ("Candidate executor returned non-JSON stdout",
                                                  TIER2,   "stdio_candidate_adapter.py:87"),
    ("Candidate executor result must be one JSON object",
                                                  TIER2,   "stdio_candidate_adapter.py:90"),
    ("candidate returned non-JSON",               TIER2,   "run_heldout_gate_v07.py:118"),
    ("output contract violation at ",             TIER2,   "grader_v07_structural.py:118,121"),
    ("output contract unavailable",               INVALID, "grader_v07_structural.py:113"),
)

# Everything the grader can say that is not matched above is professional judgment.
DEFAULT_FOR_GRADER_FAILURE = TIER1

# Anything else at all -- an unrecognised transport error, a new executor message, a truncated
# stderr -- fails closed. An unscored gate is recoverable; a mis-scored one is not.
DEFAULT_FOR_UNRECOGNISED = INVALID

RULES_DIGEST = "sha256:" + hashlib.sha256(
    json.dumps([[p, o] for p, o, _src in RULES], separators=(",", ":")).encode()
).hexdigest()


def classify_text(text: str) -> str | None:
    """Classify one failure string. Returns None when no frozen rule matches."""
    if not isinstance(text, str):
        return None
    for pattern, outcome, _source in RULES:
        if pattern in text:
            return outcome
    return None


def classify_trial(status: str, detail: str | None = None,
                   failures: list[str] | None = None) -> str:
    """Classify one recorded trial into exactly one of OUTCOMES.

    Total: every input returns exactly one outcome. Pure: depends on nothing but its arguments.
    """
    if status == "PASS":
        return PASS

    if status == "EXECUTION_ERROR":
        # The apparatus wraps the cause; the cause is what classifies. An unrecognised cause,
        # or none at all, is INVALID.
        return classify_text(detail or "") or DEFAULT_FOR_UNRECOGNISED

    if status == "FAIL":
        entries = [f for f in (failures or []) if isinstance(f, str)]
        if not entries:
            return DEFAULT_FOR_UNRECOGNISED
        classes = {classify_text(f) or DEFAULT_FOR_GRADER_FAILURE for f in entries}
        # A trial carrying any apparatus failure is not a candidate result at all.
        if INVALID in classes:
            return INVALID
        # A judgment failure is never absorbed by a co-occurring structural one.
        if TIER1 in classes:
            return TIER1
        return TIER2

    return DEFAULT_FOR_UNRECOGNISED


def gate_verdict(outcomes_by_fixture: dict[str, list[str]],
                 tier2_per_fixture_cap: int, tier2_total_cap: int) -> dict:
    """Aggregate per-trial outcomes into a gate verdict.

    INVALID > FAIL > PASS. An INVALID trial anywhere means the gate measured nothing about the
    candidate: the verdict is INVALID, never PASS and never FAIL.
    """
    flat = [o for outcomes in outcomes_by_fixture.values() for o in outcomes]
    invalid = [o for o in flat if o == INVALID]
    tier1 = [o for o in flat if o == TIER1]
    per_fixture_tier2 = {f: sum(1 for o in os if o == TIER2)
                         for f, os in outcomes_by_fixture.items()}
    tier2_total = sum(per_fixture_tier2.values())
    over_fixture_cap = {f: n for f, n in per_fixture_tier2.items() if n > tier2_per_fixture_cap}

    if invalid:
        verdict, reason = INVALID, (
            f"{len(invalid)} trial(s) did not measure the candidate; the gate is void. "
            "Re-run on the same seed: nothing about the candidate was observed.")
    elif tier1:
        verdict, reason = "FAIL", f"{len(tier1)} tier-1 professional judgment failure(s)"
    elif over_fixture_cap:
        verdict, reason = "FAIL", (
            f"tier-2 per-fixture cap {tier2_per_fixture_cap} exceeded: {over_fixture_cap}")
    elif tier2_total > tier2_total_cap:
        verdict, reason = "FAIL", (
            f"tier-2 total cap {tier2_total_cap} exceeded: {tier2_total}")
    else:
        verdict, reason = "PASS", "no tier-1 failure; tier-2 within both caps"

    return {
        "verdict": verdict,
        "reason": reason,
        "invalid_trials": len(invalid),
        "tier1_trials": len(tier1),
        "tier2_total": tier2_total,
        "tier2_per_fixture": per_fixture_tier2,
        "judgment_pass_trials": sum(1 for o in flat if o == PASS),
        "rules_digest": RULES_DIGEST,
    }


if __name__ == "__main__":
    print(f"rules: {len(RULES)}")
    print(f"digest: {RULES_DIGEST}")
    for outcome in OUTCOMES:
        n = sum(1 for _p, o, _s in RULES if o == outcome)
        if n:
            print(f"  {outcome:8} {n:2} pattern(s)")
