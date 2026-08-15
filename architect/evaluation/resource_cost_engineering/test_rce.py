from datetime import datetime, timezone
import unittest

from rce_policy import Decision, FreshnessState, GateInput, ResourceVector, evaluate_gate, post_run_accounting

NOW = datetime(2026, 8, 15, 2, 30, tzinfo=timezone.utc)
FRESH = FreshnessState("2026-08-15T02:00:00Z", 24, True, True)
STALE = FreshnessState("2026-07-01T00:00:00Z", 24, True, True)


def base(**kw):
    args = dict(
        run_id="r",
        objective="prove affected gate",
        decision_to_change="REVISE -> PASS",
        risk_class="high",
        required_quality_floor="release threshold",
        estimate=ResourceVector(model_calls=1, api_credits=2, ci_minutes=1),
        remaining=ResourceVector(model_calls=10, api_credits=20, ci_minutes=20),
        protected_reserve=ResourceVector(model_calls=3, api_credits=6, ci_minutes=5),
        recovery_reserve=ResourceVector(model_calls=1, api_credits=2, ci_minutes=2),
        expected_information_gain="whether B1 root cause is fixed",
        stop_condition="stop after one affected trial",
        midrun_exhaustion_plan="persist completed evidence and mark incomplete",
    )
    args.update(kw)
    return GateInput(**args)


class RCEBehavioralSpec(unittest.TestCase):
    def test_b1_deterministic_before_llm(self):
        r = evaluate_gate(base(deterministic_answer_available=True), NOW)
        self.assertEqual(r.decision, Decision.BLOCK)

    def test_b2_fresh_evidence_reuse(self):
        self.assertEqual(evaluate_gate(base(fresh_reusable_evidence_available=True), NOW).decision, Decision.BLOCK)

    def test_b3_protected_release_reserve(self):
        r = evaluate_gate(base(estimate=ResourceVector(model_calls=8, api_credits=16, ci_minutes=15)), NOW)
        self.assertEqual(r.decision, Decision.BLOCK)
        self.assertTrue(r.reasons[0].startswith("protected_reserve_would_be_consumed"))

    def test_b4_targeted_before_full_suite(self):
        self.assertEqual(evaluate_gate(base(full_suite=True, affected_scope_known=True, targeted_regression_available=True), NOW).decision, Decision.TARGET)

    def test_b5_stale_material_pricing_defers(self):
        self.assertEqual(evaluate_gate(base(pricing_material_to_decision=True, pricing_freshness=STALE), NOW).decision, Decision.DEFER)

    def test_b6_fresh_authoritative_pricing_allows(self):
        self.assertEqual(evaluate_gate(base(pricing_material_to_decision=True, pricing_freshness=FRESH), NOW).decision, Decision.ALLOW)

    def test_b7_privacy_beats_cheaper_provider(self):
        self.assertEqual(evaluate_gate(base(provider_eligible_privacy=False), NOW).decision, Decision.BLOCK)

    def test_b8_no_information_gain_blocks(self):
        self.assertEqual(evaluate_gate(base(expected_information_gain=None), NOW).decision, Decision.BLOCK)

    def test_b9_direct_strong_can_beat_cascade(self):
        self.assertEqual(evaluate_gate(base(alternative_direct_strong_is_lower_total_cost=True, chosen_is_direct_strong=False), NOW).decision, Decision.DOWNGRADE)

    def test_b10_midrun_plan_is_required(self):
        self.assertEqual(evaluate_gate(base(midrun_exhaustion_plan=None), NOW).decision, Decision.BLOCK)

    def test_b11_post_run_low_information_and_duplicate_detection(self):
        out = post_run_accounting({
            "planned_resources": {"model_calls": 3},
            "actual_resources": {"model_calls": 5, "human_minutes": 20},
            "new_information": "",
            "evidence_produced": "",
            "decision_before": "REVISE",
            "decision_after": "REVISE",
            "unchanged_candidate": True,
            "repeated_same_hypothesis": True,
            "retry_count": 4,
            "retry_budget": 2,
        })
        self.assertIn("high_or_material_spend_low_information", out["waste_signal"])
        self.assertIn("duplicate_run_without_new_hypothesis", out["waste_signal"])
        self.assertIn("retry_budget_exceeded", out["waste_signal"])

    def test_b12_copilot_incident_regression(self):
        r = evaluate_gate(base(
            estimate=ResourceVector(model_calls=7, api_credits=14, ci_minutes=10),
            full_suite=True,
            affected_scope_known=True,
            targeted_regression_available=True,
        ), NOW)
        self.assertEqual(r.decision, Decision.BLOCK)
        r2 = evaluate_gate(base(
            remaining=ResourceVector(model_calls=30, api_credits=60, ci_minutes=60),
            estimate=ResourceVector(model_calls=7, api_credits=14, ci_minutes=10),
            full_suite=True,
            affected_scope_known=True,
            targeted_regression_available=True,
        ), NOW)
        self.assertEqual(r2.decision, Decision.TARGET)


if __name__ == "__main__":
    unittest.main(verbosity=2)
