// Print guide.html to PDF with headless Chromium (Playwright).
//   node guide/render.cjs <html> <pdf>
const { chromium } = require("playwright");
const path = require("node:path");

const [, , htmlPath, pdfPath] = process.argv;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + path.resolve(htmlPath), { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: pdfPath,
    format: "A4",
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate:
      '<div style="width:100%;font:7pt Inter,sans-serif;color:#56645b;padding:0 15mm;display:flex;justify-content:space-between">' +
      "<span>Movers Signal · Presenter&#39;s guide · Independent prototype built from public filings. Not affiliated with Positive Moves.</span>" +
      '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    margin: { top: "16mm", bottom: "17mm", left: "15mm", right: "15mm" },
  });
  await browser.close();
})();
