import json
from pptx import Presentation
from pptx.util import Emu

L = json.load(open("out/links.json"))
D = "/home/user/founders-office-ace/interview-demos/yourdost-submission/"
k = 12192000 / 1600
parts = {
    "Q1_Data_Analysis_and_Insights": range(3, 6),
    "Q2_10_Social_Media_Posts": range(6, 14),
    "Q3_Founders_Program_Pitch_Deck": range(14, 25),
}
for name, pages in parts.items():
    pr = Presentation()
    pr.slide_width = Emu(12192000)
    pr.slide_height = Emu(6858000)
    for n in pages:
        sl = pr.slides.add_slide(pr.slide_layouts[6])
        sl.shapes.add_picture(f"out/p{n:02d}.png", 0, 0, pr.slide_width, pr.slide_height)
        for l in L[n - 1]:
            sh = sl.shapes.add_shape(1, Emu(int(l["x"] * k)), Emu(int(l["y"] * k)), Emu(int(l["w"] * k)), Emu(int(l["h"] * k)))
            sh.fill.background()
            sh.line.fill.background()
            sh.click_action.hyperlink.address = l["u"]
    pr.save(D + name + ".pptx")
    print(name, len(pages))
