import json, sys
tpl = open(sys.argv[1]).read()
data = json.load(open(sys.argv[2]))
out = tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":"), ensure_ascii=False))
open(sys.argv[3], "w").write(out)
print("wrote", sys.argv[3], len(out), "bytes")
