# Growth Experimentation & Measurement — candidate v0.5 overlay

Status: CANDIDATE / NOT QUALIFIED / NOT LIBRARY-ADMITTED.

Base assembly: `professional-model-candidate-v0.1.md` + `v0.2-overlay` + `v0.3-overlay` +
`v0.4-overlay`. Apply this overlay last.

## Incident-derived professional gap

Held-out trial `H-GDS-02` (Gemini, gate `analytics-v0.4-stability-2026-08-27`, run
`33076139535`) directed a stop at the wrong arm. Configuration A cost 520 for 26 qualified
leads and returned 400 gross profit — 20 per lead, **net −120**. Configuration B cost 360
for 6 qualified leads and returned 1800 gross profit — 60 per lead, **net +1440**. The
candidate stopped B, the profitable arm, because B's cost per lead looked three times worse.

The root cause is a scope gap in the existing model, not a new principle. v0.1 states the
upstream-proxy protection three times and every statement is scoped to `SCALE`:

- "make a **scale** decision from an upstream proxy when downstream guardrails or economics
  contradict it" (prohibition);
- "An acquisition lift with materially worse downstream handling is not unrestricted
  **scale** evidence";
- the pre-`SCALE` evidence checklist.

`KILL` is defined as "commercially unacceptable under the approved economics" without saying
which arm that condemns when a diagnostic metric and the decisive metric rank the arms in
opposite directions. v0.3 adds only the negative form — do not apply a cost-gap threshold
without economics — and never states the positive selection rule. So the protection existed
for the scale direction and was absent for the stop direction.

## Added rule — metric precedence governs arm selection, not only scale

The precedence between a diagnostic metric and a decisive metric applies to **every** action
and, in a multi-arm comparison, to **which arm the action names**.

1. Classify each available metric as diagnostic or decisive for the registered question.
   Upstream acquisition metrics — cost per lead, cost per click, cost per qualified outcome,
   volume — are **diagnostic** whenever verified matured downstream economics or a registered
   business rule designating them are available. Matured verified downstream outcomes and the
   economics computed from them are **decisive**.
2. When the diagnostic and decisive metrics rank the arms in the **same** direction, the
   action targets the arm both condemn.
3. When they rank the arms in **opposite** directions, the action targets the arm that fails
   on the **decisive** metric. The diagnostic ranking must not select the target. It may be
   reported, and it may motivate an `ITERATE` to investigate the mechanism, but it cannot
   redirect the stop.
4. When no decisive downstream metric is available, the best available upstream metric may be
   decisive for a bounded reversible action. Say so explicitly rather than implying matured
   downstream evidence exists.
5. Record which metric was decisive. An action whose stated grounds are downstream economics
   while its target is the arm favoured by downstream economics is internally inconsistent
   and invalid.

The immature-outcome, fixed-horizon, registered-estimand, denominator, identity, causal-ceiling
and `SCALE` safeguards are unchanged. Nothing here loosens any of them: a stop that is correct
about the arm is still blocked when the registered horizon is incomplete and no guardrail
fired, and `SCALE` still requires everything v0.1–v0.4 require.

## Output contract v3

`decision_record.operational` gains two requirements.

- `target` is now a **structural identifier**, not a description. It must be exactly one
  string taken from the fixture's declared `arms` list. Do not return a phrase, a description
  of the comparison, or two arms joined together — an action applies to one arm. If the
  justified action genuinely applies to the whole experiment rather than an arm, the arms list
  will contain an identifier for that, and if it does not, the honest answer is
  `INCONCLUSIVE` with `INSUFFICIENT_EVIDENCE` recorded, not an invented target.
- `decisive_metric` names the metric class that actually selected the action and the arm,
  from the closed vocabulary. It is not a label for the most discussed metric; it is the one
  that, if reversed, would change the decision.

## Anti-patterns / hard failures

Fail the professional behavior if it:

- stops, or recommends stopping, the arm with the better matured downstream economics because
  its upstream acquisition metric looks worse;
- records `decisive_metric: MATURE_DOWNSTREAM_ECONOMICS` while targeting the arm that
  downstream economics favour;
- returns a `target` that is not one of the declared arms, or that names more than one arm;
- claims matured downstream economics as decisive when the case supplies none.
