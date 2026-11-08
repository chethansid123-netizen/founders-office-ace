// Export the two v5 posts as PNGs (1080x1350) with an UPLOAD.md each.   node export.mjs [outDir]
import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const outDir = path.resolve(process.argv[2] || path.join(here, ".."));
require(path.join(here, "v5.js"));
const POSTS = globalThis.YD5.POSTS;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(here, "studio.html")).href);
for (const p of POSTS) {
  const dir = path.join(outDir, `${p.id}-${p.slug}`);
  fs.mkdirSync(dir, { recursive: true });
  const files = [];
  for (let i = 0; i < p.slides.length; i++) {
    await page.evaluate(([id, i]) => window.show(id, i), [p.id, i]);
    await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((im) => im.decode().catch(() => {}))); await new Promise((r) => setTimeout(r, 150)); });
    const name = p.kind === "single" ? "Post.png" : `Slide-${String(i + 1).padStart(2, "0")}.png`;
    await (await page.$("#stage > .f")).screenshot({ path: path.join(dir, name) });
    files.push(name);
  }
  fs.writeFileSync(path.join(dir, "UPLOAD.md"), `# Post ${p.id}: ${p.theme}

**The line:** ${p.line}
**Why:** ${p.why}
**Format:** ${p.kind === "single" ? "Single image, 4:5 (1080 × 1350)" : `Carousel, ${p.slides.length} slides, 4:5 (1080 × 1350)`}
**For:** ${p.segment}
**Post on:** ${p.date}, ${p.time}

## Files, in upload order
${files.map((f, i) => `${i + 1}. ${f}`).join("\n")}

## How to upload
1. Tap + → Post → select ${p.kind === "single" ? "Post.png" : `all ${files.length} slides in order (Slide-01 first)`}.
2. Set the crop to 4:5 (portrait) so nothing is cut off.
3. Paste the caption and hashtags below. Add the alt text under Advanced settings → Accessibility.
4. Post the first comment below from the YourDOST account and pin it.
5. Reply to comments in the first hour. If a comment suggests someone is in crisis, reply kindly with Tele MANAS 14416 (free, 24/7), send a DM, and flag it to the clinical team.

## Caption
${p.caption}

${p.tags}

## First comment (pin it)
${p.first}

## Alt text
${p.alt.map((a, i) => (p.alt.length > 1 ? `- Image ${i + 1}: ${a}` : a)).join("\n")}
`);
  console.log(p.id, files.length, "files");
}
await browser.close();
