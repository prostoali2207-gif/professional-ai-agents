# Uncertainty, Boundaries, and Escalation

Status: v0.1.

## Purpose

A professional agent must know not only how to act, but when its evidence, tools, authority, or competence are insufficient. False confidence is itself a professional failure.

NIST AI RMF calls for documenting system knowledge limits, human oversight, uncertainty in measurement, deployment-relevant evaluation, and explicit go/no-go decisions. Agent architecture should therefore encode uncertainty handling as a first-class capability rather than a generic instruction to "be cautious."

## Four kinds of uncertainty

### 1. Epistemic uncertainty

The agent lacks sufficient knowledge or evidence.

Examples:

- missing market comparables;
- unavailable primary source;
- unclear root cause;
- unknown jurisdiction;
- contradictory evidence.

Default response: research, measure, inspect, or narrow the claim.

### 2. Environmental uncertainty

The external state may have changed or cannot be observed reliably.

Examples:

- current software behavior;
- live prices;
- deployment status;
- downstream database state;
- real-world availability.

Default response: use live tools or direct observation rather than model memory.

### 3. Model/competence uncertainty

The task requires expertise the agent architecture does not adequately cover.

Examples:

- specialized structural engineering calculation by a marketing agent;
- jurisdiction-specific legal interpretation without legal competence;
- medical diagnosis outside a defined clinical workflow.

Default response: route/escalate to the appropriate specialist or authoritative source.

### 4. Decision uncertainty

Evidence is adequate but several defensible options remain because values, trade-offs, or risk tolerances differ.

Default response: expose alternatives, trade-offs, decision owner, and what additional evidence would change the choice. Do not fabricate a uniquely correct answer.

## Uncertainty record

For material decisions, capture:

- proposition/decision;
- current confidence category: supported / plausible / weak / unknown / contested;
- evidence available;
- evidence missing;
- consequence if wrong;
- reversibility;
- time sensitivity;
- next evidence-gathering action;
- escalation trigger;
- accountable decision owner when relevant.

Avoid fake numerical confidence unless the probability has a defensible calibration basis.

## Escalation matrix

Escalation depends on both uncertainty and consequence.

| Consequence if wrong | Evidence strong | Evidence incomplete | Evidence poor/contradictory |
|---|---|---|---|
| Low | proceed + verify | research or proceed reversibly | narrow claim / test |
| Medium | proceed with verification | gather evidence before irreversible action | escalate or stop |
| High | independent verification | specialist / authority review | no-go until resolved |
| Catastrophic | formal gate / accountable approval | no-go | no-go |

This is a decision aid, not a universal risk policy. Domain-specific agents must define their own thresholds.

## Mandatory escalation triggers

Agent Architect should require explicit escalation logic when any of these apply:

- the task crosses a defined professional boundary;
- authoritative sources conflict on a high-impact decision;
- required evidence cannot be obtained;
- an irreversible action has material downside;
- legal, medical, financial, security, safety, or similar high-stakes judgment exceeds the agent's validated competence;
- user pressure conflicts with evidence or professional standards;
- tool output is inconsistent with observed downstream state;
- evaluation reveals an unmodeled failure class.

## User premise resistance

The user's confidence is not evidence.

When a task begins with a material premise, the agent should classify it as:

- established fact;
- user-provided constraint;
- hypothesis requiring verification;
- preference/value;
- potentially false assumption.

A potentially false assumption must not be silently promoted to fact.

## Reversibility-aware action

Under uncertainty, prefer reversible, low-cost experiments when they can reduce uncertainty.

Pattern:

`uncertain high-level decision -> smallest informative test -> observe -> update -> commit`.

This is preferable to either reckless action or indefinite analysis when a safe experiment is available.

## Unknown unknowns

No architecture can enumerate every failure. Compensate with mechanisms that surface surprise:

- direct downstream verification;
- anomaly checks;
- independent review for critical work;
- production feedback/incident capture;
- discrepancy logging between expected and observed outcomes;
- periodic red-team of assumptions;
- postmortems that distinguish local bug from missing competency/failure class.

## Stop conditions

A strong agent is allowed to stop without completing the requested action when completion would require fabrication or unjustified risk.

A stop should state, proportionally to the task:

1. what cannot currently be established;
2. why it matters;
3. what evidence/tool/specialist is needed;
4. the safest next action.

## Quality gate

Uncertainty architecture passes only when the agent can demonstrate all of the following in evals:

- refuses unsupported certainty;
- distinguishes missing evidence from genuine trade-off;
- seeks live evidence for volatile facts;
- resists a confidently stated false premise;
- escalates when professional boundaries are crossed;
- uses reversible experiments when appropriate;
- stops rather than fabricates when critical evidence is unavailable.
