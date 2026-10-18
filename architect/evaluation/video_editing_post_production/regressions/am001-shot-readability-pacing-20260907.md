# Regression — AM-001 shot readability / pacing — 2026-09-07

Status: **ACTIVE REAL-MEDIA REGRESSION / NOT A NEW QUALIFICATION**

## Incident

Toyota Yaris AM-001 R6 used a coherent soundtrack repair but retained an overly compressed picture rhythm. The accountable user reported that transitions felt too fast and viewers would not have enough time to inspect the car.

This failure is distinct from transition effects. The issue is insufficient perceptual dwell/readability at the sequence level.

## Failure classification

- capture insufficiency: **NO for this defect**
- deterministic render/tool failure: **NO**
- business-fact failure: **NO**
- perceptual craft / pacing self-QC: **YES**

## Regression assertion

A short-form commercial edit must not optimize for maximum shot count or minimum runtime at the expense of product readability.

For every material shot, export self-QC must ask:

1. what information/product feature is this shot asking the viewer to read?
2. how long does a realistic mobile viewer need to register it?
3. is the cut occurring before that information has landed?
4. is a lower-value shot consuming time that should be given to a hero/proof shot?
5. would removing one shot improve comprehension more than shortening every shot?

## Pass condition

PASS when hero/proof shots have enough dwell to be perceptually read and the sequence does not feel like a series of flashes.

FAIL when the viewer can identify the presence of shots but cannot comfortably inspect the product before the next cut.

## Repair pattern demonstrated by R7

- reduce shot count rather than uniformly stretching the whole edit;
- allocate more time to front hero, side profile, rear three-quarter, door/interior reveal, cockpit and final hero;
- preserve faster detail shots only where their information load is low;
- target readability first, then optimize retention.

This regression proves one concrete pacing/self-QC failure mode. It does not by itself qualify broad real-media editorial craft.
