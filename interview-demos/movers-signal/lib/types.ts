export type RoleLevel = "CEO_MD" | "CXO" | "BUSINESS_HEAD" | "FUNCTION_HEAD" | "OTHER_SMP";
export type EventType = "RESIGNATION" | "RETIREMENT" | "REMOVAL" | "END_OF_TERM" | "APPOINTMENT" | "OTHER";
export type SuccessorStatus = "NAMED_PERMANENT" | "NAMED_INTERIM" | "NOT_NAMED" | "UNCLEAR";
export type SuccessorSource = "INTERNAL" | "EXTERNAL" | "UNCLEAR" | "NOT_APPLICABLE";
export type ReviewStatus = "UNREVIEWED" | "VERIFIED" | "REJECTED";
export type VerifyStatus = "match" | "mismatch" | "not_found";

export interface Evidence {
  quote: string | null;
  page: number | null;
  note?: string;
  fragments?: string[];
}

export interface ContextFact {
  label: string;
  value: string;
  quote: string;
  page: number;
}

export interface SeatRecord {
  id: string;
  company: string;
  exchange_symbol: string | null;
  practice: string;
  person_name: string | null;
  role_title: string;
  role_level: RoleLevel;
  event_type: EventType;
  filing_date: string | null;
  effective_date: string | null;
  stated_reason: string | null;
  successor_status: SuccessorStatus;
  successor_source: SuccessorSource;
  source_url: string;
  source_page: number | null;
  evidence: Record<string, Evidence>;
  review_status: ReviewStatus;
  review_note: string | null;
  source_key: string;
  source_sha256?: string;
  successor_name: string | null;
  effective_date_note: string | null;
  company_basis: string;
  context_facts: ContextFact[];
  reviewed_by?: string | null;
  reviewed_at?: string | null;
  review_overrides?: { field: string; reason: string }[];
  verification?: {
    run: string;
    fields: Record<string, VerifyStatus>;
    reasons: Record<string, string>;
    context: VerifyStatus[];
    record_flags: string[];
  };
  corrections?: { field: string; reason: string; found_by: string }[];
  extraction_note?: string | null;
}

export interface RecordsFile {
  generated_at: string;
  as_of: string;
  human_signoff: boolean;
  records: SeatRecord[];
}
