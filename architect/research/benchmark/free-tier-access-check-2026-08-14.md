# Research provider free-tier access check — 2026-08-14

Status: current official-pricing/access check before any paid-provider benchmark spend.

## Decision summary

Do **not** purchase broad subscriptions for the P0 smoke test.

Current access economics support a cost-minimizing sequence:

1. Tavily first on its recurring free Researcher allocation.
2. Exa next on its signup/monthly free credits.
3. Perplexity API only after the free-provider smoke tests establish that a Perplexity comparison is still decision-relevant; current official API onboarding requires a payment method and purchased API credits.
4. Continue direct-web, Crossref, Semantic Scholar and other public scholarly/primary-source baselines independently.

This document records access conditions only. Provider quality remains an empirical question and must not be inferred from pricing or marketing claims.

## Tavily

Official Tavily help/pricing material currently states:

- Researcher plan: free;
- 1,000 API credits per month;
- no credit card required;
- new accounts start with the free allocation;
- Basic Search costs 1 credit and Advanced Search 2 credits under the documented credit model;
- development keys are available for testing.

Implication: Tavily is immediately suitable for the P0 smoke stage without financial spend, assuming account/API-key provisioning.

Additional cost-saving note: Tavily documents a student program offering four months of Project-plan access with 4,000 credits/month after student verification. This is optional and not required for the initial smoke test.

## Exa

Exa's current official API pricing page states:

- $20 credits on signup;
- Free Tier with $10 credits per month;
- Search base price $7 / 1,000 requests up to 10 results;
- Contents $1 / 1,000 pages per content type;
- Deep Search approximately $12–15 / 1,000 requests;
- Agent fixed-effort modes range from $0.012 to $1.00 per request depending on effort.

Implication: a small controlled P0 smoke test should fit comfortably inside free credits. We should not buy an Exa subscription before the free allocation is exhausted and only if measured marginal value justifies it.

Important: Exa's self-reported accuracy claims are vendor evidence, not benchmark evidence. They must not influence scoring.

## Perplexity

Current Perplexity Help Center material distinguishes consumer plans from API Platform billing.

Official API onboarding currently says:

1. create/sign in to API Console;
2. add a payment method;
3. buy API credits;
4. generate API key.

The Help Center states that a Perplexity subscription is **not** required for API use, but API credits are purchased separately on a pay-as-you-go basis. Consumer/Computer credits are separate and are not API credits.

No recurring complimentary API allocation was found in the current official API billing material checked on 2026-08-14. Therefore we must not assume that an existing consumer Pro subscription provides free API benchmark credits.

Perplexity's consumer Standard plan does provide practically unlimited basic searches and a very limited number of Pro Searches, but those interactive-product runs are not API-equivalent and cannot be used as a clean API-to-API benchmark arm.

Implication: defer Perplexity API spend until Tavily + Exa + free baselines have completed P0 smoke. If Perplexity remains decision-relevant, buy only the minimum practical API credit amount and disable automatic top-up.

Possible exception: Perplexity advertises a startup program with API credits for eligible startups associated with approved partners. Eligibility must be verified rather than assumed.

## Cost-control policy for P0

Before any paid request:

- use free recurring/signup credits first;
- disable automatic top-up;
- set provider-side usage limits where available;
- run the five P0 cases only;
- preserve raw run records;
- stop a provider arm immediately after a decisive P0 architecture-rejection failure where further runs cannot change the decision;
- never upgrade merely to increase benchmark sample size before the pilot indicates material value.

## P0 order

Recommended execution order:

### Stage 0 — no-account baselines

Direct web/browser + primary-source inspection + public scholarly/bibliographic verification.

### Stage 1 — Tavily free

Run the five P0 cases with Search/Extract configurations that expose raw retrieval evidence. Do not use a generated answer as the sole scored artifact.

### Stage 2 — Exa free

Run the same five P0 cases with Search/Contents; optionally one low-cost Deep Search arm only if basic Search/Contents survives P0 and the incremental question is decision-relevant.

### Stage 3 — compare

Ask whether Tavily or Exa materially improve the baseline and whether their failure profiles differ enough to justify an ensemble.

### Stage 4 — Perplexity decision gate

Only purchase Perplexity API credits if at least one of these is true:

- free providers fail a deployment-relevant capability that Perplexity plausibly addresses;
- Perplexity is still a serious candidate for the default discovery/deep-research layer;
- we need an independent third provider to estimate ensemble recall/diversity;
- the expected information value of the comparison exceeds its small direct cost.

## Evidence hygiene

Pricing/access facts are volatile. Record retrieval date and re-check official pages immediately before spending money or relying on a quota.

Do not convert free-tier availability into a quality preference. Free access determines experiment ordering, not architecture selection.
