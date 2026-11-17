"""Assemble the Slides deck files (project/deck.json, deck.css, slides/*.html) into one local HTML page
for previews, PDF and PPTX export. Usage: python3 build_local.py <deck_root> <assets_dir> <out.html> [--still]
--still drops animations so every element shows in its finished state."""
import sys, json, re, os
root, assets, out = sys.argv[1:4]; still = '--still' in sys.argv
here = os.path.dirname(os.path.abspath(__file__))
idx = json.load(open(os.path.join(root, 'project/deck.json')))
css = open(os.path.join(root, 'project/deck.css')).read()
bm = json.load(open(os.path.join(here, 'blob_map.json')))
def blob(m):
    n = bm[m.group(1)]
    ext = '.png' if os.path.exists(os.path.join(assets, n + '.png')) else '.webp'
    return 'file://' + os.path.abspath(os.path.join(assets, n + ext))
secs = []
for sid in idx['order']:
    fp = os.path.join(root, 'project/slides', sid + '.html')
    if not os.path.exists(fp): continue
    s = open(fp).read()
    s = re.sub(r'/_blob/([0-9a-f]{32})', blob, s)
    s = re.sub(r'<aside>.*?</aside>', '', s, flags=re.S)
    secs.append(s)
links = ''.join(f'<link rel="stylesheet" href="{f["href"]}">' for f in idx['faces'].values() if 'href' in f)
base = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#555}
section{position:relative;width:1920px;height:1080px;overflow:hidden;margin:0 auto 0}
x-shape,x-icon,x-connector{display:block}
x-shape[kind=ellipse]{border-radius:50%}
x-connector:not([x1]){height:0;border-top:3px solid currentColor;position:relative}
x-connector:not([x1])::after{content:"";position:absolute;right:-2px;top:-9px;border-left:12px solid currentColor;border-top:7.5px solid transparent;border-bottom:7.5px solid transparent}
h1,h2,h3,p{font-weight:inherit}
img{display:block}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #D9C6AC;padding:.35em .6em;text-align:left}th{font-weight:700}
@page{size:1920px 1080px;margin:0}
"""
if still: base += "*{animation:none!important}"
html = f'<!doctype html><html><head><meta charset="utf-8">{links}<style>{base}</style><style>{css}</style></head><body>{"".join(secs)}</body></html>'
open(out, 'w').write(html); print('wrote', out, len(secs), 'slides')
