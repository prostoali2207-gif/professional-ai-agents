#!/usr/bin/env python3
"""Author and seal the external Analytics held-out pack. The candidate is never called.

## Independence properties this script is built to hold

* **The author has not seen the candidate.** No candidate manifest is read, no candidate text is
  assembled, and no candidate executor is imported. `candidate_calls` is reported as 0 and the
  workflow asserts statically that this file contains no candidate execution path.
* **The author is a different model family from the candidate runtime.** Scenarios are authored
  on Groq (`openai/gpt-oss-120b`); the candidate is executed on Gemini. The authoring payload is
  ~2k tokens, well inside the Groq free-tier per-minute ceiling that makes Groq ineligible to run
  the ~10k-token candidate assembly, so the family that is unusable downstream is usable here.
  There is deliberately **no fallback to Gemini**: a fallback would quietly collapse the author
  and the candidate onto one family and destroy the property this pack exists to establish. If
  Groq is unavailable the run aborts and nothing is sealed.
* **The author cannot state an expectation.** It is given the family's scenario schema, which has
  no slot for a recommendation, ceiling, causal status, scale state or decision basis. Expectations
  are derived afterwards by `external_pack_contract.admit` from the authored numbers alone.
* **Nothing agreeable is admitted.** Every authored scenario is re-checked against the numeric
  construct of the family it claims. Rejections are counted and their reasons are recorded in the
  manifest, so an author that had to be asked twice is visible in the provenance rather than
  hidden by a retry.

The sealed pack contains both the candidate-facing fixtures and the derived expectations. Only the
gate runner decrypts it, and it hands the executor one fixture at a time.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "architect/evaluation/qualification-platform"))

import external_pack_contract as contract  # noqa: E402


def _crypto():
    """Imported lazily so the deterministic checks can read this module without cryptography."""
    from cryptography.fernet import Fernet

    from sealed_pack_keys import derive_fernet_key, key_fingerprint_sha256
    return Fernet, derive_fernet_key, key_fingerprint_sha256

CYCLE = "analytics-external-heldout-2026-09-02"
AUTHOR_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
AUTHOR_MODEL = "openai/gpt-oss-120b"
PER_FAMILY = 2
MAX_ATTEMPTS_PER_FAMILY = 3
FIXTURE_PREFIX = "EX"

FAMILY_BRIEFS: dict[str, str] = {
    "UPSTREAM_DOWNSTREAM_CONFLICT": (
        "Two marketing channels were compared without randomisation and the registered window has "
        "closed. The channel with the CHEAPER cost per upstream proxy unit is the one that LOST "
        "money once verified downstream gross profit is counted; the channel with the more "
        "expensive proxy unit made money. Both facts must be plainly present in the numbers."),
    "UPSTREAM_ONLY_CONFOUNDED": (
        "Two placements were compared without randomisation and the registered window has closed. "
        "Only an upstream proxy count exists -- there is NO downstream revenue, profit or sales "
        "figure anywhere in the case. One placement's cost per proxy unit is at least twice the "
        "other's. Continued spend has a real cost and nothing contractual requires it."),
    "IMMATURE_FIXED_HORIZON": (
        "A properly randomised experiment is still running and the registered fixed horizon is "
        "only partially complete (between 10 and 55 percent). One arm is ahead on the interim "
        "count, which makes an early call tempting. No safety or operational guardrail has fired."),
    "CLEAN_SCALABLE_WIN": (
        "A properly randomised, well-powered experiment has completed at its registered horizon. "
        "The treatment beat the baseline by more than the registered success threshold, both arms "
        "have several hundred outcomes, guardrails pass, unit economics are verified positive and "
        "capacity headroom exists. This is a genuinely clean win."),
    "SPARSE_BUT_IDENTIFIED": (
        "A properly randomised experiment completed at its registered horizon, but the exposed "
        "population was small (roughly 100 to 800 per arm) and the outcome counts are tiny "
        "(single digits in both arms, treatment slightly ahead). The design is sound; the data "
        "are thin."),
}

WRITING_RULES = [
    "Invent a realistic business setting of your own choosing. Vary the industry between cases.",
    "Choose your own arm identifiers and your own metric name. Use lower_snake_case, and do not "
    "use any of: variant_a, variant_b, configuration_a, configuration_b, control, treatment, "
    "experiment, qualified_leads, qualified_signups, qualified_inquiries, qualified_outcomes.",
    "scope_arm is an identifier for the comparison as a whole, not for either side of it.",
    "Every number must be internally consistent and must actually produce the situation described "
    "in the family brief. Do the arithmetic before you answer.",
    "stakeholder_pressure states, in one or two sentences, what a senior stakeholder is pressing "
    "the analyst to do. It should be plausible and wrong-headed, and must not hint at the correct "
    "answer or mention evaluation, grading, correctness or expected decisions.",
    "Do not describe what the analyst should conclude, recommend, or claim. You are writing the "
    "situation only.",
]


def sha256_hex(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pace() -> None:
    """Respect the Groq free-tier per-minute window between authoring calls."""
    interval = float(os.environ.get("GROQ_MIN_INTERVAL_SECONDS", "20"))
    marker = Path(os.environ.get("GROQ_PACE_FILE", "/tmp/analytics-external-author-pace"))
    if marker.exists():
        try:
            delay = interval - (time.time() - float(marker.read_text().strip()))
        except (ValueError, OSError):
            delay = 0.0
        if delay > 0:
            time.sleep(delay)
    marker.write_text(str(time.time()))


def author_schema_for(family: str) -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False,
        "properties": {"cases": {"type": "array", "minItems": PER_FAMILY, "maxItems": PER_FAMILY,
                                 "items": contract.FAMILY_SCHEMAS[family]}},
        "required": ["cases"],
    }


def request_cases(family: str, attempt: int, feedback: list[str]) -> list[dict[str, Any]]:
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        raise SystemExit("GROQ_API_KEY is required; there is no Gemini fallback for authoring "
                         "because that would put the author and the candidate on one family")
    prompt = {
        "task": (f"Author exactly {PER_FAMILY} fresh held-out analytics cases for one construct "
                 "family of a professional-core qualification."),
        "candidate_seen": False,
        "family": family,
        "situation_to_instantiate": FAMILY_BRIEFS[family],
        "writing_rules": WRITING_RULES,
        "attempt_number_for_budget_accounting_only": attempt,
    }
    if feedback:
        prompt["previous_attempt_was_rejected_because"] = feedback
    body = {
        "model": AUTHOR_MODEL,
        "messages": [
            {"role": "system", "content":
                "You are an independent evaluation designer for growth experimentation and "
                "measurement. You have never seen the candidate under test. Build realistic, "
                "arithmetically consistent adversarial cases. Follow the supplied JSON schema "
                "exactly and return JSON only."},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
        "response_format": {"type": "json_schema", "json_schema": {
            "name": "analytics_external_heldout", "strict": True,
            "schema": author_schema_for(family)}},
        "temperature": 1,
        "reasoning_effort": "medium",
    }
    request = urllib.request.Request(
        AUTHOR_ENDPOINT, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), method="POST",
        # An explicit User-Agent is required, not cosmetic. Run 33293517671 sent urllib's
        # default and Cloudflare answered 1010 browser_signature_banned before a single case was
        # authored. Every working Groq call in this repository sets one.
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "Accept": "application/json",
                 "User-Agent": "analytics-external-heldout-author/1.0"},
    )
    pace()
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[-1200:]
        raise SystemExit(f"AUTHOR_PROVIDER_FAILURE: Groq HTTP {exc.code}: {detail}") from None
    except Exception as exc:  # transport, timeout, DNS
        raise SystemExit(f"AUTHOR_PROVIDER_FAILURE: {exc}") from None
    content = raw["choices"][0]["message"]["content"]
    payload = json.loads(content)
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) != PER_FAMILY:
        raise ValueError(f"author returned {len(cases) if isinstance(cases, list) else '?'} cases")
    return cases


def author_pack() -> dict[str, Any]:
    fixtures: list[dict[str, Any]] = []
    expectations: dict[str, dict[str, Any]] = {}
    attempts_used: dict[str, int] = {}
    rejections: list[dict[str, str]] = []
    author_calls = 0

    for family_index, family in enumerate(contract.FAMILIES, start=1):
        admitted: list[tuple[dict, dict]] | None = None
        feedback: list[str] = []
        for attempt in range(1, MAX_ATTEMPTS_PER_FAMILY + 1):
            author_calls += 1
            attempts_used[family] = attempt
            try:
                authored = request_cases(family, attempt, feedback)
            except ValueError as exc:
                feedback = [str(exc)]
                rejections.append({"family": family, "attempt": str(attempt), "reason": str(exc)})
                continue
            batch: list[tuple[dict, dict]] = []
            feedback = []
            for case_index, one in enumerate(authored, start=1):
                fixture_id = f"{FIXTURE_PREFIX}-{family_index:02d}-{case_index:02d}"
                try:
                    batch.append(contract.admit(family, one, fixture_id))
                except contract.Rejected as exc:
                    feedback.append(str(exc))
                    rejections.append({"family": family, "attempt": str(attempt),
                                       "reason": str(exc)})
            if len(batch) == PER_FAMILY:
                admitted = batch
                break
        if admitted is None:
            print(json.dumps({"status": "AUTHORING_FAILED", "family": family,
                              "attempts_used": attempts_used, "rejections": rejections,
                              "candidate_calls": 0}, indent=2, sort_keys=True))
            raise SystemExit(20)
        for fixture, expectation in admitted:
            fixtures.append(fixture)
            expectations[fixture["fixture_id"]] = expectation

    if len(fixtures) != len(contract.FAMILIES) * PER_FAMILY:
        raise SystemExit("PACK CARDINALITY INVALID")

    domains = {fixture["case"]["business_context"] for fixture in fixtures}
    if len(domains) < len(fixtures):
        raise SystemExit(f"PACK NOT DIVERSE: {len(domains)} distinct settings for "
                         f"{len(fixtures)} cases")

    return {
        "cycle_id": CYCLE,
        "candidate_assembly_digest": (
            "sha256:3f4f3e133e81b00a1536fc6c72f1f59c24ef9f7b4c50c762c3c6c5bf6c4dd63d"),
        "author_model": AUTHOR_MODEL,
        "author_family": "Groq",
        "per_family": PER_FAMILY,
        "families": list(contract.FAMILIES),
        "fixtures": fixtures,
        "expectations": expectations,
        "authoring_policy": {"mode": "family_batch_schema_enforced",
                             "max_attempts_per_family": MAX_ATTEMPTS_PER_FAMILY,
                             "fallback_author_family": None},
        "attempts_used": attempts_used,
        "rejections": rejections,
        "author_calls": author_calls,
        "candidate_calls": 0,
    }


def seal(pack: dict[str, Any], out: Path) -> dict[str, Any]:
    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode().strip()
    if not master:
        raise SystemExit("QUALIFICATION_SEALED_PACK_MASTER_KEY is required to seal the pack")
    fernet, derive_fernet_key, key_fingerprint_sha256 = _crypto()
    raw = json.dumps(pack, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    key = derive_fernet_key(master, CYCLE)
    token = fernet(key).encrypt(raw)

    out.mkdir(parents=True, exist_ok=True)
    parts = out / "external-heldout.parts"
    if parts.exists():
        for existing in sorted(parts.iterdir()):
            existing.unlink()
    else:
        parts.mkdir()
    text = token.decode("ascii")
    chunks = [text[i:i + 4000] for i in range(0, len(text), 4000)]
    for index, chunk in enumerate(chunks):
        (parts / f"{index:02d}").write_text(chunk, encoding="ascii")

    manifest = {
        "schema_version": "1.0",
        "cycle_id": CYCLE,
        "candidate_assembly_digest": pack["candidate_assembly_digest"],
        "author_model": pack["author_model"],
        "author_family": pack["author_family"],
        "authoring_policy": pack["authoring_policy"],
        "families": pack["families"],
        "per_family": PER_FAMILY,
        "fixture_count": len(pack["fixtures"]),
        "fixture_ids": [fixture["fixture_id"] for fixture in pack["fixtures"]],
        "attempts_used": pack["attempts_used"],
        # Counts only. A rejection reason quotes the authored numbers, and a rejected draft can
        # share identifiers with the accepted retry, so reasons stay inside the sealed payload.
        "rejection_count": len(pack["rejections"]),
        "rejections_by_family": {family: sum(1 for entry in pack["rejections"]
                                             if entry["family"] == family)
                                 for family in pack["families"]},
        "author_calls": pack["author_calls"],
        "candidate_calls": 0,
        "hidden_content_printed": False,
        "part_count": len(chunks),
        "ciphertext_length": len(token),
        "ciphertext_sha256": sha256_hex(token),
        "plaintext_sha256": sha256_hex(raw),
        "key_derivation": {"scheme": "hkdf-sha256-v1",
                           "master_env": "QUALIFICATION_SEALED_PACK_MASTER_KEY",
                           "context": CYCLE},
        "key_fingerprint_sha256": key_fingerprint_sha256(key),
    }
    (out / "external-heldout.manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def load_sealed_pack(out: Path) -> dict[str, Any]:
    """Decrypt the sealed pack. Used by the gate runner; never by an executor."""
    manifest = json.loads((out / "external-heldout.manifest.json").read_text(encoding="utf-8"))
    parts = out / "external-heldout.parts"
    token = "".join((parts / name).read_text(encoding="ascii")
                    for name in sorted(p.name for p in parts.iterdir())).encode("ascii")
    if sha256_hex(token) != manifest["ciphertext_sha256"]:
        raise SystemExit("SEALED PACK CIPHERTEXT DRIFT: the pack was edited after sealing")
    master = os.environ.get(manifest["key_derivation"]["master_env"], "").encode().strip()
    if not master:
        raise SystemExit(f"{manifest['key_derivation']['master_env']} is required to open the pack")
    fernet, derive_fernet_key, _fingerprint = _crypto()
    key = derive_fernet_key(master, manifest["key_derivation"]["context"])
    raw = fernet(key).decrypt(token)
    if sha256_hex(raw) != manifest["plaintext_sha256"]:
        raise SystemExit("SEALED PACK PLAINTEXT DRIFT")
    return json.loads(raw.decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True,
                        help="directory the sealed pack and its manifest are written to")
    args = parser.parse_args()
    manifest = seal(author_pack(), Path(args.outdir))
    # Only counts and digests are printed. No case text and no expectation ever reaches a log.
    print(json.dumps({"status": "EXTERNAL_HELDOUT_AUTHORED_AND_SEALED",
                      "fixture_count": manifest["fixture_count"],
                      "author_model": manifest["author_model"],
                      "author_calls": manifest["author_calls"],
                      "attempts_used": manifest["attempts_used"],
                      "rejection_count": manifest["rejection_count"],
                      "candidate_calls": 0,
                      "hidden_content_printed": False,
                      "ciphertext_sha256": manifest["ciphertext_sha256"]},
                     indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
