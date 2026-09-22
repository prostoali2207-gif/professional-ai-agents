# Low-Appetite Muscle-Gain Nutrition — knowledge packaging audit v0.1

Status: pre-SKILL audit required for CORE / BOUNDARY-CRITICAL competencies.

| Dependency | Consumed by | Class | Runtime packaging decision | Reason |
|---|---|---|---|---|
| protein sufficiency and distribution | LN-03/04 | stable/slow empirical | EMBED_CORE + source register | frequent decision; compact and stable enough |
| surplus-size uncertainty / rate-of-gain evidence | LN-01/02 | slow empirical | EMBED_CORE + reference | central judgment; must retain study limitations |
| carbohydrate-performance context | LN-05 | slow empirical | EMBED_CORE | prevents rigid high-carb folklore |
| energy-density strategy | LN-06 | stable empirical/practical | EMBED_CORE + procedural ladder | central low-appetite mechanism |
| dietary self-report uncertainty | LN-09/14 | stable measurement evidence | EMBED_CORE | prevents false precision |
| meal-frequency/timing evidence | LN-08 | slow empirical | EMBED_CORE | needed to reject unnecessary meal burden |
| micronutrient/fiber exact RDAs/AIs | LN-10 | versioned by demographic/jurisdiction | LIVE_RESEARCH when exact values matter | avoid hard-coding every population table |
| creatine efficacy/safety for healthy adults | LN-11 | slow empirical | EMBED_CORE | common, evidence-rich optional aid |
| supplement regulation/product contamination/banned status | LN-11 | volatile/jurisdiction/sport | LIVE_RESEARCH / ESCALATE | product and jurisdiction dependent |
| clinical appetite loss / malnutrition thresholds | LN-12 | clinical/versioned | REFERENCE + LIVE_RESEARCH for material case | high-stakes boundary |
| disease-specific diet/protein advice | LN-12 | clinical | ESCALATE | outside applied skill authority |
| state schema / trend arithmetic | LN-13/14 | procedural/tool-backed | PROCEDURAL_MODULE / TOOL_BACKED | deterministic and reusable in skill |
| current user's weights/intake/performance | LN-01/13 | volatile personal state | STRUCTURED_RUNTIME_STATE | must update/supersede, not bake into skill |

## Knowledge depth decisions

### Embed
The final skill must contain enough operational knowledge to make routine decisions without reopening research:
- 1.6–2.0 g/kg/day protein working range with ~1.6 default sufficiency target;
- conservative feedback-controlled energy changes;
- 20–35% energy fat working context;
- carbs as training-demand-dependent remainder;
- low-volume energy-density ladder;
- trend/measurement uncertainty;
- supplement and clinical boundaries.

### Retrieve live
Use live authoritative retrieval when:
- exact clinical guidance or escalation threshold is materially decisive;
- a supplement product/regulatory/banned-substance claim is current;
- exact demographic micronutrient reference values matter;
- a source/position statement has been materially updated.

### Tool-backed
Arithmetic for:
- body-mass trend;
- rate-of-gain percentage;
- macro grams/calories;
- candidate energy increment;
should be deterministic where a calculator/tool is available.

## Progressive disclosure

Do not load:
- exhaustive micronutrient tables;
- large food databases;
- disease-specific nutrition;
- supplement catalogs;
- contest-prep protocols.

The low-appetite skill should stay narrow: determine minimum sufficient intake and implement it with compact, tolerable food architecture.
