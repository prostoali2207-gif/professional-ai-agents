from research_policy import (
    AccessState,
    ClaimState,
    EvidenceRecord,
    FailureClass,
    ResearchContract,
    RouteInput,
    StopDecision,
    adjudicate_claim,
    choose_route,
    independent_evidence_count,
    retry_allowed,
    stopping_decision,
    validate_contract,
)


def rec(**overrides):
    base = dict(
        claim_id="c1",
        source_identity="s1",
        source_class="primary",
        authority_basis="official",
        access_state=AccessState.FULL,
        citation_entails_claim=True,
    )
    base.update(overrides)
    return EvidenceRecord(**base)


def test_contract_requires_stop_condition():
    c = ResearchContract(decision="d", material_claims=["c"], stakes="high")
    assert "missing_stop_condition" in validate_contract(c)


def test_known_official_url_routes_directly():
    result = choose_route(RouteInput(known_official_url=True, concrete_gap="verify current rule"))
    assert result.allowed
    assert result.route_class == "DIRECT_PRIMARY_INSPECTION"


def test_router_blocks_query_without_gap():
    result = choose_route(RouteInput())
    assert not result.allowed
    assert "no_concrete_evidence_gap" in result.reasons


def test_router_protects_reserve():
    result = choose_route(
        RouteInput(
            concrete_gap="verify authority",
            estimated_external_calls=2,
            remaining_external_calls=3,
            protected_external_call_reserve=2,
        )
    )
    assert not result.allowed
    assert result.route_class == "DEFER_OR_ESCALATE"


def test_snippet_only_cannot_support_material_claim():
    state = adjudicate_claim([rec(access_state=AccessState.SNIPPET_ONLY)])
    assert state == ClaimState.UNVERIFIED


def test_superseded_source_does_not_count_as_current_support():
    state = adjudicate_claim([rec(lifecycle_state="SUPERSEDED")])
    assert state == ClaimState.UNVERIFIED


def test_noncomparable_evidence_fails_aggregation():
    state = adjudicate_claim([rec(same_population=False)])
    assert state == ClaimState.NOT_COMPARABLE


def test_entailment_conflict_is_preserved():
    state = adjudicate_claim(
        [
            rec(source_identity="a", citation_entails_claim=True),
            rec(source_identity="b", citation_entails_claim=False),
        ]
    )
    assert state == ClaimState.CONFLICTED


def test_high_stakes_requires_independent_support():
    state = adjudicate_claim([rec()], high_stakes=True)
    assert state == ClaimState.PARTIAL
    state2 = adjudicate_claim(
        [rec(source_identity="a"), rec(source_identity="b")], high_stakes=True
    )
    assert state2 == ClaimState.SUPPORTED


def test_syndicated_descendants_do_not_inflate_independence():
    records = [
        rec(source_identity="copy1", canonical_parent="root"),
        rec(source_identity="copy2", canonical_parent="root"),
    ]
    assert independent_evidence_count(records) == 1


def test_common_methodology_does_not_inflate_independence():
    records = [
        rec(source_identity="a", method_common_cause="dataset-x"),
        rec(source_identity="b", method_common_cause="dataset-x"),
    ]
    assert independent_evidence_count(records) == 2
    # Source lineage and methodological dependence are deliberately separate axes.
    assert records[0].method_common_cause == records[1].method_common_cause


def test_behavioral_failure_is_not_retried():
    assert not retry_allowed(FailureClass.EVIDENCE_BEHAVIOR, 0, 2, True, True)


def test_transient_capacity_retry_is_bounded():
    assert retry_allowed(FailureClass.CAPACITY_TRANSIENT, 0, 1, True, True)
    assert not retry_allowed(FailureClass.CAPACITY_TRANSIENT, 1, 1, True, True)


def test_quota_exhaustion_is_not_blindly_retried():
    assert not retry_allowed(FailureClass.DAILY_QUOTA_EXHAUSTED, 0, 3, True, True)


def test_complete_material_claims_stop():
    decision = stopping_decision(
        material_claim_states=[ClaimState.SUPPORTED, ClaimState.CONTRADICTED],
        unresolved_high_stakes_gap=False,
        scope_ambiguous=False,
        concrete_next_gap=None,
        next_action_has_expected_value=False,
        budget_available=True,
    )
    assert decision == StopDecision.STOP


def test_budget_does_not_convert_high_stakes_gap_to_pass():
    decision = stopping_decision(
        material_claim_states=[ClaimState.UNVERIFIED],
        unresolved_high_stakes_gap=True,
        scope_ambiguous=False,
        concrete_next_gap="find current authority",
        next_action_has_expected_value=True,
        budget_available=False,
    )
    assert decision == StopDecision.ESCALATE_OR_DEFER


def test_continue_requires_gap_value_and_budget():
    decision = stopping_decision(
        material_claim_states=[ClaimState.PARTIAL],
        unresolved_high_stakes_gap=False,
        scope_ambiguous=False,
        concrete_next_gap="inspect primary",
        next_action_has_expected_value=True,
        budget_available=True,
    )
    assert decision == StopDecision.CONTINUE


def test_ambiguous_scope_clarifies_first():
    decision = stopping_decision(
        material_claim_states=[ClaimState.UNVERIFIED],
        unresolved_high_stakes_gap=False,
        scope_ambiguous=True,
        concrete_next_gap="search",
        next_action_has_expected_value=True,
        budget_available=True,
    )
    assert decision == StopDecision.CLARIFY_FIRST
