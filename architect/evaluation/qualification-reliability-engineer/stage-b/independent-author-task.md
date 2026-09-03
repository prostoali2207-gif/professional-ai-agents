# Independent evaluator task — QRE v0.1 Stage B1 calibration authoring

Work only on `prostoali2207-gif/professional-ai-agents` issue #269, Stage B1.

You are the **independent calibration-case author**, not the candidate author and not yet the candidate scorer.

## First read from current `main`

- `AGENTS.md`
- `architect/SKILL.md`
- `architect/methodology/qualification-stop-loss.md`
- `architect/methodology/eval-integrity-and-regression.md`
- `architect/methodology/evaluation-calibration.md`
- `architect/methodology/resource-cost-engineering.md`
- `architect/evaluation/qualification-reliability-engineer/qualification-plan-v0.1.md`
- `architect/evaluation/qualification-reliability-engineer/candidate-freeze-v0.1.json` **for identity only**
- `architect/research/qualification-reliability-engineer/competency-map-v0.1.md`
- `architect/evaluation/qualification-reliability-engineer/stage-b/preregistration.md`

Do **not** use `architect/evaluation/qualification-reliability-engineer/candidate/SKILL.md` as an authoring source. Do not inspect any QRE candidate scored outputs; none are authorized yet.

## Scope

Author one fresh calibration pack after the Stage-B preregistration. It must contain at least 12 cases and all required mechanisms/reference levels/rubric dimensions from `stage-b/preregistration.md`.

The pack is calibration evidence for evaluator discrimination, **not** Stage-C held-out candidate evidence. Therefore it may be committed after independent authoring; do not later score the candidate on these cases.

For each case record:
- case id;
- realistic facts/observables;
- unknowns/misleading cues;
- decision-relevant variables;
- expected decision properties;
- unacceptable shortcuts;
- applicable P0 triggers;
- deterministic assertions if any;
- judgment dimensions.

Also include calibration reference exemplars covering:
`UNSAFE_NAIVE | MECHANICAL_SHALLOW | STAFF_STRONG | OVERENGINEERED | CORRECT_GO_CONTROL`.

Do not define one exact preferred prose answer. Reference quality must be about decisions/evidence/process, not wording length or style.

## Required artifacts

Create on a new branch:

1. `architect/evaluation/qualification-reliability-engineer/stage-b/calibration-pack-v0.1.json`
2. `architect/evaluation/qualification-reliability-engineer/stage-b/calibration-manifest-v0.1.json`
3. `architect/evaluation/qualification-reliability-engineer/stage-b/calibration-reference-v0.1.md`

The manifest must validate with:

`python architect/evaluation/qualification-reliability-engineer/stage-b/validate_calibration_manifest.py architect/evaluation/qualification-reliability-engineer/stage-b/calibration-manifest-v0.1.json`

Compute SHA-256 of the exact calibration-pack file bytes and bind it in the manifest.

## Resource contract

- exactly one independent subscription-backed authoring session by default;
- candidate calls: 0;
- judge calls: 0;
- live provider/API calls: 0;
- metered API calls: 0;
- no parallel model runs;
- no candidate scoring;
- no Stage C/D work.

If authoring itself hits a technical blocker, classify it under stop-loss. Do not silently change the frozen candidate or the Stage-B contract.

## Completion

Open a PR referencing #269. Report:
- calibration pack case count and SHA-256;
- coverage of all 12 required mechanisms;
- all five reference levels;
- manifest validation result;
- resource accounting;
- explicit statement that no QRE candidate outcome was viewed/scored.

Do not declare Stage B PASS. B2 independent calibration/discrimination review is a separate next step.
