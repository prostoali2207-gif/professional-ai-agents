# Evidence Aggregation Policy Result — 2026-08-15

## Verdict

**SCOPED PASS** for deterministic claim-state aggregation.

The gate passed all 7 registered cases after correcting one root-cause defect: a retracted/withdrawn primary support lineage must invalidate dependent supporting descendants in that same lineage. Secondary copies cannot rescue an invalidated upstream claim.

## Claim states

- `SUPPORTED`
- `PARTIAL`
- `CONFLICTED`
- `CONTRADICTED`
- `UNVERIFIED`

No probabilistic confidence score is produced.

## Proven rules

1. Count independent evidentiary roots, not URLs.
2. Dependent republishing is not replication.
3. Live contradictory primary evidence remains `CONFLICTED`; do not manufacture consensus.
4. Retracted/withdrawn primary support invalidates dependent supporting descendants in the same lineage.
5. Superseded evidence is excluded from current support; it does not create a live conflict with current evidence merely by existing historically.
6. Unknown lineage/methodological metadata cannot be promoted to independence.
7. Secondary-only evidence is at most `PARTIAL` when the claim requires primary-source verification.
8. Do not emit pseudo-precise numeric confidence absent an empirically calibrated probabilistic model.

## Cases

- Independent, methodologically distinct primary support → `SUPPORTED`
- Multiple dependent copies of one line → `PARTIAL`
- Independent live primary support vs contradiction → `CONFLICTED`
- Retracted support plus dependent secondary descendants → `UNVERIFIED`
- Missing dependence metadata → `PARTIAL`
- Superseded support vs current contradiction → `CONTRADICTED`
- Independent secondary-only support → `PARTIAL`

## Red-team / unresolved gap

This policy is intentionally not universal across professions. The evidence threshold required for `SUPPORTED` must depend on the **claim class and stakes**. A safety-critical engineering claim, medical-risk claim, legal/regulatory claim, empirical benchmark claim, product hypothesis, and low-stakes descriptive statement cannot share one evidence threshold.

Therefore the next required layer is a **claim-class/stakes-aware evidence requirement model**. It must specify required source authority, lifecycle checks, independence/diversity expectations, freshness, replication burden, acceptable secondary evidence, and abstention/escalation behavior per claim class.

## Scope limitation

This is a deterministic policy gate, not a calibrated epistemic probability model. It proves state-transition logic on registered cases; it does not prove that evidence metadata extraction or claim classification will be correct in live research.