// Build the motion versions of the three v7 originals (Motion.mp4 in each folder).
//   node motion.mjs [outDir] [--only=24] [--qa]
import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const args = process.argv.slice(2);
const outDir = path.resolve(args.find((a) => !a.startsWith("--")) || path.join(here, ".."));
const only = (args.find((a) => a.startsWith("--only=")) || "").slice(7).split(",").filter(Boolean);
const QA = args.includes("--qa");
const REMUX = args.includes("--remux"); // reuse rendered frames and base video, redo only the audio mix and final encode
const FPS = 30;
require(path.join(here, "motion.js"));
const { MOTION } = globalThis.YD7M;
const ff = (a) => execFileSync("ffmpeg", ["-v", "error", "-y", ...a], { stdio: "inherit" });
const SLUG = { "24": "24-Original-Inner-Captions", "25": "25-Original-The-Gallery-Label", "26": "26-Original-Everest-Rest-Days" };
const A = (f) => path.join(here, "audio", f), V = (f) => path.join(here, "ai", f);

const CALL = "highpass=f=180,lowpass=f=6800";
const L = "pan=stereo|c0=1.0*c0|c1=0.55*c1", R = "pan=stereo|c0=0.55*c0|c1=1.0*c1";
const MIX = {
  "24": [
    { f: A("sfx-join.mp3"), at: 0, v: 0.55 },
    { f: A("m24-music.mp3"), at: 0.1, pre: "atempo=0.8", v: [[0, 0.26], [3.9, 0.26], [4.0, 0.2], [13.0, 0.2], [13.3, 0.34], [19.2, 0.3], [19.4, 0.2], [23.0, 0.2], [23.8, 0]] },
    { f: A("vo-arjun.mp3"), at: 0.2, from: 0, to: 3.58, fx: CALL, v: 1 },
    { f: A("vo-neha.mp3"), at: 3.95, from: 0, to: 0.85, fx: CALL, v: 1 },
    { f: A("vo-rahul.mp3"), at: 4.95, from: 0, to: 1.74, fx: CALL, v: 1 },
    { f: A("vo-fatima.mp3"), at: 6.85, from: 0, to: 1.0, fx: CALL, v: 1 },
    { f: A("vo-vikram.mp3"), at: 8.0, from: 0, to: 2.18, fx: CALL, v: 1 },
    { f: A("vo-sneha.mp3"), at: 10.25, from: 0, to: 2.75, fx: CALL, v: 1 },
    { f: A("sfx-toggle.mp3"), at: 13.2, v: 0.6 },
    { f: A("vo-arjun.mp3"), at: 13.45, from: 4.66, to: 6.92, fx: L, v: 1.15 },
    { f: A("vo-neha.mp3"), at: 14.05, from: 1.75, to: 4.55, fx: R, v: 1.15 },
    { f: A("vo-rahul.mp3"), at: 14.65, from: 2.54, to: 4.9, fx: L, v: 1.15 },
    { f: A("vo-fatima.mp3"), at: 15.25, from: 2.2, to: 3.7, fx: R, v: 1.15 },
    { f: A("vo-vikram.mp3"), at: 15.85, from: 3.2, to: 6.03, fx: L, v: 1.15 },
    { f: A("vo-sneha.mp3"), at: 16.45, from: 4.25, to: 7.62, fx: R, v: [[0, 1.15], [19.3, 1.15], [19.6, 0.5]] },
    { f: A("vo-m24-narrator.mp3"), at: 19.45, from: 0.05, to: 1.35, v: 3.0 },
    { f: A("vo-m24-narrator.mp3"), at: 20.95, from: 3.95, to: 5.1, v: 3.0 },
    { f: A("sfx-pop.mp3"), at: 22.4, v: 0.4 },
    { f: A("vo-m24-narrator.mp3"), at: 22.6, from: 6.35, to: 8.25, v: 3.0 },
    { f: A("vo-m24-narrator.mp3"), at: 24.6, from: 9.15, to: 11.4, v: 3.0 },
    { f: A("m24-music.mp3"), at: 22.2, from: 11.0, to: 15.0, fi: 0.6, fo: 1.2, v: 0.32 },
  ],
  "25": [
    { f: A("sfx-guide-beep.mp3"), at: 0.15, v: 0.6 },
    { f: A("sfx-gallery.mp3"), at: 0, loop: 2, v: [[0, 0.38], [22.2, 0.3], [22.8, 0.12]] },
    { f: A("m25-music.mp3"), at: 0.8, v: [[0, 0.3], [1.2, 0.22], [22.2, 0.22], [22.6, 0.36], [24.8, 0.32], [25.4, 0]] },
    ...[[0, 0.95, 1.3], [1.68, 2.42, 2.7], [4.95, 5.5, 4.24], [6.45, 7.35, 5.39], [8.35, 9.7, 7.09], [10.35, 13.98, 8.84], [14.95, 15.85, 13.02], [17.05, 19.8, 14.82], [20.85, 22.18, 18.37], [23.05, 24.69, 20.25]]
      .map(([a, b, at]) => ({ f: A("vo-m25-guide.mp3"), at, from: a, to: b, v: 1.5 })),
    { f: A("sfx-pop.mp3"), at: 22.5, v: 0.35 },
    { f: A("m25-music.mp3"), at: 22.2, from: 8.0, to: 11.3, fi: 0.5, fo: 1.0, v: 0.5 },
  ],
  "26": [
    { f: A("sfx-wind.mp3"), at: 0, loop: 1, v: [[0, 0.5], [13.8, 0.45], [14.4, 0.22], [17.5, 0.15]] },
    { f: A("m26-music.mp3"), at: 0, v: [[0, 0.32], [0.9, 0.24], [13.8, 0.24], [14.3, 0.4], [16.8, 0.35], [17.4, 0]] },
    ...[[0, 2.5, 1.0], [3.52, 4.48, 4.1], [5.24, 6.2, 5.5], [6.78, 7.46, 6.9], [8.84, 9.94, 8.3], [11.22, 12.62, 10.2], [13.1, 14.76, 11.95]]
      .map(([a, b, at]) => ({ f: A("vo-m26-narrator.mp3"), at, from: a, to: b, v: 1.1 })),
    { f: A("sfx-pop.mp3"), at: 14.3, v: 0.35 },
    { f: A("m26-music.mp3"), at: 14.0, from: 0, to: 3.5, fi: 0.3, fo: 1.0, v: 0.6 },
  ],
};

const envExpr = (pts) => { let e = String(pts[pts.length - 1][1]);
  for (let i = pts.length - 2; i >= 0; i--) { const [t0, v0] = pts[i], [t1, v1] = pts[i + 1]; e = `if(lt(t,${t1}),${v0}+(${v1 - v0})*(t-${t0})/${Math.max(t1 - t0, 0.001)},${e})`; }
  return `if(lt(t,${pts[0][0]}),${pts[0][1]},${e})`; };

function mix(id, dur, out) {
  const items = MIX[id];
  const inputs = items.flatMap((it) => [...(it.loop ? ["-stream_loop", String(it.loop)] : []), "-i", it.f]);
  const chains = items.map((it, i) => {
    let c = `[${i}:a]aresample=48000,aformat=channel_layouts=stereo`;
    if (it.pre) c += `,${it.pre}`;
    if (it.from != null) { const fi = it.fi || 0.02, fo = it.fo || 0.06; c += `,atrim=${it.from}:${it.to},asetpts=PTS-STARTPTS,afade=t=in:d=${fi},afade=t=out:st=${Math.max(0, it.to - it.from - fo)}:d=${fo}`; }
    if (it.fx) c += `,${it.fx}`;
    c += `,adelay=${Math.round(it.at * 1000)}:all=1`;
    c += Array.isArray(it.v) ? `,volume=eval=frame:volume='${envExpr(it.v)}'` : `,volume=${it.v}`;
    return `${c}[a${i}]`;
  });
  const fc = `${chains.join(";")};${items.map((_, i) => `[a${i}]`).join("")}amix=inputs=${items.length}:normalize=0:dropout_transition=0,atrim=0:${dur},alimiter=limit=0.9:level=false,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,afade=t=out:st=${dur - 0.4}:d=0.4[m]`;
  ff([...inputs, "-filter_complex", fc, "-map", "[m]", "-c:a", "pcm_s16le", out]);
}

const CROP = { "m24-rahul": "crop=1050:591:115:64", "m24-sneha": "crop=1200:676:40:22" };
function base24(dur, bg, out) {
  const cells = MOTION["24"].cells.filter((c) => c.vid);
  const inputs = ["-loop", "1", "-framerate", String(FPS), "-t", String(dur), "-i", bg, ...cells.flatMap((c) => ["-i", V(`${c.vid}.mp4`)])];
  const parts = cells.map((c, i) => {
    const pre = CROP[c.vid] ? `${CROP[c.vid]},` : "";
    return `[${i + 1}:v]${pre}scale=${c.w}:${c.h}:flags=lanczos,fps=${FPS},setsar=1,split[f${i}][r${i}];[r${i}]reverse[b${i}];[f${i}][b${i}]concat=n=2:v=1:a=0,loop=loop=4:size=${8 * FPS}:start=0,trim=0:${dur},setpts=PTS-STARTPTS[t${i}]`;
  });
  let chain = "[0:v]format=yuv420p[bg0]";
  cells.forEach((c, i) => { chain += `;[bg${i}][t${i}]overlay=${c.x}:${c.y}:shortest=0[bg${i + 1}]`; });
  ff([...inputs, "-filter_complex", `${parts.join(";")};${chain}`, "-map", `[bg${cells.length}]`, "-t", String(dur), "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", out]);
}
function base26(dur, out) {
  ff(["-i", V("m26-basecamp.mp4"), "-filter_complex",
    `[0:v]scale=1080:1920:flags=lanczos,unsharp=5:5:0.4:5:5:0,fps=${FPS},setsar=1,split[f][r];[r]reverse[b];[f][b]concat=n=2:v=1:a=0,trim=0:${dur},setpts=PTS-STARTPTS[v]`,
    "-map", "[v]", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", out]);
}

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(here, "motion.html")).href);
await page.evaluate(async () => { for (const w of ["500 40px Poppins", "600 60px Poppins", "500 24px Inter", "600 24px Inter", "700 50px Gaegu"]) await document.fonts.load(w); await document.fonts.ready; });
const settle = () => page.evaluate(async () => { await Promise.all([...document.images].map((im) => (im.complete ? 0 : im.decode().catch(() => {})))); });

for (const [id, M] of Object.entries(MOTION)) {
  if (only.length && !only.includes(id)) continue;
  const work = path.join(here, `.frames-m${id}`);
  const reuse = REMUX && fs.existsSync(path.join(work, "0000.png"));
  if (!reuse) { fs.rmSync(work, { recursive: true, force: true }); fs.mkdirSync(work, { recursive: true }); }
  let base = null;
  if (reuse) { if (id !== "25") base = path.join(work, "base.mp4"); }
  else if (id === "24") {
    const bg = path.join(work, "bg.png");
    await page.evaluate(() => { document.getElementById("root").innerHTML = `<div style="position:absolute;inset:0;background:#fdfcf7"></div><div style="position:absolute;left:30px;width:1020px;top:300px;height:1294px;border-radius:30px;background:#17171c;box-shadow:0 30px 70px rgba(0,0,0,0.3)"></div>`; });
    await page.screenshot({ path: bg });
    base = path.join(work, "base.mp4"); base24(M.dur, bg, base);
  } else if (id === "26") { base = path.join(work, "base.mp4"); base26(M.dur, base); }

  const N = Math.round(M.dur * FPS);
  const frames = QA ? [0.5, 3, 5.5, 9, 12.5, 13.6, 15, 17, 20, 21.5, 23, 26].map((t) => Math.min(N - 1, Math.round(t * FPS))) : [...Array(N).keys()];
  let last = null, lastFile = null;
  for (const n of (reuse ? [] : frames)) {
    const t = n / FPS, html = M.render(t), file = path.join(work, `${String(n).padStart(4, "0")}.png`);
    if (!QA && html === last) { fs.copyFileSync(lastFile, file); continue; }
    await page.evaluate(([id, t]) => window.YD7M.render(id, t), [id, t]); await settle();
    await page.screenshot({ path: file, omitBackground: M.transparent });
    last = html; lastFile = file;
  }
  if (QA) {
    const S = path.join(work, "qa"); fs.mkdirSync(S, { recursive: true });
    for (const n of frames) {
      const png = path.join(work, `${String(n).padStart(4, "0")}.png`), jpg = path.join(S, `${String(n).padStart(4, "0")}.jpg`);
      if (base) ff(["-ss", String(n / FPS), "-i", base, "-i", png, "-filter_complex", "[0:v][1:v]overlay=0:0,scale=300:-1", "-frames:v", "1", jpg]);
      else ff(["-i", png, "-vf", "scale=300:-1", jpg]);
    }
    ff(["-pattern_type", "glob", "-i", path.join(S, "*.jpg"), "-filter_complex", "tile=6x2:padding=6:color=white", "-frames:v", "1", path.join(here, `.qa-m${id}.jpg`)]);
    console.log("qa", id); continue;
  }
  const wav = path.join(work, "mix.wav"); mix(id, M.dur, wav);
  const dir = path.join(outDir, SLUG[id]); fs.mkdirSync(dir, { recursive: true });
  const vin = base ? ["-i", base, "-framerate", String(FPS), "-i", path.join(work, "%04d.png")] : ["-framerate", String(FPS), "-i", path.join(work, "%04d.png")];
  const vf = base ? "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]" : "[0:v]format=yuv420p[v]";
  const ai = base ? 2 : 1;
  ff([...vin, "-i", wav, "-filter_complex", vf, "-map", "[v]", "-map", `${ai}:a`, "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-r", String(FPS),
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", String(M.dur), path.join(dir, "Motion.mp4")]);
  ff(["-ss", "1.0", "-i", path.join(dir, "Motion.mp4"), "-frames:v", "1", "-q:v", "2", path.join(dir, "Motion-cover.jpg")]);
  console.log("motion", id, "->", path.relative(outDir, path.join(dir, "Motion.mp4")));
}
await browser.close();
