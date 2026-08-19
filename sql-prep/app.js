/* ===================== Postgres Interview Sandbox — app logic ===================== */
(function(){
'use strict';
var $  = function(s,r){ return (r||document).querySelector(s); };
var $$ = function(s,r){ return Array.prototype.slice.call((r||document).querySelectorAll(s)); };

/* ---------- theme ---------- */
var root = document.documentElement;
$('#btntheme').addEventListener('click', function(){
  var cur = root.getAttribute('data-theme');
  if(!cur) cur = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  root.setAttribute('data-theme', cur === 'dark' ? 'light' : 'dark');
});

/* ---------- SQL syntax highlighting ---------- */
var KW = ('select from where group by having order limit offset join inner left right full outer cross on using natural '+
'union all intersect except with recursive as distinct case when then else end and or not null is in between like ilike '+
'exists any some insert into values update set delete truncate create table view materialized index unique primary key '+
'foreign references default check constraint alter add drop column rename to cascade restrict generated always identity '+
'stored partition over rows range groups unbounded preceding following current row filter window lateral asc desc nulls '+
'first last begin commit rollback savepoint transaction isolation level explain analyze returning conflict do nothing '+
'merge matched temp if not exists cast interval date timestamp timestamptz integer bigint smallint numeric text boolean '+
'varchar real serial uuid jsonb array replace function language trigger before after each for execute declare return '+
'fetch next only ties within grouping sets rollup cube').split(' ');
var FN = ('count sum avg min max round abs ceil floor trunc mod power sqrt greatest least coalesce nullif upper lower '+
'initcap length substring left right trim ltrim rtrim position strpos split_part lpad rpad concat concat_ws now '+
'current_date current_timestamp date_trunc extract age to_char to_date generate_series row_number rank dense_rank '+
'percent_rank cume_dist ntile lag lead first_value last_value nth_value string_agg array_agg bool_and bool_or stddev '+
'variance percentile_cont percentile_disc mode repeat regexp_replace').split(' ');
var KWSET = {}, FNSET = {};
KW.forEach(function(w){ KWSET[w] = 1; });
FN.forEach(function(w){ FNSET[w] = 1; });

function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

/* Single-pass SQL tokenizer. Scanning strictly left to right means a comment or
   string literal is consumed whole, so its contents can never be re-scanned and
   mis-coloured as keywords or numbers. */
var TOK = /(--[^\n]*)|(\/\*[\s\S]*?\*\/)|('(?:[^']|'')*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][A-Za-z_0-9]*)/g;
function highlight(src){
  var out = '', last = 0, m;
  TOK.lastIndex = 0;
  while((m = TOK.exec(src)) !== null){
    out += esc(src.slice(last, m.index));
    var t = m[0];
    if(m[1] || m[2])  out += '<span class="tok-com">' + esc(t) + '</span>';
    else if(m[3])     out += '<span class="tok-str">' + esc(t) + '</span>';
    else if(m[4])     out += '<span class="tok-num">' + esc(t) + '</span>';
    else {
      var lw = t.toLowerCase();
      var isCall = /^\s*\(/.test(src.slice(TOK.lastIndex));
      if(KWSET[lw])                    out += '<span class="tok-kw">' + esc(t) + '</span>';
      else if(FNSET[lw] || isCall)     out += '<span class="tok-fn">' + esc(t) + '</span>';
      else                             out += esc(t);
    }
    last = TOK.lastIndex;
  }
  out += esc(src.slice(last));
  return out;
}

/* ---------- engine ---------- */
var db = null, ready = false;
var chip = $('#enginechip'), cstat = $('#cstat'), cout = $('#cout'), editor = $('#editor');

function say(html, cls){ cout.innerHTML = '<div class="msg '+(cls||'hint')+'">'+html+'</div>'; }

function b64ToBytes(b64){
  var bin = atob(b64), len = bin.length, out = new Uint8Array(len);
  for(var i=0;i<len;i++) out[i] = bin.charCodeAt(i);
  return out;
}
function gunzip(bytes){
  var s = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
  return new Response(s).arrayBuffer();
}

function boot(){
  var t0 = Date.now();
  cstat.textContent = 'decompressing...';
  return Promise.all([
    gunzip(b64ToBytes(window.__PG_WASM_GZ)),
    gunzip(b64ToBytes(window.__PG_INITDB_GZ)),
    gunzip(b64ToBytes(window.__PG_DATA_GZ))
  ]).then(function(bufs){
    window.__PG_WASM_GZ = window.__PG_INITDB_GZ = window.__PG_DATA_GZ = null;
    cstat.textContent = 'compiling...';
    return Promise.all([
      WebAssembly.compile(bufs[0]),
      WebAssembly.compile(bufs[1]),
      Promise.resolve(bufs[2])
    ]);
  }).then(function(p){
    cstat.textContent = 'initialising postgres...';
    return PGLITE.PGlite.create({
      pgliteWasmModule: p[0],
      initdbWasmModule: p[1],
      fsBundle: new Blob([p[2]], {type:'application/octet-stream'})
    });
  }).then(function(inst){
    db = inst;
    return seed();
  }).then(function(){
    return db.query('select version() as v');
  }).then(function(r){
    ready = true;
    var secs = ((Date.now()-t0)/1000).toFixed(1);
    var v = String(r.rows[0].v).split(' ').slice(0,2).join(' ');
    chip.textContent = '● ' + v + ' ready';
    cstat.textContent = 'ready in ' + secs + 's';
    say('PostgreSQL is running. Press <b>Run</b> on any example above, or write a query here and hit '+
        '<b>Ctrl/Cmd + Enter</b>.', 'hint');
    return loadSchema();
  }).catch(function(e){
    chip.textContent = '● engine unavailable';
    chip.classList.remove('live');
    cstat.textContent = 'unavailable';
    say('The SQL engine could not start in this browser:\n\n' + esc(e && e.message ? e.message : String(e)) +
        '\n\nEverything else still works — the full reference and all 60 drills with their solutions are '+
        'above. Only the Run buttons need the engine.', 'err');
  });
}
function seed(){
  return db.exec(window.__SCHEMA_SQL).then(function(){ return db.exec(window.__SEED_SQL); });
}

/* ---------- rendering results ---------- */
function fmt(v){
  if(v === null || v === undefined)  return {t:'NULL', c:'null'};
  if(v instanceof Date)              return {t:v.toISOString().slice(0,19).replace('T',' '), c:''};
  if(typeof v === 'object')          return {t:JSON.stringify(v), c:''};
  return {t:String(v), c:''};
}
function renderResults(results, ms){
  var withCols = results.filter(function(r){ return r && r.fields && r.fields.length; });
  if(!withCols.length){
    var n = results.reduce(function(a,r){ return a + ((r && r.affectedRows) || 0); }, 0);
    cout.innerHTML = '<div class="msg ok">✔ Statement OK — '+n+' row'+(n===1?'':'s')+
                     ' affected · '+ms+' ms</div>';
    return;
  }
  var html = '';
  withCols.forEach(function(res, idx){
    var cols = res.fields.map(function(f){ return f.name; });
    if(withCols.length > 1) html += '<div class="msg hint">result '+(idx+1)+' of '+withCols.length+'</div>';
    html += '<table class="grid"><thead><tr>';
    cols.forEach(function(c){ html += '<th>'+esc(c)+'</th>'; });
    html += '</tr></thead><tbody>';
    res.rows.slice(0,500).forEach(function(row){
      html += '<tr>';
      cols.forEach(function(c){ var f = fmt(row[c]); html += '<td class="'+f.c+'">'+esc(f.t)+'</td>'; });
      html += '</tr>';
    });
    html += '</tbody></table>';
    html += '<div class="msg ok">✔ '+res.rows.length+' row'+(res.rows.length===1?'':'s')+
            (res.rows.length>500 ? ' (showing first 500)' : '')+' · '+ms+' ms</div>';
  });
  cout.innerHTML = html;
}

function runSQL(sql){
  if(!ready){ say('The engine is still starting — give it a moment.','hint'); return Promise.resolve(null); }
  var t0 = performance.now();
  cstat.textContent = 'running...';
  return db.exec(sql).then(function(res){
    var ms = Math.round(performance.now()-t0);
    renderResults(res, ms);
    cstat.textContent = 'ok · '+ms+' ms';
    return res;
  }).catch(function(e){
    cstat.textContent = 'error';
    say(esc(e && e.message ? e.message : String(e)), 'err');
    return null;
  });
}

/* ---------- console controls ---------- */
var consoleEl = $('#console');
function openConsole(){ consoleEl.classList.remove('min'); $('#btnmin').textContent = '▾'; }
$('#btnmin').addEventListener('click', function(){
  consoleEl.classList.toggle('min');
  this.textContent = consoleEl.classList.contains('min') ? '▴' : '▾';
});
$('#btnrun').addEventListener('click', function(){ openConsole(); runSQL(editor.value); });
editor.addEventListener('keydown', function(e){
  if((e.metaKey||e.ctrlKey) && e.key === 'Enter'){ e.preventDefault(); runSQL(editor.value); }
});
$('#btnreset').addEventListener('click', function(){
  if(!ready) return;
  cstat.textContent = 'resetting...';
  say('Rebuilding the database...','hint');
  seed().then(function(){
    say('Database reset to its original state — all 8 tables reseeded.','ok');
    cstat.textContent = 'reset';
    loadSchema();
  }).catch(function(e){ say(esc(e.message),'err'); });
});

/* drag the console header to resize */
(function(){
  var head = $('#chead'), dragging = false, startY = 0, startH = 0;
  head.addEventListener('mousedown', function(e){
    if(e.target.tagName === 'BUTTON') return;
    dragging = true; startY = e.clientY; startH = consoleEl.offsetHeight; e.preventDefault();
  });
  window.addEventListener('mousemove', function(e){
    if(!dragging) return;
    var h = Math.min(Math.max(startH + (startY - e.clientY), 42), window.innerHeight - 80);
    consoleEl.style.height = h + 'px';
    $('.main').style.setProperty('--console-h', h + 'px');
  });
  window.addEventListener('mouseup', function(){ dragging = false; });
})();

/* ---------- decorate code blocks: highlight + Run button ---------- */
$$('.code').forEach(function(box){
  var pre = box.querySelector('pre');
  var raw = pre.textContent;
  pre.innerHTML = highlight(raw);
  if(box.classList.contains('syntax')) return;
  var bar = document.createElement('div');
  bar.className = 'runbar';
  var b = document.createElement('button');
  b.className = 'run'; b.type = 'button'; b.textContent = 'Run ▶';
  b.addEventListener('click', function(){
    editor.value = raw;
    $('#btncheck').hidden = true;
    currentDrill = null;
    openConsole();
    runSQL(raw);
  });
  bar.appendChild(b);
  box.appendChild(bar);
});

/* ---------- schema browser ---------- */
function loadSchema(){
  if(!db) return Promise.resolve();
  return db.query(
    "SELECT c.table_name, c.column_name, c.data_type, "+
    "       COALESCE(k.is_pk, false) AS is_pk "+
    "FROM information_schema.columns c "+
    "LEFT JOIN ( "+
    "  SELECT kcu.table_name, kcu.column_name, true AS is_pk "+
    "  FROM information_schema.table_constraints tc "+
    "  JOIN information_schema.key_column_usage kcu "+
    "    ON kcu.constraint_name = tc.constraint_name "+
    "  WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.table_schema = 'public' "+
    ") k ON k.table_name = c.table_name AND k.column_name = c.column_name "+
    "WHERE c.table_schema = 'public' "+
    "ORDER BY c.table_name, c.ordinal_position"
  ).then(function(r){
    var tables = {};
    r.rows.forEach(function(row){
      (tables[row.table_name] = tables[row.table_name] || []).push(row);
    });
    var order = ['customers','orders','order_items','products','employees',
                 'departments','web_events','staging_signups'];
    var names = Object.keys(tables).sort(function(a,b){
      var ia = order.indexOf(a), ib = order.indexOf(b);
      return (ia<0?99:ia) - (ib<0?99:ib) || a.localeCompare(b);
    });
    var short = {'character varying':'varchar','timestamp without time zone':'timestamp',
      'timestamp with time zone':'timestamptz','double precision':'float8','integer':'int'};
    var html = '';
    names.forEach(function(t){
      html += '<details><summary>'+esc(t)+'</summary><div class="cols">';
      tables[t].forEach(function(c){
        var ty = short[c.data_type] || c.data_type;
        html += '<div>'+(c.is_pk ? '<span class="pk">◆</span> ' : '')+esc(c.column_name)+
                ' <span class="t">'+esc(ty)+'</span></div>';
      });
      html += '</div></details>';
    });
    $('#schema').innerHTML = html;
  }).catch(function(){ /* schema browser is a nicety; never block on it */ });
}

/* ---------- drills ---------- */
var LVL = {e:['e','Easy'], m:['m','Medium'], h:['h','Hard']};
var currentDrill = null;
function drill(id){
  return window.DRILLS.filter(function(x){ return String(x.id) === String(id); })[0];
}
(function renderDrills(){
  var wrap = $('#drills'), html = '';
  window.DRILLS.forEach(function(d){
    var lv = LVL[d.lvl];
    html +=
      '<details class="drill" id="drill'+d.id+'">'+
        '<summary class="dhead">'+
          '<span class="id">'+(d.id<10?'0':'')+d.id+'</span>'+
          '<span class="q">'+esc(d.q)+'</span>'+
          '<span class="lvl '+lv[0]+'">'+lv[1]+'</span>'+
        '</summary>'+
        '<div class="dbody">'+
          '<div class="lab">Topic</div><p style="margin-top:0">'+esc(d.t)+
            (d.ordered ? ' · <em>row order matters</em>' : '')+'</p>'+
          '<div class="lab">Hint</div><p>'+esc(d.h)+'</p>'+
          '<div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 4px">'+
            '<button class="cbtn primary" data-attempt="'+d.id+'">Attempt this</button>'+
            '<button class="cbtn" data-reveal="'+d.id+'">Show solution</button>'+
          '</div>'+
          '<div id="sol'+d.id+'" hidden>'+
            '<div class="lab ex">Model solution</div>'+
            '<div class="code"><pre>'+highlight(d.sol)+'</pre>'+
              '<div class="runbar"><button class="run" data-runsol="'+d.id+'">Run ▶</button></div>'+
            '</div>'+
          '</div>'+
        '</div>'+
      '</details>';
  });
  wrap.innerHTML = html;

  wrap.addEventListener('click', function(e){
    var t = e.target, id;
    if(!t || !t.getAttribute) return;
    if((id = t.getAttribute('data-attempt'))){
      var d = drill(id);
      currentDrill = d;
      editor.value = '-- Drill '+d.id+': '+d.q+'\n-- Hint: '+d.h+'\n\n';
      $('#btncheck').hidden = false;
      openConsole();
      editor.focus();
      say('Write your query, then press <b>Check my answer</b>. It runs your SQL and the model solution '+
          'against the real database and compares the two result sets.','hint');
    } else if((id = t.getAttribute('data-reveal'))){
      var box = $('#sol'+id);
      box.hidden = !box.hidden;
      t.textContent = box.hidden ? 'Show solution' : 'Hide solution';
    } else if((id = t.getAttribute('data-runsol'))){
      var dd = drill(id);
      editor.value = dd.sol;
      currentDrill = dd;
      $('#btncheck').hidden = false;
      openConsole();
      runSQL(dd.sol);
    }
  });
})();

/* ---------- answer checking ---------- */
function normCell(v){
  if(v === null || v === undefined) return 'NULL';
  if(v instanceof Date)             return v.toISOString().slice(0,10);
  if(typeof v === 'boolean')        return v ? 't' : 'f';
  if(typeof v === 'object')         return JSON.stringify(v);
  var n = Number(v);
  if(v !== '' && isFinite(n))       return String(Math.round(n*10000)/10000);
  return String(v);
}
function normRows(res){
  if(!res || !res.fields) return null;
  var cols = res.fields.map(function(f){ return f.name; });
  return res.rows.map(function(r){
    return JSON.stringify(cols.map(function(c){ return normCell(r[c]); }));
  });
}
function showRow(json){
  try { return JSON.parse(json).join('  |  '); } catch(e){ return json; }
}

$('#btncheck').addEventListener('click', function(){
  if(!currentDrill || !ready) return;
  var d = currentDrill, userSQL = editor.value;
  if(!/\S/.test(userSQL.replace(/--[^\n]*/g,''))){
    say('Write a query first, then press Check my answer.','hint');
    return;
  }
  var t0 = performance.now(), userRes, solRes;
  db.exec(userSQL).then(function(r){
    userRes = r.filter(function(x){ return x.fields && x.fields.length; }).pop();
    return db.exec(d.sol);
  }).then(function(r){
    solRes = r.filter(function(x){ return x.fields && x.fields.length; }).pop();
    var ms = Math.round(performance.now()-t0);
    var u = normRows(userRes), s = normRows(solRes);
    if(!u){
      say('Your statement did not return a result set — a drill answer should be a SELECT.','err');
      return;
    }
    var msgs = [], ok = true;
    var uc = userRes.fields.length, sc = solRes.fields.length;
    if(uc !== sc){ ok = false; msgs.push('Column count: you returned '+uc+', the solution returns '+sc+'.'); }
    if(u.length !== s.length){ ok = false; msgs.push('Row count: you returned '+u.length+', the solution returns '+s.length+'.'); }
    if(ok){
      var uu = u.slice(), ss = s.slice();
      if(!d.ordered){ uu.sort(); ss.sort(); }
      for(var i=0;i<uu.length;i++){
        if(uu[i] !== ss[i]){
          ok = false;
          msgs.push('First difference at row '+(i+1)+':\n    yours     '+showRow(uu[i])+
                    '\n    expected  '+showRow(ss[i]));
          break;
        }
      }
      if(ok && d.ordered) msgs.push('Row order matched too.');
    }
    renderResults([userRes], ms);
    var banner = ok
      ? '<div class="msg ok">✔ <b>Correct</b> — your result set matches the model solution'+
        (d.ordered ? ', including row order.' : '. (Row order was ignored for this drill.)')+'</div>'
      : '<div class="msg err">✘ <b>Not a match yet.</b>\n\n'+esc(msgs.join('\n\n'))+
        '\n\nColumn names are ignored; column order and values are compared.</div>';
    cout.insertAdjacentHTML('afterbegin', banner);
    cstat.textContent = ok ? 'correct' : 'no match';
  }).catch(function(e){
    say('Your query raised an error:\n\n'+esc(e && e.message ? e.message : String(e)),'err');
    cstat.textContent = 'error';
  });
});

/* ---------- nav: scrollspy + mobile drawer ---------- */
var links = $$('.nav a');
var secs  = links.map(function(a){ return document.getElementById(a.getAttribute('href').slice(1)); });
function spy(){
  var y = window.scrollY + 90, best = 0;
  for(var i=0;i<secs.length;i++){ if(secs[i] && secs[i].offsetTop <= y) best = i; }
  links.forEach(function(a,i){ a.classList.toggle('on', i === best); });
}
window.addEventListener('scroll', spy, {passive:true});
spy();

var sidebar = $('#sidebar'), scrim = $('#scrim');
function closeNav(){ sidebar.classList.remove('open'); scrim.classList.remove('on'); }
$('#menubtn').addEventListener('click', function(){
  sidebar.classList.toggle('open');
  scrim.classList.toggle('on');
});
scrim.addEventListener('click', closeNav);
links.forEach(function(a){ a.addEventListener('click', closeNav); });

/* ---------- go ---------- */
boot();
})();
