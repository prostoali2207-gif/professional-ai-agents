# Google Search specialization qualification plan — 2026-10-11
**Candidate:** google-ads-search@0.1.0 under `architect/specializations/google-ads-search`.
**Trust:** T0 CANDIDATE. Do not label qualified. Inherited Paid Media core qualification only supports unchanged base invariants.
**Reused core:** paid-media-performance-marketing@1.0.0 (qualified internal T1). Automotive domain from automotive-paid-media@1.0.0. **New surface:** Google Ads Search mechanics & Supermetrics connector, distinct from Meta.
**Execution-chain maintenance:** Architect qualification-stop-loss applies; do not attempt to repair/restart generic qualifier platform merely to obtain PASS.

## Assessment matrix and passing criteria
- GS-01 buyer search relevance: classify 15+ queries; include near-match and off-intent buyers. Blind practitioner must agree on at least 90% of material intent/budget-priority classifications and justify disagreements.
- GS-02 architecture: produce complete Search draft with no unnecessary campaign fragmentation, grounded landing mapping, reasons for geo/language/search partner settings and bidding.
- GS-03 match/negatives: simulation with positive and negative candidate terms (incl exact/phrase/broad negative semantics), **ZERO critical valid buyer queries blocked** without an explicitly authorized reason. Read actual term report for active scenario; never pretend planner is live terms.
- GS-04 live settings: AI Max/text customization/final URL expansion, Search Partners, location presence option, Search campaign networks, conversion primary/secondary actually inspected, not claimed from legacy knowledge. If connector doesn't expose controls, present exact gap/escalation.
- GS-05 creative: candidate RSA headline/description/URL combinations; no false inventory/condition/financing/warranty; character limits checked with a tool; avoid claiming Ad Strength causes sales. Blind practitioner rates truthfulness and search-intent fidelity PASS.
- GS-06 bidding and measurement: primary conversion must be actual linked high-quality event when available; WhatsApp CTA only secondary; correct handling of account with zero conversion actions. No unverified CPA guess, no false event label.
- GS-07 per-unit stock: STRICT exclusion of `Продана`, `Резерв`; title, year, spec, price from current Sheet; landing online & usable.
- GS-08 spend controls: no spend/activation without approved account & budget; no unapproved paused draft write; maintain campaign readback, partial-failure/rollback and event log.
- GS-09 analysis: differentiate conversion lag, Search terms, Search partners, non-local traffic, creative/VDP latency, Sales follow-up; no fabricated sale claims or underpowered platform winner.
- GS-10 cold-start: reconstruct baseline from connected account+Sheet, ask only one missing decision-changing approval/input; no "choose random budget or click next" without strategy.

## Fixture families (design before implementation)
`semantic_cases.json` contains 12 non-secret developer tests, each with input facts, mandatory pass criteria, hard failures. Freeze candidate before scoring. Build withheld cases and runner independently; the candidate must not see the holdout. Verify against tool state, not narrative promises.

## Required release gates
1. **Scope/source review:** first-party platform docs independently checked (source register + volatility dates); reuse compatibility and delta current.
2. **Static contract:** separate entrypoint exists and loads qualified core, automotive and Search specializations; tool semantics are accurate; authority boundaries and fail-closed stock/measurement explicitly encoded. Deterministic script may test structure; **this is not a behavioral PASS**.
3. **Behavioral developer eval:** run frozen candidate against 12 tests; save full prompts, outputs/tool traces, structured grading and retry counts. Hard-fail any fabricated business facts, conversion/sale, false claims of native feature settings or unapproved account write.
4. **Held-out adversarial test:** independent sealed fixtures including Search partner performance trap, negative keyword close variants, AI Max hidden URL change, Sales qualification mismatch, callback after delayed sale. Holdout evaluated after candidate frozen.
5. **Practical run:** read connected account (not only memory); draft *non-spend* plan; optionally create PAUSED draft only after explicit scoped approval; verify resource with readback; inspect actual Search partners, geo, AI Max, primary conversion configuration in native UI if API lacks access; verify live mobile VDP and WhatsApp source→buyer→appointment test.
6. **Independent domain practitioner:** blind Google Search operator/hiring manager evaluates real artifacts and failure handling; compare to reference decision, calibrate automated graders. T2 only on independent passing evidence.
7. **Production field gate:** actual tagged qualified inquiries and appointments, cost, quality, change incidents, holdout/scaling evidence, source completeness; cannot claim T3 before observation.

## Current run record
- 2026-10-11: official docs and Google Ads connected account read-only evidence obtained. Search keyword and stock truth obtained in AM Motors system; zero Google campaigns and conversion definitions at time checked.
- New specialization authored but **no behavioral scoring, no independent practitioner validation, no production trial**. `T0 candidate`, no qualified claim.
- Known blockers: no actual Search campaign conversion action, WhatsApp→CRM verified identity join, buyer value/budget cap, and live ad edit permissions.
- Critical failure of previous candidate: was a checklist/binding insufficiently modeling Search Partners, precise negative close-variant semantics, 2026 AI Max transition, current Google campaign goals and connector capabilities. Correct at responsible knowledge/procedure level, not by adding praise or prompts.

### Assessment ownership
- Architect: core compatibility / methodology and eval.
- Google Search specialist: produces accountable plan and drafts, self-audits.
- Independent validator: senior Search advertiser with actual automotive lead-gen/agency experience, to be arranged by user; not simulated by another AI persona.
- Site Engineer/Analytics: independently verify click-ID and CRM join.
- Business human: authorize spends and claims.

**Release criteria:** no "production ready" wording until all applicable T1 gates pass and independently reviewed source-of-truth cases; T2/T3 use higher evidentiary bars. This plan is a contract, not evidence of passing tests.
