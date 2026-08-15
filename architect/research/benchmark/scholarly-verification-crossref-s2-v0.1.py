import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

OUT = "architect/research/benchmark/runs/scholarly-verification-crossref-s2-v0.1.json"
BERT_DOI = "10.18653/v1/N19-1423"
BERT_ARXIV = "1810.04805"
RETRACTION_DOI = "10.1177/17588359231172420"


def get_json(url, timeout=30):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "professional-ai-agents-research-benchmark/0.1 mailto:benchmark@example.invalid",
            "Accept": "application/json",
        },
        method="GET",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        return resp.status, round(time.perf_counter() - started, 3), json.loads(body)


def crossref_work(doi):
    encoded = urllib.parse.quote(doi, safe="")
    return get_json(f"https://api.crossref.org/works/{encoded}")


def s2_paper(identifier):
    encoded = urllib.parse.quote(identifier, safe=":")
    fields = "paperId,title,authors,year,venue,externalIds,url,publicationDate,journal,publicationTypes"
    return get_json(f"https://api.semanticscholar.org/graph/v1/paper/{encoded}?fields={fields}")


def author_surnames_crossref(message):
    return [str(a.get("family", "")).lower() for a in message.get("author", []) if isinstance(a, dict)]


def author_names_s2(payload):
    return [str(a.get("name", "")).lower() for a in payload.get("authors", []) if isinstance(a, dict)]


def contains_all(values, required):
    blob = " ".join(values)
    return all(r.lower() in blob for r in required)


def check(name, passed, severity="P0", detail=None):
    row = {"check": name, "passed": bool(passed), "severity": severity}
    if detail is not None:
        row["detail"] = detail
    return row


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gate": "scholarly-verification-crossref-s2-v0.1",
        "requests": [],
        "checks": [],
        "observations": {},
        "scope_limitations": [
            "This is a narrow verification gate, not a broad scholarly-recall benchmark.",
            "Crossref and Semantic Scholar are tested for different roles; no aggregate winner is computed.",
            "Semantic Scholar unauthenticated public API availability/rate behavior may vary; an HTTP/rate failure is operational evidence, not bibliographic falsification.",
        ],
    }

    # 1) Crossref exact DOI identity for BERT.
    try:
        status, latency, cr_bert_raw = crossref_work(BERT_DOI)
        cr_bert = cr_bert_raw.get("message", {})
        record["requests"].append({"case": "crossref_bert_doi", "status": status, "latency_seconds": latency})
        title = " ".join(cr_bert.get("title", []))
        surnames = author_surnames_crossref(cr_bert)
        record["observations"]["crossref_bert"] = {
            "doi": cr_bert.get("DOI"),
            "title": title,
            "authors": surnames,
            "published": cr_bert.get("published"),
            "type": cr_bert.get("type"),
        }
        record["checks"].extend([
            check("Crossref BERT DOI exact", str(cr_bert.get("DOI", "")).lower() == BERT_DOI.lower()),
            check("Crossref BERT title identity", "bert" in title.lower()),
            check("Crossref BERT author identity", contains_all(surnames, ["devlin", "chang", "lee", "toutanova"])),
        ])
    except Exception as exc:
        record["requests"].append({"case": "crossref_bert_doi", "status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
        record["checks"].append(check("Crossref BERT endpoint reachable", False, severity="P1"))
        cr_bert = {}

    # 2) Semantic Scholar exact DOI identity for same work.
    try:
        status, latency, s2_doi = s2_paper(f"DOI:{BERT_DOI}")
        record["requests"].append({"case": "s2_bert_doi", "status": status, "latency_seconds": latency})
        names = author_names_s2(s2_doi)
        ext = s2_doi.get("externalIds") or {}
        record["observations"]["s2_bert_doi"] = {
            "paperId": s2_doi.get("paperId"),
            "title": s2_doi.get("title"),
            "authors": names,
            "externalIds": ext,
            "year": s2_doi.get("year"),
            "venue": s2_doi.get("venue"),
        }
        record["checks"].extend([
            check("S2 BERT DOI exact", str(ext.get("DOI", "")).lower() == BERT_DOI.lower(), severity="P1"),
            check("S2 BERT title identity", "bert" in str(s2_doi.get("title", "")).lower(), severity="P1"),
            check("S2 BERT author identity", contains_all(names, ["devlin", "chang", "lee", "toutanova"]), severity="P1"),
        ])
    except Exception as exc:
        record["requests"].append({"case": "s2_bert_doi", "status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
        record["checks"].append(check("S2 BERT DOI endpoint reachable", False, severity="P1"))
        s2_doi = {}

    # 3) Semantic Scholar arXiv identifier: inspect whether preprint/published identity is unified or split.
    try:
        status, latency, s2_arxiv = s2_paper(f"ARXIV:{BERT_ARXIV}")
        record["requests"].append({"case": "s2_bert_arxiv", "status": status, "latency_seconds": latency})
        ext = s2_arxiv.get("externalIds") or {}
        record["observations"]["s2_bert_arxiv"] = {
            "paperId": s2_arxiv.get("paperId"),
            "title": s2_arxiv.get("title"),
            "externalIds": ext,
            "year": s2_arxiv.get("year"),
            "venue": s2_arxiv.get("venue"),
        }
        same_id = bool(s2_doi.get("paperId") and s2_doi.get("paperId") == s2_arxiv.get("paperId"))
        record["observations"]["s2_version_identity"] = {
            "doi_and_arxiv_same_paperId": same_id,
            "doi_paperId": s2_doi.get("paperId"),
            "arxiv_paperId": s2_arxiv.get("paperId"),
            "arxiv_externalIds": ext,
        }
        record["checks"].extend([
            check("S2 arXiv identifier exact", str(ext.get("ArXiv", "")) == BERT_ARXIV, severity="P1"),
            check("S2 arXiv title identity", "bert" in str(s2_arxiv.get("title", "")).lower(), severity="P1"),
        ])
    except Exception as exc:
        record["requests"].append({"case": "s2_bert_arxiv", "status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
        record["checks"].append(check("S2 BERT arXiv endpoint reachable", False, severity="P1"))

    # 4) Crossref post-publication update/retraction signal.
    try:
        status, latency, cr_ret_raw = crossref_work(RETRACTION_DOI)
        cr_ret = cr_ret_raw.get("message", {})
        record["requests"].append({"case": "crossref_retraction_signal", "status": status, "latency_seconds": latency})
        updates = cr_ret.get("update-to") or cr_ret.get("updated-by") or []
        update_rows = updates if isinstance(updates, list) else [updates]
        retraction_rows = [u for u in update_rows if isinstance(u, dict) and str(u.get("type", "")).lower() == "retraction"]
        sources = sorted({str(u.get("source", "")) for u in retraction_rows if u.get("source")})
        record["observations"]["crossref_retraction"] = {
            "doi": cr_ret.get("DOI"),
            "title": cr_ret.get("title"),
            "update_to": cr_ret.get("update-to"),
            "updated_by": cr_ret.get("updated-by"),
            "retraction_rows": retraction_rows,
            "sources": sources,
        }
        record["checks"].extend([
            check("Crossref retraction record exact DOI", str(cr_ret.get("DOI", "")).lower() == RETRACTION_DOI.lower()),
            check("Crossref exposes retraction signal", bool(retraction_rows)),
            check("Crossref exposes retraction provenance source", bool(sources), severity="P1"),
        ])
    except Exception as exc:
        record["requests"].append({"case": "crossref_retraction_signal", "status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
        record["checks"].append(check("Crossref retraction endpoint reachable", False, severity="P1"))

    p0 = [c for c in record["checks"] if c["severity"] == "P0" and not c["passed"]]
    p1 = [c for c in record["checks"] if c["severity"] == "P1" and not c["passed"]]
    record["failures"] = [c for c in record["checks"] if not c["passed"]]
    record["status"] = "FAIL_P0" if p0 else ("REVIEW_P1" if p1 else "PASS")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    if p0:
        raise SystemExit(2)
    if p1:
        raise SystemExit(3)


if __name__ == "__main__":
    main()
