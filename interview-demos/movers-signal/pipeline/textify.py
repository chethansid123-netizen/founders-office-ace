"""Extract page-marked text from each downloaded PDF (extraction engine A).

Engine A is pdfplumber. The verification pass (verify.py) deliberately uses
different engines (pypdfium2 and poppler pdftotext) so the second pass is an
independent re-read of the source, not a re-check of our own text.

Output: data/raw/<key>.txt with a header and "=== PAGE n ===" markers.
Personal e-mail addresses and phone numbers are redacted before saving.

Usage:  python3 -I pipeline/textify.py
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # pipeline/ (own code only)

import sys

import pdfplumber

from common import PDF_DIR, RAW, load_json, redact, save_json

MANIFEST = RAW / "manifest.json"
MIN_CHARS_FOR_TEXT_LAYER = 40


def main() -> int:
    manifest = load_json(MANIFEST, {})
    changed = 0
    for key, entry in manifest.items():
        pdf = PDF_DIR / f"{key}.pdf"
        out = RAW / f"{key}.txt"
        if (RAW / "screened" / f"{key}.txt").exists():  # screened-out texts live apart
            out = RAW / "screened" / f"{key}.txt"
        if not pdf.exists() or entry.get("error"):
            continue
        if out.exists() and entry.get("text_sha256") == entry.get("sha256"):
            continue
        pages_out, page_chars, redactions = [], [], 0
        engine = "pdfplumber (engine A)"
        try:
            raw_pages = []
            with pdfplumber.open(pdf) as doc:
                for page in doc.pages:
                    raw_pages.append(page.extract_text() or "")
        except Exception as exc:  # malformed PDF: fall back, and say so
            import pypdfium2 as pdfium
            print(f"  pdfplumber failed on {key} ({exc}); falling back to pypdfium2")
            engine = "pypdfium2 (fallback: pdfplumber could not parse this file)"
            raw_pages = []
            try:
                doc = pdfium.PdfDocument(str(pdf))
                for i in range(len(doc)):
                    tp = doc[i].get_textpage()
                    raw_pages.append(tp.get_text_range() or "")
                    tp.close()
                doc.close()
            except Exception as exc2:
                print(f"  {key}: no engine can parse this PDF ({exc2}); marked unreadable")
                entry["error"] = "unreadable PDF (both text engines failed)"
                save_json(MANIFEST, manifest)
                continue
        for n, text in enumerate(raw_pages, start=1):
            text, r = redact(text)
            redactions += r
            page_chars.append(len(text.strip()))
            pages_out.append(f"=== PAGE {n} ===\n{text.strip()}\n")
        entry["engine_a"] = engine
        header = (
            f"SOURCE_URL: {entry['url']}\n"
            f"SHA256: {entry['sha256']}\n"
            f"FETCHED_AT: {entry['fetched_at']}\n"
            f"PAGES: {len(pages_out)}\n"
            f"ENGINE: {engine}\n"
            f"REDACTIONS: {redactions} (personal e-mail addresses and phone numbers)\n\n"
        )
        out.write_text(header + "\n".join(pages_out), encoding="utf-8")
        entry["pages"] = len(pages_out)
        entry["page_chars"] = page_chars
        entry["text_layer"] = all(c >= MIN_CHARS_FOR_TEXT_LAYER for c in page_chars[:1]) and sum(page_chars) > 200
        entry["redactions"] = redactions
        entry["text_sha256"] = entry["sha256"]
        changed += 1
        save_json(MANIFEST, manifest)
    save_json(MANIFEST, manifest)
    print(f"text extracted for {changed} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
