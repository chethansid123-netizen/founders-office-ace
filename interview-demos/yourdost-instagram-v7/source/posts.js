/* YourDOST v7: 3 carousels + 3 original formats, built for YourDOST's STP.
   People: C21 (corporate carousel) and O24 (corporate original). Everything else is evergreen imagery:
   the night sky and a planetarium (C22), a Rajasthani stepwell (C23), a gallery painting (O25), Everest base camp (O26).
   All photos are ElevenLabs generations; the logo badge is on every slide. */
(function (root) {
  "use strict";
  const badge = `<img class="badge" src="brand/badge.png" alt="YourDOST">`;
  const count = (i, n, tone = "dark") => `<span class="count ${tone}">${i}/${n}</span>`;
  const arrow = (c = "#0d1015", w = 170, st = "") => `<svg class="doodle" style="${st}" viewBox="0 0 220 160" width="${w}"><path d="M14 20 C 40 120 120 140 186 120" fill="none" stroke="${c}" stroke-width="6" stroke-linecap="round"/><path d="M164 96 L190 120 L162 140" fill="none" stroke="${c}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

  /* ---------- C21: CAPTCHA ---------- */
  const ic = {
    refresh: `<svg width="34" height="34" viewBox="0 0 24 24"><path d="M17.7 6.3A8 8 0 1 0 20 12h-2.2a5.8 5.8 0 1 1-1.7-4.1L13 11h7V4z" fill="#555"/></svg>`,
    audio: `<svg width="34" height="34" viewBox="0 0 24 24"><path d="M12 3a8 8 0 0 0-8 8v6a3 3 0 0 0 3 3h2v-8H6v-1a6 6 0 0 1 12 0v1h-3v8h2a3 3 0 0 0 3-3v-6a8 8 0 0 0-8-8z" fill="#555"/></svg>`,
    info: `<svg width="34" height="34" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5" fill="none" stroke="#555" stroke-width="2"/><rect x="11" y="10" width="2" height="7" fill="#555"/><rect x="11" y="6.5" width="2" height="2" fill="#555"/></svg>`,
    tick: `<svg width="24" height="24" viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  };
  const tiles = (sel) => Array.from({ length: 16 }, (_, k) => {
    const c = k % 4, r = Math.floor(k / 4);
    return `<div class="t${sel ? " sel" : ""}" style="background-image:url(ai/c21-team.jpg);background-position:${c * 100 / 3}% ${r * 100 / 3}%">${sel ? `<span class="ck">${ic.tick}</span>` : ""}</div>`;
  }).join("");
  const WHO = [
    [1, "Sleeping <b>4 hours a night</b> since the re-org."],
    [2, "Had a <b>panic attack</b> in the washroom at 11 AM."],
    [3, "His dad's <b>in the ICU</b>. Nobody here knows."],
    [4, "Laughing. <b>Going through a divorce.</b>"],
    [5, "<b>Cried in the car</b> before logging in."],
    [6, "Her best day this month. <b>Ask about the other 29.</b>"],
    [7, "Sure he's <b>first on the layoff list.</b>"],
  ];
  const LABELS = [ // (unused) [left %, top %, text] relative to the photo grid
    [1, 25, "Sleeping 4 hours a night since the re-org"],
    [24, 37, "Panic attack in the washroom at 11 AM"],
    [51, 28, "Dad's in the ICU. Nobody here knows."],
    [76, 31, "Laughing. Going through a divorce."],
    [1, 53, "Cried in the car before logging in"],
    [39, 54, "Best day this month. Ask about the other 29."],
    [76, 52, "Sure he's first on the layoff list"],
  ];
  const captcha = ({ s1, big, s2, sel = false, labels = false, err = "", btn = "Skip", btnOff = false }) => `
    <div class="cap" style="left:130px;width:820px;top:210px">
      <div class="top"><small>${s1}</small><b>${big}</b><small>${s2}</small></div>
      <div class="grid">${tiles(sel)}${labels ? LABELS.map(([x, y, t]) => `<div class="lbl u" style="left:${x}%;top:${y}%;max-width:23%">${t}</div>`).join("") : ""}</div>
      ${err ? `<p class="err">${err}</p>` : ""}
      <div class="bot"><div class="icons">${ic.refresh}${ic.audio}${ic.info}</div><span class="btn${btnOff ? " off" : ""}">${btn}</span></div>
    </div>`;

  /* ---------- C22: deterministic star field ---------- */
  const stars = (n = 140, seed = 7) => { let s = seed, h = ""; const rnd = () => ((s = (s * 9301 + 49297) % 233280) / 233280);
    for (let i = 0; i < n; i++) { const r = rnd() < 0.08 ? 3.2 : rnd() < 0.3 ? 2 : 1.2; h += `<i style="position:absolute;left:${(rnd() * 100).toFixed(2)}%;top:${(rnd() * 100).toFixed(2)}%;width:${r}px;height:${r}px;border-radius:50%;background:#fff;opacity:${(0.35 + rnd() * 0.65).toFixed(2)};box-shadow:0 0 ${r * 3}px rgba(255,255,255,0.7)"></i>`; }
    return `<div class="fill">${h}</div>`; };

  /* ---------- O24: meeting tiles ---------- */
  const mic = (on) => on ? `<svg width="18" height="18" viewBox="0 0 24 24"><rect x="9" y="3" width="6" height="11" rx="3" fill="#fff"/><path d="M6 11a6 6 0 0 0 12 0M12 17v4" stroke="#fff" stroke-width="2" fill="none"/></svg>`
    : `<svg width="18" height="18" viewBox="0 0 24 24"><rect x="9" y="3" width="6" height="11" rx="3" fill="#ff6b5e"/><path d="M6 11a6 6 0 0 0 12 0M12 17v4" stroke="#ff6b5e" stroke-width="2" fill="none"/><path d="M4 4l16 16" stroke="#ff6b5e" stroke-width="2.4"/></svg>`;
  const TILES = [
    ["o24-arjun", "Arjun (host)", true, "“Quick round! How's everyone doing?”", "I haven't slept properly since the re-org.", true],
    ["o24-neha", "Neha", false, "“Super good!”", "I cried in the washroom at 9:12.", false],
    ["o24-rahul", "Rahul", false, "“All good. I can take more.”", "I can't say no. I'm drowning.", false],
    ["o24-fatima", "Fatima", false, "“Doing well, thanks.”", "Is my name on the layoff list?", false],
    [null, "Vikram", false, "“Yeah, all fine.”", "Logged in from Papa's hospital room.", false],
    ["o24-sneha", "Sneha", false, "“Never better, haha.”", "Sunday dread starts on Saturday now.", false],
  ];
  const tileHTML = ([img, name, on, said, inner, speaking]) => `<div class="tile${img ? "" : " off"}${speaking ? " speaking" : ""}" style="${img ? `background-image:url(ai/${img}.jpg)` : ""}">
      ${img ? "" : `<div class="av">VK</div>`}<span class="nm">${mic(on)}${name}</span>
      <div class="cc"><p class="said">${said}</p><p class="inner">${inner}</p></div></div>`;

  /* ---------- O26: expedition chart ---------- */
  const X = (d) => 40 + (d / 42) * 880, Yv = (a) => 178 - ((a - 5000) / 4000) * 160;
  const PLAN = [[0, 5364], [3, 5364], [5, 6065], [6, 5364], [9, 5364], [12, 6400], [14, 5364], [18, 5364], [21, 7162], [23, 5364], [32, 5364], [35, 6400], [37, 7162], [38, 7950], [39, 8849], [41, 5364]];
  const RESTS = [[0, 3], [6, 9], [14, 18], [23, 32]];
  const chart = () => {
    const pts = PLAN.map(([d, a]) => `${X(d).toFixed(1)},${Yv(a).toFixed(1)}`).join(" ");
    const grid = [5000, 6000, 7000, 8000, 9000].map((a) => `<line x1="40" x2="920" y1="${Yv(a)}" y2="${Yv(a)}" stroke="rgba(255,255,255,0.13)" stroke-width="1.5"/><text x="0" y="${Yv(a) + 6}" font-size="16" fill="rgba(255,255,255,0.55)" font-family="Inter">${a / 1000}k</text>`).join("");
    const rests = RESTS.map(([a, b]) => `<rect x="${X(a)}" y="${Yv(5364) - 9}" width="${X(b) - X(a)}" height="18" rx="9" fill="rgba(246,210,90,0.28)"/>`).join("");
    return `<svg width="940" height="196" viewBox="0 0 940 196">${grid}${rests}
      <polyline points="${X(0)},${Yv(5364)} ${X(8)},${Yv(8350)}" fill="none" stroke="#ff7a5c" stroke-width="5" stroke-linecap="round"/>
      <polyline points="${X(8)},${Yv(8350)} ${X(9.2)},${Yv(5000)}" fill="none" stroke="#ff7a5c" stroke-width="4" stroke-dasharray="8 8"/>
      <circle cx="${X(8)}" cy="${Yv(8350)}" r="6" fill="#ff7a5c"/>
      <text x="${X(8) + 14}" y="${Yv(8350) + 6}" font-size="18" font-weight="700" fill="#ff9b83" font-family="Inter">burnout</text>
      <polyline points="${pts}" fill="none" stroke="#f6d25a" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
      <circle cx="${X(39)}" cy="${Yv(8849)}" r="8" fill="#f6d25a"/><text x="${X(39) - 128}" y="${Yv(8849) + 6}" font-size="18" font-weight="700" fill="#fff" font-family="Inter">Summit</text>
      <text x="${X(9.5)}" y="${Yv(5364) + 30}" font-size="16" fill="rgba(246,210,90,0.95)" font-family="Inter" font-weight="600">rest</text>
      <text x="${X(25.5)}" y="${Yv(5364) + 30}" font-size="16" fill="rgba(246,210,90,0.95)" font-family="Inter" font-weight="600">rest, rest, rest</text>
    </svg>`;
  };

  const POSTS = [
    /* ===================== C21 · CORPORATE · PEOPLE ===================== */
    {
      id: "21", slug: "Carousel-Select-All-Squares", kind: "carousel", segment: "Corporate: people managers, HR and CHROs (B2B buyers), and the employees who share it",
      date: "Tue 15 Dec 2026", time: "11:00 AM IST", theme: "Invisible struggle at work",
      line: "Select all squares with a colleague who's struggling.",
      why: "Everyone has solved a CAPTCHA, so the first slide is impossible not to try. It's a happy team photo and nobody looks like they're struggling, so most people click Skip. The reveal shows every one of them was. That is the YourDOST pitch to employers in one swipe: you can't spot it, so give people a confidential place to say it. The Deloitte numbers back it for HR. The last slide turns the checkbox into ‘I'm not okay’.",
      slides: [
        () => `<div class="fill paper"></div><div class="abs" style="left:130px;top:118px"><span class="eyebrow">A 10-second test for every manager</span></div>
          ${captcha({ s1: "Select all squares with", big: "a colleague who's struggling", s2: "If there are none, click skip" })}${badge}`,
        () => `<div class="fill paper"></div><div class="abs" style="left:130px;top:112px;display:flex;align-items:center;gap:22px"><span class="eyebrow">Couldn't find anyone?</span><span class="note" style="font-size:42px;color:#5b4a9c">(most people can't)</span></div>
          ${captcha({ s1: "Select all squares with", big: "a colleague who's struggling", s2: "If there are none, click skip", err: "Are you sure? Look again.", btn: "Skip" })}${count(2, 6)}${badge}`,
        () => `<div class="fill paper"></div><div class="abs" style="left:130px;top:112px;display:flex;align-items:center;gap:22px"><span class="eyebrow">The answer</span><span class="note" style="font-size:42px;color:#5b4a9c">(swipe to see why)</span></div>
          ${captcha({ s1: "Correct answer:", big: "Every single square.", s2: "Struggle rarely looks like struggle.", sel: true, btn: "Verify" })}${count(3, 6)}${badge}`,
        () => `<div class="fill paper"></div>
          <div class="abs" style="left:64px;right:190px;top:96px"><span class="eyebrow">Same photo, same afternoon</span><p class="h s" style="margin-top:18px">What the photo didn't show.</p></div>
          <div class="who">${WHO.map(([n, t]) => `<div class="r"><img src="ai/c21-face${n}.jpg"><p>${t}</p></div>`).join("")}</div>${count(4, 6)}${badge}`,
        () => `<div class="fill bg-ink" style="background:#13121a"></div>
          <div class="abs" style="left:72px;right:72px;top:150px"><span class="eyebrow">The numbers</span>
            <p style="font-weight:600;font-size:220px;line-height:1;color:#f6d25a;margin-top:30px;letter-spacing:-0.03em">8 in 10</p>
            <p class="h s" style="color:#fff;margin-top:14px">employees in India reported a mental-health concern in the past year.</p>
            <p class="body" style="color:#cdb6f5;margin-top:22px">Most still came to work, and smiled for photos like that one.</p>
            <div style="border-top:2px solid rgba(255,255,255,0.18);margin-top:44px;padding-top:34px"><p style="font-weight:600;font-size:64px;color:#fff">₹1.1 lakh crore</p>
            <p class="small" style="color:rgba(255,255,255,0.8);margin-top:6px">a year: what poor mental health costs Indian employers, mostly through people who come in but can't fully be there.</p></div>
            <p class="src" style="margin-top:34px">Source: Deloitte, Mental Health and Well-being in the Workplace (2022)</p></div>${count(5, 6, "lite")}${badge}`,
        () => `<div class="fill paper"></div>
          <div class="abs" style="left:72px;right:170px;top:150px"><p class="h" style="font-size:70px">You can't spot it.</p><p class="h" style="font-size:70px;color:#5b4a9c">So make it safe to say.</p></div>
          <div class="robot" style="top:470px"><span class="box"></span><span class="lab">I'm not okay</span><span class="side"><img src="brand/badge.png">Confidential<br>24/7</span></div>
          <div class="abs" style="left:72px;right:72px;top:720px"><p class="body">YourDOST gives every employee a confidential expert by chat, call or video, any hour of the day.</p>
          <div style="margin-top:34px"><span class="cta">YourDOST for teams · <b>contact@yourdost.com</b></span></div></div>
          <p class="note abs" style="left:72px;bottom:150px;color:#5b4a9c">send this to your HR head</p>${arrow("#5b4a9c", 140, "left:520px;bottom:94px")}${count(6, 6)}${badge}`,
      ],
      caption: "Quick test for every manager. 👀\n\nSelect all squares with a colleague who's struggling.\n\nMost people click Skip. The answer is on slide 3, and slide 4 shows why.\n\nStruggle rarely looks like struggle. You can't spot it, so make it safe to say it. YourDOST gives every employee a confidential expert, 24/7.",
      tags: "#Leadership #HR #EmployeeWellbeing #MentalHealthAtWork #PeopleManagement #CorporateIndia #YourDOST",
      first: "Be honest: did you click Skip on slide 1? 👇 (Managers, save this for your next 1:1.)",
      alt: [
        "A CAPTCHA box over a photo of seven smiling colleagues at an office birthday. Text: Select all squares with a colleague who's struggling. If there are none, click skip.",
        "The same CAPTCHA with an error: Are you sure? Look again. Note: most people can't.",
        "Every square of the photo is selected. Text: Correct answer: every single square. Struggle rarely looks like struggle.",
        "What the photo didn't show: each colleague's smiling face beside what they're carrying: sleeping 4 hours a night since the re-org; had a panic attack in the washroom at 11 AM; his dad's in the ICU and nobody here knows; laughing, going through a divorce; cried in the car before logging in; her best day this month, ask about the other 29; sure he's first on the layoff list.",
        "8 in 10 employees in India reported a mental-health concern in the past year. ₹1.1 lakh crore a year is what poor mental health costs Indian employers. Source: Deloitte, 2022.",
        "You can't spot it. So make it safe to say. A checkbox reads: I'm not okay. YourDOST for teams: contact@yourdost.com.",
      ],
    },

    /* ===================== C22 · OLD LIGHT · STARS ===================== */
    {
      id: "22", slug: "Carousel-Old-Light", kind: "carousel", segment: "Young adults and students (18–30), the people most likely to send a check-in to a friend",
      date: "Mon 14 Dec 2026", time: "9:00 PM IST", theme: "Checking in on people who look fine",
      line: "The starlight you see tonight left its star years ago.",
      why: "It opens on a true, slightly mind-bending fact under a beautiful sky, which is why people swipe and save. Then it turns: people work the same way. The ‘all good!’ text and the trip photos are old light. It ends with the simplest action, ask how they are tonight. It's evergreen and very shareable, and it goes out on the night of the Geminid meteor shower, when people are already looking up.",
      slides: [
        () => `<div class="ph" style="background-image:url(ai/c22-milkyway.jpg);background-position:50% 40%"></div><div class="scrim-t" style="opacity:0.75"></div>
          <div class="abs" style="left:64px;right:180px;top:96px"><span class="eyebrow glass">Look up tonight</span>
          <p class="h l light" style="margin-top:28px">The starlight you see tonight left its star years ago.</p>
          <p class="h s y" style="margin-top:22px;text-shadow:0 2px 20px rgba(0,0,0,0.5)">Some of it, before you were born.</p></div>
          <p class="caption-tag abs" style="left:64px;bottom:52px">Hanle, Ladakh, is India's first dark-sky reserve.</p>${count(1, 5, "lite")}${badge}`,
        () => `<div class="ph" style="background-image:url(ai/c22-planetarium.jpg);background-position:50% 30%"></div><div class="scrim-t" style="opacity:0.55"></div>
          <div class="abs" style="left:64px;right:180px;top:110px"><p class="h light">So you never see a star as it is now.</p><p class="h light lav" style="margin-top:20px">Only as it was, when its light set out.</p></div>
          <div class="abs" style="left:64px;right:64px;bottom:110px;background:rgba(10,10,30,0.6);border:1.5px solid rgba(255,255,255,0.2);border-radius:24px;padding:22px 28px;color:#fff;font-family:Inter;font-size:27px;line-height:1.4">★ <b>Sirius</b>, the brightest star in our sky: the light you see tonight set out about <b style="color:#f6d25a">8.6 years ago</b>.</div>${count(2, 5, "lite")}${badge}`,
        () => `<div class="ph" style="background-image:url(ai/c22-city.jpg);background-position:50% 50%"></div><div class="fill" style="background:linear-gradient(180deg,rgba(4,6,20,0.85) 0%,rgba(4,6,20,0.7) 55%,rgba(4,6,20,0.25) 100%)"></div>
          <div class="abs" style="left:64px;right:120px;top:110px"><p class="h light">People are a bit like stars.</p>
          <div style="margin-top:44px;display:flex;flex-direction:column;gap:26px;color:#fff;font-size:40px;line-height:1.3;font-weight:500">
            <p><span class="y">✦</span>&nbsp; The “all good!” text from last week.</p><p><span class="y">✦</span>&nbsp; The laughing photos from the trip.</p><p><span class="y">✦</span>&nbsp; The “haha, just busy” reply.</p></div>
          <p class="h xl y" style="margin-top:52px">All old light.</p></div>${count(3, 5, "lite")}${badge}`,
        () => `<div class="ph" style="background-image:url(ai/c22-dawn.jpg);background-position:50% 50%"></div><div class="scrim-t" style="opacity:0.7"></div>
          <div class="abs" style="left:64px;right:180px;top:110px"><p class="h l light">So don't go by the light.</p><p class="h l light y" style="margin-top:16px">Ask how they are tonight.</p></div>
          <p class="note abs" style="left:64px;top:470px;color:#fff;text-shadow:0 2px 14px rgba(0,0,0,0.6)">send this to someone you haven't checked on</p>${count(4, 5, "lite")}${badge}`,
        () => `<div class="fill" style="background:radial-gradient(ellipse at 50% 110%,#3b2a7a 0%,#15123a 45%,#07071a 100%)"></div>${stars(170, 11)}
          <div class="abs" style="left:72px;right:120px;top:300px"><p class="h light">And if your own light has been out for a while,</p><p class="h light y" style="margin-top:18px">talk to someone who gets it.</p>
          <div style="margin-top:56px"><span class="cta inv">Talk to a certified expert, 24/7 · <b>yourdost.com</b></span></div>
          <p class="small" style="color:rgba(255,255,255,0.72);margin-top:22px">Chat, call or video. Confidential.</p></div>${count(5, 5, "lite")}${badge}`,
      ],
      caption: "The starlight you see tonight left its star years ago. ✨\n\nSo you're never seeing a star as it is now, only as it was.\n\nPeople can be like that. The “all good!” text, the trip photos, the “haha, just busy”: all old light.\n\nDon't go by the light. Ask how they are tonight.",
      tags: "#Geminids #NightSky #Stargazing #CheckOnYourFriends #MentalHealthAwareness #YourDOST",
      first: "Send this to one person whose light you haven't checked on in a while. ✨",
      alt: [
        "The Milky Way arches over the snowy mountains of Ladakh with a small observatory dome on a ridge. Text: The starlight you see tonight left its star years ago. Some of it, before you were born.",
        "An empty planetarium with a dome full of stars. Text: So you never see a star as it is now. Only as it was, when its light set out. Sirius's light is about 8.6 years old.",
        "City apartment towers at night with lit windows under a starry sky. Text: People are a bit like stars. The “all good!” text from last week. The laughing photos from the trip. The “haha, just busy” reply. All old light.",
        "Dawn over the Himalaya, a chorten with prayer flags on the ridge. Text: So don't go by the light. Ask how they are tonight.",
        "A starry sky. Text: And if your own light has been out for a while, talk to someone who gets it. Talk to a certified expert, 24/7, yourdost.com.",
      ],
    },

    /* ===================== C23 · STEPWELL · ARCHITECTURE ===================== */
    {
      id: "23", slug: "Carousel-The-Stepwell", kind: "carousel", segment: "Adults 22–40 who are curious about therapy but haven't started (first-time users)",
      date: "Sun 10 Jan 2027", time: "7:00 PM IST", theme: "What therapy actually feels like",
      line: "This well has 3,500 steps. The water is at the very bottom.",
      why: "One of the most striking structures in India, and a metaphor that does the explaining. Rajasthan's builders knew that in a dry land the water is deep, so they built a way down. Therapy can feel like that: going down a few steps first. It answers the real hesitation of first-time users, ‘will it be hard?’, and positions the YourDOST expert as the one who walks down with you. It's evergreen and people save it.",
      slides: [
        () => `<div class="ph" style="background-image:url(ai/c23-stepwell-top.jpg);background-position:50% 60%"></div><div class="scrim-t" style="opacity:0.9"></div>
          <div class="abs" style="left:64px;right:180px;top:96px"><span class="eyebrow">Chand Baori · Rajasthan</span>
          <p class="h xl light" style="margin-top:28px">This well has 3,500 steps.</p><p class="h s light y" style="margin-top:18px">The water is at the very bottom.</p></div>
          <p class="caption-tag abs" style="left:64px;bottom:52px;color:#fff;text-shadow:0 1px 8px rgba(0,0,0,0.8)">Built more than 1,000 years ago · 13 levels deep</p>${count(1, 5, "lite")}${badge}`,
        () => `<div class="ph" style="background-image:url(ai/c23-stepwell-up.jpg);background-position:50% 50%"></div><div class="scrim-b"></div>
          <div class="abs" style="left:64px;right:110px;bottom:120px"><p class="h light">Its builders knew: in a dry land, the water is deep.</p><p class="h light y" style="margin-top:18px">So they built a way down.</p></div>${count(2, 5, "lite")}${badge}`,
        () => `<div class="ph" style="background-image:url(ai/c23-stepwell-top.jpg);background-size:170%;background-position:50% 92%"></div><div class="scrim-t" style="opacity:0.95"></div>
          <div class="abs" style="left:64px;right:150px;top:110px"><p class="h light">Getting better can work like that.</p>
          <p class="body" style="color:#fff;margin-top:26px;font-size:38px;line-height:1.45;text-shadow:0 2px 16px rgba(0,0,0,0.6)">Some days it means going down a few steps first: to the hard memory, the real reason, the thing you never said out loud.</p></div>${count(3, 5, "lite")}${badge}`,
        () => `<div class="ph" style="background-image:url(ai/c23-diya.jpg);background-position:50% 50%"></div><div class="scrim-t" style="opacity:0.7"></div>
          <div class="abs" style="left:64px;right:180px;top:120px"><p class="h l light">You don't have to take the steps alone.</p></div>${count(4, 5, "lite")}${badge}`,
        () => `<div class="ph" style="background-image:url(ai/c23-stepwell-top.jpg);background-position:50% 40%;filter:blur(3px)"></div><div class="fill" style="background:rgba(70,40,15,0.8)"></div>
          <div class="abs" style="left:72px;right:120px;top:250px"><p class="h light">A YourDOST expert walks them with you.</p><p class="h s light y" style="margin-top:20px">Chat, call or video. Confidential. 24/7.</p>
          <div style="margin-top:56px"><span class="cta inv">Talk to a certified expert · <b>yourdost.com</b></span></div></div>
          <p class="note abs" style="left:72px;bottom:110px;color:#fff">save this for the day you need it</p>${count(5, 5, "lite")}${badge}`,
      ],
      caption: "This well has 3,500 steps. The water is at the very bottom. 🏛️\n\nChand Baori in Rajasthan was built more than a thousand years ago, 13 levels deep. Its builders knew that in a dry land, the water is deep, so they built a way down.\n\nGetting better can work like that. Some days it means going down a few steps first. You don't have to take them alone.",
      tags: "#ChandBaori #Rajasthan #IncredibleIndia #Therapy #Healing #MentalHealthMatters #YourDOST",
      first: "Save this for the day you need it. And if today's that day, our experts are online 24/7. 💛",
      alt: [
        "Looking down into a vast stepwell: thousands of zigzag sandstone steps descend to a small pool of green water. Text: This well has 3,500 steps. The water is at the very bottom. Chand Baori, Rajasthan, built more than 1,000 years ago, 13 levels deep.",
        "Looking up from the bottom of the stepwell towards the sky, carved galleries rising on every side. Text: Its builders knew: in a dry land, the water is deep. So they built a way down.",
        "Close view of the steps near the water. Text: Getting better can work like that. Some days it means going down a few steps first: to the hard memory, the real reason, the thing you never said out loud.",
        "A single lit diya on a step above the water at the bottom of the well. Text: You don't have to take the steps alone.",
        "Text over warm sandstone: A YourDOST expert walks them with you. Chat, call or video. Confidential. 24/7. yourdost.com.",
      ],
    },

    /* ===================== O24 · CORPORATE · PEOPLE · ORIGINAL ===================== */
    {
      id: "24", slug: "Original-Inner-Captions", kind: "single", segment: "Corporate teams: managers who run stand-ups, HR, and employees in hybrid and remote teams",
      date: "Mon 4 Jan 2027", time: "9:30 AM IST", theme: "What people don't say in meetings",
      line: "We switched on inner captions in today's stand-up.",
      why: "An original format: a video call where live captions show what each person is actually thinking under what they said. It's the first Monday back after the holidays, stand-up time. Everyone has been in this exact call, and the gap between ‘Super good!’ and ‘I cried in the washroom at 9:12’ is the hook. It ends with a practical idea for managers (add a check-in) and the B2B line.",
      slides: [
        () => `<div class="fill paper"></div>
          <div class="abs" style="left:56px;right:190px;top:70px"><span class="eyebrow">Monday stand-up</span><p class="h s" style="margin-top:18px;font-size:54px">We switched on inner captions in today's stand-up.</p></div>
          <div class="meet" style="top:290px;bottom:140px">
            <div class="bar"><span><span class="rec"></span><b>Daily stand-up</b> · 9:30 AM · 6 people</span><span class="tog"><i></i>Inner captions · beta</span></div>
            <div class="tiles">${TILES.map(tileHTML).join("")}</div></div>
          <div class="abs" style="left:56px;right:56px;bottom:36px;display:flex;align-items:center;justify-content:space-between;gap:20px">
            <p style="font-weight:600;font-size:30px;line-height:1.2">Everyone said “good.”<br><span style="color:#5b4a9c">Does your stand-up have a check-in?</span></p>
            <span class="cta" style="font-size:24px;padding:16px 26px">YourDOST for teams · <b>contact@yourdost.com</b></span></div>${badge}`,
      ],
      caption: "We switched on inner captions in today's stand-up. 🎧\n\nEveryone said “good.” Nobody was.\n\nYour stand-up has an agenda. Does it have a check-in? And when someone needs more than a check-in, YourDOST gives every employee a confidential expert, 24/7.\n\nFor teams: contact@yourdost.com",
      tags: "#Standup #RemoteWork #HybridWork #Leadership #MentalHealthAtWork #EmployeeWellbeing #YourDOST",
      first: "If inner captions were real, what would yours say in today's stand-up? 👇",
      alt: ["A video-call stand-up with six people and an Inner captions toggle switched on. Each tile shows what they said and what they meant. Arjun, host: “Quick round! How's everyone doing?” Inner: I haven't slept properly since the re-org. Neha: “Super good!” Inner: I cried in the washroom at 9:12. Rahul: “All good. I can take more.” Inner: I can't say no. I'm drowning. Fatima: “Doing well, thanks.” Inner: Is my name on the layoff list? Vikram, camera off: “Yeah, all fine.” Inner: Logged in from Papa's hospital room. Sneha: “Never better, haha.” Inner: Sunday dread starts on Saturday now. Footer: Everyone said “good.” Does your stand-up have a check-in? YourDOST for teams, contact@yourdost.com."],
    },

    /* ===================== O25 · GALLERY LABEL · PAINTING ===================== */
    {
      id: "25", slug: "Original-The-Gallery-Label", kind: "single", segment: "Urban young professionals and creatives (22–35), the people who post and share art",
      date: "Thu 7 Jan 2027", time: "8:00 PM IST", theme: "The ‘I'm fine’ mask",
      line: "Most people walk past this painting in 3 seconds.",
      why: "An original format: a museum wall label for a painting everyone has made. The yellow stroke over a storm is ‘I'm fine’, and the label reads like a curator's note, so people stop and actually read it, which is rare on Instagram. The comment prompt (‘what would your painting be called?’) gets thoughtful replies, and it's evergreen.",
      slides: [
        () => `<div class="ph" style="background-image:url(ai/o25-gallery-45.jpg)"></div>
          <div class="abs" style="left:64px;right:190px;top:74px"><p class="h s" style="font-size:54px;color:#1b1b1f">Most people walk past this painting in 3 seconds.</p></div>
          <div class="museum" style="left:690px;width:345px;top:470px">
            <p class="no">Gallery 1 · No. 1 of many</p><p class="art">Almost everyone</p><p class="ti"><i>I'm Fine</i>, 2026</p>
            <p class="md">A smile, worn daily, over a storm.<br>Oil on everything.</p>
            <p class="tx">Look closer. The yellow is one thin layer. Underneath, the storm is still being painted.<br><br>On permanent view in offices, hostels and family group chats.</p></div>
          <div class="abs" style="left:0;right:0;bottom:44px;display:flex;justify-content:center"><span class="cta">If it's yours, talk to a certified expert, 24/7 · <b>yourdost.com</b></span></div>
          <p class="note abs" style="left:64px;top:1050px;color:#1b1b1f;font-size:44px;transform:rotate(-4deg)">what would yours be called?</p>${badge}`,
      ],
      caption: "Most people walk past this painting in 3 seconds. 🖼️\n\nI'm Fine, 2026. Artist: almost everyone. A smile, worn daily, over a storm.\n\nLook closer: the yellow is one thin layer. If this one's yours, you don't have to keep it on the wall. A YourDOST expert is there, 24/7.",
      tags: "#ArtGallery #ModernArt #ImFine #MentalHealthAwareness #ArtTherapy #YourDOST",
      first: "If your last month were a painting, what would it be called? Title only. 👇",
      alt: ["A quiet gallery with a large abstract painting: dark, stormy strokes of indigo and grey with one bright yellow curved stroke like a smile. A museum label reads: Almost everyone. I'm Fine, 2026. A smile, worn daily, over a storm. Oil on everything. Look closer. The yellow is one thin layer. Underneath, the storm is still being painted. On permanent view in offices, hostels and family group chats. Headline: Most people walk past this painting in 3 seconds. Note: what would yours be called? If it's yours, talk to a certified expert, 24/7, yourdost.com."],
    },

    /* ===================== O26 · EVEREST · MOUNTAINS ===================== */
    {
      id: "26", slug: "Original-Everest-Rest-Days", kind: "single", segment: "High achievers: consultants, founders, toppers and anyone who wears ‘no days off’ as a badge",
      date: "Sat 29 May 2027", time: "9:00 AM IST", theme: "Rest as part of performance",
      line: "Even Everest climbers take rest days.",
      why: "It speaks the language of achievers: ambition, summits, plans. Climbers reach the top by going up, coming back down and resting, again and again, and the chart shows it. Next to it, the ‘no rest days’ line goes straight up and then crashes. It reframes rest as strategy, not weakness. It goes out on International Everest Day (29 May) and works as an evergreen save.",
      slides: [
        () => `<div class="ph" style="background-image:url(ai/o26-basecamp-45.jpg)"></div><div class="fill" style="background:linear-gradient(180deg,rgba(4,10,30,0.55) 0%,rgba(4,10,30,0.2) 45%,rgba(4,10,30,0) 60%,rgba(4,10,30,0) 78%,rgba(4,10,30,0.7) 100%)"></div>
          <div class="abs" style="left:56px;right:190px;top:64px"><span class="eyebrow glass">Everest · 8,849 m</span><p class="h light" style="margin-top:20px;font-size:70px">Even Everest climbers take rest days.</p></div>
          <div class="chart" style="top:330px">
            <div class="hd"><b>How climbers actually reach the top</b><span>~6 weeks</span></div>
            <div style="margin-top:10px">${chart()}</div>
            <div class="legend"><span><i style="background:#f6d25a"></i>Up, back down, rest. Repeat.</span><span><i style="background:#ff7a5c"></i>No rest days</span></div></div>
          <div class="abs" style="left:56px;right:56px;bottom:40px;display:flex;justify-content:space-between;align-items:flex-end;gap:20px">
            <p style="color:#fff;font-weight:600;font-size:34px;line-height:1.25;text-shadow:0 2px 16px rgba(0,0,0,0.7)">Rest isn't quitting.<br><span class="y">It's how you reach the top.</span></p>
            <span class="cta inv" style="font-size:22px;padding:14px 22px">Talk to an expert, 24/7 · <b>yourdost.com</b></span></div>${badge}`,
      ],
      caption: "Even Everest climbers take rest days. 🏔️\n\nNobody goes straight up. Climbers spend weeks going up, coming back down to base camp, and resting, so their bodies can handle the top.\n\nRest isn't quitting. It's how you reach the top. If you can't remember your last rest day, talk to a YourDOST expert, 24/7.",
      tags: "#InternationalEverestDay #Everest #Himalayas #HustleCulture #Burnout #Rest #YourDOST",
      first: "When was your last real rest day? Drop the date. 👇",
      alt: ["Everest base camp at dawn: orange and yellow tents, prayer flags and glowing snow peaks. A chart compares how climbers reach the summit (up, back down to base camp, rest, repeat, over about six weeks) with a ‘no rest days’ line that shoots straight up and crashes into burnout. Text: Even Everest climbers take rest days. Rest isn't quitting. It's how you reach the top. Talk to an expert, 24/7, yourdost.com."],
    },
  ];

  function frame(post, i = 0) { return `<div class="f">${post.slides[i]()}</div>`; }
  root.YD7 = { POSTS, frame };
})(typeof window !== "undefined" ? window : globalThis);
