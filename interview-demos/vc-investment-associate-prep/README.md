# VC Investment Associate: interview prep

A prep workbook for the Investment Associate general round with Chandru (CEO) at People Moves, a new
venture-capital arm. A web search found no public coverage of the firm, so tab 23 is a fill-in sheet for your own
research. **Companies in the worked examples are fictional and every number is illustrative.** Benchmarks are rules
of thumb and change with stage, sector and market cycle.

| File | What it is |
|---|---|
| `VC-Investment-Associate-Prep.xlsx` | The workbook: 24 tabs, 695 live formulas. Change any yellow cell and the results recalculate. |
| `source/` | The build script and the content files (glossary, sectors, Q&A, term sheet, checklists). |

## Tabs

| Tab | Contents |
|---|---|
| 00 Start Here | Legend, contents, what an associate does, likely interview flow, a 6-hour study plan, night-before cheat sheet |
| 01 How VC Works | LPs/GPs, money flow, stages and round sizes in India, fund life, exits, corporate VC vs independent VC, key regulations |
| 02 Glossary | 176 terms (ARR, MRR, ROI, CAC, LTV, NRR, burn multiple, IRR, TVPI, CCPS, TRL, rNPV…), each with formula, example, benchmark and why a VC cares |
| 03 Formula Lab | Every key formula as a live calculator |
| 04 Consumer | D2C unit economics (CM1/CM2/CM3), five-channel comparison, cohorts, LTV:CAC, P&L, working capital, evaluation lens |
| 05 Deep Tech | TRL ladder, milestone funding and dilution, learning-curve unit economics, risk-adjusted VC method, grants, evaluation lens |
| 06 Healthcare | Segment map, diagnostic-centre unit economics, medtech rNPV, drug success rates, regulatory pathways, evaluation lens |
| 07 Sector Playbook | 42 industries, each with a one-line summary of how it runs, plus how it makes money, metrics, flags, examples and how to evaluate it |
| 08 Founder Evaluation | Weighted scorecard (live), founder signals, founder types including manufacturing founders, reference-check questions |
| 09 Manufacturing | 5-year plant model: utilisation, EBITDA, ROCE, break-even, payback, plus a diligence checklist |
| 10 Valuation | VC method, comps, DCF, Scorecard, Berkus, First Chicago |
| 11 Cap Table | Seed + Series A with the option-pool shuffle, SAFE conversion, dilution chain |
| 12 Waterfall | Liquidation preference: non-participating vs participating vs capped |
| 13 Term Sheet | Every clause decoded, plus a live anti-dilution example |
| 14 Fund Economics | Fees, reserves, portfolio construction, power-law outcomes, carry, LP waterfall, J-curve and IRR |
| 15 Financial Statements | Linked P&L, balance sheet and cash flow, ratios, red flags |
| 16 Deal Process | 10-step process with the associate's job at each step, money flow, use of funds by sector, portfolio KPIs |
| 17 Market Sizing | TAM/SAM/SOM top-down and bottom-up, venture-scale check, guesstimate method |
| 18 India Landscape | Funds by focus, government programmes, data sources, 2026 themes |
| 19 Interview Q&A | 75 likely questions with what is being tested, how to structure the answer, and sample answers |
| 20 Mini Cases | Case framework and 5 worked cases |
| 21 IC Memo | Investment-memo template with an example column |
| 22 DD Checklist | Due-diligence checklist with status dropdowns |
| 23 Firm & Questions | Firm and CEO research sheet, questions to ask, "tell me about yourself" draft |

## Rebuild

```bash
cd source
python3 build_xlsx.py ../VC-Investment-Associate-Prep.xlsx   # then open in Excel, or recalculate in LibreOffice
```
