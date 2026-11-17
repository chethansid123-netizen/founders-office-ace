// List every <a href> on each slide with its box, for clickable links in the PPTX. Usage: node get_links.cjs <deck.html> <out.json>
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.resolve(file), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const links = await p.evaluate(() => [...document.querySelectorAll('section')].map(s => { const r = s.getBoundingClientRect();
    return [...s.querySelectorAll('a[href]')].map(a => { const q = a.getBoundingClientRect();
      return { href: a.href, x: q.left - r.left, y: q.top - r.top, w: q.width, h: q.height }; }); }));
  fs.writeFileSync(out, JSON.stringify(links, null, 1)); console.log(links.map((l, i) => `${i + 1}:${l.length}`).join(' ')); await b.close();
})();
