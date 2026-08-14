# Source and Knowledge Engineering

Status: v0.1.

## Goal

Prevent two common agent-design failures:

1. treating model priors as a complete professional knowledge base;
2. turning `knowledge/` into an uncurated document dump.

Knowledge must be selected according to the decisions the agent must make and the evidence needed to justify those decisions.

## 1. Claim-first source selection

Do not begin with "collect sources about the profession." Begin with a claim or decision dependency.

For each material knowledge item record:

- claim or decision supported;
- source type;
- authority;
- publication/update date;
- applicable jurisdiction/domain/version;
- evidence strength;
- known limitations;
- freshness requirement;
- retrieval date where relevant;
- conflicts with other sources.

A source is useful only insofar as it supports a required competency or decision.

## 2. Source taxonomy

Keep these categories distinct:

### Standards and official specifications
Use for normative requirements, protocols, regulations, interfaces, and authoritative definitions.

### Primary empirical research
Use for causal or empirical claims when available. Inspect methods, population, measurement, uncertainty, and external validity rather than copying conclusions.

### Official product/platform documentation
Use for current tool behavior, APIs, limits, supported features, and implementation constraints. Treat version-sensitive claims as volatile.

### High-quality professional literature
Use to synthesize stable practice and conceptual frameworks when stronger primary or normative evidence does not fully answer the question.

### Strong practitioner evidence
Use for tacit workflow, heuristics, craft practice, operational lessons, and edge cases that formal literature may omit. Label it as practice evidence rather than universal truth.

### Examples / inspiration
Use to expand reference literacy and divergent exploration. Do not promote an example to a rule merely because the result is attractive.

## 3. Authority is claim-dependent

There is no universal ranking that works for every claim.

Examples:

- an API behavior claim should normally defer to current official documentation;
- an empirical behavior claim should normally prefer relevant primary evidence over vendor marketing;
- a legal requirement needs authoritative legal/regulatory material for the applicable jurisdiction;
- a craft judgment may require triangulation across principles, practitioner evidence, and direct result inspection.

## 4. Freshness model

Classify knowledge by expected decay:

- `stable`: foundational concepts unlikely to change materially;
- `slow`: standards or established practice that changes occasionally;
- `versioned`: correct only for a particular specification/product version;
- `volatile`: prices, laws, software behavior, market conditions, current roles, current best practices, and similar live facts.

Stable knowledge may be stored locally with provenance. Volatile knowledge should generally be retrieved live at execution time or be protected by an explicit freshness gate.

Do not silently freeze volatile knowledge into an agent.

## 5. Provenance model

The W3C PROV family provides a general model for describing entities, activities, agents, and derivations involved in producing information. This repository does not need to implement the full ontology, but it adopts the underlying discipline: important derived knowledge should be traceable to its source and transformation.

A compact knowledge record should therefore preserve:

`source -> extracted claim/principle -> transformation/synthesis -> agent competency/decision that consumes it`.

Derived synthesis must not masquerade as a direct source claim.

## 6. Conflict handling

When high-quality sources conflict:

1. verify that they address the same claim;
2. compare date/version/jurisdiction/population/context;
3. compare methodology and evidence quality;
4. determine whether the conflict is real or scope-dependent;
5. preserve unresolved uncertainty where it cannot be resolved;
6. encode the decision boundary rather than deleting the disagreement.

## 7. Knowledge inclusion gate

Before adding material to an agent knowledge layer, ask:

- Which competency consumes this?
- Which decision would become worse without it?
- Is the source appropriate for that claim?
- Is it sufficiently current?
- Is the extracted content a fact, standard, empirical result, heuristic, opinion, or example?
- Can the agent retrieve it live instead of storing it?
- Is there a copyright-safe way to encode the useful principle without copying protected text?
- How will we test whether this knowledge actually improves performance?

If these questions cannot be answered, the material should normally not be added.

## 8. Retrieval policy

External research is mandatory when:

- the claim is time-sensitive;
- the relevant standard/documentation may have changed;
- the domain is high-stakes;
- internal confidence is low;
- sources conflict;
- the profession depends on local jurisdiction or current market conditions;
- a referenced source has not actually been opened;
- the task requires exact attribution.

Retrieval itself is a competency and must be evaluated for query formulation, source selection, source opening, claim extraction, triangulation, and uncertainty reporting.

## 9. Knowledge vs instructions

Never substitute instructions for missing disciplinary knowledge.

Bad:

`Use secure coding practices.`

Better architecture:

- security competency mapped;
- relevant threat model and secure-development knowledge available;
- current platform guidance retrieved where needed;
- code/static/runtime security checks available;
- adversarial security evals included.

The same rule applies to design, research, statistics, law, medicine, finance, marketing, and other professions.

## 10. Knowledge maintenance

Each agent should eventually maintain a source register containing at least:

- source identifier;
- source category;
- claims/competencies supported;
- version/date;
- freshness class;
- review date;
- status: active / superseded / disputed / inspiration-only.

A source becoming stale should trigger review of every dependent knowledge unit and eval, not merely replacement of a URL.

## Quality gate

Source/knowledge architecture passes only when a reviewer can trace a material professional capability back to sufficient knowledge/evidence and can identify which parts require live research at runtime.
