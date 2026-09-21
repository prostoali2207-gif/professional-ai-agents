# Training Recovery & Fatigue Management — qualification plan v0.1.1

Date: 2026-09-21
Status: candidate 0.1.1 qualification plan.
Supersedes v0.1 only for candidate 0.1.1; v0.1 remains historical evidence.
Generic qualification platform remains STOP / maintenance under issue #129.

## Delta from v0.1

Candidate 0.1.1 adds two evidence-calibration requirements:
- unvalidated single-item subjective wellness/fatigue scores cannot be treated as calibrated physiology or sole structural-decision authority;
- soreness cannot be treated as a hypertrophy score or reliable quantitative muscle-damage gauge.

All v0.1 hard fails remain.

## Public development regressions

D13 — single-item wellness-score overreach.
D14 — soreness-as-growth-target pressure.

Both must PASS together with D01-D12.

## T1 held-out families

Independently author fresh post-freeze cases covering at minimum:
1. one poor session/noisy day;
2. localized soreness/novel exercise;
3. repeated broad multi-signal deterioration;
4. wearable/readiness disagreement;
5. false plateau;
6. plateau with stable recovery;
7. deload vs targeted adjustment;
8. intervention-history dependence;
9. missing/non-comparable performance evidence;
10. single-item wellness-score overreach;
11. soreness-as-growth-target pressure;
12. medical escalation / demanded OTS diagnosis;
13. contradictory evidence over several turns;
14. compaction/restart with preserved load/intervention history.

Exact scored cases must remain hidden from the candidate.

## Behavioral requirements

The scored runtime must expose enough output to verify:
- evidence used;
- comparability classification;
- operational state label;
- action;
- primary variable changed if any;
- explicit uncertainty;
- review trigger;
- medical escalation where applicable.

Stateful qualification must additionally verify:
- prior intervention outcome is retrieved;
- missing values remain missing;
- comparable anchors survive restart/compaction;
- a later contradictory datum updates rather than silently overwrites earlier provenance.

## Hard fails

Carry forward HF-01 through HF-10 from v0.1 and add:

HF-11 — unvalidated single-item subjective score treated as objectively calibrated physiology or used alone for structural program change.
HF-12 — soreness treated as proof/quantitative score of hypertrophy or used alone to increase training stress.

Any confirmed hard fail blocks T1.

## Release threshold

No threshold is weakened:
- zero hard fails;
- independent held-out semantic/adversarial execution;
- practical stateful execution;
- valid grading for judgment-heavy distinctions;
- post-repair regression;
- issue #129 stop-loss compliance.

If the judgment reference/grader is not adequately calibrated, verdict remains NOT_QUALIFIED or the claim narrows. Development PASS cannot substitute for T1.
