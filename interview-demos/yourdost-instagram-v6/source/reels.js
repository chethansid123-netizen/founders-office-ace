/* YourDOST v6 reels: overlay timelines. Each frame is a pure function of t (seconds); render.mjs screenshots
   every frame with a transparent background and lays it over the ElevenLabs footage. */
(function (root) {
  "use strict";
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
  const back = (x) => { x = clamp(x); const c = 1.5; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  // opacity of something shown from a to b, with fade in/out lengths (fi = 0 shows it on the very first frame)
  const win = (t, a, b, fi = 0.25, fo = 0.3) => (t < a || t > b ? 0 : Math.min(fi ? clamp((t - a) / fi) : 1, fo ? clamp((b - t) / fo) : 1));
  const rise = (t, a, px = 26, d = 0.45) => (1 - ease((t - a) / d)) * px;
  const badge = (o = 1) => `<img class="mini-badge" style="opacity:${o}" src="brand/badge.png">`;
  const heart = `<svg width="50" height="50" viewBox="0 0 50 50"><path d="M25 43 C10 32 4 24 6 15 C8 7 18 5 25 13 C32 5 42 7 44 15 C46 24 40 32 25 43 Z" fill="#fff"/><path d="M9 25 H18 L21 19 L26 31 L29 25 H41" fill="none" stroke="#dd4224" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

  // the shared YourDOST end card: chat with an expert, then the call to action
  function endCard(t, t0, o) {
    if (t < t0) return "";
    const k = t - t0, a = ease(k / 0.35);
    const typing = k > 0.3 && k < 0.85;
    const dot = (i) => 0.35 + 0.65 * Math.abs(Math.sin((k * 7) - i * 0.9));
    const pop = (s) => `opacity:${clamp((k - s) / 0.12)};transform:scale(${0.85 + 0.15 * back((k - s) / 0.3)});transform-origin:${s === o.meAt ? "right" : "left"} bottom`;
    return `<div class="end" style="opacity:${clamp(k / 0.3)}">
      <img class="logo" src="brand/badge.png" style="transform:translateY(${(1 - a) * -30}px)">
      <div class="chat" style="transform:translateY(${(1 - a) * 70}px)">
        <div class="hd"><img src="brand/badge.png"><div><b>YourDOST Expert</b><span>Online now · 24/7</span></div></div>
        <div class="body">
          ${typing ? `<div class="bx"><span class="dots"><i style="opacity:${dot(0)}"></i><i style="opacity:${dot(1)}"></i><i style="opacity:${dot(2)}"></i></span></div>` : ""}
          ${k >= 0.85 ? `<div class="bx" style="${pop(0.85)}">${o.expert}</div>` : ""}
          ${k >= o.meAt ? `<div class="bme" style="${pop(o.meAt)}">${o.me}</div>` : ""}
        </div>
      </div>
      <p class="head" style="opacity:${clamp((k - 0.25) / 0.35)};transform:translateY(${rise(t, t0 + 0.25, 20)}px)">${o.head}</p>
      <div class="cta" style="opacity:${clamp((k - 0.45) / 0.35)}"><span>Talk to a certified expert, 24/7 · <b>yourdost.com</b></span></div>
      <p class="note" style="opacity:${clamp((k - 0.65) / 0.35)}">${o.note}</p>
    </div>`;
  }

  const REELS = {
    "13": {
      slug: "13-Reel-Im-Fine-Ma", dur: 17.0, end: 13.8,
      render(t) {
        let h = "";
        const hook = win(t, 0, 3.0, 0, 0.3);
        const pay = win(t, 8.55, 13.75, 0.35, 0.3);
        h += `<div class="scrim-top" style="opacity:${Math.max(hook, pay)}"></div>`;
        h += `<div class="txt" style="top:300px;opacity:${hook}"><span class="eyebrow">Top B-school · Placement week</span><p class="line">Watch her face<br>when she picks up.</p></div>`;
        const subs = [[3.0, 3.8, "“Hi Ma!”"], [4.05, 5.3, "“Yes, I ate.”"], [5.65, 7.4, "“Everything's fine, really.”"]];
        for (const [a, b, s] of subs) { const o = win(t, a, b, 0.12, 0.15); if (o) h += `<div class="sub" style="top:1380px;opacity:${o}"><span>${s}</span></div>`; }
        if (pay) h += `<div class="txt" style="top:330px;opacity:${pay}"><p class="line">You don't have<br>to be fine</p><p class="line hl" style="opacity:${clamp((t - 10.7) / 0.3)};transform:translateY(${rise(t, 10.7, 18)}px)">for everyone.</p></div>`;
        if (t < 13.8) h += badge();
        h += endCard(t, 13.8, { expert: "Hey, I'm here. What's been feeling heavy lately?", me: "honestly? i miss home.", meAt: 1.6,
          head: "Talk to someone<br>who gets it.", note: "Your college may already give you access." });
        return h;
      },
    },
    "14": {
      slug: "14-Reel-Low-Battery", dur: 17.0, end: 13.4,
      render(t) {
        let h = "";
        // 0-1.95 s: phone lock screen with a low-battery alert, swiped up to reveal him
        if (t < 1.95) {
          const up = ease((t - 1.45) / 0.5) * 1920, m = back(t / 0.3);
          h += `<div class="lock" style="transform:translateY(${-up}px)"><div class="wall" style="background-image:url(ai/r14-frameA.jpg)"></div>
            <div class="status"><span></span><span class="batt">5%<i></i></span></div>
            <p class="date">Tuesday, 24 November</p><p class="time">11:48</p>
            <div class="alert" style="transform:scale(${0.93 + 0.07 * m})"><h4>Low Battery</h4><p>5% battery remaining</p><div class="btns"><span>Close</span><span>Low Power Mode</span></div></div>
            <div class="homebar"></div></div>`;
          return h;
        }
        const l1 = win(t, 1.95, 5.1, 0.3, 0.3);
        const l3 = win(t, 9.7, 13.35, 0.3, 0.3);
        h += `<div class="scrim-top" style="opacity:${Math.max(l1, l3, win(t, 5.2, 9.35, 0.3, 0.2) * 0.8)}"></div>`;
        if (l1) h += `<div class="txt" style="top:320px;opacity:${l1};transform:translateY(${rise(t, 1.95)}px)"><p class="line">Your phone warns you<br>at <span class="hl">20%</span>.</p></div>`;
        // the body's own notifications drop in, then get swiped away
        const N = [[5.3, "Headache. Day 4 this week."], [6.05, "You snapped at someone you love."], [6.8, "Sunday-night dread is back."]];
        const away = ease((t - 9.0) / 0.35) * 1200;
        N.forEach(([a, msg], i) => {
          if (t < a || t > 9.4) return;
          const y = 280 + i * 178, d = (1 - back((t - a) / 0.45)) * -160;
          h += `<div class="notif" style="top:${y + d}px;opacity:${clamp((t - a) / 0.15)};transform:translateX(${-away}px)"><div class="ic">${heart}</div><div class="bd"><div class="top"><span>Your body</span><em>now</em></div><p class="msg">${msg}</p></div></div>`;
        });
        const l2 = win(t, 7.6, 9.3, 0.3, 0.25);
        if (l2) h += `<div class="scrim-bot" style="opacity:${l2}"></div><div class="txt" style="top:1380px;opacity:${l2}"><p class="line">Your body warns you <span class="hl">too.</span></p></div>`;
        if (l3) h += `<div class="txt" style="top:330px;opacity:${l3};transform:translateY(${rise(t, 9.7)}px)"><p class="line">Don't swipe<br><span class="hl">this one</span> away.</p></div>`;
        if (t < 13.4) h += badge();
        h += endCard(t, 13.4, { expert: "Long week? Let's talk it through. No judgement.", me: "i think i'm running on 5%", meAt: 1.6,
          head: "Recharge with someone<br>who gets it.", note: "Ask HR if your company offers YourDOST." });
        return h;
      },
    },
    "15": {
      slug: "15-Reel-Ask-How-She-Is", dur: 17.0, end: 13.8,
      render(t) {
        let h = "";
        const c = win(t, 0, 3.35, 0, 0.3), l1 = win(t, 3.7, 7.85, 0.35, 0.3), chat = win(t, 8.3, 11.0, 0.3, 0.3), pay = win(t, 11.05, 13.75, 0.3, 0.3);
        h += `<div class="scrim-top" style="opacity:${Math.max(c, l1, pay, chat * 0.6)}"></div>`;
        if (c) h += `<div class="txt" style="top:300px;opacity:${c}"><p class="clock">3:07<span style="font-size:90px;letter-spacing:0"> AM</span></p><p class="line s">Third wake-up tonight.</p></div>`;
        if (l1) h += `<div class="txt" style="top:320px;opacity:${l1};transform:translateY(${rise(t, 3.7)}px)"><p class="line">Everyone asks<br>about the baby.</p></div>`;
        if (chat) {
          const M = [[8.45, "Mom", "#c2410c", "How is the baby sleeping?"], [9.15, "Rina Aunty", "#7c3aed", "Send more photos!!"], [9.85, "Sameer", "#0f766e", "Is he feeding well?"]];
          h += `<div class="fam" style="top:${280 + rise(t, 8.3, 40)}px;opacity:${chat}"><div class="hd"><div class="av"></div><div><b>Family</b><span>14 members</span></div></div><div class="msgs">`;
          for (const [a, who, col, msg] of M) if (t >= a) h += `<div class="m" style="opacity:${clamp((t - a) / 0.12)};transform:scale(${0.85 + 0.15 * back((t - a) / 0.3)});transform-origin:left bottom"><i style="color:${col}">${who}</i><span>${msg}</span></div>`;
          h += `</div></div>`;
        }
        if (pay) h += `<div class="txt" style="top:330px;opacity:${pay};transform:translateY(${rise(t, 11.05)}px)"><p class="line xl">Ask how<br><span class="hl">she</span> is.</p></div>`;
        if (t < 13.8) h += badge();
        h += endCard(t, 13.8, { expert: "Before we talk about the baby… how are <b>you</b> doing?", me: "honestly? i haven't slept properly in weeks.", meAt: 1.6,
          head: "New parents need<br>care too.", note: "Private. Online. Whenever you're up." });
        return h;
      },
    },
  };

  root.YD6R = { REELS, render(id, t) { document.getElementById("root").innerHTML = REELS[id].render(t); } };
})(typeof window !== "undefined" ? window : globalThis);
