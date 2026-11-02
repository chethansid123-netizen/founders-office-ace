"""Build review.html: a one-file, offline page for the human review step.

Shows one record at a time beside its source link and the cited page text,
with each field's quote, page and verification result, and the AI second
reader's suggested decision. The reviewer approves or rejects by hand and
exports data/review_decisions_human.json, which pipeline/apply_review.py
treats as final.

Usage:  python3 -I pipeline/build_review_html.py
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # pipeline/ (own code only)

import json
import re
import sys

from common import DATA, RAW, ROOT, load_json


def page_texts(key: str, pages: set[int]) -> dict[int, str]:
    text = (RAW / f"{key}.txt").read_text(encoding="utf-8").split("\n\n", 1)[1]
    out, cur, buf = {}, 0, []
    for line in text.splitlines() + ["=== PAGE 0 ==="]:
        m = re.match(r"=== PAGE (\d+) ===", line)
        if m:
            if cur in pages:
                out[cur] = "\n".join(buf).strip()
            cur, buf = int(m.group(1)), []
            continue
        buf.append(line)
    return out


def main() -> int:
    final = load_json(DATA / "records.json")["records"]
    ai = {d["id"]: d for d in load_json(DATA / "review_decisions_ai.json")["decisions"]}
    v2 = load_json(DATA / "verification_v2.json")["records"]
    v1 = load_json(DATA / "verification_v1.json")["records"]
    items = []
    for r in final:
        pages = {e["page"] for e in r["evidence"].values() if isinstance(e.get("page"), int)}
        pages |= {c["page"] for c in r.get("context_facts", []) if isinstance(c.get("page"), int)}
        quotes = [e["quote"] for e in r["evidence"].values() if e.get("quote")]
        quotes += [f for e in r["evidence"].values() for f in (e.get("fragments") or [])]
        quotes += [c["quote"] for c in r.get("context_facts", [])]
        items.append({
            "id": r["id"], "company": r["company"], "practice": r["practice"],
            "source_url": r["source_url"], "source_page": r["source_page"],
            "fields": {k: r.get(k) for k in ["company", "exchange_symbol", "practice", "person_name", "role_title",
                                              "role_level", "event_type", "filing_date", "effective_date",
                                              "effective_date_note", "stated_reason", "successor_status",
                                              "successor_source", "successor_name"]},
            "evidence": r["evidence"],
            "context": r.get("context_facts", []),
            "verify": {k: {"status": f["status"], "reason": f["reason"]} for k, f in v2[r["id"]]["fields"].items()},
            "verify_v1_problems": [f"{k}: {f['reason']}" for k, f in v1[r["id"]]["fields"].items() if f["status"] == "mismatch"],
            "flags": v2[r["id"]].get("record_flags", []),
            "corrections": r.get("corrections", []),
            "ai": ai.get(r["id"]),
            "review_test": r.get("review_test"),
            "pages": page_texts(r["source_key"], pages),
            "quotes": quotes,
        })
    payload = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("/*__DATA__*/[]", payload)
    (ROOT / "review.html").write_text(html, encoding="utf-8")
    print(f"wrote review.html with {len(items)} records ({len(html)//1024} KB)")
    return 0


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Movers Signal review</title>
<style>
:root{--bg:#f6f2ea;--panel:#fffdf8;--ink:#1d2a24;--muted:#5d6b63;--line:#ddd5c6;--pine:#1f3d33;--pine2:#2f5a4b;
--ok:#2e6b4f;--okbg:#e3efe7;--bad:#9b3b2e;--badbg:#f6e3df;--nf:#6b6255;--nfbg:#ece6db;--mark:#f3e2a6}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#121815;--panel:#18211d;--ink:#e9e4d8;--muted:#a3ada6;
--line:#2c3933;--pine:#9fc5b3;--pine2:#7fb19b;--ok:#8fd0ad;--okbg:#1f3329;--bad:#f0a191;--badbg:#3a2420;--nf:#cbbfa9;--nfbg:#2b2822;--mark:#5c4f1f}}
:root[data-theme="dark"]{--bg:#121815;--panel:#18211d;--ink:#e9e4d8;--muted:#a3ada6;--line:#2c3933;--pine:#9fc5b3;--pine2:#7fb19b;
--ok:#8fd0ad;--okbg:#1f3329;--bad:#f0a191;--badbg:#3a2420;--nf:#cbbfa9;--nfbg:#2b2822;--mark:#5c4f1f}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 Georgia,'Iowan Old Style',serif}
header{position:sticky;top:0;z-index:2;background:var(--pine);color:#f6f2ea;padding:10px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
header h1{font-size:17px;margin:0;font-weight:600;letter-spacing:.02em}
header .sp{flex:1}
button,select,input{font:inherit}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:6px;padding:6px 12px;cursor:pointer}
header .btn{background:transparent;color:#f6f2ea;border-color:#ffffff55}
.btn.approve{background:var(--ok);color:#fff;border-color:var(--ok)}.btn.reject{background:var(--bad);color:#fff;border-color:var(--bad)}
main{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:16px;padding:16px;max-width:1500px;margin:0 auto}
@media (max-width:900px){main{grid-template-columns:1fr}}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px}
h2{margin:0 0 4px;font-size:21px}h3{margin:18px 0 8px;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.meta{color:var(--muted);font-size:13px}
table{width:100%;border-collapse:collapse;font-size:14px}td,th{border-top:1px solid var(--line);padding:7px 6px;vertical-align:top;text-align:left}
th{font-weight:600;color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.05em}
.q{font-style:italic}.pg{color:var(--muted);font-size:12px;white-space:nowrap}
.chip{display:inline-block;border-radius:999px;padding:1px 8px;font-size:12px;font-family:system-ui,sans-serif}
.match{background:var(--okbg);color:var(--ok)}.mismatch{background:var(--badbg);color:var(--bad)}.not_found{background:var(--nfbg);color:var(--nf)}
.note{font-size:13px;color:var(--muted)}
.ai{border-left:4px solid var(--pine2);padding:8px 12px;background:var(--bg);border-radius:4px}
.flag{color:var(--bad)}
.pagebox{white-space:pre-wrap;font:13px/1.55 ui-monospace,Menlo,Consolas,monospace;max-height:70vh;overflow:auto;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:12px}
mark{background:var(--mark);color:inherit;padding:0 1px}
.decide{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:12px}
textarea{width:100%;min-height:60px;font:inherit;border:1px solid var(--line);border-radius:6px;padding:8px;background:var(--panel);color:var(--ink)}
.status{font-weight:600}.v{color:var(--ok)}.r{color:var(--bad)}
a{color:var(--pine2)}
.kbd{font:12px ui-monospace,monospace;border:1px solid #ffffff66;border-radius:4px;padding:0 4px}
.note,.q,td,.pagebox,a{overflow-wrap:anywhere}
@media (max-width:640px){main{padding:10px}.card{padding:12px}table,tbody,tr,td{display:block;width:100%}
tr:first-child{display:none}tr{border-top:1px solid var(--line);padding:8px 0}td{border:0;padding:2px 0}
td:first-child{font-weight:600;color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.05em}
header{gap:8px}header h1{font-size:15px;width:100%}#who{width:110px}}
</style>
</head>
<body>
<header>
  <h1>Movers Signal · record review</h1>
  <span id="pos"></span>
  <span class="sp"></span>
  <select id="filter" class="btn" aria-label="Filter records">
    <option value="all">All records</option><option value="queue">Verifier flagged</option>
    <option value="ai-verified">AI: verified</option><option value="ai-rejected">AI: rejected</option>
    <option value="undecided">Not yet decided by me</option>
  </select>
  <button class="btn" id="prev" title="Previous (←)">←</button><button class="btn" id="next" title="Next (→)">→</button>
  <input id="who" class="btn" placeholder="Your name" aria-label="Reviewer name" style="width:140px">
  <button class="btn" id="export">Export decisions</button>
  <label class="btn" style="cursor:pointer">Import<input id="import" type="file" accept="application/json" hidden></label>
</header>
<main>
  <section class="card" id="left"></section>
  <section class="card" id="right"></section>
</main>
<script>
const DATA = /*__DATA__*/[];
const KEY = "movers-signal-review-v1";
let state = {};
try { state = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { state = {}; }
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} };
let idx = 0, view = DATA.map((_, i) => i);
const $ = (id) => document.getElementById(id);
const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };
const LABELS = {company:"Company",exchange_symbol:"Exchange symbol",practice:"Practice",person_name:"Person",role_title:"Role title",
  role_level:"Role level",event_type:"Event",filing_date:"Filing date",effective_date:"Effective date",stated_reason:"Stated reason",
  successor_status:"Successor status",successor_source:"Successor source",successor_name:"Successor"};

function applyFilter() {
  const f = $("filter").value;
  view = DATA.map((_, i) => i).filter(i => {
    const d = DATA[i];
    if (f === "queue") return d.verify_v1_problems.length || d.flags.length;
    if (f === "ai-verified") return d.ai && d.ai.decision === "VERIFIED";
    if (f === "ai-rejected") return d.ai && d.ai.decision === "REJECTED";
    if (f === "undecided") return !state[d.id];
    return true;
  });
  idx = 0; render();
}

function highlight(container, text, quotes) {
  // Build DOM nodes; never inject filing text as HTML.
  const norm = (s) => s.toLowerCase();
  const hay = norm(text);
  const ranges = [];
  for (const q of quotes) {
    if (!q || q.length < 4) continue;
    const words = q.toLowerCase().split(/\s+/).map(w => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    const re = new RegExp(words.join("\\s+"), "g");
    let m; while ((m = re.exec(hay))) { ranges.push([m.index, m.index + m[0].length]); if (m[0].length === 0) break; }
  }
  ranges.sort((a, b) => a[0] - b[0]);
  let pos = 0;
  for (const [s, e] of ranges) {
    if (s < pos) continue;
    container.appendChild(document.createTextNode(text.slice(pos, s)));
    container.appendChild(el("mark", null, text.slice(s, e)));
    pos = e;
  }
  container.appendChild(document.createTextNode(text.slice(pos)));
}

function render() {
  const L = $("left"), R = $("right");
  L.replaceChildren(); R.replaceChildren();
  if (!view.length) { L.appendChild(el("p", null, "No records match this filter.")); $("pos").textContent = ""; return; }
  const d = DATA[view[idx]];
  const decided = Object.keys(state).length;
  $("pos").textContent = `${idx + 1} / ${view.length} · you have decided ${decided} of ${DATA.length}`;
  L.appendChild(el("div", "meta", d.id));
  L.appendChild(el("h2", null, `${d.company}`));
  L.appendChild(el("div", "meta", `${d.practice}${d.review_test ? " · review test: " + d.review_test : ""}`));

  L.appendChild(el("h3", null, "Fields, quotes and verification (run 2)"));
  const t = el("table"); const hr = el("tr");
  ["Field", "Value", "Quote", "Check"].forEach(h => hr.appendChild(el("th", null, h))); t.appendChild(hr);
  for (const k of Object.keys(LABELS)) {
    if (!(k in d.fields) || (k === "successor_name" && d.fields[k] == null)) continue;
    const tr = el("tr");
    tr.appendChild(el("td", null, LABELS[k]));
    let val = d.fields[k]; if (k === "effective_date" && d.fields.effective_date_note) val = `${val} (${d.fields.effective_date_note})`;
    tr.appendChild(el("td", null, val == null ? "null" : String(val)));
    const ev = d.evidence[k]; const qtd = el("td");
    if (ev && ev.quote) { qtd.appendChild(el("span", "q", `“${ev.quote}”`)); qtd.appendChild(el("span", "pg", `  p${ev.page}`)); }
    else if (ev && ev.note) qtd.appendChild(el("span", "note", ev.note));
    else if (k === "role_level" || k === "practice") qtd.appendChild(el("span", "note", "Derived by rule (config/)"));
    if (ev && ev.note && ev.quote) qtd.appendChild(el("div", "note", ev.note));
    tr.appendChild(qtd);
    const v = d.verify[k]; const ctd = el("td");
    if (v) { ctd.appendChild(el("span", "chip " + v.status, v.status)); ctd.appendChild(el("div", "note", v.reason)); }
    tr.appendChild(ctd); t.appendChild(tr);
  }
  L.appendChild(t);
  if (d.context.length) {
    L.appendChild(el("h3", null, "Extra filed facts"));
    const ul = el("ul");
    d.context.forEach(c => { const li = el("li"); li.appendChild(el("strong", null, c.label + ": ")); li.appendChild(document.createTextNode(c.value + " ")); li.appendChild(el("span", "q", `“${c.quote}” `)); li.appendChild(el("span", "pg", "p" + c.page)); ul.appendChild(li); });
    L.appendChild(ul);
  }
  if (d.verify_v1_problems.length || d.corrections.length || d.flags.length) {
    L.appendChild(el("h3", null, "Audit trail"));
    d.verify_v1_problems.forEach(p => L.appendChild(el("div", "note flag", "Run 1 flagged: " + p)));
    d.corrections.forEach(c => L.appendChild(el("div", "note", `Corrected ${c.field}: ${c.reason}`)));
    d.flags.forEach(f => L.appendChild(el("div", "note flag", "Record flag: " + f)));
  }
  if (d.ai) {
    L.appendChild(el("h3", null, "AI second reader suggests"));
    const box = el("div", "ai");
    box.appendChild(el("div", "status " + (d.ai.decision === "VERIFIED" ? "v" : "r"), d.ai.decision));
    box.appendChild(el("div", null, d.ai.note || ""));
    (d.ai.overrides || []).forEach(o => box.appendChild(el("div", "note", `Override (${o.field}): ${o.reason}`)));
    L.appendChild(box);
  }
  L.appendChild(el("h3", null, "Your decision"));
  const mine = state[d.id] || {};
  const note = el("textarea"); note.placeholder = "Note (optional)"; note.value = mine.note || "";
  note.addEventListener("input", () => { if (state[d.id]) { state[d.id].note = note.value; save(); } });
  L.appendChild(note);
  const bar = el("div", "decide");
  const a = el("button", "btn approve", "Approve (A)"), r = el("button", "btn reject", "Reject (R)");
  a.onclick = () => decide("VERIFIED"); r.onclick = () => decide("REJECTED");
  bar.appendChild(a); bar.appendChild(r);
  bar.appendChild(el("span", "status " + (mine.decision === "VERIFIED" ? "v" : mine.decision === "REJECTED" ? "r" : ""),
    mine.decision ? `You: ${mine.decision}` : "Not decided"));
  L.appendChild(bar);

  R.appendChild(el("h3", null, "Source"));
  const link = el("a", null, `Open the filing PDF at page ${d.source_page} ↗`);
  link.href = d.source_url + "#page=" + d.source_page; link.target = "_blank"; link.rel = "noopener noreferrer";
  R.appendChild(link);
  R.appendChild(el("div", "note", d.source_url));
  const pages = Object.keys(d.pages).map(Number).sort((x, y) => x - y);
  pages.forEach(p => {
    R.appendChild(el("h3", null, `Page ${p} text (highlights = quotes)`));
    const box = el("div", "pagebox"); highlight(box, d.pages[p], d.quotes); R.appendChild(box);
  });

  function decide(dec) {
    state[d.id] = { decision: dec, note: note.value, at: new Date().toISOString() }; save();
    if (idx < view.length - 1) idx++; render();
  }
}

$("prev").onclick = () => { if (idx > 0) { idx--; render(); } };
$("next").onclick = () => { if (idx < view.length - 1) { idx++; render(); } };
$("filter").onchange = applyFilter;
document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT") return;
  if (e.key === "ArrowLeft") $("prev").click();
  if (e.key === "ArrowRight") $("next").click();
  if (e.key === "a" || e.key === "A") document.querySelector(".approve")?.click();
  if (e.key === "r" || e.key === "R") document.querySelector(".reject")?.click();
});
$("export").onclick = () => {
  const who = $("who").value.trim() || "Human reviewer";
  const decisions = Object.entries(state).map(([id, s]) => ({ id, decision: s.decision, note: s.note || "", overrides: (DATA.find(d => d.id === id)?.ai?.overrides) || [] }));
  const blob = new Blob([JSON.stringify({ reviewer: who, reviewed_at: new Date().toISOString().slice(0, 10), decisions }, null, 2)], { type: "application/json" });
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "review_decisions_human.json"; a.click();
};
$("import").onchange = async (e) => {
  const f = e.target.files[0]; if (!f) return;
  try { const j = JSON.parse(await f.text()); (j.decisions || []).forEach(x => { state[x.id] = { decision: x.decision, note: x.note || "" }; }); save(); render(); }
  catch (err) { alert("Could not read that file."); }
};
render();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    sys.exit(main())
