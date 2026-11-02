"""Append leads (candidate filing URLs) to data/leads.json, de-duplicated.

A lead is only a pointer to a document. Nothing about a lead is treated as a
fact until the PDF itself has been read.

Usage:  python3 -I pipeline/add_leads.py "<found_via>" URL [URL ...]
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # pipeline/ (own code only)

import sys

from common import DATA, load_json, now_utc, save_json, url_key

LEADS = DATA / "leads.json"


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    found_via = sys.argv[1]
    leads = load_json(LEADS, [])
    seen = {l["url"] for l in leads}
    added = 0
    for url in sys.argv[2:]:
        url = url.strip()
        if url.startswith("https://bseindia.com/"):
            url = "https://www.bseindia.com/" + url[len("https://bseindia.com/"):]
        if not url or url in seen:
            continue
        leads.append({"key": url_key(url), "url": url, "found_via": found_via, "added_at": now_utc()})
        seen.add(url)
        added += 1
    save_json(LEADS, leads)
    print(f"added {added}, total {len(leads)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
