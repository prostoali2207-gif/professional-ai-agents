# High-Stakes Profession Architecture

Status: v0.1.

## Purpose

Prevent Agent Architect from treating high-consequence professional roles as ordinary knowledge-and-execution problems.

In high-stakes domains, a strong agent architecture must explicitly model consequence, professional accountability, jurisdiction, decision authority, human oversight, validation burden, and escalation. The target is not maximal autonomy. The target is appropriate assistance with bounded authority and verifiable support for accountable professional judgment.

## 1. Trigger conditions

Apply this layer when a material error can plausibly cause one or more of:

- serious physical harm or deterioration of health;
- deprivation of liberty, legal rights, or due process;
- major financial loss or irreversible commitment;
- regulatory or professional-liability exposure;
- consequential discrimination or exclusion;
- damage to critical infrastructure, public safety, or security;
- disclosure of highly sensitive/confidential information;
- decisions for which a licensed/authorized professional remains accountable.

High stakes can arise from the task, context, population, jurisdiction, or requested authority even if the underlying profession is not always high stakes.

## 2. Consequence-first profession reconstruction

Before modeling competencies, map:

- affected person(s) and rights/interests;
- credible harms and severity;
- reversibility;
- time criticality;
- uncertainty and missing information;
- applicable jurisdiction/regulatory regime;
- legally/professionally authorized decision-maker;
- who bears accountability for the final decision;
- what independent verification is available;
- which actions must remain nondelegable.

Do not infer that because a model can generate a recommendation it should be authorized to make or execute the decision.

## 3. Decision-support vs decision-authority

Separate at least four levels:

1. `INFORMATION SUPPORT` — retrieve, organize, summarize, calculate, surface evidence.
2. `ANALYTICAL SUPPORT` — compare options, identify risks, generate hypotheses, test consistency.
3. `RECOMMENDATION SUPPORT` — propose a bounded recommendation with evidence, uncertainty, alternatives, and explicit need for accountable review.
4. `DECISION / EXECUTION AUTHORITY` — make or enact a consequential decision.

Default high-stakes architectures to levels 1-3 unless authoritative professional/regulatory evidence and representative evaluation justify more autonomy.

For material high-stakes decisions, distinguish `agent competence` from `delegable authority`.

## 4. Independent-reviewability requirement

A recommendation is not adequate merely because it sounds plausible or cites sources.

Where an accountable professional must review it, expose the basis needed for meaningful independent review:

- purpose/intended use;
- applicable population/context;
- key inputs and data-quality assumptions;
- governing rule/guideline/source and current version;
- reasoning-relevant evidence;
- material knowns and unknowns;
- alternatives considered;
- contraindications/conflicts/exceptions where relevant;
- uncertainty and confidence basis;
- what new fact would change the recommendation.

Do not create opaque recommendations that merely invite rubber-stamping.

## 5. Current-authority gate

High-stakes professional conclusions frequently depend on changing law, regulation, clinical guidance, standards, product labeling, market rules, or jurisdiction.

Therefore:

- live research is mandatory for material versioned/jurisdictional claims;
- primary authoritative sources should be opened, not merely cited from memory;
- effective date/version/jurisdiction must be explicit;
- conflicts between authoritative sources must be resolved or exposed;
- absence of adequate authority is an escalation condition, not a gap to fill with model priors.

## 6. Input sufficiency gate

Before making a recommendation, identify minimum decision-relevant inputs.

If a missing fact can materially change the decision, the agent must not silently assume it. It should acquire the fact, condition the recommendation, or escalate.

Classify missing information as:

- non-material;
- material but recoverable;
- material and unavailable;
- time-critical unknown;
- contradictory/unreliable.

High-stakes agents should be explicitly evaluated on resisting user pressure to provide a definitive answer when required inputs are absent.

## 7. Verification and corroboration

For consequential claims:

- verify exact citations, records, calculations, and source text;
- prefer independent corroboration when feasible;
- distinguish source existence from source applicability;
- verify downstream action/state when tools execute changes;
- use deterministic checks for arithmetic, dates, identifiers, constraints, and record consistency where possible.

A single language-model self-check is not independent verification.

## 8. Human oversight architecture

Human oversight must be designed, not merely stated.

Define:

- who reviews;
- their required competence/authorization;
- what evidence they receive;
- when review occurs;
- what they can override;
- escalation paths;
- time budget for review;
- what happens if the reviewer is unavailable;
- whether the interface encourages independent judgment or automation bias.

A human-in-the-loop who lacks context, time, authority, or sufficient evidence is not effective oversight.

## 9. Nondelegable judgment

Some work may remain professional even after substantial AI assistance.

Architects must identify whether domain rules, ethics, regulation, or professional practice make particular decisions effectively nondelegable. The agent may prepare evidence and options while the accountable professional retains final judgment.

Do not encode `consult a professional` as a generic disclaimer. Encode exactly which decision exceeds agent authority and why.

## 10. Confidentiality, consent, and sensitive data

Map:

- confidentiality duties;
- data minimization;
- permitted systems/tools;
- retention/training exposure;
- consent/disclosure requirements where applicable;
- cross-border/jurisdictional constraints;
- logging/audit requirements;
- redaction/anonymization opportunities.

A more capable tool may still be the wrong tool if its data handling conflicts with professional obligations.

## 11. High-stakes adversarial evals

At minimum include cases where:

- the user demands a definitive answer despite missing decisive facts;
- an outdated authoritative source conflicts with a current one;
- two jurisdictions have different rules;
- a plausible citation does not actually support the proposition;
- the agent is asked to exceed its authorized scope;
- the human reviewer is given an opaque recommendation that invites rubber-stamping;
- sensitive information is offered to an unsuitable tool;
- a recommendation is numerically correct but professionally inapplicable;
- time pressure tempts bypassing required verification;
- the agent should stop/escalate rather than continue;
- a user asks to remove review gates for convenience;
- one successful benchmark result is used to justify broad autonomy.

## 12. Evaluation dimensions

Grade separately:

- domain competence;
- authority/jurisdiction recognition;
- source currency and applicability;
- input sufficiency;
- uncertainty calibration;
- verification rigor;
- escalation correctness;
- confidentiality/data handling;
- reviewer support quality;
- resistance to automation bias;
- permission/authority discipline;
- outcome safety and reversibility.

A high aggregate score cannot compensate for failure on a catastrophic critical gate.

## 13. Critical-gate policy

Define domain-specific hard-fail conditions before deployment.

Examples may include:

- fabricated or unverified governing authority;
- wrong jurisdiction;
- executing a consequential action beyond authority;
- exposing protected information to an unapproved system;
- omitting a known material contraindication/conflict;
- presenting a recommendation as definitive when required decisive inputs are missing.

High-stakes readiness requires zero critical failures across representative adversarial evaluations, plus appropriate statistical confidence for non-critical metrics.

## 14. Architecture implications

High-stakes tasks often benefit from separation between:

- evidence/retrieval;
- domain analysis;
- deterministic validation;
- independent critic/verification;
- accountable human decision.

But multi-agent complexity is not automatically safer. Separation is justified only when it creates real independence, different evidence access, stronger checks, or bounded permissions.

## Quality gate

A high-stakes professional agent architecture does not pass if it merely says `verify`, `be careful`, or `consult an expert`.

It must specify the consequential decision, governing authority, required inputs, reviewable evidence, verification process, autonomy boundary, human owner, escalation condition, and representative critical-failure evals.