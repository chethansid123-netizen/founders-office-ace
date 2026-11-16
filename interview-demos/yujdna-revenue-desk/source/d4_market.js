/* Market side: how selling works now, the touchpoint and data map, buyer psychology, competitors, distribution,
   website fixes, automation rule descriptions and integrations. */

Object.assign(EVID, {
  repFree: { claim: "61% of B2B buyers preferred a rep-free buying experience in Gartner's 2024 survey, rising to 67% in the 2025 survey. 73% actively avoid suppliers who send irrelevant outreach. Buyers still want a person when judging whether something fits their situation.",
    src: "Gartner sales surveys (632 and 646 B2B buyers)", year: 2026, url: "https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-sales-survey-finds-61-percent-of-b2b-buyers-prefer-a-rep-free-buying-experience", status: "checked",
    caveat: "B2B purchases. A ₹1.5 lakh personal purchase behaves similarly: people research alone first.", use: "Let people get most of the way on their own, and make the human conversation about fit." },
  sixsense: { claim: "Buyers first contact a seller about 61% of the way through their decision. 94% have ranked their shortlist before that contact, and the vendor they favoured beforehand wins about 80% of the time (82% in the 2026 edition). Vendors not on the first shortlist win under 10%.",
    src: "6sense Buyer Experience Reports 2025 and 2026", year: 2026, url: "https://www.businesswire.com/news/home/20251112018032/en/", status: "checked",
    caveat: "B2B buying groups, vendor research.", use: "The sale is mostly won or lost before the first call. Be known and preferred early." },
  sfdc: { claim: "The average seller spends 40% of their time selling. 55% of sales professionals already use AI for prospecting, and sellers expect agents to cut research time by about a third and email drafting by 36%.",
    src: "Salesforce State of Sales 2026 (4,050 sales professionals)", year: 2026, url: "https://www.salesforce.com/news/stories/state-of-sales-report-announcement-2026/", status: "checked",
    caveat: "Vendor survey; expected savings are self-reported.", use: "Give the admin to AI and the hours back to conversations." },
  aiSearch: { claim: "Between about half and two thirds of US consumers surveyed in 2026 had used an AI assistant to research a purchase (48.5% in one survey, 63.1% in another, up from 49% a year earlier). Google is still where most journeys start.",
    src: "Alchemer 2026 Retail Report; Envision Horizons survey, February 2026", year: 2026, url: "https://martech.org/the-ai-shopping-stats-2026-what-you-need-to-know/", status: "checked",
    caveat: "US consumer surveys with different wording. No India figure found.", use: "Prospects will ask an AI which program to choose. The public facts about yuj.dna need to be clear and consistent." },
  whatsapp: { claim: "India is WhatsApp's largest market at over 500 million users. A defensible read rate for opted-in business messages is around 68%, against roughly 20% opens for email.",
    src: "Industry compilations of Mobilesquared and platform data", year: 2026, url: "https://www.go4whatsup.com/guides/whatsapp-marketing-statistics/", status: "checked",
    caveat: "The often-quoted 98% open rate is a vendor estimate, not a Meta figure.", use: "WhatsApp is the follow-up channel. Opt-in only." }
});

/* How selling works in 2026, and what that changes here. */
const MODERN = [
  { t: "People decide before they talk to you", ev: "sixsense",
    then: "The call was where you informed and persuaded.",
    now: "By the first call they are most of the way through and already have a favourite. The call confirms fit.",
    so: ["Publish what they need to decide alone: cohort dates, fee, payment options, weekly hours, mentor profiles, a casebook sample.", "Put the explain-it self-check in front of them before the call.", "Measure how many leads arrive already knowing the price."] },
  { t: "Irrelevant outreach is punished", ev: "repFree",
    then: "Volume: hundreds of templated messages.",
    now: "Three in four buyers avoid senders of irrelevant messages. One wrong blast costs the account.",
    so: ["Eight to ten hand-written messages a day, each tied to a signal: a funding round, a new role, a hiring post, an AI launch.", "The Accounts view lists companies by recent round for exactly this.", "If you cannot say why this person, why now, do not send."] },
  { t: "AI does the admin, the person does the conversation", ev: "sfdc",
    then: "Reps spent most of the day researching, typing notes and updating records.",
    now: "Sellers still spend only 40% of their time selling. AI can take research, drafting and note-taking.",
    so: ["Use the AI prompts here for the pre-call brief, the recap and the record.", "One tap to log a touch. Nothing is typed twice.", "Judge yourself on conversations held, not messages sent."] },
  { t: "Prospects ask an AI which program to pick", ev: "aiSearch",
    then: "They searched Google and compared brochures.",
    now: "A growing share ask an assistant to compare options. It answers from whatever is public and consistent.",
    so: ["Make the public facts unambiguous: who it is for, duration, fee, what you leave with.", "Fix contradictions (the site says both 17 years and 25+ years).", "Publish mentor-written pieces and named alumni stories that an assistant can cite."] },
  { t: "The conversation lives on WhatsApp", ev: "whatsapp",
    then: "Email sequences and phone tag.",
    now: "In India the reply comes on WhatsApp. Read rates are several times email.",
    so: ["Ask for WhatsApp consent on every form.", "Send short text or a 30-second voice note, never a brochure blast.", "Keep email for the offer and the manager's one-pager."] },
  { t: "Trust travels through people", ev: "challenger",
    then: "The brand carried the proof.",
    now: "People believe a practitioner they follow and a peer who did it. Recommendations move in private groups you cannot track.",
    so: ["Mentors and alumni are the channel. Their posts, their answers in groups.", "Ask 'how did you hear about us' in words, not only by tracking link.", "Give alumni something worth forwarding."] },
  { t: "Try before you buy", ev: "bloom",
    then: "A demo webinar and a brochure.",
    now: "The best predictor of buying is having experienced the value already.",
    so: ["The mentor conversation is the trial. Protect its quality.", "The explain-it check is the self-serve trial.", "Track which of the two each enrolment went through."] },
  { t: "One record, every touch", ev: "hbrLeads",
    then: "Notes in heads, sheets and chat threads.",
    now: "Each touch writes a data point as a by-product of doing the work, so the next decision is obvious.",
    so: ["Every lead carries source, segment, scores, blocker, next step and date.", "The Today view turns those into what to do first.", "See Data → Touchpoints for what is captured where and why."] }
];

/* Touchpoint map: where each data point is captured, how much effort it costs the rep, and the decision it feeds.
   decision keys: who (prioritise), say (personalise), close (predict), price (offer), fix (improve the system). */
const DECISIONS = {
  who: "Who to work on first", say: "What to say to them", close: "Whether and when they will close",
  price: "What offer to make", fix: "What to fix in the funnel"
};
const TOUCHPOINTS = [
  { where: "Any first contact", when: "Lead is created", data: ["Source", "Campaign or referrer", "Date and time"], effort: "Automatic or one tap", feeds: ["fix", "who"], why: "Without source you cannot tell which channel earns its cost." },
  { where: "Form, profile or first message", when: "Lead is created", data: ["Role and segment", "Company and its stage", "City", "Years of experience", "Seniority"], effort: "Typed once", feeds: ["who", "say"], why: "Segment picks the hook and the questions. Company stage predicts who pays." },
  { where: "First response", when: "You call or message", data: ["Minutes from lead to first touch"], effort: "Automatic", feeds: ["fix"], why: "The single most controllable number in the funnel." },
  { where: "Every touch", when: "Call, message, meeting", data: ["Channel", "Outcome", "One-line note"], effort: "One tap plus a line", feeds: ["who", "fix"], why: "Shows which touch number and channel gets replies, and which leads are going cold." },
  { where: "Explain-it self-check", when: "Before a call", data: ["Five self-scores", "Hardest decision they face (their words)"], effort: "Entered by the prospect", feeds: ["say", "who"], why: "The gap in their own words is the best opening line there is." },
  { where: "Explain-it call", when: "First conversation", data: ["Five scores from you", "Their exact sentence", "Trigger event", "Goal for 18 months"], effort: "Five taps and one line", feeds: ["say", "close", "price"], why: "Scores decide the program. The sentence goes into the recap and the offer." },
  { where: "Any hesitation", when: "They stall or object", data: ["Blocker", "Who pays"], effort: "One tap each", feeds: ["say", "price", "fix"], why: "Tells you which play to run now, and across all leads which reason is costing the most seats." },
  { where: "Intent signals", when: "As they happen", data: ["Asked price", "Asked dates", "Shared a work problem", "Attended masterclass", "Brought a colleague", "Asked about employer funding"], effort: "One tap each", feeds: ["who", "close"], why: "These separate curious from deciding." },
  { where: "Mentor conversation", when: "Booked and held", data: ["Booked", "Attended", "Mentor name", "Mentor's read"], effort: "Stage change plus a line", feeds: ["close", "fix"], why: "Show rate and conversion by mentor tell you where the trial works." },
  { where: "Offer", when: "Sent", data: ["Program", "List fee", "Scholarship levers and what each bought", "Payment plan", "Date sent"], effort: "Calculator fills it", feeds: ["price", "close", "fix"], why: "Average discount and days-to-decide are the health of the bottom of the funnel." },
  { where: "Deposit and payment", when: "Paid", data: ["Deposit date", "Plan chosen", "Paid in full date"], effort: "Stage change", feeds: ["close", "fix"], why: "Deposit-to-paid rate shows whether deposits are real commitments." },
  { where: "Lost or nurture", when: "Closed", data: ["True reason", "Call-back date"], effort: "One tap and a date", feeds: ["fix", "who"], why: "The only way to learn. And nurture leads with dates fill the next cohort." },
  { where: "Cohort", when: "Weekly", data: ["Sessions attended", "Work submitted", "Mentor review done"], effort: "Three numbers a learner", feeds: ["fix", "who"], why: "Early warning for drop-off, and the moment to ask for a referral." },
  { where: "End of program", when: "Completion", data: ["Would recommend (0 to 10)", "Result in their words", "Permission to name them", "Two referrals"], effort: "Short form", feeds: ["fix", "say"], why: "Becomes the proof the next prospect asks for." },
  { where: "Spend", when: "Monthly", data: ["Amount by channel"], effort: "One row a channel", feeds: ["fix"], why: "Turns leads by source into cost per learner by source." }
];
const DATA_RULES = [
  "Capture a data point only if it changes one of five decisions. If it does not, it is noise and a reason for the rep to stop logging.",
  "Capture it at the moment it is created, as a by-product of the work. A field filled in later from memory is fiction.",
  "Prefer their words to your summary. 'We assumed the problem was X' is worth more than 'weak on framing'.",
  "Ask for consent and say what it is for. Role, company and phone number are personal data under India's data-protection law. WhatsApp needs explicit opt-in.",
  "Keep one record per person. A second sheet is where follow-ups go to die."
];

/* Buyer psychology: principle, what it predicts about this buyer, how to use it honestly, and the line not to cross. */
const PSYCH = [
  { t: "Unknown unknowns", ev: "dk", predicts: "Capable people will sincerely believe they have nothing to learn.", use: "Never contest it. Ask them to explain one decision step by step.", line: "Do not use the research as an insult." },
  { t: "The explanation test", ev: "ioed", predicts: "Confidence drops on its own when people try to explain how something works.", use: "Build every first call and the self-check around 'walk me through it'.", line: "It is a mirror, not a trap. If they explain it well, say so." },
  { t: "Reactance", ev: "reactance", predicts: "Push, and they push back to keep their freedom to choose.", use: "Ask permission, offer choices, let them name the next step.", line: "No pressure closes, no countdown timers." },
  { t: "Loss aversion", ev: "kt", predicts: "₹1.5 lakh leaving the account feels larger than an uncertain gain.", use: "Reduce the risk of paying (deposit, refund date, instalments) and name the cost of another year unchanged.", line: "Do not frighten people about their jobs." },
  { t: "Price as a signal of quality", ev: "shiv", predicts: "A discounted program is valued less and worked at less.", use: "Hold the price. Give reductions only in exchange for something, and call them scholarships with criteria.", line: "No 'today only' prices." },
  { t: "Commitment and consistency", ev: "gym", predicts: "A small commitment now makes the larger one follow. People also overestimate their future effort.", use: "Seat-block deposit. Mentor and cohort accountability instead of a content library.", line: "Deposits are refundable to a stated date, in writing." },
  { t: "Social proof from peers", ev: "challenger", predicts: "'Someone like me did this' beats any claim from the seller.", use: "One alumnus in the same role, one specific result.", line: "Only real people, with consent." },
  { t: "Something to show", ev: "spence", predicts: "People want a visible marker of what they did: a certificate, a credential, a post. Receiving it is a real pleasure and a reason to buy.", use: "Make the ending an event and the credential specific: signed by a named mentor, tied to their casebook, easy to add to a profile.", line: "Do not imply accreditation or recognition that does not exist." },
  { t: "Identity", ev: "eurich", predicts: "People buy what fits who they believe they are becoming.", use: "Match the segment's words: 'shape direction', 'own a bet', 'second opinion from a peer'.", line: "Do not flatter. Respect is specific." },
  { t: "Authority that is earned", ev: "bloom", predicts: "A practitioner who solves a piece of your problem in 20 minutes is believed.", use: "The mentor conversation, on their real decision.", line: "The mentor advises. The mentor never sells." },
  { t: "Speed as respect", ev: "hbrLeads", predicts: "Interest decays in hours.", use: "First response within the hour, recap within the hour, offer the same day.", line: "Fast is not pushy. One clear next step each time." }
];

/* Culture and attitude: how the buyer should experience the seller. */
const STANCE = [
  { t: "Diagnostician, not pitcher", d: "You are there to find out whether there is a gap worth closing. Sometimes the answer is no, and you say so." },
  { t: "Peer, not counsellor", d: "The edtech 'admission counsellor' script is what these buyers have learned to distrust. Talk like someone who understands their work." },
  { t: "Plain about money", d: "State the fee without apology and the options without spin. People trust the rep who is straight about cost." },
  { t: "Slow to discount, quick to help", d: "Spend effort on the payment problem and the employer conversation, not on the price." },
  { t: "Honest about what is not known", d: "No placement or salary claims. Where outcomes are not yet measured, say so and offer an alumnus instead." },
  { t: "Curious about the no", d: "Every lost lead teaches you a reason. Ask for it, record it, thank them." }
];

/* Competitors. Prices as found on public pages in November 2026; conf says how solid the figure is. */
const COMPETITORS = [
  { n: "ISB Executive Education: Product Management", type: "B-school certificate", price: "₹1,59,900 + GST", conf: "Official page", fmt: "Online, months, large cohort", good: "Brand on a CV.", gap: "Lecture-led at scale. Little review of your own work.", x: 20, y: 30, url: "https://online-er.isb.edu/product-management" },
  { n: "IIM and IIT executive programs", type: "Institute certificate", price: "₹90,000 to ₹1,20,000 + GST", conf: "Third-party listings", fmt: "Online or short residential, 1 to 11 months", good: "Institute name, structured curriculum.", gap: "Academic framing, broad cohorts.", x: 22, y: 26, url: "https://trainings.internshala.com/blog/?p=12507" },
  { n: "upGrad with Duke CE", type: "Edtech certificate", price: "About ₹1,50,000", conf: "Third-party blog", fmt: "Online, recorded plus live", good: "Financing, career services.", gap: "Aimed at switchers. Counsellor-led selling.", x: 28, y: 22, url: "https://futurense.com/blog/best-product-management-courses" },
  { n: "Institute of Product Leadership", type: "Product school", price: "₹90,000 to ₹3,60,000", conf: "Own blog", fmt: "Short executive to 12-month PG", good: "Depth for product careers.", gap: "Longer, career-switch oriented.", x: 40, y: 40, url: "https://www.productleadership.com/blog/product-management-course-fees-in-india/" },
  { n: "HelloPM", type: "PM cohort", price: "₹75,000 incl. GST", conf: "Official site", fmt: "Weekend live, about 3 months, EMI", good: "Strong community, clear price, runs often.", gap: "Entry into PM. Not built for seniors or other functions.", x: 45, y: 38, url: "https://hellopm.co/" },
  { n: "NextLeap", type: "PM fellowship", price: "₹39,999 to ₹49,999", conf: "Conflicting listings", fmt: "Online fellowship with placement support", good: "Low price, placement help.", gap: "Early-career. Volume model.", x: 38, y: 24, url: "https://nextleap.app/course/product-management-course" },
  { n: "Reforge", type: "Membership", price: "About $1,995 a year", conf: "Comparison site", fmt: "Library plus live programs", good: "Operator-written depth, global names.", gap: "Mostly self-paced. US context. No review of your work.", x: 70, y: 28, url: "https://builderscamp.com/compare/reforge-alternatives" },
  { n: "Product School", type: "Certification", price: "$2,999 per certification", conf: "Comparison site", fmt: "Live online", good: "Recognised certificates, AI tracks.", gap: "Certificate-first.", x: 35, y: 34, url: "https://uxcam.com/blog/product-management-courses/" },
  { n: "Maven expert courses", type: "Cohort marketplace", price: "$499 to $2,700", conf: "Comparison site", fmt: "Short live cohorts by individual operators", good: "Current topics, named experts, AI product courses.", gap: "Quality varies. US time zones. Little follow-through.", x: 62, y: 46, url: "https://www.allthingspm.app/blog/best-ai-product-management-courses" },
  { n: "UX bootcamps (DesignBoat, IIM Skills and similar)", type: "Design bootcamp", price: "₹46,000 to ₹1,29,000", conf: "Aggregator pages", fmt: "4 to 7 months, job-oriented", good: "Portfolio and tools for beginners.", gap: "Teaches production, which is the part AI is taking.", x: 15, y: 42, url: "https://fueler.io/blog/best-ui-ux-design-courses-in-india" },
  { n: "GrowthX and paid communities", type: "Community", price: "Not confirmed for 2026", conf: "Old and conflicting", fmt: "Membership, events, peer groups", good: "Network and status.", gap: "Access rather than feedback on your work.", x: 55, y: 30, url: "https://shorts.growthx.club/p/membership-fee-increases-in-2026" },
  { n: "Free content and AI", type: "Do it yourself", price: "₹0", conf: "", fmt: "YouTube, newsletters, asking an assistant", good: "Unlimited, instant.", gap: "No feedback, no accountability. Open courses finish at about one in eight.", x: 50, y: 6, url: "" },
  { n: "yuj.dna", type: "Practitioner mentorship", price: "₹90,000 and ₹1,49,000", conf: "Official site", fmt: "7 and 12 weeks, small cohort, mentor-led", good: "Run by a working consultancy. Your own decisions reviewed. Covers human–AI and agentic design.", gap: "New name. No institute badge. Few named outcomes yet. Site lacks dates, weekly hours and payment options.", x: 86, y: 84, url: "https://www.yujdna.com/", self: true }
];

const DIFFERENTIATION = [
  { t: "Who teaches", d: "People who lead client work at a consultancy that has served enterprises since 2009, not faculty or full-time instructors." },
  { t: "What is reviewed", d: "Your own decisions on a real enterprise challenge, captured in a casebook. Others review assignments; this reviews judgment." },
  { t: "Who it is for", d: "People already in the job who want more say, across product, design, research, business and technology. Not career switchers." },
  { t: "The AI half", d: "A dedicated program on human–AI and agentic systems: where the agent acts, where it escalates, who is accountable. Few alternatives teach this as design." },
  { t: "Size", d: "Small cohorts by design. That is a cost, and the reason for the price." }
];

const SITE_FIXES = [
  { t: "No cohort dates", d: "Buyers decide alone first. Without a date there is nothing to decide by.", fix: "Show the next two start dates and seats remaining." },
  { t: "No payment options", d: "The fee appears with no instalment, EMI or employer route.", fix: "State the options next to the fee." },
  { t: "Weekly time is unclear", d: "'12 weeks' and '30+ hours' appear in different places.", fix: "One line: hours a week, which days." },
  { t: "17 years or 25+ years", d: "The FAQ and the stats block disagree. An AI assistant summarising the site will repeat the confusion.", fix: "Say what each refers to." },
  { t: "Testimonials without employers", d: "Three of five cards show a role but no company.", fix: "Named, with company and one specific result, with consent." },
  { t: "Logos without a caption", d: "A strip of enterprise names with no statement of the relationship.", fix: "'Clients of Yuj Designs' or 'Where our learners work', whichever is true." },
  { t: "No word on a certificate", d: "Many buyers ask what they receive at the end. The site does not say.", fix: "State what is issued, who signs it and how it can be shown." },
  { t: "One form for everyone", d: "Name, phone, email only. You learn nothing that helps the first call.", fix: "Add role, company and 'the hardest decision you face'. Add WhatsApp consent." },
  { t: "No self-serve trial", d: "The only next step is a call.", fix: "The explain-it self-check, and a casebook sample." }
];

const CHANNELS = [
  { n: "Alumni referral", band: "bot", cost: "Scholarship to the friend", why: "Pre-trusted, no acquisition cost.", do: "Week-three ask, two names each.", kpi: "Referrals per learner; share of enrolments" },
  { n: "Mentor-led LinkedIn content", band: "top", cost: "Mentor time", why: "The mentors are the product; their thinking is the advert.", do: "Two decision teardowns a week.", kpi: "Inbound messages from target titles" },
  { n: "Live masterclass", band: "mid", cost: "One mentor hour a month", why: "Earns the strongest intent signal before a call.", do: "One live case, registration asks role and hardest decision.", kpi: "Show rate; calls within 48 hours" },
  { n: "Signal-based outbound to funded startups", band: "top", cost: "Rep time", why: "Recent rounds mean pressure, budget and a reachable founder.", do: "Ten hand-written messages a day from the Accounts list.", kpi: "Conversations per 100 messages" },
  { n: "Explain-it self-check", band: "top", cost: "Build once", why: "Self-discovery, and the best first data point.", do: "One per role, shared in posts and groups.", kpi: "Completions; calls booked from results" },
  { n: "Communities", band: "top", cost: "Rep time", why: "Where people ask each other what is worth paying for.", do: "Be useful in five groups. No links.", kpi: "Inbound by group" },
  { n: "Two-in-a-company team deals", band: "bot", cost: "Team pricing", why: "The startup enterprise motion, built from learners upward.", do: "Manager introduction when a second person appears.", kpi: "Seats per company" },
  { n: "Yuj Designs client relationships", band: "mid", cost: "Internal coordination", why: "Over 100 enterprise clients already trust the parent.", do: "Phase two. Ask account leads for introductions to product and design heads.", kpi: "Introductions; team proposals" },
  { n: "Being the answer in AI assistants", band: "top", cost: "Content and consistency", why: "A growing share of buyers ask an assistant to compare programs.", do: "Clear public facts, comparison page, mentor articles, named stories.", kpi: "Leads saying they found you through an assistant" },
  { n: "Paid social", band: "top", cost: "₹300 to ₹800 a lead by vendor benchmarks", why: "Only after the organic funnel converts, to scale what already works.", do: "Not in the first 60 days.", kpi: "Cost per enrolled learner against target" }
];

/* Automation rules. Logic lives in the app; these are the descriptions and toggles. */
const RULES = [
  { key: "sla", name: "New lead waiting", d: "A new lead has had no first touch within the response target.", act: "Call now, then WhatsApp.", sev: "crit" },
  { key: "overdue", name: "Next step overdue", d: "A dated next step has passed.", act: "Do it or re-date it.", sev: "warn" },
  { key: "stale", name: "Going cold", d: "An open lead has had no touch for the stale limit.", act: "Run the next cadence touch.", sev: "warn" },
  { key: "nostep", name: "No next step", d: "An open lead has no dated next step.", act: "Set one. A lead without a date is not being worked.", sev: "warn" },
  { key: "offer", name: "Offer unanswered", d: "An offer has been out longer than the nudge limit.", act: "Send the blocker question.", sev: "warn" },
  { key: "noblocker", name: "Stalled without a reason", d: "A lead at offer stage, or stuck more than a week, has no blocker tagged.", act: "Ask the confirm question and tag it.", sev: "info" },
  { key: "team", name: "Two from one company", d: "Two or more leads or learners share a company.", act: "Ask for the manager introduction.", sev: "good" },
  { key: "hot", name: "Hot and unbooked", d: "A lead scoring 70 or more has no mentor call yet.", act: "Book the mentor conversation today.", sev: "good" },
  { key: "leak", name: "Stage below target", d: "A stage's conversion is under its target with enough leads to judge.", act: "Open the funnel playbook for that stage.", sev: "info" },
  { key: "pace", name: "Cohort behind pace", d: "Seats filled are behind where they should be for days remaining.", act: "Work the bottom of the funnel first.", sev: "crit" },
  { key: "risk", name: "Learner at risk", d: "An enrolled learner's attendance is under 70% or work is missing.", act: "Call today.", sev: "warn" },
  { key: "refer", name: "Referral ask due", d: "A learner is three weeks in and has not been asked.", act: "Send the week-three ask.", sev: "good" },
  { key: "nurture", name: "Nurture date reached", d: "A parked lead's call-back date has arrived.", act: "Call. Their reason had a date.", sev: "info" }
];

/* Integrations: what works inside this tool today, and what connects when it is opened in Claude. */
const INTEGRATIONS = [
  { n: "Built-in record", state: "on", d: "Leads, touches, accounts, cohorts and spend are stored with this tool. In Claude they sync across your devices; as a file they stay in this browser." },
  { n: "CSV in and out", state: "on", d: "Import leads from any sheet or CRM export. Export leads at any time. That is the bridge to Zoho, HubSpot, Salesforce or Google Sheets without a connector." },
  { n: "Claude, inside the tool", state: "claude", d: "Draft a message for a lead, prepare a pre-call brief, or review the whole pipeline. Uses your own Claude account and asks before the first use." },
  { n: "Gmail drafts", state: "claude", d: "Create a draft to a lead from any template. It lands in your drafts for you to read and send; nothing is sent from here." },
  { n: "Clay company search", state: "claude", d: "Search for more companies by size, industry and location and add them as accounts. Role-level counts need a paid Clay plan." },
  { n: "Ask Claude to update the record", state: "claude", d: "In a Claude conversation you can say 'add these 30 leads' or 'mark the Thursday masterclass attendees' and it writes to this tool's data." },
  { n: "HubSpot or Zoho two-way sync", state: "later", d: "Possible through their connectors once you choose a CRM of record. Until then, CSV keeps them aligned." },
  { n: "WhatsApp Business", state: "later", d: "Templates here are copy-and-send. Automated sending needs an approved WhatsApp Business provider and opt-in records." },
  { n: "Calendar booking", state: "later", d: "Paste your booking link in Setup and it is merged into every message. Creating events directly needs the Calendar connector." },
  { n: "Payments", state: "later", d: "Deposit and instalment status are recorded by hand. A payment-gateway webhook would set them automatically." }
];

/* Who to reach inside a company, by company type. */
const ROLE_MAP = {
  tech:  { label: "Tech and software", segs: ["pm", "ux", "uxr", "dm", "fo", "eng", "pl", "founder"], ratio: "ratioTech" },
  d2c:   { label: "Consumer brand", segs: ["mkt", "ops", "fo", "pm", "founder"], ratio: "ratioD2c" },
  deep:  { label: "Deep tech and hardware", segs: ["pgm", "eng", "fo", "ops", "founder"], ratio: "ratioDeep" },
  health:{ label: "Health and services", segs: ["ops", "pm", "fo", "mkt", "founder"], ratio: "ratioD2c" },
  fin:   { label: "Fintech and financial services", segs: ["pm", "ux", "ops", "fo", "pl", "founder"], ratio: "ratioTech" },
  edu:   { label: "Education", segs: ["pm", "mkt", "ops", "fo"], ratio: "ratioD2c" }
};
const ENTRY_PLAYS = {
  "Seed": "Founder-led. The founder is the buyer and often the learner. Lead with Program 2 and the AI question.",
  "Pre-Series A": "Founder plus first product or design hire. One seat, positioned as building the team's decision method early.",
  "Series A": "Just funded, same team, bigger targets. Message the founder within 30 days of the round and the product and design leads the same week.",
  "Series B": "Functions are forming. Heads of product and design have budgets. Two individual learners, then the team conversation.",
  "Series C+": "Has an L&D process. Enter through individuals paying themselves or with manager approval; aim for a cohort of five.",
  "Scale-up": "Treat as enterprise-lite. Find the head of product or design; offer a pilot of three seats on a real internal problem."
};
