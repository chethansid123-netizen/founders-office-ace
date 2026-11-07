// Build the one-PDF submission (A4 landscape) and the grid preview image from the exported creatives.
//   node build_pdf.mjs            (run export.mjs first: it writes ../exports)
import { createRequire } from "node:module";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
require(path.join(here, "creatives.js"));
const { POSTS } = globalThis.JBN;
const exportsDir = path.join(here, "..", "exports");
const outPdf = path.join(here, "..", "YourDOST-JoBolaNahi-Q2.pdf");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "jbn-pdf-"));
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const url = (p) => pathToFileURL(p).href;

const STORY_TIMES = { "01": [0.9, 2.9, 7.0, 11.9, 14.6, 17.2], "03": [1.2, 2.3, 5.4, 9.8, 13.5, 16.3], "08": [2.6, 6.8, 9.9, 13.1, 15.2, 16.6] };

const browser = await chromium.launch();
const studio = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await studio.goto(url(path.join(here, "studio.html")));
await studio.evaluate(() => document.fonts.ready);

// reel storyboards
const boards = {};
for (const [id, times] of Object.entries(STORY_TIMES)) {
  boards[id] = [];
  for (const t of times) {
    await studio.evaluate(([id, t]) => window.show(id, 0, t, false), [id, t]);
    await studio.evaluate(() => document.fonts.ready);
    const f = path.join(tmp, `${id}-${t}.jpg`);
    await (await studio.$("#stage > .cv")).screenshot({ path: f, type: "jpeg", quality: 90 });
    boards[id].push({ f, t });
  }
}

// grid preview: newest first, reels cropped to the 4:5 tile
await studio.evaluate(() => {
  const feed = JBN.POSTS.filter((p) => p.kind !== "story").slice().reverse();
  const tile = (p) => `<div style="position:relative;width:358px;height:447.5px;overflow:hidden"><div style="position:absolute;left:0;top:${p.kind === "reel" ? -94.5 : 0}px;width:1080px;transform:scale(${358 / 1080});transform-origin:0 0">${p.kind === "reel" ? JBN.frameHTML(p) : JBN.frameHTML(p, 0)}</div></div>`;
  window.showHTML(`<div id="g" style="display:grid;grid-template-columns:repeat(3,358px);gap:3px;width:1080px;background:#fff">${feed.map(tile).join("")}</div>`);
});
await studio.evaluate(() => document.fonts.ready);
const gridPng = path.join(exportsDir, "grid-preview.png");
await (await studio.$("#g")).screenshot({ path: gridPng });

// ---------- PDF document ----------
const img = (file, cls = "") => `<img class="${cls}" src="${url(file)}" alt="">`;
const ex = (name) => path.join(exportsDir, name);
function visuals(p) {
  const base = `${p.id}-${p.slug}`;
  if (p.kind === "reel") return `<div class="board">${boards[p.id].map((b) => `<figure>${img(b.f)}<figcaption>${b.t.toFixed(1)} s</figcaption></figure>`).join("")}</div>`;
  if (p.kind === "story") return `<div class="board">${p.slides.map((_, i) => `<figure>${img(ex(`story-mockups/${base}-${i + 1}-mockup.png`))}<figcaption>Frame ${i + 1}</figcaption></figure>`).join("")}</div>`;
  if (p.kind === "static") return `<div class="single">${img(ex(`${base}.png`))}</div>`;
  return `<div class="single">${img(ex(`${base}-1.png`))}</div>`;
}
function strip(p) {
  if (p.kind !== "carousel") return "";
  const base = `${p.id}-${p.slug}`;
  return `<div class="strip">${p.slides.map((_, i) => `<figure>${img(ex(`${base}-${i + 1}.png`))}<figcaption>${i + 1}/${p.slides.length}</figcaption></figure>`).join("")}</div>`;
}
const postPage = (p) => `
<section class="page post ${p.kind}">
  <header class="ph"><span class="pn">${p.id}</span><h2>${esc(p.title)}</h2><span class="chips"><span>${esc(p.theme)}</span><span>${esc(p.format)}</span><span>${esc(p.date)}, ${esc(p.time)}</span></span></header>
  <div class="body">
    <div class="vis">${visuals(p)}</div>
    <div class="txt">
      <div class="line"><p class="said">${esc(p.line)}</p><p class="unsaid">${esc(p.line2)}</p>${p.en ? `<p class="en">${esc(p.en)}</p>` : ""}</div>
      <p class="why"><b>Why:</b> ${esc(p.why)}</p>
      <dl>
        <dt>For</dt><dd>${esc(p.segment)}</dd>
        <dt>Hook</dt><dd>${esc(p.hook)}</dd>
        <dt>Engagement</dt><dd>${esc(p.mechanic)}</dd>
        <dt>Caption</dt><dd class="cap">${esc(p.caption).replace(/\n\n/g, "<br>").replace(/\n/g, " ")}</dd>
      </dl>
    </div>
  </div>
  ${strip(p)}
  <footer class="pf">#JoBolaNahi · Q2 Instagram posts · Chethan N for YourDOST</footer>
</section>`;

const insights = [
  ["Who they serve", "Blog sections: Student Life, Work & Careers, Love & Relationship, Self & Growth. B2B through colleges and companies.", "Posts for students, employees and couples, plus two for buyers: HR leaders, and founders with their incubators."],
  ["How people reach them", "Warrior stories: access through a college tie-up, a college subscription, a company benefit, a university email.", "Student and employee posts say \"check your college email\" or \"ask HR\"."],
  ["How they talk", "First-person stories, Hinglish, \"Please talk to someone. Don't carry it alone.\"", "Same warmth, but each post opens on one specific moment, which works as a hook."],
  ["What's missing", "Nothing on AI and jobs, festivals, founders or job hunting.", "Four posts fill those gaps, timed to Diwali, Men's Day and placement season."],
  ["What they aren't", "\"Not a medical service or suicide prevention helpline.\"", "Heavier posts carry Tele MANAS 14416 next to the YourDOST CTA."],
];
const rules = [
  ["Start inside one moment, not a topic.", "\"I picked up the phone to tell you\", not \"breakups are hard\"."],
  ["One true, specific detail per post.", "11:47 pm. 40 seconds. 92.4%. Application #147."],
  ["No clinical words in the hook.", "The feeling first; the brand in the last frame or the caption."],
  ["The language people think in.", "Hinglish for students, couples, families. English for founders and HR."],
  ["Ask for something small.", "One 🪔, your name, your application count, one question at a 1:1."],
  ["Never promise what the product can't.", "No \"AI won't take your job\", no \"free\" unless confirmed. YourDOST's numbers labelled as theirs."],
];

const html = `<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="${url(path.join(here, "fonts.local.css"))}">
<style>
@page { size: A4 landscape; margin: 0; }
:root { --ink:#18234a; --muted:#59628a; --accent:#1f3fa6; --mark:#f4de8e; --bg:#f3f6fb; --line:rgba(24,35,74,.14); --night:#141a2e;
  --d:"Anek Latin","Mukta",sans-serif; --b:"Mukta",sans-serif; --h:"Kalam",cursive; --m:"IBM Plex Mono",monospace; }
* { box-sizing: border-box; }
html, body { margin: 0; color: var(--ink); font-family: var(--b); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
p { margin: 0; }
.page { width: 297mm; height: 210mm; padding: 13mm 14mm 11mm; position: relative; overflow: hidden; break-after: page; background: #fff; display: flex; flex-direction: column; gap: 6mm; }
h1, h2, h3 { font-family: var(--d); font-stretch: 88%; font-weight: 760; margin: 0; line-height: 1; letter-spacing: -.01em; }
.label { font-family: var(--m); font-size: 7.5pt; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.pf { position: absolute; left: 14mm; right: 14mm; bottom: 6mm; font-family: var(--m); font-size: 6.5pt; color: var(--muted); }
/* cover */
.cover { flex-direction: row; gap: 12mm; align-items: center; background: var(--bg); }
.cover .l { flex: 1; display: flex; flex-direction: column; gap: 5mm; }
.cover h1 { font-size: 64pt; line-height: .92; }
.cover .hand { font-family: var(--h); font-weight: 700; color: var(--accent); font-size: 21pt; }
.cover .thesis { font-size: 12pt; line-height: 1.45; max-width: 128mm; }
.cover .meta { font-size: 9pt; color: var(--muted); line-height: 1.45; max-width: 128mm; }
.cover .r img { width: 118mm; display: block; box-shadow: 0 8mm 14mm -8mm rgba(0,0,0,.35); border-radius: 2mm; }
.counts { display: flex; gap: 2mm; flex-wrap: wrap; }
.counts span, .chips span { font-family: var(--m); font-size: 7pt; padding: .8mm 2.4mm; border-radius: 9mm; background: #e2eaf5; white-space: nowrap; }
/* ten lines */
.ten { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm 6mm; }
.ten div { border-top: .3mm solid var(--line); padding-top: 2.4mm; display: flex; flex-direction: column; gap: .8mm; }
.ten .n { font-family: var(--m); font-size: 7pt; color: var(--accent); }
.ten .said { font-family: var(--d); font-stretch: 90%; font-weight: 720; font-size: 11.5pt; line-height: 1.15; }
.ten .unsaid { font-family: var(--h); font-weight: 700; color: var(--accent); font-size: 10.5pt; line-height: 1.2; }
.ten .en { font-size: 7.6pt; color: var(--muted); line-height: 1.3; }
/* approach */
.cols { display: grid; grid-template-columns: 1.25fr 1fr; gap: 10mm; }
.ins { display: flex; flex-direction: column; }
.ins div { display: grid; grid-template-columns: 30mm 1fr 1fr; gap: 4mm; border-top: .3mm solid var(--line); padding: 2.6mm 0; font-size: 8.4pt; line-height: 1.35; }
.ins b, .rl b { font-family: var(--d); font-stretch: 90%; font-weight: 720; font-size: 9.5pt; line-height: 1.15; }
.ins .f { color: var(--muted); }
.ins .t::before { content: "→ "; color: var(--accent); font-weight: 700; }
.rl { display: flex; flex-direction: column; gap: 2.6mm; }
.rl div { display: flex; flex-direction: column; gap: .6mm; font-size: 8.4pt; line-height: 1.35; color: var(--muted); border-top: .3mm solid var(--line); padding-top: 2.4mm; }
.rl b { color: var(--ink); }
/* post pages */
.ph { display: flex; align-items: baseline; gap: 4mm; flex-wrap: wrap; }
.ph .pn { font-family: var(--m); font-size: 10pt; color: var(--accent); }
.ph h2 { font-size: 22pt; }
.ph .chips { display: flex; gap: 1.6mm; margin-left: auto; }
.body { display: flex; gap: 8mm; min-height: 0; flex: 1; }
.vis { flex: none; }
.single img { height: 150mm; display: block; border-radius: 2mm; box-shadow: 0 6mm 12mm -8mm rgba(0,0,0,.4); }
.carousel .single img { height: 96mm; }
.board { display: grid; grid-template-columns: repeat(3, 34mm); gap: 3mm; }
.board figure, .strip figure { margin: 0; display: flex; flex-direction: column; gap: 1mm; }
.board img { width: 34mm; display: block; border-radius: 1.4mm; }
figcaption { font-family: var(--m); font-size: 6.5pt; color: var(--muted); }
.strip { display: flex; gap: 3mm; }
.strip img { height: 46mm; display: block; border-radius: 1.2mm; }
.txt { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3mm; }
.line { background: var(--bg); border-radius: 2.4mm; padding: 4mm 5mm; display: flex; flex-direction: column; gap: 1.4mm; }
.line .said { font-family: var(--d); font-stretch: 90%; font-weight: 740; font-size: 15pt; line-height: 1.12; }
.line .unsaid { font-family: var(--h); font-weight: 700; color: var(--accent); font-size: 13.5pt; line-height: 1.2; }
.line .en { font-size: 8pt; color: var(--muted); }
.why { font-size: 9.6pt; line-height: 1.42; }
.why b { font-family: var(--d); font-stretch: 90%; font-weight: 720; }
dl { display: grid; grid-template-columns: 22mm 1fr; gap: 2mm 4mm; margin: 0; font-size: 8.4pt; line-height: 1.38; }
dt { font-family: var(--m); font-size: 6.8pt; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); padding-top: .6mm; }
dd { margin: 0; }
dd.cap { color: #2a3359; }
.carousel .txt dl { font-size: 7.8pt; }
/* closing */
table { width: 100%; border-collapse: collapse; font-size: 8.2pt; }
th { text-align: left; font-family: var(--m); font-size: 6.8pt; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); font-weight: 500; border-bottom: .3mm solid var(--line); padding: 1.6mm 2mm; }
td { border-bottom: .3mm solid var(--line); padding: 1.6mm 2mm; vertical-align: top; }
.src { font-size: 7.4pt; line-height: 1.4; color: var(--muted); margin: 0; padding-left: 4mm; display: flex; flex-direction: column; gap: 1mm; }
</style></head><body>

<section class="page cover">
  <div class="l">
    <span class="label">YourDOST · EIR task · Q2 Instagram posts</span>
    <div><h1>Jo Bola Nahi</h1><p class="hand">the things we don't say out loud</p></div>
    <p class="thesis">Everyone has a default answer. "Theek hoon." "Good, you?" "Haan maa, process mein hai." Each of these ten posts puts the line people say next to the line they don't, one typed and one handwritten, and ends the same way: <b>Bol do. Halka lagega.</b> (Say it. It'll feel lighter.)</p>
    <div class="counts"><span>3 reels</span><span>3 carousels</span><span>3 statics</span><span>1 story series</span><span>8–24 Nov 2026</span></div>
    <p class="meta">Prepared by Chethan N, 7 Nov 2026. A concept for the interview, not content published by YourDOST. Names and numbers inside the creatives are illustrative; every statistic is sourced on the last page. Live version with playable reels: claude.ai artifact "Jo Bola Nahi". Post-ready PNG and MP4 files accompany this PDF.</p>
  </div>
  <div class="r"><span class="label">Profile grid on 24 Nov, newest first</span><br>${img(gridPng)}</div>
</section>

<section class="page">
  <h2 style="font-size:24pt">The ten posts</h2>
  <p style="font-size:9.5pt;color:var(--muted);margin-top:-3mm">Ten short, original posts, in posting order. Each pairs the line people say with the line they don't.</p>
  <div class="ten">${POSTS.map((p) => `<div><span class="n">${p.id} · ${esc(p.date)} · ${esc(p.theme)} · ${esc(p.format.split(" ·")[0].split(" +")[0])}</span><p class="said">${esc(p.line)}</p><p class="unsaid">${esc(p.line2)}</p>${p.en ? `<p class="en">${esc(p.en)}</p>` : ""}</div>`).join("")}</div>
  <footer class="pf">#JoBolaNahi · Q2 Instagram posts · Chethan N for YourDOST</footer>
</section>

<section class="page">
  <h2 style="font-size:24pt">How I got here</h2>
  <div class="cols">
    <div><span class="label">What YourDOST's own content told me</span><div class="ins" style="margin-top:2mm">${insights.map((r) => `<div><b>${esc(r[0])}</b><span class="f">${esc(r[1])}</span><span class="t">${esc(r[2])}</span></div>`).join("")}</div></div>
    <div><span class="label">Six rules so it doesn't sound robotic</span><div class="rl" style="margin-top:2mm">${rules.map((r) => `<div><b>${esc(r[0])}</b>${esc(r[1])}</div>`).join("")}</div></div>
  </div>
  <footer class="pf">#JoBolaNahi · Q2 Instagram posts · Chethan N for YourDOST</footer>
</section>

${POSTS.map(postPage).join("")}

<section class="page">
  <h2 style="font-size:24pt">Calendar, guardrails and sources</h2>
  <table><thead><tr><th>When</th><th>Post</th><th>Format</th><th>Built for</th></tr></thead><tbody>${POSTS.map((p) => `<tr><td>${esc(p.date)} · ${esc(p.time)}</td><td>${p.id} ${esc(p.title)} (${esc(p.theme)})</td><td>${esc(p.format)}</td><td>${esc(p.measure)}</td></tr>`).join("")}</tbody></table>
  <div class="cols" style="grid-template-columns:1fr 1fr">
    <div class="rl"><span class="label">Guardrails</span>
      <div><b>Safe messaging</b>No methods, no graphic detail, no crisis words in hooks. The exam reel and Men's Day post carry Tele MANAS 14416.</div>
      <div><b>Comment protocol</b>Any comment that signals risk gets a reply within the hour with 14416 and a DM, and goes to YourDOST's clinical team.</div>
      <div><b>Check before posting</b>Confirm college/company access wording, the founders programme link, and whether any session type can be called free.</div>
    </div>
    <div><span class="label">Sources</span><ul class="src" style="margin-top:2mm">
      <li>YourDOST blog categories and Warrior stories (yourdost.com/blog), read 7 Nov 2026; site footer figures: experts within 30 seconds, 20+ Indian languages, 500+ organisations, 30 lakh+ sessions, 23+ states.</li>
      <li>YourDOST EIR brief: B2B with corporates and colleges; therapy, instant chat, self-help tools, structured programmes. Founders programme: yourdost.com/emotional-wellness-founders.</li>
      <li>Blind survey, 1,552 India-based professionals, July 2026: 66% of AI/ML professionals expect layoffs or big cuts within 3–6 months (Business Today, 10 Aug 2026).</li>
      <li>Deloitte, Mental health and well-being in the workplace (2022): about US$14 bn / ₹1.1 lakh crore a year to Indian employers (People Matters).</li>
      <li>Tele MANAS 14416, Ministry of Health and Family Welfare: free, 24×7. Diwali: Sun 8 Nov 2026. International Men's Day: 19 Nov.</li>
    </ul></div>
  </div>
  <footer class="pf">#JoBolaNahi · Q2 Instagram posts · Chethan N for YourDOST · Concept, not official YourDOST content</footer>
</section>
</body></html>`;

const docFile = path.join(tmp, "doc.html");
fs.writeFileSync(docFile, html);
const doc = await browser.newPage();
await doc.goto(url(docFile), { waitUntil: "load" });
await doc.evaluate(() => document.fonts.ready);
await doc.pdf({ path: outPdf, format: "A4", landscape: true, printBackground: true, preferCSSPageSize: true });
if (process.argv.includes("--png")) await doc.screenshot({ path: path.join(tmp, "doc.png"), fullPage: true });
await browser.close();
console.log(outPdf, (fs.statSync(outPdf).size / 1024).toFixed(0) + " KB", "tmp:", tmp);
