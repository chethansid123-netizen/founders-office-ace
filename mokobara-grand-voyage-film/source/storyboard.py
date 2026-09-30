"""Build a storyboard (12 labelled keyframes) and poster from a rendered MP4.
usage: python3 storyboard.py video.mp4 outdir"""
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
mp4, outdir = sys.argv[1], sys.argv[2]
FRAMES = [
    (3.90, 'COLD OPEN', 'Departures board · two bags?'),
    (8.40, 'THE GAP', '24 L · 28 L · then nothing'),
    (12.90, 'HERO', 'The Grand Voyage on yellow'),
    (15.30, '01 MAIN', '26 L · zip opens to yellow'),
    (17.40, '02 SHOES', '6 L vented shoe bay'),
    (19.80, '03 LAPTOP', '16-inch suspended sleeve'),
    (22.20, '04 POCKETS', 'Wet + end pockets · 40/40 L'),
    (26.20, '06 RAIN', 'YKK AquaGuard · 1,500 mm'),
    (29.95, 'SPEC RUSH', 'Squeezes into the cabin box'),
    (37.60, 'LIFESTYLE', 'Anywhere-but-here · colours'),
    (40.20, 'PRICE', '₹9,499 · 3-year warranty'),
    (44.90, 'END CARD', 'Warm hugs, Mokobara')
]
SUFFIX = ''
tmp = os.path.join(outdir, '_sb' + SUFFIX)
os.makedirs(tmp, exist_ok=True)
fontdir = os.path.join(os.path.dirname(__file__), 'fonts')
# Pillow can't read woff2; fall back to DejaVu for labels
try:
    fb = ImageFont.truetype('DejaVuSans-Bold.ttf', 22); fr = ImageFont.truetype('DejaVuSans.ttf', 19)
    ft = ImageFont.truetype('DejaVuSans-Bold.ttf', 34); fs = ImageFont.truetype('DejaVuSans.ttf', 20)
except OSError:
    fb = fr = ft = fs = ImageFont.load_default()

TW, TH = 300, 533
cols, rows = 6, 2
pad, lab = 20, 76
W = cols * TW + (cols + 1) * pad
H = 110 + rows * (TH + lab) + (rows + 1) * pad
sheet = Image.new('RGB', (W, H), '#0A0A0A')
d = ImageDraw.Draw(sheet)
d.text((pad, 26), 'Mokobara · The Grand Voyage 40L · 45s film · storyboard', font=ft, fill='#FFFFFF')
d.text((pad, 70), '1080×1920 · 60 fps · 106.67 BPM (1 bar = 2.25 s) · spec concept', font=fs, fill='#FFD400')
for i, (t, tag, desc) in enumerate(FRAMES):
    png = os.path.join(tmp, f'{i:02d}.png')
    subprocess.run([FF, '-loglevel', 'error', '-y', '-ss', str(t), '-i', mp4, '-frames:v', '1', png], check=True)
    im = Image.open(png).convert('RGB')
    if i == len(FRAMES) - 1:
        im.save(os.path.join(outdir, f'poster{SUFFIX}.jpg'), quality=92)
    th = im.resize((TW, TH), Image.LANCZOS)
    c, r = i % cols, i // cols
    x = pad + c * (TW + pad); y = 110 + pad + r * (TH + lab + pad)
    sheet.paste(th, (x, y))
    d.rounded_rectangle((x, y + TH + 8, x + 118, y + TH + 38), 8, fill='#FFD400')
    d.text((x + 8, y + TH + 11), f'{t:05.2f}s', font=fb, fill='#0A0A0A')
    d.text((x + 128, y + TH + 11), tag, font=fb, fill='#F4F3EF')
    d.text((x, y + TH + 44), desc, font=fr, fill='#E1E8E3')
sheet.save(os.path.join(outdir, f'storyboard{SUFFIX}.jpg'), quality=90)
for f in os.listdir(tmp):
    os.remove(os.path.join(tmp, f))
os.rmdir(tmp)
print('storyboard + poster written to', outdir)
