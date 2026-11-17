// Screenshot every <section> of a built deck page. Usage: node shoot_slides.cjs <deck.html> <out_dir> [scale]
const { chromium } = require('playwright');
(async () => {
  const [file, out, scale] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: +(scale || 1) });
  await p.goto('file://' + require('path').resolve(file), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const n = await p.locator('section').count();
  for (let i = 0; i < n; i++) await p.locator('section').nth(i).screenshot({ path: `${out}/slide-${String(i + 1).padStart(2, '0')}.png` });
  // overflow report: any element whose box leaves its section or crosses the footer line
  const rep = await p.evaluate(() => [...document.querySelectorAll('section')].map(s => { const r = s.getBoundingClientRect(); const bad = [];
    s.querySelectorAll('*').forEach(e => { if (e.closest('.foot')) return; const q = e.getBoundingClientRect(); if (!q.width) return;
      if (q.bottom - r.top > 1080 || q.right - r.left > 1920 + 1) bad.push((e.className || e.tagName) + ' ' + Math.round(q.bottom - r.top) + 'x' + Math.round(q.right - r.left)); });
    return s.id + ': ' + (bad.slice(0, 6).join(' | ') || 'ok'); }));
  console.log(rep.join('\n')); await b.close();
})();
