#!/usr/bin/env node
/* Verification suite. Loads the schema + seed into a real PostgreSQL (PGlite) and checks:
     1. the seeded data has every property the teaching material depends on
     2. all 60 drill solutions execute and return rows
     3. every runnable example in the reference executes (2 are meant to fail, and are named)

     npm i @electric-sql/pglite
     node verify.cjs                                                              */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const HERE = __dirname;

let PGlite;
try { ({ PGlite } = require('@electric-sql/pglite')); }
catch (e) { console.error('\nRun:  npm i @electric-sql/pglite\n'); process.exit(1); }

const sbx = { window: {} };
vm.createContext(sbx);
vm.runInContext(fs.readFileSync(path.join(HERE, 'drills.js'), 'utf8'), sbx);
const DRILLS = sbx.window.DRILLS;

/* Reference examples that deliberately raise an error, because the error message
   IS the lesson. Keyed by a distinctive fragment of the SQL. */
const EXPECTED_FAILURES = [
  { match: 'SELECT dept_id, emp_name, COUNT(*)', why: 'teaches the GROUP BY error message' },
  { match: 'WHERE  RANK() OVER',                 why: 'teaches "window functions are not allowed in WHERE"' },
];

function extractExamples(){
  const html = fs.readFileSync(path.join(HERE, 'sandbox.template.html'), 'utf8');
  const un = s => s.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"')
                   .replace(/&#39;/g,"'").replace(/&amp;/g,'&');
  const re = /<div class="code([^"]*)"><pre>([\s\S]*?)<\/pre><\/div>/g;
  const out = []; let m;
  while ((m = re.exec(html))) {
    if (/syntax/.test(m[1])) continue;           // syntax skeletons are not runnable
    const before = html.slice(0, m.index);
    const part = [...before.matchAll(/id="p(\d\d)"/g)].pop();
    out.push({ part: part ? part[1] : '??', sql: un(m[2]) });
  }
  return out;
}

const CHECKS = {
  'customers = 14':                 ['SELECT count(*) n FROM customers', 14],
  'orders = 48':                    ['SELECT count(*) n FROM orders', 48],
  'order_items = 119':              ['SELECT count(*) n FROM order_items', 119],
  'web_events = 84':                ['SELECT count(*) n FROM web_events', 84],
  'customers with no orders = 3':   ['SELECT count(*) n FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.cust_id=c.cust_id)', 3],
  'products never ordered = 2':     ['SELECT count(*) n FROM products p WHERE NOT EXISTS (SELECT 1 FROM order_items i WHERE i.product_id=p.product_id)', 2],
  'empty departments = 2':          ['SELECT count(*) n FROM departments d WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.dept_id=d.dept_id)', 2],
  'NULL cities = 2':                ['SELECT count(*) n FROM customers WHERE city IS NULL', 2],
  'CEO has no manager/dept = 1':    ['SELECT count(*) n FROM employees WHERE manager_id IS NULL AND dept_id IS NULL', 1],
  'salary tie groups = 4':          ['SELECT count(*) n FROM (SELECT salary FROM employees GROUP BY salary HAVING count(*)>1) t', 4],
  'earns more than manager = 1':    ['SELECT count(*) n FROM employees e JOIN employees m ON e.manager_id=m.emp_id WHERE e.salary>m.salary', 1],
  'hierarchy is 4 deep':            [`WITH RECURSIVE t AS (SELECT emp_id,1 lvl FROM employees WHERE manager_id IS NULL
                                       UNION ALL SELECT e.emp_id,t.lvl+1 FROM employees e JOIN t ON e.manager_id=t.emp_id)
                                      SELECT max(lvl) n FROM t`, 4],
  'anonymous events = 10':          ['SELECT count(*) n FROM web_events WHERE cust_id IS NULL', 10],
  'six months of orders':           ["SELECT count(DISTINCT date_trunc('month',order_date)) n FROM orders", 6],
  'cust 1 active every month':      ["SELECT count(DISTINCT date_trunc('month',order_date)) n FROM orders WHERE cust_id=1", 6],
  'exact duplicate staging rows=2': ['SELECT count(*) n FROM (SELECT raw_email,raw_name,source,loaded_at FROM staging_signups GROUP BY 1,2,3,4 HAVING count(*)>1) t', 2],
  'all 4 order statuses present':   ['SELECT count(DISTINCT status) n FROM orders', 4],
  'cust 1 has 3 activity islands':  [`WITH d AS (SELECT DISTINCT event_at::date dt FROM web_events WHERE cust_id=1 AND event_type='page_view'),
                                       g AS (SELECT dt, dt - (row_number() OVER (ORDER BY dt))::int grp FROM d)
                                      SELECT count(*) n FROM (SELECT grp FROM g GROUP BY grp) t`, 3],
};

(async () => {
  const db = await PGlite.create();
  await db.exec(fs.readFileSync(path.join(HERE, '01_schema.sql'), 'utf8'));
  await db.exec(fs.readFileSync(path.join(HERE, '02_seed.sql'), 'utf8'));
  let failures = 0;

  console.log('\n── data properties ──');
  for (const [name, [sql, want]] of Object.entries(CHECKS)) {
    let got;
    try { got = Number((await db.query(sql)).rows[0].n); }
    catch (e) { got = 'ERROR: ' + e.message.split('\n')[0]; }
    const ok = got === want;
    if (!ok) failures++;
    console.log(`  ${ok ? 'ok  ' : 'FAIL'}  ${name}${ok ? '' : `  (got ${got}, want ${want})`}`);
  }

  console.log('\n── drill solutions ──');
  let dFail = 0, dEmpty = 0;
  for (const d of DRILLS) {
    try {
      const r = await db.query(d.sol);
      if (!r.rows.length) { dEmpty++; console.log(`  WARN  drill ${d.id} returned zero rows`); }
    } catch (e) { dFail++; failures++; console.log(`  FAIL  drill ${d.id}: ${e.message.split('\n')[0]}`); }
  }
  console.log(`  ${DRILLS.length} drills, ${dFail} errored, ${dEmpty} empty`);

  console.log('\n── reference examples ──');
  const ex = extractExamples();
  let unexpected = 0, expected = 0;
  for (const e of ex) {
    try { await db.exec(e.sql); }
    catch (err) {
      const known = EXPECTED_FAILURES.find(f => e.sql.includes(f.match));
      if (known) { expected++; console.log(`  ok    part ${e.part}: expected error — ${known.why}`); }
      else {
        unexpected++; failures++;
        console.log(`  FAIL  part ${e.part}: ${err.message.split('\n')[0]}`);
        console.log(`        ${e.sql.trim().split('\n')[0].slice(0, 90)}`);
      }
    }
  }
  console.log(`  ${ex.length} runnable blocks, ${expected} expected errors, ${unexpected} unexpected`);

  console.log(`\n${failures === 0 ? 'ALL CHECKS PASSED' : failures + ' CHECK(S) FAILED'}\n`);
  process.exit(failures === 0 ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
