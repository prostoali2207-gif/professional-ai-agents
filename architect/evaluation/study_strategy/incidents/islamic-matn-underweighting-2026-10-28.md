# Incident — Islamic matn underweighting

Date: 2026-10-28
Severity: architecture / domain-specialization defect
Affected: `study-strategy@0.1.0-candidate`

## Observed failure

After a beginner lesson on *Three Fundamental Principles*, the skill recommended understanding and recall but initially did not assign any exact memorization target. The learner correctly challenged this because concise matn and core proofs are commonly memorized in structured طلب العلم.

## Root cause

The skill's generic anti-overmemorization and review-cost controls were stronger than its Islamic positive curriculum model.

The Islamic specialization encoded fidelity boundaries but not enough traditional acquisition structure:
`hifz al-mutun + talaqqi/sharh + fahm/dabt + muraja'ah + 'amal + tadarruj`.

## Fix

- added explicit positive role for concise matn memorization;
- added matn/sharh/dalil routing;
- added Arabic exact-text policy;
- added Qur'an priority;
- added teacher/talaqqi and progression rules;
- added muraja'ah and action;
- added targeted regressions.

## Non-fix

Do not swing to the opposite extreme:
- no "memorize everything";
- no verbatim teacher-sharh default;
- no exact target from unverified text;
- no AI-invented religious obligation.

## Regression status

Author-side semantic/static regression required before merge.
