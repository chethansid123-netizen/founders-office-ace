# YourDOST Instagram set (EIR task, Q2): v7, three carousels and three original formats

Six posts built on YourDOST's STP:
- **Segments:** corporate (HR, managers, employees), young adults and students, first-time therapy seekers, and high achievers.
- **Targeting:** the corporate buyer gets two posts, a carousel and an original format.
- **Positioning:** one line throughout. YourDOST is a confidential expert who is as easy to reach as a friend: chat, call or video, 24/7.

Two posts show **people** with candid expressions (21 and 24, both corporate). The other four use **evergreen imagery**:
- the night sky over Ladakh and a planetarium (22)
- a Rajasthani stepwell (23)
- a gallery painting (25)
- Everest base camp (26)

The logo badge is on every slide. Each folder has the files in upload order and an `UPLOAD.md` (line, why it works, segment, date and time,
caption, hashtags, first comment, alt text, upload steps). Each original also has a **`Motion.mp4`**, a reel version with expressive
ElevenLabs voices, music and sound.

| # | Folder | Format | Hook | Segment (STP) | Engagement |
|---|---|---|---|---|---|
| 21 | 21-Carousel-Select-All-Squares | Carousel, 6 · people | Select all squares with a colleague who's struggling. | Corporate: managers, HR, CHROs (B2B) | A CAPTCHA no one can solve; "did you click Skip?"; send to HR |
| 22 | 22-Carousel-Old-Light | Carousel, 5 · stars | The starlight you see tonight left its star years ago. | Young adults, students | Send to someone you haven't checked on (Geminids night) |
| 23 | 23-Carousel-The-Stepwell | Carousel, 5 · architecture | This well has 3,500 steps. The water is at the very bottom. | First-time therapy seekers | Save for the day you need it |
| 24 | 24-Original-Inner-Captions | Original + motion · people | We switched on inner captions in today's stand-up. | Corporate teams (B2B) | "What would your inner caption say?" |
| 25 | 25-Original-The-Gallery-Label | Original + motion · painting | Most people walk past this painting in 3 seconds. | Urban young professionals | "What would your painting be called?" |
| 26 | 26-Original-Everest-Rest-Days | Original + motion · mountains | Even Everest climbers take rest days. | High achievers, hustle culture | "When was your last real rest day?" |

## Original formats (not done before for this category)
- **24 · Inner captions:** a video-call screen whose live captions show what each person thinks under what they said. In the motion version each colleague speaks in their own voice, then their thoughts play as whispers, panned to where they sit on screen.
- **25 · Gallery label:** a museum wall label for a painting everyone has made: a yellow smile-stroke over a storm. The motion version is a museum audio guide.
- **26 · Expedition chart:** a real climbing plan (up, down, rest, repeat) plotted against a "no rest days" line that crashes into burnout.

## How it was made (ElevenLabs, ≈ 12,000 credits for this set)

Every model was priced first, and everything ran as a single take. Premium models were used only where they show.

| Step | Model | Count | Credits |
|---|---|---|---|
| Team photo (7 expressive faces) | Seedream 5 Pro, 2K | 1 | 818 |
| Gallery painting | Krea 3, 2K | 1 | 604 |
| Night sky, planetarium, city, dawn, stepwell ×3, base camp, webcam faces ×5 | Seedream 5 Lite, 2K | 13 | 2,757 |
| Three webcam faces remade for subtler expressions | Seedream 5 Lite, 2K | 3 | 636 |
| Live webcam tiles (5 × 4 s) + base camp (8 s) | Veo 3.1 Lite, 720p | 6 | 5,090 |
| Expressive voices: 6 colleagues, 3 narrators | ElevenLabs v3 | 9 | 1,169 |
| Scores | ElevenLabs Music v2.5 | 3 | 855 |
| Sound effects | ElevenLabs Sound Effects v2 | 6 | 94 |
| **Total** | | | **≈ 12,020** |

Together with v6 (≈ 12,200), about 24,200 of the 40,000 credits are used, so about 15,800 remain.

Facts used:
- Deloitte, Mental Health and Well-being in the Workplace (2022): about 80% of India's workforce reported mental-health concerns in the past year, at a cost to employers of about ₹1.1 lakh crore a year.
- Chand Baori: about 3,500 steps over 13 levels, more than 1,000 years old.
- Sirius's light is about 8.6 years old.
- Hanle, Ladakh is India's first dark-sky reserve.
- Everest is 8,849 m, and expeditions take about 6 weeks with acclimatisation rotations.

## Rebuild

```bash
cd source
node export.mjs ..   # the six posts (PNG) + every UPLOAD.md
node motion.mjs ..   # the three Motion.mp4 versions (Playwright + ffmpeg)
```
