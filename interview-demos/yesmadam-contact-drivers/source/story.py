"""Write story.json: titles, quotes, five whys, fixes and readout, with numbers taken from the tagged data."""
import collections
import json
import os
import math
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
full = json.load(open(f"{BASE}/analysis_full.json"))
R = full["reviews"]
UC = full["uc"]
C = [r for r in R if r["primary"] != "praise"]
nC = len(C)
by = collections.Counter(r["primary"] for r in C)
mentions = collections.Counter(k for r in C for k in {r["primary"], *r["secondary"]} if k != "praise")
contactedBy = collections.Counter(r["primary"] for r in C if r["contacted"] == "yes")
# rank by reviews; ties go to the driver mentioned more often, then the one that sent more people to support
ranked = sorted((k for k in by if k != "other"), key=lambda k: (-by[k], -mentions[k], -contactedBy[k], k))
order = ranked + (["other"] if "other" in by else [])
TOP = ranked[:3]
pct = lambda x: f"{math.floor(x * 100 + 0.5)}%"  # half-up, same as JS toFixed(0)
share = lambda k: by[k] / nC
top3 = sum(by[k] for k in TOP) / nC
oneStar = sum(1 for r in R if r["rating"] == 1)
top3c = sum(contactedBy[k] for k in TOP)
kc = contactedBy.most_common(1)[0][0]
contacted = [r for r in C if r["contacted"] == "yes"]
failed = [r for r in contacted if r["failed"] == "yes"]
churn = [r for r in C if r["churn"]]
ucC = UC["nC"]
ucs = lambda k: UC["byPrimary"].get(k, 0) / ucC
sub = lambda k, s: sum(1 for r in C if r["primary"] == k and r["subtag"] == s)
cnt = lambda k: by[k]
LABEL = {"partner_cancellation": "no-shows and cancellations", "price_clarity": "price and offer clarity", "service_quality": "service quality",
         "payment_refund": "payments and refunds", "support": "support", "app": "app bugs", "delay": "late arrivals", "product_fit": "products"}

QUOTE_PICKS = json.load(open(f"{BASE}/quote_picks.json")) if len(sys.argv) > 1 and sys.argv[1] == "--picks" else {}


def q(n, text=None):
    r = R[n - 1]
    assert r["n"] == n
    return dict(n=n, rating=r["rating"], date=r["date"], text=text or r["quote"], tag=None)


quotes = {k: [q(p["n"], p.get("text")) for p in QUOTE_PICKS.get(k, [])] for k in TOP}
for k in TOP:  # no hand-picked quotes: tagger quotes from the most severe reviews of that driver
    if not quotes[k]:
        rs = sorted([r for r in C if r["primary"] == k], key=lambda r: ({"high": 0, "medium": 1}.get(r["severity"], 2), r["rating"], -len(r["quote"])))
        quotes[k] = [q(r["n"]) for r in rs[:3]]

inj = [r for r in C if r["subtag"] in ("skin_injury_or_reaction", "product_reaction")]
inj_all, inj_wax = len(inj), sum(1 for r in inj if r["service"] == "waxing")

WHYS = {
    "partner_cancellation": dict(
        problem="Bookings fail at or after the slot time, and the customer is the last to know.",
        chain=[
            dict(text="The assigned professional declined, went on leave or fell ill, and no one else was sent (#62, #247, #250).", ev="E"),
            dict(text="Nobody checks before the slot that she is coming. The customer finds out at the slot time, or only when she calls support (#15, #193, #338).", ev="E"),
            dict(text="Accepting a job does not lock the professional in. Some ask the customer to cancel instead, so the drop is logged as a customer cancellation (#127, #219, #362).", ev="E"),
            dict(text="The app shows slots when no professional is free, and products run short too, so there is no one ready to send instead (#73, #284, #394).", ev="E"),
            dict(text="Slots are sold off the calendar, not off confirmed professional capacity in that area and hour, and payment is taken before anyone confirms.", ev="H"),
        ],
        root="Slots are sold before a professional is confirmed, and nothing checks or backfills a dropped job before the slot time.",
        test="If most failed bookings had a professional confirmed 2 hours before the slot and still failed, the problem is on-the-day behaviour, not slot inventory.",
    ),
    "price_clarity": dict(
        problem="Customers feel tricked: the free offer is gone in a minute, and the price grows at checkout.",
        chain=[
            dict(text="The offer they were sent could not be booked, or the final price was higher than the price shown (#10, #23).", ev="E"),
            dict(text="The free pedicure opens at 1 pm for everyone. Slots are gone by 1:02, and the app crashes at checkout in the rush (#78, #121, #138).", ev="E"),
            dict(text="It reads as a scam, not a sell-out, because it is pushed to everyone without saying how many slots exist (#48, #77).", ev="E"),
            dict(text="Compulsory fees sit outside the listed price: a platform fee, a ₹99 kit charge, a ₹300 line labelled tax. They appear only at checkout (#55, #126, #190).", ev="E"),
            dict(text="Offers and price pages are judged on installs and visits, not on how many offers are honoured or how many complaints they create.", ev="H"),
        ],
        root="Offers and prices are built to attract, not to be honoured: a tiny flash offer pushed to everyone, and compulsory fees shown only at checkout.",
        test="If offer complaints spike only on days the app crashed at 1 pm, this is an engineering capacity problem, not offer design.",
    ),
    "service_quality": dict(
        problem=f"The service itself goes wrong: untrained or rushed work, rude behaviour, and burns or rashes ({inj_wax} of the {inj_all} burn or reaction reviews follow waxing).",
        chain=[
            dict(text="The professional lacked the skill for that service: burnt skin after waxing, ruined brows, half-done work (#41, #152, #191).", ev="E"),
            dict(text="Professionals reach customers before their skill on each service is proven. Quality is checked by ratings after the job, not before it.", ev="H"),
            dict(text="Professionals rush the job ('in too much hurry', a facial done in 30 minutes), likely because back-to-back slots leave no slack (#50, #264, #351).", ev="E"),
            dict(text="When something goes wrong, the answer is a coupon, not a call-back or care for the injury: a ₹400 coupon for a burnt hand (#41, #104, #217).", ev="E"),
            dict(text="Complaints are closed case by case in support and don't flow back to the professional's record, training or assignment.", ev="H"),
        ],
        root="No closed loop from complaint to professional: skill isn't certified per service before risky jobs like waxing, and complaints end in coupons instead of retraining.",
        test="If complaints are spread evenly across professionals rather than concentrated in a few, the problem is training content or products, not specific people.",
    ),
    "payment_refund": dict(
        problem="Money gets stuck: refunds are slow or refused, or customers are charged without being served.",
        chain=[
            dict(text="A refund didn't arrive when promised, or a charge went through for a booking that never happened.", ev="E"),
            dict(text="Refunds go to the in-app wallet by default and customers expected their bank or UPI.", ev="E"),
            dict(text="Support can't see or speed up the refund, so customers chase it again and again.", ev="E"),
            dict(text="Refund status isn't shown in the app with a date.", ev="H"),
            dict(text="Refunds are owned by finance, not measured as a customer promise.", ev="H"),
        ],
        root="Refunds have no promised date the customer can see, and default to the wallet.",
        test="If most refunds land within 5 days and complaints are about expectation only, the fix is messaging, not process.",
    ),
}
FIXES = {
    "partner_cancellation": dict(name="Confirm or reassign 2 hours before", owner="City Ops, Supply and Product",
        what="Professional confirms 2 hours before the slot. No confirmation means auto-reassign from the nearby pool, and the customer gets a message with a choice before the slot, not after. Sell slots only against confirmed capacity. Log a professional's 'please cancel' as a partner cancellation.",
        metric="Failed bookings per 100, partner side", target="Down 40% in 8 weeks; 90% of failures with 2+ hours' notice",
        measure="Pilot in 2 cities against 2 similar cities for 4 weeks. Track failed bookings, notice given, reassign success, and contacts per 100 bookings for 'where is my professional'."),
    "price_clarity": dict(name="Price shown is price paid; honest offers", owner="Growth, Product and Finance",
        what="Show compulsory fees inside the listed price. Label flash offers with the number of slots ('200 free pedicures today') and give a waitlist or coupon when they run out. Load-test the 1 pm checkout.",
        metric="Offer and price complaints per 1,000 bookings", target="Down 50%, with checkout conversion flat or better",
        measure="A/B test all-in prices on 10% of users for 2 weeks: conversion, cart-to-payment drop-off, and contacts tagged offer or charges. Track app crashes in the 1 pm window."),
    "service_quality": dict(name="Certify risky services; close the loop on complaints", owner="Training & QA and CX",
        what="Certify each professional per service, waxing first, before she is assigned it. Every injury complaint gets a call within 24 hours, care for the customer, and the professional is paused and retrained. Weekly list of professionals with 2+ complaints.",
        metric="Injury and quality complaints per 1,000 jobs", target="Down 30% in 12 weeks; no repeat complaint within 30 days of retraining",
        measure="Before and after by hub cohort. Check how concentrated complaints are: if the worst 10% of professionals carry most of them, target them first."),
    "payment_refund": dict(name="Refund with a date the customer can see", owner="Finance, Product and CX",
        what="Refund to source by default, show the refund date in the app, and alert support when a refund is late.",
        metric="Refund contacts per 1,000 refunds", target="Down 50%", measure="Before and after, by refund type."),
}

# ---- notes computed from the data ----
gaps = sorted(((k, share(k) - ucs(k)) for k in ranked), key=lambda x: x[1])
hi_k, hi_g = gaps[-1]
lo_k, lo_g = gaps[0]
uc_rank = [k for k, _ in sorted(UC["byPrimary"].items(), key=lambda x: -x[1]) if k not in ("other", "praise")][:3]
BENCH_NOTES = [
    f"<b>Same pain, different weights.</b> Urban Company's top three are {', '.join(LABEL[k] for k in uc_rank)}. Overlap with Yes Madam's top three: {len(set(uc_rank) & set(TOP))} of 3.",
    f"<b>Yes Madam over-indexes on {LABEL[hi_k]}</b>: {pct(share(hi_k))} of complaints vs {pct(ucs(hi_k))} at Urban Company ({hi_g * 100:+.0f} pts).",
    f"<b>Yes Madam under-indexes on {LABEL[lo_k]}</b>: {pct(share(lo_k))} vs {pct(ucs(lo_k))} ({lo_g * 100:+.0f} pts).",
    f"Both apps: over 4 in 10 written reviews are 1★ ({pct(oneStar / len(R))} Yes Madam, {pct(UC['oneStar'] / UC['n'])} Urban Company), against store averages of 4.73★ and 4.77★. Reviews skew negative everywhere.",
]
months = sorted({r["date"][:7] for r in R})
offer_by_m = {m: sum(1 for r in C if r["date"].startswith(m) and r["subtag"] == "offer_not_honoured") for m in months}
peak_m = max(offer_by_m, key=offer_by_m.get)
import datetime as _dt
mname = lambda m: _dt.date(int(m[:4]), int(m[5:]), 1).strftime("%b")
dday = lambda d: f"{int(d[8:])} {_dt.date(int(d[:4]), int(d[5:7]), 1).strftime('%b')}"
import re as _re
fp = [r for r in C if r["primary"] == "price_clarity" and _re.search(r"free\s*pedi", r["title"] + " " + r["text"], _re.I)]
by_wo = collections.Counter(r["primary"] for r in C if r not in fp)
rank_wo = sorted((k for k in by_wo if k != "other"), key=lambda k: (-by_wo[k], -mentions[k])).index("price_clarity") + 1 if fp else 0
FP = dict(n=len(fp), first=min(r["date"] for r in fp) if fp else "", last=max(r["date"] for r in fp) if fp else "", rank_without=rank_wo)
MONTH_NOTE = (f"Offer complaints ('offer or coupon not honoured') peak in {mname(peak_m)} ({offer_by_m[peak_m]} reviews). "
              + (f"The free-pedicure campaign alone is {len(fp)} of the {by['price_clarity']} price and offer complaints ({dday(FP['first'])} to {dday(FP['last'])}). Take it out and price and offers still rank #{rank_wo}." if fp else "Check them against the campaign calendar before calling them structural.")
              if offer_by_m[peak_m] else "")
app_by_v = collections.Counter(r["version"] for r in C if r["primary"] == "app")
all_by_v = collections.Counter(r["version"] for r in R)
if app_by_v:
    v, nv = app_by_v.most_common(1)[0]
    VERSION_NOTE = f"<b>Version {v}</b> has the most app complaints ({nv} of {all_by_v[v]} reviews on it). {sum(app_by_v.values())} reviews in all are about the app itself: a release-quality question for tech, not an ops one."
else:
    VERSION_NOTE = "No version stands out."

story = dict(
    top3=TOP, order=order,
    t1=f"{pct(top3)} of complaints come down to three things: {LABEL[TOP[0]]}, {LABEL[TOP[1]]} and {LABEL[TOP[2]]}.",
    t2=f"{LABEL[TOP[0]].capitalize()} lead, at {pct(share(TOP[0]))} of complaints. Customers don't just dislike them; many have already called support about them.",
    t3="Each driver traces back to something the operation does, not something customers do.",
    t4="The top three drivers are the bulk of the support load, and the bigger cost is customers who don't come back.",
    t5="Three fixes, three owners, one metric each: contacts per 100 bookings by driver.",
    tR="Why customers contact Yes Madam, and what to fix first.",
    tB=f"Same top drivers as Urban Company, but Yes Madam over-indexes on {LABEL[max([k for k in ranked if k in by], key=lambda k: share(k) - ucs(k))]}.",
    tC="Complaints by month and by app version.",
    paretoNote=(f"<b>{len(contacted)} complaints ({pct(len(contacted) / nC)})</b> say they already contacted support, and {len(failed)} of them say support didn't fix it. "
                f"Weighted by who already called, the top three are {pct(top3c / len(contacted))} of contacts, and {LABEL[kc]} alone are {pct(contactedBy[kc] / len(contacted))}."),
    quotes=quotes,
    whys=[dict(driver=k, **WHYS[k]) for k in TOP if k in WHYS],
    fixes=[dict(driver=k, **FIXES[k]) for k in TOP if k in FIXES],
    plan30=[
        "Week 1: pull the last 90 days of support tickets and tag them with this codebook. Compare the ticket mix with this review mix.",
        "Week 2: put rupees on each driver from real data: contacts, refunds, compensation coupons and lost repeat bookings.",
        "Week 3: start the two pilots: confirm-or-reassign in 2 cities, and all-in prices for 10% of users.",
        "Week 4: first readout to you, and a weekly contacts-per-100-bookings view by driver.",
    ],
    northStarNote="It falls only if customers have fewer reasons to call, which is the point. Watch first-contact resolution next to it, so contacts aren't cut by making support harder to reach.",
    readout=dict(
        problem=[f"Customers who write reviews are mostly unhappy: {pct(oneStar / len(R))} of the {len(R)} most recent App Store reviews are 1★, against a {4.73}★ store average.",
                 f"{pct(top3)} of complaints come from three drivers: {LABEL[TOP[0]]} ({pct(share(TOP[0]))}), {LABEL[TOP[1]]} ({pct(share(TOP[1]))}) and {LABEL[TOP[2]]} ({pct(share(TOP[2]))}).",
                 f"{pct(len(contacted) / nC)} of complaints say they already contacted support, and the same three drivers are {pct(top3c / len(contacted))} of those; {LABEL[kc]} alone are {pct(contactedBy[kc] / len(contacted))}. {pct(len(churn) / nC)} say they will stop using the app."],
        root=[f"{WHYS[k]['root']}" for k in TOP if k in WHYS],
        impact=["At about 3.5 lakh bookings a month and an assumed 12 contacts per 100 bookings, that is about 42,000 contacts a month.",
                f"The top three drivers would be about {pct(top3)} of them, about {round(42000 * top3, -2):,.0f} a month. A 30% cut removes about {round(42000 * top3 * 0.3, -2):,.0f} contacts a month, or ₹{42000 * top3 * 0.3 * 45 * 12 / 1e5:.1f} L a year at ₹45 a contact.",
                f"The bigger prize is retention: if 1 in 10 customers behind those bad experiences would otherwise leave, keeping them is worth up to ₹{42000 * top3 * 0.3 * 0.1 * 12 * 5400 / 1e7:.1f} Cr a year at ₹5,400 a customer."],
        action=[f"{FIXES[k]['name']}: {FIXES[k]['metric'].lower()}, {FIXES[k]['target'].lower()}." for k in TOP if k in FIXES],
        caveat="Based on 500 public App Store reviews, which skew negative and towards iPhone users, and are not ticket data. Use them for the mix of problems; confirm the size with support tickets in week 1.",
    ),
    biases=[
        dict(what="Negativity.", effect=f"People write when upset: {pct(oneStar / len(R))} of written reviews are 1★, against a 4.73★ store average. Use the mix of problems, not the rate."),
        dict(what="iPhone only.", effect="App Store reviewers skew metro and higher income. Android is most of the base; a hand-copied Play Store sample would check the mix."),
        dict(what="Campaign spikes.", effect="One offer campaign can flood reviews for weeks. Check the month view before calling it structural."),
        dict(what="Not tickets.", effect="Most contacts never become reviews, and quick 'where is my professional' calls rarely do. The ticket mix will differ."),
        dict(what="Self-reported.", effect="Claims such as theft or injury are allegations, not verified facts. They are counted, not judged."),
    ],
    benchNotes=BENCH_NOTES,
    monthNote=MONTH_NOTE,
    freePedicure=FP,
    contactWeighted=dict(top3=top3c / len(contacted), lead=kc, leadShare=contactedBy[kc] / len(contacted)),
    versionNote=VERSION_NOTE,
    jd=[
        ["Root cause analysis", "Five whys on each top driver, with evidence vs hypothesis marked and a test that would prove each one wrong", "LVX: funnel analysis across ₹3.5 Cr, ₹7 Cr and ₹9 Cr+ launches; found where investors stalled; conversion up 20%"],
        ["Complaint reduction", "Three fixes with an owner, one metric, a target and a pilot design", "Techvaraha: 4 SOPs, QA workflows and KRAs; on-time delivery from 65% to 90%; zero missed deliverables for 3 quarters"],
        ["Lower contact rates", "Contacts per 100 bookings as the one metric; an impact model in contacts and rupees", "Techvaraha: escalation turnaround down 40% with one tracker and a review rhythm"],
        ["Crisp narrative", "Five slides, three minutes, and a one-page readout: problem, root cause, impact, action", "Techvaraha: 15+ executive presentations"],
        ["Leadership presentations", "A readout written for a VP decision, with the bias said out loud", "LVX: dashboards for the founder and management tracking ₹7 Cr+ of pipeline; reporting accuracy up 30%"],
        ["Clean, trustworthy data", "Two independent taggers, agreement and kappa measured, names and IDs removed", "LVX: reporting SOPs and data workflows; manual errors down 35%"],
        ["Supply-side ops", "No-show root cause traced to slot inventory vs confirmed capacity", "Built a network of 1,400+ healthcare practitioners and 15+ hospital tie-ups"],
    ],
)
json.dump(story, open(f"{BASE}/story.json", "w"), ensure_ascii=False, indent=1)
print("TOP", TOP, "top3 share", round(top3, 3), "order", order)
