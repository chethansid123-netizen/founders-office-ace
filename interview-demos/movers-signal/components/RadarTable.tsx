"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { Suspense, useMemo } from "react";
import { PriorityBar, SourceLink, StatusChip } from "@/components/ui";
import {
  ALL,
  allowedValues,
  applyFilters,
  filtersFromSearch,
  filtersToSearch,
  isFiltered,
  NO_FILTERS,
  type FilterGroups,
  type Filters,
} from "@/lib/filters";
import { EVENT_LABEL, ROLE_LEVEL_LABEL, SUCCESSOR_LABEL } from "@/lib/format";
import type { RadarRow } from "@/lib/radar";
import type { EventType, RoleLevel, SuccessorStatus } from "@/lib/types";

interface Props {
  rows: RadarRow[];
  groups: FilterGroups;
}

const CONTROLS: { key: keyof Filters; label: string; all: string; text: (v: string) => string }[] = [
  { key: "practice", label: "Practice", all: "All practices", text: (v) => v },
  { key: "roleLevel", label: "Role level", all: "All role levels", text: (v) => ROLE_LEVEL_LABEL[v as RoleLevel] },
  { key: "eventType", label: "Event type", all: "All event types", text: (v) => EVENT_LABEL[v as EventType] },
  { key: "successorStatus", label: "Successor status", all: "All successor statuses", text: (v) => SUCCESSOR_LABEL[v as SuccessorStatus] },
];

/**
 * The Radar's filters and ranked list. Filters live in the URL (?practice=…),
 * so a filtered view can be shared. The static HTML carries the full, unfiltered
 * list; the URL is applied once the page runs in the browser.
 */
export function RadarTable(props: Props) {
  return (
    <Suspense fallback={<RadarView {...props} filters={NO_FILTERS} onChange={() => {}} />}>
      <RadarWithUrl {...props} />
    </Suspense>
  );
}

function RadarWithUrl(props: Props) {
  const search = useSearchParams();
  const pathname = usePathname();
  const allowed = useMemo(() => allowedValues(props.groups), [props.groups]);
  const filters = filtersFromSearch(search.toString(), allowed);
  const onChange = (next: Filters) => {
    const qs = filtersToSearch(next);
    window.history.replaceState(null, "", qs ? `?${qs}` : pathname);
  };
  return <RadarView {...props} filters={filters} onChange={onChange} />;
}

function RadarView({ rows, groups, filters, onChange }: Props & { filters: Filters; onChange: (f: Filters) => void }) {
  const shown = useMemo(() => applyFilters(rows, filters), [rows, filters]);
  const filtered = isFiltered(filters);

  return (
    <section aria-labelledby="ranked-heading" className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-x-6 gap-y-2">
        <h2 id="ranked-heading" className="text-2xl font-semibold text-ink">Ranked seats</h2>
        <p className="text-sm text-muted">
          Priority is a transparent rule out of 100, not a probability.{" "}
          <Link href="/method/#score" className="underline underline-offset-4">How it is scored</Link>
        </p>
      </div>

      <form role="search" aria-label="Filter seats" className="grid gap-3 rounded-xl border border-line bg-surface p-4 sm:grid-cols-2 lg:grid-cols-4" onSubmit={(e) => e.preventDefault()}>
        {CONTROLS.map((c) => (
          <label key={c.key} className="flex min-w-0 flex-col gap-1 text-sm">
            <span className="font-medium text-ink">{c.label}</span>
            <select
              value={filters[c.key]}
              onChange={(e) => onChange({ ...filters, [c.key]: e.target.value })}
              className="w-full min-w-0 rounded-lg border border-line bg-bg px-3 py-2 text-ink"
            >
              <option value={ALL}>{c.all} ({rows.length})</option>
              {groups[c.key].map((o) => (
                <option key={o.value} value={o.value} disabled={o.count === 0}>
                  {c.text(o.value)} ({o.count})
                </option>
              ))}
            </select>
          </label>
        ))}
      </form>

      <div className="flex flex-wrap items-center justify-between gap-3 text-sm">
        <p aria-live="polite" className="text-muted">
          Showing <strong className="text-ink">{shown.length}</strong> of {rows.length} verified seats.
          {filtered ? " Ranks are overall ranks; filtering does not re-rank." : " Filled seats are ranked last."}
        </p>
        {filtered && (
          <button type="button" onClick={() => onChange(NO_FILTERS)} className="rounded-lg border border-line px-3 py-1.5 font-medium text-pine-2 hover:bg-surface-2">
            Clear filters
          </button>
        )}
      </div>

      {shown.length === 0 ? (
        <div className="rounded-xl border border-dashed border-line bg-surface p-8 text-center">
          <p className="font-medium text-ink">No verified seat matches these filters.</p>
          <button type="button" onClick={() => onChange(NO_FILTERS)} className="mt-3 rounded-lg border border-line px-3 py-1.5 text-sm font-medium text-pine-2 hover:bg-surface-2">
            Clear filters
          </button>
        </div>
      ) : (
        <>
          <div className="hidden overflow-hidden rounded-xl border border-line bg-surface lg:block">
            <table className="w-full text-sm">
              <caption className="sr-only">Verified leadership seats ranked by priority</caption>
              <thead className="bg-surface-2 text-left text-xs font-semibold uppercase tracking-wider text-muted">
                <tr>
                  <th scope="col" className="w-12 px-4 py-3">#</th>
                  <th scope="col" className="py-3 pr-4">Company</th>
                  <th scope="col" className="py-3 pr-4">Role</th>
                  <th scope="col" className="py-3 pr-4">Event</th>
                  <th scope="col" className="py-3 pr-4">Effective date</th>
                  <th scope="col" className="py-3 pr-4">Successor status</th>
                  <th scope="col" className="py-3 pr-4">Priority</th>
                  <th scope="col" className="py-3 pr-4">Source</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                {shown.map((r) => (
                  <tr key={r.id} data-seat={r.id} className={r.seat_filled ? "bg-surface-2/40" : undefined}>
                    <td className="num px-4 py-3 align-top text-muted">{r.rank}</td>
                    <td className="py-3 pr-4 align-top">
                      <Link
                        href={`/seat/${r.id}/`}
                        aria-label={`${r.company}: ${r.role_title}, open the seat brief`}
                        className="font-semibold text-ink underline decoration-line underline-offset-4 hover:decoration-pine-2"
                      >
                        {r.company}
                      </Link>
                      <div className="mt-0.5 text-xs text-muted">{r.practice}</div>
                    </td>
                    <td className="py-3 pr-4 align-top">
                      <div className="text-ink">{r.role_title}</div>
                      {r.person && <div className="mt-0.5 text-xs text-muted">{r.person}</div>}
                    </td>
                    <td className="py-3 pr-4 align-top text-ink">{r.event_label}</td>
                    <td className="num py-3 pr-4 align-top whitespace-nowrap text-ink">{r.effective_label}</td>
                    <td className="py-3 pr-4 align-top">
                      <StatusChip status={r.status} />
                      <div className="mt-1 text-xs text-muted">{r.successor_detail}</div>
                    </td>
                    <td className="py-3 pr-4 align-top"><PriorityBar value={r.total} muted={r.seat_filled} /></td>
                    <td className="py-3 pr-4 align-top"><SourceLink url={r.source_url} page={r.source_page} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <ol className="grid gap-3 sm:grid-cols-2 lg:hidden">
            {shown.map((r) => (
              <li key={r.id} data-seat={r.id} className="min-w-0 rounded-xl border border-line bg-surface p-4">
                <div className="flex items-start justify-between gap-3">
                  <span className="min-w-0 text-xs font-semibold uppercase tracking-wider text-muted">
                    #{r.rank} · {r.practice}
                  </span>
                  <span className="shrink-0"><PriorityBar value={r.total} muted={r.seat_filled} /></span>
                </div>
                <Link
                  href={`/seat/${r.id}/`}
                  aria-label={`${r.company}: ${r.role_title}, open the seat brief`}
                  className="wrap-any mt-2 block font-serif text-lg font-semibold text-ink underline decoration-line underline-offset-4"
                >
                  {r.company}
                </Link>
                <p className="wrap-any text-ink">{r.role_title}</p>
                {r.person && <p className="text-sm text-muted">{r.person}</p>}
                <div className="mt-3 flex flex-wrap items-center gap-x-2 gap-y-1">
                  <StatusChip status={r.status} />
                  <span className="text-xs text-muted">{r.successor_detail}</span>
                </div>
                <p className="mt-2 text-sm text-muted">
                  {r.event_label} · effective {r.effective_label}
                </p>
                <div className="mt-3 border-t border-line pt-3">
                  <SourceLink url={r.source_url} page={r.source_page} />
                </div>
              </li>
            ))}
          </ol>
        </>
      )}
    </section>
  );
}
