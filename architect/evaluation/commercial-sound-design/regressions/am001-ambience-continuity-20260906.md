# Regression — AM-001 ambience continuity — 2026-09-06

Status: **ACTIVE REAL-MEDIA REGRESSION / CANDIDATE EXTEND EVIDENCE**

## Incident

In Toyota Yaris AM-001 R5, the accountable user reported that the reel sounded somewhat better overall, but the underlying production ambience still changed audibly from shot to shot because different source clips carried different room/background sound.

The defect is not simply excessive noise. The edit exposes cut boundaries acoustically: each new picture shot arrives with a different ambient fingerprint.

## Failure classification

- picture edit source identity: unchanged
- false vehicle/product sound: no
- deterministic codec/render failure: no
- **sound-design continuity / perceptual QC: yes**

Working label: `AMBIENCE_CONTINUITY_FAIL`.

## Regression assertion

For a picture-led commercial sequence assembled from multiple source takes recorded in the same nominal location, the sound designer must not automatically preserve each clip's raw ambience when doing so makes the acoustic environment jump at every edit.

The candidate must explicitly decide whether the sequence needs:

1. one continuous ambience/room-tone bed;
2. perspective-motivated ambience changes;
3. deliberate silence/negative space; or
4. another coherent acoustic strategy.

Raw production audio should be reintroduced selectively for authentic hero actions when it serves the concept and remains truth-preserving.

## Pass condition

PASS when the exported soundtrack feels like one intentional acoustic world and cut-to-cut ambience changes are either imperceptible or perceptually motivated.

FAIL when the viewer can hear the montage primarily because each shot brings a different background/noise floor.

## Evidence boundary

This is a real production regression for the Commercial Sound Design candidate. It is not independent holdout evidence and cannot by itself qualify the capability.
