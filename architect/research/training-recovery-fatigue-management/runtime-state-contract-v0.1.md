# Training Recovery & Fatigue Management — longitudinal state contract v0.1

Date: 2026-09-21
Status: pre-SKILL runtime design.

## Purpose

The skill depends on longitudinal evidence. State must preserve enough history to detect trends and learn from interventions without manufacturing a single pseudo-scientific recovery score.

## State layers

### A. Athlete/context baseline
Retain only decision-relevant facts:
- training age/status;
- current hypertrophy/strength goal;
- normal weekly schedule;
- current exercises and typical set/rep/RIR ranges;
- known constraints relevant to training recovery;
- measurement methods/devices used.

Do not persist medical speculation.

### B. Daily recovery observation
Fields:
- date/time;
- sleep duration estimate;
- sleep timing;
- self-rated sleep quality;
- optional device sleep estimate + device/model/source;
- perceived fatigue/energy;
- stress/mood if volunteered and decision-relevant;
- soreness by body region/muscle group;
- illness/injury concern flag;
- free-text note only when decision-relevant.

Each field stores source type: self-report, device, training log, clinician/professional, unknown.

### C. Training-session observation
Fields:
- date;
- session type;
- exercise/variant;
- sets;
- reps;
- load;
- RIR/RPE where available;
- exercise order;
- notable technique/ROM/equipment change;
- failure sets;
- session duration;
- optional session RPE;
- notable novelty/eccentric emphasis;
- completion/abort reason.

### D. Comparable performance anchors
Do not compare arbitrary sessions.

A comparable performance anchor contains:
- exercise/variant identity;
- load or load band;
- rep target;
- RIR/RPE target or observed effort;
- technique/ROM/equipment constraints;
- session-order context;
- result metric;
- measurement source.

The system may mark observations as NON_COMPARABLE rather than force a trend.

### E. Load history
Track recent:
- weekly hard-set exposure by muscle group where available;
- frequency by muscle group;
- heavy/high-effort exposure;
- failure exposure;
- notable exercise changes;
- abrupt schedule changes.

Do not compress all of this into one universal load number.

### F. Intervention ledger
For every material decision:
- intervention_id;
- date_started;
- hypothesis;
- evidence that triggered it;
- variable changed;
- old state;
- new state;
- expected effect;
- review criterion;
- actual result;
- verdict: helped / neutral / worsened / unclear;
- superseded_by if later replaced.

This ledger is mandatory before repeating a prior intervention.

## Trend policy

Structural decisions use trends when evidence quality permits.

Authoring defaults for development:
- isolated bad day -> observe or make only session-local reversible modification;
- repeated comparable performance deterioration or a multi-day multi-signal cluster -> structural change may be considered;
- plateau -> requires repeated comparable exposures and recovery/adherence checks;
- severe/concerning symptoms bypass trend requirement and trigger escalation.

These are decision-policy defaults, not biological diagnostic thresholds.

## Missingness and contradiction

Missing != normal.
Unknown sleep or soreness must remain unknown.

When sources conflict:
- keep both with provenance;
- prefer direct comparable performance evidence for performance claims;
- do not overwrite self-report with wearable inference;
- if an authoritative medical assessment is supplied, treat it as higher authority for its scope without expanding beyond it.

## Wearables

Allowed:
- within-person longitudinal estimates;
- coarse sleep duration/timing trends;
- HR/HRV as optional context when measured consistently.

Disallowed as sole evidence:
- proprietary readiness score -> train/rest command;
- exact sleep-stage truth;
- inferred CNS fatigue/hormonal status;
- medical diagnosis.

## Compaction

Session history may be compacted into weekly summaries only after preserving:
- comparable performance anchors;
- material load changes;
- anomaly dates;
- intervention ledger;
- unresolved contradictions;
- medical escalation events without unnecessary sensitive detail.

Do not discard the raw facts needed to verify why a structural change was made.

## Retention / forgetting

Keep the minimum longitudinal window needed for trend and intervention learning.
Do not store rejected irrelevant personal details in notes.
If the user requests deletion/forgetting, remove or stop using the affected state according to platform memory policy.

## Stateful evaluation requirements

Must test:
- single bad day does not rewrite program;
- trend survives restart/compaction;
- wearable score conflicts with stable performance;
- intervention result prevents reflex repetition;
- newer authoritative information supersedes prior assumption;
- missing data remains missing;
- localized soreness does not become systemic-fatigue label;
- severe symptoms escalate immediately.
