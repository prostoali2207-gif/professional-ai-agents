# Training Recovery & Fatigue Management — profession reconstruction and reuse decision

Date: 2026-09-21
Status: pre-SKILL architecture decision
Target: applied skill for recovery and training-fatigue management during hypertrophy-oriented resistance training.

## 1. Profession boundary

The target is not a medical diagnostician and not a generic wellness coach. It is an applied strength-and-conditioning / sport-science decision-support capability that manages training load under uncertainty.

Accountable outputs:
1. distinguish expected acute/local fatigue from multi-session under-recovery patterns;
2. interpret performance changes in context rather than from one noisy observation;
3. decide whether to hold, locally modify, reduce, redistribute, or temporarily deload training;
4. decide which variable is most plausible to change first: volume, intensity/proximity-to-failure, frequency/distribution, exercise selection, or non-training recovery constraint;
5. preserve longitudinal evidence of sleep, sessions, performance, soreness, subjective fatigue, load history, interventions, and realized outcomes;
6. identify when medical conclusions are outside scope and escalation is required.

## 2. Competency reconstruction

CORE:
- resistance-training load and fatigue management;
- hypertrophy/strength programming interactions needed to change volume, intensity/proximity-to-failure, frequency and exercise selection without destroying the training objective;
- longitudinal performance interpretation;
- differential diagnosis of training-management causes.

BOUNDARY-CRITICAL:
- measurement/monitoring science: reliability, comparability, baselines, trend interpretation, subjective and objective signals;
- sleep/recovery science at the level required to identify an important recovery constraint and adjust training conservatively;
- uncertainty and causal-change discipline.

ESCALATION:
- sports medicine / clinical assessment for persistent unexplained deterioration, significant injury/illness symptoms, or suspected medical disorder;
- mental-health or eating-disorder care when relevant symptoms are disclosed;
- specialist sleep medicine for persistent clinically significant sleep problems.

CONTEXTUAL, not separate professions:
- nutrition/hydration status as a recovery constraint. Detailed dietary prescription belongs to the nutrition skill;
- psychosocial stress as a contextual signal;
- wearable data as one evidence stream under measurement science.

OUT OF SCOPE:
- diagnosing overtraining syndrome, endocrine disorders, anemia, infection, sleep disorders, injuries, or other medical conditions;
- declaring a proprietary readiness/recovery score objectively true;
- guaranteeing injury prevention from workload metrics;
- bodybuilding drug/PED management.

## 3. Reuse inventory

Repository searches on the current default-branch head found no eligible professional core for:
- sports nutrition;
- exercise physiology;
- strength and conditioning;
- hypertrophy training;
- recovery science;
- training-load management.

Generic Architect methodologies are reusable infrastructure/methodology, not domain professional cores.

No superficially similar marketing, UX, analytics, or qualification core has compatible professional responsibility, population, evidence base, judgment model, or evaluation construct.

Decision: BUILD NEW applied specialization.

This does not create a generic reusable framework. It creates one bounded applied skill and preserves provenance for any future reuse decision.

## 4. Architecture decision

Smallest sufficient architecture: one modular applied skill.

No multi-agent split is justified. Independent review belongs in evaluation, not runtime.

Runtime modules:
- evidence and source policy;
- competency/judgment model;
- longitudinal state contract;
- decision workflow;
- escalation boundary.

## 5. High-stakes boundary

Most load-adjustment decisions are low-to-moderate consequence when they are conservative and reversible. Health interpretation becomes high-stakes when symptoms may represent illness, injury or another medical condition.

Authority level:
- information support: YES;
- analytical support: YES;
- bounded recommendation support for training changes: YES;
- medical diagnosis/treatment authority: NO.

## 6. Reuse verdict

Target profession -> no compatible qualified core -> BUILD NEW.

Evidence retained:
- Agent Architect methodology, runtime-state, knowledge-packaging, high-stakes, evaluation, and stop-loss policies.

New evaluation required:
- all domain competencies;
- longitudinal state behavior;
- single-bad-day resistance;
- wearable-score resistance;
- deload judgment;
- plateau vs transient underperformance;
- medical escalation;
- repair/regression after observed development failures.
