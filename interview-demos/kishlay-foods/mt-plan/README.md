# Kishlay: winning modern trade (MT-first plan)

The reframed problem: get Kishlay into **modern trade (17% of the market in the brief)** first and **quick commerce (7%)** second. Fix EBITDA before scaling, test in a few strong stores near the Amingaon plant, then grow with the market. There is no export, no Nepal/Bhutan/Dubai and no bolt-on M&A in this plan.

| File | What it is |
|---|---|
| `Kishlay-MT-Plan.pdf` | 9 slides: 8 story slides and 1 slide of sources, links and workings. Every page links to the live model. |
| `Kishlay-MT-Plan.pptx` | The same slides with speaker notes; the links are clickable. |
| `Kishlay-MT-Model.xlsx` | 16-sheet model, 1,029 live formulas, 0 errors. Slow / Base / Fast in `Inputs!B3`. |
| `source/build_mt_model.py` | Rebuilds the model: `python3 source/build_mt_model.py Kishlay-MT-Model.xlsx` |
| `source/deck/project/` | Slide source (Claude Slides format): `deck.json`, `deck.css`, `slides/*.html` with speaker notes. |

**Live model (Google Sheet, private to the owner's Drive):** https://docs.google.com/spreadsheets/d/1EgiCZVVSYeVSpB-YicHgPpEQb81R1eqQ0Hub-aNuyo8/edit
**Deck online (private until shared):** https://claude.ai/artifact/KAz7ANTkhf59YGxAaJAe6B

## The story in 9 slides

1. **Cover.** A mother at 1.4 m and a child at 1.1 m in a snack aisle (AI-generated illustration of a generic store). The channel split from the brief: kirana 76%, MT 17%, QC 7%.
2. **Where we stand.** FY25 ₹288 Cr (−16%) with a ₹6.31 Cr loss. The pack, not the channel, makes the money: a ₹10 namkeen pouch leaves ₹13/kg, a 400 g pack ₹45–51/kg and a kids’ rings multipack ₹82/kg.
3. **Fix EBITDA first.** +215 bps from purchase, plant and trade spend, each lever with an owner. EBITDA reaches 7% in month 15 (Slow 21 months, Fast 9) and 8.2% at full effect.
4. **Who buys.** Behaviour and motive first, then age and income. The shelf by eye level, and a price ladder from ₹10 to ₹249.
5. **What we sell.** 12 SKUs with five jobs, launching 8. Each SKU shows its value and volume per store, ₹/kg, shelf life and the raw material to buy.
6. **Where first.** 5 stores within 30 km, then Assam, then the Northeast, then Kolkata. Includes the chain scorecard, test-store rules, vehicles, replenishment and QA.
7. **Win the buyer.** One store’s P&L (6.7-month payback), how the buyer reads a range (A/B/C), renegotiation from store 6, receivables by chain, and push vs pull.
8. **Plan and numbers.** Pilot → Prove → Propagate with gates, quick commerce second, and FY26E–FY31P Base: revenue ₹311 → ₹501 Cr, MT + QC 2% → 3.8%, EBITDA 6.0% → 8.4%.
9. **Sources, links and workings.** Sources checked against the original vs secondary ones, claims not used, every formula, the Base assumptions, and what to replace in week 1.

## Model sheets

Summary · Inputs · Scale · EBITDA · SKU_Plan · Unit_Econ · Store_PnL · Chains · Supply_Chain · Procurement · Segments · QC_Plan · Data_Capture · Primary_Research · Market · Sources.
Colour code: blue input · black formula · green link · yellow = validate first. Every input has a basis and a label (Company / External / Historical / Calculation / Hypothesis).

## Replace these first (week 1)

FY26 sales and EBITDA (the 6% starting margin is a hypothesis), SKU costing and pack grams (the ₹10 pouch is assumed to be 40 g), today’s MT and e-commerce sales (assumed 2%), and vehicle contracts and trip costs.

## Notes

- Tracxn figures are cited from the MCA filings and not redistributed.
- Claims from the shared research compendium that could not be verified (Kearney discount ranges, Redseer QC uplift, ICICI loyalty, “+39% at eye level”) are not used in any number.
- The Google Sheet and the online deck are private. Share them from Drive and from the deck’s Share menu before sending the links to anyone.
- To rebuild the exports: `python3 ../source/build_local.py source/deck ../source/assets out.html --still`, then `node ../source/export.cjs out.html Kishlay-MT-Plan.pdf <png_dir>`, `node ../source/get_links.cjs out.html links.json`, `python3 ../source/build_pptx.py source/deck <png_dir> Kishlay-MT-Plan.pptx links.json`.
