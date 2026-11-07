/* YourDOST Instagram set, v3: 3 reels, 5 carousels, 2 single images. English only.
   Visual system matched to @yourdostcom's own carousels; story structure follows the reference posts. */
(function (root) {
  "use strict";
  const Y = "#f6d25a", L = "#e1cbf9", P = "#5b4a9c", K = "#0d1015", PEACH = "#f6b8a2", SAGE = "#bcd6a7", LB = "#cdb6f2", GOLD = "#d4a62a";

  // ---------- animation helpers (frames are pure functions of t) ----------
  const C = (x) => Math.max(0, Math.min(1, x));
  const E = (x) => 1 - Math.pow(1 - C(x), 3);
  const p = (t, a, d = 0.45) => E((t - a) / d);
  const f3 = (n) => n.toFixed(3);
  const up = (t, a, d = 0.45, y = 40) => { const k = p(t, a, d); return `opacity:${f3(k)};transform:translateY(${((1 - k) * y).toFixed(1)}px)`; };
  const pop = (t, a, d = 0.35) => { const k = p(t, a, d); return `opacity:${f3(k)};transform:scale(${f3(0.88 + 0.12 * k)})`; };

  // ---------- decor: one continuous wave across all slides of a carousel ----------
  function wavePath(n, H, base, a1, a2, ph) {
    let d = `M0 ${H}`;
    for (let x = 0; x <= n * 1080; x += 24) d += ` L${x} ${(H - base + a1 * Math.sin(x / 260 + ph) + a2 * Math.sin(x / 113 + ph * 2)).toFixed(1)}`;
    return d + ` L${n * 1080} ${H} Z`;
  }
  function decor(i, n, H) {
    const sparkles = (x, y, c) => [[0, 0, -20], [34, 14, 10], [10, 40, 40]].map(([dx, dy, r]) => `<rect x="${x + dx}" y="${y + dy}" width="30" height="9" rx="4.5" fill="${c}" transform="rotate(${r} ${x + dx} ${y + dy})"/>`).join("");
    return `<svg class="decor" viewBox="${i * 1080} 0 1080 ${H}" preserveAspectRatio="none" width="1080" height="${H}">
      <path d="${wavePath(n, H, 150, 46, 22, 0.4)}" fill="${Y}" opacity=".55"/>
      <path d="${wavePath(n, H, 84, 26, 14, 2.1)}" fill="${L}" opacity=".7"/>
      ${sparkles(i * 1080 + 930, 70, i % 2 ? P : Y)}
    </svg>`;
  }
  function reelDecor(H = 1920) {
    return `<svg class="decor" viewBox="0 0 1080 ${H}" width="1080" height="${H}">
      <path d="M1080 ${H - 520} C 900 ${H - 470} 860 ${H - 300} 920 ${H - 180} C 960 ${H - 90} 1040 ${H - 40} 1080 ${H - 30} Z" fill="${Y}" opacity=".6"/>
      <path d="M0 ${H - 260} C 140 ${H - 300} 260 ${H - 200} 300 ${H} L0 ${H} Z" fill="${L}" opacity=".7"/>
      <circle cx="990" cy="420" r="90" fill="${L}" opacity=".55"/>
    </svg>`;
  }
  const badge = `<img class="badge" src="brand/badge.png" alt="YourDOST">`;

  // ---------- blob characters (pastel, like the reference posts) ----------
  function blob({ c = Y, w = 220, mood = "smile", cheeks = true, tilt = 0, extra = "" } = {}) {
    const eyes = mood === "calm"
      ? `<path d="M68 100 Q78 92 88 100 M112 100 Q122 92 132 100" fill="none" stroke="#2b2b2b" stroke-width="5" stroke-linecap="round"/>`
      : `<circle cx="80" cy="100" r="7" fill="#2b2b2b"/><circle cx="120" cy="100" r="7" fill="#2b2b2b"/>`;
    const mouth = { smile: "M88 122 Q100 134 112 122", sad: "M88 132 Q100 120 112 132", flat: "M90 128 L110 128", calm: "M90 124 Q100 132 110 124", worried: "M88 130 Q94 124 100 128 Q106 132 112 126" }[mood] || "M88 122 Q100 134 112 122";
    return `<svg viewBox="0 0 200 200" width="${w}" height="${w}" style="overflow:visible;transform:rotate(${tilt}deg)">
      <ellipse cx="100" cy="194" rx="70" ry="8" fill="#000" opacity=".08"/>
      <path d="M100 22 C150 20 184 64 184 114 C184 162 148 190 100 190 C52 190 16 162 16 114 C16 64 50 24 100 22 Z" fill="${c}" stroke="#2b2b2b" stroke-width="4"/>
      ${eyes}
      <path d="${mouth}" fill="none" stroke="#2b2b2b" stroke-width="5" stroke-linecap="round"/>
      ${cheeks ? `<ellipse cx="62" cy="122" rx="11" ry="6" fill="#f08f86" opacity=".55"/><ellipse cx="138" cy="122" rx="11" ry="6" fill="#f08f86" opacity=".55"/>` : ""}
      ${extra}
    </svg>`;
  }

  // ---------- icons (purple, like YourDOST's stat cards) ----------
  const ICON = {
    moon: `<path d="M30 5a19 19 0 1 0 13 31A16 16 0 0 1 30 5z" fill="${P}"/><circle cx="12" cy="10" r="2.5" fill="${P}"/><circle cx="20" cy="4" r="1.8" fill="${P}"/>`,
    bulb: `<path d="M24 3a14 14 0 0 0-8.5 25.1c1.4 1.1 2.5 2.8 2.5 4.6V35h12v-2.3c0-1.8 1.1-3.5 2.5-4.6A14 14 0 0 0 24 3z" fill="${P}"/><rect x="17.5" y="38" width="13" height="4" rx="2" fill="${P}"/><rect x="20" y="44" width="8" height="3" rx="1.5" fill="${P}"/>`,
    steps: `<ellipse cx="15" cy="31" rx="6.5" ry="10" fill="${P}"/><ellipse cx="33" cy="17" rx="6.5" ry="10" fill="${P}"/><circle cx="15" cy="45" r="3.2" fill="${P}"/><circle cx="33" cy="31" r="3.2" fill="${P}"/>`,
    heart: `<path d="M24 43C9 33 3 25 3 16.5a10.5 10.5 0 0 1 21-2.2 10.5 10.5 0 0 1 21 2.2C45 25 39 33 24 43z" fill="${P}"/>`,
    lock: `<rect x="9" y="21" width="30" height="23" rx="5" fill="${P}"/><path d="M15 21v-6a9 9 0 0 1 18 0v6" fill="none" stroke="${P}" stroke-width="5"/><circle cx="24" cy="32" r="3.5" fill="#fff"/>`,
    chat: `<path d="M8 8h32a5 5 0 0 1 5 5v18a5 5 0 0 1-5 5H20l-9 8v-8H8a5 5 0 0 1-5-5V13a5 5 0 0 1 5-5z" fill="${P}"/><circle cx="16" cy="22" r="3" fill="#fff"/><circle cx="24" cy="22" r="3" fill="#fff"/><circle cx="32" cy="22" r="3" fill="#fff"/>`,
    globe: `<circle cx="24" cy="24" r="19" fill="none" stroke="${P}" stroke-width="4.5"/><ellipse cx="24" cy="24" rx="8" ry="19" fill="none" stroke="${P}" stroke-width="4"/><path d="M6 18h36M6 30h36" stroke="${P}" stroke-width="4"/>`,
    clock: `<circle cx="24" cy="24" r="19" fill="${P}"/><path d="M24 13v12l8 5" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>`,
    music: `<path d="M18 36V10l22-5v26" fill="none" stroke="${P}" stroke-width="4.5" stroke-linejoin="round"/><ellipse cx="13" cy="36" rx="6.5" ry="5.5" fill="${P}"/><ellipse cx="35" cy="31" rx="6.5" ry="5.5" fill="${P}"/>`,
    eye: `<path d="M3 24C9 13 16 9 24 9s15 4 21 15c-6 11-13 15-21 15S9 35 3 24z" fill="${P}"/><circle cx="24" cy="24" r="8" fill="#fff"/><circle cx="24" cy="24" r="4" fill="${P}"/>`,
    shield: `<path d="M24 3l17 6v13c0 11-7 19-17 23C14 41 7 33 7 22V9z" fill="${P}"/><path d="M16 24l6 6 11-12" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>`,
    bolt: `<path d="M27 3L9 27h12l-3 18 21-26H27z" fill="${P}"/>`,
    phone: `<path d="M14 4l7 9-4 5c2 5 7 10 12 12l5-4 9 7-5 8C25 40 8 23 6 9z" fill="${P}"/>`,
    video: `<rect x="3" y="11" width="30" height="26" rx="5" fill="${P}"/><path d="M35 19l10-6v22l-10-6z" fill="${P}"/>`,
    person: `<circle cx="24" cy="14" r="9" fill="${P}"/><path d="M7 44c1-10 8-16 17-16s16 6 17 16z" fill="${P}"/>`,
  };
  const icon = (name, bg = "l") => `<span class="icon ${bg}"><svg viewBox="0 0 48 48">${ICON[name]}</svg></span>`;

  // ---------- objects ----------
  const marksheet = () => `
    <div class="paper sheet">
      <div class="t">STATEMENT OF MARKS · 2026</div>
      <p class="nm">NAME OF CANDIDATE: <b>RIYA SHARMA</b></p>
      <div style="margin-top:10px"><div class="row"><span>English</span><span>94</span></div><div class="row"><span>Mathematics</span><span>95</span></div><div class="row"><span>Physics</span><span>89</span></div></div>
      <div class="tot"><span>AGGREGATE</span><strong>92.4%</strong></div>
    </div>`;
  const chat = (typed, msgs = true) => `
    <div class="paper chat">
      <div class="bar"><div class="av">?</div><div class="who"><b>Don't.</b><small>last seen today at 11:47 pm</small></div></div>
      ${msgs ? `<div class="msgs"><span class="day">14 SEPTEMBER</span><div class="b">ok.</div><div class="b me">take care ❤️</div><span class="day">TODAY</span></div>` : ""}
      <div class="type"><div>${typed}<span class="caret"></span></div></div>
    </div>`;
  const exitForm = () => `
    <div class="paper form">
      <div class="fh"><span>EXIT INTERVIEW</span><span>FORM HR-07</span></div>
      <h4>Priya M. · Senior Analyst</h4>
      <p class="meta">3 years 2 months · Rated “exceeds expectations” twice</p>
      <p class="q">Primary reason for leaving</p>
      <div class="opts"><div class="opt"><span class="cb"></span>Compensation</div><div class="opt"><span class="cb on"></span>Better opportunity</div><div class="opt"><span class="cb"></span>Relocation</div><div class="opt"><span class="cb"></span>Higher studies</div></div>
    </div>`;
  const kintsugi = (w = 520) => `
    <svg viewBox="0 0 520 380" width="${w}" style="overflow:visible">
      <ellipse cx="260" cy="356" rx="190" ry="16" fill="#000" opacity=".07"/>
      <path d="M70 110 L450 110 Q440 300 330 340 L190 340 Q80 300 70 110 Z" fill="#fff" stroke="#2b2b2b" stroke-width="6" stroke-linejoin="round"/>
      <ellipse cx="260" cy="110" rx="190" ry="26" fill="#faf3dc" stroke="#2b2b2b" stroke-width="6"/>
      <path d="M450 150 C520 150 520 250 440 262" fill="none" stroke="#2b2b2b" stroke-width="6" stroke-linecap="round"/>
      <path d="M200 136 L232 186 L210 232 L252 280 L238 336" fill="none" stroke="${GOLD}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M232 186 L300 206 L338 196" fill="none" stroke="${GOLD}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M252 280 L318 300" fill="none" stroke="${GOLD}" stroke-width="8" stroke-linecap="round"/>
      ${[[150, 60], [380, 40], [430, 70], [120, 30]].map(([x, y]) => `<path d="M${x} ${y - 14} L${x + 4} ${y - 4} L${x + 14} ${y} L${x + 4} ${y + 4} L${x} ${y + 14} L${x - 4} ${y + 4} L${x - 14} ${y} L${x - 4} ${y - 4} Z" fill="${Y}"/>`).join("")}
    </svg>`;
  const squiggle = () => `
    <svg viewBox="0 0 860 300" width="860" height="300" style="overflow:visible">
      <path d="M20 260 C120 250 140 170 210 190 C290 214 250 290 330 250 C420 206 360 120 450 140 C540 160 500 230 590 180 C680 130 640 60 720 70 C780 76 800 40 840 30" fill="none" stroke="${P}" stroke-width="10" stroke-linecap="round"/>
      <circle cx="20" cy="260" r="16" fill="${Y}" stroke="#2b2b2b" stroke-width="4"/><circle cx="840" cy="30" r="16" fill="${Y}" stroke="#2b2b2b" stroke-width="4"/>
      <text x="0" y="300" font-family="Poppins" font-size="24" fill="#555">the breakup</text><text x="720" y="10" font-family="Poppins" font-size="24" fill="#555">okay again</text>
    </svg>`;

  // ---------- slide shells ----------
  const CTA = `<div class="cta">Talk to a certified expert, 24/7 <b>yourdost.com</b></div>`;
  const HELP = `<p class="help">Feeling unsafe? Call <b>Tele MANAS 14416</b>, free and 24/7.</p>`;
  function slide(i, n, inner, { swipe = false, cls = "" } = {}) {
    return `${decor(i, n, 1350)}${badge}<div class="wrap ${cls}">${inner}</div>${swipe ? `<div class="swipe">Swipe →</div>` : ""}`;
  }
  function carousel(slides) { return slides.map((fn, i) => () => slide(i, slides.length, ...fn(i, slides.length))); }
  const stem = (lead, line, ic, body = "") => () => [`
      <p class="eyebrow">${lead}</p>
      <p class="h1 m">${line}</p>
      ${body ? `<p class="p">${body}</p>` : ""}
      <div style="flex:1;display:flex;align-items:center">${ic}</div>`, {}];

  // ---------- reels ----------
  function reelFrame(reel, t) {
    const out = [`${reelDecor()}${badge}`];
    reel.scenes.forEach((s, i) => {
      const last = i === reel.scenes.length - 1;
      if (t < s.a - 0.001 || (!last && t > s.b + 0.3)) return;
      const o = (i === 0 ? 1 : p(t, s.a, 0.3)) * (last ? 1 : 1 - p(t, s.b, 0.3));
      out.push(`<div class="wrap" style="opacity:${f3(o)}">${s.html(t - s.a, t)}</div>`);
    });
    return out.join("");
  }
  const endCard = (lt, line, extra = "") => `
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:40px">
      <img src="brand/badge.png" style="width:300px;${pop(lt, 0.05)}" alt="">
      <p class="h1 m" style="${up(lt, 0.25)}">${line}</p>
      <div style="${up(lt, 0.5)}">${CTA}</div>
      ${extra ? `<div style="${up(lt, 0.7)}">${extra}</div>` : ""}
    </div>`;

  const REEL_DIWALI = { dur: 16.5, cover: 2.6, scenes: [
    { a: 0, b: 3.6, html: (lt) => {
      const items = [["Cupboards", 0.15], ["Ceiling fans", 0.55], ["Kitchen tiles", 0.95], ["Your mind", 99]];
      return `<p class="eyebrow" style="${up(lt, 0)}">Diwali cleaning checklist</p>
        <p class="h1">Everything's spotless.<br><span class="mk">Almost.</span></p>
        <div class="paper" style="padding:46px 54px;display:flex;flex-direction:column;gap:30px;width:900px">
          ${items.map(([x, at]) => `<div style="display:flex;gap:26px;align-items:center;font-size:52px;font-weight:500"><span class="cb ${lt > at ? "on" : ""}" style="width:64px;height:64px;transform:scale(1.25)"></span><span style="${at === 99 ? "background:" + L + ";border-radius:12px;padding:0 14px" : lt > at + 0.1 ? "text-decoration:line-through;text-decoration-thickness:4px;color:#888" : ""}">${x}</span></div>`).join("")}
        </div>`; } },
    { a: 3.6, b: 7.4, html: (lt) => `
        <p class="h1 m" style="${up(lt, 0.05)}">We dust every corner before the guests arrive.</p>
        <p class="h1 m" style="${up(lt, 1.1)}">But the worry, the tiredness, the <span class="mk l">“I'm fine”</span>…</p>
        <p class="h1 m" style="${up(lt, 2.2)}">we carry those into the celebration.</p>` },
    { a: 7.4, b: 12.0, html: (lt) => `
        <p class="eyebrow" style="${up(lt, 0)}">Try this before the guests arrive</p>
        <p class="h1 m" style="${up(lt, 0.15)}">A 2-minute clean-up for your mind</p>
        ${[["1", "Breathe out slowly, three times."], ["2", "Name one thing that feels heavy."], ["3", "Tell one person you trust."]].map(([n, x], k) => `<div class="card ${k % 2 ? "l" : "y"}" style="${up(lt, 0.7 + k * 0.8)}"><span class="num" style="font-size:80px">${n}</span><span class="lbl" style="font-size:46px;font-weight:500">${x}</span></div>`).join("")}` },
    { a: 12.0, b: 14.2, html: (lt, t) => `
        <div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:50px;text-align:center">
          ${diya(t, p(lt, 0.1, 0.8))}
          <p class="h1" style="${up(lt, 0.6)}">Light a diya for <span class="mk">your mind</span> too.</p>
        </div>` },
    { a: 14.2, b: 16.5, html: (lt) => endCard(lt, "Happy Diwali from YourDOST") },
  ] };
  function diya(t, k) {
    const fl = 1 + 0.05 * Math.sin(t * 17) + 0.03 * Math.sin(t * 29);
    return `<svg viewBox="0 0 520 400" width="520" height="400" style="overflow:visible">
      <circle cx="260" cy="150" r="${(150 * k).toFixed(1)}" fill="${Y}" opacity=".35"/>
      <g transform="translate(260 196) scale(${f3(k * fl)} ${f3(k * (2 - fl))}) translate(-260 -196)"><path d="M260 56 C300 104 312 150 260 196 C208 150 220 104 260 56 Z" fill="${PEACH}" stroke="#2b2b2b" stroke-width="6"/><path d="M260 112 C276 136 280 156 260 180 C240 156 244 136 260 112 Z" fill="${Y}"/></g>
      <path d="M90 230 L430 230 Q400 370 260 370 Q120 370 90 230 Z" fill="#e9a07a" stroke="#2b2b2b" stroke-width="6" stroke-linejoin="round"/>
      <ellipse cx="260" cy="230" rx="172" ry="26" fill="${Y}" stroke="#2b2b2b" stroke-width="6"/>
      ${[190, 260, 330].map((x, i) => `<circle cx="${x}" cy="${i === 1 ? 312 : 294}" r="12" fill="${L}" stroke="#2b2b2b" stroke-width="4"/>`).join("")}
    </svg>`;
  }

  const REEL_JOBS = { dur: 17, cover: 2.5, scenes: [
    { a: 0, b: 3.2, html: (lt) => `
        <p class="eyebrow">Job hunt · Day 94</p>
        <p class="h1 m">Application</p>
        <div class="counter">#${String(Math.max(1, Math.round(147 * p(lt, 0.05, 2.0)))).padStart(3, "0")}</div>
        <div style="${up(lt, 2.1)}">${blob({ c: LB, w: 260, mood: "worried" })}</div>` },
    { a: 3.2, b: 6.8, html: (lt) => {
      const rows = [["Talent Team", "Unfortunately, we have decided to move forward…"], ["Careers", "After careful consideration…"], ["Recruiting", "We regret to inform you…"], ["HR Ops", "Thank you for your interest…"]];
      return `<p class="h1 m" style="${up(lt, 0)}">Meanwhile, the inbox:</p>
        <div class="paper inbox">${rows.map((r, i) => `<div class="row" style="${up(lt, 0.2 + i * 0.35, 0.3, 20)}"><b>${r[0]}</b><span>${r[1]}</span></div>`).join("")}</div>
        <div class="chips" style="${up(lt, 2.0)}"><span>61 rejections</span><span>86 no replies</span></div>`; } },
    { a: 6.8, b: 9.6, html: (lt) => `
        <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px">
          <p class="h1" style="${up(lt, 0.05)}">Your inbox is <span class="mk">not a verdict</span> on your worth.</p>
          <p class="p" style="${up(lt, 0.9)}">Many rejection emails are sent automatically, to hundreds of people at once.</p>
        </div>` },
    { a: 9.6, b: 14.2, html: (lt) => `
        <p class="eyebrow" style="${up(lt, 0)}">3 things that help</p>
        ${[["Set job-search hours.", "Then stop for the day, guilt-free."], ["Track what you control.", "Applications sent, not replies received."], ["Talk about it.", "Rejection stings less when it's shared."]].map(([b, s], k) => `<div class="card ${k % 2 ? "l" : "y"}" style="${up(lt, 0.3 + k * 0.9)}"><span class="num">${k + 1}</span><span class="txt"><b style="font-size:46px">${b}</b><span style="font-size:36px">${s}</span></span></div>`).join("")}` },
    { a: 14.2, b: 17, html: (lt) => endCard(lt, "Career counselling and emotional support, in one place.") },
  ] };

  const REEL_MEN = { dur: 16.8, cover: 3.2, scenes: [
    { a: 0, b: 3.8, html: (lt) => {
      const n = Math.min(11, Math.floor(C((lt - 0.4) / 2.6) * 11 + (lt > 0.4 ? 1 : 0)));
      const marks = Array.from({ length: n }, (_, k) => { const g = Math.floor(k / 5), j = k % 5; return j === 4 ? `<path d="M${g * 230 + 6} 140 L${g * 230 + 196} 30" stroke="${P}" stroke-width="14" stroke-linecap="round"/>` : `<path d="M${g * 230 + 30 + j * 44} 20 L${g * 230 + 24 + j * 44} 150" stroke="${K}" stroke-width="14" stroke-linecap="round"/>`; }).join("");
      return `<p class="eyebrow">19 November · International Men's Day</p>
        <p class="h1">He said <span class="mk">“I'm fine”</span> 11 times this week.</p>
        <svg viewBox="0 0 700 170" width="900" height="220" style="overflow:visible">${marks}</svg>`; } },
    { a: 3.8, b: 7.4, html: (lt) => `
        ${[["“All good, bro.”", "y", 0], ["“Just tired.”", "l", 120], ["“It's nothing.”", "", 30], ["“Can't sleep. Otherwise fine.”", "y", 80], ["“I'll handle it.”", "l", 0]].map(([x, c, m], k) => `<div class="bub ${c}" style="${pop(lt, 0.1 + k * 0.5)};margin-left:${m}px">${x}</div>`).join("")}` },
    { a: 7.4, b: 9.8, html: (lt) => `
        <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px">
          <p class="h1" style="${up(lt, 0.05)}">Ask a 12th time.</p>
          <p class="h1" style="${up(lt, 0.8)}"><span class="mk">Then really listen.</span></p>
          <div style="${up(lt, 1.3)}">${blob({ c: SAGE, w: 260, mood: "calm" })}</div>
        </div>` },
    { a: 9.8, b: 13.8, html: (lt) => `
        <p class="eyebrow" style="${up(lt, 0)}">Not sure what to say? Try:</p>
        ${[["“You've seemed quiet lately. Want to talk?”", "y"], ["“No pressure. I'm here whenever you're ready.”", "l"], ["“How are you, really?”", ""]].map(([x, c], k) => `<div class="bub ${c}" style="${up(lt, 0.3 + k * 0.9)};font-size:46px">${x}</div>`).join("")}` },
    { a: 13.8, b: 16.8, html: (lt) => endCard(lt, "Men need someone to talk to, too.", HELP) },
  ] };

  // ---------- the ten posts, in posting order ----------
  const POSTS = [
    { id: "01", slug: "Reel-Diwali", kind: "reel", reel: REEL_DIWALI, segment: "Everyone celebrating Diwali", date: "Sun 8 Nov 2026", time: "11:00 AM IST",
      hook: "A Diwali cleaning checklist where every item is ticked except “Your mind”.",
      caption: "We clean every corner before Diwali. The worry, the tiredness and the “I'm fine” usually come along to the celebration anyway. 🪔\n\nTry the 2-minute mind clean-up before the guests arrive:\n1. Breathe out slowly, three times.\n2. Name one thing that feels heavy.\n3. Tell one person you trust.\n\nIf this festive season feels heavier than it looks, our experts are here 24/7, festival days included.\n\nHappy Diwali from all of us at YourDOST. ✨",
      tags: "#HappyDiwali #Diwali2026 #EmotionalWellness #MentalHealthMatters #SelfCare #YourDOST",
      first: "Drop a 🪔 if you're taking 2 minutes for yourself today.",
      audio: "A soft festive instrumental from Instagram's audio library (search “diwali instrumental” or “sitar lo-fi”), volume at about 30% so the on-screen text leads.",
      alt: ["Short video: a Diwali cleaning checklist with cupboards, fans and kitchen tiles ticked, but “Your mind” left unticked; then a 3-step 2-minute mind clean-up, a glowing diya, and the YourDOST logo with “Talk to a certified expert, 24/7”."] },
    { id: "02", slug: "Carousel-Exam-Stress", kind: "carousel", segment: "Students: boards, entrance exams, semester finals", date: "Tue 10 Nov 2026", time: "7:00 PM IST",
      hook: "Slide 1 names something every student has held, the marksheet, and promises what it leaves out.",
      slides: carousel([
        () => [`<p class="eyebrow">Student Life</p><p class="h1 xl">Your Marksheet Shows Your Percentage.</p><p class="h1 s">Here's What It <span class="mk">Doesn't</span> Show.</p><div style="display:flex;align-items:flex-end;gap:10px;margin-top:10px">${marksheet()}<div style="margin-left:-60px;margin-bottom:-20px">${blob({ c: Y, w: 170, mood: "worried" })}</div></div>`, { swipe: true }],
        stem("It doesn't show", "The nights you studied while everyone else was asleep.", `<div style="display:flex;gap:40px;align-items:center">${icon("moon")}${blob({ c: LB, w: 230, mood: "calm" })}</div>`),
        stem("It doesn't show", "The chapter that finally made sense, three days before the exam.", `<div style="display:flex;gap:40px;align-items:center">${icon("bulb", "y")}${blob({ c: Y, w: 230, mood: "smile" })}</div>`),
        stem("It doesn't show", "That you showed up, even on the days you wanted to quit.", `<div style="display:flex;gap:40px;align-items:center">${icon("steps")}${blob({ c: SAGE, w: 230, mood: "flat" })}</div>`),
        stem("It doesn't show", "How hard you've been on yourself.", `<div style="display:flex;gap:40px;align-items:center">${icon("heart", "y")}${blob({ c: PEACH, w: 230, mood: "sad" })}</div>`, "Self-criticism makes studying harder, not easier. Talk to yourself the way you'd talk to a friend."),
        () => [`<p class="eyebrow">Panicking before an exam? Try this</p><p class="h1 m">The 5-4-3-2-1 Reset</p>
          <ul class="numlist"><li><i>5</i>things you can see</li><li><i>4</i>things you can touch</li><li><i>3</i>things you can hear</li><li><i>2</i>things you can smell</li><li><i>1</i>thing you can taste</li></ul>
          <p class="p s">It brings your attention back to the room, and out of the spiral.</p>`, {}],
        () => [`<p class="h1 m">Your Marks Are One Chapter of Your Story.</p><p class="h1 s"><span class="mk">Not the whole book.</span></p>
          <p class="p">Talk to a YourDOST expert. Many colleges offer YourDOST to students, so check your college email.</p>${CTA}${HELP}`, { cls: "mid" }],
      ]),
      caption: "Results, rankings, “how much did you score?” Exam season can make it feel like you are your marks. You're not. 💛\n\nSwipe through, and save the 5-4-3-2-1 reset for the next time panic shows up before a paper.\n\nIf exam stress is getting heavy, talk to someone. Many colleges offer YourDOST to their students: check your college email.\n\nFeeling unsafe? Call Tele MANAS 14416 (free, 24/7).",
      tags: "#ExamStress #StudentLife #BoardExams #ExamSeason #StudentMentalHealth #YourDOST",
      first: "What's one thing your marksheet will never show about you? 👇",
      alt: ["Slide 1: “Your marksheet shows your percentage. Here's what it doesn't show.” with a marksheet showing 92.4% and a small worried yellow character.", "Slide 2: It doesn't show the nights you studied while everyone else was asleep.", "Slide 3: It doesn't show the chapter that finally made sense, three days before the exam.", "Slide 4: It doesn't show that you showed up, even on the days you wanted to quit.", "Slide 5: It doesn't show how hard you've been on yourself. Talk to yourself the way you'd talk to a friend.", "Slide 6: The 5-4-3-2-1 reset: 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.", "Slide 7: Your marks are one chapter of your story, not the whole book. Talk to a YourDOST expert; Tele MANAS 14416 for crisis support."] },
    { id: "03", slug: "Image-AI-Anxiety", kind: "single", segment: "Working professionals worried about AI and their jobs", date: "Wed 11 Nov 2026", time: "1:00 PM IST",
      hook: "A save-worthy framework: what's in your control vs. not, applied to AI anxiety.",
      slides: [() => slide(0, 1, `
        <p class="eyebrow">Work &amp; Careers</p>
        <p class="h1 m">Worried About AI and Your Job?</p>
        <p class="p" style="margin-top:-10px">Spend your energy on the <span class="mk">inner circle.</span></p>
        <div style="position:relative;width:860px;height:660px;align-self:center;margin-top:0">
          <svg viewBox="0 0 860 660" width="860" height="660" style="position:absolute;inset:0"><ellipse cx="430" cy="330" rx="428" ry="328" fill="${L}"/><ellipse cx="430" cy="330" rx="262" ry="206" fill="${Y}" stroke="#2b2b2b" stroke-width="4" stroke-dasharray="14 10"/></svg>
          <div style="position:absolute;left:0;right:0;top:26px;text-align:center"><b style="font-size:22px;letter-spacing:.06em;color:${P}">NOT IN YOUR CONTROL</b><p style="font-size:27px">How fast AI tools change</p></div>
          <div style="position:absolute;left:0;right:0;bottom:26px;text-align:center"><p style="font-size:27px">What others post on LinkedIn</p></div>
          <div style="position:absolute;left:22px;top:280px;width:150px;text-align:center;font-size:25px;line-height:1.3">Job-market headlines</div>
          <div style="position:absolute;right:22px;top:280px;width:150px;text-align:center;font-size:25px;line-height:1.3">Company restructuring</div>
          <div style="position:absolute;left:200px;right:200px;top:140px;text-align:center;display:flex;flex-direction:column;gap:5px">
            <b style="font-size:22px;letter-spacing:.06em">IN YOUR CONTROL</b>
            ${["Learning one new skill", "Asking for feedback", "Your sleep and breaks", "Who you reach out to", "How you talk to yourself", "Time spent doom-scrolling"].map((x) => `<span style="font-size:28px;font-weight:500">${x}</span>`).join("")}
          </div>
        </div>
        <div class="cta" style="font-size:26px;padding:16px 28px">Talk to a certified expert, 24/7 <b>yourdost.com</b></div>`, { cls: "" })],
      caption: "AI is changing work fast, and it's normal to feel uneasy about where you fit in. 🤖💭\n\nIn a July 2026 Blind survey, 66% of AI and ML professionals in India said they expect layoffs or big cuts within 3–6 months. If you've been lying awake over this, you're not alone.\n\nYou can't control how fast the tools change. You can control what you learn, how you rest, and who you talk to.\n\nSave this, and send it to a colleague who needs it. Our experts are here 24/7 if the worry gets heavy.",
      tags: "#AIAnxiety #FutureOfWork #WorkStress #CareerAnxiety #MentalHealthAtWork #YourDOST",
      first: "Which inner-circle habit are you starting this week? 👇",
      alt: ["Two-circle diagram titled “Worried about AI and your job?”. Outer lavender ring, not in your control: how fast AI tools change, job-market headlines, company restructuring, what others post on LinkedIn. Inner yellow circle, in your control: learning one new skill, asking for feedback, your sleep and breaks, who you reach out to, how you talk to yourself, time spent doom-scrolling."] },
    { id: "04", slug: "Carousel-Breakup", kind: "carousel", segment: "College students and young adults after a breakup", date: "Fri 13 Nov 2026", time: "9:30 PM IST",
      hook: "“The Hardest Part of a Breakup (That Nobody Warns You About)”, then one small, true moment per slide.",
      slides: carousel([
        () => [`<p class="eyebrow">Love &amp; Relationships</p><p class="h1 xl">The Hardest Part of a Breakup</p><p class="tag">(That Nobody Warns You About)</p><div style="display:flex;justify-content:center;margin-top:20px">${blob({ c: LB, w: 340, mood: "sad" })}</div>`, { swipe: true }],
        stem("It's not the goodbye.", "It's picking up your phone to tell them something funny, and then remembering.", chat("you won't believe what happened today 😂", false)),
        stem("It's not the photos.", "It's the song in the café you can't skip anymore.", `<div style="display:flex;gap:40px;align-items:center">${icon("music")}${blob({ c: PEACH, w: 230, mood: "flat" })}</div>`),
        stem("It's not the silence.", "It's checking whether they've seen your story.", `<div style="display:flex;gap:40px;align-items:center">${icon("eye", "y")}${blob({ c: Y, w: 230, mood: "worried" })}</div>`),
        stem("It's not losing them.", "It's missing who you were when you were with them.", `<div style="display:flex;gap:30px;align-items:center">${blob({ c: SAGE, w: 230, mood: "smile" })}<div style="opacity:.35">${blob({ c: SAGE, w: 200, mood: "smile" })}</div></div>`),
        () => [`<p class="h1 m">Healing After a Breakup Isn't a Straight Line.</p><p class="p">Some days you'll feel fine. Some days one song will undo you. <b>Both are part of moving on.</b></p><div style="margin-top:20px">${squiggle()}</div>`, {}],
        () => [`<div style="display:flex;justify-content:center">${blob({ c: Y, w: 260, mood: "calm", extra: "" })}</div><p class="h1 m">You Don't Have to Carry It Alone.</p><p class="p">Talk to a YourDOST expert about what you're going through, at your own pace.</p>${CTA}<p class="p s">Send this to the friend who needs it today.</p>`, { cls: "mid c" }],
      ]),
      caption: "Nobody warns you that the hardest part of a breakup isn't the goodbye. It's the small moments after. 💔\n\nThe song you can't skip. The story you check. The funny thing you can't tell them anymore.\n\nHealing isn't a straight line, and that's okay. If it feels too heavy to carry alone, our experts are here to listen, 24/7.\n\nSend this to a friend who's going through it.",
      tags: "#Breakup #Heartbreak #MovingOn #HealingJourney #RelationshipAdvice #YourDOST",
      first: "Which slide hit the hardest? You don't have to explain, just drop the number. 💛",
      alt: ["Slide 1: “The hardest part of a breakup (that nobody warns you about)” with a sad lavender character.", "Slide 2: It's not the goodbye. It's picking up your phone to tell them something funny, and then remembering. A chat with “Don't.” shows an unsent message.", "Slide 3: It's not the photos. It's the song in the café you can't skip anymore.", "Slide 4: It's not the silence. It's checking whether they've seen your story.", "Slide 5: It's not losing them. It's missing who you were when you were with them.", "Slide 6: Healing after a breakup isn't a straight line, shown as a looping line from “the breakup” to “okay again”.", "Slide 7: You don't have to carry it alone. Talk to a YourDOST expert."] },
    { id: "05", slug: "Carousel-Getting-Back-Together", kind: "carousel", segment: "Young couples who got back together", date: "Sun 15 Nov 2026", time: "8:00 PM IST",
      hook: "Everyone posts about breakups; almost nobody talks about what happens after a patch-up.",
      slides: carousel([
        () => [`<p class="eyebrow">Love &amp; Relationships</p><p class="h1 xl">You Got Back Together.</p><p class="h1 s">Here's What <span class="mk">Nobody</span> Tells You.</p><div style="display:flex;justify-content:center;margin-top:20px">${kintsugi(520)}</div>`, { swipe: true }],
        () => [`<p class="h1 m">Everyone Said “Finally!”</p><p class="p">And you still read their “ok” four times, wondering what it means.</p><div style="display:flex;flex-direction:column;gap:16px;margin-top:10px"><div class="bub y">finally!!! 🥹❤️</div><div class="bub l" style="margin-left:140px">knew it 😌</div><div class="bub" style="margin-left:40px">please don't fight again 😂</div></div>`, {}],
        () => [`<p class="h1 m">Missing Someone Isn't the Same as Trusting Them Again.</p><p class="p">Both feelings can be true at once. <b>They just heal at different speeds.</b></p><div style="display:flex;gap:40px;justify-content:center;margin-top:20px">${blob({ c: PEACH, w: 220, mood: "smile" })}${blob({ c: LB, w: 220, mood: "worried" })}</div>`, {}],
        () => [`<p class="eyebrow">Think of kintsugi</p><p class="h1 m">The Japanese Art of Repairing Broken Pottery With Gold</p><p class="p">The crack isn't hidden. It's repaired with care and becomes part of the story. <b>Rebuilding trust works the same way: you don't pretend it never broke.</b></p><div style="display:flex;justify-content:center">${kintsugi(420)}</div>`, {}],
        () => [`<p class="h1 m">3 Questions to Ask Each Other</p><ul class="numlist"><li><i>1</i>What's different this time?</li><li><i>2</i>What will we do when it gets hard?</li><li><i>3</i>What does each of us need to stop doing?</li></ul><p class="tag">(Not at 1 AM. Pick a calm moment.)</p>`, {}],
        () => [`<p class="h1 m">Sometimes the Bravest Step Is a Third Person in the Room.</p><p class="p">Seeing a relationship counsellor isn't a sign you're failing. <b>It's a sign you're serious.</b></p>${CTA}<p class="p s">Send this to your person. Or save it for yourself.</p>`, { cls: "mid" }],
      ]),
      caption: "Breakups get a thousand posts. Getting back together gets none. So here's one. 🤍\n\nIf you're back together and still feel anxious, that's normal. It doesn't mean it was a mistake. It means trust is still being rebuilt.\n\nSlide 5 is for both of you. And if you'd like help with those conversations, our relationship experts are here.",
      tags: "#Relationships #GettingBackTogether #Trust #CouplesTherapy #HealthyRelationships #YourDOST",
      first: "Have you been through a patch-up? What helped the most? 👇",
      alt: ["Slide 1: “You got back together. Here's what nobody tells you.” with a cup repaired with gold.", "Slide 2: Everyone said “finally!” and you still read their “ok” four times. Friends' comments: finally, knew it, please don't fight again.", "Slide 3: Missing someone isn't the same as trusting them again. They heal at different speeds.", "Slide 4: Kintsugi, the Japanese art of repairing broken pottery with gold. Rebuilding trust works the same way.", "Slide 5: 3 questions to ask each other: what's different this time, what will we do when it gets hard, what does each of us need to stop doing.", "Slide 6: Sometimes the bravest step is a third person in the room. Seeing a relationship counsellor is a sign you're serious."] },
    { id: "06", slug: "Reel-Job-Hunt", kind: "reel", reel: REEL_JOBS, segment: "Freshers in placement season and people looking for work", date: "Tue 17 Nov 2026", time: "8:00 PM IST",
      hook: "An application counter racing from #001 to #147 in two seconds.",
      caption: "147 applications. 61 rejections. 86 never replied. If your inbox has started to feel like a verdict on you, this one's for you. 📩\n\nMany rejection emails are sent automatically, to hundreds of people at once. Please don't give them days of your self-worth.\n\n3 things that help:\n1. Set job-search hours, then stop for the day.\n2. Track what you control: applications sent, not replies.\n3. Talk about it. Rejection stings less when it's shared.\n\nYourDOST offers career counselling and emotional support, 24/7.",
      tags: "#JobSearch #JobHunt #Placements #CareerAdvice #Rejection #YourDOST",
      first: "What's your application count right now? You're not the only one. 👇",
      audio: "A calm, steady lo-fi beat from the audio library, volume around 30%. Use the email “ping” sound in the first 3 seconds if available.",
      alt: ["Short video: an application counter goes from 1 to 147; an inbox fills with rejection emails; text says your inbox is not a verdict on your worth; three tips: set job-search hours, track what you control, talk about it; ends with the YourDOST logo and “Talk to a certified expert, 24/7”."] },
    { id: "07", slug: "Image-Founders", kind: "single", segment: "Startup founders, incubators and investors", date: "Wed 18 Nov 2026", time: "9:00 AM IST",
      hook: "A pitch-deck style “Founder Health” slide where the number nobody tracks is 0.",
      slides: [() => slide(0, 1, `
        <p class="eyebrow">Founder Wellbeing</p>
        <p class="h1 m">Investors Track Your Runway.</p>
        <p class="h1 m"><span class="mk">Who's Tracking How You're Doing?</span></p>
        <p class="eyebrow" style="margin-top:14px;color:#777">Slide 14 of 14 · Founder health</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">
          <div class="card y"><span class="txt"><span class="num">7 mo</span><span class="lbl">Runway</span></span>${icon("clock", "y")}</div>
          <div class="card l"><span class="txt"><span class="num">4 hrs</span><span class="lbl">Sleep a night</span></span>${icon("moon", "l")}</div>
          <div class="card w" style="grid-column:1 / span 2"><span class="txt"><span class="num" style="color:#c8452c">0</span><span class="lbl">People I can be completely honest with</span></span>${icon("person", "l")}</div>
        </div>
        <p class="p s" style="margin-top:6px">Building a company can be lonely. YourDOST has an emotional wellness program for founders: <b>yourdost.com/emotional-wellness-founders</b></p>`)],
      caption: "Founders are often the only people in the company who can't have a bad day out loud. 🚀\n\nThe team needs morale. Investors need conviction. Family wanted you to take the safe job. So the worry goes nowhere.\n\nIf the third number on your slide is 0, let's make it 1. YourDOST's emotional wellness program for founders: yourdost.com/emotional-wellness-founders\n\nIncubators and VCs: tag a founder who needs to see this.",
      tags: "#Founders #StartupLife #FounderMentalHealth #Entrepreneurship #StartupIndia #YourDOST",
      first: "Founders: what's the number nobody asks you about? 👇",
      alt: ["A pitch-deck style slide: “Investors track your runway. Who's tracking how you're doing?” Runway 7 months, sleep 4 hours a night, people I can be completely honest with: 0. YourDOST's emotional wellness program for founders."] },
    { id: "08", slug: "Reel-Mens-Day", kind: "reel", reel: REEL_MEN, segment: "Men, and the people who love them", date: "Thu 19 Nov 2026", time: "9:00 AM IST",
      hook: "Tally marks counting up to 11 “I'm fine”s in one week.",
      caption: "International Men's Day, 19 November. 💙\n\nMany men grow up learning to fix things, pay the bills and keep their feelings to themselves. So “I'm fine” becomes the answer to everything.\n\nToday, check in on him. Ask again, and wait for the real answer. Not sure what to say? Try: “You've seemed quiet lately. Want to talk?”\n\nIf he isn't ready to talk to you, our experts are here 24/7. In crisis? Call Tele MANAS 14416 (free, 24/7).",
      tags: "#InternationalMensDay #MensMentalHealth #ItsOkayToTalk #CheckOnYourFriends #MentalHealthMatters #YourDOST",
      first: "Tag a man you're checking in on today. 💙",
      audio: "A gentle piano or acoustic guitar track from the audio library, volume around 30%.",
      alt: ["Short video: tally marks count to 11 as the text says he said “I'm fine” 11 times this week; speech bubbles show variations like “All good, bro” and “Just tired”; text says ask a 12th time, then really listen; three things to say; ends with the YourDOST logo and Tele MANAS 14416."] },
    { id: "09", slug: "Carousel-Ask-Your-Counsellor", kind: "carousel", segment: "Employees at companies that offer YourDOST", date: "Mon 23 Nov 2026", time: "1:00 PM IST",
      hook: "“Your company offers counselling. Here's everything you were too awkward to ask.”",
      slides: carousel([
        () => [`<p class="eyebrow">Work &amp; Careers</p><p class="h1 xl">Your Company Offers Counselling.</p><p class="h1 s">Here's Everything You Were <span class="mk">Too Awkward to Ask.</span></p><div style="display:flex;justify-content:center;margin-top:10px">${blob({ c: Y, w: 300, mood: "worried" })}</div>`, { swipe: true }],
        () => [`<div class="q" style="display:flex;gap:24px;align-items:center">${icon("lock")}<p class="h1 m">“Will My Manager Find Out?”</p></div><p class="p">Counselling is <b>confidential</b>. You can ask your counsellor exactly how confidentiality works, including the rare situations where safety has to come first.</p>`, { cls: "mid" }],
        () => [`<div style="display:flex;gap:24px;align-items:center">${icon("chat", "y")}<p class="h1 m">“Do I Need a Big Problem to Talk?”</p></div><p class="p"><b>No.</b> Work stress, poor sleep, a tough manager, a breakup, feeling flat for weeks: all of it counts.</p>`, { cls: "mid" }],
        () => [`<div style="display:flex;gap:24px;align-items:center">${icon("globe")}<p class="h1 m">“Can I Talk in My Own Language?”</p></div><p class="p"><b>Yes.</b> YourDOST experts support <b>20+ Indian languages.</b></p>`, { cls: "mid" }],
        () => [`<div style="display:flex;gap:24px;align-items:center">${icon("video", "y")}<p class="h1 m">“What If I Don't Want a Video Call?”</p></div><p class="p">Start however you're comfortable: chat, audio, video or in person.</p>
          <div class="card y"><span class="txt"><span class="num">57.88%</span><span class="lbl">of YourDOST counselling sessions after the pandemic were chat-based</span></span>${icon("chat", "y")}</div>
          <p class="source">Source: YourDOST | Decade of Wellness Report</p>`, { cls: "mid" }],
        () => [`<div style="display:flex;gap:24px;align-items:center">${icon("clock")}<p class="h1 m">“When Can I Reach Someone?”</p></div><p class="p"><b>Anytime.</b> Experts are available 24/7, so a bad day doesn't have to become a bad week.</p>`, { cls: "mid" }],
        () => [`<p class="h1 m">Check If You Already Have Access.</p><p class="p">Ask HR, or look for YourDOST on your company's benefits portal. <b>Then start with a simple chat.</b></p>${CTA}`, { cls: "mid" }],
      ]),
      caption: "Your company offers counselling. You've thought about it. You haven't used it. 👀\n\nMost people hold back for the same reasons: “Will my manager know?” “Is my problem big enough?” “Do I have to be on video?”\n\nSwipe for the honest answers. Then check with HR or your benefits portal to see if you already have YourDOST.",
      tags: "#EmployeeWellbeing #WorkplaceWellness #EAP #MentalHealthAtWork #WorkLifeBalance #YourDOST",
      first: "What stopped you from booking a session so far? (No judgement, genuinely asking.) 👇",
      alt: ["Slide 1: “Your company offers counselling. Here's everything you were too awkward to ask.”", "Slide 2: Will my manager find out? Counselling is confidential; ask your counsellor how confidentiality works.", "Slide 3: Do I need a big problem to talk? No. Work stress, poor sleep, a tough manager, a breakup all count.", "Slide 4: Can I talk in my own language? Yes, YourDOST experts support 20+ Indian languages.", "Slide 5: What if I don't want a video call? Chat, audio, video or in person. 57.88% of YourDOST sessions after the pandemic were chat-based. Source: YourDOST Decade of Wellness Report.", "Slide 6: When can I reach someone? Anytime, experts are available 24/7.", "Slide 7: Check if you already have access. Ask HR or look on your benefits portal."] },
    { id: "10", slug: "Carousel-HR-and-Campus-Leaders", kind: "carousel", segment: "HR leaders, managers, deans and professors", date: "Tue 24 Nov 2026", time: "10:00 AM IST",
      hook: "An exit form with “Better opportunity” ticked, and the truth underneath.",
      slides: carousel([
        () => [`<p class="eyebrow">For HR Leaders &amp; Campus Heads</p><p class="h1 m">Her Exit Form Said “Better Opportunity.”</p><p class="h1 s"><span class="mk">The Real Reason Rarely Makes It Onto the Form.</span></p><div style="margin-top:14px">${exitForm()}</div>`, { swipe: true }],
        () => [`<p class="h1 m">Burnout Shows Up Long Before the Resignation</p><p class="p">Watch for the small signals:</p><div class="chips"><span>Cameras always off</span><span>“Sounds good 👍”</span><span>Monday sick leave</span><span>Lunch at the desk</span><span>11 PM “just checking”</span></div><p class="p s">Noticing early is kinder, and cheaper, than replacing people.</p>`, { cls: "mid" }],
        () => [`<p class="eyebrow">The cost of looking away</p><p class="h1" style="font-weight:700;font-size:120px">₹1.1 Lakh Crore</p><p class="p">What poor employee mental health costs Indian employers every year, through absenteeism, presenteeism and attrition. <b>Presenteeism, people at work but not okay, is the biggest share.</b></p><p class="source">Source: Deloitte, Mental Health and Well-being in the Workplace (2022)</p>`, { cls: "mid" }],
        () => [`<p class="h1 m">Support Has to Fit How People Reach Out</p><p class="eyebrow">Post-pandemic counselling sessions</p>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px"><div class="card y"><span class="txt"><span class="num">57.88%</span><span class="lbl">Chat-based</span></span>${icon("chat", "y")}</div><div class="card l"><span class="txt"><span class="num">18.49%</span><span class="lbl">Audio</span></span>${icon("phone")}</div><div class="card l"><span class="txt"><span class="num">17.8%</span><span class="lbl">Video</span></span>${icon("video")}</div><div class="card y"><span class="txt"><span class="num">5.84%</span><span class="lbl">In-person</span></span>${icon("person", "y")}</div></div>
          <p class="p s">Many people start by typing, not talking.</p><p class="source">Source: YourDOST | Decade of Wellness Report</p>`, { cls: "mid" }],
        () => [`<p class="h1 m">What Makes People Actually Use Support</p>
          ${[["shield", "Private", "No manager in the loop."], ["bolt", "Instant", "Certified experts, 24/7."], ["globe", "In their language", "20+ Indian languages."]].map(([ic, b, s], k) => `<div style="display:flex;gap:26px;align-items:center">${icon(ic, k % 2 ? "l" : "y")}<span class="txt" style="display:flex;flex-direction:column"><b style="font-size:40px;font-weight:600">${b}</b><span style="font-size:32px;color:#333">${s}</span></span></div>`).join("")}`, { cls: "mid" }],
        () => [`<p class="h1 m">Is Your Workplace or Campus Ready?</p><p class="p">Let's talk about making mental health support easy to reach for your people.</p><p class="p"><b>Let's start a conversation.</b><br>Visit <b>www.yourdost.com</b> or mail us at <b>contact@yourdost.com</b></p><img src="brand/badge.png" style="width:190px" alt="">`, { cls: "mid" }],
      ]),
      caption: "Exit interviews rarely tell the whole story. Burnout shows up much earlier: cameras off, “sounds good 👍”, the Monday sick leave. 📋\n\nPoor employee mental health costs Indian employers about ₹1.1 lakh crore a year (Deloitte, 2022). And when people do reach out, most start by typing: 57.88% of YourDOST sessions after the pandemic were chat-based.\n\nYourDOST works with workplaces and campuses to make support private, instant and available in 20+ Indian languages. Let's start a conversation: www.yourdost.com or contact@yourdost.com",
      tags: "#HRLeaders #EmployeeWellbeing #WorkplaceMentalHealth #CampusWellbeing #PeopleFirst #YourDOST",
      first: "HR leaders and faculty: what's one early sign of burnout you've learned to watch for? 👇",
      alt: ["Slide 1: Her exit form said “better opportunity”; the real reason rarely makes it onto the form. An exit interview form with “Better opportunity” ticked.", "Slide 2: Burnout shows up long before the resignation: cameras always off, “sounds good”, Monday sick leave, lunch at the desk, 11 PM “just checking”.", "Slide 3: ₹1.1 lakh crore a year, what poor employee mental health costs Indian employers. Source: Deloitte 2022.", "Slide 4: Post-pandemic counselling sessions: 57.88% chat, 18.49% audio, 17.8% video, 5.84% in person. Source: YourDOST Decade of Wellness Report.", "Slide 5: What makes people use support: private, instant, in their language.", "Slide 6: Is your workplace or campus ready? Visit www.yourdost.com or mail contact@yourdost.com."] },
  ];

  function frame(post, i = 0, t = null) {
    if (post.kind === "reel") return `<div class="yds tall">${reelFrame(post.reel, t === null ? post.reel.cover : t)}</div>`;
    return `<div class="yds">${post.slides[i]()}</div>`;
  }
  root.YD3 = { POSTS, frame };
})(typeof window !== "undefined" ? window : globalThis);
