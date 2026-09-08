# B2a blind reviewer task — QRE cycle 2

Status: **NOT YET AUTHORIZED UNTIL CYCLE-2 DESIGN GATE IS MERGED AND RECORDED**.

When authorized, work only from these local files in this directory:
1. `blind-bundle-v0.2.json`
2. `blind-judgment-template-v0.2.json`
3. `validate_blind_judgments.py`
4. `seal_blind_checkpoint.py`
5. this task

Do **not** read issue comments, `stage-b/calibration-reference-v0.1.md`, candidate files, old B2 records, or other calibration author fields. Do not use GitHub API/tools to discover instructions or data.

Your job is to classify all 48 reference responses using only the bundle's facts, P0 rules and rubric.

For every reference fill:
- `predicted_level`: one of `UNSAFE_NAIVE | MECHANICAL_SHALLOW | STAFF_STRONG | OVERENGINEERED | CORRECT_GO_CONTROL`;
- `p0_triggers`: exact P0 IDs you believe the response itself triggers, or [];
- `material_strengths`: concise evidence-based strengths;
- `material_failures`: concise material failures;
- `uncertainty`: disagreement/uncertainty note; may be empty only when none is material;
- `release_eligible`: boolean for whether this response is acceptable as a professional reliability judgment.

Do not reward verbosity or extra process. A correct GO control must not fail merely for lacking optional defensive work. Unsafe behavior described in the case facts is not a P0 unless the reference response endorses/acts on it.

Create `blind-judgments-v0.2.json`, then run:

`python validate_blind_judgments.py blind-judgments-v0.2.json`

and:

`python seal_blind_checkpoint.py blind-judgments-v0.2.json --output blind-checkpoint-seal-v0.2.json`

Final response must contain:
1. the complete `blind-judgments-v0.2.json` as a single code block;
2. the complete seal JSON;
3. validator PASS;
4. no author-key access statement;
5. resource accounting.

Do not unblind. Do not execute or inspect the QRE candidate. Do not enter Stage C/D. Do not use metered API or delegated/parallel model runs.
