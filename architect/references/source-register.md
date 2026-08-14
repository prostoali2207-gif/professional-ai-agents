# Agent Architect Source Register

Status: active research register. Sources are recorded by claim/function, not as a generic reading list.

| ID | Source | Type | Supports | Freshness | Notes |
|---|---|---|---|---|---|
| SRC-001 | Anthropic, *Building effective agents* (2024) | current practitioner/engineering guidance | architecture simplicity; workflow vs agent distinction; tool/interface importance; environmental feedback | slow/current-practice | Use as engineering evidence, not universal law. https://www.anthropic.com/engineering/building-effective-agents |
| SRC-002 | Anthropic, *Demystifying evals for AI agents* (2026) | current practitioner/engineering guidance | eval-driven development; multi-turn agent evaluation; code/model/human graders; outcome and trajectory evaluation | current | Recent production-oriented guidance. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents |
| SRC-003 | OpenAI, Evals / Graders documentation | official platform documentation | structured evals; deterministic, Python, label/score-model and composite graders; repeatable testing | versioned | Platform details must be rechecked live before implementation. https://platform.openai.com/docs/api-reference/evals and https://platform.openai.com/docs/api-reference/graders |
| SRC-004 | W3C PROV-O Recommendation | standard | provenance entities, activities, agents, derivations; traceability discipline | stable | Adopt conceptual provenance discipline; no requirement to implement full ontology. https://www.w3.org/TR/prov-o/ |
| SRC-005 | W3C PROV Primer / PROV family | standard/primer | provenance representation and interpretation | stable | Useful for designing compact source lineage. https://www.w3.org/TR/prov-primer/ |
| SRC-006 | NIST AI RMF 1.0 Core | official framework | lifecycle risk thinking; knowledge limits; human oversight; TEVV; uncertainty; independent assessment; deployment-context evaluation | slow, currently under revision | NIST states AI RMF 1.0 is being updated; recheck before normative adoption. https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ |
| SRC-007 | NIST AI RMF Generative AI Profile (NIST AI 600-1) | official framework | generative-AI lifecycle risk and trustworthiness considerations | slow/current | Updated publication metadata in 2026; use for risk/evaluation architecture where applicable. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence |
| SRC-008 | AHRQ Digital Healthcare Research, *Cognitive Task Analysis* | authoritative government methodology resource | eliciting otherwise unobserved reasoning, decisionmaking, information processing; observation/interview methods; limitations | stable | Useful method overview; warns that participants can struggle to verbalize cognition and coaching can bias collection. https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/cognitive-task-analysis |
| SRC-009 | AHRQ Digital Healthcare Research, *Critical Decision Method* | authoritative government methodology resource | expert decision-point elicitation; cognitive probes; incident phases; expert-system/training requirements | stable | Strong basis for tacit expertise mining; also notes dependence on analyst/participant quality and retrospective verbal accounts. https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/critical-decision-method |
| SRC-010 | AHRQ Digital Healthcare Research, *Critical Incident Technique* | authoritative government methodology resource | incident timeline reconstruction; physical + cognitive event capture; selected-point probing | stable | Explicitly notes memory degradation/reliability limits; supports triangulation requirement. https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/critical-incident-technique |
| SRC-011 | NIST AI RMF Playbook, Measure | official implementation guidance | context-relevant evaluation; dataset representativeness; domain-expert involvement; oversight metrics; escalation/go-no-go documentation | slow/current | Use as evaluation/risk discipline, not a universal profession-specific scoring standard. https://airc.nist.gov/airmf-resources/playbook/measure/ |
| SRC-012 | NIST AI 800-3, *Expanding the AI Evaluation Toolbox with Statistical Models* (2026) | official measurement-science publication | benchmark assumptions; measurement targets; distinction between notions of performance; uncertainty quantification | current/stable-method | Incorporate statistical caution for stochastic-agent evals. https://www.nist.gov/news-events/news/2026/02/new-report-expanding-ai-evaluation-toolbox-statistical-models |
| SRC-013 | OpenAI, *Measuring the performance of our models on real-world tasks / GDPval* | primary practitioner/research report | occupation-specific authentic tasks; experienced professional graders; blind comparison; detailed domain rubrics; automated graders not treated as expert replacement | current | Useful evidence for combining authentic occupational tasks and calibrated expert grading. https://openai.com/index/gdpval/ |

## Source discipline

The presence of a source in this register does not make every statement from it authoritative for every profession. Each applied agent must maintain its own claim-dependent source map.

## Resolved foundation gaps in this pass

Materially strengthened:

- cognitive task analysis and expert tacit-knowledge elicitation;
- authentic competency assessment;
- evaluator/grader calibration discipline;
- uncertainty, human oversight, escalation, and go/no-go reasoning.

## Known gaps in the Architect evidence base

The foundation still needs stronger primary/authoritative coverage for:

- retrieval quality / knowledge-base maintenance and retrieval evaluation;
- human factors in tool/interface design beyond general agent-engineering guidance;
- multi-agent coordination, handoff, and communication failure modes;
- regression-suite design, benchmark contamination, and evaluation leakage;
- longitudinal learning from production incidents without polluting stable professional knowledge;
- deciding when one professional role should be decomposed into multiple agents vs one agent with modules.

These gaps still block finalization of `architect/SKILL.md`.
