# Operations application for The Charter

A one-page application for The Charter's operations role, in The Charter's own palette and typefaces. It has five projects ranked by
fit, a mock ops kit for a Charter gathering in Bengaluru, and research on how The Charter runs. Prepared by Chethan N, 4 Nov 2026.

**Data note.** The ops kit is a mock: no venue, partner, chef or guest has been contacted, and every tracker status is simulated.
Brands marked "public list" appear on The Charter's partnerships page and are used only as candidates. Facts about The Charter come
from its website and press coverage, linked on the page. The page is not affiliated with or endorsed by The Charter.

| File | What it is |
|---|---|
| `Chethan-N-for-The-Charter.html` | The page to send. One file, works offline. |
| `Charter-Send-Checklist.html` | Private prep: the fixes to make before sending, ready answers, the cover message, how to add photos. Don't send this one. |
| `source/` | Template, build script and fonts. |

## The company page

1. **Hero and at a glance**: the pitch, two years in Founder's Office roles, six headline numbers.
2. **Five projects, ranked by fit**: cxo's × Masters' Union event · Techvaraha delivery SOPs · GastroTrack for Micro Labs ·
   LVX investor coordination and the Dubai/UK corridor · Ghomedha operations. Each ends with the role line it answers and what it
   means on a Charter evening. Swish market research is mentioned as a backup.
3. **Fit**: the five projects and the ops kit against what the role asks for. Sponsor and venue sourcing is shown as covered only by the kit.
4. **Ops kit: The F&B Sit-Down, Bengaluru** (mock): brief, run of show, venue and partner tracker (switch between T-35, T-14 and T-1),
   timeline from brief to close-out, seating, dietary sheet and risk register. Changing the mock date moves every date.
5. **How The Charter runs**: the record, room sizes, partners per big night, key numbers, formats, the partner model, the rules that
   shape logistics, and what it means for the role. Sources linked.
6. **First 30 days** and **contact**.

## No images

The page carries no photos. Each project has a text diagram instead: the event flow, the before-and-after delivery numbers,
the seven-month coordination hub, the LVX investor network and the Ghomedha supply chain. The build refuses any `<img>`.

## Lovable

Live at **https://chethan-for-the-charter.lovable.app** (Lovable project "Chethan for The Charter"). The project stores this file
unchanged as `public/chethan-for-the-charter.html` and shows it full screen on `/`. To update it, rebuild here, upload the new file
to the project and ask its agent to replace that file byte for byte, then publish.

## Rebuild

```bash
cd source
python3 build.py
```

This writes both pages here, and copies without the document wrapper to `source/artifact/` for publishing as claude.ai Artifacts.
Fonts (Cinzel, Montserrat, Source Sans 3; SIL Open Font License) are embedded so the page renders the same offline.
