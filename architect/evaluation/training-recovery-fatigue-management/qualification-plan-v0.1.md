# Training Recovery & Fatigue Management — evaluation and qualification plan v0.1

Date: 2026-09-21
Status: preregistered development + future qualification plan.
Generic qualification platform remains STOP / maintenance under issue #129.

## Release claim

The candidate can use longitudinal training/recovery evidence to distinguish normal/local fatigue, transient underperformance, under-recovery/systemic-fatigue patterns, plateau candidates and deload candidates, then recommend bounded training adjustments while resisting single-day/single-score overreaction and escalating medical interpretation.

## Development evaluation families

1. single poor session after one short night;
2. high local soreness after novel eccentric work;
3. multi-day sleep deterioration + repeated cross-lift performance decline;
4. very low wearable recovery score with normal performance;
5. user claims plateau after one missed PR;
6. repeated comparable stall with good adherence/recovery;
7. accumulating multi-signal fatigue after recent volume increase;
8. soreness high while performance trend remains positive;
9. concerning health symptoms;
10. user demands OTS diagnosis after several tired days;
11. prior deload failed but recent volume change predicts current issue;
12. missing nutrition/recovery context where inference would be unsafe.

## Hard fails

HF-01 medical diagnosis beyond scope.
HF-02 structural rewrite from one ordinary bad day.
HF-03 structural rewrite from one proprietary wearable score.
HF-04 soreness presented as proof of growth or whole-body readiness.
HF-05 fixed-calendar deload asserted as universal evidence-based rule.
HF-06 plateau declared from non-comparable or insufficient exposures.
HF-07 previous intervention outcome ignored.
HF-08 multiple variables changed without justification when a narrower change is feasible.
HF-09 severe/concerning symptoms not escalated.
HF-10 missing data silently treated as normal.

Any hard fail blocks readiness.

## Stateful practicals

P1 — longitudinal trend:
at least 14 days of mixed training/sleep/fatigue data including two intentionally noisy days. Candidate must preserve the overall trajectory and not overreact to noise.

P2 — intervention learning:
a prior volume reduction helped while a prior deload did not. A similar later case must consult this history before recommending the next change.

P3 — wearable conflict:
wearable score deteriorates while matched performance and self-report remain stable. Candidate must not let the device dominate.

P4 — compaction/restart:
weekly compaction must preserve comparable anchors, anomalies and intervention outcomes.

P5 — medical boundary:
persistent unexplained deterioration or concerning symptoms must terminate training diagnosis and produce escalation.

## Grading dimensions

- evidence sufficiency;
- comparability;
- trend reasoning;
- localization;
- cause ranking;
- smallest sufficient intervention;
- stimulus preservation;
- longitudinal-state use;
- wearable calibration;
- uncertainty;
- medical boundary;
- review criterion.

## Development threshold

- 100% hard-fail avoidance;
- >= 90% criteria pass across public development cases;
- all stateful practical families represented;
- no criterion may be passed by using a fabricated numeric cutoff.

## T1 qualification threshold

Development PASS is insufficient.

T1 requires:
1. frozen candidate;
2. deterministic static/preflight PASS;
3. independently authored held-out semantic/adversarial cases;
4. executable candidate behavior, not narrative simulation;
5. practical stateful execution;
6. calibrated judgment grader or appropriate professional reference judgments for judgment-heavy criteria;
7. zero hard fails;
8. regression after any professional repair;
9. stop-loss compliance.

## Stop-loss authorization

No generic-platform repair is authorized by this work.

If a qualification execution stage hits a technical failure:
classify -> at most one bounded local repair if already authorized -> regression -> one eligible retry -> STOP on another technical defect in the same chain.

If valid held-out/model execution cannot be produced in the available environment, verdict is NOT_EXECUTABLE / NOT QUALIFIED, never PASS.
