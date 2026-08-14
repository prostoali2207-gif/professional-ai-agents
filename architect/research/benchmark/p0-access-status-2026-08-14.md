# P0 Access Status — 2026-08-14

Status: execution-readiness note for the research-provider benchmark. Does not modify Agent Architect behavior, PR #1, or v1.1 validation.

## New finding: Exa can be tested without a user API key in principle

Official Exa MCP documentation states that its hosted MCP server can be connected directly at:

`https://mcp.exa.ai/mcp`

The default hosted MCP exposes at least web search and web fetch, and Exa documents a generous free plan for this remote MCP. A user-supplied API key is needed to raise free-plan rate limits and for some optional agent tools, but is not required for the default hosted search/fetch path.

This materially reduces the minimum paid-access requirement for P0.

## Current runtime constraint

The present ChatGPT project runtime does not expose a generic arbitrary-MCP connector for `https://mcp.exa.ai/mcp`, and the local execution container has no outbound DNS/network access. Therefore Exa's no-key MCP cannot be invoked directly from this session even though the provider supports it.

This is a tooling-boundary limitation, not an Exa access limitation.

No benchmark credit or failure should be assigned to Exa based on this inability to connect.

## Tavily

Tavily's remote MCP supports OAuth with compatible MCP clients, and the free account tier provides monthly credits. In this ChatGPT runtime there is likewise no direct arbitrary-MCP connection surface for Tavily, so the OAuth route cannot be completed here automatically.

## Practical P0 access matrix

| Arm | Provider access cost | Can this runtime invoke it now? | Action required |
|---|---:|---|---|
| direct web/browser baseline | free | yes | none |
| Crossref/public scholarly verification | free/public | yes where web access permits | none |
| Semantic Scholar/public access | free/public | yes where web access permits | none |
| Exa hosted MCP default search/fetch | free/no personal key in principle | no | run through an MCP-capable client or expose a supported connector |
| Exa API with own key | free credits available | no direct API connector | same connector/runtime issue plus key |
| Tavily MCP/API | free account/monthly credits | no | MCP-capable client/OAuth or API connector |
| Perplexity API | paid credits required for current API access | no dedicated connector | defer until earlier arms justify spend |

## Revised resource decision

Do not ask the user to buy anything yet.

The cheapest defensible sequence is now:

1. keep the existing direct-web baseline as control;
2. run Exa P0 using its no-key hosted MCP from the first available MCP-capable execution surface;
3. run Tavily P0 using free OAuth/account credits;
4. only request a Perplexity paid smoke if Exa/Tavily results leave a material architecture uncertainty that Perplexity could resolve.

## Integrity rule

Provider inability to run because of our execution environment must be recorded as `NOT_RUN / ENVIRONMENT_BLOCKED`, never as provider failure.
