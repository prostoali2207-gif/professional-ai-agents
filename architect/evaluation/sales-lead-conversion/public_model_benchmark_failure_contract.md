# Public Sales model benchmark failure evidence

This benchmark is development evidence only, not sealed qualification.

If a provider/runtime error occurs, the runner must emit a structured JSON result before exiting non-zero. The result records the attempted case, `runtime_error` status, a bounded diagnostic string, and usage accumulated before the failure. It must not expose credentials, sealed fixtures, grader keys, expected answers, or thresholds.

The benchmark stops after the first runtime error to avoid spending API credits on cases that cannot produce valid comparative evidence. Behavioral failures after successful execution may continue through all public cases.
