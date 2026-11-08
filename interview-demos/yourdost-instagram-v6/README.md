# YourDOST Instagram set (EIR task, Q2): v6, made with ElevenLabs

Eight posts for eight different audiences:
- 3 reels (16 to 17 s, with sound)
- 2 carousels
- 2 one-liner images
- 1 original format (a year-end receipt)

The YourDOST logo is on every slide and frame. Each folder holds the files in upload order and an `UPLOAD.md` covering:
- the line and why it works
- date and time
- caption, hashtags and first comment
- alt text and upload steps

| # | Folder | Format | The line | For | Genre and engagement |
|---|---|---|---|---|---|
| 13 | 13-Reel-Im-Fine-Ma | Reel, 17 s | Watch her face when she picks up. | B-school and IIT students away from home | Emotional micro-drama with real dialogue ("Hi Ma! Yes, I ate. Everything's fine, really."). Tag the person you call. |
| 14 | 14-Reel-Low-Battery | Reel, 17 s | Your phone warns you at 20%. Your body warns you too. | Corporate employees | Phone-interface satire: a low-battery alert, then the body's warnings as notifications. Comment your "low battery" sign. |
| 15 | 15-Reel-Ask-How-She-Is | Reel, 17 s | Everyone asks about the baby. Ask how she is. | New parents and their families | Quiet, sound-led (3:07 AM). Tag a new parent. |
| 16 | 16-Carousel-Not-About-The-Dishes | Carousel, 5 | You're not fighting about the dishes. | Couples | "What they said / what they meant" translator cards. Send to your person. |
| 17 | 17-Carousel-Placement-Season-Parents | Carousel, 5 | The first question after placements shouldn't be "What's the package?" | Parents of IIT/IIM students | Message-rewrite cards. Send to the family group. |
| 18 | 18-Image-Quietly-Leaving | Image | Your best employee isn't quiet. She's quietly updating her résumé. | HR leaders (B2B) | Twist line plus the B2B call to action. |
| 19 | 19-Image-Typed-Deleted-Never-Sent | Image | Some messages get typed, deleted and never sent. | Young adults, Gen Z | Text your quiet friend first. Tag them. |
| 20 | 20-Original-Your-2026-Receipt | Image | Your 2026, itemised. | Everyone, on 31 Dec | Shareable receipt. Comment your line 1. |

Every reel ends on the YourDOST product itself: a chat with an expert, because chat is how most YourDOST sessions start.
Each reel's chat ties back to its story ("honestly? i miss home", "i think i'm running on 5%", "how are *you* doing?").

## How it was made (ElevenLabs, credit-efficient)

Everything visual and audible was generated on one ElevenLabs Flow, "YourDOST v6 – Reels, carousels, images".
Every model was priced with an estimate before anything ran. Every generation was a single take. Every scene was
first made as a cheap still and checked before any video credits were spent on it.

| Step | Model | Count | Credits |
|---|---|---|---|
| Photoreal stills (reel start frames + post photos) | Seedream 5 Lite, 2K | 13 | 2,757 |
| Video clips (8 s, 6 s, 4 s; 720p, upscaled to 1080p) | Veo 3.1 Lite (native audio only on the dialogue shot) | 6 | 8,242 |
| Music beds, 17 s each | ElevenLabs Music v2.5 | 3 | 765 |
| Sound effects | ElevenLabs Sound Effects v2 | 8 | 124 |
| Voiceover | ElevenLabs v3 (Saumya, Lavkush, Parul) | 3 | 309 |
| **Total** | | | **≈ 12,200 of 40,000** |

Why these choices:
- **Video is the expensive part.** For the same 12 s, Seedance 2.5 priced at 33,611 credits, Seedance 2 Fast at 17,598 and Kling 3 Pro at 8,145. Veo 3.1 Lite does 8 s for 1,454.
- **720p is enough.** All text and interface elements are rendered sharp at 1080p on top of the footage.
- **Audio separately is cheaper.** Veo's own audio adds about 970 credits per clip, so it was used only where lip-synced dialogue mattered (Reel 13). Music, sound effects and voice came from ElevenLabs audio, which cost under 1,200 credits for all three reels.
- **Brand elements are built in HTML.** Text, the YourDOST chat interface, phone notifications and the logo are made in HTML/CSS, not by AI, so the brand is exact and costs no credits.

Students are shown at top institutes (a B-school hostel in placement week, an engineering hostel after interviews).
Institute names and logos are kept out of the visuals so nothing implies a partnership. If YourDOST works with a specific
IIT or IIM, its name can go in the caption.

## Rebuild

```bash
cd source
node render.mjs ..        # the three reels: footage + overlays + audio mix (Playwright, ffmpeg)
node render.mjs .. --qa   # key-frame previews only
node export.mjs ..        # the five static posts + every UPLOAD.md
```

`source/ai/` holds the ElevenLabs stills and clips, and `source/audio/` the music, sound effects and voiceover.
