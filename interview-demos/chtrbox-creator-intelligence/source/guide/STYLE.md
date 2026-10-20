# Presenter's guide: writing rules for every part

The reader is **Chethan N**, a Founder's Office candidate who will demo the Creator Intelligence Engine to Chtrbox
leadership (MD & CEO Raj Mishra and team) tomorrow. He needs to (1) understand everything deeply, then (2) know exactly
what to say. Every part serves both: explain it plainly first, then give him the words.

## What you produce

Write ONE HTML fragment file at the path you are given. No `<html>`, `<head>`, `<body>` or `<style>` tags.

Start the file with:

```html
<section class="part">
  <div class="part-k">Part N</div>
  <h1>Part title</h1>
  <p class="lede">Two or three sentences: what this part gives the reader.</p>
  ...
</section>
```

Use `<section class="brk">` (a page break) before each new chapter after the first. Use `<h2>` for chapters, `<h3>` for
subsections. Only one `<h1>` per file.

## Allowed building blocks (and nothing else)

| Block | Markup |
|---|---|
| Paragraph, lists, emphasis | `<p>`, `<ul><li>`, `<ol><li>`, `<b>`, `<i>` |
| Table | `<table class="t">` with `<thead>`/`<tbody>`; add class `small` or `tiny` for dense tables; `<td class="r">` right-aligns numbers |
| Note | `<div class="call"><b>Title</b><p>Text</p></div>` |
| Key insight | `<div class="call accent"><b>Title</b><p>Text</p></div>` |
| Caution | `<div class="call warn"><b>Title</b><p>Text</p></div>` |
| **Say it like this** (the words to speak) | `<div class="say"><b>Say it like this</b><p>"Exact words in quotes."</p></div>` |
| Definition | `<div class="def"><b>Term</b><p>Plain meaning. <span class="f">Formula: ...</span> Example: ...</p></div>` |
| Worked example | `<div class="example"><b>Worked example: title</b><p>...</p></div>` |
| Formula line | `<div class="formula">Fit = ...</div>` |
| Stat cards | `<div class="kpis"><div class="kpi"><b>2.7×</b><span>label text</span></div>...</div>` (2–4 cards) |
| Numbered steps | `<div class="steps"><div class="step"><b>Step title</b><p>Text</p></div>...</div>` (auto-numbered) |
| Q&A | `<div class="qa"><div class="q"><b>Question?</b><p>Answer.</p></div>...</div>` |
| Click path | `<div class="click">Brand Match → pick Amazon → Conversion</div>` |
| Two columns | `<div class="cols2"><div>...</div><div>...</div></div>` |
| Utility | `<span class="mono">`, `<span class="muted">` |

## Tone and language

- Write to Chethan in the second person ("you"). Plain English, short sentences, active voice. Explain as you would to a
  smart person who is new to influencer marketing analytics. Define every term the first time you use it.
- Then give him the words: every important idea gets a "Say it like this" box with natural, confident spoken lines
  (first person, as Chethan would say them to the CEO).
- Indian conventions: ₹, lakh (L), crore (Cr). Write "₹42.2L", "₹1.15 Cr", "3.4M views".
- No hype words (revolutionary, game-changing, cutting-edge, leverage, unlock). No em-dash asides. Avoid "not X, but Y"
  phrasing and colon-reveal sentences. Prefer specific numbers to adjectives.
- Escape `&` as `&amp;` and `<` as `&lt;` in text.

## Numbers: the one hard rule

- Use ONLY numbers that appear in the data files you are given (`guide/data/core.json`, `guide/data/brand_<id>.json`) or
  in the source code (`app.js`, `gen_data.py`, `build_pdf.py`), or that you compute from them with the formula shown.
  Never invent a number. If you compute one, show how.
- Platform numbers are **simulated** (synthetic creators, modelled campaigns). Brand names are real Chtrbox clients (as
  publicly reported) or labelled prospects, but their metrics are modelled. Say so where it matters, and coach Chethan
  to say so out loud.
- Public company figures (FY26 revenue ₹84.22 Cr, +42.5%; EBITDA margin 17.0% vs 20.5%; PAT ₹9.2 Cr; revenue mix
  Represent 39% / Brand Solutions 36% / ChtrSocial 25%; 3L+ creators; ~104 exclusive creators; IPO ₹42.86 Cr at ₹115,
  52× subscribed, BSE SME Oct 2025; ~60% of revenue in Oct–Mar; Dubai hub Jan 2026; CEO Raj Mishra, ex-TikTok India)
  come from press coverage of filings. They are cited in the GTM plan. Say "per public coverage of the filings".
- Money fields in the data are in rupees (e.g. `spend: 4216000` = ₹42.2L). `budgetLakh` is in lakh. Shares like
  `fakeAudienceShare: 0.15` mean 15%. `er`, `linkCtr`, `realFollowers`, `viewThrough` are already percentages.

## Where things live (read what you need)

- `../app.js`: the whole platform. Engine section: `audFit`, `affOf`, `cultFit`, `perfOf`, `authOf`, `safeOf`,
  `predict`, `gatesOf`, `flagsOf`, `scoreBrand`, `whyOf`, `buildPlan`, `vanityPlan`, `aggregate`, `campStats`.
  Views: `vOverview`, `vMatch`, `centreHTML`, `planHTML`, `renderDrawer`, `vDiscover`, `parseQuery`, `vVerticals`,
  `PLAY`, `vCampaigns`, `afterCampaigns`, `vHow`, `FAMILIES`, `vPlan`, `PHASES`.
- `../gen_data.py`: how the synthetic data was generated and calibrated (tiers, ER medians, rate cards, fraud rates,
  brands, campaigns).
- `../build_pdf.py`: the 36-page GTM plan (strategy, SOPs, KPIs, team, budget, risks, Q&A). Reuse its facts; do not
  contradict it.
- `data/core.json`: overview metrics, 6 campaigns, 9 verticals, tier stats, data families, phases.
- `data/brand_<id>.json`: one brand: brief, target, languages, codes, competitors, compliance, and `byObjective`
  (awareness / consideration / conversion) with gates, top creators (fit, parts, contributions, metrics, forecast,
  why, risks), the engine plan and the follower-count plan at the same spend.
- `../pdf_shots/*.jpg`: screenshots of each screen (you may reference what they show).

## Length

Be complete; the reader asked for everything. But every sentence must teach something or give words to say. Prefer
tables for repeated structures (brand cards, metric lists). Target lengths are given in your task.
