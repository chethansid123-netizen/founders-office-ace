"""Helpers for the first extraction pass (pass 1).

Pass 1 is a careful human-style read of each filing's page text (engine A,
pdfplumber). Every field is written with the exact supporting quote (under 15
words) and the page it sits on. Nothing here is inferred from outside the
filing: when the filing does not state something, the value is None and the
evidence says so.

pass1_records_a.py and pass1_records_b.py hold the records; build_pass1.py
turns them into data/extracted_v1.json.
"""

from __future__ import annotations

FIELDS = [
    "company", "exchange_symbol", "person_name", "role_title", "event_type",
    "filing_date", "effective_date", "stated_reason", "successor_status",
    "successor_source",
]

ROLE_LEVELS = {"CEO_MD", "CXO", "BUSINESS_HEAD", "FUNCTION_HEAD", "OTHER_SMP"}
EVENT_TYPES = {"RESIGNATION", "RETIREMENT", "REMOVAL", "END_OF_TERM", "APPOINTMENT", "OTHER"}
SUCCESSOR_STATUS = {"NAMED_PERMANENT", "NAMED_INTERIM", "NOT_NAMED", "UNCLEAR"}
SUCCESSOR_SOURCE = {"INTERNAL", "EXTERNAL", "UNCLEAR", "NOT_APPLICABLE"}


def E(quote: str, page, note: str | None = None) -> dict:
    """Evidence: an exact quote from the filing and its page ('auto' = locate)."""
    d = {"quote": quote, "page": page}
    if note:
        d["note"] = note
    return d


def EF(fragments: list[str], page, note: str) -> dict:
    """Evidence from a table cell that wraps around a neighbouring column.

    Each fragment must appear verbatim, in order, within 200 characters of the
    previous one on the cited page. Displayed joined with ' … '.
    """
    return {"quote": " … ".join(fragments), "fragments": fragments, "page": page, "note": note}


def ABSENT(note: str) -> dict:
    """Evidence for a field the filing does not state (value must be None)."""
    return {"quote": None, "page": None, "note": note}


def C(label: str, value: str, quote: str, page) -> dict:
    """A context fact: an extra filed fact shown in the seat brief."""
    return {"label": label, "value": value, "quote": quote, "page": page}


def R(*, id, key, company, symbol, practice, person, role_title, role_level,
      event, filed, effective, reason, succ_status, succ_source, page, ev,
      successor_name=None, effective_note=None, company_basis="text",
      context=None, extraction_note=None, review_test=None) -> dict:
    assert role_level in ROLE_LEVELS, (id, role_level)
    assert event in EVENT_TYPES, (id, event)
    assert succ_status in SUCCESSOR_STATUS, (id, succ_status)
    assert succ_source in SUCCESSOR_SOURCE, (id, succ_source)
    missing = [f for f in FIELDS if f not in ev]
    assert not missing, (id, "evidence missing for", missing)
    if successor_name is not None:
        assert "successor_name" in ev, (id, "successor_name needs evidence")
    return {
        "id": id,
        "company": company,
        "exchange_symbol": symbol,
        "practice": practice,
        "person_name": person,
        "role_title": role_title,
        "role_level": role_level,
        "event_type": event,
        "filing_date": filed,
        "effective_date": effective,
        "stated_reason": reason,
        "successor_status": succ_status,
        "successor_source": succ_source,
        "source_url": None,  # filled from the raw manifest by build_pass1.py
        "source_page": page,
        "evidence": ev,
        "review_status": "UNREVIEWED",
        "review_note": None,
        # extensions (documented in README): not part of the brief's base schema
        "source_key": key,
        "successor_name": successor_name,
        "effective_date_note": effective_note,
        "company_basis": company_basis,
        "context_facts": context or [],
        "extraction_note": extraction_note,
        "review_test": review_test,
    }
