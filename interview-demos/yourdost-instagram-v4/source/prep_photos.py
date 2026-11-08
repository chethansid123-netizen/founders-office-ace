"""Crop the chosen CC0 photos to Instagram sizes around a focal point.
    python3 prep_photos.py <src_dir>
Reel backgrounds: 1188 x 2112 (9:16 with ~10% room for slow zoom). Feed: 1080 x 1350 (4:5)."""
import sys
from PIL import Image, ImageFilter, ImageEnhance

SRC = sys.argv[1]
SPEC = [  # name, source file, kind, focal x, focal y
    ("diwali-doorstep", "diya_6", "reel", 0.55, 0.5), ("diwali-street", "wp_night_6", "reel", 0.5, 0.5),
    ("diwali-terrace", "diya_8", "reel", 0.38, 0.5), ("diwali-diya", "diya_7", "reel", 0.5, 0.5),
    ("rain-street", "wp_night_22", "reel", 0.5, 0.5), ("chai-hands", "wp_india_22", "reel", 0.5, 0.5),
    ("heater-laptop", "wp_laptop_4", "reel", 0.5, 0.5), ("keyboard-dark", "wp_laptop_10", "reel", 0.5, 0.5),
    ("sunrise-rain", "wp_rain_6", "reel", 0.6, 0.5), ("man-walking", "wp_person_11", "reel", 0.5, 0.5),
    ("dark-window", "wp_rain_10", "reel", 0.55, 0.5),
    ("notebook", "wp_study_0", "feed", 0.5, 0.5), ("sunrise-rain", "wp_rain_6", "feed", 0.6, 0.5),
    ("phone-hands", "wp_phone_22", "feed", 0.5, 0.5), ("rain-window", "wp_rain_0", "feed", 0.5, 0.45),
    ("two-by-river", "wp_friends_2", "feed", 0.45, 0.5), ("office-desk", "wp_office_11", "feed", 0.5, 0.5),
    ("keyboard-dark", "wp_laptop_10", "feed", 0.5, 0.5), ("office-night", "wp_office_20", "feed", 0.5, 0.5),
    ("two-chai", "wp_india_23", "feed", 0.4, 0.5),
    ("two-walking", "wp_friends_17", "feed", 0.5, 0.5), ("office-chai", "wp_laptop_13", "feed", 0.5, 0.5),
    # OpenArt people photos (free-plan watermark): preview versions only
    ("p-diwali-woman", "oa_diwali-woman", "reel", 0.5, 0.5), ("p-man-terrace", "oa_man-terrace", "reel", 0.5, 0.5),
    ("p-chai-friends", "oa_chai-friends", "reel", 0.5, 0.5), ("p-student-night", "oa_student-night", "feed", 0.5, 0.5),
    ("p-laptop-woman", "oa_laptop-woman", "feed", 0.5, 0.5), ("p-couple", "oa_couple", "feed", 0.5, 0.5),
]
for name, src, kind, fx, fy in SPEC:
    im = Image.open(f"{SRC}/{src}.jpg").convert("RGB")
    W, H = (1188, 2112) if kind == "reel" else (1080, 1350)
    r = W / H
    w, h = im.size
    if w / h > r:
        cw, ch = int(h * r), h
    else:
        cw, ch = w, int(w / r)
    x = int(min(max(fx * w - cw / 2, 0), w - cw))
    y = int(min(max(fy * h - ch / 2, 0), h - ch))
    out = im.crop((x, y, x + cw, y + ch)).resize((W, H), Image.LANCZOS)
    if cw < W:  # upscaled: a light sharpen keeps it crisp
        out = out.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
    out.save(f"photos/{kind}-{name}.jpg", quality=90)
    print(kind, name, (cw, ch), "->", (W, H), "upscale x%.2f" % (W / cw))
