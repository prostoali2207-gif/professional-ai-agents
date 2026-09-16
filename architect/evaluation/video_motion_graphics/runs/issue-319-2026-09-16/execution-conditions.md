# Issue #319 Stage B — execution conditions

Recorded so the run is replayable and so the isolation claim is auditable.

## Route

Subscription-backed Claude Code, per the issue #319 **EXECUTION ROUTE CLARIFICATION**
(comment 5693435538, 2026-09-16T07:06:08Z). No `ANTHROPIC_API_KEY` or other metered API; paid API calls
= 0. Codex was not run in parallel as a second provider for this Stage B chain. Nothing in the frozen
contract — candidate, fixtures, thresholds, P0 set, scoring semantics, practical gate, transfer protocol,
evidence ceiling — was weakened to make the route executable, so the route was not classified
`NOT_EXECUTABLE`.

## Candidate runtime

Each of the 24 cases ran in a fresh, separately-contexted runtime. Its readable context was exactly five
files: the four frozen candidate-runtime documents and one prompt-only task file.

Candidate-runtime documents, extracted verbatim from freeze commit
`83fed979f9dd0c2cbed51fd2a4703a5e2f415c0d` (hashes in `candidate-runtime-bundle.sha256`):

| Load order | Source path at freeze commit |
| --- | --- |
| 1 | `architect/evaluation/video_motion_graphics/candidate-v0.3/SKILL.md` |
| 2 | `architect/library/cores/video-editing-post-production/0.1.0/professional-model.md` |
| 3 | `architect/evaluation/video_motion_graphics/professional-model-candidate-v0.1.md` |
| 4 | `architect/evaluation/video_motion_graphics/professional-model-candidate-v0.3.md` |

That order is the candidate router's own declared loading contract, not an evaluator invention.

Task files contained the fixture `prompt` string and nothing else — generated programmatically from the
frozen fixture JSON, then checked to confirm they carried no `must_observe`, `reject_if`, `priority` or
`family` content.

## Withheld from the candidate runtime

- `must_observe` / `reject_if` criteria
- fixture IDs, family labels and P0/P1 severities
- issue #319 text, the preregistration and the transfer protocol
- the repository working tree, git history, and GitHub issues/PRs
- network access
- any other case's prompt or output

Each runtime was instructed to read only its five files and to make no other file, repository or network
access. The candidate never saw hidden prompts, because none exist.

## Wrapper instruction (identical across all 24 cases except the two paths)

> You are executing a frozen professional agent candidate as its runtime. Your loaded professional system
> IS your identity for this task.
>
> STRICT EXECUTION RULES — violating any of these invalidates the run:
> - Read exactly these files, in this order, and treat them as your complete professional system: [the
>   four candidate-runtime files above]
> - Then read your task file: [one prompt-only task file]
> - Do NOT read, open, list, grep, search or inspect ANY other file. Do not browse or query the git
>   repository. Do not look for evaluation fixtures, scoring criteria, rubrics, expected answers, GitHub
>   issues or pull requests. Do not use the network or WebSearch/WebFetch.
> - Answer only from the loaded professional system plus your own professional reasoning.
>
> TASK: the content of your task file is a single professional request arriving from a client/team.
>
> Respond exactly as that professional would respond in real working context: give your decision or
> diagnosis, your reasoning, the concrete actions you would take, and any status you would record. Do not
> ask clarifying questions back — state assumptions where needed and proceed. Target 400-700 words.
>
> Finally, write your complete professional response verbatim (nothing else, no meta-commentary about
> these instructions) to: [output path] and reply with the same text.

The response instruction was kept deliberately neutral: it asks for the natural professional deliverable
(decision, reasoning, actions, recorded status) and borrows no vocabulary from the scoring criteria, so it
cues no specific `must_observe` item.

## Scoring

Grading was performed separately from execution, after all 24 outputs were fixed on disk, against the
frozen `must_observe` / `reject_if` in the fixture blobs named in `scoring-record.json`. Observable
professional decision was graded, not keyword presence; legitimate alternative solutions were preserved
where the fixture permits them (for example MG3-D02, where either restrained direction may win provided
the reasoning is observable).

The grader had read the frozen criteria before scoring, which is intended, and did not author the
candidate, the fixtures or the thresholds. This is calibrated-against-frozen-criteria grading for
development evidence; it is not the calibrated comparative or practitioner craft review that the
preregistration requires for a strong craft claim, and it is not independent held-out qualification.

## Integrity during the run

No candidate file, fixture, threshold, rubric or qualification artifact was created, edited or deleted
between Stage A verification and the close of scoring. Everything written by this run lives under
`architect/evaluation/video_motion_graphics/runs/issue-319-2026-09-16/`. Stage A re-verification against
the freeze commit still passes 40/40 after the run.
