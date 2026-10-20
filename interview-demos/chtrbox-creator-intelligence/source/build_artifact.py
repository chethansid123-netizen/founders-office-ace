"""Turn the built offline page into an Artifact page: no document wrapper, theme follows the viewer."""
import re, sys

src = open(sys.argv[1]).read()
title = re.search(r"<title>.*?</title>", src, re.S).group(0)
style = re.search(r"<style>.*?</style>", src, re.S).group(0)
body = re.search(r"<body>(.*)</body>", src, re.S).group(1)
out = title + '\n<meta name="claude:viewport-fit-sides" content="cover">\n' + style + "\n" + body.strip() + "\n"
open(sys.argv[2], "w").write(out)
print("wrote", sys.argv[2], f"{len(out) / 1024:.0f} KB")
