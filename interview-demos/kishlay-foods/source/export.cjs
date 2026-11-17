// Export the built deck page to a PDF and to 2x PNGs (for the PPTX). Usage: node export.cjs <deck.html> <out.pdf> <png_dir>
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [file, pdf, pngs] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(file), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await p.addStyleTag({ content: 'html,body{background:none!important}section{margin:0!important;page-break-after:always;break-after:page}' });
  const n = await p.locator('section').count();
  for (let i = 0; i < n; i++) await p.locator('section').nth(i).screenshot({ path: `${pngs}/slide-${String(i + 1).padStart(2, '0')}.png` });
  await p.pdf({ path: pdf, width: '1920px', height: '1080px', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  console.log('slides', n); await b.close();
})();
