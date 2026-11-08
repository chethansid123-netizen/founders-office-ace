// Export the v7 posts (1080x1350 PNG) with an UPLOAD.md each.   node export.mjs [outDir] [--only=21,24]
import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const args = process.argv.slice(2);
const outDir = path.resolve(args.find((a) => !a.startsWith("--")) || path.join(here, ".."));
const only = (args.find((a) => a.startsWith("--only=")) || "").slice(7).split(",").filter(Boolean);
require(path.join(here, "posts.js"));
const POSTS = globalThis.YD7.POSTS;
let MOTION = {};
try { MOTION = require(path.join(here, "motion_meta.cjs")); } catch {}

const common = ["Paste the caption and hashtags below. Add the alt text under Advanced settings → Accessibility.",
  "Post the first comment below from the YourDOST account and pin it.",
  "Reply to comments in the first hour. If a comment suggests someone is in crisis, reply kindly with Tele MANAS 14416 (free, 24/7), send a DM, and flag it to the clinical team."];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(here, "posts.html")).href);
for (const p of POSTS) {
  if (only.length && !only.includes(p.id)) continue;
  const dir = path.join(outDir, `${p.id}-${p.slug}`);
  fs.mkdirSync(dir, { recursive: true });
  const files = [];
  for (let i = 0; i < p.slides.length; i++) {
    await page.evaluate(([id, i]) => window.show(id, i), [p.id, i]);
    await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((im) => im.decode().catch(() => {}))); await new Promise((r) => setTimeout(r, 250)); });
    const name = p.kind === "single" ? "Post.png" : `Slide-${String(i + 1).padStart(2, "0")}.png`;
    await (await page.$("#stage > .f")).screenshot({ path: path.join(dir, name) });
    files.push(name);
  }
  const m = MOTION[p.id];
  const steps = p.kind === "single"
    ? ["Tap + → Post → select Post.png.", "Set the crop to 4:5 (portrait) so nothing is cut off."]
    : [`Tap + → Post → select all ${p.slides.length} slides in order (Slide-01 first).`, "Set the crop to 4:5 (portrait) so nothing is cut off."];
  fs.writeFileSync(path.join(dir, "UPLOAD.md"), `# Post ${p.id}: ${p.theme}

**The line:** ${p.line}
**Why it works:** ${p.why}
**Format:** ${p.kind === "single" ? "Original format, single image, 4:5 (1080 × 1350)" : `Carousel, ${p.slides.length} slides, 4:5 (1080 × 1350)`}
**For (segment):** ${p.segment}
**Post on:** ${p.date}, ${p.time}

## Files, in upload order
${files.map((f, i) => `${i + 1}. ${f}`).join("\n")}
${m ? `\n**Motion version:** \`Motion.mp4\` (${m.format}). ${m.note}\n` : ""}
## How to upload
${[...steps, ...common].map((s, i) => `${i + 1}. ${s}`).join("\n")}
${m ? `\nTo post the motion version instead: Tap + → Reel → Motion.mp4, keep its original audio, and use the same caption.\n` : ""}
## Caption
${p.caption}

${p.tags}

## First comment (pin it)
${p.first}

## Alt text
${p.alt.length > 1 ? p.alt.map((a, i) => `- Image ${i + 1}: ${a}`).join("\n") : p.alt[0]}
`);
  console.log(p.id, files.length, "files");
}
await browser.close();
