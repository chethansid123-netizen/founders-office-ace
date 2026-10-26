# Contact-driver teardown from public reviews: interview demo

Why do Yes Madam customers contact support, and what should be fixed first? This teardown answers that from
**500 real, public App Store reviews** (India store, 18 Jun – 21 Oct 2026). Each review is tagged with the one
problem that would make that customer contact support. From there: a Pareto, five whys on the top three drivers,
the impact in contacts and rupees, and three fixes with how to measure them.

**Bias, said out loud:** reviews skew negative (45% of written reviews are 1★ against a 4.73★ store average from
1,28,866 ratings). They come from iPhone users only, and they are not support-ticket data. Use them for the *mix*
of problems, not the rate. The impact model's inputs (contact rate, cost per contact, customer value) are labelled
assumptions.

## Headline numbers

| | |
|---|---|
| Reviews read and tagged | 500 (288 complaints, 212 praise) |
| Top 3 drivers | No-shows & cancellations 59 · Price & offer clarity 56 · Service quality 55 = **59% of complaints** |
| Weighted by who already contacted support | Top 3 = **71%**; no-shows alone = 36% |
| Already contacted support | 72 complaints (25%); 63 say support didn't fix it |
| Tagging reliability | Two independent passes agree on 98.4% (Cohen's kappa 0.98); 8 disagreements settled by a third read |
| Benchmark | Same top three as Urban Company (500 reviews, same codebook) |

## Files

| File | What it is |
|---|---|
| `Contact-Driver-Teardown.html` | The dashboard. It opens in any browser and works offline. Five slides (Pareto · Top 3 with quotes · Root causes · Impact · Fixes) and three appendix tabs: Urban Company benchmark, trends, and every review (searchable). `F` gives full screen, the arrow keys move between slides, `1`–`5` and `A`–`C` jump. |
| `Contact-Driver-Teardown.xlsx` | Working workbook. The Pareto, drivers, benchmark and reliability tabs are live formulas over the Reviews tab. Yellow cells on Impact Model are the assumptions. |
| `Contact-Driver-Teardown-Slides.pdf` | All slides as a PDF backup. |
| `Contact-Driver-Teardown-Readout.pdf` | The one-page readout: problem, root cause, impact, action. |
| `source/` | Codebook, tags and build scripts. |

## How it was built

1. **Source.** Apple's public customer-reviews RSS feed:
   `https://itunes.apple.com/in/rss/customerreviews/page=N/id=1352802457/sortby=mostrecent/json`, pages 1–10
   (500 reviews, the feed's maximum). `extract.py` turns the pages into one JSON file and drops reviewer names.
   Google Play has no public feed, and scraping it breaks its terms, so it was not used. The Android check is a
   hand-copied sample in the same sheet.
2. **Privacy.** Names of professionals and order IDs inside the review text are replaced with `[name]` and `[id]`
   (`ym_reviews_redacted.json`). The Urban Company file here keeps only dates, ratings and versions.
3. **Codebook** (`codebook.txt`, `enums.json`) covers the 8 drivers in the brief (delay, partner cancellation, payment or
   refund, price clarity, service quality, product fit, support, app), plus praise and other. Each driver has subtags
   and tie-break rules. The key rule: support is the driver only when support itself is the whole complaint.
4. **Tagging, twice.** Two independent AI-assisted passes per review (`tagging-workflow.js`). Agreement and kappa
   are measured, and a third read settles the disagreements. The merged result is `tags_final.json`.
5. **Analysis and story.** `build_data.py` merges the tags and computes every aggregate. `story.py` writes the titles,
   five whys and fixes from the data. Each five-whys step is marked as either in the reviews (with review numbers)
   or a hypothesis to verify.

## Rebuild

```bash
cd source
python3 build_data.py tags_final.json - /dev/null      # writes analysis_full.json
python3 story.py --picks                                # writes story.json (quotes from quote_picks.json)
python3 build_data.py tags_final.json story.json data.json
python3 build_html.py template.html data.json ../Contact-Driver-Teardown.html
python3 build_xlsx.py data.json analysis_full.json teardown.xlsx   # then recalculate in Excel or LibreOffice
node pdf.js "$PWD/../Contact-Driver-Teardown.html" slides.pdf light            # needs Playwright
node pdf.js "$PWD/../Contact-Driver-Teardown.html" readout.pdf light readout
```
