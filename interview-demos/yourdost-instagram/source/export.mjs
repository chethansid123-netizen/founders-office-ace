// Render every #JoBolaNahi creative to post-ready files.
//   node export.mjs <outDir> [--only=01,04] [--fps=30] [--no-video] [--qa]
// Statics, carousel slides and story frames -> PNG at native size.
// Reels -> one PNG per frame, then ffmpeg -> H.264 MP4 (1080x1920, 30 fps), plus a cover PNG.
// --qa renders scaled-down JPEGs of every slide and a few frames per reel, for a quick visual check.
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
// CommonJS require honours NODE_PATH, so a globally installed Playwright resolves from any folder.
const { chromium } = createRequire(import.meta.url)("playwright");
const args = process.argv.slice(2);
const outDir = path.resolve(args.find((a) => !a.startsWith("--")) || path.join(here, "..", "exports"));
const flag = (n) => args.find((a) => a.startsWith(`--${n}`));
const only = flag("only") ? flag("only").split("=")[1].split(",") : null;
const fps = flag("fps") ? Number(flag("fps").split("=")[1]) : 30;
const noVideo = !!flag("no-video");
const qa = !!flag("qa");
fs.mkdirSync(outDir, { recursive: true });
if (!qa) fs.mkdirSync(path.join(outDir, "story-mockups"), { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(here, "studio.html")).href);
await page.evaluate(() => document.fonts.ready);

const posts = await page.evaluate(() =>
  JBN.POSTS.map((p) => ({ id: p.id, slug: p.slug, kind: p.kind, tall: !!p.tall, n: JBN.frameCount(p), dur: p.reel ? p.reel.dur : 0, cover: p.reel ? p.reel.cover : 0 }))
);

async function shot(file, id, i, t, bare, type = "png") {
  await page.evaluate(([id, i, t, bare]) => window.show(id, i, t, bare), [id, i, t, bare]);
  await page.evaluate(() => document.fonts.ready);
  const el = await page.$("#stage > .cv");
  const opts = { path: file, type };
  if (type === "jpeg") opts.quality = qa ? 70 : 94;
  await el.screenshot(opts);
}

for (const p of posts) {
  if (only && !only.includes(p.id)) continue;
  const base = `${p.id}-${p.slug}`;
  if (p.kind === "reel") {
    if (qa) {
      for (const t of [p.cover, 5.5, 9.4, 11.6, 13.6, p.dur - 0.4]) await shot(path.join(outDir, `${base}-t${t.toFixed(1)}.jpg`), p.id, 0, t, false, "jpeg");
      continue;
    }
    await shot(path.join(outDir, `${base}-cover.png`), p.id, 0, p.cover, false);
    if (noVideo) continue;
    const tmp = fs.mkdtempSync(path.join(outDir, `.frames-${p.id}-`));
    const total = Math.round(p.dur * fps);
    for (let f = 0; f < total; f++) {
      await shot(path.join(tmp, `${String(f).padStart(4, "0")}.jpg`), p.id, 0, f / fps, false, "jpeg");
    }
    execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(fps), "-i", path.join(tmp, "%04d.jpg"), "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart", path.join(outDir, `${base}.mp4`)]);
    fs.rmSync(tmp, { recursive: true, force: true });
    console.log(`reel ${base}: ${total} frames`);
  } else {
    for (let i = 0; i < p.n; i++) {
      const suffix = p.n > 1 ? `-${i + 1}` : "";
      const ext = qa ? "jpg" : "png";
      await shot(path.join(outDir, `${base}${suffix}.${ext}`), p.id, i, null, p.kind === "story", qa ? "jpeg" : "png");
      if (p.kind === "story" && !qa) await shot(path.join(outDir, "story-mockups", `${base}${suffix}-mockup.png`), p.id, i, null, false);
    }
    console.log(`${p.kind} ${base}: ${p.n} frame(s)`);
  }
}
await browser.close();
