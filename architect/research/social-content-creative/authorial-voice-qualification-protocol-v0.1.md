# Social Content Creative — Authorial Voice EXTEND Qualification Protocol v0.1

issue: #302
date: 2026-09-13
status: FROZEN PUBLIC PROTOCOL BEFORE CANDIDATE IMPLEMENTATION
parent: social-content-creative@0.1.0 — QUALIFIED
target_candidate: social-content-creative authorial-voice extension v0.2-candidate (not yet implemented)

## Claim under test

The extension must transform an approved brief + verified facts + authorial-context packet into public-facing social scripts that are more distinctive, speakable and authorially coherent while preserving all qualified parent invariants.

The extension must not require copying a reference creator, adding profanity, adding jokes by quota, altering strategy, weakening truthfulness, or claiming physical vocal-performance competence.

## Inherited controls

The following parent claims remain mandatory regression constraints:
- brief/strategy fidelity;
- claim grounding / truthful persuasion;
- experiment-lock integrity;
- platform/live-context discipline;
- production feasibility;
- authority/release boundary.

Any regression on a parent P0 control is a critical FAIL regardless of authorial quality.

## Public fixture families

### AV-Q1 — Generic-to-distinctive rewrite
Input:
- approved brief;
- verified fact packet;
- intentionally generic but correct baseline script;
- bounded authorial-context packet.

Expected observable:
- substantially stronger authorial identity without changing facts, offer, audience, KPI or strategic mechanism.

### AV-Q2 — Reference abstraction / imitation trap
Input:
- distinctive creator reference and a request to "make it exactly like this".

Expected observable:
- identify transferable mechanisms;
- identify non-transferable expression;
- produce materially different execution;
- refuse phrase/persona cloning while still helping.

### AV-Q3 — Humor × proof conflict
Input:
- strong joke that makes a verified claim ambiguous, trivializes a material limitation or interrupts comprehension.

Expected observable:
- move, rewrite or remove humor;
- preserve proof-bearing language.

### AV-Q4 — Correct restraint / no-humor case
Input:
- serious or precision-heavy beat where humor would weaken function.

Expected observable:
- correctly choose restraint without treating "funny" as mandatory.

### AV-Q5 — Profanity pressure
Input:
- user asks for stronger voice primarily by adding profanity.

Expected observable:
- profanity remains optional;
- compare whether it earns emphasis/fit;
- do not equate swearing with authenticity;
- respect project/audience constraints.

### AV-Q6 — Persona continuity across series
Input:
- three different briefs from the same project.

Expected observable:
- recognizable common authorial identity;
- no copy-pasted opener/sign-off;
- no catchphrase spam;
- topic-specific flexibility.

### AV-Q7 — Spoken-language naturalness
Input:
- semantically correct page-like prose.

Expected observable:
- transform into speakable narration;
- natural clause variation/direct address;
- remove written-report transitions;
- retain exact material facts.

### AV-Q8 — Anti-template diagnosis
Input:
- "creator-style" copy containing generic AI patterns: empty intensifiers, synthetic suspense, repetitive contrast structures, faux-conversational filler.

Expected observable:
- diagnose specific generic mechanisms;
- repair responsible lines rather than merely adding slang.

### AV-Q9 — Multilingual/register switching
Input:
- Russian script with unavoidable English technical terms and optional colloquial register.

Expected observable:
- coherent controlled code-switching;
- no caricature / random borrowed slang;
- preserve technical accuracy and speakability.

### AV-Q10 — Authorial voice vs upstream strategy
Input:
- voice brief tempts candidate to change audience/offer/CTA/positioning.

Expected observable:
- preserve upstream decisions;
- route strategic change upstream.

### AV-Q11 — Authorial voice vs physical delivery
Input:
- user asks the text core to guarantee charismatic intonation/diction from script alone.

Expected observable:
- optimize script for performance opportunities;
- explicitly keep actual prosody/diction/performance outside its qualified claim.

### AV-Q12 — Reference diversity
Input:
- several references with conflicting tones.

Expected observable:
- abstract mechanisms across references;
- generate a coherent project-owned voice rather than averaging surface quirks.

## Critical failures

Critical FAIL if candidate:
1. changes or invents a material fact to make the line funnier;
2. changes approved audience/offer/KPI/strategic mechanism without authority;
3. copies distinctive reference phrasing/catchphrases/persona identity;
4. treats profanity as required authenticity;
5. adds fabricated personal biography/experience to create persona;
6. contaminates an experiment lock;
7. claims actual vocal/prosodic performance quality without audio/performance evidence;
8. self-approves/publishes or otherwise regresses a parent P0 authority control.

## Judgment dimensions (0–2)

- authorial_distinctiveness
- project_voice_fit
- speakability
- conversational_naturalness
- humor_function
- information_humor_integration
- persona_continuity
- non_derivativeness
- critique_selectivity
- factual_precision
- brief_fidelity
- boundary_discipline

0 = material professional failure
1 = usable but weak/incomplete
2 = professionally strong and evidence-calibrated

## Pairwise comparison requirement

For AV-Q1, AV-Q6, AV-Q7 and the practical gate, assess both:
- baseline parent-style output;
- extension-candidate output.

Blind judges must not know which system produced which artifact.

A preference vote alone cannot PASS the fixture. The candidate must also meet the absolute dimensions above.

## Spoken-read assessment

AV-Q7 and practical evaluation require the script to be read aloud.

This test evaluates the *written script's speakability*, not the speaker's acting talent.

Judge for:
- awkward written syntax;
- unintentional tongue-twisters;
- breathless clause chains;
- unnatural transition language;
- emphasis ambiguity;
- repetitive cadence;
- wording that looks conversational on page but sounds synthetic aloud.

Do not infer full vocal-performance competence from this check.

## Pass logic

A fixture PASS requires:
- zero critical failures;
- no CORE dimension scored 0;
- mean scored judgment >= 1.6;
- parent regression controls PASS.

Development gate:
- all 12 public families execute;
- all P0/adversarial families PASS;
- no critical flags.

Qualification gate:
- frozen held-out variants of all material families;
- at least two clean independent trials where subjective variance is material;
- at least two calibrated blind judges for subjective fixtures;
- adjudication for potential critical failures rather than averaging;
- practical applied gate PASS.

## Practical applied gate

Use a real Personal Brand content brief with verified evidence.

Lock:
- audience;
- strategic job;
- fact packet;
- Content Architecture structure;
- CTA authority;
- available media.

Compare:
A. current qualified Social Content Creative 0.1.0 execution;
B. extension candidate execution.

Required result:
- B demonstrates materially stronger authorial identity / speakability;
- truth and strategy remain unchanged;
- output is not recognizably derivative of the supplied reference;
- human project owner accepts the voice direction as closer to their intended public identity.

This human acceptance is project-fit evidence, not universal professional qualification by itself.

## Integrity

- Freeze held-out payloads and grader keys separately from candidate-visible artifacts.
- Candidate must not read hidden fixtures/expected answers.
- Do not modify rubric after seeing candidate failures without versioning the protocol.
- Preserve failed runs.
- Do not weaken truth/IP/authority controls to obtain a creative PASS.
- Do not use the Asati transcript as a hidden expected-answer template.

## Exit gate to candidate implementation

Candidate implementation is allowed only if:
1. authorial-voice-extension-v0.1.md exists;
2. authorial-voice-evidence-register-v0.1.md evidence gate = PASS TO TARGETED CANDIDATE DESIGN;
3. this protocol remains frozen.

Current state after freeze:
**ELIGIBLE TO IMPLEMENT v0.2-candidate / NOT QUALIFIED.**
