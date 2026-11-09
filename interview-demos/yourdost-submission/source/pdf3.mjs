import { createRequire } from "node:module";
const require = createRequire("/home/user/founders-office-ace/interview-demos/yourdost-instagram-v7/source/");
const { chromium } = require("playwright");
import path from "node:path";
import fs from "node:fs";
import { pathToFileURL } from "node:url";
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
await p.goto(pathToFileURL(path.resolve("master.html")).href);
await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
await p.pdf({ path: "out/master.pdf", preferCSSPageSize: true, printBackground: true });
await p.evaluate(() => document.body.classList.add("ppt"));
const links = [];
for (const [i, el] of (await p.$$(".pg")).entries()) {
  await el.screenshot({ path: `out/p${String(i + 1).padStart(2, "0")}.png` });
  const bb = await el.boundingBox();
  links.push(await el.$$eval("a[href]", (as, o) => as.map(a => { const r = a.getBoundingClientRect(); return { x: r.x, y: r.y - o, w: r.width, h: r.height, u: a.href }; }), bb.y));
}
fs.writeFileSync("out/links.json", JSON.stringify(links));
await b.close();
