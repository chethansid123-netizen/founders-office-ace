import { createFileRoute } from "@tanstack/react-router";
import portrait from "@/assets/chethan.jpeg";

import pCleanup from "@/assets/personal/cleanup.jpeg";
import pCoats from "@/assets/personal/coats.jpeg";
import pHomecare from "@/assets/personal/homecare.jpeg";
import pRide from "@/assets/personal/ride.jpeg";
import pStall from "@/assets/personal/stall.jpeg";
import pMbs from "@/assets/personal/mbs.jpeg";
import pHoney from "@/assets/personal/honey.jpeg";
import pDog from "@/assets/personal/dog.jpeg";
import pRun from "@/assets/personal/run.jpeg";

const PERSONAL = [
  { src: pRun, cap: "Ran the 10K", note: "MyPragati Founder Run · LVX", featured: true },
  { src: pHomecare, cap: "Home-care field visits", note: "Where empathy meets ops" },
  { src: pCleanup, cap: "Community cleanup drives", note: "Skin in the game" },
  { src: pStall, cap: "Selling Ghomedha at the stall", note: "GTM, the hard way" },
  { src: pHoney, cap: "Forest Raw Honey — shipped", note: "Brand · packaging · sell-through" },
  { src: pCoats, cap: "White-coat era", note: "Padmashree, Bangalore" },
  { src: pMbs, cap: "MBS Physiotherapy", note: "Founded · scaled to 1,400+ network" },
  { src: pRide, cap: "Long rides recharge me", note: "Ghats · Royal Enfield · solitude" },
  { src: pDog, cap: "Best teammate at home", note: "Calm under chaos" },
];

export const Route = createFileRoute("/")({
  component: Index,
});

const NAV = [
  { id: "about", label: "About" },
  { id: "credentials", label: "Credentials" },
  { id: "skills", label: "Skills" },
  { id: "work", label: "Work" },
  { id: "personal", label: "Off-Duty" },
  { id: "testimonials", label: "Testimonials" },
  { id: "contact", label: "Contact" },
];

const SKILLS = [
  "GTM Strategy", "Founder's Office", "AIF Operations", "Investor Relations",
  "Pitch Decks", "Market Research", "N8N & AI Prompting", "SQL",
  "Power BI", "MS Excel", "SOPs & QA", "Stakeholder Mgmt",
];

const CREDENTIALS = [
  {
    period: "2025 — Present",
    title: "Master Camp",
    org: "Masters' Union, Gurugram",
    detail: "Strategic Business Management · 35% scholarship · Rank 1/350+ teams in MNNIT GTM & Strategy challenge.",
  },
  {
    period: "2018 — 2023",
    title: "Bachelor of Physiotherapy",
    org: "Padmashree Institute · RGUHS",
    detail: "Rank 13, merit-based scholarship.",
  },
  {
    period: "Certifications",
    title: "McKinsey Forward · Grant Thornton FMV",
    org: "Microsoft · Chief of Staff",
    detail: "Data analysis, project management, financial modelling & valuation.",
  },
];

const WORK = [
  {
    tag: "Founder's Office",
    company: "Lets Venture (LVX)",
    role: "AIF Operations · Founder's Office",
    period: "Feb '26 — Present",
    impact: "₹40Cr–₹100Cr",
    bullets: [
      "Led operational tracking for new scheme launches across deal sizes of ₹3.5Cr, ₹7Cr and ₹9Cr+ ensuring seamless onboarding-to-closure execution.",
      "Executed investor consent workflows for the Dubai corridor, aligning sales, legal and PMS for compliant deal execution.",
      "Built performance dashboards tracking ₹7Cr+ cumulative pipelines, improving reporting accuracy & transparency.",
      "Standardised SOPs for high-value schemes, cutting manual errors & lifting process efficiency.",
    ],
  },
  {
    tag: "Strategy & Ops",
    company: "Techvaraha Solutions",
    role: "Founder's Office — Strategy & Operations",
    period: "Jan '24 — Oct '25",
    impact: "₹40L Revenue Impact",
    bullets: [
      "Spearheaded 4 end-to-end strategic projects across 3 verticals, impacting ₹40L in revenue outcomes.",
      "Orchestrated cross-functional teams of 15–20, reducing project delays by 25%.",
      "Delivered 25+ executive decks & investor reports, contributing to ₹20L in client acquisition.",
      "Supported a ₹40L fundraise — improving investor engagement 35% and accelerating closure 20%.",
      "Designed 5+ SOPs, QA workflows & KRAs — on-time delivery 65% → 90%.",
    ],
  },
  {
    tag: "Entrepreneurship",
    company: "MBS Physiotherapy",
    role: "Founder",
    period: "Feb '21 — Apr '25",
    impact: "1,400+ Network",
    bullets: [
      "Built and scaled a healthcare network of 1,400+ physiotherapists & surgeons.",
      "Negotiated 15+ hospital collaborations, creating new revenue channels.",
      "Ran tele-platform operations for remote patient and professional engagement.",
    ],
  },
  {
    tag: "Healthcare Ops",
    company: "ESIC · Brains · BBMP PHC",
    role: "Healthcare Systems Intern",
    period: "Jul '23 — Dec '23",
    impact: "150+ Cases",
    bullets: [
      "Assessed 150+ inpatient/outpatient cases across Cardiology, Neurology, Surgery, Ortho & OBG.",
      "Designed 20+ community-level rehabilitation interventions at BBMP PHC.",
      "Coordinated across 25+ stakeholders to streamline acute-to-community transitions.",
    ],
  },
];

const STATS = [
  { k: "₹100Cr+", v: "Deal flow tracked" },
  { k: "40%", v: "Faster escalations" },
  { k: "1,400+", v: "Network built" },
  { k: "25+", v: "Investor decks shipped" },
];

function Index() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      {/* NAV */}
      <header className="sticky top-0 z-50 backdrop-blur-md bg-background/80 border-b border-border">
        <div className="mx-auto max-w-7xl px-6 py-4 flex items-center justify-between">
          <a href="#top" className="font-display text-xl">Chethan<span className="text-muted-foreground">.N</span></a>
          <nav className="hidden md:flex gap-7 text-sm font-mono uppercase tracking-wider">
            {NAV.map((n) => (
              <a key={n.id} href={`#${n.id}`} className="hover:opacity-60 transition-opacity">{n.label}</a>
            ))}
          </nav>
          <a href="mailto:chethansid123@gmail.com" className="tag bg-foreground text-background border-foreground">Hire me →</a>
        </div>
      </header>

      {/* HERO */}
      <section id="top" className="relative grain overflow-hidden border-b border-border">
        <div className="mx-auto max-w-7xl px-6 py-16 md:py-24 grid md:grid-cols-12 gap-10 items-end">
          <div className="md:col-span-7 space-y-6">
            <span className="tag">Available · Founder's Office</span>
            <h1 className="font-display text-[clamp(3rem,9vw,8rem)] leading-[0.95]">
              Founder's<br/>
              Office<br/>
              <span className="italic relative">
                Executioner
                <span className="absolute -bottom-2 left-0 right-0 h-3 bg-accent-lime -z-10" />
              </span>.
            </h1>
            <p className="max-w-xl text-lg text-muted-foreground leading-relaxed">
              I turn founder chaos into shipped outcomes. Strategy, operations and investor execution across AIF, GTM and venture-backed teams — from <em>₹3.5Cr scheme launches</em> to <em>₹40L fundraises</em>.
            </p>
            <div className="flex flex-wrap gap-3 pt-2">
              <a href="#work" className="tag bg-foreground text-background border-foreground">See the work</a>
              <a href="#contact" className="tag">Get in touch</a>
            </div>
          </div>
          <div className="md:col-span-5">
            <div className="relative">
              <div className="absolute -inset-3 bg-accent-lime translate-x-3 translate-y-3" />
              <img src={portrait} alt="Chethan N" className="relative w-full aspect-[4/5] object-cover grayscale hover:grayscale-0 transition-all duration-700" />
              <div className="absolute -bottom-4 -left-4 bg-foreground text-background px-4 py-2 font-mono text-xs uppercase tracking-widest">Chethan N · est. Bangalore</div>
            </div>
          </div>
        </div>
        {/* marquee */}
        <div className="border-t border-border py-5 overflow-hidden">
          <div className="marquee whitespace-nowrap font-display text-3xl">
            {Array.from({ length: 2 }).map((_, i) => (
              <div key={i} className="flex gap-12 pr-12 items-center">
                <span>Strategy</span><span className="text-muted-foreground">✦</span>
                <span className="italic">Execution</span><span className="text-muted-foreground">✦</span>
                <span>Investor Ops</span><span className="text-muted-foreground">✦</span>
                <span className="italic">GTM</span><span className="text-muted-foreground">✦</span>
                <span>AIF</span><span className="text-muted-foreground">✦</span>
                <span className="italic">Pitch Decks</span><span className="text-muted-foreground">✦</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* STATS */}
      <section className="border-b border-border">
        <div className="mx-auto max-w-7xl grid grid-cols-2 md:grid-cols-4">
          {STATS.map((s, i) => (
            <div key={s.k} className={`p-8 md:p-10 ${i < 3 ? "border-r border-border" : ""} ${i < 2 ? "border-b md:border-b-0" : ""} border-border`}>
              <div className="font-display text-5xl md:text-6xl">{s.k}</div>
              <div className="font-mono text-xs uppercase tracking-widest text-muted-foreground mt-2">{s.v}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ABOUT */}
      <section id="about" className="border-b border-border">
        <div className="mx-auto max-w-7xl px-6 py-20 md:py-28 grid md:grid-cols-12 gap-10">
          <div className="md:col-span-4">
            <span className="tag">01 · About</span>
            <h2 className="font-display text-5xl md:text-6xl mt-4">The story behind the title.</h2>
          </div>
          <div className="md:col-span-7 md:col-start-6 space-y-5 text-lg leading-relaxed">
            <p>I started in physiotherapy — managing 150+ ICU cases and learning that systems either save lives or cost them. That instinct for <em>execution under pressure</em> never left.</p>
            <p>Today I sit inside founder's offices building the rails: investor workflows for AIF schemes, dashboards that track ₹100Cr+ pipelines, SOPs that move on-time delivery from 65% → 90%, and decks that close fundraises.</p>
            <p>I'm the person founders bring in when an idea needs to become a shipped, measurable outcome — not next quarter, this week.</p>
            <div className="pt-4 border-t border-border mt-6">
              <div className="font-mono text-xs uppercase tracking-widest text-muted-foreground">Recognition</div>
              <div className="mt-2 font-display text-2xl">Best Execution Award · 2025</div>
              <div className="text-sm text-muted-foreground">Stakeholder management, investor communication & cross-functional leadership.</div>
            </div>
          </div>
        </div>
      </section>

      {/* CREDENTIALS */}
      <section id="credentials" className="border-b border-border bg-secondary/40">
        <div className="mx-auto max-w-7xl px-6 py-20 md:py-28">
          <div className="flex items-end justify-between mb-12 flex-wrap gap-4">
            <div>
              <span className="tag">02 · Credentials</span>
              <h2 className="font-display text-5xl md:text-6xl mt-4">Trained where it counts.</h2>
            </div>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {CREDENTIALS.map((c) => (
              <div key={c.title} className="bg-card border border-foreground p-7 hover-lift">
                <div className="font-mono text-xs uppercase tracking-widest text-muted-foreground">{c.period}</div>
                <div className="font-display text-3xl mt-3 leading-tight">{c.title}</div>
                <div className="text-sm font-medium mt-1">{c.org}</div>
                <p className="text-sm text-muted-foreground mt-4 leading-relaxed">{c.detail}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SKILLS */}
      <section id="skills" className="border-b border-border">
        <div className="mx-auto max-w-7xl px-6 py-20 md:py-28 grid md:grid-cols-12 gap-10">
          <div className="md:col-span-4">
            <span className="tag">03 · Skills</span>
            <h2 className="font-display text-5xl md:text-6xl mt-4">What I bring to the table.</h2>
            <p className="text-muted-foreground mt-4 max-w-sm">A founder's office hybrid — strategy brain, ops hands, investor voice.</p>
          </div>
          <div className="md:col-span-8 flex flex-wrap gap-3 content-start">
            {SKILLS.map((s) => (
              <span key={s} className="px-5 py-3 border border-foreground font-mono text-sm uppercase tracking-wider hover:bg-foreground hover:text-background transition-colors cursor-default">
                {s}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* WORK */}
      <section id="work" className="border-b border-border bg-foreground text-background">
        <div className="mx-auto max-w-7xl px-6 py-20 md:py-28">
          <div className="mb-14">
            <span className="tag border-background">04 · Work showcase</span>
            <h2 className="font-display text-5xl md:text-7xl mt-4">Proof of execution.</h2>
          </div>
          <div className="space-y-4">
            {WORK.map((w, i) => (
              <details key={w.company} open={i === 0} className="group border border-background/30 hover:border-accent-lime transition-colors">
                <summary className="cursor-pointer list-none p-6 md:p-8 flex flex-wrap items-center gap-6 justify-between">
                  <div className="flex items-center gap-6 flex-wrap">
                    <span className="font-mono text-xs opacity-60">0{i + 1}</span>
                    <div>
                      <div className="font-mono text-xs uppercase tracking-widest opacity-60">{w.tag} · {w.period}</div>
                      <div className="font-display text-3xl md:text-4xl mt-1">{w.company}</div>
                      <div className="text-sm opacity-80">{w.role}</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-5">
                    <span className="px-4 py-2 bg-accent-lime text-foreground font-mono text-xs uppercase tracking-widest">{w.impact}</span>
                    <span className="text-2xl group-open:rotate-45 transition-transform">+</span>
                  </div>
                </summary>
                <ul className="px-6 md:px-8 pb-8 pl-16 md:pl-24 space-y-3 text-base opacity-90 max-w-4xl">
                  {w.bullets.map((b, j) => (
                    <li key={j} className="relative pl-5 leading-relaxed">
                      <span className="absolute left-0 top-2.5 w-2 h-2 bg-accent-lime" />{b}
                    </li>
                  ))}
                </ul>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* PERSONAL — OFF DUTY */}
      <section id="personal" className="border-b border-border bg-secondary/40">
        <div className="mx-auto max-w-7xl px-6 py-20 md:py-28">
          <div className="grid md:grid-cols-12 gap-10 mb-14 items-end">
            <div className="md:col-span-7">
              <span className="tag">05 · Off-Duty</span>
              <h2 className="font-display text-5xl md:text-7xl mt-4 leading-[0.95]">
                The human behind <span className="italic">the executioner</span>.
              </h2>
            </div>
            <p className="md:col-span-5 text-lg text-muted-foreground leading-relaxed">
              Decks and dashboards are half the story. The other half? Field visits, founder runs, building from a stall, and the long rides that keep the head clear. This is the operator unplugged.
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-5">
            {PERSONAL.map((p, i) => (
              <figure
                key={p.cap}
                className={`group relative overflow-hidden border border-foreground bg-card hover-lift ${
                  i === 0 ? "col-span-2 row-span-2" : ""
                } ${i === 5 ? "md:col-span-2" : ""}`}
              >
                <img
                  src={p.src}
                  alt={p.cap}
                  loading="lazy"
                  className={`w-full ${i === 0 ? "aspect-square" : "aspect-[4/5]"} object-cover grayscale group-hover:grayscale-0 transition-all duration-700`}
                />
                <figcaption className="absolute inset-x-0 bottom-0 p-3 md:p-4 bg-gradient-to-t from-foreground/95 via-foreground/70 to-transparent text-background">
                  <div className="font-display text-lg md:text-2xl leading-tight">{p.cap}</div>
                  <div className="font-mono text-[10px] md:text-xs uppercase tracking-widest opacity-80 mt-1">{p.note}</div>
                </figcaption>
              </figure>
            ))}
          </div>

          <div className="mt-14 border-2 border-foreground bg-foreground text-background p-8 md:p-10 flex flex-wrap items-center justify-between gap-6">
            <div>
              <div className="font-mono text-xs uppercase tracking-widest opacity-70">The hook</div>
              <div className="font-display text-3xl md:text-4xl mt-2 max-w-2xl">
                I don't just <em>plan</em> the work — I show up, get hands dirty, and ship.
              </div>
            </div>
            <a href="#contact" className="px-6 py-4 bg-accent-lime text-foreground font-mono text-xs uppercase tracking-widest hover-lift inline-block whitespace-nowrap">
              Bring me in →
            </a>
          </div>
        </div>
      </section>

      {/* TESTIMONIALS */}
      <section id="testimonials" className="border-b border-border">
        <div className="mx-auto max-w-7xl px-6 py-20 md:py-28">
          <span className="tag">06 · Testimonials</span>
          <h2 className="font-display text-5xl md:text-6xl mt-4 mb-14">In their words.</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {[
              { q: "Chethan turns ambiguous founder asks into shipped, documented outcomes — fast. He owns the gap between strategy and execution.", a: "Founder, Techvaraha Solutions" },
              { q: "Exceptional command over investor workflows and AIF operations. Reliable, sharp, and unusually calm under deal pressure.", a: "Senior Lead, Lets Venture" },
            ].map((t) => (
              <figure key={t.a} className="border border-foreground p-8 md:p-10 bg-card">
                <div className="font-display text-6xl leading-none">"</div>
                <blockquote className="font-display text-2xl md:text-3xl leading-snug -mt-2">{t.q}</blockquote>
                <figcaption className="font-mono text-xs uppercase tracking-widest text-muted-foreground mt-6">— {t.a}</figcaption>
              </figure>
            ))}
          </div>
        </div>
      </section>

      {/* CONTACT */}
      <section id="contact" className="grain bg-accent-lime">
        <div className="mx-auto max-w-7xl px-6 py-24 md:py-32 text-center">
          <span className="tag">07 · Let's build</span>
          <h2 className="font-display text-6xl md:text-[10rem] leading-[0.9] mt-6">
            Need an<br/><span className="italic">executioner</span>?
          </h2>
          <p className="text-lg mt-8 max-w-xl mx-auto">If your founder's office needs someone to make things actually happen — let's talk.</p>
          <div className="mt-10 flex flex-wrap gap-4 justify-center">
            <a href="mailto:chethansid123@gmail.com" className="px-7 py-4 bg-foreground text-background font-mono text-sm uppercase tracking-widest hover-lift inline-block">
              chethansid123@gmail.com
            </a>
            <a href="tel:+918792432119" className="px-7 py-4 border-2 border-foreground font-mono text-sm uppercase tracking-widest hover-lift inline-block">
              +91 87924 32119
            </a>
          </div>
        </div>
        <footer className="border-t-2 border-foreground">
          <div className="mx-auto max-w-7xl px-6 py-6 flex justify-between items-center font-mono text-xs uppercase tracking-widest">
            <span>© 2026 Chethan N</span>
            <span>Bangalore · Gurugram</span>
          </div>
        </footer>
      </section>
    </main>
  );
}
