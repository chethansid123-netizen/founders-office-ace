"""Build storyboard.jpg (12 labelled keyframes) and poster.jpg from the rendered MP4."""
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
mp4, outdir = sys.argv[1], sys.argv[2]
FRAMES = [
    (1.45, 'HOOK', 'Identity call-out over chat chaos'),
    (3.20, 'PAIN', '8 people · 8 riders · ₹4,000'),
    (3.66, 'WIPE', 'Sparkle wipe: logo as transition'),
    (5.10, 'REVEAL', 'Team Orders · teams of 2–10'),
    (6.40, 'STEP 1', 'Create · ₹300 cap · 30-min link'),
    (7.20, 'STEP 1', 'Link lands in the team chat'),
    (8.80, 'STEP 2', 'Everyone adds their own'),
    (10.35, 'STEP 3', 'One rider · one bill'),
    (10.90, 'PAYOFF', 'Stamp: ₹0 on your card'),
    (12.35, 'SLAM', 'One link · delivery · bill'),
    (12.95, 'CALLBACK', '₹0 on your card.'),
    (14.95, 'END CARD', 'Start a Team Order →'),
]
tmp = os.path.join(outdir, '_sb')
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
sheet = Image.new('RGB', (W, H), '#0B2E17')
d = ImageDraw.Draw(sheet)
d.text((pad, 26), 'Swish Team Orders · 15s ad · storyboard', font=ft, fill='#FFFFFF')
d.text((pad, 70), '1080×1920 · 60 fps · 128 BPM (1 bar = 1.875 s) · spec ad concept', font=fs, fill='#7CD79A')
for i, (t, tag, desc) in enumerate(FRAMES):
    png = os.path.join(tmp, f'{i:02d}.png')
    subprocess.run([FF, '-loglevel', 'error', '-y', '-ss', str(t), '-i', mp4, '-frames:v', '1', png], check=True)
    im = Image.open(png).convert('RGB')
    if i == len(FRAMES) - 1:
        im.save(os.path.join(outdir, 'poster.jpg'), quality=92)
    th = im.resize((TW, TH), Image.LANCZOS)
    c, r = i % cols, i // cols
    x = pad + c * (TW + pad); y = 110 + pad + r * (TH + lab + pad)
    sheet.paste(th, (x, y))
    d.rounded_rectangle((x, y + TH + 8, x + 118, y + TH + 38), 8, fill='#22B24C')
    d.text((x + 8, y + TH + 11), f'{t:05.2f}s', font=fb, fill='#FFFFFF')
    d.text((x + 128, y + TH + 11), tag, font=fb, fill='#FFD84D')
    d.text((x, y + TH + 44), desc, font=fr, fill='#E1E8E3')
sheet.save(os.path.join(outdir, 'storyboard.jpg'), quality=90)
for f in os.listdir(tmp):
    os.remove(os.path.join(tmp, f))
os.rmdir(tmp)
print('storyboard + poster written to', outdir)
