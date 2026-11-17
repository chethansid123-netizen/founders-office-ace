# Kishlay Group: the ₹512 Cr plan

The Founder's Office deliverable for Tulsi Speciality Foods Pvt Ltd (manufacturing, 99% owned by Kishlay Foods Pvt Ltd), built around one problem:
*how can Tulsi break out of the low-margin ₹5/₹10 general-trade trap and scale to ₹512 Cr at ~10% EBITDA through a 90-day roadmap across
quick-commerce and modern-trade multipacks, asset-light 3P and M&A, and exports to Nepal and the GCC?*

**Live deck** (present, comment, export to editable PowerPoint or PDF; private until shared from its Share menu):
https://claude.ai/artifact/98v55rqXHTb9uKftpntXbA

## The answer

- **Not more packs, more money per kilo.** One kilo earns ~₹34 of contribution in ₹10 kirana packs, ₹49 in modern trade, ₹54 on quick commerce,
  ₹99 on a UAE shelf, but ₹19 as a Nepal export (30% duty, 13% VAT).
- **₹512 Cr, tested.** FY25 revenue fell 16% to ₹288 Cr with a ₹6.31 Cr loss (Tracxn, MCA filing). The base case reaches ~₹458 Cr and ~₹46 Cr
  EBITDA (10%) in FY29; ₹512 Cr arrives in FY31, or in FY29 only on the bull case (₹564 Cr). Recommendation: commit to ~₹460 Cr and ~₹46 Cr EBITDA,
  keep ₹512 Cr as the stretch, steer by EBITDA.
- **Engines to FY29:** quick commerce ₹14 Cr · modern trade + online ₹19 Cr (Vishal Mega Mart and Guwahati supermarkets first, Kolkata chains next,
  400 doors) · exports ₹34 Cr (Bhutan → Nepal → GCC) · co-packing ₹36 Cr · one ₹30 Cr bolt-on.
- **90 days:** five workstreams, gates at weeks 4, 8 and 13, ₹57.3 lakh budget (₹35 lakh is stock that sells), a 15-KPI monthly MIS.

## Files

| File | What it is |
|---|---|
| `Kishlay-512-Plan.pptx` / `.pdf` | 18 slides: 14 main (hook, problem, per-kilo insight, peer proof, ₹512 Cr test, revenue bridge, margin bridge, quick commerce, modern trade break-in, exports, 3P and M&A, 90-day roadmap, operating system, day-90 decisions) + appendix (sources, assumptions, export buyers, who is who). Full speaker notes. |
| `Kishlay-512-Growth-Model.xlsx` | 19 sheets, 753 formulas, 0 errors. Scenario switch in `Inputs!B3` (Bear/Base/Bull). Key sheets: `Target_Check` (five tests, live scenarios, gap closers, value lens, verdict), `MT_Plan` (chains, terms, door economics, rollout, gates), `Rev_Bridge`, `EBITDA_Bridge`, `Unit_Econ`, `Export_Buyers`, `Price_Audit` (tonight's screenshot sheet), `Pilots`, `Roadmap_RAG`, `Board_MIS`, `Sources` (S01–S60 with links). |
| `Kishlay-512-Playbook.html` / `.pdf` | How it was built (the prompt, sources, assumptions and trade-offs, what is missing), the ₹512 Cr backbone, what the Tracxn data changed, modern-trade break-in plan, hook and engagement, script for every slide, days 1–30, Q&A, questions to ask, numbers cheat sheet, tonight's checklist. |
| `Kishlay-512-OnePager.html` / `.pdf` | One-page leave-behind. |
| `source/` | `build_model.py` (the Excel model), `build_playbook.py` + `playbook.css`, and `deck5/` (the Slides files). Deck build scripts live in `../source/`. |

Every number is labelled Company, External, Historical, Calculation or Hypothesis. Tracxn data was supplied for this work and is cited, not
redistributed; the raw exports are not in this repository.

## Rebuild

```bash
python3 source/build_model.py Kishlay-512-Growth-Model.xlsx
python3 <xlsx-skill>/scripts/recalc.py Kishlay-512-Growth-Model.xlsx 90
cd ../source && python3 build_local.py ../growth-512/source/deck5 assets /tmp/d5.html --still
node export.cjs /tmp/d5.html ../growth-512/Kishlay-512-Plan.pdf /tmp/d5png
python3 build_pptx.py ../growth-512/source/deck5 /tmp/d5png ../growth-512/Kishlay-512-Plan.pptx
cd ../growth-512 && python3 source/build_playbook.py source/deck5 Kishlay-512-Playbook.html
node ../source/doc_pdf.cjs Kishlay-512-Playbook.html Kishlay-512-Playbook.pdf /tmp/pb
```
