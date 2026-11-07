/* #JoBolaNahi: ten Instagram posts for YourDOST.
   One file holds the copy, the strategy notes and the renderers, so the showcase page
   and the PNG/MP4 export draw exactly the same frames. */
(function (root) {
  "use strict";

  // ---------- animation helpers (deterministic: every frame is a pure function of t) ----------
  const C = (x) => Math.max(0, Math.min(1, x));
  const E = (x) => 1 - Math.pow(1 - C(x), 3);
  const p = (t, a, d = 0.45) => E((t - a) / d);
  const f3 = (n) => n.toFixed(3);
  const up = (t, a, d = 0.45, y = 36) => {
    const k = p(t, a, d);
    return `opacity:${f3(k)};transform:translateY(${((1 - k) * y).toFixed(1)}px)`;
  };
  const pop = (t, a, d = 0.35, rot = 0) => {
    const k = p(t, a, d);
    return `opacity:${f3(k)};transform:rotate(${rot}deg) scale(${f3(0.9 + 0.1 * k)})`;
  };
  const vis = (t, a, d = 0.3) => `opacity:${f3(p(t, a, d))}`;
  const pad3 = (n) => String(n).padStart(3, "0");

  // hand-drawn marks, drawn on with stroke-dashoffset
  const tickSvg = (k) =>
    `<svg class="tick" viewBox="0 0 70 70" width="86" height="86" style="left:4px;top:-30px"><path d="M8 38 L28 58 L64 6" fill="none" stroke="#1f3fa6" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="100" stroke-dashoffset="${(100 * (1 - k)).toFixed(1)}"/></svg>`;
  const ring = (k, w, h, color = "#d7313e", style = "") =>
    `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" style="position:absolute;pointer-events:none;${style}"><ellipse cx="${w / 2}" cy="${h / 2}" rx="${w / 2 - 8}" ry="${h / 2 - 8}" fill="none" stroke="${color}" stroke-width="7" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="${(100 * (1 - k)).toFixed(1)}" transform="rotate(-4 ${w / 2} ${h / 2})"/></svg>`;
  const strike = (k, w, color = "#d7313e", style = "") =>
    `<svg width="${w}" height="60" viewBox="0 0 ${w} 60" style="position:absolute;pointer-events:none;${style}"><path d="M6 40 Q ${w / 2} 18 ${w - 6} 26" fill="none" stroke="${color}" stroke-width="10" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="${(100 * (1 - k)).toFixed(1)}"/></svg>`;

  const foot = (right = "") => `<div class="foot"><span>YourDOST · #JoBolaNahi</span><span>${right}</span></div>`;
  const swipe = `<span class="swipe">swipe →</span>`;
  const signoff = (lead = "", extra = "") => `
    <div class="signoff">
      ${lead}
      <p class="hand">Bol do. Halka lagega.</p>
      <div class="wordmark">YourDOST</div>
      <div class="facts">Certified experts in 30 seconds · 24×7 · 20+ Indian languages</div>
      ${extra}
    </div>`;
  const helpline = `<div class="helpline">Abhi bahut bhaari lag raha hai? <b>Tele MANAS 14416</b>, free, 24×7, government helpline.</div>`;

  // ---------- reusable objects ----------
  const marksheet = (o = {}) => `
    <div class="paper marksheet" style="${o.style || ""}">
      <div class="ms-head"><p>STATEMENT OF MARKS · 2026</p><h5>SENIOR SECONDARY EXAMINATION</h5></div>
      <p class="ms-name">NAME OF CANDIDATE: <b style="background:linear-gradient(rgba(244,222,142,.95),rgba(244,222,142,.95)) no-repeat 0 70%/${((o.hl || 0) * 100).toFixed(1)}% 80%">RIYA SHARMA</b> · ROLL NO. 26140873</p>
      <table>
        <tr><td>English Core</td><td>94</td></tr>
        <tr><td>Physics</td><td>89</td></tr>
        <tr><td>Chemistry</td><td>91</td></tr>
        <tr><td>Mathematics</td><td>95</td></tr>
        <tr><td>Computer Science</td><td>93</td></tr>
      </table>
      <div class="ms-total"><span>AGGREGATE</span><strong style="position:relative">92.4%${o.pctMark || ""}</strong></div>
      ${o.over || ""}
    </div>`;

  const diya = (t, k, scale = 1) => {
    const flick = 1 + 0.05 * Math.sin(t * 17) + 0.03 * Math.sin(t * 29);
    return `<div class="diya" style="transform:scale(${scale})">
      <div class="glow" style="opacity:${f3(0.9 * k)};transform:translate(-50%,-50%) scale(${f3(0.6 + 0.4 * k)})"></div>
      <div class="flame" style="opacity:${f3(k)};transform:scale(${f3(k * flick)}, ${f3(k * (2 - flick))}) rotate(${(2 * Math.sin(t * 11)).toFixed(2)}deg)"></div>
      <div class="rim"></div><div class="bowl"></div>
    </div>`;
  };

  const chatCard = (o) => `
    <div class="chat card" style="${o.style || ""}">
      <div class="top"><div class="av">${o.initial}</div><div class="who"><b>${o.name}</b><small>${o.status}</small></div></div>
      <div class="msgs">${o.msgs}</div>
      <div class="compose"><div class="field">${o.field}</div><div class="send">➤</div></div>
    </div>`;

  // ---------- reels ----------
  function reelFrame(reel, t) {
    const out = [];
    reel.scenes.forEach((s, i) => {
      const last = i === reel.scenes.length - 1;
      if (t < s.a - 0.001 || (!last && t > s.b + 0.3)) return;
      const o = (i === 0 ? 1 : p(t, s.a, 0.3)) * (last ? 1 : 1 - p(t, s.b, 0.3));
      out.push(`<div class="scene ${s.ground ? "" : ""}" style="opacity:${f3(o)};${s.bg ? "background:" + s.bg : ""}">${s.html(t - s.a, t)}</div>`);
    });
    return out.join("");
  }

  const REEL_DIWALI = {
    dur: 17.5,
    cover: 2.9,
    scenes: [
      {
        a: 0, b: 4.4, bg: "var(--night)",
        html: (lt) => `
        <div class="pad vcenter" style="gap:60px">
          <p class="eyebrow">Diwali safai · Day 3</p>
          <div class="paper checklist tilt-l">
            <h4>Safai list</h4>
            <ul>
              <li><span class="box">${tickSvg(p(lt, 0.1, 0.3))}</span><span>Almirah</span></li>
              <li><span class="box">${tickSvg(p(lt, 0.55, 0.3))}</span><span>Pankhe</span></li>
              <li><span class="box">${tickSvg(p(lt, 1.0, 0.3))}</span><span>Kitchen ki tiles</span></li>
              <li><span class="box"></span><span style="position:relative">Mann${ring(p(lt, 1.7, 0.6), 230, 120, "#d7313e", "left:-40px;top:-14px")}</span></li>
            </ul>
          </div>
          <p class="said m" style="${up(lt, 2.4)}">Sab saaf ho gaya.<br><span style="color:var(--marigold)">Ek cheez reh gayi.</span></p>
        </div>`,
      },
      {
        a: 4.4, b: 8.8, bg: "var(--night)",
        html: (lt) => `
        <div class="pad" style="gap:54px">
          <p class="eyebrow" style="${up(lt, 0, 0.3)}">Safai mein kya kya nikla</p>
          <div style="display:flex;flex-direction:column;gap:44px;align-items:flex-start">
            <div class="tag" style="${pop(lt, 0.2, 0.35, -2)}">Class 10 ka report card<small>rakhein? phenkein?</small></div>
            <div class="tag" style="${pop(lt, 1.0, 0.35, 1.5)};margin-left:180px">Unka diya hua mug<small>rakhein? phenkein?</small></div>
            <div class="tag" style="${pop(lt, 1.8, 0.35, -1)};margin-left:40px">Gym membership card<small>gaye: 1 baar</small></div>
          </div>
          <p class="said m" style="${up(lt, 2.8)}">Sab sort ho gaya.</p>
        </div>`,
      },
      {
        a: 8.8, b: 12.6, bg: "linear-gradient(180deg,#f9d27e,#f39a2b)",
        html: (lt) => `
        <div class="pad vcenter" style="color:var(--text)">
          <p class="said xl" style="${up(lt, 0.1)}">Poora ghar chamka diya.</p>
        </div>
        <div style="position:absolute;inset:0;background:var(--night);opacity:${f3(0.94 * p(lt, 1.5, 0.9))}"></div>
        <div class="pad" style="justify-content:flex-end;padding-bottom:420px">
          <p class="said m" style="${up(lt, 2.0)};color:var(--chalk)">Andar ka ek kona abhi bhi andhera hai.</p>
        </div>`,
      },
      {
        a: 12.6, b: 15.4, bg: "#0c1020",
        html: (lt, t) => `
        <div class="pad center" style="gap:30px;padding-top:520px">
          ${diya(t, p(lt, 0.25, 0.9), 1.3)}
          <p class="hand" style="${up(lt, 1.0)};font-size:84px;color:var(--postcard);margin-top:80px">Is Diwali,<br>ek diya wahan bhi.</p>
        </div>`,
      },
      {
        a: 15.4, b: 17.5, bg: "#0c1020",
        html: (lt, t) => `
        <div class="pad" style="justify-content:flex-end;gap:40px">
          <div style="align-self:center;margin-bottom:60px">${diya(t, 1, 0.8)}</div>
          <div style="${up(lt, 0.15)};color:var(--chalk)">${signoff("", `<div class="facts">#JoBolaNahi</div>`)}</div>
        </div>`,
      },
    ],
  };

  const REEL_EXAMS = {
    dur: 16.6,
    cover: 2.3,
    scenes: [
      {
        a: 0, b: 3.8, bg: "var(--night)",
        html: (lt) => `
        <div class="pad center" style="gap:70px">
          <p class="hand" style="font-size:88px;color:var(--postcard)">Kabhi notice kiya?</p>
          <div class="tilt-r">${marksheet({ pctMark: ring(p(lt, 0.9, 0.7), 420, 200, "#d7313e", "left:-40px;top:-30px") })}</div>
        </div>`,
      },
      {
        a: 3.8, b: 6.8, bg: "var(--night)",
        html: (lt) => {
          const k = p(lt, 0.1, 1.1);
          const sc = 1 + 1.6 * k, tx = -510 * k, ty = -40 * k;
          return `
          <div style="position:absolute;left:110px;top:520px;transform-origin:0 0;transform:translate(${tx.toFixed(1)}px,${ty.toFixed(1)}px) scale(${f3(sc)})">${marksheet({ hl: p(lt, 1.1, 0.5) })}</div>
          <div style="position:absolute;left:0;right:0;bottom:0;height:760px;background:linear-gradient(180deg,rgba(20,26,46,0),var(--night) 34%)"></div>
          <div class="pad" style="justify-content:flex-end;gap:20px">
            <p class="said" style="${up(lt, 0.7)}">Percentage: <span style="color:var(--marigold)">bold.</span></p>
            <p class="said" style="${up(lt, 1.4)}">Naam: <span style="font-size:58px;font-weight:500;color:var(--chalk-soft)">chhote font mein.</span></p>
          </div>`;
        },
      },
      {
        a: 6.8, b: 10.4, bg: "var(--night)",
        html: (lt) => `
        <div class="pad" style="gap:30px">
          <p class="eyebrow" style="${vis(lt, 0)}">1:07 AM</p>
          <div class="card notif" style="${up(lt, 0.15)}"><div class="ic">MT</div><div class="tx"><b>Mock Test 14 · Result</b><span>AIR 8,921. Keep practising! 💪</span><small>now</small></div></div>
          <div class="card notif" style="${up(lt, 0.9)}"><div class="ic">FA</div><div class="tx"><b>Family ❤️</b><span>Bunty ke 97% aaye!! 🎉🎉🎉</span><small>2 min ago</small></div></div>
          <div class="card notif" style="${up(lt, 1.6)}"><div class="ic">MU</div><div class="tx"><b>Mummy</b><span>beta kitne aaye?</span><small>5 min ago</small></div></div>
          <p class="said m" style="${up(lt, 2.4)};margin-top:40px">Har jagah sirf number.</p>
        </div>`,
      },
      {
        a: 10.4, b: 13.8, bg: "var(--night)",
        html: (lt) => `
        <div class="pad" style="gap:46px">
          <p class="said s" style="${up(lt, 0.05)}">Marksheet pe percentage bold mein chhapta hai, naam chhote font mein.</p>
          <div style="position:relative;align-self:center">
            ${marksheet({ pctMark: strike(p(lt, 0.35, 0.4), 470, "#d7313e", "left:-30px;top:40px") })}
            <div style="position:absolute;left:40px;top:150px;font-family:var(--f-hand);font-weight:700;font-size:300px;line-height:1;color:var(--ink);transform:rotate(-7deg);clip-path:inset(-20% ${(100 - 100 * p(lt, 0.8, 1.0)).toFixed(1)}% -20% -5%)">Riya</div>
          </div>
          <p class="hand" style="${up(lt, 2.0)};font-size:96px;color:var(--postcard)">Tum ulta yaad rakhna.</p>
        </div>`,
      },
      {
        a: 13.8, b: 16.6, bg: "var(--night)",
        html: (lt) => `
        <div class="pad" style="justify-content:flex-end;gap:40px">
          <p class="said m" style="${up(lt, 0.1)}">Exam ka stress?</p>
          <div style="${up(lt, 0.4)}">${signoff("", `<p class="body s">Tumhare school ya college mein shayad YourDOST pehle se hai. College email check karo.</p>`)}</div>
          <div style="${up(lt, 0.8)}">${helpline}</div>
        </div>`,
      },
    ],
  };

  const REEL_JOBS = {
    dur: 16.8,
    cover: 2.6,
    scenes: [
      {
        a: 0, b: 3.2, bg: "var(--postcard)",
        html: (lt) => `
        <div class="pad vcenter" style="gap:30px">
          <p class="eyebrow">Job hunt · Day 94</p>
          <div class="counter">#${pad3(Math.max(1, Math.round(147 * p(lt, 0.05, 2.0))))}</div>
          <p class="hand" style="font-size:80px">applications.</p>
          <div class="pills" style="${up(lt, 2.1)}"><span class="pill">Submitted 11:58 PM</span><span class="pill">Easy Apply</span><span class="pill">Referral? none</span></div>
        </div>`,
      },
      {
        a: 3.2, b: 7.2, bg: "var(--postcard)",
        html: (lt) => {
          const rows = [
            ["Talent Team", "Update on your application"],
            ["Careers", "Unfortunately, we have decided to move forward with other candidates"],
            ["Recruiting", "After careful consideration…"],
            ["HR Ops", "We regret to inform you that…"],
            ["no-reply", "Thank you for your interest in the role"],
            ["Hiring", "Your application status has changed"],
          ];
          return `
          <div class="pad" style="gap:40px">
            <p class="eyebrow">Inbox</p>
            <div class="card inbox">${rows.map((r, i) => `<div class="row" style="${up(lt, 0.1 + i * 0.32, 0.3, 20)}"><b>${r[0]}</b><span>${r[1]}</span></div>`).join("")}</div>
            <div class="pills" style="${up(lt, 2.3)}"><span class="pill r">Rejections: 61</span><span class="pill">No reply: 86</span></div>
          </div>`;
        },
      },
      {
        a: 7.2, b: 10.2, bg: "var(--postcard)",
        html: (lt) => {
          const posts = [
            ["RK", "Rohan K.", "Excited to announce I've joined as Associate! 🎉"],
            ["SP", "Sneha P.", "Thrilled to share I'm starting a new role ✨"],
            ["KS", "Kabir S.", "Day 1. Grateful for this journey 🙏"],
          ];
          return `
          <div class="pad" style="gap:28px">
            <p class="eyebrow">Meanwhile, batchmates</p>
            ${posts.map((x, i) => `<div class="card notif" style="${up(lt, 0.15 + i * 0.6)}"><div class="ic">${x[0]}</div><div class="tx"><b>${x[1]}</b><span>${x[2]}</span><small>👏 Congratulate</small></div></div>`).join("")}
            <p class="said m" style="${up(lt, 2.2)};margin-top:30px">Sabka "excited to announce".</p>
          </div>`;
        },
      },
      {
        a: 10.2, b: 13.4, bg: "var(--postcard)",
        html: (lt) => {
          const reply = "Haan maa, process mein hai.";
          const n = Math.round(reply.length * C((lt - 0.9) / 1.1));
          return `
          <div class="pad center" style="gap:50px">
            ${chatCard({
              initial: "M", name: "Maa", status: "online",
              msgs: `<span class="chip">Today</span><div class="bub in" style="${up(lt, 0.2, 0.3, 16)}">Beta, kuch hua? 🙂<small>8:14 PM</small></div>`,
              field: `${reply.slice(0, n)}<span class="caret"></span>`,
            })}
            <p class="hand redpen" style="${up(lt, 2.3)};font-size:90px;color:var(--redpen)">(kuch nahi hua.)</p>
          </div>`;
        },
      },
      {
        a: 13.4, b: 16.8, bg: "var(--postcard)",
        html: (lt) => `
        <div class="pad" style="gap:40px;justify-content:flex-end">
          <p class="said s" style="${up(lt, 0.05)}">147 applications. 61 "we regret to inform you". 86 ne reply bhi nahi kiya.</p>
          <p class="hand" style="${up(lt, 0.7)};font-size:86px">Tumhara inbox tumhare baare mein faisla nahi hai.</p>
          <div style="${up(lt, 1.6)}">${signoff("", `<p class="body s">Career counselling aur emotional support, ek hi jagah.</p>`)}</div>
        </div>`,
      },
    ],
  };

  // ---------- statics, carousels, stories ----------
  const S = {};

  // 02 AI carousel
  S.ai = [
    () => `<div class="pad">
      <p class="said">It did my 3-day task in 40 seconds.</p>
      <div class="card prompt">
        <div class="pr-in">Make the Q3 campaign plan: audience, channels, budget split and 12 post ideas.</div>
        <div class="lines"><i style="width:92%"></i><i style="width:78%"></i><i style="width:86%"></i><i style="width:60%"></i></div>
        <div class="pr-out"><b>✓ Done in 40 sec</b></div>
      </div>
      <p class="hand">I typed "wow 🔥".<br>Then I didn't sleep.</p>
    </div>${foot(swipe)}`,
    () => `<div class="pad">
      <p class="eyebrow">My search history · 2:14 AM</p>
      <div class="card search">
        <div class="row">will AI replace marketing jobs</div>
        <div class="row">jobs AI can't do 2027</div>
        <div class="row">prompt engineering course fast</div>
        <div class="row">is 31 too late to switch careers</div>
        <div class="row">how to stop overthinking at night</div>
      </div>
      <p class="hand s">Every tab made it worse.</p>
    </div>${foot("2/7")}`,
    () => `<div class="pad">
      <p class="said m">This month I bought 4 AI courses.</p>
      <div class="courses">
        ${[["Generative AI for Professionals", 0], ["Prompt Engineering Masterclass", 3], ["AI for Marketers: Zero to Pro", 0], ["Automate Your Job with AI", 0]].map((c) => `<div class="card course"><b>${c[0]}</b><div class="bar"><i style="width:${c[1]}%"></i></div><small>${c[1]}% complete</small></div>`).join("")}
      </div>
      <p class="hand">Not lazy. Scared.<br>Panic is not a learning plan.</p>
    </div>${foot("3/7")}`,
    () => `<div class="pad vcenter" style="gap:60px">
      <p class="said m">The fear isn't really about the tool.</p>
      <p class="hand" style="font-size:84px">It's this: "If my work can be done without me… who am I?"</p>
    </div>${foot("4/7")}`,
    () => `<div class="pad vcenter" style="gap:50px">
      <p class="said">That's not a tech question.</p>
      <p class="said" style="color:var(--ink)">It's an identity question.</p>
      <p class="body">It deserves a real conversation. Not a 15th tab at 2 AM.</p>
    </div>${foot("5/7")}`,
    () => `<div class="pad" style="gap:34px">
      <p class="eyebrow">Try this tonight · 2 minutes</p>
      <p class="said s">Write 3 things people thank you for that aren't in your job description.</p>
      <div class="notebook tilt-l" style="width:904px;padding-left:120px">
        <ol style="font-size:40px">
          <li>1. <span class="dim">calming the room when things break</span></li>
          <li>2. ____________________________</li>
          <li>3. ____________________________</li>
        </ol>
      </div>
      <p class="hand s">Keep the list. Read it before the next town hall.</p>
    </div>${foot("6/7")}`,
    () => `<div class="pad" style="gap:34px">
      <p class="said s">If your chest tightens every time someone says "we're automating this", you're not overreacting.</p>
      <p class="body s">Talk it through with a YourDOST expert. Your company may already cover YourDOST: ask HR.</p>
      <p class="hand s">Send this to the colleague who's been "fine" since the last town hall.</p>
      <div style="margin-top:24px">${signoff()}</div>
    </div>`,
  ];

  // 04 breakup static
  S.breakup = [
    () => `<div class="pad" style="gap:34px">
      <p class="hand" style="font-size:62px">Aaj kuch funny hua. Tumhe batane ke liye phone uthaya.</p>
      ${chatCard({
        initial: "?", name: "don't.", status: "last seen today at 11:47 pm",
        msgs: `<span class="chip">14 September</span>
          <div class="bub in">ok.<small>10:02 PM</small></div>
          <div class="bub out">take care ❤️<small>10:05 PM ✓✓</small></div>
          <span class="chip">Today</span>`,
        field: `sun, aaj kuch bahut funny hua 😂<span class="caret"></span>`,
        style: "align-self:center",
      })}
      <p class="said xl" style="margin-top:6px">Phir yaad aaya.</p>
    </div>${foot("<b>YourDOST</b>")}`,
  ];

  // 05 patch-up carousel
  S.patchup = [
    () => `<div class="pad" style="gap:44px">
      <div class="comments">
        <div class="cmt"><i style="background:#e0699a">AN</i>finally!!! 🥹❤️</div>
        <div class="cmt" style="margin-left:120px"><i style="background:#3f7dd8">VS</i>knew it 😌</div>
        <div class="cmt" style="margin-left:40px"><i style="background:#2e9b74">MK</i>ab mat ladna dono 😂</div>
      </div>
      <p class="said m">Wapas saath hain. Sabne bola "finally!"</p>
      <p class="hand">Kisi ne nahi bataya ki asli kaam patch-up ke baad shuru hota hai.</p>
    </div>${foot(swipe)}`,
    () => `<div class="pad" style="gap:54px">
      <p class="said s">Patch-up ke baad jo koi post nahi karta:</p>
      <ul class="list">
        <li>uska "ok" chaar baar padhna</li>
        <li>doston ko na batana, kyunki "phir se?"</li>
        <li>extra accha banna, taaki dobara na toote</li>
        <li>har late reply pe wahi purana dar</li>
      </ul>
    </div>${foot("2/6")}`,
    () => `<div class="pad vcenter" style="gap:60px">
      <p class="said xl">Miss karna<br><span style="color:var(--postcard)">≠</span> bharosa karna.</p>
      <p class="hand">Dono sach hain. Dono alag speed se theek hote hain.</p>
    </div>${foot("3/6")}`,
    () => `<div class="pad vcenter" style="gap:56px">
      <svg viewBox="0 0 900 160" width="900" height="160" style="overflow:visible"><path d="M0 80 L120 70 L170 110 L260 40 L330 95 L420 60 L470 120 L560 50 L640 100 L720 70 L800 90 L900 76" fill="none" stroke="#f6f1e6" stroke-width="6" stroke-linejoin="round"/>${[150, 300, 450, 600, 750].map((x) => `<path d="M${x - 16} 40 L${x + 16} 120" stroke="#f4de8e" stroke-width="7" stroke-linecap="round"/>`).join("")}</svg>
      <p class="said m">Patch-up reset button nahi hai. Renovation hai.</p>
      <p class="hand">Crack pe paint nahi karte. Deewar theek karte hain.</p>
    </div>${foot("4/6")}`,
    () => `<div class="pad" style="gap:50px">
      <div><p class="said m">3 sawaal, ek doosre se.</p><p class="hand xs" style="margin-top:10px">(raat 1 baje nahi.)</p></div>
      <ol class="qs">
        <li>Is baar sach mein kya badla?</li>
        <li>Agli baar mushkil aaye, toh hum kya karenge?</li>
        <li>Mujhe kya bolna band karna hai, aur tumhe kya karna band karna hai?</li>
      </ol>
    </div>${foot("5/6")}`,
    () => `<div class="pad" style="gap:36px">
      <p class="said s">Kabhi kabhi room mein teesra insaan hona sabse brave move hota hai.</p>
      <p class="hand s">Counsellor ke paas jaana haar nahi. Serious hone ka sign hai.</p>
      <p class="body s">Talk to a YourDOST relationship expert. Send this to your +1. Ya chupke se save kar lo.</p>
      <div style="margin-top:24px">${signoff()}</div>
    </div>`,
  ];

  // 06 founder static
  S.founder = [
    () => `<div class="pad" style="gap:44px">
      <div class="card deck">
        <div class="dk-top"><span>14 / 14</span><span>CONFIDENTIAL</span></div>
        <h5>Founder health</h5>
        <p class="dk-sub">Not in the data room.</p>
        <div class="kpis">
          <div class="kpi"><span>Runway</span><strong>7 mo</strong><em>▼ 2 since Aug</em></div>
          <div class="kpi"><span>Sleep</span><strong>4 hrs</strong><em>▼ avg, last 30 days</em></div>
          <div class="kpi alert"><span>People I can be honest with</span><strong>0</strong><em>no change</em></div>
        </div>
      </div>
      <p class="said m">Investors ask about the first number.</p>
      <p class="hand" style="font-size:78px">Who's asking about the third?</p>
    </div>${foot("<b>YourDOST</b>")}`,
  ];

  // 07 men's day static
  S.mens = [
    () => `<div class="pad" style="gap:30px;padding-top:80px">
      <p class="eyebrow">19 Nov · International Men's Day</p>
      <div class="notebook tight tilt-l" style="width:912px;padding-left:124px;padding-right:36px">
        <h4>Is hafte usne kaha:</h4>
        <ol style="font-size:37px">
          <li><i>Mon 9:10 AM</i>"theek hoon yaar"</li>
          <li><i>Mon 8 PM</i>"haan maa, sab badhiya"</li>
          <li><i>Tue</i>"chill hai bro"</li>
          <li><i>Tue 11 PM</i>"bas thoda thaka hoon"</li>
          <li><i>Wed</i>"kuch nahi, aise hi"</li>
          <li><i>Wed 2:10 AM</i>"neend nahi aa rahi, baaki theek"</li>
          <li><i>Thu</i>"office mein thoda scene hai"</li>
          <li><i>Fri</i>"arre fine hoon"</li>
          <li><i>Sat</i>"main dekh lunga"</li>
          <li><i>Sun</i>"😂 sab mast"</li>
          <li><i>Sun 11 PM</i>"theek hoon yaar"</li>
          <li><i>12.</i>__________________</li>
        </ol>
      </div>
      <p class="said s">11 baar "theek hoon".<br><span style="color:var(--postcard)">12vi baar poocho. Phir ruko.</span></p>
    </div>${foot("<b>YourDOST</b>")}`,
  ];

  // 10 HR carousel
  S.hr = [
    () => `<div class="pad" style="gap:40px">
      <p class="said m">Her exit form said "better opportunity".</p>
      <div class="paper form tilt-r">
        <div class="fm-top"><span>EXIT INTERVIEW</span><span>FORM HR-07</span></div>
        <h5>Priya M.</h5>
        <p class="fm-meta">Senior Analyst · 3 yrs 2 months · Rated "exceeds" twice</p>
        <p class="fm-q">Primary reason for leaving</p>
        <div class="opts">
          <div class="opt"><span class="cb"></span>Compensation</div>
          <div class="opt"><span class="cb on"></span>Better opportunity</div>
          <div class="opt"><span class="cb"></span>Relocation</div>
          <div class="opt"><span class="cb"></span>Higher studies</div>
        </div>
      </div>
      <p class="hand">The real reason was her green dot at 1:40 AM.</p>
    </div>${foot(swipe)}`,
    () => `<div class="pad" style="gap:48px">
      <p class="said m">Burnout rarely arrives as a resignation letter.</p>
      <p class="body">First, it shows up as:</p>
      <div class="chips"><span>cameras off</span><span>"sounds good 👍"</span><span>Monday sick leave</span><span>the 11 PM "just checking"</span><span>lunch at the desk, every day</span></div>
    </div>${foot("2/7")}`,
    () => `<div class="pad vcenter" style="gap:34px">
      <p class="said xl" style="color:var(--postcard)">₹1.1 lakh crore</p>
      <p class="said s">a year.</p>
      <p class="body">What poor employee mental health costs Indian employers, through absenteeism, presenteeism and attrition. Presenteeism, people at work but not okay, is the biggest share.</p>
      <p class="src">Deloitte, Mental Health and Well-being in the Workplace, 2022 (about US$14 bn)</p>
    </div>${foot("3/7")}`,
    () => `<div class="pad vcenter" style="gap:50px">
      <p class="said m">An EAP nobody uses is a line item, not a benefit.</p>
      <p class="body">People reach out when support is:</p>
      <div class="tiles"><div><strong>Private</strong><span>no manager in the loop</span></div><div><strong>Instant</strong><span>at 1:40 AM, not next Tuesday</span></div><div><strong>Theirs</strong><span>in the language they think in</span></div></div>
    </div>${foot("4/7")}`,
    () => `<div class="pad vcenter" style="gap:40px">
      <p class="eyebrow">YourDOST, in numbers</p>
      <div class="tiles big"><div><strong>30 sec</strong><span>to reach a certified expert</span></div><div><strong>24×7</strong><span>including 1:40 AM</span></div><div><strong>20+</strong><span>Indian languages</span></div><div><strong>500+</strong><span>organisations</span></div><div><strong>30 lakh+</strong><span>one-on-one sessions</span></div><div><strong>23+</strong><span>states</span></div></div>
      <p class="src">Source: YourDOST</p>
    </div>${foot("5/7")}`,
    () => `<div class="pad vcenter" style="gap:50px">
      <p class="eyebrow">Try this at your next 1:1</p>
      <p class="said m">Ask: "How's your week, <span style="color:var(--postcard)">really?</span>"</p>
      <p class="hand">Then wait 5 seconds longer than feels comfortable.</p>
      <div class="timer"><i>1</i><i>2</i><i>3</i><i>4</i><i>5</i></div>
    </div>${foot("6/7")}`,
    () => `<div class="pad" style="gap:36px">
      <p class="said m">Want your people to actually use support?</p>
      <p class="body">Book a YourDOST demo. Link in bio.</p>
      <p class="hand s">Tag the leader on your team who asks "really".</p>
      <div style="margin-top:24px">${signoff()}</div>
    </div>`,
  ];

  // 09 employee stories (1080 x 1920). `bare` drops the mock stickers for export:
  // real poll / slider / quiz / question stickers are added natively in the Instagram app.
  const slot = (label) => `<div class="sticker-slot">Add native ${label} sticker here in the Instagram app</div>`;
  S.stories = [
    (o) => `<div class="pad vcenter" style="gap:60px">
      <p class="said m">Office mein "How are you?" ka sirf ek allowed answer hai:</p>
      <div class="bigbub">Good, you? 🙂</div>
      <p class="hand" style="font-size:76px">Yahan sach bol sakte ho. Tap →</p>
    </div>${foot("1/6")}`,
    (o) => `<div class="pad vcenter" style="gap:60px">
      <p class="said m">Sunday, 6 PM. Kaisa lag raha hai?</p>
      ${o.bare ? slot("poll") : `<div class="sticker"><div class="st-q">Sunday 6 PM feels like…</div><div class="st-opts"><div>Sunday hi hai 🙂</div><div>Monday ka trailer 😩</div></div></div>`}
    </div>${foot("2/6")}`,
    (o) => `<div class="pad vcenter" style="gap:60px">
      <p class="said m">Battery abhi kitni hai? Sach batana.</p>
      ${o.bare ? slot("emoji slider (🔋)") : `<div class="sticker"><div class="st-q">Meri battery right now</div><div class="slider"><b>🔋</b></div></div>`}
    </div>${foot("3/6")}`,
    (o) => `<div class="pad vcenter" style="gap:60px">
      <p class="said m">Laptop ke bina last lunch kab kiya tha?</p>
      ${o.bare ? slot("quiz") : `<div class="sticker"><div class="st-q">Quiz time</div><div class="st-opts"><div>Aaj</div><div>Is hafte</div><div>Allowed hai kya? 😶</div></div></div>`}
    </div>${foot("4/6")}`,
    (o) => `<div class="pad vcenter" style="gap:60px">
      <p class="said m">Ek baat jo tum chahte ho tumhara manager jaane.</p>
      ${o.bare ? slot("question box") : `<div class="sticker"><div class="st-q">Manager ko yeh pata hona chahiye…</div><div class="ans">Likho… naam hum kabhi share nahi karenge</div></div>`}
      <p class="hand s">Kal kuch jawab share karenge. Bina naam ke.</p>
    </div>${foot("5/6")}`,
    (o) => `<div class="pad vcenter" style="gap:46px">
      <p class="said m">Battery 20% se kam thi?</p>
      <p class="said s" style="color:var(--ink)">Yeh productivity problem nahi hai.</p>
      <p class="body s">Tumhari company shayad pehle se YourDOST deti hai. HR se poocho, ya benefits portal check karo.</p>
      ${o.bare ? slot("link (yourdost.com)") : `<div class="sticker link">🔗 TALK TO AN EXPERT</div>`}
      ${signoff()}
    </div>`,
  ];

  // ---------- the ten posts (numbered in posting order) ----------
  const POSTS = [
    {
      id: "01", slug: "diwali", kind: "reel", tall: true, ground: "g-night", reel: REEL_DIWALI,
      title: "Andar ka kona", theme: "Diwali", format: "Reel · 17 s",
      segment: "Everyone home for Diwali, especially 18–30s back from hostels and first jobs",
      date: "Sun 8 Nov", time: "11:00 AM", day: 8,
      line: "Poora ghar chamka diya. Andar ka ek kona abhi bhi andhera hai.",
      line2: "Is Diwali, ek diya wahan bhi.",
      en: "The whole house is shining. One corner inside is still dark. This Diwali, light a diya there too.",
      why: "Diwali week, every home is deep-cleaning, so the post borrows a ritual people are already doing instead of asking them to stop and think about mental health. A reel, because the turn from bright to dark has to be seen happening.",
      hook: "Frame one is a Diwali cleaning checklist: Almirah ✓, Pankhe ✓, Kitchen tiles ✓, Mann ☐. The unticked box is the hook, readable in under a second with the sound off.",
      caption: "Is saal kuch cheezein bina bataye bhaari ho gayi.\n\nAgar tumhara bhi aisa saal tha, comments mein bas ek 🪔 chhod do. Kuch likhna zaroori nahi. Hum har diya padhenge.\n\nAur agar kisi se baat karni hai, festival ke din bhi, YourDOST ke experts 24×7 hain. Link in bio.\n\n#JoBolaNahi #Diwali2026",
      mechanic: "One-emoji comment (🪔). It's the lowest-effort way to say \"me too\" in public. The team replies to every diya in the first two hours with a real line, not a template. Pin the post for festive week. Add a story \"Add Yours\" sticker: \"Ek diya mere liye\".",
      human: "Every Indian home is deep-cleaning that week, so the post rides a ritual instead of a hashtag. The gym-membership card (\"gaye: 1 baar\") gets a laugh right before the turn, and the laugh is what lets the turn land.",
      measure: "Comments and story reshares",
    },
    {
      id: "02", slug: "ai-anxiety", kind: "carousel", ground: "g-inland", slides: S.ai,
      title: "40 seconds", theme: "AI and job fear", format: "Carousel · 7 slides",
      segment: "Working professionals, 24–40, in tech, marketing, design and ops",
      date: "Tue 10 Nov", time: "9:30 PM", day: 10,
      line: "It did my 3-day task in 40 seconds.",
      line2: "I typed \"wow 🔥\". Then I didn't sleep.",
      en: "",
      why: "Most AI fear is really fear about self-worth, and a first-person confession reads like a peer, not a brand. A carousel, because each swipe is one more 2 AM thought, the way the spiral actually goes.",
      hook: "The first line is a confession, not a statistic. The chat card under it proves the 40 seconds, and the handwritten \"Then I didn't sleep\" is the unsaid half that makes people swipe.",
      caption: "In a July 2026 Blind survey, 66% of AI and ML professionals in India said they expect layoffs or big headcount cuts in the next 3–6 months.\n\nThat isn't a \"you\" problem. That's a lot of people lying awake at 2 AM with 14 tabs open.\n\nSlide 6 takes two minutes. Do it tonight.\n\nAnd send this to the colleague who's been saying \"it's fine\" since the last town hall.\n\n#JoBolaNahi #AIanxiety",
      mechanic: "Send-to-a-colleague. DM shares are the strongest reach signal on Instagram, and \"the colleague who's been fine since the town hall\" names a real person in the reader's head. Slide 6 is a two-minute exercise, which earns the save.",
      human: "Specific numbers do the work: 3 days → 40 seconds, 2:14 AM, 4 courses bought and 0 finished, \"is 31 too late\". It never claims AI won't take jobs. It talks about the part of the fear that is about self-worth, where YourDOST can actually help.",
      measure: "Shares (DM) and saves",
    },
    {
      id: "03", slug: "exams", kind: "reel", tall: true, ground: "g-night", reel: REEL_EXAMS,
      title: "Chhota font", theme: "Exam pressure", format: "Reel · 17 s",
      segment: "Students: boards, JEE/NEET aspirants, CAT takers. Parents and teachers share it",
      date: "Thu 12 Nov", time: "6:30 PM", day: 12,
      line: "Marksheet pe percentage bold mein chhapta hai, naam chhote font mein.",
      line2: "Tum ulta yaad rakhna.",
      en: "On a marksheet the percentage is printed in bold and your name in small font. Remember it the other way round.",
      why: "Every student has held this marksheet, and the font-size detail is true but nobody has pointed it out. A reel, because the zoom from 92.4% to the tiny name makes the whole argument in three seconds.",
      hook: "\"Kabhi notice kiya?\" over a real-looking marksheet, with a red-pen circle around 92.4%. It's an observation every student has seen a hundred times and never noticed, so the eye stops to check.",
      caption: "Boards, JEE, NEET, CAT… season shuru ho gaya hai.\n\nComments mein woh naam likho jisse tumhe log yaad rakhein. Rank nahi. Naam. Ghar ka naam bhi chalega. Hum shuru karte hain: Golu.\n\nPressure bhaari ho raha hai toh kisi se baat karo. Bahut saare colleges students ko YourDOST pehle se dete hain. Apna college email check karo.\n\nAbhi bahut mushkil lag raha hai? Tele MANAS: 14416, free, 24×7.\n\n#JoBolaNahi #ExamStress",
      mechanic: "\"Comment your name\". The comments become a wall of names, which is the visual for a follow-up post. Teachers and parents forward it to class and family groups. The college-email line routes students to the access many already have through campus tie-ups.",
      human: "It never says \"don't stress\". It finds a true detail (font sizes on a marksheet) and hands the student a reframe they can say to themselves. The 1:07 AM mock-test result, the family-group \"Bunty ke 97%\" and \"kitne aaye?\" are pressures every student will recognise.",
      measure: "Comments and shares to WhatsApp",
    },
    {
      id: "04", slug: "breakup", kind: "static", ground: "g-postcard", slides: S.breakup,
      title: "Drafts", theme: "Breakup", format: "Static image",
      segment: "College students and young adults, 18–26",
      date: "Sat 14 Nov", time: "10:30 PM", day: 14,
      line: "Aaj kuch funny hua. Tumhe batane ke liye phone uthaya.",
      line2: "Phir yaad aaya.",
      en: "Something funny happened today. I picked up the phone to tell you. Then I remembered.",
      why: "A screenshot-style image looks like something a friend would post, so it travels as \"literally me\". The unsent message is the campaign idea at its simplest: the thing we didn't say.",
      hook: "It looks like a friend's screenshot, not an ad: a chat with \"don't.\", last seen 11:47 pm, and a message typed but not sent. People recognise the moment before they register the brand.",
      caption: "Breakup sabse zyada fight mein nahi dukhta.\nDukhta hai kisi random Tuesday, 4:15 pm, jab kuch funny hota hai aur jisko batana tha, woh ab tumhara nahi.\n\nYeh reflex jaata hai. Jitna chahte ho usse dheere, jitna sochte ho usse jaldi.\n\nTab tak, drafts mein mat rakho. Kisi se baat karo. YourDOST ke experts raat 2 baje bhi jaage hote hain.\n\nSave this for the night you almost hit send.\n\n#JoBolaNahi",
      mechanic: "Save (\"for the night you almost hit send\") plus story reshares. The screenshot format gets reposted as \"literally me\", which carries the post into friend groups the brand can't reach.",
      human: "YourDOST's own Warrior story about Harshal describes this exact loneliness: a breakup with \"no friends to talk to\". The post picks the smallest, truest moment, the muscle memory of reaching for the phone, instead of describing heartbreak.",
      measure: "Saves and story reshares",
    },
    {
      id: "05", slug: "patch-up", kind: "carousel", ground: "g-night", slides: S.patchup,
      title: "Finally!", theme: "Getting back together", format: "Carousel · 6 slides",
      segment: "Young couples, 20–30, who got back together",
      date: "Mon 16 Nov", time: "8:30 PM", day: 16,
      line: "Wapas saath hain. Sabne bola \"finally!\"",
      line2: "Kisi ne nahi bataya ki asli kaam patch-up ke baad shuru hota hai.",
      en: "We're back together. Everyone said \"finally!\" Nobody said the real work starts after the patch-up.",
      why: "Patch-ups are a gap: plenty of breakup content, almost none for couples who got back together. A carousel, because it carries a small toolkit (three questions) that people save and send.",
      hook: "Friends' comments (\"finally!!! 🥹❤️\", \"ab mat ladna dono 😂\") set up a happy ending, then the handwritten line undercuts it. The topic itself is the hook: there are endless breakup posts and almost none about patch-ups.",
      caption: "Breakups pe hazaar posts hain. Patch-ups pe koi nahi. Toh yeh rahi.\n\nAgar tum dono wapas saath ho aur phir bhi andar se dar lagta hai, that's normal. It doesn't mean it was a mistake. It means trust is still being rebuilt.\n\nSlide 5 is for both of you. Send it to them, or save it for when you're ready.\n\n#JoBolaNahi",
      mechanic: "Send-to-partner (DM share) and save. Slide 5 gives couples three questions to ask each other, a reason to open the conversation that doesn't feel like an accusation.",
      human: "It shows the public celebration and the private fear side by side: reading their \"ok\" four times, not telling friends because \"phir se?\". The renovation metaphor (\"you fix the wall, you don't paint over the crack\") is something people repeat to each other.",
      measure: "Shares (DM) and saves",
    },
    {
      id: "06", slug: "founder", kind: "static", ground: "g-inland", slides: S.founder,
      title: "The third number", theme: "Founders", format: "Static image + LinkedIn",
      segment: "Founders and early startup teams. Incubators and VCs share it",
      date: "Wed 18 Nov", time: "8:30 AM", day: 18,
      line: "Runway: 7 months. Sleep: 4 hours. People I can be honest with: 0.",
      line2: "Investors ask about the first number. Who's asking about the third?",
      en: "",
      why: "Founders read decks all day, so the post speaks their format and ends on the number nobody tracks. It also leads into YourDOST's founders programme, the offering in Q3.",
      hook: "A pitch-deck slide is a founder's native language. \"Slide 14/14: Founder health, not in the data room\" looks like something they've made themselves, and the red 0 is the confession.",
      caption: "Founders are the only people in the company who can't have a bad day out loud.\n\nThe team needs morale. Investors need conviction. Family wanted you to take the safe job. So it goes nowhere.\n\nIf your third number is 0, let's make it 1. YourDOST has an emotional wellness programme built for founders: yourdost.com/emotional-wellness-founders. Or start small with an instant chat with an expert, 24×7, no pitch deck required.\n\nFounders: what's your third number? DM it if you'd rather not comment.\n\nIncubators and VCs: YourDOST works with portfolio teams too.\n\n#JoBolaNahi #FounderMentalHealth",
      mechanic: "\"What's your third number?\" invites a comment or a DM. Cross-post the same day on LinkedIn, where founders and investors actually read. The incubator line and the programme link open the conversation the founders-programme pitch (Q3) needs.",
      human: "It shows founder loneliness using a founder's own numbers instead of explaining it. YourDOST's blog has almost nothing for founders, so this opens a segment the brand isn't speaking to yet.",
      measure: "DMs, LinkedIn reach, incubator enquiries",
    },
    {
      id: "07", slug: "mens-day", kind: "static", ground: "g-night", slides: S.mens,
      title: "12vi baar", theme: "International Men's Day", format: "Static image",
      segment: "Men 18–35, and the people who love them: partners, sisters, friends, mothers",
      date: "Thu 19 Nov", time: "9:00 AM", day: 19,
      line: "Is hafte usne 11 baar \"theek hoon\" bola.",
      line2: "12vi baar poocho. Phir ruko.",
      en: "This week he said \"I'm fine\" 11 times. Ask him a 12th time. Then wait.",
      why: "Men's Day posts are usually quotes. This one gives people something specific to forward and one small thing to do. A static notebook page, because the list itself is the story.",
      hook: "A notebook page that logs every \"theek hoon\" with a timestamp, including \"Wed 2:10 AM: neend nahi aa rahi, baaki theek\". The 2:10 AM entry is where readers stop.",
      caption: "19 November, International Men's Day.\n\nBahut saare ladkon ko sikhaya gaya hai: bike theek karo, bill bhar do, aur jo andar hai woh chupchaap ghar le jao.\n\nAaj usse koi quote mat bhejo. Yeh bhejo. Aur poocho, sach mein kaisa hai.\n\nAgar woh tumse nahi bol pa raha, YourDOST ke experts 24×7 hain. \"Mard ko dard nahi hota\" ki zaroorat nahi.\n\nTele MANAS: 14416, free, 24×7.\n\n#JoBolaNahi #InternationalMensDay",
      mechanic: "\"Send this to him\". The post is built to be forwarded on Men's Day, when people are looking for something to send that isn't a generic quote.",
      human: "Each entry has a context (to mom, to the cricket group, at 2 AM), so the reader fills in a real man they know. It asks for one small action: ask once more, then wait.",
      measure: "Shares (DM)",
    },
    {
      id: "08", slug: "job-hunt", kind: "reel", tall: true, ground: "g-postcard", reel: REEL_JOBS,
      title: "Process mein hai", theme: "Job hunt", format: "Reel · 17 s",
      segment: "Freshers in placement season, and people laid off and looking",
      date: "Fri 20 Nov", time: "7:30 PM", day: 20,
      line: "147 applications. 61 \"we regret to inform you\". 86 ne reply bhi nahi kiya.",
      line2: "Tumhara inbox tumhare baare mein faisla nahi hai.",
      en: "147 applications. 61 rejections. 86 never replied. Your inbox is not a verdict on you.",
      why: "Job hunting runs on numbers, so the reel counts them up and then lets go of them. \"Haan maa, process mein hai\" is a line almost everyone in a job hunt has said.",
      hook: "An application counter racing from #001 to #147 in two seconds. Anyone job-hunting knows their own number, and the motion holds the thumb.",
      caption: "Woh \"after careful consideration\" wala email? Aksar software bhejta hai, ek saath sau logon ko. Please usse apni teen din ki self-worth mat do.\n\nComments mein apna application count likho. Dikhate hain ki is mein koi akela nahi hai.\n\nRecruiters reading this: reply to one candidate you ghosted. Today.\n\n#JoBolaNahi #JobHunt",
      mechanic: "\"Comment your application count\". Numbers are easy to type, and the thread becomes a solidarity wall. The recruiter line gets shared by HR people, which reaches YourDOST's B2B buyers.",
      human: "\"Haan maa, process mein hai\" is a white lie almost every job-seeker has told. The reel pairs it with the batchmates' \"excited to announce\" posts.",
      measure: "Comments and shares",
    },
    {
      id: "09", slug: "office-stories", kind: "story", tall: true, ground: "g-postcard", slides: S.stories,
      title: "Good, you?", theme: "Employees", format: "Story series · 6 frames, interactive",
      segment: "Employees, including the people at YourDOST's corporate clients",
      date: "Sun 22 Nov", time: "6:00 PM", day: 22,
      line: "Office mein \"How are you?\" ka sirf ek allowed answer hai: \"Good, you?\"",
      line2: "Yahan sach bol sakte ho.",
      en: "At the office there's only one allowed answer to \"How are you?\": \"Good, you?\" Here, you can tell the truth.",
      why: "Stories are where people answer honestly, because polls and sliders feel private. The answers become the next post, so the audience writes part of the content.",
      hook: "\"Good, you?\" in a giant speech bubble, the office's universal reflex. The story goes up at exactly 6 PM on a Sunday, when the next frame's poll (\"Sunday 6 PM feels like…\") is true for whoever's reading.",
      caption: "Stories don't carry a caption. Frame 1 does the job, and the link sticker on frame 6 points to yourdost.com.",
      mechanic: "Native poll, emoji slider, quiz and question-box stickers, the highest-engagement tools in Stories. The answers become the next post: \"1,240 of you answered. Here's what you said\" (with real numbers once they're in). Then Instagram content is built from the audience's own data.",
      human: "It asks people things they'd never be asked at work (\"Laptop ke bina last lunch kab kiya?\") and gives an honest answer a place to go. Frame 6 reminds them their company may already pay for YourDOST, which is how most people reach it.",
      measure: "Sticker taps, replies, link taps",
    },
    {
      id: "10", slug: "hr-leaders", kind: "carousel", ground: "g-night", slides: S.hr,
      title: "Exit form", theme: "HR leaders (B2B)", format: "Carousel · 7 slides + LinkedIn",
      segment: "HR leaders, CHROs and founders of 50–5,000-person companies: the people who buy EAPs",
      date: "Tue 24 Nov", time: "10:00 AM", day: 24,
      line: "Her exit form said \"better opportunity\".",
      line2: "The real reason was her green dot at 1:40 AM.",
      en: "",
      why: "HR leaders buy EAPs, and they've all filed an exit form they didn't quite believe. Data on one slide, a free tip on another, then the demo ask, in that order.",
      hook: "A real-looking exit-interview form with \"Better opportunity\" ticked, then the handwritten truth under it. Every HR leader has filed that form and suspected it wasn't the whole story.",
      caption: "Exit interviews are where the truth goes to be polite.\n\nIf you lead a team, slide 6 costs nothing and works tomorrow.\n\nIf you want a system behind it, YourDOST runs employee wellbeing and EAP programmes for 500+ organisations, with certified experts reachable in 30 seconds, in 20+ Indian languages. Book a demo, link in bio.\n\n#JoBolaNahi #EmployeeWellbeing #HR",
      mechanic: "Save, then share to HR peers, then cross-post on LinkedIn. Slide 6 is useful even to someone who never buys, which builds trust before the \"Book a demo\" ask. Tagging \"the leader who asks 'really'\" spreads it inside companies.",
      human: "It talks to HR leaders as people who've lost good people, not as a budget. The burnout signals (cameras off, \"sounds good 👍\", Monday sick leave) are observed behaviour, not jargon. The cost figure is sourced (Deloitte 2022) and YourDOST's numbers are labelled as theirs.",
      measure: "Saves, LinkedIn reach, demo requests",
    },
  ];

  function size(post) {
    return post.tall ? { w: 1080, h: 1920 } : { w: 1080, h: 1350 };
  }
  function frameCount(post) {
    return post.kind === "reel" ? 1 : post.slides.length;
  }
  // HTML for one frame: slide index i (carousel/static/story) or time t (reel)
  function frameHTML(post, i = 0, t = null, opts = {}) {
    const cls = `cv ${post.ground}${post.tall ? " tall" : ""}`;
    if (post.kind === "reel") {
      const tt = t === null ? post.reel.cover : t;
      return `<div class="${cls}">${reelFrame(post.reel, tt)}</div>`;
    }
    return `<div class="${cls}">${post.slides[i](opts)}</div>`;
  }

  root.JBN = { POSTS, frameHTML, frameCount, size };
})(typeof window !== "undefined" ? window : globalThis);
