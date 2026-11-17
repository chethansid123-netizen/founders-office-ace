"""Build the Kishlay ₹512 Cr playbook (HTML, then PDF via doc_pdf.cjs) from the deck's slide files and notes.
Usage: python3 build_playbook.py <deck_root> <out.html>"""
import sys, os, re, json, html as H
root, out = sys.argv[1:3]
idx = json.load(open(os.path.join(root, 'project/deck.json')))
slides = []
for sid in idx['order']:
    s = open(os.path.join(root, 'project/slides', sid + '.html')).read()
    eb = re.search(r'<p class="eyebrow[^"]*"[^>]*>(.*?)</p>', s, re.S)
    ti = re.search(r'<h[12] class="(?:title|hero)[^"]*"[^>]*>(.*?)</h[12]>', s, re.S)
    no = re.search(r'<aside>(.*?)</aside>', s, re.S)
    strip = lambda x: re.sub(r'<[^>]+>', ' ', x or '').replace('  ', ' ').strip()
    slides.append((sid, strip(eb.group(1) if eb else ''), strip(ti.group(1) if ti else ''), (no.group(1).strip() if no else '')))

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'playbook.css')).read()

def slide_cards():
    outp = []
    for i, (sid, eb, ti, note) in enumerate(slides):
        m = re.match(r'([A-Z ’\':&;0-9,.+()/-]+?)\s*\(([^)]*)\)\.\s*(.*)', note, re.S)
        timing = m.group(2) if m else ''
        body = m.group(3) if m else note
        appendix = eb.startswith('Appendix')
        outp.append(f'<div class="slide"><h3>{H.escape(eb)}</h3><p class="meta">{H.escape(ti)}{" · " + H.escape(timing) if timing else ""}</p><div class="say"><p>{body}</p></div></div>')
    return '\n'.join(outp)

doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>₹512 Cr Plan Playbook</title><style>{CSS}</style></head><body><main>
<header>
<p class="eyebrow">Kishlay Group · Founder’s Office interview · 18 Nov 2026</p>
<h1>The ₹512 Cr Plan: playbook</h1>
<p class="lead">How the plan was built, whether ₹512 Cr is the right number, how to present every slide, and what to do on day one.</p>
<p class="muted">Files: <b>Kishlay-512-Plan.pptx / .pdf</b> (18 slides: 14 main + 4 appendix, about 16 minutes) · <b>Kishlay-512-Growth-Model.xlsx</b> (19 sheets, 753 formulas, 0 errors) · <b>Kishlay-512-OnePager.pdf</b> (leave-behind) · Deck 4 (Growth Story) as backup for competition. Prepared by Chethan N.</p>
<ol class="toc">
<li>The answer in 60 seconds</li>
<li>Is ₹512 Cr real? The backbone</li>
<li>What the Tracxn data changed</li>
<li>Modern trade: how to break in</li>
<li>The hook and engagement</li>
<li>Slide by slide: what to say</li>
<li>How it was built, and the prompt</li>
<li>Sources: secondary and primary</li>
<li>Assumptions, and why</li>
<li>Trade-offs, and why</li>
<li>What I would do better; what I did not do</li>
<li>Executing on the ground: days 1–30</li>
<li>Questions they may ask, with answers</li>
<li>Questions to ask them</li>
<li>Your section: JD and background</li>
<li>Numbers cheat sheet</li>
<li>Tonight: price-screenshot checklist</li>
</ol>
</header>

<h2><span class="n">1</span>The answer in 60 seconds</h2>
<div class="card red">
<p><b>The question:</b> how can Tulsi Speciality Foods break out of the low-margin ₹5/₹10 general-trade trap and scale to ₹512 Cr at ~10% EBITDA through a 90-day Founder’s Office roadmap across quick-commerce and modern-trade multipacks, asset-light 3P and M&amp;A, and exports to Nepal and the GCC?</p>
<p><b>The answer in one line:</b> not more packs, more money per kilo.</p>
<p><b>The insight:</b> one kilo earns about ₹34 of contribution in ₹10 kirana packs, ₹49 in a 400 g modern-trade pack, ₹54 on quick commerce and ₹99 on a UAE shelf, but only ₹19 as a Nepal export (30% duty, 13% VAT). Move kilos up that ladder, fill the plants, and measure every move.</p>
<p><b>The number:</b> FY25 revenue fell 16% to ₹288 Cr with a ₹6.31 Cr loss. From there, the base case reaches ~₹458 Cr and ~₹46 Cr EBITDA (10%) in FY29. ₹512 Cr arrives in FY31 on the base case, or in FY29 only on the bull case. Commit to ~₹460 Cr and ~₹46 Cr EBITDA; keep ₹512 Cr as the stretch; steer by EBITDA.</p>
<p><b>The 90 days:</b> five workstreams, three gates (weeks 4, 8, 13), ₹57.3 lakh budget of which ₹35 lakh is stock that sells. Day 90 ends in five decisions made on pilot data.</p>
</div>

<h2><span class="n">2</span>Is ₹512 Cr real? The backbone</h2>
<p>You asked whether ₹512 Cr is the actual target, whether it can change, and to what. Here is the full reasoning; the live version is the <b>Target_Check</b> sheet.</p>
<h3>Where the number comes from</h3>
<p>No public source states ₹512 Cr as a revenue target. The only public “512” is Tulsi’s headcount (512 employees, February 2026, per labour filings on Tracxn). Treat ₹512 Cr as a target someone set (the founders, an investor or the brief) and ask: <i>“Where does 512 come from, and which year do you have in mind?”</i></p>
<h3>The starting point moved</h3>
<p>The model first assumed FY25 ≈ ₹354 Cr. Tracxn (from the MCA filing) shows <b>₹288 Cr for FY25, down 16%</b>, with a <b>₹6.31 Cr net loss</b>. That is Kishlay Foods Pvt Ltd standalone; group figures are not public, but in FY19–FY23 the standalone series was within ~2% of CRISIL’s consolidated numbers, and Tulsi Pvt Ltd had no FY25 revenue.</p>
<div class="tbl-wrap"><table>
<tr><th>Growth a year needed to reach ₹512 Cr</th><th>FY27</th><th>FY28</th><th>FY29</th><th>FY30</th><th>FY31</th></tr>
<tr><td>From FY25A (₹288 Cr)</td><td>33.3%</td><td>21.1%</td><td><b>15.5%</b></td><td>12.2%</td><td>10.1%</td></tr>
<tr><td>From FY26E (₹311 Cr, base)</td><td>+65% in one year</td><td>28.3%</td><td><b>18.1%</b></td><td>13.3%</td><td>10.5%</td></tr>
<tr><td>From FY24A (₹344 Cr), reference</td><td>14.2%</td><td>10.5%</td><td>8.3%</td><td>6.9%</td><td>5.9%</td></tr>
</table></div>
<p class="muted">Reference rates: Kishlay grew 5.3% a year FY21–FY24, +2.4% in FY24, −16% in FY25. The savoury-snack category grows 8–12% a year. Management told CRISIL (Feb 2024) it expected ₹350–400 Cr in the medium term; ₹512 Cr is 28–46% above that.</p>
<h3>Five tests for FY29</h3>
<div class="tbl-wrap"><table>
<tr><th>Test</th><th>Finding</th><th>Verdict</th></tr>
<tr><td>1 · Growth needed</td><td>15.5% a year from FY25; 18% from FY26E: about 2× the category</td><td>Bull case only</td></tr>
<tr><td>2 · Track record, guidance</td><td>FY25 −16%; FY21–24 +5.3% a year; own guidance ₹350–400 Cr</td><td>Stretch</td></tr>
<tr><td>3 · Capacity</td><td>₹512 Cr = 1,940–2,840 t a month at ₹220–150/kg vs 2,600 t installed (own 2,000 + AFP 300 + GUD 300). FY25 used ~42–62%.</td><td>Needs mix or more 3P</td></tr>
<tr><td>4 · Market room</td><td>₹512 Cr is 0.8% of a ₹61,000–64,000 Cr savoury-snack market</td><td>Pass</td></tr>
<tr><td>5 · Profit</td><td>₹51 Cr EBITDA = 2.7× FY26E (~₹18.7 Cr); Annapurna earns 11.6% at ₹520 Cr</td><td>Precedent exists</td></tr>
<tr><td>By FY27?</td><td>+78% in two years from ₹288 Cr with no new plant</td><td><b>Fail</b></td></tr>
</table></div>
<h3>Scenarios (live in the model)</h3>
<div class="tbl-wrap"><table>
<tr><th>FY29</th><th>Bear</th><th>Base</th><th>Bull</th></tr>
<tr><td>FY26 growth after FY25</td><td>0%</td><td>8%</td><td>15%</td></tr>
<tr><td>Revenue</td><td>₹338 Cr</td><td><b>₹458 Cr</b></td><td>₹564 Cr</td></tr>
<tr><td>Organic (no bolt-on)</td><td>₹338 Cr</td><td>₹425 Cr</td><td>₹514 Cr</td></tr>
<tr><td>EBITDA margin · EBITDA</td><td>6.8% · ₹23 Cr</td><td><b>10.0% · ₹46 Cr</b></td><td>12.7% · ₹71 Cr</td></tr>
<tr><td>Year ₹512 Cr is reached (10% a year after FY29)</td><td>FY34</td><td><b>FY31</b></td><td>FY29</td></tr>
</table></div>
<h3>What closes the ₹54 Cr FY29 gap (any one of)</h3>
<ul>
<li>General trade growing ~10% a year instead of 4.5%: unrealistic straight after a −16% year.</li>
<li>An acquisition of ~₹79 Cr of revenue instead of ₹30 Cr: a ~₹95 Cr cheque at 1.2× sales, too big for a balance sheet with bank limits near 93%.</li>
<li>~4,000 more dark stores at the base rate of sale.</li>
<li>One more year: ~₹504 Cr in FY30 and past ₹512 Cr in FY31 at 10% growth.</li>
</ul>
<h3>Why steer by EBITDA</h3>
<p>Tracxn’s listed-peer medians are <b>9.15× EBITDA but 1.02× revenue</b>. Each ₹1 Cr of EBITDA is worth about ₹9 Cr of value; each ₹1 Cr of revenue about ₹1 Cr. On those medians, base-case EBITDA moves indicative value from ~₹171 Cr (FY26E) to ~₹419 Cr (FY29). Indicative only; the Britannia talks in 2024 were reported at ₹600–700 Cr enterprise value.</p>
<div class="card gold">
<p><b>Recommendation (say it this way):</b> “₹512 Cr is the right destination. After FY25’s fall it isn’t the FY29 base case. I’d commit to about ₹460 Cr and ₹46 Cr of EBITDA for FY29, keep ₹512 Cr as the stretch the bull case reaches, and steer the company by EBITDA. If you need ₹512 Cr by FY29, these are the levers and what each costs.”</p>
<p><b>What would change my mind:</b> FY26 provisional sales above ~₹330 Cr (the bull path); group consolidated revenue meaningfully above the standalone ₹288 Cr; a bolt-on available on an earn-out; quick-commerce rate of sale above 1.3 units in the Guwahati pilot.</p>
</div>

<h2><span class="n">3</span>What the Tracxn data changed</h2>
<div class="tbl-wrap"><table>
<tr><th>Fact (Tracxn, from MCA and labour filings)</th><th>What it changed</th></tr>
<tr><td>Kishlay Foods FY25 revenue ₹288 Cr, down 16%; net loss ₹6.31 Cr (−2.2%)</td><td>Model base moved from an assumed ₹354 Cr to the actual. FY29 base fell from ₹518 Cr to ₹458 Cr; ₹512 Cr moved from FY29 to FY31 in the base case. Cover, problem, proof, target and revenue slides updated.</td></tr>
<tr><td>Tulsi Speciality Foods Pvt Ltd is a 99% subsidiary of Kishlay Foods Pvt Ltd</td><td>The hiring company is the group’s manufacturing arm: capacity, utilisation and co-packing are its levers (appendix A4).</td></tr>
<tr><td>Tulsi: 512 employees (Feb 2026), +15% YoY; EPFO payments ₹12.9 lakh (May 2025) → ₹14.3 lakh (Feb 2026); EPFO code set up in 2017 as a partnership firm</td><td>Evidence for an FY26 recovery (base +8%). Confirms the Tulsi firm’s workforce moved into the company.</td></tr>
<tr><td>Secured charges: Kishlay Foods ₹45.9 Cr (27 May 2026) + Tulsi ₹24.5 Cr (14 Apr 2026) = ₹70.4 Cr, vs ₹50.03 Cr CRISIL-rated in 2024</td><td>Credit is tighter than the rating alone shows; bolt-on must be funded with equity, earn-out or a seller note.</td></tr>
<tr><td>Auditor moved to MSKA &amp; Associates (BDO network) on 4 Mar 2026, from Bineet Bagaria &amp; Associates (FY25)</td><td>A governance upgrade: fits board-grade MIS and lender reporting (slide 12).</td></tr>
<tr><td>Tulsi had 5 GST filing delays in FY2025-26</td><td>Added to the week-4 gate, the MIS and the roadmap: fix before platform onboarding and lender reviews.</td></tr>
<tr><td>Funding: $15.9M in 3 rounds; Series A $15M (Jul 2018), post-money $32.4M; ranked 12th of 521 competitors</td><td>Investor reporting is part of the job (Norwest Venture Partners on the board per the dossier).</td></tr>
<tr><td>Listed-peer medians: 9.15× EBITDA, 1.02× revenue</td><td>The value lens: why the north star is EBITDA (Target_Check).</td></tr>
<tr><td>Corporate tree shows Kishlay Foods under Kishlay Sweets &amp; Savories Pvt Ltd, which is struck off</td><td>Flagged as likely stale; verify on MCA before quoting.</td></tr>
</table></div>

<h2><span class="n">4</span>Modern trade: how to break in</h2>
<p>Modern trade (supermarkets and hypermarkets) is where 200–400 g take-home packs earn their keep: about <b>₹49 a kilo</b> of contribution against ₹34 in ₹10 packs. The model’s <b>MT_Plan</b> sheet holds everything below with live formulas.</p>
<h3>Where: the chains, in order</h3>
<div class="tbl-wrap"><table>
<tr><th>Order</th><th>Chain</th><th>Footprint (East, Northeast)</th><th>Why it matters</th><th>Entry route</th></tr>
<tr><td>1</td><td><b>Vishal Mega Mart</b></td><td>~72 stores in the Northeast, 44–60 in Assam; 800+ in India</td><td>FMCG ~28% of FY25 sales; ~35% of that FMCG is own label: offer to co-pack it</td><td>Regional buying team</td></tr>
<tr><td>1</td><td><b>Guwahati supermarkets</b>: JDDS, Prince, The Grocer, Nayantara; Nasco Retails</td><td>Independent and small multi-store supermarkets</td><td>Fast listing, low or no fees: the pilot doors</td><td>Direct or MT distributor</td></tr>
<tr><td>2</td><td>Spencer’s Retail</td><td>131 stores in 27+ cities; focus on East India and UP; opening in West Bengal</td><td>Kolkata take-home shopper; has said it charges no listing fee</td><td>Kolkata category team</td></tr>
<tr><td>3</td><td>More Retail</td><td>877 supermarkets and 40 hypermarkets, incl. West Bengal and Odisha</td><td>Neighbourhood format suits 200–400 g packs</td><td>Regional office, Kolkata</td></tr>
<tr><td>3</td><td>Reliance Smart Bazaar / Smart</td><td>Siliguri, Darjeeling, Kolkata; former Big Bazaar stores</td><td>Scale; central buying, tougher terms</td><td>Vendor onboarding</td></tr>
<tr><td>3</td><td>Arambagh’s Foodmart</td><td>Kolkata</td><td>Bengali taste: chanachur, jhalmuri</td><td>Direct</td></tr>
<tr><td>Later</td><td>DMart</td><td>415 stores (FY25); growth in north and west</td><td>Low prices, fast payment</td><td>Central buying</td></tr>
</table></div>
<p class="muted">Sources S54–S60 in the model. Store counts come from filings, trade press and directories; confirm each chain’s current Assam and Bengal store list with its buyer.</p>
<h3>How: ten steps, with owners</h3>
<div class="tbl-wrap"><table>
<tr><th>When</th><th>Step</th><th>Owner</th></tr>
<tr><td>Week 1</td><td><b>Vendor kit:</b> FSSAI licence, GST certificate, GS1 barcodes for the hero SKUs, Legal Metrology-compliant MRP labels, ≥6 months of shelf life at dispatch, case and pallet specs, a price-to-retailer sheet, a promotion calendar, samples, and a one-page “Northeast shelf” story.</td><td>MT lead + QA</td></tr>
<tr><td>Week 1–2</td><td><b>Hero range for MT (6 SKUs):</b> 400 g Paneer and Bikaneri bhujia, 200 g Aloo Bhujia, Jolokia chanachur, Jhalmuri, 40 Aana chanachur; plus a 12 × ₹10 party pack. Consider MT-only pack sizes so shelf prices don’t clash with general trade.</td><td>Founder’s Office + Marketing</td></tr>
<tr><td>Week 2</td><td><b>Distributor:</b> appoint one modern-trade distributor in Guwahati (3–5% margin, delivery and chain paperwork) instead of serving chains’ warehouses directly at first.</td><td>Head of Sales NE</td></tr>
<tr><td>Week 2–3</td><td><b>Vishal pitch:</b> (1) a 5-store, 8-week trial of the 6 SKUs; (2) a co-packing quote for two own-label snack lines from the Amingaon plant; (3) next-day replenishment from Guwahati.</td><td>Founder’s Office + Sales</td></tr>
<tr><td>Week 2–4</td><td><b>Independents:</b> list in 5 Guwahati supermarkets with weekend sampling; these are the fastest pilot doors.</td><td>MT lead</td></tr>
<tr><td>Week 4</td><td><b>Terms:</b> margin around 20% of MRP; listing fees of ₹2,500–5,000 per SKU where charged (trade them for promoter and sampling support); credit capped at 30–45 days; clear expiry-return rules; fill-rate commitments; eye-level or end-cap space in month one.</td><td>Founder’s Office + Finance</td></tr>
<tr><td>Weeks 5–12</td><td><b>Run the 10-door pilot:</b> weekly planogram and stock-out checks, two weekend promoters, sampling, twice-weekly replenishment, weekly sell-out by store and SKU.</td><td>MT lead</td></tr>
<tr><td>Week 12</td><td><b>Gate:</b> ≥₹33k sales a door a month · ≥17 packs per SKU per door a week · contribution after promotions at least the ₹10 GT pack’s 15% · fill rate ≥95% · returns ≤3%. Scale, modify or stop.</td><td>Founders</td></tr>
<tr><td>FY27</td><td><b>Assam:</b> all Vishal Assam stores plus Guwahati independents: about 60 doors at target sales.</td><td>Head of Sales NE</td></tr>
<tr><td>FY28–29</td><td><b>Kolkata and beyond:</b> Spencer’s, More, Arambagh’s, Reliance Smart in Siliguri and Kolkata: 150 doors by FY28, 400 by FY29.</td><td>MT lead + Kolkata distributor</td></tr>
</table></div>
<h3>One door, in numbers (MT_Plan)</h3>
<div class="tbl-wrap"><table>
<tr><th>Item</th><th>Value</th><th>How</th></tr>
<tr><td>Kishlay realisation per 400 g pack (MRP ₹110)</td><td>₹75.06</td><td>After 5% GST, 20% retailer and 7% distribution</td></tr>
<tr><td>Contribution per pack</td><td>₹19.46 (26%)</td><td>After raw material, packing, conversion, freight, schemes</td></tr>
<tr><td>Target sales per door a month</td><td>₹33,000</td><td>Model input; the pilot gate</td></tr>
<tr><td>Packs per door: a month · a day · per SKU a week</td><td>~440 · ~15 · ~17</td><td>Sales ÷ realisation</td></tr>
<tr><td>Contribution per door a month</td><td>~₹8,556</td><td>Packs × contribution</td></tr>
<tr><td>Pilot spend per door (listing, promoters, sampling)</td><td>₹44,000</td><td>₹4.4 lakh ÷ 10 doors</td></tr>
<tr><td>Payback at target sales</td><td>~5.1 months</td><td>Spend ÷ monthly contribution</td></tr>
<tr><td>Break-even sales to recover ₹20k listing in 6 months</td><td>~₹12,856 a month</td><td>Listing ÷ 6 ÷ contribution per pack × realisation</td></tr>
<tr><td>Receivables per door at 45 days · at 400 doors</td><td>₹49,500 · ~₹2.0 Cr</td><td>The cash catch</td></tr>
<tr><td>Rollout: doors at target · run-rate</td><td>10 · 60 · 150 · 400 doors → ₹0.4 · ₹2.4 · ₹5.9 · ₹15.8 Cr a year</td><td>Pilot · FY27 · FY28 · FY29 (plus ₹3 Cr online)</td></tr>
</table></div>
<h3>Why a chain says yes</h3>
<ul>
<li>A range it lacks: Northeast and Bengali flavours (Jolokia, Jhalmuri, 40 Aana) next to the national brands.</li>
<li>The same shelf prices as Haldiram’s and Bikaji (₹55 for 200 g, ₹110 for 400 g).</li>
<li>Next-day supply from Guwahati; national brands ship from far away.</li>
<li>For Vishal: a co-packing offer for its own label, which fills our lines too.</li>
</ul>
<h3>Risks and how to handle them</h3>
<ul>
<li><b>Fees and promotions eat the margin:</b> start with independents; trade listing fees for in-store support; stop if contribution after promotions falls below general trade.</li>
<li><b>Credit ties up cash:</b> ~₹2 Cr at 400 doors; cap credit at 30–45 days, prefer fast payers, let the distributor carry credit early.</li>
<li><b>Clash with general trade:</b> MT-only pack sizes and a separate MT distributor.</li>
<li><b>De-listing for poor supply:</b> safety stock at the distributor; track fill rate weekly.</li>
</ul>
<p><b>Ask the founders:</b> which chains stock Kishlay today and on what terms; who owns modern trade; whether all hero SKUs have GS1 barcodes; whether there are vendor codes with Vishal, Reliance or Spencer’s.</p>

<h2><span class="n">5</span>The hook and engagement</h2>
<div class="say"><p><b>Open (first 20 seconds, before the slides):</b> “One kilo of snacks. In ₹10 kirana packs it earns Kishlay about ₹34. In a 400-gram pack on Blinkit, about ₹54. On a Dubai shelf, about ₹99. The whole plan is about selling more of the second and third kilo.”</p>
<p><b>Then the turn:</b> “And there’s a harder fact: FY25 revenue fell 16% to ₹288 Cr. So I tested whether ₹512 Cr is even the right target before building a plan to it.”</p></div>
<p><b>Three engagement moments</b> (ask, then stop talking):</p>
<ol>
<li>Slide 2: “Was FY25’s drop a real fall in sales, or did some billing move to Tulsi?”</li>
<li>Slide 5: “Where does 512 come from, and which year do you have in mind?”</li>
<li>Slide 9: “Which chains already stock Kishlay today, and on what terms?”</li>
<li>Slide 14: “Which of these numbers do you already track every week?”</li>
</ol>
<p><b>Rules:</b> label every estimate as an estimate; never defend a number you can’t source; when they correct you, write it down and say how it changes the model.</p>

<h2><span class="n">6</span>Slide by slide: what to say</h2>
<p class="muted">The same text is in the speaker notes of the PowerPoint. Main slides run about 16 minutes; use the appendix only when asked.</p>
{slide_cards()}

<h2><span class="n">7</span>How it was built, and the prompt</h2>
<h3>The steps</h3>
<ol>
<li><b>Frame:</b> took your single problem statement and turned it into four questions: is ₹512 Cr right, where does the margin come from, which engines add the revenue, and what happens in 90 days.</li>
<li><b>Ask before building:</b> 20 questions on scope, horizon, naming, sensitivity and data. Your answers set the defaults (FY29 horizon, peer-benchmarked 10%, Bhutan → Nepal → GCC, Guwahati then Kolkata, losses and CRISIL on screen framed as a reporting fix, Britannia talks only in Q&amp;A).</li>
<li><b>Secondary research:</b> CRISIL rationales, Motilal Oswal and Dealroom revenue series, listed-peer results, quick-commerce reports, retail listings, customs and VAT data, buyer and partner companies, M&amp;A precedents (60 sources).</li>
<li><b>Your data:</b> the two research dossiers and four Tracxn files (Tulsi FY25 financials, the charges screenshot, the Kishlay Foods profile and the Tulsi legal-entity profile). Each was checked for internal consistency (balance sheet balances, cash flows tie) before use.</li>
<li><b>Model first, slides second:</b> built the Excel model (inputs with Bear/Base/Bull, revenue and EBITDA bridges, unit economics, pilots, tracker) so every slide number comes from a formula.</li>
<li><b>Test the target:</b> five tests, live scenarios, gap closers and a value lens (Target_Check).</li>
<li><b>Design:</b> 14 main slides in Claude Slides, white background, logo on every slide, sources in every footer, speaker notes on every slide; checked each render for overflow.</li>
<li><b>Update on new facts:</b> when the Tracxn profiles showed FY25 at ₹288 Cr, re-based the model and rewrote the verdict rather than keeping the old answer.</li>
</ol>
<h3>The prompt (your words)</h3>
<pre>Problem statement: "How can Tulsi Speciality Foods Pvt. Ltd. break out of the low-margin ₹5/₹10 General Trade trap (where raw materials consume 70%–75% of costs and FY23 PAT stood at -₹11.50 Cr on ₹335.59 Cr revenue) and scale to ₹512 Cr at ~10% EBITDA by executing a 90-day Founder’s Office roadmap across Quick-Commerce/Modern Trade multipacks, asset-light 3P/M&amp;A expansion, and GCC/Nepal exports?"

Build brief: built for the company, to show the founder tomorrow; end to end; don't miss a single data point; ask every question first; use every resource and connector; then explain how the prompt was put, the primary and secondary sources, every assumption and why, every trade-off and why, what could be done better and what was not done; design it in Claude, write a playbook PDF, and give a strong hook and engagement for presenting; everything data-packed; if executed on the ground tomorrow, it should work.

Follow-ups: use public BigBasket data and label quick-commerce prices "to audit"; do complete research on real importers in the GCC and Nepal, all in Excel; validate the Tracxn financials; validate whether ₹512 Cr is real and what it could change to; use the new Tracxn profiles everywhere they change the answer.</pre>
<h3>A reusable prompt for the next problem</h3>
<pre>You are my Founder's Office analyst. Problem: [one sentence with the target, the horizon and the levers].
1. Before building, ask me every question that would change the answer (horizon, scope, sensitivities, data I have).
2. Test the target first: required growth by year, track record, capacity, market share, profit, live bear/base/bull, what closes any gap.
3. Build an Excel model first (inputs with sources and labels, bridges, unit economics, pilots, tracker); every slide number must come from it.
4. Label every number: Company, External, Historical, Calculation or Hypothesis; cite a source ID.
5. Deck: 12–13 slides + appendix, one message per title, sources in every footer, speaker notes with timings and engagement questions.
6. Playbook: the prompt, sources, assumptions and why, trade-offs and why, what is missing, a day-1 to day-30 plan, Q&amp;A.
7. When new facts arrive, re-base and say what changed.</pre>
<p class="muted">Tools: Claude (research, model and deck), web search, Python/openpyxl with LibreOffice recalculation (753 formulas, 0 errors), Claude Slides for the deck, headless Chromium for render checks and PDF. Live scraping of quick-commerce apps was not used; prices are indexed listings to verify live.</p>

<h2><span class="n">8</span>Sources: secondary and primary</h2>
<h3>Secondary (60, all in the model’s Sources sheet with links)</h3>
<ul>
<li><b>Company and filings:</b> Tracxn profiles of Kishlay Foods and Tulsi Speciality Foods (FY25 revenue, loss, headcount, charges, auditors, GST delays); Tracxn FY25 statements of Tulsi Pvt Ltd; kishlayfoods.com (236 products, 18 categories); job posts.</li>
<li><b>Credit:</b> CRISIL rating rationales (2020–2026), including FY22–FY23 PAT, the 70–75% raw-material share, 93% bank-limit use, ₹350–400 Cr guidance, rated facilities.</li>
<li><b>Revenue history:</b> Motilal Oswal snacks report (FY15–FY24), Dealroom.</li>
<li><b>Peers:</b> Bikaji, Gopal, Prataap results; Annapurna Swadisht (aggregator; verify on NSE).</li>
<li><b>Market and channels:</b> Ken Research, Market Report Analytics, Technavio, Mordor (market size); CareEdge (quick commerce ₹64,000 Cr → ₹2 lakh Cr); platform fees; dark-store counts; Blinkit’s Guwahati launch; GST 2.0; BigBasket listings.</li>
<li><b>Exports:</b> Nepal duty and VAT; Haldiram’s–Anandam and Bikaji–Chaudhary Group; Bhat-Bhateni, United Distributors, Nepal Overseas, Vhandar, MV Dugar; MEA (Indians in the GCC); PRAN’s UAE business; Lulu, Al Adil, Nesto, Carrefour, noon, Asian Basket; CEPA; Hormuz disruption; rupee rate.</li>
<li><b>M&amp;A:</b> Prataap–Avadh, Advent–DFM, Bikaji–Ariba, Britannia–Kishlay talks; contract-manufacturing leads.</li>
<li><b>Your research:</b> the strategic decoding report and the comprehensive business analysis dossiers.</li>
</ul>
<h3>Primary</h3>
<p><b>None yet, and the deck says so.</b> No store visits, distributor calls, buyer calls or platform data. The plan is designed so the first 30 days are primary research with a decision attached: tonight’s price screenshots; week 1 data asks; weeks 2–3 trade and broker conversations; the pilots themselves.</p>

<h2><span class="n">9</span>Assumptions, and why</h2>
<div class="tbl-wrap"><table>
<tr><th>Assumption (base)</th><th>Why this value</th><th>How to test</th></tr>
<tr><td>FY26 growth +8% (bear 0%, bull 15%)</td><td>Tulsi headcount +15% YoY and EPFO payments +11% within FY26 point to recovery after −16%</td><td>FY26 monthly sales, week 1</td></tr>
<tr><td>Group FY25 ≈ standalone ₹288 Cr</td><td>Standalone was within ~2% of CRISIL consolidated in FY19–FY23; Tulsi Pvt Ltd had no FY25 revenue</td><td>Consolidated FY25, week 1</td></tr>
<tr><td>Starting EBITDA margin 6%</td><td>Not disclosed; CRISIL interest cover and expected ₹15–18 Cr cash accrual imply mid-single digits; Gopal 6.7%</td><td>FY25–26 P&amp;L, week 1</td></tr>
<tr><td>General trade +4.5% a year</td><td>Below the category (8–12%) and the FY21–24 history (5.3%) because tail SKUs are cut</td><td>Secondary sales by state, week 2</td></tr>
<tr><td>1,000 dark stores, 6 SKUs, 1 unit a day, ₹62 net</td><td>East and Northeast coverage across four platforms by FY29; a regional brand’s rate of sale</td><td>Guwahati pilot, weeks 5–12</td></tr>
<tr><td>400 MT stores × ₹33k a month + ₹3 Cr online</td><td>Selected chains in East and Northeast; sales per door from a 400 g-led range</td><td>10-store pilot</td></tr>
<tr><td>Nepal 8 trucks a month × ₹12.5 lakh; 30% duty</td><td>Eastern Nepal first; biscuit HS line at 30% (namkeen line unconfirmed)</td><td>Broker quote (week 3), first trucks (week 10)</td></tr>
<tr><td>GCC 6 containers a month × ₹25 lakh from FY28</td><td>Registration time and shipping risk; UAE price 31% below Haldiram’s</td><td>Registrations (week 8), route gate (week 13)</td></tr>
<tr><td>Co-pack +₹17 Cr by FY29</td><td>Spare lines (FY25 output ~42–62% of capacity); Frito-Lay and Britannia already clients</td><td>Capacity audit, week 3</td></tr>
<tr><td>One ₹30 Cr bolt-on at 1.2× sales, mid-FY28</td><td>Precedents; balance-sheet limits rule out a bigger deal</td><td>Screen and shortlist, weeks 4–12</td></tr>
<tr><td>+400 bps of margin levers by FY29</td><td>Mix +140, utilisation +100, SKU +70, procurement +60, trade spend +60, freight +40, less QC fees −50 and investment −30, bolt-on +10</td><td>Pilot P&amp;Ls and costing</td></tr>
<tr><td>Trade margins: retailer 16%, distribution 7% on ₹10 packs</td><td>Industry-typical ranges</td><td>Scheme sheets and claims, week 2</td></tr>
<tr><td>Realisation ₹150–220 a kilo</td><td>Mix of ₹5/₹10 packs and larger packs; used only for the capacity test</td><td>Plant costing, week 2</td></tr>
</table></div>

<h2><span class="n">10</span>Trade-offs, and why</h2>
<ul>
<li><b>Honest target over a flattering one.</b> I could have kept FY25 at an assumed ₹354 Cr and shown ₹518 Cr in FY29. With the filing at ₹288 Cr, the honest answer is ~₹460 Cr in FY29 and ₹512 Cr in FY31. Founders trust an analyst who moves the answer when the facts move.</li>
<li><b>FY29, not FY27.</b> FY27 needs +78% in two years; FY29 is a stretch with named levers.</li>
<li><b>Bottom-up engines over a top-down growth rate.</b> Harder to build, but every rupee has an owner and a test.</li>
<li><b>Contribution per kilo as the organising idea.</b> It ignores some fixed-cost effects, but it is the cleanest way to compare channels and to explain the plan in one line.</li>
<li><b>Nepal: export first, then license.</b> Exports lose money per kilo after 30% duty; a local licence earns little but needs no capital. Haldiram’s and Bikaji both went local.</li>
<li><b>GCC gated to FY28.</b> The best price per kilo, but registration time and Hormuz risk make it a later engine with a go/no-go.</li>
<li><b>Guwahati before Kolkata.</b> Home market, Blinkit live since 2025, easier sell-through; Kolkata after the gates pass.</li>
<li><b>One bolt-on, not a big deal.</b> Bank limits near 93% and ₹70 Cr of charges leave no room; a bigger deal would need equity.</li>
<li><b>Losses and CRISIL on screen.</b> Shown as facts with a fix (reporting first), not as criticism. The Britannia talks stay out of the deck and come up only if they raise them.</li>
<li><b>Estimates shown as estimates.</b> Costs and margins per pack are model estimates; the plan replaces them with internal data in week 1.</li>
</ul>

<h2><span class="n">11</span>What I would do better; what I did not do</h2>
<h3>Not done</h3>
<ul>
<li>No primary research: no retailer, distributor, platform or importer conversations.</li>
<li>No internal data: SKU margins, utilisation by line, scheme spend, FY26 sales.</li>
<li>No consolidated FY24–FY26 accounts; FY25 is standalone.</li>
<li>Quick-commerce prices not checked live (indexed listings only); Annapurna numbers not checked against the NSE filing.</li>
<li>No customs-broker quote for Nepal HS lines; no UAE registration quote.</li>
<li>No legal check of the corporate tree (Kishlay Sweets &amp; Savories) on MCA.</li>
</ul>
<h3>With one more week</h3>
<ul>
<li>20 retailer and 3 distributor interviews in Guwahati; a price and shelf walk in 10 stores.</li>
<li>Calls with two Nepal distributors and two UAE buyers to test price acceptance.</li>
<li>Rebuild unit economics from plant costing; build an SKU-level contribution cube.</li>
<li>Add working capital and cash flow to the model, so the plan shows its funding need.</li>
</ul>

<h2><span class="n">12</span>Executing on the ground: days 1–30</h2>
<div class="tbl-wrap"><table>
<tr><th>When</th><th>Action</th><th>Owner</th><th>Output</th></tr>
<tr><td>Day 1–2</td><td>Get the four data asks: SKU sales and margin, line-wise output, scheme ledger, CRISIL letters; FY25–26 consolidated</td><td>Founder’s Office + Finance</td><td>Fact base; model re-based</td></tr>
<tr><td>Week 1</td><td>Pick 6 hero SKUs from the velocity–margin cube; start the twice-weekly RAG review and decision log</td><td>Founder’s Office + Head of Sales NE</td><td>Hero list signed; tracker live</td></tr>
<tr><td>Week 1–2</td><td>MIS v1 (15 KPIs); Bhutan baseline</td><td>Finance; export analyst</td><td>MIS on day 5 of the month</td></tr>
<tr><td>Week 1–3</td><td>Capacity audit by line (own, AFP, GUD)</td><td>GM Supply Chain</td><td>Utilisation % by line</td></tr>
<tr><td>Week 1–4</td><td>CRISIL monthly filings resumed; FY25–26 data shared; GST backlog cleared</td><td>Finance + Founders</td><td>Week-4 gate</td></tr>
<tr><td>Week 2–4</td><td>Onboard Blinkit, Zepto, Instamart in Guwahati; cost the multipacks</td><td>Founder’s Office; Marketing + Finance</td><td>Live on 3 apps</td></tr>
<tr><td>Week 2–3</td><td>Nepal customs-broker quote on HS lines; UAE registration started for 8 SKUs</td><td>Export analyst + QA</td><td>Landed-cost sheet</td></tr>
<tr><td>Week 3–6</td><td>Meet Bhat-Bhateni, United Distributors, Nepal Overseas; samples to Lulu, Al Adil, Nesto</td><td>Founder’s Office + export analyst</td><td>Term sheets, price feedback</td></tr>
<tr><td>Week 4</td><td>Gate: live on 3 apps · MIS v1 · CRISIL and GST current</td><td>Founders</td><td>Go to pilots</td></tr>
</table></div>
<p>Weeks 5–13 follow slide 12: 8-week QC pilot and 10-store MT pilot; two trucks to Nepal; 20 brands screened to 5; board pack and first update; FY27–29 plan for approval. Budget ₹57.3 lakh (cost ₹22.3 lakh, stock ₹35 lakh).</p>

<h2><span class="n">13</span>Questions they may ask, with answers</h2>
<div class="qa"><b>“Why did revenue fall 16% in FY25?”</b>“I don’t know yet. Either sales fell, or some billing moved inside the group, for example to Tulsi. The filing only shows Kishlay Foods standalone. That’s my first question for finance, because it changes the base for everything.”</div>
<div class="qa"><b>“Where do your per-kilo numbers come from?”</b>“Public shelf prices, the GST rate, industry trade margins and my cost estimates. The formulas are open in the Unit_Econ sheet. The direction is robust; the exact rupees need your costing.”</div>
<div class="qa"><b>“We want ₹512 Cr by FY29. Can you do it?”</b>“It needs the bull case: every engine at full pace plus a bigger bolt-on, or general trade at 10% a year. I’d plan for ₹460 Cr and manage to the upside with gates, rather than budget ₹512 Cr and miss.”</div>
<div class="qa"><b>“Isn’t 10% EBITDA unrealistic for a company making losses?”</b>“Annapurna earns 11.6% at ₹520 Cr on the same ₹5 model; Gopal earns 6.7% at five times our size. The bridge needs +400 bps, and 60% of it is mix and fuller plants, which we measure from week one.”</div>
<div class="qa"><b>“Why would Vishal or Spencer’s list a regional brand?”</b>“Because we bring a range they lack — Northeast and Bengali flavours — at the same prices as Haldiram’s and Bikaji, with next-day supply from Guwahati. For Vishal, we can also co-pack its own label, which is about a third of its FMCG.”</div>
<div class="qa"><b>“Modern-trade margins are high. Won’t we lose money?”</b>“After a 20% retailer margin, a 400 g pack still leaves about ₹19.5, or 26% of what we receive, against 15% on a ₹10 pack. The risk is promotions and fees, so the pilot stops if contribution after promotions falls below general trade.”</div>
<div class="qa"><b>“Why quick commerce? The fees are high.”</b>“After the 22% fee and ads, a kilo still earns ~₹20 more than in ₹10 packs, because there is no retailer margin. The pilot has a stop rule: 15% contribution after fees and ads, or we stop.”</div>
<div class="qa"><b>“Why not build a plant in Nepal?”</b>“No capital to spare, and exports already lose margin to 30% duty. Prove demand with two trucks, then license a local maker for a royalty, as Haldiram’s and Bikaji did.”</div>
<div class="qa"><b>“The Gulf is risky right now.”</b>“Yes, so it’s gated: registration first, ₹9.4 lakh at risk, routes that avoid Hormuz, and a go/no-go in week 13. Nothing ships at scale before FY28.”</div>
<div class="qa"><b>“How would you pay for an acquisition?”</b>“Not from bank limits. Equity, an earn-out or a seller note, and only a brand with EBITDA of 10% or more. The funnel is 20 screened, 5 meetings, 1 term sheet.”</div>
<div class="qa"><b>“AFP makes for us and competes with us.”</b>“Then the contract must protect recipes and price lists, and we should keep enough own capacity for hero SKUs.”</div>
<div class="qa"><b>“What would you do on Monday?”</b>“Ask for the four data sets, set up the tracker and the decision log, and book the hero-SKU session with the Head of Sales.”</div>
<div class="qa"><b>“What about the CRISIL rating?”</b>“‘Issuer Not Cooperating’ means CRISIL stopped getting information. Monthly filings and the FY25–26 accounts are a four-week fix, and the rating matters to lenders, sellers and investors.”</div>

<h2><span class="n">14</span>Questions to ask them</h2>
<ol>
<li>Where does ₹512 Cr come from, and which year do you have in mind?</li>
<li>Was FY25’s drop a fall in sales or a move of billing inside the group?</li>
<li>Which channel earns the most per kilo for you today?</li>
<li>How full are the lines today, by plant?</li>
<li>What did you learn from quick commerce so far?</li>
<li>What would make the first 90 days a success for you?</li>
</ol>

<h2><span class="n">15</span>Your section: JD and background</h2>
<div class="card">
<p><b>JD mandates → slides</b> (from your problem-statement note; check against the JD): Quick commerce, modern trade, export GTM → slides 8–10 · 3P manufacturing and brand acquisitions → slide 11 · competitor benchmarking → slides 3–4 (and Deck 4 competition slides as backup) · board and investor reporting → slide 13 · operating velocity → slides 12–13.</p>
<p><b>Your background → where it fits</b> (add your own detail): A2 Ghee &amp; Honey 3P white-labelling and logistics → slides 9 and 11 (Vishal own-label co-packing, 3P) · LVX consumer-brand M&amp;A and Dubai/UK corridor → slides 10–11 · twice-weekly RAG system (65% → 90%) → slides 12–13.</p>
<p class="muted">Space for your 20-second “why me” line at the close (slide 14).</p>
</div>

<h2><span class="n">16</span>Numbers cheat sheet</h2>
<div class="tbl-wrap"><table>
<tr><th>Number</th><th>What</th><th>Source</th></tr>
<tr><td>₹288 Cr · −16% · −₹6.31 Cr</td><td>FY25 revenue, change, net loss (Kishlay Foods standalone)</td><td>Tracxn (MCA)</td></tr>
<tr><td>₹343.4 Cr · ₹335.3 Cr · ₹319.4 Cr</td><td>Revenue FY24, FY23, FY22</td><td>Motilal Oswal</td></tr>
<tr><td>₹335.59 Cr · −₹11.50 Cr · −₹20.69 Cr</td><td>FY23 consolidated operating income and PAT; FY22 PAT</td><td>CRISIL</td></tr>
<tr><td>70–75%</td><td>Raw materials in operating cost</td><td>CRISIL</td></tr>
<tr><td>B/Stable, Issuer Not Cooperating</td><td>Rating, 24 Jun 2026 (BBB− in 2021)</td><td>CRISIL</td></tr>
<tr><td>93% · ₹350–400 Cr</td><td>Bank-limit use (2023); management guidance (2024)</td><td>CRISIL</td></tr>
<tr><td>₹70.4 Cr</td><td>Secured charges: KFPL ₹45.9 Cr + Tulsi ₹24.5 Cr</td><td>Tracxn</td></tr>
<tr><td>512 · +15%</td><td>Tulsi employees, Feb 2026, YoY</td><td>Tracxn (labour filings)</td></tr>
<tr><td>99%</td><td>Kishlay Foods’ stake in Tulsi Pvt Ltd</td><td>Tracxn</td></tr>
<tr><td>2,600 t a month</td><td>Capacity: own 2,000 + AFP 300 + GUD 300</td><td>Company, job posts</td></tr>
<tr><td>₹34 · ₹49 · ₹54 · ₹99 · ₹19 · ₹11</td><td>Contribution per kilo: GT, MT, QC, UAE, Nepal export, Nepal licence</td><td>Model (estimate)</td></tr>
<tr><td>₹338 / ₹458 / ₹564 Cr</td><td>FY29 revenue bear / base / bull</td><td>Model</td></tr>
<tr><td>10.0% · ₹46 Cr</td><td>FY29 base EBITDA margin and EBITDA</td><td>Model</td></tr>
<tr><td>FY31</td><td>Year ₹512 Cr is reached in the base case</td><td>Model</td></tr>
<tr><td>₹520 Cr · 11.6%</td><td>Annapurna Swadisht FY26 revenue and EBITDA</td><td>Aggregator (verify NSE)</td></tr>
<tr><td>13.7% · 6.7% · 2.9%</td><td>EBITDA: Bikaji FY26, Gopal FY26, Prataap FY25</td><td>Company results</td></tr>
<tr><td>9.15× · 1.02×</td><td>Listed-peer median EV/EBITDA, EV/revenue</td><td>Tracxn</td></tr>
<tr><td>₹57.3 lakh</td><td>90-day budget (₹35 lakh is stock)</td><td>Model</td></tr>
</table></div>

<h2><span class="n">17</span>Tonight: price-screenshot checklist (20 minutes)</h2>
<p>Set each app to a Guwahati pin code (for example 781005), then a Kolkata pin code. Search each pack on Blinkit, Zepto, Instamart and BigBasket; screenshot the product page with price and pack size; note “not listed” where Non Stop is missing. Enter results in the model’s Price_Audit sheet (yellow cells).</p>
<div class="tbl-wrap"><table>
<tr><th>#</th><th>Kishlay pack</th><th>Compare with</th><th>Blinkit</th><th>Zepto</th><th>Instamart</th><th>BigBasket</th></tr>
<tr><td>1</td><td>Non Stop Aloo Bhujia 200 g (₹55)</td><td>Haldiram’s Aloo Bhujia 200 g</td><td>☐</td><td>☐</td><td>☐</td><td>☐</td></tr>
<tr><td>2</td><td>Non Stop Bikaneri Bhujia 400 g (₹110)</td><td>Bikaji Bikaneri Bhujia 400 g</td><td>☐</td><td>☐</td><td>☐</td><td>☐</td></tr>
<tr><td>3</td><td>Non Stop Paneer Bhujia 400 g (₹110)</td><td>Haldiram’s Aloo Bhujia 400 g</td><td>☐</td><td>☐</td><td>☐</td><td>☐</td></tr>
<tr><td>4</td><td>Non Stop Khatta Mitha 200 g (₹55)</td><td>Haldiram’s Khatta Meetha 180 g</td><td>☐</td><td>☐</td><td>☐</td><td>☐</td></tr>
<tr><td>5</td><td>Non Stop Navrattan Mixture 200 g (₹55)</td><td>Haldiram’s Navrattan 200 g</td><td>☐</td><td>☐</td><td>☐</td><td>☐</td></tr>
<tr><td>6</td><td>Non Stop Butter Cookies 150 g</td><td>Britannia Good Day Butter 150 g</td><td>☐</td><td>☐</td><td>☐</td><td>☐</td></tr>
<tr><td>7</td><td>Nutri Zing Soya Chunks 180 g</td><td>Nutrela Soya Chunks 200 g</td><td>☐</td><td>☐</td><td>☐</td><td>☐</td></tr>
<tr><td>8</td><td>Non Stop Water Toy Rings (₹5)</td><td>Yellow Diamond or Crax Rings</td><td>☐</td><td>☐</td><td>☐</td><td>☐</td></tr>
<tr><td>9</td><td>Non Stop Masala Noodles (₹5)</td><td>Wai Wai noodles</td><td>☐</td><td>☐</td><td>☐</td><td>☐</td></tr>
<tr><td>10</td><td>Zing potato chips (₹10)</td><td>Lay’s</td><td>☐</td><td>☐</td><td>☐</td><td>☐</td></tr>
</table></div>
<p><b>Use it tomorrow:</b> if Non Stop is missing on the apps, slide 8 becomes stronger (“I checked last night”). If it is listed, note the price and rank and say so.</p>

<footer>Prepared by Chethan N for the Kishlay Group (Tulsi Speciality Foods Pvt Ltd and Kishlay Foods Pvt Ltd). Every number is labelled Company, External, Historical, Calculation or Hypothesis in the deck and the model. Tracxn data was supplied for this work and is cited, not redistributed.</footer>
</main></body></html>'''
open(out, 'w').write(doc)
print('wrote', out, len(slides), 'slides')
