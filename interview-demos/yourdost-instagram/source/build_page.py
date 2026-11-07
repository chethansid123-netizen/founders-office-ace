"""Assemble the showcase page into one offline HTML file (fonts, CSS and JS inlined).

    python3 build_page.py ../YourDOST-JoBolaNahi.html
"""
import base64
import json
import pathlib
import sys

here = pathlib.Path(__file__).parent
out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else here.parent / "YourDOST-JoBolaNahi.html")

faces = []
for f in json.loads((here / "fonts" / "fonts.json").read_text()):
    data = base64.b64encode((here / "fonts" / f["file"]).read_bytes()).decode()
    stretch = f"font-stretch:{f['stretch']};" if f["stretch"] else ""
    faces.append(
        f"@font-face{{font-family:'{f['family']}';font-style:normal;font-weight:{f['weight']};{stretch}"
        f"font-display:swap;src:url(data:font/woff2;base64,{data}) format('woff2');unicode-range:{f['range']};}}"
    )

html = (here / "template.html").read_text()
for key, value in {
    "/*FONTS*/": "\n".join(faces),
    "/*CREATIVES_CSS*/": (here / "creatives.css").read_text(),
    "/*PAGE_CSS*/": (here / "page.css").read_text(),
    "/*CREATIVES_JS*/": (here / "creatives.js").read_text(),
    "/*PAGE_JS*/": (here / "page.js").read_text(),
}.items():
    assert key in html, key
    html = html.replace(key, value)
out.write_text(html)
print(f"{out} {out.stat().st_size / 1024:.0f} KB")
