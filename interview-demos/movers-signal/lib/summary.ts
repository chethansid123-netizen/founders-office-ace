import { daysBetween } from "./score";
import type { SeatRecord } from "./types";

export interface Summary {
  seats: number;
  filings: number;
  noPermanentSuccessor: number;
  topSeats: number;
  next45: number;
  next45Days: number;
}

/** The Radar's three headline numbers, always computed from the records passed in. */
export function computeSummary(seats: SeatRecord[], asOf: string, nextDays = 45): Summary {
  return {
    seats: seats.length,
    filings: new Set(seats.map((s) => s.source_url)).size,
    noPermanentSuccessor: seats.filter((s) => s.successor_status !== "NAMED_PERMANENT").length,
    topSeats: seats.filter((s) => s.role_level === "CEO_MD" || s.role_level === "CXO").length,
    next45: seats.filter((s) => {
      if (!s.effective_date) return false;
      const d = daysBetween(asOf, s.effective_date);
      return d >= 0 && d <= nextDays;
    }).length,
    next45Days: nextDays,
  };
}

/** Count seats by a key, in a given order (for the Market pulse charts). */
export function countBy(seats: SeatRecord[], key: (s: SeatRecord) => string, order: string[]): { label: string; count: number }[] {
  return order.map((label) => ({ label, count: seats.filter((s) => key(s) === label).length }));
}
