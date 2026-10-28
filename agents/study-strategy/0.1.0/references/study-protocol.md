# Study Strategy protocol

Use this module to turn lesson/source material into an efficient durable-study plan.

## 1. Select target

For each candidate item ask:
- future use?
- consequence of forgetting/confusing?
- referenceable instead?
- source/fidelity requirement?
- repeated/foundational role?
- review cost?

Then classify:
`REFERENCE_ONLY | UNDERSTAND | RECALL | EXACT | DISCRIMINATE | APPLY | EVIDENCE_CHAIN`.

One item may carry multiple target types.

## 2. Match practice

### REFERENCE_ONLY
Keep searchable/indexed. No recurring active review by default.

### UNDERSTAND
Prompt:
- explain in own words;
- state cause/relation;
- compare source after explanation.

### RECALL
Prompt:
- free recall;
- short-answer cue;
- reconstruct list/structure.

### EXACT
Require:
- verified target;
- exact recall;
- direct comparison;
- correction;
- later exact recall.

### DISCRIMINATE
Prompt:
- A vs B;
- classify cases;
- identify condition/source that changes the answer.

### APPLY
Prompt:
- varied scenario;
- choose/apply rule;
- explain why;
- change surface details to test transfer.

### EVIDENCE_CHAIN
Prompt:
- claim/ruling;
- source/evidence;
- reasoning link;
- conditions/exceptions;
- disagreement/attribution if material.

## 3. Retrieval result classification

- `CORRECT_EASY` — accurate, fast, independent.
- `CORRECT_EFFORTFUL` — accurate with meaningful effort.
- `PARTIAL` — core recalled, material omission.
- `DISTORTED` — meaning/source/condition changed.
- `FAILED` — cannot reconstruct.
- `SOURCE_ERROR` — wrong attribution/exact wording.
- `TRANSFER_FAIL` — recalls statement but cannot use/discriminate it.

## 4. Response to result

### CORRECT_EASY
Lengthen next interval.

### CORRECT_EFFORTFUL
Keep or moderately lengthen interval.

### PARTIAL
Correct missing material; retry; do not immediately reset whole item if core is stable.

### DISTORTED / SOURCE_ERROR
Stop rehearsal.
Return to authoritative source.
Correct.
Retrieve again after correction.
Use a shorter next interval.

### FAILED
Strengthen encoding/understanding, reduce target size if needed, then retry.

### TRANSFER_FAIL
Keep recall target but add discrimination/application practice.

## 5. Spacing

No universal day sequence.

Inputs:
- retention horizon;
- importance;
- target type;
- result class;
- prior delayed successes;
- review load.

The goal is **successful effortful retrieval over increasing intervals**, not a calendar ritual.

When no history exists, a provisional schedule may be used only as a starting experiment and must be adjusted from actual performance.

## 6. Cumulative review

Periodically mix:
- recent active targets;
- older important targets;
- known confusion pairs;
- one transfer/application case where relevant.

Do not add every old item forever.

## 7. Retirement / downgrade

Move an item out of active review when:
- low future-use value;
- easily referenced;
- redundant with another stronger target;
- repeatedly strong delayed recall and low consequence;
- review cost exceeds value.

Keep high-consequence/source-critical targets at an appropriate maintenance cadence.

## 8. Lesson closeout

At the end of a lesson produce, as appropriate:
- `REFERENCE`: keep in notes;
- `UNDERSTAND`: explain once/verify;
- `ACTIVE RECALL`: short list;
- `EXACT`: verified exact targets only;
- `DISCRIMINATE/APPLY`: one or more authentic prompts;
- next delayed check window.

Do not force every bucket to contain something.

## 9. Anti-overload rule

When a learner is new to systematic study, add few active targets first.
Measure:
- completion;
- recall;
- review burden.

Scale only when the system remains sustainable.
