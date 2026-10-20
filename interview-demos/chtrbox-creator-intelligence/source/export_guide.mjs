// Export every number the platform shows, per brand and objective, for the presenter's guide.
//   G=$(npm root -g) node export_guide.mjs ../Creator-Intelligence-Engine.html guide_export.json
import { createRequire } from 'module';
import { writeFileSync } from 'fs';
import { resolve } from 'path';
const require = createRequire((process.env.G || '/usr/lib/node_modules') + '/');
const { chromium } = require('playwright');
const [, , page_path, out] = process.argv;
const browser = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage();
await page.goto('file://' + resolve(page_path));
const data = await page.evaluate(() => {
  const X = window.__cie, strip = h => h.replace(/<[^>]+>/g, '');
  const r1 = v => Math.round(v * 10) / 10, r2 = v => Math.round(v * 100) / 100;
  const agg = a => ({ creators: a.n, spend: Math.round(a.cost), views: Math.round(a.views), tgViews: Math.round(a.tg), uniqueTgReach: Math.round(a.reach), engagements: Math.round(a.eng), clicks: Math.round(a.clicks), orders: Math.round(a.orders), revenue: Math.round(a.rev), roas: r2(a.roas), recallLiftPts: r1(a.recall), fakeAudienceShare: r2(a.fake), gatedIncluded: a.gated, representCreators: a.rep, representSpend: Math.round(a.repCost), forecastBandPct: Math.round(a.band * 100), spendByTier: Object.fromEntries(Object.entries(a.tiers).map(([k, v]) => [k, Math.round(v)])) });
  const creator = (r, obj, b) => ({ rank: r.rank, id: r.c.id, name: r.c.name, niche: X.NICHE[r.c.niche], niche2: X.NICHE[r.c.niche2], tier: X.TIER[r.c.tier].label, followers: r.c.followers, city: r.c.city, languages: r.c.langs, platform: r.c.platform,
    represent: r.c.represent, credential: r.c.creds, fit: r1(r.total), parts: Object.fromEntries(Object.entries(r.s).map(([k, v]) => [k, Math.round(v)])), contributions: Object.fromEntries(Object.entries(r.contrib).map(([k, v]) => [k, r1(v)])),
    confidence: r.conf[0], er: r.c.er, linkCtr: r.c.ctr, realFollowers: r.c.cred, viewThrough: r.c.vtr, hold3s: r.c.hook, sponsoredShare: r.c.spons, adDisclosure: r.c.asci, safety: r.c.safety, audienceWomen: r.c.aud.fem,
    forecast: { cost: r.p.cost, views: Math.round(r.p.views), tgViews: Math.round(r.p.tgViews), tgShare: r2(r.p.tgShare), engagements: Math.round(r.p.eng), clicks: Math.round(r.p.clicks), orders: r1(r.p.orders), revenue: Math.round(r.p.rev), roas: r2(r.p.roas), recallLiftPts: r1(r.p.recall), costPerTgView: r2(r.p.cpv), costPerEngagement: r2(r.p.cpe), costPerClick: r2(r.p.cpc) },
    why: X.whyOf(r, obj, b).slice(0, 4).map(w => strip(w.html)), risks: X.flagsOf(b, r.c) });
  const brands = {};
  for (const b of Object.values(X.BBY)) {
    const per = {};
    for (const obj of Object.keys(X.OBJ)) {
      const res = X.scoreBrand(b, obj, X.OBJ[obj].w);
      const plan = X.buildPlan(res, b.budget * 1e5), van = X.vanityPlan(res, plan.agg.cost);
      const gates = {}; for (const r of res.gated) for (const g of r.g) gates[g.k] = (gates[g.k] || 0) + 1;
      const gatedExamples = res.gated.slice(0, 4).map(r => ({ name: r.c.name, id: r.c.id, reasons: r.g.map(g => g.t) }));
      per[obj] = { weights: X.OBJ[obj].w, eligible: res.ranked.length, gated: res.gated.length, gatesByReason: gates, gatedExamples,
        top: res.ranked.slice(0, obj === b.objective ? 10 : 5).map(r => creator(r, obj, b)), plan: agg(plan.agg), followerCountPlan: agg(van.agg),
        planCreators: plan.list.slice(0, 12).map(r => `${r.c.name} (${X.TIER[r.c.tier].label}, ${X.NICHE[r.c.niche]})`) };
    }
    brands[b.id] = { id: b.id, name: b.name, parent: b.parent, vertical: b.vertical, sub: b.sub, status: b.status, defaultObjective: b.objective, brief: b.brief, moment: b.moment, budgetLakh: b.budget,
      target: b.target, languages: b.langs, codes: b.codes, affinity: b.affinity, competitors: b.competitors, compliance: b.compliance, aov: b.aov, conversionRate: b.cvr, kpis: b.kpis, markets: b.markets, tgPoolMillions: b.pool, byObjective: per };
  }
  const campaigns = window.DATA_CAMPAIGNS = null;
  return { brands };
});
// campaigns and overview need DATA, which is a const in page scope; read it separately
const extra = await page.evaluate(() => {
  const X = window.__cie, r2 = v => Math.round(v * 100) / 100;
  const D = DATA;
  const camps = D.campaigns.map(cp => {
    const st = X.campStats(cp), b = st.b, t = st.t;
    const cr = Object.fromEntries(D.creators.map(c => [c.id, c]));
    const top = [...cp.rows].filter(r => r.a).sort((a, b2) => (b2.a.rev || b2.a.views) - (a.a.rev || a.a.views)).slice(0, 5).map(r => ({ name: cr[r.id].name, id: r.id, tier: X.TIER[cr[r.id].tier].label, niche: X.NICHE[cr[r.id].niche], fit: r.fit, cost: r.cost, views: r.a.views, viewsForecast: r.f.views, clicks: r.a.clicks, orders: r.a.orders, revenue: r.a.rev, roas: r2(r.a.rev / r.cost) }));
    return { id: cp.id, brand: b.name, title: cp.title, objective: b.objective, days: cp.days, elapsed: cp.elapsed, live: cp.live, budgetLakh: cp.budget, creators: cp.rows.length, posted: cp.rows.filter(r => r.posted).length,
      spend: t.cost, reportedViews: t.rep, apiVerifiedViews: t.api, uniqueViews: t.uniq, realPeople: t.real, inTargetGroup: t.tg, engagements: t.eng, clicks: t.clicks, orders: t.orders, attributedRevenue: t.rev,
      returnsRate: cp.returns, verifiedRevenue: Math.round(st.verified), incrementalShare: cp.inc_share, incrementalRevenue: Math.round(st.incr), attributedRoas: r2(st.groas), incrementalRoas: r2(st.iroas), ltvMultiplier: cp.ltv, ltvRoas: r2(st.ltv),
      emvClaimed: Math.round(st.emv), claimedRoi: r2(st.claimed), recallLiftPts: Math.round(st.recall * 10) / 10, brandLift: cp.lift, holdout: cp.holdout, attribution: cp.attr, mape: cp.mape, alerts: cp.alerts, topCreators: top, costPerClick: r2(t.cost / Math.max(1, t.clicks)), cpmTg: Math.round(t.cost / Math.max(1, t.tg) * 1000) };
  });
  const conv = camps.filter(c => c.objective !== 'awareness');
  const sum = (a, f) => a.reduce((s, x) => s + f(x), 0);
  const med = a => { const s = [...a].sort((x, y) => x - y); const m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
  const overview = { creators: D.creators.length, brands: D.brands.length, reportedClients: D.brands.filter(b => b.status === 'Reported client').length, prospects: D.brands.filter(b => b.status === 'Prospect').length,
    medianGatedShare: r2(med(D.brands.map(b => X.scoreBrand(b, b.objective, X.OBJ[b.objective].w).gated.length / D.creators.length))),
    incrementalRevenueAll: Math.round(sum(camps, c => c.incrementalRevenue)), conversionIroas: r2(sum(conv, c => c.incrementalRevenue) / sum(conv, c => c.spend)), conversionLtvRoas: r2(sum(conv, c => c.incrementalRevenue * c.ltvMultiplier) / sum(conv, c => c.spend)),
    meanRecallLift: Math.round(sum(camps, c => c.recallLiftPts) / camps.length * 10) / 10 };
  const verticals = D.verticals.map(([k, l]) => { const v = X.vertStats(k); return { key: k, label: l, brands: v.bs.map(b => b.name), playbook: X.PLAY[k], topCreators: v.top.slice(0, 5).map(a => ({ name: a.c.name, niche: X.NICHE[a.c.niche], tier: X.TIER[a.c.tier].label, meanFit: Math.round(a.avg), top20For: a.top })), heat: Object.fromEntries(Object.entries(v.heat).map(([n, val]) => [X.NICHE[n], Math.round(val)])) }; });
  const tiers = D.tiers;
  const creatorStats = Object.fromEntries(D.tiers.map(t => { const xs = D.creators.filter(c => c.tier === t.key); return [t.label, { count: xs.length, medianER: r2(med(xs.map(c => c.er))), medianReel: med(xs.map(c => c.rate.reel)), meanRealFollowers: Math.round(sum(xs, c => c.cred) / xs.length * 10) / 10, fraudFlagged: xs.filter(c => c.fraud).length }]; }));
  return { campaigns: camps, overview, verticals, tiers, creatorStats, families: X.FAMILIES, phases: X.PHASES, ops: X.OPS, assist: X.ASSIST, niches: D.niches };
});
writeFileSync(out, JSON.stringify({ ...data, ...extra }, null, 1));
console.log('exported', Object.keys(data.brands).length, 'brands,', extra.campaigns.length, 'campaigns');
await browser.close();
