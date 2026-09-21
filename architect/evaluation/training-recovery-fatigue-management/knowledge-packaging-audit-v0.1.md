# Training Recovery & Fatigue Management — knowledge packaging audit v0.1

Date: 2026-09-21
Status: pre-SKILL audit.

| Competency | Hard decision | Material knowledge dependency | Packaging | Failure risk | Eval |
|---|---|---|---|---|---|
| RF-01 Load-response reconstruction | identify what changed before fatigue | training variables, temporal exposure, comparability | EMBED_CORE + REFERENCE | symptom-only reaction | recent-load-change cases |
| RF-02 Local vs accumulated fatigue | local soreness vs broader fatigue | localization, novelty, time course, cross-lift evidence | EMBED_CORE + PROCEDURAL | DOMS -> systemic label | local soreness adversarial |
| RF-03 Transient vs trend | one bad day vs structural issue | measurement noise, comparable anchors, longitudinal state | EMBED_CORE + STATE | overreact to one session | single-day trap |
| RF-04 Under-recovery/systemic pattern | infer broader recovery strain | multivariate trend logic; no single biomarker | EMBED_CORE + STATE | pseudo-diagnosis/recovery score | multi-signal trend |
| RF-05 Plateau | stall vs fatigue/noise | repeated comparable exposures, adherence/recovery | PROCEDURAL + STATE | one missed PR -> plateau | plateau trap |
| RF-06 Variable selection | volume vs intensity vs frequency | hypertrophy stimulus/fatigue trade-offs | EMBED_CORE + REFERENCE | change everything | smallest-change case |
| RF-07 Deload | deload vs local adjustment | limited/mixed deload evidence | REFERENCE + PROCEDURAL | fixed-calendar dogma | deload adversarial |
| RF-08 Sleep constraint | training issue vs sleep issue | athlete sleep consensus, individualized need | REFERENCE | universal sleep cutoff | poor-sleep trend |
| RF-09 Wearables | useful signal vs false precision | validity, specificity, device limitations | REFERENCE + LIVE_RESEARCH | proprietary score truth | wearable conflict |
| RF-10 Intervention learning | repeat/avoid prior change | intervention ledger and realized outcomes | STATE + PROCEDURAL | repeat failed action | history case |
| RF-11 Medical boundary | continue vs escalate | scope and red-flag principle | EMBED_CORE + ESCALATE | diagnosis or unsafe continuation | medical hard-fail |

## Packaging decisions

Always loaded:
- state labels are operational, not diagnoses;
- single-observation gate;
- comparability gate;
- multivariate trend requirement;
- smallest sufficient reversible change;
- medical boundary;
- no proprietary readiness score as sole authority.

Reference/deeper runtime material:
- profession/evidence register;
- competency-and-judgment model;
- longitudinal state contract.

Tool-backed:
- structured state schema validation when a state store exists;
- deterministic arithmetic/log parsing when volume or load summaries are computed.

Live research:
- device-specific accuracy/algorithm claims;
- materially new consensus or clinical guidance.

Escalate:
- OTS/NFOR diagnosis;
- injury/illness diagnosis;
- persistent clinically significant sleep or systemic symptoms.

## Runtime sufficiency conclusion

PASS FOR CANDIDATE AUTHORING.

The critical decisions have packaged operational depth and explicit failure behavior. No material decision is intentionally delegated to an undeclared proprietary score or base-model medical inference.
