// Print an HTML document to A4 PDF and screenshot its top (desktop + phone). Usage: node doc_pdf.cjs <in.html> <out.pdf> <shot_prefix>
const { chromium, devices } = require('playwright'); const path = require('path');
(async () => {
  const [inp, pdf, shot] = process.argv.slice(2); const url = 'file://' + path.resolve(inp);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await p.goto(url, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: shot + '_desk.png' });
  await p.pdf({ path: pdf, format: 'A4', printBackground: true });
  const m = await (await b.newContext({ ...devices['iPhone 13'] })).newPage();
  await m.goto(url, { waitUntil: 'networkidle' });
  const over = await m.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  await m.screenshot({ path: shot + '_phone.png' });
  console.log(inp, 'phone horizontal overflow:', over); await b.close();
})();
