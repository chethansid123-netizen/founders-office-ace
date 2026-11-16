/* App core: helpers, the store (Claude-hosted database when available, this browser otherwise), and all derived numbers. */

const DAY = 864e5;
const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const uid = p => p + "_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
const clone = o => JSON.parse(JSON.stringify(o));
const todayStr = () => new Date().toISOString().slice(0, 10);
const inr = n => "₹" + Math.round(n || 0).toLocaleString("en-IN");
const inrShort = n => { n = Math.round(n || 0); const a = Math.abs(n);
  if (a >= 1e7) return "₹" + (n / 1e7).toFixed(2).replace(/\.?0+$/, "") + " Cr";
  if (a >= 1e5) return "₹" + (n / 1e5).toFixed(1).replace(/\.0$/, "") + " L";
  return inr(n); };
const pct = (a, b) => b ? Math.round(100 * a / b) : 0;
const median = arr => { if (!arr.length) return null; const s = [...arr].sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
const fmtDate = iso => iso ? new Date(iso).toLocaleDateString("en-IN", { day: "numeric", month: "short" }) : "";
const fmtDateTime = iso => iso ? new Date(iso).toLocaleString("en-IN", { day: "numeric", month: "short", hour: "numeric", minute: "2-digit" }) : "";
function ago(iso) { if (!iso) return "never"; const m = (Date.now() - new Date(iso).getTime()) / 6e4;
  if (m < 1) return "just now"; if (m < 60) return Math.round(m) + " min ago"; if (m < 1440) return Math.round(m / 60) + " h ago";
  const d = Math.round(m / 1440); return d + (d === 1 ? " day ago" : " days ago"); }
function mins(m) { if (m == null) return "–"; if (m < 60) return Math.round(m) + " min"; if (m < 1440) return (m / 60).toFixed(1).replace(/\.0$/, "") + " h"; return (m / 1440).toFixed(1).replace(/\.0$/, "") + " d"; }
function dueInfo(d) { if (!d) return { t: "No date", cls: "muted", n: null };
  const n = Math.round((new Date(d + "T00:00:00").getTime() - new Date(todayStr() + "T00:00:00").getTime()) / DAY);
  if (n < 0) return { t: "Overdue " + (-n) + (n === -1 ? " day" : " days"), cls: "crit", n };
  if (n === 0) return { t: "Today", cls: "warn", n }; if (n === 1) return { t: "Tomorrow", cls: "", n };
  return { t: "In " + n + " days", cls: "muted", n }; }
const by = (arr, k) => arr.reduce((m, x) => { const v = typeof k === "function" ? k(x) : x[k]; (m[v] = m[v] || []).push(x); return m; }, {});
const stageOf = k => STAGES.find(s => s.key === k) || STAGES[0];
const srcOf = k => SOURCES.find(s => s.key === k) || { key: k, name: k || "Unknown", warmth: 5 };
const first = name => String(name || "").trim().split(/\s+/)[0] || "there";

/* ---------- Store ---------- */
const LS_KEY = "yuj-revenue-desk.v1";
const COLLS = ["leads", "accounts", "cohorts", "spend", "config"];
const Store = { mode: "starting", ready: false, note: "", data: { leads: {}, accounts: {}, cohorts: {}, spend: {}, config: {} }, db: null, subs: [], chain: Promise.resolve(), tok: {},
  pend: { leads: {}, accounts: {}, cohorts: {}, spend: {}, config: {} } };
let onStoreChange = () => {};

function saveLocal() { try { localStorage.setItem(LS_KEY, JSON.stringify(Store.data)); } catch (e) { /* storage unavailable: keep working in memory */ } }
function loadLocal() { try { const raw = localStorage.getItem(LS_KEY); if (raw) { const d = JSON.parse(raw); COLLS.forEach(c => { Store.data[c] = d[c] || {}; }); return true; } } catch (e) { /* ignore */ } return false; }

/* One write at a time, in order. Until a queued write lands, its document is overlaid on every snapshot so the screen never flickers back. */
function overlay(c, m) { const p = Store.pend[c]; for (const id in p) { if (p[id] === null) delete m[id]; else m[id] = p[id]; } return m; }
function dbWrite(coll, id, doc) {
  const k = coll + "/" + id, token = {}; Store.pend[coll][id] = doc; Store.tok[k] = token;
  Store.chain = Store.chain.then(() => doc ? Store.db.collection(coll).doc(id).set(doc) : Store.db.collection(coll).doc(id).delete()).catch(e => {
    const code = e && e.code;
    toast(code === "quota_exceeded" ? "Storage is full. Export and remove old leads." : code === "invalid_argument" ? "You have view-only access, so this change was not saved." : "Could not save just now. It will retry on your next change.", "crit");
  }).then(() => { if (Store.tok[k] === token) { delete Store.pend[coll][id]; delete Store.tok[k]; } });
}
function put(coll, doc) {
  const d = clone(doc); if (!d.id) d.id = uid(coll[0]);
  Store.data[coll] = Object.assign({}, Store.data[coll], { [d.id]: d });
  if (Store.mode === "db") dbWrite(coll, d.id, d); else saveLocal();
  return d;
}
function del(coll, id) {
  const m = Object.assign({}, Store.data[coll]); delete m[id]; Store.data[coll] = m;
  if (Store.mode === "db") dbWrite(coll, id, null); else saveLocal();
}
function conf() { return Store.data.config.main || { id: "main" }; }
function setConf(patch) { put("config", Object.assign({}, conf(), patch, { id: "main" })); }
function A() { const c = conf().assume || {}; const a = Object.assign({}, DEFAULTS, c); a.conv = Object.assign({}, DEFAULTS.conv, c.conv || {}); return a; }
function ruleOn(k) { const r = conf().rules || {}; return r[k] !== false; }

async function initStore() {
  let db = null;
  try { if (window.claude && typeof window.claude.use === "function") db = await window.claude.use("db"); } catch (e) { db = null; }
  if (!db) {
    Store.mode = "local";
    const had = loadLocal();
    if (!had && !conf().sampleCleared) loadSample(true);
    Store.ready = true; onStoreChange(); return;
  }
  Store.mode = "db"; Store.db = db;
  const seen = {}; let left = COLLS.length;
  const timer = setTimeout(() => { if (!Store.ready) { Store.note = "Your saved pipeline has not loaded yet. It will appear here as soon as the connection answers."; onStoreChange(); } }, 10000);
  COLLS.forEach(c => {
    const done = () => { if (!seen[c]) { seen[c] = true; left--; if (left === 0) { Store.ready = true; Store.note = ""; clearTimeout(timer); } } };
    Store.subs.push(db.collection(c).onSnapshot(snap => {
      const m = {}; snap.docs.forEach(d => { const v = d.data(); if (v) m[d.id] = Object.assign(clone(v), { id: d.id }); });
      Store.data[c] = overlay(c, m); done(); onStoreChange();
    }, err => { done(); Store.note = err && err.code === "revoked" ? "Access to the saved pipeline was withdrawn." : "The saved pipeline could not be read."; onStoreChange(); }));
  });
}
function loadSample(silent) {
  const s = sampleWorkspace(Date.now());
  s.leads.forEach(l => { l.lastOpenStage = FLOW.includes(l.stage) ? l.stage : (Object.keys(l.diag || {}).length ? "diagnosed" : "contacted"); put("leads", l); });
  s.cohorts.forEach(c => put("cohorts", c)); s.spend.forEach(x => put("spend", x));
  if (!silent) toast("Sample workspace loaded");
}
function clearSample() {
  ["leads", "cohorts", "spend", "accounts"].forEach(c => Object.values(Store.data[c]).filter(x => x.sample).forEach(x => del(c, x.id)));
  setConf({ sampleCleared: true });
}
const leads = () => Object.values(Store.data.leads);
const hasSample = () => leads().some(l => l.sample) || Object.values(Store.data.cohorts).some(c => c.sample);

/* ---------- Derived: price, offer, score ---------- */
function listPrice(prog, a) { a = a || A();
  if (prog === "p2") return a.priceP2; if (prog === "combo") return Math.round((a.priceP1 + a.priceP2) * (1 - a.comboDiscountPct / 100)); return a.priceP1; }
function offerCalc(prog, leverKeys, a) { a = a || A();
  const list = listPrice(prog, a), parts = (leverKeys || []).map(k => { const L = LEVERS.find(x => x.key === k); return L ? { key: k, name: L.name, pct: L.maxPct, buys: L.buys } : null; }).filter(Boolean);
  const raw = parts.reduce((s, p) => s + p.pct, 0), capped = Math.min(raw, a.stackCapPct);
  const net = Math.round(list * (1 - capped / 100));
  const seats = prog === "combo" ? 2 : 1, cost = a.varCostPerSeat * seats;
  const margin = net - cost - a.cacTarget, marginPct = net ? Math.round(100 * margin / net) : 0;
  const verdict = marginPct < a.minMarginPct ? "approve" : raw > a.stackCapPct ? "capped" : "ok";
  return { list, parts, raw, pct: capped, discount: list - net, net, cost, margin, marginPct, verdict };
}
function leadNet(l, a) { return offerCalc(l.prog || "p1", l.offer && l.offer.levers || [], a).net; }

function leadScore(l) {
  const parts = [];
  const seg = SEG[l.seg], core = seg && (seg.group === "core" || seg.group === "buyer");
  parts.push({ g: "Fit", k: "Segment", pts: seg ? (core ? 15 : 10) : 5, max: 15, why: seg ? (core ? "Core segment" : "Adjacent segment") : "Segment not set" });
  const y = +l.yrs || 0;
  parts.push({ g: "Fit", k: "Experience", pts: !y ? 5 : (y >= 3 && y <= 12) ? 10 : 6, max: 10, why: !y ? "Not known" : y + " years" });
  const cs = l.coStage || "";
  parts.push({ g: "Fit", k: "Company", pts: /Series [ABC]|Unicorn|GCC/.test(cs) ? 10 : cs === "Seed" ? 7 : cs ? 5 : 4, max: 10, why: cs || "Not known" });
  parts.push({ g: "Fit", k: "Who pays", pts: l.payer === "employer" || l.payer === "split" ? 10 : l.payer === "self" ? 7 : 4, max: 10, why: (PAYERS.find(p => p.key === l.payer) || PAYERS[0]).name });
  parts.push({ g: "Fit", k: "Seniority", pts: l.sen && l.sen !== "ic" ? 5 : 3, max: 5, why: (SENIORITY.find(s => s.key === l.sen) || {}).name || "Not known" });
  parts.push({ g: "Intent", k: "Source", pts: srcOf(l.src).warmth, max: 15, why: srcOf(l.src).name });
  const sig = (l.signals || []).length;
  parts.push({ g: "Intent", k: "Signals", pts: Math.min(20, sig * 4), max: 20, why: sig + (sig === 1 ? " signal" : " signals") });
  const d = l.lastTouchAt ? (Date.now() - new Date(l.lastTouchAt).getTime()) / DAY : 99;
  parts.push({ g: "Intent", k: "Recency", pts: d <= 2 ? 10 : d <= 7 ? 6 : d <= 14 ? 3 : 0, max: 10, why: l.lastTouchAt ? "Last touch " + ago(l.lastTouchAt) : "No touch yet" });
  const du = l.next && l.next.due ? dueInfo(l.next.due) : null;
  parts.push({ g: "Intent", k: "Next step", pts: du && du.n >= 0 ? 5 : 0, max: 5, why: du ? du.t : "None set" });
  const fit = parts.filter(p => p.g === "Fit").reduce((s, p) => s + p.pts, 0), intent = parts.filter(p => p.g === "Intent").reduce((s, p) => s + p.pts, 0);
  const total = fit + intent;
  return { fit, intent, total, band: total >= 70 ? "hot" : total >= 45 ? "warm" : "cool", parts };
}
function diagSummary(l) {
  const d = l.diag || {}, keys = Object.keys(d);
  if (!keys.length) return null;
  const rows = DIAG.filter(x => d[x.key] != null).map(x => ({ ...x, v: +d[x.key] }));
  const p1 = rows.filter(r => r.prog === "p1"), p2 = rows.filter(r => r.prog === "p2");
  const avg = r => r.length ? r.reduce((s, x) => s + x.v, 0) / r.length : null;
  const weak = [...rows].sort((a, b) => a.v - b.v)[0], strong = [...rows].sort((a, b) => b.v - a.v)[0];
  const a1 = avg(p1), a2 = avg(p2);
  let rec = null;
  if (a1 != null && a2 != null) rec = (a1 <= 1.4 && a2 <= 1.4) ? "combo" : a2 < a1 ? "p2" : "p1"; else if (a2 != null) rec = "p2"; else if (a1 != null) rec = "p1";
  const allHigh = rows.length >= 4 && rows.every(r => r.v === 2);
  return { rows, a1, a2, weak, strong, rec, allHigh };
}
function reachedIdx(l) { const k = FLOW.includes(l.stage) ? l.stage : (l.lastOpenStage || "new"); return Math.max(0, FLOW.indexOf(k)); }
function touchCount(l) { return (l.log || []).filter(x => x.type !== "note" && x.type !== "stage").length; }
function nextCadence(l) { const n = touchCount(l); return CADENCE[Math.min(n, CADENCE.length - 1)]; }

/* ---------- Derived: metrics and alerts ---------- */
function metrics() {
  const a = A(), L = leads(), open = L.filter(l => OPEN_STAGES.includes(l.stage));
  const byStage = Object.fromEntries(STAGES.map(s => [s.key, L.filter(l => l.stage === s.key)]));
  const weekAgo = Date.now() - 7 * DAY;
  const newWeek = L.filter(l => new Date(l.createdAt).getTime() >= weekAgo).length;
  const fr = L.filter(l => l.firstTouchAt).map(l => (new Date(l.firstTouchAt) - new Date(l.createdAt)) / 6e4).filter(x => x >= 0);
  const waiting = L.filter(l => l.stage === "new" && !l.firstTouchAt);
  const within = fr.filter(x => x <= a.slaMins).length;
  const funnel = FLOW.slice(0, -1).map((k, i) => {
    const reached = L.filter(l => reachedIdx(l) >= i).length, moved = L.filter(l => reachedIdx(l) > i).length;
    return { key: k, name: stageOf(k).name, next: stageOf(FLOW[i + 1]).name, reached, moved, here: byStage[k].length, rate: reached ? Math.round(100 * moved / reached) : null, target: a.conv[k] };
  });
  const enrolled = byStage.enrolled, pipeline = open.reduce((s, l) => s + leadNet(l, a), 0),
    weighted = open.reduce((s, l) => s + leadNet(l, a) * stageOf(l.stage).prob / 100, 0),
    revenue = enrolled.reduce((s, l) => s + leadNet(l, a), 0);
  const spendBy = {}; Object.values(Store.data.spend).forEach(s => { spendBy[s.channel] = (spendBy[s.channel] || 0) + (+s.amount || 0); });
  const sources = SOURCES.map(s => { const ls = L.filter(l => l.src === s.key), en = ls.filter(l => l.stage === "enrolled" || l.stage === "committed").length, sp = spendBy[s.key] || 0;
    return { ...s, n: ls.length, won: en, rate: ls.length ? Math.round(100 * en / ls.length) : null, spend: sp, cac: en ? Math.round(sp / en) : null, open: ls.filter(l => OPEN_STAGES.includes(l.stage)).length }; }).filter(s => s.n || s.spend);
  const totalSpend = Object.values(spendBy).reduce((s, x) => s + x, 0);
  const blk = {}; L.forEach(l => { if (l.blocker && l.blocker !== "none") blk[l.blocker] = (blk[l.blocker] || 0) + 1; });
  const blockers = Object.entries(blk).map(([k, n]) => ({ key: k, name: (BLK[k] || {}).name || k, n, lost: L.filter(l => l.blocker === k && l.stage === "lost").length })).sort((x, y) => y.n - x.n);
  const segs = SEGMENTS.map(s => { const ls = L.filter(l => l.seg === s.key); return { key: s.key, name: s.name, n: ls.length, won: ls.filter(l => l.stage === "enrolled" || l.stage === "committed").length, open: ls.filter(l => OPEN_STAGES.includes(l.stage)).length }; }).filter(s => s.n);
  const discounts = L.filter(l => l.offer && (l.stage === "committed" || l.stage === "enrolled")).map(l => offerCalc(l.prog, l.offer.levers, a).pct);
  const cohorts = Object.values(Store.data.cohorts).map(c => cohortStats(c, L, a)).sort((x, y) => new Date(x.start) - new Date(y.start));
  return { a, L, open, byStage, newWeek, frMedian: median(fr), frWithin: fr.length ? pct(within, fr.length) : null, waiting, funnel, enrolled, pipeline, weighted, revenue,
    sources, totalSpend, cac: (enrolled.length + byStage.committed.length) ? Math.round(totalSpend / (enrolled.length + byStage.committed.length)) : null,
    blockers, segs, avgDiscount: discounts.length ? Math.round(discounts.reduce((s, x) => s + x, 0) / discounts.length * 10) / 10 : null, cohorts };
}
function cohortStats(c, L, a) {
  const mine = L.filter(l => l.cohortId === c.id), en = mine.filter(l => l.stage === "enrolled"), co = mine.filter(l => l.stage === "committed"), of = mine.filter(l => l.stage === "proposal");
  const days = Math.round((new Date(c.start).getTime() - Date.now()) / DAY), target = +c.target || +c.seats || 0, filled = en.length + co.length;
  const windowDays = 56, elapsed = Math.max(0, Math.min(1, 1 - days / windowDays)), expected = Math.round(target * elapsed);
  const listRev = (+c.seats || 0) * listPrice(c.prog, a), pool = Math.round(listRev * a.poolPct / 100);
  const used = mine.filter(l => l.offer && (l.stage === "committed" || l.stage === "enrolled")).reduce((s, l) => s + offerCalc(l.prog, l.offer.levers, a).discount, 0);
  const risk = en.filter(l => l.health && ((+l.health.att || 0) < 70 || (days < -14 && (+l.health.work || 0) < 2)));
  const refer = en.filter(l => days <= -21 && l.health && !l.health.referralAsked);
  return { ...c, mine, en, co, of, days, target, filled, expected, behind: days > 0 && days <= windowDays && filled < expected, running: days <= 0 && days > -((PROGRAMS[c.prog] || PROGRAMS.p1).weeks * 7), pool, used, risk, refer,
    revenue: [...en, ...co].reduce((s, l) => s + leadNet(l, a), 0) };
}
function alerts(m) {
  m = m || metrics(); const a = m.a, out = [], now = Date.now();
  const add = (rule, o) => { if (ruleOn(rule)) { const R = RULES.find(r => r.key === rule); out.push(Object.assign({ rule, sev: R.sev, name: R.name, act: R.act }, o)); } };
  m.L.forEach(l => {
    const sc = leadScore(l).total, openL = OPEN_STAGES.includes(l.stage), last = l.lastTouchAt ? (now - new Date(l.lastTouchAt).getTime()) / DAY : null;
    if (l.stage === "new" && !l.firstTouchAt) { const w = (now - new Date(l.createdAt).getTime()) / 6e4; if (w > a.slaMins) add("sla", { lead: l, sc, d: "Waiting " + mins(w) + ". Target is " + a.slaMins + " min." }); else add("sla", { lead: l, sc, sev: "warn", d: "New " + mins(w) + " ago. " + Math.max(0, Math.round(a.slaMins - w)) + " min left on the clock." }); return; }
    if (openL && l.next && l.next.due && dueInfo(l.next.due).n < 0) add("overdue", { lead: l, sc, d: (l.next.t || "Next step") + " · " + dueInfo(l.next.due).t.toLowerCase() });
    else if (openL && (!l.next || !l.next.due)) add("nostep", { lead: l, sc, d: "At " + stageOf(l.stage).name + " with nothing scheduled." });
    if (openL && last != null && last > a.staleDays && !(l.next && l.next.due && dueInfo(l.next.due).n >= 0)) add("stale", { lead: l, sc, d: "No touch for " + Math.round(last) + " days. Next: " + nextCadence(l).t.toLowerCase() + "." });
    if (l.stage === "proposal" && l.offer && l.offer.sentAt && (now - new Date(l.offer.sentAt).getTime()) / DAY > a.offerNudgeDays) add("offer", { lead: l, sc, d: "Offer sent " + ago(l.offer.sentAt) + "." });
    if ((l.stage === "proposal" || (openL && last != null && last > 7)) && (!l.blocker || l.blocker === "none")) add("noblocker", { lead: l, sc, d: "No reason recorded for the delay." });
    if (sc >= 70 && ["new", "contacted", "diagnosed"].includes(l.stage)) add("hot", { lead: l, sc, d: "Score " + sc + " and no mentor call yet." });
    if (l.stage === "nurture" && l.next && l.next.due && dueInfo(l.next.due).n <= 0) add("nurture", { lead: l, sc, d: "Call-back date reached." + (l.quote ? " They said: " + l.quote : "") });
  });
  const co = by(m.L.filter(l => l.company && l.stage !== "lost"), l => l.company.trim().toLowerCase());
  Object.values(co).filter(g => g.length >= 2).forEach(g => add("team", { company: g[0].company, sc: 60, d: g.length + " people: " + g.map(l => first(l.name)).join(", ") + ".", lead: g.sort((x, y) => reachedIdx(y) - reachedIdx(x))[0] }));
  m.funnel.forEach(f => { if (f.reached >= 8 && f.rate != null && f.rate < f.target * 0.7) add("leak", { sc: 50, route: "funnel", d: f.name + " → " + f.next + " is " + f.rate + "% so far against a " + f.target + "% target." }); });
  m.cohorts.forEach(c => {
    if (c.behind) add("pace", { sc: 90, route: "cohorts", d: c.name + ": " + c.filled + " of " + c.target + " filled with " + c.days + " days left. On pace would be " + c.expected + "." });
    c.risk.forEach(l => add("risk", { lead: l, sc: 80, d: "Attendance " + (l.health.att || 0) + "%, " + (l.health.work || 0) + ((+l.health.work || 0) === 1 ? " piece" : " pieces") + " of work in." }));
    c.refer.forEach(l => add("refer", { lead: l, sc: 55, d: "Three weeks in" + (l.health.nps ? ", would-recommend " + l.health.nps + "/10" : "") + "." }));
  });
  const rank = { crit: 0, warn: 1, good: 2, info: 3 };
  return out.sort((x, y) => (rank[x.sev] - rank[y.sev]) || (y.sc - x.sc));
}
function funnelMath(targetSeats, a) { a = a || A(); const steps = FLOW.slice(0, -1); let n = targetSeats; const need = { enrolled: targetSeats };
  for (let i = steps.length - 1; i >= 0; i--) { n = n / (a.conv[steps[i]] / 100); need[steps[i]] = Math.ceil(n); } return need; }

/* ---------- Message merge ---------- */
function mergeVars(l) {
  const a = A(), seg = SEG[l.seg] || SEGMENTS[0], P = PROGRAMS[l.prog] || PROGRAMS.p1, ds = diagSummary(l), o = offerCalc(l.prog || "p1", l.offer && l.offer.levers || [], a);
  const ev = EVID[seg.teachEv] || {};
  const co = Object.values(Store.data.cohorts).filter(c => c.prog === (l.prog === "combo" ? "p1" : l.prog) && new Date(c.start) > new Date()).sort((x, y) => new Date(x.start) - new Date(y.start))[0];
  return { first: first(l.name), name: l.name || "", role: (l.role || seg.name).toLowerCase(), company: l.company || "your company", hook: seg.hooks[0], teach: seg.teach, source: ev.src ? ev.src + ", " + ev.year : "",
    rep: a.repName || "[your name]", mentor: "[mentor]", program: P.name, weeks: P.weeks, price: inr(o.net) + (o.pct ? " (list " + inr(o.list) + ", " + o.pct + "% scholarship)" : ""), deposit: inr(a.depositAmount),
    calendar: a.calendarLink || "[your booking link]", strong: ds && ds.strong ? ds.strong.name.toLowerCase() : "[strength]", weak: ds && ds.weak ? ds.weak.name.toLowerCase() : "[gap]",
    quote: l.quote || "[their sentence]", cohort: co ? fmtDate(co.start) : "[date]", stage: l.coStage || "" };
}
function merge(text, l) { const v = mergeVars(l); return String(text).replace(/\{(\w+)\}/g, (m, k) => v[k] != null ? v[k] : m); }

/* ---------- CSV ---------- */
function toCsv(rows) { return rows.map(r => r.map(v => { v = String(v == null ? "" : v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }).join(",")).join("\n"); }
function parseCsv(text) { const rows = []; let row = [], cur = "", q = false;
  for (let i = 0; i < text.length; i++) { const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c; }
    else if (c === '"') q = true; else if (c === ",") { row.push(cur); cur = ""; } else if (c === "\n" || c === "\r") { if (c === "\r" && text[i + 1] === "\n") i++; row.push(cur); cur = ""; if (row.some(x => x.trim())) rows.push(row); row = []; } else cur += c; }
  row.push(cur); if (row.some(x => x.trim())) rows.push(row); return rows; }
function guessSegment(role) { const r = String(role || "").toLowerCase();
  const m = [["founder's office|chief of staff|strategy", "fo"], ["head of product|vp product|director of product|cpo|group product", "pl"], ["design manager|head of design|design lead|design director|ux lead", "dm"], ["research", "uxr"], ["product manager|product owner|\\bpm\\b|apm", "pm"], ["design|ux|ui", "ux"], ["program|project|delivery|scrum", "pgm"], ["brand|marketing|growth|category", "mkt"], ["sales|business development|account|customer success", "sales"], ["operations|ops|process|experience manager", "ops"], ["engineer|developer|tech lead|architect", "eng"], ["consult|analyst", "consult"], ["founder|ceo|coo|cxo", "founder"]];
  for (const [re, k] of m) if (new RegExp(re).test(r)) return k; return ""; }
function leadsFromCsv(text) {
  const rows = parseCsv(text); if (rows.length < 2) return [];
  const head = rows[0].map(h => h.trim().toLowerCase()), col = (...names) => head.findIndex(h => names.some(n => h === n || h.includes(n)));
  const ix = { name: col("name"), role: col("title", "role", "designation"), company: col("company", "organisation", "organization"), email: col("email"), phone: col("phone", "mobile", "whatsapp"), linkedin: col("linkedin"), city: col("city", "location"), src: col("source"), stage: col("company stage", "funding") };
  const nowIso = new Date().toISOString();
  return rows.slice(1).map(r => { const g = k => ix[k] >= 0 ? (r[ix[k]] || "").trim() : ""; const role = g("role"), sv = g("src").toLowerCase();
    const src = (SOURCES.find(s => s.key === sv || s.name.toLowerCase() === sv) || {}).key || "cold";
    return newLead({ name: g("name"), role, seg: guessSegment(role), company: g("company"), email: g("email"), phone: g("phone"), linkedin: g("linkedin"), city: g("city"), src, coStage: CO_STAGES.find(s => s.toLowerCase() === g("stage").toLowerCase()) || "", createdAt: nowIso }); }).filter(l => l.name);
}
function newLead(o) { const now = new Date().toISOString();
  return Object.assign({ id: uid("l"), name: "", role: "", seg: "", company: "", coStage: "", city: "", src: "inbound", email: "", phone: "", linkedin: "", waOptIn: false, yrs: "", sen: "", payer: "unknown",
    stage: "new", prog: "p1", blocker: "none", quote: "", goal: "", signals: [], diag: {}, next: { t: "Call within the hour", due: todayStr() }, offer: null, createdAt: now, firstTouchAt: "", lastTouchAt: "", stageAt: now, lastOpenStage: "new", log: [], lostReason: "", cohortId: "", health: null }, o || {}); }
const LEAD_CSV_HEAD = ["Name", "Role", "Segment", "Company", "Company stage", "City", "Source", "Stage", "Program", "Score", "Blocker", "Who pays", "Next step", "Due", "Email", "Phone", "LinkedIn", "Created", "Last touch", "Their sentence"];
function leadsCsv(list) { return toCsv([LEAD_CSV_HEAD].concat(list.map(l => [l.name, l.role, (SEG[l.seg] || {}).name || "", l.company, l.coStage, l.city, srcOf(l.src).name, stageOf(l.stage).name, (PROGRAMS[l.prog] || {}).short || "", leadScore(l).total, (BLK[l.blocker] || {}).name || "", (PAYERS.find(p => p.key === l.payer) || {}).name || "", l.next && l.next.t || "", l.next && l.next.due || "", l.email, l.phone, l.linkedin, (l.createdAt || "").slice(0, 10), (l.lastTouchAt || "").slice(0, 10), l.quote]))); }
