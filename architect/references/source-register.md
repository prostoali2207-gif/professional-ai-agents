# Agent Architect Source Register

Status: active research register. Sources are recorded by claim/function, not as a generic reading list.

| ID | Source | Type | Supports | Freshness | Notes |
|---|---|---|---|---|---|
| SRC-001 | Anthropic, *Building effective agents* (2024) | current practitioner/engineering guidance | architecture simplicity; workflow vs agent distinction; tool/interface importance; environmental feedback | slow/current-practice | Use as engineering evidence, not universal law. https://www.anthropic.com/engineering/building-effective-agents |
| SRC-002 | Anthropic, *Demystifying evals for AI agents* (2026) | current practitioner/engineering guidance | eval-driven development; multi-turn agent evaluation; code/model/human graders; outcome and trajectory evaluation | current | Recent production-oriented guidance. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents |
| SRC-003 | OpenAI, Evals / Graders documentation | official platform documentation | structured evals; deterministic, Python, label/score-model and composite graders; repeatable testing | versioned | Platform details must be rechecked live before implementation. https://platform.openai.com/docs/api-reference/evals and https://platform.openai.com/docs/api-reference/graders |
| SRC-004 | W3C PROV-O Recommendation | standard | provenance entities, activities, agents, derivations; traceability discipline | stable | Adopt conceptual provenance discipline; no requirement to implement full ontology. https://www.w3.org/TR/prov-o/ |
| SRC-005 | W3C PROV Primer / PROV family | standard/primer | provenance representation and interpretation | stable | Useful for designing compact source lineage. https://www.w3.org/TR/prov-primer/ |
| SRC-006 | NIST AI RMF 1.0 Core | official framework | lifecycle risk thinking; knowledge limits; human oversight; TEVV; uncertainty; independent assessment; deployment-context evaluation | slow, currently under revision | Recheck before normative adoption. https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ |
| SRC-007 | NIST AI RMF Generative AI Profile (NIST AI 600-1) | official framework | generative-AI lifecycle risk and trustworthiness considerations | slow/current | Use for risk/evaluation architecture where applicable. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence |
| SRC-008 | AHRQ, *Cognitive Task Analysis* | authoritative government methodology resource | eliciting otherwise unobserved reasoning, decisionmaking, information processing; observation/interview methods; limitations | stable | Participants can struggle to verbalize cognition and coaching can bias collection. https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/cognitive-task-analysis |
| SRC-009 | AHRQ, *Critical Decision Method* | authoritative government methodology resource | expert decision-point elicitation; cognitive probes; incident phases; expert-system/training requirements | stable | Strong basis for tacit expertise mining with retrospective-report limitations. https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/critical-decision-method |
| SRC-010 | AHRQ, *Critical Incident Technique* | authoritative government methodology resource | incident timeline reconstruction; physical + cognitive event capture; selected-point probing | stable | Memory degradation/reliability limits support triangulation. https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/critical-incident-technique |
| SRC-011 | NIST AI RMF Playbook, Measure | official implementation guidance | context-relevant evaluation; representativeness; domain experts; oversight metrics; escalation/go-no-go documentation | slow/current | Evaluation/risk discipline, not universal profession scoring standard. https://airc.nist.gov/airmf-resources/playbook/measure/ |
| SRC-012 | NIST AI 800-3, *Expanding the AI Evaluation Toolbox with Statistical Models* (2026) | official measurement-science publication | benchmark assumptions; measurement targets; performance notions; uncertainty quantification | current/stable-method | Supports statistical caution for stochastic-agent evals. https://www.nist.gov/news-events/news/2026/02/new-report-expanding-ai-evaluation-toolbox-statistical-models |
| SRC-013 | OpenAI, *Measuring the performance of our models on real-world tasks / GDPval* | primary practitioner/research report | occupation-specific authentic tasks; professional graders; blind comparison; domain rubrics | current | Evidence for authentic occupational tasks plus expert grading. https://openai.com/index/gdpval/ |
| SRC-014 | BRIGHT, *A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval* (2024) | peer-reviewed/research benchmark | retrieval where relevance requires reasoning beyond lexical/semantic similarity | stable/current research | Supports explicit reasoning-intensive retrieval eval cases. https://arxiv.org/abs/2407.12883 |
| SRC-015 | RAGChecker (2024) and RAG evaluation literature | research framework | fine-grained separation of retrieval and generation failures in RAG | current research | Use as research evidence; do not freeze framework-specific metrics as universal. https://arxiv.org/abs/2408.08067 |
| SRC-016 | NIST, *Towards Effective Interface Designs for Collaborative HRI in Manufacturing: Metrics and Measures* (2020) | government/peer-reviewed human-factors research | interface metrics; situation awareness; diagnostics; error correction in human-machine collaboration | stable | Domain is HRI/manufacturing, so transfer principles cautiously. https://www.nist.gov/publications/towards-effective-interface-designs-collaborative-hri-manufacturing-metrics-and |
| SRC-017 | NIST, *Performance of Human-Robot Interaction* | government measurement-science program | tool/interface usability, trust, safety, situation awareness, test methods and metrics | current program | Supports measurement-first human-machine interface discipline. https://www.nist.gov/programs-projects/performance-human-robot-interaction |
| SRC-018 | Xu et al., *Benchmark Data Contamination of Large Language Models: A Survey* (2024) | research survey | benchmark contamination threat model and mitigation landscape | current research | Use to justify contamination controls; implementation requires task-specific design. https://arxiv.org/abs/2406.04244 |
| SRC-019 | Xu et al., *Benchmarking Benchmark Leakage in Large Language Models* (2024) | empirical research | evidence of benchmark leakage and transparency requirements | current research | Supports treating exposed benchmarks as weaker independent evidence. https://arxiv.org/abs/2404.18824 |
| SRC-020 | Gao et al., *Single-agent or Multi-agent Systems? Why Not Both?* (2025) | empirical systems research | SAS/MAS trade-offs; benefits can shrink with stronger models; hybrid routing; coordination/cost considerations | current research | One study, not a universal decomposition law. Requires representative evaluation for each architecture. https://arxiv.org/abs/2505.18286 |

## Source discipline

The presence of a source in this register does not make every statement from it authoritative for every profession. Each applied agent must maintain its own claim-dependent source map.

## Foundation coverage after this pass

Materially strengthened:

- cognitive task analysis and tacit-knowledge elicitation;
- authentic competency assessment;
- evaluator/grader calibration;
- uncertainty, oversight, escalation, and go/no-go reasoning;
- retrieval evaluation and reasoning-intensive retrieval;
- human factors for tool/interface observability and recovery;
- single-vs-multi-agent architecture trade-offs and handoff discipline;
- benchmark contamination, leakage, holdouts, and regression integrity.

## Remaining gaps before final Agent Architect skill

The remaining blockers are now narrower:

- production-incident learning and knowledge lifecycle governance without contaminating stable professional knowledge;
- a formal pre-SKILL completeness audit tying every methodology layer into one executable architect workflow;
- adversarial red-team of the Agent Architect methodology itself from senior-practitioner, educator, hiring-manager, evaluation-scientist, and systems-engineer perspectives;
- practical dry-run: use the methodology to model one profession without yet publishing its applied agent, and measure where the architecture fails.

`architect/SKILL.md` should not be finalized until these are completed.