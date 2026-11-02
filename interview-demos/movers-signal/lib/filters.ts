import type { EventType, RoleLevel, SeatRecord, SuccessorStatus } from "./types";

export const ALL = "all";

export interface Filters {
  practice: string;
  roleLevel: string;
  eventType: string;
  successorStatus: string;
}

export const NO_FILTERS: Filters = { practice: ALL, roleLevel: ALL, eventType: ALL, successorStatus: ALL };

export const ROLE_LEVEL_ORDER: RoleLevel[] = ["CEO_MD", "CXO", "BUSINESS_HEAD", "FUNCTION_HEAD", "OTHER_SMP"];
export const EVENT_ORDER: EventType[] = ["RESIGNATION", "RETIREMENT", "REMOVAL", "END_OF_TERM", "APPOINTMENT", "OTHER"];
export const SUCCESSOR_ORDER: SuccessorStatus[] = ["NOT_NAMED", "NAMED_INTERIM", "UNCLEAR", "NAMED_PERMANENT"];
export const PRACTICE_ORDER = [
  "Financial Services",
  "Telecom",
  "Digital",
  "Private Equity",
  "Consumer Products & Retail",
  "Information Technology",
  "Healthcare & Life Sciences",
  "Industrial & Infrastructure",
];

export function matches(seat: SeatRecord, f: Filters): boolean {
  return (
    (f.practice === ALL || seat.practice === f.practice) &&
    (f.roleLevel === ALL || seat.role_level === f.roleLevel) &&
    (f.eventType === ALL || seat.event_type === f.eventType) &&
    (f.successorStatus === ALL || seat.successor_status === f.successorStatus)
  );
}

/** Pure filter. Works on bare records or on anything carrying a `seat`. */
export function applyFilters<T extends SeatRecord | { seat: SeatRecord }>(items: T[], f: Filters): T[] {
  return items.filter((it) => matches("seat" in it ? it.seat : (it as SeatRecord), f));
}

export interface Option {
  value: string;
  count: number;
}

/** Filter options in canonical order, with the count of seats for each value. */
export function filterOptions(seats: SeatRecord[]): {
  practice: Option[];
  roleLevel: Option[];
  eventType: Option[];
  successorStatus: Option[];
} {
  const count = (vals: string[], key: (s: SeatRecord) => string): Option[] =>
    vals.map((v) => ({ value: v, count: seats.filter((s) => key(s) === v).length }));
  return {
    practice: count(PRACTICE_ORDER, (s) => s.practice),
    roleLevel: count(ROLE_LEVEL_ORDER, (s) => s.role_level),
    eventType: count(EVENT_ORDER, (s) => s.event_type),
    successorStatus: count(SUCCESSOR_ORDER, (s) => s.successor_status),
  };
}
