## Decision

Export is a hard fail. Missing-glyph boxes are MG-04 / TEXT_GRAPHICS, not a taste question and not a "fix in the next pass" item. I am recording `TECHNICAL_FAIL`, craft state `CRAFT_NOT_OBSERVED` for every Cyrillic-bearing time range (any earlier craft observation on those ranges is invalidated), and I am not advancing this to `PRACTICAL_PASS_CANDIDATE`. It is also an overlay-ledger failure (MG3-04): a tofu box carries no approved meaning, so those time ranges no longer map to their approved semantic statements.

Assumptions, stated: the Cyrillic copy is approved required wording; the piece is commercial/social with phone-size delivery; rendering happens in a headless container rather than on the design machine.

## Diagnosis

Latin rendering correctly proves the font loaded — it does not prove coverage. Four causes produce this exact symptom and they need different repairs, so I verify rather than guess:

1. The display face genuinely has no Cyrillic in its cmap. Common for display/editorial faces shipped Latin or Latin+Ext-A only.
2. The family covers Cyrillic but the file in the render environment is a Latin subset — a Google Fonts `unicode-range: latin` webfont slice or a self-subsetted build.
3. Coverage exists in Regular but not in the specific weight/style actually used; the renderer then silently falls back or synthesizes.
4. Preview/export divergence: the design machine has a system font with Cyrillic that absorbs the fallback invisibly, while the render container's fontconfig chain has nothing for those codepoints.

Verification I run, in the render environment and not locally: dump the cmap of every font file actually resolved, per weight and style, and intersect it against the full codepoint set extracted from all text content in all language variants; then confirm which font each text run resolved to in the export.

## Repair, ranked to preserve the authored type system

I will not "repair" this by dropping in whatever fashionable face happens to have Cyrillic, and I will not transliterate or romanize approved copy.

- **Preferred:** obtain the same family's Cyrillic-covering release (Pro/extended cut, or the full static file instead of the subset), install it in the render environment, and confirm the licence permits video embedding and container rendering. Design intent is preserved intact.
- **If the family has no Cyrillic at all:** author a deliberate script pairing — a companion face matched on skeleton, x-height, contrast, weight, width and terminal treatment, applied consistently to all Cyrillic-bearing layers so scene-to-scene coherence holds (MG3-01). This is a type-system decision requiring re-approval, not a substitution.
- **Glyph extension/commission:** only if licensed and justified; that is asset-authoring work outside this capability, so it routes out per MG3-14.
- I do **not** accept mixed-family drift within one scene, nor synthetic bolding of a borrowed face.

Metrics change either way. Cyrillic typically sets wider and denser, so every affected line break, grouping, safe placement and collision check against face, proof and CTA must be re-inspected — not just the glyphs.

## Lock and provenance handling

If the title or caption layers are `LOCKED_BY_APPROVAL` or `LOCKED_BY_USER`, a font change is locked-layer drift. I solve around it where feasible; otherwise I report the exact dependency and request the minimum unlock — the type system for Cyrillic-bearing layers only — and change nothing until it is granted (MG3-10).

The fix re-renders from the controlled source chain. I will not patch or re-encode the failed export (MG3-11).

## Pipeline hardening

- Build-breaking glyph preflight: all content codepoints across every language variant intersected against each resolved font's cmap per weight and style; any uncovered codepoint fails the render.
- Disable synthetic/silent fallback so a missing glyph errors instead of substituting.
- Assert font-load completion before the first frame is rasterized.
- Pin the font file by hash in the asset ledger with version and declared language coverage.

## Re-QC before any ready claim

Full re-export, decode, frame inspection at every Cyrillic time range, glyph and placement pass, phone-size craft observation including type-character fit for the new face, plus the affected parent VE-07 checks and the historically coupled MG-04 / MG3-06 regression cases from the frozen preregistration.

## Status recorded

`TECHNICAL_FAIL`; `CRAFT_NOT_OBSERVED`. Escalates to `BLOCKED_TECHNICAL` if no licensed covering file can be placed in the render environment, or `NEEDS_UPSTREAM_REVISION` if approved wording cannot be preserved legibly.
