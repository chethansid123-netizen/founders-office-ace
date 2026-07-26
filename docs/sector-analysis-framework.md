# Sector Analysis: The End-to-End VC Framework

**How a top-decile fund actually runs a sector deep-dive — from blank page to funded thesis.**

This is the operating manual. It is written the way an investment team runs it: a
time-boxed sprint with named artifacts, not an open-ended research project. Nine
phases, a two-week calendar, the question banks, the benchmarks, the memo
templates, and the failure modes.

---

## 0. First, understand what sector analysis is *for*

Most people do sector analysis as if the goal were to *understand a market*. That
is not the goal. A fund does sector work to answer exactly three questions:

1. **Is there a fund-returner here?** Can one company in this sector plausibly
   reach an exit large enough to return our whole fund? If no — the sector is
   interesting, not investable. Stop.
2. **What has to be true?** What is the specific, falsifiable claim about the
   world that makes the winner inevitable — and how will I know within 18 months
   if I'm wrong?
3. **Who do I need to meet, and what do I ask them?** Sector work that doesn't
   end in a ranked target list and a differentiated question set was an academic
   exercise.

Everything below is in service of those three. If a piece of analysis doesn't
move one of them, cut it.

### Two modes — know which one you're in

| | **Thesis-driven** | **Reactive / deal-triggered** |
|---|---|---|
| **Trigger** | Partner allocates a sector to own | A hot deal lands, nobody understands the space |
| **Time box** | 2–4 weeks | 3–5 days |
| **Output** | Thesis memo + market map + sourcing list | Sector primer + "is this the winner?" view |
| **Bar** | Must produce a sourcing plan | Must produce a decision |
| **Danger** | Analysis paralysis; falling in love | Retrofitting a thesis to justify the deal |

The framework is the same. Reactive mode runs Phases 1, 2, 4, 6, 7 hard and
timeboxes the rest.

### The output contract — agree this before you start

Write this down on day zero and get the partner to sign off. It prevents the
single most common failure: three weeks of work that answers a question nobody
asked.

```
SECTOR:            [name]
SPONSOR:           [partner]
DEADLINE:          [date — partner meeting slot booked]
DECISION IT DRIVES: [invest / pass / build watchlist / hire an EIR / nothing]
DELIVERABLES:      Thesis memo (8pp) · Market map · Target list (50, ranked)
                   · Expert call log (12+) · Model (fund-math + unit-economics)
KILL SWITCH:       If [X] is false by day 5, we stop and reallocate the time.
```

---

## Phase 1 — Define the market (the phase everyone rushes and everyone regrets)

Bad market definitions produce confident, wrong answers. This is where 80% of
sector analyses are already broken and nobody notices for two weeks.

### 1.1 Define by *job and buyer*, not by technology

"The AI market" is not a market. "The vector database market" is not a market —
it's a component. A market is: **a buyer with a budget, doing a job, currently
solving it some way.**

Force yourself into this sentence:

> **[Buyer persona]** at **[company type / segment]** spends **[$X today]** on
> **[current solution]** to accomplish **[job]**, and is dissatisfied because
> **[specific failure of the status quo]**.

If you can't fill every blank with specifics, you don't have a market yet — you
have a technology looking for one. Write three versions of that sentence with
different buyers, and you'll usually discover the real market is one of them,
not the union of all three.

### 1.2 Draw the boundary explicitly — in and out

Make an actual two-column list. "In scope" and "out of scope," with a one-line
reason for each exclusion. This gets attacked in partner meeting; have the
answer pre-loaded.

The boundary test: **would a company on the "in" list and a company on the "out"
list ever appear in the same competitive bake-off?** If yes, they're the same
market regardless of what the category taxonomy says. If no, they aren't
regardless of how similar the tech is.

### 1.3 Segment before you size

Almost every market is really 3–6 sub-markets with different buyers, different
economics, and different winners. Segment along whichever axis actually changes
the buying behaviour:

- **By customer size** — SMB / mid-market / enterprise (usually the highest-signal cut; GTM motion, ACV, churn and defensibility all break differently)
- **By vertical** — healthcare vs logistics vs financial services
- **By geography** — US vs EU vs India vs SEA (regulation, willingness-to-pay, sales cycle)
- **By job-to-be-done** — the workflow stage being replaced
- **By deployment / trust posture** — cloud vs on-prem vs regulated/air-gapped

Now pick the segment(s) you're actually underwriting. **The rest of the analysis
happens at the segment level, not the market level.** Sizing the union and
underwriting one slice is the #1 source of overstated TAM.

### 1.4 Map the value chain

Draw the flow of money and work from raw input to end customer. For a typical
software sector:

```
Infra/compute → Data/models → Tooling → Application layer → Distribution/channel → End buyer
```

For a physical/consumer sector:

```
Input supply → Manufacturing → Brand/assembly → Logistics → Retail/channel → Consumer
```

For each link, capture four things:
- **Who** operates it (name the 3–5 real companies)
- **What share of end-customer dollar** it captures
- **Gross margin** at that layer
- **Concentration** — how many players hold >50% share?

This single diagram tells you where profit pools sit and where power sits — and
those are often different layers. You invest where they overlap.

---

## Phase 2 — Size it (three ways, and reconcile them)

Do not do one sizing. Do three. The number matters far less than the *spread
between the three* — that spread is where your real insight lives.

### 2.1 Top-down (fast, directional, always challenged)

```
TAM = (# of qualifying entities) × (annual spend per entity)
```

Start from a published industry figure, then **narrow it with explicit haircuts**
you can defend line by line:

```
Global market ($200B, per industry report)
  × 35% addressable geography                 = $70B
  × 40% segment we serve (mid-market+)        = $28B
  × 60% of budget our product actually touches= $16.8B  ← SAM
  × 15% realistic share ceiling in 10 yrs     = $2.5B   ← SOM
```

Rule: never present a top-down number without the haircut ladder. A naked "$200B
market" is the fastest way to lose credibility in a partner meeting.

### 2.2 Bottom-up (the one that's actually believed)

```
TAM = Σ (# customers in segment × ACV in segment)
```

Build it from a real, countable population. Sources: company-count databases,
industry association registries, licence registers, job-posting counts, filings.
Then get ACV from actual pricing pages, expert calls, or observed contract
values — never from a guess.

Sanity checks that catch most errors:
- **Seat math:** # of target employees globally × price/seat × realistic penetration
- **Budget-line math:** what line item does this come out of, and how big is that line today?
- **Bottoms-up on the incumbent:** if the market leader does $2B at 30% share, the market is ~$6.7B. Does that match your number? If you're off by 5x, find out why before proceeding.

### 2.3 Value-theft / wallet-reallocation (the sizing that finds real alpha)

The most interesting markets don't exist yet as a budget line. So size them by
what they *displace*:

```
New market ≈ (labour cost displaced × capture rate)
           + (legacy software budget replaced)
           + (waste/leakage eliminated × share of savings captured)
           + (new demand unlocked at the lower price point)
```

The last term is the one generalists miss and where the biggest outcomes hide.
When a cost curve collapses, demand doesn't stay flat — it expands. Ask: *at
1/10th the price, who buys this who couldn't before?* That new-demand pool is
frequently larger than the existing market, and it is invisible to top-down
sizing because it isn't in anyone's report yet.

Capture-rate discipline: services-replacement businesses typically capture
**10–30%** of the labour cost they displace, not 100%. Underwrite that band and
justify where you land in it.

### 2.4 Reconcile — and interrogate the gap

Put all three side by side. Now do the real work:

| Method | TAM | What it assumes |
|---|---|---|
| Top-down | $16.8B | Analyst category is correctly drawn |
| Bottom-up | $4.2B | Current ACVs and current buyer count hold |
| Value-theft | $31B | Displacement happens and price expands demand |

**The gap is the thesis.** If bottom-up is far smaller than value-theft, you're
betting the market *becomes* something it isn't yet — say so explicitly, and
name the mechanism that gets it there. That's a real, defensible position. What
kills you is presenting the biggest of the three numbers without acknowledging
the other two exist.

### 2.5 Size the *growth*, not just the level

A $4B market growing 60%/yr beats a $40B market growing 3%. Compute:

- **Historical CAGR** (3–5 yrs, from real revenue of the top 5 players — not from a report's forecast)
- **Forward CAGR** and, critically, **what physically drives it**: more buyers? higher price? more usage per buyer? Which one, and what's the ceiling on it?
- **Time-to-$1B-market**: if it's more than ~7 years out, a seed investment today is early even if the thesis is right. Venture returns are as much about timing as direction.

---

## Phase 3 — "Why now?" (the phase that separates real theses from decks)

Every sector has been "about to happen" for years. The differentiated question is
never *is this a good idea* — it's *why is this inevitable in the next 36 months
when it wasn't in the last 36?*

### The catalyst stack — you need at least two

| Catalyst | What to look for | Evidence to gather |
|---|---|---|
| **Technology unlock** | A capability crossed a threshold from "demo" to "deployable" | Benchmark curves, error rates, latency, accuracy at cost |
| **Cost curve collapse** | Unit cost dropped 10x+, opening new demand | $/unit over 5 yrs, forward projections |
| **Regulatory shift** | A mandate creates a forced buyer with a deadline | Effective dates, penalty size, who must comply |
| **Behaviour change** | Buyers now do something they refused to before | Adoption surveys, category search trends, procurement policy shifts |
| **Distribution unlock** | A new channel makes reaching the buyer 10x cheaper | Platform launches, marketplace/app-store openings, ecosystem shifts |
| **Capital / supply shift** | Input became available or cheap | Supply chain, talent pool size, funding availability |
| **Incumbent dislocation** | A leader stumbled, got acquired, or is distracted | Layoffs, M&A, price increases, product decay, exec churn |

**Rule of two:** one catalyst is a coincidence and often reverses. Two or more
that compound is a market. Write the "why now" as a dated timeline — this is the
single most persuasive slide you will produce:

```
2021 — [enabling tech ships, unusably expensive]
2023 — [cost falls 40x; first credible deployments]
2024 — [regulation passes, compliance deadline set for 2027]
2025 — [first buyers create a named budget line]
2026 — NOW: buyer intent exists, tooling exists, no category winner yet
2027 — compliance deadline forces the laggard 60% to buy
```

### The inverse — "why not before?"

Find who tried this before and failed. There is almost always someone. For each:
*what specifically was missing, and is it present now?* If you can't articulate
what changed, the honest answer is that nothing did — and you're about to fund
the same failure with a new logo. This one question kills more bad theses than
any other in the framework.

---

## Phase 4 — Market structure: what does the end state look like?

You are not investing in today's market. You're investing in its terminal state,
5–10 years out. Model it explicitly.

### 4.1 Winner-take-all, or fragmented?

Score each force 0–3. Total ≥14 leans monopoly/duopoly; ≤7 leans fragmented.

| Force | Question | 0 | 3 |
|---|---|---|---|
| **Network effects** | Does each user make it better for the next? | None | Strong, direct, cross-side |
| **Economies of scale** | Does unit cost fall materially with volume? | Flat | Steep |
| **Switching costs** | Cost/pain to rip out once deployed? | Trivial | Data + workflow + compliance lock-in |
| **Data advantage** | Does usage compound into a better product? | No | Proprietary loop competitors can't replicate |
| **Distribution concentration** | Do a few channels control access? | Long tail | 2–3 gatekeepers |
| **Buyer preference for a single vendor** | Consolidation vs best-of-breed? | Best-of-breed | Suite/platform |
| **Regulatory moat** | Are licences/approvals a real barrier? | None | Multi-year, capital-intensive |

**This score determines your entire strategy.** In a WTA market, only the #1
matters — you must find and win the leader, pay up for it, and being early is
worth almost any price. In a fragmented market, #3 can be a fine business,
entry price discipline matters enormously, and roll-ups/consolidators are often
the actual play. Getting this wrong means being right about the sector and still
losing money.

### 4.2 Where does power sit in the value chain?

Adapt Porter's five forces to the VC question — *who captures the margin at
steady state?* Layers with power share these traits:

- Hard to substitute; the customer relationship lives there
- Concentrated supply, fragmented demand (or the reverse in your favour)
- Owns the data or the workflow, not just a feature
- Switching away requires re-plumbing something else

**The commoditisation test:** for each layer, ask "if three well-funded teams
attacked this layer simultaneously, would prices collapse?" If yes, that layer
is a commodity — don't invest there, invest in whoever *buys* from it. Margin
migrates away from commoditising layers, and it migrates fast.

### 4.3 Sketch the end state on a page

Name the shape (a 5-line paragraph, not a chart):

> By 2032 this market is ~$Xbn. It consolidates to 2–3 platforms holding ~60%
> share, plus a long tail of vertical specialists. Margin sits at the
> [application/data/distribution] layer because [reason]. The infra layer
> commoditises to ~20% gross margin. Incumbent [X] survives by acquiring, [Y]
> does not adapt. The winner is a company that today looks like [description],
> and it wins because [structural advantage].

Then: **what would have to be true for that to be wrong?** Write the three most
likely alternative end states. You'll be judged on having considered them.

---

## Phase 5 — Business model & unit economics

Structure tells you whether a big company *can* exist. Unit economics tell you
whether *this* one will.

### 5.1 Benchmark ranges to underwrite against

Typical bands investors underwrite to. Treat these as the "is this normal?"
screen, not gospel — verify current comps for the specific sub-sector and stage,
because the bar moves with the funding environment.

**B2B SaaS**
| Metric | Good | Great |
|---|---|---|
| Gross margin | 70–75% | 80%+ |
| Net revenue retention | 100–110% | 120%+ |
| Gross logo retention | 85%+ | 90%+ (enterprise 95%+) |
| CAC payback | <18 mo | <12 mo |
| LTV/CAC | 3x | 5x+ |
| Magic number | 0.7 | >1.0 |
| Rule of 40 (growth + FCF margin) | 40 | 60+ |
| Growth at $1M→$10M ARR | 2.5x | 3x (triple-triple-double-double-double) |

**Marketplaces**
| Metric | Good | Great |
|---|---|---|
| Take rate | 10–15% | 20%+ (or lower with huge volume) |
| GMV growth | 100%+ early | — |
| Repeat rate (cohort) | 40%+ | 60%+ |
| Liquidity (fill rate) | 40%+ | 70%+ |
| Supply concentration | Top 10% < 50% of GMV | Healthy long tail |
| Contribution margin | Positive by yr 2 | Positive at launch |

**AI-native / usage-based**
| Metric | Watch for | Why |
|---|---|---|
| Gross margin | 40–70% typical; trending up with inference cost declines | The core question is whether COGS falls faster than price |
| Inference cost as % revenue | Trend matters more than level | Improving = leverage; flat = structurally capped |
| Usage expansion | >120% NRR | Consumption models live or die here |
| Eval/quality moat | Proprietary data or feedback loop | Otherwise the model layer is rented, not owned |
| Concentration risk | Single model provider dependency | Pricing power sits upstream |

**Fintech / lending**
| Metric | Note |
|---|---|
| Net interest margin, loss rate, cost of funds | Underwrite the credit box before the growth |
| Unit economics *through a full credit cycle* | Growth masks losses for 12–18 months |
| CAC vs lifetime contribution | Not vs revenue — lending CAC math misleads badly |
| Regulatory capital | Determines how much equity growth actually consumes |

**Consumer / D2C**
| Metric | Good |
|---|---|
| Contribution margin (post-shipping, post-CAC) | 20%+ |
| Repeat purchase rate (90-day) | 30%+ |
| Blended CAC vs AOV | CAC < 1/3 of first-year contribution |
| Organic/paid mix | >40% organic |

### 5.2 The three questions that actually matter

Everything above is diagnostics. The decisions come from:

1. **Does it get better with scale?** Gross margin, CAC, and churn should all
   improve as the company grows. If any degrades with scale, you have a
   structurally capped business no matter how good today's numbers look.
2. **Is revenue quality real?** Recurring > usage > transactional > services.
   Look for: contract length, auto-renewal, concentration (top-10 customers as
   % of revenue — >40% is a flag), and whether "ARR" contains one-off implementation fees.
3. **What's the cash conversion cycle?** Negative working capital (customer pays
   before you pay costs) is a genuine structural advantage that shows up nowhere
   on a metrics dashboard and quietly determines how much capital the company
   needs to reach scale.

---

## Phase 6 — Competitive landscape (do this properly, not as a logo slide)

### 6.1 Build a real market map

Not "logos in boxes." Map along the two axes that determine who wins in *this*
market — derived from Phase 4, not from convention. Common useful axes:

- Wedge (which workflow step they entered through) × Buyer segment
- Depth of product × Breadth of workflow covered
- Build (own the model/infra) × Buy (orchestrate others)
- Self-serve/PLG × Enterprise sales

For every company on the map, capture in a tracker:

```
Name · Founded · HQ · Total raised · Last round (size, date, valuation, lead)
· Est. revenue & growth · Headcount & 12-mo Δ (LinkedIn is your friend)
· Buyer segment · Wedge · Pricing model & published price
· 3 named customers · Key hire signals · Notable investors
```

Headcount growth trend and *engineering-vs-sales ratio* are the two most
under-used public signals for reading a private company's actual momentum and
stage of GTM maturity.

### 6.2 The four competitor classes — and the honest answer to each

1. **Startups** — the visible map. Least dangerous individually, most instructive collectively: *where they cluster tells you where the wedge is easy, and where nobody is playing tells you either an insight or a graveyard.* Find out which.
2. **Incumbents** — the real threat. The question is never "can they build it" (they can) but **"does their P&L let them ship it?"** Incumbents don't move when the new product cannibalises a profitable line, breaks their channel's compensation, or requires a business model their public shareholders will punish. Name the specific structural reason the incumbent won't respond well. "They're slow" is not an answer.
3. **Adjacent platforms** — the company one workflow step away that could extend into this. Usually the most underestimated threat, because they arrive with distribution already built.
4. **Status quo** — spreadsheets, agencies, offshore teams, doing nothing. In most B2B markets the largest competitor by share, and the hardest to displace because it has no sales cycle and no procurement review.

### 6.3 The "why won't the giant crush this?" memo

Write it as a paragraph, before partner meeting, because you will be asked and a
weak answer here sinks otherwise strong memos. Legitimate answers:

- **Cannibalisation** — it eats a bigger, more profitable existing line
- **Channel conflict** — their partners/resellers/sales comp structure blocks it
- **Architecture** — their stack genuinely can't do it without a rewrite
- **Focus / market size** — too small to matter to them *now* (note: this expires, and you should say when)
- **Data access** — the startup has data they structurally cannot get
- **Regulation** — they're constrained in a way a new entrant isn't
- **Talent** — the required team won't work there

Illegitimate answers: "they're slow," "they don't get it," "startups always win."

### 6.4 White space — earned, not assumed

Empty space on a market map means one of two things: an opportunity, or a
graveyard. **Assume graveyard until proven otherwise.** Go find the companies
that tried it and died. If you find three corpses, that space is empty for a
reason and you should know the reason. If you genuinely find none — and the
"why now" from Phase 3 explains the timing — that's your highest-value finding
in the whole exercise.

---

## Phase 7 — Capital flows, exits, and fund math

This is the phase that separates investors from analysts. A sector can be
fascinating, growing, and structurally attractive — and still be uninvestable
because the entry price is wrong or there's no exit.

### 7.1 Map the money already in

- Total VC invested in the sector, last 5 yrs, by year and stage
- Number of financings per year — accelerating or decelerating?
- Which funds are active, and are they leading or following?
- Median seed / A / B round size and pre-money valuation *in this sector*
- Are valuations expanding faster than revenue? (multiple expansion = you're late)
- How many companies have hit $10M / $50M / $100M ARR? (proof of scalability)

**Crowding read:** heavy capital inflow with no revenue proof points is the
classic top signal — it means price is being set by narrative, not results. The
best time to enter is usually when a sector has *one* clear proof point and
*before* capital has piled in.

### 7.2 Map the exits — no exits, no returns

- **Strategic acquirers:** name 8–12 specific companies. For each: have they bought in this space, what did they pay, what multiple, and what is their current M&A appetite (cash position, recent deal cadence)?
- **Historical exits:** every acquisition in the sector, with price and revenue multiple if disclosed
- **Public comps:** the 5–10 closest listed companies, their EV/Revenue and EV/EBITDA multiples, and their growth rates. **This is your terminal multiple** — you cannot underwrite an exit at a multiple the public market doesn't pay for this profile.
- **IPO viability:** what does a company need to look like to list from this sector? Usually ~$200M+ ARR, 30%+ growth, credible path to profitability — verify against recent listings.

If your acquirer list is short and public comps trade at 2x revenue, a
venture-scale outcome requires enormous scale. Say so in the memo.

### 7.3 Fund math — the sentence that decides it

For a fund of size **$F** needing a **3x** gross return, with typical ownership
**O%** at exit after dilution:

```
Required exit value for a fund-returner = F / O
```

| Fund size | Ownership at exit | Exit needed to return the fund |
|---|---|---|
| $100M | 10% | $1.0B |
| $250M | 12% | ~$2.1B |
| $500M | 15% | ~$3.3B |
| $1B | 15% | ~$6.7B |

Now the test: **at the terminal multiple from 7.2, what revenue does that exit
value imply, and is that revenue a plausible share of the SOM you sized in
Phase 2?**

```
Required exit value        $2.1B
÷ terminal multiple          6x   (public comps, growth-adjusted)
= required revenue         $350M
÷ SOM                      $2.5B
= required market share      14%   ← is that credible in this structure?
```

If that share number is >30% in a fragmented market, or the required revenue
exceeds anything achieved in the sector's history, the sector fails fund math.
**That is a legitimate, valuable, career-enhancing conclusion.** Write the memo
and say so — "we should not spend time here, and here's the arithmetic" is one
of the highest-leverage outputs an analyst can produce.

---

## Phase 8 — Form the thesis

Now convert everything into a position. A thesis is not a summary. It is a
**falsifiable claim about the future that most people disagree with, on which
you are willing to deploy capital.**

### 8.1 The thesis statement — one sentence, this shape

> **Because** [catalyst / structural change],
> **we believe** [specific outcome in a specific segment] **by** [date],
> **which creates** [$X of enterprise value] **at** [which layer],
> **captured by a company that** [has this specific characteristic].
> **We are wrong if** [falsifiable condition].

Worked example:

> **Because** inference costs fell ~30x in 24 months while nursing shortages
> deepened and CMS documentation rules tightened, **we believe** ambient clinical
> documentation becomes standard-of-care in >50% of US mid-market hospital systems
> **by 2029**, **creating** $8–12B of enterprise value **at the workflow-integration
> layer** (not the model layer, which commoditises), **captured by a company that**
> owns EHR write-back integrations and clinician trust rather than model quality.
> **We are wrong if** EHR vendors ship adequate native functionality bundled at
> zero marginal price before 2027.

Note the properties: it names a date, a segment, a layer, a mechanism, and a
kill condition. Anyone can check in 18 months whether you were right.

### 8.2 Sub-theses and the anti-thesis

Break the main thesis into 3–5 sub-claims, each with the evidence you have and
the evidence you still need:

| Sub-thesis | Confidence | Evidence for | Evidence needed | How to get it |
|---|---|---|---|---|
| Buyers will pay $X/seat | Medium | 6 expert calls, 2 pricing pages | 5 more buyer calls at mid-market | Cold outreach to VP Ops |
| Model layer commoditises | High | Cost curve, 4 credible providers | — | — |
| Integration is the moat | Low | 2 founder claims | Technical validation | Call an ex-EHR integration eng |

Then write the **anti-thesis** — the strongest possible argument *against*, made
in good faith, as if you were being paid to kill the deal. If your anti-thesis is
weak, you haven't done the work; go find the smartest sceptic in the sector and
call them. Funds that skip this step systematically overpay.

### 8.3 Kill criteria — write them now, while you're objective

Pre-commit to the signals that would make you exit the thesis. Date them.

```
KILL IF:
  · [Incumbent] ships native equivalent bundled free       → check quarterly
  · Sector NRR benchmarks fall below 105%                  → check semi-annually
  · No company reaches $20M ARR by Q4 2027                 → check annually
  · Entry valuations exceed 40x forward ARR                → check per deal
```

This is the discipline that prevents a thesis from becoming an identity. Theses
should die on schedule; the ones that don't are the ones that cost funds money.

---

## Phase 9 — Convert to action (sourcing, diligence, and the living thesis)

Analysis that doesn't change what you do this week was a hobby.

### 9.1 The sourcing map

Turn the market map into a ranked target list of 50, scored:

| Weight | Criterion |
|---|---|
| 30% | Thesis fit — are they positioned where you said value accrues? |
| 20% | Team — founder-market fit, prior experience, hiring quality |
| 20% | Traction relative to age and capital raised |
| 15% | Stage fit — are they raisable at your entry point in the next 12 mo? |
| 15% | Access — do you have a warm path, and how strong? |

Tier them: **A** (reach out this week) · **B** (track, quarterly touch) ·
**C** (monitor only). Then actually build the outreach: a per-company hook drawn
from your research, because *"I've spent three weeks on this sector and here's a
non-obvious thing I learned about your buyer"* opens doors that a template never
will. Your sector work is your sourcing edge — use it as the outreach asset it is.

### 9.2 Sector-specific diligence questions

Generic diligence gets generic answers. Your sector work should produce 10–15
questions only someone who did this work would know to ask — the questions that
separate an operator from a pitch-deck reader. Shape:

- "Your peers are seeing implementation slip from 6 to 14 weeks post-[change]. What are you seeing?"
- "How does your unit economics change when [input cost] falls another 5x?"
- "Three companies died attacking this wedge in 2021–23. What do you have that they didn't?"
- "Walk me through what happens to your pricing when [incumbent] bundles this."
- "Your NRR is 118%. How much of that is seat expansion versus price increases versus new modules?"

### 9.3 The living thesis

A thesis has a maintenance schedule, not an end date:

- **Weekly** — funding/product/hiring news in the sector → update tracker
- **Monthly** — 2 expert calls, 5 new companies added to the map
- **Quarterly** — re-score kill criteria; refresh the memo's key numbers; write a one-page delta ("what changed and what I now believe differently")
- **Annually** — full rebuild, and an honest scorecard against your original predictions

**Keep the scorecard publicly (within the firm).** Investors who track their own
prediction accuracy calibrate faster than those who don't, and it compounds
into the only real edge in this job.

---

## The two-week sprint calendar

| Day | Work | Output |
|---|---|---|
| **1** | Scope, output contract, market definition, first boundary draw | Scoping doc, signed off |
| **2** | Value chain map, segmentation, initial company list (~60) | Value chain diagram, raw list |
| **3** | Top-down + bottom-up sizing; funding data pull | Sizing model v1 |
| **4** | Why-now timeline; failed-predecessor research | Catalyst timeline |
| **5** | **Checkpoint** — 30 min with sponsor. Kill or continue. | Go/no-go + refined question set |
| **6–7** | Expert calls (4–6): operators, buyers, ex-incumbents | Call notes, sizing v2 |
| **8** | Competitive deep-dive; incumbent-response memo | Market map v1 |
| **9** | Unit economics benchmarking; value-theft sizing | Full model |
| **10** | Exit landscape, public comps, fund math | Returns model |
| **11–12** | Founder calls (4–6) — pressure-test thesis on people building it | Thesis v1, anti-thesis |
| **13** | Write the memo. Pre-read to one sceptical colleague. | Draft memo |
| **14** | Revise; build target list; **partner meeting** | Final memo, ranked 50, sourcing plan |

Day 5 is the most important entry on this calendar. Most bad sector reports are
bad because nobody checked in until day 14.

---

## The research stack

**Market & funding data** — Crunchbase, PitchBook, Tracxn (strong for India/SEA),
CB Insights, Dealroom, regional registries (MCA filings in India, Companies House in the UK)

**Public comps & financials** — SEC EDGAR (10-Ks are the single best free source
of market sizing and competitive intel — read the risk factors and the MD&A),
earnings call transcripts, investor day decks

**Private company signals** — LinkedIn headcount trends by function, job postings
(tech stack, GTM stage, geographic expansion), G2/Capterra review volume and
velocity, web traffic estimates, app-store rank, GitHub activity for
developer tools, pricing pages via Wayback Machine to read pricing evolution

**Expert access** — Tegus/AlphaSense (call transcript libraries — often faster
than doing your own calls), GLG/Third Bridge, your own network, ex-employees on
LinkedIn (highest signal-per-minute, and free)

**Primary** — customer/buyer calls (the single highest-value input in this whole
list), founder calls, conference floor conversations, trade publications and
industry association reports, procurement/RFP documents when public

**Regulatory** — the relevant regulator's own site; effective dates and penalty
structures are usually published and almost nobody reads them

### The expert call playbook

Twelve calls is the target for a real sector sprint. Mix: 4 buyers, 3 operators
at incumbents/competitors, 2 ex-employees of the market leader, 3 founders.

**Structure (30 min):**
1. *(2 min)* Their role and scope — calibrate how much they actually know
2. *(8 min)* How the job gets done today, step by step. Do not lead. "Walk me through last Tuesday."
3. *(8 min)* What's broken, and what have they tried? What did they buy, what did they rip out, and why?
4. *(6 min)* Budget: what line does this come from, who signs, what's the approval threshold, what's the cycle length?
5. *(4 min)* Vendor landscape from their seat — who did they evaluate, who won, why?
6. *(2 min)* "Who else should I talk to?" — always ask; referral chains are how you get to non-obvious experts

**Rules:** never pitch, never lead the witness, ask for specific numbers and
recent examples rather than opinions, and always ask "what would have to change
for you to switch?" — the answer to that question is the moat, described by the
person who'd have to cross it.

---

## The deliverable: memo structure

Eight pages. If it's longer, you haven't finished thinking.

```
1. THESIS               ½ pg — the one-sentence claim + 3 supporting bullets + kill condition
2. WHY NOW              1 pg — dated catalyst timeline + why-not-before
3. MARKET               1½ pg — definition, segmentation, three sizings reconciled, growth drivers
4. STRUCTURE            1 pg — value chain, where margin sits, WTA score, terminal state
5. COMPETITION          1 pg — market map, incumbent-response memo, white space
6. ECONOMICS            1 pg — unit economics benchmarks, what "good" looks like here
7. RETURNS              1 pg — exits, comps, fund math, required share
8. ACTION               1 pg — top 10 targets, access paths, next 30 days
   APPENDIX             — anti-thesis, expert call log, full company tracker, model
```

**Writing rules that matter:**
- Lead with the conclusion. Never make the partner read to page 6 for your view.
- Every number carries a source and a date, inline.
- Distinguish **fact** / **estimate** / **assumption** visually. Never blur them.
- State confidence explicitly: "high confidence," "we don't know yet."
- The anti-thesis goes in, not out. Suppressing it is how funds lose money.
- If your view changed during the work, say so and say why. That's evidence of thinking, not weakness.

---

## Failure modes — the ten ways this goes wrong

1. **Boiling the ocean.** Sizing "AI in healthcare" instead of "ambient documentation for 200–800 bed US hospital systems." Narrow ruthlessly.
2. **TAM theatre.** A big number with no haircut ladder. Reconciled triangulation or nothing.
3. **Falling in love.** Three weeks in, you're invested in being right. The anti-thesis and pre-written kill criteria are the antidote — write them early, while you're still objective.
4. **Mistaking a feature for a market.** Ask: would anyone buy this standalone, with its own budget line and its own buyer? If no, it's a feature of someone else's product.
5. **Ignoring the status quo competitor.** Spreadsheets and "doing nothing" win more deals than any startup on your map.
6. **Right sector, wrong layer.** The market grows 10x and all the margin accrues one layer up. Phase 4.2 exists for this.
7. **Right thesis, wrong decade.** Directionally correct, five years early, capital dead. Always ask what forces adoption *now* — a deadline, a mandate, a price point.
8. **Confusing growth with returns.** Fast-growing sectors with commodity economics and no acquirers produce zero venture returns. Run the fund math.
9. **Analyst voice.** Describing the market instead of taking a position. Nobody needs another market report. The output is a *view*.
10. **Dead-ending.** No target list, no outreach, no diligence questions. Analysis that doesn't change this week's calendar was a hobby.

---

## The 20-question self-audit

Before you present, answer every one out loud. Any "I don't know" is either your
next day of work or an explicit, stated gap in the memo.

**Market**
1. Who exactly is the buyer, and what budget line does this come from?
2. What are they doing today instead, and what does it cost them?
3. What's the market size bottom-up, and does it reconcile with top-down?
4. What's the growth rate, and what physically drives it?
5. Which segment am I actually underwriting, and why that one?

**Timing**
6. What changed in the last 24 months?
7. Who tried this before and died, and what was missing?
8. What forces the laggards to buy, and when?

**Structure**
9. Where in the value chain does margin accrue at steady state?
10. Winner-take-all or fragmented, and what's my evidence?
11. What's the moat, and does it strengthen with scale?

**Competition**
12. Why won't the obvious incumbent crush this? (structural reason, not "slow")
13. Which adjacent platform is one step away from entering?
14. Is the white space an opportunity or a graveyard?

**Economics**
15. What do best-in-class unit economics look like *in this sector*?
16. Does gross margin improve or degrade with scale?

**Returns**
17. Who buys these companies, at what multiple, and how do I know?
18. What exit value do I need, and what market share does that imply?

**Conviction**
19. What's the strongest argument against me, and what's my honest answer?
20. What would make me abandon this thesis, and when will I check?

---

## Worked micro-example (compressed, to show the shape)

**Sector:** AI-native revenue cycle management for US physician groups

| Phase | Finding |
|---|---|
| **Define** | Buyer = practice manager / CFO at 20–200 physician independent groups. Job = get claims paid faster, fewer denials. Today = offshore BPO at 4–7% of collections. |
| **Size** | Bottom-up: ~35k qualifying groups × ~$180k annual RCM spend ≈ $6.3B SAM. Value-theft: BPO labour pool much larger; capture 20% of displaced cost. Top-down category reports overstate by ~3x (they include hospital systems — out of scope). |
| **Why now** | (1) Document extraction crossed usable accuracy ~2023; (2) payer denial rates rose sharply, raising the pain; (3) BPO wage inflation eroded the offshore cost advantage; (4) staffing shortages made "hire more billers" unavailable. Four catalysts, compounding. |
| **Structure** | Fragmented-leaning (score 9/21): weak network effects, real switching costs once integrated into the practice management system, no regulatory moat. Implication: #2 and #3 can build good businesses; entry price discipline matters; consolidation play is viable. |
| **Competition** | Incumbents = legacy RCM vendors + BPOs. Why they won't respond: their P&L *is* the headcount being displaced — automating it shrinks their own revenue base. Strong structural answer. Adjacent threat: practice-management software vendors bundling it. |
| **Economics** | Gross margin 55–65% (human-in-the-loop persists on exceptions) — below SaaS but improving as automation rate rises. Underwrite the automation-rate curve, not today's margin. |
| **Returns** | Acquirer list is deep (health IT strategics, PE roll-ups, payers). Public comps trade ~4–6x revenue. $250M fund at 12% needs ~$2.1B exit → ~$400M revenue → ~6% share. **Credible in a fragmented market.** Passes fund math. |
| **Thesis** | Value accrues to whoever owns the payer-specific denial logic and the PM-system write-back, not to whoever has the best extraction model. |
| **Kill if** | Practice-management incumbents ship bundled equivalents before 2028, or automation rate plateaus below 70% (margin stays structurally capped). |

Notice what makes it a thesis rather than a report: it names the layer where
value accrues, gives a structural reason the incumbent can't respond, passes
explicit fund math, and states dated conditions under which it's wrong.

---

## The one-paragraph version

Define the market by buyer and job, not technology, and segment it before you
size it. Size it three ways and interrogate the gap between them — the gap is
your insight. Prove *why now* with at least two compounding catalysts and an
honest account of who tried before and died. Map the value chain to find where
margin will sit at steady state, and score whether the market consolidates or
fragments — that single call drives your entire strategy. Benchmark unit
economics and check whether they improve with scale. Map competitors honestly,
including the status quo, and write down the structural reason the incumbent
won't respond. Then run the fund math: at real exit multiples, what market share
does a fund-returner require, and is that credible? Convert the answer into a
falsifiable thesis with dated kill criteria, a ranked target list of 50, and
diligence questions only you know to ask. Then maintain it quarterly and keep
score of your own predictions — because the compounding edge in this job isn't
any single thesis, it's calibration.
