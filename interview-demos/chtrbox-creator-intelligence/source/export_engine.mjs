// Runs the built page headless and exports the engine's own numbers for the PDF.
//   G=$(npm root -g) node export_engine.mjs ../Creator-Intelligence-Engine.html engine_export.json
import { createRequire } from 'module';
import { writeFileSync } from 'fs';
const require = createRequire((process.env.G || '/usr/lib/node_modules') + '/');
const { chromium } = require('playwright');
const [, , page_path, out] = process.argv;
const browser = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage();
await page.goto('file://' + new URL(page_path, 'file://' + process.cwd() + '/').pathname);
const data = await page.evaluate(() => {
  const { scoreBrand, buildPlan, vanityPlan, BBY, OBJ } = window.__cie;
  const brands = {};
  for (const b of Object.values(BBY)) {
    const res = scoreBrand(b, b.objective, OBJ[b.objective].w);
    const plan = buildPlan(res, b.budget * 1e5), van = vanityPlan(res, plan.agg.cost);
    const gates = {}; for (const r of res.gated) for (const g of r.g) gates[g.k] = (gates[g.k] || 0) + 1;
    brands[b.id] = {
      name: b.name, vertical: b.vertical, objective: b.objective, budget: b.budget, status: b.status, eligible: res.ranked.length, gated: res.gated.length, gates,
      plan: plan.agg, vanity: van.agg,
      top: res.ranked.slice(0, 10).map(r => ({ id: r.c.id, name: r.c.name, niche: r.c.niche, tier: r.c.tier, followers: r.c.followers, city: r.c.city, langs: r.c.langs, platform: r.c.platform,
        fit: +r.total.toFixed(1), s: Object.fromEntries(Object.entries(r.s).map(([k, v]) => [k, Math.round(v)])), er: r.c.er, ctr: r.c.ctr, cred: r.c.cred, vtr: r.c.vtr, recallPast: r.c.recall,
        fem: r.c.aud.fem, cost: r.p.cost, views: Math.round(r.p.views), tg: Math.round(r.p.tgViews), eng: Math.round(r.p.eng), clicks: Math.round(r.p.clicks), orders: +r.p.orders.toFixed(1), rev: Math.round(r.p.rev),
        recall: +r.p.recall.toFixed(1), roas: +r.p.roas.toFixed(2), conf: r.conf[0], creds: r.c.creds, represent: r.c.represent, codes: r.c.codes })),
    };
  }
  return brands;
});
writeFileSync(out, JSON.stringify(data));
console.log('exported', Object.keys(data).length, 'brands');
await browser.close();
