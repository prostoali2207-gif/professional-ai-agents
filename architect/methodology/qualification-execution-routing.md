# Qualification Execution Routing

## Purpose

Choose how evaluation and qualification work is executed without making one metered API provider the default dependency.

This policy supplements `resource-cost-engineering.md`. It does not weaken frozen qualification protocols, independence requirements, thresholds, hard-fail rules, sealed packs, or evidence requirements.

It is also subordinate to the mandatory repair-chain governance in `qualification-stop-loss.md`. Provider routing must not be used to bypass a stop-loss decision.

## Routing order

For each evaluation step, classify what evidence is actually required before selecting a provider.

1. **Deterministic/local first when sufficient.** Use static checks, parsers, schemas, exact comparisons, unit tests, local scripts, direct state inspection, or other mechanical verification when they can prove the required condition.
2. **Already-included subscription capacity when eligible.** For model-assisted development, execution, diagnosis, or grading, prefer an available subscription-backed coding environment such as Codex or Claude Code when it satisfies the task's quality, observability, reproducibility, security, and independence requirements.
3. **Metered external model APIs only when required or justified.** Gemini, Groq, OpenAI API, Anthropic API, xAI/Grok API, or another metered provider may be used when the subscription-backed route is unavailable, exhausted, incompatible, empirically insufficient, or when the qualification design specifically requires an eligible independent external judge/provider.

This is not a fixed provider ranking. Eligibility and evidence validity come before cost.

## Subscription is not unlimited

Treat subscription capacity as quota-bearing capacity, not as infinite or free compute. Before a material run, check observable limits/status where available and preserve capacity for release-critical work. If subscription capacity is exhausted, do not repeatedly retry unchanged work; preserve completed evidence and select another eligible route or defer.

## Provider independence

Evaluation infrastructure should describe required capabilities rather than unnecessarily hard-code a provider. Provider-specific adapters belong behind a stable execution contract where practical.

A workflow may remain provider-pinned when provider/model identity is itself part of a frozen experiment, comparability requirement, calibration, independence requirement, or release contract. Changing such a provider requires explicit revalidation; routing policy must not silently mutate a frozen qualification.

## Independence rule

Codex or Claude Code cannot replace an independent judge merely because their usage is included in a subscription. Before substitution, verify that the new route preserves the required separation between candidate generation, evaluator/grader, hidden fixtures, and release decision. If independence cannot be established, use another eligible independent route or mark the gate not executable.

## Quota and failure behavior

On quota exhaustion or rate-limit failure:

- preserve all completed valid records;
- do not infer PASS from incomplete work;
- do not blindly restart the whole suite;
- resume only missing compatible work when possible;
- do not hammer Gemini, Groq, or any other provider whose quota state has not changed;
- use a fallback only if it preserves the frozen protocol and evidence validity.

Before any technical repair, fallback, migration, or retry after a qualification failure, apply `qualification-stop-loss.md` and record the failure class plus remaining repair budget for the current execution chain.

A provider change is not a fresh qualification attempt for stop-loss purposes when it still serves the same failed qualification stage. If that execution chain has already consumed its bounded technical repair and eligible retry, another technical defect must stop with `NOT_EXECUTABLE` / the preregistered infrastructure verdict unless repository evidence independently satisfies an issue #129 generic-platform reopen criterion.

A genuinely later qualification stage may form a new execution chain because it exercises a different evidence/runtime surface. Repeated infrastructure failures across different stages still require the cross-stage churn review defined in `qualification-stop-loss.md`.

## Migration rule for existing workflows

Do not bulk-replace historical Gemini/Groq/OpenAI/other workflows mechanically. For each active qualification workflow:

`required evidence -> frozen constraints -> deterministic possibility -> subscription-backed eligibility -> independence check -> metered fallback -> migration decision`

Classify each workflow as:

- `KEEP_PINNED` — provider/model identity must remain frozen;
- `ROUTE_SUBSCRIPTION` — Codex/Claude Code can execute without weakening evidence;
- `ROUTE_DETERMINISTIC` — model call is unnecessary;
- `PROVIDER_AGNOSTIC` — adapter contract can safely choose among eligible routes;
- `NOT_EXECUTABLE` — no currently available route preserves required evidence.

A migration proposal must also pass the stop-loss gate. Do not migrate solely because the current route failed if doing so would continue an already-exhausted technical repair chain for the same stage.

## User/account context

Account-specific subscriptions, quotas, credits, and API balances are runtime facts, not permanent repository assumptions. They may influence routing only when current and directly known. Never encode a user's temporary subscription state as a universal architectural rule.
