/* Creator Intelligence Engine: prototype front end.
   Everything runs in the browser on the bundled sample (DATA). The scoring, forecast and plan logic below is the
   same logic described in "How it works", so what the viewer tunes is what the engine computes. */
(() => {
"use strict";
const D = DATA;
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"']/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const sum = (a, f = x => x) => a.reduce((s, x) => s + f(x), 0);
const median = a => { if (!a.length) return 0; const s = [...a].sort((x, y) => x - y); const m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
const sumMin = (a, b) => a.reduce((s, x, i) => s + Math.min(x, b[i]), 0);

/* ---------------------------------------------------------------- formatting (Indian conventions: ₹ lakh / crore) */
function fmtN(v) {
  v = +v || 0; const a = Math.abs(v);
  if (a < 1000) return Math.round(v).toLocaleString("en-IN");
  if (a < 1e5) return (v / 1e3).toFixed(a < 1e4 ? 1 : 0).replace(/\.0$/, "") + "K";
  if (a < 1e6) return (v / 1e3).toFixed(0) + "K";
  return (v / 1e6).toFixed(a < 1e7 ? 2 : 1).replace(/\.?0+$/, "") + "M";
}
function fmtINR(v, d) {
  v = +v || 0; const a = Math.abs(v);
  if (a < 1000) return "₹" + Math.round(v).toLocaleString("en-IN");
  if (a < 1e5) return "₹" + (v / 1e3).toFixed(d ?? (a < 1e4 ? 1 : 0)).replace(/\.0$/, "") + "K";
  if (a < 1e7) return "₹" + (v / 1e5).toFixed(d ?? (a < 1e6 ? 2 : 1)).replace(/\.?0+$/, "") + "L";
  return "₹" + (v / 1e7).toFixed(d ?? 2).replace(/\.?0+$/, "") + " Cr";
}
const fmtRs = (v, d = 2) => "₹" + (+v).toFixed(d);
const pc = (v, d = 0) => (v * 100).toFixed(d) + "%";
const pct = (v, d = 1) => (+v).toFixed(d) + "%";
const xf = (v, d = 1) => (+v).toFixed(d) + "×";
const initials = n => n.split(" ").map(p => p[0]).join("").slice(0, 2);
const brandMark = n => n.replace(/[^A-Za-z0-9&' ]/g, "").split(/\s+/).map(p => p[0]).join("").slice(0, 2).toUpperCase() || n.slice(0, 2);

/* ---------------------------------------------------------------- icons */
const I = {
  overview: '<rect x="3" y="3" width="7.5" height="7.5" rx="1.6"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.6"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.6"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.6"/>',
  match: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.3"/>',
  discover: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/>',
  verticals: '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12.5 9 5 9-5"/><path d="m3 17 9 5 9-5"/>',
  campaigns: '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
  how: '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9.5 2.5v3M14.5 2.5v3M9.5 18.5v3M14.5 18.5v3M2.5 9.5h3M2.5 14.5h3M18.5 9.5h3M18.5 14.5h3"/>',
  plan: '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
  moon: '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z"/>',
  sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  check: '<path d="m5 12.5 4.5 4.5L19 7"/>',
  x: '<path d="M6 6l12 12M18 6 6 18"/>',
  warn: '<path d="M12 4 2.5 20h19L12 4Z"/><path d="M12 10v4.5M12 17.5v.01"/>',
  block: '<circle cx="12" cy="12" r="9"/><path d="m5.6 5.6 12.8 12.8"/>',
  shield: '<path d="M12 3 4.5 6v6c0 4.5 3.2 7.8 7.5 9 4.3-1.2 7.5-4.5 7.5-9V6L12 3Z"/>',
  full: '<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>',
  copy: '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/>',
  chev: '<path d="m9 6 6 6-6 6"/>',
  spark: '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
};
const ic = (k, cls = "") => `<svg viewBox="0 0 24 24" class="${cls}" aria-hidden="true">${I[k]}</svg>`;

/* ---------------------------------------------------------------- indexes */
const C = D.creators, B = D.brands;
const CBY = Object.fromEntries(C.map(c => [c.id, c]));
const BBY = Object.fromEntries(B.map(b => [b.id, b]));
const TIER = Object.fromEntries(D.tiers.map(t => [t.key, t]));
const VERT = Object.fromEntries(D.verticals);
const NICHE = D.niches;
const ASSIST = 2.8;
const OPS = 3000; // ₹ per creator for contracting, briefing, QA and payments

const METRICS = { er: c => c.er, vtr: c => c.vtr, hook: c => c.hook, recall: c => c.recall, ctr: c => c.ctr, ss: c => c.saves + c.shares, sent: c => c.sent, trust: c => c.trust };
const PCT = {};
for (const t of D.tiers) {
  PCT[t.key] = {};
  const pool = C.filter(c => c.tier === t.key);
  for (const [m, f] of Object.entries(METRICS)) PCT[t.key][m] = pool.map(f).sort((a, b) => a - b);
}
function pctl(c, m) {
  const arr = PCT[c.tier][m], v = METRICS[m](c);
  let lo = 0, hi = arr.length;
  while (lo < hi) { const mid = (lo + hi) >> 1; if (arr[mid] <= v) lo = mid + 1; else hi = mid; }
  return lo / arr.length;
}
const topPct = p => Math.max(1, Math.round((1 - p) * 100));

/* ---------------------------------------------------------------- engine */
const DIMS = [
  ["aud", "Audience fit", "--s1"], ["cont", "Content affinity", "--s2"], ["cult", "Culture & language", "--s3"],
  ["perf", "Performance", "--s4"], ["auth", "Authenticity", "--s5"], ["safe", "Safety & compliance", "--s6"], ["cost", "Cost efficiency", "--s7"],
];
const OBJ = {
  awareness: { label: "Awareness", unit: "verified TG views", w: { aud: 22, cont: 15, cult: 14, perf: 15, auth: 14, safe: 10, cost: 10 } },
  consideration: { label: "Consideration", unit: "engagements", w: { aud: 20, cont: 18, cult: 10, perf: 20, auth: 14, safe: 8, cost: 10 } },
  conversion: { label: "Conversion", unit: "orders", w: { aud: 18, cont: 14, cult: 8, perf: 26, auth: 14, safe: 8, cost: 12 } },
};

function audFit(b, c) {
  const t = b.target, a = c.aud;
  const g = 1 - Math.abs(a.fem - t.fem), ag = sumMin(a.age, t.age), tr = sumMin(a.tiers, t.tiers), af = 1 - Math.abs(a.affl - t.affl);
  let raw = .3 * g + .3 * ag + .25 * tr + .15 * af;
  if (!b.markets.includes(c.market)) raw *= .35;
  return { raw, g, ag, tr, af, s: clamp((raw - .5) / .45, 0, 1) };
}
const affOf = (b, c) => (b.affinity[c.niche] ?? .05) * .75 + (b.affinity[c.niche2] ?? .05) * .25;
function cultFit(b, c) {
  let lang = 0, best = c.langs[0];
  for (const l of c.langs) { const w = b.langs[l] ?? 0; if (w > lang) { lang = w; best = l; } }
  const shared = c.codes.filter(x => b.codes.includes(x));
  return { lang, best, shared, s: .55 * lang + .45 * Math.min(1, shared.length / 2) };
}
function perfOf(c, obj) {
  if (obj === "awareness") return .35 * pctl(c, "vtr") + .25 * pctl(c, "hook") + .4 * pctl(c, "recall");
  if (obj === "consideration") return .45 * pctl(c, "er") + .35 * pctl(c, "ss") + .2 * pctl(c, "sent");
  return .55 * pctl(c, "ctr") + .25 * pctl(c, "trust") + .2 * pctl(c, "er");
}
function authOf(c) {
  let s = .6 * clamp((c.cred - 60) / 35, 0, 1) + .2 * c.cq / 100 + .2 * clamp(1 - c.spons / 80, 0, 1);
  if (c.fraud || (c.g90 > 25 && pctl(c, "er") < .3)) s -= .25;
  return clamp(s, 0, 1);
}
const safeOf = c => clamp(.6 * c.safety / 100 + .4 * c.asci / 100, 0, 1);

function predict(b, c, aud, aff) {
  const story = TIER[c.tier].story;
  let rv = c.views, sv = 0, cost, clicks;
  if (c.platform === "YouTube") { cost = c.rate.yt; clicks = rv * c.ctr * .55 / 100; }
  else { sv = c.followers * story * 2; cost = c.rate.reel + 2 * c.rate.story; clicks = (rv * c.ctr * .3 + sv * c.ctr * 1.3) / 100; }
  const mk = b.markets.includes(c.market) ? 1 : .2;
  clicks *= (.55 + .9 * aff) * mk;
  const orders = clicks * b.cvr * c.trust * (.7 + .6 * aff) * ASSIST;
  const views = rv + sv;
  const tgShare = clamp(Math.pow(aud.raw, 1.6), .05, .95);
  const tgViews = views * (c.cred / 100) * tgShare * mk;
  const eng = c.followers * c.er / 100 + sv * .03;
  const recall = c.recall * (.55 + .6 * aff) * (.7 + .3 * tgShare);
  const rev = orders * b.aov;
  return { views, rv, sv, tgViews, tgShare, eng, clicks, orders, rev, cost, recall, cpv: cost / Math.max(1, tgViews), cpe: cost / Math.max(1, eng), cpc: cost / Math.max(1, clicks), cpa: cost / Math.max(.01, orders), roas: rev / cost };
}
const confOf = c => c.camps >= 5 && c.lifts >= 1 ? ["High", .12] : c.camps >= 2 ? ["Medium", .22] : ["Low", .35];
const outcomeOf = (obj, p, b) => obj === "awareness" ? p.tgViews * (1 + p.recall / 25) : obj === "consideration" ? p.eng : (b.aov ? p.rev : p.clicks * 40);

function gatesOf(b, c) {
  const g = [];
  if (!b.markets.includes(c.market)) g.push({ k: "market", t: `Audience is mostly in the ${c.market}; ${b.name} runs this brief in ${b.markets.join(" & ")}` });
  if (c.cred < 72) g.push({ k: "fraud", t: `Only ${c.cred}% of followers look real and active (gate is 72%)` });
  if (c.safety < 55) g.push({ k: "safety", t: `Brand-safety score ${c.safety}: ${c.flags.join(", ").toLowerCase()}` });
  const conf = c.collabs.find(([n, d]) => b.competitors.includes(n) && d <= 60);
  if (conf) g.push({ k: "conflict", t: `Posted for ${conf[0]} ${conf[1]} days ago (60-day category exclusivity)` });
  if (b.compliance === "finance" && c.niche === "finance" && !(c.creds || "").startsWith("SEBI")) g.push({ k: "reg", t: "Gives investing content without SEBI registration. SEBI-regulated brands can't work with unregistered finfluencers" });
  if (b.compliance === "health" && c.niche === "health" && !c.creds) g.push({ k: "reg", t: "Makes health claims without a medical or nutrition qualification (ASCI Addendum II)" });
  return g;
}
const GATE_LABEL = { market: "Wrong market", fraud: "Fake or inactive audience", safety: "Brand-safety risk", conflict: "Competitor conflict", reg: "Regulatory eligibility" };
function flagsOf(b, c) {
  const f = [];
  if (c.spons > 45) f.push(`Ad fatigue: ${c.spons}% of recent posts are sponsored`);
  if (c.asci < 75) f.push(`Discloses #ad on only ${c.asci}% of paid posts. Brief on disclosure in the first line`);
  const near = c.collabs.find(([n, d]) => b.competitors.includes(n) && d > 60 && d <= 120);
  if (near) f.push(`Posted for ${near[0]} ${near[1]} days ago (outside the 60-day window)`);
  if (b.compliance === "finance" && c.niche !== "finance") f.push("Brand-scripted only: no return or advice claims (SEBI, ASCI)");
  if (b.compliance === "health" && c.niche !== "health" && !c.creds) f.push("Lifestyle use only: no efficacy or medical claims without credentials");
  if (c.g90 > 25 && !c.fraud) f.push(`Followers grew ${c.g90}% in 90 days. Check where the growth came from`);
  if (c.safety >= 55) for (const x of c.flags) f.push(x);
  if (confOf(c)[0] === "Low") f.push("Few tracked campaigns, so the forecast band is wide");
  return f;
}

const cache = new Map();
function scoreBrand(b, obj, w, boost = 0) {
  const key = `${b.id}|${obj}|${Object.values(w).join(",")}|${boost}`;
  if (cache.has(key)) return cache.get(key);
  const wsum = sum(Object.values(w)) || 1;
  const rows = C.map(c => {
    const aud = audFit(b, c), aff = affOf(b, c), cult = cultFit(b, c);
    const p = predict(b, c, aud, aff);
    return { c, aud, aff, cult, p, g: gatesOf(b, c), s: { aud: aud.s * 100, cont: aff * 100, cult: cult.s * 100, perf: perfOf(c, obj) * 100, auth: authOf(c) * 100, safe: safeOf(c) * 100, cost: 0 } };
  });
  // cost efficiency = percentile of outcome per rupee among creators who pass the gates
  const elig = rows.filter(r => !r.g.length);
  const eff = r => outcomeOf(obj, r.p, b) / r.p.cost;
  const sorted = elig.map(eff).sort((x, y) => x - y);
  for (const r of rows) {
    const v = eff(r); let lo = 0, hi = sorted.length;
    while (lo < hi) { const m = (lo + hi) >> 1; if (sorted[m] <= v) lo = m + 1; else hi = m; }
    r.s.cost = (lo / Math.max(1, sorted.length)) * 100;
    r.contrib = {};
    let t = 0;
    for (const [k] of DIMS) { r.contrib[k] = r.s[k] * w[k] / wsum; t += r.contrib[k]; }
    r.boost = boost && r.c.represent ? Math.min(boost, 5) : 0;
    r.total = t + r.boost;
    r.conf = confOf(r.c);
  }
  rows.sort((x, y) => y.total - x.total);
  const ranked = rows.filter(r => !r.g.length);
  ranked.forEach((r, i) => (r.rank = i + 1));
  const res = { rows, ranked, gated: rows.filter(r => r.g.length), b, obj, w };
  cache.set(key, res);
  return res;
}

function whyOf(r, obj, b) {
  const c = r.c, t = b.target, out = [];
  const tierLbl = TIER[c.tier].label.toLowerCase();
  const txt = {
    aud: () => `Audience matches the brief: <b>${pc(c.aud.fem)} women</b> (target ${pc(t.fem)}), ${pc(r.aud.ag)} age overlap, ${pc(r.aud.tr)} city-tier overlap`,
    cont: () => `<b>${esc(NICHE[c.niche])}</b> is a ${r.aff >= .85 ? "core" : r.aff >= .6 ? "strong" : "adjacent"} category for ${esc(b.name)}, with ${esc(NICHE[c.niche2]).toLowerCase()} as a second pillar`,
    cult: () => `Creates in <b>${esc(c.langs.join(" + "))}</b>${r.cult.lang >= .9 ? `, ${esc(b.name)}'s lead language` : ""}${r.cult.shared.length ? `; shares the ${r.cult.shared.map(esc).join(" and ")} codes` : ""}`,
    perf: () => obj === "awareness" ? `Viewers watch <b>${pct(c.vtr, 0)} of each video</b>, top ${topPct(pctl(c, "vtr"))}% of ${tierLbl} creators; past recall lift +${c.recall} pts`
      : obj === "consideration" ? `Engagement rate <b>${pct(c.er, 1)}</b>, top ${topPct(pctl(c, "er"))}% of ${tierLbl} creators; ${pct(c.saves + c.shares, 1)} of viewers save or share`
      : `Link CTR <b>${pct(c.ctr, 2)}</b>, top ${topPct(pctl(c, "ctr"))}% of ${tierLbl} creators; trust index ${c.trust.toFixed(2)}`,
    auth: () => `<b>${pct(c.cred, 0)} of followers look real</b> and active; ${c.spons}% of recent posts are sponsored`,
    safe: () => `Safety score <b>${c.safety}</b>; discloses #ad on ${c.asci}% of paid posts${c.creds ? `; ${esc(c.creds)}` : ""}`,
    cost: () => obj === "awareness" ? `<b>${fmtRs(r.p.cpv)} per verified TG view</b> for 1 reel and 2 stories (${fmtINR(r.p.cost)})`
      : obj === "consideration" ? `<b>${fmtRs(r.p.cpe)} per engagement</b> (${fmtINR(r.p.cost)} for the bundle)`
      : b.aov ? `Forecast <b>${xf(r.p.roas)} ROAS</b> on ${fmtINR(r.p.cost)}, about ${fmtN(r.p.orders)} orders` : `<b>${fmtRs(r.p.cpc)} per click</b>`,
  };
  const order = Object.entries(r.contrib).sort((a, b2) => b2[1] - a[1]).map(x => x[0]);
  for (const k of order) out.push({ k, html: txt[k](), strong: r.s[k] >= 60 });
  return out;
}

/* ---------------------------------------------------------------- plan builder */
function aggregate(list, b) {
  const a = { n: list.length, cost: 0, views: 0, tg: 0, eng: 0, clicks: 0, orders: 0, rev: 0, recallW: 0, fakeAud: 0, aud: 0, gated: 0, rep: 0, repCost: 0, tiers: {}, flags: 0, band: 0 };
  let keep = 1;
  for (const r of list) {
    const p = r.p;
    a.cost += p.cost; a.views += p.views; a.tg += p.tgViews; a.eng += p.eng; a.clicks += p.clicks; a.orders += p.orders; a.rev += p.rev;
    a.recallW += p.recall * p.tgViews; a.aud += r.c.followers; a.fakeAud += r.c.followers * (1 - r.c.cred / 100);
    if (r.g.length) a.gated++;
    if (r.c.represent) { a.rep++; a.repCost += p.cost; }
    a.tiers[r.c.tier] = (a.tiers[r.c.tier] || 0) + p.cost;
    a.band += p.cost * r.conf[1];
    keep *= 1 - Math.min(.9, p.tgViews * .62 / (b.pool * 1e6));
  }
  a.recall = a.tg ? a.recallW / a.tg : 0;
  a.fake = a.aud ? a.fakeAud / a.aud : 0;
  a.reach = b.pool * 1e6 * (1 - keep);
  a.band = a.cost ? a.band / a.cost : 0;
  a.roas = a.cost ? a.rev / a.cost : 0;
  return a;
}
function buildPlan(res, budget) {
  const { ranked, obj, b } = res;
  const cand = ranked.filter(r => r.total >= 50).map(r => ({ r, k: Math.pow(r.total / 100, 2.2) * Math.pow(r.c.cred / 100, 6) * outcomeOf(obj, r.p, b) / (r.p.cost + OPS) })).sort((x, y) => y.k - x.k);
  const pick = [], cap = { mega: 1, macro: 3 }, cnt = {};
  let spent = 0;
  for (const { r } of cand) {
    const t = r.c.tier;
    if (cap[t] !== undefined && (cnt[t] || 0) >= cap[t]) continue;
    if (r.p.cost > budget * .25 || spent + r.p.cost > budget) continue;
    pick.push(r); spent += r.p.cost; cnt[t] = (cnt[t] || 0) + 1;
    if (pick.length >= 80) break;
  }
  return { list: pick, agg: aggregate(pick, b) };
}
function vanityPlan(res, budget) {
  const pool = res.rows.filter(r => res.b.markets.includes(r.c.market)).sort((x, y) => y.c.followers - x.c.followers);
  const pick = []; let spent = 0;
  for (const r of pool) { if (spent + r.p.cost > budget) continue; pick.push(r); spent += r.p.cost; if (spent > budget * .985) break; }
  return { list: pick, agg: aggregate(pick, res.b) };
}

/* ---------------------------------------------------------------- state */
const store = {
  get(k, d) { try { const v = localStorage.getItem("cie." + k); return v == null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem("cie." + k, JSON.stringify(v)); } catch { /* storage unavailable */ } },
};
const S = {
  view: "overview",
  brand: store.get("brand", "olay"),
  obj: null, w: null, boost: 0,
  budget: null,
  tiers: new Set(), platforms: new Set(),
  centre: "list",
  drawer: null,
  vertical: store.get("vertical", "beauty"),
  camp: store.get("camp", "C1"),
  campMetric: "views",
  query: "",
  dSort: ["fit", -1], dPage: 0,
  howObj: "conversion",
  live: { views: 0, clicks: 0, orders: 0, rev: 0 },
};
if (!BBY[S.brand]) S.brand = "olay";
function brandState() {
  const b = BBY[S.brand];
  if (!S.obj) S.obj = b.objective;
  if (!S.w) S.w = { ...OBJ[S.obj].w };
  if (S.budget == null) S.budget = b.budget;
  return b;
}
function setBrand(id) { S.brand = id; S.obj = null; S.w = null; S.budget = null; store.set("brand", id); }

/* ---------------------------------------------------------------- tooltip */
const tip = document.createElement("div");
tip.className = "tip"; tip.setAttribute("role", "tooltip");
document.body.appendChild(tip);
function showTip(html, x, y) {
  tip.innerHTML = html; tip.classList.add("on");
  const r = tip.getBoundingClientRect();
  let tx = x + 14, ty = y + 14;
  if (tx + r.width > innerWidth - 8) tx = x - r.width - 14;
  if (ty + r.height > innerHeight - 8) ty = y - r.height - 14;
  tip.style.left = Math.max(8, tx) + "px"; tip.style.top = Math.max(8, ty) + "px";
}
const hideTip = () => tip.classList.remove("on");
document.addEventListener("pointerover", e => {
  const t = e.target.closest("[data-tip]");
  if (t) showTip(t.dataset.tip, e.clientX, e.clientY);
});
document.addEventListener("pointermove", e => {
  const t = e.target.closest("[data-tip]");
  if (t) showTip(t.dataset.tip, e.clientX, e.clientY); else if (!e.target.closest("[data-chart]")) hideTip();
});
document.addEventListener("pointerleave", hideTip);

/* ---------------------------------------------------------------- charts */
const cssv = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
function niceMax(v) { if (v <= 0) return 1; const p = Math.pow(10, Math.floor(Math.log10(v))); const f = v / p; return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * p; }

function lineChart(el, { labels, series, yfmt = fmtN, height = 230, marker }) {
  const W = Math.max(320, el.clientWidth || 600), H = height, m = { l: 48, r: 16, t: 14, b: 26 };
  const iw = W - m.l - m.r, ih = H - m.t - m.b;
  const ymax = niceMax(Math.max(1, ...series.flatMap(s => s.vals.filter(v => v != null))) * 1.08);
  const x = i => m.l + (labels.length === 1 ? iw / 2 : i * iw / (labels.length - 1));
  const y = v => m.t + ih - v / ymax * ih;
  let g = "";
  for (let k = 0; k <= 4; k++) { const v = ymax * k / 4; g += `<line class="${k ? "grid-l" : "base-l"}" x1="${m.l}" x2="${W - m.r}" y1="${y(v)}" y2="${y(v)}"/><text x="${m.l - 8}" y="${y(v) + 4}" text-anchor="end">${yfmt(v)}</text>`; }
  const step = Math.ceil(labels.length / Math.max(2, Math.floor(iw / 56)));
  labels.forEach((l, i) => { if (i % step === 0 || i === labels.length - 1) g += `<text x="${x(i)}" y="${H - 6}" text-anchor="middle">${esc(l)}</text>`; });
  if (marker != null) g += `<line x1="${x(marker)}" x2="${x(marker)}" y1="${m.t}" y2="${m.t + ih}" stroke="${cssv("--line-2")}" stroke-width="1"/><text x="${x(marker) + 6}" y="${m.t + 10}" class="lbl-ink2">Today</text>`;
  for (const s of series) {
    const col = cssv(s.color);
    const pts = s.vals.map((v, i) => v == null ? null : [x(i), y(v)]);
    const seg = (from, to) => pts.slice(from, to).filter(Boolean).map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + "," + p[1].toFixed(1)).join("");
    const split = s.dashFrom ?? pts.length;
    const solid = seg(0, split), dash = s.dashFrom != null ? seg(Math.max(0, split - 1), pts.length) : "";
    if (s.area && solid) { const sp = pts.slice(0, split).filter(Boolean); g += `<path d="${solid}L${sp[sp.length - 1][0]},${y(0)}L${sp[0][0]},${y(0)}Z" fill="${col}" opacity=".1"/>`; }
    g += `<path d="${solid}" fill="none" stroke="${col}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>`;
    if (dash) g += `<path d="${dash}" fill="none" stroke="${col}" stroke-width="2" stroke-dasharray="4 4" opacity=".75"/>`;
    const last = pts.slice(0, split).filter(Boolean).pop();
    if (last) g += `<circle cx="${last[0]}" cy="${last[1]}" r="4.5" fill="${col}" stroke="${cssv("--surface")}" stroke-width="2"/>`;
  }
  g += `<line class="xh" x1="0" x2="0" y1="${m.t}" y2="${m.t + ih}" stroke="${cssv("--ink-2")}" stroke-width="1" opacity="0"/><rect class="hit" x="${m.l}" y="${m.t}" width="${iw}" height="${ih}" fill="transparent"/>`;
  el.innerHTML = `<svg class="chart" data-chart viewBox="0 0 ${W} ${H}" width="100%" height="${H}" role="img" aria-label="${esc(series.map(s => s.name).join(", "))} by day">${g}</svg>`;
  const svg = el.firstChild, xh = $(".xh", svg);
  $(".hit", svg).addEventListener("pointermove", e => {
    const r = svg.getBoundingClientRect(); const px = (e.clientX - r.left) * W / r.width;
    const i = clamp(Math.round((px - m.l) / iw * (labels.length - 1)), 0, labels.length - 1);
    xh.setAttribute("x1", x(i)); xh.setAttribute("x2", x(i)); xh.setAttribute("opacity", ".35");
    showTip(`<b>${esc(labels[i])}</b><br>` + series.map(s => s.vals[i] == null ? "" : `<span class="tk" style="background:${cssv(s.color)}"></span>${esc(s.name)}${s.dashFrom != null && i >= s.dashFrom ? " (forecast)" : ""}: <b>${yfmt(s.vals[i])}</b>`).join("<br>"), e.clientX, e.clientY);
  });
  $(".hit", svg).addEventListener("pointerleave", () => { xh.setAttribute("opacity", "0"); hideTip(); });
}

function scatter(el, { pts, xfmt, yfmt, xlab, ylab, height = 300, ref }) {
  const W = Math.max(320, el.clientWidth || 600), H = height, m = { l: 56, r: 18, t: 14, b: 40 };
  const iw = W - m.l - m.r, ih = H - m.t - m.b;
  const xs = pts.map(p => p.x), ys = pts.map(p => p.y).filter(v => v > 0);
  const lx0 = Math.log10(Math.min(...xs) * .8), lx1 = Math.log10(Math.max(...xs) * 1.2);
  const ly0 = Math.log10(Math.max(1, Math.min(...ys)) * .8), ly1 = Math.log10(Math.max(...ys) * 1.25);
  const X = v => m.l + (Math.log10(v) - lx0) / (lx1 - lx0) * iw;
  const Y = v => m.t + ih - (Math.log10(Math.max(v, Math.pow(10, ly0))) - ly0) / (ly1 - ly0) * ih;
  let g = "";
  const tick = (a, b) => { const out = []; for (let e = Math.floor(a); e <= Math.ceil(b); e++) for (const k of [1, 3]) { const v = k * Math.pow(10, e); if (Math.log10(v) >= a && Math.log10(v) <= b) out.push(v); } return out; };
  for (const v of tick(ly0, ly1)) g += `<line class="grid-l" x1="${m.l}" x2="${W - m.r}" y1="${Y(v)}" y2="${Y(v)}"/><text x="${m.l - 8}" y="${Y(v) + 4}" text-anchor="end">${yfmt(v)}</text>`;
  for (const v of tick(lx0, lx1)) g += `<text x="${X(v)}" y="${H - 22}" text-anchor="middle">${xfmt(v)}</text>`;
  g += `<line class="base-l" x1="${m.l}" x2="${W - m.r}" y1="${m.t + ih}" y2="${m.t + ih}"/>`;
  g += `<text x="${m.l + iw / 2}" y="${H - 4}" text-anchor="middle" class="lbl-ink2">${esc(xlab)}</text><text transform="translate(12 ${m.t + ih / 2}) rotate(-90)" text-anchor="middle" class="lbl-ink2">${esc(ylab)}</text>`;
  if (ref) { // iso-efficiency line: y = ref · x
    const xa = Math.pow(10, lx0), xb = Math.pow(10, lx1);
    const ya = clamp(ref * xa, Math.pow(10, ly0), Math.pow(10, ly1)), yb = clamp(ref * xb, Math.pow(10, ly0), Math.pow(10, ly1));
    const xa2 = ya / ref, xb2 = yb / ref;
    g += `<line x1="${X(xa2)}" y1="${Y(ya)}" x2="${X(xb2)}" y2="${Y(yb)}" stroke="${cssv("--ink-2")}" stroke-dasharray="5 4" opacity=".55"/><text x="${X(xb2) - 6}" y="${Y(yb) + 16}" text-anchor="end" class="lbl-ink2">median outcome per ₹</text>`;
  }
  const surface = cssv("--surface");
  const order = { base: 0, vanity: 1, plan: 2 };
  for (const p of [...pts].sort((a, b) => order[a.k] - order[b.k])) {
    const cx = X(p.x).toFixed(1), cy = Y(p.y).toFixed(1);
    if (p.k === "plan") g += `<circle cx="${cx}" cy="${cy}" r="5" fill="${cssv("--accent")}" stroke="${surface}" stroke-width="2" data-tip="${esc(p.tip)}"/>`;
    else if (p.k === "vanity") g += `<circle cx="${cx}" cy="${cy}" r="5" fill="${surface}" stroke="${cssv("--ink-2")}" stroke-width="1.6" data-tip="${esc(p.tip)}"/>`;
    else g += `<circle cx="${cx}" cy="${cy}" r="4" fill="${cssv("--neutral-mark")}" opacity=".7" stroke="${surface}" stroke-width="1" data-tip="${esc(p.tip)}"/>`;
  }
  el.innerHTML = `<svg class="chart" viewBox="0 0 ${W} ${H}" width="100%" height="${H}" role="img" aria-label="Cost versus forecast outcome for each eligible creator">${g}</svg>`;
}

function sparkline(vals, w = 120, h = 34, col = "--ink-2") {
  const mx = Math.max(...vals), mn = Math.min(...vals), r = mx - mn || 1;
  const pts = vals.map((v, i) => [i * (w - 6) / (vals.length - 1) + 3, h - 4 - (v - mn) / r * (h - 8)]);
  const d = pts.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + "," + p[1].toFixed(1)).join("");
  const last = pts[pts.length - 1];
  return `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" aria-hidden="true"><path d="${d}L${last[0]},${h - 2}L3,${h - 2}Z" fill="${cssv(col)}" opacity=".1"/><path d="${d}" fill="none" stroke="${cssv(col)}" stroke-width="2" stroke-linejoin="round"/><circle cx="${last[0]}" cy="${last[1]}" r="3.5" fill="${cssv(col)}" stroke="${cssv("--surface")}" stroke-width="2"/></svg>`;
}

function fitBar(r, h = 8) {
  return `<div class="fitbar" style="height:${h}px" role="img" aria-label="Fit ${r.total.toFixed(0)} of 100">${DIMS.map(([k, l, col]) => `<span style="width:${r.contrib[k]}%;background:var(${col})" data-tip="<b>${l}</b>: ${r.s[k].toFixed(0)}/100 × weight ${S.w ? S.w[k] : ""} → ${r.contrib[k].toFixed(1)} pts"></span>`).join("")}${r.boost ? `<span style="width:${r.boost}%;background:var(--accent)" data-tip="<b>Represent boost</b>: +${r.boost} (capped at 5, disclosed to brand)"></span>` : ""}<span class="rest" style="flex:1"></span></div>`;
}
const legendDims = () => `<div class="legend">${DIMS.map(([, l, col]) => `<span><i style="background:var(${col})"></i>${l}</span>`).join("")}</div>`;

function avatar(c, lg) { return `<div class="av${lg ? " lg" : ""}${c.represent ? " rep" : ""}" ${c.represent ? 'title="Chtrbox Represent roster"' : ""}>${esc(initials(c.name))}</div>`; }
function who(c, extra = "") {
  return `<div class="who">${avatar(c)}<div class="who-t"><div class="who-n">${esc(c.name)} <span class="muted mono" style="font-weight:400;font-size:11px">${c.id}</span></div><div class="who-m">${esc(NICHE[c.niche])} · ${TIER[c.tier].label} ${fmtN(c.followers)} · ${esc(c.city)} · ${esc(c.platform)}${extra}</div></div></div>`;
}

/* ---------------------------------------------------------------- views */
const VIEWS = [
  ["overview", "Overview", "The engine at a glance", "1"],
  ["match", "Brand Match", "Rank creators for a brand brief", "2"],
  ["discover", "Discovery", "Search the creator graph", "3"],
  ["verticals", "Vertical Lens", "What works, category by category", "4"],
  ["campaigns", "Campaigns & ROI", "Live tracking and verified ROI", "5"],
  ["how", "How it works", "Data, scoring and the learning loop", "6"],
  ["plan", "Rollout plan", "30 · 60 · 90 days and beyond", "7"],
];
const view = () => $("#view");

function campStats(cp) {
  const b = BBY[cp.brand], t = cp.totals;
  const live = cp.live ? S.live : { views: 0, clicks: 0, orders: 0, rev: 0 };
  const rev = t.rev + live.rev;
  const verified = rev * (1 - cp.returns), incr = verified * cp.inc_share;
  const emv = t.rep * 1.4 + t.eng * 28;
  return { b, t, views: t.api + live.views, clicks: t.clicks + live.clicks, orders: t.orders + live.orders, rev, verified, incr,
    iroas: incr / Math.max(1, t.cost), groas: rev / Math.max(1, t.cost), ltv: incr * cp.ltv / Math.max(1, t.cost), emv, claimed: emv / Math.max(1, t.cost),
    recall: cp.lift[0][2] - cp.lift[0][1] };
}

function vOverview() {
  const camps = D.campaigns.map(cp => ({ cp, ...campStats(cp) }));
  const conv = camps.filter(x => x.b.objective !== "awareness");
  const incr = sum(camps, x => x.incr), cIncr = sum(conv, x => x.incr), cSpend = sum(conv, x => x.t.cost), cLtv = sum(conv, x => x.incr * x.cp.ltv);
  const gatedShare = median(B.map(b => scoreBrand(b, b.objective, OBJ[b.objective].w).gated.length / C.length));
  const recall = sum(camps, x => x.recall) / camps.length;
  const clients = B.filter(b => b.status === "Reported client").length;
  return `
  <section class="hero">
    <div class="hero-main">
      <div class="eyebrow">Prototype for Chtrbox · simulated data</div>
      <h2>Pick creators on proof,<br>not on <em>follower counts</em>.</h2>
      <p class="lede">The Creator Intelligence Engine answers the three questions every brand asks, using 76 data points per creator and the tracking Chtrbox already runs.</p>
      <div class="qs">
        <button class="q" data-go="match"><span class="qn">01 · Brand Match</span><span class="qt">Who should we work with?</span><span class="qa">Ranks <b>${C.length}</b> creators for <b>${B.length}</b> brands, with the reason for every score.</span></button>
        <button class="q" data-go="match" data-centre="map"><span class="qn">02 · Forecast</span><span class="qt">What will it deliver?</span><span class="qa">Views, clicks, orders and recall per creator, with a confidence band.</span></button>
        <button class="q" data-go="campaigns"><span class="qn">03 · Verified ROI</span><span class="qt">Did it work?</span><span class="qa"><b>${fmtINR(incr)}</b> incremental revenue across ${camps.length} campaigns, net of returns and organic sales.</span></button>
      </div>
    </div>
    <div class="panel ctx">
      <div class="panel-h"><h3>Why now, from Chtrbox's public numbers</h3></div>
      <div class="panel-b">
        <div class="fact"><b>₹84.2 Cr</b><span>FY26 revenue, up 42.5%, but EBITDA margin fell from 20.5% to 17.0%. Services are scaling linearly.<cite>Exchange filing coverage, May 2026</cite></span></div>
        <div class="fact"><b>39/36/25</b><span>Revenue mix: Represent, Brand Solutions and ChtrSocial (%). The engine feeds the first two directly.<cite>FY26 investor presentation coverage</cite></span></div>
        <div class="fact"><b>3L+</b><span>Creators in the network. Matching that pool by hand is what eats strategist hours.<cite>YourStory, May 2026</cite></span></div>
        <div class="fact"><b>₹42.9 Cr</b><span>Raised at the Oct 2025 SME IPO (52× subscribed). Management has said proceeds go to tech, creator intelligence and new geographies.<cite>IPO coverage; Social Samosa interview</cite></span></div>
      </div>
    </div>
  </section>

  <div class="tiles">
    <div class="tile"><div class="lbl">Creators indexed</div><div class="val">${C.length}<small>sample</small></div><div class="note">The production graph covers 3L+</div></div>
    <div class="tile"><div class="lbl">Data points per creator</div><div class="val">76</div><div class="note">8 families, see How it works</div></div>
    <div class="tile"><div class="lbl">Brands profiled</div><div class="val">${B.length}</div><div class="note">${clients} reported clients · ${B.length - clients} prospects · 9 verticals</div></div>
    <div class="tile"><div class="lbl">Gated before ranking</div><div class="val">${pc(gatedShare)}</div><div class="note">Median per brief: fraud, safety, conflicts, regulation</div></div>
    <div class="tile"><div class="lbl">Incremental ROAS</div><div class="val">${xf(cIncr / cSpend, 2)}</div><div class="note">${xf(cLtv / cSpend, 2)} on 12-month value · ${conv.length} conversion campaigns</div></div>
    <div class="tile"><div class="lbl">Ad recall lift</div><div class="val">+${recall.toFixed(1)}<small>pts</small></div><div class="note">Exposed vs control, mean of 6 studies</div></div>
  </div>

  <div class="grid g2">
    <div class="panel">
      <div class="panel-h"><h3>What brands are told vs what is true</h3><span class="sub">Views per campaign, as a share of what creators report</span></div>
      <div class="panel-b">
        <div class="legend" style="margin-bottom:12px">${["Creator-reported", "API-verified", "Unique and real", "In target group"].map((l, i) => `<span><i style="background:${["var(--neutral-mark)", "color-mix(in oklab, var(--accent) 45%, var(--surface))", "color-mix(in oklab, var(--accent) 70%, var(--surface))", "var(--accent)"][i]}"></i>${l}</span>`).join("")}</div>
        <div class="ladder">${camps.map(x => {
          const t = x.t, steps = [t.rep, t.api, t.real, t.tg];
          const cols = ["var(--neutral-mark)", "color-mix(in oklab, var(--accent) 45%, var(--surface))", "color-mix(in oklab, var(--accent) 70%, var(--surface))", "var(--accent)"];
          return `<div class="lad" style="grid-template-columns:150px 1fr 64px"><div class="k">${esc(x.b.name)}<small>${esc(x.cp.title.split(" · ")[0])}</small></div><div style="display:flex;flex-direction:column;gap:2px">${steps.map((v, i) => `<div class="t" style="height:6px;background:transparent"><i style="width:${v / t.rep * 100}%;background:${cols[i]}" data-tip="<b>${["Creator-reported", "API-verified", "Unique and real", "In target group"][i]}</b>: ${fmtN(v)} (${pc(v / t.rep)})"></i></div>`).join("")}</div><div class="v">${pc(t.tg / t.rep)}</div></div>`;
        }).join("")}</div>
        <p class="view-foot" style="margin-top:12px">Right column: share of reported views that were real people in the brand's target group. Bot filtering uses each creator's audience-authenticity score.</p>
      </div>
    </div>
    <div class="panel">
      <div class="panel-h"><h3>Claimed ROI vs verified ROI</h3><span class="sub">Return per ₹1 spent, conversion campaigns</span></div>
      <div class="panel-b">
        <div class="legend" style="margin-bottom:6px"><span><i style="background:var(--surface);box-shadow:inset 0 0 0 1.6px var(--ink-2)"></i>Claimed (EMV)</span><span><i style="background:var(--s7)"></i>Attributed ROAS</span><span><i style="background:var(--accent)"></i>Incremental ROAS</span></div>
        <div id="roiDots"></div>
        <p class="view-foot">EMV prices every view and like at an industry rate card, which is how vanity ROI is usually quoted. Incremental ROAS keeps only revenue a holdout test proves would not have happened anyway.</p>
      </div>
    </div>
  </div>

  <div class="panel">
    <div class="panel-h"><h3>How the engine works</h3><span class="sub">Six stages, from raw signals to a model that improves after every campaign</span></div>
    <div class="pipeline" style="margin-top:12px;border-top:1px solid var(--line)">
      ${[
        ["Ingest", "Creator APIs with consent, campaign history, Represent roster, brand outcome feeds.", "Instagram Graph · YouTube Analytics · UTMs · pixels"],
        ["Understand", "AI reads captions, audio and frames in 12 languages to tag niche, cultural codes and brand-safety risk.", "Vision + language models · Hinglish aware"],
        ["Match", "Seven-part fit score per brand brief, after hard gates for fraud, safety, conflicts and regulation.", "Explainable · weights tunable per objective"],
        ["Forecast", "Views, TG reach, clicks, orders, recall and cost per outcome, with a confidence band.", "Calibrated on past campaigns"],
        ["Verify", "Plugs into Chtrbox's real-time tracking. Dedupe, bot-filter, net out returns, run holdouts.", "Already in place: tracking & attribution"],
        ["Learn", "Every campaign's forecast error retrains the model. Strategist overrides become training labels.", "MAPE 16–20% on the sample"],
      ].map(([h, p, s], i) => `<div class="pipe"><div class="n">0${i + 1}</div><h4>${h}</h4><p>${p}</p><div class="src">${s}</div></div>`).join("")}
    </div>
  </div>
  <p class="view-foot">Simulated data. Creator identities are synthetic personas. Brand names are publicly reported Chtrbox clients or labelled prospects. Every metric shown for them is modelled, not real campaign data. Public company figures are cited in the plan.</p>`;
}
function afterOverview() {
  const el = $("#roiDots"); if (!el) return;
  const rows = D.campaigns.map(cp => ({ cp, ...campStats(cp) })).filter(x => x.b.objective !== "awareness");
  const W = Math.max(320, el.clientWidth), rowH = 40, H = rows.length * rowH + 52, m = { l: 112, r: 20 }, top = 26;
  const xmax = niceMax(Math.max(...rows.map(r => r.claimed)) * 1.05);
  const X = v => m.l + v / xmax * (W - m.l - m.r);
  let g = "";
  for (let k = 0; k <= 4; k++) { const v = xmax * k / 4; g += `<line class="${k ? "grid-l" : "base-l"}" x1="${X(v)}" x2="${X(v)}" y1="${top - 6}" y2="${H - 26}"/><text x="${X(v)}" y="${H - 8}" text-anchor="middle">${v.toFixed(v < 10 ? 1 : 0)}×</text>`; }
  g += `<line x1="${X(1)}" x2="${X(1)}" y1="${top - 6}" y2="${H - 26}" stroke="${cssv("--ink-2")}" stroke-dasharray="3 3" opacity=".6"/><text x="${X(1)}" y="${top - 12}" text-anchor="middle" class="lbl-ink2">1× break-even</text>`;
  rows.forEach((r, i) => {
    const y = top + 14 + i * rowH;
    g += `<text x="${m.l - 12}" y="${y + 4}" text-anchor="end" class="lbl-ink2">${esc(r.b.name)}</text>`;
    g += `<line x1="${X(r.iroas)}" x2="${X(r.claimed)}" y1="${y}" y2="${y}" stroke="${cssv("--line-2")}" stroke-width="2"/>`;
    g += `<circle cx="${X(r.claimed)}" cy="${y}" r="5.5" fill="${cssv("--surface")}" stroke="${cssv("--ink-2")}" stroke-width="1.6" data-tip="<b>${esc(r.b.name)}</b><br>Claimed (EMV): ${xf(r.claimed)}"/>`;
    g += `<circle cx="${X(r.groas)}" cy="${y}" r="5.5" fill="${cssv("--s7")}" stroke="${cssv("--surface")}" stroke-width="2" data-tip="<b>${esc(r.b.name)}</b><br>Attributed ROAS: ${xf(r.groas, 2)}"/>`;
    g += `<circle cx="${X(r.iroas)}" cy="${y}" r="5.5" fill="${cssv("--accent")}" stroke="${cssv("--surface")}" stroke-width="2" data-tip="<b>${esc(r.b.name)}</b><br>Incremental ROAS: ${xf(r.iroas, 2)}<br>With 12-month LTV: ${xf(r.ltv, 2)}"/>`;
    g += `<text x="${X(r.iroas)}" y="${y - 10}" text-anchor="middle" class="lbl-strong" style="font-size:11px">${xf(r.iroas, 2)}</text>`;
  });
  el.innerHTML = `<svg class="chart" viewBox="0 0 ${W} ${H}" width="100%" height="${H}" role="img" aria-label="Claimed, attributed and incremental ROAS by campaign">${g}</svg>`;
}

/* ---------- brand match */
function brandOptions(sel) {
  return D.verticals.map(([vk, vl]) => `<optgroup label="${esc(vl)}">${B.filter(b => b.vertical === vk).map(b => `<option value="${b.id}" ${b.id === sel ? "selected" : ""}>${esc(b.name)}${b.status === "Prospect" ? " (prospect)" : ""}</option>`).join("")}</optgroup>`).join("");
}
function matchRes() {
  brandState();
  const res = scoreBrand(BBY[S.brand], S.obj, S.w, S.boost);
  const filt = r => (!S.tiers.size || S.tiers.has(r.c.tier)) && (!S.platforms.size || S.platforms.has(r.c.platform));
  return { res, list: res.ranked.filter(filt) };
}
function vMatch() {
  const b = brandState();
  const { res, list } = matchRes();
  const plan = buildPlan(res, S.budget * 1e5);
  const t = b.target;
  const ageL = ["13–17", "18–24", "25–34", "35–44", "45+"];
  const gcount = {}; for (const r of res.gated) for (const g of r.g) gcount[g.k] = (gcount[g.k] || 0) + 1;
  const comp = b.compliance === "finance" ? "SEBI: only registered creators may discuss returns or products. Others stay on brand-scripted app experience." : b.compliance === "health" ? "ASCI Addendum II: technical health claims need a qualified creator. No cure or guaranteed-result language." : "Standard ASCI disclosure: #ad or #collab in the first line of every paid post.";
  return `
  <div class="match">
    <aside class="dna">
      <div class="panel"><div class="panel-b" style="display:flex;flex-direction:column;gap:14px">
        <div class="brand-pick"><label class="eyebrow" for="brandSel">Brand brief</label><select id="brandSel" class="sel">${brandOptions(b.id)}</select></div>
        <div class="brand-head"><div class="blogo">${esc(brandMark(b.name))}</div><div><h2>${esc(b.name)}</h2><div class="muted" style="font-size:12.5px">${esc(b.parent)} · ${esc(b.sub)}</div></div></div>
        <div class="tags"><span class="tag ${b.status === "Prospect" ? "outline" : "accent"}">${esc(b.status)}</span><span class="tag">${esc(VERT[b.vertical])}</span><span class="tag">${esc(b.moment)}</span></div>
        <p class="brief">${esc(b.brief)}</p>
        <hr class="hr">
        <div><div class="mini-h">Target audience</div>
          <div class="bars-mini">
            <div class="bm"><span>Women</span><div class="t"><i style="width:${t.fem * 100}%"></i></div><span class="v">${pc(t.fem)}</span></div>
            ${t.age.map((v, i) => `<div class="bm"><span>${ageL[i]}</span><div class="t"><i style="width:${v * 100}%"></i></div><span class="v">${pc(v)}</span></div>`).join("")}
            ${t.tiers.map((v, i) => `<div class="bm"><span>Tier ${i + 1}</span><div class="t"><i style="width:${v * 100}%"></i></div><span class="v">${pc(v)}</span></div>`).join("")}
          </div></div>
        <div><div class="mini-h">Languages, by priority</div><div class="tags">${Object.entries(b.langs).sort((x, y) => y[1] - x[1]).slice(0, 6).map(([l]) => `<span class="tag">${esc(l)}</span>`).join("")}</div></div>
        <div><div class="mini-h">Cultural codes</div><div class="tags">${b.codes.map(x => `<span class="tag">${esc(x)}</span>`).join("")}</div></div>
        <div><div class="mini-h">KPIs that matter</div><div class="tags">${b.kpis.map(x => `<span class="tag outline">${esc(x)}</span>`).join("")}</div></div>
        <div><div class="mini-h">Exclusivity · 60 days</div><p class="ink2" style="font-size:12.5px">${b.competitors.map(esc).join(", ")}</p></div>
        <div><div class="mini-h">Compliance</div><p class="ink2" style="font-size:12.5px">${esc(comp)}</p></div>
      </div></div>
    </aside>

    <section style="display:flex;flex-direction:column;gap:14px;min-width:0">
      <div class="controls">
        <div class="seg" role="group" aria-label="Campaign objective">${Object.entries(OBJ).map(([k, o]) => `<button data-obj="${k}" aria-pressed="${S.obj === k}">${o.label}</button>`).join("")}</div>
        <div style="display:flex;gap:6px;flex-wrap:wrap">${D.tiers.map(tt => `<button class="chip" data-tier="${tt.key}" aria-pressed="${S.tiers.has(tt.key)}">${tt.label}</button>`).join("")}</div>
        <div style="display:flex;gap:6px;flex-wrap:wrap">${["Instagram", "YouTube", "Moj", "LinkedIn"].map(p => `<button class="chip" data-plat="${p}" aria-pressed="${S.platforms.has(p)}">${p}</button>`).join("")}</div>
      </div>
      <div class="plan">${planHTML(res, plan)}</div>
      <div class="funnel-strip">
        <div class="fs"><b>${C.length}</b><span>Creators indexed</span></div>
        <div class="fs gate" data-tip="${Object.entries(gcount).map(([k, v]) => `${v} · ${GATE_LABEL[k]}`).join("<br>") || "None"}"><b>${res.gated.length}</b><span>Gated before ranking</span></div>
        <div class="fs"><b>${res.ranked.length}</b><span>Eligible and ranked</span></div>
        <div class="fs"><b>${plan.list.length}</b><span>In the ${fmtINR(S.budget * 1e5)} plan</span></div>
      </div>
      <div class="panel" style="overflow:hidden">
        <div class="panel-h" style="padding-bottom:12px">
          <div class="seg" role="group" aria-label="Centre view"><button data-centre="list" aria-pressed="${S.centre === "list"}">Ranked list</button><button data-centre="map" aria-pressed="${S.centre === "map"}">Efficiency map</button><button data-centre="gated" aria-pressed="${S.centre === "gated"}">Gated (${res.gated.length})</button></div>
          ${S.centre === "list" ? `<div class="right">${legendDims()}<span class="legend"><span><i style="background:var(--accent);width:3px;border-radius:1px"></i>In the plan</span></span></div>` : ""}
        </div>
        <div id="centre">${centreHTML(res, list, plan)}</div>
      </div>
      <details class="panel tune" ${store.get("tuneOpen", false) ? "open" : ""}>
        <summary class="panel-b">${ic("chev", "chev")} Tune the model <span class="muted" style="font-weight:400">weights for ${OBJ[S.obj].label.toLowerCase()} · Represent boost</span></summary>
        <div class="panel-b" style="padding-top:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px">
          <div class="weights">${DIMS.map(([k, l, col]) => `<div class="wrow"><i style="background:var(${col})"></i><label for="w-${k}">${l}</label><input id="w-${k}" type="range" min="0" max="40" value="${S.w[k]}" data-w="${k}"><output>${S.w[k]}</output></div>`).join("")}</div>
          <div style="display:flex;flex-direction:column;gap:12px">
            <p class="ink2" style="font-size:12.5px">Weights are relative. Each objective starts from a preset; strategist changes are logged and, over time, become training labels for the ranking model.</p>
            <div class="wrow" style="grid-template-columns:1fr 92px 30px"><label for="boost">Represent roster boost</label><input id="boost" type="range" min="0" max="5" value="${S.boost}"><output>+${S.boost}</output></div>
            <p class="muted" style="font-size:12px">Capped at 5 points and shown on the score, so roster creators win on fit, never by default.</p>
            <button class="btn sm" id="resetW" style="align-self:flex-start">Reset to ${OBJ[S.obj].label.toLowerCase()} preset</button>
          </div>
        </div>
      </details>
    </section>

  </div>`;
}
function centreHTML(res, list, plan) {
  if (S.centre === "map") return `<div class="panel-b" style="padding-top:0"><div class="legend" style="margin-bottom:8px"><span><i style="background:var(--accent)"></i>In the engine plan</span><span><i style="background:var(--surface);box-shadow:inset 0 0 0 1.6px var(--ink-2)"></i>Follower-count plan, same budget</span><span><i style="background:var(--neutral-mark)"></i>Other eligible creators</span></div><div id="mapChart"></div><p class="view-foot">Both axes are log scale. Dots above the dashed line beat the median outcome per rupee; the engine plan clusters there. The follower-count plan buys the few dots on the far right.</p></div>`;
  if (S.centre === "gated") return `<div class="gatelist">${res.gated.slice(0, 60).map(r => `<div class="grow" data-cr="${r.c.id}">${who(r.c)}<div style="display:flex;flex-direction:column;gap:4px">${r.g.map(g => `<span class="status crit"><i></i>${esc(GATE_LABEL[g.k])}</span><span class="ink2" style="font-size:12.5px">${esc(g.t)}</span>`).join("")}</div></div>`).join("")}${res.gated.length > 60 ? `<p class="panel-b muted">Showing 60 of ${res.gated.length}.</p>` : ""}</div>`;
  const inPlan = new Set(plan.list.map(r => r.c.id));
  const b = res.b;
  const metric = S.obj === "awareness" ? ["TG views", r => fmtN(r.p.tgViews)] : S.obj === "consideration" ? ["Engagements", r => fmtN(r.p.eng)] : b.aov ? ["Orders", r => fmtN(r.p.orders)] : ["Clicks", r => fmtN(r.p.clicks)];
  return `<div class="rank-head"><span class="r">#</span><span>Creator</span><span>Fit score</span><span>Why</span><span class="r">Bundle · ${metric[0]}</span></div>
  <div class="rank">${list.slice(0, 40).map(r => {
    const why = whyOf(r, S.obj, b).slice(0, 2).map(w => w.html).join(". ");
    const added = inPlan.has(r.c.id);
    return `<div class="rrow${added ? " inplan" : ""}" data-cr="${r.c.id}"><span class="rk">${r.rank}</span>${who(r.c, r.c.creds ? ` · ${esc(r.c.creds)}` : "")}<div class="fitc"><div class="top"><span class="score">${r.total.toFixed(0)}<small>/100</small></span><span class="tag ${r.conf[0] === "High" ? "good" : r.conf[0] === "Medium" ? "" : "warn"}" data-tip="Forecast confidence: ±${r.conf[1] * 100}% band, from ${r.c.camps} tracked campaigns and ${r.c.lifts} lift studies">${r.conf[0]}</span></div>${fitBar(r)}</div><div class="why">${why}</div><div class="cost"><b>${fmtINR(r.p.cost)}</b><span>${metric[1](r)} ${metric[0].toLowerCase()}</span></div></div>`;
  }).join("")}</div>${list.length > 40 ? `<p class="panel-b muted" style="font-size:12.5px">Top 40 of ${list.length} eligible creators. Open Discovery to search the rest.</p>` : ""}`;
}
function planHTML(res, plan) {
  const b = res.b, a = plan.agg;
  const v = vanityPlan(res, a.cost).agg;
  const band = a.band;
  const rng = (x, f) => `${f(x * (1 - band))}–${f(x * (1 + band))}`;
  const tiersOrder = ["nano", "micro", "mid", "macro", "mega"];
  const tcol = { nano: "--s7", micro: "--s1", mid: "--s4", macro: "--s3", mega: "--s2" };
  const ratio = (e, vv) => vv > 0 ? xf(e / vv) : "n/a";
  const rows = [
    ["Verified TG views", a.tg, v.tg, fmtN],
    ["Engagements", a.eng, v.eng, fmtN],
    ["Link clicks", a.clicks, v.clicks, fmtN],
    ...(b.aov && b.cvr ? [["Orders", a.orders, v.orders, fmtN], ["Revenue", a.rev, v.rev, fmtINR]] : []),
    ["Ad recall lift (pts)", a.recall, v.recall, x => x.toFixed(1)],
  ];
  const maxOf = (e, vv) => Math.max(e, vv) || 1;
  return `
  <div class="panel"><div class="panel-h"><h3>Engine plan</h3><span class="sub">${OBJ[S.obj].label}</span></div>
    <div class="panel-b" style="display:flex;flex-direction:column;gap:14px">
      <div><div style="display:flex;justify-content:space-between;align-items:baseline"><label for="budget" class="mini-h" style="margin:0">Budget</label><b class="num">${fmtINR(S.budget * 1e5)}</b></div><input id="budget" type="range" min="5" max="200" step="1" value="${S.budget}"></div>
      <div class="plan-big">
        <div><b>${a.n}</b><span>creators · ${fmtINR(a.cost)} used</span><br><em>+ ${fmtINR(a.n * OPS)} ops cost</em></div>
        <div><b>${fmtN(a.reach)}</b><span>unique TG reach</span></div>
        <div><b>${fmtN(a.tg)}</b><span>verified TG views</span><br><em>${rng(a.tg, fmtN)}</em></div>
        ${b.aov && b.cvr && S.obj === "conversion" ? `<div><b>${xf(a.roas, 2)}</b><span>forecast ROAS</span><br><em>${fmtN(a.orders)} orders</em></div>` : S.obj === "consideration" ? `<div><b>${fmtN(a.eng)}</b><span>engagements</span><br><em>${fmtRs(a.cost / Math.max(1, a.eng))} each</em></div>` : `<div><b>+${a.recall.toFixed(1)}</b><span>ad recall lift, pts</span></div>`}
      </div>
      <div><div class="mini-h">Spend by tier</div><div class="pace" style="height:10px">${tiersOrder.filter(k => a.tiers[k]).map(k => `<i style="width:${a.tiers[k] / a.cost * 100}%;background:var(${tcol[k]})" data-tip="<b>${TIER[k].label}</b>: ${fmtINR(a.tiers[k])} (${pc(a.tiers[k] / a.cost)})"></i>`).join("")}</div>
        <div class="legend" style="margin-top:8px">${tiersOrder.filter(k => a.tiers[k]).map(k => `<span><i style="background:var(${tcol[k]})"></i>${TIER[k].label} ${pc(a.tiers[k] / a.cost)}</span>`).join("")}</div></div>
      ${a.rep ? `<p class="ink2" style="font-size:12.5px"><b>${a.rep}</b> Represent roster creators earned a place on fit (${fmtINR(a.repCost)}).</p>` : ""}
      <button class="btn sm" id="copyBrief">${ic("copy")} Copy shortlist</button>
    </div></div>
  <div class="panel"><div class="panel-h"><h3>Engine vs follower count</h3><span class="sub">Same ${fmtINR(a.cost)} spend</span></div>
    <div class="panel-b vs">
      <div class="legend"><span><i style="background:var(--accent)"></i>Engine plan</span><span><i style="background:var(--neutral-mark)"></i>Biggest accounts first</span></div>
      ${rows.map(([l, e, vv, f]) => `<div class="vs-row"><div class="l"><span>${l}</span><b>${f(e)} vs ${f(vv)} · ${ratio(e, vv)}</b></div><div class="vs-bars"><i class="e" style="width:${e / maxOf(e, vv) * 100}%"></i><i class="v" style="width:${vv / maxOf(e, vv) * 100}%"></i></div></div>`).join("")}
      <hr class="hr">
      <div class="kv"><dt>Fake or inactive audience bought</dt><dd>${pc(a.fake, 1)} vs <b>${pc(v.fake, 1)}</b></dd><dt>Gated creators included</dt><dd>0 vs <b class="${v.gated ? "delta-down" : ""}">${v.gated}</b></dd><dt>Creators in plan</dt><dd>${a.n} vs ${v.n}</dd></div>
    </div></div>`;
}
function afterMatch() {
  if (S.centre !== "map") return;
  const { res } = matchRes(), b = res.b;
  const planObj = buildPlan(res, S.budget * 1e5);
  const plan = new Set(planObj.list.map(r => r.c.id));
  const van = new Set(vanityPlan(res, planObj.agg.cost).list.map(r => r.c.id));
  const yv = r => outcomeOf(S.obj, r.p, b);
  const lab = S.obj === "awareness" ? "verified TG views (recall-weighted)" : S.obj === "consideration" ? "engagements" : b.aov ? "revenue (₹)" : "clicks";
  const pts = res.rows.filter(r => !r.g.length || van.has(r.c.id)).map(r => ({ x: r.p.cost, y: Math.max(1, yv(r)), k: plan.has(r.c.id) ? "plan" : van.has(r.c.id) ? "vanity" : "base",
    tip: `<b>${esc(r.c.name)}</b> · ${TIER[r.c.tier].label}<br>Cost ${fmtINR(r.p.cost)} · fit ${r.total.toFixed(0)}<br>Forecast ${S.obj === "conversion" && b.aov ? fmtINR(yv(r)) : fmtN(yv(r))} ${lab}${r.g.length ? `<br>Gated: ${esc(GATE_LABEL[r.g[0].k])}` : ""}` }));
  const ref = median(res.ranked.map(r => Math.max(1, yv(r)) / r.p.cost));
  scatter($("#mapChart"), { pts, xfmt: fmtINR, yfmt: S.obj === "conversion" && b.aov ? fmtINR : fmtN, xlab: "Cost of 1 reel + 2 stories", ylab: lab, ref });
}

/* ---------- drawer (creator profile) */
function openDrawer(id) { S.drawer = id; renderDrawer(); }
function closeDrawer() { S.drawer = null; $("#drawer").classList.remove("on"); $("#scrim").classList.remove("on"); setTimeout(() => { if (!S.drawer) { $("#drawer").hidden = true; $("#scrim").hidden = true; } }, 240); }
function renderDrawer() {
  const c = CBY[S.drawer]; if (!c) return;
  const b = brandState();
  const res = scoreBrand(b, S.obj, S.w, S.boost);
  const r = res.rows.find(x => x.c.id === c.id);
  const t = b.target, a = c.aud;
  const ageL = ["13–17", "18–24", "25–34", "35–44", "45+"];
  const why = whyOf(r, S.obj, b), flags = flagsOf(b, c);
  const band = r.conf[1];
  const rg = (x, f) => `${f(x * (1 - band))}–${f(x * (1 + band))}`;
  const dr = $("#drawer");
  dr.innerHTML = `
  <div class="dr-h">${avatar(c, true)}<div style="flex:1;min-width:0">
    <h2>${esc(c.name)}</h2>
    <div class="muted" style="font-size:12.5px">${c.id} · ${esc(NICHE[c.niche])} + ${esc(NICHE[c.niche2])} · ${esc(c.city)}, ${esc(c.state)}</div>
    <div class="tags" style="margin-top:8px"><span class="tag">${TIER[c.tier].label} · ${fmtN(c.followers)}</span><span class="tag">${esc(c.platform)}</span>${c.langs.map(l => `<span class="tag">${esc(l)}</span>`).join("")}${c.represent ? '<span class="tag accent">Represent roster</span>' : ""}${c.creds ? `<span class="tag good">${ic("shield")}${esc(c.creds)}</span>` : ""}</div>
  </div><button class="icon-btn" id="drClose" aria-label="Close profile">${ic("x")}</button></div>
  <div class="dr-b">
    <div class="dr-sec">
      <h3>Fit for ${esc(b.name)} · ${OBJ[S.obj].label.toLowerCase()}</h3>
      <div style="display:flex;align-items:center;gap:16px;margin-bottom:12px">
        <div class="score" style="font-size:40px">${r.total.toFixed(0)}<small>/100</small></div>
        <div style="flex:1">${r.g.length ? `<span class="status crit"><i></i>Gated: not ranked</span>` : `<span class="status good"><i></i>Rank ${r.rank} of ${res.ranked.length} eligible</span>`}<div style="margin-top:8px">${fitBar(r, 10)}</div></div>
      </div>
      <div class="dims">${DIMS.map(([k, l, col]) => `<div class="dim"><i style="background:var(${col})"></i><span>${l}</span><div class="t"><span style="width:${r.s[k]}%;background:var(${col})"></span></div><span class="v">${r.s[k].toFixed(0)}</span><span class="w">×${S.w[k]} → ${r.contrib[k].toFixed(1)}</span></div>`).join("")}</div>
    </div>
    <div class="dr-sec"><h3>Why, and what to watch</h3><ul class="why-list">
      ${r.g.map(g => `<li class="blk">${ic("block")}<span><b>${esc(GATE_LABEL[g.k])}.</b> ${esc(g.t)}</span></li>`).join("")}
      ${why.filter(w => w.strong).slice(0, 4).map(w => `<li class="pos">${ic("check")}<span>${w.html}</span></li>`).join("")}
      ${flags.map(f => `<li class="neg">${ic("warn")}<span>${esc(f)}</span></li>`).join("")}
    </ul></div>
    <div class="dr-sec"><h3>Forecast · 1 reel + 2 stories${c.platform === "YouTube" ? " (YouTube integration)" : ""}</h3>
      <div class="metric-grid">
        <div><b>${fmtINR(r.p.cost)}</b><span>Cost</span></div>
        <div><b>${fmtN(r.p.views)}</b><span>Views</span><br><em>${rg(r.p.views, fmtN)}</em></div>
        <div><b>${fmtN(r.p.tgViews)}</b><span>Verified TG views</span><br><em>${pc(r.p.tgShare)} in target</em></div>
        <div><b>${fmtN(r.p.clicks)}</b><span>Link clicks</span><br><em>${fmtRs(r.p.cpc)} per click</em></div>
        <div><b>${b.aov && b.cvr ? fmtN(r.p.orders) : fmtN(r.p.eng)}</b><span>${b.aov && b.cvr ? "Orders" : "Engagements"}</span><br><em>${b.aov && b.cvr ? `${fmtINR(r.p.rev)} revenue` : `${fmtRs(r.p.cpe)} each`}</em></div>
        <div><b>${b.aov && b.cvr ? xf(r.p.roas, 2) : fmtRs(r.p.cpv)}</b><span>${b.aov && b.cvr ? "Forecast ROAS" : "Per TG view"}</span></div>
        <div><b>+${r.p.recall.toFixed(1)}</b><span>Recall lift, pts</span></div>
        <div><b>${r.conf[0]}</b><span>Confidence</span><br><em>±${band * 100}% · ${c.camps} campaigns</em></div>
      </div></div>
    <div class="dr-sec"><h3>Audience vs ${esc(b.name)} target</h3>
      <div class="legend" style="margin-bottom:10px"><span><i style="background:var(--s1)"></i>${esc(c.name)}'s audience</span><span><i style="background:var(--neutral-mark)"></i>Brand target</span></div>
      <div class="mirror">
        <div class="mir"><span>Women</span><div class="a"><i style="width:${a.fem * 100}%"></i></div><div class="b"><i style="width:${t.fem * 100}%"></i></div></div>
        ${a.age.map((v, i) => `<div class="mir"><span>${ageL[i]}</span><div class="a" data-tip="${pc(v)} of audience"><i style="width:${v * 100}%"></i></div><div class="b" data-tip="${pc(t.age[i])} of target"><i style="width:${t.age[i] * 100}%"></i></div></div>`).join("")}
        ${a.tiers.map((v, i) => `<div class="mir"><span>Tier ${i + 1}</span><div class="a" data-tip="${pc(v)} of audience"><i style="width:${v * 100}%"></i></div><div class="b" data-tip="${pc(t.tiers[i])} of target"><i style="width:${t.tiers[i] * 100}%"></i></div></div>`).join("")}
      </div>
      <p class="ink2" style="font-size:12.5px;margin-top:10px">Top places: ${a.geo.map(g => `${esc(g[0])} ${g[1]}%`).join(" · ")}. Audience languages: ${Object.entries(a.langs).map(([l, v]) => `${esc(l)} ${pc(v)}`).join(", ")}. Affluence index ${Math.round(a.affl * 100)}.</p>
    </div>
    <div class="dr-sec"><h3>Performance & quality</h3>
      <div class="metric-grid">
        <div><b>${pct(c.er, 2)}</b><span>Engagement rate</span><br><em>top ${topPct(pctl(c, "er"))}% of tier</em></div>
        <div><b>${fmtN(c.views)}</b><span>Avg views</span></div>
        <div><b>${pct(c.vtr, 0)}</b><span>View-through</span></div>
        <div><b>${pct(c.hook, 0)}</b><span>Hold at 3 sec</span></div>
        <div><b>${pct(c.ctr, 2)}</b><span>Link CTR</span></div>
        <div><b>${pct(c.saves + c.shares, 1)}</b><span>Save + share rate</span></div>
        <div><b>${pct(c.sent, 0)}</b><span>Positive comments</span></div>
        <div><b>${c.cq}</b><span>Content quality</span></div>
        <div><b class="${c.cred < 72 ? "delta-down" : ""}">${pct(c.cred, 0)}</b><span>Real followers</span></div>
        <div><b>${c.spons}%</b><span>Sponsored posts</span></div>
        <div><b>${c.asci}%</b><span>#ad disclosure</span></div>
        <div><b>${c.ontime}%</b><span>On-time delivery</span></div>
      </div>
      <div style="display:flex;align-items:center;gap:14px;margin-top:12px"><div>${sparkline(c.growth, 180, 40, c.fraud ? "--crit" : "--s1")}</div><p class="ink2" style="font-size:12.5px">Followers, last 12 months. ${c.g90 > 0 ? "+" : ""}${c.g90}% in the last 90 days.${c.fraud ? " <b>A one-month spike without matching engagement suggests bought followers.</b>" : ""}</p></div>
    </div>
    <div class="dr-sec"><h3>Commercials & history</h3>
      <dl class="kv">
        <dt>Reel</dt><dd>${fmtINR(c.rate.reel)}</dd><dt>Story</dt><dd>${fmtINR(c.rate.story)}</dd>${c.rate.yt ? `<dt>YouTube integration</dt><dd>${fmtINR(c.rate.yt)}</dd>` : ""}
        <dt>Tracked campaigns with Chtrbox</dt><dd>${c.camps}</dd><dt>Brand-lift studies</dt><dd>${c.lifts}</dd>
        <dt>Recent brand work</dt><dd>${c.collabs.length ? c.collabs.map(([n, d]) => `${b.competitors.includes(n) ? `<b class="delta-down">${esc(n)}</b>` : esc(n)} (${d}d)`).join(", ") : "None in 140 days"}</dd>
        <dt>Content codes</dt><dd>${c.codes.map(esc).join(", ")}</dd>
      </dl>
    </div>
  </div>`;
  dr.hidden = false; $("#scrim").hidden = false;
  requestAnimationFrame(() => { dr.classList.add("on"); $("#scrim").classList.add("on"); });
  $("#drClose").addEventListener("click", closeDrawer);
  $("#drClose").focus({ preventScroll: true });
}

/* ---------- discovery */
const KW = {
  niche: { beauty: /beauty|skin ?care|makeup|cosmetic/, fashion: /fashion|\bstyl(?:e|ist|ing)\b|outfit|ootd/, food: /food|cook|recipe|chef/, fitness: /fitness|gym|workout|yoga/, finance: /financ|invest|money|stock|finfluencer|mutual fund/, tech: /tech|gadget|phone|laptop/, comedy: /comedy|funny|meme|comic/, parenting: /parent|mom|mother|dad|family/, travel: /travel/, lifestyle: /lifestyle|vlog/, gaming: /gaming|gamer/, health: /doctor|dietitian|health|nutrition|dermatolog/, music: /music|dance|singer/, education: /education|career|student|exam/, home: /home|decor|interior/, auto: /\bauto|car|bike/ },
};
const LANGS = D.langs;
const CITYN = [...new Set(C.map(c => c.city))];
function parseQuery(q) {
  const s = q.toLowerCase(), f = { chips: [] };
  for (const [k, re] of Object.entries(KW.niche)) if (re.test(s)) { (f.niche ||= []).push(k); }
  if (f.niche) f.chips.push(f.niche.map(k => NICHE[k]).join(" or "));
  for (const l of LANGS) if (new RegExp("\\b" + l.toLowerCase() + "\\b").test(s)) (f.lang ||= []).push(l);
  if (/\bregional\b/.test(s)) { (f.lang ||= []).push(...["Tamil", "Telugu", "Kannada", "Malayalam", "Marathi", "Bengali", "Gujarati", "Punjabi", "Odia", "Assamese"].filter(l => !(f.lang || []).includes(l))); f.chips.push("Regional languages"); }
  else if (f.lang) f.chips.push(f.lang.join(" or "));
  const alias = { bangalore: "Bengaluru", delhi: "Delhi NCR", ncr: "Delhi NCR", gurgaon: "Delhi NCR", vizag: "Visakhapatnam", bombay: "Mumbai" };
  for (const c of CITYN) if (s.includes(c.toLowerCase().split(" ")[0])) (f.city ||= []).push(c);
  for (const [k, v] of Object.entries(alias)) if (s.includes(k) && !(f.city || []).includes(v)) (f.city ||= []).push(v);
  if (f.city) f.chips.push(f.city.join(" or "));
  const tm = s.match(/tier[\s-]?(1|2|3|i{1,3})\b/); if (tm) { f.ctier = { i: 1, ii: 2, iii: 3 }[tm[1]] || +tm[1]; f.chips.push(`Tier-${f.ctier} cities`); }
  if (/\bmetro/.test(s)) { f.ctier = 1; f.chips.push("Metros"); }
  for (const t of D.tiers) if (new RegExp("\\b" + t.key + "\\b").test(s)) (f.tier ||= []).push(t.key);
  if (f.tier) f.chips.push(f.tier.map(k => TIER[k].label).join(" or "));
  const plat = { YouTube: /youtube|\byt\b/, Instagram: /instagram|\big\b|reels?/, Moj: /\bmoj\b|sharechat/, LinkedIn: /linkedin/ };
  for (const [k, re] of Object.entries(plat)) if (re.test(s)) (f.plat ||= []).push(k);
  if (f.plat) f.chips.push(f.plat.join(" or "));
  const mr = s.match(/(?:under|below|less than|max|<|upto|up to)\s*₹?\s*(\d+(?:\.\d+)?)\s*(k|l|lakh|lac|cr)?/);
  if (mr) { const mult = { k: 1e3, l: 1e5, lakh: 1e5, lac: 1e5, cr: 1e7 }[mr[2]] || 1; f.maxRate = +mr[1] * mult; f.chips.push(`Reel ≤ ${fmtINR(f.maxRate)}`); }
  const er = s.match(/\b(?:er|engagement(?: rate)?)\b[^0-9]{0,14}(\d+(?:\.\d+)?)\s*%?/); if (er) { f.minER = +er[1]; f.chips.push(`ER ≥ ${f.minER}%`); }
  if (/women|female|girls/.test(s)) { f.fem = 1; f.chips.push("Audience ≥ 60% women"); }
  if (/\bmen\b|\bmale|boys/.test(s)) { f.fem = -1; f.chips.push("Audience ≥ 60% men"); }
  if (/gen ?z|college|campus/.test(s)) { f.genz = 1; f.chips.push("Audience 18–24 ≥ 45%"); }
  if (/represent|exclusive|roster/.test(s)) { f.rep = 1; f.chips.push("Represent roster"); }
  if (/sebi|registered/.test(s)) { f.sebi = 1; f.chips.push("SEBI-registered"); }
  if (/doctor|dermatolog|dietitian|credential|qualified|certified/.test(s)) { f.cred = 1; f.chips.push("Credentialed"); }
  if (/authentic|real|no fake|clean/.test(s)) { f.auth = 1; f.chips.push("≥ 85% real followers"); }
  if (/\buae|gulf|mena|dubai|gcc/.test(s)) { f.uae = 1; f.chips.push("UAE audience"); }
  return f;
}
function matchQuery(c, f) {
  if (f.niche && !f.niche.includes(c.niche) && !f.niche.includes(c.niche2)) return false;
  if (f.lang && !c.langs.some(l => f.lang.includes(l))) return false;
  if (f.city && !f.city.includes(c.city)) return false;
  if (f.ctier && c.ctier !== f.ctier) return false;
  if (f.tier && !f.tier.includes(c.tier)) return false;
  if (f.plat && !f.plat.includes(c.platform)) return false;
  if (f.maxRate && c.rate.reel > f.maxRate) return false;
  if (f.minER && c.er < f.minER) return false;
  if (f.fem === 1 && c.aud.fem < .6) return false;
  if (f.fem === -1 && c.aud.fem > .4) return false;
  if (f.genz && c.aud.age[1] < .45) return false;
  if (f.rep && !c.represent) return false;
  if (f.sebi && !(c.creds || "").startsWith("SEBI")) return false;
  if (f.cred && !c.creds) return false;
  if (f.auth && c.cred < 85) return false;
  if (f.uae && c.market !== "UAE") return false;
  return true;
}
const EXAMPLES = ["Hindi beauty creators under 25k with ER above 3%", "SEBI-registered finance creators", "Gen Z fashion micro creators in Mumbai", "doctors and dietitians", "regional language food creators", "tier 2 creators with women audience", "Dubai lifestyle creators", "authentic mid-tier tech creators", "Represent roster"];
function vDiscover() {
  const b = brandState();
  return `
  <div class="sect-title"><h2>Search the creator graph in plain language</h2><p>Type the way a strategist briefs. The engine turns it into filters and ranks the results for ${esc(b.name)}.</p></div>
  <label class="search" for="q">${ic("discover")}<input id="q" type="search" placeholder="e.g. Hinglish beauty micro creators in Delhi" value="${esc(S.query)}" autocomplete="off"><select id="dBrand" class="sel" aria-label="Rank for brand" style="max-width:190px">${brandOptions(b.id)}</select></label>
  <div class="parsed" id="examples"><span class="muted" style="font-size:12.5px">Try:</span>${EXAMPLES.map(e => `<button class="chip" data-ex="${esc(e)}">${esc(e)}</button>`).join("")}</div>
  <div id="dres"></div>`;
}
function renderDiscover() {
  const b = brandState();
  const f = parseQuery(S.query);
  const res = scoreBrand(b, S.obj, S.w, S.boost);
  const byId = Object.fromEntries(res.rows.map(r => [r.c.id, r]));
  let rows = C.filter(c => matchQuery(c, f)).map(c => byId[c.id]);
  const [k, dir] = S.dSort;
  const key = { fit: r => r.g.length ? -1 : r.total, followers: r => r.c.followers, er: r => r.c.er, ctr: r => r.c.ctr, cred: r => r.c.cred, rate: r => r.c.rate.reel, name: r => r.c.name }[k];
  rows.sort((x, y) => (key(x) > key(y) ? 1 : key(x) < key(y) ? -1 : 0) * dir);
  const per = 25, pages = Math.max(1, Math.ceil(rows.length / per)); S.dPage = Math.min(S.dPage, pages - 1);
  const pageRows = rows.slice(S.dPage * per, S.dPage * per + per);
  const th = (key2, l, r) => `<th class="${r ? "r" : ""}" aria-sort="${S.dSort[0] === key2 ? (S.dSort[1] > 0 ? "ascending" : "descending") : "none"}"><button data-sort="${key2}">${l}${S.dSort[0] === key2 ? (S.dSort[1] > 0 ? " ↑" : " ↓") : ""}</button></th>`;
  $("#dres").innerHTML = `
  <div class="parsed" style="margin-bottom:12px">${f.chips.length ? `<span class="muted" style="font-size:12.5px">Understood:</span>${f.chips.map(c => `<span class="tag accent">${esc(c)}</span>`).join("")}` : `<span class="muted" style="font-size:12.5px">No filters yet. Showing every creator, ranked for ${esc(b.name)}.</span>`}</div>
  <div class="tiles" style="margin-bottom:14px">
    <div class="tile"><div class="lbl">Matches</div><div class="val">${rows.length}</div><div class="note">${rows.filter(r => !r.g.length).length} eligible for ${esc(b.name)}</div></div>
    <div class="tile"><div class="lbl">Median engagement</div><div class="val">${rows.length ? pct(median(rows.map(r => r.c.er)), 2) : "–"}</div></div>
    <div class="tile"><div class="lbl">Median reel rate</div><div class="val">${rows.length ? fmtINR(median(rows.map(r => r.c.rate.reel))) : "–"}</div></div>
    <div class="tile"><div class="lbl">Combined followers</div><div class="val">${rows.length ? fmtN(sum(rows, r => r.c.followers)) : "–"}</div></div>
    <div class="tile"><div class="lbl">Median real followers</div><div class="val">${rows.length ? pct(median(rows.map(r => r.c.cred)), 0) : "–"}</div></div>
  </div>
  <div class="panel" style="overflow:hidden"><div class="tbl-wrap"><table class="tbl">
    <thead><tr>${th("name", "Creator")}<th>Languages</th>${th("followers", "Followers", 1)}${th("er", "ER", 1)}${th("ctr", "Link CTR", 1)}${th("cred", "Real", 1)}${th("rate", "Reel rate", 1)}${th("fit", "Fit · " + esc(b.name), 1)}</tr></thead>
    <tbody>${pageRows.map(r => `<tr class="click" data-cr="${r.c.id}"><td style="min-width:260px">${who(r.c)}</td><td>${r.c.langs.map(esc).join(", ")}</td><td class="r">${fmtN(r.c.followers)}</td><td class="r">${pct(r.c.er, 2)}</td><td class="r">${pct(r.c.ctr, 2)}</td><td class="r ${r.c.cred < 72 ? "delta-down" : ""}">${pct(r.c.cred, 0)}</td><td class="r">${fmtINR(r.c.rate.reel)}</td><td class="r">${r.g.length ? `<span class="status crit" data-tip="${esc(r.g.map(g => g.t).join("<br>"))}"><i></i>${esc(GATE_LABEL[r.g[0].k])}</span>` : `<b>${r.total.toFixed(0)}</b>`}</td></tr>`).join("") || `<tr><td colspan="8" class="muted" style="padding:28px 12px">No creators match. Remove a filter, for example the price cap or the city.</td></tr>`}</tbody>
  </table></div>
  ${pages > 1 ? `<div class="panel-b" style="display:flex;gap:8px;align-items:center;justify-content:flex-end"><span class="muted" style="font-size:12.5px">Page ${S.dPage + 1} of ${pages}</span><button class="btn sm" data-page="-1" ${S.dPage ? "" : "disabled"}>Previous</button><button class="btn sm" data-page="1" ${S.dPage < pages - 1 ? "" : "disabled"}>Next</button></div>` : ""}</div>`;
}

/* ---------- vertical lens */
const PLAY = {
  fmcg: { thesis: "Reach the target group many times at a low cost per view, then prove memory moved. Sales show up later in quick-commerce and kirana, not in click-throughs.",
    kpi: ["Verified TG reach and frequency", "Ad recall and awareness lift (exposed vs control)", "Quick-commerce search and sales lift in test cities", "Sampling or code redemptions"],
    mix: "60% nano and micro creators in regional languages for cheap reach, 30% mid-tier, one macro anchor for salience.", formats: "15–30s Reels with the pack in the first 3 seconds; recipes and daily rituals; stories linking to Blinkit, Zepto and Instamart.",
    lang: "6 to 9 languages. Hindi and Hinglish first, then Tamil, Telugu, Marathi, Bengali and Kannada.", comp: "Health-benefit claims (immunity, energy) need substantiation; Drugs & Magic Remedies Act applies to cure language; ASCI disclosure.", moments: "Winter (Nov–Jan), summer and IPL (Mar–May), festive (Sep–Nov)." },
  ecom: { thesis: "Every rupee should trace to an order. The job is CTR × conversion, net of returns, with new-customer share as the quality check.",
    kpi: ["Verified orders and revenue, net of returns", "Incremental ROAS from geo holdouts", "New-to-platform customer share", "CAC and 60-day repeat"],
    mix: "Micro and mid-tier creators with high link CTR; storefront and affiliate links; a few macro creators only on sale days.", formats: "Haul and 'what I bought' Reels, price-drop story stickers, live countdowns before sale events.",
    lang: "Regional languages decide tier-2 and tier-3 conversion. Measure by language, not just by creator.", comp: "Price claims must match the live listing; disclose affiliate earnings; the CCPA's dark-pattern rules apply to urgency claims.", moments: "Great Indian Festival and Big Billion Days (Sep–Oct), EOSS (Jun, Dec), Pink Friday (Nov)." },
  beauty: { thesis: "Beauty is bought on proof. Saves, tutorial completion and credible voices predict sales better than likes.",
    kpi: ["Saves per view and tutorial completion", "Consideration lift", "PDP click-through and sampling to repeat", "Comment sentiment on efficacy"],
    mix: "Credentialed creators (dermatologists) for actives, micro creators for routines, K-culture Gen-Z creators for K-beauty.", formats: "Get-ready-with-me videos, 7-day and 28-day challenges, ingredient explainers, honest before-and-after (no filters).",
    lang: "English and Hinglish for premium; Hindi and regional languages for masstige makeup.", comp: "ASCI: no filters that exaggerate results; technical skin claims need qualified creators; no 'cures acne'.", moments: "Wedding season (Nov–Feb), festive glow (Oct–Nov), monsoon and summer skin." },
  fashion: { thesis: "Fashion runs on taste and on returns. Saves and shares show taste; return-adjusted revenue shows whether it sold.",
    kpi: ["Saves and shares per view", "PDP click-through", "Revenue net of returns (fashion returns run high)", "Store visits for omnichannel brands"],
    mix: "Micro creators with a distinct style, mid-tier for drops, one or two macro creators for launches.", formats: "Try-on hauls, fit checks, styling one piece three ways, size-inclusive casting.",
    lang: "English and Hinglish lead; Hindi and regional languages for value fashion.", comp: "Disclose gifted products; avoid misleading 'sustainable' claims without proof (ASCI green claims).", moments: "EOSS (Jun, Dec), wedding season, festive, back-to-college." },
  health: { thesis: "Trust is the product. A qualified creator with a smaller audience beats a large lifestyle account, and the rules require it for technical claims.",
    kpi: ["Credentialed reach (doctors, dietitians)", "Trust and sentiment", "Bookings, consultations or orders", "Repeat purchase at 60–90 days"],
    mix: "Mid-tier doctors and dietitians as the spine, fitness creators for lifestyle use, micro creators for testimonials with disclosure.", formats: "Myth-busting explainers, day-in-the-life, Q&A lives, routines without cure claims.",
    lang: "Hindi and Hinglish first; regional languages for diagnostics and pharmacy.", comp: "ASCI Addendum II (Apr 2025): technical health claims need qualified creators; Drugs & Magic Remedies Act; no disease-cure language.", moments: "New-year resolutions (Jan), monsoon health (Jul–Sep), winter immunity." },
  bfsi: { thesis: "Finance is the most regulated creator category. The engine gates who may speak, then optimises for funded accounts, not installs.",
    kpi: ["Funded accounts or policies issued", "Cost per funded account", "KYC completion rate", "Complaints and grievance rate"],
    mix: "SEBI-registered advisers and analysts for product talk; non-finance creators only for brand-scripted app experience.", formats: "Long-form YouTube explainers, LinkedIn posts, Hinglish 'how I started my first SIP' with disclaimers.",
    lang: "Hinglish and Hindi; Gujarati and Marathi over-index for investing.", comp: "SEBI rules bar regulated entities from working with unregistered finfluencers who give advice or return claims; IRDAI for insurance; ASCI Addendum II.", moments: "Tax-saving season (Jan–Mar), IPO windows, new financial year." },
  tech: { thesis: "Tech is researched before it is bought. Depth and credibility of review content matter more than reach.",
    kpi: ["Consideration lift", "Store and PDP visits", "Search lift for the model name", "Review sentiment"],
    mix: "YouTube reviewers for depth, Shorts and Reels creators for launch buzz, gaming and education creators for laptops.", formats: "Unboxings, 30-day reviews, comparisons, 'setup tour', student-life integrations.",
    lang: "English and Hinglish; Hindi and Tamil for mass phones.", comp: "No fake or paid-for reviews presented as organic (consumer protection rules on reviews); disclose free devices.", moments: "Back to college (Jun–Aug), festive (Sep–Nov), launch weeks." },
  services: { thesis: "Services are local. City-level creators and redeemable codes tie spend to bookings and visits.",
    kpi: ["Bookings or app orders", "Code redemptions by city", "Store or route demand lift", "Repeat bookings"],
    mix: "City-specific micro and mid creators; diaspora creators for international routes (Dubai first).", formats: "Real-experience vlogs, before-and-after, route launches, limited-time offers.",
    lang: "City language first: Marathi in Pune, Kannada in Bengaluru, Malayalam for Gulf routes.", comp: "Offer terms must match the app; service quality claims need substantiation.", moments: "Pre-Diwali (Oct), holiday travel (Oct–Dec), monsoon." },
  ent: { thesis: "Music and entertainment win by being used, not watched. Audio uses and shares are the leading signal.",
    kpi: ["Audio uses and remixes", "Stream lift in week one", "Shares per view", "Ad recall for platform campaigns"],
    mix: "Meme-native comedy and dance creators, regional music creators, nano creators to seed a sound at scale.", formats: "Dance challenges, duets, lip-syncs, release-week countdowns.",
    lang: "Hindi, Punjabi and Tamil over-index; regional pride content travels.", comp: "Copyright and licensing on audio; disclose label partnerships.", moments: "Release weeks, Wrapped (Dec), wedding season playlists." },
};
const vertCache = {};
function vertStats(vk) {
  if (vertCache[vk]) return vertCache[vk];
  const bs = B.filter(b => b.vertical === vk);
  const acc = {};
  for (const b of bs) {
    const res = scoreBrand(b, b.objective, OBJ[b.objective].w);
    for (const r of res.ranked) { const a = (acc[r.c.id] ||= { c: r.c, s: 0, n: 0, top: 0 }); a.s += r.total; a.n++; if (r.rank <= 20) a.top++; }
  }
  const top = Object.values(acc).filter(a => a.n === bs.length).map(a => ({ ...a, avg: a.s / a.n })).sort((x, y) => y.avg - x.avg);
  const byNiche = {};
  for (const a of top) (byNiche[a.c.niche] ||= []).push(a.avg);
  const heat = Object.fromEntries(Object.keys(NICHE).map(k => [k, byNiche[k] ? sum(byNiche[k].slice(0, 5)) / Math.min(5, byNiche[k].length) : 0]));
  return (vertCache[vk] = { bs, top, heat });
}
function vVerticals() {
  const vk = S.vertical, st = vertStats(vk), P = PLAY[vk];
  const niches = Object.keys(NICHE);
  const allHeat = D.verticals.map(([k]) => vertStats(k).heat);
  const hv = allHeat.flatMap(h => Object.values(h)).filter(Boolean);
  const lo = Math.min(...hv), hi = Math.max(...hv);
  const cell = v => { if (!v) return `<div class="hc" style="background:var(--surface-2);color:var(--muted)">–</div>`; const p = Math.round(8 + (v - lo) / (hi - lo) * 84); return `<div class="hc" style="background:color-mix(in oklab, var(--seq) ${p}%, var(--surface));color:${p > 52 ? "#fff" : "var(--ink)"}">${v.toFixed(0)}</div>`; };
  const archetypes = (() => { const m = {}; for (const a of st.top.slice(0, 60)) { const k = `${a.c.niche}|${a.c.tier}|${a.c.langs[0]}`; (m[k] ||= { n: 0, s: 0, c: a.c }).n++; m[k].s += a.avg; } return Object.entries(m).sort((x, y) => y[1].n - x[1].n || y[1].s - x[1].s).slice(0, 6); })();
  // benchmarks by tier among creators eligible for every brand in the vertical
  const bench = D.tiers.map(t => {
    const xs = st.top.filter(a => a.c.tier === t.key);
    const b0 = st.bs[0];
    const ps = xs.map(a => predict(b0, a.c, audFit(b0, a.c), affOf(b0, a.c)));
    return { t, n: xs.length, er: median(xs.map(a => a.c.er)), ctr: median(xs.map(a => a.c.ctr)), rate: median(xs.map(a => a.c.rate.reel)), cpv: median(ps.map(p => p.cpv)), cpe: median(ps.map(p => p.cpe)), cpc: median(ps.map(p => p.cpc)) };
  }).filter(r => r.n);
  return `
  <div class="parsed">${D.verticals.map(([k, l]) => `<button class="chip" data-vert="${k}" aria-pressed="${k === vk}">${esc(l)}</button>`).join("")}</div>
  <div class="grid g2">
    <div class="panel"><div class="panel-h"><h3>${esc(VERT[vk])}: what actually matters</h3></div><div class="panel-b" style="display:flex;flex-direction:column;gap:14px">
      <p style="font-size:15px;line-height:1.5">${esc(P.thesis)}</p>
      <div><div class="mini-h">KPI stack, in order of priority</div><div class="kpi-stack">${P.kpi.map((k, i) => `<div><span>0${i + 1}</span>${esc(k)}</div>`).join("")}</div></div>
      <div><div class="mini-h">Brands in this vertical</div><div class="brandcards">${st.bs.map(b => `<button class="bcard" data-brand="${b.id}"><div class="blogo">${esc(brandMark(b.name))}</div><div style="min-width:0"><b>${esc(b.name)}</b><span>${esc(b.status)} · ${esc(b.sub)}</span></div></button>`).join("")}</div></div>
    </div></div>
    <div class="panel"><div class="panel-h"><h3>Playbook</h3><span class="sub">How the engine weights and staffs this category</span></div><div class="panel-b play">
      <div><h4>Tier mix</h4><p>${esc(P.mix)}</p></div><div><h4>Formats</h4><p>${esc(P.formats)}</p></div>
      <div><h4>Languages</h4><p>${esc(P.lang)}</p></div><div><h4>Moments</h4><p>${esc(P.moments)}</p></div>
      <div style="grid-column:1/-1"><h4>Compliance gate</h4><p>${esc(P.comp)}</p></div>
    </div></div>
  </div>
  <div class="panel"><div class="panel-h"><h3>Where the talent is: vertical × creator category</h3><span class="sub">Mean fit of the top 5 creators in each category, across every brand in the vertical. Click a row.</span></div>
    <div class="panel-b"><div class="tbl-wrap"><div class="heat" style="grid-template-columns:170px repeat(${niches.length}, minmax(40px,1fr));min-width:860px">
      <div></div>${niches.map(n => `<div class="hh">${esc(NICHE[n])}</div>`).join("")}
      ${D.verticals.map(([k, l], i) => `<button class="hl" data-vert="${k}" aria-pressed="${k === vk}">${esc(l)}</button>${niches.map(n => cell(allHeat[i][n])).join("")}`).join("")}
    </div></div>
    <div class="legend" style="margin-top:10px"><span>Low fit</span><span style="display:inline-flex;gap:2px">${[10, 30, 50, 70, 90].map(p => `<i style="margin:0;width:22px;background:color-mix(in oklab, var(--seq) ${p}%, var(--surface))"></i>`).join("")}</span><span>High fit</span></div></div></div>
  <div class="grid g2">
    <div class="panel"><div class="panel-h"><h3>Top creators across ${esc(VERT[vk])}</h3><span class="sub">Eligible for every brand in the vertical</span></div>
      <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Creator</th><th class="r">Mean fit</th><th class="r">Top-20 for</th><th class="r">Reel</th></tr></thead><tbody>
      ${st.top.slice(0, 10).map(a => `<tr class="click" data-cr="${a.c.id}"><td style="min-width:200px">${who(a.c)}</td><td class="r"><b>${a.avg.toFixed(0)}</b></td><td class="r">${a.top} of ${st.bs.length}</td><td class="r">${fmtINR(a.c.rate.reel)}</td></tr>`).join("")}
      </tbody></table></div></div>
    <div class="panel"><div class="panel-h"><h3>Archetypes that win</h3><span class="sub">Most common category · tier · language among the top 60</span></div>
      <div class="panel-b"><div class="kpi-stack">${archetypes.map(([k, a], i) => { const [n, t, l] = k.split("|"); return `<div><span>0${i + 1}</span><span style="font:inherit;color:var(--ink)"><b>${esc(NICHE[n])}</b> · ${TIER[t].label} · ${esc(l)} <span class="muted">(${a.n} creators, mean fit ${(a.s / a.n).toFixed(0)})</span></span></div>`; }).join("")}</div></div></div>
  </div>
  <div class="panel"><div class="panel-h"><h3>Benchmarks by tier</h3><span class="sub">Medians for creators eligible across ${esc(VERT[vk])}, costs for 1 reel + 2 stories, priced for ${esc(st.bs[0].name)}</span></div>
    <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Tier</th><th class="r">Creators</th><th class="r">Engagement</th><th class="r">Link CTR</th><th class="r">Reel rate</th><th class="r">₹ per TG view</th><th class="r">₹ per engagement</th><th class="r">₹ per click</th></tr></thead><tbody>
    ${bench.map(r => `<tr><td><b>${r.t.label}</b> <span class="muted">${fmtN(r.t.min)}–${fmtN(r.t.max)}</span></td><td class="r">${r.n}</td><td class="r">${pct(r.er, 2)}</td><td class="r">${pct(r.ctr, 2)}</td><td class="r">${fmtINR(r.rate)}</td><td class="r">${fmtRs(r.cpv)}</td><td class="r">${fmtRs(r.cpe)}</td><td class="r">${fmtRs(r.cpc)}</td></tr>`).join("")}
    </tbody></table></div></div>`;
}

/* ---------- campaigns */
function vCampaigns() {
  const cp = D.campaigns.find(x => x.id === S.camp) || D.campaigns[0];
  const st = campStats(cp), b = st.b, t = st.t;
  const isAw = b.objective === "awareness";
  return `
  <div class="camp-pick" role="group" aria-label="Campaign">${D.campaigns.map(x => `<button class="cbtn" data-camp="${x.id}" aria-pressed="${x.id === cp.id}"><b>${esc(BBY[x.brand].name)}${x.live ? ' <span class="dot" style="display:inline-block;margin-left:4px;vertical-align:1px"></span>' : ""}</b><span>${esc(x.title.split(" · ")[0])}</span></button>`).join("")}</div>
  <div class="panel"><div class="panel-b" style="display:flex;gap:18px;flex-wrap:wrap;align-items:center">
    <div class="blogo">${esc(brandMark(b.name))}</div>
    <div style="flex:1;min-width:220px"><div class="eyebrow">${esc(VERT[b.vertical])} · ${OBJ[b.objective].label}</div><h2 style="font:650 22px/1.2 var(--f-display);letter-spacing:-.02em;margin-top:4px">${esc(b.name)}: ${esc(cp.title)}</h2></div>
    <div style="min-width:240px;flex:0 1 320px">
      <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:6px"><span>${cp.live ? `<span class="status warn"><i></i>Live · day ${cp.elapsed} of ${cp.days}</span>` : `<span class="status good"><i></i>Completed · ${cp.days} days</span>`}</span><span class="num">${fmtINR(t.cost)} of ${fmtINR(cp.budget * 1e5)}</span></div>
      <div class="pace"><i style="width:${t.cost / (cp.budget * 1e5) * 100}%;background:var(--accent)"></i><i style="width:${cp.live ? (cp.elapsed / cp.days * 100 - t.cost / (cp.budget * 1e5) * 100) : 0}%;background:var(--neutral-mark);opacity:.6" data-tip="Gap between time elapsed and spend"></i></div>
    </div>
  </div></div>
  <div class="tiles" id="campTiles">
    <div class="tile"><div class="lbl">Verified views</div><div class="val" data-live="views">${fmtN(st.views)}</div><div class="note">${pc(t.api / t.rep)} of the ${fmtN(t.rep)} creators reported</div></div>
    <div class="tile"><div class="lbl">Real people in target group</div><div class="val">${fmtN(t.tg)}</div><div class="note">Deduped, bot-filtered, in TG</div></div>
    <div class="tile"><div class="lbl">Tracked clicks</div><div class="val" data-live="clicks">${fmtN(st.clicks)}</div><div class="note">${fmtRs(t.cost / Math.max(1, st.clicks))} per click</div></div>
    ${isAw ? `<div class="tile"><div class="lbl">Cost per 1,000 TG views</div><div class="val">${fmtINR(t.cost / Math.max(1, t.tg) * 1000)}</div><div class="note">Verified CPM</div></div>`
      : `<div class="tile"><div class="lbl">Verified revenue</div><div class="val" data-live="rev">${fmtINR(st.verified)}</div><div class="note" data-live="orders">${fmtN(st.orders)} orders, net of ${pc(cp.returns)} returns</div></div>`}
    ${isAw ? "" : `<div class="tile"><div class="lbl">Incremental ROAS</div><div class="val">${xf(st.iroas, 2)}</div><div class="note">${xf(st.ltv, 2)} on 12-month value</div></div>`}
    <div class="tile"><div class="lbl">Ad recall lift</div><div class="val">+${st.recall.toFixed(1)}<small>pts</small></div><div class="note">n = ${fmtN(cp.n_lift)} per cell</div></div>
  </div>
  <div class="grid g3">
    <div class="panel span2"><div class="panel-h"><h3>Daily ${S.campMetric === "views" ? "verified views" : S.campMetric}</h3><span class="sub">${cp.live ? "Solid: tracked so far · dashed: forecast" : "Tracked through the run"}</span>
      <div class="right"><div class="seg" role="group" aria-label="Metric">${["views", "clicks", ...(b.cvr ? ["orders"] : [])].map(m => `<button data-cm="${m}" aria-pressed="${S.campMetric === m}">${m[0].toUpperCase() + m.slice(1)}</button>`).join("")}</div></div></div>
      <div class="panel-b"><div id="dailyChart"></div></div></div>
    <div class="panel"><div class="panel-h"><h3>Alerts and actions</h3><span class="sub">What the engine flagged, and what the team did</span></div><div class="panel-b"><div class="alerts">
      ${cp.alerts.map(([sv, txt]) => `<div class="alert"><span class="status ${sv}"><i></i>${{ good: "Opportunity", warning: "Watch", serious: "Act now", critical: "Critical" }[sv]}</span><p>${esc(txt)}</p></div>`).join("")}
    </div></div></div>
  </div>
  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(270px,1fr))">
    <div class="panel"><div class="panel-h"><h3>From reported to real</h3></div><div class="panel-b"><div class="ladder">
      ${[["Creator-reported", "screenshots and dashboards", t.rep], ["API-verified", "pulled with creator consent", t.api], ["Unique viewers", "deduped across creators", t.uniq], ["Real people", "bot and inactive removed", t.real], ["In target group", "age, gender, city tier", t.tg]].map(([k, s, v], i) => `<div class="lad" style="grid-template-columns:120px 1fr 56px"><div class="k">${k}<small>${s}</small></div><div class="t"><i style="width:${v / t.rep * 100}%;background:${i === 4 ? "var(--accent)" : `color-mix(in oklab, var(--accent) ${[18, 34, 50, 66][i]}%, var(--surface))`}"></i></div><div class="v">${fmtN(v)}</div></div>`).join("")}
    </div></div></div>
    ${isAw ? "" : `<div class="panel"><div class="panel-h"><h3>Revenue you can defend</h3><span class="sub">₹, whole campaign</span></div><div class="panel-b"><div id="waterfall"></div></div></div>`}
    <div class="panel"><div class="panel-h"><h3>Brand lift</h3><span class="sub">Control vs exposed, % of respondents</span></div><div class="panel-b"><div id="liftChart"></div></div></div>
    <div class="panel"><div class="panel-h"><h3>Attribution and holdout</h3></div><div class="panel-b" style="display:flex;flex-direction:column;gap:14px">
      <div><div class="mini-h">Where tracked orders came from</div>
        <div class="fitbar" style="height:12px">${[["link", "Tracked links", "--s1"], ["code", "Promo codes", "--s2"], ["affiliate", "Affiliate / marketplace attribution", "--s3"], ["view", "Modelled view-through", "--s4"]].map(([k, l, col]) => `<span style="width:${cp.attr[k] * 100}%;background:var(${col})" data-tip="<b>${l}</b>: ${pc(cp.attr[k])}"></span>`).join("")}</div>
        <div class="legend" style="margin-top:8px">${[["link", "Links", "--s1"], ["code", "Codes", "--s2"], ["affiliate", "Affiliate", "--s3"], ["view", "View-through", "--s4"]].map(([k, l, col]) => `<span><i style="background:var(${col})"></i>${l} ${pc(cp.attr[k])}</span>`).join("")}</div></div>
      ${cp.holdout.lift_pct != null ? `<div><div class="mini-h">Geo holdout · ${cp.holdout.test_cities} test vs ${cp.holdout.control_cities} control cities</div>
        <dl class="kv"><dt>Conversion per 1,000 TG users, test</dt><dd>${cp.holdout.test_rate}</dd><dt>Control</dt><dd>${cp.holdout.control_rate}</dd><dt>Lift</dt><dd><b class="delta-up">+${cp.holdout.lift_pct}%</b></dd><dt>Share of attributed orders that are incremental</dt><dd>${pc(cp.inc_share)}</dd></dl></div>` : `<p class="ink2" style="font-size:12.5px">Awareness campaign: success is judged on verified reach and the brand-lift study, with a quick-commerce sales read in test cities.</p>`}
      <div><div class="mini-h">Forecast accuracy</div><p class="ink2" style="font-size:12.5px">Views forecast error (MAPE) <b>${cp.mape}%</b> across posted creators. Each creator's error feeds the next model version.</p></div>
    </div></div>
  </div>
  <div class="panel" style="overflow:hidden"><div class="panel-h" style="padding-bottom:12px"><h3>Creator leaderboard</h3><span class="sub">Forecast vs actual, sorted by ${isAw ? "views" : "revenue"}</span></div>
      <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Creator</th><th>Status</th><th class="r">Fit</th><th class="r">Cost</th><th class="r">Views · vs forecast</th><th class="r">Clicks</th>${isAw ? "" : '<th class="r">Orders</th><th class="r">Revenue</th><th class="r">ROAS</th>'}</tr></thead><tbody>
      ${[...cp.rows].sort((x, y) => isAw ? (y.a?.views || 0) - (x.a?.views || 0) : (y.a?.rev || 0) - (x.a?.rev || 0)).slice(0, 12).map(r => { const c = CBY[r.id], a = r.a; const dv = a ? (a.views / Math.max(1, r.f.views) - 1) : 0;
        return `<tr class="click" data-cr="${c.id}"><td style="min-width:240px">${who(c)}</td><td>${a ? '<span class="status good"><i></i>Posted</span>' : '<span class="status warn"><i></i>Scheduled</span>'}</td><td class="r">${r.fit}</td><td class="r">${fmtINR(r.cost)}</td><td class="r">${a ? `${fmtN(a.views)} <span class="${dv >= 0 ? "delta-up" : "delta-down"}" style="font-size:12px">${dv >= 0 ? "+" : ""}${pc(dv)}</span>` : `<span class="muted">${fmtN(r.f.views)} fcst</span>`}</td><td class="r">${a ? fmtN(a.clicks) : "–"}</td>${isAw ? "" : `<td class="r">${a ? fmtN(a.orders) : "–"}</td><td class="r">${a ? fmtINR(a.rev) : "–"}</td><td class="r">${a ? xf(a.rev / r.cost, 2) : "–"}</td>`}</tr>`; }).join("")}
      </tbody></table></div></div>
  <p class="view-foot">Simulated campaign. Verified revenue counts orders matched to brand data, net of returns. Incremental ROAS keeps only the share a geo holdout proves. Claimed ROI elsewhere uses EMV at ₹1.4 per reported view and ₹28 per engagement.</p>`;
}
function afterCampaigns() {
  const cp = D.campaigns.find(x => x.id === S.camp) || D.campaigns[0];
  const st = campStats(cp);
  const m = S.campMetric;
  const vals = cp.daily.map(d => d[m]);
  const split = cp.live ? cp.elapsed : null;
  lineChart($("#dailyChart"), { labels: cp.daily.map(d => "Day " + d.d), series: [{ name: m === "views" ? "Verified views" : m[0].toUpperCase() + m.slice(1), vals, color: "--accent", area: true, dashFrom: split }], marker: cp.live ? cp.elapsed - 1 : null });
  // waterfall
  const wf = $("#waterfall");
  if (wf) {
    const gross = st.rev, ret = gross * cp.returns, base = (gross - ret) * (1 - cp.inc_share), inc = st.incr;
    const steps = [["Attributed", gross, 0, "--ink-2"], ["Returns", -ret, gross, "--neutral-mark"], ["Organic baseline", -base, gross - ret, "--neutral-mark"], ["Incremental", inc, 0, "--accent"], ["Spend", st.t.cost, 0, "--s7"]];
    const W = Math.max(280, wf.clientWidth), H = 230, ml = 44, mb = 46, top = 14, ih = H - mb - top;
    const ymax = niceMax(gross * 1.08), bw = Math.min(40, (W - ml) / steps.length * .55), slot = (W - ml) / steps.length;
    const Y = v => top + ih - v / ymax * ih;
    let g = "";
    for (let k = 0; k <= 4; k++) { const v = ymax * k / 4; g += `<line class="${k ? "grid-l" : "base-l"}" x1="${ml}" x2="${W}" y1="${Y(v)}" y2="${Y(v)}"/><text x="${ml - 6}" y="${Y(v) + 4}" text-anchor="end">${fmtINR(v)}</text>`; }
    steps.forEach(([l, v, from, col], i) => {
      const x = ml + slot * i + (slot - bw) / 2, y0 = v >= 0 ? Y(from + v) : Y(from), h = Math.abs(Y(from) - Y(from + v));
      g += `<rect x="${x}" y="${y0}" width="${bw}" height="${Math.max(1, h)}" rx="3" fill="${cssv(col)}" data-tip="<b>${l}</b>: ${v < 0 ? "−" : ""}${fmtINR(Math.abs(v))}"/>`;
      g += `<text x="${x + bw / 2}" y="${y0 - 6}" text-anchor="middle" class="lbl-strong">${v < 0 ? "−" : ""}${fmtINR(Math.abs(v))}</text>`;
      g += `<text x="${x + bw / 2}" y="${H - mb + 16}" text-anchor="middle">${l.split(" ")[0]}</text>${l.includes(" ") ? `<text x="${x + bw / 2}" y="${H - mb + 30}" text-anchor="middle">${l.split(" ").slice(1).join(" ")}</text>` : ""}`;
    });
    wf.innerHTML = `<svg class="chart" viewBox="0 0 ${W} ${H}" width="100%" height="${H}" role="img" aria-label="Revenue waterfall from attributed to incremental">${g}</svg><p class="view-foot">Incremental ${fmtINR(st.incr)} on ${fmtINR(st.t.cost)} spend = <b>${xf(st.iroas, 2)}</b>. Attributed alone would claim ${xf(st.groas, 2)}.</p>`;
  }
  // brand lift dumbbell
  const lc = $("#liftChart");
  if (lc) {
    const W = Math.max(260, lc.clientWidth), rowH = 44, H = cp.lift.length * rowH + 30, ml = 8, mr = 16;
    const X = v => ml + v / 60 * (W - ml - mr);
    let g = "";
    for (const v of [0, 20, 40, 60]) g += `<line class="${v ? "grid-l" : "base-l"}" x1="${X(v)}" x2="${X(v)}" y1="4" y2="${H - 20}"/><text x="${X(v)}" y="${H - 4}" text-anchor="${v ? "middle" : "start"}">${v}%</text>`;
    cp.lift.forEach(([l, c0, c1], i) => {
      const y = 26 + i * rowH;
      g += `<text x="${ml}" y="${y - 10}" class="lbl-ink2">${esc(l)}</text><text x="${W - mr}" y="${y - 10}" text-anchor="end" class="lbl-strong">+${(c1 - c0).toFixed(1)} pts</text>`;
      g += `<line x1="${X(c0)}" x2="${X(c1)}" y1="${y}" y2="${y}" stroke="${cssv("--line-2")}" stroke-width="3" stroke-linecap="round"/>`;
      g += `<circle cx="${X(c0)}" cy="${y}" r="5.5" fill="${cssv("--neutral-mark")}" stroke="${cssv("--surface")}" stroke-width="2" data-tip="<b>${esc(l)}</b><br>Control: ${c0}%"/><circle cx="${X(c1)}" cy="${y}" r="5.5" fill="${cssv("--accent")}" stroke="${cssv("--surface")}" stroke-width="2" data-tip="<b>${esc(l)}</b><br>Exposed: ${c1}%"/>`;
    });
    lc.innerHTML = `<div class="legend" style="margin-bottom:6px"><span><i style="background:var(--neutral-mark)"></i>Control</span><span><i style="background:var(--accent)"></i>Exposed</span></div><svg class="chart" viewBox="0 0 ${W} ${H}" width="100%" height="${H}" role="img" aria-label="Brand lift, control versus exposed">${g}</svg>`;
  }
}

/* ---------- how it works */
const FAMILIES = [
  ["Identity & profile", ["Platforms and handles", "Followers by platform", "Tier", "City and state", "Content languages", "Primary category", "Secondary category", "Content pillars", "Credentials (verified)", "Represent roster status", "Market (India / UAE)", "Creator gender"], "Creator OAuth, Chtrbox CRM"],
  ["Audience", ["Gender split", "Age buckets", "City-tier split", "Top cities", "Audience languages", "Affluence index", "Interest affinities", "Audience overlap between creators", "Follower growth, 12 months", "Growth in last 90 days", "Country split", "Active-follower share", "Device / OS mix", "Peak activity hours"], "Instagram Graph, YouTube Analytics (with consent)"],
  ["Content & culture", ["Cultural codes", "Hook strength (first 3 sec)", "Production quality score", "Format mix (Reel, Story, long-form)", "Posting cadence", "Brand-integration style", "Comment sentiment", "Topics and entities", "Visual brand-safety tags"], "Vision + language models over frames, audio, captions"],
  ["Performance", ["Engagement rate", "Average views", "View-through rate", "Hold at 3 seconds", "Saves per view", "Shares per view", "Comment quality", "Story link CTR", "Reel / bio link CTR", "Past conversion rate", "Recall lift from past studies", "Forecast error history"], "APIs + Chtrbox campaign history"],
  ["Authenticity", ["Real and active follower share", "Suspicious growth spikes", "Engagement-pod signal", "Bot share of comments", "Engagement vs follower consistency", "Sponsored-post saturation", "Overlap with bot clusters"], "Graph analysis, anomaly detection"],
  ["Safety & compliance", ["Brand-safety score", "Flag categories", "ASCI disclosure rate", "Credential verification", "Competitor posts, 120 days", "Exclusivity windows", "Past controversies", "Regulated-category eligibility"], "AI review + human QA, ASCI and SEBI rules"],
  ["Commercials", ["Rate card (Reel, Story, YouTube)", "Negotiated-rate history", "On-time delivery", "Response time", "Payment terms", "TDS (194R / 194J) and GST status"], "Chtrbox ops data"],
  ["Outcomes", ["API-verified views", "Unique reach", "Tracked clicks", "Orders and revenue, net of returns", "Incrementality from holdouts", "Brand lift", "12-month customer value", "Content reuse in paid ads"], "Existing tracking & attribution, brand data, lift studies"],
];
function vHow() {
  const o = S.howObj, w = OBJ[o].w, ws = sum(Object.values(w));
  return `
  <div class="sect-title"><h2>76 data points, eight families</h2><p>Each one has a source, a refresh rate and an owner. Nothing is scraped beyond platform terms.</p></div>
  <div class="fam">${FAMILIES.map(([h, items, src]) => `<div class="famc"><h4>${esc(h)}<span>${items.length}</span></h4><ul>${items.map(x => `<li>${esc(x)}</li>`).join("")}</ul><div class="src">${esc(src)}</div></div>`).join("")}</div>
  <div class="panel"><div class="panel-h"><h3>The fit score</h3><span class="sub">Seven parts, weighted by objective, after hard gates</span><div class="right"><div class="seg" role="group" aria-label="Objective">${Object.entries(OBJ).map(([k, oo]) => `<button data-how="${k}" aria-pressed="${o === k}">${oo.label}</button>`).join("")}</div></div></div>
    <div class="panel-b" style="display:flex;flex-direction:column;gap:14px">
      <div class="formula">Fit = ${DIMS.map(([k, l, col]) => `<span>${"<b style=\"color:var(" + col + ")\">" + (w[k] / ws).toFixed(2) + "</b>"} × ${l.replace(/ & /g, " &amp; ")}</span>`).join(" + ")} <span class="muted">(+ Represent boost ≤ 5)</span></div>
      <div class="grid g3">
        <div><div class="mini-h">How each part is measured</div><ul class="why-list">${[
          ["Audience fit", "overlap of gender, age, city tier and affluence with the brief"], ["Content affinity", "brand's affinity to the creator's primary and secondary category"], ["Culture & language", "best language match plus shared cultural codes"],
          ["Performance", o === "awareness" ? "view-through, 3-second hold, past recall lift" : o === "consideration" ? "engagement rate, saves and shares, sentiment" : "link CTR, trust index, engagement"],
          ["Authenticity", "real-follower share, content quality, sponsored saturation, growth anomalies"], ["Safety & compliance", "brand-safety score and #ad disclosure rate"], ["Cost efficiency", "outcome per rupee, percentile among eligible creators"],
        ].map(([a, b2]) => `<li class="pos">${ic("check")}<span><b>${a}:</b> ${b2}</span></li>`).join("")}</ul><p class="muted" style="font-size:12px;margin-top:8px">Performance metrics are percentiles within the creator's tier, so a nano creator is compared with nano creators.</p></div>
        <div><div class="mini-h">Hard gates, applied before ranking</div><ul class="why-list">${[
          "Real and active followers below 72%", "Brand-safety score below 55", "Posted for a named competitor in the last 60 days", "Finance: investing content without SEBI registration", "Health: technical claims without a medical or nutrition qualification", "Audience outside the campaign's market",
        ].map(x => `<li class="blk">${ic("block")}<span>${x}</span></li>`).join("")}</ul></div>
        <div><div class="mini-h">Forecast, per creator</div><ul class="why-list">${[
          "Views = average views + story views (followers × tier story rate × 2)", "TG views = views × real-follower share × target-group share", "Clicks = views × link CTR × category affinity", "Orders = clicks × brand conversion × creator trust × assist factor", "Confidence band ±12%, ±22% or ±35% by tracked history",
        ].map(x => `<li class="pos">${ic("chev")}<span>${x}</span></li>`).join("")}</ul></div>
      </div>
    </div></div>
  <div class="panel"><div class="panel-h"><h3>The verified-ROI ladder</h3><span class="sub">Every number in a client report carries its level. Only L4 and L5 count as verified.</span></div>
    <div class="panel-b"><div class="steps">${[
      ["L0", "Reported", "Follower counts and creator screenshots."], ["L1", "Verified delivery", "Views pulled by API with creator consent, deduped."], ["L2", "Quality", "Bot-filtered, in target group, watch time."],
      ["L3", "Action", "Tracked clicks, codes, installs, add-to-cart."], ["L4", "Outcome", "Orders and revenue matched to brand data, net of returns."], ["L5", "Incremental", "Holdouts, brand lift, MMM-calibrated iROAS."],
    ].map(([lv, h, p], i) => `<div class="step ${i >= 4 ? "on" : ""}"><div class="lv">${lv}</div><h4>${h}</h4><p>${p}</p></div>`).join("")}</div></div></div>
  <div class="grid g2">
    <div class="panel"><div class="panel-h"><h3>How the model gets better</h3></div><div class="panel-b"><div class="kpi-stack">${[
      ["v0 · Days 0–15", "Rules and expert weights. Gates on. Runs beside strategists."], ["v1 · Days 30–45", "Forecasts calibrated on the first 10+ tracked campaigns. Target MAPE under 30%."],
      ["v2 · Days 60–90", "Learning-to-rank on strategist picks plus outcomes. Overrides become labels."], ["v3 · Months 4–6", "Incrementality-calibrated: holdout and brand-lift results reweight the forecast."],
      ["v4 · Year 1–2", "Pricing model and a creator–brand graph that predicts fit for brands with no history."],
    ].map(([a, b2], i) => `<div><span>0${i + 1}</span><span style="font:inherit;color:var(--ink-2)"><b style="color:var(--ink)">${a}.</b> ${b2}</span></div>`).join("")}</div></div></div>
    <div class="panel"><div class="panel-h"><h3>What it plugs into</h3></div><div class="panel-b"><div class="kpi-stack">${[
      ["In place", "Chtrbox's real-time tracking and attribution: links, codes, affiliate, live dashboards."], ["Add · creator side", "OAuth consent for Instagram and YouTube insights, starting with the Represent roster."],
      ["Add · brand side", "Pixels and conversion APIs, marketplace attribution, app MMPs, returns data."], ["Add · lift", "Platform brand-lift studies plus a panel survey for control vs exposed."],
      ["Add · AI layer", "Vision and language models for tagging, safety review and Hinglish comment sentiment."],
    ].map(([a, b2], i) => `<div><span>0${i + 1}</span><span style="font:inherit;color:var(--ink-2)"><b style="color:var(--ink)">${a}:</b> ${b2}</span></div>`).join("")}</div></div></div>
  </div>`;
}

/* ---------- rollout plan */
const PHASES = [
  ["Days 0–15", "Foundation", ["Inventory data: campaign history, Represent roster, tracking feeds", "Freeze the 76-point schema and the Brand DNA template", "v0 rules model and gates; consent flow for the 104 Represent creators", "Pick 3 pilot brands in Beauty and E-commerce; measure today's baselines"], "Data inventory signed off, baselines measured, 3 pilots agreed"],
  ["Days 16–30", "Shadow mode", ["Engine runs beside strategists on 6–8 live briefs; no change to delivery during festive peak", "Tracking QA becomes a go-live gate: no tracking, no launch", "Design the first holdout and brand-lift study", "Weekly pick-vs-pick review with strategists"], "Engine picks ≥ 30% of final rosters; zero untracked campaigns"],
  ["Days 31–45", "Calibrate", ["Fit forecasts to the first campaign outcomes (v1)", "Tune fraud and safety thresholds on real cases", "Deliver the first Verified ROI report to a pilot brand", "Close the biggest data gaps found in shadow mode"], "Views MAPE < 30%; first L4 report delivered"],
  ["Days 46–60", "Productise", ["Brand-facing ROI report and dashboard template", "Package and price 'Verified ROI' for Brand Solutions", "Train every strategist; add Fashion and FMCG", "15+ campaigns through the engine"], "25% of campaigns at L4+; 2 packages priced and pitched"],
  ["Days 61–90", "Scale", ["50% of campaigns through the engine; v2 learning-to-rank", "Represent utilisation view for talent managers", "Dubai pilot: 300-creator UAE graph for IndiGo-style briefs", "CFO review of the payback model"], "50% of campaigns at L4+; pitch win rate +5 pts"],
  ["Months 4–6", "Prove incrementality", ["Geo holdouts at scale; brand-lift on every awareness brief", "Open regulated verticals (Health, BFSI) behind compliance gates", "Read-only dashboards for the top 10 clients"], "iROAS reported on 80% of conversion spend"],
  ["Year 1", "Standard of proof", ["Every campaign carries an ROI level (L0–L5)", "Creator scorecards inside Represent", "Agency self-serve shortlists", "MENA graph live"], "90% of revenue at L4+; margin +3 pts"],
  ["Year 2", "Platform", ["Creator Intelligence subscriptions for brands and agencies", "Outcome-based pricing on a share of campaigns", "Data partnerships with marketplaces and quick-commerce", "Integrate acquired tech; next markets in GCC"], "Intelligence revenue line ≥ ₹2 Cr; payback reached"],
];
function vPlan() {
  const team = [["Founder's Office lead (programme owner)", 1, 2.0], ["Data engineer", 1, 2.2], ["ML / data scientist", 1, 2.8], ["Full-stack engineers", 2, 3.6], ["Measurement & insights analyst", 1, 1.1], ["Data-ops associates (tagging, QA, consent)", 2, .9], ["Product designer", .5, .7], ["Compliance counsel (retainer)", .2, .6]];
  const kpis = [["Campaigns with a verified ROI report (L4+)", "~0%", "3 pilots", "25%", "50%", "90%"], ["Brief to shortlist", "~3 days", "1 day", "6 hrs", "4 hrs", "2 hrs"], ["Engine picks in final roster", "–", "30%", "50%", "65%", "75%"], ["Views forecast error (MAPE)", "–", "< 35%", "< 25%", "< 20%", "< 15%"], ["Creators with consented data", "0", "1,500", "4,000", "8,000", "25,000"], ["Spend on gated creators", "unknown", "₹0", "₹0", "₹0", "₹0"], ["#ad disclosure on live posts", "~85%", "95%", "98%", "99%", "99%"], ["Pitch win rate, verified-ROI pitches", "baseline", "–", "+5 pts", "+8 pts", "+12 pts"], ["Gross margin per campaign", "FY26", "–", "+1 pt", "+2 pts", "+3 pts"]];
  return `
  <div class="sect-title"><h2>From prototype to standard of proof</h2><p>Days 0–60 overlap the October–March peak, when about 60% of annual revenue lands. The engine runs in shadow mode until it beats strategist picks on held-out briefs.</p></div>
  <div class="panel"><div class="panel-b"><div class="timeline">${PHASES.map(([w, h, items, exit]) => `<div class="ph"><div class="when">${w}<span>${h}</span></div><ul>${items.map(x => `<li>${esc(x)}</li>`).join("")}</ul><div class="exit"><div class="mini-h">Exit criteria</div><b>${esc(exit)}</b></div></div>`).join("")}</div></div></div>
  <div class="grid g2">
    <div class="panel" style="overflow:hidden"><div class="panel-h" style="padding-bottom:12px"><h3>The 90-day pod</h3><span class="sub">New cost; strategists, a talent manager and a sales lead are seconded part-time</span></div>
      <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Role</th><th class="r">FTE</th><th class="r">₹ L / month</th></tr></thead><tbody>${team.map(([r, f, c]) => `<tr><td>${esc(r)}</td><td class="r">${f}</td><td class="r">${c.toFixed(1)}</td></tr>`).join("")}<tr><td><b>People, per month</b></td><td class="r"><b>${sum(team, x => x[1])}</b></td><td class="r"><b>${sum(team, x => x[2]).toFixed(1)}</b></td></tr></tbody></table></div></div>
    <div class="panel"><div class="panel-h"><h3>Budget</h3><span class="sub">Claude's estimate, to validate with the CFO</span></div><div class="panel-b" style="display:flex;flex-direction:column;gap:14px">
      <dl class="kv"><dt>People, 3 months</dt><dd>₹41.7L</dd><dt>Data, cloud, AI inference, lift panels</dt><dd>₹24.0L</dd><dt>Free measurement for 8 pilot brands</dt><dd>₹8.0L</dd><dt>Contingency (10%)</dt><dd>₹7.4L</dd><dt><b>First 90 days</b></dt><dd><b>₹81.1L</b></dd><dt><b>Year 1, all in</b></dt><dd><b>≈ ₹4.0 Cr</b></dd></dl>
      <hr class="hr">
      <div class="mini-h">Base-case value by Year 2 (contribution)</div>
      <dl class="kv"><dt>Brand Solutions +20% (win rate, repeat, deal size)</dt><dd>₹1.8 Cr</dd><dt>Represent utilisation +12%</dt><dd>₹1.0 Cr</dd><dt>Verified-ROI measurement fee (8% of ₹25 Cr)</dt><dd>₹1.4 Cr</dd><dt>Strategist time and fraud avoided (+2 pts margin)</dt><dd>₹1.3 Cr</dd><dt><b>Total, per year</b></dt><dd><b>≈ ₹5.5 Cr</b></dd></dl>
      <p class="muted" style="font-size:12px">Assumptions are Claude's, built on FY26 segment revenue (Represent ₹33.1 Cr, Brand Solutions ₹30.5 Cr, ChtrSocial ₹20.7 Cr). Base-case payback is about 24 months, so money is released in three tranches against the day-90 and month-6 gates.</p>
    </div></div>
  </div>
  <div class="panel" style="overflow:hidden"><div class="panel-h" style="padding-bottom:12px"><h3>KPIs and targets</h3><span class="sub">Baselines are measured in week 1; the North Star is the first row</span></div>
    <div class="tbl-wrap"><table class="tbl"><thead><tr><th>KPI</th><th class="r">Baseline</th><th class="r">Day 30</th><th class="r">Day 60</th><th class="r">Day 90</th><th class="r">Month 12</th></tr></thead><tbody>${kpis.map((r, i) => `<tr><td>${i === 0 ? `<b>${esc(r[0])}</b> <span class="tag accent">North Star</span>` : esc(r[0])}</td>${r.slice(1).map(x => `<td class="r">${esc(x)}</td>`).join("")}</tr>`).join("")}</tbody></table></div></div>
  <div class="panel"><div class="panel-h"><h3>Guardrails</h3><span class="sub">Set before the first brief, reviewed monthly</span></div><div class="panel-b"><div class="fam" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">${[
    ["Consent first", "Creator data only through OAuth, purpose-limited and deletable. Built for the DPDP Rules (notified Nov 2025; core duties by May 2027)."],
    ["Humans decide", "The engine shortlists; strategists choose. Every override is logged with a reason."],
    ["Explainable scores", "Every score shows its seven parts. No silent rejections: gated creators see why."],
    ["Gates before ranking", "Fraud, safety, competitor conflicts and regulatory eligibility are checked before any score."],
    ["Roster boost capped", "Represent creators get at most +5, shown on the score and disclosed to brands."],
    ["No ROI promises early", "Forecasts carry bands. 'Verified' is used only for L4 and L5 numbers."],
    ["Regulated categories", "ASCI Addendum II credentials, SEBI finfluencer rules, IRDAI, and health-claim review."],
    ["Protect the peak", "Shadow mode during Oct–Mar until accuracy is proven. Delivery is never the experiment."],
  ].map(([h, p]) => `<div class="famc"><h4>${esc(h)}</h4><p class="ink2" style="font-size:12.5px;margin-top:6px">${esc(p)}</p></div>`).join("")}</div></div></div>
  <p class="view-foot">The full plan, with SOPs, RACI, risk register and the 1–2 year roadmap, is in Creator-Intelligence-Engine-GTM-Plan.pdf.</p>`;
}

/* ---------------------------------------------------------------- render + events */
function render() {
  hideTip();
  const v = VIEWS.find(x => x[0] === S.view) || VIEWS[0];
  $$(".nav button").forEach(bn => bn.setAttribute("aria-current", bn.dataset.view === S.view ? "page" : "false"));
  $("#crumbT").textContent = v[1]; $("#crumbS").textContent = v[2];
  const el = view();
  el.innerHTML = { overview: vOverview, match: vMatch, discover: vDiscover, verticals: vVerticals, campaigns: vCampaigns, how: vHow, plan: vPlan }[S.view]();
  if (S.view === "overview") afterOverview();
  if (S.view === "match") afterMatch();
  if (S.view === "discover") renderDiscover();
  if (S.view === "campaigns") afterCampaigns();
}
function go(v, opts = {}) {
  S.view = v; if (opts.centre) S.centre = opts.centre;
  try { if (location.hash.slice(1) !== v) history.replaceState(null, "", "#" + v); } catch { /* sandboxed */ }
  render(); scrollTo({ top: 0 });
}
function rerenderMatch(keepScroll = true) {
  const y = scrollY;
  render();
  if (keepScroll) scrollTo({ top: y });
}

document.addEventListener("click", e => {
  const t = e.target;
  const nav = t.closest(".nav button"); if (nav) return go(nav.dataset.view);
  const g = t.closest("[data-go]"); if (g) return go(g.dataset.go, { centre: g.dataset.centre });
  const cr = t.closest("[data-cr]"); if (cr) return openDrawer(cr.dataset.cr);
  const ob = t.closest("[data-obj]"); if (ob) { S.obj = ob.dataset.obj; S.w = { ...OBJ[S.obj].w }; return rerenderMatch(); }
  const ti = t.closest("[data-tier]"); if (ti) { const k = ti.dataset.tier; S.tiers.has(k) ? S.tiers.delete(k) : S.tiers.add(k); return rerenderMatch(); }
  const pl = t.closest("[data-plat]"); if (pl) { const k = pl.dataset.plat; S.platforms.has(k) ? S.platforms.delete(k) : S.platforms.add(k); return rerenderMatch(); }
  const ce = t.closest("[data-centre]"); if (ce && S.view === "match") { S.centre = ce.dataset.centre; return rerenderMatch(); }
  if (t.closest("#resetW")) { S.w = { ...OBJ[S.obj].w }; S.boost = 0; return rerenderMatch(); }
  if (t.closest("#copyBrief")) {
    const { res } = matchRes(); const plan = buildPlan(res, S.budget * 1e5);
    const txt = `${res.b.name} · ${OBJ[S.obj].label} · ${fmtINR(S.budget * 1e5)}\n` + plan.list.map((r, i) => `${i + 1}. ${r.c.name} (${r.c.id}) · ${NICHE[r.c.niche]} · ${TIER[r.c.tier].label} · fit ${r.total.toFixed(0)} · ${fmtINR(r.p.cost)}`).join("\n");
    const bn = t.closest("#copyBrief");
    const done = ok => { bn.innerHTML = ok ? `${ic("check")} Copied ${plan.list.length} creators` : "Copy unavailable here"; setTimeout(() => (bn.innerHTML = `${ic("copy")} Copy shortlist`), 1800); };
    try { navigator.clipboard.writeText(txt).then(() => done(true), () => done(false)); } catch { done(false); }
    return;
  }
  const ex = t.closest("[data-ex]"); if (ex) { S.query = ex.dataset.ex; $("#q").value = S.query; S.dPage = 0; return renderDiscover(); }
  const so = t.closest("[data-sort]"); if (so) { const k = so.dataset.sort; S.dSort = [k, S.dSort[0] === k ? -S.dSort[1] : (k === "name" || k === "rate" ? 1 : -1)]; return renderDiscover(); }
  const pg = t.closest("[data-page]"); if (pg) { S.dPage += +pg.dataset.page; return renderDiscover(); }
  const ve = t.closest("[data-vert]"); if (ve) { S.vertical = ve.dataset.vert; store.set("vertical", S.vertical); return rerenderMatch(); }
  const bc = t.closest("[data-brand]"); if (bc) { setBrand(bc.dataset.brand); return go("match"); }
  const cb = t.closest("[data-camp]"); if (cb) { S.camp = cb.dataset.camp; store.set("camp", S.camp); return render(); }
  const cm = t.closest("[data-cm]"); if (cm) { S.campMetric = cm.dataset.cm; return rerenderMatch(); }
  const hw = t.closest("[data-how]"); if (hw) { S.howObj = hw.dataset.how; return rerenderMatch(); }
  if (t.closest("#scrim")) return closeDrawer();
  if (t.closest("#themeBtn")) {
    const root = document.documentElement;
    const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark"; store.set("theme", root.dataset.theme);
    $("#themeBtn").innerHTML = ic(dark ? "moon" : "sun");
    return;
  }
  if (t.closest("#fullBtn")) { const d = document.documentElement; try { document.fullscreenElement ? document.exitFullscreen() : d.requestFullscreen?.().catch(() => {}); } catch { /* not allowed */ } }
});
document.addEventListener("change", e => {
  if (e.target.id === "brandSel" || e.target.id === "dBrand") { setBrand(e.target.value); S.view === "discover" ? (render()) : rerenderMatch(false); }
});
let inputTimer;
document.addEventListener("input", e => {
  const t = e.target;
  if (t.dataset.w) { S.w = { ...S.w, [t.dataset.w]: +t.value }; t.nextElementSibling.textContent = t.value; clearTimeout(inputTimer); inputTimer = setTimeout(() => rerenderMatch(), 120); }
  if (t.id === "boost") { S.boost = +t.value; t.nextElementSibling.textContent = "+" + t.value; clearTimeout(inputTimer); inputTimer = setTimeout(() => rerenderMatch(), 120); }
  if (t.id === "budget") { S.budget = +t.value; clearTimeout(inputTimer); inputTimer = setTimeout(() => rerenderMatch(), 90); }
  if (t.id === "q") { S.query = t.value; S.dPage = 0; clearTimeout(inputTimer); inputTimer = setTimeout(renderDiscover, 120); }
});
document.addEventListener("toggle", e => { if (e.target.classList?.contains("tune")) store.set("tuneOpen", e.target.open); }, true);
document.addEventListener("keydown", e => {
  if (e.key === "Escape" && S.drawer) return closeDrawer();
  if (e.target.matches("input, select, textarea")) return;
  const v = VIEWS.find(x => x[3] === e.key); if (v && !e.metaKey && !e.ctrlKey && !e.altKey) return go(v[0]);
  if (e.key === "/") { e.preventDefault(); if (S.view !== "discover") go("discover"); setTimeout(() => $("#q")?.focus(), 0); }
});
let rz; addEventListener("resize", () => { clearTimeout(rz); rz = setTimeout(() => { if (["overview", "match", "campaigns"].includes(S.view)) rerenderMatch(); }, 160); });

/* live feed for the running campaign (simulated) */
const liveCamp = D.campaigns.find(x => x.live);
function tickLive() {
  if (!liveCamp) return;
  const t = liveCamp.totals, f = 1 / (liveCamp.elapsed * 24 * 60 / 2.6) * (0.6 + Math.random() * .9);
  const dv = Math.round(t.api * f), dc = Math.round(t.clicks * f + Math.random() * .8), dord = Math.random() < t.orders * f ? 1 : 0;
  S.live.views += dv; S.live.clicks += dc; S.live.orders += dord; S.live.rev += dord * BBY[liveCamp.brand].aov * (0.7 + Math.random() * .6);
  if (S.view === "campaigns" && S.camp === liveCamp.id) {
    const st = campStats(liveCamp);
    const upd = (k, txt) => { const el = $(`[data-live="${k}"]`); if (el && el.textContent !== txt) { el.textContent = txt; el.classList.remove("flash"); void el.offsetWidth; el.classList.add("flash"); } };
    upd("views", fmtN(st.views)); upd("clicks", fmtN(st.clicks)); upd("rev", fmtINR(st.verified)); upd("orders", `${fmtN(st.orders)} orders, net of ${pc(liveCamp.returns)} returns`);
  }
}
setInterval(tickLive, 2600);

window.__cie = { scoreBrand, buildPlan, vanityPlan, BBY, OBJ, C };

/* boot */
function boot() {
  const th = store.get("theme", null);
  if (th) document.documentElement.dataset.theme = th;
  $("#nav").innerHTML = VIEWS.map(([k, l, , key]) => `<button data-view="${k}" aria-current="false">${ic(k)}<span>${l}</span><kbd>${key}</kbd></button>`).join("");
  const dark = document.documentElement.dataset.theme ? document.documentElement.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  $("#themeBtn").innerHTML = ic(dark ? "sun" : "moon");
  $("#fullBtn").innerHTML = ic("full");
  if (liveCamp) $("#livePill").innerHTML = `<span class="dot"></span>Live · ${esc(BBY[liveCamp.brand].name)} · day ${liveCamp.elapsed} of ${liveCamp.days}`;
  $("#livePill").addEventListener("click", () => { S.camp = liveCamp.id; go("campaigns"); });
  const h = location.hash.slice(1);
  if (VIEWS.some(v => v[0] === h)) S.view = h;
  matchMedia("(prefers-color-scheme: dark)").addEventListener?.("change", () => render());
  new MutationObserver(() => render()).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  render();
}
boot();
})();
