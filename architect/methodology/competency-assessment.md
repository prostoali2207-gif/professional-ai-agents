# Competency Assessment

Status: v0.2.

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

## Evidence-centered inference chain

Do not jump from `the agent passed a task` to `the agent possesses the competency` without an evidence model.

For every critical competency connect four elements:

`competency/proficiency claim -> observable evidence -> task/situation that elicits the evidence -> grader/verifier that can distinguish pass from shortcut`.

This adapts the core logic of Evidence-Centered Design: define what capability is claimed, what observations would warrant that inference, and what tasks can reliably produce those observations.

Ask:

- Which behavior is diagnostic of the competency rather than generic fluency?
- Could a weak agent produce the same visible answer through memorization, leakage, lucky guessing, or an invalid process?
- Which alternative explanations for success must the task eliminate?
- Is the observed evidence broad enough to support the claimed scope of competence?

A benchmark score is evidence only for the construct actually elicited by its tasks.

## Authenticity dimensions

A practical test should approximate deployment along the dimensions that matter for the role:

- task ambiguity;
- information quality;
- available tools;
- time horizon;
- multiple intermediate decisions;
- environmental state;
- stakeholder/work-context constraints;
- real artifacts;
- consequences of error;
- need for verification and recovery;
- session/state continuity when material.

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
- alternative explanations/shortcuts the eval must exclude;
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

### Stateful task

For long-horizon or multi-session roles, the agent must preserve, update, supersede, or deliberately forget decision-relevant state across turns/restarts without importing unsupported memories.

### Security/trust task

For agents exposed to untrusted content, the task contains data that attempts to become instruction or authority. Passing requires useful task completion while preserving the trust boundary.

## Mastery evidence

A competency is considered provisionally demonstrated only when the agent can succeed across multiple forms of evidence rather than one memorized example.

Strong evidence can include:

- correct executable result;
- direct downstream state;
- artifact judged by calibrated domain experts;
- consistent performance across paraphrased/novel cases;
- correct tool/evidence trajectory;
- successful diagnosis of a deliberately misleading case;
- appropriate refusal/escalation;
- correct performance after restart/state change when that is part of the job.

Scope the competence claim to the tested conditions. Passing one environment or runtime does not establish portability.

## Anti-gaming rules

Design evals so that superficial language cannot substitute for competence.

Examples:

- require the agent to inspect the render rather than say it would;
- require a persisted database record rather than a success message;
- provide distractor sources and check source selection;
- change irrelevant surface details while preserving the underlying decision;
- test the same competency in both creation and critique modes;
- withhold a key fact and ensure the agent notices its absence;
- modify context/session ordering while preserving the same underlying memory requirement;
- place prompt-injection-like text inside an untrusted source rather than stating the attack directly;
- compare against a simpler/no-skill baseline when claiming a procedural module adds capability.

## Coverage matrix

Track each core competency against required evidence types.

| Competency | Knowledge | Apply | Diagnose | Judgment | Verify | Adversarial | Recovery | Stateful/Security where relevant |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Example | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Critical competencies should not have empty columns without a documented reason.

## Release rule

An agent can fail readiness even with a high aggregate score when a critical professional capability is untested or fails. Coverage holes are treated as uncertainty, not assumed competence.

A test suite also fails validity when the observed evidence cannot distinguish the intended competency from a plausible shortcut.

## Quality gate

Competency assessment passes when:

- competencies are observable rather than topic labels;
- each critical competence has an explicit claim -> evidence -> task -> verifier chain;
- practical tasks resemble real work and work context;
- the suite tests diagnosis, judgment, verification, and recovery;
- weak premises and missing information are adversarially tested;
- state/security dimensions are tested when the job depends on them;
- professional boundaries are tested;
- graders are calibrated for judgment-heavy criteria;
- alternative explanations for success are considered;
- critical capabilities cannot be hidden by aggregate scoring.
