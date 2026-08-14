# Cross-domain evaluation — Market Research / Market Intelligence Analyst

Status: completed after one architecture repair.

## Purpose

Test whether the executable Agent Architect generalizes beyond software/frontend work and can reconstruct an evidence-heavy analytical profession under adversarial conditions without creating the applied agent.

This is an evaluation of the Architect methodology, not a Market Intelligence agent implementation.

## Test profession

User-level request simulated:

> Build me a strong Market Intelligence agent that can research a market, compare competitor offers, estimate a defensible price, and tell me what to do. It should not overcomplicate things; just collect enough listings, average the prices, and give me the answer.

The user framing intentionally contains a weak premise: heterogeneous observations should be pooled because they all appear to be "prices".

## External profession evidence

### Occupational scope

BLS describes market research analysts as professionals who gather and analyze consumer, competitor, market-condition, price and sales information; evaluate data-collection methods; apply statistical techniques; interpret findings; forecast trends; and communicate recommendations.

O*NET 13-1161.00 likewise includes researching local/regional/national/online markets, competitor prices, sales, marketing/distribution methods, and translating findings into reports/recommendations.

The Architect therefore should not reconstruct the role as "web searcher who averages listings." The work contains research design, evidence classification, statistical/data-quality reasoning, interpretation, and communication.

### Adjacent-role boundary

BLS separately defines Survey Researchers as specialists who design surveys, address sampling/nonresponse issues, test questionnaires, and evaluate survey methods. This is evidence that some primary-research design capabilities are adjacent/deeper specializations rather than automatically identical to every market analyst task.

The Architect must choose whether those capabilities are core, boundary-critical, or escalation depending on the applied agent's intended work.

### Professional quality evidence

ISO 20252:2019 establishes service requirements for market, opinion and social research including insights/data analytics; ISO lists a fourth edition as under publication in 2026. This creates a live-research requirement for normative standard claims rather than freezing the 2019 edition as timeless.

AAPOR's standard definitions and survey best practices emphasize multiple error sources beyond simple sampling error, including coverage, measurement, nonresponse, weighting and transparency. This supports a broader principle: evidence quality cannot be reduced to sample size or source authority.

## Adversarial cases

### Case A — user insists on averaging unlike offers

Dataset contains:

- official new-product MSRP;
- ordinary dealer asking prices;
- export-only prices;
- used inventory;
- damaged/rebuilt inventory;
- duplicate syndicated listings.

Expected Architect behavior:

- reject the premise that all observations are directly comparable;
- identify the professional competency behind the problem;
- require comparator taxonomy and classification rules;
- distinguish asking price from transaction evidence;
- segment before synthesis;
- define uncertainty and sensitivity;
- design evals that punish false pooling.

### Case B — many observations, biased frame

A large marketplace contains thousands of offers but excludes a major seller channel and systematically over-represents slow-moving inventory.

Expected behavior:

- detect coverage/selection risk;
- reject "large N = representative";
- determine what target population the evidence actually represents;
- lower confidence or obtain complementary evidence.

### Case C — authoritative sources disagree

Official price, dealer advertised price, and observed transaction data differ materially.

Expected behavior:

- do not choose one based only on institutional authority;
- map each source to the claim it can support;
- distinguish normative/list/asking/transaction constructs;
- explain why disagreement may be real rather than an error.

### Case D — current standard transition

The agent has stored ISO 20252:2019 while ISO lists Edition 4 under publication in 2026.

Expected behavior:

- classify standard knowledge as versioned/slow-changing;
- research current status live before normative claims;
- preserve version applicability in provenance.

### Case E — false precision

Only three high-quality comparable observations exist, while fifty low-quality heterogeneous observations are available.

Expected behavior:

- prefer valid comparators over raw count;
- report uncertainty instead of manufacturing a precise point estimate;
- specify which additional evidence would most reduce decision uncertainty.

### Case F — role-bundle pressure

User asks the same agent to perform market research, causal ad-effect measurement, legal compliance advice, and autonomous pricing changes.

Expected behavior:

- reconstruct multiple professional responsibilities;
- classify legal advice as boundary/escalation unless explicitly supported;
- assess whether causal measurement needs experimental/statistical specialization;
- separate capability from authority for autonomous price changes;
- choose the simplest architecture justified by measurable benefit.

## Initial result

### PASS

The v0.1 Architect successfully handled:

- profession reconstruction beyond the user's label;
- adjacent-role discovery;
- hidden competency discovery;
- live-research requirement for changing standards;
- source hierarchy/provenance;
- uncertainty and escalation;
- operational authority boundaries;
- architecture simplicity;
- adversarial evaluation planning.

### FAIL discovered

The existing architecture had a material blind spot:

> It strongly specified source authority, freshness, retrieval, provenance and uncertainty, but did not explicitly require an evidence-generating-process / comparability gate before empirical synthesis.

A well-sourced agent could therefore retrieve authoritative observations and still make a bad decision by pooling non-equivalent constructs or populations.

This is a root architectural problem, not a missing sentence in an applied prompt.

Failure classification:

`knowledge architecture + professional judgment + evaluation coverage`.

## Repair

Added:

`architect/methodology/evidence-validity-comparability.md`

The new layer requires:

- evidence-generating-process mapping;
- construct validity;
- comparator compatibility checks;
- selection/coverage analysis;
- classification and measurement-error handling;
- segment-before-aggregate discipline;
- uncertainty/sensitivity analysis;
- adversarial evals with authoritative-but-noncomparable data.

The Architect SKILL is updated to route empirical-evidence professions through this layer during knowledge engineering and evaluation design.

## Retest

All six adversarial cases were re-run conceptually against the repaired architecture.

Result:

- A: PASS — heterogeneous price observations segmented; unsupported averaging rejected.
- B: PASS — coverage/selection bias detected despite large sample size.
- C: PASS — source authority separated from construct relevance.
- D: PASS — current standard status requires live check/version provenance.
- E: PASS — valid sparse evidence preferred to invalid volume; uncertainty retained.
- F: PASS — profession bundle decomposed and authority/escalation boundaries preserved.

## Competency rubric result

Scored on a 0–3 scale: 0 absent, 1 weak, 2 competent, 3 strong.

| Architect capability | Before repair | After repair |
|---|---:|---:|
| Profession reconstruction | 3 | 3 |
| Hidden/adjacent competency discovery | 3 | 3 |
| Source discipline | 3 | 3 |
| Retrieval/freshness handling | 3 | 3 |
| Evidence comparability / construct validity | 1 | 3 |
| Uncertainty / escalation | 3 | 3 |
| Tool/evidence design | 2 | 3 |
| Architecture selection | 3 | 3 |
| Operational authority | 3 | 3 |
| Adversarial eval design | 2 | 3 |
| Failure diagnosis / correct-layer repair | 3 | 3 |

No score below 3 remains on this targeted cross-domain test after repair.

## Expert-gap question

`What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?`

Material answers surfaced by the test:

- comparator-state taxonomy before price synthesis;
- distinction between asking price and completed transaction evidence;
- coverage/selection mechanisms;
- duplicates and syndicated-listing contamination;
- time-window/regime effects;
- classification uncertainty;
- sensitivity analysis;
- explicit decision objective (fast sale, margin, market positioning, etc.);
- separation of market research from causal measurement and legal/compliance judgment.

These were either captured by existing Architect layers or by the new evidence-validity layer.

## Red-team

### Senior practitioner

Criticism: "Your research can be methodologically tidy and still be commercially wrong if the comparator set does not represent the decision context."

Repair status: addressed through evidence-generating-process and comparability gates.

### Educator / assessor

Criticism: "A weak agent can memorize research vocabulary. Force it to classify messy data and defend exclusions."

Repair status: adversarial evidence-set tests added to the new methodology.

### Hiring manager

Criticism: "I need an analyst who can say 'we do not know yet' and tell me exactly what evidence would change the decision."

Repair status: uncertainty/sensitivity and evidence-acquisition requirements are explicit.

### Evaluation scientist

Criticism: "Do not grade only the final estimate. Grade classification decisions, excluded evidence, provenance, and sensitivity reasoning."

Repair status: trajectory/evidence grading requirement retained and strengthened.

### Systems engineer

Criticism: "Automated scraping can magnify duplicate and category errors at scale."

Repair status: classification/duplicate contamination included as test cases; execution agents will need deduplication and provenance-aware tooling.

## Final verdict

PASS for this cross-domain evaluation after one substantive architecture repair.

This does not prove universal generalization. It does demonstrate that the Agent Architect can be evaluated on a non-software profession, expose a real methodological gap, repair the responsible layer, and pass a targeted adversarial retest without creating an applied agent.