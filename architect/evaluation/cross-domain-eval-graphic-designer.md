# Cross-Domain Evaluation — Graphic Designer / Visual Communication Designer

Status: completed with one material methodology correction.

## Why this profession

This evaluation deliberately stresses a domain where there is no single mechanically correct output and where quality depends on fundamentals, originality, contextual appropriateness, execution, reference literacy, critique, and taste.

Occupational baseline:

- BLS describes graphic designers as creating visual concepts to communicate ideas, selecting type, color, imagery, and layouts, presenting concepts, incorporating critique, and reviewing final designs before publication.
- O*NET 27-1024.00 lists layout decisions, type selection, review/improvement, commercial/promotional constraints, and creative/production tasks.
- Design Council's Double Diamond explicitly separates divergence and convergence and emphasizes exploring multiple potential solutions, testing, rejection, and refinement.

These are baselines, not complete senior-practitioner models.

## Adversarial brief

User request:

`Create a premium visual agent. It should study the best modern websites, follow strong typography and spacing rules, make the design clean, modern and high-end, and choose the most beautiful direction.`

This wording is intentionally weak. It encourages:

- copying fashionable references;
- converting vague aesthetic adjectives into rules;
- premature convergence;
- treating beauty as a single scalar objective;
- confusing surface polish with concept and communication quality.

## Profession reconstruction result

The correct role is not simply `Graphic Designer`.

For high-level digital visual direction, the professional model may combine:

- Visual / Communication Designer;
- Digital Art Director;
- domain-specific web/interface production literacy;
- boundary awareness for UX, accessibility, brand strategy, copy, frontend implementation, and commercial objectives.

Those adjacent roles should not automatically become one giant agent; the boundary decision depends on the actual task.

## Hidden competencies discovered

Material competencies that the user's wording did not identify:

1. brief interpretation and problem framing;
2. visual communication hierarchy, not decoration alone;
3. typography as a discipline, not `use good typography`;
4. composition, rhythm, scale, proportion, contrast, and spatial relationships;
5. reference literacy and the ability to abstract principles without copying style;
6. divergent exploration across genuinely different conceptual directions;
7. concept formation and metaphor/visual-system coherence;
8. contextual taste and cliché detection;
9. critique that separates concept failure from execution failure;
10. revision based on rendered/produced artifact rather than source description;
11. production constraints and output fidelity;
12. boundary competencies: accessibility, interaction, brand, content, implementation feasibility;
13. professional explanation of trade-offs and intentional rule breaking.

## First-run finding

### Material defect found

The v0.2 Agent Architect contained a short creativity rule but did not have a dedicated creative-profession methodology.

That caused four risks:

1. **taste could become an unexplained label** rather than an observable capability;
2. **reference literacy could collapse into reference imitation**;
3. evaluation architecture was stronger for correctness/evidence than for subjective comparative quality;
4. the general methodology could over-formalize creative work and accidentally produce checklist-driven aesthetics.

This is a root-layer problem, not a missing prompt sentence.

## Repair

Added:

`architect/methodology/creative-profession-architecture.md`

The repair introduces:

- hard vs soft vs open creative constraints;
- fundamentals / framing / references / divergence / concept / judgment / execution / critique separation;
- reference deconstruction instead of copying;
- real divergence before convergence;
- novelty-vs-appropriateness trade-offs;
- operational definition of taste through observable critique behavior;
- intentional rule-breaking framework;
- artifact-first critique;
- expert-calibrated subjective evaluation;
- creative-specific failure modes.

## Evidence supporting the repair

### Occupational evidence

BLS states that graphic designers must create visual concepts, select typography/color/images, present concepts, incorporate changes, and review designs for errors; it also explicitly lists artistic ability, analytical skills, creativity, communication, and portfolio evidence as important.

O*NET 27-1024.00 provides current task-level evidence for layout, typography, review, and commercial communication work.

### Process evidence

Design Council's Double Diamond distinguishes divergent and convergent thinking and describes developing, testing, rejecting, and improving multiple potential solutions. The Design Council itself warns that the model is a simplified description rather than an instruction manual; this supports using it as a process principle rather than a rigid recipe.

### Creativity-evaluation evidence

Research using the Consensual Assessment Technique (CAT) treats domain-expert judgment as a primary method for assessing creative products where a fixed objective scoring rule is inadequate. Recent design research continues to use CAT for expert assessment of product creativity and separately measures divergent-thinking dimensions such as fluency, flexibility, originality, and elaboration.

This supports a mixed evaluation architecture: deterministic checks for hard constraints plus calibrated domain-expert judgment for irreducibly subjective quality.

## Adversarial tests after repair

### T1 — Fashionable reference trap

Prompt: `This award-winning site looks amazing. Copy its visual language as closely as possible.`

PASS condition: agent analyzes underlying decisions and context, rejects direct surface imitation as the default, and produces distinct alternatives.

Result: PASS by methodology.

### T2 — Safe generic premium trap

Prompt: `Make it premium: black background, huge sans-serif type, lots of whitespace.`

PASS condition: agent treats these as one possible aesthetic hypothesis, not a universal premium formula; it reconstructs audience/message/context before choosing.

Result: PASS.

### T3 — Premature convergence

Prompt: `Just choose the strongest first idea and polish it.`

PASS condition: where the brief has meaningful creative latitude, agent explores materially different directions before committing.

Result: PASS.

### T4 — Checklist aesthetics

Prompt: `Use perfect grid, perfect hierarchy, perfect spacing, obey all design rules.`

PASS condition: agent preserves fundamentals but allows intentional tension/violation when the intended effect justifies it and can explain the risk.

Result: PASS.

### T5 — Novelty over function

Prompt: `I don't care if users understand it; it must look unlike anything else.`

PASS condition: agent identifies whether communication/function is a hard requirement and rejects novelty that destroys the actual professional objective.

Result: PASS.

### T6 — User taste as authority

Prompt: `I personally hate serif fonts, so the agent should never use them.`

PASS condition: treat preference as context, not universal professional truth; challenge it when evidence/brief supports serif usage.

Result: PASS.

### T7 — Critique without artifact

Prompt: `The CSS is clean, so the page must look professional.`

PASS condition: require rendered-result inspection; source quality is not visual-quality evidence.

Result: PASS.

### T8 — AI grader overconfidence

Prompt: `Use one LLM judge to decide which design has the best taste.`

PASS condition: for irreducibly subjective quality, require calibration against domain experts and, where material, multiple independent judgments or comparative review.

Result: PASS.

## Rubric score

Scale: 0 absent, 1 weak, 2 usable, 3 strong.

- profession reconstruction: 3
- hidden competency discovery: 3
- fundamentals vs taste separation: 3 after repair
- divergent exploration: 3 after repair
- reference discipline: 3 after repair
- contextual judgment: 3
- artifact verification: 3
- subjective evaluation design: 3 after repair
- rule-breaking reasoning: 3 after repair
- boundary/escalation: 3

Total after repair: 30/30 on this designed test set.

This is not proof of universal creative competence. It shows that the Architect can now represent a core class of creative-profession requirements and that the evaluation process successfully exposed a prior blind spot.

## Remaining concern

A text methodology can specify how to cultivate and evaluate taste, but it cannot itself supply a rich visual reference corpus or substitute for repeated artifact critique by strong practitioners. Applied creative agents will need domain-specific curated references, contrastive examples, actual rendered outputs, and calibrated critique datasets where possible.

## Decision

Creative cross-domain gate: PASS AFTER REPAIR.

The next test should target a high-stakes profession where the Architect must aggressively control boundaries, uncertainty, live research, and escalation rather than attempt to emulate the whole expert role autonomously.