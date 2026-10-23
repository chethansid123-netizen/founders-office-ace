"""Fold the re-run pieces (batch 5 pass B, adjudications) into the tagging output.

Usage: python3 merge_final.py <workflow-output.json> <out tags_final.json>
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from build_data import kappa, load_result  # noqa: E402

res = load_result(sys.argv[1])
retry = f"{BASE}/retry"
b5 = f"{retry}/ym5_B.json"
adj = {}
for f in ("adjudication_1_4.json", "adjudication_5.json"):
    if os.path.exists(f"{retry}/{f}"):
        for d in json.load(open(f"{retry}/{f}"))["decisions"]:
            adj[d["n"]] = d
for batch in res["ym"]:
    if batch["b"] == 5 and not batch["B"] and os.path.exists(b5):
        batch["B"] = json.load(open(b5))["reviews"]
    bm = {x["n"]: x for x in batch["B"]}
    pairs = [(x, bm[x["n"]]) for x in batch["A"] if x["n"] in bm]
    if pairs:
        po, k, agree = kappa([a["primary"] for a, _ in pairs], [b["primary"] for _, b in pairs])
        batch["stats"] = dict(n=len(pairs), agree=agree, po=po, kappa=k)
    dis = [a["n"] for a, b in pairs if a["primary"] != b["primary"]]
    batch["decisions"] = [adj[n] for n in dis if n in adj]
    print(f"batch {batch['b']}: A {len(batch['A'])} B {len(batch['B'])} disagreements {dis} settled {len(batch['decisions'])}")
A, B = [], []
for batch in res["ym"]:
    bm = {x["n"]: x for x in batch["B"]}
    for x in batch["A"]:
        if x["n"] in bm:
            A.append(x["primary"]); B.append(bm[x["n"]]["primary"])
po, k, agree = kappa(A, B)
res["overall"] = dict(n=len(A), agree=agree, po=po, kappa=k)
print("overall", res["overall"])
json.dump(res, open(sys.argv[2], "w"), ensure_ascii=False)
