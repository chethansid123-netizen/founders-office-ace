import { EVENT_LABEL, formatDate, SOURCE_LABEL, SUCCESSOR_LABEL } from "./format";
import type { Evidence, SeatRecord } from "./types";

export type FieldKey =
  | "company" | "exchange_symbol" | "person_name" | "role_title" | "event_type" | "filing_date"
  | "effective_date" | "stated_reason" | "successor_status" | "successor_source" | "successor_name";

/** The filed facts of a seat brief, in display order. */
export const FIELDS: { key: FieldKey; label: string }[] = [
  { key: "company", label: "Company" },
  { key: "exchange_symbol", label: "Exchange symbol" },
  { key: "person_name", label: "Person" },
  { key: "role_title", label: "Role title" },
  { key: "event_type", label: "Event" },
  { key: "filing_date", label: "Filing date" },
  { key: "effective_date", label: "Effective date" },
  { key: "stated_reason", label: "Stated reason" },
  { key: "successor_status", label: "Successor status" },
  { key: "successor_source", label: "Successor source" },
  { key: "successor_name", label: "Successor" },
];

/** A field's display value, or null when the filing does not state it. */
export function displayValue(seat: SeatRecord, key: FieldKey): string | null {
  const v = seat[key];
  if (v === null || v === undefined) return null;
  switch (key) {
    case "event_type": return EVENT_LABEL[seat.event_type];
    case "filing_date": return formatDate(seat.filing_date);
    case "effective_date": return formatDate(seat.effective_date) + (seat.effective_date_note ? ` (${seat.effective_date_note})` : "");
    case "stated_reason": return `“${seat.stated_reason}”`;
    case "successor_status": return SUCCESSOR_LABEL[seat.successor_status];
    case "successor_source": return SOURCE_LABEL[seat.successor_source];
    default: return String(v);
  }
}

export interface FactRow {
  key: FieldKey;
  label: string;
  value: string | null;
  evidence: Evidence | null;
}

/** Rows for the Filed facts section. The successor row appears only when a successor is named. */
export function factRows(seat: SeatRecord): FactRow[] {
  return FIELDS.filter((f) => f.key !== "successor_name" || seat.successor_name).map((f) => ({
    key: f.key,
    label: f.label,
    value: displayValue(seat, f.key),
    evidence: seat.evidence[f.key] ?? null,
  }));
}
