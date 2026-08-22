# MI-R10 grader calibration review v0.1

Date: 2026-08-20
Candidate: `candidate-professional-model-v0.2.md`
Candidate blob: `7af5b93c1a4d499b5972a0dd20aec8e4253a9651`

## Question

Does repeated `SELECTION_LIMIT` on MI-R10 indicate a candidate professional failure, or a grader construct failure because v4 required `PRIMARY_RESEARCH_LIMIT`?

## Case

Twelve buyers who purchased from one budget dealership volunteer for interviews; nine mention monthly-payment sensitivity; requested inference is prevalence among all UAE vehicle shoppers.

## Candidate behavior

Across all three v4 trials the candidate selected the required high-level action `REJECT_OR_BOUND` and selected `SELECTION_LIMIT` as the critical control.

## Professional-model binding

The frozen v0.2 core explicitly requires material empirical evidence to map the population represented and the sampling/selection mechanism; it says sample size is not a substitute for representativeness. Its primary-research section requires a defensible target population, sampling/recruitment frame, eligibility rules, response/nonresponse handling and coverage-bias assessment before prevalence inference. It also separately declares that qualitative interviews do not estimate population prevalence absent suitable design.

## Calibration judgment

`SELECTION_LIMIT` is not a weaker or different professional response here. It identifies the causal validity defect that prevents transport from this convenience volunteer sample to all UAE vehicle shoppers. `PRIMARY_RESEARCH_LIMIT` is a broader administrative/category label, whereas the actual invalidity is selection/coverage.

Therefore the v4 failure is classified as `GRADER_CONSTRUCT_TOO_NARROW`, not a candidate P1 failure.

This judgment does **not** convert v4 to PASS. The observed v4 cases are now contaminated for release qualification. Candidate v0.2 remains byte-identical and must face a fresh held-out release set whose critical controls are defined at the professional mechanism level rather than by one preferred taxonomy label.

## Integrity rule

- do not modify v0.2 from MI-R10 results;
- do not regrade v4 as release PASS;
- create fresh held-out fixtures not paraphrasing MI-R10;
- require all critical cases to pass across preregistered repeats;
- run the end-to-end practical sample only after the fresh semantic gate passes.
