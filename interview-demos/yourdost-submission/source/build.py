import html
F="/home/user/founders-office-ace/interview-demos/yourdost-instagram-v7/source/fonts"
L_PDF="https://drive.google.com/file/d/1fdAX0xq4IsXEsd_6gkWUcVzFaL3BsHiu/view"
L_XLS="https://docs.google.com/spreadsheets/d/19cCklmGSg7WdDTZ-N8hVO45dms6vo0o7KZ0LSueIHiE/edit?usp=sharing"
L_R1="https://docs.google.com/videos/d/1X7mYAwXry4u6OZVEiVKrVM8dtrdsNfOMqY6UUVfA4HA/edit?usp=sharing"
L_M1="https://drive.google.com/file/d/1pflH55FVr_DStO67PVk0TRZ0Oi3PYTty/view"
L_M11="https://drive.google.com/file/d/1Mo6cVIluIbiok0jl_yrgdEThKIuxTkeA/view"
L_RD="https://drive.google.com/file/d/1heVWxzfSNEvvBRc31-E-TxypCmTCt3dg/view"
pages=[]
def page(tag,title,body,sub=""):
    pages.append(f'''<section class="pg"><header><div class="tag">{tag}</div><img class="logo" src="a/badge.png"></header>
<h1>{title}</h1>{f'<p class="sub">{sub}</p>' if sub else ''}<div class="body">{body}</div><footer><span>Chethan N · YourDOST EIR assignment</span><span class="pn"></span></footer></section>''')
def img(f,cls="",link=None):
    t=f'<img class="{cls}" src="a/{f}">'
    return f'<a href="{link}">{t}</a>' if link else t
def video(f,title,seg,link,label):
    lk=f'<a class="btn" href="{link}">▶ Watch · {label}</a>' if link else f'<span class="btn off">▶ In the Q2 videos file</span>'
    return f'<div class="vid">{img(f,"cov",link)}<b>{title}</b><span>{seg}</span>{lk}</div>'

# 1 cover
page("SUBMISSION · 3 ASSIGNMENTS","Three questions, one document.",f'''
<p class="lead">Everything I built is on the next pages, with the images side by side. You never need to click away to see my work. Files for each question are also attached separately.</p>
<div class="cards">
<div class="card c1"><span class="q">Q1</span><h3>Data analysis and insights</h3><p>Parents fear online gaming more than they understand it. More rules did not mean fewer fights. Curiosity did.</p><em>Infographic · 5-slide carousel · analysis workbook</em></div>
<div class="card c2"><span class="q">Q2</span><h3>10 Instagram posts</h3><p>Original posts for emotional wellness across 5 videos, 2 carousels and 3 single images, aimed at corporates, students and professionals.</p><em>All 10 shown inside, with hook and audience</em></div>
<div class="card c3"><span class="q">Q3</span><h3>Founders Program pitch deck</h3><p>A 10-slide deck for VCs and incubators. The founder pays ₹6,000 to ₹12,000 a program, the fund pays ₹0, and the ask is one introduction.</p><em>Price, market size, unit economics, plan</em></div>
</div>''')

# 2 map
rows=[("Q1","Infographic + 5-slide carousel + workbook","Pages 3 to 5","Q1_Infographic_and_Carousel.pdf · Q1_Insights_Workbook.xlsx",f'<a href="{L_PDF}">Carousel online</a> · <a href="{L_XLS}">Workbook online</a>'),
("Q2","10 posts: 5 videos, 2 carousels, 3 images","Pages 6 to 9","Q2_All_10_Posts.zip (5 videos + the images)",'Video links on page 7'),
("Q3","10-slide pitch deck","Pages 10 to 13","Q3_Founders_Program_Pitch_Deck.pptx","In the attached file")]
tr="".join(f"<tr><td class=qq>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a,b,c,d,e in rows)
page("HOW TO READ THIS","Where to find everything",f'''
<table><tr><th></th><th>What it is</th><th>See in this PDF</th><th>Separate file in the upload</th><th>Online (opens without sign-in)</th></tr>{tr}</table>
<div class="note"><b>Reading tip:</b> every page is one idea. The images are the real files, not mock-ups, and the reels and motion posts show their cover with a play link. Each carousel is laid out as a strip so you can read it left to right.</div>''')

# Q1
page("Q1 · DATA ANALYSIS AND INSIGHTS","Parents fear gaming more than they understand it",f'''
<div class="two"><div>
<p class="lead">The survey: 100 parents, 1 to 3 Dec 2020. One duplicate removed, which leaves 99. Of those, 66 said their kids play online games and answered the full form. Every percentage below is out of those 66.</p>
<div class="stats"><div class="st y"><b>94%</b><span>worry their child could get hooked</span></div><div class="st l"><b>6 in 10</b><span>feel frustration at home (64%)</span></div><div class="st p"><b>1 in 2</b><span>feel strain in their bond (55%)</span></div></div>
<p>Other big worries: grades <b>91%</b>, unsuitable content <b>88%</b>, health <b>83%</b>, aggressive behaviour <b>79%</b>. Aggression ranks last, so YourDOST should lead with addiction and study time, not violence.</p></div>
<div class="box"><h4>The two findings that are not obvious</h4>
<p><b>1. The loop.</b> Worry and conflict at home rise together (Spearman ρ ≈ 0.58, the strongest link in the data). The number of rules a family sets does not (ρ ≈ 0.06). Control is not the fix.</p>
<p><b>2. The way out.</b> Where parents understand why their child plays, 48% feel strain with the child. Where they do not, 79% do.</p>
<p class="small">How: frequency tables, Spearman, Mann-Whitney U, Kruskal-Wallis and 7 chi-square tests in Numiqo, α = 0.05. These are associations, not causes, and the sample is small. The infographic says so.</p></div></div>''',
"The one-line answer: curiosity, not more rules, is what eased the strain.")
page("Q1 · THE SOCIAL-MEDIA-READY INFOGRAPHIC","One image that tells the whole story",f'''
<div class="two nar"><div class="center">{img("info.jpg","tall")}</div><div>
<h4>Why it is built this way</h4>
<ul><li><b>Starts where parents are.</b> “Just 5 more minutes!” makes any parent say “that’s me” before a number appears.</li>
<li><b>Three numbers, three feelings:</b> worry, frustration, strain. It moves gaming from a screen-time topic to a family wellness topic, which is YourDOST’s space.</li>
<li><b>Calm, not scary.</b> Fear goes with conflict at home, so a scary campaign could feed the problem. It names the worry, normalises it and gives one small action.</li>
<li><b>Ends with a kind task.</b> “Try this tonight, just for 10 minutes” with three questions to ask, then “Talk to a YourDOST expert”.</li>
<li><b>Honest.</b> The source line, base of 66 and “associations, not cause” are printed on the image.</li></ul>
<p class="small">Same palette as yourdost.com: deep indigo, lavender and yellow. 1080 × 1350, ready for Instagram, LinkedIn and WhatsApp.</p></div></div>''')
page("Q1 · THE SAME STORY AS A 5-SLIDE CAROUSEL","Swipe version for Instagram",
 '<div class="strip">'+"".join(f'<div class="fr">{img(f"q1c-{i}.jpg")}<span>{i}/5</span></div>' for i in range(1,6))+f'</div><p class="small">Hook, feelings, other worries, the loop and the way out, then the action. Open online: <a href="{L_PDF}">carousel PDF</a> · <a href="{L_XLS}">analysis workbook (every number traced to the survey rows)</a>.</p><div class="cols3"><div class="box"><h4>Lead with the feeling</h4><p>Each slide says how it feels first, then gives the number. Parents see themselves before they see a statistic.</p></div><div class="box"><h4>Calm, then one small action</h4><p>No alarm. Name the worry, normalise it, then offer a 10-minute task for tonight.</p></div><div class="box"><h4>Two formats, one story</h4><p>The infographic works as a single share on LinkedIn and parent groups. The carousel gives Instagram a swipe-and-save version.</p></div></div>')

# Q2
page("Q2 · INSTAGRAM POSTS","10 original posts, one positioning line",f'''
<p class="lead">Short format, one or two lines per post. The line behind all ten: <b>YourDOST is a confidential expert who is as easy to reach as a friend, by chat, call or video, 24/7.</b></p>
<div class="cols3"><div class="box"><h4>Formats</h4><p>5 videos (3 reels, 2 motion posts with voices), 2 carousels, 3 single images. Every slide carries the logo badge.</p></div>
<div class="box"><h4>Audiences</h4><p>Corporate buyers (HR, managers, employees), students, young professionals, high achievers, and anyone marking Diwali or a hard week.</p></div>
<div class="box"><h4>Engagement</h4><p>Each post ends on something to do: send it to a colleague, tag someone, save it, or answer a question in the comments.</p></div></div>
<table class="lst"><tr><td>1 Reel · students</td><td>2 Reel · Diwali</td><td>3 Motion · corporate teams</td><td>4 Motion · high achievers</td><td>5 Motion · young professionals</td></tr><tr><td>6 Carousel · corporate</td><td>7 Carousel · employees</td><td>8 Image · HR leaders</td><td>9 Image · professionals</td><td>10 Image · young adults</td></tr></table>
<p class="small" style="margin-top:14px">Two originals use a format I have not seen in this category: <b>inner captions</b> (a video call whose captions show what people think) and a <b>museum wall label</b> for a painting of “I’m fine”.</p>''')
page("Q2 · THE VIDEOS · 5 OF 10","Reels and motion posts, with sound",'<div class="vids">'+
 video("r13.jpg","1 · Watch her face when she picks up","Students away from home, placement pressure",L_R1,"Reel, 17 s")+
 video("r01.jpg","2 · The house is ready for Diwali. Are you?","Everyone, festive check-in",L_RD,"Reel, 17 s")+
 video("m24.jpg","3 · We switched on inner captions in today’s stand-up","Corporate teams · 27 s, each colleague in their own voice",L_M1,"Motion, 27 s")+
 video("m26.jpg","4 · Even Everest climbers take rest days","High achievers · 17.5 s, narrated",L_M11,"Motion, 17.5 s")+
 video("m25.jpg","5 · Most people walk past this painting in 3 seconds","Young professionals · 25 s, museum audio guide",None,"")+'</div>')
cf=lambda p,n:"".join(f'<div class="fr">{img(f"{p}-{i}.jpg")}</div>' for i in range(1,n+1))
page("Q2 · THE CAROUSELS · 2 OF 10","Swipe through both",f'''
<h4 class="rh">6 · Select all squares with a colleague who’s struggling. <small>For corporate: managers, HR, CHROs. A CAPTCHA nobody can solve, then the reveal.</small></h4><div class="strip s6">{cf("c21",6)}</div>
<h4 class="rh">7 · Your company offers counselling. Here’s everything you were too awkward to ask. <small>For employees. Questions answered one per slide.</small></h4><div class="strip s7">{cf("c09",7)}</div>''')
page("Q2 · THE SINGLE IMAGES · 3 OF 10","One idea, one image",f'''
<div class="three"><div class="sg">{img("s18.jpg")}<b>8 · Your best employee isn’t quiet.</b><span>For HR leaders: silent burnout and attrition.</span></div>
<div class="sg">{img("s03.jpg")}<b>9 · What’s in your control about AI</b><span>For professionals worried about their jobs.</span></div>
<div class="sg">{img("s-breakup.jpg")}<b>10 · Heartbreak and small moments</b><span>For young adults.</span></div></div>''')

# Q3
page("Q3 · FOUNDERS PROGRAM · THE PITCH","One coach for every founder, at zero cost to the fund",f'''
<div class="stats4"><div class="st y"><b>₹6,000 to 12,000</b><span>per program for the founder, incl. GST: 4, 8 or 12 weeks</span></div><div class="st l"><b>₹414 Cr → ₹42 Cr</b><span>full need, then reachable through partners</span></div><div class="st p"><b>₹99 L</b><span>revenue in Year 3, 976 founders, EBITDA +₹5 L</span></div><div class="st y"><b>1 introduction</b><span>is the whole ask, with a report after 90 days</span></div></div>
<div class="two"><div class="box"><h4>Package and price I would take to VCs</h4><p>The <b>founder pays</b>; funds pay ₹0 and their founders get 10% off. Anchor: ₹1,500 for a 40-minute call, close to YourDOST’s ₹1,299 to ₹1,599 sessions and about 13× cheaper than an executive coach.</p></div>
<div class="box"><h4>Why it works</h4><p>About 50% gross margin and 6.1× value per founder against cost to win them by Year 3. Built on 250+ founders already coached and 30 lakh+ sessions.</p></div></div>
<p class="small">The next three pages show all 10 slides. The editable deck is attached as the Q3 file.</p>''')
def dg(a,b): return '<div class="dgrid">'+"".join(f'<div class="dc">{img(f"d{i}.jpg")}<span>{i}/10</span></div>' for i in range(a,b+1))+'</div>'
for t,a,b in (("Slides 1 to 4",1,4),("Slides 5 to 8",5,8),("Slides 9 and 10",9,10)):
    page("Q3 · FOUNDERS PROGRAM · THE DECK",t,dg(a,b))

css=f'''
@font-face{{font-family:Poppins;font-weight:400;src:url(file://{F}/Poppins-400.woff2)}}
@font-face{{font-family:Poppins;font-weight:500;src:url(file://{F}/Poppins-500.woff2)}}
@font-face{{font-family:Poppins;font-weight:600;src:url(file://{F}/Poppins-600.woff2)}}
@page{{size:1600px 900px;margin:0}}
*{{box-sizing:border-box;margin:0}} body{{font-family:Poppins,sans-serif;color:#0D1015;background:#FDFCF7}}
.pg{{width:1600px;height:900px;padding:54px 80px 64px;position:relative;background:#FDFCF7;page-break-after:always;overflow:hidden}}
.pg:before{{content:"";position:absolute;left:-120px;top:-150px;width:420px;height:420px;border-radius:50%;background:#F6D25A;opacity:.28}}
header{{display:flex;justify-content:space-between;align-items:center;position:relative}} .tag{{font-size:15px;letter-spacing:.14em;font-weight:600;color:#8a6a00}} .logo{{width:74px;height:74px;border-radius:50%}}
h1{{font-size:46px;line-height:1.15;font-weight:600;margin:14px 0 6px;color:#2F2663;position:relative;max-width:1250px}} .sub{{font-size:21px;color:#5B4A9C;font-weight:500;position:relative}}
.body{{margin-top:22px;position:relative}} .lead{{font-size:22px;line-height:1.5;margin-bottom:20px;max-width:1300px}} p{{font-size:18px;line-height:1.55;margin-bottom:12px}} .small{{font-size:15px;color:#555;line-height:1.5}}
footer{{position:absolute;left:80px;right:80px;bottom:24px;display:flex;justify-content:space-between;font-size:13px;color:#777}}
a{{color:#5B4A9C;font-weight:500}}
.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:30px}} .card{{border-radius:26px;padding:30px;min-height:470px;position:relative}} .c1{{background:#E1CBF9}} .c2{{background:#F6D25A}} .c3{{background:#FFE4D1}}
.card .q{{font-size:56px;font-weight:600;color:#2F2663;opacity:.9}} .card h3{{font-size:27px;margin:6px 0 12px;color:#2F2663}} .card p{{font-size:18px}} .card em{{position:absolute;left:30px;bottom:24px;font-size:14px;color:#4a3d80}}
table{{border-collapse:collapse;width:100%;font-size:17px}} th{{text-align:left;color:#8a6a00;font-size:13px;letter-spacing:.1em;padding:10px 14px;border-bottom:2px solid #F6D25A}} td{{padding:20px 14px;border-bottom:1px solid #e7e0f2;vertical-align:top;line-height:1.45}} .qq{{font-size:34px;font-weight:600;color:#2F2663}}
.lst{{margin-top:6px}} .lst td{{font-size:15px;padding:12px 10px;background:#fff;border:2px solid #E1CBF9;border-radius:12px}} .note{{margin-top:30px;background:#E1CBF9;border-radius:20px;padding:22px 28px;font-size:18px;line-height:1.55}}
.two{{display:grid;grid-template-columns:1.05fr 1fr;gap:44px}} .two.nar{{grid-template-columns:500px 1fr}} .box{{background:#fff;border:2px solid #E1CBF9;border-radius:22px;padding:24px 28px}} h4{{font-size:19px;color:#2F2663;margin-bottom:10px}}
.stats,.stats4{{display:grid;gap:16px;margin:14px 0 18px}} .stats{{grid-template-columns:repeat(3,1fr)}} .stats4{{grid-template-columns:repeat(4,1fr)}}
.st{{border-radius:20px;padding:18px 20px}} .st b{{display:block;font-size:34px;color:#2F2663;line-height:1.1}} .stats4 .st b{{font-size:27px}} .st span{{font-size:15px;line-height:1.4;display:block;margin-top:6px}} .y{{background:#F6D25A}} .l{{background:#E1CBF9}} .p{{background:#FFE4D1}}
ul{{padding-left:22px}} li{{font-size:17px;line-height:1.5;margin-bottom:10px}} .center{{text-align:center}} .tall{{height:625px;border-radius:14px;box-shadow:0 8px 30px rgba(47,38,99,.18)}}
.strip{{display:flex;gap:14px}} .fr{{position:relative;flex:1}} .fr img{{width:100%;display:block;border-radius:10px;box-shadow:0 4px 16px rgba(47,38,99,.16)}} .fr span{{position:absolute;right:8px;bottom:8px;background:#2F2663;color:#fff;font-size:12px;padding:2px 8px;border-radius:10px}}
.strip{{margin:14px 0}}
.cols3{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin:22px 0}}
.vids{{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;margin-top:10px}} .vid{{display:flex;flex-direction:column;gap:8px}} .vid img{{width:100%;border-radius:14px;aspect-ratio:9/16;object-fit:cover;box-shadow:0 6px 20px rgba(47,38,99,.2)}} .vid b{{font-size:15.5px;line-height:1.35;color:#2F2663}} .vid span{{font-size:13px;color:#555;line-height:1.4}}
.btn{{background:#2F2663;color:#fff!important;border-radius:20px;padding:7px 12px;font-size:13px;text-decoration:none;text-align:center}} .btn.off{{background:#E1CBF9;color:#2F2663}}
.rh{{font-size:17px;margin:2px 0 0}} .rh small{{display:block;font-size:13.5px;font-weight:400;color:#555;margin-top:2px}}
.s6 .fr{{flex:0 0 212px}} .s7 .fr{{flex:0 0 170px}}
.three{{display:grid;grid-template-columns:repeat(3,1fr);gap:30px}} .sg{{display:flex;flex-direction:column;gap:8px}} .sg img{{width:100%;height:560px;object-fit:cover;object-position:top;border-radius:14px;box-shadow:0 6px 20px rgba(47,38,99,.2)}} .sg b{{font-size:17px;color:#2F2663}} .sg span{{font-size:14px;color:#555}}
.dgrid{{display:grid;grid-template-columns:1fr 1fr;gap:22px 30px}} .dc{{position:relative}} .dc img{{width:100%;display:block;border-radius:10px;box-shadow:0 4px 18px rgba(0,0,0,.18)}} .dc span{{position:absolute;right:10px;bottom:10px;background:#2F2663;color:#fff;font-size:12px;padding:2px 9px;border-radius:10px}}
.dgrid .dc img{{max-height:292px;width:auto;margin:0 auto}}
'''
doc=f'<!doctype html><meta charset=utf-8><title>Chethan N · YourDOST EIR submission</title><style>{css}</style>'+"".join(pages)
open("master.html","w").write(doc)
print(len(pages),"pages")
