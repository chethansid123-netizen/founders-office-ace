/* Core reference data: programs, pipeline, lead fields, assumptions, evidence library.
   Everything a rep would otherwise keep in their head lives here as data so the views stay thin. */

const PROGRAMS = {
  p1: { key: "p1", short: "Program 1", name: "Product & Experience Mastery in an AI-enabled World", weeks: 12, price: 149000,
        promise: "Shape product direction instead of only delivering it.",
        skills: ["Frame the right problems", "Link customer needs to business value", "Decide well under uncertainty", "Influence stakeholders with evidence", "Own outcomes, not just deliverables"],
        includes: "Mentor reviews, applied learning on a real enterprise challenge, a Consultant's Casebook." },
  p2: { key: "p2", short: "Program 2", name: "Human–AI & Agentic Systems Design", weeks: 7, price: 90000,
        promise: "Design AI-enabled products people can trust and operate.",
        skills: ["Spot high-value AI opportunities", "Design human–AI workflows", "Define when AI acts, escalates, or needs a human", "Orchestrate agents, people and enterprise systems", "Build trust and accountability into AI experiences"],
        includes: "A Human–AI Casebook and mentor review of your own work." },
  combo: { key: "combo", short: "Combo", name: "Both programs, in sequence", weeks: 23, price: 239000,
        promise: "The full journey, with a four-week gap between cohorts.",
        skills: [], includes: "Both programs. The site says 'special bundle discount' without a figure; the discount here is an editable assumption." }
};

/* Pipeline stages. prob = share of leads at this stage that typically end up enrolled (editable assumption). */
const STAGES = [
  { key: "new",       name: "New",            band: "top",  prob: 3,   hint: "Captured, not yet spoken to. The clock is running." },
  { key: "contacted", name: "Contacted",      band: "top",  prob: 6,   hint: "First touch made, no real conversation yet." },
  { key: "diagnosed", name: "Diagnosed",      band: "mid",  prob: 15,  hint: "Explain-it call done. Gap scored, blocker tagged." },
  { key: "mentor",    name: "Mentor call",    band: "mid",  prob: 30,  hint: "Conversation with a yuj.dna mentor booked or held." },
  { key: "proposal",  name: "Offer sent",     band: "bot",  prob: 50,  hint: "Program, price and payment plan sent in writing." },
  { key: "committed", name: "Seat blocked",   band: "bot",  prob: 85,  hint: "Deposit paid. Seat held." },
  { key: "enrolled",  name: "Enrolled",       band: "won",  prob: 100, hint: "Fee paid or payment plan active." },
  { key: "nurture",   name: "Nurture",        band: "off",  prob: 2,   hint: "Not now. Next cohort, with a dated reason." },
  { key: "lost",      name: "Lost",           band: "off",  prob: 0,   hint: "Closed. Reason recorded." }
];
const OPEN_STAGES = ["new", "contacted", "diagnosed", "mentor", "proposal", "committed"];
const FLOW = ["new", "contacted", "diagnosed", "mentor", "proposal", "committed", "enrolled"];

const SOURCES = [
  { key: "referral",   name: "Alumni referral",        warmth: 15, band: "bot" },
  { key: "partner",    name: "Company or partner intro", warmth: 13, band: "mid" },
  { key: "inbound",    name: "Website form",           warmth: 12, band: "mid" },
  { key: "masterclass",name: "Masterclass",            warmth: 11, band: "mid" },
  { key: "event",      name: "Meetup or event",        warmth: 9,  band: "top" },
  { key: "linkedin_in",name: "LinkedIn inbound",       warmth: 9,  band: "top" },
  { key: "whatsapp",   name: "WhatsApp community",     warmth: 8,  band: "top" },
  { key: "newsletter", name: "Newsletter",             warmth: 7,  band: "top" },
  { key: "linkedin_out",name: "LinkedIn outbound",     warmth: 5,  band: "top" },
  { key: "cold",       name: "Cold email or call",     warmth: 3,  band: "top" }
];

const SIGNALS = [
  { key: "replied",    name: "Replied to a message" },
  { key: "diagnostic", name: "Did the explain-it check" },
  { key: "masterclass",name: "Attended a masterclass" },
  { key: "price",      name: "Asked about price" },
  { key: "dates",      name: "Asked about cohort dates" },
  { key: "work",       name: "Shared a real work problem" },
  { key: "intro",      name: "Brought in a colleague" },
  { key: "employer",   name: "Asked about employer sponsorship" },
  { key: "cert",       name: "Asked about a certificate" },
  { key: "trigger",    name: "Trigger event (new role, missed promotion, AI mandate)" }
];

const SENIORITY = [
  { key: "ic", name: "Individual contributor" }, { key: "lead", name: "Lead or senior" },
  { key: "manager", name: "Manager" }, { key: "head", name: "Head, director or founder" }
];
const PAYERS = [
  { key: "unknown", name: "Not known yet" }, { key: "self", name: "Self-paid" },
  { key: "split", name: "Split with employer" }, { key: "employer", name: "Employer-paid" }
];
const CO_STAGES = ["Seed", "Series A", "Series B", "Series C+", "Unicorn / public", "GCC / MNC", "Services / agency", "Independent"];
const ACTIVITY_TYPES = [
  { key: "call", name: "Call" }, { key: "whatsapp", name: "WhatsApp" }, { key: "email", name: "Email" },
  { key: "linkedin", name: "LinkedIn" }, { key: "meeting", name: "Meeting" }, { key: "note", name: "Note" }
];
const OUTCOMES = ["Connected", "No answer", "Replied", "Booked next step", "Sent material", "Not interested", "Asked to call later"];

/* The explain-it check. Ten dimensions lifted from the two programs' own skill lists, so the diagnosis
   measures exactly what the program builds. Rep scores 0 (can't explain), 1 (partly), 2 (clear, with evidence). */
const DIAG = [
  { key: "frame",    prog: "p1", name: "Frames the problem",        ask: "Why was this the right problem to solve now?" },
  { key: "value",    prog: "p1", name: "Links need to business value", ask: "Which business number was it meant to move, and did it?" },
  { key: "decide",   prog: "p1", name: "Decides under uncertainty", ask: "What would have changed your mind?" },
  { key: "influence",prog: "p1", name: "Influences with evidence",  ask: "What did you bring when a senior person disagreed?" },
  { key: "own",      prog: "p1", name: "Owns the outcome",          ask: "What happened after launch, and what did you do about it?" },
  { key: "spot",     prog: "p2", name: "Spots AI opportunities",    ask: "Where would AI change the economics of your product, not just a task?" },
  { key: "workflow", prog: "p2", name: "Designs human–AI workflow", ask: "Who does what, human or AI, step by step?" },
  { key: "handoff",  prog: "p2", name: "Sets act / escalate rules", ask: "When must the AI stop and ask a person?" },
  { key: "orchestrate", prog: "p2", name: "Orchestrates agents and systems", ask: "What happens when two systems disagree?" },
  { key: "trust",    prog: "p2", name: "Builds trust and accountability", ask: "Who is accountable when the AI is wrong, and how would the user know?" }
];

/* Editable assumptions. `src` says where the default came from: site (yujdna.com), bench (public benchmark), guess (to be replaced). */
const DEFAULTS = {
  priceP1: 149000, priceP2: 90000, comboDiscountPct: 10,
  seatsP1: 25, seatsP2: 25, cohortsYearP1: 4, cohortsYearP2: 5,
  varCostPerSeat: 30000, cacTarget: 15000, minMarginPct: 35,
  slaMins: 60, staleDays: 4, offerNudgeDays: 5, cadenceTouches: 9,
  conv: { new: 85, contacted: 40, diagnosed: 55, mentor: 60, proposal: 45, committed: 85 },
  stackCapPct: 20, poolPct: 8, needCapPct: 15, depositAmount: 10000,
  ratioTech: 12, ratioD2c: 8, ratioDeep: 5,
  tamPm: 85000, tamDesign: 60000, tamAdjacent: 400000, reachPct: 25, fitPct: 20,
  repName: "", calendarLink: ""
};
const ASSUMPTION_META = [
  { k: "priceP1", label: "Program 1 fee (₹)", src: "site", note: "₹1,49,000 on yujdna.com. GST treatment not stated on the site." },
  { k: "priceP2", label: "Program 2 fee (₹)", src: "site", note: "₹90,000 on yujdna.com." },
  { k: "comboDiscountPct", label: "Combo discount (%)", src: "guess", note: "Site says 'special bundle discount' with no figure." },
  { k: "seatsP1", label: "Seats per Program 1 cohort", src: "guess", note: "Site says 'small cohort'. Replace with the real cap." },
  { k: "seatsP2", label: "Seats per Program 2 cohort", src: "guess", note: "Same." },
  { k: "cohortsYearP1", label: "Program 1 cohorts a year", src: "guess", note: "12 weeks each; four a year is the ceiling without overlap." },
  { k: "cohortsYearP2", label: "Program 2 cohorts a year", src: "guess", note: "7 weeks each." },
  { k: "varCostPerSeat", label: "Variable cost per seat (₹)", src: "guess", note: "Mentor review time, casebook, platform. Drives the discount floor." },
  { k: "cacTarget", label: "Target cost to acquire one learner (₹)", src: "guess", note: "About 10% of the Program 1 fee. Vendor benchmarks for adult upskilling run ₹3,000 to ₹10,000 at far lower ticket sizes." },
  { k: "minMarginPct", label: "Minimum contribution margin after discount (%)", src: "guess", note: "Below this an offer needs approval." },
  { k: "slaMins", label: "First-response target (minutes)", src: "bench", note: "HBR 2011: contact within the hour made qualifying about 7 times likelier." },
  { k: "staleDays", label: "Days without a touch before a lead is stale", src: "guess", note: "" },
  { k: "offerNudgeDays", label: "Days an offer may sit unanswered", src: "guess", note: "" },
  { k: "stackCapPct", label: "Maximum total scholarship (%)", src: "guess", note: "Stacked levers never exceed this." },
  { k: "poolPct", label: "Scholarship pool per cohort (% of list revenue)", src: "guess", note: "A budget, so scholarships are scarce and real." },
  { k: "needCapPct", label: "Need-based scholarship cap (%)", src: "guess", note: "" },
  { k: "depositAmount", label: "Seat-block deposit (₹)", src: "guess", note: "Small enough to say yes to today, large enough to mean it." },
  { k: "ratioTech", label: "Addressable roles in a tech company (% of headcount)", src: "guess", note: "Product, design, research, program, analytics. Replace per account with a real count." },
  { k: "ratioD2c", label: "Addressable roles in a consumer brand (%)", src: "guess", note: "Brand, marketing, category, operations leads." },
  { k: "ratioDeep", label: "Addressable roles in a deep-tech company (%)", src: "guess", note: "Product, program and business roles." }
];

/* Evidence library. status: 'checked' = looked up while building this tool (Nov 2026);
   'classic' = long-established source cited from the literature, open it before quoting a number. */
const EVID = {
  wef: { claim: "Employers expect 39% of workers' core skills to change by 2030. Analytical thinking is the skill most employers call essential (about 7 in 10), and 63% name skill gaps as the main barrier to transformation.",
    src: "World Economic Forum, Future of Jobs Report", year: 2025, url: "https://www.weforum.org/publications/the-future-of-jobs-report-2025/", status: "checked",
    caveat: "Employer expectations from a survey of 1,000+ employers, not measured outcomes.", use: "Why judgment and thinking skills, not tools, are the safe investment." },
  jagged: { claim: "In a field experiment with 758 BCG consultants, those using GPT-4 on tasks inside its ability finished 12.2% more tasks, 25.1% faster, at about 40% higher quality. On a task outside its ability they were 19 percentage points less likely to be right.",
    src: "Dell'Acqua et al., Harvard Business School working paper 'Navigating the Jagged Technological Frontier'", year: 2023, url: "https://papers.ssrn.com/abstract=4573321", status: "checked",
    caveat: "One firm, one model generation. The pattern, not the exact numbers, is the point.", use: "AI lifts everyone's output. Knowing where to trust it is the scarce skill." },
  metr: { claim: "Sixteen experienced open-source developers on 246 real tasks took 19% longer when allowed AI tools. Before starting they predicted a 24% speed-up, and afterwards still believed they had been about 20% faster.",
    src: "METR randomised controlled trial", year: 2025, url: "https://www.theregister.com/2025/07/11/ai_code_tools_slow_down/", status: "checked",
    caveat: "Small sample, experts on large familiar codebases, early-2025 tools. Do not generalise to all coding.", use: "The cleanest evidence that people misjudge their own performance with AI." },
  nanda: { claim: "95% of the organisations studied were getting no measurable profit-and-loss return from generative-AI pilots. The authors blame workflow fit and integration, not model quality.",
    src: "MIT NANDA, 'The GenAI Divide: State of AI in Business 2025'", year: 2025, url: "https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/", status: "checked",
    caveat: "150 interviews, 350 survey responses, 300 public deployments. 'No measurable return' is not the same as 'failed'.", use: "The gap is design of the human–AI workflow, which is what Program 2 teaches." },
  gartner: { claim: "Gartner predicts over 40% of agentic-AI projects will be cancelled by the end of 2027 because of rising cost, unclear business value or weak risk controls.",
    src: "Gartner press release, 25 June 2025", year: 2025, url: "https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027", status: "checked",
    caveat: "A forecast, not an observation.", use: "Companies need people who can decide where agents create value and where they must stop." },
  eurich: { claim: "Across ten studies with nearly 5,000 people, most believed they were self-aware but only an estimated 10 to 15% met the criteria. Accuracy fell as people gained experience and power.",
    src: "Tasha Eurich, Harvard Business Review, 'What Self-Awareness Really Is'", year: 2018, url: "https://hbr.org/2018/01/what-self-awareness-really-is-and-how-to-cultivate-it", status: "checked",
    caveat: "The 10 to 15% is the author's estimate, not a population rate.", use: "Why 'I already know this' is the expected answer, especially from senior people." },
  dk: { claim: "People who scored in the bottom quarter on tests of reasoning and grammar estimated themselves well above average (around the 62nd percentile against an actual 12th). Skill at a task and skill at judging one's own performance are the same skill.",
    src: "Kruger & Dunning, Journal of Personality and Social Psychology 77(6)", year: 1999, url: "https://doi.org/10.1037/0022-3514.77.6.1121", status: "classic",
    caveat: "Later work debates the size of the effect. Never use this to tell a prospect they are incompetent.", use: "You cannot see a gap in a skill you do not have. So show it, do not tell it." },
  ioed: { claim: "People rate their understanding of how something works as high, then rate it much lower after being asked to explain it step by step.",
    src: "Rozenblit & Keil, Cognitive Science 26, 'The illusion of explanatory depth'", year: 2002, url: "https://doi.org/10.1207/s15516709cog2605_1", status: "classic",
    caveat: "Lab studies on everyday devices and concepts.", use: "The mechanism behind the explain-it call: ask them to walk you through it." },
  kohavi: { claim: "Of ideas tested in controlled experiments at Microsoft, only about one third improved the metric they were designed to improve. A third did nothing and a third made it worse.",
    src: "Kohavi et al., 'Online Experimentation at Microsoft' and later talks", year: 2009, url: "https://ai.stanford.edu/~ronnyk/2012-09ACMRecSysNR.pdf", status: "checked",
    caveat: "Microsoft, 2009 to 2013. Kohavi puts failure at 60 to 90% depending on domain.", use: "Shipping is not impact. Choosing what to build is the skill." },
  pendo: { claim: "In the average software product, 80% of features are rarely or never used.",
    src: "Pendo, 2019 Feature Adoption Report (615 product subscriptions)", year: 2019, url: "https://www.pendo.io/resources/the-2019-feature-adoption-report/", status: "checked",
    caveat: "Vendor data on features its customers chose to tag.", use: "Feature production versus product direction." },
  mckDecide: { claim: "Only 20% of managers say their organisation excels at decision making, and 61% say most of their decision-making time is used ineffectively.",
    src: "McKinsey, 'Decision making in the age of urgency'", year: 2019, url: "https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/decision-making-in-the-age-of-urgency", status: "checked",
    caveat: "Self-reported survey.", use: "Decision quality is a recognised, expensive, unsolved problem." },
  mckDesign: { claim: "Companies in the top quarter of McKinsey's Design Index grew revenue 32 percentage points and shareholder returns 56 points faster than peers over five years. The other three quarters performed about the same as each other.",
    src: "McKinsey, 'The business value of design' (300 companies)", year: 2018, url: "https://www.mckinsey.com/business-functions/mckinsey-design/our-insights/the-business-value-of-design", status: "checked",
    caveat: "Correlation, not proof of cause.", use: "Design pays only when it is tied to business decisions, and only the best get the reward." },
  hbrLeads: { claim: "Firms that tried to contact a web lead within an hour were about seven times as likely to qualify it as those that waited longer. The average firm took 42 hours.",
    src: "Oldroyd, McElheran & Elkington, Harvard Business Review, 'The Short Life of Online Sales Leads' (2,241 US firms)", year: 2011, url: "https://scholarsarchive.byu.edu/facpub/9711", status: "checked",
    caveat: "US B2B web leads; secondary summaries disagree on the lead count.", use: "The first-response target on every new lead." },
  gong: { claim: "In recorded sales calls, top performers talk less than they listen (about 43:57 in the original analysis; a 2025 re-run found won deals at 57% talk time against 62% for lost). Successful discovery calls carry 11 to 14 questions spread through the call.",
    src: "Gong Labs", year: 2025, url: "https://www.gong.io/blog/talk-to-listen-conversion-ratio", status: "checked",
    caveat: "Vendor analysis, mostly US B2B software sales.", use: "The diagnostic call is questions, not a pitch." },
  completion: { claim: "Median completion for open online courses is about 12.6%. On one course platform's data, scheduled cohorts averaged 53.4% completion against 41.9% for self-paced.",
    src: "Jordan (IRRODL, 221 MOOCs); Ruzuku platform data (26,632 courses)", year: 2015, url: "https://www.ruzuku.com/learn/articles/course-success-index", status: "checked",
    caveat: "Different learner populations. The format effect is real but smaller than marketing claims.", use: "Honest answer to 'I've done courses and nothing changed'." },
  fibe: { claim: "72% of Indian professionals surveyed said they would upskill through edtech if EMI was available, and 69% named budget as a barrier.",
    src: "Fibe survey, March 2025", year: 2025, url: "https://www.fibe.in/news/72-percent-indian-professionals-willing-upskill-edtech-emi/", status: "checked",
    caveat: "Commissioned by a lender.", use: "Why a payment plan belongs in every offer, stated plainly." },
  bench: { claim: "Agency benchmarks for Indian edtech put lead-to-enrolment at 3 to 10% depending on ticket size, and 8 to 18% for professional certifications at ₹20,000 to ₹1.5 lakh with a one-to-three-month decision window.",
    src: "upGrowth and similar agency benchmark tables", year: 2026, url: "https://upgrowth.in/edtech-marketing-calculators/", status: "checked",
    caveat: "Vendor marketing pages with no disclosed sample. Directional only; your own funnel replaces them within a month.", use: "Starting targets for the funnel until real numbers exist." },
  gcc: { claim: "India hosts 2,117 global capability centres across 3,728 units, employing about 2.36 million people with $98.4 billion revenue in FY26.",
    src: "Nasscom–Zinnov, reported May 2026", year: 2026, url: "https://yourstory.com/enterprise-story/2026/05/gccs-number-touch-2117-in-india-revenue-just-short-of-100-billion", status: "checked",
    caveat: "Count rose partly through wider scope since the 2024 report.", use: "Size of the phase-two enterprise market." },
  nasscom: { claim: "India's technology industry employs about 5.95 million people (FY26 estimate), adding about 135,000 jobs in the year.",
    src: "Nasscom Strategic Review, February 2026", year: 2026, url: "https://www.thecore.in/business/ai-dampens-tech-hiring-in-india-23-growth-in-fy26-vs-fy25-859053", status: "checked",
    caveat: "", use: "The outer bound of the addressable workforce." },
  tracxn: { claim: "Indian tech companies raised $10.3 billion in the first nine months of 2026, up 7%, across 1,134 rounds, down 38%. Early-stage funding rose 27% to $4.2 billion while seed fell 37%. Bengaluru took 43%.",
    src: "Tracxn India Tech 9M 2026", year: 2026, url: "https://yourstory.com/2026/09/indias-tech-cos-raise-usd-103b-in-2026-tracxn-report", status: "checked",
    caveat: "", use: "Fewer, larger rounds: funded Series A and B teams are concentrated and findable." },
  shiv: { claim: "People who bought an energy drink at a discount solved fewer puzzles than those who paid full price. Price changes not just perceived quality but actual performance.",
    src: "Shiv, Carmon & Ariely, Journal of Marketing Research 42(4)", year: 2005, url: "https://doi.org/10.1509/jmkr.2005.42.4.383", status: "classic",
    caveat: "Lab studies on consumer products.", use: "Why unconditional discounts damage the product, not just the margin." },
  kt: { claim: "Losses weigh roughly twice as heavily as equal gains when people decide under risk.",
    src: "Kahneman & Tversky, Econometrica 47(2), 'Prospect Theory'", year: 1979, url: "https://doi.org/10.2307/1914185", status: "classic",
    caveat: "", use: "Frame the cost of standing still, and remove the risk of paying." },
  bloom: { claim: "Students tutored one-to-one with mastery learning performed about two standard deviations above a conventional class.",
    src: "Bloom, Educational Researcher 13(6), 'The 2 Sigma Problem'", year: 1984, url: "https://doi.org/10.3102/0013189X013006004", status: "classic",
    caveat: "Later replications find smaller effects. The direction holds.", use: "Why mentor review of your own work beats recorded content." },
  ericsson: { claim: "Expert performance comes from deliberate practice on hard tasks with immediate feedback, not from years of experience.",
    src: "Ericsson, Krampe & Tesch-Römer, Psychological Review 100(3)", year: 1993, url: "https://doi.org/10.1037/0033-295X.100.3.363", status: "classic",
    caveat: "", use: "Ten years of experience can be one year repeated ten times." },
  gym: { claim: "Gym members on monthly contracts paid about 70% more per visit than pay-per-visit would have cost them. People overestimate their own future follow-through.",
    src: "DellaVigna & Malmendier, American Economic Review 96(3), 'Paying Not to Go to the Gym'", year: 2006, url: "https://doi.org/10.1257/aer.96.3.694", status: "classic",
    caveat: "", use: "Why accountability to a mentor and a cohort matters more than access to content." },
  challenger: { claim: "In a study of more than 6,000 sales reps, the highest performers were disproportionately those who taught the customer something new about their own business, tailored it, and took control of the conversation.",
    src: "Dixon & Adamson, The Challenger Sale (CEB)", year: 2011, url: "", status: "classic",
    caveat: "Complex B2B sales.", use: "Lead with an insight about their work, not with the program." },
  spin: { claim: "Across 35,000 observed sales calls, success in larger sales tracked with questions about the implications of a problem and the payoff of solving it, not with feature presentation or closing techniques.",
    src: "Neil Rackham, SPIN Selling (Huthwaite)", year: 1988, url: "", status: "classic",
    caveat: "", use: "The question order in the diagnostic call." },
  reactance: { claim: "When people feel pushed toward a conclusion they push back to protect their freedom to choose.",
    src: "Brehm, A Theory of Psychological Reactance", year: 1966, url: "", status: "classic",
    caveat: "", use: "Never tell a prospect they have a gap. Ask the question that lets them say it." },
  spence: { claim: "A credential works as a signal: it lets someone show an ability that others cannot observe directly. Its value depends on how hard it is to get without the ability.",
    src: "Michael Spence, Quarterly Journal of Economics 87(3), 'Job Market Signaling'", year: 1973, url: "https://doi.org/10.2307/1882010", status: "classic",
    caveat: "An economic model, not a study of certificates.", use: "People want something to show. A credential tied to assessed work is a stronger signal than a completion certificate." },
  yuj: { claim: "yuj.dna is a mentor-led program from Yuj Designs, a UX and agentic-AI design consultancy founded in 2009 in Pune. The site reports 412+ professionals enabled, 100+ enterprise clients, 12+ industries.",
    src: "yujdna.com and public company profiles", year: 2026, url: "https://www.yujdna.com/", status: "checked",
    caveat: "The site's own figures, unaudited. It also shows '25+ years of practice' beside '17 years' in the FAQ, which needs one clear explanation.", use: "Proof points, and one thing to fix." }
};
