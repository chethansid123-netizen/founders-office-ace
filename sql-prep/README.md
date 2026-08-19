# Postgres Interview Sandbox

A complete PostgreSQL reference wired to a **real PostgreSQL database that runs inside a web page** —
no server, no Docker, no install, works offline. Built for interview prep.

The published sandbox is a single self-contained HTML file (~8 MB) containing PostgreSQL 18.3
compiled to WebAssembly ([PGlite](https://github.com/electric-sql/pglite)), the teaching database,
25 chapters of reference material, and 60 graded drills with automatic answer checking.

---

## What's here

| File | What it is |
|---|---|
| `01_schema.sql` | The teaching database DDL. Written to double as the CREATE TABLE lesson — every constraint type appears at least once, commented. |
| `02_seed.sql` | Seed data, generated deterministically. Small enough to verify results by hand. |
| `sandbox.template.html` | All 25 chapters of reference content, plus the page shell and styles. |
| `drills.js` | The 60 practice problems and their model solutions. |
| `app.js` | Engine boot, SQL syntax highlighting, the console, and the answer checker. |
| `build.cjs` | Assembles everything into one standalone HTML file. |
| `runner.cjs` | Terminal REPL — same engine, same data, for practising without a browser. |
| `verify.cjs` | Test suite: data properties, all 60 drill solutions, all 100 reference examples. |

## The database

Eight tables modelling a B2B software business, seeded so that **every trap in the material is
demonstrable on real data**:

```
departments ──< employees ──┐ (self-referencing manager_id, 4 levels deep)
                            │
customers ──< orders ──< order_items >── products
    │
    └──< web_events                      staging_signups (deliberately dirty)
```

Deliberate properties the material depends on — all asserted by `verify.cjs`:

- 3 customers have **no orders**, 2 products were **never ordered**, 2 departments are **empty** → anti-joins
- The CEO has `manager_id IS NULL` **and** `dept_id IS NULL` → an inner join silently drops them
- 2 customers have a **NULL city**; one employee has a **NULL email** → NULL handling
- 4 groups of **tied salaries** → `RANK` vs `DENSE_RANK` vs `ROW_NUMBER` genuinely differ
- One employee **earns more than their manager** → the classic self-join question
- The employee tree is **4 levels deep** → recursive CTEs
- Orders span **6 months** with a dip in April → month-over-month growth, running totals
- Customer 1 has exactly **3 runs of consecutive active days** → gaps-and-islands
- `staging_signups` contains **exact duplicates and a case-variant duplicate** → de-duplication
- `orders` (48 rows) → `order_items` (119 rows) is a **fan-out** → double-counting

## Build the standalone sandbox

```bash
cd sql-prep
npm i @electric-sql/pglite esbuild
node build.cjs                 # → dist/sandbox.html
```

Open `dist/sandbox.html` in any browser. It needs no network connection at runtime
(the only external request is Google Fonts, which degrades to system fonts).

## Practise in the terminal instead

```bash
npm i @electric-sql/pglite
node runner.cjs
```

```
sql> \d                    list tables          \d orders    describe one
sql> \list hard            list drills          \drill 27    show a drill
sql> \sol 27               show its solution    \check 27    check your last query
sql> \reset                rebuild the database \q           quit
```

Anything else is run as SQL. `\check` compares your result set against the model solution —
row order is ignored unless the drill says it matters, and column names are ignored.

## Verify everything still works

```bash
node verify.cjs
```

Checks the 18 seeded-data properties, executes all 60 drill solutions, and runs all 100
runnable examples from the reference. Two examples are *meant* to fail — they teach the
`GROUP BY` and "window functions are not allowed in WHERE" error messages — and are named
explicitly in the expected-failures list rather than silently skipped.

## Why PostgreSQL and not SQLite

SQLite is smaller and boots faster, but it cannot run `GROUPING SETS`, `ROLLUP`, `CUBE`,
`LATERAL`, `DISTINCT ON`, `ILIKE`, `EXTRACT`, `MERGE` or `TRUNCATE` — all of which are fair
game in a PostgreSQL interview. Shipping real PostgreSQL costs about 7 MB of compressed
WebAssembly and roughly 5 seconds of first load, and in exchange every example in the
material is genuinely runnable and the error messages are the real ones.
