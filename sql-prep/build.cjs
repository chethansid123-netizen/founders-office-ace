/* Assembles the standalone sandbox HTML: template + engine + payload + data + drills + app.
   Usage:  node build.js [outfile]
   Requires: npm i @electric-sql/pglite esbuild   (see README) */
const fs = require('fs'), path = require('path'), zlib = require('zlib'), cp = require('child_process');
const HERE = __dirname;
const OUT  = process.argv[2] || path.join(HERE, 'dist', 'sandbox.html');
const NM   = process.env.PGLITE_NODE_MODULES || path.join(HERE, 'node_modules');
const DIST = path.join(NM, '@electric-sql', 'pglite', 'dist');

function need(p){ if(!fs.existsSync(p)) { console.error('Missing: '+p+'\nRun: npm i @electric-sql/pglite esbuild'); process.exit(1);} return p; }
need(DIST);

// 1. bundle pglite to a single IIFE exposing window.PGLITE
const tmp = path.join(HERE, '.build');
fs.mkdirSync(tmp, {recursive:true});
// import by absolute path so resolution does not depend on where node_modules sits
fs.writeFileSync(path.join(tmp,'entry.js'),
  'export { PGlite } from ' + JSON.stringify(path.join(DIST,'index.js').split(path.sep).join('/')) + ';\n');
const esbuild = need(path.join(NM,'.bin','esbuild'));
cp.execFileSync(esbuild, [
  path.join(tmp,'entry.js'), '--bundle', '--format=iife', '--global-name=PGLITE',
  '--platform=browser', '--target=es2020', '--minify',
  '--define:import.meta.url="file:///pglite.js"',
  '--outfile='+path.join(tmp,'pglite.iife.js')
], {stdio:'inherit'});

// 2. gzip + base64 the three binary assets
const gz = f => zlib.gzipSync(fs.readFileSync(path.join(DIST,f)), {level:9}).toString('base64');
const payload =
  'window.__PG_WASM_GZ='   + JSON.stringify(gz('pglite.wasm'))  + ';\n' +
  'window.__PG_INITDB_GZ=' + JSON.stringify(gz('initdb.wasm'))  + ';\n' +
  'window.__PG_DATA_GZ='   + JSON.stringify(gz('pglite.data'))  + ';\n';

// 3. the teaching database, as JS strings
const rd = f => fs.readFileSync(path.join(HERE,f),'utf8');
const data =
  'window.__SCHEMA_SQL=' + JSON.stringify(rd('01_schema.sql')) + ';\n' +
  'window.__SEED_SQL='   + JSON.stringify(rd('02_seed.sql'))   + ';\n';

// 4. stitch it together
const html = rd('sandbox.template.html')
  + '\n<script>' + fs.readFileSync(path.join(tmp,'pglite.iife.js'),'utf8') + '</script>\n'
  + '<script>' + payload + '</script>\n'
  + '<script>' + data + '</script>\n'
  + '<script>' + rd('drills.js') + '</script>\n'
  + '<script>' + rd('app.js') + '</script>\n';

fs.mkdirSync(path.dirname(OUT), {recursive:true});
fs.writeFileSync(OUT, html);
fs.rmSync(tmp, {recursive:true, force:true});
console.log('built ' + OUT + '  (' + (html.length/1048576).toFixed(2) + ' MB)');
