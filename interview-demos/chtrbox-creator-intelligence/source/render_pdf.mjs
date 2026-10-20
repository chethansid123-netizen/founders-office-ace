// Render plan.html to PDF with headless Chromium.
//   G=$(npm root -g) node render_pdf.mjs plan.html ../Creator-Intelligence-Engine-GTM-Plan.pdf
import { createRequire } from 'module';
import { resolve } from 'path';
const require = createRequire((process.env.G || '/usr/lib/node_modules') + '/');
const { chromium } = require('playwright');
const [, , src, out] = process.argv;
const browser = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage();
await page.goto('file://' + resolve(src), { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
await browser.close();
console.log('wrote', out);
