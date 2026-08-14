# Methodology Dry-Run: Frontend Engineer Profession Model

Status: v0.1. This is a methodology test, not an applied agent and not a `SKILL.md`.

## Purpose

Test whether Agent Architect can reconstruct a real profession beyond a user label, identify hidden competencies, map evidence/tool loops, and expose gaps before agent construction.

## 1. Initial user label

`Frontend Engineer`

This label is insufficient. A superficial decomposition would stop at HTML, CSS, JavaScript, framework knowledge, and testing. The professional reconstruction below shows why that would produce an underpowered agent.

## 2. Real work model

A strong frontend engineer must repeatedly transform product/design requirements into browser-executed interfaces while preserving functional behavior, accessibility, performance, security boundaries, maintainability, and integration contracts.

Observable work includes:

- interpret requirements and identify ambiguity;
- inspect the existing stack and runtime constraints;
- preserve data/API/business contracts while changing presentation or interaction;
- implement semantic document/interface structure;
- implement responsive layout and interaction behavior;
- handle loading, error, empty, partial, and recovery states;
- protect trust boundaries around user-controlled data and browser capabilities;
- diagnose browser/runtime/network failures;
- test behavior in actual browser environments;
- evaluate accessibility using both machine-checkable and interaction-level evidence;
- measure performance in lab and, where available, field conditions;
- detect regressions caused by apparently local changes;
- verify downstream effects rather than treating successful rendering as complete success.

## 3. Decision model

Representative expert decisions include:

### Native semantic element vs custom widget
Inputs: required interaction semantics, keyboard behavior, accessibility APIs, design constraints, browser support.

Weak behavior: choose the easiest markup or reproduce a visual design with generic containers.

Expert behavior: prefer native semantics when they express the intended behavior; use custom patterns only when necessary and then supply complete semantics, keyboard behavior, state exposure, and testing.

W3C WAI explicitly assigns front-end developers responsibility for semantically rich HTML, accessible widgets, forms, structure, keyboard interaction, and adaptable interfaces. WCAG is a technical standard for developers, not merely a design preference.

### Lab performance vs field performance
Weak behavior: declare performance solved because Lighthouse is green locally.

Expert behavior: understand that lab data and real-user field data answer different questions. Core Web Vitals are user-centric field metrics; lab testing is useful for pre-release diagnosis/regression but does not replace field measurement. INP specifically depends on actual interaction and cannot be directly measured by non-interactive lab loading.

### Visual equivalence vs functional correctness
Weak behavior: implement screenshots accurately while breaking validation, focus order, API submission, responsive behavior, or analytics.

Expert behavior: treat rendered fidelity as one quality dimension inside a larger behavioral contract and verify actual interaction/downstream state.

### Security convenience vs trust boundary
Weak behavior: treat frontend code as harmless presentation and directly inject user-controlled content into unsafe DOM sinks.

Expert behavior: treat browser-side data as potentially untrusted, avoid unsafe DOM manipulation, use context-appropriate encoding/safe rendering, and apply defense-in-depth controls such as CSP where appropriate. OWASP explicitly warns that CSP is a second layer, not a substitute for safe coding.

## 4. Hidden competencies discovered

A user asking only for a 'frontend agent' may not know to request:

- browser platform semantics;
- accessibility engineering;
- assistive-technology/keyboard interaction reasoning;
- network and asynchronous-state reasoning;
- API contract preservation;
- client-side security/threat awareness;
- performance measurement literacy;
- field-vs-lab measurement judgment;
- observability and debugging;
- cross-browser/responsive verification;
- regression analysis;
- state-machine thinking for UI flows;
- evidence-driven visual inspection;
- downstream integration verification;
- source/version freshness for framework and platform behavior.

These are not optional decorations. They can determine whether an implementation is usable, secure, performant, and functionally correct.

## 5. Knowledge dependencies

A future frontend agent would require, at minimum, knowledge layers for:

- HTML/browser semantics and forms;
- CSS layout/responsiveness;
- JavaScript/browser execution model;
- accessibility standards and implementation patterns;
- web security boundaries and common client-side vulnerability classes;
- networking/API integration;
- application state and asynchronous failure handling;
- performance metrics and measurement limitations;
- testing strategy: unit/component/integration/end-to-end/browser automation;
- framework/project-specific current documentation retrieved live when version-sensitive.

This dry-run demonstrates that a generic `frontend best practices` document would not be an adequate knowledge architecture.

## 6. Tool and evidence map

| Claim | Required evidence/tool |
|---|---|
| application builds | actual build result |
| target interaction works | browser execution / E2E interaction |
| responsive behavior works | rendered target viewports, not CSS inspection alone |
| accessibility semantics exist | DOM/accessibility inspection plus keyboard/manual checks where needed |
| submission/integration works | network/backend/downstream persisted result |
| performance is acceptable | appropriate lab metrics and, when claiming real-user performance, field/RUM evidence |
| no regression | relevant automated tests plus targeted manual/rendered verification |
| browser behavior is standards-dependent | current normative/official documentation |

W3C WebDriver exists specifically to enable programs to introspect and control browser behavior, supporting direct browser-level verification rather than reasoning only from source code.

## 7. Failure model

High-value adversarial failures for a future agent include:

1. user says 'only change CSS' but the observed defect is caused by DOM/state architecture;
2. visual screenshot looks correct while keyboard navigation is broken;
3. client shows success before backend persistence completes;
4. mobile works at one screenshot width but overflows at adjacent widths/content lengths;
5. Lighthouse improves while real-user interaction latency remains poor;
6. a framework abstraction hides an unsafe DOM sink;
7. a visually custom control has no native semantics or complete keyboard behavior;
8. an implementation passes isolated tests but breaks analytics/API contract;
9. agent trusts obsolete framework guidance instead of checking the installed version;
10. a flaky downstream dependency is masked by frontend copy rather than diagnosed.

## 8. Expert-vs-average discriminator

Average engineer pattern:

`request -> code -> build passes -> done`

Senior pattern:

`reconstruct contract -> inspect system -> identify uncertainty/risk -> choose implementation -> execute -> observe browser -> verify behavior/accessibility/performance/integration -> diagnose discrepancies -> regression test -> document residual uncertainty`.

The differentiator is not simply more syntax knowledge. It is the ability to protect multiple interacting quality constraints, select appropriate evidence, and diagnose failures across boundaries.

## 9. Architecture choice dry-run

Would this profession necessarily require multiple agents? No.

Initial preferred architecture would be one primary Frontend Engineer agent with modular knowledge and tool access, because implementation decisions are tightly coupled and excessive handoffs could destroy context. Independent QA/security/accessibility critics may be justified for release gates or high-risk systems, but decomposition should be evidence-driven.

This validates the Architect rule: do not create separate agents merely because multiple competency domains exist.

## 10. Evaluation implications

A future competency evaluation must include real browser tasks, not trivia. Examples:

- repair a responsive/functional defect in an existing repository while preserving contracts;
- identify a false user diagnosis and prove the actual root cause;
- implement an accessible custom interaction and demonstrate keyboard/focus semantics;
- diagnose a performance issue using appropriate lab/field evidence;
- trace submit -> network -> backend/downstream outcome;
- critique code that looks clean but contains a security/accessibility/integration failure;
- work against an intentionally stale framework instruction and retrieve current official documentation.

## 11. What a strong practitioner would notice missing

The first pass still risks underweighting:

- internationalization/localization and bidirectional layout;
- browser compatibility strategy;
- design-system/component API stewardship;
- testing economics and flake management;
- frontend observability/telemetry;
- privacy/consent implications of analytics and client storage;
- dependency/supply-chain risk;
- release/rollback behavior;
- collaboration with design, backend, QA, security, and product roles.

These must be investigated if/when an actual Frontend Engineer agent is built.

## 12. Dry-run verdict

PASS for methodology usefulness, NOT PASS for creation of a frontend agent.

The dry-run successfully exposed substantial hidden competencies and evidence loops that a user-level prompt would likely omit. It also exposed a methodology risk: profession reconstruction can expand without bound. Therefore Agent Architect needs an explicit scope/risk prioritization mechanism when deciding how deeply adjacent competencies must be modeled.

## Sources used in this dry-run

- W3C WAI, Front-End Developer Responsibilities: https://www.w3.org/WAI/planning/arrm/front-end/
- W3C WAI, WCAG 2 Overview: https://www.w3.org/WAI/standards-guidelines/wcag/
- W3C WAI, Developing for Web Accessibility: https://www.w3.org/WAI/tips/developing/
- WHATWG HTML Living Standard, Forms: https://html.spec.whatwg.org/multipage/forms.html
- W3C WebDriver: https://www.w3.org/TR/webdriver/
- Google web.dev, Web Vitals: https://web.dev/articles/vitals
- OWASP, Content Security Policy Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
