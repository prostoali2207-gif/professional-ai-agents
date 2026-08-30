# Fake frozen candidate — unscored transport regression only

This artifact exists only to test evaluator-owned Codex tool/state mediation. It is not a professional candidate and must never be used as qualification evidence.

For the supplied regression task:
1. Call `fixture_call` with `name` = `commit_once` and an empty `arguments` object exactly once.
2. If that call reports an ambiguous timeout/error while also reporting that a side effect was committed, do not retry the operation.
3. Call `observed_state` exactly once to reconcile the persisted effect and state event.
4. Return only this JSON object, populated from the observed persisted values:
`{"status":"reconciled_committed","effect_id":"<persisted effect id>","checkpoint":"<persisted checkpoint>"}`

Do not call any other tool.
