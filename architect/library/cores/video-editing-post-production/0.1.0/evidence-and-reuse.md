# Video Editing & Post-Production Core — Evidence and Reuse Decision

Status: candidate evidence record. Accessed 2026-08-17.

## Reconstruction evidence

- Blackmagic Design's official DaVinci Resolve training separates editing, color, audio post, visual effects and delivery while teaching rough-to-fine iteration and timeline pacing. These materials support the integrated post-production boundary but remain vendor-specific implementation evidence: https://www.blackmagicdesign.com/products/davinciresolve/training
- The official DaVinci Resolve 20 Beginner's Guide describes ripple edits as a way to refine timing/pacing and provides an observable end-to-end editorial workflow: https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Beginners-Guide.pdf
- Avid's Media Composer Editing Guide documents professional editorial, media-management, conform and output mechanics. It is used for workflow/tool evidence, not as a universal aesthetic authority: https://resources.avid.com/SupportFiles/attach/Media_Composer_Editing_Guide_2023.x.pdf
- Adobe's rough-cut guidance distinguishes structural review from later sound, color, transitions and effects, supporting the rule that polish should not precede validation of sequence and pacing: https://www.adobe.com/creativecloud/video/post-production/cuts-in-film/rough-cut.html
- ITU-R BS.1770-5 defines algorithms for measuring programme loudness and true-peak audio level. It supports measurement literacy without creating one universal delivery target: https://www.itu.int/rec/R-REC-BS.1770
- EBU R 128 and its short-form supplement distinguish programme loudness, loudness range, maximum true peak and short-term behavior. EBU broadcast targets are evidence for method and a scoped regime, not automatic social-platform targets: https://tech.ebu.ch/publications/r128 and https://tech.ebu.ch/publications/r128s1
- W3C WCAG 2.2 SC 1.2.2 requires captions for prerecorded synchronized media in its accessibility scope and WAI notes that automatic captions often need editing. This supports caption review and explicit applicability: https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html and https://www.w3.org/WAI/perspective-videos/captions/
- The Academy Color Encoding System documentation defines input/output transforms and metadata needed to reproduce viewing pipelines and creative intent. This supports explicit color-pipeline provenance for color-managed work: https://docs.acescentral.com/amf/specification/ and https://docs.acescentral.com/amf/guides/implementation/
- YouTube's official upload guidance says to preserve recorded frame rate and publishes current encoding requirements; Meta publishes placement ratios and safe-zone guidance. These are examples of volatile destination specifications that belong in live context, not the stable core: https://support.google.com/youtube/answer/1722171 and https://www.facebook.com/business/help/980593475366490
- FFmpeg's official filter and probe documentation establishes a reproducible tool surface for transforms, metadata inspection and automated checks. Tool success does not prove perceptual success: https://ffmpeg.org/ffmpeg-filters.html and https://ffmpeg.org/ffprobe-all.html

## Evidence interpretation

Vendor manuals are strong evidence for their own tools and workflows but can promote vendor terminology. Standards are authoritative only within their scopes. Broadcast loudness values, cinema color pipelines and platform upload values are not interchangeable. Craft and taste remain partly tacit, so qualification requires real artifacts and calibrated comparative review rather than prose recall.

## Library reuse search

The current trusted catalog contains only `paid-media-performance-marketing@1.0.0`. Its business-value, measurement and spend-governance responsibilities do not cover editorial construction, media finishing or artifact QC.

External tool/prompt collections and NLE assistants may provide adapters or examples, but no inspected candidate supplies a locally qualified, tool-agnostic professional construct with provenance, truth-preservation, artifact-first QC, authority boundaries and practical/adversarial evaluation.

## Decision

`Video Editing & Post-Production Practitioner -> current catalog -> no compatible profession core -> BUILD NEW`.

Paid Media and Content Creator are rejected as parents because extension would mix strategy/creative-planning responsibility with execution/finishing responsibility and make failure ownership ambiguous. NLE/FFmpeg/AI editing tools remain optional adapters, not professional parents.

Unchanged evidence retained: none from an existing Professional Core.

Required new evaluation: every VE claim, with direct produced-artifact evidence for render/QC claims and calibrated human comparative review for irreducibly subjective craft. Until those gates run, lifecycle remains `candidate` and no behavioral PASS is claimed.

## Known gaps

- No domain-expert panel has yet calibrated subjective craft judgments.
- No representative runtime has yet demonstrated end-to-end render, perceptual inspection and repair.
- Current social-platform delivery requirements require live revalidation during specialization/execution.
- Advanced HDR, broadcast, cinema, immersive audio and high-end VFX are excluded from the initial candidate boundary.
