# Stage C — EVALUATOR_CONSTRUCT_FAIL — corpus validity not established

Date: 2026-09-13
Issue: #294
Branch: `fix/video-capture-v0.4-294`
Execution chain: Stage C held-out author / review / seal

Status: **STOP before candidate execution.** Candidate calls: **0**. Grader calls: **0**.

## 1. The final eligible technical retry succeeded technically

Both planned calls returned rc=0. **No technical defect occurred**, so the rule-5
`NOT_EXECUTABLE`-on-technical-defect branch was not triggered.

| call | callee | model | result |
|---|---|---|---|
| targeted field repair, `SPEECH_FALLBACK` case 2 `competent_generic_baseline` | candidate-blind author | `opus` | `revised`, structural validation passed |
| re-audit of `SPEECH_FALLBACK` only | candidate-blind auditor | `sonnet` | `REVISE` |

The narrow repair path did exactly what it was built to do. Deterministic diff against the
pre-revision artifact:

- `case2.competent_generic_baseline` — **changed** (the intended repair);
- every other field of both cases, and the whole `pair_contract` — **identical**;
- all candidate-visible text (`brief`, `context`, `constraints`, both cases) — **byte-identical**,
  sha256 `72c0484b9f1f…` before and after.

`baseline_is_fair`, the check that motivated the repair, now passes. The repair worked.

## 2. What the re-audit found instead

The re-audit failed a **different** check, `no_hidden_leakage`, on candidate-visible text that is
byte-identical to the text the **first** audit passed on that same check.

The finding is asymmetric disclosure across the pair: case 2's context states that the cabin can be
shut, which is exactly the affordance its `professional_criteria` reward ("tests a sheltered
position… the cabin with doors shut"), while case 1's otherwise-parallel sentence omits it for the
same physical vehicle.

### The finding is correct, and it is not auditor noise

Verified deterministically against the family's own pair contract:

- `expected_stance_relation`: `MUST_DIVERGE`;
- `controlled_material_fact`: the compressor duty cycle — cycling with 2-3 minute quiet windows
  versus continuous running until 18:00;
- `held_constant_facts` explicitly include **"Same vehicle, location and layout"** and
  **"the car cannot be repositioned during the slot"**.

The shut-cabin affordance is therefore **not** the controlled variable. It is an incidental,
answer-relevant affordance that the pair contract's own held-constant declaration requires to be the
same in both cases. Disclosing it only in the case where it is the solution is a genuine
discriminative-validity defect: a careful responder can pattern-match the hint rather than reason
from the noise evidence.

## 3. Classification and its corpus-wide consequence

**Classification: `EVALUATOR_CONSTRUCT_FAIL`.**

Not a professional failure — the candidate has never been run against this corpus. Not a
technical/runtime failure — both calls succeeded.

The consequence is larger than one family. The first audit returned `no_hidden_leakage: true` on
this exact text; the second returned `false` and was right. **The construct auditor has produced a
demonstrated false negative.**

Every one of the other **11 ACCEPT verdicts is a single-sample verdict from that same auditor**.
`SPEECH_FALLBACK` is the only family that ever received a second look, and the second look found a
real defect the first missed. There is no basis for assuming the remaining families are clean; there
is now concrete evidence that one pass is insufficient to establish construct validity.

## 4. Why the candidate was not run

Running the frozen v0.4 candidate against this corpus now would consume 24 candidate calls and 24
grader calls and produce a held-out pass rate that **looks like release evidence but is not**: it
would rest on a corpus whose construct validity has just been falsified in the one family that was
checked twice.

A wrong number that carries the authority of a held-out result is worse than no number. Stage C
stops here with the corpus preserved and no candidate evidence claimed in either direction.

## 5. Budget state — nothing further was spent

- bounded local repair for this chain: **1, consumed** (the narrow field-only path);
- final eligible technical retry: **spent, and it did not fail technically**;
- no further harness repair was attempted, per the standing instruction;
- the auditor was **not** re-run to seek a better verdict. Re-running a grader until it returns
  ACCEPT is verdict shopping and would corrupt the qualification.

Cumulative Stage C model calls: 34 prior + 2 this retry = **36**. Candidate calls remain **0**.

## 6. Open decision for the owner

The corpus cannot be sealed with an unresolved REVISE, and the other 11 families now carry unquantified
false-negative risk. Three options, none of which may be taken unilaterally inside a chain whose
budget is spent:

1. **Re-audit the 11 ACCEPT families once more** (11 candidate-blind auditor calls, 0 candidate
   calls) to measure the false-negative rate before deciding anything else. This is the cheapest way
   to learn whether the corpus is broadly sound or broadly suspect, and is the recommended next step.
2. **Repair the `SPEECH_FALLBACK` asymmetry** by having the candidate-blind author restate the
   affordance symmetrically in both cases. This touches candidate-visible fields in both cases, so it
   is beyond a field-only repair and beyond the consumed budget; it needs explicit authorization.
3. **Declare Stage C `NOT_EXECUTABLE`** for this chain, preserve the corpus, and re-open held-out
   authoring under a stricter review design — for example two independent audit passes per family,
   with disagreement forcing revision.

## 7. Release claim — unchanged

`CANDIDATE / DEVELOPMENT_PASS / HELDOUT_NOT_EXECUTED / PRACTICAL_NOT_EXECUTED`.

Stage C has produced **no professional evidence about the candidate**. The Stage D real ordinary
used-car practical gate remains mandatory. **Not QUALIFIED.**
