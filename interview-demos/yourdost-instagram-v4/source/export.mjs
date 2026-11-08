// Export v4: one folder per post. Reels -> MP4 (1080x1920, 30 fps, original music), Cover.png. Feed -> PNGs. Plus UPLOAD.md.
//   node export.mjs [outDir] [--only=01,02] [--qa]
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const args = process.argv.slice(2);
const outDir = path.resolve(args.find((a) => !a.startsWith("--")) || path.join(here, ".."));
const only = (args.find((a) => a.startsWith("--only=")) || "").split("=")[1]?.split(",");
const qa = args.includes("--qa");
const people = args.includes("--people");
const SWAP = { "diwali-street": "p-diwali-woman", "man-walking": "p-man-terrace", "chai-hands": "p-chai-friends", "notebook": "p-student-night", "keyboard-dark": "p-laptop-woman", "two-chai": "p-couple" };
require(path.join(here, "v4.js"));
const POSTS = globalThis.YD4.POSTS;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(here, "studio.html")).href);
if (people) await page.evaluate((s) => { window.YD4_SWAP = s; }, SWAP);
async function shot(file, id, i, t, type = "png") {
  await page.evaluate(([id, i, t]) => window.show(id, i, t), [id, i, t]);
  await page.evaluate(async () => {
    await document.fonts.ready;
    const urls = [...document.querySelectorAll("[style*='background-image']")].map((e) => getComputedStyle(e).backgroundImage.slice(5, -2));
    await Promise.all([...urls.map((u) => new Promise((r) => { const im = new Image(); im.onload = im.onerror = r; im.src = u; })), ...[...document.images].map((im) => im.decode().catch(() => {}))]);
  });
  const o = { path: file, type }; if (type === "jpeg") o.quality = qa ? 70 : 92;
  await (await page.$("#stage > .f")).screenshot(o);
}
for (const p of POSTS) {
  if (only && !only.includes(p.id)) continue;
  const dir = path.join(outDir, `${p.id}-${p.slug}`);
  if (!qa) fs.mkdirSync(dir, { recursive: true });
  if (p.kind === "reel") {
    if (qa) { for (const s of p.reel.scenes) await shot(path.join(outDir, `${p.id}-t${(s.a + 1.8).toFixed(1)}.jpg`), p.id, 0, s.a + 1.8, "jpeg"); continue; }
    await shot(path.join(dir, "Cover.png"), p.id, 0, p.reel.cover);
    const tmp = fs.mkdtempSync(path.join(outDir, ".frames-"));
    const total = Math.round(p.reel.dur * 30);
    for (let f = 0; f < total; f++) await shot(path.join(tmp, `${String(f).padStart(4, "0")}.jpg`), p.id, 0, f / 30, "jpeg");
    const music = path.join(here, "music", `${p.reel.audio}.wav`);
    execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", "30", "-i", path.join(tmp, "%04d.jpg"), "-i", music, "-map", "0:v", "-map", "1:a", "-shortest",
      "-af", `afade=t=out:st=${(p.reel.dur - 1.6).toFixed(2)}:d=1.5`, "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", path.join(dir, "Reel.mp4")]);
    fs.rmSync(tmp, { recursive: true, force: true });
  } else {
    for (let i = 0; i < p.slides.length; i++) {
      const name = p.kind === "single" ? "Post" : `Slide-${String(i + 1).padStart(2, "0")}`;
      await shot(qa ? path.join(outDir, `${p.id}-${i + 1}.jpg`) : path.join(dir, `${name}.png`), p.id, i, null, qa ? "jpeg" : "png");
    }
  }
  if (qa) continue;
  const files = p.kind === "reel" ? ["Reel.mp4 (video with music)", "Cover.png (cover image)"] : p.kind === "single" ? ["Post.png"] : p.slides.map((_, i) => `Slide-${String(i + 1).padStart(2, "0")}.png`);
  const steps = p.kind === "reel"
    ? ["Tap + → Reel → select Reel.mp4. The music is already in the video.", "Tap Next → Edit cover → Add from camera roll → choose Cover.png.", "Keep “Share to Feed” on.", "Paste the caption and hashtags below. Add the alt text under Advanced settings → Accessibility."]
    : [`Tap + → Post → select ${p.kind === "single" ? "Post.png" : `all ${p.slides.length} slides in order (Slide-01 first)`}.`, "Set the crop to 4:5 (portrait) so nothing is cut off.", "Paste the caption and hashtags below.", "Advanced settings → Accessibility → paste the alt text below."];
  fs.writeFileSync(path.join(dir, "UPLOAD.md"), `# Post ${p.id}: ${p.theme}

**The line:** ${p.line}
**Why:** ${p.why}
**Format:** ${p.kind === "reel" ? `Reel, 9:16, ${p.reel.dur} s, with original music` : p.kind === "single" ? "Single image, 4:5" : `Carousel, ${p.slides.length} slides, 4:5`}
**For:** ${p.segment}
**Post on:** ${p.date}, ${p.time}

## Files, in upload order
${files.map((f, i) => `${i + 1}. ${f}`).join("\n")}

## How to upload
${steps.map((s, i) => `${i + 1}. ${s}`).join("\n")}
${steps.length + 1}. Post the first comment below from the YourDOST account and pin it.
${steps.length + 2}. Reply to comments in the first hour. If a comment suggests someone is in crisis, reply kindly with Tele MANAS 14416 (free, 24/7), send a DM, and flag it to the clinical team.

## Caption
${p.caption}

${p.tags}

## First comment (pin it)
${p.first}

## Alt text
${p.alt.map((a, i) => (p.alt.length > 1 ? `- Image ${i + 1}: ${a}` : a)).join("\n")}
`);
  console.log(p.id, "done");
}
await browser.close();
