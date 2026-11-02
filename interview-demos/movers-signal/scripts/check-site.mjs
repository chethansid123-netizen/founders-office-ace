#!/usr/bin/env node
// Checks the built site in out/ against the data, independently of the site's own code.
//
//   1. No rejected or unreviewed record reaches the site (ids, and names/companies
//      that appear only in rejected records), in HTML, RSC payloads or JS.
//   2. There is a seat page for every verified record and for nothing else.
//   3. Every external link points to a source PDF of a verified record (or a
//      cited practice-evidence filing), and that PDF passed the link check.
//   4. Every number tagged data-metric equals a fresh recomputation from
//      data/records.json, so no summary number is hard-coded.
//   5. The disclaimer is on every page; "probability" only ever appears negated;
//      no e-mail address or phone number appears anywhere.
//
// Usage: node scripts/check-site.mjs   (after `next build`)

import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join, relative, extname } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname;
const OUT = join(ROOT, "out");
const read = (p) => readFileSync(join(ROOT, p), "utf8");

const failures = [];
const fail = (msg) => failures.push(msg);
const ok = (msg) => console.log(`  ok  ${msg}`);

if (!existsSync(OUT)) {
  console.error("out/ not found: run `npm run build` first.");
  process.exit(2);
}

const { records } = JSON.parse(read("data/records.json"));
const score = JSON.parse(read("config/score.json"));
const practices = JSON.parse(read("config/practices.json"));
const manifest = JSON.parse(read("data/raw/manifest.json"));
const linkCheck = existsSync(join(ROOT, "data/link_check.json")) ? JSON.parse(read("data/link_check.json")) : null;

const verified = records.filter((r) => r.review_status === "VERIFIED");
const others = records.filter((r) => r.review_status !== "VERIFIED");

function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}
const files = walk(OUT).filter((p) => [".html", ".txt", ".js", ".json"].includes(extname(p)));
const htmlFiles = files.filter((p) => p.endsWith(".html"));
const contents = new Map(files.map((p) => [p, readFileSync(p, "utf8")]));
const rel = (p) => relative(OUT, p);

// Decode the HTML-escaped and JSON-escaped forms a string can take in the output.
const forms = (s) => [s, s.replace(/&/g, "&amp;"), JSON.stringify(s).slice(1, -1), s.replace(/'/g, "&#x27;")];
const appears = (s) => {
  const hits = [];
  for (const [p, text] of contents) if (forms(s).some((f) => text.includes(f))) hits.push(rel(p));
  return hits;
};

console.log(`Checking ${htmlFiles.length} pages and ${files.length - htmlFiles.length} payload files in out/`);

// 1. Nothing unverified leaks.
const verifiedText = new Set(verified.flatMap((r) => [r.company, r.person_name, r.successor_name].filter(Boolean)));
let leaks = 0;
for (const r of others) {
  for (const value of [r.id, r.company, r.person_name, r.successor_name]) {
    if (!value || (value !== r.id && verifiedText.has(value))) continue;
    const hits = appears(value);
    if (hits.length) {
      leaks++;
      fail(`unverified record ${r.id}: "${value}" appears in ${hits.slice(0, 3).join(", ")}`);
    }
  }
}
if (!leaks) ok(`none of the ${others.length} rejected or unreviewed records appears anywhere in out/`);

// 2. Seat pages match the verified set exactly.
const seatDir = join(OUT, "seat");
const pages = existsSync(seatDir) ? readdirSync(seatDir).filter((d) => existsSync(join(seatDir, d, "index.html"))) : [];
const want = new Set(verified.map((r) => r.id));
const extra = pages.filter((p) => !want.has(p));
const missing = [...want].filter((id) => !pages.includes(id));
if (extra.length) fail(`seat pages with no verified record: ${extra.join(", ")}`);
if (missing.length) fail(`verified records with no seat page: ${missing.join(", ")}`);
if (!extra.length && !missing.length) ok(`${pages.length} seat pages, one per verified record`);

// 3. External links.
// The site links to the permanent copy of a filing when one exists (byte-identical, see pipeline/stable_links.py).
const allowed = new Set(verified.map((r) => r.source_url_stable ?? r.source_url));
const verifiedCompanies = new Set(verified.map((r) => r.company));
for (const [company, info] of Object.entries(practices.companies)) {
  if (!verifiedCompanies.has(company)) continue;
  for (const ev of info.evidence ?? []) if (manifest[ev.source_key]) allowed.add(manifest[ev.source_key].url);
}
const checkedOk = new Set((linkCheck?.results ?? []).filter((r) => r.ok === true).map((r) => r.url));
const external = new Map();
for (const p of htmlFiles) {
  for (const m of contents.get(p).matchAll(/href="(https?:\/\/[^"]+)"/g)) {
    const href = m[1].replace(/&amp;/g, "&");
    if (!external.has(href)) external.set(href, rel(p));
  }
}
let badLinks = 0;
for (const [href, where] of external) {
  const [url, frag] = href.split("#");
  if (!allowed.has(url)) {
    badLinks++;
    fail(`link to a non-source URL ${href} (in ${where})`);
    continue;
  }
  if (frag && !/^page=\d+$/.test(frag)) {
    badLinks++;
    fail(`unexpected fragment in ${href}`);
  }
  if (!linkCheck) {
    badLinks++;
    fail("data/link_check.json missing: run python3 -I pipeline/check_links.py");
    break;
  }
  if (!checkedOk.has(url)) {
    badLinks++;
    fail(`source link not confirmed by the link check: ${url}`);
  }
}
const pdfs = new Set([...external.keys()].map((h) => h.split("#")[0]));
if (!badLinks) ok(`${external.size} distinct external links (${pdfs.size} PDFs), all source filings confirmed on ${linkCheck.checked_at.slice(0, 10)}`);

// 4. Numbers: recompute independently and compare with every data-metric in the HTML.
const DAY = 86_400_000;
const days = (from, to) => Math.round((Date.parse(`${to}T00:00:00Z`) - Date.parse(`${from}T00:00:00Z`)) / DAY);
const asOf = score.as_of;
const expected = {
  seats: verified.length,
  filings: new Set(verified.map((r) => r.source_url)).size,
  noPermanentSuccessor: verified.filter((r) => r.successor_status !== "NAMED_PERMANENT").length,
  topSeats: verified.filter((r) => r.role_level === "CEO_MD" || r.role_level === "CXO").length,
  next45: verified.filter((r) => r.effective_date && days(asOf, r.effective_date) >= 0 && days(asOf, r.effective_date) <= 45).length,
  "footer-seats": verified.length,
  "footer-filings": new Set(verified.map((r) => r.source_url)).size,
  "practice-n": verified.length,
  "role-n": verified.length,
  "share-n": verified.length,
};
const seen = {};
for (const p of htmlFiles) {
  for (const m of contents.get(p).matchAll(/data-metric="([^"]+)"[^>]*>(\d+)</g)) {
    const [, key, value] = m;
    seen[key] = (seen[key] ?? 0) + 1;
    if (!(key in expected)) fail(`unknown metric ${key} in ${rel(p)}`);
    else if (Number(value) !== expected[key]) fail(`metric ${key} shows ${value} in ${rel(p)} but recomputes to ${expected[key]}`);
  }
}
for (const key of Object.keys(expected)) if (!seen[key]) fail(`metric ${key} not found on any page`);
if (!failures.some((f) => f.startsWith("metric"))) {
  ok(`numbers match a fresh recomputation: ${Object.entries(expected).slice(0, 5).map(([k, v]) => `${k}=${v}`).join(", ")}; footer on ${seen["footer-seats"]} pages`);
}

// 5. Wording and privacy.
const DISCLAIMER = "Independent prototype built from public filings. Not affiliated with Positive Moves.";
const noDisclaimer = htmlFiles.filter((p) => !contents.get(p).includes(DISCLAIMER));
if (noDisclaimer.length) fail(`disclaimer missing on ${noDisclaimer.map(rel).join(", ")}`);
else ok(`disclaimer on all ${htmlFiles.length} pages`);

const visible = (html) => html.replace(/<script[\s\S]*?<\/script>/g, " ").replace(/<[^>]+>/g, " ").replace(/&[a-z#0-9]+;/gi, " ");
let badProb = 0;
for (const p of htmlFiles) {
  const text = visible(contents.get(p));
  for (const m of text.matchAll(/probabilit/gi)) {
    const before = text.slice(Math.max(0, m.index - 12), m.index).toLowerCase();
    if (!/not a\s*$/.test(before)) {
      badProb++;
      fail(`"probability" used without "not a" in ${rel(p)}: …${text.slice(m.index - 40, m.index + 20)}…`);
    }
  }
}
if (!badProb) ok(`"probability" appears only as "not a probability"`);

const EMAIL = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/;
const PHONE = /(?:\+91[\s-]?)?\b[6-9]\d{4}[\s-]?\d{5}\b|\b0\d{2,4}[\s-]\d{6,8}\b/;
let pii = 0;
for (const p of htmlFiles) {
  const text = visible(contents.get(p));
  const e = text.match(EMAIL);
  const ph = text.match(PHONE);
  if (e) { pii++; fail(`e-mail address on ${rel(p)}: ${e[0]}`); }
  if (ph) { pii++; fail(`phone-like number on ${rel(p)}: ${ph[0]}`); }
}
if (!pii) ok("no e-mail addresses or phone numbers in page text");

if (failures.length) {
  console.error(`\n${failures.length} problem(s):`);
  for (const f of failures) console.error(`  FAIL ${f}`);
  process.exit(1);
}
console.log("\nSite check passed.");
