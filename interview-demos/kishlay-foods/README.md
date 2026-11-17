# Kishlay Foods, Decoded: interview pack

A 9-slide, first-principles teardown of Kishlay Foods for the Founder's Office interview (18 Nov 2026), with a
presenting playbook and the prompt that produced the deck. Funding and valuation are deliberately left out of the deck.

**Live decks (present, comment, export to editable PowerPoint or PDF), private until shared from their Share menu:**
- Deck 1, *Kishlay Foods, Decoded* (9 slides, the story): https://claude.ai/artifact/FqFLNd7wSz5RKZ6DCZFxPv
- Deck 2, *The Operating Machine* (20 slides, chart-first: hub-and-spoke, plant, pack physics, price tiers, all 236 SKUs, distribution, a six-slide competition chapter with positioning map, five forces, blue ocean, BCG and Ansoff, constraints): https://claude.ai/artifact/Gu16ckmyge4xzT8czsMpKT

- **Deck 3, *Kishlay Foods in 10 Slides*** (the 20-slide operating deck compressed into 10 dense, left-to-right story slides — use this one to present): https://claude.ai/artifact/NpweY5vAm9utsAEay1geVQ

All decks share one look: a white background on every slide, a red band across the top, and the Kishlay logo.

| File | What it is |
|---|---|
| `Kishlay-Foods-Decoded.pptx` | The 9 slides as PowerPoint, 16:9, with the full talk track in each slide's speaker notes. Slides are full-bleed images; for an editable version use Share › Export on the live deck. |
| `Kishlay-Foods-Decoded.pdf` | The same 9 slides as a PDF (1920 × 1080 pages). |
| `Kishlay-in-10-Slides.pptx` / `.pdf` | Deck 3: the 10-slide version — hook, why + illustrated hub-and-spoke, inside the plant, packs and price, range treemap, distribution and the ₹10 split, 17 rivals by tier and product, five forces with sourced numbers, where to play (blue-ocean map + Ansoff), limits and the 90-day plan. Speaker notes on every slide. |
| `Kishlay-Operating-Machine.pptx` / `.pdf` | Deck 2: 20 chart-first slides on how the business runs, with speaker notes. No branding or marketing content. |
| `Interview-Playbook.html` / `.pdf` | Story spine, talk track per slide with timings, delivery rules, numbers cheat sheet with sources, likely questions with answers, a guesstimate, things to know but not lead with, the 4 questions to ask, tonight's checklist. |
| `Deck-Prompt.md` | The reusable prompt behind the deck (fill in the braces for another company). |
| `Deck-Prompt.html` / `.pdf` | The same prompt as a designed page with a copy button, notes on why each part is there, and a 60-second version. |
| `source/` | Deck sources (`deck/`, `deck2/`, `deck3/`, Slides format), images, and the build scripts. |

## The nine slides

1. **Hook**: same ₹10 packet, Kishlay keeps ~25 paise (est.), Gopal ~52, Bikaji ~76.
2. **Why Kishlay exists**: mostly air, one narrow corridor, humidity, coin MRPs → make it where it's eaten.
3. **What it built**: ₹5 → ₹250 price-pack ladder, 236 products by category, brands.
4. **Make**: plants and capacity, inputs at 70–75% of cost, estimated 50–75% utilisation.
5. **Move**: five hops to the kirana and the ₹10 waterfall; ~₹17k sales per outlet a year.
6. **Sell**: the hanging strip, customer vs consumer, the 3-second funnel, three shoppers.
7. **Fight**: three competitor tiers and a peer-economics table.
8. **Brand & digital**: Keller pyramid and an 8-point website audit with the fix.
9. **Plan**: north star (sales per active outlet), four moves over 90 days and 12 months, what I'd own.

## Deck 2: The Operating Machine

1. Cover · 2. Five numbers (KPI tiles with mini charts) · 3. Hub-and-spoke diagram · 4. Inside the North Guwahati hub ·
5. Pack formats and shelf-life chart · 6. Price staircase · 7. Treemap of all 236 products · 8. Pack wall ·
9. Distribution: five hops and four KPIs · 10. Positioning map (price × reach) · 11. Porter’s five forces ·
12. Peer economics and rivals by aisle · 13. Red ocean vs blue ocean: strategy canvas and ERRC grid · 14. BCG matrix (directional) ·
15. Ansoff growth matrix · 16. Four constraints · 17–20. Appendix: every product name by category.

**Data note.** Company facts come from kishlayfoods.com (audited 17 Nov 2026), CRISIL rating rationales, company and peer
filings, BigBasket and court records. Anything marked "est." is my estimate; the working is in the playbook.
Product photos, logos and plant photos are Kishlay's own, taken from its website for this analysis.

## Rebuild

```bash
cd source
python3 prep_assets.py <downloaded_images_dir> <site_screenshots_dir> assets   # images from kishlayfoods.com → WebP
python3 build_local.py deck assets /tmp/deck.html --still                       # assemble the Slides files into one page
node export.cjs /tmp/deck.html ../Kishlay-Foods-Decoded.pdf /tmp/pngs           # PDF + 2x PNGs (use deck2 for Deck 2)
python3 build_pptx.py deck /tmp/pngs ../Kishlay-Foods-Decoded.pptx              # PPTX with speaker notes
node shoot_slides.cjs /tmp/deck.html /tmp/pngs                                   # previews + overflow check
python3 build_prompt_page.py ../Deck-Prompt.md ../Deck-Prompt.html
node doc_pdf.cjs ../Interview-Playbook.html ../Interview-Playbook.pdf /tmp/pb   # documents → A4 PDF
```

`blob_map.json` maps the live deck's uploaded image ids to the files in `assets/`. Fonts: Bricolage Grotesque and Inter
(Google Fonts, SIL Open Font License).
