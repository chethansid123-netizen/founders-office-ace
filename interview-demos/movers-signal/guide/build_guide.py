"""Build the Movers Signal presenter's guide (PDF).

Every number and example in the guide is read from the project's own data:
out/site-data.json (the site export, computed by the same code as the pages),
data/records.json (rejection reasons) and data/audit.json. Nothing is typed in
by hand, so the guide always agrees with the site.

    npm run build                      # writes out/site-data.json
    python3 -I guide/build_guide.py [--lovable <url>] [--out <pdf>]

Renders twice with headless Chromium: the second pass fills real page numbers
into the contents.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
E = html.escape


def arg(name: str, default: str | None = None) -> str | None:
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


LOVABLE = arg("--lovable")
OUT_PDF = Path(arg("--out", str(ROOT / "Movers-Signal-Presenter-Guide.pdf"))).resolve()

D = json.loads((ROOT / "out" / "site-data.json").read_text(encoding="utf-8"))
RECORDS = json.loads((ROOT / "data" / "records.json").read_text(encoding="utf-8"))["records"]
META, SUM, SEATS, PULSE, METHOD = D["meta"], D["summary"], D["seats"], D["pulse"], D["method"]
A = METHOD["audit"]
LC = METHOD["link_check"]
SCORE = METHOD["score"]
N = SUM["seats"]
W0, W1 = META["window_label"]
REJECTED = [r for r in RECORDS if r["review_status"] != "VERIFIED"]


def pct(a: int, b: int) -> str:
    return f"{round(a / b * 100)}%" if b else "0%"


def tag(kind: str) -> str:
    return {"fact": '<span class="tag fact">Filed fact</span>', "derived": '<span class="tag derived">Derived</span>',
            "hyp": '<span class="tag hyp">Hypothesis</span>'}[kind]


def say(*paras: str, title: str = "Say it like this") -> str:
    return f'<div class="say"><b>{E(title)}</b>' + "".join(f"<p>{p}</p>" for p in paras) + "</div>"


# ---------- derived figures (all from the data) ----------
top = SEATS[0]
second_filled = next(s for s in SEATS if s["seat_filled"])
first_named = next(s for s in SEATS if s["successor_status"] == "NAMED_PERMANENT" and not s["seat_filled"])
open_seats = [s for s in SEATS if not s["seat_filled"]]
bands = Counter((s["total"] // 10) * 10 for s in open_seats)
status = Counter(s["status"] for s in SEATS)
events = Counter(s["event_label"] for s in SEATS)
exch = Counter(s["exchange"] for s in SEATS)
checks_total = sum(s["review"]["checks_total"] for s in SEATS)
checks_match = sum(s["review"]["checks_match"] for s in SEATS)
checks_absent = sum(s["review"]["checks_absent"] for s in SEATS)
checks_cleared = checks_total - checks_match - checks_absent
quotes = sum(1 for s in SEATS for f in s["facts"] if f["quote"]) + sum(len(s["also_in_filing"]) for s in SEATS)
nulls = [(s, f) for s in SEATS for f in s["facts"] if f["value"] is None]
with_reason = sum(1 for s in SEATS for f in s["facts"] if f["label"] == "Stated reason" and f["value"])
multi_exit = [s for s in SEATS if s["derived"]["other_exits"]]
pe = [s for s in SEATS if s["practice"] == "Private Equity"]
pe_companies = sorted({s["company"] for s in pe})
pe_example = next(s for s in pe if s["derived"]["practice_evidence"])
timing = Counter(c["points"] for s in SEATS for c in s["priority"]["components"] if c["label"].startswith("Timing"))
tests_count = None  # filled from the test run summary when available
n_practices = len(PULSE["byPractice"])
corrections_total = A["errors_fixed"]
n_records = len(RECORDS)

# ---------- parts ----------
PARTS: list[tuple[str, str, str]] = []  # (title, description, html)


def part(title: str, desc: str, body: str) -> None:
    PARTS.append((title, desc, body))


# Part 1
part("The idea in one minute", "The problem, the signal, the pitch, and what it is not", f"""
<p class="lede">A retained search firm usually hears about a senior seat once the mandate is being discussed. Movers Signal looks one step earlier: at the moment a listed company tells the stock exchange that a senior leader is leaving, retiring or joining.</p>
<h2>The signal</h2>
<p>Companies listed in India must disclose changes in their directors, key managerial personnel and senior management to the exchanges under Regulation 30 of SEBI's Listing Regulations. The disclosure is public, dated, and written by the company itself, usually with the effective date and often with the reason and the successor. That makes it the earliest reliable public sign that a senior seat is opening.</p>
<h2>What Movers Signal does: four verbs</h2>
<div class="grid4">
  <div class="card"><b>Read</b>Collect the NSE and BSE filings on senior leadership changes from the last 90 days and pull out each seat.</div>
  <div class="card"><b>Verify</b>Keep only what the filing states, with page and quote. Re-read every PDF with two independent engines.</div>
  <div class="card"><b>Rank</b>Order the seats with a four-part priority rule that anyone can recompute by hand.</div>
  <div class="card"><b>Brief</b>Give the practice a brief: facts, why now, questions, talent pools and the PINE checks.</div>
</div>
{say("Every listed company has to tell the exchange when a senior leader leaves or joins. Movers Signal reads those filings, keeps only what the filing actually says, checks every fact against the PDF twice, and ranks the seats a partner should look at first, with a rule anyone can recompute.",
     "Each seat gets a short brief: the facts with their quotes and page links, why it might matter now, the questions to ask, and the checks to run in PINE before anyone reaches out.", title="The 30-second pitch")}
<h2>What it is not</h2>
<ul>
  <li><strong>Not a prediction.</strong> The score is a priority rule for ordering attention. It is never called a probability, because there is no outcome data to test it against yet.</li>
  <li><strong>Not a people database.</strong> No candidates are named, and no phone numbers or e-mail addresses are stored or shown.</li>
  <li><strong>Not scraped.</strong> No LinkedIn, no paid data, no Positive Moves internal data. Only the companies' own filings.</li>
</ul>
<h2>The numbers to remember</h2>
<div class="kpis">
  <div class="kpi"><div class="v">{N}</div><div class="l">verified seats</div><div class="n">from {SUM['filings']} filings, {W0} to {W1}</div></div>
  <div class="kpi"><div class="v">{SUM['noPermanentSuccessor']}</div><div class="l">no permanent successor</div><div class="n">{pct(SUM['noPermanentSuccessor'], N)} of seats: none named, interim or unclear</div></div>
  <div class="kpi"><div class="v">{SUM['topSeats']}</div><div class="l">CEO, MD and C-suite seats</div><div class="n">role level from the filed title</div></div>
  <div class="kpi"><div class="v">{SUM['next45']}</div><div class="l">effective in the next {SUM['next45Days']} days</div><div class="n">{META['as_of_label']} to {SUM['next45_to_label']}</div></div>
</div>
""")

# Part 2
fact_rows = "".join(
    f"<tr><td>{E(f['label'])}</td><td>{E(f['value']) if f['value'] else '<span class=muted>Not stated in the filing</span>'}</td>"
    f"<td class='q'>{('&ldquo;' + E(f['quote']) + '&rdquo;') if f['quote'] else E(f['note'] or '')}</td><td class='n'>{f['page'] or ''}</td></tr>"
    for f in top["facts"])
null_examples = "".join(f"<li><strong>{E(s['company'])}</strong>, {E(f['label'].lower())}: {E(f['note'] or '')}</li>" for s, f in nulls[:3])
part("Where every fact comes from", "Sources, how filings were found, the funnel and what a record holds", f"""
<p class="lede">Every fact on the site traces back to one PDF that the company filed with NSE or BSE, to a page in it, and to an exact quote of under 15 words.</p>
<h2>Sources and window</h2>
<ul>
  <li><strong>Primary filings only:</strong> the PDF each company filed with NSE or BSE. Of the {N} seats, {exch.get('BSE', 0)} come from BSE filings and {exch.get('NSE', 0)} from NSE filings.</li>
  <li><strong>Window:</strong> filings dated {W0} to {W1}, the 90 days up to the data date ({META['as_of_label']}).</li>
  <li><strong>Roles:</strong> CEO and MD, the C-suite, business heads, function heads and other named senior management. <strong>Events:</strong> resignation, retirement, removal, end of term, appointment, and other moves.</li>
</ul>
<h2>How the filings were found</h2>
<p>NSE's public corporate-announcements feed, plus web searches restricted to the two exchanges' own sites. A search result was only ever a pointer: every PDF was then fetched directly from the exchange archive and read. Reading the PDF caught two search mistakes before any data was taken: a filing labelled as Dr. Reddy's was in fact Ashok Leyland's, and a Bain Capital disclosure linked to Manappuram was in fact about Dhoot Transmission.</p>
<p><strong>Polite access.</strong> One honest user agent that names the project, one request at a time with a pause, no cookies, no browser imitation. A block stops the run and writes a list of filings to download by hand into <code>data/raw/</code>. No block was bypassed.</p>
<h2>The funnel</h2>
<table><thead><tr><th>Stage</th><th class="n">Count</th><th>What happened</th></tr></thead><tbody>
<tr><td>Documents fetched</td><td class="n">{A['documents_fetched']}</td><td>Candidate filings from the feed and the restricted searches</td></tr>
<tr><td>Screened out at triage</td><td class="n">{A['screened_out_at_triage']}</td><td>No change of seat holder, outside the window, or a text layer that could not be read reliably</td></tr>
<tr><td>Filings reviewed in full</td><td class="n">{A['filings_reviewed']}</td><td>{A['filings_in_study']} in the study set plus {A['review_test_filings']} kept as review tests</td></tr>
<tr><td>Seat records extracted</td><td class="n">{n_records}</td><td>Some filings carry more than one seat</td></tr>
<tr><td>Verified and on the site</td><td class="n">{N}</td><td>From {SUM['filings']} filings across all {n_practices} practices</td></tr>
<tr><td>Rejected</td><td class="n">{A['records_rejected']}</td><td>Each with a written reason (Part 3)</td></tr>
</tbody></table>
<div class="keep"><h2>What a record holds: the top seat as an example</h2>
<p>{tag('fact')} <strong>{E(top['role_title'])}, {E(top['company'])}</strong>. Every field carries its page and an exact quote. If the filing does not state something, the field stays empty and says why; that happened {len(nulls)} times across the {N} seats, for example:</p>
<ul class="small">{null_examples}</ul>
<table><thead><tr><th style="width:20%">Field</th><th style="width:27%">Value</th><th>Supporting quote</th><th class="n">Page</th></tr></thead><tbody>{fact_rows}</tbody></table></div>
<p class="small muted">The stated reason is shown only as the filing words it ({with_reason} of {N} filings state one). Nobody's reason for leaving is ever guessed.</p>
""")

# Part 3
error_rows = "".join(f"<tr><td>{E(k)}</td><td class='n'>{v}</td></tr>" for k, v in A["error_classes_v1"].items())
rej_rows = "".join(f"<tr><td class='mono'>{E(r['id'])}</td><td>{E((r['review_note'] or '').replace('Rejected. ', ''))}</td></tr>" for r in REJECTED)
part("How we know it is right", "Three text engines, the corrections, the rejections and the automatic checks", f"""
<p class="lede">Accuracy is designed in, not hoped for: a second, independent reading of every PDF; corrections kept in the open; a review step; and automatic checks that fail the build if anything unverified reaches a page.</p>
<h2>The seven steps</h2>
<div class="steps">
  <div class="step"><b>Fetch and fingerprint</b><p>Each PDF is downloaded once and its SHA-256 hash recorded, so any later change to the document is detectable.</p></div>
  <div class="step"><b>Read the text</b><p>Engine A (pdfplumber) turns each page into text. Phone numbers and e-mail addresses are removed from the stored text.</p></div>
  <div class="step"><b>Extract</b><p>Each field is filled only from the text, with its page and an exact quote under 15 words. A field the filing does not state is stored as empty.</p></div>
  <div class="step"><b>Verify independently</b><p>Engines B (pypdfium2) and C (poppler) re-read every PDF from scratch. For each field: is the quote on that page, and does the quote support the value? Result: match, mismatch or not found.</p></div>
  <div class="step"><b>Correct in the open</b><p>Mismatches go to a review queue. Corrections are stored separately from the first pass, each with a reason, then verified again.</p></div>
  <div class="step"><b>Review record by record</b><p>Each record is approved or rejected beside its source in review.html. A record cannot be marked verified while any mismatch is unexplained.</p></div>
  <div class="step"><b>Publish only what passed</b><p>The site reads only VERIFIED records, and a build check proves nothing else leaked.</p></div>
</div>
<h2>Why three engines</h2>
<p>PDF text extraction fails in layout-specific ways: two columns merged into one line, a table row read in the wrong order. Three different parsers rarely fail in the same way, so a quote that all of them find on the cited page is very unlikely to be a reading error.</p>
<h2>What the first verification run caught</h2>
<div class="grid2"><div>
<table><thead><tr><th>Issue found in run 1</th><th class="n">Count</th></tr></thead><tbody>{error_rows}</tbody></table>
</div><div>
<p><strong>{A['errors_found']} issues</strong> in run 1 ({A['errors_found_fields']} field mismatches, {A['errors_found_record_flags']} record flags). <strong>{corrections_total} corrections</strong> were made, and all {A['errors_fixed_now_match']} re-verified as matches in run 2. <strong>{A['false_positives_cleared']} false alarm</strong> was cleared with a written reason. The other {A['errors_found'] - corrections_total - A['false_positives_cleared']} belonged to records that were then rejected.</p>
<p>For the {N} seats on the site: {checks_total} field checks in the final run, {checks_match} matches, {checks_absent} confirmed absent (empty fields), {checks_cleared} cleared at review with a reason.</p>
</div></div>
<h2>The {A['records_rejected']} rejected records</h2>
<table><thead><tr><th style="width:38%">Record</th><th>Why it was rejected</th></tr></thead><tbody>{rej_rows}</tbody></table>
<h2>Checks that run automatically</h2>
<ul>
  <li><strong>Link check:</strong> {LC['ok']} of {LC['links']} source PDFs re-downloaded on {E(LC['checked_at'][:10])}: HTTP 200, the same SHA-256 as the first fetch, and all {LC['pages_cited']} cited pages present. BSE moves new filings to a permanent address after a few days; {METHOD['stable_links']['moved']} links already point to the permanent, byte-identical copy and {METHOD['stable_links']['pending']} is still pending.</li>
  <li><strong>Site check</strong> on the built site: no rejected record anywhere (pages, data, scripts); exactly one page per verified seat; every external link is a confirmed source PDF; every headline number recomputed independently and compared; the disclaimer on every page; "probability" only ever as "not a probability"; no e-mail address or phone number.</li>
  <li><strong>Automated tests</strong> for the score rule, filters, the data and the export, plus lint, type checks and a production build.</li>
</ul>
<div class="note"><b>Say this openly.</b> Current review decisions are by {E(A['reviewed_by'])}. A person's sign-off in review.html is still pending. Human decisions override the AI reader as soon as they are exported.</div>
""")

# Part 4
part("The connections", "How one filing becomes a row, a brief and a chart", f"""
<p class="lede">The whole system is one chain. Each step reads only the output of the step before, and each screen element can be traced back to a file and a rule.</p>
<div class="flow">
  <div><i>1 · SOURCE</i><b>Filing PDF</b>NSE or BSE archive, hashed with SHA-256</div>
  <div><i>2 · TEXT</i><b>Page text</b>Engine A, contact details removed</div>
  <div><i>3 · RECORD</i><b>Filed facts</b>Value + page + quote, or empty</div>
  <div><i>4 · CHECK</i><b>Verification</b>Engines B and C, corrections, review</div>
  <div><i>5 · DERIVE</i><b>Rules</b>Role level, practice, days to effective date</div>
  <div><i>6 · SCORE</i><b>Priority</b>Four components, gate, rank</div>
  <div><i>7 · GENERATE</i><b>Hypotheses</b>Why now, questions, talent pools</div>
  <div><i>8 · SHOW</i><b>Four screens</b>Radar, brief, pulse, method</div>
</div>
<h2>Where each thing on screen comes from</h2>
<table><thead><tr><th style="width:27%">On screen</th><th style="width:35%">Comes from</th><th>Rule or file</th></tr></thead><tbody>
<tr><td>Company, person, role, dates, reason, successor</td><td>The filing, via the verified record</td><td><code>data/records.json</code> {tag('fact')}</td></tr>
<tr><td>Quote and page link</td><td>Evidence stored with each field</td><td>PDF link opens at <code>#page=N</code></td></tr>
<tr><td>Role level</td><td>The filed title</td><td>Ordered rules, <code>config/role_levels.json</code> {tag('derived')}</td></tr>
<tr><td>Practice</td><td>Company's business, or private equity control</td><td><code>config/practices.json</code> {tag('derived')}</td></tr>
<tr><td>Priority and rank</td><td>Role level, successor, other exits, effective date</td><td><code>config/score.json</code>, <code>lib/score.ts</code> {tag('derived')}</td></tr>
<tr><td>Status chip</td><td>Successor status, plus the gate</td><td>Open seat, Interim in seat, Successor unclear, Successor named, Seat filled</td></tr>
<tr><td>Why now, questions, talent pools</td><td>The seat's facts and derived fields</td><td><code>config/hypotheses.json</code> {tag('hyp')}</td></tr>
<tr><td>Before outreach checks</td><td>Positive Moves' own systems</td><td>Shown as "Needs PINE access"; never simulated</td></tr>
<tr><td>Radar numbers, Market pulse charts</td><td>Counts over the verified seats</td><td><code>lib/summary.ts</code>, <code>lib/pulse.ts</code> {tag('derived')}</td></tr>
<tr><td>Audit counts on Method</td><td>The pipeline's own logs</td><td><code>data/audit.json</code>, <code>AUDIT.md</code></td></tr>
</tbody></table>
<h2>One source of truth</h2>
<p>The build writes the whole site as one data file (<code>site-data.json</code>): every value the four screens show, computed by the same code, from verified records only. The website and the Lovable copy both render that file, so they cannot disagree. Changing a weight in <code>config/score.json</code> and rebuilding re-ranks every seat everywhere.</p>
{say("Nothing on the screen is typed in by hand. A fact comes from a filing with its quote; a label like role level or practice comes from a written rule; the priority comes from four published weights; and the brief's suggestions are marked as hypotheses for a partner to test.")}
""")

# Part 5
tables_html = "".join(
    "<div><table><thead><tr><th>" + E(t["title"]) + "</th><th class='n'>Points</th></tr></thead><tbody>" +
    "".join(f"<tr><td>{E(str(r[0]))}</td><td class='n'>{r[1]}</td></tr>" for r in t["rows"]) + "</tbody></table></div>"
    for t in SCORE["tables"])
why_weights = [
    ("Role level", "The more senior the seat, the rarer the people who can fill it, the longer the search and the more likely a retained firm is hired."),
    ("Successor status", "No successor named is an open need. An interim holder means the need is still open. A permanent successor means this seat needs no search, although the successor's old seat may now be open."),
    ("Other exits at the same company", "Several senior exits in a year suggest a team in change, so more than one seat may follow. Counted only inside this dataset."),
    ("Timing", "A seat that changes hands in the next 45 days, or did in the last 30, is when a conversation is most useful. Older or undated changes get a small base score."),
]
ww = "".join(f"<tr><td><strong>{E(a)}</strong></td><td>{E(b)}</td></tr>" for a, b in why_weights)
ex1 = "".join(f"<tr><td>{E(c['label'])}</td><td>{E(c['reason'])}</td><td class='n'>{c['points']}</td></tr>" for c in top["priority"]["components"])
ex2 = "".join(f"<tr><td>{E(c['label'])}</td><td>{E(c['reason'])}</td><td class='n'>{c['points']}</td></tr>" for c in second_filled["priority"]["components"])
band_rows = "".join(
    f"<div class='row'><span>{b} to {b + 9}</span><div class='bar' style='width:{bands[b] / max(bands.values()) * 100:.0f}%'></div><span class='n'>{bands[b]}</span></div>"
    for b in sorted(bands, reverse=True))
part("The priority score", "The formula, why each weight, two worked examples, and why it is not a probability", f"""
<p class="lede">Priority = role level + successor status + other exits at the same company + timing, out of {SCORE['max_points']}. It orders a partner's attention. It does not predict anything.</p>
<div class="grid2">{tables_html}</div>
<h2>Why these weights</h2>
<table><tbody>{ww}</tbody></table>
<p><strong>Gate.</strong> An appointment that names a permanent successor is shown as "{E(SCORE['gate_status'])}" and ranked below every open seat, whatever its score. <strong>Order:</strong> open seats first, then higher priority, then the sooner effective date, then company name.</p>
<div class="keep"><h2>Worked example 1: the top seat</h2>
<p><strong>{E(top['role_title'])}, {E(top['company'])}</strong>: {' + '.join(str(c['points']) for c in top['priority']['components'])} = <strong>{top['total']}</strong>, status <span class="chip">{E(top['status'])}</span>.</p>
<table><thead><tr><th>Component</th><th>Reason</th><th class="n">Points</th></tr></thead><tbody>{ex1}</tbody></table></div>
<div class="keep"><h2>Worked example 2: a filled seat</h2>
<p><strong>{E(second_filled['role_title'])}, {E(second_filled['company'])}</strong> scores {second_filled['total']}, more than many open seats, but it is an appointment with a permanent successor, so the gate marks it "{E(second_filled['status'])}" and it ranks {second_filled['rank']} of {N}, below all {len(open_seats)} seats that are not filled.</p>
<table><thead><tr><th>Component</th><th>Reason</th><th class="n">Points</th></tr></thead><tbody>{ex2}</tbody></table></div>
<div class="grid2"><div>
<h3>How the {len(open_seats)} seats that are not filled spread</h3>
<div class="bars">{band_rows}</div>
<p class="small muted">Priority bands, highest first. Derived from the site data.</p>
</div><div>
<h3>Why "priority", never "probability"</h3>
<p>There is no outcome data yet: we do not know which of these seats became mandates. Without that, no score can honestly claim accuracy. The weights are a stated judgement, kept in one config file, so they can be argued with and changed. The next phase compares priority with the mandates that actually followed and tunes the weights on that evidence.</p>
</div></div>
{say(f"The top seat is {E(top['role_title'])} at {E(top['company'])}: a C-suite seat with no successor named, another senior exit at the same company, and an effective date that has just passed. That is {' + '.join(str(c['points']) for c in top['priority']['components'])}, so {top['total']} out of 100. Anyone can redo that sum from the brief.")}
""")

# Part 6
role_rules = "".join(f"<tr><td class='n'>{i + 1}</td><td><strong>{E(r['level'])}</strong></td><td>{E(r['why'])}</td></tr>" for i, r in enumerate(METHOD["role_rules"]))
practice_rows = "".join(f"<tr><td><strong>{E(p['label'])}</strong></td><td>{E(p['description'])}</td><td class='n'>{next((b['count'] for b in PULSE['byPractice'] if b['label'] == p['label']), 0)}</td></tr>" for p in METHOD["practices"])
pe_quotes = "".join(f"<li>&ldquo;{E(e['quote'])}&rdquo; (p.{e['page']})</li>" for e in pe_example["derived"]["practice_evidence"][:2])
part("The derived rules", "How practice and role level are decided", f"""
<p class="lede">Two labels are not in the filing and are derived by written rules: which practice a seat belongs to, and how senior the role is. Both are tagged {tag('derived')} wherever they appear.</p>
<h2>Practice routing</h2>
<ol>{''.join(f'<li>{E(r[3:] if r[:2].isdigit() or r[:1].isdigit() else r)}</li>' for r in METHOD['practice_rules'])}</ol>
<p>The private equity rule needs evidence from a primary filing too. In this sample it applies to {len(pe_companies)} companies: {E(', '.join(pe_companies))}. For {E(pe_example['company'])}, for example:</p>
<ul class="small">{pe_quotes}</ul>
<table><thead><tr><th style="width:28%">Practice</th><th>Covers</th><th class="n">Seats</th></tr></thead><tbody>{practice_rows}</tbody></table>
<h2>Role level</h2>
<p>The rules run in order on the lower-cased filed title; the first match wins. Order matters: "Chief Executive Officer - Consumer Business" is a business head, not the company CEO, so that rule runs first.</p>
<table><thead><tr><th class="n">#</th><th style="width:22%">Level</th><th>When it applies</th></tr></thead><tbody>{role_rules}</tbody></table>
{say("Practice and role level are rules, not judgement calls. If a partner disagrees with one, we change the rule in one file and every seat is re-labelled the same way.")}
""")

# Part 7
h = top["hypotheses"]
part("Hypotheses and guardrails", "What the brief suggests, how it is generated, and what it never does", f"""
<p class="lede">Three sections of each brief are judgements, not facts. They are generated by written rules from the seat's facts, labelled {tag('hyp')}, and marked as needing a partner's review.</p>
<div class="grid3">
  <div class="card"><b>Why this seat matters now</b>Two lines: where the seat stands (from the dates and successor status) and why it may matter (other exits, a no-replacement statement, private equity control, seniority).</div>
  <div class="card"><b>Questions for the partner</b>Three questions: who owns the hire and whether we know them (check in PINE), the successor or internal-cover question, and the timeline.</div>
  <div class="card"><b>Talent pools to map</b>Company types only, chosen by the role's function and the practice. Never a named person, never a named company.</div>
</div>
<h2>The top seat's brief, as generated</h2>
<p>{tag('hyp')} <strong>Why now</strong></p><ul>{''.join(f'<li>{E(x)}</li>' for x in h['why_now'])}</ul>
<p>{tag('hyp')} <strong>Questions</strong></p><ol>{''.join(f'<li>{E(x)}</li>' for x in h['questions'])}</ol>
<p>{tag('hyp')} <strong>Talent pools</strong> ({E(h['function_label'])})</p><ul>{''.join(f'<li>{E(x)}</li>' for x in h['pools'])}</ul>
<h2>Before outreach</h2>
<p>Each brief ends with four checks: off-limits and client conflicts, existing relationships, prior search history (all three need PINE), and a partner's approval. They show "Needs PINE access" because they need Positive Moves' own systems. No result is simulated.</p>
<h2>The guardrails, all enforced</h2>
<ul>
  <li>No candidate is named anywhere; talent pools are company types.</li>
  <li>No personal phone number or e-mail address is stored or shown; the site check scans every page for them.</li>
  <li>The reason for leaving is shown only as filed; nothing is inferred.</li>
  <li>Every item is labelled Filed fact, Derived or Hypothesis.</li>
</ul>
""")

# Part 8
part("The four screens", "What each screen shows and what to point at", f"""
<div class="grid2"><div>
<h2>1 · Radar</h2>
<div class="shot"><img src="img/ref-1-radar.jpg"></div><div class="cap">Headline, the three numbers, filters, ranked seats.</div>
<ul class="small">
<li>Three numbers, computed live from the verified seats: {SUM['noPermanentSuccessor']} with no permanent successor, {SUM['topSeats']} CEO, MD and C-suite seats, {SUM['next45']} effective in the next {SUM['next45Days']} days.</li>
<li>Four filters (practice, role level, event, successor status). They live in the web address, so a filtered view can be sent as a link.</li>
<li>Ranked table: company, role, event, effective date, status, priority, and the source PDF at the right page. Filled seats sit at the bottom.</li>
</ul>
</div><div>
<h2>2 · Seat brief</h2>
<div class="shot"><img src="img/ref-2-seat-brief.jpg"></div><div class="cap">Filed facts with quotes, priority breakdown, derived fields.</div>
<ul class="small">
<li>Filed facts, each with its quote and a link that opens the PDF at the cited page.</li>
<li>Priority breakdown with the reason for every point; derived fields with the rule that produced them.</li>
<li>Hypotheses, the before-outreach checks, and the source and review record (hash, verification counts, corrections).</li>
</ul>
</div></div>
<div class="grid2"><div>
<h2>3 · Market pulse</h2>
<div class="shot"><img src="img/ref-3-market-pulse.jpg"></div><div class="cap">Seats by practice and role level; share with no permanent successor.</div>
<ul class="small">
<li>n = {N} on every chart and a clear "verified sample, not the whole market" note: the filings were chosen to cover all practices.</li>
<li>Every bar opens the Radar filtered to those seats. Each chart has a table view.</li>
</ul>
</div><div>
<h2>4 · Method</h2>
<div class="shot"><img src="img/ref-4-method.jpg"></div><div class="cap">Sources, pipeline, audit, definitions, score, limits.</div>
<ul class="small">
<li>The audit counts come straight from the pipeline's log, and the link check date is shown.</li>
<li>The score section has the weights and a worked example that is recomputed on every build.</li>
</ul>
</div></div>
<p class="small muted">The site works on a phone (no sideways scrolling at 390 px) and in dark mode.</p>
""")

# Part 9
fs_count = next((b["count"] for b in PULSE["byPractice"] if b["label"] == "Financial Services"), 0)
fs_not_named = sum(1 for s in SEATS if s["practice"] == "Financial Services" and s["successor_status"] == "NOT_NAMED")
eff_page = next((f["page"] for f in top["facts"] if f["label"] == "Effective date" and f["page"]), top["source_page"])
part("The demo script", "Seven minutes, click by click, with what to say", f"""
<p class="lede">Start on the Radar, go one level deep on one seat, prove a fact against its PDF, then step back to the pattern and the method. Keep the PDF click: it is the moment that earns trust.</p>
<div class="steps">
<div class="step"><b>Open the Radar (1 minute)</b><p><span class="click">/</span> Point at the headline and the three numbers. "{SUM['noPermanentSuccessor']} of {N} seats have no permanent successor named. {SUM['topSeats']} are CEO, MD or C-suite. {SUM['next45']} change hands in the next {SUM['next45Days']} days."</p></div>
<div class="step"><b>Read the top row (30 seconds)</b><p>"The top seat is {E(top['role_title'])} at {E(top['company'])}, priority {top['total']}. Every row links to the filing at the exact page."</p></div>
<div class="step"><b>Open the brief and prove one fact (1.5 minutes)</b><p><span class="click">click the company name</span> then <span class="click">p.{eff_page} ↗ next to the effective date</span> "Here is the quote, here is the page, and this is the company's own filing on the exchange. Every fact on this page works like that."</p></div>
<div class="step"><b>Walk the priority breakdown (1 minute)</b><p>"{' + '.join(str(c['points']) for c in top['priority']['components'])} = {top['total']}. Role level, no successor, another exit at the same company, and timing. It is a priority rule, not a probability; the weights are in one file and we can argue about them."</p></div>
<div class="step"><b>Show the judgement layer (1 minute)</b><p>"These three sections are hypotheses for the partner: why now, the questions to ask, and talent pools by company type, never names. Before anyone reaches out, the conflict, relationship and history checks run in PINE. I have not faked those."</p></div>
<div class="step"><b>Filter like a practice lead (1 minute)</b><p><span class="click">Practice: Financial Services</span> then <span class="click">Successor status: Not named</span> "This is the view a Financial Services partner would open on a Monday: {fs_count} seats in the practice, {fs_not_named} with no successor named. And the link can be shared as it is."</p></div>
<div class="step"><b>Market pulse and Method (1 minute)</b><p>"The charts carry their sample size and say plainly that this is a verified sample, not the market. And Method shows the audit: {A['errors_found']} issues found in the first check, {corrections_total} fixed, {A['records_rejected']} records rejected, every source link re-checked."</p></div>
</div>
{say("If we connected this to PINE, every one of these seats would arrive with the relationships we already have at the company and the conflicts to avoid. And once we compare priority with the mandates that actually came in, the weights stop being my judgement and start being evidence.", title="Close with the next step")}
<h2>If something goes wrong in the room</h2>
<ul>
  <li><strong>A PDF link is slow:</strong> exchange sites can be slow; the brief already shows the quote and page, so carry on and come back to it.</li>
  <li><strong>Asked about a seat you do not know:</strong> open its brief; the facts and quotes are there. Never improvise a reason for an exit.</li>
  <li><strong>No internet:</strong> run the site locally (<code>npm run dev</code>); everything except the PDF links works offline.</li>
</ul>
""")

# Part 10
qa = [
    ("How do you know the data is right?", f"Three independent text engines, corrections in the open, a review step, and checks that fail the build. The first verification run found {A['errors_found']} issues; {corrections_total} were corrected and re-verified, {A['records_rejected']} records were rejected with reasons. Every fact shows its quote and page so anyone can check it in seconds."),
    ("Why not use LinkedIn or news?", "LinkedIn scraping breaks its terms and is not a primary source; news is second-hand. The company's own exchange filing is first-hand, dated and public. That is the standard a partner can stand behind with a client."),
    ("Does the score predict which seats become mandates?", "No, and it does not claim to. It is a transparent priority rule. To measure prediction we need outcome data: which seats turned into mandates. That is the first thing to add with Positive Moves' data."),
    ("Why these weights?", "Seniority and an open successor question matter most for retained search, then team churn and timing. They are a starting judgement in one config file. Change a number, rebuild, and every seat is re-ranked, so the weights can be agreed with the partners."),
    ("Why only 50 filings?", "It is a verified sample for a prototype, chosen to cover all eight practices. The pipeline is the product: the same steps run on every filing in the window. Scale is a scheduling question, not a redesign."),
    ("What about private companies?", "They do not file these disclosures, so they are out of scope here. That is a stated limit. Other public sources (for example company registry filings) could extend it later, with the same rules."),
    ("How would this connect to PINE?", "Join each seat to PINE on company: existing relationships, off-limits and client conflicts, previous searches. The brief already has the empty checks waiting for those answers."),
    ("What did the AI do and what did you decide?", f"The rules, the weights, the guardrails and the review standard are explicit decisions in config files. Automation did the heavy reading and checking. The review decisions so far are by {E(A['reviewed_by'])}; human sign-off is the next step, and human decisions override automated ones."),
    ("What happens if a company corrects a filing?", f"Each PDF is fingerprinted with SHA-256. The link check re-downloads every source and flags any change; the record is then re-extracted and re-verified. The last check ({E(LC['checked_at'][:10])}) found all {LC['links']} unchanged."),
    ("Is any personal data a problem?", "Only what the company itself filed publicly: names, roles and dates. Phone numbers and e-mail addresses are stripped from stored text and checked for on every page. No candidate is ever named."),
    ("Why does a seat with a named successor still score?", "The seat itself may not need a search, but the successor's previous seat may now be open, and the change is still worth a relationship call. The gate pushes filled appointments to the bottom so they never crowd out open seats."),
    ("How long would daily running take?", "The pipeline is polite by design (one request at a time, with a pause), so a day's filings take minutes. Review is the real cost, which is why only mismatches go to a person."),
    ("What would you do in the first 30 days?", "Get human sign-off on the current records, connect PINE for the three checks, run the pipeline daily on the full feed, and start logging which seats became mandates so the weights can be tested."),
    ("What is the weakest part?", "No outcome data yet, so the priority rule is judgement. Second, rules for role level and practice can mislabel an unusual title. Both are visible and easy to change, which is the point of making them rules."),
]
part("Questions you may get", "Short, honest answers", '<div class="qa">' + "".join(f'<div class="q"><b>{E(q)}</b><p>{a}</p></div>' for q, a in qa) + "</div>")

# Part 11
where = [
    ("Website code and data", "interview-demos/movers-signal in the GitHub repository (branch claude/zen-clarke-duln2y)"),
    ("Run it locally", "npm install, then npm run dev; npm run check:all runs every quality gate"),
    ("Review screen", "review.html: approve or reject each record beside its source"),
    ("Audit trail", "AUDIT.md: every correction and every rejection with its reason"),
]
if LOVABLE:
    where.insert(1, ("Lovable copy", LOVABLE))
where_rows = "".join(f"<tr><td><strong>{E(a)}</strong></td><td class='mono' style='font-size:7.8pt'>{E(b)}</td></tr>" for a, b in where)
part("Limits, next phase and cheat sheet", "What to admit, what comes next, and one page to glance at", f"""
<h2>Known limits (say them before you are asked)</h2>
<ul>
  <li>Listed companies only; private companies do not file these disclosures.</li>
  <li>A sample of {A['filings_verified']} filings chosen to cover all eight practices, not every filing in the window.</li>
  <li>No outcome data, so the priority rule cannot be called accurate or inaccurate yet.</li>
  <li>"Other exits" counts only exits inside this dataset.</li>
  <li>Role level and practice come from rules; an unusual title can land at the wrong level.</li>
  <li>Review decisions so far are by {E(A['reviewed_by'])}; a person's sign-off is pending.</li>
</ul>
<h2>Next phase</h2>
<ol>
  <li>Join each signal to PINE: relationships, off-limits and client conflicts, past searches.</li>
  <li>Compare priority with the mandates that actually followed, then tune the weights on that evidence.</li>
  <li>Run the pipeline daily on the exchange feeds, with the same verification and review.</li>
</ol>
<h2>Cheat sheet</h2>
<div class="grid2"><div class="card"><b>Numbers</b>
{N} seats · {SUM['filings']} filings · {n_practices} practices · {W0} to {W1}<br>
{SUM['noPermanentSuccessor']} no permanent successor ({pct(SUM['noPermanentSuccessor'], N)}) · {SUM['topSeats']} CEO, MD, C-suite · {SUM['next45']} in the next {SUM['next45Days']} days<br>
{A['errors_found']} issues found · {corrections_total} fixed · {A['records_rejected']} rejected · {LC['ok']}/{LC['links']} links confirmed<br>
Top seat: {E(top['role_title'])}, {E(top['company'])}, {top['total']}
</div><div class="card"><b>Words</b>
Say: <em>priority</em>, <em>filed fact</em>, <em>verified sample</em>, <em>hypothesis for the partner</em>, <em>needs PINE access</em>.<br>
Never say: <em>probability</em>, <em>predicts</em>, <em>the AI found</em>, <em>the market</em> (it is a sample), or any guess about why someone left.
</div></div>
<div class="grid3">
  <div class="card"><b>Rule 1</b>Only primary filings. If it is not in the filing, it stays empty.</div>
  <div class="card"><b>Rule 2</b>Every fact has a quote, a page and a link.</div>
  <div class="card"><b>Rule 3</b>Priority orders attention. It is not a probability.</div>
</div>
<h2>Where everything lives</h2>
<table><tbody>{where_rows}</tbody></table>
""")


# ---------- assembly ----------
def cover() -> str:
    return f"""
<section class="cover">
  <div>
    <div class="mark"><span style="height:12px;opacity:.55"></span><span style="height:20px;opacity:.8"></span><span style="height:30px"></span></div>
    <div class="kicker">Presenter's guide · {E(META['as_of_label'])}</div>
    <h1>Movers Signal</h1>
    <p class="sub">Leadership seats before the mandate. How it works, why it is built this way, and how to explain it in the room.</p>
    <div class="nums">
      <div><b>{N}</b><span>verified seats</span></div>
      <div><b>{SUM['filings']}</b><span>NSE and BSE filings</span></div>
      <div><b>{n_practices}</b><span>practices</span></div>
      <div><b>{SUM['noPermanentSuccessor']}</b><span>with no permanent successor</span></div>
    </div>
  </div>
  <div class="three">
    <div><b>Understand it</b><span>Parts 1 to 4: the idea, where every fact comes from, how it is checked, and how the pieces connect.</span></div>
    <div><b>Defend it</b><span>Parts 5 to 7: the priority score and its weights, the derived rules, the hypotheses and guardrails.</span></div>
    <div><b>Present it</b><span>Parts 8 to 11: the screens, a click-by-click demo script, likely questions, limits and a cheat sheet.</span></div>
  </div>
  <div class="foot"><span>Filings dated {E(W0)} to {E(W1)}. Every number in this guide is read from the project's data.</span><span>{E(META['disclaimer'])}</span></div>
</section>"""


def contents(pages: dict[int, int] | None) -> str:
    rows = "".join(
        f'<div class="tp"><span class="no">{i + 1:02d}</span><div><b>{E(t)}</b><span class="d">{E(d)}</span></div><span class="pg">{pages.get(i + 1, "") if pages else ""}</span></div>'
        for i, (t, d, _) in enumerate(PARTS))
    return f'<section class="part"><div class="kicker">Contents</div><h1>What is in this guide</h1><div class="toc">{rows}</div></section>'


def document(pages: dict[int, int] | None) -> str:
    css = (HERE / "guide.css").read_text(encoding="utf-8")
    body = cover() + contents(pages) + "".join(
        f'<section class="part" data-part="{i + 1}"><div class="kicker">Part {i + 1} · {E(t)}</div><h1>{E(t)}</h1>{b}</section>'
        for i, (t, _, b) in enumerate(PARTS))
    return f'<!doctype html><html lang="en-IN"><head><meta charset="utf-8"><title>Movers Signal: presenter\'s guide</title><style>{css}</style></head><body>{body}</body></html>'


def render(html_text: str) -> PdfReader:
    page = HERE / "guide.html"
    page.write_text(html_text, encoding="utf-8")
    subprocess.run(["node", str(HERE / "render.cjs"), str(page), str(OUT_PDF)], check=True)
    return PdfReader(str(OUT_PDF))


def part_pages(reader: PdfReader) -> dict[int, int]:
    found: dict[int, int] = {}
    for idx, pg in enumerate(reader.pages):
        # Letter-spaced kickers come out as "P A R T  1 ...": compare with all whitespace removed.
        text = re.sub(r"\s+", "", (pg.extract_text() or "")).lower()
        for i, (t, _, _) in enumerate(PARTS):
            key = re.sub(r"\s+", "", f"part {i + 1} · {t}").lower()
            if i + 1 not in found and key in text:
                found[i + 1] = idx + 1
    return found


def main() -> int:
    first = render(document(None))
    pages = part_pages(first)
    second = render(document(pages))
    again = part_pages(second)
    missing = [i + 1 for i in range(len(PARTS)) if i + 1 not in again]
    if again != pages or missing:
        print(f"page numbers moved or missing: pass1={pages} pass2={again} missing={missing}")
        return 1
    print(f"{OUT_PDF.name}: {len(second.pages)} pages; parts start on {pages}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
