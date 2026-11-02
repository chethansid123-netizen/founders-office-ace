import auditJson from "@/data/audit.json";
import manifestJson from "@/data/raw/manifest.json";
import recordsJson from "@/data/records.json";
import practicesJson from "@/config/practices.json";
import scoreJson from "@/config/score.json";
import { rankScored, scoreSeat, type ScoreConfig, type ScoredSeat } from "./score";
import type { RecordsFile, SeatRecord } from "./types";

/**
 * The only bridge between the dataset and the site. It hands the UI VERIFIED
 * records and nothing else; rejected or unreviewed records never leave here.
 * Import it from server components only, so the full file is never bundled
 * into client JavaScript.
 */
export function onlyVerified(records: SeatRecord[]): SeatRecord[] {
  return records.filter((r) => r.review_status === "VERIFIED");
}

const file = recordsJson as unknown as RecordsFile;

export const SCORE_CONFIG = scoreJson as unknown as ScoreConfig;
export const AS_OF: string = SCORE_CONFIG.as_of;
export const HUMAN_SIGNOFF: boolean = file.human_signoff;
export const SEATS: SeatRecord[] = onlyVerified(file.records);
export const SCORED: ScoredSeat[] = rankScored(
  SEATS.map((seat) => scoreSeat(seat, { asOf: AS_OF, allSeats: SEATS, config: SCORE_CONFIG })),
);

export function getScored(id: string): ScoredSeat | undefined {
  return SCORED.find((s) => s.seat.id === id);
}

export function rankOf(id: string): number {
  return SCORED.findIndex((s) => s.seat.id === id) + 1;
}

export interface PracticeInfo {
  practice: string;
  sector: string;
  symbol: string | null;
  pe_basis?: string;
  evidence?: { source_key: string; quote: string; page: number }[];
}

export const PRACTICES = practicesJson as unknown as {
  rules: string[];
  practices: Record<string, string>;
  companies: Record<string, PracticeInfo>;
};

export const AUDIT = auditJson as unknown as {
  filings_reviewed: number;
  fields_checked_per_run: number;
  context_facts_checked_per_run: number;
  errors_found: number;
  errors_found_fields: number;
  errors_found_record_flags: number;
  errors_fixed: number;
  errors_fixed_now_match: number;
  false_positives_cleared: number;
  records_rejected: number;
  seats_verified: number;
  filings_verified: number;
  documents_fetched: number;
  screened_out_at_triage: number;
  date_of_last_review: string;
  reviewed_by: string;
  human_signoff: boolean;
  window: [string, string];
  error_classes_v1: Record<string, number>;
};

const MANIFEST = manifestJson as unknown as Record<string, { url: string; sha256?: string }>;

/** Public URL of a source document by its pipeline key (used for practice evidence). */
export function urlForKey(key: string): string | undefined {
  return MANIFEST[key]?.url;
}
