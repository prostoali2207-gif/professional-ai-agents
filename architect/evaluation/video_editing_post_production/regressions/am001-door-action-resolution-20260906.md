# Regression — AM-001 Door Action Resolution — 2026-09-06

Status: **ACTIVE REGRESSION / NOT A NEW QUALIFICATION**

## Source incident

Applied case: Toyota Yaris AM-001 real-media post-production, 2026-09-06.

The R3 candidate used a real door-opening source shot. The export showed the door beginning/opening and then cut almost immediately to the next interior shot. The accountable user noticed that the beat felt weak because the door opened and the sequence moved on before the action produced a satisfying perceptual payoff.

The available source contained enough post-open material to resolve the action. R4 extended the door beat through a visible post-open state and then cut into the cockpit. The user judged the corrected door moment acceptable.

## Failure classification

- source/capture insufficiency: **NO for this defect**
- deterministic render/tool failure: **NO**
- missing automotive fact/business truth: **NO**
- missing professional decision vocabulary: **NO evidence**
- perceptual craft / export self-QC: **YES**

The candidate failed to detect an obvious action-resolution defect in its own export before human review.

## Regression assertion

Given source footage containing a physical action with a usable resolved state, a real-media post-production candidate must not:

- cut away after only the setup/start of the action when the intended beat requires the result;
- confuse source availability with perceptual resolution in the final export;
- declare continuity/delivery finish acceptable without checking the action payoff in the rendered sequence.

The candidate must inspect the export and record:

- action setup;
- resolved/payoff state;
- hold/readability;
- relationship of the following cut to the action.

## Pass condition

PASS only when the exported sequence either:

1. lets the viewer register the resolved action before the next cut; or
2. intentionally interrupts the action for a defensible rhythmic/semantic purpose that survives perceptual review.

An accidental "starts action -> immediate unrelated cut" is FAIL.

## Evidence boundary

This regression proves one concrete self-QC failure mode. It does not by itself qualify broad real-media editorial craft or create a new professional core/specialization.
