"""Resize the images downloaded from kishlayfoods.com (and the site screenshots) into small WebP files.
Usage: python3 prep_assets.py <raw_img_dir> <shots_dir> <out_dir>"""
import sys, os
from PIL import Image
raw, shots, out = sys.argv[1:4]
J = os.path.join
spec = {  # name: (source path, max side px, quality)
 'logo': (J(raw,'logo.png'), 420, 90), 'nonstop': (J(raw,'partner1.png'), 360, 90),
 'facility': (J(raw,'facility.jpg'), 1600, 80), 'panda_packs': (J(raw,'kfhero.png'), 900, 82),
 'panda_popcorn': (J(raw,'home_about.png'), 800, 82), 'panda_parachute': (J(raw,'parachute.png'), 700, 82),
 'bus': (J(raw,'bus.png'), 1100, 80), 'stall': (J(raw,'g_wmnc2.jpg'), 1000, 78), 'expo': (J(raw,'g_wmnc1.jpg'), 1000, 78),
 'powerbi': (J(raw,'g_powerbi.jpeg'), 900, 78), 'award': (J(raw,'g_award.jpeg'), 900, 78), 'health': (J(raw,'g_health.jpeg'), 900, 78),
 'office': (J(raw,'g_office.png'), 900, 78), 'chilli': (J(raw,'hp_1756712860_3b9500c286d49e33.webp'), 400, 85),
 'chips_fly': (J(raw,'hp_1756887936_de7fc43d374e9015.png'), 420, 85), 'chips_bowl': (J(raw,'hp_1757048311_9455c97f27ee992a.png'), 420, 85),
 'cert_iso': (J(raw,'cert_iso.png'), 300, 90), 'cert_fssai': (J(raw,'cert_fssai.png'), 300, 90), 'cert_haccp': (J(raw,'cert_haccp.png'), 300, 90),
 'shot_desktop': (J(shots,'desktop_home.png'), 1440, 80), 'shot_mobile': (J(shots,'mobile_home.png'), 600, 80),
 'shot_products': (J(shots,'desktop_products.png'), 1440, 80), 'shot_about': (J(shots,'desktop_about.png'), 1440, 80),
}
for f in os.listdir(J(raw,'p')):
    n = os.path.splitext(f)[0]; spec['p_'+n] = (J(raw,'p',f), 440, 82)
tot = 0
for name,(src,mx,q) in spec.items():
    im = Image.open(src); im = im.convert('RGBA') if im.mode in ('RGBA','LA','P') else im.convert('RGB')
    im.thumbnail((mx,mx), Image.LANCZOS)
    dst = J(out, name+'.webp'); im.save(dst, 'WEBP', quality=q, method=6); tot += os.path.getsize(dst)
print(len(spec), 'assets,', round(tot/1e6,2), 'MB')
