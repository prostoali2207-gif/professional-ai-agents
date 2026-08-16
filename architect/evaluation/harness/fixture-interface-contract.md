# Behavioral Fixture Tool Interface Contract

Status: required for controlled behavioral fixtures.

The evaluation harness may hide fixture responses, downstream state, grader keys, future variants, and expected answers. It must not hide the callable interface itself.

For every controlled `fixture_call` operation that a candidate may legitimately need, the candidate-visible task or tool catalog must expose the operation name and enough argument-shape information to invoke it. Requiring the model to guess a hidden operation identifier measures interface guessing, not professional tool-use competence.

A failed invocation caused solely by an undisclosed operation name is a harness/interface failure and is not behavioral release evidence against the candidate.

Disclosure of an operation name or schema is not disclosure of its response, side effect, hidden state, or correct decision policy. The evaluator must still keep those hidden where the test requires it.

When a fixture is repaired after outputs were observed, the repaired fixture is regression evidence only. Release evidence must use a fresh held-out variant, consistent with `v1.1-benchmark-validation-gate.md`.
