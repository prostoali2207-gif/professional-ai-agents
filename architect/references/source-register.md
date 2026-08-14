# Agent Architect Source Register

Status: initial research register. Sources are recorded by claim/function, not as a generic reading list.

| ID | Source | Type | Supports | Freshness | Notes |
|---|---|---|---|---|---|
| SRC-001 | Anthropic, *Building effective agents* (2024) | current practitioner/engineering guidance | architecture simplicity; workflow vs agent distinction; tool/interface importance; environmental feedback | slow/current-practice | Use as engineering evidence, not universal law. https://www.anthropic.com/engineering/building-effective-agents |
| SRC-002 | Anthropic, *Demystifying evals for AI agents* (2026) | current practitioner/engineering guidance | eval-driven development; multi-turn agent evaluation; code/model/human graders; outcome and trajectory evaluation | current | Recent production-oriented guidance. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents |
| SRC-003 | OpenAI, Evals documentation/API | official platform documentation | structured evals; repeatable testing infrastructure; graders/data sources | versioned | Platform details must be rechecked live before implementation. https://platform.openai.com/docs/api-reference/evals |
| SRC-004 | W3C PROV-O Recommendation | standard | provenance entities, activities, agents, derivations; traceability discipline | stable | Adopt conceptual provenance discipline; no requirement to implement full ontology. https://www.w3.org/TR/prov-o/ |
| SRC-005 | W3C PROV Primer / PROV family | standard/primer | provenance representation and interpretation | stable | Useful for designing compact source lineage. https://www.w3.org/TR/prov-primer/ |
| SRC-006 | NIST AI RMF 1.0 Core | official framework | lifecycle risk thinking; Govern/Map/Measure/Manage; continuous risk management | slow, currently under revision | NIST states AI RMF 1.0 is being updated; recheck before normative adoption. https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ |
| SRC-007 | NIST AI RMF Generative AI Profile (NIST AI 600-1) | official framework | generative-AI lifecycle risk and trustworthiness considerations | slow/current | Updated publication metadata in 2026; use for risk/evaluation architecture where applicable. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence |

## Source discipline

The presence of a source in this register does not make every statement from it authoritative for every profession. Each applied agent must maintain its own claim-dependent source map.

## Known gaps in the Architect evidence base

The foundation still needs stronger primary/authoritative coverage for:

- cognitive task analysis and expert tacit-knowledge elicitation;
- competency modeling and authentic assessment;
- retrieval quality / knowledge-base maintenance;
- evaluator reliability and inter-rater calibration;
- uncertainty calibration and escalation design;
- human factors in tool/interface design;
- multi-agent coordination failure modes;
- regression and benchmark contamination risks.

These gaps block finalization of `architect/SKILL.md`.
