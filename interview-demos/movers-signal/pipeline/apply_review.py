"""Merge review decisions into the final dataset: data/records.json.

Decision sources, in order of precedence:
  1. data/review_decisions_human.json  (exported from review.html by a person)
  2. data/review_decisions_ai.json     (the AI second reader)

Guard: a record can only be VERIFIED if every mismatch and every record flag
left by the latest verification run (verification_v2.json) is covered by a
written override in the decision. Otherwise it stays UNREVIEWED.
The site reads data/records.json and shows only VERIFIED records.

Also adds `source_url_stable` where data/stable_links.json holds a
byte-identical permanent copy of a BSE document (see stable_links.py).

Usage:  python3 -I pipeline/apply_review.py [--require-human]
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # pipeline/ (own code only)

import sys

from common import DATA, load_json, now_utc, save_json


def main() -> int:
    require_human = "--require-human" in sys.argv
    records = load_json(DATA / "extracted_v2.json")
    ver = load_json(DATA / "verification_v2.json")["records"]
    ai = load_json(DATA / "review_decisions_ai.json")
    human = load_json(DATA / "review_decisions_human.json", None)
    ai_by = {d["id"]: d for d in ai["decisions"]}
    hu_by = {d["id"]: d for d in (human or {}).get("decisions", [])}

    # Permanent BSE addresses for documents first fetched from the temporary
    # AttachLive path; accepted only when byte-identical (pipeline/stable_links.py).
    stable = load_json(DATA / "stable_links.json", {"links": {}})["links"]

    out, blocked = [], []
    for rec in records:
        rid = rec["id"]
        v = ver[rid]
        d, who, when = None, None, None
        if rid in hu_by:
            d, who, when = hu_by[rid], human.get("reviewer", "Human reviewer"), human.get("reviewed_at")
        elif rid in ai_by and not require_human:
            d, who, when = ai_by[rid], ai["reviewer"], ai["reviewed_at"]

        status, note = "UNREVIEWED", None
        if d:
            status, note = d["decision"], d.get("note")
            if status == "VERIFIED":
                covered = {o["field"] for o in d.get("overrides", [])}
                open_items = [k for k, f in v["fields"].items() if f["status"] == "mismatch" and k not in covered]
                open_items += [f for f in v.get("record_flags", []) if f.split(":")[0] not in covered]
                if open_items:
                    status = "UNREVIEWED"
                    note = f"Blocked: unresolved verification items {open_items}"
                    blocked.append(rid)
        rec = dict(rec)
        rec["review_status"] = status
        rec["review_note"] = note
        rec["reviewed_by"] = who if d else None
        rec["reviewed_at"] = when if d else None
        rec["review_overrides"] = (d or {}).get("overrides", [])
        link = stable.get(rec["source_url"])
        if link and link.get("same_sha256") and link.get("sha256") == rec.get("source_sha256"):
            rec["source_url_stable"] = link["stable_url"]
        rec["verification"] = {
            "run": "verification_v2",
            "fields": {k: f["status"] for k, f in v["fields"].items()},
            "reasons": {k: f["reason"] for k, f in v["fields"].items()},
            "context": [c["status"] for c in v["context"]],
            "record_flags": v.get("record_flags", []),
        }
        out.append(rec)

    save_json(DATA / "records.json", {
        "generated_at": now_utc(),
        "as_of": "2026-11-02",
        "human_signoff": bool(human),
        "records": out,
    })
    counts = {s: sum(r["review_status"] == s for r in out) for s in ("VERIFIED", "REJECTED", "UNREVIEWED")}
    print(f"data/records.json: {counts}; human decisions: {len(hu_by)}; blocked by guard: {blocked}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
