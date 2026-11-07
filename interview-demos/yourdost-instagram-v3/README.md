# YourDOST Instagram set (EIR task, Q2): v3

Ten posts in English: 3 reels, 5 carousels and 2 single images. Each folder holds the files in upload order and an
`UPLOAD.md` with the posting date and time, caption, hashtags, first comment, alt text and step-by-step upload instructions.

| # | Folder | Format | For | Post on |
|---|---|---|---|---|
| 01 | 01-Reel-Diwali | Reel, 16.5 s | Everyone celebrating Diwali | Sun 8 Nov, 11:00 AM |
| 02 | 02-Carousel-Exam-Stress | Carousel, 7 slides | Students | Tue 10 Nov, 7:00 PM |
| 03 | 03-Image-AI-Anxiety | Single image | Professionals worried about AI | Wed 11 Nov, 1:00 PM |
| 04 | 04-Carousel-Breakup | Carousel, 7 slides | Students and young adults | Fri 13 Nov, 9:30 PM |
| 05 | 05-Carousel-Getting-Back-Together | Carousel, 6 slides | Couples | Sun 15 Nov, 8:00 PM |
| 06 | 06-Reel-Job-Hunt | Reel, 17 s | Freshers and job seekers | Tue 17 Nov, 8:00 PM |
| 07 | 07-Image-Founders | Single image | Founders, incubators, VCs | Wed 18 Nov, 9:00 AM |
| 08 | 08-Reel-Mens-Day | Reel, 16.8 s | Men, and people who love them | Thu 19 Nov, 9:00 AM |
| 09 | 09-Carousel-Ask-Your-Counsellor | Carousel, 7 slides | Employees | Mon 23 Nov, 1:00 PM |
| 10 | 10-Carousel-HR-and-Campus-Leaders | Carousel, 6 slides | HR leaders, deans, professors | Tue 24 Nov, 10:00 AM |

## Where the look and the structure come from

- **Look:** @yourdostcom's own carousels (Decade of Wellness, awards): warm off-white canvas, soft yellow shapes,
  Poppins in Title Case, yellow #F6D25A and lavender #E1CBF9 cards with purple icons, small gold caps labels,
  the round logo badge top-left on every slide, and a "Source:" line under a rule for any statistic.
- **Story structure:** the reference posts shared by Ruchi: short title-only first slides with a curiosity line,
  one repeating stem per carousel ("It doesn't show…", "It's not the goodbye…"), small pastel characters,
  a save-worthy framework (the in-control / not-in-control circle), and soft closing slides.

## Facts used

- YourDOST website footer: certified experts available 24/7, 20+ Indian languages, 500+ organisations.
- YourDOST, Decade of Wellness Report (from @yourdostcom's carousel): post-pandemic sessions 57.88% chat, 18.49% audio, 17.8% video, 5.84% in person.
- Deloitte, Mental Health and Well-being in the Workplace (2022): about ₹1.1 lakh crore (US$14 bn) a year.
- Blind survey, July 2026: 66% of AI/ML professionals in India expect layoffs within 3–6 months (caption of post 03).
- Tele MANAS 14416: India's free 24/7 government mental health helpline.
- YourDOST founders programme: yourdost.com/emotional-wellness-founders. CTA wording for post 10 follows YourDOST's own (www.yourdost.com, contact@yourdost.com).
- Names and numbers inside the visuals (Riya Sharma, Priya M., 147 applications) are illustrative.

## Rebuild

```bash
cd source
node export.mjs ..          # all folders: PNGs, MP4 reels (needs Playwright and ffmpeg), UPLOAD.md
node export.mjs /tmp/qa --qa   # quick low-res check
```

Reels are exported with a silent audio track; add music in the Instagram app as each UPLOAD.md describes.
