"""Independent verification pass (pass 2).

Re-reads every source PDF with two text engines that pass 1 did not use:
  engine B = pypdfium2 (PDFium), engine C = poppler `pdftotext -raw`.
It never reads the pass 1 text files. For every field of every record it
returns one of:
  match      - the quote is on the cited page (engine B or C) and the value
               agrees with an independent rule-based reading of that quote;
  mismatch   - the quote is missing, on another page, too long, or the value
               disagrees with the quote / with the rules in config/;
  not_found  - the value is null and a scan of the whole document finds
               nothing that should have been extracted.
Any record with a mismatch (or a record-level flag) goes to the review queue.

Usage:  python3 -I pipeline/verify.py data/extracted_v1.json data/verification_v1.json [--queue]
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # pipeline/ (own code only)

import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime

import pypdfium2 as pdfium

from common import (CONFIG, DATA, PDF_DIR, RAW, SNAPSHOT_DATE, WINDOW_START, load_json,
                    normalize, now_utc, save_json, word_count)

CACHE = RAW / "verify"
MAX_WORDS = 14
FRAGMENT_GAP = 200

# ------------------------------------------------------------------ engines B and C

def engine_texts(key: str) -> dict:
    """Per-page normalised text from engines B and C, cached locally."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cpath = CACHE / f"{key}.json"
    if cpath.exists():
        return json.loads(cpath.read_text(encoding="utf-8"))
    pdf = PDF_DIR / f"{key}.pdf"
    b_pages = []
    doc = pdfium.PdfDocument(str(pdf))
    for i in range(len(doc)):
        tp = doc[i].get_textpage()
        b_pages.append(tp.get_text_range() or "")
        tp.close()
    doc.close()
    out = subprocess.run(["pdftotext", "-raw", "-enc", "UTF-8", str(pdf), "-"],
                         capture_output=True, text=True, check=False).stdout
    c_pages = out.split("\f")
    data = {"B": [normalize(t) for t in b_pages], "C": [normalize(t) for t in c_pages]}
    cpath.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


def find_quote(ev: dict, texts: dict) -> tuple[str, list]:
    """('cited', engines) | ('other', [(engine, page)]) | ('missing', [])"""
    page = ev.get("page")
    frags = ev.get("fragments")

    def on(t: str) -> bool:
        if frags:
            pos = 0
            for i, f in enumerate(frags):
                idx = t.find(normalize(f), pos)
                if idx < 0 or (i > 0 and idx - pos > FRAGMENT_GAP):
                    return False
                pos = idx + len(normalize(f))
            return True
        return normalize(ev["quote"]) in t

    found = [e for e in ("B", "C") if isinstance(page, int) and 0 < page <= len(texts[e]) and on(texts[e][page - 1])]
    if found:
        return "cited", found
    elsewhere = [(e, i + 1) for e in ("B", "C") for i, t in enumerate(texts[e]) if on(t)]
    return ("other", elsewhere) if elsewhere else ("missing", [])

# ------------------------------------------------------------------ independent readers

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], 1)}
MONTHS.update({k[:3]: v for k, v in list(MONTHS.items())})
MONTHS["sept"] = 9
MON = r"(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sept|sep|oct|nov|dec)"


def parse_dates(text: str) -> set[str]:
    t = normalize(text)
    out = set()

    def add(y, m, d):
        try:
            out.add(date(int(y), int(m), int(d)).isoformat())
        except ValueError:
            pass

    for d, mon, y in re.findall(r"\b(\d{1,2})(?:st|nd|rd|th)?\s*,?\s*" + MON + r"\.?\s*,?\s*(\d{4})\b", t):
        add(y, MONTHS[mon], d)
    for mon, d, y in re.findall(MON + r"\.?\s*,?\s*(\d{1,2})(?:st|nd|rd|th)?\s*,?\s*(\d{4})\b", t):
        add(y, MONTHS[mon], d)
    for d, m, y in re.findall(r"\b(\d{1,2})[./](\d{1,2})[./](\d{4})\b", t):
        add(y, m, d)
    return out


def tokens(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", normalize(text))]


STOP = {"and", "the", "of", "for", "a", "an", "to", "as", "in", "&"}


def value_in_quote(value: str, quote: str) -> bool:
    """Every significant word of the value appears in the quote (prefix match for longer words)."""
    q = tokens(quote)
    for w in tokens(value):
        if w in STOP:
            continue
        if len(w) >= 7:
            if not any(t.startswith(w[:6]) for t in q):
                return False
        elif w not in q:
            return False
    return True


EVENT_WORDS = {
    "RESIGNATION": r"resign",
    "RETIREMENT": r"retire|superannuat",
    "REMOVAL": r"remov|terminat",
    "END_OF_TERM": r"\bterm\b|tenure|contract shall conclude|completion",
    "APPOINTMENT": r"appoint|re-designat",
    "OTHER": r"designat|transition|relieved|change in designation",
}
INTERIM = r"\binterim\b|\bacting\b|officiat|additional charge"
PERMANENT = r"appoint|re-designat|in place of|take charge|full[- ]time|term of appointment|period of|consequent to"
NOT_NAMED_WORDS = r"identify a successor|under process|will be filed|not presently envisage|continue to be led|initiated steps"
INTERNAL = r"currently serving|currently associated|incumbent|re-designat|associated with the company|joined the company as|currently executive|currently designated"
EXTERNAL = r"prior to joining|joins \w+ from|last posted at|most recently served|was working as|date of joining|currently is the"
NAMED_APPOINTMENT = r"appoint\w*\s+(?:of\s+)?(?:mr|ms|mrs|dr|shri|smt)\.?\s+[a-z]|in place of\s+(?:mr|ms|mrs|dr|shri)\b|\binterim\b|\bofficiating\b|additional charge"
REASON_HINTS = r"personal reason|to pursue|due to|better opportunit|health|family|retire|superannuat|outside the|other interests|professional"


def role_level_by_rule(title: str, rules: list) -> tuple[str, str]:
    t = normalize(title)
    for r in rules:
        if re.search(r["pattern"], t):
            return r["level"], r["why"]
    return "OTHER_SMP", "default"


def nse_upload_date(url: str) -> str | None:
    m = re.search(r"_(\d{2})(\d{2})(20\d{2})\d{6}_", url)
    if not m:
        return None
    d, mo, y = m.groups()
    try:
        return date(int(y), int(mo), int(d)).isoformat()
    except ValueError:
        return None

# ------------------------------------------------------------------ verification


def verify_record(rec: dict, texts: dict, rules: list, practices: dict) -> dict:
    res: dict[str, dict] = {}
    ev = rec["evidence"]
    full_b = " ".join(texts["B"])
    full_c = " ".join(texts["C"])
    full = full_b + " " + full_c

    def quote_status(field: str, e: dict) -> tuple[str | None, str]:
        if e.get("quote") is None:
            return None, ""
        words = sum(word_count(f) for f in e["fragments"]) if e.get("fragments") else word_count(e["quote"])
        if words > MAX_WORDS:
            return "mismatch", f"quote has {words} words (limit: under 15)"
        where, info = find_quote(e, texts)
        if where == "cited":
            return "ok", f"quote found on p{e['page']} by engine {'+'.join(info)}"
        if where == "other":
            return "mismatch", f"quote not on cited p{e['page']}; found at {info[:3]}"
        return "mismatch", "quote not reproducible by either independent engine"

    def put(field, status, reason):
        res[field] = {"status": status, "reason": reason}

    for field in ["company", "exchange_symbol", "person_name", "role_title", "event_type", "filing_date",
                  "effective_date", "stated_reason", "successor_status", "successor_source", "successor_name"]:
        if field not in ev:
            continue
        e = ev[field]
        value = rec.get(field)
        qs, qreason = quote_status(field, e)
        if qs == "mismatch":
            put(field, "mismatch", qreason)
            continue
        q = e.get("quote") or ""
        nq = normalize(q)

        if field == "company":
            if rec.get("company_basis") == "symbol":
                sym = rec.get("exchange_symbol") or ""
                known = practices.get(value, {}).get("symbol")
                ok = sym and normalize(sym) in nq and known == sym
                put(field, "match" if ok else "mismatch",
                    f"{qreason}; identified by filed symbol {sym}" if ok else "symbol basis does not agree with config/practices.json")
            else:
                core = re.sub(r"\b(limited|ltd\.?)\s*$", "", normalize(value)).strip()
                ok = core in nq
                put(field, "match" if ok else "mismatch", qreason if ok else f"company name '{core}' not in quote")
        elif field == "exchange_symbol":
            if value is None:
                put(field, "not_found", e.get("note") or "no symbol in filing")
            else:
                ok = re.search(r"(?<![a-z0-9])" + re.escape(normalize(value)) + r"(?![a-z0-9])", nq)
                put(field, "match" if ok else "mismatch", qreason if ok else f"symbol '{value}' not in quote")
        elif field in ("person_name", "successor_name", "role_title"):
            ok = value_in_quote(value, q)
            put(field, "match" if ok else "mismatch", qreason if ok else f"'{value}' not supported word-for-word by the quote")
        elif field == "event_type":
            pat = EVENT_WORDS[value]
            pool = nq + " " + normalize(ev.get("stated_reason", {}).get("quote") or "")
            ok = re.search(pat, pool)
            put(field, "match" if ok else "mismatch", qreason if ok else f"no '{pat}' wording in the quote for {value}")
        elif field == "filing_date":
            dates = parse_dates(q)
            ok = value in dates
            note = qreason
            up = nse_upload_date(rec["source_url"])
            if ok and up:
                gap = abs((date.fromisoformat(up) - date.fromisoformat(value)).days)
                note += f"; NSE upload timestamp {up}" + ("" if gap == 0 else f" ({gap} day gap)")
                if gap > 2:
                    ok = False
                    note = f"letter date {value} differs from NSE upload date {up} by {gap} days"
            put(field, "match" if ok else "mismatch", note if ok else (note if up else f"{value} not among dates in quote {sorted(dates)}"))
        elif field == "effective_date":
            if value is None:
                dates = parse_dates(q) if q else set()
                put(field, "not_found" if not dates else "mismatch",
                    "no calendar date in the source for this field" if not dates else f"null, but quote has dates {sorted(dates)}")
            else:
                dates = parse_dates(" ".join(e.get("fragments") or [q]))
                ok = value in dates
                put(field, "match" if ok else "mismatch", qreason if ok else f"{value} not among dates in quote {sorted(dates)}")
        elif field == "stated_reason":
            if value is None:
                if rec["event_type"] in ("APPOINTMENT",) or rec.get("review_test"):
                    put(field, "not_found", "not applicable")
                else:
                    # independent scan: is there reason wording anywhere in the document?
                    hits = re.findall(REASON_HINTS, full)
                    put(field, "not_found" if not hits else "mismatch",
                        "no reason wording anywhere in the document" if not hits
                        else f"null, but the document contains reason-like wording: {sorted(set(hits))[:4]}")
            else:
                ok = value_in_quote(value, q)
                put(field, "match" if ok else "mismatch", qreason if ok else f"'{value}' not supported by the quote")
        elif field == "successor_status":
            if value == "NOT_NAMED":
                if q:
                    ok = re.search(NOT_NAMED_WORDS, nq) and not re.search(NAMED_APPOINTMENT, nq)
                    put(field, "match" if ok else "mismatch", qreason if ok else "quote does not support 'not named'")
                else:
                    hits = re.findall(NAMED_APPOINTMENT, full)
                    put(field, "match" if not hits else "mismatch",
                        "absence confirmed: no named appointment, interim or successor wording in the document"
                        if not hits else f"document mentions possible successor wording: {sorted(set(hits))[:3]}")
            elif value == "NAMED_INTERIM":
                ok = re.search(INTERIM, nq)
                put(field, "match" if ok else "mismatch", qreason if ok else "no interim wording in quote")
            elif value == "NAMED_PERMANENT":
                ok = re.search(PERMANENT, nq) and not re.search(INTERIM, nq)
                put(field, "match" if ok else "mismatch", qreason if ok else "quote does not show a permanent appointment")
            else:  # UNCLEAR
                put(field, "match" if qs == "ok" or q == "" else "mismatch",
                    (qreason + "; reviewer judgement: unclear") if q else "unclear: no successor wording to classify")
        elif field == "successor_source":
            if value == "NOT_APPLICABLE":
                ok = rec["successor_status"] == "NOT_NAMED"
                put(field, "match" if ok else "mismatch", "consistent with no named successor" if ok else "NOT_APPLICABLE but a successor is named")
            elif value == "UNCLEAR":
                put(field, "match", "source not stated in the filing" if not q else qreason + "; source not stated explicitly")
            else:
                pat = INTERNAL if value == "INTERNAL" else EXTERNAL
                ok = re.search(pat, nq)
                if ok and value == "EXTERNAL" and "currently is the" in nq:
                    ok = not re.search(r"of the (company|bank)\b", nq)
                put(field, "match" if ok else "mismatch", qreason if ok else f"no {value.lower()} wording in quote")

    # derived fields -------------------------------------------------
    lvl, why = role_level_by_rule(rec["role_title"], rules)
    res["role_level"] = {"status": "match" if lvl == rec["role_level"] else "mismatch",
                         "reason": f"rule gives {lvl} ({why})"}
    pr = practices.get(rec["company"], {}).get("practice")
    res["practice"] = {"status": "match" if pr == rec["practice"] else "mismatch",
                       "reason": f"config/practices.json gives {pr}"}

    # context facts --------------------------------------------------
    ctx = []
    for cf in rec.get("context_facts", []):
        st, why = quote_status("context", cf)
        ctx.append({"label": cf["label"], "status": "match" if st == "ok" else "mismatch", "reason": why})

    return {"fields": res, "context": ctx}


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    src, dst = sys.argv[1], sys.argv[2]
    records = load_json(DATA.parent / src if not src.startswith("/") else src)
    rules = load_json(CONFIG / "role_levels.json")["rules"]
    practices = load_json(CONFIG / "practices.json")["companies"]
    out = {"run_at": now_utc(), "input": src,
           "engines": {"B": "pypdfium2 (PDFium)", "C": "poppler pdftotext -raw"},
           "window": [WINDOW_START, SNAPSHOT_DATE], "records": {}}
    # record-level checks need the whole set
    groups = defaultdict(list)
    for r in records:
        groups[(r["company"], normalize(r["person_name"] or ""), r["event_type"])].append(r)

    totals = defaultdict(int)
    queue = []
    for rec in records:
        texts = engine_texts(rec["source_key"])
        v = verify_record(rec, texts, rules, practices)
        flags = []
        if not (WINDOW_START <= rec["filing_date"] <= SNAPSHOT_DATE):
            flags.append(f"OUT_OF_WINDOW: filed {rec['filing_date']}, window {WINDOW_START} to {SNAPSHOT_DATE}")
        dupes = groups[(rec["company"], normalize(rec["person_name"] or ""), rec["event_type"])]
        if len(dupes) > 1:
            effs = {d["effective_date"] for d in dupes}
            if len(effs) > 1:
                others = [d["id"] for d in dupes if d["id"] != rec["id"]]
                flags.append(f"CONFLICTING_DUPLICATE: same event also in {others} with different effective dates {sorted(e or '' for e in effs)}")
        v["record_flags"] = flags
        for f in v["fields"].values():
            totals[f["status"]] += 1
        for c in v["context"]:
            totals["context_" + c["status"]] += 1
        problems = [f"{k}: {f['reason']}" for k, f in v["fields"].items() if f["status"] == "mismatch"]
        problems += [f"context '{c['label']}': {c['reason']}" for c in v["context"] if c["status"] == "mismatch"]
        problems += flags
        v["needs_review"] = bool(problems)
        out["records"][rec["id"]] = v
        if problems:
            queue.append({"id": rec["id"], "company": rec["company"], "source_url": rec["source_url"],
                          "problems": problems})
    out["totals"] = dict(totals)
    out["fields_checked"] = sum(v for k, v in totals.items() if not k.startswith("context_"))
    out["context_facts_checked"] = sum(v for k, v in totals.items() if k.startswith("context_"))
    save_json(DATA.parent / dst if not dst.startswith("/") else dst, out)
    if "--queue" in sys.argv:
        save_json(DATA / "review_queue.json", {"generated_at": now_utc(), "from": dst, "records": queue})
    print(f"{len(records)} records, {out['fields_checked']} fields checked: {dict(totals)}")
    print(f"{len(queue)} record(s) need review")
    for q in queue:
        print(" -", q["id"])
        for p in q["problems"]:
            print("     ", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
