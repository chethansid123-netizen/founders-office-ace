"""Download filing PDFs listed in data/leads.json, politely.

Rules this script enforces (brief, rule 9):
  * one honest user agent, no cookies, no browser impersonation;
  * only the exchange archive hosts in common.ALLOWED_HOSTS;
  * a pause between requests;
  * on 401/403/429 (or any other refusal) it stops at once, writes
    data/manual_download_list.md and exits non-zero. It never retries a block.

Usage:  python3 -I pipeline/fetch.py
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # pipeline/ (own code only)

import sys
import time
from urllib.parse import urlparse

import requests

from common import (ALLOWED_HOSTS, DATA, PDF_DIR, USER_AGENT, load_json, now_utc,
                    save_json, sha256_file, url_key)

PAUSE_SECONDS = 2.5
BLOCK_CODES = {401, 403, 407, 429, 451}

LEADS = DATA / "leads.json"
MANIFEST = DATA / "raw" / "manifest.json"
MANUAL = DATA / "manual_download_list.md"


def write_manual_list(pending: list[dict], reason: str) -> None:
    lines = [
        "# Filings to download by hand",
        "",
        f"Automatic download stopped: {reason}",
        "",
        "Save each PDF into `data/raw/pdf/` using the file name shown, then run",
        "`python3 -I pipeline/fetch.py --local` to register them.",
        "",
        "| File name | Source URL |",
        "|---|---|",
    ]
    for lead in pending:
        lines.append(f"| `{url_key(lead['url'])}.pdf` | {lead['url']} |")
    MANUAL.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    leads = load_json(LEADS, [])
    manifest = load_json(MANIFEST, {})
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    local_only = "--local" in sys.argv

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/pdf"})
    session.max_redirects = 3

    todo = [l for l in leads if url_key(l["url"]) not in manifest]
    print(f"{len(leads)} leads, {len(todo)} to fetch")
    for i, lead in enumerate(todo):
        url = lead["url"]
        key = url_key(url)
        dest = PDF_DIR / f"{key}.pdf"
        host = urlparse(url).hostname or ""
        if host not in ALLOWED_HOSTS:
            print(f"  skip (host not allowed): {url}")
            continue

        if local_only or dest.exists():
            if not dest.exists():
                continue
            entry = {"url": url, "final_url": url, "http_status": None,
                     "content_type": "application/pdf", "fetched_at": now_utc(),
                     "fetched_by": "manual download" if local_only else "cache"}
        else:
            try:
                resp = session.get(url, timeout=60, allow_redirects=True)
            except requests.RequestException as exc:
                print(f"  network error, stopping: {exc}")
                write_manual_list(todo[i:], f"network error on {url}: {exc}")
                save_json(MANIFEST, manifest)
                return 2
            final_host = urlparse(resp.url).hostname or ""
            if resp.status_code in BLOCK_CODES or final_host not in ALLOWED_HOSTS:
                reason = f"HTTP {resp.status_code} from {final_host} for {url}"
                print(f"  BLOCKED, stopping: {reason}")
                write_manual_list(todo[i:], reason)
                save_json(MANIFEST, manifest)
                return 3
            ctype = resp.headers.get("Content-Type", "")
            if resp.status_code != 200 or not resp.content.startswith(b"%PDF"):
                print(f"  not a PDF ({resp.status_code}, {ctype}): {url}")
                manifest[key] = {"url": url, "final_url": resp.url,
                                 "http_status": resp.status_code, "content_type": ctype,
                                 "fetched_at": now_utc(), "error": "not a PDF"}
                save_json(MANIFEST, manifest)
                time.sleep(PAUSE_SECONDS)
                continue
            dest.write_bytes(resp.content)
            entry = {"url": url, "final_url": resp.url, "http_status": resp.status_code,
                     "content_type": ctype, "fetched_at": now_utc(),
                     "fetched_by": "pipeline/fetch.py"}
            time.sleep(PAUSE_SECONDS)

        entry["bytes"] = dest.stat().st_size
        entry["sha256"] = sha256_file(dest)
        manifest[key] = entry
        save_json(MANIFEST, manifest)
        print(f"  ok {key} {entry['bytes']:>8} B  {url}")

    save_json(MANIFEST, manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
