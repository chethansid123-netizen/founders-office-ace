"""Generate one consistent mock dataset for the VP Ops weekly MIS demo.

Every number is mock. Week 41 and Week 42 national totals are pinned to the
numbers in the interview prep pack; city rows always add up to national totals.
"""
import datetime as dt
import json
import math
import random
import sys

random.seed(19)

WEEKS = list(range(31, 43))
CUR, PREV = 42, 41


def week_start(w):
    return dt.date.fromisocalendar(2026, w, 1)


def month_of(w):
    # ISO convention: a week belongs to the month its Thursday falls in
    return dt.date.fromisocalendar(2026, w, 4).strftime("%b")


def alloc(total, weights):
    """Split an integer total across weights, largest remainder rounding."""
    s = sum(weights)
    raw = [total * x / s for x in weights]
    fl = [math.floor(r) for r in raw]
    rem = total - sum(fl)
    order = sorted(range(len(raw)), key=lambda i: raw[i] - fl[i], reverse=True)
    for i in order[:rem]:
        fl[i] += 1
    return fl


# ---------------------------------------------------------------- national
REQ = [72600, 73100, 74000, 74500, 75300, 76100, 76800, 77600, 78300, 79100, 79900, 81400]
FILL = [94.1, 94.4, 93.9, 94.2, 94.0, 93.7, 93.9, 93.5, 93.6, 93.2, 93.0, 91.6]
CC = [2.6, 2.7, 2.5, 2.6, 2.8, 2.6, 2.5, 2.7, 2.6, 2.4, 2.5, 2.9]
PC = [1.1, 1.2, 1.1, 1.2, 1.1, 1.2, 1.3, 1.2, 1.3, 1.2, 1.3, 1.6]
OT = [90.4, 90.1, 90.6, 90.2, 89.9, 90.3, 89.8, 89.6, 89.9, 89.4, 89.1, 88.4]
ACTIVE = [7060, 7090, 7130, 7160, 7190, 7230, 7260, 7300, 7340, 7380, 7420, 7480]
CERT = [168, 172, 175, 160, 181, 177, 170, 188, 179, 192, 185, 210]
RET = [66, 65, 66, 64, 65, 63, 64, 62, 63, 62, 63, 64]
RATING = [4.75, 4.74, 4.76, 4.75, 4.74, 4.75, 4.73, 4.74, 4.75, 4.73, 4.74, 4.72]
CPK = [7.6, 7.9, 7.4, 7.8, 8.0, 7.7, 7.9, 8.2, 7.8, 8.0, 8.1, 9.8]
REDO = [0.9, 1.0, 0.9, 1.0, 1.0, 0.9, 1.0, 1.1, 1.0, 1.0, 1.0, 1.1]
KIT = [1.6, 1.7, 1.5, 1.8, 1.7, 1.9, 1.8, 2.0, 1.9, 2.2, 2.1, 3.2]
LOW = [2.2, 2.3, 2.1, 2.3, 2.4, 2.2, 2.4, 2.5, 2.3, 2.4, 2.4, 2.8]  # % of ratings below 4 stars
RATED = [0.62, 0.615, 0.62, 0.625, 0.62, 0.618, 0.622, 0.62, 0.617, 0.621, 0.62, 0.62]
COHORT = [251, 238, 262, 244, 255, 249, 241, 258, 246, 252, 248, 260]
AOV = [1328, 1331, 1335, 1330, 1338, 1341, 1339, 1344, 1347, 1350, 1352, 1365]

# Pinned to the prep pack (Week 41 = last week, Week 42 = this week)
PIN = {
    41: dict(req=79900, asg=74307, cc=1850, pc=957, ratings_sum_round=True,
             cpl=579, redo=715, stock=156, coh_active=156),
    42: dict(req=81400, asg=74562, cc=2165, pc=1197, cpl=698, redo=783,
             stock=239, coh_active=166),
}

nat = {}
for i, w in enumerate(WEEKS):
    p = PIN.get(w, {})
    req = p.get("req", REQ[i])
    asg = p.get("asg", round(req * FILL[i] / 100))
    cc = p.get("cc", round(asg * CC[i] / 100))
    pc = p.get("pc", round(asg * PC[i] / 100))
    comp = asg - cc - pc
    ot = round(comp * OT[i] / 100)
    cpl = p.get("cpl", round(comp * CPK[i] / 1000))
    redo = p.get("redo", round(comp * REDO[i] / 100))
    rc = round(comp * RATED[i])
    rs = round(rc * RATING[i])
    low = round(rc * LOW[i] / 100)
    act = ACTIVE[i]
    stock = p.get("stock", round(act * KIT[i] / 100))
    coh = COHORT[i]
    coh_a = p.get("coh_active", round(coh * RET[i] / 100))
    qfail = (cpl + redo + low) / comp * 0.85  # overlap between the three
    perfect = round(ot * (1 - qfail))
    gmv = comp * AOV[i]
    nat[w] = dict(req=req, asg=asg, cc=cc, pc=pc, comp=comp, ot=ot, perfect=perfect,
                  cpl=cpl, redo=redo, rc=rc, rs=rs, low=low, act=act, cert=CERT[i],
                  stock=stock, coh=coh, coh_a=coh_a, gmv=gmv)

# ---------------------------------------------------------------- cities
CITIES = ["Delhi", "Gurugram", "Noida & Ghaziabad", "Mumbai", "Bengaluru",
          "Hyderabad", "Pune", "Rest of India"]
SHARE = [0.17, 0.12, 0.11, 0.14, 0.12, 0.08, 0.06, 0.20]
CITY_AOV = [1340, 1420, 1310, 1460, 1410, 1300, 1330, 1240]
UTIL = [1.00, 1.03, 0.98, 1.10, 1.06, 0.99, 0.97, 0.90]  # jobs per partner, relative

BASE = {  # relative multipliers on each city's rate, every week
    "fill": [1.008, 0.996, 1.002, 0.992, 0.995, 1.004, 1.001, 1.000],
    "cc": [0.95, 1.05, 1.0, 1.08, 1.02, 0.95, 0.97, 0.98],
    "pc": [0.9, 1.15, 1.1, 0.95, 1.0, 0.95, 0.95, 1.0],
    "ot": [1.003, 0.997, 1.0, 0.992, 0.995, 1.004, 1.002, 1.003],
    "cpl": [0.95, 1.1, 1.05, 0.95, 1.0, 0.95, 0.9, 1.05],
    "redo": [1.0, 1.05, 1.0, 1.0, 1.0, 0.95, 0.95, 1.0],
    "stock": [1.0, 1.1, 1.1, 0.9, 0.95, 0.9, 0.9, 1.0],
    "rating": [0.0, -0.01, 0.0, 0.01, 0.01, 0.0, 0.0, -0.01],
    "low": [0.95, 1.1, 1.0, 0.95, 0.95, 1.0, 1.0, 1.05],
}
SHOCK42 = {  # what went wrong this week, by city
    "fill": [1.0, 0.99, 1.0, 0.962, 0.972, 1.006, 1.004, 1.008],
    "cc": [1.0, 1.0, 1.0, 1.2, 1.05, 1.0, 1.0, 0.95],
    "pc": [0.85, 1.6, 1.4, 0.9, 0.9, 0.8, 0.8, 0.75],
    "ot": [1.0, 0.985, 0.99, 0.982, 0.99, 1.003, 1.004, 1.006],
    "cpl": [0.88, 1.65, 1.05, 0.88, 0.88, 0.82, 0.82, 0.88],
    "stock": [1.1, 1.95, 1.55, 0.7, 0.75, 0.65, 0.65, 0.6],
    "rating": [0.0, -0.06, -0.01, 0.0, 0.0, 0.01, 0.01, 0.01],
    "low": [0.95, 1.5, 1.05, 0.95, 0.95, 0.9, 0.9, 0.95],
}


def noise(sd):
    return 1 + random.gauss(0, sd)


rows = []
for w in WEEKS:
    n = nat[w]
    sh = [s * noise(0.012) for s in SHARE]
    m = {k: [BASE[k][c] * (SHOCK42[k][c] if (w == CUR and k in SHOCK42) else 1) *
             (noise(0.006) if k in ("fill", "ot") else noise(0.05) if k != "rating" else 1)
             for c in range(8)] for k in BASE}
    req = alloc(n["req"], sh)
    asg = alloc(n["asg"], [req[c] * m["fill"][c] for c in range(8)])
    cc = alloc(n["cc"], [asg[c] * m["cc"][c] for c in range(8)])
    pc = alloc(n["pc"], [asg[c] * m["pc"][c] for c in range(8)])
    comp = [asg[c] - cc[c] - pc[c] for c in range(8)]
    ot = alloc(n["ot"], [comp[c] * m["ot"][c] for c in range(8)])
    cpl = alloc(n["cpl"], [comp[c] * m["cpl"][c] for c in range(8)])
    redo = alloc(n["redo"], [comp[c] * m["redo"][c] for c in range(8)])
    rc = alloc(n["rc"], [comp[c] * noise(0.01) for c in range(8)])
    rating_c = [RATING[WEEKS.index(w)] + m["rating"][c] for c in range(8)]
    rs = alloc(n["rs"], [rc[c] * rating_c[c] for c in range(8)])
    low = alloc(n["low"], [rc[c] * m["low"][c] for c in range(8)])
    act = alloc(n["act"], [comp[c] / UTIL[c] for c in range(8)])
    stock = alloc(n["stock"], [act[c] * m["stock"][c] for c in range(8)])
    cert = alloc(n["cert"], [act[c] * noise(0.08) for c in range(8)])
    coh = alloc(n["coh"], [act[c] * noise(0.05) for c in range(8)])
    coh_a = alloc(n["coh_a"], [coh[c] * noise(0.03) for c in range(8)])
    qf = [(cpl[c] + redo[c] + low[c]) / comp[c] * 0.85 for c in range(8)]
    perfect = alloc(n["perfect"], [ot[c] * (1 - qf[c]) for c in range(8)])
    for c, city in enumerate(CITIES):
        rows.append(dict(
            week=w, week_start=week_start(w).isoformat(), month=month_of(w), city=city,
            req=req[c], asg=asg[c], cc=cc[c], pc=pc[c], comp=comp[c], ot=ot[c],
            perfect=perfect[c], cpl=cpl[c], redo=redo[c], rc=rc[c], rs=rs[c], low=low[c],
            act=act[c], cert=cert[c], stock=stock[c], coh=coh[c], coh_a=coh_a[c],
            gmv=comp[c] * CITY_AOV[c],
        ))

# sanity: integrity rules the MIS checks for
for r in rows:
    assert r["asg"] <= r["req"] and r["ot"] <= r["comp"] and r["perfect"] <= r["ot"], r
    assert r["stock"] <= r["act"] and r["coh_a"] <= r["coh"] and r["low"] <= r["rc"], r
for w in WEEKS:
    for k in ("req", "asg", "cc", "pc", "comp", "ot", "perfect", "cpl", "redo", "act", "stock"):
        assert sum(r[k] for r in rows if r["week"] == w) == nat[w][k], (w, k)

# ---------------------------------------------------------------- week-42 detail
# Day x slot grid: share of requests and fill rate (adjusted so the grid totals match)
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SLOTS = ["8–11", "11–14", "14–17", "17–20", "20–22"]
DAY_SH = [12.0, 11.6, 11.8, 12.1, 13.5, 19.4, 19.6]
SLOT_SH = [20, 24, 21, 23, 12]
BASE_FILL = [96.6, 96.0, 95.4, 93.8, 92.2]
WKND = [-2.4, -3.6, -4.6, -9.2, -10.8]
cells = []
weights = [DAY_SH[d] * SLOT_SH[s] for d in range(7) for s in range(5)]
creq = alloc(nat[CUR]["req"], weights)
fills = []
for d in range(7):
    for s in range(5):
        f = BASE_FILL[s] + (WKND[s] if d >= 5 else (-1.8 if d == 4 and s >= 3 else 0))
        fills.append(f + random.gauss(0, 0.35))
casg = alloc(nat[CUR]["asg"], [creq[i] * fills[i] for i in range(35)])
grid = []
for d in range(7):
    row = []
    for s in range(5):
        i = d * 5 + s
        row.append(dict(req=creq[i], asg=casg[i]))
    grid.append(row)
unfilled_total = nat[CUR]["req"] - nat[CUR]["asg"]
wknd_eve = [(d, s) for d in (5, 6) for s in (3, 4)]
wknd_eve_req = sum(grid[d][s]["req"] for d, s in wknd_eve)
wknd_eve_unf = sum(grid[d][s]["req"] - grid[d][s]["asg"] for d, s in wknd_eve)

# Service categories, completed jobs and complaints, W41 and W42
CATS = ["Waxing", "Facial & clean-up", "Massage & body", "Hair care", "Mani-pedi",
        "Threading & de-tan", "Laser & Hydra", "Makeup"]
CAT_SH = [24, 20, 9, 13, 12, 11, 6, 5]
CPK41 = [9.4, 7.9, 6.2, 8.4, 7.1, 6.8, 10.6, 9.0]
CPK42 = [15.0, 8.6, 6.4, 9.1, 7.3, 6.9, 11.5, 10.1]
cats = []
cj41 = alloc(nat[PREV]["comp"], CAT_SH)
cj42 = alloc(nat[CUR]["comp"], [CAT_SH[i] * (1.03 if CATS[i] in ("Makeup", "Laser & Hydra") else 1)
                                for i in range(8)])
cc41 = alloc(nat[PREV]["cpl"], [cj41[i] * CPK41[i] for i in range(8)])
cc42 = alloc(nat[CUR]["cpl"], [cj42[i] * CPK42[i] for i in range(8)])
for i, cat in enumerate(CATS):
    cats.append(dict(cat=cat, jobs41=cj41[i], cpl41=cc41[i], jobs42=cj42[i], cpl42=cc42[i]))

# Complaint reasons (W42)
REASONS = [("Service quality", 236), ("Late arrival", 162), ("Product & hygiene", 118),
           ("Pricing & billing", 71), ("Partner behaviour", 64), ("Damage & other", 47)]
assert sum(x[1] for x in REASONS) == nat[CUR]["cpl"]

# Hubs (12 of ~140), W42
HUBS = [
    # code, city, partners, jobs, complaints, stock-out partners, partner cancels, assigned
    ("GGN-2", "Gurugram", 61, 612, 15, 6, 21, 650),
    ("GGN-4", "Gurugram", 57, 571, 12, 5, 15, 604),
    ("NOI-1", "Noida & Ghaziabad", 64, 598, 7, 4, 16, 628),
    ("GGN-1", "Gurugram", 55, 540, 7, 3, 9, 566),
    ("DEL-3", "Delhi", 66, 640, 6, 2, 13, 664),
    ("NOI-3", "Noida & Ghaziabad", 52, 489, 5, 3, 8, 512),
    ("DEL-1", "Delhi", 70, 702, 6, 1, 9, 722),
    ("MUM-2", "Mumbai", 58, 655, 5, 1, 10, 688),
    ("BLR-1", "Bengaluru", 54, 588, 5, 1, 5, 610),
    ("MUM-4", "Mumbai", 49, 560, 4, 0, 7, 590),
    ("HYD-2", "Hyderabad", 50, 496, 4, 1, 4, 512),
    ("PUN-1", "Pune", 41, 402, 3, 0, 5, 418),
]
hubs = [dict(hub=h[0], city=h[1], partners=h[2], jobs=h[3], cpl=h[4], stock=h[5], pc=h[6], asg=h[7])
        for h in HUBS]

# Kit SKUs: partners reporting a stock-out, by item (a partner can report several)
SKUS = [("Wax & strips", 52, 118), ("Disposable sheets & towels", 38, 74),
        ("Single-use facial kits", 31, 61), ("Gloves & hygiene pack", 24, 45),
        ("Threading & bleach", 14, 22), ("Hair spa & colour", 12, 19), ("Mani-pedi tools", 9, 14)]
skus = [dict(sku=s[0], w41=s[1], w42=s[2]) for s in SKUS]

# Partner supply funnel by week (national)
supply = []
for i, w in enumerate(WEEKS):
    cert = CERT[i]
    sourced = round(cert * random.uniform(5.7, 6.2))
    started = round(cert * random.uniform(2.55, 2.75))
    kit = round(cert * random.uniform(0.92, 0.95))
    first = round(cert * random.uniform(0.80, 0.84))
    supply.append(dict(week=w, sourced=sourced, started=started, cert=cert, kit=kit, first_job=first,
                       in_training=round(1320 + i * 14 + random.gauss(0, 20))))

# Monthly joining cohorts: % still active at week 1, 2, 4, 8, 13
cohorts = [
    dict(cohort="Apr 2026", size=690, ret=[93, 87, 79, 71, 65]),
    dict(cohort="May 2026", size=720, ret=[92, 86, 78, 70, 64]),
    dict(cohort="Jun 2026", size=705, ret=[93, 86, 77, 69, 63]),
    dict(cohort="Jul 2026", size=760, ret=[92, 85, 77, 70, 64]),
    dict(cohort="Aug 2026", size=790, ret=[91, 85, 76, 69, None]),
    dict(cohort="Sep 2026", size=800, ret=[92, 84, 77, None, None]),
]

# Partners by average jobs per working day, W42
util_bands = [("< 0.5", 560), ("0.5–1", 980), ("1–1.5", 1720), ("1.5–2", 2240),
              ("2–2.5", 1330), ("2.5+", 650)]
assert sum(b[1] for b in util_bands) == nat[CUR]["act"]

# ---------------------------------------------------------------- actions
REPORT_DATE = "2026-10-19"
actions = [
    dict(id="A-101", action="Refill top 5 kit items at Gurugram and Noida hubs", owner="Inventory",
         kpi="Kit stock-out", raised="2026-10-12", due="2026-10-16", status="In progress", closed=None,
         update="3 of 5 items refilled; wax batch on hold for QC", next="Clear wax QC Tue, refill by Wed"),
    dict(id="A-102", action="Retrain 41 flagged waxing partners, GGN-2 and GGN-4", owner="Training & QA",
         kpi="Complaints / 1,000", raised="2026-10-14", due="2026-10-22", status="In progress", closed=None,
         update="18 of 41 retrained", next="Two more batches Wed and Thu"),
    dict(id="A-103", action="QC check on wax batch #W-2291 used in Gurugram", owner="Inventory",
         kpi="Complaints / 1,000", raised="2026-10-15", due="2026-10-20", status="In progress", closed=None,
         update="Samples sent to vendor lab", next="Lab result Tue"),
    dict(id="A-104", action="Weekend-evening incentive pilot: MUM-2, MUM-4, BLR-1", owner="City Ops",
         kpi="Fill rate", raised="2026-10-15", due="2026-10-23", status="Not started", closed=None,
         update="Waiting for VP budget sign-off", next="Decision in Mon review"),
    dict(id="A-105", action="Root-cause late arrivals beyond a 3 km dispatch radius", owner="City Ops",
         kpi="On-time arrival", raised="2026-10-13", due="2026-10-22", status="In progress", closed=None,
         update="Pulled 2 weeks of dispatch logs", next="Share findings Thu"),
    dict(id="A-106", action="Re-activate 420 partners with no job in 14 days", owner="Supply",
         kpi="Active partners", raised="2026-10-12", due="2026-10-24", status="In progress", closed=None,
         update="240 called, 96 back on app", next="Finish calls Fri"),
    dict(id="A-107", action="Week-4 drop-off survey, Aug joining cohort", owner="Supply",
         kpi="90-day retention", raised="2026-10-08", due="2026-10-17", status="In progress", closed=None,
         update="62 of 150 responses", next="Close Tue, readout at review"),
    dict(id="A-108", action="Add 2 Noida training batches for wedding season", owner="Training & QA",
         kpi="New partners certified", raised="2026-10-12", due="2026-10-26", status="In progress", closed=None,
         update="Trainers confirmed", next="Batch 1 starts Mon 26"),
    dict(id="A-109", action="Auto-escalate complaints open over 24 hours", owner="CX",
         kpi="Complaints resolved < 24h", raised="2026-10-13", due="2026-10-23", status="In progress", closed=None,
         update="Rule drafted with tech", next="Go live Thu"),
    dict(id="A-110", action="Audit refund approvals above ₹1,500", owner="CX",
         kpi="Redo / refund rate", raised="2026-10-06", due="2026-10-15", status="In progress", closed=None,
         update="Data pulled; review pending", next="Needs 1 hour with Finance"),
    dict(id="A-111", action="Hub kit auto-reorder at 5 days of stock", owner="Inventory",
         kpi="Kit stock-out", raised="2026-10-15", due="2026-10-30", status="Not started", closed=None,
         update="Needs VP approval for buffer stock", next="Decision in Mon review"),
    dict(id="A-112", action="Wedding-season staffing plan, Nov to Feb", owner="City Ops",
         kpi="Fill rate", raised="2026-10-12", due="2026-10-28", status="In progress", closed=None,
         update="Demand forecast done", next="Supply gap by city Wed"),
    dict(id="A-113", action="One definition for 'fill rate' across all 5 teams", owner="Founder's Office",
         kpi="Data quality", raised="2026-10-12", due="2026-10-19", status="Done", closed="2026-10-18",
         update="Metric dictionary v1 shared and used in the MIS", next="Sign-off by 5 managers and the VP (decision 3)"),
    dict(id="A-114", action="Cap Mumbai Saturday-evening slots at capacity", owner="City Ops",
         kpi="Fill rate", raised="2026-10-05", due="2026-10-14", status="Done", closed="2026-10-13",
         update="Live since 13 Oct", next="Review impact next week"),
    dict(id="A-115", action="Hygiene audit of 30 random partners", owner="Training & QA",
         kpi="Average rating", raised="2026-10-01", due="2026-10-12", status="Done", closed="2026-10-14",
         update="28 of 30 passed; 2 re-briefed", next="—"),
    dict(id="A-116", action="Automate the MIS refresh from the ops app", owner="Founder's Office",
         kpi="Data quality", raised="2026-10-12", due="2026-11-06", status="Not started", closed=None,
         update="Scoping with tech", next="Plan by 26 Oct"),
]

# On-time closure, last 4 weeks, by owner (mock history)
closure = {"City Ops": (9, 11), "Supply": (7, 9), "Training & QA": (8, 9), "CX": (6, 9), "Inventory": (5, 8),
           "Founder's Office": (6, 6)}

out = dict(
    meta=dict(cur=CUR, prev=PREV, weeks=WEEKS, report_date=REPORT_DATE,
              week_label="Week 42 · 12–18 Oct 2026", aov_note="mock"),
    cities=CITIES, rows=rows,
    grid=dict(days=DAYS, slots=SLOTS, cells=grid, wknd_eve_req=wknd_eve_req,
              wknd_eve_unf=wknd_eve_unf, unfilled=unfilled_total),
    cats=cats, reasons=REASONS, hubs=hubs, skus=skus, supply=supply, cohorts=cohorts,
    util_bands=util_bands, actions=actions, closure=closure,
)
json.dump(out, open(sys.argv[1], "w"), indent=1)

# quick summary for the build log
for w in (31, 41, 42):
    n = nat[w]
    print(w, "req", n["req"], "fill %.1f" % (100 * n["asg"] / n["req"]), "comp", n["comp"],
          "ot %.1f" % (100 * n["ot"] / n["comp"]), "perfect", n["perfect"],
          "nsm %.1f" % (100 * n["perfect"] / n["req"]), "jppd %.2f" % (n["comp"] / n["act"] / 6),
          "cpk %.1f" % (1000 * n["cpl"] / n["comp"]), "rating %.2f" % (n["rs"] / n["rc"]),
          "ret %.0f" % (100 * n["coh_a"] / n["coh"]), "kit %.1f" % (100 * n["stock"] / n["act"]),
          "cc %.1f pc %.1f" % (100 * n["cc"] / n["asg"], 100 * n["pc"] / n["asg"]),
          "redo %.1f" % (100 * n["redo"] / n["comp"]))
print("weekend eve share of req %.1f%%, of unfilled %.1f%% (%d of %d)" % (
    100 * wknd_eve_req / nat[CUR]["req"], 100 * wknd_eve_unf / unfilled_total, wknd_eve_unf, unfilled_total))
for r in rows:
    if r["week"] == CUR:
        print("  %-18s req %6d fill %.1f pc %.2f cpk %.1f kit %.1f ot %.1f jppd %.2f" % (
            r["city"], r["req"], 100 * r["asg"] / r["req"], 100 * r["pc"] / r["asg"],
            1000 * r["cpl"] / r["comp"], 100 * r["stock"] / r["act"], 100 * r["ot"] / r["comp"],
            r["comp"] / r["act"] / 6))

wx = cats[0]
print("waxing share of complaint rise %.0f%%" % (100 * (wx["cpl42"] - wx["cpl41"]) / (nat[CUR]["cpl"] - nat[PREV]["cpl"])),
      "waxing cpk %.1f -> %.1f" % (1000 * wx["cpl41"] / wx["jobs41"], 1000 * wx["cpl42"] / wx["jobs42"]))
xs = [h["stock"] / h["partners"] for h in hubs]; ys = [h["pc"] / h["asg"] for h in hubs]
mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys)); sxx = sum((a - mx) ** 2 for a in xs); syy = sum((b - my) ** 2 for b in ys)
print("hub r = %.2f" % (sxy / (sxx * syy) ** 0.5))
