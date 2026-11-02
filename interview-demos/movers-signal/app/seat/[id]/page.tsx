import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Section, SourceLink, StatusChip, Tag, PriorityBar } from "@/components/ui";
import { AS_OF, getScored, HUMAN_SIGNOFF, PRACTICES, rankOf, SCORED, urlForKey } from "@/lib/data";
import { factRows } from "@/lib/brief";
import { EVENT_LABEL, exchangeOf, formatDate, ROLE_LEVEL_LABEL, sourceHref } from "@/lib/format";
import { buildHypotheses } from "@/lib/hypotheses";
import type { Evidence } from "@/lib/types";

export const dynamicParams = false;

export function generateStaticParams() {
  return SCORED.map((s) => ({ id: s.seat.id }));
}

export async function generateMetadata({ params }: { params: Promise<{ id: string }> }): Promise<Metadata> {
  const { id } = await params;
  const s = getScored(id);
  return s ? { title: `${s.seat.role_title}, ${s.seat.company}` } : {};
}

function QuoteLine({ ev, url }: { ev: Evidence; url: string }) {
  if (!ev.quote) return <p className="mt-1 text-sm text-muted">{ev.note}</p>;
  return (
    <div className="mt-1.5 text-sm">
      <q className="wrap-any italic text-muted">{ev.quote}</q>{" "}
      <SourceLink url={url} page={ev.page}>
        p.{ev.page} <span aria-hidden>↗</span>
      </SourceLink>
      {ev.note && <p className="mt-1 text-xs text-muted">{ev.note}</p>}
    </div>
  );
}

export default async function SeatPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const s = getScored(id);
  if (!s) notFound();
  const seat = s.seat;
  const h = buildHypotheses(s);
  const practice = PRACTICES.companies[seat.company];
  const verification = seat.verification;
  const checks = verification ? Object.values(verification.fields) : [];
  const matched = checks.filter((c) => c === "match").length;
  const absent = checks.filter((c) => c === "not_found").length;
  const days = s.daysToEffective;
  const href = sourceHref(seat);

  return (
    <article className="space-y-6">
      <nav aria-label="Breadcrumb" className="text-sm text-muted">
        <Link href="/" className="underline underline-offset-4">Radar</Link> <span aria-hidden>/</span> {seat.company}
      </nav>

      <header className="grid gap-5 rounded-xl border border-line bg-surface p-5 sm:p-6 lg:grid-cols-[1fr_auto]">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-muted">
            {seat.practice} · {exchangeOf(seat.source_url)}
            {seat.exchange_symbol ? `: ${seat.exchange_symbol}` : ""} · Rank {rankOf(seat.id)} of {SCORED.length}
          </p>
          <h1 className="mt-2 text-3xl font-semibold leading-tight text-ink sm:text-4xl">{seat.role_title}</h1>
          <p className="mt-1 font-serif text-xl text-pine-2">{seat.company}</p>
          <p className="mt-3 text-muted">
            {seat.person_name} · {EVENT_LABEL[seat.event_type]} · effective {formatDate(seat.effective_date)}
            {seat.effective_date_note ? ` (${seat.effective_date_note})` : ""}
          </p>
        </div>
        <div className="flex flex-row items-center gap-4 lg:flex-col lg:items-end">
          <div className="text-right">
            <div className="text-xs font-semibold uppercase tracking-wider text-muted">Priority</div>
            <div className="text-5xl font-semibold leading-none text-ink">{s.total}<span className="text-xl font-normal text-muted">/100</span></div>
          </div>
          <StatusChip status={s.status} />
        </div>
      </header>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="space-y-6 lg:col-span-2">
          <Section title="Filed facts" tag="fact">
            <dl className="divide-y divide-line">
              {factRows(seat).map((f) => (
                <div key={f.key} className="grid gap-1 py-3 sm:grid-cols-[10rem_1fr] sm:gap-4">
                  <dt className="text-sm font-medium text-muted">{f.label}</dt>
                  <dd>
                    <div className="wrap-any font-medium text-ink">{f.value ?? <span className="text-muted">Not stated in the filing</span>}</div>
                    {f.evidence && <QuoteLine ev={f.evidence} url={href} />}
                  </dd>
                </div>
              ))}
            </dl>
          </Section>

          {seat.context_facts.length > 0 && (
            <Section title="Also in the filing" tag="fact">
              <ul className="space-y-3">
                {seat.context_facts.map((c) => (
                  <li key={c.label}>
                    <span className="font-medium text-ink">{c.label}:</span> {c.value}
                    <div className="mt-1 text-sm">
                      <q className="wrap-any italic text-muted">{c.quote}</q>{" "}
                      <SourceLink url={href} page={c.page}>p.{c.page} <span aria-hidden>↗</span></SourceLink>
                    </div>
                  </li>
                ))}
              </ul>
            </Section>
          )}

          <Section title="Why this seat matters now" tag="hypothesis">
            <div className="space-y-2 text-ink">
              {h.whyNow.map((l) => <p key={l}>{l}</p>)}
            </div>
            <p className="mt-3 text-xs text-muted">Generated by the rules in config/hypotheses.json from this seat&apos;s facts. Needs a partner&apos;s review.</p>
          </Section>

          <Section title="Questions for the partner" tag="hypothesis">
            <ol className="list-decimal space-y-2 pl-5 text-ink">
              {h.questions.map((q) => <li key={q}>{q}</li>)}
            </ol>
          </Section>

          <Section title="Talent pools to map" tag="hypothesis">
            <p className="mb-2 text-sm text-muted">Company types only, for this seat ({h.functionLabel}). No individuals are named.</p>
            <ul className="list-disc space-y-1.5 pl-5 text-ink">
              {h.pools.map((p) => <li key={p}>{p}</li>)}
            </ul>
          </Section>
        </div>

        <aside className="space-y-6">
          <Section title="Priority breakdown" tag="derived">
            <table className="w-full text-sm">
              <tbody className="divide-y divide-line">
                {s.components.map((c) => (
                  <tr key={c.key}>
                    <td className="py-2.5 pr-2 align-top">
                      <div className="font-medium text-ink">{c.label}</div>
                      <div className="text-muted">{c.reason}</div>
                    </td>
                    <td className="num py-2.5 text-right align-top font-semibold whitespace-nowrap">{c.points} <span className="font-normal text-muted">/ {c.max}</span></td>
                  </tr>
                ))}
                <tr>
                  <td className="pt-3 font-semibold text-ink">Priority</td>
                  <td className="num pt-3 text-right"><PriorityBar value={s.total} /></td>
                </tr>
              </tbody>
            </table>
            {s.seatFilled && (
              <p className="mt-3 rounded-lg bg-surface-2 p-3 text-sm text-ink">
                Gate applied after scoring: an appointment with a permanent successor is shown as <strong>Seat filled</strong> and ranked below open seats.
              </p>
            )}
            <p className="mt-3 text-xs text-muted">A transparent priority rule, not a probability. There is no outcome data, so no accuracy is claimed. <Link href="/method/#score" className="underline">How it works</Link></p>
          </Section>

          <Section title="Derived" tag="derived">
            <dl className="space-y-3 text-sm">
              <div>
                <dt className="font-medium text-ink">Practice: {seat.practice}</dt>
                <dd className="text-muted">
                  {practice?.pe_basis ?? `Main line of business: ${practice?.sector ?? "not classified"}.`}
                  {practice?.evidence?.map((e) => (
                    <span key={e.quote} className="mt-1 block">
                      <q className="italic">{e.quote}</q>{" "}
                      {urlForKey(e.source_key) && <SourceLink url={urlForKey(e.source_key)!} page={e.page}>p.{e.page} ↗</SourceLink>}
                    </span>
                  ))}
                </dd>
              </div>
              <div>
                <dt className="font-medium text-ink">Role level: {ROLE_LEVEL_LABEL[seat.role_level]}</dt>
                <dd className="text-muted">From the filed title by config/role_levels.json: {verification?.reasons.role_level?.replace(/^rule gives \w+ /, "") ?? ""}</dd>
              </div>
              <div>
                <dt className="font-medium text-ink">Days to effective date</dt>
                <dd className="text-muted">
                  {days === null ? "No date stated" : days === 0 ? `0 (effective on the as-of date, ${formatDate(AS_OF)})` : days > 0 ? `${days} days after ${formatDate(AS_OF)}` : `${-days} days before ${formatDate(AS_OF)}`}
                </dd>
              </div>
              <div>
                <dt className="font-medium text-ink">Other exits at this company (12 months, this dataset)</dt>
                <dd className="text-muted">
                  {s.otherExits.length === 0
                    ? "None"
                    : s.otherExits.map((o) => (
                        <Link key={o.id} href={`/seat/${o.id}/`} className="block underline underline-offset-4">
                          {o.role_title} · {formatDate(o.effective_date)}
                        </Link>
                      ))}
                </dd>
              </div>
            </dl>
          </Section>

          <Section title="Before outreach">
            <ul className="space-y-3 text-sm">
              {[
                ["Off-limits and client conflict check", "Needs PINE access"],
                ["Existing relationship check in PINE", "Needs PINE access"],
                ["Prior search history check in PINE", "Needs PINE access"],
                ["Human approval", "Pending a partner's sign-off"],
              ].map(([label, state]) => (
                <li key={label} className="flex items-start gap-3">
                  <span aria-hidden className="mt-0.5 h-4 w-4 shrink-0 rounded border border-line bg-surface-2" />
                  <span>
                    <span className="block font-medium text-ink">{label}</span>
                    <span className="block text-muted">{state}</span>
                  </span>
                </li>
              ))}
            </ul>
            <p className="mt-3 text-xs text-muted">Not run here. These checks need Positive Moves&apos; own systems; no result is simulated.</p>
          </Section>

          <Section title="Source and review">
            <dl className="space-y-2 text-sm">
              <div>
                <dt className="font-medium text-ink">Filing</dt>
                <dd className="text-muted">{exchangeOf(seat.source_url)} filing dated {formatDate(seat.filing_date)} · <SourceLink url={href} page={seat.source_page} /></dd>
              </div>
              {seat.source_sha256 && (
                <div>
                  <dt className="font-medium text-ink">SHA-256 of the PDF</dt>
                  <dd className="wrap-any font-mono text-xs text-muted">{seat.source_sha256}</dd>
                </div>
              )}
              <div>
                <dt className="font-medium text-ink">Verification</dt>
                <dd className="text-muted">
                  Re-read by two independent text engines: {matched} of {checks.length} checks match, {absent} confirmed absent.
                  {(seat.review_overrides ?? []).map((o) => (
                    <span key={o.field} className="mt-1 block">Cleared at review ({o.field}): {o.reason}</span>
                  ))}
                </dd>
              </div>
              {(seat.corrections ?? []).length > 0 && (
                <div>
                  <dt className="font-medium text-ink">Corrected after verification</dt>
                  <dd className="text-muted">
                    {seat.corrections!.map((c, i) => (
                      <span key={i} className="block">{c.field}: {c.reason}</span>
                    ))}
                  </dd>
                </div>
              )}
              <div>
                <dt className="font-medium text-ink">Review</dt>
                <dd className="text-muted">
                  {seat.review_status} by {seat.reviewed_by} on {formatDate(seat.reviewed_at)}.{" "}
                  {HUMAN_SIGNOFF ? "Human sign-off recorded." : "Human sign-off pending in review.html."}
                </dd>
              </div>
            </dl>
            <div className="mt-3 flex flex-wrap gap-2">
              <Tag kind="fact" /> <Tag kind="derived" /> <Tag kind="hypothesis" />
            </div>
          </Section>
        </aside>
      </div>
    </article>
  );
}
