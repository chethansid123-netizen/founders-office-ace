/* Shell, shared components, Claude capabilities (ask Claude, Gmail draft, Clay search, file save) and event wiring. */

const UI = {
  route: "today", tabs: {}, drawer: null, modal: null, toastT: null,
  f: { q: "", stage: "open", seg: "", src: "", sort: "score" }, leadsView: "table",
  acc: { stage: "Series A", type: "", q: "", mine: false }, segKey: "pm",
  scr: { seg: "pm", call: "explain" }, obj: "gap", calc: { prog: "p1", levers: [], seats: 0 }, ev: { q: "", only: "" },
  ai: {}, aiBusy: {}, clay: { state: "idle", list: [], size: "51-200", industry: "Software Development", kw: "" }, drTab: "now"
};
const Cap = { sample: null, mcp: null, downloads: null, checked: false, hosted: !!(window.claude && typeof window.claude.use === "function") };

const NAV = [
  { g: "Operate", items: [["today", "Today"], ["leads", "Leads"], ["accounts", "Accounts"], ["cohorts", "Cohorts"]] },
  { g: "Playbook", items: [["segments", "Segments"], ["funnel", "Funnel"], ["scripts", "Scripts"], ["objections", "Objections"], ["pricing", "Pricing"]] },
  { g: "Know", items: [["market", "Market"], ["data", "Data"], ["evidence", "Evidence"]] },
  { g: "System", items: [["automation", "Automation"], ["setup", "Setup"]] }
];
const TITLES = {
  today: ["Today", "What to do first, and how the funnel is doing"], leads: ["Leads", "Every person, one record"], accounts: ["Accounts", "Funded companies and who to reach inside them"],
  cohorts: ["Cohorts", "Seats, pace, learners and referrals"], segments: ["Segments", "Thirteen kinds of buyer and how to speak to each"], funnel: ["Funnel", "Top, middle, bottom and after: goals, plays and the 90-day plan"],
  scripts: ["Scripts", "Calls, messages and prompts"], objections: ["Objections", "The real reason behind a no, and what to do about each"], pricing: ["Pricing", "Scholarships that buy something, and the numbers behind a cohort"],
  market: ["Market", "Competitors, position, channels and the buyer's psychology"], data: ["Data", "What is captured at each touch, and why"], evidence: ["Evidence", "Every number in this tool, with its source and its limits"],
  automation: ["Automation", "Rules that watch the pipeline, and what connects"], setup: ["Setup", "Assumptions, your answers, import and export"]
};
const I = {
  today: '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>',
  leads: '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 5.2a3.2 3.2 0 0 1 0 5.6M18 14.4c1.8.9 3 2.7 3 4.9"/>',
  accounts: '<path d="M4 21V5l8-2v18M12 9l8 2v10M2 21h20M7.5 8.5h1M7.5 12.5h1M7.5 16.5h1M15.5 14h1M15.5 17.5h1"/>',
  cohorts: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  segments: '<rect x="3" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.5"/>',
  funnel: '<path d="M3 4h18l-7 8v7l-4 2v-9z"/>', scripts: '<path d="M4 5h16v11H9l-5 4z"/>',
  objections: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 1-1 1.7M12 17h.01"/>',
  pricing: '<path d="M7 5h10M7 9h10M7 5c5.5 0 6.5 8 0 8l7 7"/>', market: '<path d="M3 20l5-13 4 8 3-5 6 10z"/>',
  data: '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
  evidence: '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM4 21h15"/>', automation: '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
  setup: '<path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/>',
  plus: '<path d="M12 5v14M5 12h14"/>', x: '<path d="M6 6l12 12M18 6L6 18"/>', copy: '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h9"/>',
  ext: '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>', check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  spark: '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z"/>',
  mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>', arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>', search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>'
};
const ico = (n, cls) => '<svg class="ico ' + (cls || "") + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (I[n] || "") + "</svg>";

/* ---------- components ---------- */
const pill = (t, cls) => '<span class="pill ' + (cls || "") + '">' + esc(t) + "</span>";
const evShort = k => EV_SHORT[k] || (EVID[k] ? EVID[k].src.split(/[,(:]/)[0].trim() + " " + EVID[k].year : "");
const evChip = k => EVID[k] ? '<button type="button" class="ev" data-act="ev" data-k="' + k + '" title="Open the source">' + esc(evShort(k)) + "</button>" : "";
const copyBtn = (text, label) => '<button type="button" class="btn sm ghost" data-act="copy" data-copy="' + esc(text) + '">' + ico("copy") + (label || "Copy") + "</button>";
function tabs(view, list) { const cur = UI.tabs[view] || list[0][0];
  return '<div class="tabs" role="tablist">' + list.map(([k, t]) => '<button type="button" role="tab" aria-selected="' + (k === cur) + '" data-act="tab" data-v="' + view + '" data-k="' + k + '">' + esc(t) + "</button>").join("") + "</div>"; }
const tabOf = (view, d) => UI.tabs[view] || d;
function barRow(label, value, max, opts) { opts = opts || {}; const w = max ? Math.max(0, Math.min(100, 100 * value / max)) : 0;
  return '<div class="bar-row"><div class="bar-l">' + label + '</div><div class="bar-t"><div class="bar-f ' + (opts.cls || "") + '" style="width:' + w.toFixed(1) + '%"></div>' + (opts.tick != null ? '<i class="bar-tick" style="left:' + Math.min(100, opts.tick) + '%" title="Target ' + opts.tick + '%"></i>' : "") + '</div><div class="bar-v">' + (opts.text != null ? opts.text : value) + "</div></div>"; }
const empty = (t, d, action) => '<div class="empty"><h3>' + esc(t) + "</h3><p>" + d + "</p>" + (action || "") + "</div>";
const opt = (v, t, cur) => '<option value="' + esc(v) + '"' + (String(v) === String(cur) ? " selected" : "") + ">" + esc(t) + "</option>";
const scoreDot = sc => '<span class="score ' + sc.band + '" title="Fit ' + sc.fit + " + intent " + sc.intent + '">' + sc.total + "</span>";
const stagePill = k => { const s = stageOf(k); return pill(s.name, "st-" + s.band); };
function toast(msg, cls) { const el = document.getElementById("toast"); if (!el) return; el.textContent = msg; el.className = "toast show " + (cls || ""); clearTimeout(UI.toastT); UI.toastT = setTimeout(() => { el.className = "toast"; }, 3200); }

/* ---------- shell ---------- */
function renderShell() {
  const m = Store.ready ? metrics() : null, al = m ? alerts(m) : [];
  const urgent = al.filter(a => a.sev === "crit").length;
  document.getElementById("nav").innerHTML = NAV.map(g => '<div class="nav-g">' + g.g + "</div>" + g.items.map(([k, t]) =>
    '<a href="#' + k + '" class="' + (UI.route === k ? "on" : "") + '"' + (UI.route === k ? ' aria-current="page"' : "") + ">" + ico(k) + "<span>" + t + "</span>" +
    (k === "today" && urgent ? '<b class="badge">' + urgent + "</b>" : k === "leads" && m ? '<b class="count">' + m.open.length + "</b>" : "") + "</a>").join("")).join("");
  const T = TITLES[UI.route] || TITLES.today;
  document.getElementById("pageT").textContent = T[0]; document.getElementById("pageS").textContent = T[1];
  document.getElementById("saveState").innerHTML = Store.mode === "db" ? '<i class="dot good"></i>Saved to your Claude workspace' : Store.mode === "local" ? '<i class="dot"></i>Saved in this browser only' : '<i class="dot"></i>Loading';
}
function render() {
  UI.dirty = false; renderShell();
  const v = document.getElementById("view");
  if (!Store.ready) { v.innerHTML = '<div class="empty"><h3>Loading your pipeline</h3><p>' + esc(Store.note || "Leads, accounts and cohorts appear here in a moment.") + "</p></div>"; return; }
  const banner = hasSample() ? '<div class="banner"><div><strong>Sample workspace.</strong> ' + leads().filter(l => l.sample).length + ' made-up people at made-up companies, so every screen shows how it works. Company data in Accounts is real.</div><button type="button" class="btn sm" data-act="clearSample">Remove samples and start with real leads</button></div>' : "";
  const note = Store.note ? '<div class="banner warn"><div>' + esc(Store.note) + "</div></div>" : "";
  v.innerHTML = note + banner + (VIEWS[UI.route] || VIEWS.today)();
  renderDrawer(); renderModal();
}
function safeRender() { const a = document.activeElement;
  if (a && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName) && a.closest("#view,#drawer,#modal") && a.type !== "checkbox" && a.type !== "radio") { UI.dirty = true; return; }
  render(); }
function go(route) { if (location.hash.slice(1) !== route) location.hash = route; else { UI.route = route; render(); } }
function readHash() { const h = location.hash.slice(1); UI.route = TITLES[h] ? h : "today"; }

/* ---------- Claude capabilities ---------- */
async function initCaps() {
  const use = n => Cap.hosted ? Promise.resolve(window.claude.use(n)).catch(() => null) : Promise.resolve(null);
  const r = await Promise.all([use("sample"), use("mcp"), use("downloads")]);
  Cap.sample = r[0]; Cap.mcp = r[1]; Cap.downloads = r[2]; Cap.checked = true; safeRender();
}
const AI_ERR = { not_granted: "Claude is not switched on for this page.", sampling_disabled: "Claude is not available on this account.", rate_limited: "Claude is busy. Try again in a minute.", refused: "Claude declined that request. Change what you are asking for.", session_expired: "Sign in to Claude again.", prompt_too_large: "Too much text. Try with fewer leads." };
async function askClaude(key, prompt) {
  if (!Cap.sample || UI.aiBusy[key]) return;
  UI.aiBusy[key] = new AbortController(); UI.ai[key] = "Thinking…"; paintAi(key);
  try { const r = await Cap.sample(prompt, { signal: UI.aiBusy[key].signal, cache: false, onText: u => { UI.ai[key] = u.text; paintAi(key); } }); UI.ai[key] = r.text + (r.truncated ? "\n\n(Cut short. Ask for less at a time.)" : ""); }
  catch (e) { const code = e && e.code; UI.ai[key] = (e && e.text ? e.text + "\n\n" : "") + (code === "cancelled" ? "" : (AI_ERR[code] || "That did not work. Try again.")); }
  UI.aiBusy[key] = null; paintAi(key);
}
function paintAi(key) { const el = document.getElementById("ai-" + key); if (!el) return; el.hidden = !UI.ai[key]; const out = el.querySelector(".ai-out"); if (out) out.textContent = UI.ai[key] || ""; const st = el.querySelector("[data-act=aiStop]"); if (st) st.hidden = !UI.aiBusy[key]; }
function aiBox(key) { return '<div class="ai" id="ai-' + key + '"' + (UI.ai[key] ? "" : " hidden") + '><div class="ai-h">' + ico("spark") + "<span>Claude</span><span class=\"sp\"></span>" +
  '<button type="button" class="btn sm ghost" data-act="aiStop" data-k="' + key + '"' + (UI.aiBusy[key] ? "" : " hidden") + '>Stop</button><button type="button" class="btn sm ghost" data-act="aiCopy" data-k="' + key + '">' + ico("copy") + 'Copy</button></div><div class="ai-out">' + esc(UI.ai[key] || "") + "</div></div>"; }
function mcpMsg(e, name) { const c = e && e.code;
  if (c === "needs_reauth") return "Reconnect " + name + " in claude.ai Settings → Connectors.";
  if (c === "server_not_connected" || c === "selection_required") return "Add " + name + " in claude.ai Settings → Connectors, then try again.";
  if (c === "not_in_manifest") return name + " is switched off for this page.";
  if (c === "approval_required") return "This needs your approval. Try again and allow it.";
  if (c === "blocked_by_policy") return "Your organisation's policy blocks this.";
  if (c === "tool_error") return name + " said: " + String(e.message || "it could not do that").slice(0, 160);
  return name + " did not answer. Check there before trying again."; }
async function gmailDraft(lead, subject, body) {
  if (!Cap.mcp) return; if (!lead.email) { toast("Add this person's email first", "crit"); return; }
  toast("Creating the draft…");
  try { await Cap.mcp.callTool("Gmail", "create_draft", { to: [lead.email], subject: subject || "", body });
    logTouch(lead.id, { type: "email", outcome: "Sent material", note: "Draft created in Gmail: " + (subject || "(no subject)") }, true); toast("Draft is in your Gmail drafts. Read it, then send."); }
  catch (e) { toast(mcpMsg(e, "Gmail"), "crit"); }
}
async function claySearch() {
  if (!Cap.mcp) return; const c = UI.clay; c.state = "busy"; render();
  let q = 'select from companies where locations.any(country_name = "India") and company_size = "' + c.size + '" and industry = "' + c.industry + '"';
  if (c.kw.trim()) q += ' and description contains "' + c.kw.trim().replace(/"/g, "") + '"';
  q += " limit 30";
  try { const r = await Cap.mcp.callTool("Clay", "search-companies", { dslQuery: q }); const p = r && r.payload;
    c.list = p && p.companies ? Object.values(p.companies).filter(x => x && x.name) : []; c.state = "done"; }
  catch (e) { c.state = "err"; c.msg = mcpMsg(e, "Clay"); }
  render();
}
async function saveFile(filename, text) {
  if (Cap.downloads) { try { await Cap.downloads.save({ filename, data: text }); toast("Saved " + filename); } catch (e) { if (!e || e.code !== "declined") openModal({ kind: "text", title: filename, text }); } return; }
  if (Cap.hosted) { openModal({ kind: "text", title: filename, text }); return; }
  try { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([text], { type: "text/plain" })); a.download = filename; document.body.appendChild(a); a.click(); a.remove(); }
  catch (e) { openModal({ kind: "text", title: filename, text }); }
}
function copyText(text) {
  const done = () => toast("Copied");
  const fallback = () => { try { const t = document.createElement("textarea"); t.value = text; t.setAttribute("readonly", ""); t.style.position = "fixed"; t.style.opacity = "0"; document.body.appendChild(t); t.select(); document.execCommand("copy"); t.remove(); done(); } catch (e) { openModal({ kind: "text", title: "Copy this", text }); } };
  try { navigator.clipboard.writeText(text).then(done, fallback); } catch (e) { fallback(); }
}

/* ---------- modal ---------- */
function openModal(m) { UI.modal = m; renderModal(); const el = document.querySelector("#modal input,#modal textarea,#modal select"); if (el) el.focus(); }
function closeModal() { UI.modal = null; renderModal(); }
function renderModal() {
  const wrap = document.getElementById("modal"), sc = document.getElementById("scrim2"), m = UI.modal;
  if (!m) { wrap.hidden = true; sc.hidden = true; wrap.innerHTML = ""; return; }
  const body = (MODALS[m.kind] || (() => ""))(m);
  wrap.innerHTML = '<div class="modal-h"><h2>' + esc(m.title || "") + '</h2><button type="button" class="icon-btn" data-act="closeModal" aria-label="Close">' + ico("x") + '</button></div><div class="modal-b">' + body + "</div>";
  wrap.hidden = false; sc.hidden = false;
}
const MODALS = {
  text: m => '<p class="muted">Select all and copy.</p><textarea class="mono" rows="14" readonly id="m-text">' + esc(m.text) + "</textarea>",
  ev: m => { const e = EVID[m.k]; if (!e) return "";
    return '<p class="lead-p">' + esc(e.claim) + '</p><dl class="dl"><dt>Source</dt><dd>' + esc(e.src) + ", " + e.year + (e.url ? ' <a class="xl" href="' + esc(e.url) + '" target="_blank" rel="noopener">Open' + ico("ext") + "</a>" : "") + "</dd><dt>How solid</dt><dd>" +
      (e.status === "checked" ? pill("Checked Nov 2026", "good") + " Looked up while building this tool." : pill("Established source", "info") + " Cited from the literature. Open it before quoting a number.") + "</dd>" +
      (e.caveat ? "<dt>Limits</dt><dd>" + esc(e.caveat) + "</dd>" : "") + "<dt>Use it for</dt><dd>" + esc(e.use) + "</dd></dl>" +
      '<div class="row-end">' + copyBtn(e.claim + " (" + e.src + ", " + e.year + ")", "Copy with source") + "</div>"; }
};

/* ---------- events ---------- */
const ACT = {}, CHG = {}, INP = {};
function wire() {
  document.addEventListener("click", e => { const el = e.target.closest("[data-act]"); if (!el) return; const fn = ACT[el.dataset.act]; if (fn) { if (el.tagName === "A" && el.getAttribute("href") === "#") e.preventDefault(); fn(el, e); } });
  document.addEventListener("change", e => { const el = e.target.closest("[data-chg]"); if (!el) return; const fn = CHG[el.dataset.chg]; if (fn) fn(el, e); });
  document.addEventListener("input", e => { const el = e.target.closest("[data-inp]"); if (!el) return; const fn = INP[el.dataset.inp]; if (fn) fn(el, e); });
  document.addEventListener("submit", e => { e.preventDefault(); const fn = ACT[e.target.dataset.submit]; if (fn) fn(e.target, e); });
  document.addEventListener("focusout", () => setTimeout(() => { if (UI.dirty) safeRender(); }, 60));
  document.addEventListener("keydown", e => { if (e.key === "Escape") { if (UI.modal) closeModal(); else if (UI.drawer) ACT.closeDrawer(); }
    if (e.key === "/" && !/^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement || {}).tagName || "")) { const s = document.getElementById("gsearch"); if (s) { e.preventDefault(); s.focus(); } } });
  window.addEventListener("hashchange", () => { readHash(); render(); window.scrollTo(0, 0); });
  document.getElementById("scrim").addEventListener("click", () => ACT.closeDrawer());
  document.getElementById("scrim2").addEventListener("click", closeModal);
}
Object.assign(ACT, {
  tab: el => { UI.tabs[el.dataset.v] = el.dataset.k; render(); },
  go: el => go(el.dataset.r),
  ev: el => openModal({ kind: "ev", k: el.dataset.k, title: "Source" }),
  copy: el => copyText(el.dataset.copy || ""),
  closeModal: () => closeModal(),
  clearSample: () => { clearSample(); toast("Samples removed. The pipeline is yours."); render(); },
  loadSample: () => { loadSample(); render(); },
  aiStop: el => { const c = UI.aiBusy[el.dataset.k]; if (c) c.abort(); },
  aiCopy: el => copyText(UI.ai[el.dataset.k] || "")
});
INP.gsearch = el => { UI.f.q = el.value; if (UI.route !== "leads") { go("leads"); setTimeout(() => { const s = document.getElementById("gsearch"); if (s) { s.focus(); s.setSelectionRange(s.value.length, s.value.length); } }, 0); } else paintLeads(); };
