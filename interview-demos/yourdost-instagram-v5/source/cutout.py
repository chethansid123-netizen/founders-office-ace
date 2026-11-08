"""Cut people/objects out of CC0 photos and give them a white sticker outline, like the reference posts.
    python3 cutout.py <photo_dir>"""
import sys
from PIL import Image, ImageFilter, ImageOps
from rembg import remove, new_session

SRC = sys.argv[1]
JOBS = [  # name, source, optional crop box as fractions (l, t, r, b)
    ("backpack", "wp2_student_6", None),
    ("student-walking", "wp2_student_4", None),
    ("phone-hands", "wp_phone_22", None),
]
session = new_session("isnet-general-use")
for name, src, box in JOBS:
    im = Image.open(f"{SRC}/{src}.jpg").convert("RGB")
    if box:
        w, h = im.size
        im = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    im.thumbnail((1600, 1600))
    cut = remove(im, session=session, post_process_mask=True)
    if name == "phone-hands":  # fill see-through holes (the screen) with a dark display
        m = cut.split()[3].point(lambda v: 255 if v > 128 else 0)
        outside = m.copy()
        from PIL import ImageDraw
        for corner in [(0, 0), (m.width - 1, 0), (0, m.height - 1), (m.width - 1, m.height - 1)]:
            if outside.getpixel(corner) == 0:
                ImageDraw.floodfill(outside, corner, 128)
        hole = outside.point(lambda v: 255 if v == 0 else 0).filter(ImageFilter.MaxFilter(5))
        dark = Image.new("RGBA", cut.size, (18, 18, 22, 255))
        cut.paste(dark, (0, 0), hole)
        # drop stray specks: morphological opening of the alpha
        al = cut.split()[3].filter(ImageFilter.MinFilter(15)).filter(ImageFilter.MaxFilter(15))
        cut.putalpha(Image.composite(cut.split()[3], Image.new("L", cut.size, 0), al.point(lambda v: 255 if v > 128 else 0)))
    a = cut.split()[3].point(lambda v: 255 if v > 128 else 0)
    bb = a.getbbox()
    pad = 40
    cut = cut.crop((max(0, bb[0] - pad), max(0, bb[1] - pad), min(cut.width, bb[2] + pad), min(cut.height, bb[3] + pad)))
    a = cut.split()[3].point(lambda v: 255 if v > 128 else 0)
    # white sticker border: dilate the mask, smooth it
    border = a
    for _ in range(3):
        border = border.filter(ImageFilter.MaxFilter(9))
    border = border.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 100 else 0)
    canvas = Image.new("RGBA", cut.size, (0, 0, 0, 0))
    white = Image.new("RGBA", cut.size, (255, 255, 255, 255))
    canvas.paste(white, (0, 0), border)
    canvas.alpha_composite(cut)
    canvas.save(f"cutouts/{name}.png")
    print(name, canvas.size)
