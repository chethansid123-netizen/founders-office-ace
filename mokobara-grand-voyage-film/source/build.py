"""Build film.html from film.template.html: inject the round Mokobara wordmark (drawn as SVG text on a circle)."""
import re
h = open('film.template.html').read()
n = [0]
def rlogo(_):
    n[0] += 1; i = n[0]
    return (f'<svg class="rlogo" viewBox="0 0 200 200"><circle cx="100" cy="100" r="100" fill="#0A0A0A"/>'
            f'<path id="rl{i}" d="M100,100 m-64,0 a64,64 0 1,1 128,0 a64,64 0 1,1 -128,0" fill="none"/>'
            f'<text font-family="Outfit" font-weight="600" font-size="37" fill="#F4F3EF">'
            f'<textPath href="#rl{i}" textLength="398" lengthAdjust="spacing">mokobara mokobara </textPath></text></svg>')
h = re.sub(r'%%RLOGO%%', rlogo, h)
# make sure CSS background images are decoded before the first frame is captured
h = h.replace("window.ready=document.fonts.ready.then(()=>Promise.all([...document.images]",
  "const PRE=['img/couple.jpg','img/tile_trolley.jpg','img/tile_open1.jpg','img/tile_open2.jpg','img/tile_front.jpg','img/tile_top.jpg','img/tile_base.jpg','img/tile_detail.jpg'].map(u=>{const i=new Image();i.src=u;return i;});\n"
  "window.ready=document.fonts.ready.then(()=>Promise.all([...document.images,...PRE]")
h = h.replace("im.complete?1:new Promise(r=>{im.onload=r;im.onerror=r;})", "im.decode?im.decode().catch(()=>1):1")
open('film.html', 'w').write(h); print('built film.html', len(h))
