// Compose the three v6 reels: ElevenLabs footage (Veo 3.1 Lite, 720p) upscaled to 1080x1920, brand overlays
// rendered frame by frame with Playwright, and an audio mix of ElevenLabs music, SFX and voiceover.
//   node render.mjs [outDir] [--only=13,14] [--qa]      (--qa writes key-frame previews only)
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
const FPS = 30;
require(path.join(here, "reels.js"));
const REELS = globalThis.YD6R.REELS;
const ff = (a) => execFileSync("ffmpeg", ["-v", "error", "-y", ...a], { stdio: "inherit" });

// footage plan: [file, trimFrom, trimTo] in order; startHold = seconds to freeze the first frame (under the R14 lock screen)
const FOOT = {
  "13": { clips: [["ai/r13-A.mp4", 0, 8], ["ai/r13-B.mp4", 0, 5.8]], startHold: 0 },
  "14": { clips: [["ai/r14-A.mp4", 0, 8], ["ai/r14-B.mp4", 0, 4]], startHold: 1.4 },
  "15": { clips: [["ai/r15-A.mp4", 0, 8], ["ai/r15-B.mp4", 0, 5.8]], startHold: 0 },
};

// audio plan: { f: file, at: start in reel, from/to: trim of the source, v: volume or [[t, v], ...] envelope in reel time }
const A = (f) => path.join(here, "audio", f);
const MIX = {
  "13": [
    { f: path.join(here, "ai/r13-A.mp4"), at: 0, from: 0, to: 8, v: 1.0, fo: 0.3 },
    { f: A("r13-music.mp3"), at: 0, v: [[0, 0.16], [7.7, 0.16], [8.4, 0.42], [8.7, 0.3], [11.9, 0.3], [12.4, 0.48], [14.1, 0.34], [16.4, 0.34], [17, 0]] },
    { f: A("sfx-hostel.mp3"), at: 8.0, from: 0, to: 5.8, v: 0.3, fi: 0.4, fo: 0.6 },
    { f: A("r13-vo.mp3"), at: 8.7, from: 0, to: 3.15, v: 1.05 },
    { f: A("r13-vo.mp3"), at: 14.2, from: 4.25, to: 6.43, v: 1.05 },
    { f: A("sfx-pop.mp3"), at: 14.65, v: 0.5 }, { f: A("sfx-pop.mp3"), at: 15.4, v: 0.5 },
  ],
  "14": [
    { f: A("sfx-alert.mp3"), at: 0.05, v: 0.75 },
    { f: A("r14-music.mp3"), at: 0, v: [[0, 0.3], [1.9, 0.3], [2.0, 0.2], [5.1, 0.2], [5.3, 0.34], [7.5, 0.34], [7.7, 0.2], [11.5, 0.2], [12, 0.36], [13.5, 0.36], [13.7, 0.22], [16.4, 0.22], [17, 0]] },
    { f: A("sfx-office.mp3"), at: 1.4, from: 0, to: 8.0, v: 0.32, fi: 0.4, fo: 0.4 },
    { f: A("r14-vo.mp3"), at: 1.95, from: 0.1, to: 3.38, v: 1.0 },
    { f: A("sfx-ping.mp3"), at: 5.3, v: 0.6 }, { f: A("sfx-ping.mp3"), at: 6.05, v: 0.6 }, { f: A("sfx-ping.mp3"), at: 6.8, v: 0.6 },
    { f: A("r14-vo.mp3"), at: 7.6, from: 3.42, to: 5.42, v: 1.0 },
    { f: A("sfx-laptop.mp3"), at: 9.45, v: 0.7 },
    { f: A("r14-vo.mp3"), at: 9.75, from: 5.48, to: 7.22, v: 1.0 },
    { f: A("r14-vo.mp3"), at: 13.6, from: 7.28, to: 10.68, v: 1.0 },
    { f: A("sfx-pop.mp3"), at: 14.25, v: 0.5 }, { f: A("sfx-pop.mp3"), at: 15.0, v: 0.5 },
  ],
  "15": [
    { f: A("sfx-3am.mp3"), at: 0, from: 0, to: 8.0, v: 0.55, fo: 0.4 },
    { f: A("r15-music.mp3"), at: 0, v: [[0, 0.3], [10.9, 0.3], [11.1, 0.2], [12.7, 0.2], [13.0, 0.34], [14.0, 0.34], [14.2, 0.22], [16.1, 0.22], [16.4, 0.3], [17, 0]] },
    { f: A("sfx-morning.mp3"), at: 8.0, from: 0, to: 5.8, v: 0.4, fi: 0.3, fo: 0.5 },
    { f: A("sfx-pop.mp3"), at: 8.45, v: 0.5 }, { f: A("sfx-pop.mp3"), at: 9.15, v: 0.5 }, { f: A("sfx-pop.mp3"), at: 9.85, v: 0.5 },
    { f: A("r15-vo.mp3"), at: 11.15, from: 0, to: 1.5, v: 1.1 },
    { f: A("r15-vo.mp3"), at: 14.1, from: 2.12, to: 4.05, v: 1.1 },
    { f: A("sfx-pop.mp3"), at: 14.65, v: 0.5 }, { f: A("sfx-pop.mp3"), at: 15.4, v: 0.5 },
  ],
};

const envExpr = (pts) => {
  let e = String(pts[pts.length - 1][1]);
  for (let i = pts.length - 2; i >= 0; i--) {
    const [t0, v0] = pts[i], [t1, v1] = pts[i + 1];
    e = `if(lt(t,${t1}),${v0}+(${v1 - v0})*(t-${t0})/${Math.max(t1 - t0, 0.001)},${e})`;
  }
  return `if(lt(t,${pts[0][0]}),${pts[0][1]},${e})`;
};

function baseVideo(id, dur, out) {
  const { clips, startHold } = FOOT[id];
  const inputs = clips.flatMap(([f]) => ["-i", path.join(here, f)]);
  const parts = clips.map(([, a, b], i) => `[${i}:v]trim=${a}:${b},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,unsharp=5:5:0.45:5:5:0,fps=${FPS},setsar=1${i === 0 && startHold ? `,tpad=start_mode=clone:start_duration=${startHold}` : ""}[c${i}]`);
  const fc = `${parts.join(";")};${clips.map((_, i) => `[c${i}]`).join("")}concat=n=${clips.length}:v=1:a=0,tpad=stop_mode=clone:stop_duration=6,trim=0:${dur},setpts=PTS-STARTPTS[v]`;
  ff([...inputs, "-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", out]);
}

function mixAudio(id, dur, out) {
  const items = MIX[id];
  const inputs = items.flatMap((it) => ["-i", it.f]);
  const chains = items.map((it, i) => {
    const len = (it.to ?? 999) - (it.from ?? 0);
    let c = `[${i}:a]aresample=48000,aformat=channel_layouts=stereo`;
    if (it.from != null || it.to != null) c += `,atrim=${it.from ?? 0}:${it.to ?? 999},asetpts=PTS-STARTPTS`;
    if (it.fi) c += `,afade=t=in:d=${it.fi}`;
    if (it.fo && it.to != null) c += `,afade=t=out:st=${Math.max(0, len - it.fo)}:d=${it.fo}`;
    c += `,adelay=${Math.round(it.at * 1000)}:all=1`;
    c += Array.isArray(it.v) ? `,volume=eval=frame:volume='${envExpr(it.v)}'` : `,volume=${it.v}`;
    return `${c}[a${i}]`;
  });
  const fc = `${chains.join(";")};${items.map((_, i) => `[a${i}]`).join("")}amix=inputs=${items.length}:normalize=0:dropout_transition=0,atrim=0:${dur},alimiter=limit=0.9:level=false,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,afade=t=out:st=${dur - 0.35}:d=0.35[m]`;
  ff([...inputs, "-filter_complex", fc, "-map", "[m]", "-c:a", "pcm_s16le", out]);
}

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(here, "reel.html")).href);
await page.evaluate(async () => { await document.fonts.load("600 80px Poppins"); await document.fonts.load("500 40px Poppins"); await document.fonts.ready; });

for (const [id, R] of Object.entries(REELS)) {
  if (only.length && !only.includes(id)) continue;
  const work = path.join(here, `.frames-${id}`);
  fs.rmSync(work, { recursive: true, force: true });
  fs.mkdirSync(work, { recursive: true });
  const base = path.join(work, "base.mp4");
  baseVideo(id, R.dur, base);
  const N = Math.round(R.dur * FPS);
  const times = QA ? [0, 1.0, 1.7, 2.6, 4.5, 6.4, 7.0, 8.0, 9.2, 10.0, 11.5, 12.5, 14.2, 15.0, 16.5] : null;
  const frames = times ? times.map((t) => Math.min(N - 1, Math.round(t * FPS))) : [...Array(N).keys()];
  let last = null, lastFile = null;
  for (const n of frames) {
    const t = n / FPS;
    const html = R.render(t);
    const file = path.join(work, `${String(n).padStart(4, "0")}.png`);
    if (html === last && !QA) { fs.copyFileSync(lastFile, file); continue; }
    await page.evaluate(([id, t]) => window.YD6R.render(id, t), [id, t]);
    await page.evaluate(async () => { await Promise.all([...document.images].map((im) => (im.complete ? 0 : im.decode().catch(() => {})))); });
    await page.screenshot({ path: file, omitBackground: true });
    last = html; lastFile = file;
  }
  if (QA) {
    const S = path.join(work, "qa");
    fs.mkdirSync(S, { recursive: true });
    for (const n of frames) {
      const t = n / FPS, png = path.join(work, `${String(n).padStart(4, "0")}.png`);
      ff(["-ss", String(t), "-i", base, "-i", png, "-filter_complex", "[0:v][1:v]overlay=0:0,scale=360:-1", "-frames:v", "1", path.join(S, `${String(n).padStart(4, "0")}.jpg`)]);
    }
    ff(["-pattern_type", "glob", "-i", path.join(S, "*.jpg"), "-filter_complex", "tile=8x2:padding=6:color=white", "-frames:v", "1", path.join(here, `.qa-${id}.jpg`)]);
    console.log("qa", id);
    continue;
  }
  const wav = path.join(work, "mix.wav");
  mixAudio(id, R.dur, wav);
  const dir = path.join(outDir, R.slug);
  fs.mkdirSync(dir, { recursive: true });
  ff(["-i", base, "-framerate", String(FPS), "-i", path.join(work, "%04d.png"), "-i", wav,
    "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]", "-map", "[v]", "-map", "2:a",
    "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-r", String(FPS),
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", String(R.dur), path.join(dir, "Reel.mp4")]);
  // cover: the hook frame
  ff(["-ss", "0.6", "-i", path.join(dir, "Reel.mp4"), "-frames:v", "1", "-q:v", "2", path.join(dir, "Cover.jpg")]);
  console.log("reel", id, "->", path.relative(outDir, path.join(dir, "Reel.mp4")));
}
await browser.close();
