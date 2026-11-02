# Movers Signal

Leadership seats before the mandate. Movers Signal reads public NSE and BSE filings about senior
leadership changes, finds seats that are open or at risk, ranks them with a transparent priority
rule, and gives the matching practice a brief where every fact links to the page of the filing it
came from.

*Independent prototype built from public filings. Not affiliated with Positive Moves.*

## What is in the data

| | |
|---|---|
| Window | Filings dated 4 Aug 2026 to 2 Nov 2026 (90 days to the data date) |
| Sources | NSE and BSE filing PDFs only (Regulation 30 disclosures) |
| Study set | 50 filings, 53 verified seats, all eight practices |
| Reviewed | 57 filings (7 kept as review tests), 51 more screened out at triage |
| Checked | 731 fields per verification run, 2 runs, 3 independent text engines |
| Rejected | 7 records, each with a written reason |

Every count above is produced by the pipeline; see [AUDIT.md](AUDIT.md) for the full audit, every
correction and every rejection.

## The rules it keeps

1. Facts come only from primary filings (NSE, BSE or the company's own filing PDF).
2. Nothing is invented. A field the filing does not state is stored as `null`.
3. Every extracted field carries the source URL, page and an exact supporting quote under 15 words.
4. Everything shown is labelled **Filed fact**, **Derived** or **Hypothesis**.
5. The reason someone left is shown only as the filing states it.
6. No candidates are named. No personal phone numbers or e-mail addresses are stored or shown.
7. No LinkedIn scraping, paid data or Positive Moves internal data.
8. The score is a priority rule, never a probability; no accuracy is claimed.
9. Robots rules, access controls and site terms are respected. A block stops the run and writes a
   list of filings to download by hand into `data/raw/`.

## Run the site

```bash
npm install
```

```bash
npm run dev
```

The site is a static export: `npm run build` writes plain HTML, CSS and JS to `out/`, which any
static host can serve. There is no login and no database; it reads `data/records.json` and shows
only records whose `review_status` is `VERIFIED`.

| Page | What it shows |
|---|---|
| `/` Radar | Three computed summary numbers, four filters (practice, role level, event type, successor status) kept in the URL, ranked seats |
| `/seat/<id>/` Seat brief | Filed facts with quotes and PDF links, priority breakdown, derived fields, three Hypothesis sections, the before-outreach checks that need PINE access |
| `/pulse/` Market pulse | Seats by practice, by role level, and the share with no permanent successor, with n on every chart |
| `/method/` Method | Sources, pipeline, audit counts, definitions, score formula, known limits, next phase |

## Quality gates

```bash
npm run check:all
```

That runs, in order: ESLint, the TypeScript compiler, the Vitest suite (score rule, filters, URL
filters, data invariants), the static build, and `scripts/check-site.mjs`, which reads `out/`
independently of the site code and fails if:

- a rejected or unreviewed record appears anywhere in the output (HTML, payloads or JS);
- the seat pages differ from the verified set;
- an external link is not a source PDF confirmed by the link check;
- any tagged number differs from a fresh recomputation from `data/records.json`;
- the disclaimer is missing from a page, "probability" is used other than negated, or an e-mail
  address or phone number appears.

## Rebuild the data

Python 3 with `requests`, `pdfplumber`, `pypdfium2` and poppler's `pdftotext`. Run from this folder:

```bash
python3 -I pipeline/fetch.py
```

```bash
python3 -I pipeline/textify.py
```

```bash
python3 -I pipeline/build_pass1.py
```

```bash
python3 -I pipeline/verify.py data/extracted_v1.json data/verification_v1.json
```

```bash
python3 -I pipeline/apply_corrections.py
```

```bash
python3 -I pipeline/verify.py data/extracted_v2.json data/verification_v2.json --queue
```

```bash
python3 -I pipeline/stable_links.py
```

```bash
python3 -I pipeline/apply_review.py
```

```bash
python3 -I pipeline/build_audit.py
```

```bash
python3 -I pipeline/check_links.py
```

Human review: open `review.html`, approve or reject each record beside its source, export the
decisions to `data/review_decisions_human.json`, and run `apply_review.py --require-human`. Human
decisions override the AI second reader. **The current decisions are the AI second reader's; a
person's sign-off is still pending.**

## Layout

| Path | Contents |
|---|---|
| `pipeline/` | Fetch, text extraction, pass 1 extraction, independent verification, corrections, review merge, audit, link checks |
| `data/raw/` | Manifest (URL, SHA-256, pages) and the redacted page text of each filing used |
| `data/` | `extracted_v1/v2.json`, `verification_v1/v2.json`, `corrections.json`, `review_queue.json`, `records.json`, `audit.json`, `link_check.json` |
| `config/` | `score.json` (weights), `role_levels.json`, `practices.json`, `hypotheses.json` |
| `lib/` | Pure TypeScript: score rule, filters, summary, hypotheses, data loading |
| `app/`, `components/` | The four screens |
| `tests/` | Vitest suite |
| `scripts/check-site.mjs` | Post-build site check |

## Known limits

Listed companies only; private companies are not covered. A sample of 50 filings chosen to cover
all eight practices, not every filing in the window. No outcome data, so the priority rule cannot be
called accurate yet. "Other exits" counts only exits inside this dataset. Role level and practice
come from rules. One BSE filing is too recent to have a permanent address yet; re-run
`pipeline/stable_links.py` in a few days.

## Next phase

Join each signal to PINE (relationships, off-limits and conflicts, past searches), compare
priority with the mandates that actually followed and tune the weights, and run the pipeline daily
on the exchange feeds with the same verification and review.
