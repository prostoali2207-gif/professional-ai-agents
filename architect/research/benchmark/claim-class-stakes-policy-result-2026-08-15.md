# Claim-Class + Stakes-Aware Evidence Policy — Result (2026-08-15)

## Verdict

**STRUCTURAL PASS — 9/9 frozen cases.**

This gate validates a routing/abstention scaffold, not domain-specific legal, medical, engineering, or scientific professional standards.

## What passed

The policy correctly distinguished evidence requirements for:

- legal/regulatory claims;
- medical/safety claims;
- safety-critical engineering claims;
- scientific/benchmark claims;
- current product/platform facts;
- low-stakes product hypotheses.

The frozen cases verified that the same evidence packet must not receive the same status across all claim classes. Examples include:

- a blog cannot establish a current legal/regulatory requirement;
- current regulator/official evidence can support a jurisdiction-resolved legal fact;
- one primary medical study is insufficient for a patient-specific/high-risk conclusion;
- a superseded engineering standard cannot establish a current safety-critical requirement;
- non-comparable scientific metrics force abstention even with multiple primary sources;
- old community posts cannot establish current platform state;
- live official product documentation can support a current product fact;
- one experiment can provide PARTIAL evidence for a low-stakes product hypothesis without being promoted to a universal fact.

## Required architecture behavior

Claim evaluation must first classify the claim and decision context, then apply a domain/stakes evidence profile. It must not apply one global `SUPPORTED` threshold.

At minimum the routing object should carry:

- claim class;
- harm severity / stakes;
- reversibility of the decision;
- jurisdiction where applicable;
- user- or patient-specificity where applicable;
- decision horizon / freshness requirement;
- lifecycle/version requirement;
- required source authority classes;
- replication/diversity requirement;
- expert-escalation condition;
- mandatory abstention conditions.

## Expert-gap discovery

A strong practitioner would notice that **claim class is not enough**. Two claims in the same class can have radically different evidence requirements depending on harm severity, reversibility, population/person specificity, jurisdiction and timing.

Freshness should not be encoded as a universal age cutoff. It should be represented as lifecycle/version requirements appropriate to the claim: current law, current product plan, matching engineering standard version, benchmark version, current clinical guidance, etc.

High-stakes retrieval success also does not remove the need for professional escalation. A research layer can establish evidence status; it must not impersonate a licensed or accountable professional when interpretation or action requires one.

## Red-team

**Senior researcher:** would reject any universal threshold table that ignores study design quality, domain conventions and heterogeneous evidence hierarchies.

**Information-retrieval engineer:** would reject using retrieval score or provider confidence as evidence adequacy.

**Evaluation scientist:** would require domain-adjudicated cases before claiming cross-domain validity. Current result proves the architecture/scaffold, not universal domain calibration.

**Security engineer:** would require claim-class/stakes assignment to be made by trusted orchestration policy, not by retrieved content or tool metadata. A hostile source must not be able to downgrade a high-stakes claim into a low-stakes class.

## Scoped conclusion

Use this as a **policy interface** with domain-specific profiles, not as a hard-coded universal evidence doctrine.

The next unresolved layer is **trusted claim/stakes classification and escalation**: how the system prevents under-classification of stakes, handles mixed/multi-claim questions, and routes uncertain classifications conservatively without turning every task into a high-cost high-stakes workflow.
