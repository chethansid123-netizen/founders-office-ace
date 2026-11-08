# YourDOST Instagram set (EIR task, Q2): two story-style posts, 11 and 12

These two posts follow the style of the reference carousels (TailCrafts, @therapeuticallyours):
- a candid photo cut out as a sticker with a white edge
- handwritten side notes
- hand-drawn arrows and doodles
- a story that builds across the swipe

They keep YourDOST's colours and put the logo on every slide. Each folder has the files in upload order, plus an
`UPLOAD.md` with the line, why it works, posting date and time, caption, hashtags, first comment, alt text and upload steps.

| # | Folder | Format | The line | For | Engagement |
|---|---|---|---|---|---|
| 11 | 11-Carousel-First-Semester | Carousel, 5 | Nobody tells you how the first semester feels. | College students who moved cities | Tag your hostel roommate; "send this to your hostel group chat" |
| 12 | 12-Image-Weekend-Off | Image | You promised yourself one weekend off. | Employees at corporate clients | Comment how many times you checked work email this weekend |

Post 11 goes out Mon 30 Nov 2026 at 8:00 PM IST, when hostel evenings are quiet.
Post 12 goes out Sun 6 Dec 2026 at 6:00 PM IST, the exact moment it describes.

## Photos and fonts

- **Photos:** real photographs from the WordPress Photo Directory, all CC0 (free to use, no credit needed), found through Openverse.
  `source/cutout.py` turns the student, the backpack and the hands holding a phone into stickers. It uses rembg for the cut-out, then adds a white edge.
- **Fonts:** all from Google Fonts, under the Open Font License.
  - Fredoka for headlines
  - Gaegu for handwritten notes
  - Poppins, YourDOST's own font, for body text and the call to action
- **Logo:** the YourDOST round badge, at the bottom of every slide.

## Rebuild

```bash
cd source
node export.mjs ..                          # renders both posts and their UPLOAD.md (needs Playwright)
python3 cutout.py <folder with the photos>  # only to remake the stickers (needs rembg)
```

The finished stickers are already in `source/cutouts/`, so the export alone rebuilds both posts. In `phone-hands.png`, a small
dark speck on the hand was painted out by hand after the cut-out.
