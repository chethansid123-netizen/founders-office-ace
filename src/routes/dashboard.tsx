import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export const Route = createFileRoute("/dashboard")({
  component: Dashboard,
});

/* ------------------------------------------------------------------ */
/*  BRAND PALETTE  (ink + reserved lime accent + sequential gray ramp) */
/* ------------------------------------------------------------------ */
const INK = "#1a1c22";
const LIME = "#c4ec13";
const MUTED = "#6b6f78";
const GRID = "#e4e2da";
// sequential single-hue ramp (light -> dark) for the funnel — monotonic lightness
const RAMP = ["#d7d7d5", "#adb0b6", "#83868f", "#4e525c", INK];

/* ------------------------------------------------------------------ */
/*  PROJECTION MODEL — driver-based, bottom-up.                        */
/*  All figures in ₹ Lakhs internally. Clearly a plan, not booked.     */
/* ------------------------------------------------------------------ */
const MONTHLY = [
  { name: "Now", cum: 0, inc: 0, mrr: 22 },
  { name: "M1", cum: 30, inc: 30, mrr: 27 },
  { name: "M2", cum: 75, inc: 45, mrr: 33 },
  { name: "M3", cum: 135, inc: 60, mrr: 40 },
  { name: "M4", cum: 210, inc: 75, mrr: 47 },
  { name: "M5", cum: 310, inc: 100, mrr: 52 },
  { name: "M6", cum: 440, inc: 130, mrr: 58 },
];

const LEVERS = {
  6: [
    { key: "New business", v: 180 },
    { key: "Expansion / upsell", v: 90 },
    { key: "Pipeline acceleration", v: 80 },
    { key: "Retention saved", v: 50 },
    { key: "Partnerships", v: 40 },
  ],
  4: [
    { key: "New business", v: 88 },
    { key: "Expansion / upsell", v: 40 },
    { key: "Pipeline acceleration", v: 45 },
    { key: "Retention saved", v: 22 },
    { key: "Partnerships", v: 15 },
  ],
};

const FUNNEL = {
  6: [
    { k: "Leads sourced", v: 320 },
    { k: "Qualified", v: 145 },
    { k: "Demos run", v: 82 },
    { k: "Proposals", v: 46 },
    { k: "Closed–won", v: 27 },
  ],
  4: [
    { k: "Leads sourced", v: 190 },
    { k: "Qualified", v: 84 },
    { k: "Demos run", v: 46 },
    { k: "Proposals", v: 24 },
    { k: "Closed–won", v: 13 },
  ],
};

const HEAD = {
  6: { impactCr: 4.4, exitMrr: 58, mrrDelta: 164, nrr: 112, logos: 27, cycle: -22 },
  4: { impactCr: 2.1, exitMrr: 47, mrrDelta: 114, nrr: 108, logos: 13, cycle: -14 },
};

const OPS = [
  { k: "Founder hours reclaimed / wk", to: 12, suffix: "h", meter: 0.8 },
  { k: "Board reports & sales decks", to: 18, suffix: "", meter: 0.9 },
  { k: "SOPs & playbooks standardised", to: 9, suffix: "", meter: 0.6 },
  { k: "Avg. response time", to: -40, suffix: "%", meter: 0.62, good: true },
  { k: "Weekly pipeline reviewed", to: 7, prefix: "₹", suffix: "Cr+", meter: 0.72 },
];

const MILESTONES = [
  {
    day: "Day 30",
    title: "Revenue baseline + full pipeline audit",
    metric: "₹30L",
    note: "Instrument every deal · single source of truth",
    status: "Live",
  },
  {
    day: "Day 60",
    title: "Pricing & packaging v2 shipped",
    metric: "₹75L",
    note: "Cumulative · ACV lift on new logos",
    status: "On track",
  },
  {
    day: "Day 90",
    title: "First partnership / channel signed",
    metric: "₹1.35Cr",
    note: "Cumulative · new revenue channel live",
    status: "On track",
  },
  {
    day: "Day 120",
    title: "4-Month milestone",
    metric: "₹2.1Cr",
    note: "Run-rate ₹47L MRR · +114%",
    status: "Target",
    flag: true,
  },
  {
    day: "Day 150",
    title: "Expansion / upsell motion online",
    metric: "₹3.1Cr",
    note: "Cumulative · NRR crosses 110%",
    status: "Target",
  },
  {
    day: "Day 180",
    title: "6-Month milestone",
    metric: "₹4.4Cr",
    note: "Exit MRR ₹58L · +164%",
    status: "Target",
    flag: true,
  },
];

const ASSUMPTIONS = [
  ["Starting MRR", "₹22L (₹2.6Cr ARR)"],
  ["Blended ACV", "₹6.6L / year"],
  ["Win rate on qualified", "~19%"],
  ["Gross monthly churn held", "< 2%"],
  ["Model type", "Bottom-up · driver-based"],
  ["Status", "Projection — not booked revenue"],
];

/* ------------------------------------------------------------------ */
/*  HOOKS                                                              */
/* ------------------------------------------------------------------ */
function useInView<T extends HTMLElement>(once = true) {
  const ref = useRef<T>(null);
  const [seen, setSeen] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(
      ([e]) => {
        if (e.isIntersecting) {
          setSeen(true);
          if (once) io.disconnect();
        } else if (!once) {
          setSeen(false);
        }
      },
      { threshold: 0.25 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, [once]);
  return [ref, seen] as const;
}

function CountUp({
  to,
  decimals = 0,
  prefix = "",
  suffix = "",
  className,
  duration = 1100,
}: {
  to: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
  className?: string;
  duration?: number;
}) {
  const [ref, seen] = useInView<HTMLSpanElement>(false);
  const [val, setVal] = useState(0);
  useEffect(() => {
    if (!seen) return;
    let raf = 0;
    const start = performance.now();
    const from = 0;
    const tick = (now: number) => {
      const p = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setVal(from + (to - from) * eased);
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [seen, to, duration]);
  const shown = val.toLocaleString("en-IN", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
  return (
    <span ref={ref} className={className}>
      {prefix}
      {shown}
      {suffix}
    </span>
  );
}

function Reveal({
  children,
  className = "",
  delay = 0,
}: {
  children: React.ReactNode;
  className?: string;
  delay?: number;
}) {
  const [ref, seen] = useInView<HTMLDivElement>(true);
  return (
    <div
      ref={ref}
      className={className}
      style={{
        opacity: seen ? 1 : 0,
        transform: seen ? "translateY(0)" : "translateY(18px)",
        transition: `opacity .6s cubic-bezier(.2,.8,.2,1) ${delay}ms, transform .6s cubic-bezier(.2,.8,.2,1) ${delay}ms`,
      }}
    >
      {children}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  SHARED PIECES                                                      */
/* ------------------------------------------------------------------ */
type TooltipEntry = { value: number; name?: string; color?: string; fill?: string };
type ChartTooltipProps = {
  active?: boolean;
  payload?: TooltipEntry[];
  label?: string | number;
  fmt?: (v: number) => string;
};

function ChartTooltip({ active, payload, label, fmt }: ChartTooltipProps) {
  if (!active || !payload?.length) return null;
  return (
    <div className="border-2 border-foreground bg-card px-3 py-2 font-mono text-xs shadow-[4px_4px_0_var(--ink)]">
      {label != null && (
        <div className="uppercase tracking-widest text-muted-foreground">{label}</div>
      )}
      {payload.map((p, i) => (
        <div key={i} className="mt-1 flex items-center gap-2">
          <span
            className="inline-block h-2 w-2 border border-foreground"
            style={{ background: p.color || p.fill }}
          />
          <span className="font-semibold">{fmt ? fmt(p.value) : p.value}</span>
          {p.name && <span className="text-muted-foreground">{p.name}</span>}
        </div>
      ))}
    </div>
  );
}

const lakhFmt = (v: number) => (v >= 100 ? `₹${(v / 100).toFixed(2)}Cr` : `₹${Math.round(v)}L`);

function SectionHead({
  n,
  kicker,
  title,
  blurb,
}: {
  n: string;
  kicker: string;
  title: string;
  blurb?: string;
}) {
  return (
    <div className="mb-8 grid gap-4 md:grid-cols-12 md:items-end">
      <div className="md:col-span-7">
        <span className="tag">
          {n} · {kicker}
        </span>
        <h2 className="mt-3 font-display text-4xl leading-[0.95] md:text-5xl">{title}</h2>
      </div>
      {blurb && (
        <p className="text-sm leading-relaxed text-muted-foreground md:col-span-5">{blurb}</p>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  PAGE                                                               */
/* ------------------------------------------------------------------ */
function Dashboard() {
  const [horizon, setHorizon] = useState<4 | 6>(6);
  const h = HEAD[horizon];
  const months = horizon === 4 ? MONTHLY.slice(0, 5) : MONTHLY;
  const levers = LEVERS[horizon];
  const leverMax = Math.max(...levers.map((l) => l.v));
  const funnel = FUNNEL[horizon];
  const funnelTop = funnel[0].v;

  return (
    <main className="min-h-screen bg-background text-foreground">
      {/* HEADER */}
      <header className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-4">
          <Link to="/" className="font-display text-xl">
            ← Chethan<span className="text-muted-foreground">.N</span>
          </Link>
          <div className="flex items-center gap-2 font-mono text-[11px] uppercase tracking-widest">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[var(--accent-lime)] opacity-75" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-[var(--accent-lime)] ring-1 ring-foreground" />
            </span>
            <span className="hidden sm:inline">Live projection</span>
          </div>
          <a
            href="mailto:chethansid123@gmail.com"
            className="tag border-foreground bg-foreground text-background"
          >
            Hire me →
          </a>
        </div>
      </header>

      {/* HERO — NORTH STAR */}
      <section className="grain relative overflow-hidden border-b border-border">
        <div className="mx-auto max-w-7xl px-6 py-14 md:py-20">
          <div className="grid gap-10 md:grid-cols-12 md:items-end">
            <div className="md:col-span-8">
              <div className="flex flex-wrap items-center gap-3">
                <span className="tag">Chethan N × Shortloop</span>
                <span className="tag border-foreground bg-accent-lime">
                  Founder's Office · Revenue Plan
                </span>
              </div>
              <div className="mt-6 font-mono text-xs uppercase tracking-[0.2em] text-muted-foreground">
                North-Star metric · Cumulative revenue impact
              </div>
              <h1 className="mt-2 font-display text-[clamp(3.5rem,11vw,9rem)] leading-[0.85]">
                <CountUp to={h.impactCr} decimals={1} prefix="₹" suffix="Cr" />
                <span className="align-top text-accent-lime">.</span>
              </h1>
              <p className="mt-4 max-w-xl text-lg leading-relaxed text-muted-foreground">
                Projected revenue I'd drive at <em>Shortloop</em> in my first{" "}
                <strong className="text-foreground">{horizon} months</strong> — modelled bottom-up
                across five levers, from a <strong className="text-foreground">₹22L</strong>{" "}
                starting MRR to an exit run-rate of{" "}
                <strong className="text-foreground">₹{h.exitMrr}L</strong>.
              </p>

              {/* HORIZON TOGGLE */}
              <div className="mt-7 inline-flex border-2 border-foreground">
                {([4, 6] as const).map((opt) => (
                  <button
                    key={opt}
                    onClick={() => setHorizon(opt)}
                    className={`px-5 py-3 font-mono text-xs uppercase tracking-widest transition-colors ${
                      horizon === opt
                        ? "bg-foreground text-background"
                        : "bg-transparent hover:bg-secondary"
                    } ${opt === 4 ? "border-r-2 border-foreground" : ""}`}
                  >
                    {opt}-Month {opt === 4 ? "Sprint" : "Horizon"}
                  </button>
                ))}
              </div>
            </div>

            {/* North-star mini spark */}
            <div className="md:col-span-4">
              <div className="border-2 border-foreground bg-card p-5">
                <div className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
                  Cumulative build-up
                </div>
                <div className="mt-1 font-display text-3xl">
                  {lakhFmt(months[months.length - 1].cum)}
                </div>
                <div className="mt-3 h-24">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={months} margin={{ top: 4, right: 4, bottom: 0, left: 4 }}>
                      <defs>
                        <linearGradient id="spark" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor={LIME} stopOpacity={0.9} />
                          <stop offset="100%" stopColor={LIME} stopOpacity={0.1} />
                        </linearGradient>
                      </defs>
                      <Area
                        type="monotone"
                        dataKey="cum"
                        stroke={INK}
                        strokeWidth={2}
                        fill="url(#spark)"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-1 flex justify-between font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                  <span>Now</span>
                  <span>M{horizon}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* KPI ROW — SUCCESS METRIC DECOMPOSED */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-7xl px-6 pt-10">
          <span className="tag">The success metric, decomposed</span>
        </div>
        <div className="mx-auto mt-6 grid max-w-7xl grid-cols-2 border-t border-border md:grid-cols-4 xl:grid-cols-5">
          {[
            {
              label: "Revenue impact",
              node: <CountUp to={h.impactCr} decimals={1} prefix="₹" suffix="Cr" />,
              sub: `over ${horizon} months`,
              big: true,
            },
            {
              label: "Exit MRR run-rate",
              node: <CountUp to={h.exitMrr} prefix="₹" suffix="L" />,
              sub: `+${h.mrrDelta}% vs today`,
              up: true,
            },
            {
              label: "Net revenue retention",
              node: <CountUp to={h.nrr} suffix="%" />,
              sub: "expansion > churn",
              up: true,
            },
            {
              label: "New logos closed",
              node: <CountUp to={h.logos} />,
              sub: "qualified → won",
              up: true,
            },
            {
              label: "Sales-cycle time",
              node: <CountUp to={h.cycle} suffix="%" />,
              sub: "faster to close",
              up: true,
            },
          ].map((k, i) => (
            <div
              key={k.label}
              className={`border-b border-border p-6 md:p-7 ${i < 4 ? "md:border-r" : ""} border-border ${
                i === 4 ? "col-span-2 xl:col-span-1" : ""
              }`}
            >
              <div className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
                {k.label}
              </div>
              <div className="mt-2 font-display text-4xl md:text-5xl">{k.node}</div>
              <div className="mt-2 flex items-center gap-1.5 font-mono text-[11px] uppercase tracking-widest">
                {k.up && <span className="text-foreground">▲</span>}
                <span className="text-muted-foreground">{k.sub}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 01 — REVENUE BUILD-UP */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-7xl px-6 py-16 md:py-20">
          <SectionHead
            n="01"
            kicker="Revenue build-up"
            title="How the number compounds, month by month."
            blurb="Cumulative revenue impact against the two milestone gates. The bars show what each individual month contributes; the line is the running total the North-Star metric tracks."
          />
          <Reveal className="border-2 border-foreground bg-card p-4 md:p-6">
            <div className="h-[340px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={months} margin={{ top: 16, right: 16, bottom: 8, left: 8 }}>
                  <defs>
                    <linearGradient id="build" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor={LIME} stopOpacity={0.55} />
                      <stop offset="100%" stopColor={LIME} stopOpacity={0.04} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke={GRID} vertical={false} />
                  <XAxis
                    dataKey="name"
                    tickLine={false}
                    axisLine={{ stroke: INK }}
                    tick={{ fontSize: 12, fill: MUTED }}
                  />
                  <YAxis
                    tickLine={false}
                    axisLine={false}
                    width={52}
                    tick={{ fontSize: 11, fill: MUTED }}
                    tickFormatter={(v) => (v >= 100 ? `${v / 100}Cr` : `${v}L`)}
                  />
                  <Tooltip
                    content={<ChartTooltip fmt={lakhFmt} />}
                    cursor={{ stroke: INK, strokeWidth: 1 }}
                  />
                  <ReferenceLine
                    x="M4"
                    stroke={INK}
                    strokeDasharray="4 4"
                    label={{
                      value: "4-mo · ₹2.1Cr",
                      position: "insideTopLeft",
                      fontSize: 10,
                      fill: INK,
                    }}
                  />
                  {horizon === 6 && (
                    <ReferenceLine
                      x="M6"
                      stroke={INK}
                      strokeDasharray="4 4"
                      label={{
                        value: "6-mo · ₹4.4Cr",
                        position: "insideTopRight",
                        fontSize: 10,
                        fill: INK,
                      }}
                    />
                  )}
                  <Area
                    type="monotone"
                    dataKey="cum"
                    name="Cumulative"
                    stroke={INK}
                    strokeWidth={2.5}
                    fill="url(#build)"
                    dot={{ r: 3, fill: INK }}
                    activeDot={{ r: 6, fill: LIME, stroke: INK, strokeWidth: 2 }}
                    animationDuration={1200}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </Reveal>
        </div>
      </section>

      {/* 02 — WHERE THE REVENUE COMES FROM */}
      <section className="border-b border-border bg-secondary/40">
        <div className="mx-auto max-w-7xl px-6 py-16 md:py-20">
          <SectionHead
            n="02"
            kicker="Revenue by lever"
            title="Where every rupee comes from."
            blurb="Five levers a founder's-office operator actually controls. New business leads, but expansion, faster pipeline, saved churn and partnerships compound the total."
          />
          <div className="grid gap-8 md:grid-cols-12">
            <Reveal className="md:col-span-7">
              <div className="border-2 border-foreground bg-card p-4 md:p-6">
                <div className="h-[320px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={levers}
                      layout="vertical"
                      margin={{ top: 4, right: 56, bottom: 4, left: 8 }}
                    >
                      <CartesianGrid stroke={GRID} horizontal={false} />
                      <XAxis type="number" hide />
                      <YAxis
                        type="category"
                        dataKey="key"
                        width={130}
                        tickLine={false}
                        axisLine={false}
                        tick={{ fontSize: 12, fill: INK }}
                      />
                      <Tooltip
                        content={<ChartTooltip fmt={lakhFmt} />}
                        cursor={{ fill: "rgba(0,0,0,0.04)" }}
                      />
                      <Bar
                        dataKey="v"
                        name="Impact"
                        radius={[0, 4, 4, 0]}
                        barSize={26}
                        animationDuration={1100}
                        label={{
                          position: "right",
                          formatter: lakhFmt,
                          fontSize: 11,
                          fill: INK,
                          fontFamily: "monospace",
                        }}
                      >
                        {levers.map((l, i) => (
                          <Cell
                            key={i}
                            fill={l.v === leverMax ? LIME : INK}
                            stroke={INK}
                            strokeWidth={l.v === leverMax ? 2 : 0}
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </Reveal>
            <div className="flex flex-col gap-3 md:col-span-5">
              {levers.map((l, i) => {
                const pct = Math.round((l.v / levers.reduce((s, x) => s + x.v, 0)) * 100);
                return (
                  <Reveal
                    key={l.key}
                    delay={i * 60}
                    className="flex items-center justify-between border-2 border-foreground bg-card p-4"
                  >
                    <div>
                      <div className="font-display text-xl">{l.key}</div>
                      <div className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
                        {pct}% of total
                      </div>
                    </div>
                    <div className="font-display text-2xl">{lakhFmt(l.v)}</div>
                  </Reveal>
                );
              })}
            </div>
          </div>
        </div>
      </section>

      {/* 03 — MRR TRAJECTORY */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-7xl px-6 py-16 md:py-20">
          <SectionHead
            n="03"
            kicker="Run-rate trajectory"
            title="The recurring engine, climbing."
            blurb="Monthly recurring revenue is the compounding asset. This is the run-rate the plan lifts from ₹22L to ₹58L — a durable +164% by month six."
          />
          <Reveal className="border-2 border-foreground bg-card p-4 md:p-6">
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={months} margin={{ top: 16, right: 24, bottom: 8, left: 8 }}>
                  <CartesianGrid stroke={GRID} vertical={false} />
                  <XAxis
                    dataKey="name"
                    tickLine={false}
                    axisLine={{ stroke: INK }}
                    tick={{ fontSize: 12, fill: MUTED }}
                  />
                  <YAxis
                    tickLine={false}
                    axisLine={false}
                    width={44}
                    domain={[0, 64]}
                    tick={{ fontSize: 11, fill: MUTED }}
                    tickFormatter={(v) => `₹${v}L`}
                  />
                  <Tooltip
                    content={<ChartTooltip fmt={(v: number) => `₹${v}L MRR`} />}
                    cursor={{ stroke: INK, strokeWidth: 1 }}
                  />
                  <Line
                    type="monotone"
                    dataKey="mrr"
                    name="MRR run-rate"
                    stroke={INK}
                    strokeWidth={2.5}
                    dot={{ r: 4, fill: "#fff", stroke: INK, strokeWidth: 2 }}
                    activeDot={{ r: 7, fill: LIME, stroke: INK, strokeWidth: 2 }}
                    animationDuration={1200}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </Reveal>
        </div>
      </section>

      {/* 04 — PIPELINE FUNNEL */}
      <section className="border-b border-border bg-secondary/40">
        <div className="mx-auto max-w-7xl px-6 py-16 md:py-20">
          <SectionHead
            n="04"
            kicker="Pipeline funnel"
            title="The engine behind the closes."
            blurb="Revenue is an output — this is the input. Conversion at each stage is where an operator earns the number, not by hoping for more leads."
          />
          <div className="grid gap-3 md:grid-cols-5">
            {funnel.map((f, i) => {
              const w = Math.round((f.v / funnelTop) * 100);
              const conv = i === 0 ? 100 : Math.round((f.v / funnel[i - 1].v) * 100);
              return (
                <Reveal key={f.k} delay={i * 70} className="border-2 border-foreground bg-card p-4">
                  <div className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
                    {f.k}
                  </div>
                  <div className="mt-1 font-display text-3xl">
                    <CountUp to={f.v} />
                  </div>
                  <div className="mt-3 h-2 w-full bg-secondary">
                    <div
                      className="h-full"
                      style={{
                        width: `${w}%`,
                        background: i === funnel.length - 1 ? LIME : RAMP[i],
                        outline: `1px solid ${INK}`,
                      }}
                    />
                  </div>
                  {i > 0 && (
                    <div className="mt-2 font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                      {conv}% step conversion
                    </div>
                  )}
                </Reveal>
              );
            })}
          </div>
        </div>
      </section>

      {/* 05 — OPERATING KPIs (LEADING INDICATORS) */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-7xl px-6 py-16 md:py-20">
          <SectionHead
            n="05"
            kicker="Leading indicators"
            title="The inputs I control every week."
            blurb="Lagging revenue is downstream of operating discipline. These are the weekly habits that move the number — the part that's fully in my hands from day one."
          />
          <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-5">
            {OPS.map((o, i) => (
              <Reveal
                key={o.k}
                delay={i * 60}
                className="flex flex-col justify-between border-2 border-foreground bg-card p-5 hover-lift"
              >
                <div className="font-mono text-[11px] uppercase leading-snug tracking-widest text-muted-foreground">
                  {o.k}
                </div>
                <div className="mt-4 font-display text-4xl">
                  <CountUp to={o.to} prefix={o.prefix || ""} suffix={o.suffix} />
                </div>
                <div className="mt-3 h-1.5 w-full bg-secondary">
                  <div
                    className="h-full bg-foreground"
                    style={{ width: `${Math.round(o.meter * 100)}%` }}
                  />
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* 06 — MILESTONE PLAN */}
      <section className="border-b border-border bg-foreground text-background">
        <div className="mx-auto max-w-7xl px-6 py-16 md:py-20">
          <div className="mb-10">
            <span className="tag border-background">06 · The plan</span>
            <h2 className="mt-3 font-display text-4xl md:text-6xl">
              30 → 180 days, gated by revenue.
            </h2>
          </div>
          <div className="divide-y divide-background/20 border-y-2 border-background/30">
            {MILESTONES.map((m, i) => (
              <Reveal
                key={m.day}
                delay={i * 40}
                className={`grid grid-cols-12 items-center gap-4 px-2 py-6 md:px-4 ${m.flag ? "bg-accent-lime/10" : ""}`}
              >
                <div className="col-span-3 font-mono text-xs uppercase tracking-widest opacity-70 md:col-span-2">
                  {m.day}
                </div>
                <div className="col-span-9 md:col-span-6">
                  <div
                    className={`font-display text-2xl leading-tight ${m.flag ? "text-accent-lime" : ""}`}
                  >
                    {m.title}
                  </div>
                  <div className="text-sm opacity-70">{m.note}</div>
                </div>
                <div className="col-span-7 col-start-4 md:col-span-2 md:col-start-auto">
                  <span
                    className={`inline-block px-3 py-1.5 font-mono text-[10px] uppercase tracking-widest ${
                      m.status === "Live"
                        ? "bg-accent-lime text-foreground"
                        : m.status === "On track"
                          ? "border border-background/50"
                          : "border border-background/30 opacity-70"
                    }`}
                  >
                    {m.status}
                  </span>
                </div>
                <div className="col-span-5 text-right font-display text-2xl md:col-span-2">
                  {m.metric}
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* 07 — ASSUMPTIONS (TRANSPARENCY) */}
      <section className="border-b border-border bg-secondary/40">
        <div className="mx-auto max-w-7xl px-6 py-16 md:py-20">
          <SectionHead
            n="07"
            kicker="The model, in the open"
            title="Every number has a stated assumption."
            blurb="A dashboard is only trustworthy if you can see the engine. These are the inputs behind the projection — swap them for Shortloop's real figures and the whole board re-computes."
          />
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {ASSUMPTIONS.map((a) => (
              <div
                key={a[0]}
                className="flex items-center justify-between border-2 border-foreground bg-card p-5"
              >
                <span className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
                  {a[0]}
                </span>
                <span className="font-display text-xl">{a[1]}</span>
              </div>
            ))}
          </div>
          <p className="mt-6 max-w-3xl text-sm leading-relaxed text-muted-foreground">
            <strong className="text-foreground">Note.</strong> Figures are a driver-based projection
            built to demonstrate how I'd instrument and grow revenue in a founder's office — not
            booked or audited results. Give me Shortloop's baseline MRR, ACV and funnel and I'll
            rebuild this on real data in a day.
          </p>
        </div>
      </section>

      {/* CTA */}
      <section className="grain bg-accent-lime">
        <div className="mx-auto max-w-7xl px-6 py-20 text-center md:py-28">
          <span className="tag">Let's build</span>
          <h2 className="mt-5 font-display text-5xl leading-[0.9] md:text-8xl">
            Put me on <span className="italic">Shortloop's</span> number.
          </h2>
          <p className="mx-auto mt-6 max-w-xl text-lg">
            This is the plan on paper. Give me the seat and I'll make it the reporting you check
            every Monday.
          </p>
          <div className="mt-9 flex flex-wrap justify-center gap-4">
            <a
              href="mailto:chethansid123@gmail.com"
              className="hover-lift inline-block bg-foreground px-7 py-4 font-mono text-sm uppercase tracking-widest text-background"
            >
              chethansid123@gmail.com
            </a>
            <Link
              to="/"
              className="hover-lift inline-block border-2 border-foreground px-7 py-4 font-mono text-sm uppercase tracking-widest"
            >
              ← Back to portfolio
            </Link>
          </div>
        </div>
        <footer className="border-t-2 border-foreground">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 font-mono text-xs uppercase tracking-widest">
            <span>© 2026 Chethan N</span>
            <span>Revenue plan · Projection</span>
          </div>
        </footer>
      </section>
    </main>
  );
}
