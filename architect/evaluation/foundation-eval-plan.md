# Agent Architect Foundation Evaluation Plan

Status: draft v0.1. This evaluates the methodology before it is promoted into a SKILL.

## Objective

Test whether the Agent Architect can construct a professional cognitive system rather than merely produce polished prompts.

## Evaluation dimensions

### A. Profession reconstruction
Given a vague user goal, identify the actual profession or combination of professions, responsibility boundaries, outputs, and excluded responsibilities without blindly accepting the user's label.

### B. Competency extraction
Produce observable expert capabilities rather than topic labels. Distinguish knowledge, competence, judgment, execution, and verification.

### C. Hidden competency discovery
Identify adjacent and tacit skills that a non-expert user would likely omit.

### D. Source discipline
For material claims, choose claim-appropriate authoritative evidence, distinguish source categories, inspect freshness/version applicability, and preserve provenance.

### E. Conflict resolution
Handle conflicting credible sources by analyzing scope, version, evidence quality, jurisdiction, and uncertainty rather than cherry-picking.

### F. Knowledge architecture
Map competencies to necessary foundational, specialized, current, heuristic, and failure-pattern knowledge. Avoid using instructions as a substitute for missing disciplines.

### G. Professional judgment
Encode trade-offs, applicability conditions, exceptions, justified rule-breaking, and epistemic boundaries.

### H. Tool/evidence architecture
Identify what can be directly observed, executed, measured, or verified and require ground-truth checks where possible.

### I. Architecture selection
Choose among single agent, workflow, critic/evaluator, specialist handoff, and multi-agent orchestration based on measurable need rather than fashion.

### J. Evaluation design
Create authentic practical and adversarial tests with appropriate graders and quality gates.

### K. Failure diagnosis
Given a failed eval, identify the responsible layer and repair that layer rather than append arbitrary prompt text.

## Adversarial scenarios

1. User asks for a "branding agent" but the real goal spans brand strategy, identity design, naming, research, and implementation governance.
2. User insists their preferred solution is correct despite weak evidence.
3. A popular practitioner blog conflicts with a current official standard.
4. An old authoritative document conflicts with newer versioned platform documentation.
5. A beautiful real-world example violates important functional constraints.
6. A domain contains irreducible professional disagreement rather than one universal best practice.
7. The proposed multi-agent system can be replaced by a simpler workflow with equal expected quality.
8. The agent produces a plausible result that has not been directly tested despite available tools.
9. The evaluator rewards verbosity rather than professional performance.
10. A failed task is caused by tool/interface design, not missing prompt instructions.
11. A requested capability depends on a discipline the user never mentioned.
12. The correct response requires stating uncertainty or escalation instead of fabricating a confident decision.

## Practical benchmark format

Each benchmark should provide:

- realistic task/context;
- available tools and information;
- hidden traps;
- expected professional behaviors;
- prohibited shortcuts;
- outcome criteria;
- trajectory/tool-use criteria where material;
- grader type;
- severity weighting;
- regression identifier.

## Grading strategy

Use the strongest feasible verifier:

1. deterministic/environmental outcome checks when ground truth is inspectable;
2. structured rubric-based model grading for qualitative outputs;
3. domain-expert human review for high-consequence or irreducibly judgment-heavy cases;
4. mixed grading when no single verifier is sufficient.

Do not use an LLM judge for facts that can be mechanically checked.

## Release gate for Agent Architect SKILL.md

Do not write/finalize the Agent Architect SKILL until:

- methodology coverage exists for profession discovery, competence, knowledge, judgment, tools/evidence, evaluation, and failure recovery;
- source register includes primary/authoritative foundations;
- adversarial suite exists;
- at least one dry-run profession decomposition has been evaluated without turning that profession into a production agent;
- major failures from the dry run are repaired at the methodology layer;
- senior-practitioner / educator / hiring-manager red-team questions have been applied.

## Failure loop

For every failed test:

`failure -> evidence -> root-cause class -> affected architecture layer -> repair -> regression test -> adversarial retest`.

Record recurring failures as a taxonomy. Do not hide them by loosening the grader.
