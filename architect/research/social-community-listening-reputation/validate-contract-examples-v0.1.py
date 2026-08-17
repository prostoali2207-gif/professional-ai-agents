#!/usr/bin/env python3
"""Reproducible public development examples for the v0.1 live-context/handoff schema.

Requires jsonschema>=4.18. These cases are visible contract tests, not held-out
behavioral evidence and not a substitute for the sealed CG-06 evaluation.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE / "live-context-and-handoff-contracts.schema.json"
TS = "2026-08-17T09:00:00Z"


ROUTE = {
    "role_key": "community.owner",
    "named_owner": None,
    "backup_role_keys": ["business.owner"],
    "route_reason": "Own the decision",
    "acknowledgment_target_seconds": 900,
    "fallback_after_seconds": 1800,
}

SOURCE = {
    "source_id": "src-001",
    "source_kind": "approved_policy",
    "locator": "policy://community/v1",
    "trust_class": "authorized_context",
    "observed_at": TS,
    "effective_at": TS,
    "expires_at": None,
    "version": "1",
    "owner_role": "community_owner",
    "content_hash": None,
}

LIVE_CONTEXT = {
    "schema_version": "0.1.0",
    "artifact_type": "live_context_packet",
    "binding_id": "ctx-001",
    "organization_id": "org-001",
    "business_scope_id": "scope-001",
    "created_at": TS,
    "effective_at": TS,
    "expires_at": None,
    "owner_role": "business_owner",
    "status": "active",
    "supersedes_binding_id": None,
    "brand": {
        "brand_id": "brand-001",
        "voice_policy_ref": "policy://voice/v1",
        "allowed_claims_policy_ref": "policy://claims/allow/v1",
        "prohibited_claims_policy_ref": "policy://claims/deny/v1",
    },
    "jurisdictions": [
        {
            "jurisdiction_id": "jur-uae",
            "scope": "UAE operations",
            "legal_policy_ref": "policy://legal/uae/v1",
            "verified_at": TS,
            "expires_at": None,
            "owner_role": "legal",
        }
    ],
    "languages": [
        {
            "language": "en",
            "permitted_scope": "Routine and approved factual replies",
            "high_impact_reviewer_route": ROUTE,
        }
    ],
    "roles": [
        {
            "role_key": "community.owner",
            "accountability": "Community decisions",
            "primary_route": ROUTE,
            "out_of_hours_route": None,
            "authority_policy_ref": "policy://authority/v1",
        }
    ],
    "response_targets": [
        {
            "case_class": "complaint",
            "acknowledgment_target_seconds": 3600,
            "resolution_owner_role": "support",
        }
    ],
    "policy_bindings": [
        {
            "policy_key": "moderation.v1",
            "policy_ref": "policy://moderation/v1",
            "version": "1",
            "owner_role": "community_owner",
            "verified_at": TS,
            "expires_at": None,
            "status": "active",
            "supersedes_policy_key": None,
            "source_refs": ["src-001"],
        }
    ],
    "platform_capability_binding_refs": ["platform-001"],
    "runtime_requirements": {
        "required_features": ["structured_output", "state_read_after_write"],
        "structured_output_required": True,
        "persistent_state_required": True,
        "network_requirement": "restricted",
        "human_approval_required": True,
        "side_effect_observability_required": True,
        "acceptable_substitutes": ["manual route"],
        "unsupported_conditions": ["no approval channel"],
    },
    "sources": [SOURCE],
    "conflicts": [],
    "unknowns": [],
}

PLATFORM_CAPABILITY = {
    "schema_version": "0.1.0",
    "artifact_type": "platform_capability_binding",
    "binding_id": "platform-001",
    "organization_id": "org-001",
    "platform": "Example",
    "account_scope_ref": "account://001",
    "channel": "comments",
    "adapter": {
        "adapter_id": "adapter-001",
        "version": "1",
        "runtime": "controlled",
        "permission_scopes": ["read"],
    },
    "verified_at": TS,
    "expires_at": None,
    "owner_role": "channel_owner",
    "sources": [SOURCE],
    "capabilities": [
        {
            "action": "hide",
            "support_status": "supported",
            "permission_status": "approval_only",
            "reversibility": "fully_reversible",
            "verification_method": "read after write",
            "rollback_or_recovery": "unhide",
            "limitations": [],
            "last_observed_at": TS,
        }
    ],
    "limitations": [],
    "fallback_mode": "manual",
    "fallback_route": ROUTE,
}

HANDOFF_BASE = {
    "schema_version": "0.1.0",
    "artifact_type": "handoff_envelope",
    "handoff_id": "handoff-001",
    "correlation_id": "case-001",
    "organization_context_id": "ctx-001",
    "source_role": "community_core",
    "source_artifacts": [
        {
            "artifact_id": "case-001",
            "artifact_type": "community_case",
            "schema_version": "0.1.0",
            "content_hash": None,
        }
    ],
    "target_route": ROUTE,
    "objective": "Obtain an accountable downstream decision",
    "evidence_refs": ["src-001"],
    "facts": [
        {
            "statement": "Customer reported a service issue",
            "status": "asserted",
            "evidence_refs": ["src-001"],
        }
    ],
    "assumptions": [],
    "unknowns": ["Operational cause"],
    "decisions_already_made": [],
    "invariant_constraints": ["Do not promise compensation"],
    "required_output_schema_ref": "schema://downstream/v1",
    "evidence_required": ["Owner decision"],
    "definition_of_done": "Acknowledged decision artifact returned",
    "escalation_condition": "Deadline expires without acknowledgment",
    "priority": "time_sensitive",
    "created_at": TS,
    "deadline_at": None,
    "authority_requested": "analyze",
    "sensitive_data_class": "internal",
    "payload_minimization_note": "Only evidence references transferred",
    "actions_already_taken": ["Public acknowledgment drafted"],
    "actions_not_authorized": ["Compensation promise"],
    "acknowledgment_status": "pending",
    "acknowledged_at": None,
    "acknowledged_by": None,
    "status": "open",
    "idempotency_key": "idem-001",
    "result_artifact_refs": [],
}

HANDOFF_PAYLOADS = [
    {
        "kind": "sales_lead",
        "intent_summary": "Purchase interest",
        "consent_status": "confirmed",
        "contact_ref": "contact-001",
        "requested_next_action": "Qualify lead",
    },
    {
        "kind": "support_case",
        "issue_summary": "Service defect",
        "requested_remedy": "Investigate",
        "operational_fact_refs": ["fact-001"],
    },
    {
        "kind": "analytics_request",
        "decision_question": "Is recurrence material?",
        "metric_or_construct": "unique complaint rate",
        "observation_window": "7 days",
        "coverage_ref": "coverage-001",
    },
    {
        "kind": "market_intelligence_signal",
        "research_question": "Is this issue broader than owned channels?",
        "entities": ["brand"],
        "geography": "UAE",
        "time_scope": "30 days",
        "exclusions": ["owned comments"],
        "inference_limit": "Signal only, not population opinion",
    },
    {
        "kind": "content_strategy_input",
        "community_insight": "Recurring clarification need",
        "decision_use": "Consider educational content",
        "evidence_limitations": ["Observed comments only"],
    },
    {
        "kind": "publisher_action_request",
        "requested_action": "pause",
        "artifact_ref": {
            "artifact_id": "response-001",
            "artifact_type": "approved_response",
            "schema_version": "0.1.0",
            "content_hash": None,
        },
        "channel": "instagram",
        "scope": "Affected scheduled post only",
        "approval_ref": None,
    },
    {
        "kind": "specialist_review",
        "specialty": "legal",
        "issue_summary": "Removal request cites law",
        "scope_or_jurisdiction": "UAE",
        "decision_requested": "Interpret applicable requirement",
    },
    {
        "kind": "incident_decision",
        "trigger": "Credible safety allegation",
        "consequence_if_wrong": "high",
        "decision_requested": "Approve holding response",
        "clock_started_at": TS,
    },
]


def build_cases() -> tuple[list[tuple[str, dict]], list[tuple[str, dict]]]:
    valid = [
        ("live-context", copy.deepcopy(LIVE_CONTEXT)),
        ("platform-capability", copy.deepcopy(PLATFORM_CAPABILITY)),
    ]
    for index, payload in enumerate(HANDOFF_PAYLOADS, start=1):
        handoff = copy.deepcopy(HANDOFF_BASE)
        handoff["handoff_id"] = f"handoff-{index + 10:03}"
        handoff["idempotency_key"] = f"idem-{index + 10:03}"
        handoff["payload"] = payload
        valid.append((f"handoff-{payload['kind']}", handoff))

    missing_minimization = copy.deepcopy(valid[2][1])
    del missing_minimization["payload_minimization_note"]

    forbidden_extra_property = copy.deepcopy(PLATFORM_CAPABILITY)
    forbidden_extra_property["capabilities"][0]["unexpected"] = "x"

    invalid = [
        ("handoff-missing-payload-minimization", missing_minimization),
        ("platform-forbidden-extra-property", forbidden_extra_property),
    ]
    return valid, invalid


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    valid, invalid = build_cases()

    failures: list[str] = []
    for name, instance in valid:
        errors = list(validator.iter_errors(instance))
        if errors:
            failures.append(f"valid:{name}: {errors[0].message}")

    for name, instance in invalid:
        if not list(validator.iter_errors(instance)):
            failures.append(f"invalid:{name}: unexpectedly accepted")

    if failures:
        print("contract_examples=FAIL")
        for failure in failures:
            print(failure)
        return 1

    print("draft2020_schema=PASS")
    print(f"valid_examples={len(valid)} PASS")
    print(f"invalid_examples={len(invalid)} REJECTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
