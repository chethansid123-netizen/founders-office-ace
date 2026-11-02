import type { EventType, RoleLevel, SeatRecord, SuccessorStatus } from "./types";

/** Shape of config/score.json (only the parts the rule uses). */
export interface ScoreConfig {
  as_of: string;
  components: {
    role_level: { label: string; points: Record<RoleLevel, number> };
    successor_status: { label: string; points: Record<SuccessorStatus, number> };
    company_exits: {
      label: string;
      exit_event_types: EventType[];
      window_days: number;
      bands: { min: number; max: number | null; points: number }[];
    };
    timing: {
      label: string;
      next_days: number;
      next_points: number;
      past_days: number;
      past_points: number;
      otherwise_points: number;
    };
  };
  max_points: number;
  gate: { when: { event_type: EventType; successor_status: SuccessorStatus }; status: string };
  status_labels: Record<SuccessorStatus, string>;
}

export type ComponentKey = "role_level" | "successor_status" | "company_exits" | "timing";

export interface ScoreComponent {
  key: ComponentKey;
  label: string;
  points: number;
  max: number;
  reason: string;
}

export interface ScoredSeat {
  seat: SeatRecord;
  total: number;
  components: ScoreComponent[];
  status: string;
  seatFilled: boolean;
  daysToEffective: number | null;
  timingBand: "next" | "past" | "otherwise";
  otherExits: SeatRecord[];
}

const DAY_MS = 86_400_000;

/** Whole days from `from` to `to` (both ISO yyyy-mm-dd), in UTC. */
export function daysBetween(from: string, to: string): number {
  return Math.round((Date.parse(`${to}T00:00:00Z`) - Date.parse(`${from}T00:00:00Z`)) / DAY_MS);
}

/** Other exit records at the same company, filed in the window up to the as-of date. */
export function otherExitsAtCompany(seat: SeatRecord, all: SeatRecord[], asOf: string, cfg: ScoreConfig): SeatRecord[] {
  const c = cfg.components.company_exits;
  return all.filter(
    (o) =>
      o.id !== seat.id &&
      o.company === seat.company &&
      c.exit_event_types.includes(o.event_type) &&
      o.filing_date !== null &&
      daysBetween(o.filing_date, asOf) >= 0 &&
      daysBetween(o.filing_date, asOf) <= c.window_days,
  );
}

export function exitPoints(count: number, cfg: ScoreConfig): number {
  const band = cfg.components.company_exits.bands.find((b) => count >= b.min && (b.max === null || count <= b.max));
  return band ? band.points : 0;
}

export function timingFor(days: number | null, cfg: ScoreConfig): { points: number; band: "next" | "past" | "otherwise" } {
  const t = cfg.components.timing;
  if (days === null) return { points: t.otherwise_points, band: "otherwise" };
  if (days >= 0 && days <= t.next_days) return { points: t.next_points, band: "next" };
  if (days < 0 && days >= -t.past_days) return { points: t.past_points, band: "past" };
  return { points: t.otherwise_points, band: "otherwise" };
}

const ROLE_WORDS: Record<RoleLevel, string> = {
  CEO_MD: "CEO / MD",
  CXO: "C-suite (CXO)",
  BUSINESS_HEAD: "Business head",
  FUNCTION_HEAD: "Function head",
  OTHER_SMP: "Other senior management",
};

const SUCCESSOR_WORDS: Record<SuccessorStatus, string> = {
  NOT_NAMED: "No successor named",
  NAMED_INTERIM: "Interim successor named",
  UNCLEAR: "Successor unclear",
  NAMED_PERMANENT: "Permanent successor named",
};

function fmt(d: string): string {
  const [y, m, day] = d.split("-").map(Number);
  const mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][(m ?? 1) - 1];
  return `${day} ${mon} ${y}`;
}

/**
 * The priority rule. Pure: the same seat, dataset, date and config always give
 * the same result. It is a transparent priority, not a probability.
 */
export function scoreSeat(
  seat: SeatRecord,
  ctx: { asOf: string; allSeats: SeatRecord[]; config: ScoreConfig },
): ScoredSeat {
  const { asOf, allSeats, config } = ctx;
  const comps = config.components;

  const rolePts = comps.role_level.points[seat.role_level];
  const roleMax = Math.max(...Object.values(comps.role_level.points));

  const succPts = comps.successor_status.points[seat.successor_status];
  const succMax = Math.max(...Object.values(comps.successor_status.points));
  let succReason = SUCCESSOR_WORDS[seat.successor_status];
  if (seat.successor_status === "NAMED_PERMANENT" && seat.successor_source !== "NOT_APPLICABLE") {
    succReason += ` (${seat.successor_source.toLowerCase()})`;
  }

  const others = otherExitsAtCompany(seat, allSeats, asOf, config);
  const exitPts = exitPoints(others.length, config);
  const exitMax = Math.max(...comps.company_exits.bands.map((b) => b.points));

  const days = seat.effective_date ? daysBetween(asOf, seat.effective_date) : null;
  const timing = timingFor(days, config);
  const timingMax = Math.max(comps.timing.next_points, comps.timing.past_points, comps.timing.otherwise_points);
  let timingReason: string;
  if (days === null) timingReason = "No effective date stated";
  else if (days === 0) timingReason = `Effective ${fmt(seat.effective_date!)}, the as-of date`;
  else if (days > 0) timingReason = `Effective ${fmt(seat.effective_date!)}, ${days} days after ${fmt(asOf)}`;
  else timingReason = `Effective ${fmt(seat.effective_date!)}, ${-days} days before ${fmt(asOf)}`;

  const components: ScoreComponent[] = [
    { key: "role_level", label: comps.role_level.label, points: rolePts, max: roleMax, reason: ROLE_WORDS[seat.role_level] },
    { key: "successor_status", label: comps.successor_status.label, points: succPts, max: succMax, reason: succReason },
    {
      key: "company_exits",
      label: comps.company_exits.label,
      points: exitPts,
      max: exitMax,
      reason: others.length === 0 ? "No other exits at this company in the dataset" : `${others.length} other exit${others.length > 1 ? "s" : ""} at this company in the dataset`,
    },
    { key: "timing", label: comps.timing.label, points: timing.points, max: timingMax, reason: timingReason },
  ];
  const total = components.reduce((s, c) => s + c.points, 0);

  const g = config.gate.when;
  const seatFilled = seat.event_type === g.event_type && seat.successor_status === g.successor_status;
  const status = seatFilled ? config.gate.status : config.status_labels[seat.successor_status];

  return { seat, total, components, status, seatFilled, daysToEffective: days, timingBand: timing.band, otherExits: others };
}

/** Rank: open seats before filled ones, then priority, then the soonest effective date, then company. */
export function rankScored(list: ScoredSeat[]): ScoredSeat[] {
  return [...list].sort((a, b) => {
    if (a.seatFilled !== b.seatFilled) return a.seatFilled ? 1 : -1;
    if (b.total !== a.total) return b.total - a.total;
    const ad = a.seat.effective_date ?? "9999-12-31";
    const bd = b.seat.effective_date ?? "9999-12-31";
    if (ad !== bd) return ad < bd ? -1 : 1;
    return a.seat.company.localeCompare(b.seat.company);
  });
}
