"""Print a filing's stored text compactly, page by page (developer aid).

Usage:  python3 -I pipeline/show.py KEY [first_page-last_page] [max_lines_per_page]
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # pipeline/ (own code only)

import re
import sys

from common import RAW


def main() -> int:
    key = sys.argv[1]
    lo, hi = 1, 9999
    if len(sys.argv) > 2 and "-" in sys.argv[2]:
        lo, hi = (int(x) for x in sys.argv[2].split("-"))
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    text = (RAW / f"{key}.txt").read_text(encoding="utf-8")
    body = text.split("\n\n", 1)[1]
    page, n = 0, 0
    for line in body.splitlines():
        m = re.match(r"=== PAGE (\d+) ===", line)
        if m:
            page, n = int(m.group(1)), 0
            if lo <= page <= hi:
                print(f"--- p{page}")
            continue
        if not (lo <= page <= hi) or not line.strip():
            continue
        n += 1
        if n <= cap:
            print(line.rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
