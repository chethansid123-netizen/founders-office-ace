import hypothesesConfig from "@/config/hypotheses.json";
import { formatDate, ROLE_LEVEL_LABEL } from "./format";
import type { ScoredSeat } from "./score";
import type { SeatRecord } from "./types";

/**
 * Rule-generated hypotheses for a seat brief. Every line is a judgement for a
 * partner to review, built only from the seat's filed and derived facts.
 * No person or specific company is ever named as a candidate.
 */
export interface Hypotheses {
  whyNow: [string, string];
  questions: [string, string, string];
  pools: string[];
  functionLabel: string;
}

interface HypConfig {
  functions: { key: string; label: string; pattern: string }[];
  general_levels: string[];
  peers: Record<string, string>;
  pools: Record<string, string[]>;
}

const H = hypothesesConfig as HypConfig;

export function functionOf(seat: SeatRecord): { key: string; label: string } {
  const title = seat.role_title.toLowerCase();
  if (H.general_levels.includes(seat.role_level) && !/president\s*[-–—]\s*operations/.test(title)) {
    const g = H.functions.find((f) => f.key === "general")!;
    return { key: g.key, label: g.label };
  }
  for (const f of H.functions) {
    if (new RegExp(f.pattern).test(title)) return { key: f.key, label: f.label };
  }
  return { key: "general", label: "General management" };
}

function roleName(seat: SeatRecord): string {
  return seat.role_title.replace(/\s*\((CEO|CFO|CRO|CHRO|CDIO|KMP|SMP)\)\s*/g, " ").replace(/\s+/g, " ").trim();
}

function capitalise(s: string): string {
  return s ? s[0]!.toUpperCase() + s.slice(1) : s;
}

export function buildHypotheses(s: ScoredSeat): Hypotheses {
  const seat = s.seat;
  const role = roleName(seat);
  const d = s.daysToEffective;
  const when = seat.effective_date ? formatDate(seat.effective_date) : null;
  const filedText = [...seat.context_facts.map((c) => c.quote), seat.evidence.successor_status?.quote ?? ""];
  const noLikeForLike = filedText.some((q) => /not presently envisage like-for-like/i.test(q));

  // Line 1: where the seat stands, from filed and derived facts.
  let line1: string;
  if (s.seatFilled) {
    const src = seat.successor_source === "EXTERNAL" ? "an external" : seat.successor_source === "INTERNAL" ? "an internal" : "a named";
    line1 = `${seat.company} has filled the ${role} seat with ${src} appointee${when ? ` from ${when}` : ""}.`;
  } else if (seat.successor_status === "NOT_NAMED") {
    if (d === null) line1 = `The filing names no successor for the ${role} seat and gives no exit date.`;
    else if (d > 0) line1 = `The ${role} seat opens in ${d} days (${when}) and the filing names no successor.`;
    else if (d === 0) line1 = `The ${role} seat opens today (${when}) and the filing names no successor.`;
    else line1 = `The ${role} seat has had no named successor since ${when} (${-d} days).`;
  } else if (seat.successor_status === "NAMED_PERMANENT") {
    line1 = `A permanent successor is already named, so the live question is the seat that successor leaves behind.`;
  } else if (seat.successor_status === "NAMED_INTERIM") {
    line1 = `Only an interim holder is named for the ${role} seat, so a permanent appointment is still to come.`;
  } else {
    line1 = `The filing does not make clear who will hold the ${role} seat next.`;
  }

  // Line 2: why it may matter for a search conversation (judgement).
  let line2: string;
  if (noLikeForLike) line2 = "The company says it does not plan a like-for-like hire, so treat this as a watch, not a live search.";
  else if (s.otherExits.length >= 2) line2 = `With ${s.otherExits.length} other senior exits at ${seat.company} in this sample, the team around this seat is changing.`;
  else if (s.otherExits.length === 1) line2 = `One other senior exit at ${seat.company} in this sample points to wider movement in the team.`;
  else if (s.seatFilled && seat.role_level === "CEO_MD") line2 = "New chief executives often reshape their leadership teams, so the seats around this one may move next.";
  else if (seat.practice === "Private Equity") line2 = "With a private equity investor involved in control, leadership hiring may follow an investor agenda.";
  else if (s.seatFilled) line2 = "The seat itself is closed, but a new appointee can change the seats that report into it.";
  else if (seat.role_level === "CEO_MD" || seat.role_level === "CXO") line2 = "Boards tend to move quickly on top-seat vacancies at listed companies.";
  else line2 = "A named senior seat at a listed company: worth an early, light-touch conversation.";

  // Questions for the partner.
  const q1 = `Who owns this hire at ${seat.company}, and does Positive Moves already know them? (Check in PINE.)`;
  let q2: string;
  if (s.seatFilled) {
    q2 = seat.successor_source === "EXTERNAL"
      ? "Which seat did the appointee leave at their previous employer, and is it open now?"
      : seat.successor_source === "INTERNAL"
        ? "Which role does the promoted executive leave behind, and will it need a search?"
        : "Was this an external hire or an internal move, and what does it change around the seat?";
  } else if (seat.successor_status === "NOT_NAMED") {
    q2 = noLikeForLike
      ? "If the role is absorbed internally, which remaining leaders now carry more, and are any of those seats at risk?"
      : `Is ${seat.company} likely to search externally, or is an internal successor being prepared?`;
  } else if (seat.successor_status === "NAMED_PERMANENT") {
    q2 = seat.successor_source === "EXTERNAL"
      ? "Which seat did the incoming successor leave at their previous employer, and is it open now?"
      : seat.successor_source === "INTERNAL"
        ? "Which role does the internal successor vacate, and will that seat need a search?"
        : "Is the successor joining from outside or moving internally, and which seat opens as a result?";
  } else {
    q2 = "Is the person named alongside this change the real successor, or is the seat still open?";
  }
  const q3 = d === null
    ? "What timeline is the company working to, given that the filing gives no date?"
    : d >= 0
      ? `What timeline is the company working to before ${when}?`
      : "Who is covering the role now, and how long can that arrangement last?";

  const fn = functionOf(seat);
  const peers = H.peers[seat.practice] ?? "companies in the same sector";
  const pools = (H.pools[fn.key] ?? H.pools.general ?? []).map((p) => capitalise(p.replace("{peers}", peers)));

  return {
    whyNow: [line1, line2],
    questions: [q1, q2, q3],
    pools,
    functionLabel: `${fn.label} · ${ROLE_LEVEL_LABEL[seat.role_level]}`,
  };
}
