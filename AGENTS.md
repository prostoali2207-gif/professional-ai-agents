# Repository operating rules

This repository exists to design, research, evaluate, and strengthen specialized professional AI agents.

## Prime directive

Do not write a role SKILL.md first.

Before an applied agent can receive a SKILL.md, the profession must be mapped, expert competencies must be identified, authoritative knowledge must be assembled, judgment and failure modes must be modeled, tools/evidence must be specified, and an evaluation plan must exist.

## Evidence over opinion

A user suggestion, an AI suggestion, a popular practice, or an attractive example is not evidence by itself. Material professional claims must be classified and supported by the best available evidence.

Prefer, in order appropriate to the claim:
1. authoritative standards and official documentation;
2. primary research and empirical data;
3. recognized professional frameworks and high-quality technical literature;
4. current practice from demonstrably strong practitioners;
5. examples and inspiration, explicitly labeled as such.

When sources conflict, record the conflict, scope, assumptions, and decision rationale. Do not silently select the convenient source.

## Runtime judgment and opportunity search

For material recommendations, architecture choices, and open-ended solution design, apply `docs/runtime-judgment-and-opportunity.md`.

In particular:
- do not manufacture a low-value balancing objection when an idea is already well supported;
- do not treat user or AI confidence as evidence;
- accept correct corrections when new evidence changes the decision;
- before fixing the first plausible mechanism, briefly test whether the mechanism can be replaced, eliminated, reused through existing capability/integration, or moved across AI/software/human boundaries;
- count alternatives as distinct only when their mechanisms or system boundaries materially differ;
- stop exploring when additional search no longer has plausible decision value.

## Professional model before prompt

For each agent, reconstruct the real profession or combination of professions. Extract observable work, decision points, tacit cues, trade-offs, expert-vs-average differences, failure modes, unknowns, and escalation boundaries.

Do not confuse:
- knowledge with competence;
- competence with judgment;
- judgment with execution;
- execution with verification;
- instructions with training material.

## Entry state and decision readiness

For every applied agent, model how professional work begins, not only how it proceeds after good inputs already exist.

When the deployment can receive a new/unknown user, incomplete case, or first-turn request:
- distinguish cold-start/onboarding from ongoing/follow-up work;
- recover relevant established context before asking for it again;
- map each material decision to its decision-critical prerequisites;
- classify missing inputs as safety-critical, decision-changing, calibration-only, or optional;
- obtain the smallest high-information set of missing decision-critical facts before making a personalized material decision;
- allow a provisional action only when the missing information cannot plausibly reverse the decision and the uncertainty is explicit;
- do not substitute folk labels, stereotypes, or convenient proxies for direct decision-relevant measurements/history.

Use `architect/methodology/initial-intake-and-decision-readiness.md`.

## Verification

If an outcome can be directly observed or tested, direct observation/test is required. Reasoning is not a substitute for execution evidence.

## Evaluation-driven development

Each agent must have evaluation coverage before it is declared ready. Include practical tasks, adversarial cases, ambiguity, conflicting requirements, bad user assumptions, insufficient information, tool/evidence use, critique, self-critique, and regression tests.

Failure handling:

FAIL -> classify failure -> root cause -> repair the correct layer -> regression test -> adversarial retest.

Do not patch every failure by adding arbitrary prompt text.

## Qualification stop-loss

The generic qualification platform is in **STOP / maintenance mode by default** under the evidence-based decision in issue #129.

Before repairing or rerunning any failed qualification, follow `architect/methodology/qualification-stop-loss.md`.

Mandatory rules:
- classify the failure before repair;
- do not reopen generic platform engineering without an explicit #129 reopen criterion and repository evidence;
- do not create serial infrastructure-repair issues to chase executability of the same qualification stage;
- after one bounded technical repair and one eligible retry in the same execution chain, another technical defect stops that chain and yields `NOT_EXECUTABLE` / the preregistered infrastructure verdict;
- a new issue, provider, transport, or renamed error does not reset the repair budget for the same failed stage;
- genuinely later qualification stages may form new execution chains because they test different evidence/runtime surfaces, but repeated cross-stage infrastructure churn must trigger explicit stop-loss review;
- never weaken professional scope, thresholds, hard-fails, held-out secrecy, independence, or practical evidence to obtain PASS.

This stop-loss limits infrastructure churn, not professional rigor.

## Architecture discipline

Use the simplest architecture that can meet the professional task. Do not default to multi-agent systems. Split roles only when separation of expertise, independent critique, parallel work, or risk boundaries create measurable value.

## Professional trust evidence

Internal qualification and external professional trust are different claims.

Follow `architect/methodology/professional-trust-validation.md`.

Mandatory rules:
- `QUALIFIED` / library lifecycle `qualified` is the internal T1 evidence tier, not a claim of strong-practitioner equivalence;
- do not claim `EXPERT-VALIDATED` without independent strong-practitioner evidence for the exact claim boundary;
- do not claim `PRODUCTION-PROVEN` without representative monitored field evidence;
- judgment-heavy AI graders must be grounded against professional reference judgments before they can support an expert-level claim;
- existing qualified artifacts remain valid T1 evidence and are not silently promoted to T2/T3;
- material incidents, repeated practitioner corrections, drift, runtime changes, or invalidated eval assumptions can trigger claim narrowing, revalidation, downgrade, quarantine, or revocation.

Use human experts where their judgment has high information value; do not turn every routine evaluation into permanent manual review.

## Definition of done

An applied agent is internally ready for T1 qualification only after:

profession mapped -> entry states/intake prerequisites mapped -> competencies mapped -> authoritative knowledge assembled -> gaps identified -> workflows designed -> tools/evidence strategy defined -> professional judgment encoded -> failure modes encoded -> skill orchestrates the system -> cold-start/incomplete-information evaluation run where applicable -> competency evaluation run -> weaknesses corrected -> practical evaluation passed.

After T1, assign the strongest evidence tier actually supported. If the intended deployment claim is that a non-expert user should not need profession-specific knowledge to catch routine professional errors, the agent must earn the corresponding T2/T3 evidence rather than inheriting that claim from internal qualification.

Even then, never claim exhaustive knowledge. The agent must know how to handle unknowns and when to research or escalate.
