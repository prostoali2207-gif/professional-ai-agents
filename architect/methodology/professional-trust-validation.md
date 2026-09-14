# Professional Trust Validation

Status: v0.1.

## Purpose

Separate three different claims that must not be collapsed:

1. an agent or Professional Core passed the repository's internal qualification;
2. independent strong practitioners validated that the evaluation and the agent's decisions represent strong professional work;
3. the agent demonstrated reliable performance in real deployment.

The repository lifecycle value `qualified` remains an internal admission/qualification state. It is **not** by itself evidence that the artifact is equivalent to a strong practitioner or safe to rely on without profession-specific supervision.

This methodology governs any stronger trust claim.

Relevant evidence basis in `references/source-register.md`:

- SRC-011 — NIST AI RMF Measure: deployment-relevant evaluation, domain experts and independent assessment;
- SRC-013 — OpenAI GDPval: authentic occupational tasks and professional graders;
- SRC-021 — NIST AI 800-4: controlled pre-deployment evaluation cannot substitute for post-deployment monitoring.

## First principle

Trust claims must not exceed the strongest independent evidence actually obtained.

Do not infer:

`QUALIFIED -> expert-level -> production-proven`.

Instead record the evidence tier explicitly.

## Evidence tiers

### T1 — QUALIFIED

Meaning:

- the exact artifact/agent passed its applicable internal qualification;
- required deterministic, held-out, adversarial, practical, runtime and other release gates passed within the recorded claim boundary;
- the evaluation has the documented graders, environment, thresholds and limitations.

Claim ceiling:

> Internally qualified against the repository's frozen professional construct and evaluation.

T1 does **not** establish that:

- independent practitioners endorse the construct;
- model graders agree with expert practitioners on difficult boundary cases;
- the agent performs at a strong-practitioner level in real work;
- a non-expert user can safely stop reviewing its professional decisions.

All existing `qualified` cores/agents default to T1 unless stronger evidence records exist.

### T2 — EXPERT-VALIDATED

Meaning:

- T1 is satisfied;
- independent, demonstrably strong current practitioners have reviewed the professional construct/evaluation and blind work samples from the exact agent or behavior-equivalent artifact;
- material AI/model graders used for judgment-heavy criteria have been calibrated against professional reference judgments;
- the validation supports the stated professional-performance claim boundary.

Claim ceiling:

> Independently validated against strong-practitioner judgments for the tested work and conditions.

T2 still does not establish broad production reliability outside the validated conditions.

### T3 — PRODUCTION-PROVEN

Meaning:

- T2 is satisfied for judgment-heavy professional claims unless a documented rationale shows that external expert judgment is not material because the relevant claims are mechanically verifiable;
- the exact deployed behavior or a justified behavior-equivalent artifact has accumulated representative field evidence;
- real outcomes, human corrections/overrides, incidents, near-misses and drift signals are monitored;
- the preregistered production evidence gate passes.

Claim ceiling:

> Production-proven within the recorded deployment context, exposure and monitoring window.

T3 is not a permanent certificate. Material drift, severe incidents, behavior-relevant changes or invalidated evaluation assumptions can reduce the supported tier.

## Expert-validator eligibility

A person counts as a domain expert for T2 only when the validation record documents evidence appropriate to the profession, such as:

- recent hands-on responsibility for comparable work;
- evidence of strong outcomes, portfolio/work artifacts, senior responsibility, recognized professional standing or equivalent demonstrable competence;
- familiarity with the target market/context when that context materially affects judgment;
- independence from authoring the candidate behavior and from knowing the desired validation result.

Do not use title, follower count, employer prestige or self-description alone as expert evidence.

For tacit, subjective or judgment-heavy work, prefer multiple independent practitioners. A single validator may be acceptable only when the claim is narrow and the record explains why one person's judgment is sufficient. Do not invent a universal reviewer count.

Conflicts of interest and prior involvement must be disclosed.

## Expert validation design

T2 validation must be preregistered before revealing candidate outputs to validators.

Record:

- exact artifact/version/digest and runtime;
- professional claim being tested;
- deployment context and exclusions;
- validator eligibility criteria;
- task-sampling rationale;
- rubric/decision dimensions;
- critical failure definitions;
- whether process, outcome or both are visible;
- blinding procedure;
- comparison baseline where applicable;
- disagreement handling;
- pass/fail rule;
- revalidation triggers.

### Task set

Use authentic work samples, not trivia.

Cover as appropriate:

- routine work;
- difficult diagnosis/judgment;
- ambiguity and missing information;
- a bad user premise or pressure to make a weak decision;
- misleading evidence;
- edge/boundary conditions;
- revision after critique;
- end-to-end work where local polish can hide a weak professional outcome.

Sample size must be justified by consequence, breadth, variance and cost. Do not choose a convenient fixed count without evidence.

### Blind review

Where feasible, validators should not know:

- which output came from the candidate versus a comparison professional/baseline;
- the desired result;
- internal development history;
- hidden expected-answer wording.

For subjective work, pairwise or comparative judgment is preferred when it reduces scale/verbosity bias.

### What experts judge

Do not ask only whether the answer is "good."

Ask observable professional questions such as:

- Would you make materially the same decision under these facts?
- What decision-critical cue did the agent miss?
- Is the reasoning professionally defensible even if another strong practitioner might choose a different valid option?
- Would you trust this work for a real client/project within the stated authority?
- Would you need to correct the agent before the work could proceed?
- Is the error a preference difference, P2 quality weakness, or P0/P1 professional failure?

Preserve legitimate professional disagreement. Do not average incompatible judgments into a fake consensus.

## Calibrating AI judges

AI/model graders may scale evaluation after professional grounding; they must not manufacture the professional ground truth they are intended to measure.

For material judgment-heavy criteria:

1. build a calibration set containing clear passes, clear failures and hard boundary cases;
2. obtain blind professional reference judgments;
3. run the model grader blind;
4. inspect criterion-level disagreement, false accepts and false rejects;
5. repair rubric/construct before prompt-tuning the grader;
6. test on held-out expert-judged cases;
7. define when human review is still mandatory;
8. periodically revalidate after model, rubric, profession or deployment drift.

A model grader that is only calibrated against another AI-authored answer cannot support T2.

Deterministic/mechanical criteria do not need artificial human scoring merely to satisfy this policy.

## T2 release decision

Do not grant EXPERT-VALIDATED on aggregate preference alone.

Block T2 when any of the following is true:

- validators identify a repeated P1/core professional error;
- a critical blind case reveals a missing profession competency or invalid evaluation construct;
- AI graders systematically disagree with expert reference judgments on a release-critical criterion;
- validators must repeatedly repair decision substance rather than style/polish;
- the expert evidence is not independent or its eligibility is not defensible.

A disagreement that represents legitimate alternative professional judgment is not automatically a failure.

The validation record must state limitations and the exact claim boundary.

## Production proof

T3 is earned through monitored field evidence, not elapsed time or anecdotal success.

Before field use counts toward T3, preregister:

- deployment context and authority;
- expected task distribution and important excluded tasks;
- outcome/quality signals;
- human correction/override capture;
- critical incident and near-miss definitions;
- drift signals;
- observation window or exposure target justified for the profession;
- stop/downgrade conditions;
- accountable reviewer/owner.

Use `evaluation/field-evidence-feedback-gate.md` and `methodology/production-incident-learning.md`.

Relevant signals may include:

- professional correction rate by severity;
- accepted-without-substantive-repair rate;
- downstream outcome quality where attribution is defensible;
- P0/P1 incident rate;
- repeated failure families;
- expert spot-review disagreement;
- tool/runtime failure patterns;
- escalation appropriateness;
- drift versus qualification/expert-validation performance.

Do not invent one universal numeric threshold. Freeze thresholds appropriate to the profession, consequences and measurement quality before evaluating the production evidence.

## Downgrade and revalidation

Evidence maturity is revocable.

Trigger review when there is:

- a confirmed P0/P1 professional failure;
- repeated substantive corrections by strong practitioners;
- a new failure class not represented by existing evals;
- material model/runtime/tool behavior change;
- changed professional standard, market/jurisdiction regime or deployment context;
- grader calibration breakdown;
- evidence that the original expert validators or tasks were not representative;
- production drift beyond the preregistered tolerance.

Possible dispositions:

`KEEP_TIER | NARROW_CLAIM | REVALIDATE_T2 | REVALIDATE_T3 | DOWNGRADE_TO_T2 | DOWNGRADE_TO_T1 | QUARANTINE | REVOKE`.

Do not preserve a high trust label for reputational convenience.

## Relationship to library lifecycle

Professional Core lifecycle and trust evidence are separate axes.

Example:

`lifecycle = qualified`

can coexist with:

`trust_tier = T1 QUALIFIED`.

A core does not need to be removed from the library merely because it has not yet reached T2 or T3.

Conversely, T2/T3 evidence does not override lifecycle quarantine/revocation, compatibility analysis or target-specific requalification obligations.

## Claim language

Allowed examples:

- "Qualified for the recorded internal claim boundary."
- "Expert-validated for the listed tasks and context."
- "Production-proven for the recorded deployment context and monitoring window."

Disallowed without matching evidence:

- "top expert";
- "human-level professional";
- "safe to trust blindly";
- "fully autonomous professional";
- "better than professionals";
- any equivalent claim that exceeds the validation record.

The operational target may be that a non-expert user does not need profession-specific knowledge to catch routine professional errors. That target must be demonstrated through T2/T3 evidence; it is not granted by wording.

## Scaling rule

Do not send every candidate response to humans forever.

Use experts where their judgment has highest information value:

1. validate the profession construct and hard cases;
2. establish expert reference judgments;
3. calibrate scalable graders;
4. spot-check and revalidate boundary cases;
5. investigate incidents/drift;
6. refresh validation when material conditions change.

This preserves external grounding without turning the factory into a permanent manual review service.

## Mandatory red-team before T2/T3

Ask exactly:

`What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?`

Then ask:

- senior practitioner: would the candidate create hidden rework or client risk?
- educator/assessor: does this evidence measure competence or test-taking?
- hiring manager: would this evidence justify giving the person/agent the represented responsibility?
- evaluation scientist: are sampling, blinding, calibration and disagreement handling construct-valid?
- operations owner: does production evidence represent real behavior rather than survivorship or selective review?

Material gaps must be repaired or the claim narrowed before promotion.

## Quality gate

This methodology is satisfied only when a reviewer can trace:

`artifact -> T1 qualification evidence -> independent practitioner evidence -> calibrated scalable evaluation -> field evidence -> current trust claim -> downgrade/revalidation policy`.

If a link is absent, stop at the strongest tier actually supported.
