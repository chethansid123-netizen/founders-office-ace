# Kishlay Foods, Decoded: interview pack

A 9-slide, first-principles teardown of Kishlay Foods for the Founder's Office interview (18 Nov 2026), with a
presenting playbook and the prompt that produced the deck. Funding and valuation are deliberately left out of the deck.

**Live deck (present, comment, export to editable PowerPoint or PDF):** https://claude.ai/artifact/FqFLNd7wSz5RKZ6DCZFxPv
(private until shared from its Share menu).

| File | What it is |
|---|---|
| `Kishlay-Foods-Decoded.pptx` | The 9 slides as PowerPoint, 16:9, with the full talk track in each slide's speaker notes. Slides are full-bleed images; for an editable version use Share › Export on the live deck. |
| `Kishlay-Foods-Decoded.pdf` | The same 9 slides as a PDF (1920 × 1080 pages). |
| `Interview-Playbook.html` / `.pdf` | Story spine, talk track per slide with timings, delivery rules, numbers cheat sheet with sources, likely questions with answers, a guesstimate, things to know but not lead with, the 4 questions to ask, tonight's checklist. |
| `Deck-Prompt.md` | The reusable prompt behind the deck (fill in the braces for another company). |
| `Deck-Prompt.html` / `.pdf` | The same prompt as a designed page with a copy button, notes on why each part is there, and a 60-second version. |
| `source/` | Deck source (Slides format), images, and the build scripts. |

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

**Data note.** Company facts come from kishlayfoods.com (audited 17 Nov 2026), CRISIL rating rationales, company and peer
filings, BigBasket and court records. Anything marked "est." is my estimate; the working is in the playbook.
Product photos, logos and plant photos are Kishlay's own, taken from its website for this analysis.

## Rebuild

```bash
cd source
python3 prep_assets.py <downloaded_images_dir> <site_screenshots_dir> assets   # images from kishlayfoods.com → WebP
python3 build_local.py deck assets /tmp/deck.html --still                       # assemble the Slides files into one page
node export.cjs /tmp/deck.html ../Kishlay-Foods-Decoded.pdf /tmp/pngs           # PDF + 2x PNGs
python3 build_pptx.py deck /tmp/pngs ../Kishlay-Foods-Decoded.pptx              # PPTX with speaker notes
node shoot_slides.cjs /tmp/deck.html /tmp/pngs                                   # previews + overflow check
python3 build_prompt_page.py ../Deck-Prompt.md ../Deck-Prompt.html
node doc_pdf.cjs ../Interview-Playbook.html ../Interview-Playbook.pdf /tmp/pb   # documents → A4 PDF
```

`blob_map.json` maps the live deck's uploaded image ids to the files in `assets/`. Fonts: Bricolage Grotesque and Inter
(Google Fonts, SIL Open Font License).
