import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from urllib.parse import urlparse

OUT = "architect/research/benchmark/runs/source-lineage-correlated-evidence-v0.1.json"

FIXTURES = [
    {
        "claim_id": "C1",
        "sources": [
            {"id": "s1", "url": "https://agency.example/press/alpha", "source_type": "primary", "upstream": None, "content_fingerprint": "A1", "claim": "alpha"},
            {"id": "s2", "url": "https://news-a.example/story", "source_type": "secondary", "upstream": "s1", "content_fingerprint": "A1-summary", "claim": "alpha"},
            {"id": "s3", "url": "https://news-b.example/story", "source_type": "secondary", "upstream": "s1", "content_fingerprint": "A1-summary", "claim": "alpha"},
            {"id": "s4", "url": "https://blog.example/post", "source_type": "secondary", "upstream": "s2", "content_fingerprint": "A1-summary", "claim": "alpha"},
        ],
        "expected_independent_roots": 1,
    },
    {
        "claim_id": "C2",
        "sources": [
            {"id": "s1", "url": "https://publisher-a.example/paper", "source_type": "primary", "upstream": None, "content_fingerprint": "PAPER-A", "claim": "beta"},
            {"id": "s2", "url": "https://publisher-b.example/paper", "source_type": "primary", "upstream": None, "content_fingerprint": "PAPER-B", "claim": "beta"},
            {"id": "s3", "url": "https://review.example/article", "source_type": "secondary", "upstream": None, "cites": ["s1", "s2"], "content_fingerprint": "REVIEW", "claim": "beta"},
        ],
        "expected_independent_roots": 2,
    },
    {
        "claim_id": "C3",
        "sources": [
            {"id": "s1", "url": "https://wire.example/release", "source_type": "secondary", "upstream": "origin", "content_fingerprint": "WIRE-EXACT", "claim": "gamma"},
            {"id": "s2", "url": "https://paper1.example/news", "source_type": "secondary", "upstream": "origin", "content_fingerprint": "WIRE-EXACT", "claim": "gamma"},
            {"id": "s3", "url": "https://paper2.example/news", "source_type": "secondary", "upstream": "origin", "content_fingerprint": "WIRE-EXACT", "claim": "gamma"},
        ],
        "synthetic_external_root": "origin",
        "expected_independent_roots": 1,
    },
    {
        "claim_id": "C4",
        "sources": [
            {"id": "s1", "url": "https://lab-a.example/result", "source_type": "primary", "upstream": None, "content_fingerprint": "LAB-A", "claim": "delta"},
            {"id": "s2", "url": "https://lab-b.example/result", "source_type": "primary", "upstream": None, "content_fingerprint": "LAB-B", "claim": "delta"},
            {"id": "s3", "url": "https://lab-c.example/result", "source_type": "primary", "upstream": None, "content_fingerprint": "LAB-C", "claim": "delta"},
        ],
        "expected_independent_roots": 3,
    },
]


def primitive_roots(source_id, by_id, seen=None):
    seen = set() if seen is None else set(seen)
    if source_id in seen:
        return {f"cycle:{source_id}"}
    seen.add(source_id)

    source = by_id.get(source_id)
    if source is None:
        return {source_id}

    cites = source.get("cites") or []
    if source.get("source_type") != "primary" and cites:
        roots = set()
        for cited_id in cites:
            roots.update(primitive_roots(cited_id, by_id, seen))
        return roots or {"UNKNOWN"}

    upstream = source.get("upstream")
    if upstream:
        if upstream not in by_id:
            return {upstream}
        return primitive_roots(upstream, by_id, seen)

    return {source_id}


def lineage_for_case(case):
    by_id = {s["id"]: s for s in case["sources"]}
    source_roots = {s["id"]: sorted(primitive_roots(s["id"], by_id)) for s in case["sources"]}
    clusters = defaultdict(list)
    all_roots = set()
    for sid, roots in source_roots.items():
        all_roots.update(roots)
        for rid in roots:
            clusters[rid].append(sid)
    return source_roots, dict(clusters), all_roots


def domain(url):
    return urlparse(url).hostname or ""


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gate": "source-lineage-correlated-evidence-v0.1",
        "rules": [
            "Evidence independence is counted by primitive lineage roots, not URL count.",
            "Syndicated/repackaged copies sharing one upstream source count as one evidentiary lineage.",
            "A secondary review inherits the primitive roots of the evidence it cites; it does not create a new independent lineage for the same claim.",
            "Different domains are not sufficient evidence of independence.",
            "Unknown lineage must remain UNKNOWN rather than assumed independent.",
        ],
        "cases": [],
    }

    failures = []
    for case in FIXTURES:
        roots, clusters, all_roots = lineage_for_case(case)
        unique_roots = len(all_roots)
        source_domains = {s["id"]: domain(s["url"]) for s in case["sources"]}
        passed = unique_roots == case["expected_independent_roots"]
        row = {
            "claim_id": case["claim_id"],
            "source_count": len(case["sources"]),
            "domains": source_domains,
            "roots": roots,
            "clusters": clusters,
            "independent_root_count": unique_roots,
            "expected_independent_roots": case["expected_independent_roots"],
            "passed": passed,
        }
        record["cases"].append(row)
        if not passed:
            failures.append(row)

    adversarial = []
    for case in FIXTURES:
        domain_count = len({domain(s["url"]) for s in case["sources"]})
        _, _, all_roots = lineage_for_case(case)
        root_count = len(all_roots)
        adversarial.append({
            "claim_id": case["claim_id"],
            "domain_count": domain_count,
            "root_count": root_count,
            "domain_count_would_overstate": domain_count > root_count,
        })
    record["adversarial_checks"] = adversarial
    record["failures"] = failures
    record["status"] = "PASS" if not failures else "FAIL"

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
