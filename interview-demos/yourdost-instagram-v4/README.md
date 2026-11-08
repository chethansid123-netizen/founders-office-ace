# YourDOST Instagram set (EIR task, Q2): v4

Ten posts, English only, one or two short lines per frame, built on real photographs:
4 reels with original music, 3 carousels and 3 single images. Each folder holds the files in upload order
plus `UPLOAD.md` (the line, why, date and time, caption, hashtags, first comment, alt text, upload steps).

| # | Folder | Format | The line | For |
|---|---|---|---|---|
| 01 | 01-Reel-Diwali | Reel, 17.4 s, music | The house is ready for Diwali. Are you? | Everyone |
| 02 | 02-Reel-Pause-On-A-Word | Reel, 19 s, music | Pause this reel on a word. That's how today really feels. | Everyone |
| 03 | 03-Carousel-Exam-Stress | Carousel, 4 | Your marksheet shows your marks. Not the nights you studied. | Students |
| 04 | 04-Image-AI-Anxiety | Image | AI finished my 3-day task in 40 seconds. Then I couldn't sleep. | Professionals |
| 05 | 05-Carousel-Breakup | Carousel, 4 | You picked up your phone to tell them. Then you remembered. | Young adults |
| 06 | 06-Reel-Job-Hunt | Reel, 17.4 s, music | Rejection emails are often automated. Your worth isn't. | Job seekers |
| 07 | 07-Image-Founders | Image | Investors track your runway. Who's tracking you? | Founders |
| 08 | 08-Reel-Mens-Day | Reel, 17.2 s, music | He says “I'm fine.” Ask him again. Over chai. | Men |
| 09 | 09-Image-Getting-Back-Together | Image | Getting back together is easy. Trusting again takes time. | Couples |
| 10 | 10-Carousel-HR-and-Campus-Leaders | Carousel, 5 | Her exit form said “better opportunity.” | HR leaders, deans |

## Photos, music, and the OpenArt preview

- **Photos in the final posts:** real photographs from the WordPress Photo Directory, StockSnap and Rawpixel, all CC0
  (free to use, no credit needed), found through Openverse.
- **Music:** composed for these reels in `source/music.py` (a tanpura and santoor phrase for Diwali, soft lo-fi for the
  check-in reel, piano for the job-hunt and Men's Day reels). It is original, so there are no copyright claims.
- **`Preview-with-OpenArt-people-photos-WATERMARKED/`:** posts 01, 02, 03, 04, 08 and 09 rebuilt with six photos of
  people generated on OpenArt (Wan 2.7 Image, 36 of the 40 free credits). The free plan stamps an OpenArt watermark on
  them, so these are previews only. To use them in the final posts, upgrade OpenArt, download the unwatermarked copies
  of the same six images from your OpenArt library into `source/` as described below, and re-run the export.

## Facts used

- Deloitte, Mental Health and Well-being in the Workplace (2022): about ₹1.1 lakh crore a year to Indian employers.
- YourDOST, Decade of Wellness Report (from @yourdostcom's carousel): post-pandemic sessions 57.88% chat, 18.49% audio, 17.8% video, 5.84% in person.
- YourDOST website: certified experts available 24/7. Founders programme: yourdost.com/emotional-wellness-founders.
- Tele MANAS 14416: India's free 24/7 government mental health helpline.

## Rebuild

```bash
cd source
python3 music.py music                       # the four music tracks
python3 prep_photos.py <folder with photos>  # crops to 1188x2112 (reels) and 1080x1350 (feed)
node export.mjs ..                           # final set (needs Playwright and ffmpeg)
node export.mjs "../Preview-with-OpenArt-people-photos-WATERMARKED" --people --only=01,02,03,04,08,09
```

To swap in clean OpenArt images later, save them as `oa_diwali-woman.jpg`, `oa_man-terrace.jpg`, `oa_chai-friends.jpg`,
`oa_student-night.jpg`, `oa_laptop-woman.jpg` and `oa_couple.jpg` in the photo folder, re-run `prep_photos.py`, then run
the export with `--people` into the main folder.
