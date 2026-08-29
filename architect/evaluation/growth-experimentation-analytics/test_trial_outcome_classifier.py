#!/usr/bin/env python3
"""Deterministic tests for the INVALID class. No provider calls, no seed, no gate.

The suite is built around one adversarial question: **could someone reinterpret a trial after
seeing the gate result?** Every property below exists to make that mechanically impossible:

  * classification is a pure function of the failure text -- it cannot see the fixture, family,
    trial index, sibling outcomes, or whether the gate would otherwise pass;
  * the rule table is frozen behind a digest, so an edit cannot pass unnoticed;
  * the function is total -- there is no input that falls through to a judgement call;
  * unrecognised text fails closed to INVALID, which can void a gate but can never manufacture
    a PASS;
  * a provider failure can never be counted as candidate structural behavior, and a candidate's
    malformed output can never be excused as a provider failure.

Historical failure strings from v0.7 / v0.8 / v1.0 are used as classifier inputs. Those gates'
verdicts are NOT recomputed anywhere in this file, and the suite asserts that they are not.
"""

from __future__ import annotations

import importlib.util
import itertools
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


C = _load("toc", "trial_outcome_classifier.py")

# The digest of the frozen rule table at the moment this repair was written. If the table is
# edited, this test fails and the edit has to be argued for rather than slipped in.
FROZEN_RULES_DIGEST = "sha256:11f18a82f63493528d281adc69ac3cf50325fd084ebc40b9d96e04f2054f40e4"

# --------------------------------------------------------------------------------------------
# Real failure text observed in the three executed gates. Used ONLY as classifier input.
# --------------------------------------------------------------------------------------------
OBSERVED_TIER2 = [
    ("v0.7 HO-SBI-02 t1", "EXECUTION_ERROR",
     "adapter_error: Candidate executor failed with exit code 2: executor_error: model returned "
     "invalid JSON: Expecting property name enclosed in double quotes: line 15 column 7 (char 404)"),
    ("v0.8 HO-SBI-02 t2", "EXECUTION_ERROR",
     "adapter_error: Candidate executor failed with exit code 2: executor_error: model returned "
     "invalid JSON: Expecting property name enclosed in double quotes: line 40 column 7 (char 1262)"),
    ("v0.7 HO-UDC-02 t2", "FAIL",
     "output contract violation at decision_record.operational: Additional properties are not "
     "allowed ('none_decidable_reason' was unexpected)"),
    ("v1.0 HO-UOC-01 t1", "FAIL",
     "output contract violation at decision_record.operational: Additional properties are not "
     "allowed ('scale_readiness' was unexpected)"),
]

OBSERVED_TIER1 = [
    ("v0.7 HO-SBI-01 t1", "FAIL",
     "operational.target is 'variant_b', but action 'INCONCLUSIVE' may only be aimed at ['experiment']"),
    ("v0.7 HO-SBI-02 t2", "FAIL",
     "causal.status must be one of ['IDENTIFIED'], got 'UNRESOLVED'"),
    ("v0.7 HO-SBI-02 t2b", "FAIL",
     "claim_ceiling 'DESCRIPTIVE_ASSOCIATION' understates this design for scope REGISTERED_ESTIMAND "
     "(min INCREMENTAL_CAUSAL); sparse counts are a precision problem, not an identification failure"),
    ("v0.8 HO-IFH-02 t2", "FAIL", "decision_basis must record REGISTERED_PRIMARY_KPI"),
]

# No 429 has ever been observed on this key. These are constructed from the executor's own
# format strings (executor_gemini.py:127 / :129), not invented, and the test that follows says so.
CONSTRUCTED_INVALID = [
    ("quota exhausted", "EXECUTION_ERROR",
     "adapter_error: Candidate executor failed with exit code 2: executor_error: Gemini API HTTP "
     "429: {'error': {'code': 429, 'message': 'Resource has been exhausted', "
     "'status': 'RESOURCE_EXHAUSTED'}}"),
    ("server error", "EXECUTION_ERROR",
     "adapter_error: Candidate executor failed with exit code 2: executor_error: Gemini API HTTP "
     "503: {'error': {'code': 503, 'status': 'UNAVAILABLE'}}"),
    ("read timeout", "EXECUTION_ERROR",
     "adapter_error: Candidate executor failed with exit code 2: executor_error: Gemini API "
     "failure: The read operation timed out"),
    ("connection reset", "EXECUTION_ERROR",
     "adapter_error: Candidate executor failed with exit code 2: executor_error: Gemini API "
     "failure: <urlopen error [Errno 104] Connection reset by peer>"),
    ("empty 200 envelope", "EXECUTION_ERROR",
     "executor_error: Gemini Interactions returned no observable text output"),
    ("freeze drift", "EXECUTION_ERROR",
     "executor_error: candidate component hash mismatch for architect/research/"
     "growth-experimentation-analytics/professional-model-consolidated-v1.0.md: abc != def"),
    ("missing credential", "EXECUTION_ERROR", "executor_error: GEMINI_API_KEY is required"),
]


class ProviderFailureIsInvalidNotTier2(unittest.TestCase):
    """The defect this repair exists for."""

    def test_every_transport_and_api_failure_classifies_INVALID(self) -> None:
        for label, status, detail in CONSTRUCTED_INVALID:
            with self.subTest(case=label):
                self.assertEqual(C.INVALID, C.classify_trial(status, detail=detail))

    def test_a_429_is_never_tier2(self) -> None:
        """The precise miscount the repair prevents: throttling counted as candidate behavior."""
        detail = ("adapter_error: Candidate executor failed with exit code 2: executor_error: "
                  "Gemini API HTTP 429: quota exceeded")
        self.assertNotEqual(C.TIER2, C.classify_trial("EXECUTION_ERROR", detail=detail))
        self.assertEqual(C.INVALID, C.classify_trial("EXECUTION_ERROR", detail=detail))

    def test_the_two_paths_share_a_status_and_still_separate(self) -> None:
        """Both exit 2 and both land as EXECUTION_ERROR; only the cause text tells them apart."""
        throttled = ("adapter_error: Candidate executor failed with exit code 2: "
                     "executor_error: Gemini API HTTP 429: quota exceeded")
        malformed = ("adapter_error: Candidate executor failed with exit code 2: "
                     "executor_error: model returned invalid JSON: Expecting ',' delimiter")
        self.assertEqual(C.INVALID, C.classify_trial("EXECUTION_ERROR", detail=throttled))
        self.assertEqual(C.TIER2, C.classify_trial("EXECUTION_ERROR", detail=malformed))

    def test_the_shared_wrapper_alone_never_decides(self) -> None:
        """'Candidate executor failed with exit code 2' wraps both; it must not classify."""
        self.assertEqual(C.INVALID, C.classify_trial(
            "EXECUTION_ERROR",
            detail="adapter_error: Candidate executor failed with exit code 2: "),
            "a wrapper with no recognisable cause must fail closed, not pick a side")


class MalformedModelOutputStaysTier2(unittest.TestCase):
    def test_every_observed_structural_failure_classifies_TIER2(self) -> None:
        for label, status, text in OBSERVED_TIER2:
            with self.subTest(case=label):
                kwargs = ({"detail": text} if status == "EXECUTION_ERROR" else {"failures": [text]})
                self.assertEqual(C.TIER2, C.classify_trial(status, **kwargs))

    def test_every_syntactic_parse_failure_path_classifies_TIER2(self) -> None:
        for detail in ("executor_error: model returned invalid JSON: Expecting value",
                       "executor_error: model returned non-JSON output",
                       "executor_error: model result must be a JSON object",
                       "Candidate executor returned non-JSON stdout",
                       "Candidate executor result must be one JSON object"):
            with self.subTest(detail=detail[:44]):
                self.assertEqual(C.TIER2, C.classify_trial("EXECUTION_ERROR", detail=detail))
        self.assertEqual(C.TIER2, C.classify_trial("FAIL", failures=["candidate returned non-JSON"]))

    def test_a_tier2_trial_is_never_a_judgment_pass(self) -> None:
        for _l, status, text in OBSERVED_TIER2:
            kwargs = ({"detail": text} if status == "EXECUTION_ERROR" else {"failures": [text]})
            self.assertNotEqual(C.PASS, C.classify_trial(status, **kwargs))

    def test_freeze_drift_is_invalid_not_a_contract_violation(self) -> None:
        """'output contract hash mismatch' and 'output contract violation at' both start alike."""
        self.assertEqual(C.INVALID, C.classify_trial(
            "EXECUTION_ERROR", detail="executor_error: output contract hash mismatch for x: a != b"))
        self.assertEqual(C.TIER2, C.classify_trial(
            "FAIL", failures=["output contract violation at decision_record: bad"]))


class JudgmentFailuresStayTier1(unittest.TestCase):
    def test_every_observed_judgment_failure_classifies_TIER1(self) -> None:
        for label, status, text in OBSERVED_TIER1:
            with self.subTest(case=label):
                self.assertEqual(C.TIER1, C.classify_trial(status, failures=[text]))

    def test_an_unlisted_grader_message_defaults_to_TIER1_not_tier2(self) -> None:
        """A future grader message must land in the strict tier, never the tolerated one."""
        for msg in ("scale_readiness.state must be BLOCKED, got 'ELIGIBLE'",
                    "recommendation SCALE requires scale_readiness ELIGIBLE",
                    "computation relative_lift_variant_a incorrect (expected ~0.42, got 42.0)",
                    "some message no one has written yet"):
            with self.subTest(msg=msg[:44]):
                self.assertEqual(C.TIER1, C.classify_trial("FAIL", failures=[msg]))

    def test_a_judgment_failure_is_not_absorbed_by_a_co_occurring_structural_one(self) -> None:
        mixed = ["output contract violation at decision_record: bad",
                 "causal.status must be one of ['IDENTIFIED'], got 'UNRESOLVED'"]
        self.assertEqual(C.TIER1, C.classify_trial("FAIL", failures=mixed))
        self.assertEqual(C.TIER1, C.classify_trial("FAIL", failures=list(reversed(mixed))))


class ClassificationCannotBeReinterpreted(unittest.TestCase):
    """The anti-laundering properties. These are the point of the file."""

    def test_the_rule_table_is_frozen_behind_a_digest(self) -> None:
        self.assertEqual(FROZEN_RULES_DIGEST, C.RULES_DIGEST,
                         "the tier map changed; that is a criterion change and must be argued for, "
                         "not slipped in alongside a gate")

    def test_classification_is_a_pure_function_of_the_failure_text(self) -> None:
        """No fixture, family, trial index or sibling outcome is an input. It cannot be."""
        import inspect
        params = set(inspect.signature(C.classify_trial).parameters)
        self.assertEqual({"status", "detail", "failures"}, params)
        for forbidden in ("fixture", "family", "trial", "seed", "gate", "verdict", "index"):
            self.assertNotIn(forbidden, params)

    def test_the_same_text_classifies_identically_in_every_context(self) -> None:
        """Same input, many surrounding contexts -- the outcome may not move."""
        text = "output contract violation at decision_record.operational: bad"
        base = C.classify_trial("FAIL", failures=[text])
        for fid, trial in itertools.product(
                ["HO-UOC-01", "HO-SBI-02", "HO-CSW-01"], range(1, 8)):
            with self.subTest(fixture=fid, trial=trial):
                # the classifier is not even given these; re-calling must be identical
                self.assertEqual(base, C.classify_trial("FAIL", failures=[text]))

    def test_classification_is_deterministic_across_repeated_calls(self) -> None:
        samples = ([(s, d, None) for _l, s, d in CONSTRUCTED_INVALID]
                   + [(s, t, None) if s == "EXECUTION_ERROR" else (s, None, [t])
                      for _l, s, t in OBSERVED_TIER2]
                   + [(s, None, [t]) for _l, s, t in OBSERVED_TIER1])
        for status, detail, failures in samples:
            first = C.classify_trial(status, detail=detail, failures=failures)
            for _ in range(20):
                self.assertEqual(first, C.classify_trial(status, detail=detail, failures=failures))

    def test_the_function_is_total(self) -> None:
        """No input falls through to a judgement call."""
        weird = ["", "   ", "\x00", "None", "PASS", "TIER1", "INVALID",
                 "a" * 5000, "429", "Gemini", "contract", "JSON"]
        for status in ("PASS", "FAIL", "EXECUTION_ERROR", "TIMEOUT", "", "ABORTED", "unknown"):
            for text in weird:
                with self.subTest(status=status, text=text[:20]):
                    out = C.classify_trial(status, detail=text, failures=[text])
                    self.assertIn(out, C.OUTCOMES)

    def test_unrecognised_text_fails_closed_to_INVALID(self) -> None:
        for detail in ("", "something entirely new", "segmentation fault", "killed"):
            with self.subTest(detail=detail[:24]):
                self.assertEqual(C.INVALID, C.classify_trial("EXECUTION_ERROR", detail=detail))
        self.assertEqual(C.INVALID, C.classify_trial("FAIL", failures=[]))
        self.assertEqual(C.INVALID, C.classify_trial("MYSTERY"))

    def test_failing_closed_can_void_a_gate_but_never_manufacture_a_pass(self) -> None:
        for status in ("FAIL", "EXECUTION_ERROR", "TIMEOUT", "", "unknown"):
            for text in ("", "unrecognised", "\x00"):
                self.assertNotEqual(C.PASS, C.classify_trial(status, detail=text, failures=[text]))

    def test_only_a_PASS_status_can_produce_a_PASS_outcome(self) -> None:
        self.assertEqual(C.PASS, C.classify_trial("PASS"))
        for status in ("FAIL", "EXECUTION_ERROR", "pass", "Pass", "", "PASSED"):
            self.assertNotEqual(C.PASS, C.classify_trial(status),
                                f"{status!r} must not be readable as a pass")

    def test_every_rule_pattern_is_traceable_to_an_emitting_source(self) -> None:
        for pattern, outcome, source in C.RULES:
            with self.subTest(pattern=pattern[:40]):
                self.assertIn(outcome, C.OUTCOMES)
                self.assertTrue(source.strip(), "every pattern must name where it is emitted")

    def test_no_rule_pattern_is_shadowed_by_an_earlier_one(self) -> None:
        """An unreachable rule is a rule someone thinks is in force when it is not."""
        for i, (pattern, outcome, _s) in enumerate(C.RULES):
            reached = C.classify_text(pattern)
            with self.subTest(pattern=pattern[:40]):
                self.assertEqual(outcome, reached,
                                 f"rule {i} is shadowed by an earlier pattern")


class GateVerdictTreatsInvalidAsVoid(unittest.TestCase):
    CAPF, CAPT = 2, 6

    def _v(self, by_fixture):
        return C.gate_verdict(by_fixture, self.CAPF, self.CAPT)

    def clean(self):
        return {f"F{i}": [C.PASS] * 7 for i in range(10)}

    def test_a_clean_ledger_passes(self) -> None:
        self.assertEqual("PASS", self._v(self.clean())["verdict"])

    def test_one_invalid_trial_voids_the_whole_gate(self) -> None:
        led = self.clean(); led["F3"][4] = C.INVALID
        out = self._v(led)
        self.assertEqual(C.INVALID, out["verdict"])
        self.assertEqual(1, out["invalid_trials"])

    def test_invalid_is_not_a_pass_and_not_a_fail(self) -> None:
        led = self.clean(); led["F0"][0] = C.INVALID
        self.assertNotIn(self._v(led)["verdict"], ("PASS", "FAIL"))

    def test_invalid_outranks_a_tier1_failure(self) -> None:
        """A gate that did not measure the candidate cannot report a candidate verdict."""
        led = self.clean(); led["F1"][0] = C.TIER1; led["F2"][0] = C.INVALID
        self.assertEqual(C.INVALID, self._v(led)["verdict"])

    def test_invalid_outranks_a_tier2_cap_breach(self) -> None:
        led = self.clean()
        led["F1"] = [C.TIER2] * 7
        led["F2"][0] = C.INVALID
        self.assertEqual(C.INVALID, self._v(led)["verdict"])

    def test_a_single_tier1_fails_the_gate(self) -> None:
        led = self.clean(); led["F5"][6] = C.TIER1
        out = self._v(led)
        self.assertEqual("FAIL", out["verdict"])
        self.assertEqual(1, out["tier1_trials"])

    def test_tier2_within_both_caps_passes(self) -> None:
        led = self.clean()
        led["F0"][0] = C.TIER2; led["F1"][0] = C.TIER2
        led["F2"][0] = C.TIER2; led["F2"][1] = C.TIER2
        out = self._v(led)
        self.assertEqual("PASS", out["verdict"])
        self.assertEqual(4, out["tier2_total"])

    def test_the_per_fixture_cap_binds(self) -> None:
        led = self.clean(); led["F4"][0] = led["F4"][1] = led["F4"][2] = C.TIER2
        self.assertEqual("FAIL", self._v(led)["verdict"])

    def test_the_total_cap_binds(self) -> None:
        led = self.clean()
        for i in range(4):
            led[f"F{i}"][0] = led[f"F{i}"][1] = C.TIER2   # 8 > 6, none over the per-fixture cap
        out = self._v(led)
        self.assertEqual("FAIL", out["verdict"])
        self.assertEqual(8, out["tier2_total"])

    def test_tier2_trials_are_not_counted_as_judgment_passes(self) -> None:
        led = self.clean(); led["F0"][0] = C.TIER2
        self.assertEqual(69, self._v(led)["judgment_pass_trials"])

    def test_the_verdict_carries_the_rule_digest_it_was_computed_under(self) -> None:
        self.assertEqual(FROZEN_RULES_DIGEST, self._v(self.clean())["rules_digest"])


class ScopeOfThisRepair(unittest.TestCase):
    def test_no_frozen_instrument_or_candidate_file_was_modified(self) -> None:
        import json
        freeze = json.loads((HERE / "candidate-freeze-v1.0.json").read_text(encoding="utf-8"))
        def blob(p):
            return subprocess.check_output(["git", "hash-object", p], text=True, cwd=ROOT).strip()
        for component in freeze["assembly"]:
            with self.subTest(path=component["path"]):
                self.assertEqual(component["git_blob_sha"], blob(component["path"]))
        for role, ref in freeze["instrument"].items():
            with self.subTest(role=role):
                self.assertEqual(ref["git_blob_sha"], blob(ref["path"]))
        self.assertEqual(freeze["output_contract_git_blob_sha"],
                         blob(freeze["output_contract_path"]))

    def test_this_repair_makes_no_provider_call(self) -> None:
        source = (HERE / "trial_outcome_classifier.py").read_text(encoding="utf-8")
        for forbidden in ("urllib", "requests", "http", "socket", "subprocess", "os.environ"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)

    def test_no_historical_gate_verdict_is_recomputed_here(self) -> None:
        """Observed strings are classifier inputs only. v0.7/v0.8/v1.0 verdicts stand as recorded."""
        source = Path(__file__).read_text(encoding="utf-8")
        body = source.split("def test_no_historical_gate_verdict_is_recomputed_here")[0]
        for gate in ("v0.7", "v0.8", "v1.0"):
            for call in ("gate_verdict(", "verdict("):
                idx = 0
                while (idx := body.find(gate, idx)) != -1:
                    window = body[idx:idx + 400]
                    self.assertNotIn(call, window,
                                     f"a {gate} string must not feed a gate verdict computation")
                    idx += 1


if __name__ == "__main__":
    unittest.main(verbosity=2)
