# Sales / Lead Conversion Practitioner — Evidence and Reuse Record 0.2.0

Status: revision-candidate support artifact. Not qualification evidence.

## Why 0.2.0 exists

Sales core 0.1.0 completed a fresh sealed 45-fixture qualification on gpt-5.6-terra with 40/45 passes and 0 critical hard fails. The only below-threshold families were:

- ownership-community-boundary: 0/3;
- next-commitment: 2/3;
- state-supersession: 2/3.

This revision uses only aggregate family-level evidence plus pre-existing professional research and architecture methodology. Hidden fixture text, grader keys and expected answers are intentionally not inspected or reconstructed.

## Hypothesis -> evidence -> decision

### H1 — Mixed ownership was under-operationalized

**Hypothesis:** 0.1.0 stated that Community retains complaint/reputation governance while Sales may qualify purchase intent, but did not operationalize accountable ownership, parallel workstreams, acceptance/fallback, or when unresolved non-sales work constrains sales progression.

**Evidence:**

- Existing Social Community competency CM-01 explicitly permits multi-label cases rather than sentiment-only collapse.
- Existing CM-06 requires minimum-sufficient handoff, one accountable owner, named destination, acknowledgment/acceptance state, and fallback rather than fire-and-forget.
- CM-06's evaluation hook explicitly covers a public price question evolving into both complaint and purchase intent.
- The Sales profession reconstruction already stated that mixed cases retain Community complaint/reputation governance while Sales may separately qualify purchase intent only if it does not trivialize or interfere with the unresolved complaint.
- Aggregate sealed result ownership-community-boundary = 0/3 indicates the 0.1.0 wording was not behaviorally sufficient.

**Alternative considered:** merge Community behavior into the Sales profession to eliminate routing ambiguity.

**Rejected because:** moderation, complaint/reputation governance and social listening are separate responsibilities with different authority, evidence and evaluation. Merging them would create a super-agent and blur accountability.

**Decision:** retain professional separation but add operational mixed-case semantics: owner-by-workstream, one accountable owner per workstream, sales-progression gate, acceptance/fallback for executable handoff, and duplicate-ownership prevention.

### H2 — “Smallest sensible next commitment” needed an explicit selection model

**Hypothesis:** 0.1.0 named good possible commitments but left ranking implicit when several actions were feasible.

**Evidence:**

- Existing profession reconstruction D5 identifies next-commitment size as a difficult professional judgment and says the goal is not always “close now.”
- Existing evidence record retained the principle that progression should reduce uncertainty or move to a proportionate next commitment, while proxy metrics such as appointments should not override fit or blockers.
- 0.1.0 already distinguished appointment readiness from general lead progression.
- Aggregate sealed result next-commitment = 2/3 indicates a residual selection failure, not a wholesale failure of the concept.

**Alternative considered:** encode a fixed ladder such as answer -> call -> appointment -> close.

**Rejected because:** a rigid funnel can increase friction, ignore prerequisites, and force appointments where verification, specialist handoff, or respectful close is professionally better.

**Decision:** add a comparative ranking rule: hard constraints -> decision relevance -> evidence sufficiency -> buyer readiness -> effort/reversibility -> dependency order, then choose the smallest sufficient action among the best feasible candidates. Require rationale against the nearest alternative when ambiguity remains.

### H3 — State continuity needed an operational supersession contract

**Hypothesis:** 0.1.0 said new authoritative facts may supersede old facts, but did not encode enough mechanics to distinguish replacement from scope difference or unresolved conflict, nor propagate changes into dependent decisions.

**Evidence:**

- Agent Architect runtime-state methodology explicitly requires conflict classification rather than silently selecting the latest value.
- Its authoritative-supersession rule says an explicit identified authoritative replacement for the same scope becomes current without redundant reconfirmation; prior provenance/history may be retained; recency alone is insufficient; ambiguity requires verification/escalation.
- The methodology requires stateful evaluation of authoritative supersession, contradiction and restart/resume behavior.
- Aggregate sealed result state-supersession = 2/3 indicates 0.1.0 was close but not operationally reliable.

**Alternative considered:** always treat conflicting values as unresolved and ask for confirmation.

**Rejected because:** this creates unnecessary friction and incorrectly lets stale memory block a clear authoritative replacement.

**Decision:** encode four-way relationship classification: explicit authoritative replacement -> supersession; different scope -> coexist; ambiguous authority/scope -> unresolved contradiction; newer-but-weaker -> no supersession. Require downstream replan when dependent drafts, comparisons, commitments or follow-ups rely on the superseded fact.

## Knowledge packaging delta

| Dependency | Packaging | 0.2.0 delta |
|---|---|---|
| Mixed-case ownership | EMBED_CORE + PROCEDURAL_STATE | Add owner-by-workstream, progression gate, acceptance/fallback semantics. |
| Next-commitment selection | EMBED_CORE | Add comparative ranking rather than a fixed funnel. |
| State supersession | EMBED_CORE + STRUCTURED_STATE | Add authority/scope relationship classification and downstream invalidation. |
| Current commercial facts | TOOL_BACKED / LIVE | Unchanged. |
| Current channel/org policy | LIVE / ORGANIZATION CONTEXT | Unchanged. |
| Legal/finance/trade-in/discount decisions | ESCALATE / TOOL_BACKED | Unchanged. |

## Reuse and boundary decision

- Sales remains one modular professional core; do not split qualification, objections and follow-up into separate agents absent evidence of measurable benefit.
- Social Community / Listening / Reputation remains a boundary dependency, not inherited profession ownership.
- Runtime state methodology is reused for supersession semantics because the state-consistency mechanism is profession-independent and already part of Agent Architect's professional architecture.

## Required development regressions before freeze

Public/development tests must include novel cases for:

1. pure complaint with incidental product mention -> no Sales takeover;
2. mixed complaint + genuine purchase interest -> separate workstreams/owners, no complaint bypass;
3. existing non-sales owner -> no duplicate promise/competing response;
4. missing fact versus appointment -> verify prerequisite before appointment when it is the blocker;
5. buyer explicitly ready for appointment with prerequisites satisfied -> do not over-question;
6. several feasible next steps -> smallest sufficient decision-useful commitment;
7. explicit authoritative same-scope replacement -> update without redundant reconfirmation;
8. newer but weaker/conflicting source -> do not overwrite by recency;
9. same-looking values with different scope/entity -> preserve both;
10. superseded fact invalidates downstream draft/open loop -> replan dependent state.

These are development cases, not reconstructions of hidden fixtures.

## Evaluation integrity for 0.2.0

- The previous sealed pack is now diagnostic historical evidence only for 0.2.0 and must not be reused as an unbiased release gate.
- Freeze the exact 0.2.0 artifact and digest after public/development regressions pass.
- Build a fresh preregistered held-out pack after freeze.
- Preserve thresholds independently of observed 0.2.0 hidden results.
- Include repeated trials for the three repaired families plus all prior critical authority/commercial-grounding invariants.

## Expert-gap discovery

What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?

Material additions retained in 0.2.0:

- ownership is attached to workstreams, not merely whole conversations;
- a handoff must have acceptance/fallback when execution exists;
- next-step quality depends on dependency order and buyer effort, not appointment maximization;
- authoritative replacement can invalidate downstream decisions, not just one stored field;
- recency, authority, scope and applicability must be separated.

## Red-team

**Senior practitioner criticism:** “The agent can still sound helpful while stealing ownership from Support or forcing a sales motion.” Repair: explicit owner-by-workstream and progression gate.

**Educator/assessor criticism:** “The old next-step rule was a slogan, not an observable decision model.” Repair: ranked candidate comparison and nearest-alternative rationale.

**Hiring/operator criticism:** “Stale facts can survive in drafts, handoffs or follow-ups even if the state store updated.” Repair: dependent-state invalidation and replan requirement.

## Limitations

- 0.2.0 is not qualified until a fresh sealed held-out cycle passes.
- It does not grant autonomous customer communication or booking authority.
- Domain-specific commercial facts and legal interpretation remain outside the reusable core.
- Aggregate prior failures support where to investigate, not what the hidden correct answers were.
