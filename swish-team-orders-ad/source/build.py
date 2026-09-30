import re
paths=open('logo_paths.txt').read().split('\n')
spark=paths[5]; word=[p for i,p in enumerate(paths) if i!=5]
W,H=1592,525
def xform(d,f):
    toks=re.findall(r'[MLCZ]|-?\d+\.?\d*',d); out=[];nums=[]
    res=[];i=0;
    # coordinates come in x,y pairs after commands
    pair=[]
    for tk in toks:
        if tk in 'MLCZ': res.append(tk); continue
        pair.append(float(tk))
        if len(pair)==2:
            x,y=f(*pair); res.append(f"{x:.4f},{y:.4f}"); pair=[]
    s=''
    for r in res:
        s+= r if r in 'MLCZ' else r+' '
    return s
star=xform(spark,lambda x,y:((x-91)/100,(y-136)/100))
def logo(cls):
    return (f'<svg viewBox="-10 0 {W+10} {H}" xmlns="http://www.w3.org/2000/svg">'
            f'<path fill="#fff" fill-rule="evenodd" d="{" ".join(word)}"/>'
            f'<g class="spark" style="transform-origin:91px 136px;transform-box:view-box"><path fill="#fff" d="{spark}"/></g></svg>')
def sparkicon(color,size):
    return (f'<svg width="{size}" height="{size}" viewBox="-5 36 192 200" xmlns="http://www.w3.org/2000/svg" style="display:block">'
            f'<path fill="{"#fff" if color=="white" else color}" d="{spark}"/></svg>')
h=open('ad.template.html').read()
h=h.replace('%%LOGO:s3%%',logo('s3')).replace('%%LOGO:end%%',logo('end'))
h=re.sub(r'%%SPARK:(\w+):(\d+)%%',lambda m:sparkicon(m.group(1),m.group(2)),h)
h=h.replace('%%STAR%%',star)
h=h.replace('%%BAGS%%',''.join('<span class="emoji">🛍️</span>' for _ in range(5)))
h=h.replace('%%SCOOTERS%%',''.join('<span class="emoji">🛵</span>' for _ in range(5)))
h=h.replace('%%TITLECHARS%%',''.join(f'<span class="ch">{"&nbsp;" if c==" " else c}</span>' for c in 'Team Orders'))
open('ad.html','w').write(h); print('built', len(h))
