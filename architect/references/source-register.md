# Agent Architect Source Register

Status: active research register for v1.1 benchmark candidate. Sources are recorded by claim/function, not as a generic reading list.

| ID | Source | Type | Supports | Freshness | Notes |
|---|---|---|---|---|---|
| SRC-001 | Anthropic, *Building effective agents* (2024) | practitioner engineering guidance | architecture simplicity; workflow vs agent distinction; tool/interface importance; environmental feedback | slow/current-practice | Engineering evidence, not universal law. https://www.anthropic.com/engineering/building-effective-agents |
| SRC-002 | Anthropic, *Demystifying evals for AI agents* (2026) | practitioner engineering guidance | eval-driven development; multi-turn agent evaluation; code/model/human graders; outcome and trajectory evaluation | current | Production-oriented guidance. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents |
| SRC-003 | OpenAI, Evals / Graders documentation | official platform documentation | structured evals; heterogeneous deterministic/model graders; repeatable testing | versioned | Recheck platform details live before implementation. https://platform.openai.com/docs/api-reference/evals |
| SRC-004 | W3C PROV-O Recommendation | standard | provenance entities, activities, agents, derivations; traceability | stable | Adopt conceptual provenance discipline; full ontology not required. https://www.w3.org/TR/prov-o/ |
| SRC-005 | W3C PROV Primer / PROV family | standard/primer | provenance representation and interpretation | stable | Basis for compact source lineage. https://www.w3.org/TR/prov-primer/ |
| SRC-006 | NIST AI RMF 1.0 Core | official framework | lifecycle risk; knowledge limits; oversight; TEVV; uncertainty; deployment context | slow/current | Recheck before normative adoption. https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ |
| SRC-007 | NIST AI RMF Generative AI Profile (NIST AI 600-1) | official framework | generative-AI lifecycle risk and trustworthiness | slow/current | Risk/evaluation architecture, not profession scoring standard. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence |
| SRC-008 | AHRQ, *Cognitive Task Analysis* | authoritative methodology | eliciting unobserved reasoning/decisionmaking; observation/interview limitations | stable | Self-report must be triangulated. https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/cognitive-task-analysis |
| SRC-009 | AHRQ, *Critical Decision Method* | authoritative methodology | expert decision-point elicitation; cognitive probes; tacit expertise | stable | Retrospective-report limits remain. https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/critical-decision-method |
| SRC-010 | AHRQ, *Critical Incident Technique* | authoritative methodology | incident timeline reconstruction; physical+cognitive event capture | stable | Memory/reliability limits support triangulation. https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/critical-incident-technique |
| SRC-011 | NIST AI RMF Playbook, Measure | official guidance | context-relevant evaluation; representativeness; domain experts; oversight/go-no-go | slow/current | Evaluation discipline, not universal rubric. https://airc.nist.gov/airmf-resources/playbook/measure/ |
| SRC-012 | NIST AI 800-3, *Expanding the AI Evaluation Toolbox with Statistical Models* (2026) | official measurement science | benchmark assumptions; measurement targets; uncertainty | current/stable-method | Supports statistical caution for stochastic agents. https://www.nist.gov/news-events/news/2026/02/new-report-expanding-ai-evaluation-toolbox-statistical-models |
| SRC-013 | OpenAI, GDPval / real-world task evaluation | primary practitioner/research report | occupation-specific authentic tasks; professional graders; blind comparison | current | Evidence for authentic occupational tasks plus expert grading. https://openai.com/index/gdpval/ |
| SRC-014 | BRIGHT (2024) | research benchmark | reasoning-intensive retrieval beyond lexical similarity | stable/current | Supports reasoning-intensive retrieval evals. https://arxiv.org/abs/2407.12883 |
| SRC-015 | RAGChecker (2024) | research framework | separation of retrieval and generation failures | current research | Metrics not frozen as universal. https://arxiv.org/abs/2408.08067 |
| SRC-016 | NIST, collaborative HRI interface metrics (2020) | government/peer-reviewed human factors | interface metrics; situation awareness; diagnostics; error correction | stable | Transfer from HRI cautiously. https://www.nist.gov/publications/towards-effective-interface-designs-collaborative-hri-manufacturing-metrics-and |
| SRC-017 | NIST, *Performance of Human-Robot Interaction* | government measurement program | usability, trust, safety, situation awareness, test methods | current program | Supports measurement-first interface discipline. https://www.nist.gov/programs-projects/performance-human-robot-interaction |
| SRC-018 | Xu et al., benchmark contamination survey (2024) | research survey | benchmark contamination threat model | current research | Supports contamination controls. https://arxiv.org/abs/2406.04244 |
| SRC-019 | Xu et al., *Benchmarking Benchmark Leakage in LLMs* (2024) | empirical research | evidence of benchmark leakage | current research | Exposed benchmarks are weaker independent evidence. https://arxiv.org/abs/2404.18824 |
| SRC-020 | Gao et al., *Single-agent or Multi-agent Systems? Why Not Both?* (2025) | empirical systems research | SAS/MAS trade-offs; hybrid routing; coordination/cost | current research | One study; representative eval still required. https://arxiv.org/abs/2505.18286 |
| SRC-021 | NIST AI 800-4, deployed-AI monitoring (2026) | official measurement report | drift; incident/feedback monitoring; field-vs-controlled gap | current | Monitoring methods evolving. https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation |
| SRC-022 | NIST AI RMF Playbook, Manage | official guidance | incident response; recovery; change management; continual improvement | slow/current | Production-learning architecture. https://airc.nist.gov/airmf-resources/playbook/manage/ |
| SRC-023 | OpenAI, *Improving support with every interaction* | first-party production case | real interactions -> evals/knowledge/automation improvements | current practice | Case evidence, not universal law. https://openai.com/index/openai-support-model/ |
| SRC-024 | W3C WAI / WCAG 2 | standards/official role guidance | frontend/accessibility dry-run | stable/versioned | Profession dry-run evidence. https://www.w3.org/WAI/standards-guidelines/wcag/ |
| SRC-025 | WHATWG HTML Living Standard | living standard | browser/HTML semantics/forms | versioned/live | Check live for exact behavior. https://html.spec.whatwg.org/ |
| SRC-026 | W3C WebDriver | web standard | direct browser automation/observation | slow/versioned | Supports execution evidence. https://www.w3.org/TR/webdriver/ |
| SRC-027 | Google web.dev, Web Vitals | first-party platform guidance | lab-vs-field performance measurement | current/versioned | Retrieve current metric guidance. https://web.dev/articles/vitals |
| SRC-028 | OWASP CSP Cheat Sheet | authoritative security practice | frontend defense-in-depth example | current practice | CSP not substitute for safe coding. https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html |
| SRC-029 | U.S. BLS, Market Research Analysts | authoritative occupation description | analytical profession reconstruction | slow/current | Baseline, not complete senior model. https://www.bls.gov/ooh/business-and-financial/market-research-analysts.htm |
| SRC-030 | O*NET 13-1161.00 | authoritative occupational/task database | market research tasks and outputs | slow/current | Task evidence, not expert-judgment proof. https://www.onetonline.org/link/summary/13-1161.00 |
| SRC-031 | ISO 20252:2019 + Edition 4 project status | international standard/version metadata | market-research requirements; freshness/version transition | versioned/current | Shows need for live normative version checks. https://www.iso.org/standard/73671.html |
| SRC-032 | AAPOR, *Standard Definitions* | professional methodology | total survey error; coverage/measurement/nonresponse | stable/current | Survey-specific transfer with care. https://aapor.org/standards-and-ethics/standard-definitions/ |
| SRC-033 | AAPOR, *Best Practices for Survey Research* | professional guidance | sampling, weighting, transparency, nonresponse | stable/current | Supports biased-evidence adversarial tests. https://aapor.org/standards-and-ethics/best-practices/ |
| SRC-034 | Anthropic, *AuditBench* (2026) | empirical agent-evaluation research | tool-to-agent gap; realistic agentic success | current research | Evaluate whether agents actually use tool evidence. https://alignment.anthropic.com/2026/auditbench/ |
| SRC-035 | NIST CAISI, agent-evaluation transcript analysis (2026) | official evaluation-science guidance | trajectory review; artifacts/cheating in long-horizon evals | current | Not universal scoring rubric. https://www.nist.gov/blogs/caisi-research-blog/analyzing-transcripts-ai-agent-evaluations |
| SRC-036 | U.S. BLS, Graphic Designers | authoritative occupation description | creative profession baseline | slow/current | Baseline duties, not senior art-direction curriculum. https://www.bls.gov/ooh/arts-and-design/graphic-designers.htm |
| SRC-037 | O*NET 27-1024.00, Graphic Designers | authoritative occupational/task database | layout/type/review/commercial tasks | slow/current | Task evidence, not proof of taste. https://www.onetonline.org/link/summary/27-1024.00 |
| SRC-038 | Design Council, Double Diamond | professional framework | divergence/convergence; testing/rejection/iteration | stable/current | Simplified framework, not rigid recipe. https://www.designcouncil.org.uk/resources/the-double-diamond/ |
| SRC-039 | AIGA Designer 2025 | professional competency/education framework | communication-design competency framing | historical/current relevance | Useful education evidence, not current-tech guidance. https://educators.aiga.org/aiga-designer-2025/ |
| SRC-040 | Consensual Assessment Technique research | peer-reviewed creativity assessment | domain-expert judgment for creative products | stable/current | Supports calibrated expert creative judging. https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.00032/full |
| SRC-041 | 2026 product-design divergent-thinking study | peer-reviewed research | expert CAT + divergent-thinking dimensions | current | Separates ideation process from final-product judgment. https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1839565/full |
| SRC-042 | Anthropic/Claude, Agent Skills documentation (2025-2026) | current platform/open-format guidance | skills as instructions+scripts+resources; dynamic loading; progressive disclosure | current/versioned | Implementation pattern, not universal architecture. https://support.claude.com/en/articles/12512176-what-are-skills |
| SRC-043 | OpenAI, *Introducing the Codex app* (2026) | first-party production/platform guidance | skill bundles; tool-connected workflow; direct artifact validation | current | Supports procedural packaging + execution verification. https://openai.com/index/introducing-the-codex-app/ |
| SRC-044 | OpenAI Academy, *Using skills* (2026) | first-party guidance | reusable workflows; SKILL.md; dependent resources | current | User-facing description, weaker than empirical evidence. https://openai.com/academy/skills/ |
| SRC-045 | Microsoft Agent Framework Overview (2026) | official platform documentation | agent/harness/workflow separation; session state; memory/context; checkpointing; HITL | current/versioned | Strong implementation example, not universal law. https://learn.microsoft.com/en-us/agent-framework/overview/ |
| SRC-046 | Microsoft Agent Framework Harness (2026) | official platform documentation | planning/todo state; context compaction; persistent history; file memory; approvals; OpenTelemetry; iteration limits | current/versioned | Evidence for explicit runtime harness mechanisms. https://learn.microsoft.com/en-us/agent-framework/get-started/harness |
| SRC-047 | Magentic-One (2024/2025) | research/open-source multi-agent implementation | Task Ledger; Progress Ledger; stall detection; replanning; orchestrated specialists | current research | Extract control patterns; do not default to MAS. https://arxiv.org/abs/2411.04468 |
| SRC-048 | Google Agent Development Kit | official platform documentation | session/state/memory services; workflows; long-running pause/resume; eval | current/versioned | Platform example; capability abstractions preferred. https://google.github.io/adk-docs/ |
| SRC-049 | Google DeepMind, AI Co-Scientist | research system | specialized generation/reflection/ranking/evolution/meta-review; external evidence; experiment validation | current research | Task-specific scientific-search architecture; not universal decomposition. https://deepmind.google/discover/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/ |
| SRC-050 | Yao et al., ReAct (2022) | primary research | interleaved reasoning/action; environment feedback; plan updates | stable research | Supports action-observation feedback loop. https://arxiv.org/abs/2210.03629 |
| SRC-051 | Shinn et al., Reflexion (2023) | primary research | feedback-driven reflection; episodic memory; trial-to-trial improvement | stable research | Reflection benefits depend on feedback/task. https://arxiv.org/abs/2303.11366 |
| SRC-052 | Huang et al., *LLMs Cannot Self-Correct Reasoning Yet* (2023) | empirical research | intrinsic self-correction can fail/degrade without external feedback | stable research | Supports bounded evidence-driven remediation. https://arxiv.org/abs/2310.01798 |
| SRC-053 | Yao et al., tau-bench (2024) | primary benchmark research | tool+user+policy interactions; database end-state grading; pass^k reliability | stable/current | Strong evidence for end-state + repeated-trial eval. https://arxiv.org/abs/2406.12045 |
| SRC-054 | Wu et al., LongMemEval (2024) | primary benchmark research | extraction; multi-session reasoning; temporal reasoning; knowledge updates; abstention | stable/current | Supports first-class memory/state evaluation. https://arxiv.org/abs/2410.10813 |
| SRC-055 | Liu et al., AgentBench (2023) | primary benchmark research | multi-environment interactive agent evaluation; long-term reasoning failure modes | stable | Broad environment evidence. https://arxiv.org/abs/2308.03688 |
| SRC-056 | Zhou et al., WebArena (2023) | primary benchmark research | realistic reproducible web environment; functional end-to-end outcomes | stable | Supports environment-grounded long-horizon testing. https://arxiv.org/abs/2307.13854 |
| SRC-057 | Mialon et al., GAIA (2023) | primary benchmark research | real-world multimodal/web/tool-use assistant tasks | stable | Supports authentic cross-tool tasks. https://arxiv.org/abs/2311.12983 |
| SRC-058 | SWE-agent / Agent-Computer Interface work | research/open-source implementation | tool-interface ergonomics; bounded observations; edit/lint feedback; trajectories | current/versioned | Interface design affects agent performance; evaluate ACI itself. https://swe-agent.com/ |
| SRC-059 | OpenHands architecture | open-source implementation | action/observation event stream; state/controller; runtime/sandbox; replayable execution | current/versioned | Implementation example for observable runtime state. https://docs.openhands.dev/ |
| SRC-060 | O*NET Content Model | authoritative occupational framework | work activities/tasks/context; knowledge/skills; occupation requirements | slow/current | Use for profession-model coverage, not as complete expert model. https://www.onetcenter.org/content.html |
| SRC-061 | ETS, Evidence-Centered Design | assessment/measurement framework | proficiency claim -> evidence model -> task model; validity argument | stable | Supports explicit competency-inference chain. https://www.ets.org/research/policy_research_reports/publications/report/2002/ijzv.html |
| SRC-062 | OpenAI, *Running Codex safely at OpenAI* (2026) | first-party production/security guidance | sandbox/approval/network controls; agent-native telemetry | current | Platform practice, supported by broader agent-security evidence. https://openai.com/index/running-codex-safely-at-openai/ |
| SRC-063 | NIST CAISI / agent-hijacking research and challenge materials (2026) | official security/evaluation evidence | indirect prompt injection / agent hijacking as agentic-system threat | current | Supports dedicated trust-boundary adversarial testing. https://www.nist.gov/aisi |

## Source discipline

The presence of a source in this register does not make every statement from it authoritative for every profession. Each applied agent must maintain its own claim-dependent source map.

Platform documentation establishes current product mechanisms, not universal laws. General architecture changes should normally require either convergence across independent systems, empirical evidence, a defensible professional/measurement framework, or a clear risk argument.

## Foundation coverage after 2026-08 benchmark

The Agent Architect foundation has explicit coverage for:

- profession reconstruction, work context, and tacit-knowledge elicitation;
- competency modeling, evidence-centered inference, and authentic assessment;
- source/provenance/freshness/retrieval discipline;
- empirical validity and comparator compatibility;
- professional judgment and uncertainty;
- creative and high-stakes profession extensions;
- procedural capability/skill packaging and progressive disclosure;
- tool/agent-computer-interface quality, execution semantics, and downstream verification;
- runtime working/session/persistent state, memory lifecycle, context compaction, checkpoint/resume, and multi-session eval;
- long-horizon execution control, discrepancy detection, bounded remediation, replanning, rollback/escalation, and termination;
- single-vs-multi-agent architecture selection and handoff contracts;
- prompt-injection/trust-boundary, skill supply-chain, memory-poisoning, sandbox/network, and data-flow security;
- permissions, blast radius, environment assumptions, and accountable ownership;
- evaluator calibration, holdouts, regression, transcript/trajectory review, benchmark contamination, and repeated-trial reliability;
- production incidents, drift, near-misses, and knowledge/state-policy lifecycle governance.

## Current state

`architect/SKILL.md` is a **v1.1 benchmark candidate**.

The prior v1.0 cross-domain evidence remains valid for the profession-first core, but the external benchmark exposed runtime state/memory, execution control/remediation, procedural capability packaging, and security/trust boundaries as material under-modeled layers. Those layers are now documented and routed.

Benchmark PASS is intentionally withheld until held-out practical/stateful/security/control-loop evaluations demonstrate the new mechanisms behaviorally. See `../evaluation/external-benchmark-2026-08.md`.
