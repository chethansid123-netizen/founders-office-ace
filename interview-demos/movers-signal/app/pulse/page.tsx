import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import { Tag } from "@/components/ui";
import { AUDIT, SEATS } from "@/lib/data";
import { FILTER_PARAMS, PRACTICE_ORDER, ROLE_LEVEL_ORDER } from "@/lib/filters";
import { formatDate, pct, ROLE_LEVEL_LABEL } from "@/lib/format";
import { countBy } from "@/lib/summary";
import type { SeatRecord } from "@/lib/types";

export const metadata: Metadata = { title: "Market pulse" };

const SMALL_SAMPLE = 5;

/** A seat counts as "no permanent successor" when the filing names none, an interim, or is unclear. */
const noPermanent = (s: SeatRecord) => s.successor_status !== "NAMED_PERMANENT";

function radarHref(param: keyof typeof FILTER_PARAMS, value: string): string {
  return `/?${new URLSearchParams({ [FILTER_PARAMS[param]]: value }).toString()}`;
}

interface BarDatum {
  label: string;
  count: number;
  href: string;
}

function ChartCard({ id, title, n, sub, children }: { id: string; title: string; n: number; sub: string; children: ReactNode }) {
  return (
    <figure aria-labelledby={`${id}-title`} className="min-w-0 rounded-xl border border-line bg-surface p-5 sm:p-6">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h2 id={`${id}-title`} className="text-xl font-semibold text-ink">{title}</h2>
          <p className="mt-1 text-sm text-muted">
            <span className="font-semibold text-ink">
              n = <span data-metric={`${id}-n`}>{n}</span>
            </span>{" "}
            verified seats · {sub}
          </p>
        </div>
        <Tag kind="derived" />
      </div>
      {children}
    </figure>
  );
}

/** Single-series horizontal bars: one hue, value at the tip, the row links to the filtered Radar. */
function Bars({ data, n }: { data: BarDatum[]; n: number }) {
  const max = Math.max(1, ...data.map((d) => d.count));
  return (
    <ul className="mt-5 space-y-1">
      {data.map((d) => (
        <li key={d.label}>
          <Link
            href={d.href}
            className="group relative grid gap-1 rounded-md px-2 py-1.5 no-underline hover:bg-surface-2 focus-visible:bg-surface-2 sm:grid-cols-[12.5rem_1fr] sm:items-center sm:gap-3"
          >
            <span className="text-sm text-ink">{d.label}</span>
            <span className="flex items-center gap-2">
              {d.count > 0 && (
                <span aria-hidden className="h-4 shrink-0 rounded-r-[4px] bg-viz-bar" style={{ width: `calc((100% - 3rem) * ${d.count / max})` }} />
              )}
              <span className="num text-sm font-semibold text-ink">
                {d.count}
                <span className="sr-only"> of {n} seats. Open these on the Radar.</span>
              </span>
            </span>
            <span
              aria-hidden
              className="pointer-events-none absolute bottom-full left-1/2 z-10 mb-1 -translate-x-1/2 whitespace-nowrap rounded-md bg-ink px-2.5 py-1 text-xs text-bg opacity-0 shadow transition-opacity group-hover:opacity-100 group-focus-visible:opacity-100"
            >
              <strong>{d.count} seats</strong> · {pct(d.count, n)} of {n} · {d.label}
            </span>
          </Link>
        </li>
      ))}
    </ul>
  );
}

function TableView({ caption, head, rows }: { caption: string; head: string[]; rows: (string | number)[][] }) {
  return (
    <details className="mt-4 text-sm">
      <summary className="cursor-pointer font-medium text-pine-2">Show as a table</summary>
      <div className="mt-2 overflow-x-auto">
        <table className="w-full min-w-[18rem]">
          <caption className="sr-only">{caption}</caption>
          <thead>
            <tr className="border-b border-line text-left text-muted">
              {head.map((h, i) => (
                <th key={h} scope="col" className={`py-1.5 pr-3 font-medium ${i > 0 ? "text-right" : ""}`}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={String(r[0])} className="border-b border-line last:border-0">
                {r.map((c, i) => (
                  <td key={i} className={`py-1.5 pr-3 ${i > 0 ? "num text-right" : "text-ink"}`}>{c}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </details>
  );
}

export default function PulsePage() {
  const n = SEATS.length;
  const filings = new Set(SEATS.map((s) => s.source_url)).size;
  const [from, to] = AUDIT.window;

  const byPractice: BarDatum[] = countBy(SEATS, (s) => s.practice, PRACTICE_ORDER)
    .map((c) => ({ label: c.label, count: c.count, href: radarHref("practice", c.label) }))
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label));

  const byRole: BarDatum[] = countBy(SEATS, (s) => s.role_level, ROLE_LEVEL_ORDER).map((c) => ({
    label: ROLE_LEVEL_LABEL[c.label as keyof typeof ROLE_LEVEL_LABEL],
    count: c.count,
    href: radarHref("roleLevel", c.label),
  }));

  const openAll = SEATS.filter(noPermanent).length;
  const share = PRACTICE_ORDER.map((p) => {
    const seats = SEATS.filter((s) => s.practice === p);
    const open = seats.filter(noPermanent).length;
    return { label: p, n: seats.length, open, ratio: seats.length ? open / seats.length : 0, href: radarHref("practice", p) };
  })
    .filter((r) => r.n > 0)
    .sort((a, b) => b.ratio - a.ratio || b.n - a.n || a.label.localeCompare(b.label));

  return (
    <div className="space-y-8">
      <header className="max-w-3xl">
        <p className="text-xs font-semibold uppercase tracking-wider text-muted">Market pulse</p>
        <h1 className="mt-2 text-4xl font-semibold leading-tight text-ink sm:text-5xl">Where senior seats are moving</h1>
        <p className="mt-4 text-lg text-muted">
          The {n} verified seats from {filings} filings dated {formatDate(from)} to {formatDate(to)}, counted three ways. Select a bar to
          open those seats on the Radar.
        </p>
      </header>

      <p role="note" className="rounded-xl border border-brass bg-brass-soft p-4 text-sm text-ink">
        <strong>Verified sample, not the whole market.</strong> Filings were chosen to cover all eight practices, not drawn at random,
        so these counts describe this sample of {n} seats only. They are not market shares or trends.
      </p>

      <div className="grid gap-6 lg:grid-cols-2">
        <ChartCard id="practice" title="Seats by practice" n={n} sub="largest first">
          <Bars data={byPractice} n={n} />
          <TableView
            caption={`Seats by practice, n = ${n}`}
            head={["Practice", "Seats", "Share of n"]}
            rows={byPractice.map((d) => [d.label, d.count, pct(d.count, n)])}
          />
        </ChartCard>

        <ChartCard id="role" title="Seats by role level" n={n} sub="most senior first">
          <Bars data={byRole} n={n} />
          <TableView
            caption={`Seats by role level, n = ${n}`}
            head={["Role level", "Seats", "Share of n"]}
            rows={byRole.map((d) => [d.label, d.count, pct(d.count, n)])}
          />
          <p className="mt-3 text-xs text-muted">Role level is derived from the filed title by the ordered rules in config/role_levels.json.</p>
        </ChartCard>
      </div>

      <ChartCard id="share" title="Share with no permanent successor named" n={n} sub="by practice, highest share first">
        <div className="mt-5 flex flex-wrap gap-x-5 gap-y-1 text-xs text-muted">
          <span className="inline-flex items-center gap-1.5"><span aria-hidden className="h-2.5 w-4 rounded-sm bg-viz-accent" /> No permanent successor: not named, interim or unclear</span>
          <span className="inline-flex items-center gap-1.5"><span aria-hidden className="h-2.5 w-4 rounded-sm bg-viz-track" /> Permanent successor named</span>
        </div>
        <ul className="mt-4 space-y-1">
          {[{ label: "All practices", n, open: openAll, ratio: openAll / n, href: "/", all: true }, ...share.map((s) => ({ ...s, all: false }))].map((r) => (
            <li key={r.label} className={r.all ? "border-b border-line pb-2" : undefined}>
              <Link
                href={r.href}
                className="group relative grid gap-1 rounded-md px-2 py-1.5 no-underline hover:bg-surface-2 focus-visible:bg-surface-2 sm:grid-cols-[16rem_1fr_9.5rem] sm:items-center sm:gap-3"
              >
                <span className={`text-sm text-ink ${r.all ? "font-semibold" : ""}`}>
                  {r.label}
                  {!r.all && r.n < SMALL_SAMPLE && <span className="ml-2 whitespace-nowrap text-xs text-muted">small sample</span>}
                </span>
                <span aria-hidden className="flex h-2.5 overflow-hidden rounded-full bg-viz-track">
                  {r.open > 0 && <span className="h-full bg-viz-accent" style={{ width: `${r.ratio * 100}%` }} />}
                </span>
                <span className="num text-sm text-ink sm:text-right">
                  <strong>{pct(r.open, r.n)}</strong> <span className="text-muted">({r.open} of {r.n})</span>
                </span>
                <span
                  aria-hidden
                  className="pointer-events-none absolute bottom-full left-1/2 z-10 mb-1 -translate-x-1/2 whitespace-nowrap rounded-md bg-ink px-2.5 py-1 text-xs text-bg opacity-0 shadow transition-opacity group-hover:opacity-100 group-focus-visible:opacity-100"
                >
                  <strong>{pct(r.open, r.n)}</strong> · {r.open} of {r.n} seats · {r.label}
                </span>
              </Link>
            </li>
          ))}
        </ul>
        <TableView
          caption={`Share of seats with no permanent successor named, by practice, n = ${n}`}
          head={["Practice", "No permanent successor", "Seats", "Share"]}
          rows={[["All practices", openAll, n, pct(openAll, n)], ...share.map((s) => [s.label, s.open, s.n, pct(s.open, s.n)])]}
        />
        <p className="mt-3 text-xs text-muted">
          Practices with fewer than {SMALL_SAMPLE} seats are marked as a small sample: there, one seat moves the share by{" "}
          {Math.round(100 / (SMALL_SAMPLE - 1))} points or more.
        </p>
      </ChartCard>
    </div>
  );
}
