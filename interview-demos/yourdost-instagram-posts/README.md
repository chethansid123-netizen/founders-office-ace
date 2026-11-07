# YourDOST Instagram posts (EIR task, Q2)

Ten single-image Instagram posts (1080 × 1350 PNG), English only, built on YourDOST's own brand: the official logo on every post, YourDOST yellow and black, coral and pale pink from YourDOST's report design, Poppins and Lato, line art in the style of the two-heads logo, and YourDOST's blog section names as labels. Prepared by Chethan N, 7 Nov 2026, as an interview concept.

| # | File | Label | Post |
|---|---|---|---|
| 01 | Post-01-diwali.png | Festive Wellbeing | Every corner of the house is shining this Diwali. Light a diya for your mind too. |
| 02 | Post-02-exam-stress.png | Student Life | Your marksheet prints your percentage in bold and your name in small font. Remember it the other way round. |
| 03 | Post-03-breakup.png | Love & Relationships | Something funny happened today. I picked up my phone to tell you. Then I remembered. |
| 04 | Post-04-getting-back-together.png | Love & Relationships | You got back together. Everyone said “finally!” Nobody tells you trust takes longer to rebuild. |
| 05 | Post-05-ai-anxiety.png | Work & Careers | AI finished my 3-day task in 40 seconds. I said “wow.” Then I couldn't sleep. |
| 06 | Post-06-job-hunt.png | Work & Careers | 147 applications. 61 rejections. 86 never replied. Your inbox is not a verdict on your worth. |
| 07 | Post-07-founders.png | Founder Wellbeing | Investors track your runway. Who's tracking how you're doing? |
| 08 | Post-08-how-are-you.png | Work & Careers | At work, there's only one acceptable answer to “How are you?” Here, you can tell the truth. |
| 09 | Post-09-hr-leaders.png | For HR Leaders | Her exit interview said “better opportunity.” The real reason was her 1:40 AM online status. |
| 10 | Post-10-im-fine.png | Self & Growth | He said “I'm fine” 11 times this week. Ask a 12th time. Then really listen. |

## Captions

**01.** The house is spotless, the lights are up, everyone looks happy. And sometimes you still feel low. That's okay, and you don't have to hide it. This Diwali, make a little space for how you're really feeling. Our experts are here 24/7, even on festival days. #HappyDiwali #EmotionalWellness #YourDOST

**02.** Boards, entrance exams, semester finals: the numbers matter, but they are not who you are. If exam pressure is keeping you up at night, talk to someone. Many colleges already give students access to YourDOST. In crisis? Call Tele MANAS 14416 (free, 24/7). #ExamStress #StudentLife #YourDOST

**03.** The hardest part of a breakup is often not the fight. It's the small moments after, when the person you'd tell isn't yours to tell anymore. That reflex fades, slower than you'd like. Until then, talk to someone. Save this for the night you almost hit send. #Heartbreak #Relationships #YourDOST

**04.** Getting back together is the easy part. Feeling safe again takes longer, and that doesn't mean it was a mistake. Ask each other: what's different this time, and what will we do when it gets hard? If you need help with those conversations, our relationship experts are here. #Relationships #Trust #YourDOST

**05.** AI is changing work fast, and it's normal to feel uneasy about where you fit in. That worry is often about more than the job: it's about your sense of worth. You don't have to figure it out alone at 2 AM. Talk it through with a YourDOST expert. #AIAnxiety #WorkStress #YourDOST

**06.** Rejection emails are often sent automatically, to hundreds of people at once. Please don't give them days of your self-worth. If the job hunt is wearing you down, talk to someone about the career side and the emotional side. #JobSearch #CareerStress #YourDOST

**07.** Founders are often the only people in the company who can't have a bad day out loud. The team needs morale, investors need conviction, and family wanted the safe job. If you have no one to be honest with, start here. YourDOST's emotional wellness program for founders: yourdost.com/emotional-wellness-founders #FounderWellbeing #Startups #YourDOST

**08.** "Good, you?" is the answer we give at work, even on the days it isn't true. You deserve a place where you can say how you really are. Many companies offer YourDOST to their employees. Ask your HR team, and talk to an expert today. #WorkplaceWellbeing #EmployeeWellbeing #YourDOST

**09.** Exit interviews rarely tell the whole story. Burnout shows up earlier: cameras off, Monday sick leave, the 11 PM "just checking". YourDOST works with 500+ organisations to make emotional support private, instant and available in 20+ Indian languages. Want to support your people better? Book a demo at yourdost.com. #HR #EmployeeWellbeing #YourDOST

**10.** International Men's Day, 19 November. Many men grow up learning to fix things, pay the bills and keep their feelings to themselves. Today, check in on him. Ask again, and wait for the real answer. If he isn't ready to talk to you, our experts are here 24/7. In crisis? Call Tele MANAS 14416. #InternationalMensDay #MensMentalHealth #YourDOST

## Notes

- Logo: cropped from resources.yourdost.com/YD_OG_Image.png (for yellow posts) and extracted from YourDOST's Wellness Across Ages report page (for white posts), in source/brand/.
- Claims used: certified experts 24/7, 500+ organisations, 20+ Indian languages (YourDOST website footer); founders programme at yourdost.com/emotional-wellness-founders; Tele MANAS 14416 is India's free 24/7 government mental health helpline.
- Names and numbers inside the visuals (Riya Sharma, Priya M., 147 applications) are illustrative.

## Rebuild

```bash
cd source
node export.mjs ..   # writes Post-01 … Post-10 PNGs (needs Playwright)
```

Fonts: Poppins and Lato, SIL Open Font License 1.1.
