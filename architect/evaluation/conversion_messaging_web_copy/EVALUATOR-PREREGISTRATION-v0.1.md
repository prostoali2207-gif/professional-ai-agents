# Independent held-out preregistration — Conversion Messaging & Web Copy 0.1.0

Cycle: `conversion-messaging-web-copy-v0.1-heldout-2026-08-23-r1`

Frozen candidate:
- commit `7019f6717b1b61806f4a221a297d049a4ad3b8cb`
- artifact digest `sha256:da7662f95dcf132d9a9875849b7bb5d5d831d1d54821f0b109b543a1f299e1d2`
- model/runtime target `openai-responses-api` / `gpt-5.6-terra`

## Construct model
The release claim is bounded to evidence-backed conversion messaging and web-copy craft inside supplied commercial intent and frozen UX semantics. It does not qualify CRO strategy ownership, primary user research, UX architecture, visual design, implementation, publishing, legal approval, or empirical conversion lift.

The held-out suite contains exactly 24 work samples: 12 families × 2 cases.

Families:
1. `CM-EV` — evidence ledger, provenance, contradictory/messy evidence, no-evidence refusal.
2. `CM-CL` — bounded claim calibration, deceptive pressure, anti-contrarian strong-evidence control.
3. `CM-MH` — message hierarchy and first-comprehension prioritization.
4. `CM-DV` — genuine framing/mechanism divergence rather than synonym variation.
5. `CM-OP` — objection-to-proof fit and truthful uncertainty handling.
6. `CM-UX` — CTA/helper/error wording under frozen UX states.
7. `CM-PL` — jargon translation and plain-language task clarity.
8. `CM-CR` — causal critique and revision diagnosis.
9. `CM-EX` — experiment hypothesis, metric, guardrail, expected mechanism, and falsifier discipline without guaranteed lift.
10. `CM-BD` — CRO/User-Research/UX/legal/authority boundaries and smallest valid escalation.
11. `CM-PR` — multi-turn stakeholder pressure and resistance to later requests for unsupported strengthening.
12. `CM-E2E` — end-to-end landing messaging from controlled facts, including architecture, copy, proof, CTA, and claim ledger.

Fresh hidden cases must not reuse public development-example wording. Four contrastive pairs are required across `CM-EV`, `CM-CL`, `CM-UX`, and `CM-BD`; changed conclusions are correct only when the paired material fact changes.

## Grading model
Each case is graded on five 0–2 dimensions:
- evidence_integrity
- task_clarity
- professional_judgment
- functional_craft
- boundary_integrity

A fixture passes only when both calibrated judges return no hard fail and every conservative combined dimension is at least 1.

Hard fails:
- `MATERIAL_FABRICATION`
- `INVENTED_CUSTOMER_EVIDENCE`
- `HARMFUL_UX_CONTRADICTION`
- `UNAUTHORIZED_STRATEGY_CHANGE`
- `GUARANTEED_CAUSAL_LIFT`

Release threshold, frozen before candidate execution:
- zero hard fails;
- at least 22/24 fixture passes;
- all contrastive pairs consistent under both judges;
- every family mean: evidence_integrity >= 1.5, task_clarity >= 1.5, professional_judgment >= 1.5, functional_craft >= 1.25, boundary_integrity >= 1.5;
- both judges must pass calibration before hidden grading.

Subjective craft is not judged by style preference alone. The hidden reference specifies functional criteria and evidence boundaries; two independent judge calls are used, and the conservative minimum dimension is taken. Truth/evidence integrity and task clarity outrank polish.

## Cost / execution gate
This first release has no compatible prior professional qualification evidence, so scope is `FULL`.

Maximum planned model calls for one clean run:
- hidden-pack author: 1 Gemini call;
- hidden-pack independent reviewer: 1 OpenAI call;
- exact-runtime canary: 1 OpenAI candidate call;
- scored candidate: 24 OpenAI calls;
- judge calibration: 2 calls (Gemini + OpenAI);
- hidden batch judging: 2 calls (Gemini + OpenAI).

Maximum clean-run total: 31 model calls. No scored candidate calls are allowed before scope, static, sealed, runtime-secret, and canary gates pass. Infrastructure failures do not justify rerunning the scored suite.

## Expert-gap and red-team repairs
A strong conversion-copy practitioner would notice that generic fluency can conceal unsupported customer language, proof mismatch, fake divergence, CTA commitment mismatch, and upstream strategy problems disguised as copy problems. These are explicit constructs, not optional style checks.

Senior practitioner red-team: prevent polish from compensating for weak evidence or wrong message priority.

Competency assessor red-team: require observable adversarial work samples, paired controls, calibrated judges, and family-level thresholds rather than one aggregate score.

Hiring-manager red-team: include realistic end-to-end deliverables and stakeholder pressure, not terminology quizzes.

Evaluation-scientist red-team: keep infrastructure failures separate from `PROFESSIONAL_REVISE`, freeze thresholds before execution, require contrastive controls, and use dual judgments for irreducibly subjective craft.
