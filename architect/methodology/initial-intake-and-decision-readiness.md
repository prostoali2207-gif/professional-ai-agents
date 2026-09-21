# Initial Intake and Decision Readiness

Status: v0.1.

## Purpose

Prevent an applied agent from behaving as though a complete professional case already exists when deployment begins with a new user, an underspecified request, stale prior state, or only fragments of a baseline.

This is a general Agent Architect design requirement, not a domain questionnaire.

## Core rule

A material personalized decision requires enough decision-relevant evidence to make that decision.

Before acting:

`entry state -> known context -> missing prerequisites -> information value -> acquire minimum sufficient evidence -> decision readiness -> act / provisional / escalate`.

Do not confuse "the user asked for an answer" with "the decision is ready".

## 1. Entry modes

Model the modes that can occur in the target deployment:

- `COLD_START` — no reliable baseline exists.
- `PARTIAL_BASELINE` — some relevant facts exist, but one or more decision-changing prerequisites are missing.
- `ONGOING` — a current baseline and active plan/state exist.
- `FOLLOW_UP` — new evidence must be compared with a prior decision/intervention.
- `CONFLICTING_STATE` — current user/tool evidence conflicts with stored or earlier context.

Not every agent needs all five modes, but a deployment that can receive first-contact users must not omit `COLD_START`.

## 2. Decision-prerequisite map

Do not create one giant list of "required inputs". Map prerequisites to decisions.

For each material decision classify an input as:

- `SAFETY_CRITICAL` — missingness can make the action unsafe or outside authority.
- `DECISION_CHANGING` — plausible values can reverse or materially alter the recommendation.
- `CALIBRATION_ONLY` — improves precision but normally does not change the action class.
- `OPTIONAL` — useful context with low current decision value.

A field may change class across decisions.

## 3. Intake policy

When information is missing:

1. Recover relevant established context from valid current state first.
2. Do not ask again for a fact that is already reliable and applicable.
3. Ask for the smallest coherent batch of `SAFETY_CRITICAL` and `DECISION_CHANGING` facts.
4. Prefer direct measurements, records, observations and concrete history over labels or stereotypes.
5. Defer calibration-only questions until they become useful.
6. Do not turn the first contact into an exhaustive interview when a smaller intake can unlock the next professional decision.

## 4. Decision readiness

Use three states:

- `READY` — material safety and decision-changing prerequisites are sufficiently resolved.
- `PROVISIONAL` — missing information limits precision but cannot plausibly reverse the bounded action; uncertainty and verification are explicit.
- `BLOCKED_OR_ESCALATE` — a safety-critical or material decision-changing gap remains.

A provisional action must name what is unknown and what later evidence could change it.

## 5. Weak proxies and false premises

The intake itself requires professional judgment.

Do not collect a familiar field merely because users expect it. Ask whether it has decision value.

Reject or translate:
- folk typologies presented as biological categories;
- demographic stereotypes used as substitutes for observed capability/state;
- vague self-labels when concrete history or measurement is available;
- duplicated data already present in valid state.

If a user asks for a weak proxy, explain the more decision-relevant substitute briefly and use that instead.

## 6. Stateful behavior

The first completed baseline should become structured state only when future-useful and sufficiently reliable.

Preserve:
- provenance/source;
- date or applicability window when material;
- uncertainty/estimated status;
- supersession when newer authoritative evidence replaces it.

Do not let stale baseline fields silently control a later decision.

## 7. Architecture ownership

The component that owns the first material decision must also own or explicitly coordinate the prerequisites for that decision.

When several specialists share one user journey, choose the least-complex sufficient architecture:
- a single primary practitioner with routed specialist modules when context is highly shared;
- a small deterministic/router layer when the only missing function is entry-state classification and handoff;
- an orchestrator only when specialist boundaries and handoffs create measurable value.

Do not create a new agent merely to hold a questionnaire.

## 8. Evaluation requirements

When deployment permits first contact, include at least:

1. **Cold-start case** — user asks "what should I do?" with no usable baseline.
2. **Partial-baseline case** — most information exists; one decision-changing fact is missing.
3. **Known-context contrast** — required facts already exist; re-asking them is a failure.
4. **False-proxy case** — user supplies or requests a familiar but weak label; agent replaces it with decision-relevant evidence.
5. **Provisional case** — missing calibration-only information; useful bounded action should proceed.
6. **Blocked case** — missing safety-critical information; material action must not proceed.

The grader should inspect the **trajectory**, not only the final prose: what was recovered, what was asked, whether the questions had decision value, and whether action began before readiness.

## 9. Failure signatures

Treat these as architecture/evaluation failures, not mere style problems:

- starting a personalized plan from a cold start without obtaining decision-changing baseline facts;
- exhaustive intake unrelated to the next decision;
- re-asking reliable known context;
- collecting stereotypes/folk categories while missing direct evidence;
- marking a case "insufficient information" without trying to obtain the minimum sufficient facts;
- giving a confident plan and appending questions afterward;
- allowing separate specialists to ask overlapping baselines because no component owns intake.

## 10. Production-learning trigger

A user correction such as "you started in the middle; you never asked who I am / what my baseline is" should be tested for this failure family.

If reproduced, route the repair to:
1. entry-state/intake architecture;
2. affected applied skill/router;
3. cold-start regression.

Do not patch only the observed wording.
