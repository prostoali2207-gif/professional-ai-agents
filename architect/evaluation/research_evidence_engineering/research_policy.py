from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ClaimState(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    CONFLICTED = "CONFLICTED"
    CONTRADICTED = "CONTRADICTED"
    UNVERIFIED = "UNVERIFIED"
    NOT_COMPARABLE = "NOT_COMPARABLE"


class AccessState(str, Enum):
    FULL = "FULL"
    PARTIAL = "PARTIAL"
    METADATA_ONLY = "METADATA_ONLY"
    SNIPPET_ONLY = "SNIPPET_ONLY"
    INACCESSIBLE = "INACCESSIBLE"


class StopDecision(str, Enum):
    STOP = "STOP"
    CONTINUE = "CONTINUE"
    CLARIFY_FIRST = "CLARIFY_FIRST"
    STOP_WITH_LIMITATION = "STOP_WITH_LIMITATION"
    ESCALATE_OR_DEFER = "ESCALATE_OR_DEFER"


class FailureClass(str, Enum):
    EVIDENCE_BEHAVIOR = "EVIDENCE_BEHAVIOR"
    AUTH_CONFIG = "AUTH_CONFIG"
    RATE_LIMIT_SHORT = "RATE_LIMIT_SHORT"
    DAILY_QUOTA_EXHAUSTED = "DAILY_QUOTA_EXHAUSTED"
    CAPACITY_TRANSIENT = "CAPACITY_TRANSIENT"
    PROVIDER_OUTAGE = "PROVIDER_OUTAGE"
    MODEL_LIFECYCLE = "MODEL_LIFECYCLE"


@dataclass
class ResearchContract:
    decision: str
    material_claims: List[str]
    stakes: str
    jurisdiction: Optional[str] = None
    population: Optional[str] = None
    version: Optional[str] = None
    freshness_required: bool = False
    confidentiality_constraints: List[str] = field(default_factory=list)
    unresolved_gaps: List[str] = field(default_factory=list)
    stop_condition: Optional[str] = None
    max_external_calls: Optional[int] = None
    remaining_external_calls: Optional[int] = None
    protected_external_call_reserve: int = 0


@dataclass
class EvidenceRecord:
    claim_id: str
    source_identity: str
    source_class: str
    authority_basis: str
    access_state: AccessState
    lifecycle_state: str = "CURRENT_OR_UNKNOWN"
    canonical_parent: Optional[str] = None
    method_common_cause: Optional[str] = None
    same_construct: bool = True
    same_population: bool = True
    same_condition: bool = True
    same_metric: bool = True
    same_lifecycle: bool = True
    citation_entails_claim: Optional[bool] = None

    @property
    def inspectable_for_material_claim(self) -> bool:
        return self.access_state in {AccessState.FULL, AccessState.PARTIAL}

    @property
    def comparable(self) -> bool:
        return all(
            [
                self.same_construct,
                self.same_population,
                self.same_condition,
                self.same_metric,
                self.same_lifecycle,
            ]
        )


@dataclass
class RouteInput:
    known_official_url: bool = False
    authority_sensitive: bool = False
    long_document: bool = False
    scholarly_identity: bool = False
    concrete_gap: Optional[str] = None
    provider_health_ok: bool = True
    provider_quota_available: bool = True
    provider_eligible: bool = True
    expected_decision_value: bool = True
    estimated_external_calls: int = 1
    remaining_external_calls: Optional[int] = None
    protected_external_call_reserve: int = 0


@dataclass
class RouteDecision:
    allowed: bool
    route_class: str
    reasons: List[str]


def validate_contract(contract: ResearchContract) -> List[str]:
    errors: List[str] = []
    if not contract.decision.strip():
        errors.append("missing_decision")
    if not contract.material_claims:
        errors.append("missing_material_claims")
    if not contract.stakes.strip():
        errors.append("missing_stakes")
    if not contract.stop_condition:
        errors.append("missing_stop_condition")
    if contract.max_external_calls is not None and contract.max_external_calls < 0:
        errors.append("invalid_max_external_calls")
    if contract.protected_external_call_reserve < 0:
        errors.append("invalid_protected_reserve")
    return errors


def choose_route(r: RouteInput) -> RouteDecision:
    if not r.concrete_gap:
        return RouteDecision(False, "NONE", ["no_concrete_evidence_gap"])
    if not r.provider_eligible:
        return RouteDecision(False, "NONE", ["provider_or_route_ineligible"])
    if not r.expected_decision_value:
        return RouteDecision(False, "NONE", ["insufficient_expected_decision_value"])
    if not r.provider_health_ok:
        return RouteDecision(False, "FALLBACK_OR_DEFER", ["provider_health_failure"])
    if not r.provider_quota_available:
        return RouteDecision(False, "FALLBACK_OR_DEFER", ["provider_quota_unavailable"])
    if r.remaining_external_calls is not None:
        spendable = max(0, r.remaining_external_calls - r.protected_external_call_reserve)
        if r.estimated_external_calls > spendable:
            return RouteDecision(False, "DEFER_OR_ESCALATE", ["protected_reserve_would_be_consumed"])

    if r.known_official_url:
        return RouteDecision(True, "DIRECT_PRIMARY_INSPECTION", ["known_official_url"])
    if r.scholarly_identity:
        return RouteDecision(True, "IDENTIFIER_OR_SCHOLARLY_VERIFICATION", ["identity_or_lifecycle_check"])
    if r.long_document:
        return RouteDecision(True, "LONG_DOCUMENT_EXTRACTION_ADAPTER", ["document_extraction_required"])
    if r.authority_sensitive:
        return RouteDecision(True, "AUTHORITY_DISCOVERY_ADAPTER", ["authority_sensitive_discovery"])
    return RouteDecision(True, "GENERAL_DISCOVERY_ADAPTER", ["eligible_gap_targeted_route"])


def independent_evidence_count(records: List[EvidenceRecord]) -> int:
    seen = set()
    count = 0
    for rec in records:
        lineage_root = rec.canonical_parent or rec.source_identity
        method_root = rec.method_common_cause or rec.source_identity
        key = (lineage_root, method_root)
        if key not in seen:
            seen.add(key)
            count += 1
    return count


def adjudicate_claim(records: List[EvidenceRecord], high_stakes: bool = False) -> ClaimState:
    if not records:
        return ClaimState.UNVERIFIED

    current = [r for r in records if r.lifecycle_state not in {"RETRACTED", "WITHDRAWN", "SUPERSEDED"}]
    if not current:
        return ClaimState.UNVERIFIED

    inspectable = [r for r in current if r.inspectable_for_material_claim]
    if not inspectable:
        return ClaimState.UNVERIFIED

    if any(not r.comparable for r in inspectable):
        return ClaimState.NOT_COMPARABLE

    entailments = [r.citation_entails_claim for r in inspectable if r.citation_entails_claim is not None]
    if any(v is False for v in entailments) and any(v is True for v in entailments):
        return ClaimState.CONFLICTED
    if entailments and all(v is False for v in entailments):
        return ClaimState.CONTRADICTED
    if entailments and all(v is True for v in entailments):
        if high_stakes and independent_evidence_count(inspectable) < 2:
            return ClaimState.PARTIAL
        return ClaimState.SUPPORTED
    return ClaimState.UNVERIFIED


def retry_allowed(
    failure: FailureClass,
    retries_used: int,
    retry_budget: int,
    concrete_gap_remains: bool,
    budget_and_quota_allow: bool,
) -> bool:
    if failure in {
        FailureClass.EVIDENCE_BEHAVIOR,
        FailureClass.AUTH_CONFIG,
        FailureClass.DAILY_QUOTA_EXHAUSTED,
        FailureClass.MODEL_LIFECYCLE,
    }:
        return False
    return (
        concrete_gap_remains
        and budget_and_quota_allow
        and retries_used < retry_budget
        and failure in {
            FailureClass.RATE_LIMIT_SHORT,
            FailureClass.CAPACITY_TRANSIENT,
            FailureClass.PROVIDER_OUTAGE,
        }
    )


def stopping_decision(
    *,
    material_claim_states: List[ClaimState],
    unresolved_high_stakes_gap: bool,
    scope_ambiguous: bool,
    concrete_next_gap: Optional[str],
    next_action_has_expected_value: bool,
    budget_available: bool,
) -> StopDecision:
    if scope_ambiguous:
        return StopDecision.CLARIFY_FIRST

    complete_states = {ClaimState.SUPPORTED, ClaimState.CONTRADICTED}
    if material_claim_states and all(s in complete_states for s in material_claim_states):
        return StopDecision.STOP

    if unresolved_high_stakes_gap and not budget_available:
        return StopDecision.ESCALATE_OR_DEFER

    if concrete_next_gap and next_action_has_expected_value and budget_available:
        return StopDecision.CONTINUE

    if unresolved_high_stakes_gap:
        return StopDecision.ESCALATE_OR_DEFER

    return StopDecision.STOP_WITH_LIMITATION
