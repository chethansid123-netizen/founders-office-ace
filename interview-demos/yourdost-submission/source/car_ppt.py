from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

PX = 7620  # 1600 px = 12192000 EMU
D = "/home/user/founders-office-ace/interview-demos/yourdost-submission/"
L_PDF = "https://drive.google.com/file/d/1fdAX0xq4IsXEsd_6gkWUcVzFaL3BsHiu/view"
L_XLS = "https://docs.google.com/spreadsheets/d/19cCklmGSg7WdDTZ-N8hVO45dms6vo0o7KZ0LSueIHiE/edit?usp=sharing"
SETS = [("q1c", 5), ("c21", 6), ("c09", 6)]


def e(v):
    return Emu(int(v * PX))


def tile(sl, x, y, w, h, text, url, fill, fg, size):
    sh = sl.shapes.add_shape(1, e(x), e(y), e(w), e(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = RGBColor.from_string(fill)
    sh.line.fill.background()
    sh.click_action.hyperlink.address = url
    tf = sh.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.color.rgb = RGBColor.from_string(fg)


def link_tiles(sl, x, y, w, h, size):
    tile(sl, x, y, w, h / 2, "Click here: insights and the full analysis →", L_XLS, "F6D25A", "2F2663", size)
    tile(sl, x, y + h / 2, w, h / 2, "Open the carousel PDF →", L_PDF, "2F2663", "FFFFFF", size)


def build(name, W, H, fn):
    pr = Presentation()
    pr.slide_width = e(W)
    pr.slide_height = e(H)
    fn(pr, W, H)
    pr.save(D + name)


def strips(pr, W, H):
    cw, ch = 320, 400  # 4:5 cells, six across = 1920 px, no gaps
    for pref, n in SETS:
        sl = pr.slides.add_slide(pr.slide_layouts[6])
        for i in range(n):
            sl.shapes.add_picture(f"a/{pref}-{i+1}.jpg", e(i * cw), 0, e(cw), e(ch))
        if n == 5:
            link_tiles(sl, 5 * cw, 0, cw, ch, 15)


def grids(pr, W, H):
    cw, ch = 533.34, 666.67  # 3 across x 2 down = 1600 x 1333, no gaps
    for pref, n in SETS:
        sl = pr.slides.add_slide(pr.slide_layouts[6])
        for i in range(n):
            sl.shapes.add_picture(f"a/{pref}-{i+1}.jpg", e((i % 3) * cw), e((i // 3) * ch), e(cw), e(ch))
        if n == 5:
            link_tiles(sl, 2 * cw, ch, cw, ch, 22)


build("Carousels_A_One_Row_Full_Page.pptx", 1920, 400, strips)
build("Carousels_B_Large_3_Up_3_Down.pptx", 1600, 1333.34, grids)
print("ok")
