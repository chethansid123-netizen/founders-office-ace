// Export every post into its own folder: PNG slides (1080x1350), or MP4 reel (1080x1920, 30 fps) + cover,
// plus UPLOAD.md with the caption, hashtags, alt text and posting steps.
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
require(path.join(here, "v3.js"));
const POSTS = globalThis.YD3.POSTS;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(here, "studio.html")).href);
async function shot(file, id, i, t, type = "png") {
  await page.evaluate(([id, i, t]) => window.show(id, i, t), [id, i, t]);
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((im) => im.decode().catch(() => {}))); });
  const o = { path: file, type }; if (type === "jpeg") o.quality = qa ? 70 : 92;
  await (await page.$("#stage > .yds")).screenshot(o);
}

for (const p of POSTS) {
  if (only && !only.includes(p.id)) continue;
  const dir = path.join(outDir, `${p.id}-${p.slug}`);
  fs.mkdirSync(dir, { recursive: true });
  if (p.kind === "reel") {
    if (qa) { for (const t of [p.reel.cover, ...p.reel.scenes.slice(1).map((s) => s.a + 1.6)]) await shot(path.join(outDir, `${p.id}-t${t.toFixed(1)}.jpg`), p.id, 0, t, "jpeg"); continue; }
    await shot(path.join(dir, "Cover.png"), p.id, 0, p.reel.cover);
    const tmp = fs.mkdtempSync(path.join(outDir, ".frames-"));
    const total = Math.round(p.reel.dur * 30);
    for (let f = 0; f < total; f++) await shot(path.join(tmp, `${String(f).padStart(4, "0")}.jpg`), p.id, 0, f / 30, "jpeg");
    execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", "30", "-i", path.join(tmp, "%04d.jpg"), "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", path.join(dir, "Reel.mp4")]);
    fs.rmSync(tmp, { recursive: true, force: true });
  } else {
    for (let i = 0; i < p.slides.length; i++) {
      const name = p.kind === "single" ? "Post" : `Slide-${String(i + 1).padStart(2, "0")}`;
      await shot(qa ? path.join(outDir, `${p.id}-${i + 1}.jpg`) : path.join(dir, `${name}.png`), p.id, i, null, qa ? "jpeg" : "png");
    }
  }
  if (qa) continue;
  const files = p.kind === "reel" ? ["Reel.mp4 (the video)", "Cover.png (the cover image)"] : p.kind === "single" ? ["Post.png"] : p.slides.map((_, i) => `Slide-${String(i + 1).padStart(2, "0")}.png`);
  const steps = p.kind === "reel"
    ? [`Tap + → Reel → select Reel.mp4.`, `Add audio: ${p.audio}`, `Tap Next → Edit cover → Add from camera roll → choose Cover.png. Check the grid preview shows the headline.`, `Keep "Share to Feed" on.`, `Paste the caption and hashtags below. Add the alt text under Advanced settings → Accessibility.`]
    : [`Tap + → Post → select ${p.kind === "single" ? "Post.png" : `all ${p.slides.length} slides in order (Slide-01 first)`}.`, `Set the crop to 4:5 (portrait) so nothing is cut off.`, `Paste the caption and hashtags below.`, `Advanced settings → Accessibility → write alt text: paste the alt text for each image below.`];
  const md = `# Post ${p.id}: ${p.slug.replace(/-/g, " ")}

**Format:** ${p.kind === "reel" ? "Reel (9:16, 1080 × 1920, " + p.reel.dur + " s)" : p.kind === "single" ? "Single image (4:5, 1080 × 1350)" : `Carousel, ${p.slides.length} slides (4:5, 1080 × 1350)`}
**For:** ${p.segment}
**Post on:** ${p.date}, ${p.time}
**Hook:** ${p.hook}

## Files, in upload order
${files.map((f, i) => `${i + 1}. ${f}`).join("\n")}

## How to upload
${steps.map((s, i) => `${i + 1}. ${s}`).join("\n")}
${steps.length + 1}. Post the first comment below from the YourDOST account, then pin it.
${steps.length + 2}. Share the post to Stories with a poll or question sticker, and reply to comments in the first hour.
${steps.length + 3}. If a comment suggests someone is in crisis, reply kindly with Tele MANAS 14416 (free, 24/7), send a DM, and flag it to the clinical team.

## Caption
${p.caption}

${p.tags}

## First comment (pin it)
${p.first}

## Alt text
${p.alt.map((a, i) => (p.alt.length > 1 ? `- Image ${i + 1}: ${a}` : a)).join("\n")}
`;
  fs.writeFileSync(path.join(dir, "UPLOAD.md"), md);
  console.log(`${p.id} ${p.kind} done`);
}
await browser.close();
