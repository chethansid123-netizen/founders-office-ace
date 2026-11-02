"""Check every source link the site shows.

For each PDF the site links to (the filing behind every verified seat, plus the
filings cited as practice evidence) this script:

  1. downloads it again with the same honest User-Agent as fetch.py,
     one request at a time with a pause between requests;
  2. checks HTTP 200, a PDF body, and an allowed exchange host after redirects;
  3. compares the SHA-256 with the hash recorded when the filing was first
     fetched, so a changed or replaced document is caught;
  4. checks that every cited page number exists in that PDF (the site links to
     url#page=N).

It respects blocks: on HTTP 401/403/407/429/451 it stops at once and records
which links were not checked. It never retries around a block.

Usage:  python3 -I pipeline/check_links.py
Output: data/link_check.json
"""

from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

import requests  # noqa: E402

from common import ALLOWED_HOSTS, CONFIG, DATA, USER_AGENT, load_json, now_utc, save_json, url_key  # noqa: E402

PAUSE_SECONDS = 2.5
BLOCK_CODES = {401, 403, 407, 429, 451}
OUT = DATA / "link_check.json"


def site_links() -> dict[str, dict]:
    """URL -> {why: [...], pages: set of cited pages} for everything the site links to."""
    records = load_json(DATA / "records.json")["records"]
    manifest = load_json(DATA / "raw" / "manifest.json", {})
    practices = load_json(CONFIG / "practices.json")
    links: dict[str, dict] = {}

    def add(url: str, why: str, page, sha: str | None = None) -> None:
        entry = links.setdefault(url, {"why": [], "pages": set(), "sha256": sha})
        if why not in entry["why"]:
            entry["why"].append(why)
        if isinstance(page, int):
            entry["pages"].add(page)

    for r in records:
        if r["review_status"] != "VERIFIED":
            continue
        # The address the site links to: the permanent copy when there is one.
        url = r.get("source_url_stable") or r["source_url"]
        sha = r.get("source_sha256")
        add(url, f"seat {r['id']}", r.get("source_page"), sha)
        for ev in r.get("evidence", {}).values():
            add(url, f"seat {r['id']}", ev.get("page"), sha)
        for c in r.get("context_facts", []):
            add(url, f"seat {r['id']}", c.get("page"), sha)

    verified_companies = {r["company"] for r in records if r["review_status"] == "VERIFIED"}
    for company, info in practices["companies"].items():
        if company not in verified_companies:
            continue
        for ev in info.get("evidence", []) or []:
            m = manifest.get(ev["source_key"])
            if m:
                add(m["url"], f"practice evidence for {company}", ev.get("page"), m.get("sha256"))
    return links


def main() -> int:
    manifest = load_json(DATA / "raw" / "manifest.json", {})
    links = site_links()
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/pdf"})
    session.max_redirects = 3

    results = []
    stopped = None
    urls = sorted(links)
    print(f"{len(urls)} links to check")
    for i, url in enumerate(urls):
        info = links[url]
        rec = {"url": url, "used_by": info["why"], "cited_pages": sorted(info["pages"])}
        host = urlparse(url).hostname or ""
        if host not in ALLOWED_HOSTS:
            rec.update(ok=False, problem=f"host not allowed: {host}")
            results.append(rec)
            continue
        if stopped:
            rec.update(ok=None, problem=f"not checked: {stopped}")
            results.append(rec)
            continue
        try:
            resp = session.get(url, timeout=60, allow_redirects=True)
        except requests.RequestException as exc:
            stopped = f"network error on {url}: {exc}"
            rec.update(ok=None, problem=f"not checked: {stopped}")
            results.append(rec)
            continue
        final_host = urlparse(resp.url).hostname or ""
        if resp.status_code in BLOCK_CODES:
            stopped = f"HTTP {resp.status_code} from {final_host}; stopped without retrying"
            rec.update(ok=None, http_status=resp.status_code, problem=stopped)
            results.append(rec)
            continue

        body = resp.content
        sha = hashlib.sha256(body).hexdigest()
        known = manifest.get(url_key(url), {})
        if not known:  # a permanent copy: same document, recorded under its first address
            known = next((m for m in manifest.values() if m.get("sha256") == info["sha256"]), {})
        pages = known.get("pages")
        rec.update(
            http_status=resp.status_code,
            final_host=final_host,
            is_pdf=body.startswith(b"%PDF"),
            bytes=len(body),
            sha256=sha,
            sha256_recorded=info["sha256"] or known.get("sha256"),
            sha256_match=(info["sha256"] or known.get("sha256")) == sha,
            pdf_pages=pages,
            pages_ok=bool(pages) and all(1 <= p <= pages for p in info["pages"]),
        )
        problems = []
        if resp.status_code != 200:
            problems.append(f"HTTP {resp.status_code}")
        if final_host not in ALLOWED_HOSTS:
            problems.append(f"redirected to {final_host}")
        if not rec["is_pdf"]:
            problems.append("body is not a PDF")
        if not rec["sha256_match"]:
            problems.append("SHA-256 differs from the hash recorded at first fetch")
        if not rec["pages_ok"]:
            problems.append(f"a cited page is outside 1..{pages}")
        rec["ok"] = not problems
        if problems:
            rec["problem"] = "; ".join(problems)
        results.append(rec)
        print(f"  {'ok ' if rec['ok'] else 'BAD'} {resp.status_code} {url}" + (f"  ({rec.get('problem')})" if not rec["ok"] else ""))
        if i < len(urls) - 1:
            time.sleep(PAUSE_SECONDS)

    checked = [r for r in results if r.get("ok") is not None]
    out = {
        "checked_at": now_utc(),
        "user_agent": USER_AGENT,
        "links": len(results),
        "checked": len(checked),
        "ok": sum(1 for r in results if r.get("ok") is True),
        "failed": sum(1 for r in results if r.get("ok") is False),
        "not_checked": sum(1 for r in results if r.get("ok") is None),
        "stopped": stopped,
        "pages_cited": sum(len(r["cited_pages"]) for r in results),
        "results": results,
    }
    save_json(OUT, out)
    print(f"{out['ok']} ok, {out['failed']} failed, {out['not_checked']} not checked -> {OUT.relative_to(DATA.parent)}")
    return 0 if out["failed"] == 0 and out["not_checked"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
