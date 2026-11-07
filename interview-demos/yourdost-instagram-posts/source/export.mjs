// Render each YourDOST post to its own PNG (1080 x 1350).
//   node export.mjs [outDir]
import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const { chromium } = createRequire(import.meta.url)("playwright");
const outDir = path.resolve(process.argv[2] || path.join(here, ".."));
fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(here, "studio.html")).href);
const posts = await page.evaluate(() => YDP.POSTS.map((p) => ({ id: p.id, slug: p.slug })));
for (const p of posts) {
  await page.evaluate((id) => window.show(id), p.id);
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((i) => i.decode().catch(() => {}))); });
  const over = await page.evaluate(() => { const el = document.querySelector(".post"); return el.scrollHeight - el.clientHeight; });
  if (over > 0) console.warn(`post ${p.id} overflows by ${over}px`);
  const file = path.join(outDir, `Post-${p.id}-${p.slug}.png`);
  await (await page.$(".post")).screenshot({ path: file });
  console.log(path.basename(file));
}
await browser.close();
