# Authorial Voice v0.4 — held-out qualification preregistration

issue: #302
date: 2026-09-14
status: FROZEN BEFORE HELD-OUT EXECUTION

## Frozen candidate

- qualified parent blob: `d8eee4c6f9141f362d91a340c37dcae6ad6bfa71`
- v0.4 overlay blob: `abed0d6762299c82b82e603355beac9f79b4cca2`
- qualification protocol blob: `c9942aa64cead4f0b55c7949a6a59debbde88356`
- candidate status: CANDIDATE / NOT QUALIFIED / NOT LIBRARY-ADMITTED

## Development prerequisites

- visible targeted development: 18/18 PASS, run `34808976107`
- PBGS three-case practical: PASS / generalization signal observed
- practical evidence is not qualification evidence by itself

## Hidden distribution

Runtime author must create 17 fresh cases, one for each family:
- AV-Q1 generic-to-distinctive
- AV-Q2 reference-imitation trap
- AV-Q3 humor/proof conflict
- AV-Q4 correct no-humor
- AV-Q5 profanity pressure
- AV-Q6 persona continuity
- AV-Q7 spoken naturalness
- AV-Q8 anti-template
- AV-Q9 multilingual/register
- AV-Q10 strategy boundary
- AV-Q11 text-vs-performance boundary
- AV-Q12 reference diversity
- AV-Q13 safe pedagogic collapse
- AV-Q14 benchmark-to-execution transfer
- AV-Q15 visual proof economy
- AV-Q16 closure without lecture recap
- AV-Q17 fake spontaneity trap

No hidden case may reuse the exact visible development facts/phrasing.

## Evaluation independence

- hidden author: Groq/Qwen family
- candidate: Gemini family
- judge A: Gemini family
- judge B: Groq/Qwen family
- candidate never receives expected observables / answer key
- judges receive full fixture + hidden rubric only after candidate output exists
- no candidate retry / best-of-N
- evaluator JSON-format repair: max one retry per evaluator role

## Scoring

0 = material failure
1 = usable but weak
2 = professionally strong

Dimensions:
- truth_preservation
- brief_fidelity
- authority_boundary
- anti_imitation
- distinctiveness
- clarity
- speakability
- humor_function
- creator_native_execution
- earned_stance_quality
- benchmark_transfer_visibility
- visual_proof_economy
- closure_selectivity

Hard fail:
- fabricated facts/results/anecdotes
- reference cloning
- strategy/CTA boundary violation
- candidate presented as qualified
- SAFE_PEDAGOGIC_COLLAPSE on Q13
- BENCHMARK_WITHOUT_EXECUTION_TRANSFER on Q14
- VOICE_OVER_EXPLAINS_VISIBLE_PROOF on Q15
- LECTURE_RECAP_CLOSURE on Q16
- FAKE_SPONTANEITY_REPAIR on Q17
- physical vocal-delivery competence claimed from text alone

Per-case PASS:
- both judges pass
- zero hard-fail flags
- truth/brief/authority/anti-imitation >=1 from both judges
- all materially applicable new dimensions >=1
- relevant-dimension mean across both judges >=1.5

Overall hidden PASS:
- 17/17 cases pass
- zero hard-fail flags
- no judge pass/fail disagreement

## PBGS practical comparative review

Use exact applied artifacts:
- failed historical landing creative blob `2075489711777214e94e2e6f65863c30fce79419`
- v0.4 three-case stress-test blob `fcaeeb96c8a23213c39adf2dfced4450a8887818`
- current orientation creative blob `6d3141a06a115fb725e7d16d24ef1ff7e3f511eb`

Required:
- both judges agree v0.4 execution materially reduces pedagogic collapse versus historical failure
- truth/strategy preserved
- no reference imitation
- no fake spontaneity shortcut
- no claim of vocal-performance qualification

## Release rule

Qualification PASS requires:
1. 17/17 hidden PASS;
2. practical comparative PASS from both judges;
3. no execution invalidity;
4. exact frozen candidate identity verified.

A PASS qualifies only the Authorial Voice text-level extension. Narration/vocal performance remains separate.

Provider/runtime portability must be recorded as a revalidation trigger, not inherited automatically.

## RCE

Provider-backed workflow must be `workflow_dispatch` only.
