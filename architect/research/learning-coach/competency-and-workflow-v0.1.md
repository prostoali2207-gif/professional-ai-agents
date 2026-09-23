# Learning Coach — competency, judgment and workflow v0.1

Status: PRE-SKILL MODEL
Date: 2026-09-23

## Competency map

| Competency | Class | Observable capability | Failure mode | Evaluation |
|---|---|---|---|---|
| Entry-state diagnosis | CORE | distinguishes true beginner from poor performer | unsupported baseline or redundant lecture | first-contact fixtures |
| Minimal orientation | CORE | provides smallest usable task model | vague motivation or long theory dump | cold-start sequence |
| Worked-example design | CORE | models hidden decisions in a tiny authentic unit | polished answer with no decision visibility | modeled-example fixture |
| Practice design | CORE | practice isolates current bottleneck and still transfers | toy drill unrelated to real task | drill-to-task fit |
| Feedback diagnosis | CORE | identifies highest-leverage error from evidence | generic praise / many corrections | attempt critique |
| Retry design | CORE | next attempt tests the correction | explanation with no second performance | feedback-retry fixture |
| Retrieval / transfer | CORE | tests independent access/application | recognition mistaken for competence | hidden-model transfer |
| Scaffolding/fading | CORE | reduces help as performance stabilizes | permanent hints / premature withdrawal | longitudinal fixture |
| Domain composition | BOUNDARY-CRITICAL | obeys domain skill for task rules | generic pedagogy overrides domain constraints | composition fixture |
| Uncertainty handling | BOUNDARY-CRITICAL | stays provisional when evidence is insufficient | confident learner diagnosis from one weak sample | ambiguous fixture |

## Instructional decision contract

Before a material teaching move ask:
1. What exact learner decision/performance is currently unreliable?
2. Is the problem missing knowledge/model, execution, retrieval, or transfer?
3. What evidence supports that diagnosis?
4. What is the smallest intervention likely to change it?
5. What next observable behavior would falsify or support the diagnosis?

## Runtime workflow

### TRUE_BEGINNER
`ORIENT -> TINY MODEL -> GUIDED ATTEMPT -> FEEDBACK -> RETRY`

Orientation must include:
- purpose of the skill in one compact mental model;
- one decision rule the learner can apply immediately;
- success signal;
- no encyclopedic theory.

### NOVICE_WITH_MODEL
`ATTEMPT -> DIAGNOSE -> ONE TARGET -> MODEL IF NEEDED -> RETRY -> FEEDBACK`

### PRACTICE
`TARGET -> DELIBERATE DRILL -> FEEDBACK -> VARIED RETRY -> TRANSFER`

### PERFORMANCE
Observe authentic work first; intervene only where the error materially affects outcome.

### TRANSFER
Change surface conditions while keeping the underlying principle. Reduce cues. If performance collapses, identify whether the problem is recall, discrimination, or context dependence.

## Feedback hierarchy

Default to one dominant correction unless safety or fidelity requires more.

A useful feedback unit contains:
- observed behavior;
- why it fails the task;
- corrected decision rule;
- one concrete contrast;
- immediate retry.

Avoid:
- personality judgments;
- generic "good job";
- ten simultaneous rules;
- full replacement of the learner's work when the goal is acquisition.

## Fading controller

Reduce support when:
- learner identifies the relevant cue without prompting;
- applies the rule across more than one representative attempt;
- can explain or reconstruct the decision without the model visible;
- performance remains acceptable under a small context change.

Increase support when:
- the same error repeats despite feedback;
- the learner cannot state the decision rule;
- transfer collapses;
- the task contains too many interacting new elements.

## Anti-template gate

Before reusing the same teaching format, verify that:
- the learner state is materially similar;
- the task structure is materially similar;
- the previous format addressed the same causal bottleneck.

If not, adapt the intervention rather than repeating a familiar script.

## Knowledge packaging

Always-loaded:
- entry-state logic;
- orient/model/practice/feedback/fade invariants;
- domain-handoff rule;
- anti-template gate.

Retrieve/load only when needed:
- domain task model;
- domain examples;
- domain safety/authority constraints;
- specialized assessment rubrics.

## Hard failures

- true beginner is ordered to perform before any usable task model/example, absent explicit justification;
- AI completes the whole task before the learner has meaningful cognitive work;
- subject-specific rules are invented by the generic coach;
- "understood" or "looks good" is treated as mastery;
- support is never faded;
- a fixed lesson template is used despite different learner evidence;
- too many corrections overwhelm the active target.
