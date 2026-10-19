# Build, Practical Use, and Optional Formal Qualification

Status: operative Agent Architect policy (2026-10-19).

## Decision

**Formal repository qualification is optional by default.** It is a separate evidence/credentialing track, not a prerequisite to building an applied `SKILL.md`, completing practical development checks, or starting bounded real work with a candidate.

The user supplies the objective; Agent Architect still owns profession reconstruction, hidden competencies, tacit judgment, authoritative evidence, alternatives, tools, risk boundaries, failure modes, and root-cause repairs. This policy removes duplicated qualification ceremony, **not** professional substance, safety checks, or direct verification of observable work.

## Default path: BUILD -> CHECK -> USE -> LEARN

1. **BUILD.** Follow the profession-first architecture and the pre-SKILL gate. Reuse/adapt proven capability when appropriate; preserve knowledge provenance, operational instructions, and coverage of material hidden competencies.
2. **CHECK.** Define the intended task and authority boundary; run a *small, risk-proportionate* set of direct practical checks: representative real work, material adversarial/failure case(s), relevant tool/state/security guards, and targeted regression when something changed. Render/execute and inspect the outcome when possible. Fix substantive failures before calling the checked task ready.
3. **USE.** A candidate can be used immediately within the checked scope, with human supervision or other limits proportional to remaining uncertainty. Do not label it `QUALIFIED`, `T1`, `EXPERT-VALIDATED`, `PRODUCTION-PROVEN`, or assert untested performance. Record known limitations and what was actually checked. Do not block a low-risk practical task on a generic sealed-pack, multi-provider, repeated-trial, full held-out, or qualification-infrastructure gate.
4. **LEARN.** Observe real outcomes, user corrections, overrides and incidents. Triage the root cause, repair the right layer, add a targeted regression, and retest. Evidence from deployment may justify a later formal qualification, but it does not silently certify the candidate.

**Minimum check record:** task/scope, artifact version or commit, checks and observed results, material failures/limitations, supervision/authority boundary, and follow-up/feedback route. Keep it short; no parallel qualification dossier is necessary for ordinary work.

## When formal qualification IS requested or necessary for a claim

Initiate the full, independent qualification track only if:
- the user explicitly requests it;
- a repository/library promotion to lifecycle `qualified` / internal `T1 QUALIFIED` is intended;
- another explicitly specified contract or claim requires the corresponding formal qualification evidence.

For that track, retain frozen scope, independent/held-out evaluation, preregistered thresholds, hard-fails, identity/integrity controls, practical evidence, and the existing stop-loss policy. Never weaken a required threshold for PASS, and never portray a candidate's practical checks as formal certification.

Formal qualification is **not** a default prerequisite for ordinary candidate use, project-level application, exploratory research, or iterative improvement.

## Risk/authority override, independent of the qualification label

- For high-stakes, regulated, irreversible, externally consequential, security/privacy-critical or unsupervised autonomous actions, require evidence and controls proportional to the actual consequences **before granting that authority**. These may include professional review, representative scenario checks, runtime verification, approvals, least privilege, limits, reversibility and monitoring.
- If sufficient evidence/controls are unavailable, **narrow authority or keep a professional human in the loop**. Candidate use is not permission to make unsafe consequential decisions or execute unverified side effects.
- These safeguards depend on risk, not on whether the expensive formal qualification track ran. Conversely a `QUALIFIED` label never substitutes for deployment-specific safety and validity checks.

## Terminology and precedence

- **Practical readiness**: task-scoped, directly checked ability to work under declared limits; may apply to a `candidate`.
- **Formal qualification / T1**: exact frozen artifact passed its separate internal qualification contract; only then may it claim `QUALIFIED`.
- **T2/T3**: independent expert validation and monitored production evidence respectively; neither follows automatically from practical readiness or T1.
- **Pre-SKILL gate**: readiness to assemble a professional skill after adequate architecture; it is *not* formal agent qualification.

Read general phrases such as "evaluation before readiness", "practical evaluation passed", or "required release gates" in the Agent Architect documents as **risk-proportionate practical readiness for the declared task**, unless the artifact explicitly opts into formal qualification or makes a trust/library claim that requires it. Specific hard safety, authority and evidence requirements continue to apply.

Do not extend this policy retroactively to change existing frozen qualification records, statuses, sealed packs, thresholds or completed artifacts. Change the default *routing* for future work, not the validity of past evidence.

## Decision hygiene

At each creation/revision, ask: "What does an experienced practitioner see missing?" Red-team from a senior practitioner, educator/assessor, and hiring-manager perspective. Repair material gaps without turning that inspection into another mandatory multi-week qualification process.

Trade-off: less initial statistical confidence for ordinary candidate use, offset by narrow claims, targeted practical checks, observed field feedback, and escalation for consequential authority. When this trade-off is unacceptable, choose formal qualification or independent professional validation.
