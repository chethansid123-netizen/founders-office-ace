"""Bundle template + CSS + JS + fonts into one offline HTML file, and an Artifact-ready copy.

    python3 build.py

Writes ../Revenue-Desk.html (open it in any browser, works offline, saves to that browser)
and ../artifact/revenue-desk.html (same page without the document wrapper, for publishing in Claude,
where leads are saved to the page's own database and the Claude, Gmail and Clay features switch on).
Fonts (Bricolage Grotesque, Geist, Geist Mono; SIL Open Font License) are reused from the Chtrbox demo.
"""
import base64, os, re

here = os.path.dirname(os.path.abspath(__file__))
font_dir = os.path.join(here, "..", "..", "chtrbox-creator-intelligence", "source", "fonts")
FACES = [
    ("Bricolage Grotesque", "bricolage-grotesque-latin-standard-normal.woff2", "200 800"),
    ("Geist", "geist-latin-wght-normal.woff2", "100 900"),
    ("Geist Mono", "geist-mono-latin-wght-normal.woff2", "100 900"),
]
fonts = []
for fam, fn, wt in FACES:
    b64 = base64.b64encode(open(os.path.join(font_dir, fn), "rb").read()).decode()
    fonts.append(f'@font-face{{font-family:"{fam}";font-style:normal;font-weight:{wt};font-display:swap;src:url(data:font/woff2;base64,{b64}) format("woff2")}}')
ORDER = ["d1_core.js", "d2_segments.js", "d3_playbook.js", "d4_market.js", "d5_accounts.js", "a1_core.js", "a2_ui.js", "a3_ops.js", "a4_views.js", "a5_views.js"]
js = "\n".join(open(os.path.join(here, f)).read() for f in ORDER).replace("</", "<\\/")
tpl = open(os.path.join(here, "template.html")).read()
css = open(os.path.join(here, "styles.css")).read()
out = tpl.replace("/*__FONTS__*/", "\n".join(fonts)).replace("/*__CSS__*/", css).replace("/*__APP__*/", js)
dst = os.path.join(here, "..", "Revenue-Desk.html")
open(dst, "w").write(out)
print("wrote", os.path.normpath(dst), f"{len(out) / 1024:.0f} KB")

title = re.search(r"<title>.*?</title>", out, re.S).group(0)
style = re.search(r"<style>.*?</style>", out, re.S).group(0)
body = re.search(r"<body>(.*)</body>", out, re.S).group(1)
art = title + '\n<meta name="claude:viewport-fit-sides" content="cover">\n' + style + "\n" + body.strip() + "\n"
os.makedirs(os.path.join(here, "..", "artifact"), exist_ok=True)
adst = os.path.join(here, "..", "artifact", "revenue-desk.html")
open(adst, "w").write(art)
print("wrote", os.path.normpath(adst), f"{len(art) / 1024:.0f} KB")
