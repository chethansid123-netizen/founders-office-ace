import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export const Route = createFileRoute("/sales-dashboard")({
  component: SalesDashboard,
  head: () => ({
    meta: [
      { title: "ShortLoop — Sales Command Center" },
      {
        name: "description",
        content:
          "Founder's Office sales command center for ShortLoop — the AI conversation OS for auto dealerships. Illustrative sample data.",
      },
    ],
  }),
});

/* ------------------------------------------------------------------ */
/*  DESIGN TOKENS — chart colors (validated categorical palette).      */
/*  Run: node scripts/validate_palette.js on the dataviz skill.        */
/*  Text/labels use ink tokens, never the series color.                */
/* ------------------------------------------------------------------ */
const C = {
  ink: "#15161d",
  muted: "#6b6a64",
  grid: "#e4e3dc",
  axis: "#c3c2b7",
  lime: "oklch(0.88 0.20 115)",
  good: "#0a8f0a",
  bad: "#c93b3b",
  // categorical slots (fixed order, never cycled)
  blue: "#2a78d6",
  aqua: "#1baf7a",
  yellow: "#eda100",
  green: "#008300",
  violet: "#4a3aa7",
  red: "#e34948",
  // sequential blue ramp (ordinal, funnel — no lighter than step 250)
  ramp: ["#184f95", "#256abf", "#2a78d6", "#3987e5", "#5598e7", "#86b6ef"],
};

/* ------------------------------------------------------------------ */
/*  ILLUSTRATIVE SAMPLE DATA — modelled to ShortLoop's business.       */
/*  US auto-dealer AI conversation OS · land-and-expand SaaS motion.   */
/*  All figures are directional dummy data for demonstration.          */
/* ------------------------------------------------------------------ */

const AS_OF = "Jul 12, 2026";

const HEADLINE = [
  { k: "$3.4M", v: "Annual Recurring Revenue" },
  { k: "214", v: "Dealer rooftops live" },
  { k: "23", v: "Dealer groups" },
  { k: "128%", v: "Net revenue retention" },
];

const KPIS = [
  {
    label: "New ARR · Q2 FY26",
    value: "$842K",
    delta: "+18% QoQ",
    pos: true,
    sub: "112% of $750K target",
  },
  {
    label: "Pipeline Coverage · Q3",
    value: "3.4×",
    delta: "+0.6×",
    pos: true,
    sub: "$2.6M open vs $760K target",
  },
  {
    label: "Win Rate",
    value: "26%",
    delta: "+3 pts",
    pos: true,
    sub: "Qualified → closed won",
  },
  {
    label: "Avg ACV / Rooftop",
    value: "$21.4K",
    delta: "+$1.8K",
    pos: true,
    sub: "Annual subscription",
  },
  {
    label: "Sales Cycle",
    value: "46 days",
    delta: "−6 days",
    pos: true,
    sub: "Demo → closed won",
  },
  {
    label: "Pilot → Paid",
    value: "61%",
    delta: "−4 pts",
    pos: false,
    sub: "30-day pilot conversion",
  },
];

// New ARR by month ($K) — split New Logo vs Expansion, with target line.
const TREND = [
  { m: "Jul", newLogo: 105, expansion: 58, target: 150 },
  { m: "Aug", newLogo: 120, expansion: 62, target: 160 },
  { m: "Sep", newLogo: 138, expansion: 70, target: 170 },
  { m: "Oct", newLogo: 132, expansion: 80, target: 180 },
  { m: "Nov", newLogo: 150, expansion: 88, target: 190 },
  { m: "Dec", newLogo: 168, expansion: 95, target: 200 },
  { m: "Jan", newLogo: 155, expansion: 102, target: 210 },
  { m: "Feb", newLogo: 176, expansion: 110, target: 220 },
  { m: "Mar", newLogo: 190, expansion: 120, target: 230 },
  { m: "Apr", newLogo: 205, expansion: 128, target: 240 },
  { m: "May", newLogo: 220, expansion: 140, target: 250 },
  { m: "Jun", newLogo: 238, expansion: 152, target: 250 },
];

// Open-pipeline funnel — current snapshot.
const FUNNEL = [
  { stage: "Prospecting", accounts: 240, value: 6.1, conv: null },
  { stage: "Discovery", accounts: 118, value: 3.9, conv: 49 },
  { stage: "Live Demo", accounts: 64, value: 2.4, conv: 54 },
  { stage: "Pilot · 30-day", accounts: 33, value: 1.5, conv: 52 },
  { stage: "Proposal / Procurement", accounts: 19, value: 0.9, conv: 58 },
  { stage: "Closed Won · QTD", accounts: 8, value: 0.31, conv: 42 },
];

// Channel mix — TTM. arr in $K.
const CHANNELS = [
  { name: "Outbound (SDR)", arr: 1020, deals: 46, win: 22, cycle: 52, color: C.blue },
  { name: "Partner (DMS / OEM)", arr: 860, deals: 28, win: 34, cycle: 41, color: C.aqua },
  { name: "Inbound", arr: 580, deals: 31, win: 29, cycle: 38, color: C.yellow },
  { name: "Events (NADA · 20 Groups)", arr: 410, deals: 14, win: 25, cycle: 58, color: C.green },
  { name: "Referral / Expansion", arr: 520, deals: 22, win: 41, cycle: 33, color: C.violet },
];

const REPS = [
  { name: "Marcus Bell", role: "Sr AE", attain: 118, arr: 232, pipe: 640, win: 31, cycle: 42 },
  { name: "Sarah Kim", role: "AE · Groups", attain: 108, arr: 180, pipe: 720, win: 24, cycle: 61 },
  { name: "Priya Raman", role: "AE", attain: 104, arr: 188, pipe: 580, win: 28, cycle: 45 },
  { name: "Diego Alvarez", role: "AE", attain: 96, arr: 164, pipe: 510, win: 26, cycle: 48 },
  {
    name: "Tom Whitfield",
    role: "AE · ramping",
    attain: 71,
    arr: 78,
    pipe: 300,
    win: 21,
    cycle: 44,
  },
];

const ACTIVITY = [
  { k: "4,820", v: "Dials logged" },
  { k: "612", v: "Conversations" },
  { k: "96", v: "Demos booked" },
  { k: "33", v: "Pilots started" },
];

const ACCOUNTS = [
  {
    group: "Sunbelt Auto Group",
    rooftops: 42,
    region: "Texas",
    brand: "Multi-brand",
    stage: "Pilot",
    acv: 840,
    next: "Group rollout review · Jul 18",
  },
  {
    group: "Summit Dealer Group",
    rooftops: 27,
    region: "Southeast",
    brand: "Toyota / Honda",
    stage: "Discovery",
    acv: 560,
    next: "Exec demo scheduled",
  },
  {
    group: "Prestige Motor Collective",
    rooftops: 18,
    region: "West",
    brand: "Luxury / import",
    stage: "Proposal",
    acv: 390,
    next: "MSA in legal",
  },
  {
    group: "Pacific Rim Dealers",
    rooftops: 15,
    region: "Northwest",
    brand: "Import",
    stage: "Live Demo",
    acv: 310,
    next: "Pilot proposal sent",
  },
  {
    group: "Coastal Auto Partners",
    rooftops: 12,
    region: "Southeast",
    brand: "Multi-brand",
    stage: "Pilot",
    acv: 250,
    next: "Day-21 pilot check-in",
  },
  {
    group: "Lakeside Automotive",
    rooftops: 9,
    region: "Midwest",
    brand: "Domestic",
    stage: "Live Demo",
    acv: 190,
    next: "ROI review",
  },
  {
    group: "Heartland Motors",
    rooftops: 6,
    region: "Midwest",
    brand: "Ford / GM",
    stage: "Proposal",
    acv: 130,
    next: "Procurement",
  },
];

const REGIONS = [
  { region: "Texas / Southwest", rooftops: 58, arr: 940, pipe: 1180 },
  { region: "Southeast", rooftops: 47, arr: 720, pipe: 890 },
  { region: "West", rooftops: 41, arr: 690, pipe: 760 },
  { region: "Midwest", rooftops: 38, arr: 560, pipe: 640 },
  { region: "Northeast", rooftops: 30, arr: 490, pipe: 520 },
];

// The value story reps sell — customer impact from the service-lane wedge.
const VALUE = [
  { k: "1.24M", v: "Customer calls handled (TTM)" },
  { k: "338K", v: "After-hours & missed calls recovered" },
  { k: "92K", v: "Service repair orders booked" },
  { k: "$18.6M", v: "Customer RO revenue influenced" },
  { k: "+$7.2K", v: "Avg incremental RO / rooftop / mo" },
];

const STRATEGY = [
  {
    tag: "Double down",
    tone: "good",
    points: [
      "Partner + Referral channels — 34% & 41% win rates, shortest cycles (41d / 33d). Lean into DMS-native co-sell (Tekion, CDK, Reynolds).",
      "Land-and-expand into dealer groups — NRR at 128%; a single rooftop is a wedge into 20–40 more.",
    ],
  },
  {
    tag: "Focus",
    tone: "focus",
    points: [
      "Convert the 33 active pilots to paid before Q3 close — the single biggest ARR lever on the board.",
      "Expand marquee logos into their parent groups: Sunbelt (42 rooftops) and Summit (27) alone are ~$1.4M of expansion ACV.",
    ],
  },
  {
    tag: "Fix",
    tone: "warn",
    points: [
      "Pilot → paid slipped 4 pts to 61% — procurement drag at group level and onboarding time-to-value. Tighten the 30-day pilot playbook.",
      "Outbound win rate (22%) and Events cycle (58d) lag — sharpen ICP to high service-call-volume rooftops.",
    ],
  },
  {
    tag: "Build",
    tone: "build",
    points: [
      "OEM co-sell motion — the path from group to OEM-endorsed rollout.",
      "In-rep ROI calculator wired to live call/RO data; sales-lane product wedge beyond service.",
    ],
  },
  {
    tag: "Drop / leave out",
    tone: "bad",
    points: [
      "Single independent rooftops with no DMS integration — low fit, high churn, no expansion path.",
      "Sub-scale used-car lots below the service-call-volume threshold — they don't hit payback.",
    ],
  },
];

/* ------------------------------------------------------------------ */
/*  HELPERS                                                            */
/* ------------------------------------------------------------------ */
function useMounted() {
  const [m, setM] = useState(false);
  useEffect(() => setM(true), []);
  return m;
}

const usd = (k: number) => (k >= 1000 ? `$${(k / 1000).toFixed(1)}M` : `$${k}K`);

const toneMap: Record<string, { bar: string; chip: string }> = {
  good: { bar: C.green, chip: "bg-[#008300] text-white" },
  focus: { bar: C.blue, chip: "bg-[#2a78d6] text-white" },
  warn: { bar: C.yellow, chip: "bg-[#eda100] text-[#15161d]" },
  build: { bar: C.violet, chip: "bg-[#4a3aa7] text-white" },
  bad: { bar: C.red, chip: "bg-[#c93b3b] text-white" },
};

/* ------------------------------------------------------------------ */
/*  SMALL COMPONENTS                                                   */
/* ------------------------------------------------------------------ */
function SectionHead({
  n,
  kicker,
  title,
  note,
}: {
  n: string;
  kicker: string;
  title: string;
  note?: string;
}) {
  return (
    <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        <span className="tag">
          {n} · {kicker}
        </span>
        <h2 className="mt-3 font-display text-3xl md:text-4xl leading-tight">{title}</h2>
      </div>
      {note && <p className="max-w-md text-sm text-muted-foreground leading-relaxed">{note}</p>}
    </div>
  );
}

type TooltipEntry = { name?: string; value?: number; color?: string; fill?: string };
function ChartTooltip({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: TooltipEntry[];
  label?: string;
}) {
  if (!active || !payload?.length) return null;
  return (
    <div className="border border-foreground bg-card px-3 py-2 shadow-[4px_4px_0_var(--ink)]">
      <div className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
        {label}
      </div>
      {payload.map((p) => (
        <div key={p.name} className="mt-1 flex items-center gap-2 text-sm tabular-nums">
          <span className="inline-block h-2.5 w-2.5" style={{ background: p.color || p.fill }} />
          <span className="text-muted-foreground">{p.name}</span>
          <span className="ml-auto font-medium">${p.value}K</span>
        </div>
      ))}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  PAGE                                                               */
/* ------------------------------------------------------------------ */
function SalesDashboard() {
  const mounted = useMounted();
  const funnelMax = FUNNEL[0].accounts;
  const channelMax = Math.max(...CHANNELS.map((c) => c.arr));
  const regionMax = Math.max(...REGIONS.map((r) => r.pipe));

  return (
    <main className="min-h-screen bg-background text-foreground">
      {/* NAV */}
      <header className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-[1400px] items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <span className="grid h-8 w-8 place-items-center bg-foreground font-display text-lg text-background">
              S
            </span>
            <div className="leading-tight">
              <div className="font-display text-lg">ShortLoop</div>
              <div className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                Sales Command Center
              </div>
            </div>
          </div>
          <div className="hidden items-center gap-3 md:flex">
            <span className="tag">Data as of {AS_OF}</span>
            <span className="tag bg-accent-lime border-foreground">● Illustrative sample data</span>
            <Link to="/" className="tag bg-foreground text-background border-foreground">
              ← Portfolio
            </Link>
          </div>
        </div>
      </header>

      {/* HERO / HEADLINE */}
      <section className="border-b border-border grain">
        <div className="mx-auto max-w-[1400px] px-6 py-12 md:py-16">
          <div className="grid gap-8 md:grid-cols-12 md:items-end">
            <div className="md:col-span-7">
              <span className="tag">Founder's Office · Revenue Review</span>
              <h1 className="mt-4 font-display text-[clamp(2.4rem,6vw,4.5rem)] leading-[0.95]">
                Turning missed calls into{" "}
                <span className="relative italic">
                  repair orders
                  <span className="absolute -bottom-1 left-0 right-0 -z-10 h-3 bg-accent-lime" />
                </span>
                .
              </h1>
              <p className="mt-5 max-w-xl text-lg leading-relaxed text-muted-foreground">
                ShortLoop is the AI conversation OS for auto dealerships — service-lane inbound
                calls, unbooked slots and dormant records converted into revenue, automatically.
                This is how the sales engine that sells it is performing.
              </p>
            </div>
            <div className="md:col-span-5">
              <div className="grid grid-cols-2 border-l border-t border-foreground">
                {HEADLINE.map((s) => (
                  <div key={s.v} className="border-b border-r border-foreground p-5">
                    <div className="font-display text-4xl md:text-5xl">{s.k}</div>
                    <div className="mt-1 font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                      {s.v}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* KPI STRIP */}
      <section className="border-b border-border bg-secondary/40">
        <div className="mx-auto max-w-[1400px] px-6 py-10">
          <SectionHead
            n="01"
            kicker="The scoreboard"
            title="Six numbers the founder reads first."
            note="Quarter-close view. Green deltas beat plan; the amber one is the watch-item — flagged below."
          />
          <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
            {KPIS.map((k) => (
              <div key={k.label} className="border border-foreground bg-card p-5 hover-lift">
                <div className="font-mono text-[10px] uppercase leading-tight tracking-widest text-muted-foreground">
                  {k.label}
                </div>
                <div className="mt-3 font-display text-4xl tabular-nums">{k.value}</div>
                <div
                  className="mt-2 inline-flex items-center gap-1 font-mono text-xs tabular-nums"
                  style={{ color: k.pos ? C.good : C.bad }}
                >
                  {k.pos ? "▲" : "▼"} {k.delta}
                </div>
                <div className="mt-2 text-xs leading-snug text-muted-foreground">{k.sub}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* BOOKINGS TREND */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-[1400px] px-6 py-14">
          <SectionHead
            n="02"
            kicker="Bookings"
            title="New ARR is compounding — and expansion is carrying more of it."
            note="Monthly New ARR ($K), split New Logo vs Expansion, against the monthly target line. Land-and-expand is the story: the blue base is steady, the green expansion layer keeps thickening."
          />
          <div className="border border-foreground bg-card p-4 md:p-6">
            {/* legend */}
            <div className="mb-4 flex flex-wrap items-center gap-5 font-mono text-xs uppercase tracking-wider">
              <span className="flex items-center gap-2">
                <span className="inline-block h-3 w-3" style={{ background: C.blue }} /> New logo
              </span>
              <span className="flex items-center gap-2">
                <span className="inline-block h-3 w-3" style={{ background: C.aqua }} /> Expansion
              </span>
              <span className="flex items-center gap-2">
                <span
                  className="inline-block h-3 w-5 border-t-2 border-dashed"
                  style={{ borderColor: C.ink }}
                />{" "}
                Target
              </span>
            </div>
            <div style={{ height: 340 }}>
              {mounted ? (
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart
                    data={TREND}
                    margin={{ top: 8, right: 8, left: -8, bottom: 0 }}
                    barCategoryGap="22%"
                  >
                    <CartesianGrid vertical={false} stroke={C.grid} />
                    <XAxis
                      dataKey="m"
                      tick={{ fill: C.muted, fontSize: 12 }}
                      tickLine={false}
                      axisLine={{ stroke: C.axis }}
                    />
                    <YAxis
                      tick={{ fill: C.muted, fontSize: 12 }}
                      tickLine={false}
                      axisLine={false}
                      tickFormatter={(v) => `$${v}K`}
                      width={56}
                    />
                    <Tooltip content={<ChartTooltip />} cursor={{ fill: "rgba(0,0,0,0.04)" }} />
                    <Bar
                      dataKey="newLogo"
                      name="New logo"
                      stackId="a"
                      fill={C.blue}
                      radius={[0, 0, 0, 0]}
                    />
                    <Bar
                      dataKey="expansion"
                      name="Expansion"
                      stackId="a"
                      fill={C.aqua}
                      radius={[3, 3, 0, 0]}
                    />
                    <Line
                      dataKey="target"
                      name="Target"
                      stroke={C.ink}
                      strokeWidth={2}
                      strokeDasharray="5 4"
                      dot={false}
                    />
                  </ComposedChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full w-full animate-pulse bg-secondary/60" />
              )}
            </div>
          </div>
        </div>
      </section>

      {/* FUNNEL + CHANNELS */}
      <section className="border-b border-border bg-secondary/40">
        <div className="mx-auto max-w-[1400px] px-6 py-14">
          <div className="grid gap-10 lg:grid-cols-2">
            {/* FUNNEL */}
            <div>
              <SectionHead n="03" kicker="Pipeline" title="Where the deals are." />
              <div className="border border-foreground bg-card p-6">
                <div className="space-y-3">
                  {FUNNEL.map((f, i) => (
                    <div key={f.stage}>
                      <div className="flex items-baseline justify-between text-sm">
                        <span className="font-medium">{f.stage}</span>
                        <span className="tabular-nums text-muted-foreground">
                          {f.accounts} accts · {usd(f.value * 1000)}
                        </span>
                      </div>
                      <div className="mt-1.5 h-7 w-full bg-secondary">
                        <div
                          className="flex h-7 items-center justify-end px-2"
                          style={{
                            width: `${Math.max((f.accounts / funnelMax) * 100, 6)}%`,
                            background: C.ramp[i],
                          }}
                        >
                          {f.conv != null && (
                            <span className="font-mono text-[10px] tabular-nums text-white">
                              {f.conv}%→
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <p className="mt-4 border-t border-border pt-3 font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                  % = stage-to-stage conversion · pilot → paid is the leak to fix
                </p>
              </div>
            </div>

            {/* CHANNELS */}
            <div>
              <SectionHead n="04" kicker="Sourcing" title="How sales gets made." />
              <div className="border border-foreground bg-card p-6">
                <div className="space-y-4">
                  {CHANNELS.map((c) => (
                    <div key={c.name}>
                      <div className="flex items-baseline justify-between text-sm">
                        <span className="flex items-center gap-2 font-medium">
                          <span className="inline-block h-3 w-3" style={{ background: c.color }} />
                          {c.name}
                        </span>
                        <span className="tabular-nums font-medium">{usd(c.arr)}</span>
                      </div>
                      <div className="mt-1.5 h-4 w-full bg-secondary">
                        <div
                          className="h-4"
                          style={{ width: `${(c.arr / channelMax) * 100}%`, background: c.color }}
                        />
                      </div>
                      <div className="mt-1 flex gap-4 font-mono text-[10px] uppercase tracking-wider tabular-nums text-muted-foreground">
                        <span>{c.deals} deals</span>
                        <span>{c.win}% win</span>
                        <span>{c.cycle}d cycle</span>
                      </div>
                    </div>
                  ))}
                </div>
                <p className="mt-4 border-t border-border pt-3 text-xs leading-snug text-muted-foreground">
                  <span className="font-medium text-foreground">Read:</span> Outbound drives volume,
                  but <span className="font-medium text-foreground">Partner (34%)</span> and{" "}
                  <span className="font-medium text-foreground">Referral (41%)</span> win more per
                  swing and close faster. That's where to add fuel.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* REPS */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-[1400px] px-6 py-14">
          <SectionHead
            n="05"
            kicker="The team"
            title="What every rep is doing — and how they're pacing."
            note="Attainment against individual quota. Sarah carries the group book (long cycle, high pipeline); Tom is ramping. Marcus is the model to clone."
          />
          <div className="overflow-x-auto border border-foreground bg-card">
            <table className="w-full min-w-[720px] text-sm">
              <thead>
                <tr className="border-b border-foreground text-left font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                  <th className="p-4">Rep</th>
                  <th className="p-4">Quota attainment</th>
                  <th className="p-4 text-right">Closed ARR</th>
                  <th className="p-4 text-right">Open pipeline</th>
                  <th className="p-4 text-right">Win rate</th>
                  <th className="p-4 text-right">Avg cycle</th>
                </tr>
              </thead>
              <tbody>
                {REPS.map((r) => (
                  <tr key={r.name} className="border-b border-border last:border-0">
                    <td className="p-4">
                      <div className="font-medium">{r.name}</div>
                      <div className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                        {r.role}
                      </div>
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-3">
                        <div className="h-2.5 w-40 max-w-[40vw] bg-secondary">
                          <div
                            className="h-2.5"
                            style={{
                              width: `${Math.min(r.attain, 100)}%`,
                              background:
                                r.attain >= 100 ? C.good : r.attain >= 85 ? C.blue : C.yellow,
                            }}
                          />
                        </div>
                        <span className="tabular-nums font-medium">{r.attain}%</span>
                      </div>
                    </td>
                    <td className="p-4 text-right tabular-nums font-medium">{usd(r.arr)}</td>
                    <td className="p-4 text-right tabular-nums text-muted-foreground">
                      {usd(r.pipe)}
                    </td>
                    <td className="p-4 text-right tabular-nums">{r.win}%</td>
                    <td className="p-4 text-right tabular-nums text-muted-foreground">
                      {r.cycle}d
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {/* activity strip */}
          <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
            {ACTIVITY.map((a) => (
              <div key={a.v} className="border border-border bg-card p-5">
                <div className="font-display text-3xl tabular-nums">{a.k}</div>
                <div className="mt-1 font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                  {a.v}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ACCOUNTS + REGIONS */}
      <section className="border-b border-border bg-secondary/40">
        <div className="mx-auto max-w-[1400px] px-6 py-14">
          <div className="grid gap-10 lg:grid-cols-12">
            {/* ACCOUNTS */}
            <div className="min-w-0 lg:col-span-8">
              <SectionHead n="06" kicker="Who we're talking to" title="Top accounts in play." />
              <div className="overflow-x-auto border border-foreground bg-card">
                <table className="w-full min-w-[640px] text-sm">
                  <thead>
                    <tr className="border-b border-foreground text-left font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                      <th className="p-4">Dealer group</th>
                      <th className="p-4 text-right">Rooftops</th>
                      <th className="p-4">Region</th>
                      <th className="p-4">Stage</th>
                      <th className="p-4 text-right">ACV</th>
                      <th className="p-4">Next step</th>
                    </tr>
                  </thead>
                  <tbody>
                    {ACCOUNTS.map((a) => (
                      <tr key={a.group} className="border-b border-border last:border-0">
                        <td className="p-4">
                          <div className="font-medium">{a.group}</div>
                          <div className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                            {a.brand}
                          </div>
                        </td>
                        <td className="p-4 text-right tabular-nums font-medium">{a.rooftops}</td>
                        <td className="p-4 text-muted-foreground">{a.region}</td>
                        <td className="p-4">
                          <span className="tag border-foreground text-[10px]">{a.stage}</span>
                        </td>
                        <td className="p-4 text-right tabular-nums font-medium">{usd(a.acv)}</td>
                        <td className="p-4 text-xs text-muted-foreground">{a.next}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* REGIONS */}
            <div className="lg:col-span-4">
              <SectionHead n="07" kicker="Coverage" title="By region." />
              <div className="border border-foreground bg-card p-6">
                <div className="space-y-4">
                  {REGIONS.map((r) => (
                    <div key={r.region}>
                      <div className="flex items-baseline justify-between text-sm">
                        <span className="font-medium">{r.region}</span>
                        <span className="tabular-nums text-muted-foreground">
                          {r.rooftops} live
                        </span>
                      </div>
                      <div className="mt-1.5 h-4 w-full bg-secondary">
                        <div
                          className="h-4"
                          style={{ width: `${(r.pipe / regionMax) * 100}%`, background: C.blue }}
                        />
                      </div>
                      <div className="mt-1 flex gap-4 font-mono text-[10px] uppercase tracking-wider tabular-nums text-muted-foreground">
                        <span>{usd(r.arr)} ARR</span>
                        <span>{usd(r.pipe)} pipe</span>
                      </div>
                    </div>
                  ))}
                </div>
                <p className="mt-4 border-t border-border pt-3 font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                  Bar = open pipeline · Texas leads on both
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CUSTOMER VALUE PROOF */}
      <section className="border-b border-border bg-foreground text-background">
        <div className="mx-auto max-w-[1400px] px-6 py-14">
          <div className="mb-8">
            <span className="tag border-background">08 · The value we sell</span>
            <h2 className="mt-3 font-display text-3xl md:text-4xl">
              Why dealers say yes — the ROI reps put on the table.
            </h2>
          </div>
          <div className="grid grid-cols-2 gap-px bg-background/20 md:grid-cols-5">
            {VALUE.map((s) => (
              <div key={s.v} className="bg-foreground p-5">
                <div className="font-display text-3xl md:text-4xl text-accent-lime">{s.k}</div>
                <div className="mt-2 font-mono text-[10px] uppercase leading-snug tracking-widest opacity-80">
                  {s.v}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* STRATEGY BOARD */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-[1400px] px-6 py-14">
          <SectionHead
            n="09"
            kicker="The call"
            title="Focus · Fix · Double-down · Build · Drop."
            note="The founder's-office read: not just what happened, but what we do about it next quarter."
          />
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-5">
            {STRATEGY.map((s) => {
              const t = toneMap[s.tone];
              return (
                <div
                  key={s.tag}
                  className="flex flex-col border border-foreground bg-card hover-lift"
                >
                  <div className="border-b-4 p-4" style={{ borderColor: t.bar }}>
                    <span className={`tag border-transparent ${t.chip}`}>{s.tag}</span>
                  </div>
                  <ul className="flex-1 space-y-3 p-4">
                    {s.points.map((p, i) => (
                      <li
                        key={i}
                        className="relative pl-4 text-sm leading-relaxed text-muted-foreground"
                      >
                        <span
                          className="absolute left-0 top-2 h-1.5 w-1.5"
                          style={{ background: t.bar }}
                        />
                        {p}
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* METHODOLOGY / FOOTER */}
      <section className="bg-secondary/40">
        <div className="mx-auto max-w-[1400px] px-6 py-14">
          <div className="grid gap-8 md:grid-cols-12">
            <div className="md:col-span-4">
              <span className="tag">10 · Notes</span>
              <h2 className="mt-3 font-display text-3xl">How this was built.</h2>
            </div>
            <div className="space-y-4 text-sm leading-relaxed text-muted-foreground md:col-span-8">
              <p>
                <span className="font-medium text-foreground">Data:</span> every figure here is{" "}
                <span className="font-medium text-foreground">illustrative sample data</span>,
                modelled to ShortLoop's real business — a US, DMS-native AI conversation OS for auto
                dealerships with a land-and-expand motion (rooftop → group → OEM). Totals are
                internally consistent (channel ARR ties to the $3.4M headline; regional rooftops sum
                to 214) so the dashboard reads as one coherent quarter, not scattered numbers.
              </p>
              <p>
                <span className="font-medium text-foreground">Design:</span> built on the same
                system as the portfolio (Instrument Serif display, JetBrains Mono labels, hard
                borders, lime accent). Charts use a colorblind-safe categorical palette validated
                with a contrast/CVD script — series color carries identity, text stays in ink
                tokens, and every low-contrast series ships a direct label.
              </p>
              <p>
                <span className="font-medium text-foreground">Stack:</span> React 19 · TanStack
                Router · Recharts · Tailwind v4. One route, one file, no backend — swap the data
                constants at the top for live CRM exports (HubSpot / Salesforce) and it's
                production-ready.
              </p>
            </div>
          </div>
          <div className="mt-10 flex flex-wrap items-center justify-between gap-4 border-t border-foreground pt-6 font-mono text-xs uppercase tracking-widest text-muted-foreground">
            <span>ShortLoop · Sales Command Center · {AS_OF}</span>
            <span>Illustrative sample data · built for founder review</span>
          </div>
        </div>
      </section>
    </main>
  );
}
