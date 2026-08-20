# Market & Competitive Intelligence Research Practitioner — Evidence and Reuse

## Reconstruction evidence

The target work was reconstructed as market/competitive intelligence rather than a generic SMM role. Material work includes current market research, buyer/demand investigation, competitor/offer monitoring, social/platform signal interpretation, primary-research interpretation, evidence validity/comparability, provenance/dependence control, longitudinal monitoring and decision-useful handoff.

Methodology dependencies include:
- `architect/methodology/source-knowledge-engineering.md`
- `architect/methodology/evidence-validity-comparability.md`
- `architect/methodology/professional-core-reuse.md`
- `architect/methodology/evaluation-calibration.md`

The applied UAE automotive system supplied authentic evidence/failure patterns including purposive competitor samples, account-normalized social metrics, visible-comment buyer questions, incomplete visual/transcript observability, price/commercial comparability requirements and MI→Strategist handoff requirements.

## Professional Core Library reuse decision

Candidates inspected included qualified `paid-media-performance-marketing/1.0.0` and `growth-experimentation-measurement/1.0.0`.

Decision: `BUILD NEW` for the target profession.

Rationale: those cores provide useful adjacent invariants—measurement integrity, causal-claim discipline, live verification and experiment boundaries—but neither owns market/competitive research, evidence collection, source provenance, buyer/competitor investigation, primary research, non-observation handling or longitudinal intelligence monitoring. Reusing either as the profession would create a material responsibility/construct mismatch.

Evidence retained conceptually: adjacent qualified cores informed compatible boundary principles, but no prior qualification was inherited as evidence that this Market Intelligence core itself is qualified.

## External reuse search

External market-intelligence/competitive-analysis skill repositories were inspected as candidate sources, including the `deanpeters/Product-Manager-Skills` investigation and market-landscape components. Useful ideas included search-plan discipline, Fact/Inference/Assumption separation, do-not-invent constraints, evidence stacking, substitutes/non-consumption and repeatable monitoring schemas.

Decision: `REJECT for direct REUSE/ADAPT; use as inspiration/evidence only`.

Reason: public skill/prompt provenance and plausible workflow design do not establish compatibility with this profession boundary or provide local qualification evidence for material professional claims.

## Failure-driven repair history

### v0.2 real failure

A fresh practical diagnostic showed a real epistemic-calibration defect: the candidate preserved representativeness, causal and strategy-authority limits, but intermittently demoted valid within-sample observations/calculations to `INFERENCE` or `HYPOTHESIS` merely because external validity was weak.

Repair: preserve the frozen v0.2 base and add the minimal `epistemic-status-calibration-overlay-v0.1.md`, forming v0.3. The overlay separates exact-claim epistemic status from support scope, external validity, causal validity and uncertainty.

### Evaluation failures kept separate

Several earlier enum/action graders were rejected as construct-invalid because they treated professional synonyms or administrative labels as behavior failures. MI-R10, for example, correctly detected selection/sampling-frame bias while a grader demanded a broader `PRIMARY_RESEARCH_LIMIT` label. Those failures were documented and were not converted into PASS; candidate changes were not made from grader-only defects.

Final qualification therefore used single-decision held-out cases for isolated critical constructs plus a separate end-to-end practical work sample.

## Qualification evidence

Frozen assembly:
- base blob: `7af5b93c1a4d499b5972a0dd20aec8e4253a9651`
- overlay blob: `e0685f4a5a868cd2e2d119d9c01d8ad36bb59b21`
- assembly digest: `sha256:7dee471c3b707927fd255a2539548882e2b18765c943d0e6c7dbee9a2edbff62`

Fresh single-decision held-out:
- fixture: `architect/evaluation/market_competitive_intelligence/v03_single_decision_heldout.json`
- 10 independent professional decisions × 3 stochastic trials = 30 evaluations
- result: `30/30 PASS`
- model: `gemini-3.1-flash-lite`, thinking level medium
- workflow run: `32377948412`, successful attempt/job after an earlier infra-only 429
- successful sealed artifact digest: `sha256:1968ce5399b4f0b6361a7b460284d7d53fcca51cda91c8de0f94df357c541664`

Fresh end-to-end practical work sample:
- fixture: `architect/evaluation/market_competitive_intelligence/v03_fresh_practical_case.json` (`MI-P02`)
- theme deliberately differed from the repair examples: inspection/history-proof content
- trials: 3
- result: `3/3 PASS`, no mismatches
- model: `gemini-3.1-flash-lite`, thinking level medium
- workflow run: `32378536989`
- sealed artifact digest: `sha256:8d69f04dabc74170b9b0e612559e0906bba0e3bfb05eb64ef5a1842cc76d7ead`

The practical sample simultaneously required useful synthesis, sample-bound facts, prevalence limits, causal limits, observability limits, confounding recognition, unresolved commercial facts, stopping discipline and Strategist handoff.

## Reuse contract

Stable transferable invariants include evidence-contract discipline, source/evidence validity, epistemic calibration, selection/coverage limits, comparability, provenance/dependence, non-observation handling, longitudinal collection-drift control, prompt-injection resistance, stopping and evidence-vs-strategy authority boundaries.

Domain/live bindings that must not be frozen into the universal core include UAE automotive prices, current inventory, vehicle history/condition, platform metrics/features, competitor state, legal/privacy/terms requirements, market benchmarks and organization-specific business facts.

Applied reuse decision should normally be `ADAPT` when the professional responsibilities remain the same and only domain/live/project bindings change. Any new tools, data collection authority, automated external actions, new primary-research execution, domain-specific comparability rules or changed handoff responsibility require targeted regression/new interaction evaluation.

## Known limitations

- Qualification does not establish current market knowledge; live facts require retrieval.
- Qualification does not establish specialist legal advice or advanced causal/statistical expertise outside the declared core.
- Qualification used the declared Gemini runtime; portability to other model/runtime/tool environments requires validation proportional to the changed behavior surface.
- UAE automotive specialization and the production composed Market Intelligence agent still require independent compatibility and practical/adversarial evaluation.