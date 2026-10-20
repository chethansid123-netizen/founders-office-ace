"""Bundle template + CSS + JS + data + fonts into one offline HTML file.

    python3 build_html.py data.json fonts/ ../Creator-Intelligence-Engine.html

fonts/ holds the three woff2 files (Bricolage Grotesque, Geist, Geist Mono) from the
@fontsource-variable npm packages; they are embedded so the page looks the same offline.
"""
import base64, json, os, sys

here = os.path.dirname(os.path.abspath(__file__))
data_p, font_dir, out_p = sys.argv[1:4]
FACES = [  # family, file, weight range, unicode range
    ("Bricolage Grotesque", "bricolage-grotesque-latin-standard-normal.woff2", "200 800", None),
    ("Geist", "geist-latin-wght-normal.woff2", "100 900", None),
    ("Geist", "geist-latin-ext-wght-normal.woff2", "100 900", "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF"),
    ("Geist Mono", "geist-mono-latin-wght-normal.woff2", "100 900", None),
]
fonts = []
for fam, fn, wt, ur in FACES:
    b64 = base64.b64encode(open(os.path.join(font_dir, fn), "rb").read()).decode()
    fonts.append(f'@font-face{{font-family:"{fam}";font-style:normal;font-weight:{wt};font-display:swap;'
                 f'src:url(data:font/woff2;base64,{b64}) format("woff2");{"unicode-range:" + ur + ";" if ur else ""}}}')
tpl = open(os.path.join(here, "template.html")).read()
css = open(os.path.join(here, "styles.css")).read()
js = open(os.path.join(here, "app.js")).read()
data = json.dumps(json.load(open(data_p)), separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
out = (tpl.replace("/*__FONTS__*/", "\n".join(fonts))
          .replace("/*__CSS__*/", css)
          .replace("/*__DATA__*/null", data)
          .replace("/*__APP__*/", js))
open(out_p, "w").write(out)
print("wrote", out_p, f"{len(out) / 1024:.0f} KB")
