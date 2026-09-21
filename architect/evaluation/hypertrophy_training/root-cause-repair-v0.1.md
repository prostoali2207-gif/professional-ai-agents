# Hypertrophy Training v0.1 — evaluator root-cause repair record

Date: 2026-09-21
Stage: post-assembly development review
Threshold changes: **NONE**

## Failure 1 — HT-DEV-13 was underdetermined

Observed problem:
- fixture expected `PROGRESS_REPS`;
- the task did not state the active rep-range prescription or next load increment;
- multiple professional actions could therefore be valid.

Root cause: **evaluator/fixture layer**, not candidate behavior.

Repair:
- add active 8-15 rep target at 1-2 RIR;
- add available 30 -> 35 kg equipment increments;
- keep expected action `PROGRESS_REPS` because the large next increment and remaining rep room now make the decision observable.

Regression:
- static suite still requires the same action vocabulary and fixture count;
- future semantic gate must grade the decision against the now-specified prescription.

## Failure 2 — HT-PRAC-02 forced two causal changes

Observed problem:
- practical expected both exercise substitution and a volume increase in the same target area;
- the equipment removal already forces a new baseline;
- adding volume simultaneously can make downstream interpretation needlessly ambiguous.

Root cause: **practical-evaluation construct**, specifically confounding.

Repair:
- preserve the prior plateau observation;
- require function-based substitution because the machine is removed;
- HOLD total volume initially during forced exercise change;
- establish a new exercise version/baseline;
- reassess volume only after comparable data exist.

Regression:
- hard fail added for forcing a simultaneous volume increase without need;
- progressing pulldown remains unchanged.

## Stop-loss / integrity

No generic qualification infrastructure changed.
No threshold/hard-fail was weakened.
No SKILL rule was patched to memorize either fixture.
The responsible evaluator layer was corrected before further scoring.


## Failure 3 — HT-PRAC-01 lacked load-increment observability

Observed problem:
- practical expected a concrete machine-press load progression;
- available equipment increments were absent;
- inventing a 2.5 kg step would itself violate the candidate's no-invention rule.

Root cause: **practical fixture input sufficiency**.

Repair:
- add explicit 2.5 kg total bench increment and 2.5 kg machine-press increment;
- freeze the expected machine-press progression to 72.5 kg while bench load remains 87.5 kg until its current rep target progresses.

Regression:
- practical grader must hard-fail invented increments when fixture increments are missing in future cases.


## Failure 4 — HT-PRAC-01 lacked active rep/RIR prescriptions

Observed problem:
- a progression decision is only interpretable relative to the current target;
- the history supplied reps/RIR but not the active bench or machine-press rep ranges.

Root cause: **practical fixture input sufficiency**.

Repair:
- add bench 3x4-6 @1-2 RIR;
- add machine press 3x8-12 @1-2 RIR;
- make current quad dose and known prior tolerated dose explicit.

Regression:
- future practical progression fixtures must expose the active prescription whenever a specific load/rep decision is scored.
