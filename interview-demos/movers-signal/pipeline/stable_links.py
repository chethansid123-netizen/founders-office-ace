"""Find permanent addresses for BSE filings linked from BSE's temporary path.

BSE serves a new attachment under /AttachLive/ and later moves it to
/AttachHis/; after the move the AttachLive link returns 404. For every
verified seat whose source is an AttachLive URL, this script asks once for the
AttachHis copy and accepts it only if it is byte-identical to the document
that was extracted and verified (same SHA-256). Nothing about the record
changes except that the site can link to the address that will keep working.

Same polite rules as fetch.py: honest User-Agent, one request at a time with a
pause, and a block (401/403/407/429/451) stops the run without a retry.

Usage:  python3 -I pipeline/stable_links.py      then  python3 -I pipeline/apply_review.py
Output: data/stable_links.json
"""

from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import requests  # noqa: E402

from common import DATA, USER_AGENT, load_json, now_utc, save_json  # noqa: E402

PAUSE_SECONDS = 2.5
BLOCK_CODES = {401, 403, 407, 429, 451}
OUT = DATA / "stable_links.json"


def main() -> int:
    records = load_json(DATA / "records.json")["records"]
    previous = load_json(OUT, {"links": {}})
    todo = {}
    for r in records:
        if r["review_status"] == "VERIFIED" and "/AttachLive/" in r["source_url"]:
            todo[r["source_url"]] = r["source_sha256"]

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/pdf"})
    links = dict(previous.get("links", {}))
    pending = []
    for i, (url, sha) in enumerate(sorted(todo.items())):
        if url in links:
            continue
        stable = url.replace("/AttachLive/", "/AttachHis/")
        try:
            resp = session.get(stable, timeout=60)
        except requests.RequestException as exc:
            print(f"  network error, stopping: {exc}")
            pending.extend(u for u in todo if u not in links)
            break
        if resp.status_code in BLOCK_CODES:
            print(f"  HTTP {resp.status_code}: stopping without retrying")
            pending.extend(u for u in todo if u not in links)
            break
        got = hashlib.sha256(resp.content).hexdigest() if resp.status_code == 200 else None
        if got == sha:
            links[url] = {"stable_url": stable, "sha256": sha, "same_sha256": True, "checked_at": now_utc()}
            print(f"  stable copy, identical: {stable}")
        else:
            pending.append(url)
            print(f"  no identical stable copy yet (HTTP {resp.status_code}): {stable}")
        if i < len(todo) - 1:
            time.sleep(PAUSE_SECONDS)

    save_json(OUT, {"checked_at": now_utc(), "links": links, "pending": sorted(set(pending))})
    print(f"{len(links)} stable, {len(set(pending))} pending -> data/stable_links.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
