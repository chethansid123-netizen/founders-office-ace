# Jo Bola Nahi: YourDOST Instagram posts (EIR task, Q2)

Ten Instagram posts that raise awareness about emotional wellness, built as one campaign, **#JoBolaNahi** ("what went unsaid").
Each post pairs the line people say ("theek hoon", "Good, you?", "Haan maa, process mein hai") with the line they don't,
one typed and one handwritten, and signs off **"Bol do. Halka lagega."** Prepared by Chethan N, 7 Nov 2026.
This is an interview concept, not content published by YourDOST.

| File | What it is |
|---|---|
| `YourDOST-JoBolaNahi-Q2.pdf` | The submission: 14 A4 landscape pages. Cover, the ten posts, approach, one page per post (visual, the line, a short why, hook, engagement, caption), calendar, guardrails, sources. |
| `YourDOST-JoBolaNahi.html` | The same work as an interactive page. Reels play, carousels swipe, stories tap through. Works offline. |
| `exports/` | Post-ready files: 3 reels as MP4 (1080 × 1920, 30 fps, silent so audio can be added in the app) with cover PNGs, carousel and static PNGs (1080 × 1350), story frames (1080 × 1920, without stickers; mockups with stickers in `story-mockups/`), and `grid-preview.png`. |
| `source/` | Copy, strategy notes and renderers (`creatives.js`, `creatives.css`), the page (`page.js`, `page.css`, `template.html`), build and export scripts, fonts. |

## The ten posts

| # | When | Post | Format | For |
|---|---|---|---|---|
| 01 | Sun 8 Nov | Poora ghar chamka diya. Andar ka ek kona abhi bhi andhera hai. *Is Diwali, ek diya wahan bhi.* | Reel | Everyone home for Diwali |
| 02 | Tue 10 Nov | It did my 3-day task in 40 seconds. *I typed "wow 🔥". Then I didn't sleep.* | Carousel | Professionals anxious about AI |
| 03 | Thu 12 Nov | Marksheet pe percentage bold mein chhapta hai, naam chhote font mein. *Tum ulta yaad rakhna.* | Reel | Students in exam season |
| 04 | Sat 14 Nov | Aaj kuch funny hua. Tumhe batane ke liye phone uthaya. *Phir yaad aaya.* | Static | Young adults after a breakup |
| 05 | Mon 16 Nov | Wapas saath hain. Sabne bola "finally!" *Kisi ne nahi bataya ki asli kaam patch-up ke baad shuru hota hai.* | Carousel | Couples who got back together |
| 06 | Wed 18 Nov | Runway: 7 months. Sleep: 4 hours. People I can be honest with: 0. *Who's asking about the third?* | Static + LinkedIn | Founders, incubators, VCs |
| 07 | Thu 19 Nov | Is hafte usne 11 baar "theek hoon" bola. *12vi baar poocho. Phir ruko.* | Static | Men, and people who love them |
| 08 | Fri 20 Nov | 147 applications. 61 "we regret to inform you". *Tumhara inbox tumhare baare mein faisla nahi hai.* | Reel | Freshers and job seekers |
| 09 | Sun 22 Nov | Office mein "How are you?" ka sirf ek allowed answer hai: "Good, you?" *Yahan sach bol sakte ho.* | Story series | Employees |
| 10 | Tue 24 Nov | Her exit form said "better opportunity". *The real reason was her green dot at 1:40 AM.* | Carousel + LinkedIn | HR leaders (B2B buyers) |

## Accuracy notes

- Statistics are sourced: Blind survey, July 2026 (66% of AI/ML professionals in India expect layoffs within 3–6 months);
  Deloitte 2022 (about US$14 bn, ₹1.1 lakh crore, a year to Indian employers); YourDOST's own site footer (30 seconds,
  20+ languages, 500+ organisations, 30 lakh+ sessions, 23+ states); Tele MANAS 14416.
- Names and numbers inside the creatives (Riya, Priya M., application #147, 7 months of runway) are illustrative.
- To confirm with YourDOST before posting: college/company access wording, the founders programme link, and whether any session type may be called free.
- Colours and type are campaign choices. To match YourDOST's brand kit, change the tokens at the top of `source/creatives.css` and re-run the build.

## Rebuild

```bash
cd source
python3 build_page.py ../YourDOST-JoBolaNahi.html     # interactive page (fonts, CSS, JS inlined)
node export.mjs ../exports                            # PNGs and MP4 reels (needs Playwright and ffmpeg)
node build_pdf.mjs                                    # the PDF and exports/grid-preview.png
node export.mjs /tmp/qa --qa                          # quick low-res check of every frame
```

Fonts: Anek Latin and Mukta (Ek Type), Kalam (Indian Type Foundry), IBM Plex Mono, all SIL Open Font License 1.1.
