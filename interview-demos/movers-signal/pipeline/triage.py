"""Print a quick triage view of downloaded filings (developer aid, no output files).

For each text file: the letter date line, subject line and every line that
mentions a leadership event word. Used to decide which leads are worth a full
read. Nothing printed here is used as a fact; facts are taken only from a full
read of the page, and then checked by verify.py.

Usage:  python3 -I pipeline/triage.py [key ...]
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # pipeline/ (own code only)

import re
import sys

from common import RAW, load_json

EVENT = re.compile(
    r"(resign|cessation|ceas|appoint|retire|superannuat|w\.?e\.?f|effective|interim|officiat|"
    r"additional charge|chief|officer|president|head|managing director|\bCEO\b|\bCFO\b|\bCOO\b|\bCTO\b|"
    r"\bCHRO\b|\bCMO\b|\bCIO\b|senior management|key managerial|\bSMP\b|\bKMP\b|successor|in place of|"
    r"term|tenure|last working|relieve)",
    re.I,
)


def main() -> int:
    manifest = load_json(RAW / "manifest.json", {})
    keys = sys.argv[1:] or list(manifest.keys())
    for key in keys:
        e = manifest.get(key, {})
        p = RAW / f"{key}.txt"
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        body = text.split("\n\n", 1)[1] if "\n\n" in text else text
        print("#" * 100)
        print(key, e.get("url", "")[-90:], "pages", e.get("pages"))
        page = 0
        shown = 0
        for line in body.splitlines():
            m = re.match(r"=== PAGE (\d+) ===", line)
            if m:
                page = int(m.group(1))
                continue
            s = line.strip()
            if not s:
                continue
            if page == 1 and shown < 6 and re.search(r"(20\d\d|sub|ref)", s, re.I):
                print(f"  p{page}| {s[:160]}")
                shown += 1
                continue
            if EVENT.search(s) and len(s) > 25:
                print(f"  p{page}: {s[:200]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
