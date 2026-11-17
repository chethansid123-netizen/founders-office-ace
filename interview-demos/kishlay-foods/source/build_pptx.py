"""Build a 16:9 PowerPoint from the slide PNGs, with each slide's speaker notes (the <aside> text).
Usage: python3 build_pptx.py <deck_root> <png_dir> <out.pptx> [links_json]
links_json (from get_links.cjs) adds an invisible clickable box over each link."""
import sys, os, re, json, html
from pptx import Presentation
from pptx.util import Emu
from PIL import Image
root, pngs, out = sys.argv[1:4]
links_json = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else None
from pptx.enum.shapes import MSO_SHAPE
PX = 12192000 / 1920
idx = json.load(open(os.path.join(root, 'project/deck.json')))
prs = Presentation(); prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
prs.core_properties.title = idx['title']; prs.core_properties.author = 'Chethan N'
blank = prs.slide_layouts[6]
for i, sid in enumerate(idx['order'], 1):
    src = os.path.join(pngs, f'slide-{i:02d}.png'); jpg = src[:-4] + '.jpg'
    Image.open(src).convert('RGB').save(jpg, 'JPEG', quality=90, optimize=True)
    s = prs.slides.add_slide(blank)
    s.shapes.add_picture(jpg, 0, 0, prs.slide_width, prs.slide_height)
    for L in (links_json[i - 1] if links_json and i - 1 < len(links_json) else []):
        box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(int(L['x'] * PX)), Emu(int(L['y'] * PX)), Emu(int(L['w'] * PX)), Emu(int(L['h'] * PX)))
        box.fill.background(); box.line.fill.background(); box.click_action.hyperlink.address = L['href']
    m = re.search(r'<aside>(.*?)</aside>', open(os.path.join(root, 'project/slides', sid + '.html')).read(), re.S)
    if m: s.notes_slide.notes_text_frame.text = html.unescape(m.group(1).strip())
prs.save(out); print('wrote', out, len(idx['order']), 'slides')
