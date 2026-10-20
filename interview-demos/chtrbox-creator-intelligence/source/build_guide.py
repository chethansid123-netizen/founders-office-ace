"""Assemble the presenter's guide from guide/part*.html and render it to PDF in two passes
(the second pass fills real page numbers into the contents).

    G=$(npm root -g) python3 build_guide.py ../Creator-Intelligence-Engine-Presenter-Guide.pdf
"""
import glob, html, os, re, subprocess, sys
from pypdf import PdfReader

here = os.path.dirname(os.path.abspath(__file__))
out_pdf = os.path.abspath(sys.argv[1])
parts = sorted(glob.glob(os.path.join(here, "guide", "part*.html")), key=lambda p: int(re.search(r"part(\d+)", p).group(1)))
bodies = [open(p).read() for p in parts]


def text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


toc = []  # (part kicker, h1, [h2...])
for b in bodies:
    k = re.search(r'class="part-k">(.*?)<', b, re.S)
    h1 = re.search(r"<h1>(.*?)</h1>", b, re.S)
    h2s = [text(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", b, re.S)]
    toc.append((text(k.group(1)) if k else "", text(h1.group(1)) if h1 else "", h2s))

cover = """
<section class="cover">
  <div class="cv-top"><div class="cv-mark"><span>CI</span></div><div><div class="cv-n">Creator Intelligence Engine</div><div class="cv-s">Presenter's guide for the Chtrbox conversation</div></div></div>
  <div class="cv-mid">
    <div class="cv-k">Understand it · Explain it · Run it</div>
    <h1 class="cv-h">Everything you built,<br>and how to say it.</h1>
    <p class="cv-p">What the platform is, every number on every screen, how it was built, what to track, every brand from Amazon onward, and the exact words to use in the room.</p>
  </div>
  <div class="cv-grid">
    <div><b>Understand</b><span>Parts 1–3: the idea, every metric and formula, and every screen element.</span></div>
    <div><b>Every brand</b><span>Parts 4–7: Amazon in full, the five campaign brands, and all 35 brands by vertical.</span></div>
    <div><b>Run and explain</b><span>Parts 8–9: what to track, how to run it, scripts, Q&amp;A and a cheat sheet.</span></div>
  </div>
  <div class="cv-foot"><span>Chethan N · prepared 20 October 2026</span><span>Platform numbers are simulated. Public company figures are cited in the GTM plan.</span></div>
</section>"""


def toc_html(pages=None):
    rows = []
    for k, h1, h2s in toc:
        pg = (pages or {}).get(("h1", h1), "")
        sub = "".join(f'<div class="tc"><span>{html.escape(h)}</span><span class="pg">{(pages or {}).get(("h2", h), "")}</span></div>' for h in h2s)
        rows.append(f'<div class="tp"><div><span>{html.escape(k)} · {html.escape(h1)}</span><span class="pg">{pg}</span></div>{sub}</div>')
    how = ('<div class="how"><div><b>Tonight</b><span>Read Parts 1, 3 and 4, then the cheat sheet at the end of Part 9.</span></div>'
           '<div><b>Before the meeting</b><span>Rehearse the 8-minute talk track in Part 9 with the platform open.</span></div>'
           '<div><b>In the room</b><span>Keep Part 4 (Amazon) and the Q&amp;A bank in Part 9 at hand.</span></div></div>')
    return f'<section class="brk"><div class="sec-k">Contents</div><h1>How this guide is organised</h1>{how}<div class="gtoc">{"".join(rows)}</div></section>'


def build(pages=None):
    css = open(os.path.join(here, "plan.css")).read() + "\n" + open(os.path.join(here, "guide.css")).read()
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Creator Intelligence Engine · Presenter\'s guide</title>'
           f"<style>{css}</style></head><body>{cover}{toc_html(pages)}{''.join(bodies)}</body></html>")
    src = os.path.join(here, "guide.html")
    open(src, "w").write(doc)
    env = dict(os.environ)
    subprocess.run(["node", os.path.join(here, "render_pdf.mjs"), src, out_pdf], check=True, env=env, cwd=here)


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())


build()
reader = PdfReader(out_pdf)
page_text = [norm(p.extract_text() or "") for p in reader.pages]
pages, start = {}, 2
for k, h1, h2s in toc:
    key = norm(h1)[:40]
    for i in range(start, len(page_text)):
        if key and key in page_text[i]:
            pages[("h1", h1)] = i + 1; start = i; break
    for h in h2s:
        hk = norm(h)[:36]
        for i in range(start, len(page_text)):
            if hk and hk in page_text[i]:
                pages[("h2", h)] = i + 1; start = i; break
build(pages)
print("pages", len(PdfReader(out_pdf).pages), "· headings located", len(pages), "of", sum(1 + len(t[2]) for t in toc))
