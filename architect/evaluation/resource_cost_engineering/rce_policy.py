from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class Decision(str, Enum):
    ALLOW = "ALLOW"
    DOWNGRADE = "DOWNGRADE"
    TARGET = "TARGET"
    DEFER = "DEFER"
    BLOCK = "BLOCK"


@dataclass
class ResourceVector:
    model_calls: float = 0
    input_tokens: float = 0
    output_tokens: float = 0
    api_credits: float = 0
    compute_minutes: float = 0
    ci_minutes: float = 0
    storage_gb_hours: float = 0
    network_gb: float = 0
    human_minutes: float = 0

    def exceeds(self, other: "ResourceVector") -> List[str]:
        return [k for k in self.__dataclass_fields__ if getattr(self, k) > getattr(other, k)]

    def minus(self, other: "ResourceVector") -> "ResourceVector":
        return ResourceVector(**{k: max(0.0, getattr(self, k) - getattr(other, k)) for k in self.__dataclass_fields__})


@dataclass
class FreshnessState:
    checked_at: Optional[str]
    max_age_hours: Optional[float]
    source_authoritative: bool = True
    account_specific: bool = False

    def is_fresh(self, now: datetime) -> bool:
        if self.checked_at is None or self.max_age_hours is None:
            return False
        try:
            dt = datetime.fromisoformat(self.checked_at.replace("Z", "+00:00"))
        except ValueError:
            return False
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        age = (now - dt.astimezone(timezone.utc)).total_seconds() / 3600
        return 0 <= age <= self.max_age_hours


@dataclass
class GateInput:
    run_id: str
    objective: str
    decision_to_change: str
    risk_class: str
    required_quality_floor: str
    estimate: ResourceVector
    remaining: ResourceVector
    protected_reserve: ResourceVector = field(default_factory=ResourceVector)
    recovery_reserve: ResourceVector = field(default_factory=ResourceVector)
    hard_cap: Optional[ResourceVector] = None
    deterministic_answer_available: bool = False
    fresh_reusable_evidence_available: bool = False
    expected_information_gain: Optional[str] = None
    stop_condition: Optional[str] = None
    midrun_exhaustion_plan: Optional[str] = None
    pricing_material_to_decision: bool = False
    pricing_freshness: Optional[FreshnessState] = None
    quota_material_to_decision: bool = False
    quota_freshness: Optional[FreshnessState] = None
    provider_eligible_privacy: bool = True
    provider_eligible_authority: bool = True
    provider_eligible_reliability: bool = True
    full_suite: bool = False
    affected_scope_known: bool = False
    targeted_regression_available: bool = False
    release_gate: bool = False
    explicit_release_override: bool = False
    alternative_direct_strong_is_lower_total_cost: bool = False
    chosen_is_direct_strong: bool = False


@dataclass
class GateResult:
    decision: Decision
    reasons: List[str]
    spendable: ResourceVector


def evaluate_gate(g: GateInput, now: Optional[datetime] = None) -> GateResult:
    now = now or datetime.now(timezone.utc)
    reasons: List[str] = []
    if not g.objective.strip() or not g.decision_to_change.strip():
        return GateResult(Decision.BLOCK, ["missing_objective_or_decision"], ResourceVector())
    if not g.expected_information_gain:
        return GateResult(Decision.BLOCK, ["no_expected_information_gain"], ResourceVector())
    if g.deterministic_answer_available:
        return GateResult(Decision.BLOCK, ["deterministic_evidence_already_sufficient"], ResourceVector())
    if g.fresh_reusable_evidence_available:
        return GateResult(Decision.BLOCK, ["fresh_reusable_evidence_already_sufficient"], ResourceVector())
    if not (g.provider_eligible_privacy and g.provider_eligible_authority and g.provider_eligible_reliability):
        return GateResult(Decision.BLOCK, ["provider_ineligible"], ResourceVector())
    if g.pricing_material_to_decision:
        if not g.pricing_freshness or not g.pricing_freshness.source_authoritative or not g.pricing_freshness.is_fresh(now):
            return GateResult(Decision.DEFER, ["pricing_state_unverified_or_stale"], ResourceVector())
    if g.quota_material_to_decision:
        if not g.quota_freshness or not g.quota_freshness.is_fresh(now):
            return GateResult(Decision.DEFER, ["quota_state_unverified_or_stale"], ResourceVector())
    if not g.stop_condition or not g.midrun_exhaustion_plan:
        return GateResult(Decision.BLOCK, ["unsafe_execution_without_stop_or_exhaustion_plan"], ResourceVector())

    spendable = g.remaining.minus(g.protected_reserve).minus(g.recovery_reserve)
    if g.hard_cap:
        cap_exceeded = g.estimate.exceeds(g.hard_cap)
        if cap_exceeded and not (g.release_gate and g.explicit_release_override):
            return GateResult(Decision.BLOCK, [f"hard_cap_exceeded:{','.join(cap_exceeded)}"], spendable)
        if cap_exceeded:
            reasons.append("explicit_release_override")

    reserve_exceeded = g.estimate.exceeds(spendable)
    if reserve_exceeded and not (g.release_gate and g.explicit_release_override):
        return GateResult(Decision.BLOCK, [f"protected_reserve_would_be_consumed:{','.join(reserve_exceeded)}"], spendable)
    if reserve_exceeded:
        reasons.append("explicit_release_override_consumes_reserve")

    if g.full_suite and g.affected_scope_known and g.targeted_regression_available and not g.release_gate:
        return GateResult(Decision.TARGET, ["targeted_regression_precedes_full_suite"], spendable)
    if g.alternative_direct_strong_is_lower_total_cost and not g.chosen_is_direct_strong:
        return GateResult(Decision.DOWNGRADE, ["chosen_cascade_not_total_cost_optimal"], spendable)
    return GateResult(Decision.ALLOW, reasons or ["eligible_and_budgeted"], spendable)


def post_run_accounting(record: Dict[str, Any]) -> Dict[str, Any]:
    flags: List[str] = []
    planned = ResourceVector(**record.get("planned_resources", {}))
    actual = ResourceVector(**record.get("actual_resources", {}))
    decision_changed = record.get("decision_before") != record.get("decision_after")
    new_information = bool(record.get("new_information"))
    evidence = bool(record.get("evidence_produced"))
    material_actual = (actual.model_calls + actual.api_credits + actual.compute_minutes + actual.ci_minutes + actual.human_minutes) > 0
    if material_actual and not new_information and not evidence and not decision_changed:
        flags.append("high_or_material_spend_low_information")
    if record.get("unchanged_candidate") and record.get("repeated_same_hypothesis"):
        flags.append("duplicate_run_without_new_hypothesis")
    if record.get("full_suite") and record.get("affected_scope_only"):
        flags.append("full_suite_when_targeted_regression_sufficient")
    if record.get("deterministic_equivalent") and record.get("llm_grader_used"):
        flags.append("llm_used_for_deterministic_predicate")
    if int(record.get("retry_count", 0)) > int(record.get("retry_budget", 0)):
        flags.append("retry_budget_exceeded")
    variance = {k: getattr(actual, k) - getattr(planned, k) for k in planned.__dataclass_fields__}
    return {"variance_from_plan": variance, "waste_signal": flags, "decision_changed": decision_changed}
