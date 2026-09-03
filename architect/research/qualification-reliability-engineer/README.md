# Qualification Reliability Engineer — research workspace

Status: profession discovery only. Do not write a role SKILL first.

Purpose: reconstruct the professional role responsible for proving that AI-agent qualification/evaluation infrastructure is technically trustworthy before model/API spend and before professional verdicts are accepted.

This workspace is governed by current `AGENTS.md` and `architect/SKILL.md`.

Required evidence domains:
- AI evaluation harness validity and broken-environment detection;
- software test engineering and fault injection;
- site reliability / production engineering;
- distributed/API transport reliability and idempotency;
- observability, incident classification and postmortem practice;
- experiment validity and measurement error;
- resource/cost engineering, retry budgets and quota protection;
- secrets/privacy/retention boundaries for held-out evaluation data.

Role boundary:
- Agent Architect designs professional-agent architecture and qualification requirements.
- Independent Evaluator judges profession-specific candidate performance.
- Qualification Reliability Engineer owns whether the evaluation machine itself is executable, observable, bounded, cost-safe and trustworthy enough to produce valid evidence.

Initial primary-source anchors:
- OpenAI, `A shared playbook for trustworthy third party evaluations` (2026-05-29): harness choices, broken problems/environments, validity checks, retry/token/time/inference budgets.
- Google SRE, `Testing for Reliability`: reliability confidence must be established by testing the system, not assumed.
- Google Gemini API, `Background execution`: long-running standard HTTP calls can be interrupted by connection timeouts; background execution/polling is the documented mechanism where storage/retention is acceptable.

No provider/model calls are authorized by this research workspace.
