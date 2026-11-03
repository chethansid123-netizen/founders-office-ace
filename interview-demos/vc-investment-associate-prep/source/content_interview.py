# Interview, process and template content. Illustrative; adapt answers to your own story.

# ---------- How VC works ----------
PLAYERS = [
    ("LP (Limited Partner)", "Gives money to the fund. Passive.", "Family offices, HNIs, corporates, banks, insurers, SIDBI Fund of Funds, pension & sovereign funds, endowments", "Wants 3x+ net in ~10 years and DPI as early as possible."),
    ("GP (General Partner) / Fund manager", "Runs the fund: raises money, picks startups, manages portfolio, delivers exits.", "Partners, principals, VPs, associates, analysts", "Earns management fee (2%) + carried interest (20% of profits)."),
    ("Sponsor / Investment Manager (India)", "SEBI-registered entity behind an AIF; must keep 'skin in the game'.", "For Cat I/II AIFs: at least 2.5% of corpus or ₹5 cr, whichever is lower", "Aligns manager with LPs."),
    ("Investment Associate", "Engine room of the fund: sourcing, screening, research, financial analysis, diligence, IC memos, portfolio support.", "Reports to partners / principal / CEO", "Measured on deal flow quality, analysis quality, speed and judgement."),
    ("Portfolio company (startup)", "Receives money, issues shares (CCPS) to the fund, uses it to grow.", "Founders, management", "Wants capital + help: hiring, customers, next round, strategy."),
    ("Co-investors", "Other funds or angels in the same round.", "Lead + followers", "Share risk and add networks."),
    ("Service providers", "Lawyers, valuers, auditors, fund administrators, trustees.", "Law firms, registered valuers, CA firms", "Make the deal legal, compliant and auditable."),
]

STAGES = [
    ("Pre-seed", "Idea to first product; team + insight", "₹1–5 cr ($0.1–0.6M)", "₹8–30 cr", "Founder quality, insight, early prototype", "Angels, accelerators, pre-seed funds, grants"),
    ("Seed", "Early product, first customers / revenue", "₹4–25 cr ($0.5–3M)", "₹25–120 cr", "Early PMF signals, retention, founder speed", "Seed funds, angel networks, micro-VCs"),
    ("Pre-Series A", "Product works; scaling GTM", "₹15–40 cr ($2–5M)", "₹80–250 cr", "Repeatable growth, unit economics", "Seed + early VCs"),
    ("Series A", "Product–market fit proven; scale the engine", "₹40–130 cr ($5–15M)", "₹200–700 cr", "PMF, 2–3x growth, clear unit economics, strong team", "Early-stage VCs"),
    ("Series B", "Scale across markets / categories", "₹130–350 cr ($15–40M)", "₹700–2,500 cr", "Efficient scaling, leadership team, path to profit", "VCs, growth funds"),
    ("Series C+ / Growth", "Market leadership, new lines, profitability", "₹350 cr+ ($40M+)", "₹2,500 cr+", "Profitability, market share, IPO readiness", "Growth funds, PE, sovereigns"),
    ("Pre-IPO / IPO", "Listing on NSE/BSE (mainboard or SME)", "Varies", "Public market valuation", "Governance, profitability, audited track record", "Public market investors, mutual funds"),
]

FUND_LIFECYCLE = [
    ("Year 0", "Fundraising", "GP pitches LPs, signs commitments; first close and final close (usually within 12–24 months)."),
    ("Years 1–4/5", "Investment period", "New investments made; capital is drawn down from LPs as needed (capital calls)."),
    ("Years 3–8", "Follow-on & value creation", "Reserves invested in winners; board work; help with hiring, customers, next rounds."),
    ("Years 5–10", "Harvest / exits", "IPOs, strategic sales, secondary sales; cash distributed to LPs."),
    ("Years 10–12", "Extensions & wind-down", "1–2 year extensions to exit the remaining holdings; fund closes."),
]

EXITS = [
    ("IPO", "Company lists on a stock exchange; fund sells after lock-in.", "Swiggy, Zomato (Eternal), Nykaa, Honasa, Ola Electric, Lenskart"),
    ("Strategic acquisition (M&A)", "A bigger company buys the startup.", "Flipkart bought by Walmart (2018); Minimalist by HUL (2025)"),
    ("Secondary sale", "Fund sells its shares to another investor before an IPO.", "Common in Series C+ rounds"),
    ("Buyback", "Company buys back shares from investors.", "Used by profitable companies"),
    ("Write-off", "Company shuts down; shares are worth zero.", "Most early-stage outcomes"),
]

# ---------- Likely interview flow ----------
INTERVIEW_FLOW = [
    ("0–5 min", "Warm-up & 'tell me about yourself'", "Your 90-second story: what you've done → what you learned about businesses → why investing now → why this firm.", "Practise out loud 3 times tonight. End with 'that's why I'm excited about this role'."),
    ("5–15 min", "Why VC / why investment associate / why us", "Motivation, understanding of the role, research on the firm", "Use tab 23: their thesis, their portfolio, what a new arm needs (deal flow, thesis-building, structured diligence)."),
    ("15–30 min", "Thinking like an investor", "Pitch a startup you like; a sector you'd back; how you'd evaluate a founder", "Use the pitch structure in tab 19 (Q #9). Have one consumer, one deep tech, one healthcare example ready."),
    ("30–40 min", "Numbers check", "Can you read metrics: ARR, CAC, LTV, burn, dilution, valuation, IRR?", "Revise tab 03 Formula Lab and the 15 metric questions in tab 19."),
    ("40–50 min", "Mini case / curveball", "'Here's a startup with these numbers — would you invest?'", "Use the 6-step case framework in tab 20; always end with a clear yes/no + what you'd need to believe."),
    ("50–60 min", "Your questions", "Curiosity, seriousness, fit", "Ask 3–4 questions from tab 23. Ask about the thesis, decision process and what success looks like in 6 months."),
]

STUDY_PLAN = [
    ("Hour 1", "02 Glossary (all 'Revenue', 'Customers', 'Profitability', 'Returns' rows) + 03 Formula Lab", "Change the yellow inputs and watch outputs move. Say each formula out loud."),
    ("Hour 2", "04 Consumer, 05 Deep Tech, 06 Healthcare examples", "Be able to explain each example in 60 seconds."),
    ("Hour 3", "07 Sector Playbook + 08 Founder Evaluation + 09 Manufacturing", "Pick 3 sectors you'll talk about confidently; know their 3 key metrics."),
    ("Hour 4", "10 Valuation, 11 Cap Table, 12 Waterfall, 13 Term Sheet, 14 Fund Economics", "Practise: pre/post money, dilution, liquidation preference, MOIC vs IRR, fund returner."),
    ("Hour 5", "19 Interview Q&A + 20 Mini Cases", "Answer 15 questions aloud; time yourself (90 seconds each)."),
    ("Hour 6", "23 Firm Research & Your Questions", "Research the firm, its portfolio and Chandru on LinkedIn/website/news; fill the yellow cells; pick 4 questions to ask."),
    ("Morning", "Revise 'Night-before cheat sheet' at the bottom of tab 00", "Sleep well; carry a notebook and pen; reach 15 minutes early."),
]

CHEAT_SHEET = [
    "ARR = MRR × 12. Run-rate ≠ ARR unless revenue is recurring.",
    "LTV = ARPU × Gross margin ÷ Churn. LTV:CAC > 3x. CAC payback < 12–18 months.",
    "NRR > 100% means existing customers alone grow revenue. GRR shows pure stickiness.",
    "Burn multiple = Net burn ÷ Net new ARR. Under 1.5x is good.",
    "Runway = Cash ÷ Net burn. Raise with 18–24 months left.",
    "Post-money = Pre-money + Investment. Ownership = Investment ÷ Post-money.",
    "Dilution: New % = Old % × (1 − new investor %).",
    "MOIC = Value back ÷ Money in. IRR adds time: 3x in 3 years ≈ 44%; 3x in 7 years ≈ 17%.",
    "Fund returner: Exit value needed = Fund size ÷ Exit ownership.",
    "1x non-participating preference: investor takes the higher of money back or its % of the exit.",
    "Consumer: GM → CM1 → CM2 → CM3. CM2 35%+, repeat 30%+, check channel economics.",
    "Deep tech: TRL, IP ownership, paid pilots → orders, BOM curve, capital needed to breakeven.",
    "Healthcare: clinical evidence, regulatory path, who pays, distribution to doctors, rNPV.",
    "Manufacturing: utilisation, EBITDA margin, ROCE, asset turnover, customer concentration, order book.",
    "Founder: founder–market fit, speed of learning, clarity, integrity, ability to hire and sell.",
    "Always end an investment view with: 'I would invest IF … ; the key risk is … ; I'd check it by …'.",
]

# ---------- Interview Q&A ----------
# (category, question, what he is testing, how to structure the answer, sample answer / key points)
QA = [
    # A. Opening & motivation
    ("A. Opening", "Tell me about yourself.", "Communication, self-awareness, relevance", "Present → Past → Why investing → Why here (90 seconds).", "'I've spent my career close to founders and operations — building MIS, dashboards and operating plans that showed me how businesses really make or lose money. That made me curious about the other side of the table: which businesses deserve capital and why. I want to combine that operator lens with investing discipline, and a new VC arm is the ideal place because I can help build the thesis, deal flow and diligence process from day one.' Replace with your real roles and one concrete achievement with a number."),
    ("A. Opening", "Why venture capital?", "Genuine motivation vs glamour", "Love for founders + love for analysing businesses + long-term impact.", "1) I enjoy meeting founders and understanding many businesses at once. 2) I like making decisions under uncertainty with structured analysis. 3) VC backs the companies that create jobs and new categories in India. Give one example of a startup you followed closely and what you learned."),
    ("A. Opening", "Why an Investment Associate role and not consulting / banking / operations?", "Understanding of the role", "Show you know what associates actually do.", "An associate sources deals, screens them, builds the financial and market analysis, does diligence, writes IC memos and supports portfolio companies. I want breadth across sectors, judgement-building and direct founder exposure — consulting gives analysis without ownership; operations gives depth in one company. VC gives both breadth and a real decision."),
    ("A. Opening", "Why our firm? Why this new arm?", "Research and fit", "Thesis → portfolio → stage → why you add value to a new arm.", "Mention (after research tonight): their focus sectors, 1–2 portfolio companies and why you like them, their cheque size/stage, and that a new arm needs someone who can build pipelines, trackers, frameworks and memos fast — which is exactly what you have done in founder's-office style roles."),
    ("A. Opening", "What do you know about us?", "Homework", "3 facts + 1 opinion + 1 question.", "Fill tab 23 tonight: founding story, thesis, portfolio, recent news. Then: 'What I find interesting is … ; I'd love to understand how the new arm differs from the existing business.'"),
    ("A. Opening", "Where do you see yourself in 5 years?", "Commitment, ambition", "Grow inside investing.", "'Growing into a principal role — owning a sector thesis, leading deals and sitting on boards — while helping build this new arm into a respected fund.'"),
    ("A. Opening", "What is your edge as an investor?", "Self-awareness", "One real edge + proof.", "Operator lens: you can read MIS, find the metric that matters, and spot when numbers don't add up. Proof: a dashboard/MIS you built and an insight it produced."),
    ("A. Opening", "What is your biggest weakness?", "Honesty and growth", "Real weakness + what you're doing about it.", "'I don't yet have deep experience in legal structuring of deals like SHA clauses. I've been studying term sheets and cap tables, and I would learn fastest by sitting in on live deals.'"),

    # B. Thinking like an investor
    ("B. Investor thinking", "Pitch me a startup you would invest in.", "Structured thinking, conviction", "Problem → Solution → Market (TAM) → Traction → Business model & unit economics → Team → Moat → Risks → Why now → Valuation/return view.", "Pick a real Indian startup you know well (consumer, deep tech or healthcare). Speak 2 minutes. End: 'I would invest at up to ₹X post-money because at ₹Y cr exit our Z% stake returns N× the cheque; biggest risk is … which I'd check by …'."),
    ("B. Investor thinking", "A startup you would NOT invest in — and why.", "Critical thinking", "Respectful, evidence-based.", "Use metrics: e.g., a brand growing only through discounts with negative CM2, or a deep tech company with only free pilots and no path to production. Show what would change your mind."),
    ("B. Investor thinking", "Which sector in India excites you most right now?", "Conviction + understanding of themes", "Theme → why now → 2–3 sub-segments → 2 companies → key risk.", "Example: healthcare + AI: rising insurance penetration, ABDM digital rails, shortage of radiologists → AI diagnostics and specialty clinics. Risks: payer clarity and regulation. Or consumer: premiumisation + quick commerce lets new brands reach metros in months."),
    ("B. Investor thinking", "How would you build an investment thesis for a sector?", "Process", "Market map → value chain → where profit pools are → why now → what winning looks like → target companies.", "Steps: 1) Size the market and growth. 2) Map the value chain and margins. 3) Identify change (policy, tech, behaviour). 4) Define criteria for a winner. 5) Build a list of 30–50 startups (Tracxn/Inc42). 6) Meet the top 10 and refine."),
    ("B. Investor thinking", "What makes a great founder?", "Judgement about people", "3–4 traits + how you'd test each.", "Founder–market fit, speed of learning, clarity of thought, resilience, ability to sell (customers, talent, investors), integrity. Test: ask how their thinking changed in the last 6 months; ask for a hard decision they made; do reference checks with ex-colleagues and customers."),
    ("B. Investor thinking", "How would you source deals for a new fund?", "Hustle, network", "Inbound + outbound + network + ecosystem.", "Outbound: theme-driven lists from Tracxn/LinkedIn, cold outreach to founders. Network: accelerators (IIT/IISc incubators, Antler), angel networks, other VCs (co-investing), lawyers/CAs. Inbound: content (LinkedIn posts on your thesis), founder referrals from portfolio. Track everything in a CRM with weekly pipeline review."),
    ("B. Investor thinking", "How can a VC add value beyond money?", "Understanding of portfolio support", "Hiring, customers, fundraising, strategy, governance.", "Hiring senior talent, customer introductions, preparing for next round, MIS and board discipline, pricing and unit economics reviews, regulatory and compliance help, exit planning."),
    ("B. Investor thinking", "What is the single most important metric for a startup?", "Nuance", "It depends on the business model — give 3 examples.", "SaaS: NRR and burn multiple. Consumer: repeat rate and CM2. Marketplace: take rate and liquidity. Deep tech: pilot-to-order conversion. Healthcare: utilisation and payer economics. Early stage overall: retention — it shows real value."),
    ("B. Investor thinking", "Tell me about a famous VC mistake or a deal you think was mispriced.", "Market awareness", "Facts → what went wrong → lesson.", "E.g., the Byju's collapse: governance, aggressive revenue recognition and debt-funded acquisitions; lesson: diligence governance and cash, not just growth. Or 2021 valuations reset in 2022–23: lesson about entry price discipline."),

    # C. Metrics & finance
    ("C. Metrics & finance", "What's the difference between revenue, ARR and run-rate?", "Basics", "Define each + when founders misuse them.", "Revenue = recognised in the period. ARR = recurring subscription revenue × 12 (SaaS only). Run-rate = latest month × 12 for any business. A D2C brand saying '₹50 cr ARR' means run-rate; ask for trailing-12-month revenue and seasonality."),
    ("C. Metrics & finance", "A SaaS company has ₹50 L MRR, 3% monthly churn, 75% gross margin, CAC ₹1.5 L and ARPA ₹25,000. Is it good?", "Calculation under pressure", "LTV, LTV:CAC, payback.", "LTV = 25,000 × 75% ÷ 3% = ₹6.25 L. LTV:CAC = 4.2x (good). Payback = 1.5 L ÷ (25,000 × 75%) = 8 months (very good). Ask about NRR and whether churn is improving by cohort. See tab 03."),
    ("C. Metrics & finance", "What is NRR and why does >100% matter?", "SaaS depth", "Formula + implication.", "NRR = (Start MRR + Expansion − Churn − Contraction) ÷ Start MRR. Above 100% the existing base grows by itself, so every new customer is additive. 120%+ is elite and earns premium valuations."),
    ("C. Metrics & finance", "Explain CM1, CM2, CM3 for a D2C brand.", "Consumer depth", "Layer by layer with an example.", "CM1 = net revenue − COGS. CM2 = CM1 − logistics, packaging, payment gateway, marketplace fees. CM3 = CM2 − performance marketing. Example in tab 04: ₹405 net revenue → CM1 ₹275 → CM2 ₹169 → CM3 ₹39 per order."),
    ("C. Metrics & finance", "What is burn multiple and what's good?", "Capital efficiency", "Formula + benchmark.", "Net burn ÷ net new ARR. <1x amazing, 1–1.5x good, 2x+ worrying. ₹10 cr burn to add ₹8 cr ARR = 1.25x."),
    ("C. Metrics & finance", "What is the Rule of 40?", "SaaS benchmark", "Formula + example.", "Revenue growth % + EBITDA (or FCF) margin % ≥ 40. 60% growth with −15% margin = 45: passes."),
    ("C. Metrics & finance", "Gross margin vs contribution margin vs EBITDA?", "P&L layers", "Explain the layers top-down.", "Gross margin removes only COGS. Contribution removes all variable costs (logistics, fees, marketing). EBITDA also removes fixed costs (salaries, rent, tech). A company can have great gross margin and still terrible contribution if delivery and CAC are high."),
    ("C. Metrics & finance", "Why can a profitable company run out of cash?", "Cash vs profit", "Working capital story.", "Profit ignores cash timing. Rising inventory and receivables (e.g., modern trade paying in 90 days) absorb cash. Check the cash conversion cycle: DIO + DSO − DPO."),
    ("C. Metrics & finance", "GMV is ₹100 cr and take rate 12%. What is revenue?", "Marketplace basics", "Revenue = GMV × take rate.", "₹12 cr. Then ask about discounts funded by the platform (which reduce net revenue) and returns."),
    ("C. Metrics & finance", "MOIC vs IRR — which matters more?", "Returns understanding", "Both; explain time.", "MOIC = how many times; IRR = how fast. 3x in 3 years ≈ 44% IRR; 3x in 8 years ≈ 15%. LPs care about both, plus DPI (actual cash back)."),
    ("C. Metrics & finance", "TVPI vs DPI?", "Fund metrics", "Define + why LPs prefer DPI.", "TVPI = (distributions + remaining value) ÷ paid-in. DPI = distributions ÷ paid-in. DPI is real cash; TVPI includes paper marks that can fall."),
    ("C. Metrics & finance", "How do you value a pre-revenue startup?", "Early-stage valuation", "VC method + scorecard/Berkus + market comparables of recent rounds.", "No DCF. Use: 1) VC method — exit value × retention ÷ target MOIC; 2) recent comparable seed rounds; 3) Scorecard/Berkus for qualitative factors; 4) what ownership the fund needs (e.g., 12–15%) and how much capital the company needs to reach the next milestone. See tab 10."),
    ("C. Metrics & finance", "Pre-money ₹40 cr, investment ₹10 cr. Post-money and ownership?", "Basic cap table", "Post = pre + investment; ownership = investment ÷ post.", "Post = ₹50 cr; investor owns 20%; existing holders diluted by 20% (a 60% founder goes to 48%)."),
    ("C. Metrics & finance", "Founders own 70%. Seed takes 20%, Series A 25%. What do founders own after A?", "Dilution chain", "Multiply (1 − round %).", "70% × 0.8 × 0.75 = 42% (before any ESOP pool). With a 10% pool created at seed: 70% × 0.7 × 0.75 = 36.75%. See tab 11."),
    ("C. Metrics & finance", "What is a fund returner? Calculate for a ₹200 cr fund.", "Portfolio construction", "Fund size ÷ exit ownership.", "If you own 8% at exit, the company must be worth ₹200 cr ÷ 8% = ₹2,500 cr (~$285M). That's why VCs ask 'can this be a ₹2,500 cr+ company?'."),
    ("C. Metrics & finance", "What is EBITDA and why do people adjust it?", "Finance literacy", "Define + scepticism.", "Operating profit before D&A, interest, tax. Adjusted EBITDA removes ESOP cost and one-offs; be sceptical if 'one-offs' recur every year."),

    # D. Sector deep-dives
    ("D. Sectors", "How do you evaluate a D2C / consumer brand?", "Consumer framework", "Category → brand → cohorts → unit economics → channels → working capital → founder.", "Is the category big and growing? Why will consumers choose this brand? Cohort repeat 30%+? CM2 35%+ by channel? Organic share? Offline readiness and secondary sales? Inventory and receivable days? Use tab 04."),
    ("D. Sectors", "Is D2C dead in India?", "Nuanced view", "No — the model evolved.", "Pure online, ad-led D2C struggles with rising CAC. Winners go omnichannel (quick commerce, modern trade, general trade, exports), build brand-led organic demand and run tight CM2. Examples: Mamaearth (listed), Minimalist (acquired by HUL), The Whole Truth."),
    ("D. Sectors", "How has quick commerce changed consumer brands?", "Current trends", "Opportunity + cost.", "Opportunity: launch in metros fast, high-visibility discovery, impulse buys. Cost: platform margins + ads, dark-store listing fees, and data owned by the platform. Brands need strong CM2 after QC margins and must not depend on one platform."),
    ("D. Sectors", "How do you evaluate a deep tech startup with no revenue?", "Deep tech framework", "Tech → IP → team → customer pull → TRL roadmap → unit economics at scale → capital needed → exits.", "Check TRL today and the milestone this round buys; benchmark vs alternatives; IP ownership; paid pilots and LOIs; BOM curve; total capital to breakeven; certification path; who would acquire. Value with milestone-based / risk-adjusted VC method (tab 05)."),
    ("D. Sectors", "How do you de-risk a deep tech investment?", "Risk thinking", "Tranching + grants + milestones.", "Milestone-linked tranches; use grants (iDEX, BIRAC, DST) for early R&D; co-invest with specialist deep tech funds; insist on paid pilots; strong technical advisor diligence; plan venture debt only after revenue."),
    ("D. Sectors", "What are exit routes for Indian deep tech?", "Exit realism", "Strategic + IPO + global.", "Strategic M&A by Indian conglomerates (Tata, Reliance, L&T, Adani), global tech/defence firms; IPO (ideaForge listed in 2023); secondary sales to later-stage funds."),
    ("D. Sectors", "How do you evaluate a healthcare startup?", "Healthcare framework", "Clinical value → regulatory path → payer → distribution → unit economics → team → data compliance.", "Who pays and why? Evidence of outcomes? Approval status (CDSCO class, FDA)? How it reaches doctors? Centre/test/device economics? Clinical + business team? Use tab 06."),
    ("D. Sectors", "Why does healthcare take longer to scale?", "Domain understanding", "Trust, regulation, payer, behaviour.", "Doctors change habits slowly, approvals take time, insurers/government set prices, and clinical liability raises the bar. That's why capital efficiency and patience matter, and rNPV is used for valuation."),
    ("D. Sectors", "How would you evaluate a manufacturing startup (China+1)?", "Industrial lens", "Order book → customers → plant economics → ROCE → working capital → founder.", "Customer concentration and quality of OEM customers; certifications (ISO 9001, IATF 16949 auto, AS9100 aerospace); capacity utilisation; EBITDA margin; asset turnover; ROCE; working capital days; PLI dependence; founder's shop-floor depth. See tab 09."),
    ("D. Sectors", "Is a capex-heavy business right for VC?", "Fit of capital", "Depends on returns and capital stack.", "VC equity should fund what is risky and scalable (tech, first plant proof); debt and project finance should fund repeatable capex once utilisation is proven. Check ROCE >20% and asset turnover >1.5x."),
    ("D. Sectors", "How do you evaluate an AI startup? Isn't it just a wrapper?", "Current thinking", "Moat test.", "Moat comes from proprietary data, deep workflow integration, distribution, and switching costs — not the model. Check gross margin after inference costs, retention, and what happens if foundation models get 10x cheaper (good AI apps get better margins; wrappers get commoditised)."),
    ("D. Sectors", "Give me a one-line take on 5 sectors.", "Breadth", "Use the playbook.", "Pick from tab 07: SaaS (rent software, judge NRR), D2C (brand margin, judge repeat & CM2), Lending (spread business, judge NPAs), Deep tech (IP-led, judge TRL & pilots), Healthcare (trust-led, judge evidence & payer)."),

    # E. Founder evaluation
    ("E. Founders", "How do you assess a founder in a 30-minute meeting?", "People judgement", "Clarity, depth, honesty, speed, ambition.", "Listen for: crisp problem statement, deep customer insight, numbers known by heart, honest answer to 'what's not working', ambition backed by a plan. Ask one deep follow-up on every claim. Then reference-check."),
    ("E. Founders", "Would you back a solo founder?", "Nuance", "Yes, with conditions.", "Yes if the founder has shown they can hire strong leaders and cover gaps; risk is bandwidth and key-person dependency. Check the second line of leadership."),
    ("E. Founders", "First-time founder or repeat founder?", "Bias awareness", "Both; what each brings.", "Repeat founders bring networks and speed; first-time founders often bring fresh insight and hunger. Judge founder–market fit and learning speed, not CV."),
    ("E. Founders", "A founder says they have no competition. Your reaction?", "Market awareness", "Red flag; explain why.", "There is always competition — including the status quo (Excel, doing nothing). It shows weak market understanding. Ask: 'What do customers use today, and why will they switch?'"),
    ("E. Founders", "How do you do reference checks?", "Diligence", "On-list + off-list.", "Speak to 5–8 people: ex-managers, ex-colleagues, customers, suppliers, existing investors — including people not suggested by the founder (off-list). Ask about integrity, decision-making under stress, and how they treat people."),
    ("E. Founders", "What are red flags in a founding team?", "Risk", "List + why.", "Unclear equity split or roles, a co-founder leaving, inconsistent numbers, unwillingness to share data, no skin in the game, governance shortcuts, related-party transactions."),

    # F. Deal & term sheet
    ("F. Deals", "Walk me through a term sheet.", "Deal literacy", "Economics + control + process.", "Economics: amount, pre-money, instrument (CCPS), liquidation preference, anti-dilution, ESOP pool. Control: board seats, reserved matters, information rights, founder vesting. Exit/transfer: ROFR, tag, drag, exit rights. Process: exclusivity, conditions precedent, DD. See tab 13."),
    ("F. Deals", "Explain liquidation preference with numbers.", "Waterfall", "1x non-participating example.", "Investor puts ₹25 cr for 20%. Exit at ₹100 cr: 20% = ₹20 cr < ₹25 cr, so investor takes ₹25 cr preference; founders get ₹75 cr. Exit at ₹500 cr: investor converts and takes 20% = ₹100 cr. Breakeven exit = 25 ÷ 20% = ₹125 cr. See tab 12."),
    ("F. Deals", "What is anti-dilution? Full ratchet vs weighted average?", "Protection mechanics", "Both + which is standard.", "If a later round is cheaper, the investor's conversion price is adjusted down. Full ratchet resets it to the new price (harsh). Broad-based weighted average adjusts partially, based on how many new shares are issued (market standard)."),
    ("F. Deals", "Why do Indian VCs invest through CCPS?", "India specifics", "FEMA + preference rights.", "CCPS are treated as equity under FDI rules (non-convertible preference would be debt), and they carry liquidation preference and investor rights. They convert to equity at IPO."),
    ("F. Deals", "What happens in due diligence?", "Process", "Business, financial, legal, tech, people.", "Commercial (customers, market, competition), financial (quality of revenue, unit economics, cash), legal (incorporation, cap table, IP, contracts, litigation, FEMA/ROC filings), tech (architecture, security), team (background checks, references), regulatory and ESG. See tab 22."),
    ("F. Deals", "What goes in an IC memo?", "Writing & structure", "Recommendation first.", "Recommendation and deal terms → company overview → market → product → traction & metrics → unit economics → team → competition → financials & projections → valuation & returns → risks & mitigants → DD findings → conditions. See tab 21."),
    ("F. Deals", "How do you decide the cheque size?", "Portfolio construction", "Ownership target + fund model + round need.", "Start from target ownership (e.g., 10–15%) and the fund's average initial cheque; check the company's capital need to reach the next milestone; keep reserves for follow-on (pro-rata)."),
    ("F. Deals", "What is pro-rata and why does it matter?", "Rights", "Definition + value.", "Right to invest in future rounds to maintain ownership. It lets the fund concentrate capital in winners — where most returns come from."),

    # G. Cases
    ("G. Cases", "Size the market for healthy packaged snacks in India.", "Structured guesstimate", "Top-down + bottom-up + sanity check.", "Urban households (~10 cr, assumption) × share buying packaged healthy snacks (25%) × annual spend (₹2,400) = ₹6,000 cr TAM; reachable online + quick commerce in metros (35%) = ₹2,100 cr SAM; 5% share in 5 years = ₹105 cr SOM. State assumptions clearly. See tab 17."),
    ("G. Cases", "A D2C brand: ₹30 cr revenue, 3x YoY, CM2 25%, asks ₹40 cr at ₹240 cr pre. Invest?", "Judgement", "6-step case framework.", "Growth is strong but CM2 25% is below the 35% benchmark and the price is 8x revenue (high for consumer). I'd ask for cohort repeat and channel-wise CM2. If repeat >30% and CM2 can reach 35% via price/mix, invest at ₹150–180 cr pre; otherwise pass. See tab 20."),
    ("G. Cases", "Two startups: one grows 4x with ₹30 cr burn; one grows 2x with ₹5 cr burn. Which?", "Capital efficiency", "Compare burn multiple + quality of growth.", "Compute burn multiple on net new revenue. The efficient one may be the better investment if retention is strong; the fast grower may be buying growth. Ask about cohorts, unit economics and market size before choosing."),
    ("G. Cases", "Your portfolio company has 4 months of runway. What do you do?", "Portfolio management", "Triage → options → action.", "1) Verify the real cash position and burn. 2) Cut non-essential burn immediately. 3) Options: insider bridge (CCD), venture debt, revenue acceleration, strategic sale. 4) Decide based on whether the company has reached key milestones. 5) Communicate clearly with the board and team."),
    ("G. Cases", "A company wants to raise a down round. What are the implications?", "Deal mechanics", "Anti-dilution, morale, signalling.", "Anti-dilution adjusts earlier investors' conversion prices, founders get diluted more, ESOPs go underwater (may need repricing), signals weakness. But a down round with a funded plan beats running out of cash."),

    # H. Building a new arm
    ("H. New fund arm", "If you joined us tomorrow, what would you do in the first 90 days?", "Initiative, structure", "30/60/90 plan.", "30 days: learn thesis, portfolio and process; set up deal-flow CRM and pipeline tracker; map 3 sector themes. 60 days: build market maps and target lists (50+ startups per theme); meet 40–60 founders; standardise screening memo and IC memo templates. 90 days: bring 2–3 deals to IC; set up portfolio MIS dashboard; publish 1–2 thesis notes on LinkedIn for inbound."),
    ("H. New fund arm", "How would you build deal flow for a new fund from scratch?", "Hustle", "Channels + system.", "Ecosystem mapping (incubators, accelerators, angel networks, co-investors), founder community events, content on thesis, outbound from Tracxn lists, referrals from portfolio founders, campus incubators (IITs, IISc, AIIMS for healthcare). Run a weekly pipeline review with conversion metrics."),
    ("H. New fund arm", "What should the first 10 investments of a new fund look like?", "Portfolio strategy", "Thesis consistency + diversification + signalling.", "Consistent with the thesis, diversified across 2–3 themes, priced sensibly, co-invested with reputable leads to build signalling, with reserves for follow-ons. Early winners help the next fundraise."),
    ("H. New fund arm", "How would you think about portfolio construction?", "Fund maths", "Fund size → fees → investable → initial vs reserves → number of companies → ownership.", "₹200 cr fund, ~₹35 cr fees over life, ~₹164 cr investable, 50% reserves → ₹82 cr initial; ₹3 cr average cheque → ~27 companies at ~12% entry ownership. See tab 14."),
    ("H. New fund arm", "What do LPs care about?", "Fund perspective", "Returns, DPI, team, process, governance.", "Net TVPI/IRR, DPI timing, consistency of thesis, team stability, deal access, governance and reporting quality, and alignment (GP commitment)."),
    ("H. New fund arm", "If this is a corporate/family-office arm, how is it different from a pure VC?", "Strategic understanding", "Strategic + financial objectives.", "A corporate VC also seeks strategic value (new tech, partnerships, market insight) and can offer startups distribution and customers. Risks: conflicts of interest, slower decisions, founders worried about information sharing. Good CVCs separate investment decisions from business-unit politics."),

    # I. Curveballs
    ("I. Curveballs", "If I give you ₹10 cr today, where would you invest it?", "Conviction", "Thesis → 2–3 bets → why.", "Spread across 3–4 seed bets in your strongest theme(s), or one deep conviction bet with reserves. Explain your reasoning, ownership target and expected outcome."),
    ("I. Curveballs", "What's a recent funding round or IPO you followed and what did you learn?", "Market awareness", "Facts → valuation → your view.", "Pick one from the last 3 months (check Inc42/Entrackr tonight): company, amount, valuation, investors, metric that justified it, and your view."),
    ("I. Curveballs", "What's your view on our portfolio company X?", "Preparation", "Positive + one question.", "Pick 2 portfolio companies tonight. Know their product, customers, stage and one thoughtful question about their growth or unit economics."),
    ("I. Curveballs", "Convince me to invest in this pen.", "Communication", "Treat it like a pitch.", "Need → product → market → differentiation → business model → ask. Keep it short and structured."),
    ("I. Curveballs", "What's your view on the Indian startup funding market right now?", "Macro awareness", "Data point + trend + implication.", "Check the latest Tracxn/Inc42 quarterly report tonight for one number. Themes: investors favour efficient growth; AI, consumer, fintech and deep tech draw the most interest; IPO markets give real exits; valuations are more disciplined than 2021."),
]

# ---------- Mini cases (worked) ----------
# (case, situation, numbers given, step-by-step analysis, verdict / what to say)
CASES = [
    ("Case 1 — Consumer: millet snack brand", "D2C + quick commerce snack brand raising Series A.", "Revenue ₹30 cr (3x YoY); gross margin 58%; CM2 25%; repeat rate 28% in 6 months; 55% of sales on quick commerce; asks ₹40 cr at ₹240 cr pre (8x revenue).",
     "1) Growth: strong. 2) Unit economics: GM fine; CM2 below 35% benchmark → find the leak (QC margin + ads?). 3) Retention: 28% close to 30% benchmark — check cohort curve shape. 4) Channel risk: 55% on QC → concentration. 5) Valuation: 8x revenue is rich for consumer (Series A consumer brands often price at roughly 2–5x revenue). 6) Return math: to 10x ₹280 cr post, needs ~₹2,800 cr+ exit after dilution.",
     "'Promising brand, but I'd negotiate valuation down to ₹150–180 cr pre and ask for a plan to lift CM2 to 35% via pricing, pack sizes and general-trade expansion. Key diligence: cohort data by channel, QC payment terms, contract manufacturer quality.'"),
    ("Case 2 — Deep tech: inspection drones", "Drone + AI analytics company for steel, power and oil & gas plants.", "TRL 6; 3 paid pilots (₹15 L each); 1 LOI for 20 units; BOM ₹6 L + assembly ₹0.6 L at current volume; price ₹12 L + ₹1.5 L/yr software; asks ₹15 cr at ₹60 cr pre.",
     "1) Tech: TRL 6 → this round must reach TRL 8 (DGCA type certificate). 2) Pull: paid pilots are a good sign; LOI is not revenue. 3) Unit economics: hardware GM ~45% now; 85% learning curve → ~68% at 500 units (tab 05); software adds recurring revenue. 4) Capital: estimate total ₹80–100 cr to breakeven. 5) Exits: strategic (industrial/defence majors) or IPO. 6) Valuation: risk-adjusted VC method in tab 05.",
     "'Invest with milestone-based tranches (₹8 cr now, ₹7 cr on type certificate + 2 purchase orders). Bring in a technical advisor for tech diligence; check IP ownership and DGCA timeline.'"),
    ("Case 3 — Healthcare: diagnostic centre chain", "Tier-2 city diagnostic + imaging centres, 6 centres live.", "Capex ₹1.5 cr per centre; 80 patients/day; ₹1,200 revenue per patient; centre EBITDA ~27%; payback ~22 months; wants ₹30 cr to open 15 more centres.",
     "1) Centre economics: payback <24 months is healthy (tab 06). 2) Ramp: how many months for a new centre to reach 80 patients/day? 3) Repeatability: are new centres as good as old ones (cohort of centres)? 4) Talent: radiologists/pathologists availability. 5) Payer mix: cash vs insurance vs government. 6) Competition from national chains and aggregator apps.",
     "'Strong unit economics; invest if centre cohorts show consistent ramp and if the team can hire doctors at scale. Consider part-funding capex with debt once centres are proven.'"),
    ("Case 4 — SaaS: AI customer-support software", "Indian SaaS selling AI support agents to US mid-market.", "ARR ₹18 cr ($2M), 2.5x YoY; NRR 118%; GRR 88%; gross margin 68% (after model costs); burn multiple 1.4x; asks $8M at $40M pre (20x ARR).",
     "1) Growth + retention: strong; NRR 118% elite-ish. 2) Margin: 68% OK — check inference cost trend. 3) Efficiency: burn multiple 1.4x good. 4) Moat: integration into helpdesk + proprietary conversation data? 5) Valuation: 20x ARR is high; justified only if growth sustains 2.5x+. 6) Risks: incumbents (Zendesk/Intercom AI) bundling.",
     "'Lean yes, but push for 14–16x ARR or structure with a smaller first cheque plus pro-rata. Diligence: logo-level NRR, top-10 customer concentration, model-cost sensitivity.'"),
    ("Case 5 — Manufacturing: precision components exporter", "Machined components for global auto and aerospace OEMs (China+1).", "Revenue ₹60 cr, EBITDA 18%, ROCE 22%, top customer 45% of revenue, new ₹25 cr plant planned, order book ₹90 cr.",
     "1) Order visibility: order book 1.5x revenue = good. 2) Concentration: 45% top customer = high risk. 3) Returns: ROCE 22% healthy. 4) Plant: utilisation ramp and break-even (tab 09). 5) Certifications: IATF 16949 / AS9100? 6) Financing: plant could be part debt-funded.",
     "'Good industrial business; VC fit only if it can become a platform (multiple plants, high-value aerospace/defence). Ask for customer diversification plan; mix equity with term debt for the plant.'"),
]

CASE_FRAMEWORK = [
    ("1. Clarify", "Restate the business and the ask in one line. Ask 1–2 clarifying questions."),
    ("2. Market", "How big, how fast, why now? (TAM/SAM/SOM)"),
    ("3. Business quality", "Growth, retention/cohorts, unit economics (CM2, LTV:CAC, payback), moat."),
    ("4. Team", "Founder–market fit, gaps, references."),
    ("5. Valuation & returns", "Entry multiple vs peers; exit value needed for 10x; fund-returner check."),
    ("6. Decision", "Yes / No / Yes-if. Name the top 2 risks and how diligence would test them."),
]

# ---------- Founder evaluation ----------
# (criterion, weight, what to look for, example score)
SCORECARD = [
    ("Founder–market fit", 0.15, "Why is this team uniquely suited? Lived the problem? Domain depth?", 4),
    ("Founder quality", 0.15, "Clarity, speed of learning, resilience, integrity, ability to sell and hire", 4),
    ("Team completeness", 0.05, "Tech + business + domain covered; key hires planned", 3),
    ("Market size & why now", 0.10, "Can it be a ₹2,500 cr+ company? What changed recently?", 4),
    ("Problem & product", 0.10, "Painful problem; product clearly better than alternatives", 4),
    ("Traction & PMF evidence", 0.15, "Growth, cohorts flattening, paid pilots, references", 3),
    ("Business model & unit economics", 0.10, "Positive CM2 / LTV:CAC >3x / gross margin path", 3),
    ("Moat / defensibility", 0.05, "Brand, network effects, IP, data, switching costs", 3),
    ("Capital efficiency & use of funds", 0.05, "Milestones this round buys; burn multiple", 4),
    ("Deal terms & valuation", 0.05, "Entry price vs peers; ownership; rights", 3),
    ("Exit potential", 0.05, "IPO or strategic buyers; fund-returner potential", 3),
]

FOUNDER_SIGNALS = [
    ("Clarity of thought", "Explains the business simply in 2 minutes", "Jargon, buzzwords, vague answers", "Explain your business to a 12-year-old."),
    ("Knows the numbers", "Knows CAC, retention, burn, runway by heart", "Has to check with the CFO for basics", "What was your CM2 last month and why did it change?"),
    ("Customer obsession", "Talks to customers weekly; quotes them", "Talks mostly about competitors and funding", "Tell me about the last 3 customer conversations you had."),
    ("Speed of learning", "Shows how thinking changed with data", "Same pitch for 2 years", "What did you believe 6 months ago that you no longer believe?"),
    ("Integrity", "Shares bad news proactively", "Inconsistent numbers; hides churn", "What's not working right now?"),
    ("Ability to recruit", "Has pulled strong people from good companies", "Team of only friends and juniors", "Who is the best person you've hired, and how did you convince them?"),
    ("Resilience", "Has handled a near-death moment calmly", "Blames market/investors", "Tell me about the hardest month of the company."),
    ("Ambition with realism", "Big vision + concrete next 18 months", "Fantasy projections (₹1,000 cr next year)", "What exactly will this round's money achieve by month 18?"),
    ("Coachability", "Listens, pushes back with logic", "Defensive, or agrees with everything", "Give one hard piece of feedback and watch the reaction."),
    ("Skin in the game", "Full-time, own money invested, below-market salary", "Part-time; high salaries", "How much have you personally invested?"),
]

FOUNDER_TYPES = [
    ("Consumer founder", "Brand sense, consumer insight, distribution know-how, cost discipline", "Cohorts, CM2 by channel, organic share, offline sell-through", "Over-reliance on paid ads; GMV vanity metrics"),
    ("Deep tech founder", "Technical depth (often PhD/industry R&D), ability to productise, commercial partner", "TRL roadmap, IP ownership, paid pilots, BOM curve, certification plan", "Science project; no customer contact; IP owned by institute"),
    ("Healthcare founder", "Clinical credibility (doctor co-founder or advisors), regulatory knowledge, patience", "Evidence, approvals, payer strategy, centre/device economics", "Ignores regulation; assumes patients will pay"),
    ("Manufacturing founder", "Shop-floor depth, customer relationships with OEMs, quality systems, capital discipline", "Capacity utilisation, OEE, ROCE, customer concentration, order book, certifications (ISO 9001/IATF 16949/AS9100), working capital", "Capex before orders; one customer >40%; no quality certification"),
    ("SaaS founder", "Product + GTM thinking, enterprise sales skill, global ambition", "NRR, CAC payback, sales cycle, burn multiple", "Services-heavy revenue; heavy customisation"),
    ("Fintech founder", "Regulatory understanding, risk management, partnerships with banks/NBFCs", "Licences, credit metrics (DPD, NPA), cost of funds", "Growth ahead of risk controls"),
]

REFERENCE_QS = [
    "How do you know the founder, and for how long?",
    "What is the founder exceptionally good at? What do they need help with?",
    "Tell me about a time they made a tough decision under pressure.",
    "How do they treat their team when things go wrong?",
    "Would you work for them / invest in them again? Why?",
    "Is there anything I should know that might not come up in a normal diligence?",
    "(Customer reference) Why did you choose this product? What would make you switch away?",
    "(Ex-employee) Why did you leave? How were decisions made?",
]

# ---------- Deal process ----------
# (stage, what happens, associate's job, output / document, typical time)
DEAL_PROCESS = [
    ("1. Sourcing", "Find startups: referrals, networks, outbound, events, inbound decks", "Build theme-based lists, cold outreach, attend demo days, log every company in CRM", "Pipeline tracker / CRM entry", "Continuous"),
    ("2. Screening", "Quick filter against fund thesis: stage, sector, cheque size, geography, red flags", "Read deck, check founders on LinkedIn, quick market check, 1-paragraph note", "Screening note (go / no-go)", "15–30 min per deck"),
    ("3. First meeting", "Founder pitch + Q&A with associate/partner", "Prepare questions, take notes, ask for data room / MIS", "Meeting notes + data request list", "45–60 min"),
    ("4. Deep dive", "Understand business deeply: metrics, market, competition, customers", "Build financial analysis (cohorts, unit economics), market sizing, competitor map, customer calls", "Investment thesis draft, model, market map", "1–3 weeks"),
    ("5. Partner / IC discussion", "Internal discussion; decide whether to issue a term sheet", "Write IC memo, prepare valuation and returns analysis, answer partner questions", "IC memo + deck", "1–2 weeks"),
    ("6. Term sheet", "Agree on valuation and key terms; usually 30–60 day exclusivity", "Draft/compare term sheets, cap table and dilution model", "Signed term sheet", "1–2 weeks"),
    ("7. Due diligence", "Legal, financial, tax, tech, commercial, background checks", "Coordinate lawyers/CAs, track DD checklist, flag issues", "DD reports + issue list", "3–8 weeks"),
    ("8. Documentation & closing", "SSA, SHA, board resolutions, valuation report, money transfer, share allotment", "Track conditions precedent, valuation report, FEMA filings (FC-GPR) if foreign money", "Signed SSA/SHA, share certificates, filings", "2–4 weeks"),
    ("9. Portfolio management", "Board meetings, MIS reviews, hiring and customer help, follow-on decisions", "Monthly MIS tracking, quarterly reporting to LPs, prepare board decks, help with next round", "Portfolio dashboard, LP reports", "Years"),
    ("10. Exit", "IPO, strategic sale, secondary sale", "Exit analysis, buyer lists, valuation", "Exit memo; distributions to LPs", "Year 5–10"),
]

MONEY_FLOW = [
    ("1", "LPs commit capital to the fund", "e.g., ₹200 cr committed by family offices, HNIs, corporates, SIDBI FFS"),
    ("2", "Fund calls capital as needed (drawdowns)", "LPs transfer money only when a capital call notice is issued"),
    ("3", "Fund invests in startup via SSA", "Money moves to the startup's bank account; startup allots CCPS to the fund"),
    ("4", "Startup deploys money against milestones", "Hiring, product, marketing, inventory, capex, R&D — per the agreed use-of-funds plan"),
    ("5", "Startup reports monthly MIS; fund monitors", "Board seat / information rights; reserves used for follow-on rounds"),
    ("6", "Exit: IPO / M&A / secondary", "Fund receives cash (or listed shares, which it sells)"),
    ("7", "Distribution waterfall to LPs and GP", "Return of capital → preferred return (hurdle) → GP catch-up → 80/20 split (see tab 14)"),
]

# (sector, where the money mostly goes, how it is usually released, what the investor tracks)
USE_OF_FUNDS = [
    ("Consumer / D2C", "Marketing & brand (30–40%), inventory & working capital (20–30%), team (20%), offline distribution (10–20%)", "Single tranche; sometimes revenue-based financing for inventory", "CAC, repeat, CM2, inventory days"),
    ("SaaS", "Sales & marketing (40–50%), engineering & product (30–40%), G&A (10–15%)", "Single tranche", "ARR, NRR, payback, burn multiple"),
    ("Deep tech", "R&D talent (40–50%), prototyping & testing (20–30%), certification (10%), pilot deployments (10–20%)", "Milestone-linked tranches + grants", "TRL milestones, pilot conversions, BOM"),
    ("Healthcare", "Clinical studies & regulatory (30–40%), team (25%), centre capex or device manufacturing (20–30%), sales (10–20%)", "Milestone-linked (approval, trial data) or per-centre", "Approvals, evidence, centre payback"),
    ("Manufacturing", "Capex for plant & machinery (40–60%), working capital (20–30%), team & certifications (10–20%)", "Equity for first plant proof; debt for later capex", "Utilisation, ROCE, order book"),
    ("Fintech lending", "Equity capital to support loan book (leverage), tech, risk team", "Equity + debt lines from banks/NBFCs", "AUM, NPA, capital adequacy"),
]

# ---------- Term sheet decoder ----------
# (clause, what it means in simple words, founder-friendly version, investor-friendly version, Indian market norm / note)
TERM_SHEET = [
    ("Amount & instrument", "How much is invested and in what security", "Equity / CCPS on clean terms", "CCPS with many rights", "CCPS is standard for VC in India"),
    ("Pre-money valuation", "Company value before the money", "Higher pre-money", "Lower pre-money", "Negotiated; compare with peers"),
    ("ESOP pool", "Shares reserved for employees", "Pool created post-money or sized to real hiring plan", "Large pool created in pre-money (option pool shuffle)", "10–15% pool at seed/Series A"),
    ("Liquidation preference", "Who gets paid first on sale/wind-up", "1x non-participating", "2x or participating", "1x non-participating is the norm"),
    ("Participation", "Whether investor gets preference AND a share of the rest", "Non-participating", "Full participation (double dip)", "Participation is uncommon in India early stage"),
    ("Anti-dilution", "Protection if a later round is cheaper", "Broad-based weighted average", "Full ratchet", "Broad-based weighted average is standard"),
    ("Board composition", "Who sits on the board", "Founders control; 1 investor seat", "Investor majority or many seats", "Lead investor usually gets 1 seat; others observer seats"),
    ("Reserved / affirmative matters", "Decisions needing investor approval", "Short list: new shares, change of business, sale of company", "Long list including budgets and hiring", "Negotiate a reasonable list"),
    ("Information rights", "Investor's right to MIS, financials, audits", "Quarterly reports", "Monthly MIS + audits + budget approval", "Monthly MIS is common"),
    ("Pro-rata / pre-emptive rights", "Right to invest in future rounds to keep %", "Pro-rata only for major investors", "Super pro-rata", "Standard for leads"),
    ("ROFR / ROFO", "Right of first refusal/offer when shareholders sell shares", "Limited ROFR", "ROFR on all transfers", "Common"),
    ("Tag-along", "Investor can sell alongside if founders sell", "Standard", "Standard", "Common"),
    ("Drag-along", "Majority can force others to sell in an exit", "High threshold, minimum price", "Low threshold, after X years", "Often linked to exit timelines"),
    ("Exit rights / put option", "Investor's right to exit by a date via IPO, sale, buyback", "Best-efforts IPO/sale; no put on founders", "Put option on company/founders", "Exit clauses common in India; avoid founder personal liability"),
    ("Founder vesting / lock-in", "Founders' shares vest or are locked over time", "Credit for time served; short lock-in", "4-year reverse vesting from now", "Founder lock-in common"),
    ("Non-compete / non-solicit", "Founders can't start competing business", "Limited to employment period", "Long post-exit period", "Post-employment non-competes are hard to enforce in India (Sec 27, Contract Act)"),
    ("Exclusivity / no-shop", "Founders can't talk to other investors for a period", "Short (30 days)", "Long (60–90 days)", "30–60 days typical; binding clause"),
    ("Conditions precedent (CPs)", "What must happen before money comes in", "Short list", "Long list incl. key hires, IP assignment", "Valuation report, IP assignment, board approvals"),
    ("Representations & warranties", "Facts the company/founders confirm as true", "Company-only reps, knowledge-qualified", "Founder personal reps", "Negotiate caps on liability"),
    ("Indemnity", "Who pays if a rep turns out false", "Capped, company only", "Uncapped, founders jointly liable", "Caps and time limits are standard asks"),
    ("Redemption", "Investor can ask company to buy back shares", "None", "After 5–7 years", "Rare for CCPS; check FEMA"),
    ("Most favoured nation (MFN)", "Investor gets the best terms given to later investors", "None", "Broad MFN", "Common in SAFEs/notes"),
    ("Confidentiality & costs", "Keep terms private; who pays legal fees", "Each side pays own", "Company pays investor legal fees (capped)", "Company usually pays capped investor costs"),
]

# ---------- DD checklist ----------
# (area, item, why it matters)
DD_CHECKLIST = [
    ("Commercial", "Customer list with revenue by customer (top 10 concentration)", "Concentration risk"),
    ("Commercial", "Customer calls (5–10), including churned customers", "Real product value"),
    ("Commercial", "Market sizing and competitor mapping", "Size of prize"),
    ("Commercial", "Pipeline / order book with stage and probability", "Revenue visibility"),
    ("Commercial", "Pricing history and discounting", "Pricing power"),
    ("Financial", "Audited financials (last 2–3 years) + monthly MIS (last 12–24 months)", "Quality of numbers"),
    ("Financial", "Revenue recognition policy (GMV vs net, deferred revenue)", "Inflated revenue risk"),
    ("Financial", "Cohort data, unit economics by channel/product", "Business quality"),
    ("Financial", "Bank statements reconciled to MIS", "Fraud check"),
    ("Financial", "Burn, runway, debt, contingent liabilities", "Cash risk"),
    ("Financial", "Working capital: inventory ageing, receivable ageing", "Hidden cash drain"),
    ("Financial", "Projections and assumptions; use of funds", "Plan realism"),
    ("Tax", "GST, TDS, income tax filings and notices", "Hidden liabilities"),
    ("Legal", "Incorporation documents, MoA/AoA, statutory registers", "Corporate hygiene"),
    ("Legal", "Cap table, all past share issues, valuation reports, ESOP plan", "Ownership clarity"),
    ("Legal", "Past SHA/SSA rights of existing investors", "Conflicting rights"),
    ("Legal", "FEMA compliance (FC-GPR, FC-TRS), ROC filings", "Regulatory penalties"),
    ("Legal", "IP: patents, trademarks, IP assignment from founders/employees", "Who owns the tech/brand"),
    ("Legal", "Material contracts: customers, suppliers, leases, loans", "Change-of-control and exclusivity clauses"),
    ("Legal", "Litigation and disputes", "Contingent risk"),
    ("Legal", "Licences and approvals (FSSAI, CDSCO, RBI, DGCA, etc.)", "Licence to operate"),
    ("Technology", "Architecture, scalability, security audit, code ownership", "Tech risk"),
    ("Technology", "Data protection (DPDP Act) practices", "Compliance risk"),
    ("Team / HR", "Founder background checks (education, employment, litigation, credit)", "Integrity risk"),
    ("Team / HR", "Reference checks (on-list and off-list)", "Founder quality"),
    ("Team / HR", "Org chart, key employee contracts, attrition, ESOP grants", "Execution risk"),
    ("Team / HR", "Labour law compliance (PF, ESI, gratuity)", "Hidden liabilities"),
    ("Regulatory / sector", "Sector-specific rules (RBI for fintech, CDSCO for health, FSSAI for food, DGCA for drones)", "Business can be shut by regulation"),
    ("ESG", "Environmental, social, governance policies; related-party transactions", "LP and reputation requirements"),
]

# ---------- IC memo template ----------
# (section, what to write, example (fictional company))
IC_MEMO = [
    ("1. Recommendation", "Invest / pass; amount; instrument; valuation; ownership; key conditions", "Invest ₹8 cr in CCPS at ₹60 cr pre-money (11.8% post) in AeroSense (drones), in two tranches"),
    ("2. Company snapshot", "What it does in 2 lines; stage; founded; team size; location", "Inspection drones + AI analytics for heavy industry; Bengaluru; 28 people; founded 2023"),
    ("3. Problem & solution", "Customer pain; current alternatives; why this is better", "Manual inspections need shutdowns; drones cut inspection time 70%"),
    ("4. Market", "TAM/SAM/SOM; growth; why now", "₹4,000 cr India industrial inspection market; drone rules 2021 + import ban on foreign drones"),
    ("5. Traction & metrics", "Revenue, growth, customers, retention, pilots, key KPIs", "3 paid pilots, 1 LOI for 20 units, ₹1.2 cr revenue"),
    ("6. Business model & unit economics", "How it makes money; margins; CAC; payback", "₹12 L per drone + ₹1.5 L/yr software; GM 50% → 60% at scale"),
    ("7. Team", "Founders, key hires, gaps, references", "IIT-M aero PhD + ex-L&T sales head; need CFO by Series A"),
    ("8. Competition & moat", "Competitor map; differentiation; defensibility", "ideaForge (defence), foreign drones (restricted); moat = AI models trained on plant data"),
    ("9. Financials & projections", "Past 2 years + 3–5 year plan; key assumptions", "₹1.2 cr → ₹8 cr → ₹25 cr → ₹60 cr revenue"),
    ("10. Valuation & returns", "Entry valuation vs comps; exit scenarios; MOIC/IRR; fund-returner test", "Base case 12x MOIC; fund-returner at ₹2,500 cr exit"),
    ("11. Risks & mitigants", "Top 5 risks and how they're mitigated", "Certification delay → tranche 2 linked to type certificate"),
    ("12. Due diligence summary", "Findings from legal, financial, tech, references", "Clean cap table; IP assigned; 6 positive references"),
    ("13. Deal terms", "Key term sheet points", "1x non-participating, board seat, broad-based anti-dilution, pro-rata"),
    ("14. Use of funds & milestones", "What the money buys by when", "TRL 8 + 2 POs in 15 months; team to 45"),
    ("15. Post-investment plan", "How the fund will help; KPIs to monitor", "Intro to 5 steel/power companies; monthly MIS"),
]

# ---------- Firm research template ----------
FIRM_RESEARCH = [
    ("Firm name", "People Moves", "No public coverage found in a web search — confirm website/LinkedIn and the legal entity name (MCA)."),
    ("Parent business behind the new VC arm", "", "Is People Moves a corporate, family office or existing fund launching a VC arm? What does the parent do?"),
    ("Website / LinkedIn page", "", ""),
    ("CEO: Chandru — background", "", "LinkedIn: past roles, companies founded, sectors, posts/podcasts. Find one thing to mention."),
    ("Fund size / corpus", "", "Website, news, SEBI AIF list (sebi.gov.in → AIF registrations)"),
    ("SEBI registration (Cat I / Cat II AIF?)", "", "Search the fund name on the SEBI AIF list"),
    ("Stage focus (pre-seed / seed / Series A / growth)", "", ""),
    ("Cheque size", "", ""),
    ("Sector focus / thesis", "", "Likely consumer, deep tech, healthcare (from what you've heard) — confirm"),
    ("Portfolio company 1 + what it does", "", "Tracxn / Crunchbase / website"),
    ("Portfolio company 2 + what it does", "", ""),
    ("Portfolio company 3 + what it does", "", ""),
    ("Recent news / deals (last 6 months)", "", "Inc42, Entrackr, ET, VCCircle"),
    ("Team size and structure", "", "Who else is in the investment team?"),
    ("What makes them different from other funds", "", ""),
    ("My one-line 'why this firm'", "", "Write it here and say it tomorrow."),
]

QUESTIONS_TO_ASK = [
    ("Thesis", "What is the core thesis of the new arm, and how is it different from the existing business?"),
    ("Thesis", "Which 2–3 sectors do you expect the first set of investments to come from?"),
    ("Strategy", "Is the new arm purely financial, or also strategic for the parent business?"),
    ("Process", "How does an investment decision get made here — who sits on the investment committee?"),
    ("Process", "What does a typical week look like for an investment associate in your team?"),
    ("Role", "What would make someone in this role exceptional in the first 6 months?"),
    ("Role", "How much ownership does an associate get on sourcing and leading a deal end-to-end?"),
    ("Portfolio", "Which portfolio company are you most excited about, and why?"),
    ("Portfolio", "What does portfolio support look like after you invest?"),
    ("Fund", "What stage and cheque size are you targeting, and how many companies per year?"),
    ("Learning", "What is the biggest lesson from your past investments that shapes how you invest now?"),
    ("Close", "Is there anything in my background that makes you hesitate? I'd like to address it."),
]

DONT_DO = [
    "Don't quote numbers you're unsure of — say 'roughly' and give your logic.",
    "Don't say 'no competition' or 'this sector has no risk'.",
    "Don't bad-mouth any founder, fund or company.",
    "Don't give a long answer without a conclusion — end with your view.",
    "Don't pretend to know their portfolio if you haven't researched it — ask instead.",
    "Don't ask about salary/leave in the first general round unless he raises it.",
]
