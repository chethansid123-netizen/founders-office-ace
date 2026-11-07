/* Ten single-image Instagram posts for YourDOST (1080 x 1350), English only.
   Every post: YourDOST logo, one of YourDOST's own blog section labels, a 1–2 line message,
   a line-art visual in the logo's style, and the "Talk to a certified expert, 24/7" CTA. */
(function (root) {
  "use strict";
  const K = "#111214", Y = "#fed13c", C = "#dd4224", W = "#ffffff", P = "#f8d9d3";

  // a tangled scribble, like the left head in the logo (deterministic)
  function scribble(cx, cy, r, turns = 26, seed = 7) {
    let s = seed;
    const rnd = () => ((s = (s * 9301 + 49297) % 233280) / 233280);
    let d = `M${cx} ${cy}`;
    for (let i = 0; i < turns; i++) {
      const a1 = rnd() * 6.283, a2 = rnd() * 6.283, a3 = rnd() * 6.283;
      const r1 = r * (0.3 + 0.7 * rnd()), r2 = r * (0.3 + 0.7 * rnd()), r3 = r * (0.2 + 0.8 * rnd());
      d += ` C${(cx + r1 * Math.cos(a1)).toFixed(1)} ${(cy + r1 * Math.sin(a1)).toFixed(1)} ${(cx + r2 * Math.cos(a2)).toFixed(1)} ${(cy + r2 * Math.sin(a2)).toFixed(1)} ${(cx + r3 * Math.cos(a3)).toFixed(1)} ${(cy + r3 * Math.sin(a3)).toFixed(1)}`;
    }
    return d;
  }

  const V = {
    diya: () => `
      <svg class="svgart" viewBox="0 0 560 420" width="560" height="420">
        <circle cx="280" cy="150" r="150" fill="${W}" opacity=".35"/>
        <circle cx="280" cy="150" r="96" fill="${W}" opacity=".5"/>
        ${[[-120, -10], [-96, -84], [-34, -128], [34, -128], [96, -84], [120, -10]].map(([x, y]) => `<path d="M${280 + x * 0.78} ${150 + y * 0.78} L${280 + x} ${150 + y}" stroke="${K}" stroke-width="8" stroke-linecap="round"/>`).join("")}
        <path d="M280 52 C322 104 334 152 280 200 C226 152 238 104 280 52 Z" fill="${C}" stroke="${K}" stroke-width="8" stroke-linejoin="round"/>
        <path d="M280 112 C298 138 302 160 280 184 C258 160 262 138 280 112 Z" fill="${W}"/>
        <path d="M100 236 L460 236 Q428 380 280 380 Q132 380 100 236 Z" fill="${K}" transform="translate(16 16)"/>
        <path d="M100 236 L460 236 Q428 380 280 380 Q132 380 100 236 Z" fill="${W}" stroke="${K}" stroke-width="8" stroke-linejoin="round"/>
        <ellipse cx="280" cy="236" rx="182" ry="28" fill="${Y}" stroke="${K}" stroke-width="8"/>
        <path d="M280 200 L280 232" stroke="${K}" stroke-width="7" stroke-linecap="round"/>
        ${[200, 280, 360].map((x, i) => `<circle cx="${x}" cy="${i === 1 ? 318 : 298}" r="13" fill="${C}" stroke="${K}" stroke-width="6"/>`).join("")}
        <path d="M150 282 Q170 300 186 286 M224 304 Q246 324 266 312 M296 312 Q316 324 338 304 M376 286 Q392 300 410 282" fill="none" stroke="${K}" stroke-width="6" stroke-linecap="round"/>
      </svg>`,

    marksheet: () => `
      <div class="card sheet">
        <div class="t">STATEMENT OF MARKS · 2026</div>
        <p class="nm">NAME OF CANDIDATE: <b>RIYA SHARMA</b></p>
        <div style="margin-top:12px">
          <div class="row"><span>English</span><span>94</span></div>
          <div class="row"><span>Mathematics</span><span>95</span></div>
        </div>
        <div class="tot"><span>AGGREGATE</span><strong>92.4%</strong></div>
      </div>`,

    phone: () => `
      <div class="card phone">
        <div class="scr">
          <div class="bar"><div class="av">?</div><div class="who"><b>Don't.</b><small>last seen today at 11:47 pm</small></div></div>
          <div class="msgs">
            <span class="day">14 SEPTEMBER</span>
            <div class="b">ok.</div>
            <div class="b me">take care ❤️</div>
            <span class="day">TODAY</span>
          </div>
          <div class="type">You won't believe what happened today 😂<span class="caret"></span></div>
        </div>
      </div>`,

    heart: () => `
      <svg class="svgart" viewBox="0 0 560 440" width="520" height="408">
        <path d="M280 410 C130 316 46 232 46 146 C46 82 98 38 160 38 C214 38 256 70 280 112 C304 70 346 38 400 38 C462 38 514 82 514 146 C514 232 430 316 280 410 Z" fill="${Y}" transform="translate(18 18)"/>
        <path d="M280 410 C130 316 46 232 46 146 C46 82 98 38 160 38 C214 38 256 70 280 112 C304 70 346 38 400 38 C462 38 514 82 514 146 C514 232 430 316 280 410 Z" fill="${P}" stroke="${K}" stroke-width="9" stroke-linejoin="round"/>
        <path d="M280 112 L256 170 L296 226 L262 286 L292 344 L280 404" fill="none" stroke="${K}" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>
        ${[[150, 254, 178], [206, 274, 216], [262, 266, 284], [318, 266, 336]].map(([y, x1, x2], i) => `<path d="M${(i % 2 ? 250 : 236)} ${y - 14} L${(i % 2 ? 312 : 300)} ${y + 14}" stroke="${C}" stroke-width="9" stroke-linecap="round"/>`).join("")}
      </svg>`,

    laptop: () => `
      <svg class="svgart" viewBox="0 0 680 440" width="640" height="414">
        <path d="M606 34 A70 70 0 1 0 662 150 A56 56 0 1 1 606 34 Z" fill="${W}" stroke="${K}" stroke-width="8" stroke-linejoin="round"/>
        <text x="548" y="70" font-family="Poppins" font-weight="800" font-size="34" fill="${K}">z</text>
        <text x="520" y="40" font-family="Poppins" font-weight="800" font-size="26" fill="${K}">z</text>
        <rect x="124" y="74" width="440" height="282" rx="24" fill="${K}"/>
        <rect x="108" y="58" width="440" height="282" rx="24" fill="${W}" stroke="${K}" stroke-width="8"/>
        <rect x="140" y="90" width="376" height="218" rx="12" fill="${Y}" stroke="${K}" stroke-width="6"/>
        <text x="172" y="156" font-family="Poppins" font-weight="800" font-size="38" fill="${K}">Task complete</text>
        <rect x="172" y="184" width="312" height="26" rx="13" fill="${W}" stroke="${K}" stroke-width="5"/>
        <rect x="172" y="184" width="312" height="26" rx="13" fill="${K}"/>
        <path d="M176 262 L194 280 L226 244" fill="none" stroke="${K}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
        <text x="240" y="276" font-family="Lato" font-weight="900" font-size="30" fill="${K}">in 40 seconds</text>
        <path d="M56 352 L600 352 L636 398 Q640 412 624 412 L32 412 Q16 412 20 398 Z" fill="${W}" stroke="${K}" stroke-width="8" stroke-linejoin="round"/>
        <path d="M282 352 L374 352" stroke="${K}" stroke-width="7" stroke-linecap="round"/>
      </svg>`,

    inbox: () => `
      <svg class="svgart" viewBox="0 0 620 430" width="600" height="416">
        ${[[110, 30, -6], [70, 70, -2]].map(([x, y, r]) => `<g transform="rotate(${r} ${x + 210} ${y + 140})"><rect x="${x}" y="${y}" width="420" height="270" rx="20" fill="${W}" stroke="${K}" stroke-width="8"/><path d="M${x + 4} ${y + 10} L${x + 210} ${y + 150} L${x + 416} ${y + 10}" fill="none" stroke="${K}" stroke-width="8" stroke-linejoin="round"/></g>`).join("")}
        <rect x="46" y="128" width="420" height="270" rx="20" fill="${Y}" transform="translate(16 16)"/>
        <rect x="46" y="128" width="420" height="270" rx="20" fill="${W}" stroke="${K}" stroke-width="8"/>
        <path d="M50 138 L256 278 L462 138" fill="none" stroke="${K}" stroke-width="8" stroke-linejoin="round"/>
        <path d="M50 394 L196 238 M462 394 L316 238" fill="none" stroke="${K}" stroke-width="8" stroke-linecap="round"/>
        <circle cx="486" cy="128" r="74" fill="${C}" stroke="${K}" stroke-width="8"/>
        <text x="486" y="148" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="56" fill="${W}">147</text>
      </svg>`,

    deck: () => `
      <div class="card deck">
        <div class="dh"><span>SLIDE 14 OF 14</span><span>CONFIDENTIAL</span></div>
        <h4>Founder health</h4>
        <div class="kpis">
          <div class="kpi"><span>Runway</span><strong>7 mo</strong></div>
          <div class="kpi"><span>Sleep</span><strong>4 hrs</strong></div>
          <div class="kpi c"><span>People I can be honest with</span><strong>0</strong></div>
        </div>
      </div>`,

    talk: () => `
      <div style="position:relative;width:900px;height:440px">
        <div style="position:absolute;left:0;top:10px;background:${P};border:6px solid ${K};border-radius:40px;padding:22px 38px;font-family:Poppins;font-weight:700;font-size:44px">How are you?</div>
        <div class="bubble" style="position:absolute;right:0;top:120px">Good, you? 🙂</div>
        <svg class="svgart" viewBox="0 0 300 220" width="300" height="220" style="position:absolute;left:0;top:215px">
          <circle cx="248" cy="40" r="14" fill="${W}" stroke="${K}" stroke-width="6"/>
          <circle cx="214" cy="82" r="20" fill="${W}" stroke="${K}" stroke-width="6"/>
          <ellipse cx="104" cy="148" rx="100" ry="66" fill="${W}" stroke="${K}" stroke-width="7"/>
          <path d="${scribble(104, 148, 52, 28, 11)}" fill="none" stroke="${K}" stroke-width="5" stroke-linecap="round"/>
        </svg>
      </div>`,

    exitform: () => `
      <div class="card form">
        <div class="fh"><span>EXIT INTERVIEW</span><span>FORM HR-07</span></div>
        <h4>Priya M. · Senior Analyst</h4>
        <p style="font-size:22px;color:#4a4a4f">3 years 2 months · Rated "exceeds expectations" twice</p>
        <p class="q">Primary reason for leaving</p>
        <div class="opts">
          <div class="opt"><span class="cb"></span>Compensation</div>
          <div class="opt"><span class="cb on"></span>Better opportunity</div>
          <div class="opt"><span class="cb"></span>Relocation</div>
          <div class="opt"><span class="cb"></span>Higher studies</div>
        </div>
      </div>`,

    tally: () => `
      <div class="card note">
        <p class="nt">Times he said "I'm fine" this week</p>
        <div class="tally">
          <svg class="svgart" viewBox="0 0 470 70" width="470" height="70">
            ${[0, 1].map((g) => [0, 1, 2, 3].map((i) => `<path d="M${g * 190 + 20 + i * 30} 8 L${g * 190 + 16 + i * 30} 62" stroke="${K}" stroke-width="7" stroke-linecap="round"/>`).join("") + `<path d="M${g * 190 + 4} 52 L${g * 190 + 128} 14" stroke="${C}" stroke-width="7" stroke-linecap="round"/>`).join("")}
            <path d="M400 8 L396 62" stroke="${K}" stroke-width="7" stroke-linecap="round"/>
          </svg>
          <span style="font-family:Poppins;font-weight:800;font-size:44px;line-height:1">11</span>
        </div>
        <ul>
          <li>"All good, bro." <i>Tue</i></li>
          <li>"Can't sleep. Otherwise fine." <i>Wed, 2:10 AM</i></li>
          <li>"It's nothing, really." <i>Fri</i></li>
        </ul>
      </div>`,
  };

  const CTA = '<div class="cta"><span>Talk to a certified expert, 24/7</span><b>yourdost.com</b></div>';
  const HELP = '<p class="help">In crisis? Call <b>Tele MANAS 14416</b>, free and 24/7.</p>';

  const POSTS = [
    {
      id: "01", slug: "diwali", theme: "yellow", label: "Festive Wellbeing", visual: "diya",
      headline: "Every corner of the house is shining this Diwali.",
      hl: "Light a diya for your mind too.",
      body: "If the festive season feels heavy this year, you're not alone. Talk to someone who gets it.",
      caption: "The house is spotless, the lights are up, everyone looks happy. And sometimes you still feel low. That's okay, and you don't have to hide it. This Diwali, make a little space for how you're really feeling. Our experts are here 24/7, even on festival days. #HappyDiwali #EmotionalWellness #YourDOST",
    },
    {
      id: "02", slug: "exam-stress", theme: "white", label: "Student Life", visual: "marksheet", hs: true,
      headline: "Your marksheet prints your percentage in bold and your name in small font.",
      hl: "Remember it the other way round.",
      body: "Exam stress feeling heavy? Many colleges give students access to YourDOST. Check your college email.",
      help: true,
      caption: "Boards, entrance exams, semester finals: the numbers matter, but they are not who you are. If exam pressure is keeping you up at night, talk to someone. Many colleges already give students access to YourDOST. In crisis? Call Tele MANAS 14416 (free, 24/7). #ExamStress #StudentLife #YourDOST",
    },
    {
      id: "03", slug: "breakup", theme: "yellow", label: "Love & Relationships", visual: "phone",
      headline: "Something funny happened today. I picked up my phone to tell you.",
      hl: "Then I remembered.",
      body: "Heartbreak hides in the small moments. You don't have to carry them alone.",
      caption: "The hardest part of a breakup is often not the fight. It's the small moments after, when the person you'd tell isn't yours to tell anymore. That reflex fades, slower than you'd like. Until then, talk to someone. Save this for the night you almost hit send. #Heartbreak #Relationships #YourDOST",
    },
    {
      id: "04", slug: "getting-back-together", theme: "white", label: "Love & Relationships", visual: "heart",
      headline: "You got back together. Everyone said “finally!”",
      hl: "Nobody tells you trust takes longer to rebuild.",
      body: "A relationship expert can help you rebuild, one honest conversation at a time.",
      caption: "Getting back together is the easy part. Feeling safe again takes longer, and that doesn't mean it was a mistake. Ask each other: what's different this time, and what will we do when it gets hard? If you need help with those conversations, our relationship experts are here. #Relationships #Trust #YourDOST",
    },
    {
      id: "05", slug: "ai-anxiety", theme: "yellow", label: "Work & Careers", visual: "laptop",
      headline: "AI finished my <span style=\"white-space:nowrap\">3-day</span> task in 40 seconds. I said “wow.”",
      hl: "Then I couldn't sleep.",
      body: "Feeling anxious about your future at work is valid. Talking it through helps.",
      caption: "AI is changing work fast, and it's normal to feel uneasy about where you fit in. That worry is often about more than the job: it's about your sense of worth. You don't have to figure it out alone at 2 AM. Talk it through with a YourDOST expert. #AIAnxiety #WorkStress #YourDOST",
    },
    {
      id: "06", slug: "job-hunt", theme: "white", label: "Work & Careers", visual: "inbox",
      headline: "147 applications. 61 rejections. 86 never replied.",
      hl: "Your inbox is not a verdict on your worth.",
      body: "Job hunting can wear you down. Career counselling and emotional support are just a chat away.",
      caption: "Rejection emails are often sent automatically, to hundreds of people at once. Please don't give them days of your self-worth. If the job hunt is wearing you down, talk to someone about the career side and the emotional side. #JobSearch #CareerStress #YourDOST",
    },
    {
      id: "07", slug: "founders", theme: "yellow", label: "Founder Wellbeing", visual: "deck",
      headline: "Investors track your runway.",
      hl: "Who's tracking how you're doing?",
      body: "Building a company can be lonely. YourDOST has an emotional wellness program for founders: yourdost.com/emotional-wellness-founders",
      caption: "Founders are often the only people in the company who can't have a bad day out loud. The team needs morale, investors need conviction, and family wanted the safe job. If you have no one to be honest with, start here. YourDOST's emotional wellness program for founders: yourdost.com/emotional-wellness-founders #FounderWellbeing #Startups #YourDOST",
    },
    {
      id: "08", slug: "how-are-you", theme: "white", label: "Work & Careers", visual: "talk", hs: true,
      headline: "At work, there's only one acceptable answer to “How are you?”",
      hl: "Here, you can tell the truth.",
      body: "Your company may already offer YourDOST. Ask your HR team, then talk to an expert.",
      caption: "\"Good, you?\" is the answer we give at work, even on the days it isn't true. You deserve a place where you can say how you really are. Many companies offer YourDOST to their employees. Ask your HR team, and talk to an expert today. #WorkplaceWellbeing #EmployeeWellbeing #YourDOST",
    },
    {
      id: "09", slug: "hr-leaders", theme: "yellow", label: "For HR Leaders", visual: "exitform",
      headline: "Her exit interview said “better opportunity.”",
      hl: "The real reason was her 1:40 AM online status.",
      body: "Burnout rarely makes it into an exit form. Make support easy to reach, before people leave.",
      cta: '<div class="cta"><span>Partner with YourDOST</span><b>yourdost.com</b></div>',
      caption: "Exit interviews rarely tell the whole story. Burnout shows up earlier: cameras off, Monday sick leave, the 11 PM \"just checking\". YourDOST works with 500+ organisations to make emotional support private, instant and available in 20+ Indian languages. Want to support your people better? Book a demo at yourdost.com. #HR #EmployeeWellbeing #YourDOST",
    },
    {
      id: "10", slug: "im-fine", theme: "white", label: "Self & Growth", visual: "tally",
      headline: "He said “I'm fine” 11 times this week.",
      hl: "Ask a 12th time. Then really listen.",
      body: "Men are often taught to keep it in. One honest conversation can change that.",
      help: true,
      caption: "International Men's Day, 19 November. Many men grow up learning to fix things, pay the bills and keep their feelings to themselves. Today, check in on him. Ask again, and wait for the real answer. If he isn't ready to talk to you, our experts are here 24/7. In crisis? Call Tele MANAS 14416. #InternationalMensDay #MensMentalHealth #YourDOST",
    },
  ];

  function html(p, logoBase = "brand/") {
    const logo = `${logoBase}${p.theme === "yellow" ? "logo-on-yellow.png" : "logo-on-white.png"}`;
    return `<div class="post ${p.theme}">
      <div class="top"><img class="logo" src="${logo}" alt="YourDOST"><span class="label">${p.label}</span></div>
      <p class="headline${p.hs ? " s" : ""}">${p.headline}</p>
      <p class="hl">${p.hl}</p>
      <div class="visual">${V[p.visual]()}</div>
      <p class="body">${p.body}</p>
      ${p.cta || CTA}
      ${p.help ? HELP : ""}
    </div>`;
  }

  root.YDP = { POSTS, html };
})(typeof window !== "undefined" ? window : globalThis);
