import type { ReactNode } from "react";
import { exchangeOf, pdfLink } from "@/lib/format";

export type Provenance = "fact" | "derived" | "hypothesis";

const TAG_TEXT: Record<Provenance, string> = { fact: "Filed fact", derived: "Derived", hypothesis: "Hypothesis" };
const TAG_TITLE: Record<Provenance, string> = {
  fact: "Directly stated in the filing",
  derived: "Calculated from filed facts by a stated rule",
  hypothesis: "Generated judgement that needs human review",
};
const TAG_CLASS: Record<Provenance, string> = {
  fact: "bg-pine-soft text-pine-2 border-transparent",
  derived: "bg-slate-soft text-slate border-transparent",
  hypothesis: "bg-brass-soft text-brass border-brass border-dashed",
};

export function Tag({ kind }: { kind: Provenance }) {
  return (
    <span
      title={TAG_TITLE[kind]}
      className={`inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wide ${TAG_CLASS[kind]}`}
    >
      <span aria-hidden className="h-1.5 w-1.5 rounded-full bg-current" />
      {TAG_TEXT[kind]}
    </span>
  );
}

const STATUS_CLASS: Record<string, string> = {
  "Open seat": "bg-brass-soft text-brass",
  "Successor unclear": "bg-slate-soft text-slate",
  "Interim in seat": "bg-slate-soft text-slate",
  "Successor named": "bg-pine-soft text-pine-2",
  "Seat filled": "bg-surface-2 text-muted",
};

export function StatusChip({ status }: { status: string }) {
  return (
    <span className={`inline-block whitespace-nowrap rounded-full px-2.5 py-0.5 text-xs font-semibold ${STATUS_CLASS[status] ?? "bg-surface-2 text-muted"}`}>
      {status}
    </span>
  );
}

/** Priority as a meter: the fill is the score, the track a lighter step of the same hue. */
export function PriorityBar({ value, max = 100, muted = false }: { value: number; max?: number; muted?: boolean }) {
  const w = Math.max(0, Math.min(100, (value / max) * 100));
  return (
    <span className="flex items-center gap-2">
      <span className="num w-7 text-right font-semibold text-ink">
        {value}
        <span className="sr-only"> out of {max}</span>
      </span>
      <span aria-hidden className="relative h-2 w-16 overflow-hidden rounded-full bg-viz-bar-track">
        <span className={`absolute inset-y-0 left-0 rounded-full ${muted ? "bg-muted" : "bg-viz-bar"}`} style={{ width: `${w}%` }} />
      </span>
    </span>
  );
}

export function SourceLink({ url, page, children }: { url: string; page?: number | null; children?: ReactNode }) {
  return (
    <a
      href={pdfLink(url, page)}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-1 whitespace-nowrap text-sm font-medium text-pine-2 underline decoration-line underline-offset-4 hover:decoration-pine-2"
    >
      {children ?? (
        <>
          {exchangeOf(url)} PDF{page ? ` · p.${page}` : ""} <span aria-hidden>↗</span>
        </>
      )}
    </a>
  );
}

export function Section({ title, tag, children, id }: { title: string; tag?: Provenance; children: ReactNode; id?: string }) {
  return (
    <section id={id} className="rounded-xl border border-line bg-surface p-5 sm:p-6">
      <div className="mb-4 flex flex-wrap items-center gap-3">
        <h2 className="text-xl font-semibold text-ink">{title}</h2>
        {tag && <Tag kind={tag} />}
      </div>
      {children}
    </section>
  );
}

/**
 * A KPI tile. The value is always computed by the caller from verified records;
 * `metric` names it so scripts/check-site.mjs can recompute and compare.
 */
export function Stat({ value, label, note, metric }: { value: number; label: string; note: ReactNode; metric: string }) {
  return (
    <div className="rounded-xl border border-line bg-surface p-5">
      <div className="flex items-start justify-between gap-3">
        <div data-metric={metric} className="text-4xl font-semibold leading-none text-ink">{value}</div>
        <Tag kind="derived" />
      </div>
      <div className="mt-3 font-medium text-ink">{label}</div>
      <div className="mt-1 text-sm text-muted">{note}</div>
    </div>
  );
}
