// node pdf.js <html> <out.pdf> [light|dark] [slideIdsCommaSeparated]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [,, file, out, theme, only] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  if (theme === 'dark') await p.addInitScript(() => { try { localStorage.setItem('cdt-theme', 'dark'); } catch (e) {} });
  await p.goto('file://' + file + '?print');
  await p.waitForTimeout(300);
  if (only) {
    const keep = only.split(',').map(s => '#' + s + '.slide').join(', ');
    await p.addStyleTag({ content: `body.printing .slide:not(${keep}) { display: none !important; }` });
  }
  const over = await p.$$eval('.slide', ss => ss.filter(s => getComputedStyle(s).display !== 'none')
    .map(s => [s.id, s.scrollHeight]).filter(([, h]) => h > 900));
  console.log('overflowing slides:', JSON.stringify(over));
  await p.emulateMedia({ media: 'print' });
  await p.pdf({ path: out, width: '1440px', height: '900px', printBackground: true, preferCSSPageSize: true });
  console.log('errors:', JSON.stringify(errs));
  await b.close();
})();
