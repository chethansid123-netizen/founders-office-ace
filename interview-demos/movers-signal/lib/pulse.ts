import { FILTER_PARAMS, PRACTICE_ORDER, ROLE_LEVEL_ORDER } from "./filters";
import { ROLE_LEVEL_LABEL } from "./format";
import { countBy } from "./summary";
import type { RoleLevel, SeatRecord } from "./types";

export const SMALL_SAMPLE = 5;

/** A seat counts as "no permanent successor" when the filing names none, an interim, or is unclear. */
export const noPermanent = (s: SeatRecord) => s.successor_status !== "NAMED_PERMANENT";

export function radarHref(param: keyof typeof FILTER_PARAMS, value: string): string {
  return `/?${new URLSearchParams({ [FILTER_PARAMS[param]]: value }).toString()}`;
}

export interface BarDatum {
  label: string;
  value: string;
  count: number;
  href: string;
}

export interface ShareDatum {
  label: string;
  n: number;
  open: number;
  ratio: number;
  href: string;
  small: boolean;
}

/** Everything the Market pulse page draws, computed from the seats passed in. */
export function pulseData(seats: SeatRecord[]) {
  const n = seats.length;
  const byPractice: BarDatum[] = countBy(seats, (s) => s.practice, PRACTICE_ORDER)
    .map((c) => ({ label: c.label, value: c.label, count: c.count, href: radarHref("practice", c.label) }))
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label));
  const byRole: BarDatum[] = countBy(seats, (s) => s.role_level, ROLE_LEVEL_ORDER).map((c) => ({
    label: ROLE_LEVEL_LABEL[c.label as RoleLevel],
    value: c.label,
    count: c.count,
    href: radarHref("roleLevel", c.label),
  }));
  const openAll = seats.filter(noPermanent).length;
  const share: ShareDatum[] = PRACTICE_ORDER.map((p) => {
    const inP = seats.filter((s) => s.practice === p);
    const open = inP.filter(noPermanent).length;
    return { label: p, n: inP.length, open, ratio: inP.length ? open / inP.length : 0, href: radarHref("practice", p), small: inP.length < SMALL_SAMPLE };
  })
    .filter((r) => r.n > 0)
    .sort((a, b) => b.ratio - a.ratio || b.n - a.n || a.label.localeCompare(b.label));
  return { n, filings: new Set(seats.map((s) => s.source_url)).size, byPractice, byRole, openAll, share };
}
