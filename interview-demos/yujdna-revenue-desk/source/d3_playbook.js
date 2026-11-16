/* The playbook: first principles, funnel stages and plays, outreach cadence, message templates, call structures,
   the blocker taxonomy (why a prospect says no), the payment ladder, scholarship levers, AI prompts and the 90-day plan. */

const PRINCIPLES = [
  { t: "The product is a change in what someone is trusted with", d: "Nobody wants a course. They want to be in the room where direction is set. yuj.dna's own line says it: trusted to deliver, rarely invited to decide. Every message sells that change, and the program is how it happens." , ev: "yuj" },
  { t: "People cannot see a gap in a skill they lack", d: "Judging your own performance uses the same skill as performing. Senior people are the least accurate. So 'I already know this' is the expected first answer, not a rejection.", ev: "dk" },
  { t: "Show the gap, never state it", d: "Telling someone they have a gap makes them defend themselves. Asking them to explain a real decision step by step lets them hear it. The first call is a diagnostic, not a pitch.", ev: "ioed" },
  { t: "There are many reasons for no. Find which one before answering", d: "Not seeing the gap, doubting the outcome, price, course fatigue, time, employer, timing, alternatives, trust and status each need a different answer. Tag the reason on every lead and the tool shows which ones are actually costing seats.", ev: "spin" },
  { t: "Speed and persistence beat polish", d: "A lead answered within the hour is several times likelier to become a conversation. One message is not a sequence: plan nine touches over three weeks across three channels.", ev: "hbrLeads" },
  { t: "Seats are perishable and mentor time is the constraint", d: "An empty seat is worth nothing the day the cohort starts. That argues for filling it, and a discount lowers how much the learner values the program. So price stays, and any reduction buys something specific in return.", ev: "shiv" },
  { t: "Every learner is a channel", d: "A referral arrives pre-trusted. Two learners from one company are the opening for a team conversation with their manager. For startups this is the whole enterprise motion.", ev: "challenger" }
];

/* Blockers: the real reason behind a no. `confirm` is the question that tells you whether this is the one. */
const BLOCKERS = [
  { key: "gap", name: "Cannot see the gap", hear: "'I already know this.' 'I have been doing this for years.'",
    real: "They are competent at delivery and have no way to see what better judgment would look like. This is the default state, not arrogance.",
    confirm: "Ask one explain-it question from their segment. If the answer is fluent on what they did and thin on why it was the right thing, this is the blocker.",
    do: ["Do not argue. Agree they are good at what they do.", "Ask them to walk you through one real decision, step by step.", "Reflect back the one place they said 'I think' or 'we assumed'.", "Offer the mentor call as a second opinion on that one decision."],
    say: "You clearly know the work. I am not suggesting you do not. Can I ask about one decision, the last thing you shipped? ... You said you assumed the problem was X. What would it have cost if that assumption was wrong? That one moment is what our mentors work on, with your real case. Would 20 minutes with one of them on exactly that be useful?",
    proof: "The explain-it score sheet, shared with them. Their own words.", dont: "Quote Dunning–Kruger at them. Say 'you don't know what you don't know'.", ev: ["ioed", "dk", "reactance"] },
  { key: "outcome", name: "Doubts the outcome", hear: "'Will this actually change anything for me?' 'What do people get after this?'",
    real: "They accept there is a gap. They do not believe a program closes it, or that their employer will notice.",
    confirm: "'If it worked exactly as described, what would be different for you in six months?' If they can answer, the doubt is about delivery, not about need.",
    do: ["Make the outcome concrete: the casebook, a decision they will make at work during the program, a named mentor.", "Connect them to an alumnus in the same role.", "Agree a personal success measure and write it into the offer."],
    say: "Fair question, and I would not trust anyone who promised you a promotion. What I can show you is what you leave with: a casebook of your own decisions on a real enterprise problem, reviewed by a practitioner. Let us write down the one thing that would have to be true in six months for this to have been worth it, and you can test that with someone who finished last cohort.",
    proof: "A named alumnus in the same role. A sample casebook page. The mentor's own background.", dont: "Promise salary, promotion or placement. The site makes no such claims, so neither do you.", ev: ["bloom", "ericsson"] },
  { key: "price", name: "Price and risk", hear: "'It is too expensive.' 'I cannot spend ₹1.5 lakh right now.'",
    real: "Two different things hide here. Either they cannot fund it (cash), or they are not yet sure it is worth it (value). Losses weigh about twice as much as gains, so paying feels riskier than standing still.",
    confirm: "'If the fee were not a factor, would you start with this cohort?' Yes means cash. Hesitation means value: go back to the gap or the outcome.",
    do: ["If cash: go to the payment ladder (deposit, instalments, EMI, employer).", "If value: do not discount. Return to the diagnostic.", "Reduce risk, not price: seat-block deposit and a clear refund window."],
    say: "Understood. Let me separate two things. If the fee were not in the way, would you start in this cohort? ... Good, then it is about how to pay, not whether. Most people in your position do one of three things: block the seat with a small deposit and pay in three parts across the program, use a no-cost EMI, or ask their employer to cover part of it. I have a one-page case you can send your manager. Which of those is closest to workable?",
    proof: "The payment options in writing. The employer one-pager.", dont: "Offer a discount to close. It teaches them the price was never real.", ev: ["kt", "fibe", "shiv"] },
  { key: "fatigue", name: "Course fatigue", hear: "'I have done courses. Nothing changed.' 'I have three unfinished ones already.'",
    real: "They are right about most courses. Recorded content has low completion and no feedback. They assume this is the same thing.",
    confirm: "'What was the last one, and what was missing?' Listen for: no feedback, no accountability, not about my real work.",
    do: ["Agree with them about recorded courses.", "Name the three differences in their words: your own work, a mentor who reviews it, a small cohort that expects you.", "Let them sit in on a mentor conversation before deciding."],
    say: "You are right, and the numbers back you: open online courses finish at around one in eight. What was missing in the last one you did? ... That is the difference here. There is no library to get through. You bring a real problem from your work, a practitioner reviews what you did with it, and a small cohort is expecting you on the call. Would you like to speak with a mentor first and judge for yourself?",
    proof: "Completion data. The mentor conversation itself.", dont: "Call it a 'course' at any point.", ev: ["completion", "gym", "bloom"] },
  { key: "time", name: "No time", hear: "'Twelve weeks is a lot.' 'Work is crazy right now.'",
    real: "They are weighing hours against an unclear return. The real question is whether it fits around the job.",
    confirm: "'If it were four hours a week on a problem you already have to solve at work, would that change it?'",
    do: ["State the real weekly load plainly once you have confirmed it internally.", "Tie the applied work to something they must deliver at work anyway.", "Offer Program 2 (7 weeks) as the shorter start where it fits."],
    say: "That is the right thing to check. The applied work is meant to be done on a real problem, so the ideal is that it overlaps with something already on your plate. What is the hardest decision you have to make at work this quarter? ... That could be your case. If the 12 weeks still does not fit, the 7-week Human–AI program is a shorter way in.",
    proof: "A sample week. A learner with a similar job.", dont: "Say 'it is only a few hours' unless you have the real number.", ev: ["gym"] },
  { key: "employer", name: "Wants the employer to pay", hear: "'My company should fund this.' 'I need my manager's approval.'",
    real: "Often genuine and often a way to delay. Either way it is good news: an employer conversation is the door to a team deal.",
    confirm: "'Has your company paid for something like this before, and who approved it?'",
    do: ["Give them the manager one-pager with a business case in the company's own terms.", "Offer a three-way call with the manager.", "Keep the seat with a deposit while approval runs, with a dated check-in."],
    say: "Good, that is worth pursuing. Managers approve this when it is tied to a problem they already own. Let us write the one page together: the decision you will work on during the program, what it is worth to the team, and what you will bring back. I can join a 15-minute call with your manager if that helps. Meanwhile a refundable deposit holds your seat so approval does not cost you the cohort.",
    proof: "Manager one-pager. Invoice in the company's name. Team pricing.", dont: "Wait passively for 'I will check with HR'. Set the date.", ev: ["wef"] },
  { key: "timing", name: "Not now", hear: "'Next cohort.' 'After appraisals.' 'Let me think.'",
    real: "Either a real constraint with a date, or an unresolved blocker they have not named.",
    confirm: "'What will be different by the next cohort?' A specific answer is a real constraint. A vague one means another blocker is underneath.",
    do: ["If real: move to nurture with a dated reason and a deposit option for the next cohort.", "If vague: ask what would have to be true to decide this week.", "State real deadlines only. Never invent scarcity."],
    say: "No problem. What changes between now and the next cohort? ... If it is the appraisal, that makes sense, and I will hold a note to call you on the 10th. If you would rather lock the next cohort now at today's terms, the deposit does that and is refundable until two weeks before the start.",
    proof: "The actual cohort calendar and seat count.", dont: "Fake urgency. 'Only two seats left' is only said when it is true.", ev: ["kt"] },
  { key: "alternatives", name: "Comparing alternatives", hear: "'ISB has one for the same price.' 'There are cheaper ones.' 'I can learn this free with AI.'",
    real: "They are comparing on brand and price because they cannot yet see the difference in what happens inside.",
    confirm: "'What are you comparing it with, and what do you want from either?'",
    do: ["Never run down a competitor. Agree on what each is good for.", "Shift the comparison from content and certificate to who reviews your work.", "For 'free with AI': content is free. Feedback on your judgment is not."],
    say: "ISB is a strong name on a CV, and if the certificate is the main goal that is a reasonable choice. The difference here is who you work with: practitioners from a consultancy that has done this for enterprise clients for 17 years, reviewing your own decisions in a small group. One is a credential, the other is practice with feedback. Which do you need more right now?",
    proof: "The competitor comparison in this tool. A mentor's client work.", dont: "Claim to be better at everything.", ev: ["ericsson", "bloom"] },
  { key: "trust", name: "Does not know yuj", hear: "'I have not heard of yuj.dna.' 'Who runs this?'",
    real: "A new program from a consultancy they may not know. The site has few named outcomes and some testimonial cards without employers.",
    confirm: "'What would you want to see to feel confident about who is behind it?'",
    do: ["Lead with the parent: Yuj Designs, founded 2009, enterprise client work.", "Put a mentor in front of them early.", "Introduce an alumnus.", "Send one piece of the mentors' real thinking, not a brochure."],
    say: "Reasonable. yuj.dna is run by Yuj Designs, a design and AI-experience consultancy that has been working with large enterprises since 2009. The mentors are the people who lead that client work. The simplest way to judge is to spend 20 minutes with one of them on a problem of yours. If that conversation is not useful, you have your answer.",
    proof: "Mentor profiles. Client list as stated on the site (confirm internally which can be named). Alumni.", dont: "Overstate. Use only the numbers on the site until better ones exist.", ev: ["yuj"] },
  { key: "status", name: "Status and ego", hear: "'I am quite senior for this.' 'Is this for juniors?'",
    real: "Being a learner feels like a step down. They need to know who else is in the room and that it is peer-level.",
    confirm: "'Who would you want to be learning alongside?'",
    do: ["Describe the cohort by seniority and employer type.", "Position the mentor as a peer giving a second opinion.", "For heads and directors, lead with their team's capability, then their own seat."],
    say: "It is built for people already doing the job. The cohort is working professionals, and at your level the value is mostly the mentor: a practitioner outside your reporting line who will tell you what your team will not. Most senior people have nobody doing that for them.",
    proof: "Cohort composition. Eurich's finding that accuracy falls with seniority, offered as a general point, never about them.", dont: "Flatter. Or imply they need basics.", ev: ["eurich"] },
  { key: "aifatal", name: "AI will do it anyway", hear: "'AI will do all this in a year.' 'Things change too fast to learn anything.'",
    real: "Anxiety presented as a reason to wait.",
    confirm: "'Which part of your job do you think AI takes first, and which last?'",
    do: ["Agree that production work is being automated.", "Show that judgment about where to trust AI is what the evidence says goes up in value.", "Point to Program 2: it is about exactly this."],
    say: "A lot of it will be automated, yes: drafting, synthesis, first versions. The evidence so far is that people with AI are faster and also more confidently wrong when the task is outside what it does well. So the value moves to the person who can tell the difference and design the work around it. That is the part worth getting good at, and it is what the Human–AI program is about.",
    proof: "The BCG–Harvard study. The METR trial.", dont: "Dismiss the fear, or fuel it.", ev: ["jagged", "metr", "wef"] },
  { key: "cert", name: "Wants a certificate", hear: "'Do I get a certificate?' 'Is it recognised?' 'What can I put on LinkedIn?'",
    real: "They want something to show: to an employer, on a profile, to themselves. That is a legitimate reason to buy, and a real pleasure in finishing. The site does not mention a certificate at all.",
    confirm: "'Who do you want to be able to show it to, and what do you want it to say about you?'",
    do: ["Answer the factual question first, with whatever the program actually issues.", "Then show what is stronger than a certificate: a casebook of their own decisions, reviewed and signed by a named practitioner.", "Describe the moment of finishing: the showcase, the credential, how it appears on a profile."],
    say: "Yes, and I will tell you exactly what you receive. A certificate says you attended. What gets noticed is proof of what you can do. You leave with a casebook of your own decisions on a real enterprise problem, and a credential signed by your mentor that names the capability you demonstrated. Who do you most want to be able to show that to?",
    proof: "A sample credential and a sample casebook page. An alumnus's LinkedIn post.", dont: "Promise recognition the program does not have, or dismiss the wish as vanity.", ev: ["spence", "ericsson"] },
  { key: "none", name: "Not diagnosed yet", hear: "", real: "", confirm: "", do: [], say: "", proof: "", dont: "", ev: [] }
];
const BLK = Object.fromEntries(BLOCKERS.map(b => [b.key, b]));

/* When they want it and are not paying: options in the order to offer them. */
const PAY_LADDER = [
  { t: "Seat-block deposit", d: "A small refundable deposit holds the seat. It turns 'I will think about it' into a decision with a date, and people follow through on commitments they have made.", why: "Commitment and consistency; a smaller first yes.", guard: "State the refund deadline in writing." },
  { t: "Three instalments", d: "Deposit, then two parts tied to program milestones (start, mid-point). No lender, no interest.", why: "Removes the single large outflow, which is what loss aversion reacts to.", guard: "Needs finance sign-off on the schedule." },
  { t: "No-cost EMI through a lender", d: "Six to nine monthly payments via a partner. In a 2025 survey 72% of professionals said EMI would make them willing to upskill.", why: "Matches the cost to monthly salary.", guard: "It is a loan. Name the lender, the tenure and what happens on cancellation. Never push it." },
  { t: "Employer pays or splits", d: "Send the manager one-pager, offer a three-way call, invoice in the company's name.", why: "Opens a team deal and removes the personal cost.", guard: "Set a dated check-in so it does not drift." },
  { t: "Earned scholarship", d: "A reduction in return for something of value: early commitment, a referral, a second seat, a published case, or assessed need.", why: "Keeps the price real and buys something useful.", guard: "From the cohort's scholarship pool, never above the cap." },
  { t: "Next cohort with a deposit", d: "If the constraint is real and dated, lock the next cohort at today's terms.", why: "Keeps the lead without discounting.", guard: "Record the reason and the call-back date." },
  { t: "Let it go", d: "If none fit, say so and stay in touch. A lost lead who was treated well refers others.", why: "Trust is the long-term channel.", guard: "Record the true reason." }
];

/* Scholarship levers. Each is a purchase: the fee reduction buys something worth at least as much.
   maxPct is the most this lever can give; basis says how to work out the right figure. */
const LEVERS = [
  { key: "early", name: "Early commitment", maxPct: 5, basis: "Deposit paid 30 or more days before start. Buys certainty of fill and earlier cash. Worth about what one extra week of selling costs.", buys: "Fill certainty" },
  { key: "referral", name: "Came through an alumnus", maxPct: 8, basis: "No acquisition spend on this seat. Give back up to the acquisition cost saved, never more.", buys: "Acquisition cost saved" },
  { key: "group", name: "Second seat from the same company", maxPct: 10, basis: "One sale, two seats, and the opening for a team deal. 7% for two, 10% for three or more.", buys: "Shared acquisition cost, team-deal entry" },
  { key: "proof", name: "Publishes their case", maxPct: 5, basis: "Agrees in writing to a named testimonial and a public write-up of their casebook project. Buys marketing proof the site currently lacks.", buys: "Named proof" },
  { key: "logo", name: "First learner from a target account", maxPct: 7, basis: "A head-of role or first seat inside a named target company. Buys the door.", buys: "Account entry" },
  { key: "merit", name: "Merit", maxPct: 10, basis: "Top explain-it score or outstanding work sample. Raises the level of the cohort for everyone paying full fee.", buys: "Cohort quality" },
  { key: "need", name: "Assessed need", maxPct: 15, basis: "Self-funded, with income or circumstances that make the fee out of reach. Limited seats per cohort from the pool.", buys: "Access, and the program's reputation for it" }
];

/* Funnel: for each band the objective, how it is measured, and the plays. */
const FUNNEL = [
  { key: "top", name: "Top of funnel", goal: "Turn the right strangers into conversations.", exit: "They replied, registered or asked a question.",
    measure: "New leads a week, share from the 13 segments, cost per lead, reply rate, time to first response.",
    plays: [
      { t: "Decision teardown posts", how: "Twice a week on LinkedIn from the rep and one mentor: one real product decision, what the team assumed, what the evidence said. End with a question, no link.", why: "Teaches before it sells and shows how mentors think.", kpi: "Comments from target titles; profile visits; inbound messages." },
      { t: "The explain-it check as a lead magnet", how: "A five-question self-check per role: 'Can you explain your last decision?' They get their gap map; you get role, company and score.", why: "Lets people find the gap themselves. Captures the most useful data point first.", kpi: "Completions; share with one or more low scores; call bookings from results." },
      { t: "Monthly live masterclass", how: "45 minutes with a mentor on one live case ('Where should the agent stop?'). Registration asks role, company and the hardest decision they face.", why: "Trust in the mentor is the product. Attendance is the strongest intent signal you can earn at this stage.", kpi: "Registrations; show rate; calls booked within 48 hours." },
      { t: "Funded-startup outbound", how: "From the Accounts view: companies that raised a Series A or B in the last 90 days. Message product, design and founder's-office people with a role-specific hook, eight to ten a day, by hand.", why: "Funding means bigger targets on the same team, and a founder who can approve spend.", kpi: "Accept rate; reply rate; conversations per 100 messages." },
      { t: "Alumni referral loop", how: "In week three of each cohort, ask every learner for two names. Offer the referral scholarship to the friend, not cash to the referrer.", why: "A referral arrives pre-trusted and costs nothing to acquire.", kpi: "Referrals per learner; referral share of enrolments." },
      { t: "Community presence", how: "Be useful in four or five product, design and founder's-office groups. Answer questions. Share the teardown posts. Never drop links.", why: "These groups are where the segments ask each other what is worth doing.", kpi: "Inbound from groups; masterclass sign-ups by group." }
    ] },
  { key: "mid", name: "Middle of funnel", goal: "Help them see the gap and want the mentor conversation.", exit: "Mentor call held and the blocker is known.",
    measure: "Contact rate, diagnostic calls held, share scored, mentor calls booked and attended, days in stage.",
    plays: [
      { t: "The explain-it call", how: "A 15-minute first call that is almost all questions. Score five dimensions silently, reflect one gap in their words, offer the mentor call. Structure is in Scripts.", why: "People lower their own confidence when they have to explain step by step. Telling them does the opposite.", kpi: "Calls held; share that book a mentor call." },
      { t: "Gap map in writing within the hour", how: "Send their five scores, the one sentence they said that mattered, and the mentor's name and slot.", why: "Makes the gap theirs and keeps momentum.", kpi: "Reply rate to the recap; mentor-call show rate." },
      { t: "Mentor conversation", how: "20 minutes with a named mentor on one real decision the prospect is facing. Not a pitch. The mentor gives one useful piece of advice.", why: "A sample of the product. Tutoring with feedback is where the learning effect is.", kpi: "Show rate; share moving to offer." },
      { t: "Peer proof", how: "Introduce one alumnus in the same role for a 10-minute chat or a voice note.", why: "Answers 'does it work for someone like me' better than any claim.", kpi: "Intros made; conversion with and without." },
      { t: "Nine-touch cadence", how: "Three channels over three weeks, each touch adding something. The tool tells you which touch is next.", why: "Most replies come after the third touch, and most reps stop at two.", kpi: "Touches per lead; reply by touch number." }
    ] },
  { key: "bot", name: "Bottom of funnel", goal: "Turn intent into a paid seat without discounting the price.", exit: "Deposit paid, then fee paid or plan active.",
    measure: "Offers sent, offer-to-deposit rate, deposit-to-paid rate, days from offer to deposit, discount given, blocker mix.",
    plays: [
      { t: "Offer in writing the same day", how: "One page: the gap in their words, the program, the mentor, dates, fee, payment options, what they leave with, refund terms.", why: "A written offer is a decision to be made. A verbal one is a conversation that continues.", kpi: "Hours from mentor call to offer." },
      { t: "Seat-block deposit", how: "Ask for the deposit on the offer call. Small, refundable to a stated date.", why: "A small commitment makes the larger one consistent.", kpi: "Deposit rate; deposit-to-paid rate." },
      { t: "Diagnose the blocker before answering", how: "Use the confirm question for each blocker. Tag it on the lead. Run that blocker's play.", why: "Price objections are value objections about half the time. Answering the wrong one loses the seat.", kpi: "Share of open offers with a blocker tagged; win rate by blocker." },
      { t: "Employer path", how: "Manager one-pager, three-way call, company invoice. Ask who else on the team would benefit.", why: "Converts one seat into two or three and opens the account.", kpi: "Employer-funded share; seats per company." },
      { t: "Scholarships that buy something", how: "Use the calculator. Each lever is recorded with what it bought, drawn from the cohort pool.", why: "Keeps price integrity and makes every reduction defensible.", kpi: "Average discount; pool used; margin per seat." },
      { t: "Honest deadlines", how: "Cohort start, seat count and deposit refund date are the only deadlines used.", why: "False urgency costs referrals later.", kpi: "Refund requests; complaints." }
    ] },
  { key: "after", name: "After enrolment", goal: "Completion, proof and the next seat.", exit: "Learner finishes, gives a named result, refers or brings a colleague.",
    measure: "Attendance, mentor reviews done, completion, satisfaction, referrals per learner, second seats per company.",
    plays: [
      { t: "First-week call", how: "Ten minutes in week one: is the problem they chose a good one, are they set up.", why: "Early drop-off is decided in the first two weeks.", kpi: "Week-two attendance." },
      { t: "At-risk watch", how: "Two missed sessions or a missed submission raises a flag here. Call the same day.", why: "Cheaper than a refund and protects the cohort.", kpi: "Saves; completion rate." },
      { t: "Week-three referral ask", how: "When they have had their first mentor review, ask for two names.", why: "Enthusiasm peaks after the first real feedback.", kpi: "Names per learner." },
      { t: "Two-in-a-company trigger", how: "When two people from one company are leads or learners, ask for the manager introduction.", why: "This is the team deal, built bottom-up.", kpi: "Manager meetings; team proposals." },
      { t: "A credential worth showing", how: "At completion: a mentor-signed credential that names the capability demonstrated and links to the casebook, a short showcase session, and a ready-made post for LinkedIn.", why: "People want something to show, and finishing should feel like an event. Every post is also an introduction to their network.", kpi: "Share rate; profile visits and leads from alumni posts." },
      { t: "Casebook to case study", how: "With consent, turn the best casebook projects into named stories with a number in them.", why: "The site has few named outcomes. Every cohort should fix that.", kpi: "Published stories per cohort." }
    ] }
];

/* Nine touches over three weeks. band says when it applies. */
const CADENCE = [
  { day: 0,  ch: "call",     t: "Call within the hour", d: "If no answer, WhatsApp within five minutes: who you are, why, one question." },
  { day: 0,  ch: "whatsapp", t: "WhatsApp with one question", d: "The segment hook. No brochure, no link." },
  { day: 1,  ch: "email",    t: "Email: the idea, not the program", d: "The segment's teaching point with its source. Offer the 15-minute explain-it call." },
  { day: 3,  ch: "linkedin", t: "LinkedIn connect with a note", d: "Reference their role and one thing from their profile." },
  { day: 5,  ch: "call",     t: "Second call, different time of day", d: "Leave a voice note on WhatsApp if no answer." },
  { day: 8,  ch: "whatsapp", t: "Send something useful", d: "A teardown post or a masterclass invite matched to their role." },
  { day: 12, ch: "email",    t: "Peer proof", d: "One line from someone in the same role, with permission, and an offer to connect them." },
  { day: 16, ch: "call",     t: "Third call", d: "Ask directly whether this is a 'not now' and when to come back." },
  { day: 21, ch: "whatsapp", t: "Close the loop", d: "Say you will stop messaging, leave the door open, name the next cohort date. Move to nurture." }
];

/* Message templates. Placeholders: {first} {role} {company} {hook} {teach} {source} {rep} {mentor} {program} {price} {deposit} {calendar}. */
const TEMPLATES = [
  { key: "wa_first", stage: ["new"], ch: "whatsapp", name: "First WhatsApp after a missed call",
    body: "Hi {first}, {rep} from yuj.dna here. You asked to speak with a mentor, I just tried calling. One question while we find a time: {hook}" },
  { key: "li_connect", stage: ["new", "contacted"], ch: "linkedin", name: "LinkedIn connect note (under 300 characters)",
    body: "Hi {first}, I work with {role}s at companies like {company} on one thing: getting invited to decide, not only deliver. Would like to connect and ask you one question about how decisions get made on your team." },
  { key: "li_dm", stage: ["new", "contacted"], ch: "linkedin", name: "LinkedIn message after connecting",
    body: "Thanks for connecting, {first}. The question I promised: {hook}\n\nNo pitch. I am collecting answers from {role}s and will share what I am hearing." },
  { key: "em_idea", stage: ["contacted"], ch: "email", name: "Email: lead with the idea", subject: "A question about your last decision at {company}",
    body: "Hi {first},\n\n{teach}\n(Source: {source})\n\nI run a 15-minute call where you walk me through one recent decision and I show you where it scores on five dimensions. People find it useful whether or not they ever join a program.\n\nWould {calendar} work?\n\n{rep}\nyuj.dna" },
  { key: "wa_recap", stage: ["diagnosed"], ch: "whatsapp", name: "Recap after the explain-it call",
    body: "Thanks {first}. Here is what I heard.\n\nStrongest: {strong}\nWorth working on: {weak}\n\nYou said: \"{quote}\"\n\nThat is exactly what {mentor} works on with people. I have held 20 minutes for you: {calendar}. Bring that one decision." },
  { key: "em_mentor", stage: ["diagnosed", "mentor"], ch: "email", name: "Mentor call confirmation", subject: "20 minutes with {mentor} on your decision",
    body: "Hi {first},\n\nConfirming your conversation with {mentor}.\n\nPlease bring one real decision you are facing at {company} in the next month. {mentor} will work through it with you. This is not a presentation about the program.\n\nBefore the call it helps to write three lines: what you are deciding, what you believe today, and what would change your mind.\n\n{rep}" },
  { key: "em_offer", stage: ["mentor", "proposal"], ch: "email", name: "Offer", subject: "Your place in {program}",
    body: "Hi {first},\n\nFollowing your conversation with {mentor}, here is what we discussed in one place.\n\nWhat you want to change: {weak}\nProgram: {program}\nFee: {price}\nTo hold your seat: {deposit} deposit, refundable until two weeks before the start\nHow to pay the rest: in three parts across the program, by no-cost EMI, or through your employer (I can send a one-page case for your manager)\nWhat you leave with: a casebook of your own decisions on a real enterprise problem, reviewed by your mentor\n\nIf anything here is not right for you, tell me which part and we will sort it out.\n\n{rep}" },
  { key: "wa_nudge", stage: ["proposal"], ch: "whatsapp", name: "Offer follow-up that asks for the blocker",
    body: "Hi {first}, checking in on the offer. No pressure either way. If you are hesitating, which is closest: the fee, the time, whether it will change anything, or the timing? Tell me which and I will give you a straight answer." },
  { key: "em_manager", stage: ["proposal", "committed"], ch: "email", name: "One-page case for their manager", subject: "Request: {program} at yuj.dna",
    body: "Hi [manager],\n\nI would like to join a mentor-led program run by Yuj Designs, a design and AI-experience consultancy that has worked with enterprises since 2009.\n\nWhy now: [the decision or initiative I own this quarter]\nWhat I will work on during the program: that same problem, reviewed by a practitioner mentor\nWhat the team gets: [a decision memo / a human–AI workflow design / a tested recommendation] by [date]\nTime: {weeks} weeks alongside work\nCost: {price}. I am asking for [full / part] support.\n\nI will share what I learn with the team in a session afterwards. Could we take 15 minutes to discuss?\n\n{first}" },
  { key: "wa_referral", stage: ["enrolled"], ch: "whatsapp", name: "Week-three referral ask",
    body: "Hi {first}, glad the first mentor review was useful. A favour: who are two people you work with or respect who are in the spot you were in three weeks ago? I would rather speak to people you would vouch for. If they join, they get the referral scholarship." },
  { key: "wa_close", stage: ["contacted", "nurture"], ch: "whatsapp", name: "Close the loop",
    body: "Hi {first}, I have tried a few times and do not want to crowd your inbox, so this is my last message for now. The next cohort starts {cohort}. If the timing is ever right, reply here and I will pick it up. Wishing you well at {company}." }
];

/* Call structures, minute by minute. */
const CALLS = [
  { key: "explain", name: "Explain-it call (first conversation, 15 minutes)", goal: "They hear their own gap. You know the blocker. A mentor call is booked.",
    steps: [
      ["0:00", "Permission and frame", "Thanks for the time. I will ask you about one real piece of work, and at the end I will tell you honestly whether I think we can help. Fair?"],
      ["1:00", "Their context", "What are you working on at the moment, and what would make this year a good one for you?"],
      ["3:00", "Explain-it questions", "Use the five questions for their segment. Ask, then stay quiet. Follow with 'why' or 'how did you know' once each. Score 0 to 2 as you go."],
      ["9:00", "Reflect one gap", "You said '[their words]'. If that assumption had been wrong, what would it have cost? Wait for the answer."],
      ["11:00", "Teach one thing", "Share the segment's teaching point with its source, in two sentences."],
      ["12:00", "Offer the next step", "The useful next step is not a brochure. It is 20 minutes with [mentor], on that one decision. They do this for enterprise clients. Would that be worth your time?"],
      ["13:30", "Book and confirm", "Agree the slot on the call. Say you will send what you heard within the hour."],
      ["After", "Log it", "Scores, their exact sentence, the likely blocker, next step and date. Send the recap."]
    ],
    rules: ["Aim to talk for less than half the call.", "Never say 'you don't know'. Ask the question that lets them say it.", "If all five scores are 2, tell them so. They may be a mentor referral, not a learner."] },
  { key: "mentor", name: "Mentor conversation (20 minutes)", goal: "They experience the product. The mentor gives one piece of real advice.",
    steps: [
      ["0:00", "Mentor asks for the decision", "Tell me what you are deciding and what you believe today."],
      ["3:00", "Mentor probes", "Who is the customer, what is it worth, what would change your mind, who has to agree."],
      ["12:00", "One reframe", "The mentor offers a different way to look at it, from their own client work."],
      ["16:00", "What working together looks like", "Two minutes on how the program would take this problem further."],
      ["18:00", "Rep closes the meeting", "I will send the offer today. Is there anything that would stop you starting with this cohort?"]
    ],
    rules: ["The mentor never sells.", "The rep joins silently and takes the last two minutes.", "Offer goes out the same day."] },
  { key: "offer", name: "Offer call (10 minutes)", goal: "A deposit, or a named blocker with a dated next step.",
    steps: [
      ["0:00", "Summarise in their words", "You want to [their goal]. The gap we found was [their words]. [Mentor] suggested [reframe]."],
      ["1:30", "State the offer once", "Program, dates, fee, what they leave with. Then stop talking."],
      ["3:00", "Ask the deciding question", "Is there anything stopping you from holding your seat today?"],
      ["4:00", "Diagnose the blocker", "Use the confirm question. Do not answer a blocker you have not confirmed."],
      ["7:00", "Run that blocker's play", "Payment ladder for cash. Back to the gap for value. Manager page for employer."],
      ["9:00", "Agree the next step with a date", "Deposit link now, or a specific call-back with what will have happened by then."]
    ],
    rules: ["Say the fee plainly, without apology.", "Silence after the fee is yours to keep.", "No discount to close. Reductions come only from the scholarship levers."] }
];

/* Prompts to use with Claude (inside this tool where connected, or anywhere). */
const AI_PROMPTS = [
  { t: "Research a lead before the call", p: "I am about to call {name}, {role} at {company} ({stage}). From what is publicly known about this company and role, give me: three decisions this person probably owns this quarter, one sentence on what the company is under pressure to do, and two questions that would make them explain a recent decision step by step. No flattery, no pitch." },
  { t: "Turn call notes into a record", p: "Here are my raw notes from a 15-minute call. Return: (1) a score from 0 to 2 for each of: frames the problem, links to business value, decides under uncertainty, influences with evidence, owns the outcome, with one line of evidence each; (2) the single sentence the prospect said that best shows the gap, verbatim; (3) the most likely blocker from this list: cannot see the gap, doubts the outcome, price and risk, course fatigue, no time, wants employer to pay, not now, comparing alternatives, does not know yuj, status, AI will do it anyway; (4) the next step and date. Notes: ..." },
  { t: "Write the recap message", p: "Write a WhatsApp recap under 90 words for {name}. Use their own sentence: '...'. Name one strength and one thing to work on from these scores: ... Offer 20 minutes with {mentor}. Plain language, no hype, no emoji." },
  { t: "Build the manager's one-pager", p: "{name} is a {role} at {company} and wants their employer to fund {program}. They own this problem at work: ... Write a one-page request to their manager: why now, what they will work on, what the team gets and by when, time and cost. Under 200 words. Make no claims about promotion or salary." },
  { t: "Practise an objection", p: "Play a {role} at a {stage} company who has said: '{objection}'. Stay in character, push back realistically, and do not make it easy. After five exchanges, step out and tell me which of my lines worked, which did not, and what the real blocker probably was." },
  { t: "Weekly pipeline review", p: "Here is my pipeline as a table. Tell me: the three leads to call first today and why, the stage where I am losing the most people compared with target, the blocker that appears most often and what to change in my approach, and whether the cohort will fill at the current pace. Be direct." }
];

/* Ninety days, week by week. */
const PLAN90 = [
  { w: "Week 1", focus: "Get the facts", items: ["Confirm with the team: cohort dates, seat caps, GST, refund terms, EMI partner, discount authority.", "Listen to five recent sales conversations or read the notes.", "Interview five alumni: why they joined, what nearly stopped them, what changed.", "Fill in Setup → Assumptions with real numbers."] },
  { w: "Week 2", focus: "Build the base", items: ["Import every existing lead. Tag segment, source and stage.", "Publish the first explain-it check for product managers and designers.", "Agree the mentor-call rota: who, which slots, how many a week.", "Write the offer page and the manager one-pager with real terms."] },
  { w: "Weeks 3–4", focus: "Start the top of the funnel", items: ["Two decision-teardown posts a week from you and one mentor.", "Ten hand-written messages a day to people at companies funded in the last 90 days.", "Announce the first masterclass.", "Call every new lead within the hour. Log every touch."] },
  { w: "Weeks 5–6", focus: "Run the middle", items: ["15 explain-it calls a week.", "Recap within the hour, mentor call within five days.", "Tag a blocker on every lead that stalls.", "First masterclass. Call every attendee within 48 hours."] },
  { w: "Weeks 7–8", focus: "Close the first cohort", items: ["Offers out the same day as mentor calls.", "Deposits on the offer call.", "Use scholarship levers only from the pool.", "First review: conversion by stage against target, blocker mix, cost per source."] },
  { w: "Weeks 9–10", focus: "Fix the biggest leak", items: ["Change one thing at the stage losing the most people. Measure for two weeks.", "Drop the worst source, double the best.", "Start the week-three referral ask in the running cohort.", "Publish the first named alumni story."] },
  { w: "Weeks 11–13", focus: "Open the team motion", items: ["Every company with two leads or learners: ask for the manager introduction.", "Three founder or product-head conversations at funded startups.", "Draft team pricing with the leadership.", "Write up what worked as the standard playbook for the next hire."] }
];

/* Open questions for the user. Each has a working assumption so nothing is blocked. */
const QUESTIONS = [
  { k: "authority", q: "How much discount can you give without approval, and who approves above that?", why: "Sets the cap in the scholarship calculator.", assume: "20% total cap, anything below 35% margin needs approval." },
  { k: "seats", q: "What is the real seat cap per cohort, and when do the next cohorts start?", why: "Drives fill pace, deadlines and how many leads you need.", assume: "25 seats. Dates entered by you in Cohorts." },
  { k: "gst", q: "Are the fees on the site inclusive of GST?", why: "Changes the number you say on the offer call and the employer invoice.", assume: "Shown as listed; GST not added." },
  { k: "refund", q: "What are the refund and deferral terms?", why: "The seat-block deposit and risk-reversal lines depend on it.", assume: "Deposit refundable until two weeks before start." },
  { k: "emi", q: "Is there a lending partner for EMI today?", why: "The third rung of the payment ladder.", assume: "Not yet; instalments offered first." },
  { k: "mentors", q: "How many mentor conversations a week can the four mentors give to prospects?", why: "This is the real ceiling on the middle of the funnel.", assume: "Eight a week in total." },
  { k: "format", q: "Is delivery online, in person in Pune, or mixed? Weekdays or weekends?", why: "Decides which cities to target and how to answer 'no time'.", assume: "Online, weekend-led, so all India." },
  { k: "load", q: "What is the real weekly time commitment?", why: "The site says '30+ hours of guided learning'; prospects will ask for hours per week.", assume: "Four to five hours a week." },
  { k: "alumni", q: "Which alumni will take a call from a prospect, and which results can be named?", why: "Peer proof is the strongest answer to 'will it work for me'.", assume: "None named yet; collect five in week one." },
  { k: "clients", q: "Which Yuj Designs clients can be named in sales conversations?", why: "The site shows logos without saying what the relationship is.", assume: "Use only what the site states until confirmed." },
  { k: "cert", q: "What do learners receive at the end: a certificate, a credential, who signs it, can it be verified online?", why: "Prospects ask, and the site says nothing. Many people buy partly for something they can show.", assume: "A mentor-signed credential linked to the casebook. Confirm before saying it." },
  { k: "history", q: "Where did the 412 past learners come from, and what converted them?", why: "Your real funnel numbers replace every benchmark in this tool.", assume: "Unknown; benchmarks used." },
  { k: "team", q: "Is there existing team or company pricing?", why: "Needed for the two-in-a-company play.", assume: "7% for two seats, 10% for three or more." },
  { k: "tools", q: "Which tools are already in use: CRM, WhatsApp Business, calendar, payments?", why: "Decides what to connect first.", assume: "None; this tool is the system of record." },
  { k: "budget", q: "Is there any marketing budget, and for what?", why: "Sets cost per lead targets and whether paid channels are an option.", assume: "No paid spend in the first 60 days." },
  { k: "target", q: "What is your enrolment target for the next cohort and the next quarter?", why: "The funnel calculator works backwards from it.", assume: "Fill one Program 1 and one Program 2 cohort." },
  { k: "yours", q: "In your own conversations so far, which reason for 'no' have you heard most?", why: "You said there may be many reasons. Your first guess, then the data, will show which matter.", assume: "Unknown. The tool starts counting from your first tagged lead." }
];
