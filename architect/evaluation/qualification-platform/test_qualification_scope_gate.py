import unittest

import qualification_scope_gate as g


BASE = {
    "purpose": "repair",
    "change_surface": "local",
    "existing_evidence": "incompatible",
    "affected_families": ["F-02"],
    "full_release_required": False,
    "runtime_uncertainty": False,
    "professional_behavior_changed": True,
}


class QualificationScopeGateTests(unittest.TestCase):
    def test_release_always_requires_full(self):
        x = dict(BASE, purpose="release", change_surface="local")
        r = g.decide(x)
        self.assertEqual(r["scope"], "FULL")
        self.assertTrue(r["release_pass_allowed_from_this_scope"])

    def test_preregistered_full_release_cannot_be_optimized_away(self):
        x = dict(BASE, full_release_required=True)
        self.assertEqual(g.decide(x)["scope"], "FULL")

    def test_compatible_unchanged_evidence_is_reused(self):
        x = dict(
            BASE,
            change_surface="infrastructure",
            existing_evidence="compatible",
            affected_families=[],
            professional_behavior_changed=False,
        )
        r = g.decide(x)
        self.assertEqual(r["scope"], "REUSE")
        self.assertFalse(r["paid_scored_run_allowed"])

    def test_local_change_targets_declared_families(self):
        x = dict(BASE, affected_families=["F-02", "F-01", "F-02"])
        r = g.decide(x)
        self.assertEqual(r["scope"], "TARGET")
        self.assertEqual(r["affected_families"], ["F-01", "F-02"])
        self.assertFalse(r["release_pass_allowed_from_this_scope"])

    def test_local_without_family_mapping_blocks(self):
        x = dict(BASE, affected_families=[])
        self.assertEqual(g.decide(x)["scope"], "BLOCK")

    def test_shared_change_escalates_full(self):
        x = dict(BASE, change_surface="shared")
        self.assertEqual(g.decide(x)["scope"], "FULL")

    def test_unknown_change_escalates_full(self):
        x = dict(BASE, change_surface="unknown")
        self.assertEqual(g.decide(x)["scope"], "FULL")

    def test_infrastructure_without_compatible_evidence_blocks(self):
        x = dict(
            BASE,
            change_surface="infrastructure",
            affected_families=[],
            professional_behavior_changed=False,
            existing_evidence="none",
        )
        self.assertEqual(g.decide(x)["scope"], "BLOCK")

    def test_runtime_uncertainty_marks_canary_without_changing_scope(self):
        x = dict(BASE, runtime_uncertainty=True)
        r = g.decide(x)
        self.assertEqual(r["scope"], "TARGET")
        self.assertEqual(r["runtime_canary"], "REQUIRED_IF_NOT_STATICALLY_RESOLVED")

    def test_bad_request_fails_closed(self):
        x = dict(BASE)
        del x["professional_behavior_changed"]
        with self.assertRaises(g.ScopeGateError):
            g.decide(x)


if __name__ == "__main__":
    unittest.main()
