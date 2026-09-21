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
