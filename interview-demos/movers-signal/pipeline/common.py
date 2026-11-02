"""Shared helpers for the Movers Signal data pipeline.

Every script in this folder is plain Python 3 with no network access except
fetch.py and check_links.py. Paths are resolved from the project root so the
scripts can be run from anywhere:  python3 -I pipeline/<script>.py
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"
PDF_DIR = RAW / "pdf"  # original PDFs: local cache only, never committed
CONFIG = ROOT / "config"

# One honest identity for every request. No browser impersonation, no cookies.
USER_AGENT = "MoversSignal-research-prototype/0.1 (independent interview prototype; public filings only)"

# Hosts we fetch filing documents from. Anything else is refused.
ALLOWED_HOSTS = {
    "nsearchives.nseindia.com",
    "www.bseindia.com",
    "bseindia.com",
}

# Window for the dataset: the 90 days up to and including the snapshot date.
SNAPSHOT_DATE = "2026-11-02"
WINDOW_START = "2026-08-04"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def url_key(url: str) -> str:
    """Stable short key for a source URL (used for raw file names)."""
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


_TRANSLATE = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"',
    "–": "-", "—": "-", "‒": "-", "−": "-", "­": "",
    " ": " ", " ": " ", " ": " ", " ": " ", "​": "",
    "ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl",
}


def normalize(text: str) -> str:
    """Normalise text for quote matching: unicode NFKC, straight quotes,
    plain hyphens, collapsed whitespace, case-folded. Never used to *create*
    quotes, only to compare them."""
    text = unicodedata.normalize("NFKC", text)
    text = "".join(_TRANSLATE.get(c, c) for c in text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().casefold()


def word_count(text: str) -> int:
    return len([w for w in re.split(r"\s+", text.strip()) if w])


# Personal contact details are redacted from stored text (brief, rule 6).
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_RES = [
    # +91 mobile or landline with separators: +91 98765 43210, +91-22-6645 5555
    re.compile(r"\+\s?91[\s\-]*\(?\d{2,5}\)?[\s\-]*\d{3,5}[\s\-]*\d{3,5}(?:[\s\-]*\d{1,4})?"),
    # bare Indian mobile numbers: 10 digits starting 6-9, optional 0 prefix
    re.compile(r"(?<![\d/])0?[6-9]\d{4}[\s\-]?\d{5}(?![\d/])"),
    # landlines with STD code: 022-2659 8100, (022) 66455555, 0124 4567890
    re.compile(r"(?<![\d/])\(?0\d{2,4}\)?[\s\-]\d{3,4}[\s\-]?\d{3,5}(?![\d/])"),
]
# explicitly labelled numbers: "Tel: 2272 1234", "Phone No. 66455555", "Mob 98..."
LABELLED_PHONE_RE = re.compile(
    r"(?i)\b(tel|telephone|phone|ph|mob|mobile|fax|contact)(\s*(?:no\.?)?\s*[.:]?\s*)(\+?[\d][\d\s\-()+/]{6,}\d)"
)


def redact(text: str) -> tuple[str, int]:
    """Remove e-mail addresses and phone numbers. Returns (text, count)."""
    count = 0

    def _sub(pattern, repl, s):
        nonlocal count
        s2, n = pattern.subn(repl, s)
        count += n
        return s2

    text = _sub(EMAIL_RE, "[email redacted]", text)
    text = _sub(LABELLED_PHONE_RE, r"\1\2[phone redacted]", text)
    for p in PHONE_RES:
        text = _sub(p, "[phone redacted]", text)
    return text, count
