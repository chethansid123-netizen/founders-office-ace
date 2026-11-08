/* YourDOST v6 static posts: 2 carousels, 2 one-liner images and 1 original format (a receipt).
   Photos are ElevenLabs (Seedream 5 Lite) generations; the logo badge sits top-right on every slide. */
(function (root) {
  "use strict";
  const badge = `<img class="badge" src="brand/badge.png" alt="YourDOST">`;
  const CTA = `<span class="cta">Talk to a certified expert, 24/7 · <b>yourdost.com</b></span>`;
  const swap = `<svg width="44" height="44" viewBox="0 0 44 44"><path d="M14 8 V34 M14 34 L7 27 M14 34 L21 27 M30 36 V10 M30 10 L23 17 M30 10 L37 17" fill="none" stroke="#0d1015" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  const arrow = (c = "#0d1015", w = 190, st = "") => `<svg class="doodle" style="${st}" viewBox="0 0 220 160" width="${w}"><path d="M14 20 C 40 120 120 140 186 120" fill="none" stroke="${c}" stroke-width="6" stroke-linecap="round"/><path d="M164 96 L190 120 L162 140" fill="none" stroke="${c}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  const count = (i, n) => `<span class="count">${i}/${n}</span>`;

  const tr = (n, said, meant, note) => () => `<div class="paper bg-cream" style="position:absolute;inset:0"></div>
    <div class="tophead"><p>Couple → Honest translator</p><p class="h s">What they said vs. what they meant</p></div>
    <div class="tr"><div class="pane"><div class="lab">Said <span class="chip">Argument</span></div><p class="said">${said}</p></div>
      <div class="swap" style="top:calc(50% - 44px)">${swap}</div>
      <div class="pane meant"><div class="lab" style="color:#5b4a9c">Meant <span class="chip">Honest</span></div><p>${meant}</p></div></div>
    <p class="note abs" style="left:64px;bottom:72px;color:#5b4a9c">${note}</p>${count(n, 5)}${badge}`;

  const rw = (n, no, yes, note) => () => `<div class="paper bg-cream" style="position:absolute;inset:0"></div>
    <div class="tophead"><p>Placement season · for parents</p><p class="h s">Before you hit send tonight</p></div>
    <div class="rw"><div class="hd"><i></i><div><b>Family</b><span>Mom, Papa, you</span></div></div>
      <div class="in"><div class="tag no">✕ Instead of</div><p class="draft">${no}</p></div>
      <div class="sent"><div class="tag yes" style="align-self:flex-start;margin:6px 0 14px">✓ Try</div><p class="bub">${yes}</p><span class="tick">Sent · Read</span></div></div>
    <p class="note abs" style="left:64px;bottom:72px;color:#5b4a9c">${note}</p>${count(n, 5)}${badge}`;

  const POSTS = [
    {
      id: "16", slug: "Carousel-Not-About-The-Dishes", kind: "carousel", segment: "Couples and young married professionals",
      date: "Sun 13 Dec 2026", time: "7:30 PM IST", theme: "What couples really fight about",
      line: "You're not fighting about the dishes.",
      why: "Every couple has had the dishes fight. The swipe turns it into a 'translator': what was said on the left, what was meant on the right. People recognise themselves, then send it to their partner. That share is the engagement, and it opens the door to couples counselling without shame.",
      slides: [
        () => `<div class="ph" style="background-image:url(ai/c16-couple.jpg);background-position:50% 60%"></div><div class="scrim-t"></div>
          <div class="abs" style="left:64px;right:180px;top:96px"><span class="eyebrow">For couples</span><p class="h xl light" style="margin-top:26px">You're not fighting about <span class="y">the dishes.</span></p></div>
          <p class="note abs" style="right:64px;bottom:70px;color:#fff;text-align:right">swipe for the translation →</p>${badge}`,
        tr(2, "“You never help around the house.”", "“I'm exhausted, and I feel like I'm doing this alone.”", "(sound familiar?)"),
        tr(3, "“Fine. Do whatever you want.”", "“I want you to choose me without me having to ask.”", "(we've all said it)"),
        tr(4, "“Why are you always on your phone?”", "“I miss you. Even when you're right here.”", "(ouch.)"),
        () => `<div class="paper bg-yellow" style="position:absolute;inset:0"></div>
          <div class="abs" style="left:64px;right:120px;top:190px"><p class="h">Couples counselling isn't for couples who are breaking.</p>
          <p class="h" style="margin-top:34px;color:#5b4a9c">It's for couples who want to stay.</p>
          <div style="margin-top:56px">${CTA}</div></div>
          <p class="note abs" style="left:64px;bottom:150px">send this to your person</p>${arrow("#0d1015", 170, "left:470px;bottom:40px")}${count(5, 5)}${badge}`,
      ],
      caption: "You're not fighting about the dishes. 🍽️\n\nMost fights are a translation problem. “You never help” usually means “I'm tired and I feel alone in this.”\n\nCouples counselling isn't for couples who are breaking. It's for couples who want to stay. YourDOST has certified relationship experts, 24/7.",
      tags: "#Relationships #CouplesTherapy #MarriedLife #Communication #MentalHealthMatters #YourDOST",
      first: "Which translation hit closest to home: 2, 3 or 4? 👇 (Or just send this to your person.)",
      alt: [
        "A couple in a small Indian kitchen at night: she scrubs a pan at a sink full of dishes, he scrolls his phone a few steps away. Text: You're not fighting about the dishes. Swipe for the translation.",
        "A translator card. Said: You never help around the house. Meant: I'm exhausted, and I feel like I'm doing this alone.",
        "A translator card. Said: Fine. Do whatever you want. Meant: I want you to choose me without me having to ask.",
        "A translator card. Said: Why are you always on your phone? Meant: I miss you. Even when you're right here.",
        "Text on yellow: Couples counselling isn't for couples who are breaking. It's for couples who want to stay. Talk to a certified expert, 24/7, yourdost.com. Send this to your person.",
      ],
    },
    {
      id: "17", slug: "Carousel-Placement-Season-Parents", kind: "carousel", segment: "Parents of students at top institutes (IITs, IIMs) during campus placements",
      date: "Tue 1 Dec 2026", time: "7:30 PM IST", theme: "Placement pressure from home",
      line: "The first question after placements shouldn't be “What's the package?”",
      why: "Placement week at top campuses starts on 1 December, and the pressure comes from home as much as from recruiters. The swipe shows parents the exact message to rewrite, so it is useful, not preachy. Students share it into the family group, which is how it reaches parents.",
      slides: [
        () => `<div class="ph" style="background-image:url(ai/c17-placement.jpg);background-position:50% 55%"></div><div class="scrim-t"></div>
          <div class="abs" style="left:64px;right:180px;top:96px"><span class="eyebrow">For parents · Placement season</span><p class="h light" style="margin-top:26px">The first question after placements shouldn't be <span class="y">“What's the package?”</span></p></div>
          <p class="note abs" style="right:64px;bottom:70px;color:#fff;text-align:right">(swipe before you call tonight)</p>${badge}`,
        rw(2, "What's the package?", "How are you holding up?", "(start here)"),
        rw(3, "Your cousin got ₹40 lakh.", "We're proud of you. Whatever the offer.", "(comparison never helped anyone)"),
        rw(4, "Why didn't you get placed on Day 1?", "Have you eaten? Call us when you're free.", "(it's one day out of many)"),
        () => `<div class="paper bg-lav" style="position:absolute;inset:0"></div>
          <div class="abs" style="left:64px;right:120px;top:190px"><p class="h">They cleared the toughest exams in the country to get there.</p>
          <p class="h" style="margin-top:34px;color:#5b4a9c">Home shouldn't feel like another one.</p>
          <p class="body" style="margin-top:40px;max-width:820px">YourDOST experts help students and parents talk through placement stress, confidentially.</p>
          <div style="margin-top:40px">${CTA}</div></div>
          <p class="note abs" style="left:64px;bottom:120px">send this to the family group</p>${arrow("#0d1015", 150, "left:560px;bottom:20px")}${count(5, 5)}${badge}`,
      ],
      caption: "The first question after placements shouldn't be “What's the package?” 💼\n\nPlacement week is hard enough on campus. Home should be the one place it isn't a test.\n\nParents: the words on slides 2 to 4 are small changes that land big. Students: send this to the family group. 💛",
      tags: "#Placements #PlacementSeason #IIT #IIM #StudentMentalHealth #Parenting #YourDOST",
      first: "What's one thing you wish your parents had asked you during placements? 👇",
      alt: [
        "A young man in a formal shirt and loosened tie sits on his hostel bed after placement interviews, phone in hand, staring at the floor. Text: The first question after placements shouldn't be “What's the package?”",
        "A family chat card. Instead of: What's the package? Try: How are you holding up?",
        "A family chat card. Instead of: Your cousin got ₹40 lakh. Try: We're proud of you. Whatever the offer.",
        "A family chat card. Instead of: Why didn't you get placed on Day 1? Try: Have you eaten? Call us when you're free.",
        "Text on lavender: They cleared the toughest exams in the country to get there. Home shouldn't feel like another one. YourDOST experts help students and parents talk. Talk to a certified expert, 24/7, yourdost.com.",
      ],
    },
    {
      id: "18", slug: "Image-Quietly-Leaving", kind: "single", segment: "HR leaders, CHROs and people managers at corporates (B2B)",
      date: "Tue 8 Dec 2026", time: "10:00 AM IST", theme: "Silent burnout and attrition",
      line: "Your best employee isn't quiet. She's quietly updating her résumé.",
      why: "Every HR leader has lost a top performer who never complained. The twist in line two makes them stop scrolling, and the post ends with the B2B ask: confidential support for every employee.",
      slides: [
        () => `<div class="ph" style="background-image:url(ai/i18-office.jpg);background-position:50% 40%"></div><div class="scrim-t"></div>
          <div class="abs" style="left:64px;right:180px;top:96px"><span class="eyebrow">For HR leaders</span><p class="h light" style="margin-top:26px">Your best employee isn't quiet.</p><p class="h light y" style="margin-top:14px">She's quietly updating her résumé.</p></div>
          <div class="abs bg-ink" style="left:0;right:0;bottom:0;padding:34px 64px 40px"><p style="font-size:30px;font-weight:600">Burnout rarely resigns loudly.</p>
          <p style="font-size:26px;color:rgba(255,255,255,0.75);margin-top:6px">YourDOST for teams: confidential support for every employee, 24/7 · <b style="color:#f6d25a">contact@yourdost.com</b></p></div>${badge}`,
      ],
      caption: "Your best employee isn't quiet. She's quietly updating her résumé.\n\nBurnout rarely resigns loudly. By the time it shows up in an exit interview, it's too late to help.\n\nYourDOST gives every employee confidential access to certified experts, 24/7. For teams: contact@yourdost.com",
      tags: "#HR #EmployeeWellbeing #Burnout #Attrition #MentalHealthAtWork #PeopleFirst #YourDOST",
      first: "HR folks: what's the earliest sign of burnout you've learned to spot? 👇",
      alt: ["A professional woman at her office desk, chin on hand, gazing out of a window at the city skyline. Text: Your best employee isn't quiet. She's quietly updating her résumé. Burnout rarely resigns loudly. YourDOST for teams: confidential support for every employee, 24/7."],
    },
    {
      id: "19", slug: "Image-Typed-Deleted-Never-Sent", kind: "single", segment: "Young adults and Gen Z: friendships and loneliness",
      date: "Fri 11 Dec 2026", time: "10:30 PM IST", theme: "Reaching out first",
      line: "Some messages get typed, deleted and never sent.",
      why: "Posted late on a Friday, when people are lying in bed scrolling, like the man in the photo. Everyone has typed and deleted a message, and everyone has a quiet friend. The ask is tiny and doable: text them first. The last line catches the people doing the typing.",
      slides: [
        () => `<div class="ph" style="background-image:url(ai/i19-typing.jpg);background-position:50% 30%"></div><div class="scrim-b"></div>
          <div class="abs" style="left:64px;right:64px;top:620px"><div style="display:inline-flex;align-items:center;gap:14px;background:rgba(255,255,255,0.94);border-radius:999px;padding:16px 30px;font-size:30px;color:#333;box-shadow:0 10px 30px rgba(0,0,0,0.35)">hey, are you okay? i've been<span style="width:3px;height:36px;background:#5b8def;display:inline-block"></span></div>
          <p style="margin-top:14px;font-size:24px;font-weight:600;color:rgba(255,255,255,0.75);letter-spacing:0.04em;text-transform:uppercase">Typed 3 times · Deleted 3 times</p></div>
          <div class="abs" style="left:64px;right:120px;bottom:96px"><p class="h light">Some messages get typed, deleted and never sent.</p><p class="h s light y" style="margin-top:18px">Text your quiet friend first.</p>
          <p style="margin-top:22px;font-size:25px;color:rgba(255,255,255,0.78)">And if you're the one typing: talk to a certified expert, 24/7 · yourdost.com</p></div>${badge}`,
      ],
      caption: "Some messages get typed, deleted and never sent. 📱\n\nIf someone's gone a little quiet lately, don't wait for them to finish typing. Text them first.\n\nAnd if you're the one typing and deleting: you don't have to send it to anyone you know. A YourDOST expert is there, 24/7.",
      tags: "#Friendship #Loneliness #CheckOnYourFriends #GenZ #MentalHealthAwareness #YourDOST",
      first: "Tag the friend you're going to text tonight. 💛",
      alt: ["A young man lies in bed at night, his face lit by his phone, thumbs over the keyboard. A text box reads: hey, are you okay? i've been. Label: Typed 3 times, deleted 3 times. Text: Some messages get typed, deleted and never sent. Text your quiet friend first."],
    },
    {
      id: "20", slug: "Original-Your-2026-Receipt", kind: "single", segment: "Everyone, at year-end (Gen Z and working adults share it most)",
      date: "Thu 31 Dec 2026", time: "6:00 PM IST", theme: "Year-end reflection",
      line: "Your 2026, itemised.",
      why: "An original format: the year as a shop receipt from YourDOST. Every line is something people did this year without counting, and the total, “You made it,” lands as a hug. It's built to be screenshotted and reshared on New Year's Eve, and the comment prompt asks for their own line-1 number.",
      slides: [
        () => `<div class="paper bg-yellow" style="position:absolute;inset:0"></div>
          <p class="h abs" style="left:64px;top:66px;font-size:58px">Your 2026, itemised.</p>
          <div class="rcpt-wrap"><div class="rcpt">
            <div class="c"><img src="brand/badge.png" style="width:92px;height:92px"><br><b class="big">YOURDOST</b><br>Emotional wellness, 24/7</div>
            <div class="hr"></div>
            <div class="row"><span style="flex:1;text-align:left">RECEIPT #2026</span><span>31.12.2026</span></div>
            <div class="row"><span style="flex:1;text-align:left">CUSTOMER: YOU</span><span>11:59 PM</span></div>
            <div class="hr"></div>
            <div class="row"><span>412</span><span>“I'm fine”</span></div>
            <div class="row"><span>96</span><span>Nights overthinking at 2 AM</span></div>
            <div class="row"><span>37</span><span>Plans cancelled, too tired</span></div>
            <div class="row"><span>23</span><span>Sunday-night dreads</span></div>
            <div class="row"><span>∞</span><span>Times you checked on others</span></div>
            <div class="row"><span>?</span><span>Times someone checked on you</span></div>
            <div class="hr"></div>
            <div class="row"><span style="flex:1;text-align:left">SUBTOTAL</span><span>EXHAUSTED</span></div>
            <div class="row"><span style="flex:1;text-align:left">REST YOU SKIPPED</span><span>-0%</span></div>
            <div class="hr"></div>
            <div class="row big"><span style="flex:1;text-align:left">TOTAL</span><span>YOU MADE IT.</span></div>
            <div class="row"><span style="flex:1;text-align:left">PAID WITH</span><span>showing up anyway</span></div>
            <div class="hr"></div>
            <div class="c">Refunds on the past: not available<br>Fresh start: 01.01.2027<br><b>Talk to a certified expert, 24/7</b><br>yourdost.com</div>
            <div class="bar"></div>
            <div class="c" style="letter-spacing:0.12em">THANK YOU FOR STAYING</div>
          </div></div>
          <p class="note abs" style="left:30px;bottom:60px;width:150px;transform:rotate(-6deg)">what's your line 1?</p>${badge}`,
      ],
      caption: "Your 2026, itemised. 🧾\n\nLots of “I'm fine.” Too many 2 AM thoughts. A few cancelled plans. And still: you made it, paid in full with showing up anyway.\n\nIf 2027 needs a fresh start, a YourDOST expert is there, 24/7.",
      tags: "#NewYearsEve #2026Wrapped #YearInReview #SelfCare #MentalHealthMatters #YourDOST",
      first: "What number would be on your line 1 this year? 👇 Be honest.",
      alt: ["A shop-style receipt from YourDOST on yellow, titled Your 2026, itemised. Items: 412 I'm fine; 96 nights overthinking at 2 AM; 37 plans cancelled, too tired; 23 Sunday-night dreads; infinite times you checked on others; question mark times someone checked on you. Subtotal: exhausted. Total: you made it. Paid with: showing up anyway. Fresh start 01.01.2027. Talk to a certified expert, 24/7, yourdost.com. Thank you for staying."],
    },
  ];

  function frame(post, i = 0) { return `<div class="f">${post.slides[i]()}</div>`; }
  root.YD6 = { POSTS, frame };
})(typeof window !== "undefined" ? window : globalThis);
