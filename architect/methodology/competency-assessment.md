# Competency Assessment

Status: v0.1.

## Purpose

Competence is demonstrated performance in context, not possession of terminology. Agent Architect therefore evaluates observable professional behavior through representative tasks, artifacts, decisions, and recovery—not only question answering.

## Assessment model

For each competency define five layers:

1. **Knowledge** — understands relevant concepts, constraints, standards, and evidence.
2. **Application** — applies them to a representative task.
3. **Diagnosis** — identifies why an existing result is weak or failing.
4. **Judgment** — resolves ambiguity, exceptions, and conflicting principles.
5. **Verification** — obtains evidence that the chosen action actually worked.

Passing knowledge alone never establishes professional competence.

## Authenticity dimensions

A practical test should approximate deployment along the dimensions that matter for the role:

- task ambiguity;
- information quality;
- available tools;
- time horizon;
- multiple intermediate decisions;
- environmental state;
- stakeholder constraints;
- real artifacts;
- consequences of error;
- need for verification and recovery.

Not every test must reproduce production, but the suite must expose the same cognitive demands.

## Competency unit

Each core capability should have a record containing:

- name;
- professional purpose;
- representative situations;
- prerequisite knowledge;
- observable behaviors;
- expert-vs-average discriminators;
- cues/information used;
- decision model;
- trade-offs/exceptions;
- tools;
- evidence of success;
- failure modes;
- professional boundary;
- practical test;
- adversarial test;
- criticality/severity.

## Test families

### Knowledge probe

Useful only to verify prerequisites. It should not dominate the score.

### Application task

The agent produces or changes a real artifact under realistic constraints.

### Diagnosis task

The agent inspects flawed work where the stated explanation may be wrong. It must identify root cause rather than merely restyle symptoms.

### Critique task

The agent evaluates another practitioner's work against evidence and professional criteria.

### Conflicting-principles task

Two valid principles point toward different actions. The agent must expose the trade-off and choose based on context.

### Incomplete-information task

Critical information is missing. The agent must identify what is unknown and obtain, request, test, or escalate rather than hallucinating.

### Adversarial premise task

The user or upstream agent confidently supplies a weak or false premise. The agent must challenge it when material.

### Recovery task

The first approach fails or a tool returns contradictory evidence. The agent must diagnose, update its model of the situation, and recover.

### Boundary task

The task crosses into another profession or exceeds validated competence. The agent must route or escalate correctly.

## Mastery evidence

A competency is considered provisionally demonstrated only when the agent can succeed across multiple forms of evidence rather than one memorized example.

Strong evidence can include:

- correct executable result;
- direct downstream state;
- artifact judged by calibrated domain experts;
- consistent performance across paraphrased/novel cases;
- correct tool/evidence trajectory;
- successful diagnosis of a deliberately misleading case;
- appropriate refusal/escalation.

## Anti-gaming rules

Design evals so that superficial language cannot substitute for competence.

Examples:

- require the agent to inspect the render rather than say it would;
- require a persisted database record rather than a success message;
- provide distractor sources and check source selection;
- change irrelevant surface details while preserving the underlying decision;
- test the same competency in both creation and critique modes;
- withhold a key fact and ensure the agent notices its absence.

## Coverage matrix

Track each core competency against required evidence types.

| Competency | Knowledge | Apply | Diagnose | Judgment | Verify | Adversarial | Recovery |
|---|---:|---:|---:|---:|---:|---:|---:|
| Example | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Critical competencies should not have empty columns without a documented reason.

## Release rule

An agent can fail readiness even with a high aggregate score when a critical professional capability is untested or fails. Coverage holes are treated as uncertainty, not assumed competence.

## Quality gate

Competency assessment passes when:

- competencies are observable rather than topic labels;
- practical tasks resemble real work;
- the suite tests diagnosis, judgment, verification, and recovery;
- weak premises and missing information are adversarially tested;
- professional boundaries are tested;
- graders are calibrated for judgment-heavy criteria;
- critical capabilities cannot be hidden by aggregate scoring.
