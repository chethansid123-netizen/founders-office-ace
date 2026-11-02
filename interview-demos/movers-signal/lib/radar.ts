import { EVENT_LABEL, exchangeOf, formatDate, SOURCE_LABEL, sourceHref, SUCCESSOR_LABEL } from "./format";
import type { Filterable } from "./filters";
import type { ScoredSeat } from "./score";

/**
 * One Radar row: only what the ranked table shows. The page sends these rows to
 * the browser instead of full records, so evidence quotes, review notes and
 * hashes never ship in client JavaScript.
 */
export interface RadarRow extends Filterable {
  id: string;
  rank: number;
  company: string;
  exchange: string;
  symbol: string | null;
  person: string | null;
  role_title: string;
  event_label: string;
  effective_date: string | null;
  effective_label: string;
  status: string;
  successor_detail: string;
  seat_filled: boolean;
  total: number;
  source_url: string;
  source_page: number | null;
}

/** The successor line under the status chip: the filed classification, plus the source when one is stated. */
export function successorDetail(s: ScoredSeat["seat"]): string {
  const base = SUCCESSOR_LABEL[s.successor_status];
  if (s.successor_status === "NAMED_PERMANENT" && (s.successor_source === "INTERNAL" || s.successor_source === "EXTERNAL")) {
    return `${base} · ${SOURCE_LABEL[s.successor_source].toLowerCase()}`;
  }
  return base;
}

export function toRadarRow(s: ScoredSeat, rank: number): RadarRow {
  const seat = s.seat;
  return {
    id: seat.id,
    rank,
    company: seat.company,
    exchange: exchangeOf(seat.source_url),
    symbol: seat.exchange_symbol,
    person: seat.person_name,
    role_title: seat.role_title,
    practice: seat.practice,
    role_level: seat.role_level,
    event_type: seat.event_type,
    successor_status: seat.successor_status,
    event_label: EVENT_LABEL[seat.event_type],
    effective_date: seat.effective_date,
    effective_label: formatDate(seat.effective_date),
    status: s.status,
    successor_detail: successorDetail(seat),
    seat_filled: s.seatFilled,
    total: s.total,
    source_url: sourceHref(seat),
    source_page: seat.source_page,
  };
}
