# YourDOST EIR assignment: submission package

The upload form allows 5 files (100 MB each). These are the 5, in reading order.

| # | File | What it is |
|---|---|---|
| 1 | `00_START_HERE_Chethan_YourDOST_Submission.pdf` | 24 pages. Q1, Q2 and the full Q3 deck, one slide per page. The logo is top-right on every page. Open this first. |
| 2 | `Q1_Infographic_and_Carousel.pdf` | The social-media infographic, then the 5-slide carousel. |
| 3 | `Q1_Insights_Workbook.xlsx` | Survey data, Numiqo analysis, and the maths behind every number. |
| 4 | `Q2_All_10_Posts.zip` | The 10 posts: 4 videos, 2 carousels, 4 images, one folder each. Not tracked in git (83 MB). |
| 5 | `Q3_Founders_Program_Pitch_Deck.pptx` | The 10-slide pitch deck. |

Online copies (anyone with the link): carousel PDF
https://drive.google.com/file/d/1fdAX0xq4IsXEsd_6gkWUcVzFaL3BsHiu/view and workbook
https://docs.google.com/spreadsheets/d/19cCklmGSg7WdDTZ-N8hVO45dms6vo0o7KZ0LSueIHiE/edit?usp=sharing

## Rebuild the master PDF
`source/build2.py` writes `master.html` from images in `a/`; `source/pdf2.mjs` prints it to PDF with Playwright.
