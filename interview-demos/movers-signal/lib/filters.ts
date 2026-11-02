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

/** The four fields the Radar filters on. Rows sent to the browser carry only these. */
export type Filterable = Pick<SeatRecord, "practice" | "role_level" | "event_type" | "successor_status">;

export function matches(seat: Filterable, f: Filters): boolean {
  return (
    (f.practice === ALL || seat.practice === f.practice) &&
    (f.roleLevel === ALL || seat.role_level === f.roleLevel) &&
    (f.eventType === ALL || seat.event_type === f.eventType) &&
    (f.successorStatus === ALL || seat.successor_status === f.successorStatus)
  );
}

/** Pure filter. Works on bare records or on anything carrying a `seat`. */
export function applyFilters<T extends Filterable | { seat: Filterable }>(items: T[], f: Filters): T[] {
  return items.filter((it) => matches("seat" in it ? it.seat : (it as Filterable), f));
}

/** Query-string names for each filter, so a filtered Radar view can be shared as a link. */
export const FILTER_PARAMS: Record<keyof Filters, string> = {
  practice: "practice",
  roleLevel: "role",
  eventType: "event",
  successorStatus: "successor",
};

const FILTER_KEYS = Object.keys(FILTER_PARAMS) as (keyof Filters)[];

/** Read filters from a query string. A missing, unknown or unavailable value means "all". */
export function filtersFromSearch(search: string, allowed: Record<keyof Filters, string[]>): Filters {
  const params = new URLSearchParams(search);
  const pick = (k: keyof Filters): string => {
    const v = params.get(FILTER_PARAMS[k]);
    return v !== null && allowed[k].includes(v) ? v : ALL;
  };
  return { practice: pick("practice"), roleLevel: pick("roleLevel"), eventType: pick("eventType"), successorStatus: pick("successorStatus") };
}

/** Write filters to a query string, leaving out any filter set to "all". */
export function filtersToSearch(f: Filters): string {
  const params = new URLSearchParams();
  for (const k of FILTER_KEYS) if (f[k] !== ALL) params.set(FILTER_PARAMS[k], f[k]);
  return params.toString();
}

export function isFiltered(f: Filters): boolean {
  return FILTER_KEYS.some((k) => f[k] !== ALL);
}

export interface Option {
  value: string;
  count: number;
}

export type FilterGroups = Record<keyof Filters, Option[]>;

/** Values a link may select: those with at least one seat. */
export function allowedValues(groups: FilterGroups): Record<keyof Filters, string[]> {
  const pick = (opts: Option[]) => opts.filter((o) => o.count > 0).map((o) => o.value);
  return { practice: pick(groups.practice), roleLevel: pick(groups.roleLevel), eventType: pick(groups.eventType), successorStatus: pick(groups.successorStatus) };
}

/** Filter options in canonical order, with the count of seats for each value. */
export function filterOptions(seats: SeatRecord[]): FilterGroups {
  const count = (vals: string[], key: (s: SeatRecord) => string): Option[] =>
    vals.map((v) => ({ value: v, count: seats.filter((s) => key(s) === v).length }));
  return {
    practice: count(PRACTICE_ORDER, (s) => s.practice),
    roleLevel: count(ROLE_LEVEL_ORDER, (s) => s.role_level),
    eventType: count(EVENT_ORDER, (s) => s.event_type),
    successorStatus: count(SUCCESSOR_ORDER, (s) => s.successor_status),
  };
}
