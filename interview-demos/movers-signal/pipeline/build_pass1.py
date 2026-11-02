"""Build data/extracted_v1.json from the pass 1 record modules.

Adds source_url from the raw manifest, resolves page 'auto' by searching the
engine A page text, and runs the extractor's own self-checks:
  * every quote is under 15 words;
  * every quote occurs (after normalisation) on the page it cites.
A failed self-check stops the build: pass 1 must be internally consistent
before the independent verification pass (verify.py) ever runs.

Usage:  python3 -I pipeline/build_pass1.py
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # pipeline/ (own code only)

import re
import sys

from common import DATA, RAW, load_json, normalize, now_utc, save_json, word_count

MAX_WORDS = 14  # "under 15 words"
FRAGMENT_GAP = 200  # max characters between consecutive table-cell fragments


def fragments_on_page(fragments: list[str], page_text: str) -> bool:
    """True if every fragment occurs in order, each within FRAGMENT_GAP chars of the last."""
    pos = 0
    for i, frag in enumerate(fragments):
        idx = page_text.find(normalize(frag), pos)
        if idx < 0 or (i > 0 and idx - pos > FRAGMENT_GAP):
            return False
        pos = idx + len(normalize(frag))
    return True


def load_pages(key: str) -> dict[int, str]:
    path = RAW / f"{key}.txt"
    if not path.exists():
        path = RAW / "screened" / f"{key}.txt"
    text = path.read_text(encoding="utf-8").split("\n\n", 1)[1]
    pages: dict[int, list[str]] = {}
    page = 0
    for line in text.splitlines():
        m = re.match(r"=== PAGE (\d+) ===", line)
        if m:
            page = int(m.group(1))
            pages[page] = []
            continue
        pages.setdefault(page, []).append(line)
    return {p: normalize("\n".join(lines)) for p, lines in pages.items()}


def main() -> int:
    from pass1_records_a import RECORDS as A
    from pass1_records_b import RECORDS as B
    try:
        from pass1_records_c import RECORDS as Cc
    except ImportError:
        Cc = []
    records = A + B + Cc
    manifest = load_json(RAW / "manifest.json", {})
    problems, log = [], []
    ids = set()
    for rec in records:
        rid = rec["id"]
        if rid in ids:
            problems.append(f"{rid}: duplicate id")
        ids.add(rid)
        entry = manifest.get(rec["source_key"])
        if not entry or entry.get("error"):
            problems.append(f"{rid}: no usable source document for key {rec['source_key']}")
            continue
        rec["source_url"] = entry["url"]
        rec["source_sha256"] = entry["sha256"]
        pages = load_pages(rec["source_key"])

        def check(label: str, ev: dict, key: str = rec["source_key"], pages=pages):
            q = ev.get("quote")
            if q is None:
                return
            if ev.get("fragments"):
                words = sum(word_count(f) for f in ev["fragments"])
                if words > MAX_WORDS:
                    problems.append(f"{rid}.{label}: fragments have {words} words (max {MAX_WORDS})")
                if not fragments_on_page(ev["fragments"], pages.get(ev.get("page"), "")):
                    problems.append(f"{rid}.{label}: fragments not found in order on page {ev.get('page')}")
                return
            if word_count(q) > MAX_WORDS:
                problems.append(f"{rid}.{label}: quote has {word_count(q)} words (max {MAX_WORDS})")
            nq = normalize(q)
            if ev.get("page") == "auto":
                hits = [p for p, t in sorted(pages.items()) if nq in t]
                if not hits:
                    problems.append(f"{rid}.{label}: 'auto' quote not found anywhere: {q!r}")
                    return
                ev["page"] = hits[0]
                log.append({"record": rid, "field": label, "resolved_page": hits[0], "all_pages": hits})
            p = ev.get("page")
            if nq not in pages.get(p, ""):
                problems.append(f"{rid}.{label}: quote not on page {p}: {q!r}")

        for field, ev in rec["evidence"].items():
            check(field, ev)
        for i, cf in enumerate(rec.get("context_facts", [])):
            check(f"context[{i}]", cf)
        rec["extraction"] = {"pass": 1, "method": "read of page text (engine A: pdfplumber)",
                             "built_at": now_utc()}

    if problems:
        print(f"{len(problems)} self-check problem(s):")
        for p in problems:
            print("  -", p)
        return 1
    save_json(DATA / "extracted_v1.json", records)
    save_json(DATA / "pass1_log.json", {"built_at": now_utc(), "auto_pages": log})
    print(f"wrote data/extracted_v1.json: {len(records)} records from "
          f"{len({r['source_key'] for r in records})} filings; {len(log)} 'auto' page(s) resolved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
