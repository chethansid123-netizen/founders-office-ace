/* Thirteen buyer segments. For each: the job they are paid for, the root problem, what they believe versus what the
   evidence says, when they buy, how they see themselves, how to open, what to ask on the call, and which program fits.
   `pairs` rows are [what they believe, what is true, evidence key]. `prompts` rows are [call question, DIAG key it scores]. */

const SEGMENTS = [
  {
    key: "pm", name: "Product manager", group: "core", prog: "p1",
    titles: ["Product Manager", "Senior Product Manager", "Associate Product Manager", "Product Owner", "Growth Product Manager"],
    job: "Decide what gets built and prove it mattered.",
    root: "The roadmap is set by the loudest stakeholder and the PM becomes a delivery coordinator. Writing specs is no longer scarce, AI drafts them. What is scarce is choosing which problem deserves the quarter and defending that choice with evidence.",
    pairs: [
      ["I ship on time, so I am a strong PM.", "Shipping is not impact. In controlled tests only about one idea in three moves the metric it was built to move.", "kohavi"],
      ["I know my users, I talk to them.", "Most teams validate solutions, not problems. Around 80% of features are rarely or never used.", "pendo"],
      ["I already use AI for specs and research.", "So does everyone. People using AI are confidently wrong on tasks outside its ability. Knowing where to trust it is the skill.", "jagged"]
    ],
    triggers: ["Passed over for Senior or Group PM", "A new manager who keeps asking 'why this?'", "Founder overruled the roadmap", "Told to do more with fewer PMs because of AI", "Appraisal season (March to April, September to October)"],
    identity: { sees: "The person who should be choosing the bets.", wants: "A seat in the room where direction is set.",
      say: "Sharper product judgment, reviewed by people who do this for enterprise clients.", avoid: "'Course', 'training', 'upskilling', 'basics'." },
    hooks: [
      "Of the last five things your team shipped, how many moved the number they were meant to? Most PMs I ask say 'not sure', and that is the actual problem.",
      "When your founder overrules the roadmap, what do you do next? That moment is what we work on.",
      "AI writes the spec now. What is left is the call on what to build. How are you getting better at that call?"
    ],
    prompts: [
      ["Walk me through the last thing you shipped. What was the customer problem, and how did you know it was the right one for this quarter?", "frame"],
      ["Which business number was it meant to move, by how much, and what happened?", "value"],
      ["Tell me about a call you made with incomplete data. What would have changed your mind?", "decide"],
      ["When a senior stakeholder disagreed, what evidence did you bring and what happened?", "influence"],
      ["After launch, what did you learn that changed the next decision?", "own"],
      ["Where do you want to be in 18 months, and what stands between you and that?", null]
    ],
    teach: "About two ideas in three do not move their metric even at Microsoft. The PMs who get promoted are not the ones who ship more; they are the ones who are right more often about what to build, and can show why.",
    teachEv: "kohavi",
    fitWhy: "Program 1 maps one-to-one to the gap: framing, business value, decisions under uncertainty, influence, ownership. Add Program 2 if they own an AI feature.",
    channels: ["LinkedIn", "PM WhatsApp and Slack groups", "Product meetups in Bengaluru, Pune, Gurugram", "Alumni referrals", "Newsletter"],
    blockers: ["gap", "alternatives", "time"],
    search: '("product manager" OR "senior product manager" OR "product owner") AND India'
  },
  {
    key: "ux", name: "UX and product designer", group: "core", prog: "p1",
    titles: ["Product Designer", "UX Designer", "Senior Product Designer", "Interaction Designer", "UI/UX Designer"],
    job: "Make the product work for the people who use it, and for the business that pays for it.",
    root: "Designers are briefed after the decision is made. They polish a solution to a problem nobody tested. As AI generates competent screens in seconds, the craft of producing them is losing its price. What keeps its price is deciding what should exist and arguing for it in business terms.",
    pairs: [
      ["My craft and my portfolio speak for themselves.", "Only the top quarter of companies on design maturity out-grow their peers. The rest get no reward for good-looking work.", "mckDesign"],
      ["Business people just do not get design.", "Design gets heard when it is argued in revenue, cost and risk. That is a learnable skill, and few designers have been taught it.", "mckDecide"],
      ["AI cannot do what I do.", "AI already does the production part. It makes average output cheap, which moves the value to judgment.", "jagged"]
    ],
    triggers: ["Handed a finished brief once too often", "Design team cut or merged into product", "Passed over for Lead", "Asked to 'add AI' to a flow with no guidance", "A PM or founder rejected work for 'business reasons'"],
    identity: { sees: "A problem-solver who is treated as a pixel-producer.", wants: "To be invited to decide, not only to deliver.",
      say: "Moving from executing briefs to shaping them.", avoid: "'UI course', 'Figma', 'tools', anything that sounds like a bootcamp." },
    hooks: [
      "When was the last time you changed what got built, rather than how it looked? If that is rare, it is not a talent problem. It is a language problem.",
      "yuj's own line fits most designers I speak to: trusted to deliver, rarely invited to decide. Does that land?",
      "AI now gets you to a decent screen in a minute. So what is the designer for? I would like your answer, then I will share how our mentors answer it."
    ],
    prompts: [
      ["Pick a recent project. Who decided this was the problem to solve, and what was your part in that decision?", "frame"],
      ["How did the business know your design worked? Which number, and who tracked it?", "value"],
      ["Tell me about a time you had to choose between two directions without research to settle it.", "decide"],
      ["When product or engineering pushed back, what did you put on the table besides the design?", "influence"],
      ["What happened to that work three months after it shipped?", "own"],
      ["If your manager described your impact in one sentence, what would they say? What would you want them to say?", null]
    ],
    teach: "McKinsey tracked 300 companies: only the top quarter on design maturity grew faster, and the other three quarters looked the same as each other. Design is rewarded when it is tied to business decisions. That is a way of working, not a style.",
    teachEv: "mckDesign",
    fitWhy: "Program 1 gives the business and decision language. Program 2 is the growth track: designing human–AI workflows is where new design work is appearing.",
    channels: ["LinkedIn", "Design communities and meetups", "Portfolio platforms", "Alumni designers", "yuj's design-led content"],
    blockers: ["gap", "fatigue", "price"],
    search: '("product designer" OR "ux designer" OR "interaction designer") AND India'
  },
  {
    key: "dm", name: "Design manager or lead", group: "core", prog: "combo",
    titles: ["Design Manager", "Lead Product Designer", "Head of Design", "Design Director", "UX Lead"],
    job: "Get a design team to produce outcomes the business values, and earn the team a say in direction.",
    root: "They were promoted for craft and now need influence. Their team is measured on output, so it is the first budget questioned. They must show design changes results, and decide how AI changes the shape of the team.",
    pairs: [
      ["My team's work is strong, so our value is obvious.", "Value is obvious only when someone ties it to a number. Most design leaders are never asked to and never learn to.", "mckDesign"],
      ["I manage people, I do not need more training.", "Self-assessment gets less accurate with seniority, not more.", "eurich"],
      ["We will add AI when the tools settle.", "Over 40% of agentic-AI projects are expected to be cancelled. The teams that survive are the ones that design where AI acts and where it stops.", "gartner"]
    ],
    triggers: ["Headcount review", "A new product head who wants proof of design's impact", "Asked to lead the AI experience strategy", "Design reporting line moved under product"],
    identity: { sees: "A leader fighting for their function.", wants: "Peer standing with product and engineering heads.",
      say: "Leadership judgment, and a method your whole team can run.", avoid: "Anything aimed at juniors." },
    hooks: [
      "If your CEO asked tomorrow what design added to revenue last year, what would you send them?",
      "How is your team deciding where AI should act on its own in your product and where a person must step in? Most teams have not written that down.",
      "One of our mentors runs design for a 17-year consultancy. The question they hear most from design heads is 'how do I prove it'. Is that yours too?"
    ],
    prompts: [
      ["How does your team decide what to work on this quarter? Who else is in that decision?", "frame"],
      ["What does the business believe design contributed last year? How do they know?", "value"],
      ["Tell me about a bet your team made that could have gone either way.", "decide"],
      ["When did you last change a product or business decision above your level? How?", "influence"],
      ["Which of your team's outcomes do you personally answer for?", "own"],
      ["Where in your product is AI acting without a human today, and who decided that was safe?", "handoff"]
    ],
    teach: "Self-awareness research across nearly 5,000 people found accuracy falls with seniority, because fewer people give senior people honest feedback. A mentor outside your reporting line is the cheapest fix there is.",
    teachEv: "eurich",
    fitWhy: "Combo. Program 1 for the influence and evidence case; Program 2 because design heads are being handed AI experience strategy. Also the natural buyer for two or three of their own team.",
    channels: ["LinkedIn", "Design leadership circles", "Referral from a team member in the cohort", "Yuj Designs client relationships"],
    blockers: ["status", "time", "employer"],
    search: '("design manager" OR "head of design" OR "design lead" OR "design director") AND India'
  },
  {
    key: "uxr", name: "UX researcher", group: "core", prog: "p1",
    titles: ["UX Researcher", "User Researcher", "Senior UX Researcher", "Research Lead", "Design Researcher"],
    job: "Reduce the risk of building the wrong thing.",
    root: "Research is asked for after the decision, to confirm it. Findings land in a deck nobody acts on. AI now transcribes, clusters and summarises interviews, so synthesis is no longer the scarce part. Framing the question that a decision depends on, and getting that decision changed, is.",
    pairs: [
      ["My research is rigorous, so it has impact.", "Rigor is not impact. Six in ten managers say most of their decision time is wasted, and research that arrives after the decision cannot fix that.", "mckDecide"],
      ["Stakeholders ignore research because they do not value it.", "They ignore findings that do not say what to do, by when, and what it is worth.", "challenger"],
      ["AI synthesis is shallow, my job is safe.", "AI output is good enough inside its range and wrong outside it. The researcher who knows the boundary becomes more valuable; the one who only synthesises does not.", "jagged"]
    ],
    triggers: ["Research team shrunk or 'democratised'", "A study that changed nothing", "Asked to evaluate an AI feature with no method for it", "Moving from researcher to strategist"],
    identity: { sees: "The person who actually knows the user.", wants: "To be the one decisions wait for.",
      say: "From insight to decision: research that changes what the company does.", avoid: "'Learn research methods'. They know methods." },
    hooks: [
      "Think of your last three studies. Which one changed a decision that was already half-made? If the answer is none, the method was fine. The framing was not.",
      "Now that AI can cluster 40 interviews in minutes, where do you add the most value? I ask every researcher this and the answers split cleanly in two.",
      "How do you test whether users trust an AI feature enough to act on it? Few teams have a method. We teach one."
    ],
    prompts: [
      ["Take your last study. What decision was it meant to inform, and who owned that decision?", "frame"],
      ["What was that decision worth to the business if it went right or wrong?", "value"],
      ["When the evidence was mixed, what did you recommend, and how sure were you?", "decide"],
      ["Tell me about a finding a stakeholder did not want to hear. What did you do?", "influence"],
      ["Did you follow what happened after they acted on it?", "own"],
      ["How would you study whether people trust an AI recommendation in your product?", "trust"]
    ],
    teach: "The illusion of explanatory depth: people are sure they understand something until asked to explain it step by step. Stakeholders feel that way about their users. Your job is to run that test on their assumptions, which is a decision skill, not a research method.",
    teachEv: "ioed",
    fitWhy: "Program 1, because the gap is influence and business framing, not method. Program 2 if they are studying AI features: trust and accountability are research problems.",
    channels: ["LinkedIn", "Research communities", "Conference talks", "Alumni"],
    blockers: ["gap", "outcome", "price"],
    search: '("ux researcher" OR "user researcher" OR "design researcher" OR "research lead") AND India'
  },
  {
    key: "pl", name: "Product leader", group: "buyer", prog: "combo",
    titles: ["Head of Product", "Director of Product", "VP Product", "Group Product Manager", "Chief Product Officer"],
    job: "Make the whole product team's bets pay off.",
    root: "They have hired smart people who ship, and still most bets miss. They cannot review every decision. They need the team to frame problems and argue trade-offs the way they would, and they need a view on AI that is more than a pilot.",
    pairs: [
      ["My team needs to move faster.", "Speed is rarely the constraint. Decision quality is: only one in five managers say their organisation is good at it.", "mckDecide"],
      ["We run AI pilots, we are on it.", "95% of organisations studied saw no measurable return from generative-AI pilots. The cause was workflow design, not the model.", "nanda"],
      ["Good people learn on the job.", "Years of experience do not build expertise. Deliberate practice with feedback does.", "ericsson"]
    ],
    triggers: ["A missed annual target", "New funding round with a hiring freeze: 'do more with the same team'", "Board asking for the AI plan", "Two strong PMs or designers asking for growth"],
    identity: { sees: "The owner of the product's direction.", wants: "A team that needs less of their time and makes better calls.",
      say: "Raising the decision quality of your team without adding headcount.", avoid: "Selling them a seat. Sell them the team outcome." },
    hooks: [
      "How many of your team's decisions last quarter would you have made differently? What does that gap cost you in a year?",
      "After your round, the board will ask what AI does to the roadmap and the team. What is your answer today?",
      "Two people from your team in one cohort, working on a real problem from your product, reviewed by our mentors. Would that be worth 20 minutes to explore?"
    ],
    prompts: [
      ["Where do your team's decisions most often go wrong: the problem chosen, the evidence, or the follow-through?", "frame"],
      ["How do you currently grow a strong PM or designer into someone who can own a bet?", "own"],
      ["What is your position on where AI acts alone in your product?", "handoff"],
      ["Who on your team would you send first, and what would you want back?", null],
      ["Is there a learning budget, and who signs it off?", null]
    ],
    teach: "MIT's 2025 study of enterprise AI found 95% of organisations saw no measurable return, and the reason was not the model. It was that nobody redesigned the work around it. That is a capability your team either has or does not.",
    teachEv: "nanda",
    fitWhy: "Buyer for two to five seats. Start with one or two people in Program 1, add Program 2 for whoever owns AI features.",
    channels: ["Warm intro through a learner on their team", "LinkedIn", "Founder and product-leader dinners", "Yuj Designs relationships"],
    blockers: ["employer", "outcome", "timing"],
    search: '("head of product" OR "vp product" OR "director of product" OR "chief product officer") AND India'
  },
  {
    key: "fo", name: "Founder's office and strategy", group: "core", prog: "p1",
    titles: ["Founder's Office", "Chief of Staff", "Strategy Associate", "Business Strategy Manager", "Entrepreneur in Residence"],
    job: "Turn the founder's priorities into outcomes across teams, without authority over any of them.",
    root: "They are generalists judged on results they do not control. They are handed ambiguous problems, expected to structure them in a day, and to get product, design and engineering to move. Nobody taught them how products are actually decided, so they manage by spreadsheet and escalation.",
    pairs: [
      ["I am a strong problem-solver, that is why I was hired.", "Structuring a problem on a slide is not the same as choosing the right problem with users and constraints in view.", "ioed"],
      ["I get things done through the founder's name.", "Borrowed authority runs out. Evidence is the only influence that scales, and six in ten managers say decision time is mostly wasted.", "mckDecide"],
      ["AI makes me faster, so I am fine.", "The study that showed the AI lift was run on consultants like you. They were also 19 points more likely to be wrong when the task sat outside AI's range.", "jagged"]
    ],
    triggers: ["First year in the role ending, wants a function to own", "Asked to run a product or AI initiative", "Founder says 'own this end to end'", "Planning a move into product"],
    identity: { sees: "Future founder or business head.", wants: "To be trusted with a real bet, not a tracker.",
      say: "The product and decision skills that turn a generalist into someone who can own a business line.", avoid: "Anything that sounds like a design course." },
    hooks: [
      "When the founder gives you a vague problem on Monday, what is your process by Wednesday? Most people in your role have never been shown one.",
      "You sit between product, design and business without owning any of them. Where does that go wrong most often?",
      "The BCG–Harvard AI study was run on people very like you. The headline was the speed-up. The part that matters is where they got it wrong. Want the two-minute version?"
    ],
    prompts: [
      ["Take a problem the founder handed you recently. How did you decide what the real problem was?", "frame"],
      ["What was it worth to the business, and how did you size that?", "value"],
      ["Where did you have to commit before the data was in?", "decide"],
      ["How did you get a team that does not report to you to change course?", "influence"],
      ["What did you personally own at the end, and what happened?", "own"],
      ["What do you want your next role to be?", null]
    ],
    teach: "People rate their understanding highly until they have to explain it step by step. Founders do this with their own product decisions. The founder's-office person who can run that test calmly, with evidence, becomes the person the founder cannot do without.",
    teachEv: "ioed",
    fitWhy: "Program 1. It gives a generalist the product-decision method they were never taught. Strong referral source: they sit next to the founder who signs team deals.",
    channels: ["LinkedIn", "Founder's-office communities", "B-school alumni groups", "Startup WhatsApp groups"],
    blockers: ["alternatives", "employer", "time"],
    search: '("founder\'s office" OR "chief of staff" OR "strategy manager" OR "entrepreneur in residence") AND India'
  },
  {
    key: "pgm", name: "Program and project manager", group: "adjacent", prog: "p1",
    titles: ["Program Manager", "Technical Program Manager", "Project Manager", "Delivery Manager", "Scrum Master"],
    job: "Land complex work on time across teams.",
    root: "They are measured on delivery of scope they did not choose. When the scope is wrong they still own the delay. Scheduling and status reporting are being automated. The durable version of the role questions the scope, sees the business risk early and brings options.",
    pairs: [
      ["On time and on scope is success.", "On time with the wrong thing is failure that looks like success. Two ideas in three do not move their metric.", "kohavi"],
      ["Deciding what to build is not my job.", "It becomes the job at the next level. Analytical thinking is the skill most employers now call essential.", "wef"],
      ["Agents will handle the tracking and I will manage the agents.", "Over 40% of agentic-AI projects are forecast to be cancelled. Someone has to decide where the agent acts and where it escalates.", "gartner"]
    ],
    triggers: ["Wants to move into product", "Role re-scoped as tools automate reporting", "Handed an AI rollout", "GCC or delivery org pushing 'ownership'"],
    identity: { sees: "The reliable one who holds it together.", wants: "To be seen as a decision-maker, not a coordinator.",
      say: "From managing delivery to owning outcomes.", avoid: "'PM certification'. They have certificates." },
    hooks: [
      "How often do you deliver exactly what was asked and still watch it miss? What would it take for you to be the one who catches that early?",
      "A lot of program managers want to move into product. The gap is rarely knowledge. It is practice at making the call. How are you getting that practice?",
      "If an agent did your status reporting tomorrow, what would you spend the time on?"
    ],
    prompts: [
      ["Think of a program that delivered but disappointed. When could you first have known?", "frame"],
      ["What was the business case for it, in numbers? Who owned that?", "value"],
      ["Tell me about a trade-off you made between scope, time and quality without sign-off.", "decide"],
      ["How do you get a team to change scope when they are sure they are right?", "influence"],
      ["What do you track after go-live?", "own"]
    ],
    teach: "The World Economic Forum's employer survey puts analytical thinking first among skills employers need, ahead of any tool. Delivery skill gets you hired. Judgment about what to deliver gets you the next role.",
    teachEv: "wef",
    fitWhy: "Program 1 is the bridge into product ownership. Program 2 if they run AI or automation rollouts.",
    channels: ["LinkedIn", "GCC and services alumni networks", "PM-transition communities"],
    blockers: ["gap", "alternatives", "price"],
    search: '("program manager" OR "technical program manager" OR "delivery manager") AND India'
  },
  {
    key: "mkt", name: "Brand and marketing manager", group: "adjacent", prog: "p1",
    titles: ["Brand Manager", "Marketing Manager", "Growth Manager", "Category Manager", "Product Marketing Manager"],
    job: "Grow demand profitably and build a brand people choose.",
    root: "Campaigns are judged on reach and clicks while the business asks about revenue. Content and creative are now abundant because AI makes them. The scarce part is knowing the customer well enough to choose what to say, to whom, and proving it worked.",
    pairs: [
      ["I know my consumer.", "Most teams know their segment's demographics, not the problem the product is hired for. Ask them to explain the buying decision step by step and the gaps show.", "ioed"],
      ["The campaign performed.", "Performance against a metric you chose is easy. Most tested ideas do not move the business metric.", "kohavi"],
      ["AI gives me ten times the content.", "It gives everyone ten times the content. Selection and judgment become the whole job.", "jagged"]
    ],
    triggers: ["Budget cut with the same target", "Moving from brand to product or business role", "Launch that under-delivered", "Asked to own customer experience end to end"],
    identity: { sees: "The voice of the customer in the company.", wants: "A P&L or product role.",
      say: "Customer problems and business value, the way product leaders work with them.", avoid: "'Marketing course'." },
    hooks: [
      "If I asked you to explain, step by step, how your customer decides to buy, where would you start guessing? Most marketers find the guess is earlier than they thought.",
      "Your last launch: which business number moved because of it, and how do you know it was the launch?",
      "Now that everyone can produce endless content with AI, what makes your choices better than a competitor's?"
    ],
    prompts: [
      ["Take your last campaign or launch. What customer problem was it built on, and how did you establish that?", "frame"],
      ["Which business number was it accountable to?", "value"],
      ["Where did you have to choose between two audiences or messages without a clear test?", "decide"],
      ["How do you win budget or roadmap space from product or sales?", "influence"],
      ["What did you change after you saw the results?", "own"]
    ],
    teach: "At Microsoft, with all its data, two ideas in three still fail to move their metric. Marketing is no different. The managers who rise are the ones who frame the customer problem properly before spending.",
    teachEv: "kohavi",
    fitWhy: "Program 1, sold as the route from marketing into product and business ownership. Stronger fit in consumer brands and product-led startups.",
    channels: ["LinkedIn", "D2C founder and marketer communities", "Brand events", "Alumni"],
    blockers: ["outcome", "alternatives", "price"],
    search: '("brand manager" OR "product marketing manager" OR "growth manager" OR "category manager") AND India'
  },
  {
    key: "sales", name: "Sales and business development", group: "adjacent", prog: "p1",
    titles: ["Business Development Manager", "Account Executive", "Key Account Manager", "Enterprise Sales Manager", "Customer Success Manager"],
    job: "Win and grow customers.",
    root: "They sell features to buyers who want outcomes. The best reps diagnose the customer's business problem better than the customer can, and that is a product-thinking skill. Most are trained on pitch and process only.",
    pairs: [
      ["I close because I build relationships.", "In a study of 6,000 reps, top performers were the ones who taught customers something about their own business.", "challenger"],
      ["I know the customer's needs, they tell me.", "Stated needs are not the real problem. Success in large sales tracks with implication questions, not presentations.", "spin"],
      ["More talk time means more control.", "Won deals have less rep talk time than lost ones.", "gong"]
    ],
    triggers: ["Moving to enterprise or solution selling", "Selling an AI product they cannot explain", "Wants to move to product, founder's office or a GM role", "Quota missed on larger deals"],
    identity: { sees: "The revenue engine.", wants: "To be the strategic advisor the customer calls first.",
      say: "Diagnose a customer's business the way a consultant does.", avoid: "'Sales training'." },
    hooks: [
      "In your last lost deal, what was the customer's real problem, in their numbers? If you are not sure, that is why it was lost.",
      "Top reps teach the customer something about their own business. What did you teach your last prospect?",
      "You are selling an AI product. Can you explain to a CFO where it acts alone and who is accountable when it is wrong?"
    ],
    prompts: [
      ["Take a deal you are working. What is the customer's business problem, in their words and their numbers?", "frame"],
      ["What is solving it worth to them? How did you establish that?", "value"],
      ["Where did you have to decide whether to walk away?", "decide"],
      ["How do you move a buying committee that disagrees with itself?", "influence"],
      ["What happens to the account after you close?", "own"]
    ],
    teach: "Rackham watched 35,000 sales calls. In large deals, pitch and closing technique barely mattered. What mattered was asking about the consequences of the problem. That is problem framing, the first thing Program 1 trains.",
    teachEv: "spin",
    fitWhy: "Program 1 for consultative depth. Smaller segment; best when they sell a product or AI solution and want a path beyond quota-carrying.",
    channels: ["LinkedIn", "SaaS sales communities", "Referral from product colleagues"],
    blockers: ["gap", "outcome", "employer"],
    search: '("enterprise sales" OR "account executive" OR "business development manager" OR "customer success manager") AND SaaS AND India'
  },
  {
    key: "ops", name: "Operations manager", group: "adjacent", prog: "p2",
    titles: ["Operations Manager", "Business Operations Manager", "Process Excellence Lead", "City or Category Operations Head", "Customer Experience Manager"],
    job: "Run the process at lower cost and higher reliability every quarter.",
    root: "They are being told to automate with AI agents and are accountable when the automation fails a customer. Nobody has shown them how to decide which steps an agent should own, where a person must approve, and how to keep trust when it goes wrong.",
    pairs: [
      ["Automation is an IT project.", "The failures are in workflow design, which operations owns. 95% of organisations saw no measurable return from AI pilots for that reason.", "nanda"],
      ["We will pilot an agent and scale it.", "Over 40% of agentic projects are expected to be cancelled on cost, unclear value or risk.", "gartner"],
      ["I know my process inside out.", "Ask anyone to write down every decision in their process and who makes it. The gaps appear within minutes.", "ioed"]
    ],
    triggers: ["AI or automation target in the annual plan", "A bot or agent that embarrassed the company", "Headcount freeze with rising volume", "Moving from running operations to designing them"],
    identity: { sees: "The person who makes things actually work.", wants: "To design the system, not firefight it.",
      say: "Designing operations where people and AI each do what they are good at.", avoid: "'Design course', 'UX'." },
    hooks: [
      "In your process, which decisions would you let an AI agent make alone today, and which never? Most ops heads have not drawn that line, and their vendor is drawing it for them.",
      "When your bot gets it wrong, who finds out first: you or the customer?",
      "Gartner expects 40% of agent projects to be cancelled. Want the three questions that predict which ones?"
    ],
    prompts: [
      ["Pick one process you want to automate. Which outcome are you actually trying to improve?", "spot"],
      ["Walk me through it step by step. Who decides what today?", "workflow"],
      ["Where must a person approve before the system acts?", "handoff"],
      ["Which other systems and teams does it touch, and what happens when they disagree?", "orchestrate"],
      ["When it fails, who is accountable and how does the customer find out?", "trust"]
    ],
    teach: "MIT found that almost all enterprise AI pilots returned nothing measurable, and the reason was workflow, not the model. Operations people are the ones best placed to fix that, once they have a method for it.",
    teachEv: "nanda",
    fitWhy: "Program 2 first: seven weeks, directly on the mandate they have been given. Program 1 later if they move toward product or business roles.",
    channels: ["LinkedIn", "Operations and CX communities", "Company intros", "Startup operator groups"],
    blockers: ["employer", "gap", "time"],
    search: '("operations manager" OR "business operations" OR "process excellence" OR "customer experience manager") AND India'
  },
  {
    key: "eng", name: "Engineer and tech lead", group: "adjacent", prog: "p2",
    titles: ["Frontend Engineer", "Software Engineer", "Tech Lead", "Engineering Manager", "AI Engineer", "Solutions Architect"],
    job: "Build what was decided, well.",
    root: "They are building AI features with no specification for how the AI should behave toward a person: when it acts, when it asks, how it shows uncertainty, who is accountable. Front-end and full-stack engineers are making those product decisions by default, in code.",
    pairs: [
      ["AI tools make me much faster.", "In a controlled trial, experienced developers were 19% slower with AI and believed they were 20% faster.", "metr"],
      ["Product decides behaviour, I implement it.", "For AI features, the behaviour is the implementation. If you do not design the hand-off, you have still decided it.", "gartner"],
      ["A better model will fix it.", "The failures were workflow and integration, not model quality.", "nanda"]
    ],
    triggers: ["Leading the first agent or copilot feature", "Promotion to tech lead or engineering manager", "A demo that worked and a rollout that did not", "Wants to move toward product or architecture"],
    identity: { sees: "The one who actually builds it.", wants: "To be the engineer product and design trust with the hard calls.",
      say: "Designing how an AI system behaves with people, as rigorously as you design its architecture.", avoid: "'Soft skills', 'design thinking workshop'." },
    hooks: [
      "In the AI feature you are building, where is the line between the model acting and a person approving, and who drew it? If the answer is 'me, in a pull request', that is worth a conversation.",
      "There is a randomised trial where experienced developers were 19% slower with AI and felt 20% faster. Want to see what explained the gap?",
      "Your agent demo works. What happens the first time it is confidently wrong in front of a customer?"
    ],
    prompts: [
      ["Take the AI feature you are closest to. What user or business outcome is it for?", "spot"],
      ["Step by step, what does the model do and what does the person do?", "workflow"],
      ["When does it stop and ask? Who decided that threshold?", "handoff"],
      ["Which systems does it call, and what happens when one is wrong or slow?", "orchestrate"],
      ["How does the user know how far to trust an answer?", "trust"]
    ],
    teach: "METR ran a proper randomised trial: experienced developers, real repositories. With AI they were 19% slower and sure they had been faster. It is a small study, but it is the clearest demonstration that people misjudge their own performance with these tools.",
    teachEv: "metr",
    fitWhy: "Program 2. Seven weeks on the exact decisions they are already making without a method. Position as systems design for human–AI products, not as a design course.",
    channels: ["LinkedIn", "Engineering meetups", "Developer communities", "Referral from product and design colleagues"],
    blockers: ["status", "alternatives", "gap"],
    search: '("frontend engineer" OR "tech lead" OR "engineering manager" OR "ai engineer") AND India'
  },
  {
    key: "consult", name: "Consultant and business analyst", group: "core", prog: "combo",
    titles: ["Consultant", "Senior Consultant", "Business Analyst", "Digital Transformation Consultant", "Product Consultant"],
    job: "Tell a client what to do and help them do it.",
    root: "Research, analysis and slide production are exactly what AI does well, so clients ask why they are paying for hours. What clients still pay for is judgment about their specific business and someone who can design the change, including the AI part.",
    pairs: [
      ["My structured thinking is the product.", "The Harvard–BCG study ran on 758 consultants. AI lifted the weakest performers most. Structure is being commoditised.", "jagged"],
      ["I advise on AI, so I understand it.", "Advising on AI strategy and designing a workflow where AI and people share work are different skills. Most pilots return nothing measurable.", "nanda"],
      ["Experience makes me senior.", "Expertise comes from practice with feedback, not years.", "ericsson"]
    ],
    triggers: ["Client asked for an AI-agent solution and the team had no method", "Manager promotion case", "Leaving consulting for a product or strategy role", "Firm pushing 'AI-first delivery'"],
    identity: { sees: "The smartest person in most rooms.", wants: "To be the consultant clients ask for by name.",
      say: "The casebook: your judgment on real enterprise problems, reviewed by practitioners.", avoid: "Anything implying they lack fundamentals." },
    hooks: [
      "The Harvard study on AI and knowledge work was run on BCG consultants. The speed-up made the headlines. The 19-point drop in accuracy on the wrong kind of task did not. Which side of that line is your current project on?",
      "When a client asks you to design an agent workflow, not a strategy for one, what is your method?",
      "Two of the people in our testimonials are consultants at EY and Deloitte. I can tell you what they came in for."
    ],
    prompts: [
      ["Take a current engagement. How did you decide what the client's real problem was, versus the brief?", "frame"],
      ["What is the outcome worth to them, and how did you size it?", "value"],
      ["Where did you make a recommendation the data did not fully support?", "decide"],
      ["How did you move a client stakeholder who disagreed?", "influence"],
      ["If the client wanted AI in that process, where would it act alone and where not?", "handoff"],
      ["What do you want to be known for in two years?", null]
    ],
    teach: "In the BCG experiment, consultants using AI on the right tasks produced about 40% better work. On a task just outside AI's range they were 19 points more likely to be wrong, and could not tell. The valuable consultant is the one who can tell.",
    teachEv: "jagged",
    fitWhy: "Combo. Program 1 sharpens the product and decision side; Program 2 gives a method for the agent work clients are now asking for. The site's testimonials already include consultants.",
    channels: ["LinkedIn", "Consulting alumni networks", "B-school groups", "Referrals"],
    blockers: ["status", "alternatives", "price"],
    search: '("consultant" OR "senior consultant" OR "business analyst") AND ("digital" OR "product" OR "experience") AND India'
  },
  {
    key: "founder", name: "Founder and CXO", group: "buyer", prog: "p2",
    titles: ["Founder", "Co-founder", "CEO", "COO", "Chief Business Officer", "Head of People"],
    job: "Make the company's few big bets right, with the team they have.",
    root: "After a round, hiring slows and expectations rise. The founder is the bottleneck on every product decision because the team frames problems differently from them. They also owe the board an AI plan that is more than a demo.",
    pairs: [
      ["My team is strong, they just need direction.", "If every decision needs your direction, the team has not been taught how to decide. Only one in five managers say their organisation is good at decisions.", "mckDecide"],
      ["We have AI features in the product.", "95% of organisations saw no measurable return from AI pilots. The difference was workflow design.", "nanda"],
      ["Training is a perk for later.", "Employers name skill gaps as the main barrier to transformation.", "wef"]
    ],
    triggers: ["Just closed a Series A or B", "Hiring freeze", "Board asked for the AI roadmap", "A senior hire did not work out", "Two team members ask for the same program"],
    identity: { sees: "The builder.", wants: "A team that makes good calls without them.",
      say: "Two or three of your people, your real problem, 7 to 12 weeks, mentor-reviewed.", avoid: "'Corporate training', 'L&D'." },
    hooks: [
      "Congratulations on the round. The next 18 months are the same team with bigger targets. Which two people, if they made better calls, would take the most off your plate?",
      "How many product decisions waited on you last month? What would it be worth to halve that?",
      "Your board will ask where AI acts alone in your product and who is accountable. Do you have that written down?"
    ],
    prompts: [
      ["Which decisions still come back to you that should not?", "frame"],
      ["Where is AI in your roadmap, and what is it meant to change in the numbers?", "spot"],
      ["Where does it act without a person today?", "handoff"],
      ["Who are the two or three people you would bet on?", null],
      ["How do you usually approve spending like this, and by when would you want them started?", null]
    ],
    teach: "MIT's study found the 5% of companies getting real value from AI were not the ones with better models. They were the ones that redesigned the work. That is a people capability, and it can be built in a quarter.",
    teachEv: "nanda",
    fitWhy: "Buyer for a small team. Lead with Program 2 (AI mandate, shorter), then Program 1 for their product and design leads.",
    channels: ["Warm intro through a learner", "Investor and founder networks", "LinkedIn after a funding announcement", "Founder dinners"],
    blockers: ["timing", "outcome", "trust"],
    search: '("founder" OR "co-founder" OR "ceo") AND ("series a" OR "series b") AND India'
  }
];

const SEG = Object.fromEntries(SEGMENTS.map(s => [s.key, s]));
