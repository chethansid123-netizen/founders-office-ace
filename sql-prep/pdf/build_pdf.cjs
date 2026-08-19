#!/usr/bin/env node
/* Builds the printable SQL syntax reference.
   Every example is EXECUTED against the real teaching database and its actual
   output is embedded, so nothing in the PDF is a guess.

     npm i @electric-sql/pglite playwright
     node build_pdf.cjs [out.pdf]                                            */
'use strict';
const fs = require('fs'), path = require('path');
const HERE = __dirname, SP = path.join(HERE, '..');
const OUT = process.argv[2] || path.join(HERE, 'sql-syntax-reference.pdf');

const ENTRIES = require('./entries.cjs');
const { PGlite } = require('@electric-sql/pglite');
const { chromium } = require('playwright');

/* ---------- html helpers ---------- */
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

const KW = new Set(('select from where group by having order limit offset join inner left right full outer cross on using natural '+
'union all intersect except with recursive as distinct case when then else end and or not null is in between like ilike '+
'exists any some insert into values update set delete truncate create table view materialized index unique primary key '+
'foreign references default check constraint alter add drop column rename to cascade restrict generated always identity '+
'stored partition over rows range groups unbounded preceding following current row filter window lateral asc desc nulls '+
'first last begin commit rollback savepoint transaction isolation level explain analyze returning conflict do nothing '+
'merge matched temp if cast interval date timestamp timestamptz integer bigint smallint numeric text boolean varchar '+
'real serial uuid jsonb array replace function language trigger before after each for execute fetch next only ties '+
'within grouping sets rollup cube immutable stable skip locked concurrently').split(' '));
const TOK = /(--[^\n]*)|('(?:[^']|'')*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][A-Za-z_0-9]*)/g;
function hl(src){
  let out = '', last = 0, m; TOK.lastIndex = 0;
  while((m = TOK.exec(src)) !== null){
    out += esc(src.slice(last, m.index));
    const t = m[0];
    if(m[1])      out += `<i class="c">${esc(t)}</i>`;
    else if(m[2]) out += `<i class="s">${esc(t)}</i>`;
    else if(m[3]) out += `<i class="n">${esc(t)}</i>`;
    else if(KW.has(t.toLowerCase())) out += `<b class="k">${esc(t)}</b>`;
    else if(/^\s*\(/.test(src.slice(TOK.lastIndex))) out += `<i class="f">${esc(t)}</i>`;
    else out += esc(t);
    last = TOK.lastIndex;
  }
  return out + esc(src.slice(last));
}

/* ---------- run every example, capture the real output ---------- */
function fmtVal(v){
  if (v === null || v === undefined) return 'NULL';
  if (v instanceof Date) return v.toISOString().slice(0,10);
  if (typeof v === 'object') return JSON.stringify(v);
  return String(v);
}
function fmtResult(results){
  const withCols = results.filter(r => r && r.fields && r.fields.length);
  if (!withCols.length) {
    const n = results.reduce((a,r) => a + ((r && r.affectedRows) || 0), 0);
    return n ? `OK, ${n} row${n===1?'':'s'} affected` : 'OK';
  }
  const res = withCols[withCols.length-1];
  const cols = res.fields.map(f => f.name);
  const rows = res.rows;
  if (!rows.length) return '0 rows';
  if (rows.length === 1 && cols.length === 1) return fmtVal(rows[0][cols[0]]);
  const render = r => cols.map(c => `${c}=${fmtVal(r[c])}`).join('  ');
  if (rows.length === 1) return render(rows[0]);
  let out = rows.slice(0,2).map(render).join('   ·   ');
  if (out.length > 150) out = rows.slice(0,1).map(render).join('');
  return out + (rows.length > 2 ? `   … ${rows.length} rows` : `   (${rows.length} rows)`);
}

(async () => {
  console.log('starting PostgreSQL…');
  const db = await PGlite.create();
  await db.exec(fs.readFileSync(path.join(SP,'01_schema.sql'),'utf8'));
  await db.exec(fs.readFileSync(path.join(SP,'02_seed.sql'),'utf8'));

  let ran = 0, failed = 0;
  for (const e of ENTRIES) {
    if (!e.ex) continue;
    try {
      const r = await db.exec(e.ex);
      e.result = fmtResult(r);
      ran++;
    } catch (err) {
      e.result = 'ERROR: ' + err.message.split('\n')[0];
      e.failed = true;
      failed++;
      console.log(`  FAIL  ${e.s}  ->  ${err.message.split('\n')[0].slice(0,90)}`);
    }
  }
  console.log(`ran ${ran} examples, ${failed} failed`);

  /* ---------- build the html ---------- */
  const secs = ENTRIES.filter(e => e.sec).map((e,i) => ({ n:i+1, title:e.sec, note:e.note }));
  let body = '', secIdx = 0;
  for (const e of ENTRIES) {
    if (e.sec) {
      secIdx++;
      body += `<section class="sec"><h2 id="s${secIdx}">${esc(e.sec)}</h2>`;
      if (e.note) body += `<p class="note">${esc(e.note)}</p>`;
      continue;
    }
    if (e.dialect) {
      body += '<table class="dial"><thead><tr>' +
        e.dialect[0].map(h => `<th>${esc(h)}</th>`).join('') + '</tr></thead><tbody>' +
        e.dialect.slice(1).map(r => '<tr>' +
          r.map((c,i) => i===0 ? `<td class="task">${esc(c)}</td>` : `<td class="code">${esc(c)}</td>`).join('') +
        '</tr>').join('') + '</tbody></table>';
      continue;
    }
    body += '<div class="e">';
    body += `<div class="sig">${esc(e.s)}</div>`;
    body += `<div class="def">${esc(e.d)}</div>`;
    if (e.ex) {
      body += `<div class="ex"><span class="q">${hl(e.ex)}</span>` +
              `<span class="r${e.failed?' bad':''}">${esc(e.result)}</span></div>`;
    } else if (e.plain) {
      body += `<div class="ex"><span class="q plain">${hl(e.plain)}</span></div>`;
    }
    body += '</div>';
  }

  const toc = secs.map(s => `<li><span class="tn">${esc(s.title.split(' · ')[0])}</span>` +
                            `<span>${esc(s.title.split(' · ').slice(1).join(' · '))}</span></li>`).join('');

  const html = `<!doctype html><html><head><meta charset="utf-8">
<title>SQL Syntax Reference</title>
<style>
@page { size: A4; margin: 14mm 12mm 16mm 12mm; }
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact; print-color-adjust:exact}
body{
  margin:0; font-family:"Source Sans 3","Helvetica Neue",Arial,sans-serif;
  font-size:8.6pt; line-height:1.34; color:#10192A;
}
code,.mono,.sig,.ex,.dial .code{font-family:"JetBrains Mono","DejaVu Sans Mono",Menlo,monospace}

/* ---- cover ---- */
.cover{page-break-after:always; padding-top:26mm}
.cover h1{font-size:30pt; line-height:1.05; margin:0 0 6mm; letter-spacing:-.02em; font-weight:700}
.cover .sub{font-size:11pt; color:#55627A; max-width:150mm; line-height:1.5}
.cover .rule{height:3px; background:#2A5D8F; width:52mm; margin:8mm 0}
.cover .facts{margin-top:12mm; display:flex; gap:14mm; font-size:9pt}
.cover .facts b{display:block; font-size:19pt; color:#2A5D8F; font-weight:700}
.cover .facts span{color:#55627A}
.cover .how{margin-top:14mm; font-size:9pt; color:#3B4760; max-width:150mm; border-left:3px solid #DCE3EC; padding-left:5mm}
.cover .how b{color:#10192A}
.toc{margin-top:10mm; column-count:2; column-gap:10mm; font-size:9pt}
.toc ul{margin:0; padding:0; list-style:none}
.toc li{display:flex; gap:3mm; padding:1.1mm 0; break-inside:avoid}
.toc .tn{color:#B4690E; font-weight:700; font-family:"JetBrains Mono",monospace; min-width:6mm; text-align:right}

/* ---- sections ---- */
.sec{break-inside:auto}
h2{
  font-size:13pt; font-weight:700; margin:7mm 0 1.5mm; padding-bottom:1.2mm;
  border-bottom:1.6pt solid #10192A; letter-spacing:-.01em;
  break-after:avoid; break-inside:avoid;
}
.note{margin:0 0 2.5mm; color:#55627A; font-size:8.4pt; font-style:italic; break-after:avoid}

/* ---- one entry ---- */
.e{
  break-inside:avoid; padding:1.5mm 0 1.6mm; border-bottom:.4pt solid #E8EEF4;
  display:grid; grid-template-columns:58mm 1fr; column-gap:4mm; row-gap:.7mm;
}
.sig{grid-column:1; font-weight:700; font-size:8.3pt; color:#1D4570; word-break:break-word}
.def{grid-column:2}
.ex{grid-column:2; font-size:7.7pt; line-height:1.4}
.ex .q{display:block; color:#3B4760; white-space:pre-wrap; word-break:break-word}
.ex .q.plain{color:#55627A}
.ex .r{display:block; color:#1F6F4A; font-weight:700; margin-top:.3mm}
.ex .r::before{content:"→  "; color:#8593AA; font-weight:400}
.ex .r.bad{color:#A3282B}
.k{color:#1D4570; font-weight:700}
.s{color:#1F6F4A; font-style:normal}
.n{color:#A3502B; font-style:normal}
.c{color:#8593AA; font-style:italic}
.f{color:#7A3E9D; font-style:normal}

/* ---- dialect table ---- */
.dial{border-collapse:collapse; width:100%; font-size:7.6pt; margin-top:2mm}
.dial th{
  background:#F2F5F8; text-align:left; padding:1.4mm 2mm; border-bottom:1pt solid #C6D1DF;
  font-size:7.6pt; text-transform:uppercase; letter-spacing:.05em; color:#3B4760;
}
.dial td{padding:1.2mm 2mm; border-bottom:.4pt solid #E8EEF4; vertical-align:top}
.dial tr{break-inside:avoid}
.dial .task{font-weight:600; width:32mm}
.dial .code{color:#1D4570}
</style></head><body>

<div class="cover">
  <h1>SQL Syntax Reference</h1>
  <div class="rule"></div>
  <div class="sub">Every clause, operator and function you need for a PostgreSQL interview —
  each one with what it does in a single line, the syntax, a worked example, and the answer
  that example actually returns.</div>
  <div class="facts">
    <div><b>${ENTRIES.filter(e=>e.s).length}</b><span>entries</span></div>
    <div><b>${secs.length}</b><span>sections</span></div>
    <div><b>${ran}</b><span>live examples</span></div>
    <div><b>PG 18</b><span>dialect</span></div>
  </div>
  <div class="how">
    <b>How to read an entry.</b> The left column is the syntax. The right column is what it does,
    then the example, then <b>→</b> the real result. Every example was executed against the
    sql-prep teaching database while this document was generated — the results are recorded
    output, not illustrations.
  </div>
  <div class="toc"><ul>${toc}</ul></div>
</div>

${body}
</body></html>`;

  const htmlPath = path.join(HERE, 'dist', 'reference.html');
  fs.mkdirSync(path.dirname(htmlPath), {recursive:true});
  fs.writeFileSync(htmlPath, html);

  /* ---------- render ---------- */
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium',
    args:['--no-sandbox']
  });
  const page = await browser.newPage();
  await page.goto('file://' + htmlPath, { waitUntil:'load' });
  await page.emulateMedia({ media:'print' });
  fs.mkdirSync(path.dirname(OUT), {recursive:true});
  await page.pdf({
    path: OUT, format:'A4', printBackground:true,
    margin:{ top:'14mm', bottom:'16mm', left:'12mm', right:'12mm' },
    displayHeaderFooter:true,
    headerTemplate:'<div></div>',
    footerTemplate:
      '<div style="width:100%;font-size:7pt;color:#8593AA;padding:0 12mm;'+
      'font-family:Helvetica,Arial,sans-serif;display:flex;justify-content:space-between;">'+
      '<span>SQL Syntax Reference · PostgreSQL</span>'+
      '<span class="pageNumber"></span></div>'
  });
  await browser.close();

  const kb = (fs.statSync(OUT).size/1024).toFixed(0);
  console.log(`built ${OUT}  (${kb} KB)`);
  if (failed) { console.log(`\n${failed} example(s) failed — fix before shipping.`); process.exit(1); }
})().catch(e => { console.error(e); process.exit(1); });
