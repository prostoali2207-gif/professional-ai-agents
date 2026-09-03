# Conversion Messaging & Web Copy v0.2 — evaluation plan

Status: development evaluation contract. No qualification run is authorized by this file.

Issue: #259

## Purpose

Evaluate the material v0.2 professional delta while preserving v0.1 invariants. The plan must distinguish professional evidence from infrastructure executability and must not disguise a retry of the stopped v0.1 held-out author/review/seal chain.

## Preserved baseline families

A future v0.2 release qualification must still cover the v0.1 release-critical behaviors:
- evidence/customer-language provenance and no-evidence refusal;
- bounded claims / anti-fabrication;
- message hierarchy;
- genuine framing divergence;
- objection/proof matching;
- CTA/helper/error semantics within frozen UX;
- jargon/plain-language translation;
- causal critique/revision;
- experiment hypothesis/metric/guardrail/falsifier discipline;
- CRO/User Research/UX authority boundaries;
- stakeholder pressure;
- end-to-end landing messaging.

Changed/new behavior requires fresh evidence. Unaffected v0.1 deterministic artifacts are prior evidence only, not a transferable PASS.

## New delta families

### CM-MM — message-match / entry-continuity

Competency claim: preserve material continuity between an approved acquisition/search entry promise and landing-page messaging while refusing unsupported source claims and without taking over acquisition strategy.

Representative adversarial cases:
1. Approved ad promise and CTA are supported; generic landing brief omits them. Expected: preserve the relevant promise/next action in page hierarchy without verbatim-copy requirement.
2. Ad says a stronger guarantee/discount/availability claim than evidence supports. Expected: do not propagate the claim; classify/escalate the source-message conflict.
3. Two entry ads differ in one material audience/offer fact. Expected: page variants change only where that difference justifies it.
4. Stakeholder asks to rewrite the landing page to maximize Quality Score. Expected: treat platform metric as diagnostic input, not the commercial objective; preserve CRO boundary.

Hard fail candidates:
- knowingly echo unsupported acquisition claim as page truth;
- silently change the approved offer/CTA commitment;
- claim message match guarantees conversion lift.

### CM-A11Y — accessible wording inside frozen UX

Competency claim: produce understandable link/action, label/instruction and error wording inside supplied interaction states without inventing UX/validation semantics or claiming copy-only accessibility conformance.

Representative adversarial cases:
1. Multiple `Learn more` links lead to materially different destinations. Expected: make purpose distinguishable from text/context available in the frozen UI.
2. Input format is supplied but label/helper text is ambiguous. Expected: clarify expected input without changing required fields.
3. Detected validation state says an email is malformed; existing error says `Something went wrong`. Expected: identify field/error in text and give authorized correction guidance if available.
4. User asks the copy practitioner to “make the site WCAG compliant” without rendered/semantic implementation evidence. Expected: improve wording within scope and explicitly refuse a copy-only conformance claim.

Hard fail candidates:
- invent required fields, validation rules or navigation behavior;
- hide a detected error behind generic persuasive wording;
- claim full accessibility conformance from copy alone.

### CM-L10N — localization/translatability

Competency claim: preserve message intent, evidence strength, CTA commitment and UX semantics across localized variants; distinguish localization from literal translation and escalate language/local-market uncertainty.

Representative adversarial cases:
1. English idiom/wordplay does not translate cleanly. Expected: preserve function/meaning rather than literal wording and flag creative loss/trade-off.
2. Target-language customer vocabulary is absent. Expected: do not present machine translation or marketer inference as voice-of-customer evidence.
3. Translation strengthens a bounded claim into certainty. Expected: reduce target wording to the same evidence state.
4. RTL/local-format requirements affect implementation. Expected: surface handoff requirement without pretending the copy layer has implemented i18n.
5. Regulated/high-stakes local wording cannot be independently verified. Expected: require qualified/local accountable review.

Hard fail candidates:
- invent target-language customer evidence;
- strengthen claim certainty through localization;
- certify language/local legal correctness without sufficient evidence or review.

## Baseline regression risk

Because D1-D3 touch entry context, CTA/microcopy, plain language, evidence calibration and boundaries, v0.2 must regress at least:
- no-evidence refusal / fabricated proof pressure;
- claim calibration;
- CTA/state semantics;
- CRO/UX boundary preservation;
- genuine divergence;
- end-to-end landing case.

## Grading dimensions

Use the existing v0.1 dimensions unless later evaluator evidence demonstrates a construct-valid change:
- `evidence_integrity`;
- `task_clarity`;
- `professional_judgment`;
- `functional_craft`;
- `boundary_integrity`.

For new families, graders must separately observe:
- continuity fidelity without unsupported repetition;
- accessibility wording correctness within supplied state;
- localization intent/evidence preservation and escalation quality.

## Evaluation form

Subjective craft cannot be released on one unvalidated scalar judge. Prefer calibrated comparative/multi-judge review for semantic/craft dimensions and deterministic checks where ground truth is mechanical (required state facts, forbidden claim tokens, source-message facts, preserved CTA commitment, supplied validation state).

Do not use conversion lift as a qualification ground truth. Causal lift remains downstream empirical evidence.

## Stop-loss identity

A future v0.2 qualification is a genuinely new candidate/release cycle only if the candidate contains the material D1-D3 behavior described in `professional-delta-v0.2.md`.

It must preregister its own execution-chain identities by stage. It may reuse stable platform mechanisms but may not treat a new issue/provider/transport as a reset of any failed stage inside that new cycle.

The stopped v0.1 #225/#237 chain remains terminal and is not reopened.

## Candidate assembly gate

Candidate assembly is authorized only because `professional-delta-v0.2.md` concludes `V0_2_JUSTIFIED` from source-backed professional gaps. The candidate must preserve v0.1 behavior unless explicitly changed above and must expose the new behavior in a way that can be elicited by CM-MM, CM-A11Y and CM-L10N work samples.
