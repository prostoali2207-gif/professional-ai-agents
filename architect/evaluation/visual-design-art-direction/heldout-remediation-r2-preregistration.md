# Visual Design / Art Direction 0.1.0 — held-out authoring remediation r2 preregistration

Status: **PRE-SCORE / evaluator-infrastructure remediation only**

Issue: #158

Frozen professional candidate (unchanged):
- commit `e8be839b02f181193afe076839c6ae94fb477a9b`
- candidate `SKILL.md` blob `9d251d97a84e16ade91c8ced07425f9208f9f900`
- professional-model blob `bbea595e299445cf79f798ed1e86eecd0b53cd50`

Prior r1 held-out authoring gate ended `NOT_EXECUTABLE — HELDOUT_AUTHORING_GATE` after its preregistered bounded whole-pack budget was exhausted. No r1 rejected case is eligible evidence for this cycle. Candidate scoring calls remain zero.

## Evidence compatibility

The authoritative judge calibration run `33262394565` remains reusable because this remediation does not change the release judges, judge prompt/decision construct, calibration corpus, calibration thresholds, candidate, professional families, P0 policy, or FULL release requirement.

Frozen calibration corpus ciphertext SHA256 remains `7ff98e8a9eb8bb82edb0c0a8ebde78553dd40f08487b1eb85f0412ac291ddeb1`.

Release judges remain:
- Gemini `gemini-3.5-flash-lite`
- Groq `openai/gpt-oss-120b`

The Groq call used during held-out *authoring* is a construct-quality auditor, not a candidate scorer and not a substitute for the calibrated release judges.

## Root-cause classification

The r1 authoring architecture generated one 20-case corpus in a single author call and then required ten independent family audits to all pass. A single weak family discarded the complete corpus. Audit output was intentionally binary and hidden case content was not inspected. This created a multiplicative whole-pack acceptance bottleneck and expensive full-pack regeneration without adding candidate independence.

The remediation changes only the evaluator-owned corpus-production mechanism. It does not repair, tune, observe, or score the candidate.

## r2 authoring design

Author and audit **one family at a time**.

For each required family, in the frozen order below:
1. Gemini authors exactly two fresh candidate-free cases for that family under a family-specific contract.
2. Deterministic structural validation runs.
3. Groq independently audits the two cases only for held-out construct quality: freshness, self-containment, realism, non-leakage, safe/generic baseline, grounded hidden criteria, and contrastive validity where paired.
4. The **first** pair that passes the unchanged construct-quality audit is accepted for that family.
5. Rejected or structurally invalid pairs are discarded without reading, editing, substituting, or semantically repairing their hidden content.
6. After all ten families have an accepted pair, the 20 accepted cases are aggregated and sealed once.

Required families:
`FRAMING, REFERENCE, DIVERGENCE, CRAFT_JUDGMENT, MOBILE, TRUTH, CONTRACT, CRITIQUE_REPAIR, ADVANCED_MEDIA_ROUTING, AUTHORITY_BOUNDARY`.

Paired contrast families remain:
- `REFERENCE`
- `MOBILE`
- `TRUTH`
- `ADVANCED_MEDIA_ROUTING`
- `AUTHORITY_BOUNDARY`

## Frozen authoring budget and stop rule

Maximum author attempts: **3 per family**, counting every Gemini author call whether it fails structural validation or construct audit.

Acceptance rule: **first construct-valid audited pair per family**. There is no ranking or choosing among multiple passing pairs.

If any family has no accepted pair after attempt 3, stop the cycle as `NOT_EXECUTABLE — HELDOUT_AUTHORING_GATE_R2`. Do not increase the limit, edit a rejected case, alter the family contract/audit rubric/model, inspect candidate outputs, or generate a fourth pair in this cycle.

Maximum envelope before sealing: 30 Gemini author calls + 30 Groq construct-audit calls. Actual calls should stop as soon as each family obtains its first accepted pair. Candidate calls = 0 throughout authoring.

## Independence / anti-cherry-picking rules

Forbidden before the sealed corpus identity exists:
- candidate execution or candidate-output inspection;
- reuse of r1 rejected hidden cases;
- case-level human/AI editing after an audit result;
- choosing the “best” among multiple passing pairs;
- changing family semantics in response to rejection;
- changing release judges, thresholds, P0 policy or professional scoring rubric;
- publishing hidden brief/context/criteria/P0 text.

Construct QA is allowed because it occurs before candidate exposure, uses candidate-free material, and accepts by a preregistered first-pass rule rather than by candidate outcome.

## Resource / execution gate

Run static/no-secret checks first. Metered authoring requires explicit issue-command/manual authorization and repository credentials. The workflow must never run metered authoring automatically on push or pull request.

Exact provider billing/quota is account-specific and not assumed here. Stop on quota exhaustion or non-transient provider failure; do not infer professional failure.

## Release boundary after seal

A successful r2 seal only makes the semantic qualification executable. It is **not** professional PASS.

After seal, freeze the held-out ciphertext identity into the release configuration before candidate scoring. FULL semantic held-out scoring and the rendered P1–P4 practical gate remain mandatory. A professional failure must produce `REVISE/FAIL` according to the frozen release policy and must not be rerun against the same held-out pack merely to seek a better stochastic outcome.
