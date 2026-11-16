# Revenue Desk for yuj.dna

One working tool for running sales, marketing and business development for [yuj.dna](https://www.yujdna.com/)'s two programs
(Product & Experience Mastery, ₹1,49,000, 12 weeks; Human–AI & Agentic Systems Design, ₹90,000, 7 weeks). It holds the
playbook and the pipeline in the same place, so what to say next sits beside the person you are about to say it to.
Prepared by Chethan N. Independent work, not an official yuj.dna or Yuj Designs product.

**Data note.** Program names and fees are as published on yujdna.com in November 2026. Company funding rounds are as
published by StartupTalky and Indexed.vc (read 14–16 Nov 2026); headcounts are from a Clay search (16 Nov 2026). Research
figures are listed inside the tool under Evidence with source, year, limits and whether they were re-checked while building.
The 26 sample leads and their companies are invented and marked as samples. Costs, seat caps, conversion targets and
discount limits are placeholders, editable under Setup.

| File | What it is |
|---|---|
| `Revenue-Desk.html` | The tool. One file, works offline, saves to the browser it is opened in. |
| `artifact/revenue-desk.html` | The same page for publishing inside Claude, where leads are saved to the page's own database and the Claude, Gmail and Clay features switch on. |
| `source/` | Content (`d*.js`), app (`a*.js`), styles, template and `build.py`. |

## The fourteen screens

**Operate**
1. **Today** — what to do first, from 13 rules watching the pipeline (new lead waiting, overdue step, offer gone quiet, cohort behind pace, two people from one company…), plus first-response time, stage conversion against target, reasons people hesitate, and cost per learner by source.
2. **Leads** — table and board. Each person's panel has: next step and date, the opening lines and call questions for their segment, the explain-it scoring sheet (ten dimensions taken from the programs' own skill lists), the hesitation and its play, the offer with scholarship levers, history, and one-tap logging.
3. **Accounts** — 94 funded Indian companies by stage (Seed, Series A, Series B, Series C+) with round, investors, headcount where known, who to reach by role, the LinkedIn search for each role, and how to get in at that stage.
4. **Cohorts** — seats against pace, scholarship pool used, learners at risk, referral asks due, the leads-needed calculator and cohort economics.

**Playbook**
5. **Segments** — 13 buyers (product manager, designer, design manager, researcher, product leader, founder's office, program manager, brand and marketing, sales, operations, engineer, consultant, founder). For each: root problem, what they believe against what the evidence says, when they buy, how they see themselves, opening lines, call questions, where to find them.
6. **Funnel** — top, middle, bottom and after: goals, plays, a nine-touch cadence, the first principles, how selling works in 2026, and a 90-day plan.
7. **Scripts** — the explain-it call, the mentor conversation and the offer call minute by minute; message templates by stage; prompts for Claude.
8. **Objections** — twelve distinct reasons behind a no, each with how to confirm it, what to say, what to show and what not to do; and the payment ladder for when they want it and are not paying.
9. **Pricing** — scholarship calculator where every reduction buys something, with the reasoning for why this number and not a larger one.

**Know**
10. **Market** — positioning map, competitors with fees and sources, channels, buyer psychology, market size against delivery capacity, gaps on the website.
11. **Data** — what is captured at each touchpoint, how much effort it costs, which decision it feeds; the lead score and how to check it against outcomes.
12. **Evidence** — every figure used, with source and limits.

**System**
13. **Automation** — the rules, switchable, and what connects.
14. **Setup** — assumptions, seventeen open questions with working answers, import, export, backup.

## Rebuild

```bash
cd source
```

```bash
python3 build.py
```

Fonts (Bricolage Grotesque, Geist, Geist Mono; SIL Open Font License) are embedded from `../chtrbox-creator-intelligence/source/fonts`.

## What is and is not verified

- Tested in a headless browser: every screen and tab at 1440 px, 400 px and in dark mode with no script errors or sideways scroll; adding, scoring, offering, logging, CSV import, persistence across reload, sample removal, full wipe; a simulated run of the Claude-hosted database path; and an injection test on user-entered fields.
- Not exercised against the live services: creating a Gmail draft and searching Clay from inside the page. Both are coded to those tools' published inputs and fail with a plain message if the connector is missing.
- Stage conversion targets are public agency benchmarks, not yuj.dna's own numbers. Replace them after the first month of real leads.
