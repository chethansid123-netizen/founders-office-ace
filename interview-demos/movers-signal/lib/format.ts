import type { EventType, RoleLevel, SuccessorSource, SuccessorStatus } from "./types";

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export function formatDate(iso: string | null | undefined): string {
  if (!iso) return "Not stated";
  const [y, m, d] = iso.split("-").map(Number);
  return `${d} ${MONTHS[(m ?? 1) - 1]} ${y}`;
}

/** ISO date plus n days (UTC), as yyyy-mm-dd. */
export function addDays(iso: string, n: number): string {
  const d = new Date(`${iso}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

export const ROLE_LEVEL_LABEL: Record<RoleLevel, string> = {
  CEO_MD: "CEO / MD",
  CXO: "CXO",
  BUSINESS_HEAD: "Business head",
  FUNCTION_HEAD: "Function head",
  OTHER_SMP: "Other SMP",
};

export const EVENT_LABEL: Record<EventType, string> = {
  RESIGNATION: "Resignation",
  RETIREMENT: "Retirement",
  REMOVAL: "Removal",
  END_OF_TERM: "End of term",
  APPOINTMENT: "Appointment",
  OTHER: "Other move",
};

export const SUCCESSOR_LABEL: Record<SuccessorStatus, string> = {
  NOT_NAMED: "Not named",
  NAMED_INTERIM: "Interim",
  UNCLEAR: "Unclear",
  NAMED_PERMANENT: "Permanent named",
};

export const SOURCE_LABEL: Record<SuccessorSource, string> = {
  INTERNAL: "Internal",
  EXTERNAL: "External",
  UNCLEAR: "Not stated",
  NOT_APPLICABLE: "Not applicable",
};

export function exchangeOf(url: string): string {
  if (url.includes("nseindia.com")) return "NSE";
  if (url.includes("bseindia.com")) return "BSE";
  return "Company";
}

/** The address the site links to for a seat's filing: the permanent copy when there is one. */
export function sourceHref(seat: { source_url: string; source_url_stable?: string }): string {
  return seat.source_url_stable ?? seat.source_url;
}

export function pdfLink(url: string, page: number | null | undefined): string {
  return page ? `${url}#page=${page}` : url;
}

export function pct(n: number, d: number): string {
  return d === 0 ? "0%" : `${Math.round((n / d) * 100)}%`;
}
