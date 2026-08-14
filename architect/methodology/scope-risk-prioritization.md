# Scope and Risk Prioritization

Status: v0.1.

## Problem

Professional reconstruction can expand indefinitely because real professions overlap with adjacent disciplines. Agent Architect therefore needs a principled stopping rule: include enough neighboring competence to protect outcomes, but do not model every adjacent profession at equal depth.

## Core rule

Depth is determined by decision criticality, coupling, reversibility, and evidence—not by whether a topic is traditionally considered 'inside' the profession.

## 1. Classify each adjacent competency

For every discovered neighboring competency, classify it as one of:

- `CORE`: the role cannot perform credibly without it;
- `BOUNDARY-CRITICAL`: the role need not master the whole discipline but must recognize, reason about, and protect the interface;
- `ESCALATION`: the role must detect when specialist involvement is required;
- `OPTIONAL/CONTEXTUAL`: only needed in specific products/domains;
- `OUT-OF-SCOPE`: no meaningful effect on the role's decisions or outcomes.

## 2. Priority factors

Increase modeling depth when one or more are high:

- severity if wrong;
- frequency of the decision;
- irreversibility/cost of rollback;
- coupling to downstream systems;
- likelihood that users omit the requirement;
- historical incidence of failures;
- difficulty of detecting the mistake after the fact;
- legal/safety/security/privacy impact;
- volatility of required knowledge;
- degree of tacit professional judgment.

## 3. Boundary competency pattern

A role does not need to become a full specialist in every adjacent field. It may instead need:

- enough conceptual knowledge to detect risk;
- a decision rule for when the boundary matters;
- the evidence/tool needed for a preliminary check;
- explicit escalation criteria;
- preservation of the downstream specialist's contract.

Example: a frontend engineer does not become a penetration tester, but must understand client-side trust boundaries, avoid common unsafe patterns, recognize when a security review is warranted, and not destroy security controls.

## 4. Stop rule

Stop expanding a competency when the current architecture can reliably answer all of:

1. What decisions in the agent's work depend on this competency?
2. What failure occurs if it is absent?
3. What minimum knowledge/judgment is needed to protect those decisions?
4. What evidence verifies the outcome?
5. When must the agent escalate instead of deciding itself?

If an adjacent discipline cannot be connected to a material decision, failure, evidence loop, or escalation boundary, it should normally not receive deep modeling.

## 5. Risk-tiered evaluation

Evaluation depth should track consequence:

- low-risk/reversible: representative tests may be sufficient;
- medium-risk: regression + adversarial cases + direct verification;
- high-risk: independent review, stronger evidence, specialist escalation, deployment monitoring, and explicit go/no-go gates.

## 6. Anti-patterns

Avoid:

- profession maximalism: modeling everything because it might someday matter;
- title literalism: excluding important knowledge because another profession 'owns' it;
- checklist minimalism: including a one-line warning without enough knowledge to detect the risk;
- specialist cosplay: pretending the primary agent can replace a deep specialist after reading a short reference file;
- equal-depth architecture: allocating the same knowledge/eval effort to low- and high-consequence competencies.

## Quality gate

Scope architecture passes when a reviewer can explain why each material competency is core, boundary-critical, escalation-only, contextual, or excluded, and when the depth of modeling is proportional to consequence and coupling.