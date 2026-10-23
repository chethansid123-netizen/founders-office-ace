"""Turn Apple's public review RSS pages into one clean JSON file per app (reviewer names dropped)."""
import json, sys, collections
src, app, out = sys.argv[1], sys.argv[2], sys.argv[3]
rows, seen = [], set()
for p in range(1, 11):
    d = json.loads(open(f"{src}/rss_{app}_{p}.json").read().strip())
    ents = d.get("feed", {}).get("entry", [])
    if isinstance(ents, dict): ents = [ents]
    for e in ents:
        if "im:rating" not in e: continue
        rid = e["id"]["label"]
        if rid in seen: continue
        seen.add(rid)
        rows.append(dict(
            id=rid, date=e["updated"]["label"][:10], rating=int(e["im:rating"]["label"]),
            version=e.get("im:version", {}).get("label", ""), title=e["title"]["label"].strip(),
            text=e["content"]["label"].strip(), votes=int(e.get("im:voteCount", {}).get("label", "0") or 0),
        ))
rows.sort(key=lambda r: r["date"], reverse=True)
for i, r in enumerate(rows, 1): r["n"] = i
json.dump(rows, open(out, "w"), ensure_ascii=False, indent=0)
c = collections.Counter(r["rating"] for r in rows)
print(app, len(rows), "ratings", dict(sorted(c.items())), "avg %.2f" % (sum(r["rating"] for r in rows) / len(rows)),
      "avg words %.0f" % (sum(len((r["title"] + " " + r["text"]).split()) for r in rows) / len(rows)))
