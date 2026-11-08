/* YourDOST Instagram set v4: real photographs, one or two short lines per frame, English only.
   4 reels (with original music), 3 carousels, 3 single images. */
(function (root) {
  "use strict";
  const C = (x) => Math.max(0, Math.min(1, x));
  const E = (x) => 1 - Math.pow(1 - C(x), 3);
  const p = (t, a, d = 0.6) => E((t - a) / d);
  const f3 = (n) => n.toFixed(3);
  // soft reveal: fade, rise, de-blur
  const rv = (t, a, d = 0.8) => { const k = p(t, a, d); return `opacity:${f3(k)};transform:translateY(${((1 - k) * 26).toFixed(1)}px);filter:blur(${((1 - k) * 6).toFixed(2)}px)`; };

  const sw = (n) => (root.YD4_SWAP && root.YD4_SWAP[n]) || n;
  const badge = `<img class="badge" src="brand/badge.png" alt="YourDOST">`;
  const grain = `<div class="grain"></div>`;
  const CTA = `<div class="cta">Talk to a certified expert, 24/7 · <b>yourdost.com</b></div>`;
  const HELP = `<p class="help">In crisis? Call Tele MANAS 14416, free and 24/7.</p>`;

  // ---------- reels ----------
  // photo with a slow push-in; dir sets the drift
  const kb = (src, lt, dur, dir = [0, -1], z = 0.09) => {
    const k = C(lt / dur);
    return `<div class="ph" style="background-image:url(photos/reel-${sw(src)}.jpg);transform:scale(${f3(1.03 + z * k)}) translate(${(dir[0] * 18 * k).toFixed(1)}px,${(dir[1] * 18 * k).toFixed(1)}px)"></div>`;
  };
  function embers(t, n = 16) {
    let s = "";
    for (let i = 0; i < n; i++) {
      const sp = 26 + (i * 37) % 40, x0 = (i * 211) % 1040 + 20, y0 = 1960 - ((i * 487) % 1700);
      const y = ((y0 - sp * t) % 2000 + 2000) % 2000 - 40;
      const x = x0 + 16 * Math.sin(t * 0.7 + i);
      const sz = 10 + (i * 13) % 30;
      const o = 0.18 + 0.3 * (0.5 + 0.5 * Math.sin(t * 1.6 + i * 2.1));
      s += `<div class="glow" style="left:${x.toFixed(1)}px;top:${y.toFixed(1)}px;width:${sz}px;height:${sz}px;opacity:${f3(o)}"></div>`;
    }
    return s;
  }
  function reelFrame(reel, t) {
    const out = [];
    reel.scenes.forEach((s, i) => {
      const last = i === reel.scenes.length - 1;
      if (t < s.a - 0.001 || (!last && t > s.b + 0.6)) return;
      const o = (i === 0 ? 1 : p(t, s.a, 0.6)) * (last ? 1 : 1 - p(t, s.b, 0.6));
      out.push(`<div style="position:absolute;inset:0;opacity:${f3(o)}">${s.html(t - s.a, t, s.b - s.a)}</div>`);
    });
    return out.join("") + (reel.overlay ? reel.overlay(t) : "") + grain + badge;
  }
  const endCard = (photo, lt, line, extra = "", dur = 3) => `
    ${kb(photo, lt, dur, [0, 0], 0.04)}<div class="shade-all"></div>
    <div class="txt center light" style="align-items:center;text-align:center;gap:34px">
      <img src="brand/badge.png" style="width:260px;${rv(lt, 0.05, 0.6)}" alt="">
      <p class="line s" style="${rv(lt, 0.3)}">${line}</p>
      <div style="${rv(lt, 0.6)}">${CTA}</div>
      ${extra ? `<div style="${rv(lt, 0.8)}">${extra}</div>` : ""}
    </div>`;

  const DIWALI = { dur: 17.4, cover: 2.2, audio: "diwali", overlay: (t) => (t < 15.2 ? embers(t) : ""), scenes: [
    { a: 0, b: 4.0, html: (lt, t, d) => `${kb("diwali-doorstep", lt, d + 0.6, [-1, 0])}<div class="shade-b"></div>
      <div class="txt bottom light"><p class="eyebrow" style="${rv(lt, 0.1)}">Diwali 2026</p><p class="line" style="${rv(lt, 0.3)}">The house is ready for Diwali.</p></div>` },
    { a: 4.0, b: 8.0, html: (lt, t, d) => `${kb("diwali-street", lt, d + 0.6, [0, 1])}<div class="shade-all" style="opacity:.55"></div>
      <div class="txt ${sw("diwali-street") === "diwali-street" ? "center" : "top"} light" style="align-items:center;text-align:center"><p class="line xl" style="${rv(lt, 0.4, 1.0)}">Are <span class="mk">you?</span></p></div>` },
    { a: 8.0, b: 12.4, html: (lt, t, d) => `${kb("diwali-terrace", lt, d + 0.6, [1, 0])}<div class="shade-b"></div>
      <div class="txt bottom light"><p class="line" style="${rv(lt, 0.3)}">If this festival feels heavy, that's okay.</p></div>` },
    { a: 12.4, b: 15.2, html: (lt, t, d) => `${kb("diwali-diya", lt, d + 0.6, [0, -1], 0.12)}<div class="shade-b"></div>
      <div class="txt bottom light"><p class="line" style="${rv(lt, 0.3)}">Light one diya <span class="mk">for yourself</span> too.</p></div>` },
    { a: 15.2, b: 17.4, html: (lt) => endCard("diwali-diya", lt, "Happy Diwali from YourDOST") },
  ] };

  const WORDS = ["Tired", "Hopeful", "Anxious", "Calm", "Lonely", "Proud", "Overwhelmed", "Okay", "Restless", "Grateful", "Numb", "Loved", "Stuck", "Lighter", "Scared", "Ready", "Drained", "Content"];
  const CHECKIN = { dur: 19.0, cover: 1.4, audio: "checkin", scenes: [
    { a: 0, b: 3.2, html: (lt, t, d) => `${kb("rain-street", lt, 10, [0, -1], 0.05)}<div class="shade-all" style="opacity:.75"></div>
      <div class="txt center light"><p class="line xl" style="${rv(lt, 0, 0.5)}">Pause this reel on a word.</p><p class="small" style="font-size:44px;${rv(lt, 0.7)}">That's how today really feels.</p></div>` },
    { a: 3.2, b: 9.65, html: (lt) => {
      const step = 60 / 84 / 2, i = Math.min(WORDS.length - 1, Math.floor(lt / step)), k = C((lt - i * step) / 0.12);
      return `${kb("rain-street", 3.2 + lt, 10, [0, -1], 0.05)}<div class="shade-all" style="opacity:.78"></div>
        <div class="txt center light" style="align-items:center"><p class="wordflash" style="opacity:${f3(0.4 + 0.6 * k)};transform:scale(${f3(0.94 + 0.06 * k)})">${WORDS[i]}</p></div>`; } },
    { a: 9.65, b: 13.2, html: (lt) => `${kb("rain-street", 9.65 + lt, 12, [0, -1], 0.05)}<div class="shade-all" style="opacity:.72"></div>
      <div class="txt center light"><p class="line xl" style="${rv(lt, 0.1)}">Got your word?</p><p class="line s" style="${rv(lt, 0.9)}">Drop it in the comments.</p></div>` },
    { a: 13.2, b: 16.3, html: (lt, t, d) => `${kb("chai-hands", lt, d + 0.6, [0, 1])}<div class="shade-b"></div>
      <div class="txt bottom light"><p class="line" style="${rv(lt, 0.3)}">Whatever it is, you can <span class="mk">talk about it.</span></p></div>` },
    { a: 16.3, b: 19.0, html: (lt) => endCard("chai-hands", lt, "Your daily check-in, from YourDOST") },
  ] };

  const JOBS = { dur: 17.4, cover: 2.6, audio: "jobs", scenes: [
    { a: 0, b: 4.4, html: (lt, t, d) => `${kb("heater-laptop", lt, d + 0.6, [0, -1])}<div class="shade-b"></div>
      <div class="txt bottom light"><p class="eyebrow">Job hunt · Day 94</p><p class="line xl">Application #${String(Math.max(1, Math.round(147 * p(lt, 0.1, 2.0)))).padStart(3, "0")}</p><p class="line s" style="${rv(lt, 2.4)}">Still no reply.</p></div>` },
    { a: 4.4, b: 8.8, html: (lt, t, d) => `${kb("keyboard-dark", lt, d + 0.6, [1, 0])}<div class="shade-b"></div>
      <div class="txt bottom light"><p class="line s" style="${rv(lt, 0.3)}">Rejection emails are often automated.</p><p class="line" style="${rv(lt, 1.3)}"><span class="mk">Your worth isn't.</span></p></div>` },
    { a: 8.8, b: 13.4, html: (lt, t, d) => `${kb("sunrise-rain", lt, d + 0.6, [0, -1])}<div class="shade-b"></div>
      <div class="txt bottom light"><p class="line" style="${rv(lt, 0.3)}">Close the laptop. Try again tomorrow.</p></div>` },
    { a: 13.4, b: 17.4, html: (lt) => endCard("sunrise-rain", lt, "Career counselling and emotional support, in one place.") },
  ] };

  const MEN = { dur: 17.2, cover: 2.2, audio: "men", scenes: [
    { a: 0, b: 4.2, html: (lt, t, d) => `${kb("man-walking", lt, d + 0.6, [0, -1])}<div class="shade-b"></div>
      <div class="txt bottom light"><p class="eyebrow" style="${rv(lt, 0.1)}">19 Nov · International Men's Day</p><p class="line" style="${rv(lt, 0.3)}">He says, “I'm fine.”</p></div>` },
    { a: 4.2, b: 8.4, html: (lt, t, d) => `${kb("dark-window", lt, d + 0.6, [-1, 0])}<div class="shade-b"></div>
      <div class="txt bottom light"><p class="line" style="${rv(lt, 0.3)}">He's said it all week.</p></div>` },
    { a: 8.4, b: 12.8, html: (lt, t, d) => `${kb("chai-hands", lt, d + 0.6, [0, 1])}<div class="shade-b"></div>
      <div class="txt bottom light"><p class="line" style="${rv(lt, 0.3)}">Ask him again. <span class="mk">Over chai.</span></p></div>` },
    { a: 12.8, b: 17.2, html: (lt) => endCard("chai-hands", lt, "Men need someone to talk to, too.", HELP) },
  ] };

  // ---------- feed frames ----------
  const photo = (src, html, shade = "shade-b") => `<div class="ph" style="background-image:url(photos/feed-${sw(src)}.jpg)"></div><div class="${shade}"></div>${grain}${badge}${html}`;
  const cream = (html) => `${badge}${html}`;

  const POSTS = [
    { id: "01", slug: "Reel-Diwali", kind: "reel", reel: DIWALI, theme: "Diwali", segment: "Everyone celebrating Diwali", date: "Sun 8 Nov 2026", time: "11:00 AM IST",
      line: "The house is ready for Diwali. Are you?",
      why: "Real Diwali photos and one quiet question turn a festive post into a gentle check-in; the diya at the end gives people something to do for themselves.",
      caption: "The house is ready for Diwali. Are you? 🪔\n\nIf this festival feels heavier than it looks, that's okay. Light one diya for yourself too.\n\nOur experts are here 24/7, festival days included.\n\nHappy Diwali from all of us at YourDOST.",
      tags: "#HappyDiwali #Diwali2026 #EmotionalWellness #MentalHealthMatters #YourDOST",
      first: "Drop a 🪔 if you're lighting one for yourself today.",
      alt: ["Short video: diyas on a doorstep, festive street lights, a diya on a terrace at sunset and a single glowing diya. Text: The house is ready for Diwali. Are you? If this festival feels heavy, that's okay. Light one diya for yourself too. Ends with the YourDOST logo."] },
    { id: "02", slug: "Reel-Pause-On-A-Word", kind: "reel", reel: CHECKIN, theme: "Daily emotional check-in", segment: "Everyone: students, employees, young adults", date: "Tue 10 Nov 2026", time: "8:30 PM IST",
      line: "Pause this reel on a word. That's how today really feels.",
      why: "A game people replay to land on a word, then answer in the comments: replays and comments are what Instagram rewards, and every answer is a small, safe way of naming a feeling.",
      caption: "Pause on a word. That's your word for today. 👀\n\nTired, hopeful, numb, proud: every one of them is allowed.\n\nDrop your word in the comments. We read every one. And if your word felt heavy, you can talk to us, 24/7.",
      tags: "#EmotionalCheckIn #HowAreYouReally #MentalHealthMatters #FeelYourFeelings #YourDOST",
      first: "Mine was “Lighter” 💛 What did you get?",
      alt: ["Short video: over a rainy city street at night, text says pause this reel on a word, that's how today really feels. Feeling words flash one after another: tired, hopeful, anxious, calm, lonely, proud, overwhelmed and more. Then: got your word? Drop it in the comments. Two hands with cups of chai: whatever it is, you can talk about it. Ends with the YourDOST logo."] },
    { id: "03", slug: "Carousel-Exam-Stress", kind: "carousel", theme: "Exam stress", segment: "Students: boards, entrance exams, semester finals", date: "Thu 12 Nov 2026", time: "7:00 PM IST",
      line: "Your marksheet shows your marks. Not the nights you studied.",
      why: "Four short slides, one line each, so the swipe does the storytelling; the real notebook photo makes it feel like a student's own desk.",
      slides: [
        () => photo("notebook", `<div class="txt bottom light"><p class="eyebrow">Student Life</p><p class="line">Your marksheet shows your marks.</p></div>`),
        () => cream(`<div class="txt center"><p class="line">It doesn't show the <span class="mk">nights you studied.</span></p></div>`),
        () => `${badge}<div class="txt center"><p class="line">Or the days you <span class="mk">didn't give up.</span></p></div>`,
        () => photo("sunrise-rain", `<div class="txt bottom light"><p class="line">You are more than a number.</p>${CTA}${HELP}</div>`),
      ], bg: ["", "cream", "yel", ""],
      caption: "Results season can make you feel like a number. You're not. 💛\n\nIf exam stress is getting heavy, talk to someone. Many colleges offer YourDOST to students: check your college email.\n\nIn crisis? Call Tele MANAS 14416 (free, 24/7).",
      tags: "#ExamStress #StudentLife #BoardExams #ExamSeason #YourDOST",
      first: "Tag a friend who needs to hear this before results day. 💛",
      alt: ["A handwritten notebook with a pen. Text: Your marksheet shows your marks.", "Text: It doesn't show the nights you studied.", "Text: Or the days you didn't give up.", "Sunrise through a rainy window. Text: You are more than a number. Talk to a certified expert, 24/7."] },
    { id: "04", slug: "Image-AI-Anxiety", kind: "single", theme: "AI and job fear", segment: "Working professionals", date: "Fri 13 Nov 2026", time: "9:30 PM IST",
      line: "AI finished my 3-day task in 40 seconds. Then I couldn't sleep.",
      why: "A real keyboard in the dark at night is the exact moment the worry shows up; the confession reads like a peer, not a brand.",
      slides: [() => photo("keyboard-dark", `<div class="txt bottom light"><p class="eyebrow">Work &amp; Careers</p><p class="line s">AI finished my 3-day task in 40 seconds.</p><p class="line"><span class="mk">Then I couldn't sleep.</span></p>${CTA}</div>`)],
      caption: "AI is changing work fast, and it's normal to feel uneasy about where you fit in. 💭\n\nIf the worry is keeping you up, talk it through with a YourDOST expert, 24/7. Your company may already cover it: ask HR.",
      tags: "#AIAnxiety #FutureOfWork #WorkStress #MentalHealthAtWork #YourDOST",
      first: "Has AI changed how you feel about your job? You're not alone. 👇",
      alt: ["A laptop keyboard in a dark room. Text: AI finished my 3-day task in 40 seconds. Then I couldn't sleep. Talk to a certified expert, 24/7."] },
    { id: "05", slug: "Carousel-Breakup", kind: "carousel", theme: "Breakup", segment: "College students and young adults", date: "Sun 15 Nov 2026", time: "9:30 PM IST",
      line: "You picked up your phone to tell them. Then you remembered.",
      why: "Two real photos carry the moment with no explanation; the last slide turns it toward support without sounding like an ad.",
      slides: [
        () => photo("phone-hands", `<div class="txt bottom light"><p class="eyebrow">Love &amp; Relationships</p><p class="line">You picked up your phone to tell them.</p></div>`),
        () => photo("rain-window", `<div class="txt bottom light"><p class="line xl">Then you remembered.</p></div>`),
        () => cream(`<div class="txt center"><p class="line">Healing isn't a <span class="mk">straight line.</span></p><svg viewBox="0 0 860 220" width="860" height="220" style="margin-top:30px"><path d="M10 190 C120 180 150 110 220 130 C300 154 260 210 340 180 C430 146 380 70 470 90 C560 110 520 170 610 130 C700 90 660 30 740 40 C800 46 820 20 850 14" fill="none" stroke="#5b4a9c" stroke-width="8" stroke-linecap="round"/></svg></div>`),
        () => photo("two-walking", `<div class="txt bottom light"><p class="line">You don't have to do it alone.</p>${CTA}</div>`),
      ], bg: ["", "", "cream", ""],
      caption: "The hardest part of a breakup is often the small moments after. 💔\n\nHealing isn't a straight line, and you don't have to do it alone. Our experts are here to listen, 24/7.\n\nSend this to a friend who's going through it.",
      tags: "#Breakup #Heartbreak #MovingOn #HealingJourney #YourDOST",
      first: "Which slide felt the most true? 💛",
      alt: ["Hands holding a phone. Text: You picked up your phone to tell them.", "Rain on a window at dusk. Text: Then you remembered.", "Text: Healing isn't a straight line, with a wavy line.", "Two people walking along a beach at sunset. Text: You don't have to do it alone. Talk to a certified expert, 24/7."] },
    { id: "06", slug: "Reel-Job-Hunt", kind: "reel", reel: JOBS, theme: "Job hunt", segment: "Freshers and job seekers", date: "Tue 17 Nov 2026", time: "8:00 PM IST",
      line: "Rejection emails are often automated. Your worth isn't.",
      why: "A laptop next to a heater at night is what job hunting really looks like at home; the counter hooks the eye and the sunrise ends it on hope.",
      caption: "Application #147. Still no reply. 📩\n\nMany rejection emails are sent automatically, to hundreds of people at once. Your worth isn't decided by an inbox.\n\nClose the laptop tonight. Try again tomorrow. And if it's wearing you down, YourDOST offers career counselling and emotional support, 24/7.",
      tags: "#JobSearch #JobHunt #Placements #CareerAdvice #YourDOST",
      first: "What's your application count right now? You're not the only one. 👇",
      alt: ["Short video: a laptop beside a glowing heater at night, an application counter rises to 147, still no reply; a dark keyboard: rejection emails are often automated, your worth isn't; sunrise through a rainy window: close the laptop, try again tomorrow. Ends with the YourDOST logo."] },
    { id: "07", slug: "Image-Founders", kind: "single", theme: "Founders", segment: "Founders, incubators and investors", date: "Wed 18 Nov 2026", time: "9:00 AM IST",
      line: "Investors track your runway. Who's tracking you?",
      why: "A real desk, a laptop and a cup of chai is every founder's day; the line names the one metric nobody asks about.",
      slides: [() => photo("office-chai", `<div class="txt bottom light"><p class="eyebrow">Founder Wellbeing</p><p class="line">Investors track your runway.</p><p class="line"><span class="mk">Who's tracking you?</span></p><p class="small">YourDOST's emotional wellness program for founders: yourdost.com/emotional-wellness-founders</p></div>`)],
      caption: "Founders are often the only people in the company who can't have a bad day out loud. 🚀\n\nIf there's no one you can be honest with, start here: YourDOST's emotional wellness program for founders, yourdost.com/emotional-wellness-founders\n\nIncubators and VCs: tag a founder who needs to see this.",
      tags: "#Founders #StartupLife #FounderMentalHealth #StartupIndia #YourDOST",
      first: "Founders: who do you talk to when it's hard? 👇",
      alt: ["A work desk with a laptop, monitors and a cup of chai. Text: Investors track your runway. Who's tracking you? YourDOST's emotional wellness program for founders."] },
    { id: "08", slug: "Reel-Mens-Day", kind: "reel", reel: MEN, theme: "International Men's Day", segment: "Men, and the people who love them", date: "Thu 19 Nov 2026", time: "9:00 AM IST",
      line: "He says “I'm fine.” Ask him again. Over chai.",
      why: "Chai is how many Indian men open up; the reel turns a heavy topic into one easy thing to do today.",
      caption: "International Men's Day, 19 November. 💙\n\n“I'm fine” is the answer to everything, until someone asks twice. Check in on him today, over chai.\n\nIf he isn't ready to talk to you, our experts are here 24/7. In crisis? Call Tele MANAS 14416 (free, 24/7).",
      tags: "#InternationalMensDay #MensMentalHealth #ItsOkayToTalk #CheckOnYourFriends #YourDOST",
      first: "Tag the man you're asking for chai today. ☕",
      alt: ["Short video: a man walking away across a terrace: he says I'm fine; a dark room with a window: he's said it all week; two hands clinking cups of chai: ask him again, over chai. Ends with the YourDOST logo and Tele MANAS 14416."] },
    { id: "09", slug: "Image-Getting-Back-Together", kind: "single", theme: "Getting back together", segment: "Couples", date: "Sat 21 Nov 2026", time: "8:00 PM IST",
      line: "Getting back together is easy. Trusting again takes time.",
      why: "Two cups of chai on one table is the everyday picture of two people trying again; the line normalises the anxiety after a patch-up.",
      slides: [() => photo("two-chai", `<div class="txt bottom light"><p class="eyebrow">Love &amp; Relationships</p><p class="line s">Getting back together is easy.</p><p class="line"><span class="mk">Trusting again takes time.</span></p>${CTA}</div>`)],
      caption: "Back together, and still a little anxious? That's normal. 🤍\n\nMissing someone and trusting them again heal at different speeds. If you'd like help with those conversations, our relationship experts are here.",
      tags: "#Relationships #Trust #GettingBackTogether #HealthyRelationships #YourDOST",
      first: "What helped you trust again? 👇",
      alt: ["Two cups of chai and snacks on a table, seen from above. Text: Getting back together is easy. Trusting again takes time. Talk to a certified expert, 24/7."] },
    { id: "10", slug: "Carousel-HR-and-Campus-Leaders", kind: "carousel", theme: "HR and campus leaders (B2B)", segment: "HR leaders, managers, deans and professors", date: "Tue 24 Nov 2026", time: "10:00 AM IST",
      line: "Her exit form said “better opportunity.” Burnout starts long before the resignation.",
      why: "Short lines with YourDOST's own data style: one real photo to open, two numbers with sources, and their usual “Let's start a conversation” close.",
      slides: [
        () => photo("office-desk", `<div class="txt bottom light"><p class="eyebrow">For HR Leaders &amp; Campus Heads</p><p class="line">Her exit form said “better opportunity.”</p></div>`),
        () => cream(`<div class="txt center"><p class="line">Burnout starts long <span class="mk">before the resignation.</span></p></div>`),
        () => cream(`<div class="txt center"><p class="eyebrow">Every year</p><p class="big">₹1.1 lakh crore</p><p class="line s">lost by Indian employers to poor employee mental health.</p><p class="source">Source: Deloitte, Mental Health and Well-being in the Workplace (2022)</p></div>`),
        () => cream(`<div class="txt center"><p class="line s">Most people start by <span class="mk">typing, not talking.</span></p><div class="cards"><div class="card y"><b>57.88%</b><span>Chat</span></div><div class="card l"><b>18.49%</b><span>Audio</span></div><div class="card l"><b>17.8%</b><span>Video</span></div><div class="card y"><b>5.84%</b><span>In person</span></div></div><p class="source">Source: YourDOST | Decade of Wellness Report (post-pandemic sessions)</p></div>`),
        () => `${badge}<div class="txt center"><p class="line">Let's start a conversation.</p><p class="small" style="font-size:36px">Visit <b>www.yourdost.com</b><br>or mail us at <b>contact@yourdost.com</b></p></div>`,
      ], bg: ["", "cream", "cream", "cream", "yel"],
      caption: "Exit interviews rarely tell the whole story. Burnout shows up much earlier. 📋\n\nPoor employee mental health costs Indian employers about ₹1.1 lakh crore a year (Deloitte, 2022). And most people start support by typing: 57.88% of YourDOST sessions after the pandemic were chat-based.\n\nLet's make support easy to reach for your people: www.yourdost.com or contact@yourdost.com",
      tags: "#HRLeaders #EmployeeWellbeing #WorkplaceMentalHealth #CampusWellbeing #YourDOST",
      first: "HR leaders and faculty: what's one early sign of burnout you watch for? 👇",
      alt: ["An empty office desk. Text: Her exit form said better opportunity.", "Text: Burnout starts long before the resignation.", "Text: ₹1.1 lakh crore lost every year by Indian employers to poor employee mental health. Source: Deloitte 2022.", "Text: Most people start by typing, not talking. 57.88% chat, 18.49% audio, 17.8% video, 5.84% in person. Source: YourDOST Decade of Wellness Report.", "Text: Let's start a conversation. Visit www.yourdost.com or mail contact@yourdost.com."] },
  ];

  function frame(post, i = 0, t = null) {
    if (post.kind === "reel") return `<div class="f tall">${reelFrame(post.reel, t === null ? post.reel.cover : t)}</div>`;
    const bg = (post.bg && post.bg[i]) || "";
    return `<div class="f ${bg}">${post.slides[i]()}</div>`;
  }
  root.YD4 = { POSTS, frame };
})(typeof window !== "undefined" ? window : globalThis);
