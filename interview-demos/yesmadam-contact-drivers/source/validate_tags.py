"""Check a tagging file: python3 validate_tags.py <tags.json> <first_n> <last_n>"""
import json, sys
E = json.load(open(__file__.rsplit("/", 1)[0] + "/enums.json"))
d = json.load(open(sys.argv[1])); lo, hi = int(sys.argv[2]), int(sys.argv[3])
rs = d["reviews"]; errs = []
ns = [r.get("n") for r in rs]
missing = sorted(set(range(lo, hi + 1)) - set(ns)); dup = sorted({n for n in ns if ns.count(n) > 1})
if missing: errs.append(f"missing n: {missing}")
if dup: errs.append(f"duplicate n: {dup}")
REQ = ["n", "primary", "subtag", "secondary", "contacted_support", "support_failed", "severity", "churn_signal", "service", "city", "amount_inr", "quote"]
for r in rs:
    for k in REQ:
        if k not in r: errs.append(f"#{r.get('n')}: missing {k}")
    if r.get("primary") not in E["PRIMARY"]: errs.append(f"#{r['n']}: bad primary {r.get('primary')}")
    if r.get("subtag") not in E["SUBTAGS"]: errs.append(f"#{r['n']}: bad subtag {r.get('subtag')}")
    if any(s not in E["PRIMARY"] for s in r.get("secondary", [])): errs.append(f"#{r['n']}: bad secondary")
    if r.get("contacted_support") not in ("yes", "no") or r.get("support_failed") not in ("yes", "no"): errs.append(f"#{r['n']}: bad yes/no")
    if r.get("severity") not in ("none", "low", "medium", "high"): errs.append(f"#{r['n']}: bad severity")
    if not isinstance(r.get("churn_signal"), bool): errs.append(f"#{r['n']}: churn_signal not boolean")
    if r.get("service") not in E["SERVICES"]: errs.append(f"#{r['n']}: bad service {r.get('service')}")
    if not isinstance(r.get("amount_inr"), (int, float)): errs.append(f"#{r['n']}: amount_inr not a number")
print("OK" if not errs else "ERRORS:\n" + "\n".join(errs[:50]))
