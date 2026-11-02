import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import linkCheckJson from "@/data/link_check.json";
import stableLinksJson from "@/data/stable_links.json";
import roleLevelsJson from "@/config/role_levels.json";
import { Section, Tag } from "@/components/ui";
import { AS_OF, AUDIT, HUMAN_SIGNOFF, PRACTICES, SCORE_CONFIG, SCORED, SEATS } from "@/lib/data";
import { EVENT_ORDER, PRACTICE_ORDER, ROLE_LEVEL_ORDER, SUCCESSOR_ORDER } from "@/lib/filters";
import { EVENT_LABEL, formatDate, ROLE_LEVEL_LABEL, SUCCESSOR_LABEL } from "@/lib/format";
import type { RoleLevel } from "@/lib/types";

export const metadata: Metadata = { title: "Method" };

const LINK_CHECK = linkCheckJson as unknown as {
  checked_at: string;
  links: number;
  ok: number;
  failed: number;
  not_checked: number;
  pages_cited: number;
  stopped: string | null;
};

const STABLE = stableLinksJson as unknown as { links: Record<string, { stable_url: string }>; pending: string[] };

const ROLE_RULES = (roleLevelsJson as unknown as { rules: { level: RoleLevel; pattern: string; why: string }[] }).rules;

const EVENT_MEANING: Record<string, string> = {
  RESIGNATION: "The filing says the person resigned.",
  RETIREMENT: "The filing says the person retires or superannuates.",
  REMOVAL: "The filing says the person was removed or terminated.",
  END_OF_TERM: "The filing says the person's term ends or is not renewed.",
  APPOINTMENT: "The filing appoints a person to the seat.",
  OTHER: "Any other change of seat holder the filing describes, such as a move to another role.",
};

const SUCCESSOR_MEANING: Record<string, string> = {
  NOT_NAMED: "The filing names no successor.",
  NAMED_INTERIM: "The filing names someone to hold the seat for now (interim or additional charge).",
  UNCLEAR: "The filing's wording leaves it unclear whether a successor is named.",
  NAMED_PERMANENT: "The filing names a permanent successor, internal or external.",
};

function Steps({ items }: { items: { title: string; body: ReactNode }[] }) {
  return (
    <ol className="space-y-4">
      {items.map((it, i) => (
        <li key={it.title} className="grid grid-cols-[2rem_1fr] gap-3">
          <span aria-hidden className="num flex h-8 w-8 items-center justify-center rounded-full bg-pine text-sm font-semibold text-on-pine">{i + 1}</span>
          <div className="min-w-0">
            <h3 className="font-sans text-base font-semibold text-ink">{it.title}</h3>
            <div className="mt-0.5 text-muted">{it.body}</div>
          </div>
        </li>
      ))}
    </ol>
  );
}

export default function MethodPage() {
  const comps = SCORE_CONFIG.components;
  const top = SCORED[0]!;
  const filings = new Set(SEATS.map((s) => s.source_url)).size;
  const [from, to] = AUDIT.window;

  return (
    <div className="space-y-8">
      <header className="max-w-3xl">
        <p className="text-xs font-semibold uppercase tracking-wider text-muted">Method</p>
        <h1 className="mt-2 text-4xl font-semibold leading-tight text-ink sm:text-5xl">How each number is made, and where it stops</h1>
        <p className="mt-4 text-lg text-muted">
          Movers Signal reads public exchange filings, keeps only what the filing states, checks it twice, and ranks seats with a rule
          you can recompute by hand.
        </p>
      </header>

      <Section title="Three kinds of statement">
        <dl className="grid gap-4 sm:grid-cols-3">
          <div>
            <dt><Tag kind="fact" /></dt>
            <dd className="mt-2 text-sm text-muted">Stated in the filing. Shown with the exact quote (under 15 words), the page, and a link to the PDF. If a filing does not state it, the field is empty and says so.</dd>
          </div>
          <div>
            <dt><Tag kind="derived" /></dt>
            <dd className="mt-2 text-sm text-muted">Calculated from filed facts by a stated rule: role level, practice, days to the effective date, counts and the priority score.</dd>
          </div>
          <div>
            <dt><Tag kind="hypothesis" /></dt>
            <dd className="mt-2 text-sm text-muted">A judgement for a partner to test: why the seat matters now, questions to ask, talent pools by company type. Never names a person.</dd>
          </div>
        </dl>
      </Section>

      <Section title="Sources">
        <ul className="list-disc space-y-2 pl-5 text-ink">
          <li>
            <strong>Primary filings only.</strong> Disclosures of senior leadership changes made to the National Stock Exchange (NSE) and
            BSE under Regulation 30 of SEBI&apos;s Listing Regulations, read from the PDF each company filed.
          </li>
          <li>
            <strong>Window.</strong> Filings dated {formatDate(from)} to {formatDate(to)}: the 90 days up to the data date, {formatDate(AS_OF)}.
          </li>
          <li>
            <strong>Finding filings.</strong> NSE&apos;s public announcements feed and web searches limited to the two exchanges&apos; own sites.
            Search results only pointed to filings; no fact was taken from a search result.
          </li>
          <li>
            <strong>Polite access.</strong> One honest user agent, one request at a time with a pause, no cookies, no browser imitation.
            A block stops the run and writes a list of filings to download by hand. No block was bypassed.
          </li>
          <li>
            <strong>Not used.</strong> LinkedIn or any scraping of profiles, paid data, news articles, and any Positive Moves internal data.
          </li>
        </ul>
        <p className="mt-4 text-sm text-muted">
          {AUDIT.documents_fetched} documents fetched; {AUDIT.screened_out_at_triage} screened out at triage (no seat change, outside the
          window, or an unreadable text layer); {AUDIT.filings_reviewed} filings reviewed in full; {filings} filings and {SEATS.length} seats
          on this site.
        </p>
      </Section>

      <Section title="From filing to seat">
        <Steps
          items={[
            { title: "Fetch and fingerprint", body: "Each PDF is downloaded once and its SHA-256 hash recorded, so any later change to the document is detectable." },
            { title: "Read the text", body: "Engine A (pdfplumber) turns each page into text. Phone numbers and email addresses are removed from the stored text. The PDFs themselves stay in a local cache; the site links to the exchange's own copy." },
            { title: "Extract", body: "Every field is filled only from the text, with its page and an exact supporting quote under 15 words. A field the filing does not state is stored as empty." },
            { title: "Verify independently", body: "Engines B (pypdfium2) and C (poppler) re-read every PDF from scratch. Each field's quote, page and value must match; each result is match, mismatch or not found." },
            { title: "Correct in the open", body: "Mismatches go to a review queue. Corrections are kept apart from the first pass, each with a reason, then verified again." },
            { title: "Review record by record", body: <>Each record is approved or rejected beside its source in review.html. Current decisions are by {AUDIT.reviewed_by}; {HUMAN_SIGNOFF ? "a person has signed them off." : "a person's sign-off is pending."}</> },
            { title: "Publish only what passed", body: "The site reads only records marked VERIFIED. A build check confirms no rejected or unreviewed record reaches any page." },
          ]}
        />
      </Section>

      <Section title="Audit">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[20rem] text-sm">
            <caption className="sr-only">Audit counts from data/audit.json</caption>
            <tbody className="divide-y divide-line">
              {[
                ["Filings reviewed", `${AUDIT.filings_reviewed} (${filings} in the study, the rest kept as review tests)`],
                ["Fields checked", `${AUDIT.fields_checked_per_run} per verification run, plus ${AUDIT.context_facts_checked_per_run} extra filed facts; 2 runs`],
                ["Errors found", `${AUDIT.errors_found} in the first run: ${AUDIT.errors_found_fields} field mismatches and ${AUDIT.errors_found_record_flags} record flags`],
                ["Errors fixed", `${AUDIT.errors_fixed}, each re-verified as a match (${AUDIT.errors_fixed_now_match} of ${AUDIT.errors_fixed})`],
                ["False alarms cleared", `${AUDIT.false_positives_cleared}, with a written reason`],
                ["Records rejected", `${AUDIT.records_rejected}`],
                ["Seats verified", `${AUDIT.seats_verified} from ${AUDIT.filings_verified} filings`],
                ["Date of last review", `${formatDate(AUDIT.date_of_last_review)} by ${AUDIT.reviewed_by}; human sign-off ${AUDIT.human_signoff ? "recorded" : "pending"}`],
                [
                  "Source links checked",
                  LINK_CHECK.not_checked > 0
                    ? `${LINK_CHECK.ok} of ${LINK_CHECK.links} confirmed on ${formatDate(LINK_CHECK.checked_at.slice(0, 10))}; ${LINK_CHECK.not_checked} could not be checked`
                    : `${LINK_CHECK.ok} of ${LINK_CHECK.links} PDFs re-downloaded on ${formatDate(LINK_CHECK.checked_at.slice(0, 10))}: HTTP 200, same SHA-256, all ${LINK_CHECK.pages_cited} cited pages present`,
                ],
              ].map(([k, v]) => (
                <tr key={k}>
                  <th scope="row" className="w-48 py-2.5 pr-4 text-left align-top font-medium text-ink">{k}</th>
                  <td className="py-2.5 text-muted">{v}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-sm text-muted">Full detail, every correction and every rejection with its reason: AUDIT.md in the project.</p>
      </Section>

      <Section title="Definitions" tag="derived">
        <div className="space-y-6">
          <div>
            <h3 className="font-sans text-base font-semibold text-ink">Role level</h3>
            <p className="mt-1 text-sm text-muted">From the filed title. Rules run in order on the lower-cased title and the first match wins.</p>
            <ol className="mt-2 space-y-1.5 text-sm">
              {ROLE_RULES.map((r, i) => (
                <li key={i} className="grid gap-1 sm:grid-cols-[9rem_1fr] sm:gap-3">
                  <span className="font-medium text-ink">{i + 1}. {ROLE_LEVEL_LABEL[r.level]}</span>
                  <span className="text-muted">{r.why}</span>
                </li>
              ))}
            </ol>
          </div>
          <div>
            <h3 className="font-sans text-base font-semibold text-ink">Event type</h3>
            <dl className="mt-2 space-y-1.5 text-sm">
              {EVENT_ORDER.map((e) => (
                <div key={e} className="grid gap-1 sm:grid-cols-[9rem_1fr] sm:gap-3">
                  <dt className="font-medium text-ink">{EVENT_LABEL[e]}</dt>
                  <dd className="text-muted">{EVENT_MEANING[e]}</dd>
                </div>
              ))}
            </dl>
          </div>
          <div>
            <h3 className="font-sans text-base font-semibold text-ink">Successor status</h3>
            <dl className="mt-2 space-y-1.5 text-sm">
              {SUCCESSOR_ORDER.map((s) => (
                <div key={s} className="grid gap-1 sm:grid-cols-[9rem_1fr] sm:gap-3">
                  <dt className="font-medium text-ink">{SUCCESSOR_LABEL[s]}</dt>
                  <dd className="text-muted">{SUCCESSOR_MEANING[s]}</dd>
                </div>
              ))}
            </dl>
            <p className="mt-2 text-sm text-muted">The reason someone left is shown only as the filing states it. It is never guessed.</p>
          </div>
          <div>
            <h3 className="font-sans text-base font-semibold text-ink">Practice</h3>
            <ol className="mt-2 list-none space-y-1 text-sm text-muted">
              {PRACTICES.rules.map((r) => <li key={r}>{r}</li>)}
            </ol>
            <dl className="mt-3 space-y-1.5 text-sm">
              {PRACTICE_ORDER.map((p) => (
                <div key={p} className="grid gap-1 sm:grid-cols-[13rem_1fr] sm:gap-3">
                  <dt className="font-medium text-ink">{p}</dt>
                  <dd className="text-muted">{PRACTICES.practices[p]}</dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </Section>

      <Section id="score" title="Priority score" tag="derived">
        <p className="text-ink">
          Priority = role level + successor status + other exits at the same company + timing, out of {SCORE_CONFIG.max_points}. It is a
          transparent rule for ordering a partner&apos;s attention. <strong>It is not a probability</strong>: there is no outcome data, so
          no accuracy is claimed.
        </p>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <ScoreTable title={comps.role_level.label} rows={ROLE_LEVEL_ORDER.map((k) => [ROLE_LEVEL_LABEL[k], comps.role_level.points[k]])} />
          <ScoreTable title={comps.successor_status.label} rows={SUCCESSOR_ORDER.map((k) => [SUCCESSOR_LABEL[k], comps.successor_status.points[k]])} />
          <ScoreTable
            title={comps.company_exits.label}
            rows={comps.company_exits.bands.map((b) => [b.max === null ? `${b.min} or more` : b.min === b.max ? `${b.min}` : `${b.min} to ${b.max}`, b.points])}
          />
          <ScoreTable
            title={comps.timing.label}
            rows={[
              [`Effective in the next ${comps.timing.next_days} days (today counts)`, comps.timing.next_points],
              [`Effective in the last ${comps.timing.past_days} days`, comps.timing.past_points],
              ["Any other date, or no date stated", comps.timing.otherwise_points],
            ]}
          />
        </div>
        <div className="mt-4 space-y-2 text-sm text-muted">
          <p>
            <strong className="text-ink">Gate.</strong> An appointment that names a permanent successor is shown as &ldquo;{SCORE_CONFIG.gate.status}&rdquo; and
            ranked below every open seat, whatever its score.
          </p>
          <p>
            <strong className="text-ink">Order.</strong> Open seats first, then higher priority, then the sooner effective date, then company name.
          </p>
          <p>
            <strong className="text-ink">Worked example.</strong> The top seat,{" "}
            <Link href={`/seat/${top.seat.id}/`} className="underline underline-offset-4">{top.seat.role_title} at {top.seat.company}</Link>, scores{" "}
            {top.components.map((c) => c.points).join(" + ")} = {top.total}.
          </p>
          <ul className="list-disc space-y-1 pl-5">
            {top.components.map((c) => (
              <li key={c.key}>
                {c.label}: {c.reason} <span className="num font-semibold text-ink">{c.points}</span>
              </li>
            ))}
          </ul>
          <p>Weights live in config/score.json and the rule in lib/score.ts, a pure function covered by tests.</p>
        </div>
      </Section>

      <Section title="Known limits">
        <ul className="list-disc space-y-2 pl-5 text-ink">
          <li>Listed companies only. Private and unlisted companies do not file these disclosures and are not covered.</li>
          <li>A sample of {AUDIT.filings_verified} filings chosen to cover all eight practices, not every filing in the window.</li>
          <li>No outcome data. We do not know which seats became mandates, so the priority rule cannot be called accurate or inaccurate yet.</li>
          <li>&ldquo;Other exits at the same company&rdquo; counts only exits inside this dataset, not every exit the company filed.</li>
          <li>Role level and practice come from rules. A title the rules do not foresee can land at the wrong level.</li>
          <li>Text engines can misread tables and scans. Filings with no usable text layer were screened out rather than guessed.</li>
          <li>
            Review decisions so far are by {AUDIT.reviewed_by}. {HUMAN_SIGNOFF ? "A person has signed them off." : "A person's sign-off in review.html is still pending."}
          </li>
          <li>Companies can revise a filing later. The site reflects each PDF as fetched, identified by its SHA-256.</li>
          <li>
            BSE first serves a new filing at a temporary address and later moves it.{" "}
            {Object.keys(STABLE.links).length} links already point to the permanent, byte-identical copy
            {STABLE.pending.length > 0
              ? `; ${STABLE.pending.length} filing is too recent to have one yet, so pipeline/stable_links.py should be re-run in a few days.`
              : "."}
          </li>
        </ul>
      </Section>

      <Section title="Next phase">
        <ol className="list-decimal space-y-2 pl-5 text-ink">
          <li>Join each signal to PINE: existing relationships, off-limits and client conflicts, and past searches at the company.</li>
          <li>Compare priority with the mandates that actually followed, then tune the weights on that evidence.</li>
          <li>Run the pipeline daily on the exchange feeds, with the same verification and review before anything is shown.</li>
        </ol>
      </Section>
    </div>
  );
}

function ScoreTable({ title, rows }: { title: string; rows: [string, number][] }) {
  return (
    <table className="w-full text-sm">
      <caption className="mb-1 text-left font-semibold text-ink">{title}</caption>
      <tbody className="divide-y divide-line border-y border-line">
        {rows.map(([label, pts]) => (
          <tr key={label}>
            <td className="py-1.5 pr-3 text-muted">{label}</td>
            <td className="num py-1.5 text-right font-semibold text-ink">{pts}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
