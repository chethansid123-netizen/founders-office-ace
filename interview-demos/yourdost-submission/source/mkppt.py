import json
from pptx import Presentation
from pptx.util import Emu

L = json.load(open("out/links.json"))
pr = Presentation()
pr.slide_width = Emu(12192000)
pr.slide_height = Emu(6858000)
k = 12192000 / 1600
for i in range(len(L)):
    sl = pr.slides.add_slide(pr.slide_layouts[6])
    sl.shapes.add_picture(f"out/p{i+1:02d}.png", 0, 0, pr.slide_width, pr.slide_height)
    for l in L[i]:
        sh = sl.shapes.add_shape(1, Emu(int(l["x"] * k)), Emu(int(l["y"] * k)), Emu(int(l["w"] * k)), Emu(int(l["h"] * k)))
        sh.fill.background()
        sh.line.fill.background()
        sh.click_action.hyperlink.address = l["u"]
pr.save("out/master.pptx")
print("pptx ok")
