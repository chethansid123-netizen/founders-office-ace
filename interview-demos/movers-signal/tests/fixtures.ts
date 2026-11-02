import scoreJson from "@/config/score.json";
import type { ScoreConfig } from "@/lib/score";
import type { SeatRecord } from "@/lib/types";

export const CONFIG = scoreJson as unknown as ScoreConfig;
export const AS_OF = "2026-11-02";

let n = 0;
export function seat(over: Partial<SeatRecord> = {}): SeatRecord {
  n += 1;
  return {
    id: `fixture-${n}`,
    company: "Alpha Limited",
    exchange_symbol: "ALPHA",
    practice: "Financial Services",
    person_name: "Test Person",
    role_title: "Chief Financial Officer",
    role_level: "CXO",
    event_type: "RESIGNATION",
    filing_date: "2026-10-01",
    effective_date: "2026-11-02",
    stated_reason: null,
    successor_status: "NOT_NAMED",
    successor_source: "NOT_APPLICABLE",
    source_url: "https://nsearchives.nseindia.com/corporate/TEST.pdf",
    source_page: 1,
    evidence: {},
    review_status: "VERIFIED",
    review_note: null,
    source_key: `key${n}`,
    successor_name: null,
    effective_date_note: null,
    company_basis: "text",
    context_facts: [],
    ...over,
  };
}
