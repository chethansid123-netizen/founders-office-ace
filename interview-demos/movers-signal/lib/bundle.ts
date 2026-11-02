import linkCheckJson from "@/data/link_check.json";
import stableLinksJson from "@/data/stable_links.json";
import roleLevelsJson from "@/config/role_levels.json";
import { factRows } from "./brief";
import { AS_OF, AUDIT, HUMAN_SIGNOFF, PRACTICES, rankOf, SCORE_CONFIG, SCORED, SEATS, urlForKey } from "./data";
import { EVENT_MEANING, SUCCESSOR_MEANING } from "./definitions";
import { EVENT_ORDER, filterOptions, PRACTICE_ORDER, ROLE_LEVEL_ORDER, SUCCESSOR_ORDER } from "./filters";
import { addDays, EVENT_LABEL, exchangeOf, formatDate, ROLE_LEVEL_LABEL, SOURCE_LABEL, sourceHref, SUCCESSOR_LABEL } from "./format";
import { buildHypotheses } from "./hypotheses";
import { pulseData, SMALL_SAMPLE } from "./pulse";
import { toRadarRow } from "./radar";
import { computeSummary } from "./summary";
import type { RoleLevel } from "./types";

export const DISCLAIMER = "Independent prototype built from public filings. Not affiliated with Positive Moves.";

/**
 * The whole site as data: every value the four screens show, computed by the
 * same code as the pages, from VERIFIED records only. Published as
 * /site-data.json so another front end (the Lovable copy) can render the site
 * without re-implementing any rule.
 */
export function buildBundle() {
  const summary = computeSummary(SEATS, AS_OF);
  const linkCheck = linkCheckJson as unknown as { checked_at: string; links: number; ok: number; failed: number; not_checked: number; pages_cited: number };
  const stable = stableLinksJson as unknown as { links: Record<string, unknown>; pending: string[] };
  const roleRules = (roleLevelsJson as unknown as { rules: { level: RoleLevel; why: string }[] }).rules;
  const comps = SCORE_CONFIG.components;
  const top = SCORED[0]!;

  const seats = SCORED.map((s, i) => {
    const seat = s.seat;
    const h = buildHypotheses(s);
    const practice = PRACTICES.companies[seat.company];
    const v = seat.verification;
    const checks = v ? Object.values(v.fields) : [];
    const days = s.daysToEffective;
    const row = toRadarRow(s, i + 1);
    return {
      ...row,
      practice_label: seat.practice,
      role_level_label: ROLE_LEVEL_LABEL[seat.role_level],
      successor_label: SUCCESSOR_LABEL[seat.successor_status],
      successor_source_label: SOURCE_LABEL[seat.successor_source],
      filing_date: seat.filing_date,
      filing_date_label: formatDate(seat.filing_date),
      effective_date_note: seat.effective_date_note,
      source_sha256: seat.source_sha256 ?? null,
      facts: factRows(seat).map((f) => ({
        label: f.label,
        value: f.value,
        quote: f.evidence?.quote ?? null,
        page: f.evidence?.page ?? null,
        note: f.evidence?.note ?? null,
      })),
      also_in_filing: seat.context_facts.map((c) => ({ label: c.label, value: c.value, quote: c.quote, page: c.page })),
      priority: {
        total: s.total,
        components: s.components.map((c) => ({ label: c.label, reason: c.reason, points: c.points, max: c.max })),
        seat_filled: s.seatFilled,
      },
      hypotheses: { why_now: h.whyNow, questions: h.questions, pools: h.pools, function_label: h.functionLabel },
      derived: {
        practice: seat.practice,
        practice_basis: practice?.pe_basis ?? `Main line of business: ${practice?.sector ?? "not classified"}.`,
        practice_evidence: (practice?.evidence ?? []).map((e) => ({ quote: e.quote, page: e.page, url: urlForKey(e.source_key) ?? null })),
        role_level: ROLE_LEVEL_LABEL[seat.role_level],
        role_rule: v?.reasons.role_level?.replace(/^rule gives \w+ /, "") ?? "",
        days_to_effective: days,
        days_text: days === null ? "No date stated" : days === 0 ? `0 (effective on the as-of date, ${formatDate(AS_OF)})` : days > 0 ? `${days} days after ${formatDate(AS_OF)}` : `${-days} days before ${formatDate(AS_OF)}`,
        other_exits: s.otherExits.map((o) => ({ id: o.id, role_title: o.role_title, effective_label: formatDate(o.effective_date), rank: rankOf(o.id) })),
      },
      review: {
        status: seat.review_status,
        by: seat.reviewed_by ?? null,
        at: seat.reviewed_at ?? null,
        at_label: formatDate(seat.reviewed_at ?? null),
        checks_total: checks.length,
        checks_match: checks.filter((c) => c === "match").length,
        checks_absent: checks.filter((c) => c === "not_found").length,
        cleared: (seat.review_overrides ?? []).map((o) => ({ field: o.field, reason: o.reason })),
        corrections: (seat.corrections ?? []).map((c) => ({ field: c.field, reason: c.reason })),
      },
      exchange_name: exchangeOf(sourceHref(seat)),
    };
  });

  const groups = filterOptions(SEATS);
  const label = {
    practice: (v: string) => v,
    roleLevel: (v: string) => ROLE_LEVEL_LABEL[v as RoleLevel],
    eventType: (v: string) => EVENT_LABEL[v as keyof typeof EVENT_LABEL],
    successorStatus: (v: string) => SUCCESSOR_LABEL[v as keyof typeof SUCCESSOR_LABEL],
  };

  return {
    meta: {
      name: "Movers Signal",
      headline: "Leadership seats before the mandate",
      disclaimer: DISCLAIMER,
      as_of: AS_OF,
      as_of_label: formatDate(AS_OF),
      window: AUDIT.window,
      window_label: [formatDate(AUDIT.window[0]), formatDate(AUDIT.window[1])],
      human_signoff: HUMAN_SIGNOFF,
      reviewed_by: AUDIT.reviewed_by,
      generated_from: "data/records.json (VERIFIED records only)",
    },
    summary: { ...summary, next45_to_label: formatDate(addDays(AS_OF, summary.next45Days)) },
    filters: {
      params: { practice: "practice", roleLevel: "role", eventType: "event", successorStatus: "successor" },
      groups: Object.fromEntries(
        (Object.keys(groups) as (keyof typeof groups)[]).map((k) => [k, groups[k].map((o) => ({ value: o.value, label: label[k](o.value), count: o.count }))]),
      ),
    },
    seats,
    pulse: { ...pulseData(SEATS), small_sample: SMALL_SAMPLE },
    method: {
      audit: AUDIT,
      link_check: { checked_at: linkCheck.checked_at, links: linkCheck.links, ok: linkCheck.ok, failed: linkCheck.failed, not_checked: linkCheck.not_checked, pages_cited: linkCheck.pages_cited },
      stable_links: { moved: Object.keys(stable.links).length, pending: stable.pending.length },
      filings_on_site: summary.filings,
      seats_on_site: summary.seats,
      role_rules: roleRules.map((r) => ({ level: ROLE_LEVEL_LABEL[r.level], why: r.why })),
      events: EVENT_ORDER.map((e) => ({ label: EVENT_LABEL[e], meaning: EVENT_MEANING[e] })),
      successor_statuses: SUCCESSOR_ORDER.map((s) => ({ label: SUCCESSOR_LABEL[s], meaning: SUCCESSOR_MEANING[s] })),
      practice_rules: PRACTICES.rules,
      practices: PRACTICE_ORDER.map((p) => ({ label: p, description: PRACTICES.practices[p] })),
      score: {
        max_points: SCORE_CONFIG.max_points,
        tables: [
          { title: comps.role_level.label, rows: ROLE_LEVEL_ORDER.map((k) => [ROLE_LEVEL_LABEL[k], comps.role_level.points[k]]) },
          { title: comps.successor_status.label, rows: SUCCESSOR_ORDER.map((k) => [SUCCESSOR_LABEL[k], comps.successor_status.points[k]]) },
          {
            title: comps.company_exits.label,
            rows: comps.company_exits.bands.map((b) => [b.max === null ? `${b.min} or more` : b.min === b.max ? `${b.min}` : `${b.min} to ${b.max}`, b.points]),
          },
          {
            title: comps.timing.label,
            rows: [
              [`Effective in the next ${comps.timing.next_days} days (today counts)`, comps.timing.next_points],
              [`Effective in the last ${comps.timing.past_days} days`, comps.timing.past_points],
              ["Any other date, or no date stated", comps.timing.otherwise_points],
            ],
          },
        ],
        gate_status: SCORE_CONFIG.gate.status,
        worked_example: {
          id: top.seat.id,
          title: `${top.seat.role_title} at ${top.seat.company}`,
          total: top.total,
          components: top.components.map((c) => ({ label: c.label, reason: c.reason, points: c.points })),
        },
      },
    },
  };
}

export type SiteBundle = ReturnType<typeof buildBundle>;
