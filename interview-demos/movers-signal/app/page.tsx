import Link from "next/link";
import { RadarTable } from "@/components/RadarTable";
import { Stat, Tag } from "@/components/ui";
import { AS_OF, AUDIT, HUMAN_SIGNOFF, SCORED, SEATS } from "@/lib/data";
import { filterOptions } from "@/lib/filters";
import { addDays, formatDate, pct } from "@/lib/format";
import { toRadarRow } from "@/lib/radar";
import { computeSummary } from "@/lib/summary";

export default function RadarPage() {
  // Every number on this page is computed here from the verified records.
  const summary = computeSummary(SEATS, AS_OF);
  const rows = SCORED.map((s, i) => toRadarRow(s, i + 1));
  const groups = filterOptions(SEATS);
  const [from, to] = AUDIT.window;

  return (
    <div className="space-y-10">
      <header className="max-w-3xl">
        <p className="text-xs font-semibold uppercase tracking-wider text-muted">Radar</p>
        <h1 className="mt-2 text-4xl font-semibold leading-tight text-ink sm:text-5xl">Leadership seats before the mandate</h1>
        <p className="mt-4 text-lg text-muted">
          <span data-metric="seats">{summary.seats}</span> senior seats opening or changing hands, read from{" "}
          <span data-metric="filings">{summary.filings}</span> NSE and BSE filings dated {formatDate(from)} to {formatDate(to)}. Every
          fact links to the page of the filing it came from. Open a seat for its brief.
        </p>
        <ul aria-label="How to read the labels" className="mt-4 flex flex-wrap items-center gap-x-5 gap-y-2 text-sm text-muted">
          <li className="inline-flex items-center gap-2"><Tag kind="fact" /> stated in a filing</li>
          <li className="inline-flex items-center gap-2"><Tag kind="derived" /> calculated by a stated rule</li>
          <li className="inline-flex items-center gap-2"><Tag kind="hypothesis" /> a judgement for a partner to test</li>
        </ul>
      </header>

      <section aria-label="Summary" className="grid gap-4 sm:grid-cols-3">
        <Stat
          metric="noPermanentSuccessor"
          value={summary.noPermanentSuccessor}
          label="Seats with no permanent successor named"
          note={`${pct(summary.noPermanentSuccessor, summary.seats)} of ${summary.seats} seats. The filing names no successor, an interim, or is unclear.`}
        />
        <Stat
          metric="topSeats"
          value={summary.topSeats}
          label="CEO, MD and C-suite seats"
          note={`Of ${summary.seats} seats. Role level comes from the filed title by a fixed rule.`}
        />
        <Stat
          metric="next45"
          value={summary.next45}
          label={`Changes effective in the next ${summary.next45Days} days`}
          note={`Effective date from ${formatDate(AS_OF)} to ${formatDate(addDays(AS_OF, summary.next45Days))}, as stated in the filing.`}
        />
      </section>

      <RadarTable rows={rows} groups={groups} />

      <aside className="rounded-xl border border-line bg-surface-2 p-5 text-sm text-muted">
        <p>
          A verified sample of listed companies, not the whole market. Records were checked by two independent text engines and a
          second reader; {HUMAN_SIGNOFF ? "a person has signed off the review." : "a person's sign-off of that review is still pending."}{" "}
          <Link href="/method/" className="font-medium text-pine-2 underline underline-offset-4">Method and limits</Link>
        </p>
      </aside>
    </div>
  );
}
