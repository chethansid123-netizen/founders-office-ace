F="/home/user/founders-office-ace/interview-demos/yourdost-v7-fonts"
F="/home/user/founders-office-ace/interview-demos/yourdost-instagram-v7/source/fonts"
L_PDF="https://drive.google.com/file/d/1fdAX0xq4IsXEsd_6gkWUcVzFaL3BsHiu/view"
L_XLS="https://docs.google.com/spreadsheets/d/19cCklmGSg7WdDTZ-N8hVO45dms6vo0o7KZ0LSueIHiE/edit?usp=sharing"
V=[("r13.jpg","https://docs.google.com/videos/d/1X7mYAwXry4u6OZVEiVKrVM8dtrdsNfOMqY6UUVfA4HA/edit?usp=sharing"),
("r01.jpg","https://drive.google.com/file/d/1heVWxzfSNEvvBRc31-E-TxypCmTCt3dg/view"),
("m24.jpg","https://drive.google.com/file/d/1pflH55FVr_DStO67PVk0TRZ0Oi3PYTty/view"),
("m26.jpg","https://drive.google.com/file/d/1Mo6cVIluIbiok0jl_yrgdEThKIuxTkeA/view")]
P=[]
LOGO='<img class="logo" src="a/badge.png">'
def pg(cls,body,tag=""): P.append(f'<section class="pg {cls}">{LOGO}{f"<div class=tag>{tag}</div>" if tag else ""}{body}</section>')
def big(url,txt,cls="y"): return f'<a class="bigbtn {cls}" href="{url}">{txt} <i>→</i></a>'
im=lambda f,c="":f'<img class="{c}" src="a/{f}">'

pg("txt",f'''<h1>Three questions, one document.</h1>
<p class="lead">Everything I built is on the next pages, with the images side by side. Files for each question are also attached separately.</p>
<div class="cards"><div class="card c1"><span class="q">Q1</span><h3>Data analysis and insights</h3><em>Infographic · 5-slide carousel · analysis workbook</em></div>
<div class="card c2"><span class="q">Q2</span><h3>10 social media posts</h3><p>Original posts for emotional wellness across 4 videos, 2 carousels and 4 single images, aimed at corporates, students and professionals.</p></div>
<div class="card c3"><span class="q">Q3</span><h3>Founders Program pitch deck</h3><em>Price · market size · unit economics</em></div></div>''',"SUBMISSION · 3 ASSIGNMENTS")
rows=[("Q1","Infographic + 5-slide carousel + workbook","Pages 3 to 5","Q1_Infographic_and_Carousel.pdf · Q1_Insights_Workbook.xlsx",f'<a href="{L_PDF}">Carousel online</a> · <a href="{L_XLS}">Workbook online</a>'),
("Q2","10 social media posts: 4 videos, 2 carousels, 4 images","Pages 6 to 13","Q2_All_10_Posts.zip","Video links on page 7"),
("Q3","Founders Program pitch deck","Pages 14 to 24","Q3_Founders_Program_Pitch_Deck.pptx","In the attached file")]
tr="".join(f"<tr><td class=qq>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a,b,c,d,e in rows)
pg("txt",f'<h1>Where to find everything</h1><table><tr><th></th><th>What it is</th><th>See in this PDF</th><th>Separate file in the upload</th><th>Online (opens without sign-in)</th></tr>{tr}</table>',"HOW THIS DOCUMENT IS ORGANISED")
# Q1
pg("split",f'''<div class="left"><h1>Parents fear gaming more than they understand it</h1>
{big(L_XLS,"Click here to get the insights and the full analysis")}{big(L_PDF,"Open the 5-slide carousel PDF","p")}</div>
<div class="right">{im("info.jpg","info")}</div>''',"Q1 · DATA ANALYSIS AND INSIGHTS")
def strip(n, pref, tag, links=True):
    parts = [(1, 3), (4, n)]
    for pi, (lo, hi) in enumerate(parts, 1):
        cells = "".join(f'<div class="cell">{im(f"{pref}-{i}.jpg")}</div>' for i in range(lo, hi + 1))
        if links and hi < lo + 2:
            cells += f'<div class="cell tiles"><a class="t1" href="{L_XLS}">Click here: insights and the full analysis →</a><a class="t2" href="{L_PDF}">Open the carousel PDF →</a></div>'
        P.append(f'<section class="pg car3"><div class="band"><span class="bt">{tag}</span><span class="bn">{pi} / 2</span><img class="lg" src="a/badge.png"></div><div class="cells">{cells}</div></section>')
strip(5, "q1c", "Parents · Online gaming")
# Q2
pg("txt",f'''<h1>10 social media posts</h1>
<p class="lead">YourDOST is a confidential expert who is as easy to reach as a friend, by chat, call or video, 24/7.</p>
<div class="cols2"><div class="box"><h4>Formats</h4><p>4 videos, 2 carousels, 4 single images.</p></div><div class="box"><h4>Audiences</h4><p>Corporate buyers (HR, managers, employees), students, young professionals, high achievers, and anyone marking Diwali or a hard week.</p></div></div>
<table class="lst"><tr><td>1 Reel · students</td><td>2 Reel · Diwali</td><td>3 Reel · corporate teams</td><td>4 Reel · high achievers</td><td>5 Carousel · corporate</td></tr><tr><td>6 Carousel · employees</td><td>7 Image · HR leaders</td><td>8 Image · professionals</td><td>9 Image · young adults</td><td>10 Image · stress and smoking</td></tr></table>''',"Q2 · SOCIAL MEDIA POSTS")
vs="".join(f'<a class="v" href="{u}">{im(c)}<span class="play">▶ Watch the reel</span></a>' for c,u in V)
pg("vids",f'<div class="vrow">{vs}</div>',"Q2 · THE VIDEOS · TAP A REEL TO WATCH")
strip(6,"c21","Corporate managers, HR, CHROs",False)
strip(6,"c09","Employees",False)
for a,b,n in (("s18.jpg","s03.jpg","1 OF 2"),("s-breakup.jpg","s-smoke.jpg","2 OF 2")): pg("pair",f'<div class="prow">{im(a)}{im(b)}</div>',f"Q2 · SINGLE IMAGES · {n}")
# Q3
pg("title",'<div class="mid"><small>ASSIGNMENT 3</small><h1>Founders Program</h1><h2>The pitch deck</h2></div>')
for i in range(1,11): P.append(f'<section class="pg full"><img src="a/d{i}.jpg"></section>')
css=f'''
.pg.car3{{padding:0}} .band{{height:245px;background:#F6D25A;display:flex;align-items:center;gap:26px;padding:0 40px 0 56px}} .bt{{font-size:52px;font-weight:600;color:#2F2663;line-height:1.1}} .bn{{font-size:28px;font-weight:500;color:#2F2663;opacity:.7}} .band .lg{{margin-left:auto;width:120px;height:120px;border-radius:50%}}
.cells{{display:flex;gap:14px;height:655px;background:#FDFCF7}} .cell{{width:524px;height:655px;flex:none}} .cell img{{width:100%;height:100%;display:block}}
.tiles{{display:flex;flex-direction:column}} .tiles a{{flex:1;display:flex;align-items:center;justify-content:center;text-align:center;padding:30px;font-size:34px;font-weight:600;text-decoration:none;line-height:1.3}} .t1{{background:#E1CBF9;color:#2F2663}} .t2{{background:#2F2663;color:#fff}}






@font-face{{font-family:Poppins;font-weight:400;src:url(file://{F}/Poppins-400.woff2)}}
@font-face{{font-family:Poppins;font-weight:500;src:url(file://{F}/Poppins-500.woff2)}}
@font-face{{font-family:Poppins;font-weight:600;src:url(file://{F}/Poppins-600.woff2)}}
@page{{size:1600px 900px;margin:0}} *{{box-sizing:border-box;margin:0}} body{{font-family:Poppins,sans-serif;color:#0D1015;background:#FDFCF7}}
.pg{{width:1600px;height:900px;position:relative;background:#FDFCF7;page-break-after:always;overflow:hidden;padding:100px 60px 30px}}
.logo{{position:absolute;right:34px;top:18px;width:68px;height:68px;border-radius:50%;z-index:5}} .tag{{position:absolute;left:60px;top:34px;font-size:14px;letter-spacing:.14em;font-weight:600;color:#8a6a00}}
h1{{font-size:44px;line-height:1.18;font-weight:600;color:#2F2663}} .lead{{font-size:22px;line-height:1.5;margin:18px 0 24px;max-width:1300px}} .lead2{{font-size:19px;line-height:1.5;margin-top:16px;color:#333}}
.txt{{padding:110px 80px}} p{{font-size:18px;line-height:1.55}} a{{color:#5B4A9C;font-weight:500}}
.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:30px}} .card{{border-radius:26px;padding:30px;min-height:420px;position:relative}} .c1{{background:#E1CBF9}} .c2{{background:#F6D25A}} .c3{{background:#FFE4D1}}
.card .q{{font-size:56px;font-weight:600;color:#2F2663}} .card h3{{font-size:28px;margin:6px 0 14px;color:#2F2663}} .card em{{position:absolute;left:30px;bottom:26px;font-size:16px;color:#4a3d80}}
table{{border-collapse:collapse;width:100%;font-size:17px;margin-top:20px}} th{{text-align:left;color:#8a6a00;font-size:13px;letter-spacing:.1em;padding:10px 14px;border-bottom:2px solid #F6D25A}} td{{padding:22px 14px;border-bottom:1px solid #e7e0f2;vertical-align:top;line-height:1.45}} .qq{{font-size:34px;font-weight:600;color:#2F2663}}
.split{{display:flex;gap:40px;padding-top:100px}} .left{{width:500px;flex:none}} .right{{flex:1}}
.bigbtn{{display:block;margin-top:26px;border-radius:22px;padding:26px 28px;font-size:24px;line-height:1.3;font-weight:600;text-decoration:none;color:#2F2663;box-shadow:0 6px 18px rgba(47,38,99,.2)}} .bigbtn i{{font-style:normal;float:right;margin-left:10px}} .bigbtn.y{{background:#F6D25A}} .bigbtn.p{{background:#2F2663;color:#fff}}
.info{{height:760px;border-radius:14px;box-shadow:0 8px 30px rgba(47,38,99,.2);display:block;margin:0 auto}}
.grid{{display:grid;grid-template-columns:repeat(3,304px);gap:14px;justify-content:start;align-content:start}} .s img{{width:304px;display:block;border-radius:8px;box-shadow:0 4px 14px rgba(47,38,99,.2)}}
.cols2{{display:grid;grid-template-columns:1fr 1.4fr;gap:26px;margin:10px 0 26px}} .box{{background:#fff;border:2px solid #E1CBF9;border-radius:22px;padding:24px 28px}} h4{{font-size:19px;color:#2F2663;margin-bottom:10px}}
.lst td{{font-size:16px;padding:16px 12px;background:#fff;border:2px solid #E1CBF9}}
.vids{{padding:104px 30px 20px}} .vrow{{display:flex;gap:24px;justify-content:center}} .v{{position:relative;display:block;width:368px;height:654px}} .v img{{width:100%;height:100%;object-fit:cover;border-radius:16px;box-shadow:0 8px 26px rgba(47,38,99,.28)}}
.play{{position:absolute;left:50%;bottom:26px;transform:translateX(-50%);background:#F6D25A;color:#2F2663;font-weight:600;font-size:21px;padding:13px 26px;border-radius:40px;white-space:nowrap;box-shadow:0 4px 14px rgba(0,0,0,.35)}}
.pair{{padding:100px 30px 20px}} .prow{{display:flex;gap:40px;justify-content:center}} .prow img{{height:760px;border-radius:14px;box-shadow:0 8px 26px rgba(47,38,99,.25)}}
.full{{padding:0}} .full img{{width:1600px;height:900px;display:block}}
.title{{background:#F6D25A}} .mid{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}} .mid small{{letter-spacing:.2em;font-weight:600;font-size:18px;color:#2F2663}} .mid h1{{font-size:96px;margin-top:10px}} .mid h2{{font-size:40px;font-weight:500;color:#2F2663;margin-top:6px}}
'''
open("master.html","w").write(f'<!doctype html><meta charset=utf-8><title>Chethan N · YourDOST EIR submission</title><style>{css}</style>'+"".join(P))
print(len(P))
