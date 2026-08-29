# Visual Design / Art Direction 0.1.0 — held-out authoring remediation r3 preregistration

Status: **PRE-SCORE / evaluator-infrastructure remediation only**  
Issue: #158

Frozen professional candidate remains unchanged and unobserved:
- commit `e8be839b02f181193afe076839c6ae94fb477a9b`
- candidate `SKILL.md` blob `9d251d97a84e16ade91c8ced07425f9208f9f900`
- professional-model blob `bbea595e299445cf79f798ed1e86eecd0b53cd50`
- candidate calls before r3: `0`

Authoritative release-judge calibration remains run `33262394565` = `CALIBRATION_PASS`, ciphertext SHA256 `7ff98e8a9eb8bb82edb0c0a8ebde78553dd40f08487b1eb85f0412ac291ddeb1`. Release judges, calibration corpus, calibration thresholds, FULL scope, required families and P0 policy are unchanged.

## Evidence from closed r2

R2 run `33264920878` stopped `NOT_EXECUTABLE_HELDOUT_AUTHORING_GATE_R2` at family `DIVERGENCE` after its preregistered 3/3 author attempts.

Sanitized counters were:
- `author_calls = 6`
- `audit_calls = 2`
- `attempts_used = {FRAMING:2, REFERENCE:1, DIVERGENCE:3}`
- `candidate_calls = 0`
- `hidden_content_printed = false`

Because FRAMING and REFERENCE account for the two construct-audit calls, all three DIVERGENCE attempts failed before independent audit. Therefore the actionable r2 failure is the model-to-validator structural interface, not candidate behavior and not a Groq construct-quality verdict. The exact rejected hidden payloads remain uninspected and are not eligible evidence.

## R3 infrastructure change

R3 keeps the r2 family-local first-pass acceptance policy but removes free-form JSON shape generation.

Gemini Interactions authoring must use top-level native structured output (`response_format`, MIME `application/json`, JSON Schema). The author model generates only semantic case fields. Evaluator-owned metadata is assigned deterministically after parsing:
- `id`
- `family`
- `pair_id`

The schema requires exactly two semantic case objects, each with:
- non-empty `brief`
- non-empty `context`
- non-empty `constraints`
- non-empty `competent_generic_baseline`
- `professional_criteria` array with at least three non-empty strings
- `p0_guardrail` either null or an object with a preregistered category and non-empty trigger.

No semantic quality requirement is weakened. The independent Groq construct-quality audit prompt/decision remains materially unchanged from r2 and still cannot assess or predict the frozen candidate.

## Required families and paired contrasts

Required families, frozen order:
`FRAMING, REFERENCE, DIVERGENCE, CRAFT_JUDGMENT, MOBILE, TRUTH, CONTRACT, CRITIQUE_REPAIR, ADVANCED_MEDIA_ROUTING, AUTHORITY_BOUNDARY`.

Declared contrastive pairs remain:
- `REFERENCE`
- `MOBILE`
- `TRUTH`
- `ADVANCED_MEDIA_ROUTING`
- `AUTHORITY_BOUNDARY`

## Acceptance, budget and stop rules

For each family:
1. Gemini authors exactly two fresh cases using the frozen schema and family requirement.
2. Deterministic validation verifies schema-derived invariants and P0 category membership.
3. Groq independently audits construct quality.
4. The **first** audited pair with `accept=true` is accepted. There is no comparison among passing pairs.
5. A rejected pair is discarded without inspection, editing, repair or reuse.

Maximum author attempts: **3 per family**, every Gemini author call counts. At most one Groq audit per successfully parsed/validated authored pair.

If any family has no accepted pair after attempt 3, stop `NOT_EXECUTABLE — HELDOUT_AUTHORING_GATE_R3`. No fourth pair, no model/rubric/family semantic change and no candidate observation in this cycle.

Maximum envelope before sealing: <=30 Gemini author calls and <=30 Groq construct-audit calls, stopping at first accepted pair for every family.

## Independence / contamination controls

Forbidden before sealed r3 ciphertext identity exists:
- candidate execution or candidate-output inspection;
- reuse or semantic inspection of r1/r2 rejected hidden cases;
- tuning author prompts from rejected hidden case wording;
- editing a rejected case to make it pass;
- ranking multiple passing pairs;
- changing release judges, release thresholds, P0 policy or professional rubric;
- publishing hidden case content or hidden expected criteria.

R3 may report only sanitized structural class/counters, accepted-attempt numbers, provider/model identity, ciphertext identity and candidate call count.

## Execution boundary

Static/no-secret CI must pass before any r3 metered run. Metered authoring must remain explicitly issue-command/manual authorized and must never run automatically on push or pull request.

A successful r3 seal only makes semantic qualification executable. It is not professional PASS. The sealed ciphertext identity must be frozen into release configuration before any candidate scoring. FULL semantic held-out scoring and rendered P1–P4 practical qualification remain mandatory afterward.
