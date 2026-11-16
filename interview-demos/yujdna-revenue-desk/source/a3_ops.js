/* Operating screens: Today, Leads, and the lead panel. */
const VIEWS = {};

/* ---------- Today ---------- */
VIEWS.today = () => {
  const m = metrics(), al = alerts(m), a = m.a;
  if (!m.L.length) return empty("No leads yet", "Add your first lead, import a list, or load the sample workspace to see how the tool works.",
    '<div class="row-c"><button type="button" class="btn primary" data-act="addLead">' + ico("plus") + 'Add a lead</button><button type="button" class="btn" data-act="importLeads">Import a list</button><button type="button" class="btn ghost" data-act="loadSample">Load the sample workspace</button></div>');
  const nextC = m.cohorts.find(c => c.days > 0);
  const kpi = (label, val, note, cls) => '<div class="kpi ' + (cls || "") + '"><div class="kpi-l">' + label + '</div><div class="kpi-v">' + val + '</div><div class="kpi-n">' + note + "</div></div>";
  const frCls = m.waiting.length ? "crit" : m.frMedian != null && m.frMedian > a.slaMins ? "warn" : "";
  const kpis = '<div class="kpis">' +
    kpi("First response", m.frMedian == null ? "–" : mins(m.frMedian), (m.waiting.length ? "<b>" + m.waiting.length + " waiting now.</b> " : "") + (m.frWithin == null ? "No calls logged yet" : m.frWithin + "% inside " + a.slaMins + " min"), frCls) +
    kpi("New this week", m.newWeek, m.open.length + " open in total") +
    kpi("Open pipeline, weighted", inrShort(m.weighted), inrShort(m.pipeline) + " at list, before stage odds") +
    (nextC ? kpi("Next cohort", nextC.filled + "<small> / " + nextC.target + "</small>", esc(nextC.name) + " · " + nextC.days + " days · " + nextC.of.length + " offers out", nextC.behind ? "crit" : "") : kpi("Next cohort", "–", 'Add cohort dates in <a href="#cohorts">Cohorts</a>')) +
    kpi("Cost per learner", m.cac == null ? "–" : inrShort(m.cac), m.totalSpend ? inrShort(m.totalSpend) + " spent · target " + inrShort(a.cacTarget) : "Log spend in Cohorts to see this", m.cac != null && m.cac > a.cacTarget ? "warn" : "") + "</div>";
  const seenL = new Set(), top = al.filter(x => { const k = x.rule === "team" ? "co:" + x.company : x.lead ? x.lead.id : x.rule + x.d; if (seenL.has(k)) return false; seenL.add(k); return true; });
  const todo = top.slice(0, 12).map(x => '<li class="todo ' + x.sev + '"><div class="todo-m"><div class="todo-t">' + esc(x.name) + (x.lead ? ' · <button type="button" class="link" data-act="openLead" data-id="' + x.lead.id + '">' + esc(x.company && x.rule === "team" ? x.company : x.lead.name) + "</button>" : "") +
    (x.lead && x.rule !== "team" ? ' <span class="muted">' + esc((SEG[x.lead.seg] || {}).name || x.lead.role || "") + (x.lead.company ? ", " + esc(x.lead.company) : "") + "</span>" : "") + '</div><div class="todo-d">' + esc(x.d) + '</div></div><div class="todo-a">' +
    (x.lead ? '<button type="button" class="btn sm" data-act="openLead" data-id="' + x.lead.id + '">' + esc(x.act.split(".")[0]) + "</button>" : '<a class="btn sm" href="#' + x.route + '">' + esc(x.act.split(".")[0]) + "</a>") + "</div></li>").join("");
  const fmax = Math.max(1, ...m.funnel.map(f => f.reached));
  const funnel = m.funnel.map(f => { const low = f.reached >= 8 && f.rate != null && f.rate < f.target * 0.7;
    return '<div class="fn-row"><div class="fn-n"><b>' + esc(f.name) + '</b><span class="muted">' + f.reached + " reached · " + f.here + ' here now</span></div><div class="fn-b"><div class="bar-t"><div class="bar-f ' + (low ? "crit" : "") + '" style="width:' + (f.rate || 0) + '%"></div><i class="bar-tick" style="left:' + f.target + '%"></i></div></div><div class="fn-v ' + (low ? "crit-t" : "") + '">' + (f.rate == null ? "–" : f.rate + "%") + '<span class="muted"> / ' + f.target + "%</span></div></div>"; }).join("");
  const bmax = Math.max(1, ...m.blockers.map(b => b.n));
  const blockers = m.blockers.length ? m.blockers.map(b => barRow('<button type="button" class="link" data-act="openObj" data-k="' + b.key + '">' + esc(b.name) + "</button>", b.n, bmax, { text: b.n + (b.lost ? ' <span class="muted">(' + b.lost + " lost)</span>" : "") })).join("") : '<p class="muted">Tag a reason on any lead that hesitates. The pattern shows up here after ten or so.</p>';
  const src = m.sources.length ? '<div class="tbl-w"><table class="tbl"><thead><tr><th>Source</th><th class="num">Leads</th><th class="num">Seats</th><th class="num">Rate</th><th class="num">Spend</th><th class="num">Per seat</th></tr></thead><tbody>' +
    m.sources.sort((x, y) => y.n - x.n).map(s => "<tr><td>" + esc(s.name) + '</td><td class="num">' + s.n + '</td><td class="num">' + s.won + '</td><td class="num">' + (s.rate == null ? "–" : s.rate + "%") + '</td><td class="num">' + (s.spend ? inrShort(s.spend) : "–") + '</td><td class="num">' + (s.cac == null ? "–" : inrShort(s.cac)) + "</td></tr>").join("") + "</tbody></table></div>" : "";
  const coach = Cap.sample ? '<button type="button" class="btn sm" data-act="coach">' + ico("spark") + "Ask Claude to review the pipeline</button>" : "";
  return kpis + '<div class="split"><section class="panel"><div class="panel-h"><h2>Do first</h2><span class="muted">' + top.length + " to act on · " + al.length + " flags from " + RULES.filter(r => ruleOn(r.key)).length + ' rules</span><span class="sp"></span>' + coach + '</div>' + aiBox("coach") +
    (todo ? '<ul class="todos">' + todo + "</ul>" : '<p class="pad muted">Nothing needs you right now.</p>') + (top.length > 12 ? '<p class="pad muted">' + (top.length - 12) + " more after these. One line per person; open a lead to see everything flagged on it.</p>" : "") + "</section>" +
    '<div class="stack"><section class="panel"><div class="panel-h"><h2>Funnel so far</h2><span class="muted">share that moved on · tick is target</span></div><div class="pad">' + funnel + '<p class="fine">Open leads can still move, so early numbers read low. Targets are starting benchmarks; change them in <a href="#setup">Setup</a>. ' + evChip("bench") + "</p></div></section>" +
    '<section class="panel"><div class="panel-h"><h2>Why people hesitate</h2></div><div class="pad">' + blockers + "</div></section></div></div>" +
    '<section class="panel"><div class="panel-h"><h2>Where leads come from</h2><span class="muted">seats = deposit paid or enrolled</span></div>' + src + "</section>";
};
ACT.coach = () => { const m = metrics();
  const rows = m.open.map(l => [l.name, (SEG[l.seg] || {}).name || l.role, l.coStage, stageOf(l.stage).name, "score " + leadScore(l).total, "blocker: " + ((BLK[l.blocker] || {}).name || "none"), "last touch " + ago(l.lastTouchAt), "next: " + (l.next && l.next.t || "none") + " " + (l.next && l.next.due || "")].join(" | ")).join("\n");
  askClaude("coach", AI_PROMPTS[5].p + "\n\nStage conversion so far vs target: " + m.funnel.map(f => f.name + " " + (f.rate == null ? "n/a" : f.rate + "%") + "/" + f.target + "%").join(", ") + ".\nCohorts: " + m.cohorts.map(c => c.name + " " + c.filled + "/" + c.target + " in " + c.days + " days").join("; ") + ".\nKeep it under 180 words, plain text.\n\nPipeline:\n" + rows); };
ACT.openObj = el => { UI.obj = el.dataset.k; go("objections"); };

/* ---------- Leads ---------- */
function filteredLeads() {
  const f = UI.f, q = f.q.trim().toLowerCase();
  let L = leads().filter(l => (f.stage === "open" ? OPEN_STAGES.includes(l.stage) : f.stage === "all" ? true : l.stage === f.stage) && (!f.seg || l.seg === f.seg) && (!f.src || l.src === f.src) &&
    (!q || [l.name, l.company, l.role, l.city, l.email].join(" ").toLowerCase().includes(q)));
  const sc = l => leadScore(l).total, due = l => l.next && l.next.due ? l.next.due : "9999";
  L.sort(f.sort === "due" ? (x, y) => due(x).localeCompare(due(y)) : f.sort === "new" ? (x, y) => new Date(y.createdAt) - new Date(x.createdAt) : f.sort === "touch" ? (x, y) => new Date(x.lastTouchAt || 0) - new Date(y.lastTouchAt || 0) : (x, y) => sc(y) - sc(x));
  return L;
}
function leadListHtml() {
  const L = filteredLeads();
  if (!L.length) return empty("Nobody matches", "Change the filters, or add a lead.");
  if (UI.leadsView === "board") {
    return '<div class="board">' + FLOW.map(k => { const col = L.filter(l => l.stage === k), s = stageOf(k);
      return '<div class="col"><div class="col-h"><b>' + esc(s.name) + '</b><span class="count">' + col.length + '</span></div>' + (col.map(l => { const sc = leadScore(l), d = l.next && l.next.due ? dueInfo(l.next.due) : null;
        return '<button type="button" class="card" data-act="openLead" data-id="' + l.id + '"><div class="card-t">' + scoreDot(sc) + "<b>" + esc(l.name) + "</b></div><div class=\"muted\">" + esc(l.role || "") + (l.company ? " · " + esc(l.company) : "") + "</div>" +
          (l.next && l.next.t ? '<div class="card-n"><span class="' + (d ? d.cls + "-t" : "") + '">' + esc(d ? d.t : "") + "</span> " + esc(l.next.t) + "</div>" : '<div class="card-n warn-t">No next step</div>') + (l.blocker && l.blocker !== "none" ? pill((BLK[l.blocker] || {}).name, "muted") : "") + "</button>"; }).join("") || '<p class="fine">' + esc(s.hint) + "</p>") + "</div>"; }).join("") + "</div>";
  }
  return '<div class="tbl-w"><table class="tbl rows"><thead><tr><th class="num">Score</th><th>Person</th><th>Segment</th><th>Stage</th><th>Next step</th><th>Hesitation</th><th>Last touch</th><th>Source</th></tr></thead><tbody>' +
    L.map(l => { const sc = leadScore(l), d = l.next && l.next.due ? dueInfo(l.next.due) : null;
      return '<tr data-act="openLead" data-id="' + l.id + '" tabindex="0"><td class="num">' + scoreDot(sc) + '</td><td><b>' + esc(l.name) + "</b>" + (l.sample ? ' <span class="tag">sample</span>' : "") + '<div class="muted">' + esc(l.role || "") + (l.company ? " · " + esc(l.company) : "") + (l.coStage ? " · " + esc(l.coStage) : "") + "</div></td><td>" + esc((SEG[l.seg] || {}).name || "–") + "</td><td>" + stagePill(l.stage) +
        "</td><td>" + (l.next && l.next.t ? esc(l.next.t) + (d ? '<div class="' + d.cls + '-t fine">' + esc(d.t) + "</div>" : "") : '<span class="warn-t">None set</span>') + "</td><td>" + (l.blocker && l.blocker !== "none" ? esc((BLK[l.blocker] || {}).name) : '<span class="muted">–</span>') + '</td><td class="muted">' + esc(ago(l.lastTouchAt)) + '</td><td class="muted">' + esc(srcOf(l.src).name) + "</td></tr>"; }).join("") + "</tbody></table></div>";
}
function paintLeads() { const el = document.getElementById("leadList"); if (el) el.innerHTML = leadListHtml(); }
VIEWS.leads = () => {
  const f = UI.f, L = leads(), n = k => k === "open" ? L.filter(l => OPEN_STAGES.includes(l.stage)).length : k === "all" ? L.length : L.filter(l => l.stage === k).length;
  const chip = (k, t) => '<button type="button" class="chip" aria-pressed="' + (f.stage === k) + '" data-act="fStage" data-k="' + k + '">' + esc(t) + ' <span class="count">' + n(k) + "</span></button>";
  if (!L.length) return VIEWS.today();
  return '<div class="toolbar"><div class="chips">' + chip("open", "Open") + STAGES.filter(s => s.band !== "off").map(s => chip(s.key, s.name)).join("") + chip("nurture", "Nurture") + chip("lost", "Lost") + chip("all", "All") + "</div></div>" +
    '<div class="toolbar"><label class="sel"><span>Segment</span><select data-chg="fSeg">' + opt("", "All", f.seg) + SEGMENTS.map(s => opt(s.key, s.name, f.seg)).join("") + '</select></label><label class="sel"><span>Source</span><select data-chg="fSrc">' + opt("", "All", f.src) + SOURCES.map(s => opt(s.key, s.name, f.src)).join("") +
    '</select></label><label class="sel"><span>Sort</span><select data-chg="fSort">' + opt("score", "Score", f.sort) + opt("due", "Next step due", f.sort) + opt("touch", "Longest untouched", f.sort) + opt("new", "Newest", f.sort) + '</select></label><span class="sp"></span>' +
    '<div class="tabs"><button type="button" aria-selected="' + (UI.leadsView === "table") + '" data-act="lView" data-k="table">Table</button><button type="button" aria-selected="' + (UI.leadsView === "board") + '" data-act="lView" data-k="board">Board</button></div>' +
    '<button type="button" class="btn" data-act="importLeads">Import</button><button type="button" class="btn" data-act="exportLeads">Export</button><button type="button" class="btn primary" data-act="addLead">' + ico("plus") + "Add lead</button></div>" +
    '<section class="panel flush" id="leadList">' + leadListHtml() + "</section>";
};
Object.assign(ACT, {
  fStage: el => { UI.f.stage = el.dataset.k; render(); }, lView: el => { UI.leadsView = el.dataset.k; render(); },
  exportLeads: () => saveFile("leads-" + todayStr() + ".csv", leadsCsv(filteredLeads())),
  addLead: () => openModal({ kind: "lead", title: "Add a lead" }),
  importLeads: () => openModal({ kind: "import", title: "Import leads" }),
  openLead: el => { UI.drawer = el.dataset.id; UI.drTab = "now"; renderDrawer(); },
  closeDrawer: () => { UI.drawer = null; renderDrawer(); if (UI.dirty) render(); }
});
Object.assign(CHG, { fSeg: el => { UI.f.seg = el.value; render(); }, fSrc: el => { UI.f.src = el.value; render(); }, fSort: el => { UI.f.sort = el.value; render(); } });
document.addEventListener("keydown", e => { if (e.key === "Enter" && e.target.matches && e.target.matches("tr[data-act]")) e.target.click(); });

MODALS.lead = () => '<form data-submit="saveNewLead" class="form"><label class="field"><span>Name</span><input name="name" id="nl-name" required autocomplete="off"></label><label class="field"><span>Role or title</span><input name="role" id="nl-role" autocomplete="off" placeholder="Senior Product Manager"></label>' +
  '<label class="field"><span>Company</span><input name="company" id="nl-company" autocomplete="off"></label><label class="field"><span>Company stage</span><select name="coStage" id="nl-costage">' + opt("", "Not known", "") + CO_STAGES.map(s => opt(s, s, "")).join("") + "</select></label>" +
  '<label class="field"><span>Where they came from</span><select name="src" id="nl-src">' + SOURCES.map(s => opt(s.key, s.name, "inbound")).join("") + '</select></label><label class="field"><span>City</span><input name="city" id="nl-city" autocomplete="off"></label>' +
  '<label class="field"><span>Phone or WhatsApp</span><input name="phone" id="nl-phone" autocomplete="off" inputmode="tel"></label><label class="field"><span>Email</span><input name="email" id="nl-email" type="email" autocomplete="off"></label>' +
  '<label class="field wide"><span>LinkedIn</span><input name="linkedin" id="nl-li" autocomplete="off" placeholder="linkedin.com/in/…"></label><label class="check wide"><input type="checkbox" name="waOptIn" id="nl-wa"> They agreed to be messaged on WhatsApp</label>' +
  '<div class="row-end wide"><button type="button" class="btn ghost" data-act="closeModal">Cancel</button><button class="btn primary">Add and open</button></div></form>';
ACT.saveNewLead = form => { const d = Object.fromEntries(new FormData(form).entries()); d.waOptIn = !!d.waOptIn; d.seg = guessSegment(d.role);
  const l = put("leads", newLead(d)); closeModal(); UI.drawer = l.id; UI.drTab = "now"; render(); toast("Added. The clock has started."); };
MODALS.import = () => '<p>Paste rows from a sheet or CRM export, with a header row. Columns it understands: <b>Name, Title or Role, Company, Email, Phone, LinkedIn, City, Source, Company stage</b>. Segment is guessed from the title.</p>' +
  '<label class="field wide"><span>CSV text</span><textarea id="imp-text" class="mono" rows="9" placeholder="Name,Title,Company,Email,Phone&#10;Asha Rao,Product Manager,Acme,asha@example.com,98…"></textarea></label><label class="field wide"><span>Or choose a .csv file</span><input type="file" id="imp-file" accept=".csv,text/csv" data-chg="impFile"></label>' +
  '<div class="row-end"><button type="button" class="btn ghost" data-act="closeModal">Cancel</button><button type="button" class="btn primary" data-act="doImport">Import</button></div>';
CHG.impFile = el => { const f = el.files && el.files[0]; if (!f) return; const r = new FileReader(); r.onload = () => { document.getElementById("imp-text").value = String(r.result || ""); }; r.readAsText(f); };
ACT.doImport = () => { const rows = leadsFromCsv(document.getElementById("imp-text").value || ""); if (!rows.length) { toast("No rows found. Check there is a header row with a Name column.", "crit"); return; }
  rows.forEach(l => put("leads", l)); closeModal(); UI.f.stage = "new"; UI.f.sort = "new"; go("leads"); render(); toast(rows.length + " leads imported"); };

/* ---------- lead mutations ---------- */
const getLead = id => Store.data.leads[id];
function patchLead(id, patch) { const l = getLead(id); if (!l) return null; return put("leads", Object.assign({}, l, patch)); }
function logTouch(id, t, silent) { const l = getLead(id); if (!l) return; const now = new Date().toISOString();
  const patch = { log: [...(l.log || []), Object.assign({ at: now }, t)].slice(-200) };
  if (t.type !== "note") { patch.lastTouchAt = now; if (!l.firstTouchAt) patch.firstTouchAt = now; if (l.stage === "new") { patch.stage = "contacted"; patch.stageAt = now; patch.lastOpenStage = "contacted"; } }
  patchLead(id, patch); if (!silent) toast("Logged"); render(); }
function setStage(id, k) { const l = getLead(id); if (!l || l.stage === k) return; const now = new Date().toISOString();
  const patch = { stage: k, stageAt: now, log: [...(l.log || []), { at: now, type: "stage", outcome: stageOf(k).name, note: "Moved from " + stageOf(l.stage).name }] };
  if (FLOW.includes(k)) patch.lastOpenStage = k; else if (FLOW.includes(l.stage)) patch.lastOpenStage = l.stage;
  if (k !== "new" && !l.firstTouchAt) { patch.firstTouchAt = now; patch.lastTouchAt = now; }
  if (k === "proposal" && !l.offer) patch.offer = { levers: [], plan: "", sentAt: now };
  if (k === "enrolled" && !l.health) patch.health = { att: 100, work: 0, reviews: 0, nps: null, referralAsked: false };
  if (k === "lost") patch.lostReason = l.blocker || "none";
  if ((k === "proposal" || k === "committed" || k === "enrolled") && !l.cohortId) { const c = Object.values(Store.data.cohorts).filter(c => c.prog === (l.prog === "combo" ? "p1" : l.prog) && new Date(c.start) > new Date()).sort((x, y) => new Date(x.start) - new Date(y.start))[0]; if (c) patch.cohortId = c.id; }
  patchLead(id, patch); render(); }

/* ---------- lead panel ---------- */
function renderDrawer() {
  const el = document.getElementById("drawer"), sc = document.getElementById("scrim"), l = UI.drawer && getLead(UI.drawer);
  if (!l) { el.hidden = true; sc.hidden = true; el.innerHTML = ""; UI.drawer = null; return; }
  const keep = el.querySelector(".dr-b") ? el.querySelector(".dr-b").scrollTop : 0, same = el.dataset.id === l.id + UI.drTab;
  const s = leadScore(l), seg = SEG[l.seg];
  const step = k => '<button type="button" class="step ' + (l.stage === k ? "on" : FLOW.indexOf(k) >= 0 && FLOW.indexOf(k) < reachedIdx(l) && FLOW.includes(l.stage) ? "done" : "") + '" data-act="stage" data-k="' + k + '" title="' + esc(stageOf(k).hint) + '">' + esc(stageOf(k).name) + "</button>";
  const tab = (k, t) => '<button type="button" role="tab" aria-selected="' + (UI.drTab === k) + '" data-act="drTab" data-k="' + k + '">' + t + "</button>";
  el.innerHTML = '<div class="dr-h"><div class="dr-id">' + scoreDot(s) + '<div><h2>' + esc(l.name) + (l.sample ? ' <span class="tag">sample</span>' : "") + '</h2><div class="muted">' + esc(l.role || "Role not set") + (l.company ? " · " + esc(l.company) : "") + (l.coStage ? " · " + esc(l.coStage) : "") + (l.city ? " · " + esc(l.city) : "") + '</div></div></div><button type="button" class="icon-btn" data-act="closeDrawer" aria-label="Close">' + ico("x") + "</button></div>" +
    '<div class="steps-rail">' + FLOW.map(step).join('<i></i>') + '<span class="sp"></span>' + step("nurture") + step("lost") + "</div>" +
    '<div class="tabs dr-tabs" role="tablist">' + tab("now", "Now") + tab("diag", "Diagnose") + tab("offer", "Offer") + tab("log", "History <span class=\"count\">" + (l.log || []).length + "</span>") + tab("info", "Details") + "</div>" +
    '<div class="dr-b">' + ({ now: drNow, diag: drDiag, offer: drOffer, log: drLog, info: drInfo }[UI.drTab] || drNow)(l, s, seg) + "</div>";
  el.dataset.id = l.id + UI.drTab; el.hidden = false; sc.hidden = false; if (same) el.querySelector(".dr-b").scrollTop = keep;
}
function tplBlock(l, t) { const body = merge(t.body, l), subj = t.subject ? merge(t.subject, l) : "";
  return '<div class="tpl"><div class="tpl-h"><b>' + esc(t.name) + "</b>" + pill(t.ch === "whatsapp" ? "WhatsApp" : t.ch === "linkedin" ? "LinkedIn" : "Email", "muted") + '<span class="sp"></span>' + copyBtn((subj ? "Subject: " + subj + "\n\n" : "") + body) +
    (t.ch === "email" && Cap.mcp ? '<button type="button" class="btn sm ghost" data-act="draft" data-id="' + l.id + '" data-t="' + t.key + '">' + ico("mail") + "Draft in Gmail</button>" : "") + "</div>" + (subj ? '<div class="tpl-s">Subject: ' + esc(subj) + "</div>" : "") + '<pre class="tpl-b">' + esc(body) + "</pre></div>"; }
function drNow(l, s, seg) {
  const d = l.next && l.next.due ? dueInfo(l.next.due) : null, cad = nextCadence(l), B = BLK[l.blocker], ds = diagSummary(l);
  const quick = [["call", "No answer", "Called, no answer"], ["call", "Connected", "Called, spoke"], ["whatsapp", "Sent material", "WhatsApp sent"], ["email", "Sent material", "Email sent"], ["linkedin", "Sent material", "LinkedIn sent"]]
    .map(q => '<button type="button" class="btn sm" data-act="quick" data-type="' + q[0] + '" data-out="' + q[1] + '">' + q[2] + "</button>").join("");
  let guide = "";
  if (!seg) guide = '<div class="note warn">Set the segment in Details and this panel fills with the right opening lines and questions.</div>';
  else if (l.stage === "new" || l.stage === "contacted") guide = '<h3>Open with one of these</h3>' + seg.hooks.map(h => '<div class="say"><p>' + esc(h) + "</p>" + copyBtn(h) + "</div>").join("") +
    '<div class="note"><b>How ' + esc(seg.name.toLowerCase()) + "s see themselves:</b> " + esc(seg.identity.sees) + " <b>Say:</b> " + esc(seg.identity.say) + " <b>Avoid:</b> " + esc(seg.identity.avoid) + "</div>";
  else if (l.stage === "diagnosed") guide = "<h3>Teach one thing, then offer the mentor</h3><div class=\"say\"><p>" + esc(seg.teach) + "</p>" + evChip(seg.teachEv) + "</div>" + (ds && ds.allHigh ? '<div class="note good">All scores are at the top. Tell them so. They may be better as a referrer or a mentor than a learner.</div>' : "");
  else if (l.stage === "mentor") guide = '<h3>Before and after the mentor conversation</h3><ul class="ticks"><li>Brief the mentor: ' + esc(l.quote ? "they said “" + l.quote + "”" : "their weakest dimension and one real decision") + ".</li><li>Join silently. Take the last two minutes.</li><li>Send the offer the same day.</li></ul>";
  else if (l.stage === "proposal") guide = B && l.blocker !== "none" ? "<h3>Their hesitation: " + esc(B.name) + '</h3><div class="note"><b>Confirm it first:</b> ' + esc(B.confirm) + '</div><div class="say"><p>' + esc(B.say) + "</p>" + copyBtn(B.say) + '</div><p class="fine"><b>Do not:</b> ' + esc(B.dont) + ' <button type="button" class="link" data-act="openObj" data-k="' + B.key + '">Full play</button></p>'
    : '<div class="note warn"><b>No reason recorded yet.</b> Ask: “Is there anything stopping you from holding your seat today?” Then tag the hesitation in Diagnose.</div>';
  else if (l.stage === "committed") guide = '<h3>Deposit is in. Now make it real</h3><ul class="ticks"><li>Confirm the payment plan in writing.</li><li>If the employer is paying part, send the manager page and book the three-way call.</li><li>Ask who else on their team should see this.</li></ul>';
  else if (l.stage === "enrolled") guide = '<h3>Learner</h3>' + healthBlock(l) + '<p class="fine">Week one: a ten-minute call. Week three, after the first mentor review: ask for two names.</p>';
  else guide = '<div class="note">' + (l.stage === "nurture" ? "Parked with a date. Call on the day, and open with the reason they gave." : "Closed. Record the true reason; it is the most useful data in the tool.") + "</div>";
  const tpls = TEMPLATES.filter(t => t.stage.includes(l.stage)).map(t => tplBlock(l, t)).join("");
  const ai = Cap.sample ? '<div class="row-c"><button type="button" class="btn sm" data-act="aiBrief" data-id="' + l.id + '">' + ico("spark") + 'Pre-call brief</button><button type="button" class="btn sm" data-act="aiMsg" data-id="' + l.id + '">' + ico("spark") + "Write the next message</button></div>" + aiBox("lead") : "";
  return '<section class="blk"><h3>Next step</h3><div class="next"><input id="nx-t" value="' + esc(l.next && l.next.t || "") + '" placeholder="What happens next" data-chg="nextT" data-id="' + l.id + '" aria-label="Next step"><input id="nx-d" type="date" value="' + esc(l.next && l.next.due || "") + '" data-chg="nextD" data-id="' + l.id + '" aria-label="Due date">' + (d ? '<span class="' + d.cls + '-t fine">' + esc(d.t) + "</span>" : "") + "</div>" +
    (l.stage === "new" || l.stage === "contacted" ? '<p class="fine">Touch ' + (touchCount(l) + 1) + " of " + CADENCE.length + ": <b>" + esc(cad.t) + ".</b> " + esc(cad.d) + ' <button type="button" class="link" data-act="useCad" data-id="' + l.id + '">Set as next step</button></p>' : "") +
    '<div class="row-c">' + quick + "</div></section>" + '<section class="blk">' + guide + "</section>" + (ai ? '<section class="blk">' + ai + "</section>" : "") + (tpls ? '<section class="blk"><h3>Messages for this stage</h3>' + tpls + "</section>" : "") +
    '<section class="blk"><details><summary>Why the score is ' + s.total + ' <span class="muted">(fit ' + s.fit + "/50, intent " + s.intent + "/50)</span></summary>" + s.parts.map(p => barRow(esc(p.k) + ' <span class="muted">' + esc(p.why) + "</span>", p.pts, p.max, { text: p.pts + "/" + p.max })).join("") + "</details></section>";
}
function healthBlock(l) { const h = l.health || {}; const f = (k, label, max) => '<label class="field"><span>' + label + '</span><input type="number" min="0" max="' + max + '" value="' + esc(h[k] == null ? "" : h[k]) + '" data-chg="health" data-id="' + l.id + '" data-k="' + k + '" id="h-' + k + '"></label>';
  return '<div class="form three">' + f("att", "Attendance %", 100) + f("work", "Work submitted", 20) + f("reviews", "Mentor reviews", 20) + f("nps", "Would recommend 0–10", 10) + '<label class="check"><input type="checkbox" ' + (h.referralAsked ? "checked" : "") + ' data-chg="healthRef" data-id="' + l.id + '" id="h-ref"> Asked for referrals</label></div>'; }
function drDiag(l, s, seg) {
  const d = l.diag || {}, ds = diagSummary(l);
  const scoreBtns = k => '<div class="seg3" role="group" aria-label="Score">' + [0, 1, 2].map(v => '<button type="button" aria-pressed="' + (d[k] === v) + '" data-act="diag" data-id="' + l.id + '" data-k="' + k + '" data-v="' + v + '" title="' + ["Could not explain it", "Partly", "Clear, with evidence"][v] + '">' + v + "</button>").join("") + "</div>";
  const asked = seg ? seg.prompts : [], used = new Set(asked.map(p => p[1]).filter(Boolean));
  const qs = asked.map(p => { const D = DIAG.find(x => x.key === p[1]); return '<div class="q"><div><p>' + esc(p[0]) + "</p>" + (D ? '<span class="fine">Scores: ' + esc(D.name.toLowerCase()) + "</span>" : '<span class="fine">Context, not scored</span>') + "</div>" + (D ? scoreBtns(D.key) : "") + "</div>"; }).join("");
  const rest = DIAG.filter(x => !used.has(x.key)).map(x => '<div class="q small"><div><p>' + esc(x.name) + '</p><span class="fine">' + esc(x.ask) + "</span></div>" + scoreBtns(x.key) + "</div>").join("");
  const sum = ds ? '<div class="note ' + (ds.allHigh ? "good" : "") + '"><b>' + (ds.allHigh ? "Strong across the board." : "Weakest: " + esc(ds.weak.name.toLowerCase()) + ". Strongest: " + esc(ds.strong.name.toLowerCase()) + ".") + "</b> " +
    (ds.rec ? "Suggested: <b>" + esc(PROGRAMS[ds.rec].short + " · " + PROGRAMS[ds.rec].name) + "</b>" + (ds.rec !== l.prog ? ' <button type="button" class="link" data-act="setProg" data-id="' + l.id + '" data-k="' + ds.rec + '">Use this</button>' : "") : "") + "</div>" : "";
  const B = BLK[l.blocker];
  return '<section class="blk"><h3>Explain-it questions' + (seg ? " for a " + esc(seg.name.toLowerCase()) : "") + '</h3><p class="fine">Ask, then stay quiet. Follow up once with “why” or “how did you know”. Score 0 if they could not explain it, 1 if partly, 2 if clear with evidence. ' + evChip("ioed") + "</p>" + (qs || '<div class="note warn">Set the segment in Details to see the questions.</div>') + sum + "</section>" +
    '<section class="blk"><details' + (Object.keys(d).some(k => !used.has(k)) ? " open" : "") + "><summary>Other dimensions</summary>" + rest + "</details></section>" +
    '<section class="blk"><h3>Their sentence</h3><p class="fine">The one thing they said that shows the gap, word for word. It goes into the recap and the offer.</p><textarea rows="2" id="dg-quote" data-chg="lf" data-id="' + l.id + '" data-k="quote" placeholder="“We assumed the problem was pricing and never checked.”">' + esc(l.quote || "") + "</textarea></section>" +
    '<section class="blk"><h3>What is holding them back</h3><select id="dg-blk" data-chg="lfs" data-id="' + l.id + '" data-k="blocker">' + BLOCKERS.map(b => opt(b.key, b.name, l.blocker || "none")).join("") + "</select>" +
    (B && l.blocker !== "none" ? '<div class="note"><b>You hear:</b> ' + esc(B.hear) + "<br><b>What is going on:</b> " + esc(B.real) + "<br><b>Confirm with:</b> " + esc(B.confirm) + ' <button type="button" class="link" data-act="openObj" data-k="' + B.key + '">Open the play</button></div>' : '<p class="fine">Not sure? Ask the confirm question for the most likely two. See Objections.</p>') +
    '<label class="field"><span>Who pays</span><select id="dg-pay" data-chg="lfs" data-id="' + l.id + '" data-k="payer">' + PAYERS.map(p => opt(p.key, p.name, l.payer)).join("") + "</select></label></section>" +
    '<section class="blk"><h3>Signals</h3><div class="checks">' + SIGNALS.map(g => '<label class="check"><input type="checkbox" ' + ((l.signals || []).includes(g.key) ? "checked" : "") + ' data-chg="signal" data-id="' + l.id + '" data-k="' + g.key + '" id="sg-' + g.key + '"> ' + esc(g.name) + "</label>").join("") + "</div></section>";
}
function drOffer(l) {
  const a = A(), lev = l.offer && l.offer.levers || [], o = offerCalc(l.prog || "p1", lev, a), P = PROGRAMS[l.prog] || PROGRAMS.p1;
  const cohorts = Object.values(Store.data.cohorts).sort((x, y) => new Date(x.start) - new Date(y.start));
  return '<section class="blk"><div class="form"><label class="field"><span>Program</span><select id="of-prog" data-chg="lfs" data-id="' + l.id + '" data-k="prog">' + Object.values(PROGRAMS).map(p => opt(p.key, p.short + " · " + inr(listPrice(p.key, a)), l.prog)).join("") + '</select></label><label class="field"><span>Cohort</span><select id="of-coh" data-chg="lfs" data-id="' + l.id + '" data-k="cohortId">' + opt("", "Not chosen", l.cohortId) + cohorts.map(c => opt(c.id, c.name + " · " + fmtDate(c.start), l.cohortId)).join("") + "</select></label></div>" +
    '<p class="fine">' + esc(P.name) + ". " + P.weeks + " weeks. " + esc(P.includes) + "</p></section>" +
    '<section class="blk"><h3>Scholarship</h3><p class="fine">Tick only what is true for this person. Each one buys something. ' + evChip("shiv") + '</p><div class="levers">' + LEVERS.map(L => '<label class="lever"><input type="checkbox" ' + (lev.includes(L.key) ? "checked" : "") + ' data-chg="lever" data-id="' + l.id + '" data-k="' + L.key + '" id="lv-' + L.key + '"><div><b>' + esc(L.name) + ' <span class="muted">up to ' + L.maxPct + "%</span></b><span class=\"fine\">" + esc(L.basis) + "</span></div></label>").join("") + "</div>" + offerBox(o, a) + "</section>" +
    '<section class="blk"><div class="form"><label class="field"><span>How they will pay</span><select id="of-plan" data-chg="plan" data-id="' + l.id + '">' + [["", "Not agreed"], ["full", "In full"], ["instalments", "Deposit + instalments"], ["emi", "No-cost EMI"], ["employer", "Employer invoice"], ["split", "Split with employer"]].map(p => opt(p[0], p[1], l.offer && l.offer.plan || "")).join("") + "</select></label></div>" +
    '<div class="row-c">' + (l.stage !== "proposal" && FLOW.indexOf(l.stage) < FLOW.indexOf("proposal") ? '<button type="button" class="btn primary" data-act="stage" data-k="proposal">Mark offer sent</button>' : "") + (l.stage === "proposal" ? '<button type="button" class="btn primary" data-act="stage" data-k="committed">Deposit received</button>' : "") + (l.stage === "committed" ? '<button type="button" class="btn primary" data-act="stage" data-k="enrolled">Paid or plan active</button>' : "") + "</div></section>" +
    '<section class="blk">' + tplBlock(l, TEMPLATES.find(t => t.key === "em_offer")) + tplBlock(l, TEMPLATES.find(t => t.key === "em_manager")) + "</section>";
}
function offerBox(o, a) {
  return '<div class="offer"><div class="of-row"><span>List fee</span><b>' + inr(o.list) + "</b></div>" + o.parts.map(p => '<div class="of-row sub"><span>' + esc(p.name) + ' <span class="muted">buys ' + esc(p.buys.toLowerCase()) + "</span></span><span>−" + p.pct + "%</span></div>").join("") +
    (o.raw > o.pct ? '<div class="of-row sub warn-t"><span>Capped at ' + a.stackCapPct + "% (levers add to " + o.raw + "%)</span><span></span></div>" : "") +
    '<div class="of-row total"><span>They pay</span><b>' + inr(o.net) + (o.pct ? ' <span class="muted">(' + o.pct + "% off)</span>" : "") + '</b></div><div class="of-row sub"><span>Left after delivery (' + inrShort(o.cost) + ") and acquisition (" + inrShort(a.cacTarget) + ')</span><span>' + inr(o.margin) + " · " + o.marginPct + "%</span></div>" +
    '<div class="verdict ' + (o.verdict === "ok" ? "good" : "warn") + '">' + (o.verdict === "approve" ? "Below the " + a.minMarginPct + "% margin floor. Needs approval." : o.verdict === "capped" ? "Within policy after the cap." : o.pct ? "Within policy. Record what each lever bought." : "Full fee. No approval needed.") + "</div></div>";
}
function drLog(l) {
  const items = [...(l.log || [])].reverse().map(x => '<li class="lg ' + esc(x.type) + '"><div class="lg-h"><b>' + esc((ACTIVITY_TYPES.find(t => t.key === x.type) || { name: x.type === "stage" ? "Stage" : x.type }).name) + "</b> " + (x.outcome ? pill(x.outcome, "muted") : "") + '<span class="sp"></span><span class="muted">' + esc(fmtDateTime(x.at)) + "</span></div>" + (x.note ? "<p>" + esc(x.note) + "</p>" : "") + "</li>").join("");
  return '<section class="blk"><h3>Log a touch</h3><form data-submit="addTouch" data-id="' + l.id + '" class="form"><label class="field"><span>Type</span><select name="type" id="lg-type">' + ACTIVITY_TYPES.map(t => opt(t.key, t.name, "call")).join("") + '</select></label><label class="field"><span>Outcome</span><select name="outcome" id="lg-out">' + OUTCOMES.map(o => opt(o, o, "Connected")).join("") + '</select></label><label class="field wide"><span>One line</span><input name="note" id="lg-note" autocomplete="off" placeholder="What was said, in their words"></label><div class="row-end wide"><button class="btn primary">Log it</button></div></form></section>' +
    '<section class="blk"><h3>History</h3>' + (items ? '<ul class="lgs">' + items + "</ul>" : '<p class="muted">Nothing logged yet.</p>') + '<p class="fine">Created ' + esc(fmtDateTime(l.createdAt)) + (l.firstTouchAt ? " · first response after " + mins((new Date(l.firstTouchAt) - new Date(l.createdAt)) / 6e4) : " · no response yet") + "</p></section>";
}
function drInfo(l) {
  const f = (k, label, type, ph) => '<label class="field"><span>' + label + '</span><input id="df-' + k + '" ' + (type ? 'type="' + type + '" ' : "") + 'value="' + esc(l[k] == null ? "" : l[k]) + '" data-chg="lf" data-id="' + l.id + '" data-k="' + k + '" autocomplete="off"' + (ph ? ' placeholder="' + ph + '"' : "") + "></label>";
  const s = (k, label, opts) => '<label class="field"><span>' + label + '</span><select id="df-' + k + '" data-chg="lfs" data-id="' + l.id + '" data-k="' + k + '">' + opts + "</select></label>";
  return '<section class="blk"><div class="form">' + f("name", "Name") + f("role", "Role or title") + s("seg", "Segment", opt("", "Not set", l.seg) + SEGMENTS.map(x => opt(x.key, x.name, l.seg)).join("")) + f("company", "Company") + s("coStage", "Company stage", opt("", "Not known", l.coStage) + CO_STAGES.map(x => opt(x, x, l.coStage)).join("")) + f("city", "City") +
    s("src", "Source", SOURCES.map(x => opt(x.key, x.name, l.src)).join("")) + f("yrs", "Years of experience", "number") + s("sen", "Seniority", opt("", "Not known", l.sen) + SENIORITY.map(x => opt(x.key, x.name, l.sen)).join("")) + f("phone", "Phone or WhatsApp") + f("email", "Email", "email") + f("linkedin", "LinkedIn") +
    '<label class="field wide"><span>Their goal for the next 18 months</span><input id="df-goal" value="' + esc(l.goal || "") + '" data-chg="lf" data-id="' + l.id + '" data-k="goal" autocomplete="off"></label><label class="check wide"><input type="checkbox" id="df-wa" ' + (l.waOptIn ? "checked" : "") + ' data-chg="lfc" data-id="' + l.id + '" data-k="waOptIn"> Agreed to WhatsApp messages</label></div></section>' +
    '<section class="blk"><div class="row-c"><button type="button" class="btn ghost danger" data-act="delLead" data-id="' + l.id + '">' + (UI.confirmDel === l.id ? "Confirm: delete this lead for good" : "Delete lead") + "</button></div></section>";
}
Object.assign(ACT, {
  drTab: el => { UI.drTab = el.dataset.k; UI.confirmDel = null; renderDrawer(); },
  stage: el => { if (UI.drawer) setStage(UI.drawer, el.dataset.k); },
  quick: el => logTouch(UI.drawer, { type: el.dataset.type, outcome: el.dataset.out, note: "" }),
  useCad: el => { const l = getLead(el.dataset.id), c = nextCadence(l); patchLead(l.id, { next: { t: c.t, due: new Date(new Date(l.createdAt).getTime() + c.day * DAY) > new Date() ? new Date(new Date(l.createdAt).getTime() + c.day * DAY).toISOString().slice(0, 10) : todayStr() } }); render(); },
  diag: el => { const l = getLead(el.dataset.id), d = Object.assign({}, l.diag), k = el.dataset.k, v = +el.dataset.v; if (d[k] === v) delete d[k]; else d[k] = v;
    const sig = new Set(l.signals || []); if (Object.keys(d).length) sig.add("diagnostic"); patchLead(l.id, { diag: d, signals: [...sig] }); render(); },
  setProg: el => { patchLead(el.dataset.id, { prog: el.dataset.k }); render(); },
  addTouch: form => { const d = Object.fromEntries(new FormData(form).entries()); logTouch(form.dataset.id, d); },
  delLead: el => { if (UI.confirmDel !== el.dataset.id) { UI.confirmDel = el.dataset.id; renderDrawer(); return; } del("leads", el.dataset.id); UI.confirmDel = null; UI.drawer = null; render(); toast("Deleted"); },
  draft: el => { const l = getLead(el.dataset.id), t = TEMPLATES.find(x => x.key === el.dataset.t); if (l && t) gmailDraft(l, merge(t.subject || "", l), merge(t.body, l)); },
  aiBrief: el => { const l = getLead(el.dataset.id), v = mergeVars(l), seg = SEG[l.seg];
    askClaude("lead", "I sell a mentor-led program for working professionals (yuj.dna, by Yuj Designs). I am about to call " + v.name + ", " + (l.role || "role unknown") + " at " + (l.company || "an unnamed company") + " (" + (l.coStage || "stage unknown") + ", " + (l.city || "India") + "). Do not invent facts about the person or company. From the role and company stage alone, give me: (1) three decisions someone in this role probably owns this quarter, (2) one sentence on the pressure a company at this stage is under, (3) which two of these questions to ask first and why: " + (seg ? seg.prompts.map(p => p[0]).join(" | ") : "walk me through your last decision") + ". Under 150 words, plain text, no flattery."); },
  aiMsg: el => { const l = getLead(el.dataset.id), v = mergeVars(l), seg = SEG[l.seg], B = BLK[l.blocker];
    askClaude("lead", "Write one WhatsApp message, under 70 words, from me (" + v.rep + ", yuj.dna) to " + v.first + ", a " + (l.role || "professional") + " at " + (l.company || "their company") + ". Stage: " + stageOf(l.stage).name + ". " + (l.quote ? "They told me: \"" + l.quote + "\". Use it. " : "") + (B && l.blocker !== "none" ? "Their hesitation: " + B.name + ". " + B.real + " " : "") + (seg ? "How they see themselves: " + seg.identity.sees + " Avoid these words: " + seg.identity.avoid + " " : "") + "Next step I want: " + (l.next && l.next.t || nextCadence(l).t) + ". Plain, respectful, peer to peer. No hype, no emoji, no discount, no false urgency. End with one question."); }
});
Object.assign(CHG, {
  nextT: el => { const l = getLead(el.dataset.id); patchLead(l.id, { next: { t: el.value, due: l.next && l.next.due || "" } }); UI.dirty = true; },
  nextD: el => { const l = getLead(el.dataset.id); patchLead(l.id, { next: { t: l.next && l.next.t || "", due: el.value } }); UI.dirty = true; },
  lf: el => { const v = el.type === "number" ? (el.value === "" ? "" : +el.value) : el.value; const p = { [el.dataset.k]: v }; if (el.dataset.k === "role" && !getLead(el.dataset.id).seg) p.seg = guessSegment(v); patchLead(el.dataset.id, p); UI.dirty = true; },
  lfs: el => { patchLead(el.dataset.id, { [el.dataset.k]: el.value }); render(); },
  lfc: el => { patchLead(el.dataset.id, { [el.dataset.k]: el.checked }); },
  signal: el => { const l = getLead(el.dataset.id), s = new Set(l.signals || []); if (el.checked) s.add(el.dataset.k); else s.delete(el.dataset.k); patchLead(l.id, { signals: [...s] }); render(); },
  lever: el => { const l = getLead(el.dataset.id), o = Object.assign({ levers: [], plan: "", sentAt: "" }, l.offer), s = new Set(o.levers); if (el.checked) s.add(el.dataset.k); else s.delete(el.dataset.k); o.levers = [...s]; patchLead(l.id, { offer: o }); render(); },
  plan: el => { const l = getLead(el.dataset.id), o = Object.assign({ levers: [], plan: "", sentAt: "" }, l.offer); o.plan = el.value; patchLead(l.id, { offer: o, payer: el.value === "employer" ? "employer" : el.value === "split" ? "split" : l.payer }); render(); },
  health: el => { const l = getLead(el.dataset.id), h = Object.assign({}, l.health); h[el.dataset.k] = el.value === "" ? null : +el.value; patchLead(l.id, { health: h }); UI.dirty = true; },
  healthRef: el => { const l = getLead(el.dataset.id), h = Object.assign({}, l.health); h.referralAsked = el.checked; patchLead(l.id, { health: h }); render(); }
});
