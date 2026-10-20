"""Build the GTM & execution plan as print HTML, then render it to PDF with render_pdf.mjs.

    python3 build_pdf.py engine_export.json data.json plan.html
    G=$(npm root -g) node render_pdf.mjs plan.html ../Creator-Intelligence-Engine-GTM-Plan.pdf

Creator and campaign numbers come from the engine export, so the PDF matches the platform.
"""
import html, json, sys

E = json.load(open(sys.argv[1]))
D = json.load(open(sys.argv[2]))
OUT = sys.argv[3]
NICHE = D["niches"]
TIER = {t["key"]: t["label"] for t in D["tiers"]}
BR = {b["id"]: b for b in D["brands"]}
VERT = dict(D["verticals"])
esc = html.escape


def inr(v):
    v = float(v)
    if v >= 1e7: return f"₹{v / 1e7:.2f} Cr".replace(".00 ", " ")
    if v >= 1e5: return f"₹{v / 1e5:.1f}L".replace(".0L", "L")
    if v >= 1e3: return f"₹{v / 1e3:.1f}K".replace(".0K", "K")
    return f"₹{v:.0f}"


def n(v):
    v = float(v)
    if v >= 1e6: return f"{v / 1e6:.2f}M".replace(".00M", "M")
    if v >= 1e3: return f"{v / 1e3:.1f}K".replace(".0K", "K")
    return f"{v:.0f}"


def table(head, rows, cls="", right=()):
    th = "".join(f'<th class="{"r" if i in right else ""}">{h}</th>' for i, h in enumerate(head))
    tr = "".join("<tr>" + "".join(f'<td class="{"r" if i in right else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<table class="t {cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def ul(items, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def sec(num, title, kicker, body, brk=True):
    return f'<section class="{"brk" if brk else ""}"><div class="sec-k">{num} · {kicker}</div><h1>{title}</h1>{body}</section>'


def callout(title, body, kind=""):
    return f'<div class="call {kind}"><b>{title}</b>{body}</div>'


def why_line(t):
    bits = [f"{t['fem'] * 100:.0f}% women in audience", f"ER {t['er']:.2f}%", f"link CTR {t['ctr']:.2f}%", f"{t['cred']:.0f}% real followers"]
    if t.get("creds"): bits.insert(0, t["creds"])
    return " · ".join(bits)


# ------------------------------------------------------------------------------------------------ sections
cover = """
<section class="cover">
  <div class="cv-top"><div class="cv-mark"><span>CI</span></div><div><div class="cv-n">Creator Intelligence Engine</div><div class="cv-s">Prepared for Chtrbox (Chatterbox Technologies Ltd)</div></div></div>
  <div class="cv-mid">
    <div class="cv-k">Founder's Office · Strategy &amp; Execution</div>
    <h1 class="cv-h">Verified ROI,<br>not vanity metrics.</h1>
    <p class="cv-p">The platform, the go-to-market and the operating plan to make creator selection and measurement Chtrbox's moat: 30, 60 and 90 days, then years one and two.</p>
  </div>
  <div class="cv-grid">
    <div><b>What is built</b><span>A working prototype: brand matching, forecasting, discovery, vertical playbooks and verified-ROI campaign analytics.</span></div>
    <div><b>What is asked</b><span>A six-person core pod and ₹81L for 90 days, released in tranches against measurable gates.</span></div>
    <div><b>What it returns</b><span>About ₹5.5 Cr a year in contribution at maturity (base case), plus a new measurement revenue line.</span></div>
  </div>
  <div class="cv-foot"><span>Chethan N · 21 October 2026</span><span>Platform data is simulated; company figures are from public sources, cited in the appendix.</span></div>
</section>"""

toc_items = [
    ("01", "Executive summary"), ("02", "Where Chtrbox stands"), ("03", "The problem from first principles"), ("04", "What is built: the platform"),
    ("05", "The data: 76 points per creator"), ("06", "The matching and forecasting model"), ("07", "The verified-ROI framework"),
    ("08", "Brand to creators: Olay, worked end to end"), ("09", "Across the client list, vertical by vertical"), ("10", "GTM segmentation model"),
    ("11", "Execution: 30 · 60 · 90 days"), ("12", "The data flywheel: 15, 45, 60, 90 days, 1–2 years"), ("13", "SOPs"), ("14", "KPIs"),
    ("15", "Team and organisation"), ("16", "Budget and funding"), ("17", "Management system"), ("18", "Guardrails"),
    ("19", "Before we proceed: pre-flight checks"), ("20", "Risks, warnings and honest cons"), ("21", "Roadmap: years one and two"),
    ("22", "Interview walkthrough and likely questions"), ("A", "Appendix: sources, assumptions, glossary"),
]
toc = '<section class="brk"><div class="sec-k">Contents</div><h1>What is in this document</h1><div class="toc">' + "".join(
    f'<div><span>{a}</span>{b}</div>' for a, b in toc_items) + "</div>" + callout(
    "How to read the numbers",
    "<p>Three kinds of number appear here, and each is marked. <b>Public:</b> Chtrbox and market figures from filings coverage and press, cited in the appendix. "
    "<b>Simulated:</b> creators, campaign results and forecasts from the prototype. Creator identities are synthetic. Brand names are publicly reported Chtrbox clients or labelled prospects, "
    "but every metric attached to them is modelled. <b>Assumption:</b> my estimates for cost, team and value, to be validated with the CFO in week one.</p>") + "</section>"

# 01 executive summary
olay, amz = E["olay"], E["amazon"]
s01 = sec("01", "Executive summary", "The short version", f"""
<p class="lede">Chtrbox grew revenue 42.5% to ₹84.2 Cr in FY26, but EBITDA margin fell from 20.5% to 17.0%. Growth is being bought with people: every new brief needs strategists to search, shortlist, negotiate and report by hand. The company has already said where it wants to go: from a service-led model to a platform and intelligence-led one, with verified ROI instead of vanity metrics. This document is the plan to get there.</p>
<div class="cols3">
  <div class="kpi"><b>3 questions</b><span>Every brand asks: who should we work with, what will it deliver, and did it work? The engine answers each with data instead of opinion.</span></div>
  <div class="kpi"><b>{olay['plan']['tg'] / olay['vanity']['tg']:.1f}× more</b><span>verified target-group views for Olay than a follower-count plan at the same ₹{olay['plan']['cost'] / 1e5:.0f}L spend (simulated), with {olay['plan']['fake'] * 100:.0f}% fake audience instead of {olay['vanity']['fake'] * 100:.0f}%.</span></div>
  <div class="kpi"><b>{amz['plan']['rev'] / amz['vanity']['rev']:.1f}× revenue</b><span>forecast for Amazon's conversion brief versus picking the biggest accounts first, using the same budget (simulated).</span></div>
</div>
<h2>What I am proposing</h2>
{ul([
    "<b>Build the Creator Intelligence Engine</b> on top of the real-time tracking and attribution Chtrbox already runs. It ranks creators for each brief with an explainable seven-part fit score, forecasts outcomes with a confidence band, and reports every campaign on a six-level verified-ROI ladder.",
    "<b>Start where the data is richest:</b> Beauty and E-commerce, which account for most of the reported client list (Olay, Bioderma, d'Alba, Celimax, Forever52, Nykaa, Amazon, Flipkart, Meesho). Then FMCG and Fashion, then Health and BFSI behind compliance gates, then the Dubai hub.",
    "<b>Protect the peak.</b> Days 0–60 overlap October–March, when about 60% of annual revenue lands. The engine runs in shadow mode beside strategists until it beats their picks on held-out briefs.",
    "<b>Make verified ROI a product.</b> Package it as a measurement fee (6–10% of creator spend) and as outcome-linked pricing for performance brands, creating a revenue line that does not scale with headcount.",
])}
<h2>What success looks like at day 90</h2>
{table(["Measure", "Today (to confirm)", "Day 90"], [
    ["Campaigns with a verified-ROI report (L4+)", "~0%", "50%"], ["Brief to shortlist", "~3 days", "4 hours"], ["Engine picks in final rosters", "–", "65%"],
    ["Views forecast error (MAPE)", "–", "under 20%"], ["Spend on fraudulent or conflicted creators", "unknown", "₹0"], ["Pitch win rate on verified-ROI pitches", "baseline", "+8 pts"]], right=(1, 2))}
<h2>What I need</h2>
<p>A six-person core pod (data engineer, ML scientist, two full-stack engineers, a measurement analyst and two data-ops associates, with design and compliance part-time), two strategists and a talent manager seconded part-time, and <b>₹81L for the first 90 days</b>. Year one is about ₹4.0 Cr all-in, released in three tranches against the day-90 and month-6 gates. Base-case payback is about 24 months, and the gates are there so we stop early if the numbers don't come.</p>
""")

# 02 where chtrbox stands
s02 = sec("02", "Where Chtrbox stands", "Public numbers, and what they imply", f"""
<div class="cols2">
<div>{table(["Metric", "Value", "Source"], [
    ["FY26 revenue from operations", "₹84.22 Cr, +42.5%", "[4][5]"], ["FY26 EBITDA · margin", "₹14.32 Cr · 17.0% (FY25: 20.5%)", "[4]"],
    ["FY26 PAT · margin", "₹9.2 Cr · 10.9% (FY25: 14.9%)", "[4]"], ["H2 FY26 revenue", "₹48.23 Cr, +50% YoY; PAT down 12%", "[3]"],
    ["FY26 revenue mix", "Represent 39% · Brand Solutions 36% · ChtrSocial 25%", "[5]"], ["FY25 revenue mix", "Represent 46% · ChtrSocial 11%", "[5]"],
    ["Seasonality", "~60% of revenue in H2 (Oct–Mar)", "[6][8]"], ["Geography (FY25)", "Maharashtra 57.9% of revenue", "[8]"],
    ["Client concentration", "Top-5 customers 22.6% (FY25), from 48.8% (FY24)", "[6]"], ["IPO (BSE SME, Oct 2025)", "₹42.86 Cr at ₹115; 52× subscribed", "[2]"],
    ["IPO use of proceeds", "Capex ₹11.07 Cr · office & studio ₹7.14 Cr · brand ₹5.02 Cr · WC ₹6.33 Cr", "[7]"],
    ["Network", "3L+ creators; ~104 exclusively managed", "[9][17]"], ["Leadership", "Raj Mishra, MD & CEO (ex-TikTok India)", "[9][10]"],
    ["Expansion", "Dubai hub for MENA (Jan 2026); evaluating tech acquisitions (Jun 2026)", "[10][11]"]], cls="small")}</div>
<div>
<div class="mini-chart"><div class="mc-h">FY26 revenue by segment (₹ Cr, derived)</div>
  <div class="hb"><span>Represent</span><i style="width:100%"></i><b>33.1</b></div>
  <div class="hb"><span>Brand Solutions</span><i style="width:92%"></i><b>30.5</b></div>
  <div class="hb"><span>ChtrSocial</span><i style="width:62.5%"></i><b>20.7</b></div>
  <div class="mc-f">84.22 × reported segment shares</div></div>
<div class="mini-chart"><div class="mc-h">Margin trend</div>
  <div class="hb"><span>EBITDA FY24</span><i style="width:100%" class="g"></i><b>21.8%</b></div>
  <div class="hb"><span>EBITDA FY25</span><i style="width:94%" class="g"></i><b>20.5%</b></div>
  <div class="hb"><span>EBITDA FY26</span><i style="width:78%" class="g"></i><b>17.0%</b></div></div>
{callout("Market context", "<p>Estimates for India's influencer-marketing market cluster around ₹3,600 Cr (2024) growing about 25% a year to roughly ₹4,500 Cr in 2025, with e-commerce the largest spender at about 23% share [18][19]. Brands are moving budget from experiments to accountable programmes, which favours the agency that can prove outcomes.</p>")}
</div></div>
<h2>Five implications</h2>
{ul([
    "<b>Margin is the problem to solve, not growth.</b> Revenue is growing faster than the market, but each rupee costs more to deliver. Tooling that cuts strategist hours per campaign and fees lost to bad picks goes straight to margin.",
    "<b>Represent and Brand Solutions are 75% of revenue and share one input: knowing which creator fits which brief.</b> The engine serves both. Talent managers see roster demand; strategists get shortlists.",
    "<b>The peak is October to March.</b> Any change to delivery must not land in the middle of festive and wedding season. Hence shadow mode first.",
    "<b>Concentration has fallen; repeat business now matters more.</b> With the top five clients at 22.6%, growth depends on many mid-size brands renewing. A verified-ROI report gives a renewal argument that a screenshot deck cannot.",
    "<b>The company has publicly committed to this direction.</b> IPO proceeds are earmarked for technology and creator intelligence, and the CEO has framed the goal as verified ROI with live tracking [12]. This plan executes a stated strategy rather than inventing a new one.",
])}
""")

# 03 first principles
s03 = sec("03", "The problem from first principles", "Why vanity metrics survive, and what replaces them", """
<p class="lede">A brand does not buy posts. It buys a change in what people think or do: remembering the brand, considering it, or buying it. Everything else is a proxy. Influencer marketing still runs on the weakest proxies because they are the easiest to collect.</p>
<div class="cols2">
<div><h2>Why vanity metrics persist</h2>""" + ul([
    "<b>Information asymmetry.</b> Creators report their own numbers, often as screenshots. Brands can't check audience quality.",
    "<b>No counterfactual.</b> Few campaigns run a holdout, so nobody knows which sales would have happened anyway.",
    "<b>Fragmented data.</b> Reach lives on the platform, clicks in link tools, orders in the brand's systems, returns in the warehouse.",
    "<b>Incentives.</b> Bigger reported numbers make everyone look good in the wrap-up deck.",
]) + """</div><div><h2>Four Rs, in order</h2>""" + ul([
    "<b>Reach:</b> real people in the target group, deduplicated and bot-filtered, not followers.",
    "<b>Relevance:</b> audience, category and cultural fit with the brief.",
    "<b>Resonance:</b> attention and trust: watch-through, saves, sentiment, recall lift.",
    "<b>Return:</b> verified and incremental outcomes, net of returns and organic baseline.",
]) + """<p class="muted">Chtrbox already describes matching as reach, relevance and resonance [9]. The engine adds the fourth R and puts a number on each.</p></div></div>
<h2>Where value leaks today</h2>""" + table(["Leak", "Cause", "What the engine does", "Measured by"], [
    ["Fake or inactive audiences bought", "Follower counts taken at face value", "Authenticity gate (72% real followers) and score", "Spend on gated creators = ₹0"],
    ["Competitor conflicts", "No memory of creators' recent brand work", "60-day exclusivity check before ranking", "Conflicts caught pre-contract"],
    ["Regulatory exposure", "Unqualified health or finance claims", "Credential and SEBI eligibility gates", "Compliance incidents = 0"],
    ["Strategist hours", "Manual search across thousands of profiles", "Ranked shortlist with reasons in minutes", "Brief-to-shortlist time"],
    ["Overpaying for reach", "Big accounts cost less per follower but deliver less per rupee", "Plan builder optimises outcome per rupee", "Cost per verified TG view"],
    ["Weak renewals", "Wrap-up decks can't prove impact", "Verified-ROI report with holdouts and lift", "Repeat-brand rate"],
]) + callout("The core bet", "<p>The agency that can say <i>these creators will deliver this, with this confidence</i>, and later <i>here is what actually happened, net of what would have happened anyway</i>, will win the accountable budgets. That needs three assets Chtrbox already has: a large creator network, years of campaign outcomes, and live tracking. The engine connects them.</p>", "accent"))

# 04 platform
s04 = sec("04", "What is built: the platform", "A working prototype, shown in the interview", f"""
<p>The prototype is a single offline web app (<span class="mono">Creator-Intelligence-Engine.html</span>) with seven modules. It runs on a sample of 420 synthetic creators, 35 brands across 9 verticals and 6 simulated campaigns. The scoring, forecasting and plan logic is the logic described in sections 5 to 7.</p>
<figure class="narrow"><img src="pdf_shots/overview.jpg" alt="Overview screen"><figcaption>Overview: the thesis, Chtrbox's public numbers, reported-versus-real views and claimed-versus-verified ROI.</figcaption></figure>
{table(["Module", "What it does", "Who uses it"], [
    ["Overview", "Thesis, why now, headline engine metrics", "Leadership, pitches"],
    ["Brand Match", "Brand DNA → hard gates → seven-part fit score → plan under budget → engine vs follower-count comparison → efficiency map", "Strategists"],
    ["Creator profile", "76 data points, audience vs target mirror, forecast with confidence band, reasons and risks", "Strategists, talent managers"],
    ["Discovery", "Plain-language search ('Hindi beauty creators under 25k with ER above 3%') parsed into filters, ranked for a brand", "Strategists, sales"],
    ["Vertical Lens", "Playbooks for 9 verticals, talent heatmap, top creators, archetypes, tier benchmarks", "Sales, planners"],
    ["Campaigns & ROI", "Live tracking, reported-to-real ladder, revenue waterfall, brand lift, holdout, leaderboard, alerts", "Account teams, brands"],
    ["How it works · Rollout", "Data families, formula, gates, ROI ladder, model maturity; 30/60/90 plan", "Everyone"],
])}
""")
s04b = """<section class="brk"><div class="cols2 figs">
<figure><img src="pdf_shots/match.jpg" alt="Brand Match"><figcaption>Brand Match for Olay: brand DNA, objective, the engine plan and the comparison with a follower-count plan at the same spend.</figcaption></figure>
<figure><img src="pdf_shots/drawer.jpg" alt="Creator profile"><figcaption>Creator profile: fit breakdown, reasons, risks and forecast with a confidence band.</figcaption></figure>
<figure><img src="pdf_shots/map.jpg" alt="Efficiency map"><figcaption>Efficiency map: outcome per rupee. The engine plan sits above the median line; the follower-count plan buys the expensive dots on the right.</figcaption></figure>
<figure><img src="pdf_shots/discover.jpg" alt="Discovery"><figcaption>Discovery: plain-language search parsed into filters.</figcaption></figure>
<figure><img src="pdf_shots/campaigns.jpg" alt="Campaigns"><figcaption>Campaigns &amp; ROI: the live Amazon campaign, from reported views to real people in the target group, and revenue you can defend.</figcaption></figure>
<figure><img src="pdf_shots/verticals.jpg" alt="Vertical Lens"><figcaption>Vertical Lens: where the talent is, by vertical and creator category.</figcaption></figure>
</div></section>"""

# 05 data
FAM = [
    ("Identity & profile", 12, "Platforms, followers by platform, tier, city, languages, primary and secondary category, pillars, verified credentials, roster status, market, gender", "Creator OAuth, CRM", "On change"),
    ("Audience", 14, "Gender, age buckets, city tiers, top cities, audience languages, affluence index, interests, overlap between creators, 12-month growth, 90-day growth, country split, active share, device mix, peak hours", "Instagram Graph / YouTube Analytics with consent", "Weekly"),
    ("Content & culture", 9, "Cultural codes, hook strength, production quality, format mix, cadence, integration style, comment sentiment, topics, visual safety tags", "Vision + language models on frames, audio, captions", "Per post"),
    ("Performance", 12, "ER, average views, view-through, 3-second hold, saves/view, shares/view, comment quality, story link CTR, reel/bio CTR, past conversion, recall lift, forecast-error history", "APIs + Chtrbox campaign history", "Daily / per campaign"),
    ("Authenticity", 7, "Real and active follower share, growth spikes, engagement pods, bot comments, engagement-follower consistency, sponsored saturation, bot-cluster overlap", "Graph analysis, anomaly detection", "Weekly"),
    ("Safety & compliance", 8, "Safety score, flag categories, ASCI disclosure rate, credential verification, competitor posts (120 days), exclusivity windows, controversies, regulated-category eligibility", "AI review + human QA", "Per post / monthly"),
    ("Commercials", 6, "Rate card, negotiated-rate history, on-time delivery, response time, payment terms, TDS (194R/194J) and GST status", "Chtrbox ops data", "Per deal"),
    ("Outcomes", 8, "API-verified views, unique reach, tracked clicks, orders and revenue net of returns, incrementality, brand lift, 12-month value, content reuse in paid", "Existing tracking & attribution, brand data, lift studies", "Per campaign"),
]
s05 = sec("05", "The data: 76 points per creator", "What we collect, from where, how often", table(["Family", "#", "Data points", "Source", "Refresh"], [[f"<b>{a}</b>", b, c, d, e] for a, b, c, d, e in FAM], cls="small") + """
<div class="cols2"><div><h2>Acquisition plan</h2>""" + ul([
    "<b>Consent first.</b> Creators connect Instagram and YouTube through OAuth, which unlocks first-party audience demographics that public scraping cannot give and platform terms do not allow.",
    "<b>Start with the Represent roster</b> (about 104 creators), where Chtrbox has a contract and a relationship. Then the 2,000 creators used most in the last 24 months, then the next 8,000.",
    "<b>Give creators a reason:</b> a personal scorecard, faster brief matching and faster payments in exchange for connecting.",
    "<b>Fill gaps with licensed data,</b> such as third-party creator-data APIs, for coverage beyond consented creators, clearly flagged as lower confidence.",
]) + """</div><div><h2>Data-quality rules</h2>""" + ul([
    "Every field carries its source, timestamp and confidence; stale fields decay in the score.",
    "Audience data older than 30 days is refreshed before a creator is shortlisted.",
    "Brand outcome data is used for training only in aggregate, under a contract clause agreed with each brand.",
    "No personal data on followers is stored. The engine needs distributions, not individuals.",
    "A data-ops associate reviews a 5% sample of AI tags each week; tags below 90% precision are retrained.",
]) + "</div></div>")

# 06 model
s06 = sec("06", "The matching and forecasting model", "Explainable by design", """
<div class="formula">Fit = w<sub>1</sub>·Audience fit + w<sub>2</sub>·Content affinity + w<sub>3</sub>·Culture &amp; language + w<sub>4</sub>·Performance + w<sub>5</sub>·Authenticity + w<sub>6</sub>·Safety &amp; compliance + w<sub>7</sub>·Cost efficiency &nbsp;(+ Represent boost ≤ 5)</div>
""" + table(["Part", "How it is measured", "Awareness", "Consideration", "Conversion"], [
    ["Audience fit", "Overlap of gender, age, city tier and affluence with the brand's target", "22", "20", "18"],
    ["Content affinity", "Brand's affinity to creator's primary (75%) and secondary (25%) category", "15", "18", "14"],
    ["Culture & language", "Best language match + shared cultural codes (festive, regional pride, Gen-Z humour…)", "14", "10", "8"],
    ["Performance", "Within-tier percentiles. Awareness: view-through, hold, recall. Consideration: ER, saves+shares, sentiment. Conversion: link CTR, trust, ER", "15", "20", "26"],
    ["Authenticity", "Real-follower share, content quality, sponsored saturation, growth anomalies", "14", "14", "14"],
    ["Safety & compliance", "Brand-safety score and #ad disclosure rate", "10", "8", "8"],
    ["Cost efficiency", "Outcome per rupee, percentile among eligible creators", "10", "10", "12"],
], cls="small", right=(2, 3, 4)) + """
<div class="cols2"><div><h2>Hard gates, before any score</h2>""" + ul([
    "Real and active followers below 72%",
    "Brand-safety score below 55",
    "Posted for a named competitor in the last 60 days",
    "Finance: investing content without SEBI registration (SEBI-regulated brands cannot associate)",
    "Health: technical claims without a medical or nutrition qualification (ASCI Addendum II)",
    "Audience outside the campaign's market",
]) + """<p class="muted">Gated creators are listed with the reason, so a strategist can challenge a gate rather than wonder why someone is missing.</p></div><div><h2>Forecast, per creator</h2>""" + ul([
    "Views = average reel views + story views (followers × tier story-view rate × 2)",
    "Verified TG views = views × real-follower share × target-group share",
    "Clicks = (reel views × CTR × 0.3 + story views × CTR × 1.3) × category affinity",
    "Orders = clicks × brand conversion × creator trust × assist factor (codes, affiliate, search)",
    "Confidence band ±12%, ±22% or ±35% depending on tracked campaigns and lift studies",
]) + """<h2>Plan builder</h2><p>Picks creators by fit² × authenticity × outcome per rupee, including a ₹3,000 per-creator operating cost, with caps of one mega and three macro creators and no single creator above 25% of budget.</p></div></div>
<h2>How the model improves</h2>""" + table(["Version", "When", "What changes", "Gate to move on"], [
    ["v0 · rules", "Days 0–15", "Expert weights, gates, benchmarks from historical campaigns", "Strategists agree the top 20 are plausible on 5 briefs"],
    ["v1 · calibrated", "Days 30–45", "Forecast multipliers fitted to the first 10+ tracked campaigns, by tier and vertical", "Views MAPE < 30%"],
    ["v2 · learning-to-rank", "Days 60–90", "Ranking trained on strategist choices and outcomes; overrides become labels", "Engine picks ≥ 50% of final rosters"],
    ["v3 · incrementality", "Months 4–6", "Holdout and brand-lift results reweight forecasts toward incremental outcomes", "iROAS reported on 80% of conversion spend"],
    ["v4 · graph and pricing", "Year 1–2", "Creator–brand graph predicts fit for new brands; fair-rate model per outcome", "Pricing accepted by 5+ brands"],
], cls="small") + callout("Fairness check", "<p>Performance is compared within each tier, so nano and regional creators are not crowded out by reach. Each quarter we audit the share of shortlist slots by language, city tier and creator gender against the eligible pool, and investigate any group under-selected by more than 20%.</p>"))

# 07 verified ROI
s07 = sec("07", "The verified-ROI framework", "Every number carries its level", table(["Level", "Name", "What it means", "Method", "Who can claim it"], [
    ["L0", "Reported", "Followers, likes, creator screenshots", "None", "Never shown as a result"],
    ["L1", "Verified delivery", "Views pulled by API, deduped", "Creator OAuth, platform insights", "Delivery reports"],
    ["L2", "Quality", "Real people in the target group, watch time", "Authenticity and audience model", "Awareness reports"],
    ["L3", "Action", "Tracked clicks, codes, installs, add-to-cart", "Existing tracking and attribution", "Performance reports"],
    ["L4", "Outcome", "Orders and revenue matched to brand data, net of returns", "Brand data, marketplace attribution, MMP", "'Verified' starts here"],
    ["L5", "Incremental", "Outcomes that would not have happened anyway", "Geo holdouts, brand lift, MMM", "iROAS"],
], cls="small") + """
<div class="cols2"><div><h2>Measurement by objective</h2>""" + table(["Objective", "Primary", "Method"], [
    ["Awareness", "Verified TG reach, ad recall lift", "Brand lift: exposed vs control, n ≈ 1,200 per cell"],
    ["Consideration", "Consideration lift, saves, PDP visits", "Brand lift + tracked clicks"],
    ["Conversion", "Verified orders, iROAS, CAC", "Codes + links + affiliate; 6 test vs 6 control cities"],
], cls="small") + """</div><div><h2>What a client report contains</h2>""" + ul([
    "Spend, delivery and pacing against plan",
    "The ladder: reported → API-verified → unique → real → in target group",
    "Revenue waterfall: attributed → returns → organic baseline → incremental",
    "Brand lift with sample sizes and significance",
    "Creator leaderboard: forecast vs actual",
    "What we changed mid-flight and why",
    "The level (L0–L5) of every number",
]) + "</div></div>" + f"""
<figure class="narrow short"><img src="pdf_shots/campaigns.jpg" alt="Campaign analytics"><figcaption>Simulated Amazon campaign: {n(D['campaigns'][0]['totals']['rep'])} reported views become {n(D['campaigns'][0]['totals']['tg'])} real people in the target group. Attributed ROAS is about 3.1×; incremental ROAS after returns and organic baseline is about 1.7×.</figcaption></figure>
""" + callout("Why this is a sales asset, not just a report", "<p>The honest number is usually lower than the vanity number. Brands that have been burned know this. Showing the claimed figure, the attributed figure and the incremental figure side by side, then showing how the engine raises the incremental one, is the strongest renewal and pitch argument available.</p>", "accent"))

# 08 Olay deep dive
o = E["olay"]; ob = BR["olay"]
rows8 = []
for i, t in enumerate(o["top"][:10]):
    rows8.append([str(i + 1), f"<b>{esc(t['name'])}</b><br><span class='muted'>{t['id']} · {esc(t['city'])} · {esc(', '.join(t['langs']))}</span>",
                  f"{esc(NICHE[t['niche']])}<br><span class='muted'>{TIER[t['tier']]} · {n(t['followers'])}</span>",
                  f"<b>{t['fit']:.0f}</b>", f"{t['er']:.2f}%", f"{t['ctr']:.2f}%", f"{t['cred']:.0f}%", inr(t['cost']), n(t['tg']), n(t['eng']), f"+{t['recall']:.1f}"])
top3 = o["top"][:3]
p, v = o["plan"], o["vanity"]
s08 = sec("08", "Brand to creators: Olay, worked end to end", "One reported client, every data point", f"""
<div class="cols2"><div>
<h2>The brief (Brand DNA)</h2>
{table(["Field", "Olay"], [
    ["Category", "Premium skincare (P&G) · Reported Chtrbox client"], ["Job to be done", esc(ob['brief'])], ["Objective", "Consideration"],
    ["Target", "86% women · core age 25–34 (44%) and 35–44 (21%) · 62% tier 1 · affluence index 70"],
    ["Languages", "English, Hinglish, Hindi"], ["Cultural codes", "Science-backed · Aspirational luxury · Working professional"],
    ["KPIs", "Consideration lift · saves per view · PDP clicks"], ["Exclusivity (60 days)", esc(', '.join(ob['competitors']))], ["Moment", esc(ob['moment'])]], cls="small")}
</div><div>
<h2>What the engine did</h2>
{table(["Step", "Result"], [
    ["Creators indexed", "420"], ["Gated before ranking", f"{o['gated']}: " + ", ".join(f"{v2} {k}" for k, v2 in o['gates'].items()).replace("fraud", "fake audience").replace("conflict", "competitor conflicts").replace("market", "wrong market")],
    ["Eligible and ranked", str(o['eligible'])], ["In the ₹{:.0f}L plan".format(o['budget']), f"{p['n']} creators"],
    ["Verified TG views", f"{n(p['tg'])} vs {n(v['tg'])} for a follower-count plan ({p['tg'] / v['tg']:.1f}×)"],
    ["Engagements", f"{n(p['eng'])} vs {n(v['eng'])} ({p['eng'] / v['eng']:.1f}×)"],
    ["Ad recall lift", f"+{p['recall']:.1f} vs +{v['recall']:.1f} pts"], ["Fake or inactive audience bought", f"{p['fake'] * 100:.0f}% vs {v['fake'] * 100:.0f}%"]], cls="small")}
<p class="muted">Same spend for both plans. The follower-count plan simply buys the largest accounts until the money runs out.</p>
</div></div>
<h2>Top 10 creators for Olay (simulated)</h2>
{table(["#", "Creator", "Category · tier", "Fit", "ER", "Link CTR", "Real", "Bundle cost", "TG views", "Engagements", "Recall"], rows8, cls="small", right=(3, 4, 5, 6, 7, 8, 9, 10))}
<h2>What the top three bring to the table</h2>
<div class="cols3">{"".join(f'<div class="kpi"><b>{esc(t["name"])}</b><span>{esc(NICHE[t["niche"]])} · {TIER[t["tier"]]} · {esc(t["city"])}<br>{esc(why_line(t))}. Forecast {n(t["tg"])} verified TG views and {n(t["eng"])} engagements for {inr(t["cost"])}, recall +{t["recall"]:.1f} pts, {t["conf"].lower()} confidence.</span></div>' for t in top3)}</div>
""")

# 09 across the client list
pick = [("fmcg", "dabur"), ("ecom", "amazon"), ("beauty", "olay"), ("fashion", "puma"), ("health", "hkvitals"), ("bfsi", "groww"), ("tech", "hp"), ("services", "indigo"), ("ent", "spotify")]
blocks = []
for vk, bid in pick:
    b = E[bid]; bb = BR[bid]
    obj = b["objective"]
    metric = {"awareness": ("TG views", "tg"), "consideration": ("Engagements", "eng"), "conversion": ("Orders", "orders")}[obj]
    rr = [[f"<b>{esc(t['name'])}</b>", f"{esc(NICHE[t['niche']])} · {TIER[t['tier']]} · {esc(t['langs'][0])}", f"{t['fit']:.0f}", inr(t["cost"]), n(t[metric[1]]), esc(why_line(t))] for t in b["top"][:5]]
    mult = b["plan"][metric[1]] / max(1, b["vanity"][metric[1]])
    blocks.append(f'<div class="vb"><div class="vb-h"><b>{esc(VERT[vk])}</b> · {esc(bb["name"])} <span class="muted">({esc(bb["status"])}, {obj})</span><span class="vb-r">Engine plan {mult:.1f}× the follower-count plan on {metric[0] if metric[0].startswith("TG") else metric[0].lower()}</span></div>'
                  + table(["Creator", "Archetype", "Fit", "Cost", metric[0], "Data points"], rr, cls="small", right=(2, 3, 4)) + "</div>")
allrows = []
for bid, b in E.items():
    obj = b["objective"]; k = {"awareness": "tg", "consideration": "eng", "conversion": "rev"}[obj]
    vv = b["vanity"][k] or 1
    allrows.append([esc(b["name"]), esc(VERT[b["vertical"]]), esc(b["status"]), obj, str(b["gated"]), str(b["plan"]["n"]), inr(b["plan"]["cost"]), f"{b['plan'][k] / vv:.1f}×", f"{b['plan']['fake'] * 100:.0f}% / {b['vanity']['fake'] * 100:.0f}%"])
s09 = sec("09", "Across the client list, vertical by vertical", "Who resembles each brand, and why", "<p>For one brand in each vertical, the five best-fit creators and the data points that put them there. The full ranking for all 35 brands is live in the platform.</p>" + "".join(blocks[:5]))
s09b = '<section class="brk">' + "".join(blocks[5:]) + "<h2>All 35 brands at a glance (simulated)</h2>" + table(["Brand", "Vertical", "Status", "Objective", "Gated", "Plan size", "Spend", "Engine ÷ follower plan", "Fake audience (engine / follower)"], allrows, cls="tiny", right=(4, 5, 6, 7)) + "</section>"

# vertical playbooks
PB = [
    ("FMCG", "Reach the target group often and cheaply, then prove memory moved. Sales show up in quick-commerce and kirana, not clicks.", "TG reach & frequency → recall lift → q-commerce search/sales lift in test cities → sampling redemptions", "60% nano/micro regional, 30% mid, one macro anchor", "Health-benefit claims need substantiation; no cure language (Drugs & Magic Remedies Act)"),
    ("E-commerce", "Every rupee should trace to an order: CTR × conversion, net of returns, with new-customer share as the quality check.", "Verified orders net of returns → iROAS from geo holdouts → new-customer share → CAC and 60-day repeat", "Micro and mid with high link CTR; macro only on sale days", "Price claims must match listings; disclose affiliate earnings; no dark-pattern urgency"),
    ("Beauty & personal care", "Beauty is bought on proof. Saves, tutorial completion and credible voices predict sales better than likes.", "Saves/view → consideration lift → PDP CTR and sampling-to-repeat → efficacy sentiment", "Dermatologists for actives, micro for routines, K-culture Gen-Z for K-beauty", "No exaggerating filters; technical skin claims need qualified creators"),
    ("Fashion & footwear", "Fashion runs on taste and on returns. Saves show taste; return-adjusted revenue shows whether it sold.", "Saves & shares → PDP CTR → revenue net of returns → store visits", "Distinct-style micro, mid for drops, 1–2 macro for launches", "Disclose gifting; substantiate sustainability claims"),
    ("Healthcare & wellness", "Trust is the product. A qualified creator with a smaller audience beats a large lifestyle account.", "Credentialed reach → trust & sentiment → bookings/orders → 60–90 day repeat", "Mid-tier doctors and dietitians as the spine; fitness for lifestyle use", "ASCI Addendum II credentials; no disease-cure claims"),
    ("BFSI & fintech", "The most regulated category. Gate who may speak, then optimise for funded accounts, not installs.", "Funded accounts/policies → cost per funded account → KYC completion → grievance rate", "SEBI-registered advisers for product talk; others brand-scripted only", "SEBI finfluencer rules; IRDAI for insurance; ASCI Addendum II"),
    ("Consumer tech", "Researched before bought. Depth and credibility of reviews beat reach.", "Consideration lift → store/PDP visits → model-name search lift → review sentiment", "YouTube reviewers for depth; Shorts/Reels for launches; education and gaming for laptops", "No paid reviews presented as organic; disclose free devices"),
    ("Food, travel & services", "Services are local. City-level creators and redeemable codes tie spend to bookings.", "Bookings/app orders → code redemptions by city → route or store lift → repeat", "City-specific micro and mid; diaspora creators for Gulf routes", "Offer terms must match the app"),
    ("Entertainment & music", "Music wins by being used, not watched. Audio uses and shares lead.", "Audio uses → week-one stream lift → shares/view → recall for platform campaigns", "Meme-native comedy and dance creators; nano seeding at scale", "Licensing on audio; disclose label partnerships"),
]
s09c = sec("09b", "Vertical playbooks", "What actually matters in each category", table(["Vertical", "Thesis", "KPI stack (in order)", "Tier mix", "Compliance gate"], [[f"<b>{a}</b>", b, c, d, e] for a, b, c, d, e in PB], cls="tiny xtiny"))

# 10 GTM
s10 = sec("10", "GTM segmentation model", "Who buys what, in what order", table(["Segment", "Example accounts (reported clients unless marked)", "What they buy", "Offer", "Pricing logic"], [
    ["A · Enterprise brand-builders", "P&G (Olay, Whisper), Coca-Cola, Nestlé (KitKat), Dabur, Samsung, HP, Sony, Philips", "Safety, scale, proof of recall", "<b>Verified Reach &amp; Lift</b>: L2 delivery + brand lift + gates", "Managed fee + 6–8% measurement fee; lift studies ₹1.5–2.5L each"],
    ["B · Performance commerce", "Amazon, Flipkart, Meesho, Nykaa, Neeman's, HK Vitals, Forever52, Zink London, d'Alba, Celimax, Crocs", "Orders, CAC, iROAS", "<b>Verified Performance</b>: L4–L5, codes, affiliate, holdouts", "Base fee + bonus above an agreed iROAS; 8–10% measurement fee"],
    ["C · Regulated categories", "Groww, PolicyBazaar, CRED, Tata 1mg, Cult (prospects); Bioderma, HK Vitals", "Compliance, trust, auditability", "<b>Compliant Expert Network</b>: credential-verified creators, claim review, audit trail", "Premium managed fee; per-creator verification fee"],
    ["D · Agencies & in-house teams", "Media agencies subcontracting influencer work; brand in-house teams", "Speed and evidence", "<b>Intelligence seats</b> (Year 2): shortlists, benchmarks, reports", "SaaS seats + usage"],
    ["E · Cross-border (MENA)", "IndiGo (Dubai routes), Indian brands entering the UAE, GCC brands targeting the diaspora", "Diaspora reach", "<b>Cross-border creator graph</b> from the Dubai hub", "Managed fee, premium rates"],
    ["Supply side · Represent", "~104 exclusive creators", "More and better-fitting briefs", "Creator scorecards and demand view", "Higher utilisation, no direct fee"],
], cls="tiny xtiny") + """
<div class="cols2"><div><h2>Sequencing</h2>""" + table(["When", "Segments", "Why"], [
    ["Days 0–45", "B (e-com) + Beauty from A/B", "Most frequent briefs, measurable outcomes, strongest client list"],
    ["Days 46–90", "Add FMCG and Fashion; Segment A lift studies", "Brand-lift method proven on pilots"],
    ["Months 4–6", "C, regulated", "Gates and claim review proven first"],
    ["Day 61+ pilot, Year 1 scale", "E, MENA", "Dubai team in place; small graph first"],
    ["Year 2", "D, seats", "Product mature enough for self-serve"],
], cls="small") + """</div><div><h2>Account prioritisation score</h2>""" + ul([
    "<b>Relationship</b> (existing client = 3, warm = 2, cold = 1)",
    "<b>Spend size</b> (annual creator spend band)",
    "<b>Data readiness</b> (pixel or attribution available, willing to share outcomes)",
    "<b>Objective clarity</b> (a KPI that maps to L3+)",
    "<b>Regulatory complexity</b> (lower is better early)",
    "<b>Timing</b> (a moment in the next 60 days)",
]) + """<p class="muted">The top 15 accounts by this score get the free verified-ROI audit offer in week three.</p></div></div>
<h2>Sales motion</h2>""" + ul([
    "<b>Existing clients first:</b> offer a free verified-ROI audit of their last campaign (8 pilot brands). Show the gap between claimed and verified, then show how the engine closes it. Convert to a measurement package.",
    "<b>New logos:</b> lead with Vertical Lens insight (benchmarks, archetypes, cost per outcome by tier) and the audit offer.",
    "<b>Agencies:</b> white-label measurement for media agencies that subcontract influencer work.",
    "<b>Thought leadership:</b> a quarterly 'India Creator ROI Index' built from aggregated, anonymised benchmarks, for PR and lead generation.",
]))

# 11 execution
gantt_rows = [
    ("Data & consent", [(0, 12, "Inventory · schema"), (12, 45, "Represent OAuth → top 2,000"), (45, 90, "Next 6,000 creators")]),
    ("Model", [(5, 15, "v0"), (30, 45, "v1 calibrate"), (60, 90, "v2 rank")]),
    ("Product", [(0, 30, "Internal tool"), (30, 60, "ROI report + dashboard"), (60, 90, "Represent view")]),
    ("Measurement", [(10, 26, "Tracking QA gate"), (26, 60, "First holdout + lift"), (60, 90, "Scale")]),
    ("GTM", [(15, 45, "3 pilots · audits"), (46, 60, "Package + price"), (61, 90, "Sell · MENA pilot")]),
    ("People", [(0, 30, "Hire / contract"), (30, 60, "Train strategists"), (60, 90, "Champions")]),
    ("Governance", [(0, 90, "Weekly WBR · monthly steering · gates at day 30, 45, 60, 90")]),
]
gantt = '<div class="gantt"><div class="g-axis"><span></span>' + "".join(f'<span style="left:{d / 90 * 100}%">D{d}</span>' for d in (0, 15, 30, 45, 60, 75, 90)) + "</div>"
for name, bars in gantt_rows:
    gantt += f'<div class="g-row"><span class="g-n">{name}</span><div class="g-track">' + "".join(f'<i style="left:{a / 90 * 100}%;width:{(b - a) / 90 * 100}%">{t}</i>' for a, b, t in bars) + "</div></div>"
gantt += "</div>"
PH = [
    ("Days 0–15 · Foundation", "Stakeholder interviews (CEO, heads of Brand Solutions, Represent, ChtrSocial, finance, tech); inventory campaign history, roster and tracking feeds; freeze schema and Brand DNA template; v0 rules and gates; consent flow for Represent; measure baselines; pick 3 pilot brands", "Programme lead, data engineer, ML scientist", "Data inventory, baseline sheet, v0 model, pilot list", "Inventory signed off; baselines measured; 3 pilots agreed"),
    ("Days 16–30 · Shadow mode", "Engine runs beside strategists on 6–8 live briefs with no change to delivery; weekly pick-vs-pick review; tracking QA becomes a go-live gate; design the first holdout and brand-lift study", "Strategist champions, analyst", "Pick-vs-pick log, tracking QA checklist, test designs", "Engine picks ≥ 30% of final rosters; zero untracked campaigns"),
    ("Days 31–45 · Calibrate", "Fit forecasts to first outcomes (v1); tune fraud and safety thresholds on real cases; deliver the first verified-ROI report; close data gaps", "ML scientist, analyst", "v1 model, first L4 report", "Views MAPE < 30%; one L4 report delivered"),
    ("Days 46–60 · Productise", "Brand-facing report and dashboard template; package and price Verified ROI; train every strategist; add Fashion and FMCG; 15+ campaigns through the engine", "Programme lead, designer, sales lead", "Report template, 2 priced packages, training", "25% of campaigns at L4+"),
    ("Days 61–90 · Scale", "50% of campaigns through the engine; v2 learning-to-rank; Represent utilisation view; Dubai pilot (300-creator UAE graph); CFO review of payback", "Whole pod", "v2 model, Represent view, MENA seed, gate pack", "50% at L4+; win rate +5 pts; day-90 gate passed"),
]
WEEKS = [
    ("Week 1", "Meet every head of function; agree success metrics; data inventory; baseline brief-to-shortlist time, win rate, margin per campaign, repeat rate"),
    ("Week 2", "Schema freeze; v0 weights with strategists; Represent consent flow live; tracking audit; hiring or contractor plan approved"),
    ("Week 3", "Shadow mode on the first 3 briefs; pick-vs-pick review; tracking QA SOP live; audit offers to the top 15 accounts"),
    ("Week 4", "Shadow mode on 3–5 more briefs; first holdout designed; WBR cadence running; day-30 gate review with CEO and CFO"),
]
s11 = sec("11", "Execution: 30 · 60 · 90 days", "Workstreams, owners, exit criteria", gantt + table(["Phase", "Key actions", "Owners", "Deliverables", "Exit criteria"], [[f"<b>{a}</b>", b, c, d, e] for a, b, c, d, e in PH], cls="tiny") +
    "<h2>The first 30 days, week by week</h2>" + table(["Week", "What happens"], [[f"<b>{a.replace(' ', '&nbsp;')}</b>", b] for a, b in WEEKS], cls="small"))

# 12 flywheel
FLY = [
    ("Days 0–15", "24 months of campaign history; Represent roster data; current tracking feeds", "Baseline benchmarks per vertical and tier; which fields predict outcomes; data gaps", "v0 weights and gates; benchmark tables", "Strategists get a ranked list on day 15"),
    ("Days 15–45", "6–8 shadow briefs; pick-vs-pick outcomes; first live results; override reasons", "Forecast error by tier and vertical; why strategists disagree; false positives in the fraud gate", "v1 calibration; vertical weight presets; threshold tuning", "Forecasts trusted enough to quote ranges to pilot brands"),
    ("Days 45–60", "15+ campaigns at L4; first brand-lift study; first holdout", "Which content codes and languages drive outcomes per vertical; creator-level conversion; recall per creator", "Creator-level priors; vertical-specific weights; fair-rate insight", "First Verified ROI packages priced and pitched"),
    ("Days 60–90", "30+ campaigns; ~500 logged strategist decisions; Represent demand data; UAE seed data", "What good strategists know that the rules miss", "v2 learning-to-rank; Represent utilisation model", "50% of campaigns through the engine; talent managers see demand"),
    ("Months 4–12", "150+ campaigns; holdouts at scale; consented data for 8,000+ creators", "Incrementality by vertical, tier and format; rate-to-outcome curves", "v3 incrementality-calibrated forecasts; pricing model; creator scorecards", "Outcome-linked pricing; margin +3 pts; renewals citing verified ROI"),
    ("Years 1–2", "500+ campaigns a year; 25,000 consented creators; brand outcome partnerships", "Fit for brands with no history; demand forecasting by season", "v4 creator–brand graph; seasonal demand model", "Intelligence subscriptions; data partnerships; MENA graph live"),
]
s12 = sec("12", "The data flywheel", "How each phase's data makes the next phase better", table(["Window", "Data in", "What we learn", "Model change", "Business effect"], [[f"<b>{a}</b>", b, c, d, e] for a, b, c, d, e in FLY], cls="tiny") +
    callout("Why the flywheel compounds", "<p>Each campaign adds three things competitors cannot buy: a forecast-versus-actual pair for every creator, a strategist decision with a reason, and (from L4) an outcome tied to a brand's sales. After about 150 campaigns the forecasts are tuned to Indian categories, languages and seasons in a way a generic creator-data tool cannot match. That is the moat.</p>", "accent"))

# 13 SOPs
SOPS = [
    ("SOP-01 · Brief intake → Brand DNA", "New brief received", "Brand strategist (R) · Head of Brand Solutions (A)", "Capture objective and KPI; fill target (gender, age, tier, affluence), languages, cultural codes, competitors and exclusivity window, compliance class, budget and moment; confirm with brand", "4 business hours", "Signed-off Brand DNA in the engine"),
    ("SOP-02 · Creator onboarding & consent", "Creator joins roster or is shortlisted", "Data-ops (R) · Head of Represent (A)", "OAuth connect; DPDP consent notice and record; verify credentials (medical, SEBI, CA); PAN for TDS; safety and authenticity scan; tag niche and codes", "48 hours", "Creator profile at confidence ≥ medium"),
    ("SOP-03 · Shortlist & human review", "Brand DNA approved", "Strategist (R) · Programme lead (A)", "Run engine; review gated list; pick final roster; log every override with a reason code; check plan against budget and tier caps", "4 hrs (2 hrs by month 6)", "Shortlist + plan + forecast ranges"),
    ("SOP-04 · Contracting & compliance", "Roster approved by brand", "Ops (R) · Legal counsel (A)", "Contract with ASCI disclosure clause, exclusivity, morality/kill clause, usage rights, data-sharing clause; TDS (194R/194J) and GST handling; regulated-category script rules", "48 hours", "Executed contracts"),
    ("SOP-05 · Content review & brand safety", "Draft content received", "Strategist (R) · Compliance (C)", "AI pre-check for claims, disclosure position and safety; human review; health and finance claim check against substantiation; approve or return with notes", "24 hours", "Approved content with audit trail"),
    ("SOP-06 · Tracking setup & go-live gate", "Content approved", "Analyst (R) · Programme lead (A)", "Unique links and codes per creator; affiliate tags; brand pixel/MMP check; holdout cities fixed; test every link; no tracking, no launch", "Before go-live", "Tracking QA pass (100%)"),
    ("SOP-07 · Live monitoring & optimisation", "Campaign live", "Analyst (R) · Strategist (C)", "Daily pulse; alert if CTR < 60% of forecast at 48 hours (swap creative), pacing off by > 15%, disclosure missing (fix within 2 hours); reallocate budget to over-performers", "Daily", "Alert log and actions"),
    ("SOP-08 · Verified-ROI report", "Campaign closes", "Analyst (R) · Head of Brand Solutions (A) · Brand (C)", "Pull API data; dedupe and bot-filter; match outcomes; net returns; compute holdout lift and brand lift; label every number L0–L5; review with brand", "T+7 days (T+5 by month 6)", "Client report + data write-back"),
    ("SOP-09 · Data quality & retraining", "Weekly", "ML scientist (R) · Programme lead (A)", "Drift checks; 5% tag audit; forecast error by segment; retrain monthly; model card updated; fairness audit quarterly", "Weekly / monthly", "Model card, MAPE trend"),
    ("SOP-10 · Incident response", "Creator controversy, disclosure breach, fraud found, data breach", "Programme lead (R) · Legal (A) · CEO (I)", "Triage within 1 hour; pause content if needed; inform brand within 4 hours; for personal-data breach follow DPDP notification duties; root cause and fix within 5 days", "1 hr triage", "Incident record and fix"),
]
s13 = sec("13", "SOPs", "Ten procedures that make it repeatable", table(["SOP", "Trigger", "Owner", "Steps", "SLA", "Output"], [[f"<b>{a}</b>", b, c, d, e, f] for a, b, c, d, e, f in SOPS], cls="tiny"))

# 14 KPIs
KPIS = [
    ("North Star", "Share of campaign revenue reported at L4+", "Revenue of campaigns with an L4+ report ÷ total campaign revenue", "~0%", "3 pilots", "25%", "50%", "90%"),
    ("Engine", "Brief to shortlist", "Time from approved Brand DNA to shortlist", "~3 days", "1 day", "6 hrs", "4 hrs", "2 hrs"),
    ("Engine", "Engine picks in final roster", "Final-roster creators from engine top 30 ÷ roster size", "–", "30%", "50%", "65%", "75%"),
    ("Engine", "Views forecast error", "Mean absolute % error, posted creators", "–", "< 35%", "< 25%", "< 20%", "< 15%"),
    ("Data", "Creators with consented data", "Creators with live OAuth connection", "0", "1,500", "4,000", "8,000", "25,000"),
    ("Safety", "Spend on gated creators", "₹ spent on creators failing a gate", "unknown", "₹0", "₹0", "₹0", "₹0"),
    ("Safety", "#ad disclosure on live posts", "Compliant posts ÷ paid posts", "~85%", "95%", "98%", "99%", "99%"),
    ("Commercial", "Win rate, verified-ROI pitches", "Won ÷ pitched, vs baseline", "baseline", "–", "+5 pts", "+8 pts", "+12 pts"),
    ("Commercial", "Gross margin per campaign", "vs FY26 baseline", "FY26", "–", "+1 pt", "+2 pts", "+3 pts"),
    ("Commercial", "Repeat-brand rate", "Brands with a second campaign in 6 months", "baseline", "–", "–", "+5 pts", "+10 pts"),
    ("Commercial", "Measurement revenue", "Fees for L4/L5 measurement", "₹0", "–", "first fee", "₹25L run-rate", "₹2 Cr run-rate"),
    ("People", "Strategist usefulness score", "Monthly survey, 1–5", "–", "3.5", "3.8", "4.0", "4.2"),
]
s14 = sec("14", "KPIs", "One North Star, inputs that drive it, guardrails around it", table(["Type", "KPI", "Definition", "Baseline", "D30", "D60", "D90", "M12"], [[f"<b>{a}</b>" if a == "North Star" else a, f"<b>{b}</b>" if a == "North Star" else b, c, d, e, f, g, h] for a, b, c, d, e, f, g, h in KPIS], cls="tiny", right=(3, 4, 5, 6, 7)) + """
<div class="cols2"><div><h2>KPI tree</h2>""" + ul([
    "<b>North Star:</b> share of revenue at L4+",
    "↳ <b>Coverage:</b> consented creators, brands sharing outcomes, tracking QA pass rate",
    "↳ <b>Quality:</b> forecast error, engine picks in rosters, strategist usefulness",
    "↳ <b>Commercial outcomes:</b> win rate, repeat rate, margin, measurement revenue, Represent utilisation",
    "↳ <b>Guardrails:</b> disclosure compliance, incidents, creator and strategist satisfaction",
]) + """</div><div><h2>Dashboards and owners</h2>""" + table(["Dashboard", "Owner", "Cadence"], [
    ["North Star & inputs", "Programme lead", "Weekly (WBR)"], ["Model health (MAPE, drift, fairness)", "ML scientist", "Weekly"], ["Live campaigns & alerts", "Analyst", "Daily"],
    ["Commercial (win, repeat, margin)", "Head of Brand Solutions + CFO office", "Monthly"], ["Represent demand & utilisation", "Head of Represent", "Weekly"]], cls="small") + "</div></div>")

# 15 team
TEAM = [
    ("Founder's Office lead (programme owner)", "1.0", "2.0", "Owns plan, cadence, gates, pricing proposals, stakeholder alignment; acts as PM until month 4", "Day 0"),
    ("Data engineer", "1.0", "2.2", "Pipelines from APIs, tracking feeds and history; consent and data store; quality checks", "Week 2"),
    ("ML / data scientist", "1.0", "2.8", "Scoring, forecasting, calibration, learning-to-rank, incrementality analysis, fairness audits", "Week 2"),
    ("Full-stack engineers", "2.0", "3.6", "Internal tool, brand report and dashboard, Represent view, integrations", "Weeks 2–4"),
    ("Measurement & insights analyst", "1.0", "1.1", "Tracking QA, holdout and lift design, ROI reports, benchmarks", "Week 4"),
    ("Data-ops associates", "2.0", "0.9", "Creator consent, credential checks, AI tag QA, data hygiene", "Week 2"),
    ("Product designer", "0.5", "0.7", "Internal tool and brand-facing report UX", "Week 3"),
    ("Compliance counsel (retainer)", "0.2", "0.6", "ASCI, SEBI, IRDAI, DPDP, contract clauses, claim review escalations", "Week 1"),
]
s15 = sec("15", "Team and organisation", "Who is needed, when, and who owns what", """
<div class="org">
  <div class="o1"><b>Executive sponsor</b><span>MD &amp; CEO</span></div>
  <div class="o2"><b>Steering committee (monthly)</b><span>CEO · CFO · Heads of Brand Solutions, Represent, ChtrSocial · Tech lead · Programme owner</span></div>
  <div class="o3"><b>Programme owner</b><span>Founder's Office lead</span></div>
  <div class="o4">
    <div><b>Data &amp; ML</b><span>Data engineer · ML scientist · 2 data-ops</span></div>
    <div><b>Product &amp; engineering</b><span>2 full-stack · designer (0.5)</span></div>
    <div><b>Measurement</b><span>Insights analyst</span></div>
    <div><b>Business champions (seconded)</b><span>2 strategists (30%) · talent manager (20%) · sales lead (20%)</span></div>
    <div><b>Compliance</b><span>Counsel (retainer)</span></div>
  </div>
</div>""" + table(["Role", "FTE", "₹ L / month", "Responsibilities", "Start"], [[f"<b>{a}</b>", b, c, d, e] for a, b, c, d, e in TEAM] + [["<b>Total new cost</b>", "<b>8.7</b>", "<b>13.9</b>", "Contractors or a specialist agency can cover engineering for the first 90 days if hiring lags", ""]], cls="tiny xtiny", right=(1, 2)) + """
<h2>RACI for the critical activities</h2>""" + table(["Activity", "Programme owner", "Strategists", "Represent", "Data & ML", "Analyst", "Legal", "CEO / CFO"], [
    ["Brand DNA", "C", "R", "–", "C", "–", "–", "–"], ["Creator consent & verification", "A", "–", "R", "C", "–", "C", "–"], ["Model and gates", "A", "C", "C", "R", "C", "C", "I"],
    ["Shortlist decisions", "C", "R/A", "C", "I", "–", "–", "–"], ["Tracking QA gate", "A", "C", "–", "C", "R", "–", "–"], ["Verified-ROI report", "C", "C", "–", "C", "R", "–", "I"],
    ["Packaging & pricing", "R", "C", "C", "–", "C", "C", "A"], ["Compliance gates", "A", "C", "C", "C", "–", "R", "I"], ["Budget tranches & gates", "R", "–", "–", "–", "C", "–", "A"]], cls="tiny xtiny") +
    callout("Change management", "<p>The engine is a co-pilot for strategists and talent managers. It removes search and spreadsheet work and leaves judgement with them. Strategists co-design the weights, every override is respected and logged, and incentives move toward verified outcomes rather than volume. No headcount reduction is planned from this programme; the capacity freed goes into more briefs per person during peak season.</p>"))

# 16 budget
s16 = sec("16", "Budget and funding", "What it costs, where the money comes from, what it returns", """
<div class="cols2"><div><h2>First 90 days</h2>""" + table(["Line", "Detail", "₹"], [
    ["People", "₹13.9L a month × 3", "41.7L"], ["Creator-data licences (stop-gap)", "₹2.5L a month", "7.5L"], ["Cloud and storage", "₹1.2L a month", "3.6L"],
    ["AI inference (tagging, safety, sentiment)", "₹1.0L a month", "3.0L"], ["Brand-lift panels and surveys", "~₹2.5L a month", "7.5L"], ["Attribution tooling, BI, security", "₹0.8L a month", "2.4L"],
    ["Pilot credits", "Free measurement for 8 pilot brands", "8.0L"], ["Contingency", "10%", "7.4L"], ["<b>Total</b>", "", "<b>81.1L</b>"]], cls="small", right=(2,)) + """</div><div><h2>Year one, in tranches</h2>""" + table(["Tranche", "Released when", "₹"], [
    ["1 · Pilot", "Day 0", "0.81 Cr"], ["2 · Productise & prove", "Day-90 gate passed", "1.40 Cr"], ["3 · Scale", "Month-6 gate passed", "1.80 Cr"], ["<b>Year one</b>", "", "<b>≈ 4.0 Cr</b>"]], cls="small", right=(2,)) + """
<p><b>Funding source:</b> the IPO allocation for capex in the existing business (₹11.07 Cr), which management has said covers technology and creator intelligence, plus internal accruals. Year-two run cost is about ₹3.2 Cr.</p>
<p class="muted">For scale: year-one cost is about 28% of FY26 EBITDA (₹14.3 Cr). That is why money is released in tranches and why the kill criteria in section 20 exist.</p></div></div>
<h2>Value model (assumptions, annual contribution at maturity)</h2>""" + table(["Driver", "Conservative", "Base", "Aggressive", "Logic"], [
    ["Brand Solutions growth from win rate, repeat and deal size", "+8% → ₹0.7 Cr", "+20% → ₹1.8 Cr", "+35% → ₹3.2 Cr", "On ₹30.5 Cr FY26 base, 30% contribution"],
    ["Represent utilisation", "+5% → ₹0.4 Cr", "+12% → ₹1.0 Cr", "+20% → ₹1.7 Cr", "On ₹33.1 Cr, 25% contribution"],
    ["Measurement fees", "5% of ₹12 Cr → ₹0.4 Cr", "8% of ₹25 Cr → ₹1.4 Cr", "10% of ₹40 Cr → ₹2.8 Cr", "70% contribution"],
    ["Margin from strategist time and fraud avoided", "+1 pt → ₹0.6 Cr", "+2 pts → ₹1.3 Cr", "+3 pts → ₹1.9 Cr", "On ₹63.6 Cr influencer revenue"],
    ["<b>Total per year</b>", "<b>₹2.1 Cr</b>", "<b>₹5.5 Cr</b>", "<b>₹9.6 Cr</b>", "Versus ~₹3.2 Cr year-two run cost"],
    ["Payback (benefits ramp from month 4 to month 15)", "not within 3 years", "~24 months", "~16 months", "Gates decide which case we are in by month 6"],
], cls="tiny") + callout("Build versus buy", "<p><b>Buy</b> commodity creator data (licences) and survey panels at first. <b>Build</b> what is defensible: the scoring and forecasting model trained on Chtrbox outcomes, the verified-ROI pipeline on top of existing tracking, and the internal tool. If an acquisition target with mature creator data appears (management has said it is evaluating tech acquisitions), the licence line is the part it would replace.</p>"))

# 17 management system
s17 = sec("17", "Management system", "How the programme is run, decided and kept honest", table(["Rhythm", "Who", "Inputs", "Decisions"], [
    ["Daily · 15-min stand-up", "Pod", "Yesterday, today, blockers; live-campaign alerts", "Unblock; act on alerts"],
    ["Weekly · Monday business review", "Programme owner, heads of Brand Solutions & Represent, tech lead", "North Star and input KPIs, pick-vs-pick log, risks", "Priorities for the week; escalations"],
    ["Fortnightly · demo and feedback", "Pod + strategist champions", "Working software", "Backlog changes; weight changes"],
    ["Monthly · steering committee", "CEO, CFO, heads of function", "Gate pack: KPIs vs plan, spend vs tranche, risk register", "Go / adjust / stop; tranche release"],
    ["Quarterly · audits", "ML scientist, counsel, external reviewer", "Model card, fairness audit, compliance sample", "Model and policy changes"],
], cls="small") + """
<div class="cols2"><div><h2>Decision rights</h2>""" + ul([
    "<b>Strategists</b> decide final rosters; the engine recommends.",
    "<b>Programme owner</b> decides model weights and gates, within policy set by steering.",
    "<b>Legal counsel</b> can veto any creator or claim on compliance grounds.",
    "<b>CFO</b> releases tranches; <b>CEO</b> approves pricing and external claims about the engine.",
]) + """</div><div><h2>Documents that keep it honest</h2>""" + ul([
    "<b>Decision log:</b> every material decision, the options and why",
    "<b>RAID log:</b> risks, assumptions, issues, dependencies, reviewed weekly",
    "<b>Model card:</b> data, metrics, known limits, last retrain",
    "<b>Override log:</b> every strategist override with a reason code",
    "<b>Gate packs:</b> one page per gate, numbers against targets",
]) + "</div></div>")

# 18 guardrails
s18 = sec("18", "Guardrails", "Set before the first brief, reviewed monthly", table(["Area", "Guardrail", "Basis"], [
    ["Data & privacy", "Creator data only through OAuth consent; purpose-limited; deletable on request; no follower-level personal data; retention limits", "DPDP Act and Rules (notified Nov 2025; core obligations by about May 2027) [20]"],
    ["Platform terms", "No scraping beyond what platform terms allow; use official APIs and licensed data", "Meta and YouTube developer terms"],
    ["Disclosure", "#ad or #collab in the first line or overlay of every paid post; checked within 2 hours of going live", "ASCI influencer guidelines; Consumer Affairs endorsement guidance [21]"],
    ["Health claims", "Technical claims only by qualified creators; no cure or guaranteed-result language", "ASCI Addendum II (Apr 2025); Drugs & Magic Remedies Act [22]"],
    ["Finance", "Only SEBI-registered creators discuss securities or returns; others brand-scripted; IRDAI rules for insurance", "SEBI rules on regulated entities and unregistered finfluencers; ASCI Addendum II [23]"],
    ["Tax", "TDS on creator benefits and fees, GST on services, handled in contracting", "Income-tax 194R / 194J; GST"],
    ["Model", "Human in the loop; explainable scores; quarterly fairness audit; Represent boost capped at +5 and disclosed", "Internal policy"],
    ["Commercial claims", "'Verified' only for L4/L5; forecasts always shown with bands; no guaranteed ROI", "Consumer protection rules on misleading claims"],
    ["Brand safety", "Safety gate; morality and kill clauses; monitoring for controversies during flights", "Contracts"],
    ["Security", "Role-based access, encryption of personal data, audit logs, vendor reviews", "DPDP security safeguards"],
    ["Peak season", "Shadow mode during October–March until accuracy is proven", "~60% of revenue in H2"],
], cls="tiny"))

# 19 pre-flight
PRE = [
    "What tracking and attribution exists today: which brands, which methods, what share of revenue is covered",
    "Brand contracts allow aggregated use of campaign outcomes for model training; if not, add the clause to renewals",
    "Represent contracts updated for data consent and scorecards",
    "Platform API access confirmed (business/creator accounts, permissions, rate limits)",
    "DPDP readiness: notices, consent records, retention schedule, breach process, data map",
    "Baselines measured: brief-to-shortlist time, win rate, margin per campaign, repeat rate",
    "Heads of Brand Solutions and Represent agree the success metrics and the roster-boost policy",
    "Peak-season protection plan agreed: what the engine may and may not change before April",
    "CFO signs off tranches and kill criteria",
    "Security baseline in place before any creator data is ingested",
    "Legal review of the words we use externally: 'verified', 'incremental', 'AI'",
    "Pilot brands selected, with data-sharing agreed in writing",
    "Engineering capacity confirmed: hires or a contractor in place by week 2",
    "A written list of what we will not do in 90 days: no self-serve, no regulated verticals before month 4, no MENA before day 61",
]
s19 = sec("19", "Before we proceed", "Pre-flight checks: awareness before anything ships", '<div class="checks">' + "".join(f'<div><span>{i + 1:02d}</span>{t}</div>' for i, t in enumerate(PRE)) + "</div>")

# 20 risks
RISKS = [
    ("Creators refuse to connect data", "Medium", "High", "Start with Represent (contracted); value exchange through scorecards and faster payments; licensed data fallback", "Consent rate < 40% by day 30", "Head of Represent"),
    ("Brands won't share outcome data", "Medium", "High", "Begin with codes, links and affiliate (L3); aggregated or clean-room sharing; contract clause", "< 2 pilots at L4 by day 45", "Head of Brand Solutions"),
    ("Verified ROI looks worse than past claims", "High", "Medium", "Frame as an upgrade; show claimed, attributed and incremental together; show engine improvement; start with friendly brands", "Pilot brand pushback", "Programme owner"),
    ("Cold start and forecast error", "High", "Medium", "Shadow mode; confidence bands; MAPE gates; human in the loop", "MAPE > 35% at day 45", "ML scientist"),
    ("Strategist resistance", "Medium", "High", "Co-design weights; champions; incentives on outcomes; no-headcount-cut commitment", "Usefulness score < 3.5", "Programme owner"),
    ("Platform API changes", "Medium", "Medium", "Multiple sources; abstraction layer; consented data first", "Deprecation notices", "Data engineer"),
    ("Regulatory change (ASCI, SEBI, DPDP)", "Medium", "Medium", "Counsel on retainer; gates are configuration, not code", "New circulars", "Legal counsel"),
    ("Represent conflict of interest", "Medium", "High", "Boost capped at +5 and shown on the score; quarterly audit; disclosure to brands", "Roster share of plans rises without fit", "Steering committee"),
    ("Peak-season disruption", "Low", "High", "Shadow mode October–March; no delivery changes without strategist sign-off", "Any delivery miss linked to the engine", "Programme owner"),
    ("Hiring delays", "Medium", "Medium", "Contractors or agency for 90 days; scope cut before deadlines slip", "Roles unfilled at week 4", "Programme owner"),
    ("Cost overrun or value not proven", "Medium", "High", "Tranches; kill criteria; monthly gate packs", "Spend > 110% of tranche", "CFO"),
    ("Data breach", "Low", "High", "Minimal personal data, encryption, access control, incident SOP", "Security alerts", "Tech lead"),
    ("Optimising only what is measurable", "Medium", "Medium", "Objective-specific KPIs; brand lift for awareness; LTV for repeat categories", "Awareness briefs judged on clicks", "Programme owner"),
    ("Regional and small creators excluded", "Medium", "Medium", "Within-tier percentiles; language coverage; fairness audit", "Under-selection > 20% for any group", "ML scientist"),
    ("MENA distracts the core", "Medium", "Medium", "Starts day 61, 300-creator pilot, separate success metric", "Core KPIs slip after MENA start", "Steering committee"),
]
CONS = [
    "Verified ROI will often be lower than the numbers brands have been shown before. Some brands prefer flattering numbers, and some will leave.",
    "Measurement costs money. Holdouts and lift studies don't fit every brief; small campaigns will stay at L3–L4.",
    "The data advantage takes time. The first three months are mostly learning, and the engine will be wrong in visible ways.",
    "Optimising outcome per rupee shifts spend from mega creators to mid and micro creators. Revenue per campaign can dip even as results improve, and some creator relationships will feel it.",
    "Performance transparency can strain relationships with creators who score poorly, including roster creators.",
    "The engine depends on platform APIs and creator consent, neither of which Chtrbox controls.",
    "A tool that sits beside strategists only works if they use it. Adoption is the real risk, not the code.",
]
s20 = sec("20", "Risks, warnings and honest cons", "What could go wrong, how we'll know early, what we'll do", table(["Risk", "Likelihood", "Impact", "Mitigation", "Early warning", "Owner"], [list(r) for r in RISKS], cls="tiny xtiny") + "<h2>The honest cons</h2>" + '<div class="cols2 cons">' + ul(CONS[:4]) + ul(CONS[4:]) + "</div>" + "")

# 21 roadmap
s21 = sec("21", "Roadmap: years one and two", "From internal co-pilot to a product brands pay for", callout(
    "Kill and scale criteria", "<p><b>Day 90:</b> continue to tranche 2 if at least two of three hold: engine picks ≥ 50% of final rosters with usefulness ≥ 3.8; views MAPE < 25%; at least one brand renews or expands citing verified ROI. Otherwise stop the build and keep the measurement SOPs, which pay for themselves on their own. "
    "<b>Month 6:</b> scale to tranche 3 if L4+ covers ≥ 60% of revenue, win rate is up ≥ 5 points and at least three brands pay a measurement fee.</p>", "warn") + table(["Horizon", "Product", "Commercial", "Organisation"], [
    ["Months 4–6", "Incrementality at scale; regulated verticals behind gates; read-only dashboards for top 10 clients", "Verified ROI packages sold to 10+ brands", "Pod complete; strategist champions in every team"],
    ["Months 7–12", "Creator scorecards in Represent; agency shortlists; pricing model (fair rate per outcome); MENA graph live", "Measurement fee on ~₹25 Cr of spend; outcome-linked pricing on a share of performance briefs", "Add ML engineer, data engineer, MENA analyst"],
    ["Year 2", "Creator Intelligence subscriptions (brands, agencies); creator–brand graph for brands with no history; seasonal demand forecasts", "Intelligence revenue ≥ ₹2 Cr; data partnerships with marketplaces and quick-commerce", "Product and data as a standing unit with its own P&L"],
    ["Year 2+", "Integrate any acquired creator-tech; expand graph to wider GCC", "Platform revenue growing faster than headcount", "Engine is the default way every brief starts"],
], cls="small") + callout("Where this leaves Chtrbox", "<p>Today Chtrbox sells campaigns, and every campaign needs people. In two years it can sell proof: a standard for what a creator campaign achieved, used across its own campaigns, licensed to agencies and brands, and backed by data no new entrant has. That changes the margin profile and the story the company tells investors.</p>", "accent"))

# 22 interview walkthrough
s22 = sec("22", "Interview walkthrough and likely questions", "Eight minutes, then Q&A", table(["Time", "Screen", "What to show and say"], [
    ["0:00–1:00", "Overview", "The thesis and the four public numbers: revenue up 42.5%, margin down 3.5 points. The engine is how growth stops costing margin."],
    ["1:00–3:00", "Brand Match · Olay", "Brand DNA → gated creators (fake audience, competitor conflicts) → top-ranked creator and why → switch objective to Conversion and watch the ranking change → engine plan vs follower count → efficiency map."],
    ["3:00–3:30", "Brand Match · Groww", "Finance creators without SEBI registration are gated. Compliance is built in, not a checklist."],
    ["3:30–4:15", "Discovery", "Type 'Hindi beauty creators under 25k with ER above 3%' and show it parsed into filters."],
    ["4:15–5:00", "Vertical Lens", "Heatmap of where talent sits; the Beauty playbook and benchmarks by tier."],
    ["5:00–6:30", "Campaigns & ROI · Amazon (live)", "Reported → real people in target; waterfall from attributed to incremental; holdout; alerts and actions."],
    ["6:30–8:00", "How it works · Rollout plan", "76 data points, the formula, the ROI ladder; then 30/60/90, the pod, ₹81L, guardrails and kill criteria."],
], cls="small") + table(["Likely question", "Answer in one breath"], [
    ["How is this different from Qoruz, Kofluence, Modash or HypeAuditor?", "Those show creator data. This connects creator data to Chtrbox's campaign outcomes and live tracking, so it can forecast and verify results, not just describe audiences."],
    ["Where does the data come from?", "Creator OAuth for first-party audience data (Represent first), Chtrbox's campaign history and tracking, brand outcome data under contract, and licensed data to fill gaps."],
    ["What if creators don't consent?", "Represent creators are contracted; others get scorecards and faster briefs in return. Licensed data covers the rest at lower confidence, and the score says so."],
    ["Doesn't the roster boost bias it?", "It is capped at 5 points, shown on every score and disclosed to brands. Roster creators win on fit."],
    ["When will we see results?", "A ranked list on day 15, the first verified-ROI report by day 45, half of campaigns at L4+ by day 90."],
    ["What does it cost, and what if it doesn't work?", "₹81L for 90 days. Money is released in tranches; if the day-90 gate fails we stop building and keep the measurement SOPs."],
    ["What do you need from us?", "Data access, two strategist champions, a talent manager, three pilot brands and a weekly hour from the heads of Brand Solutions and Represent."],
], cls="small") + "<h2>Objections brands will raise</h2>" +  table(["Objection", "Answer"], [
    ["'Our numbers will look worse.'", "They will look honest. We show claimed, attributed and incremental side by side, and the engine raises the incremental figure. Brands that fund the next campaign trust the honest number."],
    ["'We already use a creator tool.'", "Tools show creator data. They don't connect it to your orders and a holdout. That needs campaign execution and tracking, which is what we run."],
    ["'We can't share sales data.'", "Start at L3 with codes and links; move to L4 with aggregated or clean-room sharing. Nothing about individual customers is needed."],
    ["'Is this just a black box?'", "Every score shows its seven parts and the reason. Strategists can override; every override is logged."],
], cls="tiny xtiny"))

# appendix
SRC = [
    ("1", "Inc42, Chtrbox financials (FY24 ₹55.4 Cr, FY25 ₹59.4 Cr; estimates)", "https://inc42.com/company/chtrbox/financials/"),
    ("2", "Social Samosa, Chtrbox reports 33% revenue growth in H1 FY26 following IPO (IPO ₹42.86 Cr, 52× subscribed)", "https://www.socialsamosa.com/industry-updates/chtrbox-reports-33-revenue-growth-10597998"),
    ("3", "Storyboard18, Chtrbox H2 FY26 revenue jumps 50% to ₹48.23 Cr, profit declines 12%", "https://www.storyboard18.com/brand-marketing/chtrbox-h2-fy26-revenue-jumps-50-to-rs-48-23-crore-profit-declines-12-99692.htm"),
    ("4", "Whalesbook, Chatterbox Technologies revenue ₹84.22 Cr, margins compress", "https://www.whalesbook.com/corporate-news/English/media-and-entertainment/Chatterbox-Technologies-Sees-Revenue-Surge-to-indian-rupee8422-Cr-But-Margins-Compress/6a3ff8497465030c38bb31f8"),
    ("5", "Multibagg, Chatterbox Technologies FY26: growth, margin pressure and a shifting mix", "https://www.multibagg.ai/market-pulse/articles/chtrbox-fy26-96153"),
    ("6", "Groww, Chatterbox Technologies IPO (client concentration, RHP summary)", "https://groww.in/ipo/chatterbox-technologies-ipo"),
    ("7", "IPOHub, Chatterbox Technologies IPO objects of the issue", "https://ipohub.in/chatterbox-technologies-ipo/"),
    ("8", "Storyboard18, Chatterbox Technologies IPO DRHP coverage (Represent revenue, seasonality, geography)", "https://www.storyboard18.com/advertising/chatterbox-technologies-ipo-influencer-marketing-agency-spends-rs-12-28-lakh-revenue-surges-to-rs-24-2-lakh-in-fy24-81787.htm"),
    ("9", "YourStory, Chtrbox aims to become the engine behind India's creator economy (May 2026)", "https://yourstory.com/2026/05/chtrbox-india-influencer-marketing-creator-economy"),
    ("10", "PR Newswire, Chtrbox establishes Dubai as first global market (Jan 2026)", "https://www.prnewswire.com/news-releases/chtrbox-announces-international-expansion-establishing-dubai-as-its-first-global-market-and-middle-east-hub-302658437.html"),
    ("11", "Buzzincontent, Chatterbox eyes acquisitions to scale creator tech (Jun 2026)", "https://www.buzzincontent.com/news/chatterbox-eyes-acquisitions-to-scale-creator-tech-international-expansion-11894829"),
    ("12", "Social Samosa, interview with Raj Mishra on verified ROI and creator intelligence", "https://www.socialsamosa.com/interviews/creator-economy-far-from-saturation-chatterbox-raj-mishra-10897446"),
    ("13", "Storyboard18, agencies driving India's influencer boom (client names)", "https://www.storyboard18.com/agency-news/monk-e-to-chtrbox-the-agencies-driving-indias-influencer-marketing-boom-89664.htm"),
    ("14", "PR Newswire, Chtrbox named best influencer marketing agency (client names)", "https://www.prnewswire.com/news-releases/chtrbox-awarded-best-influencer-marketing-agency-of-the-year-by-entrepreneur-india-301994469.html"),
    ("15", "Qoruz agency profile (P&G, Amazon, HP)", "https://qoruz.com/agencies/profile/chtrbox"),
    ("16", "Chtrbox blog, Livon campus case study (2017)", "https://blog.chtrbox.com/salon-nahi-livon-case-study/"),
    ("17", "Campaign India, QYOU Media acquires Chtrbox (2021)", "https://campaignindia.in/article/qyou-media-acquires-chtrbox/470055"),
    ("18", "WION, India's influencer sector to grow 25% in 2025 (Goat Agency / Kantar)", "https://www.wionews.com/business-economy/india-influencer-sector-to-grow-25-in-2025-here-are-the-details-1749707845196/amp"),
    ("19", "Tribune India, Kofluence report on the creator economy's institutional age", "https://www.tribuneindia.com/news/business/the-era-of-informal-influence-is-over-indias-creator-economy-is-entering-its-institutional-age/"),
    ("20", "Deccan Herald, Centre notifies DPDP Rules with 12–18 month phased implementation", "https://www.deccanherald.com/amp/story/india%2Fcentre-notifies-dpdp-rules-implementation-planned-in-phases-spread-over-12-18-months-3798465"),
    ("21", "ASCI, social media and influencer disclosure guidelines", "https://www.ascionline.in/social/guidelines/"),
    ("22", "Legal 500 (Khaitan & Co.), ASCI update: qualifications for technical health, nutrition and finance claims", "https://www.legal500.com/intelligence/india/media-telecoms-it-entertainment/asci-update-to-influencer-advertising-guidelines-qualification-mandatory-for-making-claims-related-to-technical-aspects-of-health-nutrition-and-finance"),
    ("23", "Angel One, ASCI eases rules for finfluencers but SEBI regulations still apply", "https://www.angelone.in/news/asci-eases-rules-for-financial-and-health-influencers-but-sebi-regulations-still-apply"),
    ("24", "Dexfluence, engagement-rate benchmarks for Indian creators by tier (2026)", "https://www.dexfluence.com/blog/engagement-rate-benchmarks-india"),
    ("25", "Qolab, types of influencers with India numbers (rates by tier)", "https://qolab.in/blog/types-of-influencers-nano-to-mega-india"),
    ("26", "Indiibot, influencer marketing in India: micro vs macro cost ranges", "https://indiibot.com/blog-influencer-india.html"),
]
ASSUME = [
    "Simulated platform: 420 synthetic creators; tier engagement medians scaled to India 2026 benchmarks (nano 4.9%, micro 2.8%, mid 1.4%, macro 0.9%, mega 0.4%) [24]; reel rates scaled to published ranges (micro ₹5K–50K, mid ₹50K–2L, macro ₹2–5L) [25][26].",
    "Larger accounts carry more fake or inactive followers in the sample (mean real share 86% nano to 75% mega).",
    "Forecast assist factor 2.8 (codes, affiliate and search-assisted orders per clicked order) and brand-specific conversion rates are modelling assumptions, to be calibrated in days 31–45.",
    "Campaign incrementality shares (45–66%) and return rates (2–17%) are assumptions typical of category, replaced by holdout results in practice.",
    "Segment revenue is derived as FY26 revenue × reported segment shares. Sources differ slightly on FY25 margins (20.46% vs 20.57%).",
    "Salaries are Mumbai market estimates for 2026. Budget, value model and payback are my assumptions, to be validated with the CFO.",
    "Brand names are publicly reported Chtrbox clients [13][14][15][16] or labelled prospects. No real campaign data for them is used or implied.",
]
GLOSS = [("ER", "Engagement rate: interactions ÷ followers"), ("CTR", "Click-through rate: link clicks ÷ views"), ("TG", "Target group defined in the Brand DNA"),
         ("MAPE", "Mean absolute percentage error of forecasts"), ("iROAS", "Incremental revenue ÷ spend, using a holdout"), ("EMV", "Earned media value: a rate-card valuation of views and likes"),
         ("L0–L5", "Levels on the verified-ROI ladder"), ("Holdout", "Matched cities or users not exposed, used as the control"), ("Brand lift", "Survey difference between exposed and control groups"),
         ("OAuth", "Creator-authorised connection to platform insights"), ("Represent", "Chtrbox's exclusive talent-management division"), ("WBR", "Weekly business review")]
sA = sec("A", "Appendix", "Sources, assumptions, glossary", "<h2>Sources</h2><ol class='src'>" + "".join(f"<li value='{a}'>{esc(b)}<br><span class='mono'>{esc(c)}</span></li>" for a, b, c in SRC) + "</ol>")
sA2 = '<section class="brk"><h2>Assumptions and method</h2>' + ul(ASSUME) + "<h2>Glossary</h2>" + table(["Term", "Meaning"], [[f"<b>{a}</b>", b] for a, b in GLOSS], cls="small") + callout(
    "About the prototype", "<p>Open <span class='mono'>Creator-Intelligence-Engine.html</span> in any browser; it works offline. Keys 1–7 switch views, / searches, Esc closes a creator profile. The rebuild scripts are in <span class='mono'>source/</span>.</p>") + "</section>"

CSS = open(__file__.replace("build_pdf.py", "plan.css")).read()
doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Creator Intelligence Engine · GTM and Execution Plan</title><style>{CSS}</style></head><body>
{cover}{toc}{s01}{s02}{s03}{s04}{s04b}{s05}{s06}{s07}{s08}{s09}{s09b}{s09c}{s10}{s11}{s12}{s13}{s14}{s15}{s16}{s17}{s18}{s19}{s20}{s21}{s22}{sA}{sA2}
</body></html>"""
open(OUT, "w").write(doc)
print("wrote", OUT, len(doc) // 1024, "KB")
