#!/usr/bin/env node
/* Terminal practice runner — the same real PostgreSQL engine the web sandbox uses,
   so results match exactly. No Docker, no server, no install beyond one npm package.

     npm i @electric-sql/pglite
     node runner.cjs

   Commands inside the REPL:
     \d              list tables
     \d <table>      describe one table
     \drill <n>      show drill n
     \sol  <n>       show the model solution for drill n
     \check <n>      check the query you last ran against drill n's solution
     \list [easy|medium|hard]   list drills
     \reset          rebuild the database
     \q              quit
   Anything else is executed as SQL. End with ';' or just press enter twice. */
'use strict';
const fs = require('fs'), path = require('path'), readline = require('readline'), vm = require('vm');
const HERE = __dirname;

let PGlite;
try { ({ PGlite } = require('@electric-sql/pglite')); }
catch (e) {
  console.error('\nMissing dependency. Run:\n\n    npm i @electric-sql/pglite\n');
  process.exit(1);
}

const sbx = { window: {} };
vm.createContext(sbx);
vm.runInContext(fs.readFileSync(path.join(HERE, 'drills.js'), 'utf8'), sbx);
const DRILLS = sbx.window.DRILLS;

const SCHEMA = fs.readFileSync(path.join(HERE, '01_schema.sql'), 'utf8');
const SEED   = fs.readFileSync(path.join(HERE, '02_seed.sql'), 'utf8');

const C = process.stdout.isTTY
  ? { d:'\x1b[2m', b:'\x1b[1m', g:'\x1b[32m', r:'\x1b[31m', y:'\x1b[33m', c:'\x1b[36m', x:'\x1b[0m' }
  : { d:'', b:'', g:'', r:'', y:'', c:'', x:'' };

function cell(v){
  if (v === null || v === undefined) return 'NULL';
  if (v instanceof Date) return v.toISOString().slice(0, 10);
  if (typeof v === 'object') return JSON.stringify(v);
  return String(v);
}
function table(res){
  if (!res || !res.fields || !res.fields.length) return C.d + '(no rows returned)' + C.x;
  const cols = res.fields.map(f => f.name);
  const rows = res.rows.map(r => cols.map(c => cell(r[c])));
  const w = cols.map((c, i) => Math.min(38, Math.max(c.length, ...rows.map(r => r[i].length), 1)));
  const pad = (s, n) => (s.length > n ? s.slice(0, n - 1) + '…' : s + ' '.repeat(n - s.length));
  const line = (l, m, r) => l + w.map(n => '─'.repeat(n + 2)).join(m) + r;
  let out = line('┌', '┬', '┐') + '\n│ ' + cols.map((c, i) => C.b + pad(c, w[i]) + C.x).join(' │ ') + ' │\n'
          + line('├', '┼', '┤') + '\n';
  for (const r of rows.slice(0, 100))
    out += '│ ' + r.map((v, i) => (v === 'NULL' ? C.d + pad(v, w[i]) + C.x : pad(v, w[i]))).join(' │ ') + ' │\n';
  out += line('└', '┴', '┘');
  if (res.rows.length > 100) out += '\n' + C.d + `(showing 100 of ${res.rows.length} rows)` + C.x;
  else out += '\n' + C.d + `(${res.rows.length} row${res.rows.length === 1 ? '' : 's'})` + C.x;
  return out;
}
const norm = v => {
  if (v === null || v === undefined) return 'NULL';
  if (v instanceof Date) return v.toISOString().slice(0, 10);
  if (typeof v === 'boolean') return v ? 't' : 'f';
  if (typeof v === 'object') return JSON.stringify(v);
  const n = Number(v);
  return (v !== '' && isFinite(n)) ? String(Math.round(n * 1e4) / 1e4) : String(v);
};
const rowsOf = res => {
  if (!res || !res.fields) return null;
  const cols = res.fields.map(f => f.name);
  return res.rows.map(r => JSON.stringify(cols.map(c => norm(r[c]))));
};

(async () => {
  process.stdout.write('starting PostgreSQL… ');
  const db = await PGlite.create();
  const seed = async () => { await db.exec(SCHEMA); await db.exec(SEED); };
  await seed();
  const v = (await db.query('select version() as v')).rows[0].v.split(' ').slice(0, 2).join(' ');
  console.log(C.g + v + ' ready' + C.x);
  console.log(C.d + 'Type \\d for tables, \\list for drills, \\q to quit.' + C.x + '\n');

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout, prompt: 'sql> ' });
  let buf = '', lastSQL = '';
  rl.prompt();

  async function handleLine(raw){
    const line = raw.trim();

    if (!buf && line.startsWith('\\')) {
      const [cmd, arg] = [line.split(/\s+/)[0], line.split(/\s+/).slice(1).join(' ')];
      try {
        if (cmd === '\\q') { rl.close(); return; }
        else if (cmd === '\\reset') { await seed(); console.log(C.g + 'database reset' + C.x); }
        else if (cmd === '\\d' && !arg) {
          console.log(table(await db.query(
            "SELECT table_name, (SELECT count(*) FROM information_schema.columns c " +
            "WHERE c.table_name=t.table_name) AS columns FROM information_schema.tables t " +
            "WHERE table_schema='public' AND table_type='BASE TABLE' ORDER BY table_name")));
        }
        else if (cmd === '\\d') {
          console.log(table(await db.query(
            "SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns " +
            "WHERE table_schema='public' AND table_name=$1 ORDER BY ordinal_position", [arg])));
        }
        else if (cmd === '\\list') {
          const want = { easy:'e', medium:'m', hard:'h' }[arg] || null;
          DRILLS.filter(d => !want || d.lvl === want).forEach(d =>
            console.log(`${C.c}${String(d.id).padStart(2,'0')}${C.x} ${C.d}[${d.lvl}]${C.x} ${d.q}`));
        }
        else if (cmd === '\\drill' || cmd === '\\sol' || cmd === '\\check') {
          const d = DRILLS.find(x => String(x.id) === arg);
          if (!d) console.log(C.r + 'no such drill: ' + arg + C.x);
          else if (cmd === '\\drill')
            console.log(`${C.b}Drill ${d.id}${C.x} [${d.t}] ${d.q}\n${C.d}hint: ${d.h}${C.x}`);
          else if (cmd === '\\sol') console.log(C.y + d.sol + C.x);
          else {
            if (!lastSQL) console.log(C.r + 'run a query first, then \\check ' + arg + C.x);
            else {
              const mine = (await db.exec(lastSQL)).filter(r => r.fields && r.fields.length).pop();
              const want = (await db.exec(d.sol)).filter(r => r.fields && r.fields.length).pop();
              let u = rowsOf(mine), s = rowsOf(want), ok = true, why = [];
              if (!u) { ok = false; why.push('your statement returned no result set'); }
              else {
                if (mine.fields.length !== want.fields.length)
                  { ok = false; why.push(`column count ${mine.fields.length} vs ${want.fields.length}`); }
                if (ok && u.length !== s.length)
                  { ok = false; why.push(`row count ${u.length} vs ${s.length}`); }
                if (ok) {
                  if (!d.ordered) { u = u.slice().sort(); s = s.slice().sort(); }
                  for (let i = 0; i < u.length; i++) if (u[i] !== s[i]) {
                    ok = false;
                    why.push(`row ${i+1}:\n    yours    ${JSON.parse(u[i]).join('  |  ')}` +
                             `\n    expected ${JSON.parse(s[i]).join('  |  ')}`);
                    break;
                  }
                }
              }
              console.log(ok ? C.g + '✔ correct' + (d.ordered ? ' (order matched)' : ' (order ignored)') + C.x
                             : C.r + '✘ not a match — ' + why.join('; ') + C.x);
            }
          }
        }
        else console.log(C.r + 'unknown command ' + cmd + C.x);
      } catch (e) { console.log(C.r + e.message + C.x); }
      rl.prompt(); return;
    }

    buf += raw + '\n';
    if (!/;\s*$/.test(line) && line !== '') { rl.setPrompt('...> '); rl.prompt(); return; }
    const sql = buf.trim(); buf = ''; rl.setPrompt('sql> ');
    if (sql) {
      lastSQL = sql;
      try {
        const t0 = Date.now();
        const res = await db.exec(sql);
        const withCols = res.filter(r => r.fields && r.fields.length);
        if (withCols.length) withCols.forEach(r => console.log(table(r)));
        else console.log(C.g + 'OK' + C.x + C.d + ` (${res.reduce((a,r)=>a+(r.affectedRows||0),0)} rows affected)` + C.x);
        console.log(C.d + (Date.now() - t0) + ' ms' + C.x);
      } catch (e) { console.log(C.r + e.message + C.x); }
    }
    rl.prompt();
  }

  // readline delivers piped input faster than an async handler can finish, so
  // serialise the lines onto one promise chain instead of letting them interleave.
  let chain = Promise.resolve();
  rl.on('line', (raw) => {
    chain = chain
      .then(() => handleLine(raw))
      .catch((e) => { console.log(C.r + e.message + C.x); rl.prompt(); });
  });

  rl.on('close', () => { console.log('\nbye'); process.exit(0); });
})().catch(e => { console.error(e); process.exit(1); });
