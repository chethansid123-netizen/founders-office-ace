"""Merge the tagging workflow output with the redacted reviews and compute the analysis.

Usage: python3 build_data.py <workflow-output.json> <story.json|-> <out data.json>
"""
import collections
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

DRIVERS = {
    "partner_cancellation": ("No-shows & cancellations", "No-shows", "The professional didn't turn up, cancelled late, or the company kept rescheduling or had no one to send"),
    "service_quality": ("Service quality & conduct", "Service quality", "Poor skill, rushed or incomplete work, hygiene, burns or rashes from technique, rude behaviour, safety"),
    "price_clarity": ("Price & offer clarity", "Price & offers", "Price or offer not as shown: extra charges at checkout, coupons or free-service offers that don't work"),
    "payment_refund": ("Payments & refunds", "Refunds", "Money taken or stuck: refund slow or refused, charged but not served, wallet or coupon money lost"),
    "support": ("Support itself", "Support", "Complaint is only about support: unreachable, scripted, slow, no escalation"),
    "app": ("App & booking bugs", "App", "App crashes or won't open, login, booking or checkout bugs, no slots, spam notifications"),
    "delay": ("Late arrivals", "Delays", "Professional arrived late, assignment took long, or the service overran"),
    "product_fit": ("Products used", "Products", "Product quality, missing or wrong products, pushed upsells, reactions blamed on the product"),
    "other": ("Other or vague", "Other", "A complaint with no specific problem, e.g. 'worst app', 'scam'"),
    "praise": ("Praise", "Praise", "Positive review with no complaint"),
}
SUBTAGS = {
    "late_arrival": "Arrived late", "slow_assignment": "Slow to assign a professional", "service_overran": "Service overran",
    "no_show": "Didn't show up", "last_minute_cancel": "Cancelled at the last minute", "repeated_reschedule": "Rescheduled again and again",
    "no_partner_available": "No professional available",
    "refund_delayed": "Refund delayed", "refund_denied": "Refund refused", "charged_not_served": "Charged, not served",
    "wallet_or_coupon_lost": "Wallet or coupon money lost", "payment_failed": "Payment failed",
    "hidden_charges": "Extra charges at checkout", "offer_not_honoured": "Offer or coupon not honoured",
    "price_mismatch": "Price different from shown", "membership_or_package_confusion": "Membership or package confusion",
    "poor_skill": "Poor skill", "rushed_or_incomplete": "Rushed or incomplete", "hygiene": "Hygiene",
    "skin_injury_or_reaction": "Burn, cut or rash", "rude_behaviour": "Rude behaviour", "safety_or_theft": "Safety, privacy or theft",
    "product_quality": "Product quality", "missing_or_wrong_products": "Missing or wrong products", "product_upsell": "Pushed product upsell",
    "product_reaction": "Reaction to a product",
    "unreachable": "Can't reach support", "unhelpful_or_scripted": "Scripted, unhelpful replies", "slow_resolution": "Slow resolution",
    "no_escalation": "No escalation",
    "crash_or_wont_open": "Crashes or won't open", "login_or_otp": "Login or OTP", "booking_or_checkout_bug": "Booking or checkout bug",
    "slots_unavailable": "No slots", "spam_notifications": "Spam notifications", "other_app": "Other app issue",
    "praise_professional": "Praised the professional", "praise_service": "Praised the service", "praise_value": "Praised the value",
    "other_issue": "Other issue", "unclear": "Too vague to classify",
}


def load_result(path):
    d = json.load(open(path))
    res = d.get("result", d)
    if isinstance(res, str):
        res = json.loads(res)
    return res


def kappa(a, b):
    n = len(a)
    agree = sum(1 for x, y in zip(a, b) if x == y)
    ca, cb = collections.Counter(a), collections.Counter(b)
    po = agree / n
    pe = sum(ca[k] / n * cb.get(k, 0) / n for k in ca)
    return po, (po - pe) / (1 - pe), agree


def main():
    res = load_result(sys.argv[1])
    story = json.load(open(sys.argv[2])) if sys.argv[2] != "-" else {}
    reviews = json.load(open(f"{BASE}/ym_reviews_redacted.json"))
    uc_rows = json.load(open(f"{BASE}/uc_reviews.json"))

    # Yes Madam: tagger A's record, with the adjudicated primary/subtag where A and B disagreed
    A, B, ADJ = {}, {}, {}
    for batch in res["ym"]:
        for x in batch["A"]:
            A[x["n"]] = x
        for x in batch["B"]:
            B[x["n"]] = x
        for x in batch["decisions"]:
            ADJ[x["n"]] = x
    missing = [r["n"] for r in reviews if r["n"] not in A]
    if missing:
        print("WARNING: no tags from tagger A for", missing[:20], "... falling back to B")
    pa, pb = [], []
    for r in reviews:
        n = r["n"]
        t = dict(A.get(n) or B.get(n))
        if n in A and n in B:
            pa.append(A[n]["primary"]); pb.append(B[n]["primary"])
            if A[n]["primary"] != B[n]["primary"]:
                if n in ADJ:
                    t["primary"], t["subtag"] = ADJ[n]["primary"], ADJ[n]["subtag"]
                    t["adjudicated"] = ADJ[n]["reason"]
        t["secondary"] = [s for s in t.get("secondary", []) if s != t["primary"] and s != "praise"]
        # keep the subtag consistent with the final primary
        r.update(primary=t["primary"], subtag=t["subtag"], secondary=t["secondary"], contacted=t["contacted_support"],
                 failed=t["support_failed"], severity=t["severity"], churn=bool(t["churn_signal"]), service=t["service"],
                 city=t["city"], amount=t["amount_inr"], quote=t["quote"], adjudicated=t.get("adjudicated", ""),
                 tagA=A[n]["primary"] if n in A else "", tagB=B[n]["primary"] if n in B else "")
    po, kap, agree = kappa(pa, pb)
    reliability = dict(n=len(pa), agree=agree, po=po, kappa=kap, adjudicated=sum(1 for r in reviews if r["adjudicated"]),
                       by_batch=[dict(b=b["b"], po=b["stats"]["po"], kappa=b["stats"]["kappa"]) for b in res["ym"] if b["stats"].get("n")])

    # Urban Company
    uc_tags = {}
    for batch in res["uc"]:
        for x in batch["reviews"]:
            uc_tags[x["n"]] = x
    ucc = [uc_tags[r["n"]] for r in uc_rows if r["n"] in uc_tags]
    uc_comp = [x for x in ucc if x["primary"] != "praise"]
    uc = dict(n=len(uc_rows), tagged=len(ucc), nC=len(uc_comp),
              byPrimary=dict(collections.Counter(x["primary"] for x in uc_comp)),
              contacted=sum(1 for x in uc_comp if x["contacted_support"] == "yes"),
              churn=sum(1 for x in uc_comp if x["churn_signal"]),
              high=sum(1 for x in uc_comp if x["severity"] == "high"),
              oneStar=sum(1 for r in uc_rows if r["rating"] == 1),
              subs=dict(collections.Counter(x["subtag"] for x in uc_comp)),
              **{"from": min(r["date"] for r in uc_rows), "to": max(r["date"] for r in uc_rows)})

    comp = [r for r in reviews if r["primary"] != "praise"]
    by = collections.Counter(r["primary"] for r in comp)
    ranked = [k for k, _ in by.most_common() if k != "other"]
    top3 = story.get("top3") or ranked[:3]
    churn_top3 = sum(1 for r in comp if r["primary"] in top3 and r["churn"]) / max(1, sum(1 for r in comp if r["primary"] in top3))

    meta = dict(app="Yes Madam", n=len(reviews), **{"from": min(r["date"] for r in reviews), "to": max(r["date"] for r in reviews)},
                store_avg=4.73, store_ratings=128866, fetched="2026-10-22",
                source_short="Apple App Store (India), public customer-reviews feed",
                source_long="Apple's public customer-reviews feed for the Yes Madam app, India storefront, sorted by most recent",
                playNote="Google Play has no public review feed, and copying it at scale breaks its terms. The Android version of this analysis is a hand-copied sample of 100–300 reviews in the same sheet.")
    impact = dict(defaults=dict(bookings=350000, contactRate=12, costPerContact=45, reduction=30, lostShare=10, annualValue=5400),
                  churnTop3=churn_top3)
    out = dict(meta=meta, drivers={k: dict(label=v[0], short=v[1], desc=v[2]) for k, v in DRIVERS.items()},
               subtags=SUBTAGS, reviews=[{k: r[k] for k in ("n", "date", "rating", "version", "title", "text", "primary", "subtag", "secondary",
                                                            "contacted", "failed", "severity", "churn", "service", "city", "amount", "quote")}
                                         for r in reviews],
               uc=uc, reliability=reliability, impact=impact, story=story)
    if story:
        json.dump(out, open(sys.argv[3], "w"), ensure_ascii=False, separators=(",", ":"))
        print("wrote", sys.argv[3])
    # always keep a full analysis copy (with adjudication notes) for review
    json.dump(dict(reviews=reviews, uc_tags=ucc, uc_rows=uc_rows, reliability=reliability, uc=uc), open(f"{BASE}/analysis_full.json", "w"), ensure_ascii=False, indent=0)

    # ---------- printed analysis ----------
    nC = len(comp)
    print(f"\nYES MADAM: {len(reviews)} reviews, {nC} complaints, {len(reviews) - nC} praise")
    print(f"reliability: {reliability['n']} double-tagged, agreement {po:.1%}, kappa {kap:.2f}, adjudicated {reliability['adjudicated']}")
    cum = 0
    for k, v in by.most_common():
        cum += v
        rs = [r for r in comp if r["primary"] == k]
        print(f"  {k:22s} {v:4d} {v / nC:6.1%} cum {cum / nC:6.1%} | contacted {sum(r['contacted'] == 'yes' for r in rs) / v:5.0%} "
              f"high {sum(r['severity'] == 'high' for r in rs) / v:5.0%} churn {sum(r['churn'] for r in rs) / v:5.0%} "
              f"1star {sum(r['rating'] == 1 for r in rs) / v:5.0%}")
        for s, c in collections.Counter(r["subtag"] for r in rs).most_common(6):
            print(f"        {s:28s} {c}")
    ment = collections.Counter(k for r in comp for k in set([r["primary"]] + r["secondary"]))
    print("mentions:", dict(ment.most_common()))
    print("contacted:", sum(r["contacted"] == "yes" for r in comp), "failed:", sum(r["failed"] == "yes" for r in comp),
          "churn:", sum(r["churn"] for r in comp), "high:", sum(r["severity"] == "high" for r in comp))
    print("services:", collections.Counter(r["service"] for r in comp).most_common())
    print("cities:", collections.Counter(r["city"] for r in comp if r["city"]).most_common(10))
    print("months x primary:")
    for m in sorted(set(r["date"][:7] for r in reviews)):
        print("  ", m, dict(collections.Counter(r["primary"] for r in comp if r["date"].startswith(m)).most_common()))
    print("versions app:", collections.Counter(r["version"] for r in comp if r["primary"] == "app").most_common())
    print(f"\nURBAN COMPANY: {uc['n']} reviews, tagged {uc['tagged']}, complaints {uc['nC']}")
    for k, v in sorted(uc["byPrimary"].items(), key=lambda x: -x[1]):
        print(f"  {k:22s} {v:4d} {v / uc['nC']:6.1%}   YM {by.get(k, 0) / nC:6.1%}")
    print("UC contacted", uc["contacted"], "churn", uc["churn"], "high", uc["high"])
    print("top3", top3, "churn among top3 complaints", f"{churn_top3:.1%}")


if __name__ == "__main__":
    main()
