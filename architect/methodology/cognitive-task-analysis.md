# Cognitive Task Analysis for Agent Architecture

Status: v0.1.

## Purpose

Agent Architect must reconstruct how strong practitioners actually perceive, decide, recover, and verify—not merely collect job-description topics.

Cognitive Task Analysis (CTA) is used to surface otherwise hidden decision processes, especially in non-routine work. The Critical Decision Method (CDM) is preferred when real expert incidents are available because it probes decision points, cues, alternatives, uncertainty, and adaptations.

## Core rule

Do not infer tacit expertise from generic competency lists when direct evidence from expert work, incidents, artifacts, or observation is available.

## Evidence hierarchy for profession mining

1. Direct observation of expert work in representative tasks.
2. Critical incident / Critical Decision Method interviews with strong practitioners.
3. Expert-produced artifacts plus retrospective explanation.
4. High-quality training standards and competency frameworks.
5. Professional literature describing expert practice.
6. Job descriptions and generic skill lists only as low-confidence recall aids.

No single source type is sufficient for a complex profession.

## CTA workflow

### 1. Define the work boundary

Specify:

- task family;
- operating environment;
- stakes;
- common and non-routine cases;
- available tools and information;
- downstream consequences;
- what counts as success and failure.

### 2. Sample representative situations

Include more than routine success cases. Prefer a portfolio containing:

- routine task;
- ambiguous task;
- time-pressured task;
- conflicting-goal task;
- failure/recovery case;
- rare but high-impact case.

### 3. Reconstruct the timeline

For each incident or task, record observable events and decision points. Do not collapse the account into a post-hoc summary too early.

### 4. Probe key decision points

For each decision point extract:

- goals at that moment;
- cues noticed;
- cues ignored;
- interpretation of cues;
- information sought;
- uncertainty;
- options considered;
- option rejected and why;
- trade-offs;
- expectations/predictions;
- prior experience or pattern recognition involved;
- what would have changed the decision;
- likely novice error;
- recovery path if the decision proved wrong.

### 5. Separate report from inference

Tag findings as:

- `observed` — directly visible in behavior/artifacts;
- `reported` — practitioner stated it;
- `inferred` — analyst reconstruction;
- `corroborated` — supported by multiple independent signals;
- `contested` — experts disagree materially.

Retrospective verbal reports are not treated as literal access to cognition. AHRQ notes that recall, analyst skill, and participant quality can affect CTA/CDM data.

### 6. Extract reusable cognitive demands

Convert incidents into capabilities such as:

- cue discrimination;
- anomaly detection;
- prioritization under constraint;
- mental simulation;
- trade-off resolution;
- adaptive planning;
- uncertainty management;
- escalation;
- verification;
- recovery.

Do not encode one-off incident details as universal rules.

### 7. Triangulate

A material expert heuristic should be checked against at least one independent source where feasible: another practitioner, direct artifact evidence, standard, empirical research, or repeated task performance.

## Tacit expertise mining

Tacit expertise often appears as fast recognition or "obvious" judgment. Probe the hidden structure behind it.

Useful probes:

- What made this case feel different?
- What did you notice first?
- What would a junior likely focus on instead?
- At what point did you know the initial approach was wrong?
- Which weak signal mattered most?
- What information did you deliberately not collect?
- Which rule did you violate, and why was that justified?
- What would have made you escalate rather than continue?
- What failure were you actively trying to prevent?

The output must be a testable capability or decision model, not folklore.

## Expert-vs-average discriminator

For each important decision, record:

| Dimension | Average behavior | Strong practitioner behavior | Evidence |
|---|---|---|---|
| Cue selection | | | |
| Problem framing | | | |
| Alternatives | | | |
| Trade-offs | | | |
| Uncertainty | | | |
| Verification | | | |
| Recovery | | | |

If the distinction cannot be supported, mark it as a hypothesis and create an eval rather than presenting it as fact.

## Failure modes

- interviewing only articulate experts and mistaking verbal fluency for competence;
- asking for abstract rules instead of reconstructing real decisions;
- overfitting to memorable incidents;
- converting an expert preference into a universal principle;
- ignoring environmental tools and information sources;
- failing to capture recovery behavior;
- treating self-report as ground truth;
- missing disagreement between experts;
- copying a competency framework without validating it against real work.

## Quality gate

Profession mining passes only when the architecture can answer:

1. What decisions actually make the role difficult?
2. Which cues distinguish strong from weak performance?
3. Which knowledge supports those decisions?
4. Which trade-offs and exceptions require judgment?
5. How does the practitioner detect and recover from error?
6. What evidence shows these claims describe real professional work?

If those questions are unanswered, SKILL authoring is premature.
