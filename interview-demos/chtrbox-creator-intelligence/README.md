# Creator Intelligence Engine: Chtrbox interview demo

A working prototype and a written GTM and execution plan for Chtrbox's stated move from vanity metrics to verified ROI:
AI creator discovery, brand matching, forecasting and campaign analytics, built on the real-time tracking and attribution
Chtrbox already runs. Prepared by Chethan N for the Founder's Office conversation (21 Oct 2026).

**Data note.** Every creator is a synthetic persona. Brand names are publicly reported Chtrbox clients or labelled prospects,
but every metric shown for them is simulated. Company and market figures in the plan are from public sources, cited in its appendix.

| File | What it is |
|---|---|
| `Creator-Intelligence-Engine.html` | The platform. One file, works offline. Open it in a browser. Keys `1`–`7` switch views, `/` searches, `Esc` closes a creator profile. |
| `Creator-Intelligence-Engine-GTM-Plan.pdf` | The 36-page plan: where Chtrbox stands, first principles, the platform, data and model, verified-ROI framework, Olay worked end to end, all 35 brands by vertical, GTM segmentation, 30/60/90 execution, data flywheel, 10 SOPs, KPIs, team and RACI, budget and funding, management system, guardrails, pre-flight checks, risks and honest cons, 1–2 year roadmap, interview walkthrough. |
| `source/` | Data generator, front-end source, build and render scripts. |

## The platform, in seven views

1. **Overview**: the thesis, Chtrbox's public numbers (why now), reported vs verified views, claimed vs verified ROI, how the engine works.
2. **Brand Match**: pick any of 35 brands → brand DNA → hard gates (fake audience, safety, competitor conflicts, SEBI and ASCI eligibility) → seven-part explainable fit score → plan under budget → engine vs follower-count plan at the same spend → efficiency map. Objective and weights are tunable.
3. **Creator profile**: 76 data points, audience vs brand target, forecast with a confidence band, reasons and risks.
4. **Discovery**: plain-language search ("Hindi beauty creators under 25k with ER above 3%") parsed into filters and ranked for a brand.
5. **Vertical Lens**: playbooks for FMCG, e-commerce, beauty, fashion, healthcare, BFSI, tech, services and entertainment; talent heatmap; top creators; archetypes; benchmarks by tier.
6. **Campaigns & ROI**: six simulated campaigns (Amazon live): reported → real people in target group, revenue waterfall to incremental ROAS, brand lift, geo holdout, leaderboard, alerts.
7. **How it works** and **Rollout plan**: data families, formula, gates, ROI ladder, model maturity, 30/60/90, pod, budget, KPIs, guardrails.

## Rebuild

```bash
cd source
python3 gen_data.py data.json                                   # synthetic creators, brands, campaigns
python3 build_html.py data.json fonts ../Creator-Intelligence-Engine.html
G=$(npm root -g) node export_engine.mjs ../Creator-Intelligence-Engine.html engine_export.json   # engine numbers for the PDF
python3 build_pdf.py engine_export.json data.json plan.html
G=$(npm root -g) node render_pdf.mjs plan.html ../Creator-Intelligence-Engine-GTM-Plan.pdf
```

The PDF screenshots in `source/pdf_shots/` come from the built page at 1440 px. Fonts (Bricolage Grotesque, Geist, Geist Mono;
SIL Open Font License) are embedded so the page renders the same offline.
