# Training Recovery & Fatigue Management — stateful practical failure and repair record v0.1

Date: 2026-09-21
Stage: post-SKILL development stateful practical
Candidate status: pre-freeze / NOT QUALIFIED

## Failure

The first stateful practical execution stopped with:

`AssertionError: sleep timing fields must be explicit`

The exact candidate state schema exposed sleep duration/quality but did not explicitly encode sleep start/end despite the runtime-state contract requiring sleep timing.

Inspection of the same schema also found:
- `sessions[].exercises` was an unstructured array;
- `load_history` was an unstructured array;
- performance anchors had no stable `anchor_id` for compaction/restart verification.

These are material because the requested skill depends on longitudinal evidence, comparable training performance, volume/frequency history, and realized intervention outcomes.

## Classification

`PROFESSIONAL_FAIL` at the runtime state-contract implementation layer.

This is not qualification infrastructure failure. Issue #129 generic platform remains closed/maintenance.

## Root cause

The narrative state design was stronger than the machine-readable state contract. The schema allowed storage but did not prove that decision-critical longitudinal facts had stable, typed locations.

## Repair

Repair only the responsible state layer:
- add explicit sleep timing;
- structure session exercises and working sets;
- add stable performance-anchor IDs;
- structure weekly load history for hard sets, frequency, failure exposure and notable changes;
- preserve the intervention ledger;
- keep raw wearable evidence separate instead of creating a composite recovery score.

No professional threshold or hard fail is weakened.

## Regression obligations

After repair:
1. stateful schema/compaction practical must PASS;
2. deterministic static gate must still PASS;
3. adversarial case review must confirm no decision rule was weakened.
