# Market & Competitive Intelligence — expert-gap red team v0.1

Date: 2026-08-20
Candidate under test: `candidate-professional-model-v0.1.md`, blob `b0f65c3720db08309ef9d9fa10df8f61021f9648`.

Required Architect question:

> What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?

## Senior practitioner perspective

### Gap A — Ongoing intelligence is change detection, not repeated report generation
A production MI function must distinguish baseline from delta, preserve collection scope/method, detect material changes, and avoid calling schema/sampling changes “market movement.”

Severity: P1 for an ongoing monitoring claim; P2 for one-shot research.
Repair implication: add explicit monitoring/change-detection invariant before reusable-core admission; evaluate scope/method drift versus genuine signal change.

### Gap B — Primary research method boundary is under-specified
The reconstructed profession includes interviews/surveys/authorized first-party buyer research, but v0.1 mainly specifies external/open-source collection. It does not explicitly say when qualitative interviews can discover themes versus when survey/sample design is required to estimate prevalence.

Severity: P1 if the core claims general market-research competence; otherwise narrow scope to secondary/observational intelligence.
Repair implication: either narrow profession name/scope or add primary-research design/interpretation boundary and evaluation.

### Gap C — Missingness/absence requires stronger interpretation rule
The evidence model records missingness, but v0.1 should explicitly prohibit interpreting “not observed/not found” as “does not exist” when collection coverage is incomplete.

Severity: P1 because competitor/buyer monitoring frequently encounters partial observability.
Repair implication: add absence-vs-nonobservation invariant and adversarial case.

## Educator / competency-assessor perspective

### Gap D — The current 16-case gate mostly tests classification decisions
It is useful but insufficient by itself to prove the candidate can produce an auditable end-to-end research artifact. The preregistered practical work sample remains mandatory.

Severity: P1 evaluation gap, not candidate-content failure.
Repair implication: add a frozen practical case requiring ResearchContract + evidence ledger + findings + counterevidence + stop + handoff, graded semantically and structurally.

### Gap E — Source-count rejection needs an explicit evidence-strength positive model
v0.1 rejects fixed N-source heuristics and lists relevant dimensions, which is good. Evaluation must verify the candidate can still synthesize when evidence is sufficient rather than becoming permanently cautious.

Severity: P1 evaluation gap.
Repair implication: include sparse-but-high-quality evidence and “evidence sufficient, stop” cases.

## Hiring-manager perspective

### Gap F — Decision usefulness must be graded
A report can be epistemically cautious yet commercially useless. The core should preserve a direct chain from decision need -> strongest supported findings -> implications/constraints -> unresolved questions -> named owner.

Severity: P1 evaluation criterion; candidate already partially encodes it.
Repair implication: practical grader must fail evasive disclaimer-only reports.

## Evaluation-scientist perspective

### Gap G — Current semantic gate is single-provider
Three stochastic trials on one model test reliability but not cross-model portability or grader independence.

Severity: P2 for candidate behavior evidence; P1 before broad “portable across models” claim.
Repair implication: qualify exact runtime/model scope now; require a second independent model/runtime before claiming portable behavior.

### Gap H — Designer-authored post-freeze held-outs are weaker than independently sealed fixtures
Candidate was frozen before adversarial cases were authored, which protects tuning leakage into v0.1, but the same Architect designed candidate and fixtures.

Severity: P2 evidence-independence limitation.
Repair implication: label first gate as frozen adversarial qualification; add independently authored/sealed held-out pack before strongest library maturity claim.

## Security / operations perspective

### Gap I — Collection adapters can silently alter the evidence population
Search ranking, scraper limits, API pagination, deleted/private posts, language filters and platform access changes can change observed data without a market change.

Severity: P1 for monitoring/benchmarking.
Repair implication: bind collector/tool/version/coverage metadata to evidence ledgers and monitoring deltas; evaluate collector drift.

## Decision

Candidate v0.1 must **not** be admitted to the Professional Core Library unchanged even if the currently running 16-case gate passes.

Required v0.2 repair before admission:
1. add longitudinal monitoring/change-detection discipline;
2. add primary-research method boundary or narrow the profession claim;
3. add explicit absence-vs-nonobservation rule;
4. bind collector/tool/coverage drift to evidence validity;
5. add an end-to-end practical work-sample gate.

The running v0.1 gate remains useful baseline evidence. Because these are behavior-relevant repairs, its PASS cannot certify v0.2; affected/new behaviors require fresh evaluation.