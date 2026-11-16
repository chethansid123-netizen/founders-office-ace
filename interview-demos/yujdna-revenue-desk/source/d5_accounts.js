/* Company universe. Rounds are as published by StartupTalky's 2026 funding tracker and Indexed.vc (read 14-16 Nov 2026).
   Headcount, where present, is from a Clay company search on 16 Nov 2026. Rows:
   [name, stage, amount, month, what they do, location, lead investors, type, headcount|null, flag]
   flag: "" | "est" (stage inferred from total funding, verify) | "tot" (amount is total funding, not this round) */
const ACCOUNT_ROWS = [
  // Series A
  ["AuxoAI", "Series A", "$20.7M", "Oct 2026", "Enterprise AI applications", "India", "NTTVC", "tech", null, ""],
  ["Firstwork", "Series A", "$15M", "Oct 2026", "AI for workforce onboarding", "California / India", "Earlybird Venture Capital", "tech", null, ""],
  ["Cent", "Series A", "$15M", "Oct 2026", "AI-led preventive healthcare", "Karnataka", "Blume Ventures, South Park Commons", "tech", null, ""],
  ["Baba", "Series A", "$40M", "Oct 2026", "Healthcare software", "Haryana", "FirstMark Capital", "tech", null, ""],
  ["Confido Health", "Series A", "$12.5M", "Oct 2026", "Healthcare software", "India", "Z47", "tech", null, ""],
  ["Clinics On Cloud", "Series A", "$14.3M", "Nov 2026", "Health kiosks and software", "Maharashtra", "Model 42", "health", null, ""],
  ["PowerUp Money", "Series A", "$10M", "Nov 2026", "Wealth advice app", "Karnataka", "Flourish Ventures", "fin", null, ""],
  ["Spill Games", "Series A", "$10.5M", "Oct 2026", "Mobile games", "Karnataka", "Elevation Capital", "tech", null, ""],
  ["Clueso", "Series A", "$10M", "Oct 2026", "AI product videos and documentation", "California / Karnataka", "Dharana Capital", "tech", null, ""],
  ["Fission Labs", "Series A", "$10M", "Oct 2026", "Investment technology", "Karnataka", "Pantera Capital", "fin", null, ""],
  ["Lumio", "Series A", "$12M", "Oct 2026", "Consumer electronics brand", "Karnataka", "Blume Ventures", "d2c", null, ""],
  ["Arivihan", "Series A", "$10.2M", "Oct 2026", "AI tutoring for school students", "Madhya Pradesh", "Accel, Prosus", "edu", null, ""],
  ["Mesa School of Business", "Series A", "₹110 Cr (with venture debt)", "Oct 2026", "Business school for startup careers", "Karnataka", "Dharana Capital, Elevation Capital", "edu", 289, ""],
  ["Hunar.AI", "Series A", "$4.2M", "Oct 2026", "AI hiring for frontline roles", "Karnataka", "Blume Ventures", "tech", null, ""],
  ["CapGrid Solutions", "Series A", "$4.87M", "Oct 2026", "Manufacturing sourcing platform", "Haryana", "Nexus Venture Partners", "tech", null, ""],
  ["Greenzo Energy", "Series A", "$13.7M", "Oct 2026", "Energy storage", "Delhi", "Ashish Kacholia", "deep", null, ""],
  ["Quanfluence", "Series A", "$10M", "Oct 2026", "Photonic quantum computing", "Karnataka", "Chiratae Ventures", "deep", null, ""],
  ["Sunfox Technologies", "Series A", "$7M", "Oct 2026", "Portable ECG devices", "Uttarakhand", "Ashish Kacholia, 3one4 Capital and others", "health", null, ""],
  ["KISAH", "Series A", "₹35.9 Cr", "Oct 2026", "Menswear brand", "West Bengal", "Fireside Ventures", "d2c", null, ""],
  ["Rotoris", "Series A", "₹70 Cr", "Nov 2026", "Watch brand", "Haryana", "Blume Ventures", "d2c", null, ""],
  ["altM", "Series A", "$10.3M", "Nov 2026", "Bio-based materials", "Karnataka", "Rainmatter, Mela Ventures", "deep", null, ""],
  ["Let's Game Now", "Series A", "₹30 Cr", "Nov 2026", "Esports platform", "Karnataka", "Anand Mahindra, Bestvantage", "tech", null, ""],
  ["QNu Labs", "Series A", "$21M", "Sep 2026", "Quantum-safe security", "Karnataka", "Speciale Invest", "deep", null, ""],
  ["Yuma Energy", "Series A", "$35M", "Sep 2026", "Battery swapping network", "Karnataka", "Magna", "deep", null, ""],
  ["Provilac", "Series A", "$14M", "Sep 2026", "Dairy brand", "Maharashtra", "Panthera", "d2c", null, ""],
  ["Cradlewise", "Series A", "$12M", "Sep 2026", "Smart cribs", "California / India", "3one4 Capital", "d2c", null, ""],
  ["Trucksup", "Series A", "$8.2M", "Sep 2026", "Trucking marketplace", "Haryana", "Not stated", "tech", null, ""],
  ["Fundly", "Series A", "$4M", "Sep 2026", "Pharmacy supply-chain finance", "Maharashtra", "Accel", "fin", null, ""],
  ["Navana", "Series A", "$4.2M", "Sep 2026", "Voice AI for Indian languages", "Maharashtra", "Antler", "tech", null, ""],
  ["Sol Foundry", "Series A", "$4M", "Sep 2026", "Productivity software", "Karnataka", "General Catalyst", "tech", null, ""],
  ["Disha Health", "Series A", "$4.58M", "Sep 2026", "Health technology", "Karnataka", "General Catalyst", "tech", null, ""],
  ["CURAA", "Series A", "$4.18M", "Sep 2026", "Consumer health products", "Maharashtra", "3one4 Capital", "d2c", null, ""],
  ["Aerchain", "Series A", "Not disclosed", "Sep 2026", "AI procurement software", "Karnataka", "Corporate investor", "tech", 123, ""],
  ["Ringg AI", "Series A", "$30.5M total raised", "Aug 2026", "Voice AI agents", "Bengaluru", "Not shown", "tech", null, "tot"],
  ["Airbound", "Series A", "$75.7M total raised", "Aug 2026", "Autonomous delivery aircraft", "Bengaluru", "Not shown", "deep", null, "tot"],
  ["Peeko", "Series A", "$10.2M total raised", "Aug 2026", "E-commerce software", "Bengaluru", "Not shown", "tech", null, "tot"],
  ["Lissun", "Series A", "$7.1M total raised", "Aug 2026", "Mental health care", "Gurugram", "Not shown", "health", null, "tot"],
  ["Convin", "Series A", "$5M–10M total raised", "Clay, Nov 2026", "AI agents for customer conversations", "Bengaluru", "Kalaari Capital", "tech", 117, "est"],
  ["BiteSpeed", "Series A", "$5M–10M total raised", "Clay, Nov 2026", "Marketing and support suite for e-commerce", "Bengaluru", "Not shown", "tech", 169, "est"],
  ["Trademo", "Series A", "$10M–25M total raised", "Clay, Nov 2026", "Global trade intelligence", "Palo Alto / India", "Saama Capital and angels", "tech", 158, "est"],
  ["Darwix AI", "Series A", "$1M–5M total raised", "Clay, Nov 2026", "Conversation intelligence for sales", "San Francisco / India", "Not shown", "tech", 108, "est"],
  // Series B
  ["Even Healthcare", "Series B", "$50M", "Oct 2026", "Hospitals and managed care", "Bengaluru", "Khosla Ventures", "health", 659, ""],
  ["RapidCanvas", "Series B", "$29M", "Oct 2026", "Enterprise AI platform", "Austin / India", "Vertex Ventures SEA and India", "tech", 123, ""],
  ["Leena AI", "Series B", "Not disclosed", "Oct 2026", "Agentic AI for employee support", "San Francisco / Haryana", "IBM", "tech", 327, ""],
  ["Simplismart", "Series B", "$14M", "Nov 2026", "AI inference infrastructure", "Karnataka", "Dallas Venture Capital", "tech", null, ""],
  ["StockGro", "Series B", "$10.4M", "Oct 2026", "Investment advice and community", "Bengaluru", "BITKRAFT Ventures", "fin", 211, ""],
  ["Boldfit", "Series B", "₹400 Cr", "Oct 2026", "Fitness and activewear brand", "Karnataka", "Bharat Value Fund", "d2c", null, ""],
  ["The Pant Project", "Series B", "₹109 Cr", "Oct 2026", "Custom trousers brand", "Maharashtra", "Mirae Asset Venture Investments", "d2c", null, ""],
  ["Beyond Appliances", "Series B", "₹110 Cr", "Oct 2026", "Kitchen appliances brand", "Karnataka", "Fireside Ventures", "d2c", null, ""],
  ["byteXL", "Series B", "$9M", "Oct 2026", "Tech skilling for colleges", "Telangana", "Elevar Equity", "edu", null, ""],
  ["Troovy", "Series B", "₹100 Cr", "Nov 2026", "Children's food brand", "Haryana", "Fireside Ventures", "d2c", null, ""],
  ["TASE", "Series B", "$31.8M", "Nov 2026", "Manufacturing services", "Tamil Nadu", "ValueQuest", "deep", null, ""],
  ["Navitas Solar", "Series B", "$20M", "Oct 2026", "Solar modules", "Gujarat", "responsAbility", "deep", null, ""],
  ["Comet", "Series B", "$10.2M", "Sep 2026", "Sneaker brand", "Karnataka", "Verlinvest", "d2c", null, ""],
  ["Seeds Fincap", "Series B", "₹100 Cr", "Oct 2026", "Small-business lending", "Haryana", "Michael & Susan Dell Foundation", "fin", null, ""],
  ["Nexedge Capital", "Series B", "$20M", "Sep 2026", "Wealth management", "Delhi", "Mirae Asset Venture Investments", "fin", null, ""],
  ["Zorit", "Series B", "₹27 Cr", "Nov 2026", "B2B e-commerce", "Delhi", "Sparrow Capital", "tech", null, ""],
  ["Balwaan Krishi", "Series B", "₹100 Cr", "Oct 2026", "Farm equipment brand", "Rajasthan", "First Bridge India Growth Fund", "d2c", null, ""],
  ["Sarvam", "Series B", "$25M–50M total raised (Clay)", "Clay, Nov 2026", "Indian-language AI models and agents", "Bengaluru", "Lightspeed, Peak XV, Khosla Ventures", "tech", 477, "est"],
  ["Entropik", "Series B", "$25M–50M total raised", "Clay, Nov 2026", "Emotion-AI consumer research platform", "Bengaluru / US", "Bessemer, SIG", "tech", 95, "est"],
  ["Lucidity", "Series B", "$25M–50M total raised", "Clay, Nov 2026", "Cloud storage automation", "New York / India", "Not shown", "tech", 126, "est"],
  ["Ema", "Series B", "$50M–100M total raised", "Clay, Nov 2026", "Agentic AI employees for enterprises", "San Francisco / India", "Not shown", "tech", 330, "est"],
  // Series C and later
  ["EloElo Group", "Series C+", "$80M (Series C)", "Nov 2026", "Consumer AI and micro-drama apps", "Bengaluru", "Hornbill Capital, NBCUniversal", "tech", 454, ""],
  ["Pixxel", "Series C+", "$100M (Series C)", "Sep 2026", "Hyperspectral earth imaging", "Bengaluru", "Seraphim", "deep", 405, ""],
  ["Ultrahuman", "Series C+", "$65M (Series C)", "Sep 2026", "Health wearables", "Bengaluru", "Qualcomm Ventures", "d2c", 508, ""],
  ["Nua", "Series C+", "$50M (Series C)", "Sep 2026", "Women's wellness brand", "Mumbai", "Peak XV Partners", "d2c", 265, ""],
  ["Mokobara", "Series C+", "$18M (Series C)", "Sep 2026", "Travel gear brand", "Bengaluru", "Sauce", "d2c", 281, ""],
  ["DailyObjects", "Series C+", "₹332 Cr (Series C)", "Oct 2026", "Lifestyle and tech accessories", "Gurugram", "Xponentia, Anicut, Axiom Asia", "d2c", 187, ""],
  ["Battery Smart", "Series C+", "Series C", "Aug 2026", "Battery swapping for electric vehicles", "Gurugram", "Not shown", "deep", 1155, ""],
  ["Darwinbox", "Series C+", "Not disclosed (Series D)", "Sep 2026", "HR software suite", "Hyderabad", "Ontario Teachers' Pension Plan", "tech", 1342, ""],
  ["Slice", "Series C+", "$100M (Series D)", "Sep 2026", "Digital bank", "Karnataka", "Kado Capital", "fin", null, ""],
  ["Simple Energy", "Series C+", "$180M (Series C)", "Oct 2026", "Electric scooters", "Karnataka", "Velumani family office", "deep", null, ""],
  ["Ultraviolette", "Series C+", "$85M (Series E)", "Sep 2026", "Electric motorcycles", "Karnataka", "Yali Capital", "deep", null, ""],
  ["Glance", "Series C+", "Not disclosed (Series D)", "Nov 2026", "Lock-screen content platform", "Karnataka", "L Catterton", "tech", null, ""],
  ["Sugar Cosmetics", "Series C+", "$15.3M (Series D)", "Sep 2026", "Beauty brand", "Maharashtra", "A91 Partners", "d2c", null, ""],
  ["MakeO", "Series C+", "₹90 Cr (Series D)", "Oct 2026", "Dental and skin care", "Maharashtra", "Singularity AMC", "d2c", null, ""],
  ["Nat Habit", "Series C+", "₹142 Cr (Series C)", "Oct 2026", "Fresh personal-care brand", "India", "Trident Growth Partners", "d2c", null, ""],
  ["MATTER", "Series C+", "$25M (Series C)", "Sep 2026", "Electric motorcycles", "Gujarat", "Not stated", "deep", null, ""],
  ["Jar", "Series C+", "$2.63M (tracker label: Series B)", "Sep 2026", "Daily savings in digital gold", "Bengaluru", "Arkam Ventures", "fin", 948, "est"],
  ["HackerEarth", "Series C+", "Stage not verified", "Clay, Nov 2026", "Developer assessment and hiring", "Bengaluru / US", "Not shown", "tech", 523, "est"],
  // Seed and Pre-Series A
  ["Different", "Seed", "$48M", "Oct 2026", "Marketing technology", "California / Karnataka", "General Catalyst", "tech", null, ""],
  ["Matiks", "Seed", "$10M (Pre-Series A)", "Nov 2026", "Mental-maths games", "Karnataka", "General Catalyst", "edu", null, ""],
  ["BioStack", "Seed", "$9.5M", "Nov 2026", "Life-science software", "India", "Peak XV Partners, Afore Capital", "tech", null, ""],
  ["Armatrix", "Seed", "$7.1M", "Nov 2026", "Industrial robot arms", "Karnataka", "Crane Venture Partners", "deep", null, ""],
  ["Parallel Loop", "Seed", "$6.6M", "Oct 2026", "AI applications", "India", "3one4 Capital", "tech", null, ""],
  ["Tradl", "Seed", "$4.1M", "Nov 2026", "Investment technology", "Karnataka", "Nexus Venture Partners", "fin", null, ""],
  ["Zomint", "Seed", "₹36 Cr", "Oct 2026", "Asset management", "Chandigarh", "Lightspeed, Prime Venture Partners", "fin", null, ""],
  ["Desible.ai", "Seed", "₹32 Cr", "Oct 2026", "Conversational AI", "Karnataka", "Prime Venture Partners", "tech", null, ""],
  ["Karta AI", "Seed", "$3M", "Oct 2026", "AI customer service", "Karnataka", "PeerCapital, Cedar Hill Capital", "tech", null, ""],
  ["Vectorial", "Seed", "$3M", "Oct 2026", "AI for product research", "India", "SenseAI Ventures", "tech", null, ""],
  ["Venttup", "Seed", "$3M (Pre-Series A)", "Nov 2026", "Manufacturing services", "Tamil Nadu", "Rainmatter, Unicorn India Ventures", "deep", null, ""],
  ["Circle", "Seed", "₹25 Cr", "Oct 2026", "E-commerce", "Karnataka", "Nexus Venture Partners", "tech", null, ""],
  ["dubdub", "Seed", "$1.3M", "Nov 2026", "Mobile games", "Karnataka", "3one4 Capital, Antler, Stellaris", "tech", null, ""],
  ["Signeasy", "Seed", "Funding not verified", "Clay, Nov 2026", "Contract and e-signature software", "Bengaluru / US", "Not shown", "tech", 65, "est"]
];
const ACCOUNTS = ACCOUNT_ROWS.map(r => ({
  id: "a_" + r[0].toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, ""),
  name: r[0], stage: r[1], amount: r[2], when: r[3], what: r[4], loc: r[5], lead: r[6], type: r[7], hc: r[8], flag: r[9]
}));
const ACCOUNT_STAGES = ["Seed", "Series A", "Series B", "Series C+"];
const STAGE_TYPICAL = { "Seed": "10–40", "Series A": "40–150", "Series B": "150–400", "Series C+": "400+" };

/* Names shown as a logo strip on yujdna.com. The site does not say what the relationship is. Phase two. */
const WARM_ENTERPRISE = ["Honeywell", "Tata", "Verizon", "Wayfair", "ZS", "Amdocs", "Intel", "Ford", "Jio", "PayPal"];

/* Sample workspace: made-up people at made-up companies, so every screen has something on it.
   Row: [name, role, seg, company, coStage, city, src, stage, prog, yrs, sen, payer, blocker, createdDaysAgo, lastTouchDaysAgo,
         firstResponseMins|null, signals, nextText, nextDueInDays|null, diag|null, quote] */
const SAMPLE_ROWS = [
  ["Aarav Menon", "Senior Product Manager", "pm", "Northlane Pay", "Series B", "Bengaluru", "inbound", "new", "p1", 7, "lead", "unknown", "none", 0.05, null, null, [], "Call within the hour", 0, null, ""],
  ["Ishita Rao", "Product Designer", "ux", "Kettle Labs", "Series A", "Pune", "masterclass", "new", "p1", 4, "ic", "unknown", "none", 0.4, null, null, ["masterclass"], "Call: attended Thursday's masterclass", 0, null, ""],
  ["Kabir Sethi", "Founder's Office", "fo", "Loomstack", "Series A", "Gurugram", "linkedin_in", "contacted", "p1", 3, "ic", "unknown", "none", 2, 1, 35, ["replied"], "Explain-it call", 1, null, ""],
  ["Meera Iyer", "UX Researcher", "uxr", "Finch Health", "Series B", "Bengaluru", "referral", "contacted", "p1", 6, "lead", "self", "none", 3, 2, 20, ["replied", "work"], "Explain-it call booked", 0, null, ""],
  ["Rohan Kulkarni", "Program Manager", "pgm", "Orbitline GCC", "GCC / MNC", "Pune", "linkedin_out", "contacted", "p1", 9, "manager", "unknown", "none", 6, 5, 190, [], "Second call, evening", -1, null, ""],
  ["Ananya Bose", "Product Manager", "pm", "Kettle Labs", "Series A", "Pune", "referral", "diagnosed", "p1", 5, "ic", "self", "gap", 8, 2, 15, ["replied", "diagnostic", "work"], "Mentor call with Shaun", 2, { frame: 1, value: 0, decide: 1, influence: 1, own: 0 }, "We assumed drop-off was a pricing problem and never checked."],
  ["Dev Malhotra", "Design Manager", "dm", "Parcelwise", "Series B", "Mumbai", "event", "diagnosed", "combo", 11, "manager", "split", "status", 10, 6, 55, ["replied", "diagnostic"], "Send cohort composition", -2, { frame: 2, value: 1, decide: 1, influence: 0, own: 1, handoff: 0, trust: 1 }, "I can't tell you what design added to revenue last year."],
  ["Sana Qureshi", "Consultant", "consult", "Harbour Advisory", "Services / agency", "Mumbai", "newsletter", "diagnosed", "combo", 5, "lead", "self", "alternatives", 12, 3, 80, ["replied", "diagnostic", "price"], "Send comparison note", 1, { frame: 1, value: 1, decide: 1, influence: 1, own: 1, handoff: 0 }, "Clients now ask for the agent workflow, not the strategy deck."],
  ["Vikram Nair", "Engineering Manager", "eng", "Northlane Pay", "Series B", "Bengaluru", "masterclass", "mentor", "p2", 10, "manager", "employer", "employer", 14, 1, 25, ["replied", "diagnostic", "masterclass", "employer", "work"], "Mentor call Friday 4pm", 1, { spot: 1, workflow: 1, handoff: 0, orchestrate: 1, trust: 0 }, "Honestly the threshold is whatever I set in the pull request."],
  ["Priya Deshmukh", "Product Designer", "ux", "Finch Health", "Series B", "Bengaluru", "referral", "mentor", "p1", 6, "lead", "self", "outcome", 16, 2, 10, ["replied", "diagnostic", "work", "dates"], "Send offer after mentor call", 0, { frame: 1, value: 0, decide: 1, influence: 0, own: 1 }, "I get the brief after the decision is made."],
  ["Arjun Khanna", "Head of Product", "pl", "Kettle Labs", "Series A", "Pune", "partner", "mentor", "combo", 13, "head", "employer", "timing", 9, 4, 40, ["replied", "intro", "employer"], "Team proposal: 3 seats", 3, null, "Two of my PMs asked me about this in the same week."],
  ["Nikita Sharma", "Brand Manager", "mkt", "Saffron & Co", "Series B", "Mumbai", "linkedin_in", "proposal", "p1", 6, "lead", "self", "price", 21, 6, 30, ["replied", "diagnostic", "price", "dates"], "Blocker question: fee or value?", -1, { frame: 1, value: 1, decide: 0, influence: 1, own: 1 }, "The launch hit reach targets and sales didn't move."],
  ["Rahul Verma", "Product Manager", "pm", "Parcelwise", "Series B", "Mumbai", "inbound", "proposal", "p1", 8, "lead", "split", "employer", 18, 2, 12, ["replied", "diagnostic", "price", "employer", "work"], "Three-way call with manager", 2, { frame: 1, value: 1, decide: 1, influence: 0, own: 1 }, "My founder overrode the roadmap twice this quarter."],
  ["Tanvi Joshi", "Operations Manager", "ops", "Quickcart", "Series C+", "Bengaluru", "event", "proposal", "p2", 8, "manager", "employer", "none", 15, 7, 70, ["replied", "diagnostic", "employer"], "Follow up on offer", -2, { spot: 1, workflow: 1, handoff: 0, orchestrate: 0, trust: 1 }, "The bot refunded 40 orders it shouldn't have."],
  ["Farhan Ali", "Founder's Office", "fo", "Northlane Pay", "Series B", "Bengaluru", "referral", "committed", "p1", 4, "ic", "split", "none", 26, 1, 8, ["replied", "diagnostic", "price", "dates", "employer", "work"], "Collect second instalment plan", 4, { frame: 1, value: 1, decide: 0, influence: 1, own: 1 }, "I structure the problem, but I don't choose it."],
  ["Sneha Pillai", "UX Researcher", "uxr", "Loomstack", "Series A", "Gurugram", "masterclass", "committed", "p1", 5, "lead", "self", "none", 30, 3, 18, ["replied", "diagnostic", "masterclass", "price", "dates"], "Balance due before start", 6, { frame: 1, value: 0, decide: 1, influence: 0, own: 1 }, "My last three studies changed nothing."],
  ["Aditya Rao", "Product Manager", "pm", "Finch Health", "Series B", "Bengaluru", "referral", "enrolled", "p1", 6, "lead", "self", "none", 60, 4, 10, ["replied", "diagnostic", "work"], "Week-three referral ask", 0, { frame: 1, value: 1, decide: 1, influence: 0, own: 1 }, ""],
  ["Lavanya Krishnan", "Design Manager", "dm", "Orbitline GCC", "GCC / MNC", "Pune", "partner", "enrolled", "p1", 12, "manager", "employer", "none", 70, 9, 30, ["replied", "diagnostic", "employer"], "Check attendance", -1, { frame: 2, value: 1, decide: 1, influence: 1, own: 1 }, ""],
  ["Karthik Reddy", "Consultant", "consult", "Harbour Advisory", "Services / agency", "Hyderabad", "inbound", "enrolled", "p1", 4, "ic", "self", "none", 65, 2, 22, ["replied", "diagnostic", "price"], "Ask for a named result", 5, { frame: 1, value: 1, decide: 1, influence: 1, own: 0 }, ""],
  ["Pooja Agarwal", "Product Designer", "ux", "Saffron & Co", "Series B", "Mumbai", "linkedin_in", "enrolled", "p1", 5, "ic", "self", "none", 58, 3, 45, ["replied", "diagnostic"], "Mentor review follow-up", 2, { frame: 0, value: 1, decide: 1, influence: 0, own: 1 }, ""],
  ["Manish Gupta", "Technical Program Manager", "pgm", "Orbitline GCC", "GCC / MNC", "Pune", "linkedin_out", "nurture", "p1", 10, "manager", "employer", "timing", 34, 12, 300, ["replied"], "Call after appraisal cycle", 12, null, "Budget opens in April."],
  ["Divya Menon", "Marketing Manager", "mkt", "Quickcart", "Series C+", "Bengaluru", "cold", "lost", "p1", 7, "lead", "self", "fatigue", 40, 20, 600, [], "", null, null, "I have three unfinished courses already."],
  ["Siddharth Jain", "Software Engineer", "eng", "Loomstack", "Series A", "Gurugram", "whatsapp", "lost", "p2", 3, "ic", "self", "price", 28, 15, 240, ["replied", "price"], "", null, { spot: 0, workflow: 1, handoff: 0, orchestrate: 1, trust: 0 }, "Not from my own pocket this year."],
  ["Neha Kapoor", "Co-founder", "founder", "Kettle Labs", "Series A", "Pune", "partner", "contacted", "p2", 9, "head", "employer", "none", 4, 3, 50, ["replied"], "20 minutes on the AI roadmap", 1, null, "The board asked for our AI plan last week."],
  ["Yash Bhatt", "Account Executive", "sales", "Parcelwise", "Series B", "Mumbai", "event", "contacted", "p1", 5, "ic", "unknown", "none", 7, 7, 120, [], "Explain-it call", -3, null, ""],
  ["Ritika Sen", "Senior Product Manager", "pm", "Quickcart", "Series C+", "Bengaluru", "linkedin_in", "diagnosed", "combo", 9, "lead", "self", "time", 11, 4, 28, ["replied", "diagnostic", "work"], "Share a sample week", 0, { frame: 2, value: 1, decide: 1, influence: 1, own: 1, spot: 1, handoff: 0 }, "Twelve weeks on top of a launch is a lot."]
];

function sampleWorkspace(nowMs) {
  const now = nowMs || Date.now(), DAY = 864e5;
  const iso = ms => new Date(ms).toISOString();
  const cohorts = [
    { id: "c_p1_run", sample: true, prog: "p1", name: "Program 1 · running cohort", start: iso(now - 24 * DAY), seats: 25, target: 20 },
    { id: "c_p2_next", sample: true, prog: "p2", name: "Program 2 · next cohort", start: iso(now + 20 * DAY), seats: 25, target: 20 },
    { id: "c_p1_next", sample: true, prog: "p1", name: "Program 1 · next cohort", start: iso(now + 38 * DAY), seats: 25, target: 22 }
  ];
  const leads = SAMPLE_ROWS.map((r, i) => {
    const [name, role, seg, company, coStage, city, src, stage, prog, yrs, sen, payer, blocker, cAgo, tAgo, frm, signals, nextT, nextIn, diag, quote] = r;
    const created = now - cAgo * DAY;
    const last = tAgo == null ? null : now - tAgo * DAY;
    const first = frm == null ? null : created + frm * 6e4;
    const log = [];
    if (first) log.push({ at: iso(first), type: "call", outcome: "Connected", note: "First call. " + (quote ? "Said: " + quote : "Agreed to a short conversation.") });
    if (last && last - first > DAY) log.push({ at: iso(last), type: "whatsapp", outcome: "Replied", note: "Follow-up sent, reply received." });
    const l = {
      id: "s_" + String(i + 1).padStart(2, "0"), sample: true, name, role, seg, company, coStage, city, src,
      email: "", phone: "", linkedin: "", waOptIn: true, yrs, sen, payer, stage, prog, blocker, quote, goal: "",
      signals, diag: diag || {}, next: nextT ? { t: nextT, due: nextIn == null ? "" : iso(now + nextIn * DAY).slice(0, 10) } : { t: "", due: "" },
      offer: null, createdAt: iso(created), firstTouchAt: first ? iso(first) : "", lastTouchAt: last ? iso(last) : "", stageAt: iso(last || created),
      log, lostReason: stage === "lost" ? blocker : "", cohortId: "", health: null
    };
    if (stage === "proposal" || stage === "committed") {
      const levers = name === "Farhan Ali" ? ["referral", "early"] : name === "Rahul Verma" ? ["group"] : [];
      l.offer = { levers, plan: stage === "committed" ? "instalments" : "", sentAt: iso(now - (tAgo + 1) * DAY) };
      l.cohortId = prog === "p2" ? "c_p2_next" : "c_p1_next";
    }
    if (stage === "enrolled") {
      l.cohortId = "c_p1_run";
      l.health = name === "Lavanya Krishnan" ? { att: 50, work: 1, reviews: 0, nps: null, referralAsked: false }
        : name === "Aditya Rao" ? { att: 100, work: 3, reviews: 1, nps: 9, referralAsked: false }
        : name === "Karthik Reddy" ? { att: 83, work: 3, reviews: 1, nps: 8, referralAsked: true }
        : { att: 83, work: 2, reviews: 1, nps: null, referralAsked: false };
    }
    return l;
  });
  const month = iso(now).slice(0, 7);
  const spend = [
    { id: "sp_1", sample: true, month, channel: "masterclass", amount: 15000 },
    { id: "sp_2", sample: true, month, channel: "event", amount: 12000 },
    { id: "sp_3", sample: true, month, channel: "linkedin_out", amount: 8000 },
    { id: "sp_4", sample: true, month, channel: "newsletter", amount: 3000 }
  ];
  return { leads, cohorts, spend };
}
