// Export the v6 static posts (1080x1350 PNG) and write an UPLOAD.md for every post and reel.
//   node export.mjs [outDir] [--only=16,20]
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
require(path.join(here, "reels.js"));
const POSTS = globalThis.YD6.POSTS, REELS = globalThis.YD6R.REELS, META = require(path.join(here, "reels_meta.cjs"));

const steps = {
  carousel: (n) => [`Tap + → Post → select all ${n} slides in order (Slide-01 first).`, "Set the crop to 4:5 (portrait) so nothing is cut off."],
  single: () => ["Tap + → Post → select Post.png.", "Set the crop to 4:5 (portrait) so nothing is cut off."],
  reel: () => ["Tap + → Reel → select Reel.mp4. Keep the original audio on (music, sound and voice are already mixed in). Don't add Instagram music on top.",
    "Tap Edit cover → Add from camera roll → Cover.jpg (the hook frame).", "Turn on auto-generated captions as a backup; the key lines are already burned into the video."],
};
const common = ["Paste the caption and hashtags below. Add the alt text under Advanced settings → Accessibility.",
  "Post the first comment below from the YourDOST account and pin it.",
  "Reply to comments in the first hour. If a comment suggests someone is in crisis, reply kindly with Tele MANAS 14416 (free, 24/7), send a DM, and flag it to the clinical team."];
const md = (o) => `# ${o.title}

**The line:** ${o.line}
**Why it works:** ${o.why}
**Format:** ${o.format}
**For:** ${o.segment}
**Post on:** ${o.date}, ${o.time}
${o.audio ? `**Audio:** ${o.audio}\n` : ""}
## Files, in upload order
${o.files.map((f, i) => `${i + 1}. ${f}`).join("\n")}

## How to upload
${[...o.steps, ...common].map((s, i) => `${i + 1}. ${s}`).join("\n")}

## Caption
${o.caption}

${o.tags}

## First comment (pin it)
${o.first}

## Alt text
${o.alt}
`;

for (const [id, R] of Object.entries(REELS)) {
  if (only.length && !only.includes(id)) continue;
  const m = META[id], dir = path.join(outDir, R.slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, "UPLOAD.md"), md({ title: `Reel ${id}: ${m.theme}`, ...m, format: `Reel, ${R.dur} s, 9:16 (1080 × 1920), with music, sound and voice`,
    files: ["Reel.mp4", "Cover.jpg (cover image)"], steps: steps.reel() }));
}

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
    await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((im) => im.decode().catch(() => {}))); await new Promise((r) => setTimeout(r, 200)); });
    const name = p.kind === "single" ? "Post.png" : `Slide-${String(i + 1).padStart(2, "0")}.png`;
    await (await page.$("#stage > .f")).screenshot({ path: path.join(dir, name) });
    files.push(name);
  }
  fs.writeFileSync(path.join(dir, "UPLOAD.md"), md({ title: `Post ${p.id}: ${p.theme}`, ...p,
    format: p.kind === "single" ? "Single image, 4:5 (1080 × 1350)" : `Carousel, ${p.slides.length} slides, 4:5 (1080 × 1350)`,
    files, steps: p.kind === "single" ? steps.single() : steps.carousel(p.slides.length),
    alt: p.alt.length > 1 ? p.alt.map((a, i) => `- Image ${i + 1}: ${a}`).join("\n") : p.alt[0] }));
  console.log(p.id, files.length, "files");
}
await browser.close();
