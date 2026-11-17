"""Wrap Deck-Prompt.md in a designed, copyable page. Usage: python3 build_prompt_page.py <Deck-Prompt.md> <out.html>"""
import sys, html
src, out = sys.argv[1:3]
prompt = open(src, encoding='utf-8').read().strip()
page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Teardown Deck Prompt</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
:root{--ink:#1E1712;--ink2:#2C2219;--line:#4A3B2E;--cream:#FFF6EA;--dim:#E9DCCB;--muted:#B9AB9A;--red:#E0262E;--turm:#F2B21B}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--ink);color:var(--cream);font:16px/1.55 Inter,Arial,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:56px 24px 80px}
.eyebrow{font-size:12px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--turm)}
h1{font-family:'Bricolage Grotesque',Inter,sans-serif;font-size:52px;font-weight:800;letter-spacing:-.03em;line-height:1.04;margin-top:10px}
h1 span{color:var(--red)}
.lede{font-size:18px;color:var(--dim);margin-top:14px;max-width:720px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:34px 0}
.step{background:var(--ink2);border:1px solid var(--line);border-radius:16px;padding:18px}
.step b{display:block;font-family:'Bricolage Grotesque',Inter,sans-serif;font-size:30px;color:var(--turm);line-height:1}
.step p{margin-top:8px;color:var(--dim);font-size:15px}
.card{background:#FFF6EA;color:var(--ink);border-radius:20px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.35)}
.bar{display:flex;justify-content:space-between;align-items:center;padding:12px 18px;background:#F6E7D0;border-bottom:1px solid #E6D5BC}
.dots{display:flex;gap:7px}.dots i{width:12px;height:12px;border-radius:50%;background:#E0262E;display:block}.dots i:nth-child(2){background:#F2B21B}.dots i:nth-child(3){background:#1F7A3A}
.bar span{font-size:13px;font-weight:600;color:#5E5147}
button{font:600 14px Inter,sans-serif;background:#C8141C;color:#FFF6EA;border:0;border-radius:99px;padding:9px 18px;cursor:pointer}
button:focus-visible{outline:3px solid #F2B21B;outline-offset:2px}
pre{font:14px/1.6 'JetBrains Mono',ui-monospace,Menlo,monospace;white-space:pre-wrap;word-wrap:break-word;padding:22px 24px;max-height:none}
h2{font-family:'Bricolage Grotesque',Inter,sans-serif;font-size:28px;font-weight:800;margin:44px 0 12px}
.why{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.why div{background:var(--ink2);border:1px solid var(--line);border-left:5px solid var(--red);border-radius:12px;padding:14px 16px}
.why b{color:var(--turm)}
.why p{color:var(--dim);font-size:15px;margin-top:4px}
.short{background:var(--ink2);border:1px dashed var(--turm);border-radius:14px;padding:18px 20px;color:var(--dim);font-size:15.5px}
.foot{margin-top:40px;color:var(--muted);font-size:13px}
@media (max-width:680px){h1{font-size:36px}.steps,.why{grid-template-columns:1fr}pre{font-size:12.5px;padding:16px}}
@media print{body{background:#fff;color:#1E1712}.step,.why div,.short{background:#fff;color:#1E1712}.step p,.why p,.lede,.short{color:#3a2f27}.card{box-shadow:none;border:1px solid #ccc}button{display:none}.wrap{padding:0}@page{size:A4;margin:14mm}.card,.why div{break-inside:avoid-page}}
</style></head><body><div class="wrap">
<p class="eyebrow">The prompt behind the deck</p>
<h1>One prompt. <span>Nine slides.</span><br>Any company.</h1>
<p class="lede">This is the prompt that produced “Kishlay Foods, Decoded”: research first, a first-principles model second, a nine-slide story third, design last. Swap the words in braces for your next company.</p>
<div class="steps">
<div class="step"><b>1</b><p>Fill in the braces: company, website, your files, the logo to use, and anything to leave out.</p></div>
<div class="step"><b>2</b><p>Attach your research PDFs and a few screenshots of slide styles you like.</p></div>
<div class="step"><b>3</b><p>Paste it into Claude. Ask for changes slide by slide, by number.</p></div>
</div>
<div class="card"><div class="bar"><div class="dots"><i></i><i></i><i></i></div><span>Deck-Prompt.md</span><button id="copy" type="button">Copy prompt</button></div>
<pre id="prompt">__PROMPT__</pre></div>
<h2>Why each part is there</h2>
<div class="why">
<div><b>Research before design</b><p>Decks go generic when design starts first. Reading the files, the website and peers first gives every slide a real number.</p></div>
<div><b>Facts vs estimates</b><p>Interviewers test numbers. Labelling “est.” and keeping the working lets you defend or update any figure on the spot.</p></div>
<div><b>One unit, followed end to end</b><p>The ₹10 waterfall turns an abstract P&amp;L into something you can say in one breath, and it pays off the hook.</p></div>
<div><b>Exactly 9 slides</b><p>Nine forces one idea per slide and fits a 10–12 minute slot, leaving time for the conversation that wins the job.</p></div>
<div><b>Action titles</b><p>A title that states the insight lets the room follow the story even if they only read titles.</p></div>
<div><b>Speaker notes as script</b><p>The talk track lives with the slide, so the PPTX doubles as your rehearsal script.</p></div>
<div><b>Real photos only</b><p>The company’s own packs and plant make the deck feel like theirs, and show you did the legwork.</p></div>
<div><b>Quick wins, not criticism</b><p>A website audit framed as “I’d own this” shows initiative without putting the founder on the defensive.</p></div>
</div>
<h2>The 60-second version</h2>
<div class="short">Act as a strategy consultant and presentation designer. Research {COMPANY} ({WEBSITE}) and my attached files, audit its website on desktop and mobile, and benchmark 2–3 listed peers. Then build a 9-slide first-principles teardown (hook, need gap, portfolio, make, move with a ₹10 waterfall, sell, competition, brand and website audit, 90-day plan) in Claude Slides using the company’s logo, real product photos, brand colours, infographics instead of bullets, action titles, sources and speaker notes on every slide. Leave out {TOPICS}. Also give me a presenting playbook and the 4 best questions to ask the interviewer.</div>
<p class="foot">Prepared by Chethan N · November 2026</p>
</div>
<script>
document.getElementById('copy').addEventListener('click', async function () {
  var t = document.getElementById('prompt').innerText, b = this;
  try { await navigator.clipboard.writeText(t); }
  catch (e) { var r = document.createRange(); r.selectNodeContents(document.getElementById('prompt')); var s = getSelection(); s.removeAllRanges(); s.addRange(r); try { document.execCommand('copy'); } catch (_) {} }
  b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy prompt'; }, 1600);
});
</script>
</body></html>"""
open(out, 'w', encoding='utf-8').write(page.replace('__PROMPT__', html.escape(prompt)))
print('wrote', out)
