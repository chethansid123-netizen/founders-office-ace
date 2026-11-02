"""Apply reviewer corrections to pass 1 and write data/extracted_v2.json.

data/corrections.json lists every fix made after the verification pass, with
the field, the old and new evidence or value, the reason and the run that
found it. Pass 1 (extracted_v1.json) is never edited, so the audit trail
shows exactly what the verifier caught and what changed.

Usage:  python3 -I pipeline/apply_corrections.py
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # pipeline/ (own code only)

import copy
import sys

from common import DATA, load_json, now_utc, save_json


def main() -> int:
    records = load_json(DATA / "extracted_v1.json")
    corr = load_json(DATA / "corrections.json")
    by_id = {r["id"]: r for r in records}
    applied = []
    for c in corr["corrections"]:
        rec = by_id.get(c["id"])
        if rec is None:
            print(f"unknown record {c['id']}")
            return 1
        field = c["field"]
        entry = {"id": c["id"], "field": field, "reason": c["reason"], "found_by": c["found_by"]}
        if "set_evidence" in c:
            old = copy.deepcopy(rec["evidence"].get(field))
            rec["evidence"][field] = dict(c["set_evidence"])
            entry.update({"old_evidence": old, "new_evidence": c["set_evidence"]})
        if "set_value" in c:
            entry.update({"old_value": rec.get(field), "new_value": c["set_value"]})
            rec[field] = c["set_value"]
        rec.setdefault("corrections", []).append({k: entry[k] for k in ("field", "reason", "found_by")})
        applied.append(entry)
    save_json(DATA / "extracted_v2.json", records)
    save_json(DATA / "corrections_applied.json", {"applied_at": now_utc(), "count": len(applied), "items": applied})
    print(f"applied {len(applied)} correction(s) -> data/extracted_v2.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
