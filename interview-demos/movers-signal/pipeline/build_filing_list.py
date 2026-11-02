"""Render data/filing_list.md from data/shortlist.json and the raw manifest.

Usage:  python3 -I pipeline/build_filing_list.py
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # pipeline/ (own code only)

import sys
from collections import Counter

from common import DATA, RAW, load_json


def main() -> int:
    sl = load_json(DATA / "shortlist.json")
    manifest = load_json(RAW / "manifest.json", {})
    leads = {l["key"]: l for l in load_json(DATA / "leads.json", [])}

    def url(k):
        return manifest.get(k, {}).get("url") or leads.get(k, {}).get("url", "")

    out = []
    out.append("# Movers Signal: filing list")
    out.append("")
    out.append(f"Snapshot {sl['snapshot_date']}. Window: filings dated {sl['window'][0]} to {sl['window'][1]} (90 days).")
    out.append("")
    out.append("This is the discovery list, written before extraction. The one-line descriptions are")
    out.append("pointers from triage, **not facts**. Every fact shown on the site comes from the filing")
    out.append("PDF itself, with page and quote, after the verification pass and the review step.")
    out.append("")
    out.append("How filings were found: NSE's public announcements RSS feed (2 Nov 2026) and web search")
    out.append("restricted to `nsearchives.nseindia.com` and `bseindia.com`. Every PDF was then fetched")
    out.append("directly from the exchange archive with an honest user agent. No request was blocked.")
    out.append("")

    ex = sl["extract"]
    by_practice = Counter(e["practice"] for e in ex)
    out.append(f"## 1. Filings to extract ({len(ex)})")
    out.append("")
    out.append("| Practice | Filings |")
    out.append("|---|---|")
    for p, n in sorted(by_practice.items()):
        out.append(f"| {p} | {n} |")
    out.append("")
    out.append("| # | Company | Practice (proposed) | Lead (unverified) | Source |")
    out.append("|---|---|---|---|---|")
    for i, e in enumerate(ex, 1):
        out.append(f"| {i} | {e['company']} | {e['practice']} | {e['lead']} | [PDF]({url(e['key'])}) |")
    out.append("")

    rt = sl["extract_for_review_test"]
    out.append(f"## 2. Extracted but expected to fail review ({len(rt)})")
    out.append("")
    out.append("These go through the same extraction and verification. They test whether the review")
    out.append("step catches superseded filings, filings outside the window, no-change designations and")
    out.append("unreliable text.")
    out.append("")
    out.append("| Company | Why it is a test | Source |")
    out.append("|---|---|---|")
    for e in rt:
        out.append(f"| {e['company']} | {e['lead']} | [PDF]({url(e['key'])}) |")
    out.append("")

    seen = set()
    so = []
    for e in sl["screened_out"]:
        if e["key"] in seen:
            continue
        seen.add(e["key"])
        so.append(e)
    out.append(f"## 3. Screened out before extraction ({len(so)})")
    out.append("")
    out.append("Selection rule when more valid filings existed than the 50-filing sample allows:")
    out.append("C-suite and business heads first, then larger companies, then practice balance.")
    out.append("")
    out.append("| Company | Reason | Source |")
    out.append("|---|---|---|")
    for e in so:
        out.append(f"| {e['company']} | {e['reason']} | [PDF]({url(e['key'])}) |")
    out.append("")

    pe = sl["practice_evidence"]
    out.append("## 4. Supporting filings for the Private Equity label")
    out.append("")
    out.append("| Company | Use | Source |")
    out.append("|---|---|---|")
    for e in pe:
        out.append(f"| {e['company']} | {e['use']} | [PDF]({url(e['key'])}) |")
    out.append("")
    (DATA / "filing_list.md").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote data/filing_list.md: {len(ex)} to extract, {len(rt)} review tests, {len(so)} screened out")
    return 0


if __name__ == "__main__":
    sys.exit(main())
