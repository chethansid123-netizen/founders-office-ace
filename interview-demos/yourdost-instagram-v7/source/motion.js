/* YourDOST v7 motion versions of the three originals. Each frame is a pure function of t (seconds).
   M24 overlay is transparent over composited Veo tiles; M25 is fully rendered here (gallery photo with a slow camera);
   M26 overlay is transparent over the Veo base-camp clip. */
(function (root) {
  "use strict";
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
  const inout = (x) => { x = clamp(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  const win = (t, a, b, fi = 0.25, fo = 0.3) => (t < a || t > b ? 0 : Math.min(fi ? clamp((t - a) / fi) : 1, fo ? clamp((b - t) / fo) : 1));
  const type = (s, t, a, d) => { if (t < a) return ""; const n = Math.round(clamp((t - a) / d) * s.length); return s.slice(0, n); };
  const badge = (o = 1) => `<img class="mbadge" style="opacity:${o}" src="brand/badge.png">`;
  const lerp = (a, b, k) => a + (b - a) * k;
  const seg = (t, keys) => { // piecewise-eased keyframes [[t, v], ...]
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 0; i < keys.length - 1; i++) { const [t0, v0] = keys[i], [t1, v1] = keys[i + 1]; if (t <= t1) return lerp(v0, v1, inout((t - t0) / (t1 - t0))); }
    return keys[keys.length - 1][1];
  };

  /* ---------------- M24: stand-up with inner captions ---------------- */
  const L24 = { top: 300, bar: 66, left: 44, colW: 490, gap: 12, tileH: 276, capH: 116, rowGap: 12 };
  const cell = (i) => { const c = i % 2, r = Math.floor(i / 2); return { x: L24.left + c * (L24.colW + L24.gap), y: L24.top + L24.bar + r * (L24.tileH + L24.capH + L24.rowGap) }; };
  const P24 = [ // name, video, said, saidAt, saidDur, inner, innerAt, innerDur
    ["Arjun (host)", "m24-arjun", "Okay team, quick round before we start. How's everyone doing?", 0.2, 3.6, "I haven't slept properly since the re-org.", 13.45, 2.3],
    ["Neha", "m24-neha", "Super good!", 3.95, 0.85, "I cried in the washroom at 9:12.", 14.05, 2.8],
    ["Rahul", "m24-rahul", "All good, I can take more!", 4.95, 1.75, "I can't say no. I'm drowning.", 14.65, 2.4],
    ["Fatima", "m24-fatima", "Doing well, thanks.", 6.85, 1.0, "Is my name on the layoff list?", 15.25, 1.5],
    ["Vikram", null, "Yeah... all fine.", 8.0, 2.2, "Logged in from Papa's hospital room.", 15.85, 2.8],
    ["Sneha", "m24-sneha", "Never better, haha!", 10.25, 2.75, "Sunday dread starts on Saturday now.", 16.45, 3.3],
  ];
  const mic = `<svg width="18" height="18" viewBox="0 0 24 24"><rect x="9" y="3" width="6" height="11" rx="3" fill="#fff"/><path d="M6 11a6 6 0 0 0 12 0M12 17v4" stroke="#fff" stroke-width="2" fill="none"/></svg>`;
  const TOG = 13.2, DIM = 19.2, END24 = 22.3;
  function m24(t) {
    let h = "";
    if (t < END24) {
      const head = win(t, 0, DIM, 0, 0.4);
      h += `<div class="abs" style="left:56px;right:180px;top:96px;opacity:${head}"><span class="eyebrow">Monday stand-up · 9:30 AM</span><p class="hd1" style="margin-top:16px;font-size:48px">We switched on inner captions in today's stand-up.</p></div>`;
      const on = clamp((t - TOG) / 0.25);
      h += `<div class="bar24"><span><span class="rec"></span><b>Daily stand-up</b> · 6 people</span><span class="tog" style="background:${on ? "rgba(246,210,90,0.16)" : "rgba(255,255,255,0.08)"};border:1.5px solid ${on ? "#f6d25a" : "rgba(255,255,255,0.3)"};color:${on ? "#f6d25a" : "rgba(255,255,255,0.75)"}"><i style="background:${on ? "#f6d25a" : "#55555f"};--k:${3 + on * 20}px"></i>Inner captions${on ? " · on" : ""}</span></div>`;
      P24.forEach(([name, vid, said, sa, sd, inner, ia, id], i) => {
        const { x, y } = cell(i);
        const speaking = t >= sa && t <= sa + sd + 0.15;
        if (vid) h += `<div class="hole${speaking ? " spk" : ""}" style="left:${x}px;top:${y}px;width:${L24.colW}px;height:${L24.tileH}px"></div>`;
        else h += `<div class="off24" style="left:${x}px;top:${y}px;width:${L24.colW}px;height:${L24.tileH}px;${speaking ? "box-shadow:inset 0 0 0 5px #f6d25a" : ""}"><span>VK</span></div>`;
        h += `<span class="nm24" style="left:${x + 12}px;top:${y + 12}px">${mic}${name}</span>`;
        const s = type(said, t, sa, sd), n = type(inner, t, ia, id * 0.8);
        h += `<div class="cc24" style="left:${x}px;top:${y + L24.tileH}px;width:${L24.colW}px;height:${L24.capH}px">${s ? `<p class="said">“${s}${s.length === said.length ? "”" : ""}</p>` : ""}${n ? `<p class="inner">${n}</p>` : ""}</div>`;
      });
      const d = win(t, DIM, END24 + 0.3, 0.5, 0.01);
      if (d) h += `<div class="abs" style="inset:0;background:rgba(10,10,16,${0.8 * d})"></div>
        <div class="abs" style="left:80px;right:80px;top:760px;text-align:center;opacity:${clamp((t - 19.4) / 0.4)}"><p style="color:#fff;font-weight:600;font-size:76px;line-height:1.1">Everyone said “good.”</p>
        <p class="y" style="font-weight:600;font-size:96px;margin-top:22px;opacity:${clamp((t - 20.95) / 0.35)}">Nobody was.</p></div>`;
      h += badge();
    }
    if (t >= END24 - 0.3) {
      const k = t - END24 + 0.3, a = ease(k / 0.5);
      h += `<div class="endc" style="opacity:${clamp(k / 0.35)}"><img class="logo" src="brand/badge.png" style="transform:translateY(${(1 - a) * -24}px)">
        <p class="t" style="transform:translateY(${(1 - a) * 30}px)">Give your team somewhere to say it.</p>
        <div class="chips" style="top:800px;opacity:${clamp((k - 0.6) / 0.4)}"><span>A confidential expert for every employee</span><span>Chat, call or video · 24/7</span></div>
        <div class="ctaL" style="top:1060px;opacity:${clamp((k - 2.3) / 0.4)}"><span>YourDOST for teams · <b>contact@yourdost.com</b></span></div>
        <p class="notec" style="top:1190px;opacity:${clamp((k - 2.8) / 0.4)}">does your stand-up have a check-in?</p></div>`;
    }
    return h;
  }

  /* ---------------- M25: the gallery audio guide ---------------- */
  const IMG25 = { w: 1536, h: 2720, base: 1920 / 2720 };
  const CAP25 = [[1.3, 3.6, "Exhibit one. “I'm Fine.”"], [4.2, 6.6, "Artist… almost everyone."], [7.05, 8.6, "Notice the yellow."], [8.8, 12.6, "One thin, bright layer, painted fresh every morning…"], [12.95, 14.3, "…over a storm."], [14.75, 17.9, "Most visitors walk past it in under three seconds."], [18.3, 19.95, "If this painting is yours…"], [20.2, 22.2, "…you don't have to keep it on the wall."]];
  const END25 = 22.4, DUR25 = 25.5;
  const head = `<svg width="44" height="44" viewBox="0 0 24 24"><path d="M12 3a8 8 0 0 0-8 8v6a3 3 0 0 0 3 3h2v-8H6v-1a6 6 0 0 1 12 0v1h-3v8h2a3 3 0 0 0 3-3v-6a8 8 0 0 0-8-8z" fill="#f6d25a"/></svg>`;
  function m25(t) {
    let h = "";
    if (t < END25 + 0.4) {
      const z = seg(t, [[0, 1.0], [4, 1.07], [8.4, 1.75], [13.5, 2.55], [17.8, 2.4], [22.4, 1.3]]);
      const fx = seg(t, [[0, 768], [4, 760], [8.4, 590], [13.5, 600], [22.4, 640]]);
      const fy = seg(t, [[0, 1360], [4, 1340], [8.4, 1290], [13.5, 1370], [22.4, 1330]]);
      const S = IMG25.base * z, W = IMG25.w * S, H = IMG25.h * S;
      let x = 540 - fx * S, y = 960 - fy * S;
      x = Math.min(0, Math.max(1080 - W, x)); y = Math.min(0, Math.max(1920 - H, y));
      const lab = win(t, 1.2, 9.5, 0.6, 0.6);
      h += `<div class="abs" style="left:0;top:0;width:${IMG25.w}px;height:${IMG25.h}px;transform-origin:0 0;transform:translate(${x.toFixed(2)}px,${y.toFixed(2)}px) scale(${S.toFixed(5)})">
        <img src="ai/o25-gallery.jpg" style="width:${IMG25.w}px;height:${IMG25.h}px;display:block">
        <div class="label25" style="left:985px;top:960px;width:470px;opacity:${lab}"><p class="no">Gallery 1 · Exhibit 1</p><p class="art">Almost everyone</p><p class="ti"><i>I'm Fine</i>, 2026</p><p class="md">A smile, worn daily, over a storm. Oil on everything.</p></div></div>`;
      h += `<div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(0,0,0,0.25) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 62%,rgba(0,0,0,0.35) 100%)"></div>`;
      const p = clamp((t - 1.3) / (22.2 - 1.3)), sec = (s) => `0:${String(Math.floor(s)).padStart(2, "0")}`;
      h += `<div class="player" style="opacity:${win(t, 0, END25 + 0.4, 0.01, 0.4)}"><div class="ic">${head}</div><div class="meta"><small>Audio guide · Exhibit 1</small><b><i>I'm Fine</i>, 2026</b>
        <div class="prog"><i style="width:${(p * 100).toFixed(2)}%"></i></div><div class="tm"><span>${sec(p * 21)}</span><span>0:21</span></div></div></div>`;
      for (const [a, b, s] of CAP25) { const o = win(t, a, b, 0.2, 0.2); if (o) h += `<div class="sub25" style="opacity:${o}"><span>${s}</span></div>`; }
      h += badge();
    }
    if (t >= END25) {
      const k = t - END25, a = ease(k / 0.5);
      h += `<div class="endc" style="opacity:${clamp(k / 0.4)}"><img class="logo" src="brand/badge.png" style="transform:translateY(${(1 - a) * -24}px)">
        <p class="t" style="transform:translateY(${(1 - a) * 30}px)">If it's yours, you don't have to keep it on the wall.</p>
        <div class="ctaL" style="top:900px;opacity:${clamp((k - 0.5) / 0.4)}"><span>Talk to a certified expert, 24/7 · <b>yourdost.com</b></span></div>
        <p class="notec" style="top:1030px;opacity:${clamp((k - 0.9) / 0.4)}">what would your painting be called?</p></div>`;
    }
    return h;
  }

  /* ---------------- M26: Everest rest days ---------------- */
  const X = (d) => 40 + (d / 42) * 880, Yv = (a) => 200 - ((a - 5000) / 4000) * 180;
  const PLAN = [[0, 5364], [3, 5364], [5, 6065], [6, 5364], [9, 5364], [12, 6400], [14, 5364], [18, 5364], [21, 7162], [23, 5364], [32, 5364], [35, 6400], [37, 7162], [38, 7950], [39, 8849], [41, 5364]];
  const RESTS = [[0, 3], [6, 9], [14, 18], [23, 32]];
  const plen = (() => { let L = 0; for (let i = 1; i < PLAN.length; i++) { const dx = X(PLAN[i][0]) - X(PLAN[i - 1][0]), dy = Yv(PLAN[i][1]) - Yv(PLAN[i - 1][1]); L += Math.hypot(dx, dy); } return L; })();
  const END26 = 14.2;
  const KIN = [[1.0, 3.7, "Nobody climbs Everest <span class=\"y\">in one go.</span>"], [4.1, 7.9, "Climb high. Come back down. <span class=\"y\">Rest.</span>"], [8.3, 9.8, "Then do it <span class=\"y\">again.</span>"], [10.2, 14.0, "Rest isn't quitting.<br><span class=\"y\">It's how you reach the top.</span>"]];
  function m26(t) {
    let h = "";
    if (t < END26 + 0.4) {
      h += `<div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(4,10,30,0.55) 0%,rgba(4,10,30,0.15) 40%,rgba(4,10,30,0) 55%,rgba(4,10,30,0) 70%,rgba(4,10,30,0.6) 100%)"></div>`;
      h += `<div class="abs" style="left:56px;right:190px;top:140px;opacity:${win(t, 0, END26 + 0.4, 0.01, 0.4)}"><span class="eyebrow glass">Everest · 8,849 m</span><p class="hd1" style="color:#fff;margin-top:18px;font-size:68px;text-shadow:0 3px 24px rgba(0,0,0,0.5)">Even Everest climbers take rest days.</p></div>`;
      const c = win(t, 2.6, END26 + 0.4, 0.5, 0.4);
      if (c) {
        const draw = clamp((t - 4.0) / 5.4);
        const restGlow = clamp((t - 6.9) / 0.4) * (1 - clamp((t - 9.4) / 0.6) * 0.5);
        const coral = clamp((t - 9.3) / 0.7), crash = clamp((t - 10.0) / 0.4);
        const pts = PLAN.map(([d, a]) => `${X(d).toFixed(1)},${Yv(a).toFixed(1)}`).join(" ");
        const grid = [5000, 6000, 7000, 8000, 9000].map((a) => `<line x1="40" x2="920" y1="${Yv(a)}" y2="${Yv(a)}" stroke="rgba(255,255,255,0.13)" stroke-width="1.5"/><text x="0" y="${Yv(a) + 6}" font-size="17" fill="rgba(255,255,255,0.55)" font-family="Inter">${a / 1000}k</text>`).join("");
        const rests = RESTS.map(([a, b]) => `<rect x="${X(a)}" y="${Yv(5364) - 10}" width="${X(b) - X(a)}" height="20" rx="10" fill="rgba(246,210,90,${0.18 + 0.35 * restGlow})"/>`).join("");
        h += `<div class="chart26" style="opacity:${c}"><div class="hd"><b>How climbers actually reach the top</b><span>~6 weeks</span></div>
          <svg width="944" height="220" viewBox="0 0 944 220" style="margin-top:10px">${grid}${rests}
            <polyline points="${pts}" fill="none" stroke="#f6d25a" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="${plen.toFixed(0)}" stroke-dashoffset="${(plen * (1 - draw)).toFixed(1)}"/>
            ${draw >= 0.99 ? `<circle cx="${X(39)}" cy="${Yv(8849)}" r="9" fill="#f6d25a"/><text x="${X(39) - 128}" y="${Yv(8849) + 7}" font-size="20" font-weight="700" fill="#fff" font-family="Inter">Summit</text>` : ""}
            ${coral ? `<polyline points="${X(0)},${Yv(5364)} ${X(0 + 8 * coral)},${Yv(5364 + (8350 - 5364) * coral)}" fill="none" stroke="#ff7a5c" stroke-width="5" stroke-linecap="round"/>` : ""}
            ${crash ? `<polyline points="${X(8)},${Yv(8350)} ${X(8 + 1.2 * crash)},${Yv(8350 - 3350 * crash)}" fill="none" stroke="#ff7a5c" stroke-width="4" stroke-dasharray="8 8"/><text x="${X(8) + 14}" y="${Yv(8350) + 7}" font-size="20" font-weight="700" fill="#ff9b83" font-family="Inter" opacity="${crash}">burnout</text>` : ""}
          </svg>
          <div class="legend"><span><i style="background:#f6d25a"></i>Up, back down, rest. Repeat.</span><span style="opacity:${coral}"><i style="background:#ff7a5c"></i>No rest days</span></div></div>`;
      }
      for (const [a, b, s] of KIN) { const o = win(t, a, b, 0.3, 0.3); if (o) h += `<p class="kin" style="opacity:${o};transform:translateY(${(1 - ease((t - a) / 0.5)) * 24}px)">${s}</p>`; }
      h += badge();
    }
    if (t >= END26) {
      const k = t - END26, a = ease(k / 0.5);
      h += `<div class="endc" style="opacity:${clamp(k / 0.4)}"><img class="logo" src="brand/badge.png" style="transform:translateY(${(1 - a) * -24}px)">
        <p class="t" style="transform:translateY(${(1 - a) * 30}px)">Rest isn't quitting.<br><span style="color:#5b4a9c">It's how you reach the top.</span></p>
        <div class="ctaL" style="top:900px;opacity:${clamp((k - 0.5) / 0.4)}"><span>Talk to a certified expert, 24/7 · <b>yourdost.com</b></span></div>
        <p class="notec" style="top:1030px;opacity:${clamp((k - 0.9) / 0.4)}">when was your last real rest day?</p></div>`;
    }
    return h;
  }

  const MOTION = {
    "24": { dur: 27.2, render: m24, transparent: true, cells: P24.map((p, i) => ({ vid: p[1], ...cell(i), w: L24.colW, h: L24.tileH })) },
    "25": { dur: DUR25, render: m25, transparent: false },
    "26": { dur: 17.5, render: m26, transparent: true },
  };
  root.YD7M = { MOTION, render(id, t) { document.getElementById("root").innerHTML = MOTION[id].render(t); } };
})(typeof window !== "undefined" ? window : globalThis);
