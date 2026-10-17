# VP Ops weekly MIS: interview demo

A sample weekly MIS for a VP Operations at an at-home beauty services company, built as a demo for the
Founder's Office – Operations interview (Mon 19 Oct 2026). **Every number is mock data**, scaled to public
figures (about 3.5 lakh bookings a month, about 7,500 active partners). None of it is actual company data.

| File | What it is |
|---|---|
| `VP-Ops-Weekly-MIS-Dashboard.html` | The dashboard: 6 slides and 2 appendix slides. Open in a browser; it works offline. `F` for full screen, arrow keys to move. |
| `VP-Ops-Weekly-MIS.xlsx` | The same MIS as a working Excel model. Pick a week and a city on the Weekly MIS tab and everything recalculates. |
| `VP-Ops-Weekly-MIS-Slides.pdf` | The 8 slides as a PDF backup. |
| `source/` | The data generator and build scripts. |

Slides: North Star (perfect bookings) · Weekly scorecard · Demand & fulfilment · Partner supply · Quality, CX & kits ·
Manager actions & review rhythm · Data health · How the pack maps to the JD.

## Rebuild

```bash
cd source
python3 gen_data.py data.json                          # mock data
python3 build_html.py template.html data.json ../VP-Ops-Weekly-MIS-Dashboard.html
python3 build_xlsx.py data.json mis.xlsx               # then recalculate in Excel or LibreOffice
```

For the PDF, open the dashboard with `?print` added to the URL, then print to PDF at 1440 × 900.
